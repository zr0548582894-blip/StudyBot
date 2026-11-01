"""
ingest.py - בניית מאגר הידע של StudyBot.
שלב א: קריאת כל הקבצים מתיקיית data לרשימה של Document-ים.
שלב ב: חלוקה למקטעים, יצירת Embeddings ושמירה ב-ChromaDB.
מריצים פעם אחת, ושוב רק כשמשנים מסמכים או הגדרות Chunking.
"""

from collections import Counter
from pathlib import Path

# config ראשון: הוא מתקן את ה-SSL לפני שהספריות האחרות נטענות
from config import (DATA_DIR, CHROMA_DIR, COLLECTION_NAME,
                    EMBED_MODEL, CHUNK_SIZE, CHUNK_OVERLAP)

import chromadb
from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from pptx import Presentation
from pypdf import PdfReader


# ===== קוראים לכל סוג קובץ =====
# כל פונקציה מקבלת נתיב לקובץ ומחזירה רשימה של Document-ים.

def load_pptx(path: Path) -> list[Document]:
    """מצגת: Document נפרד לכל שקופית, כדי שנוכל להפנות לשקופית מדויקת.
    מנקה "רעש": שורה שחוזרת בהרבה שקופיות (כותרת תחתונה כמו שם הקורס והמרצה) ומספרי שקופיות."""
    presentation = Presentation(path)

    # שלב 1: אוספים את השורות של כל שקופית
    slides = []
    for slide_num, slide in enumerate(presentation.slides, start=1):
        lines = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                lines += [line.strip() for line in shape.text.splitlines() if line.strip()]
        slides.append((slide_num, lines))

    # שלב 2: שורה שמופיעה ביותר מ-30% מהשקופיות היא כותרת תחתונה, לא תוכן
    line_counts = Counter(line for _, lines in slides for line in set(lines))
    repeated = {line for line, count in line_counts.items() if count > 0.3 * len(slides)}

    # שלב 3: בונים Document רק מהתוכן האמיתי
    docs = []
    for slide_num, lines in slides:
        content = [line for line in lines
                   if line not in repeated and not line.isdigit()]   # isdigit = מספר שקופית
        if content:  # מדלגים על שקופיות בלי טקסט (למשל תמונה בלבד)
            docs.append(Document(text="\n".join(content), metadata={"slide": slide_num}))
    return docs


def load_pdf(path: Path) -> list[Document]:
    """PDF: Document נפרד לכל עמוד."""
    docs = []
    reader = PdfReader(path)
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and text.strip():
            docs.append(Document(text=text, metadata={"page": page_num}))
    return docs


def load_text(path: Path) -> list[Document]:
    """Markdown או טקסט: כל הקובץ הוא Document אחד."""
    text = path.read_text(encoding="utf-8")
    return [Document(text=text)]


# מילון שממפה סיומת קובץ -> הפונקציה שיודעת לקרוא אותה
LOADERS = {
    ".pptx": load_pptx,
    ".pdf": load_pdf,
    ".md": load_text,
    ".txt": load_text,
}


# ===== הפונקציה הראשית =====

def load_documents() -> list[Document]:
    """עוברת על כל הקבצים ב-data, קוראת אותם ומוסיפה Metadata משותף."""
    all_docs = []
    for path in sorted(DATA_DIR.rglob("*")):        # rglob = כולל תתי-תיקיות
        loader = LOADERS.get(path.suffix.lower())
        if loader is None:                           # קובץ שלא נתמך - מדלגים
            continue

        docs = loader(path)
        for doc in docs:
            doc.metadata["file_name"] = path.name
            doc.metadata["course"] = path.parent.name   # שם התיקייה = שם הקורס
        all_docs.extend(docs)
        print(f"  {path.name}: {len(docs)} מסמכים")

    return all_docs


# ===== שלב ב: מקטעים, Embeddings ושמירה =====

def get_embed_model():
    """מודל ה-Embeddings. בהרצה הראשונה הוא יורד מ-HuggingFace (כ-2GB) ונשמר במטמון."""
    return HuggingFaceEmbedding(model_name=EMBED_MODEL)


def build_index(documents: list[Document]) -> VectorStoreIndex:
    """חותכת למקטעים, הופכת לווקטורים ושומרת ב-ChromaDB."""

    # 1. החותך: מחלק לפי משפטים, כך שמקטע לא נגמר באמצע משפט
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    # 2. ChromaDB: מסד ששמור כתיקייה על הדיסק
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    # מוחקים אוסף ישן אם יש, כדי שלא יישארו מקטעים מהרצה קודמת
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)
    collection = client.create_collection(
        COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},   # מדד המרחק: דמיון קוסינוס
    )

    # 3. מחברים את Chroma ל-LlamaIndex
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. כאן קורה הכול: חיתוך -> Embedding לכל מקטע -> שמירה
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=get_embed_model(),
        transformations=[splitter],
        show_progress=True,
    )

    print(f"\nנשמרו {collection.count()} מקטעים ב-ChromaDB ({CHROMA_DIR})")
    return index


# ===== הרצה ישירה =====
if __name__ == "__main__":
    print("שלב א: קורא מסמכים מתוך", DATA_DIR)
    documents = load_documents()
    print(f"סה\"כ: {len(documents)} מסמכים")

    print("\nשלב ב: חיתוך, Embeddings ושמירה (בפעם הראשונה ייקח כמה דקות)")
    build_index(documents)
