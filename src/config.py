"""
config.py - כל ההגדרות של StudyBot במקום אחד.
כשרוצים לשפר או לנסות משהו (מודל אחר, גודל Chunk אחר) - משנים רק כאן.
"""

import os
from pathlib import Path

# ===== 0. תיקון SSL (חייב לרוץ לפני כל פנייה לאינטרנט) =====
# NetFree מחליף את אישורי האבטחה של אתרים באישור משלו.
# Python 3.13 בודק אישורים בקפדנות ודוחה אותו, ולכן ההורדה מ-HuggingFace נכשלה.
# truststore גורם ל-Python לסמוך על מאגר האישורים של Windows, שבו האישור של NetFree כבר מותקן.
import truststore
truststore.inject_into_ssl()

from dotenv import load_dotenv

# ===== 1. נתיבים =====
# BASE_DIR = תיקיית הפרויקט (תיקייה אחת מעל src)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"          # המסמכים שהמערכת לומדת מהם
CHROMA_DIR = BASE_DIR / "chroma_db"   # כאן ChromaDB ישמור את הווקטורים
COLLECTION_NAME = "studybot"          # שם "הטבלה" בתוך ChromaDB

# ===== 2. מפתח API =====
# load_dotenv קוראת את קובץ .env ומכניסה את מה שבו למשתני הסביבה
load_dotenv(BASE_DIR / ".env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ===== 3. מודלים =====
LLM_MODEL = "gemini-3.8-flash"        # מודל השפה שמנסח את התשובה
# מודלי גיבוי, לפי הסדר. לכל מודל יש מכסה יומית נפרדת בשכבה החינמית,
# כך שכשהמכסה של מודל אחד נגמרת (שגיאת 429) - עוברים לבא בתור
# (השמות נלקחו מהרשימה ש-list_models.py הציג - מודלים שקיימים בחשבון)
FALLBACK_LLM_MODELS = ["gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]
LLM_RETRIES = 3                       # כמה פעמים לנסות שוב מודל עמוס (503) לפני שעוברים לבא
EMBED_MODEL = "BAAI/bge-m3"           # מודל Embeddings רב-לשוני (עברית + אנגלית)
# כמה Gemini "חושב" לפני שהוא עונה. LOW = הרמה הנמוכה ביותר ש-gemini-3.8-flash תומך בה
# (MINIMAL נדחה עם שגיאה 400). מספיק לתשובות מתוך חומר שכבר נשלף.
THINKING_LEVEL = "LOW"

# המודל bge-m3 שמור ב-HuggingFace בפורמט הישן (pytorch_model.bin).
# אחרי שהוא נטען, transformers מנסה להוריד גם גרסת safetensors שלו - עוד 2.27GB מיותרים.
# המשתנה הזה מבטל את ההורדה הנוספת.
os.environ.setdefault("DISABLE_SAFETENSORS_CONVERSION", "1")

# ===== 4. חלוקה למקטעים (Chunking) =====
CHUNK_SIZE = 512       # גודל כל מקטע, בטוקנים
CHUNK_OVERLAP = 50     # כמה טוקנים חוזרים בין מקטע למקטע, כדי לא לחתוך רעיון באמצע

# ===== 5. אחזור (Retrieval) =====
TOP_K = 4              # כמה מקטעים לשלוף לכל שאלה
# מקטע עם ציון נמוך מזה לא נשלח ל-LLM. רק "מסננת גסה": את המקורות הלא רלוונטיים מסנן Gemini עצמו (שורת SOURCES).
# 0.6 היה גבוה מדי - חסם שאלות בעברית על שקופיות באנגלית (למשל "מה זה רשת נוירונים?")
SIMILARITY_CUTOFF = 0.45

# ===== 6. שיחה =====
MAX_HISTORY_MESSAGES = 6   # כמה הודעות קודמות לשלוח ל-LLM כהקשר
NO_ANSWER = "לא מצאתי את התשובה בחומר הלימוד."


def check_config():
    """בדיקה מהירה שהכול מוכן לפני שמתחילים."""
    if not GOOGLE_API_KEY:
        raise ValueError("לא נמצא GOOGLE_API_KEY. ודאי שהדבקת את המפתח בקובץ .env ושמרת.")
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"תיקיית הנתונים לא נמצאה: {DATA_DIR}")
    print("ההגדרות תקינות ✓")
