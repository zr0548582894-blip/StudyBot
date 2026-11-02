"""
ui_style.py - העיצוב של StudyBot: "מחברת פתוחה על שולחן".

הרעיון: האפליקציה היא מחברת אמיתית בתלת-ממד -
דף עם שורות וקו שוליים, טבעות ספירלה מימין, ערימת דפים מתחת, לשוניות צבעוניות שבולטות מהצד,
ופתקיות דביקות עם סלוטייפ. בטעינה המחברת "נפתחת" (סיבוב תלת-ממדי סביב הטבעות).

לכל נושא צבע מרקר משלו, והוא חוזר בלשונית, בפתקית השאלה ובפתקית המקור - הצבע נושא מידע.
הגופנים נטענים מקומית מ-src/static/fonts, כך שהם עובדים גם בלי Google Fonts (ו-NetFree).
"""

import html
from pathlib import Path

# צבע מרקר לכל נושא. המפתח הוא מילה שמופיעה בשם הקובץ
SUBJECT_COLORS = {
    "python": "#FFEE7A",      # צהוב
    "java_": "#FFB8CB",       # ורוד (java_oop - לא javascript)
    "javascript": "#FFD2A6",  # אפרסק
    "sql": "#AEEFD3",         # מנטה
    "lecture": "#D9CCFF",     # לילך - מצגות AI
    "comparison": "#C2E2FF",  # תכלת - השוואת שפות
}
DEFAULT_COLOR = "#E6E3EE"

SUBJECTS = [  # (שם בלשונית, צבע) - הסדר של הלשוניות בצד המחברת
    ("AI", "#D9CCFF"), ("Python", "#FFEE7A"), ("Java", "#FFB8CB"),
    ("JS", "#FFD2A6"), ("SQL", "#AEEFD3"),
]


def subject_color(file_name: str) -> str:
    name = file_name.lower()
    for key, color in SUBJECT_COLORS.items():
        if key in name:
            return color
    return DEFAULT_COLOR


# כל ה-CSS נמצא בקובץ נפרד, style.css. כאן רק טוענים אותו ועוטפים בתגית <style>
CSS = "<style>" + Path(__file__).with_name("style.css").read_text(encoding="utf-8") + "</style>"


def hero_html() -> str:
    tabs = "".join(f'<span style="--c:{c}">{n}</span>' for n, c in SUBJECTS)
    doodle = (   # חץ מצויר ביד, שמצביע למטה אל הפתקיות
        '<div class="sb-start"><span class="sb-start-text">אפשר להתחיל מכאן</span>'
        '<svg class="sb-doodle" viewBox="0 0 70 64" aria-hidden="true">'
        '<path d="M64 8 C 40 2, 18 14, 22 36 C 23 44, 26 50, 30 58"/>'
        '<path d="M20 50 L30 59 L38 48"/></svg></div>'
    )
    return (
        f'<div class="sb-tabs" aria-hidden="true">{tabs}</div>'
        '<div class="sb-hero">'
        '<div class="sb-logo">StudyBot<span class="mark"></span></div>'
        '<p class="sb-tagline">שואלים על חומר הקורס, ומקבלים תשובה עם השקופית או העמוד שממנו היא נלקחה</p>'
        f'{doodle}</div>'
    )


def prompt_html() -> str:
    return '<div class="sb-prompt"></div>'


def sidebar_stats_html(chunks: int, model: str) -> str:
    return (
        '<div class="sb-side-title">StudyBot</div>'
        f'<div class="sb-stat">{chunks}</div><div class="sb-stat-label">מקטעים במאגר הידע</div>'
        '<div class="sb-stat">5</div><div class="sb-stat-label">נושאי לימוד</div>'
        f'<div class="sb-stack">מודל שפה: {html.escape(model)}<br>Embeddings: bge-m3<br>LlamaIndex + ChromaDB</div>'
    )


def sources_html(documents: list[dict]) -> str:
    """כל המקורות כשורה של פתקיות דביקות, בצבע הנושא, עם מד דמיון."""
    tilts = ["-2deg", "1.5deg", "-1deg", "2deg"]
    notes = []
    for i, doc in enumerate(documents):
        color = subject_color(doc["source"])
        location = f'<div class="sb-note-loc">{html.escape(doc["location"])}</div>' if doc["location"] else ""
        width = max(0, min(100, round(doc["score"] * 100)))
        # קטע נקי: בלי ירידות שורה וסימני Markdown (```, #), שאחרת "שוברים" את ה-HTML של הפתקית
        snippet = " ".join(doc["text"].replace("`", "").replace("#", "").split())
        text = html.escape(snippet[:150]) + "..."
        notes.append(
            f'<div class="sb-note" style="--tab:{color};--tilt:{tilts[i % 4]}">'
            f'<div class="sb-note-title">{html.escape(doc["source"])}</div>{location}'
            f'<div class="sb-meter"><i style="--w:{width}%"></i>{doc["score"]:.2f}</div>'
            f'<div class="sb-note-text">{text}</div></div>'
        )
    return f'<div class="sb-notes">{"".join(notes)}</div>'


def user_marker() -> str:
    """סימון נסתר בתוך הודעת המשתמש - כדי שה-CSS יציג אותה בכתב יד."""
    return '<span class="sb-user"></span>'


def bot_marker() -> str:
    """סימון נסתר בתוך תשובת הבוט - כדי שה-CSS יציג אותה ככרטיס עם אטב."""
    return '<span class="sb-bot"></span>'
