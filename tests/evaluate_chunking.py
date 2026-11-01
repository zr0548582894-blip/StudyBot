"""
evaluate_chunking.py - בונוס: השוואה בין שתי אסטרטגיות Chunking.

לכל אסטרטגיה בונים אינדקס בזיכרון (בלי לגעת ב-chroma_db), שואלים 15 שאלות
שהתשובה הנכונה שלהן ידועה מראש (eval_questions.json), ומודדים:
  Hit@1  - כמה פעמים המקטע הראשון שנשלף הוא מהמקור הנכון
  Hit@4  - כמה פעמים המקור הנכון נמצא בין 4 המקטעים שנשלפו (מה שנשלח ל-LLM)
  MRR    - ממוצע של 1/המיקום של המקור הנכון (1 = תמיד ראשון, 0 = אף פעם)
  הקשר   - כמה מילים נשלחות ל-LLM בממוצע (קירוב לעלות בטוקנים)
ההשוואה לא משתמשת ב-Gemini בכלל - רק ב-Embeddings המקומיים, ולכן לא צורכת מכסה.

הרצה מתיקיית הפרויקט:   .venv\\Scripts\\python.exe tests\\evaluate_chunking.py
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import TOP_K   # ראשון: גם מתקן SSL ומגדיר את מצב ההורדה

from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from ingest import get_embed_model, load_documents

# שתי האסטרטגיות שמשווים: מקטעים גדולים (מה שהמערכת משתמשת בו) מול מקטעים קטנים
STRATEGIES = {
    "A - מקטעים גדולים (512/50)": SentenceSplitter(chunk_size=512, chunk_overlap=50),
    "B - מקטעים קטנים (128/20)": SentenceSplitter(chunk_size=128, chunk_overlap=20),
}

QUESTIONS = json.loads((Path(__file__).parent / "eval_questions.json").read_text(encoding="utf-8"))


def is_correct(node, expected):
    """המקטע נכון אם הוא מהקובץ הצפוי, ואם צוינו שקופיות/עמודים - מאחד מהם."""
    meta = node.metadata
    if meta.get("file_name") != expected["file"]:
        return False
    if not expected["loc"]:
        return True
    return (meta.get("slide") or meta.get("page")) in expected["loc"]


def evaluate(name, splitter, documents, embed_model):
    start = time.time()
    nodes = splitter.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes, embed_model=embed_model, show_progress=True)
    retriever = index.as_retriever(similarity_top_k=TOP_K)

    hits1 = hits4 = 0
    reciprocal_ranks, context_words = [], []
    misses = []
    for item in QUESTIONS:
        results = retriever.retrieve(item["q"])
        ranks = [i for i, r in enumerate(results, start=1) if is_correct(r.node, item)]
        if ranks and ranks[0] == 1:
            hits1 += 1
        if ranks:
            hits4 += 1
        else:   # שומרים גם מה כן נשלף, כדי להבין למה המקור הנכון פוספס
            got = ", ".join(f"{r.node.metadata.get('file_name')}:{r.node.metadata.get('slide') or r.node.metadata.get('page') or '-'}"
                            for r in results)
            misses.append(f"{item['q']} (נשלף: {got})")
        reciprocal_ranks.append(1 / ranks[0] if ranks else 0)
        context_words.append(sum(len(r.node.get_content().split()) for r in results))

    n = len(QUESTIONS)
    return {
        "name": name,
        "chunks": len(nodes),
        "avg_words": round(sum(len(x.get_content().split()) for x in nodes) / len(nodes)),
        "hit1": f"{hits1}/{n} ({hits1 / n:.0%})",
        "hit4": f"{hits4}/{n} ({hits4 / n:.0%})",
        "mrr": f"{sum(reciprocal_ranks) / n:.2f}",
        "context": round(sum(context_words) / n),
        "seconds": round(time.time() - start),
        "misses": misses,
    }


if __name__ == "__main__":
    print("קורא מסמכים...")
    documents = load_documents()
    embed_model = get_embed_model()

    results = []
    for name, splitter in STRATEGIES.items():
        print(f"\n=== {name} ===")
        results.append(evaluate(name, splitter, documents, embed_model))

    lines = [
        "| אסטרטגיה | מקטעים | מילים למקטע | Hit@1 | Hit@4 | MRR | מילים שנשלחות ל-LLM | זמן בנייה (שניות) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in results:
        lines.append(f"| {r['name']} | {r['chunks']} | {r['avg_words']} | {r['hit1']} | {r['hit4']} "
                     f"| {r['mrr']} | {r['context']} | {r['seconds']} |")
    for r in results:
        if r["misses"]:
            lines.append(f"\n**{r['name']} - שאלות שהמקור הנכון לא נמצא בהן:** " + "; ".join(r["misses"]))

    report = "\n".join(lines)
    print("\n" + report)
    out = Path(__file__).parent / "chunking_results.md"
    out.write_text("# השוואת אסטרטגיות Chunking\n\n" + report + "\n", encoding="utf-8")
    print(f"\nהתוצאות נשמרו ב-{out}")
