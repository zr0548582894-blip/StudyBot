"""
list_models.py - כלי עזר: מציג את מודלי Gemini שהמפתח שלך יכול להשתמש בהם.
שימושי כדי לבחור שמות נכונים ל-LLM_MODEL ול-FALLBACK_LLM_MODELS ב-config.py.
הרצה מתיקיית הפרויקט:   .venv\\Scripts\\python.exe src\\list_models.py
(רשימת המודלים לא נחשבת כבקשה מהמכסה היומית)
"""

from config import GOOGLE_API_KEY   # ראשון: גם מתקן SSL

from google import genai

client = genai.Client(api_key=GOOGLE_API_KEY)
print("מודלים שיודעים לייצר טקסט:\n")
for model in client.models.list():
    actions = model.supported_actions or []
    if "generateContent" in actions and "gemini" in model.name:
        print("  ", model.name.replace("models/", ""))
