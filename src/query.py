"""
query.py - שאלה ותשובה מול מאגר הידע של StudyBot.
1. פותחים את המאגר הקיים ב-ChromaDB (נבנה ב-ingest.py)
2. שולפים את המקטעים הכי קרובים לשאלה (Retrieval)
3. שולחים אותם ל-Gemini עם הוראה לענות רק מתוכם (Generation)
4. מחזירים את התשובה יחד עם המקורות
"""

# config ראשון: תיקון SSL ומשתני סביבה לפני שהספריות נטענות
from config import (CHROMA_DIR, COLLECTION_NAME, EMBED_MODEL,
                    LLM_MODEL, GOOGLE_API_KEY, TOP_K, check_config)

import chromadb
from llama_index.core import PromptTemplate, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.chroma import ChromaVectorStore


# ===== 1. הפרומפט =====
# {context_str} = המקטעים שנשלפו, {query_str} = השאלה. LlamaIndex ממלאת אותם.
QA_PROMPT = PromptTemplate(
    "את StudyBot, עוזרת לימוד. עני על השאלה רק על סמך המידע שבחומר הלימוד שלמטה.\n"
    "אם התשובה לא נמצאת בחומר, כתבי בדיוק: \"לא מצאתי את התשובה בחומר הלימוד.\"\n"
    "אל תשתמשי בידע כללי מחוץ לחומר. עני בשפה שבה נשאלה השאלה, בקצרה ובבהירות.\n"
    "\n"
    "חומר הלימוד:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "שאלה: {query_str}\n"
    "תשובה:"
)


# ===== 2. בניית מנוע השאלות =====
def build_query_engine():
    """פותחת את המאגר ומחברת אליו את מודל ה-Embeddings ואת Gemini."""
    check_config()

    # אותו מודל Embeddings כמו ב-ingest - חובה! אחרת השאלה והמקטעים
    # יהיו וקטורים ב"מרחבים" שונים, והחיפוש לא יעבוד
    embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)

    # temperature נמוך = תשובות עקביות וצמודות לחומר, פחות "יצירתיות"
    llm = GoogleGenAI(model=LLM_MODEL, api_key=GOOGLE_API_KEY, temperature=0.1)

    # פותחים את האוסף הקיים (לא יוצרים מחדש!)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    # query engine = Retriever (שולף TOP_K מקטעים) + LLM (מנסח תשובה)
    return index.as_query_engine(
        llm=llm,
        similarity_top_k=TOP_K,
        text_qa_template=QA_PROMPT,
    )


# ===== 3. הצגת מקורות =====
def format_sources(response) -> list[str]:
    """הופכת את המקטעים שנשלפו לשורות קריאות: קובץ, שקופית/עמוד, ציון דמיון."""
    lines = []
    for node in response.source_nodes:
        meta = node.metadata
        location = ""
        if "slide" in meta:
            location = f", שקופית {meta['slide']}"
        elif "page" in meta:
            location = f", עמוד {meta['page']}"
        snippet = node.get_content()[:120].replace("\n", " ")
        lines.append(f"{meta.get('file_name')}{location}  (דמיון: {node.score:.2f})\n      \"{snippet}...\"")
    return lines


# ===== הרצה ישירה: שאלות מהטרמינל =====
if __name__ == "__main__":
    print("טוען את StudyBot...")
    engine = build_query_engine()
    print("מוכן! כתבי שאלה (או 'יציאה' לסיום)\n")

    while True:
        question = input("שאלה: ").strip()
        if question in ("יציאה", "exit", ""):
            break

        response = engine.query(question)
        print("\nתשובה:", response.response)
        print("\nמקורות:")
        for i, line in enumerate(format_sources(response), start=1):
            print(f"  {i}. {line}")
        print("\n" + "=" * 60 + "\n")
