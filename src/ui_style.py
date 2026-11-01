"""
ui_style.py - העיצוב של StudyBot: "מחברת פתוחה על שולחן".

הרעיון: האפליקציה היא מחברת אמיתית בתלת-ממד -
דף עם שורות וקו שוליים, טבעות ספירלה מימין, ערימת דפים מתחת, לשוניות צבעוניות שבולטות מהצד,
ופתקיות דביקות עם סלוטייפ. בטעינה המחברת "נפתחת" (סיבוב תלת-ממדי סביב הטבעות).

לכל נושא צבע מרקר משלו, והוא חוזר בלשונית, בפתקית השאלה ובפתקית המקור - הצבע נושא מידע.
הגופנים נטענים מקומית מ-src/static/fonts, כך שהם עובדים גם בלי Google Fonts (ו-NetFree).
"""

import html

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


_FONTS = "".join(
    f"@font-face {{ font-family: '{fam}'; src: url('/app/static/fonts/{file}.woff2') format('woff2');"
    f" font-weight: {w}; font-display: swap; {rng} }}\n"
    for fam, file, w, rng in [
        ("Gveret Levin", "gveret-levin-hebrew-400-normal", 400, "unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;"),
        ("Gveret Levin", "gveret-levin-latin-400-normal", 400, ""),
        ("Rubik", "rubik-hebrew-400-normal", 400, "unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;"),
        ("Rubik", "rubik-latin-400-normal", 400, ""),
        ("Rubik", "rubik-hebrew-500-normal", 500, "unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;"),
        ("Rubik", "rubik-latin-500-normal", 500, ""),
        ("Rubik", "rubik-hebrew-700-normal", 700, "unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;"),
        ("Rubik", "rubik-latin-700-normal", 700, ""),
        ("Caveat", "caveat-latin-700-normal", 700, ""),
        ("Frank Ruhl Libre", "frank-ruhl-libre-hebrew-400-normal", 400, "unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;"),
        ("Frank Ruhl Libre", "frank-ruhl-libre-latin-400-normal", 400, ""),
        ("Frank Ruhl Libre", "frank-ruhl-libre-hebrew-500-normal", 500, "unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;"),
        ("Frank Ruhl Libre", "frank-ruhl-libre-latin-500-normal", 500, ""),
        ("Frank Ruhl Libre", "frank-ruhl-libre-hebrew-700-normal", 700, "unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;"),
        ("Frank Ruhl Libre", "frank-ruhl-libre-latin-700-normal", 700, ""),
    ]
)

# מרקם נייר עדין (רעש) כ-SVG בתוך ה-CSS
_NOISE = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'>"
          "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/>"
          "<feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .05 0'/></filter>"
          "<rect width='100%' height='100%' filter='url(%23n)'/></svg>\")")

CSS = "<style>\n" + _FONTS + """
:root {
    --desk: #ECE9F3;
    --paper: #FFFEFB;
    --rule: #DCE6F5;
    --margin: #F3B0B0;
    --ink: #1E2B4F;
    --ink-blue: #2F4A9A;
    --pencil: #6B7290;
    --line-h: 34px;
}

/* ---------- בסיס ---------- */
html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebarUserContent"] {
    direction: rtl; font-family: 'Rubik', sans-serif; color: var(--ink);
}
/* כשסוגרים את סרגל הצד - מסתירים את התוכן שלו, כדי שלא יישארו מילים בקצה המסך */
[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarContent"] { visibility: hidden; }
pre, code { direction: ltr; text-align: left; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li { unicode-bidi: plaintext; text-align: start; line-height: 1.75; }

/* ---------- השולחן ---------- */
[data-testid="stApp"] {
    background:
        radial-gradient(70% 55% at 50% 0%, rgba(255,255,255,0.85), transparent 70%),
        """ + _NOISE + """,
        var(--desk);
}
[data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stBottom"], [data-testid="stBottom"] > div { background: transparent !important; }

/* ---------- הדף: מחברת בתלת-ממד ---------- */
[data-testid="stMainBlockContainer"] {
    position: relative;
    max-width: 780px;
    margin: 2.2rem auto 9rem;
    padding: 2.6rem 3.4rem 2.6rem 2.4rem !important;
    background:
        linear-gradient(to left, transparent 54px, var(--margin) 54px, var(--margin) 56px, transparent 56px),
        repeating-linear-gradient(to bottom, transparent 0 calc(var(--line-h) - 1px), var(--rule) calc(var(--line-h) - 1px) var(--line-h)),
        """ + _NOISE + """,
        var(--paper);
    background-position: 0 0, 0 18px, 0 0, 0 0;
    border-radius: 8px 4px 4px 8px;
    /* ערימת דפים מתחת לדף העליון + צל רך על השולחן */
    box-shadow:
        -5px 5px 0 -1px #F8F6F0, -5px 5px 0 0 #DAD5E3,
        -10px 10px 0 -1px #F4F1EA, -10px 10px 0 0 #D2CCDD,
        -15px 15px 0 -1px #EFEBE3, -15px 15px 0 0 #C9C2D6,
        -30px 40px 60px -20px rgba(47, 35, 100, 0.35);
    transform-origin: right center;
    animation: open-notebook 1.1s cubic-bezier(.16,.84,.3,1) both;
}
@keyframes open-notebook {
    from { transform: perspective(1800px) rotateY(-32deg) translateX(-30px); opacity: 0; }
    to   { transform: perspective(1800px) rotateY(0) translateX(0); opacity: 1; }
}
/* טבעות ספירלה מתכתיות בצד ימין */
[data-testid="stMainBlockContainer"]::before {
    content: ""; position: absolute; top: 26px; bottom: 26px; right: -15px; width: 30px;
    background: linear-gradient(90deg, #6F7590, #F6F7FC 42%, #C3C7D8 58%, #6A7088);
    -webkit-mask: repeating-linear-gradient(to bottom, #000 0 8px, transparent 8px 28px);
            mask: repeating-linear-gradient(to bottom, #000 0 8px, transparent 8px 28px);
    border-radius: 10px;
    filter: drop-shadow(-2px 2px 1px rgba(30,30,60,0.35));
    z-index: 3;
}
/* חורי הטבעות בדף */
[data-testid="stMainBlockContainer"]::after {
    content: ""; position: absolute; top: 26px; bottom: 26px; right: 10px; width: 12px;
    background: radial-gradient(circle at 50% 4px, #CFCADB 4px, transparent 5px) 0 0 / 12px 28px repeat-y;
    z-index: 2;
}

/* ---------- לשוניות נושא שבולטות מהצד השמאלי ---------- */
.sb-tabs { position: absolute; left: calc(-2.4rem - 44px); top: 40px; display: flex; flex-direction: column; gap: 8px; z-index: 0; }
.sb-tabs span {
    display: block; width: 44px; padding: 14px 0; text-align: center;
    background: linear-gradient(90deg, color-mix(in srgb, var(--c) 70%, #000 6%), var(--c) 40%);
    border-radius: 10px 0 0 10px;
    font-family: 'Caveat', 'Gveret Levin', cursive; font-weight: 700; font-size: 1.15rem; color: var(--ink);
    writing-mode: vertical-rl; transform: rotate(180deg);
    box-shadow: -3px 3px 6px -2px rgba(40,30,90,0.25);
    animation: tab-in .5s cubic-bezier(.2,.9,.3,1.3) both;
}
.sb-tabs span:nth-child(1) { animation-delay: .9s; } .sb-tabs span:nth-child(2) { animation-delay: 1s; }
.sb-tabs span:nth-child(3) { animation-delay: 1.1s; } .sb-tabs span:nth-child(4) { animation-delay: 1.2s; }
.sb-tabs span:nth-child(5) { animation-delay: 1.3s; }
@keyframes tab-in { from { transform: rotate(180deg) translateY(-30px); opacity: 0; } to { transform: rotate(180deg) translateY(0); opacity: 1; } }

/* ---------- כותרת בכתב יד עם מרקר ---------- */
.sb-hero { position: relative; padding: 0.3rem 0 0.6rem; }
.sb-logo {
    font-family: 'Caveat', cursive; font-weight: 700; font-size: 5.6rem; line-height: 0.95;
    color: var(--ink); direction: ltr; display: inline-block; position: relative; z-index: 0;
    transform: rotate(-2deg);
}
.sb-logo .mark {
    position: absolute; z-index: -1; left: -10px; right: -14px; bottom: 0.12em; height: 0.38em;
    background: #FFEE7A; border-radius: 40% 10% 35% 12% / 60% 30% 70% 40%;
    transform-origin: left; transform: skewX(-12deg);
    animation: swipe .8s 1s cubic-bezier(.6,.1,.2,1) both;
}
@keyframes swipe { from { transform: skewX(-12deg) scaleX(0); } to { transform: skewX(-12deg) scaleX(1); } }
.sb-tagline {
    font-family: 'Gveret Levin', 'Rubik', sans-serif; font-size: 1.65rem; line-height: 1.35;
    color: var(--ink-blue); margin: 0.6rem 0 0; max-width: 24ch;
}
/* חץ מצויר ביד שמצביע על הפתקיות - "נכתב" באנימציה */
.sb-start { display: flex; justify-content: flex-end; align-items: flex-end; gap: 4px; margin-top: 0.4rem; height: 64px; }
.sb-start-text { font-family: 'Gveret Levin', cursive; font-size: 1.35rem; color: var(--ink-blue); opacity: 0; animation: fade .4s 2.3s forwards; margin-bottom: 26px; }
.sb-doodle { width: 70px; height: 64px; }
.sb-doodle path { fill: none; stroke: var(--ink-blue); stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round;
    stroke-dasharray: 260; stroke-dashoffset: 260; animation: draw 1s 1.6s ease-out forwards; }

@keyframes draw { to { stroke-dashoffset: 0; } }
@keyframes fade { to { opacity: 1; } }

/* ---------- פתקיות שאלה (כפתורים) ---------- */
.sb-prompt { height: 1.2rem; margin: 0; }
div[class*="st-key-ex_"] { perspective: 900px; }
div[class*="st-key-ex_"] button {
    position: relative; width: 100%; min-height: 128px;
    display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-start;
    text-align: right; padding: 1.4rem 1.1rem 1rem;
    background: linear-gradient(170deg, color-mix(in srgb, var(--tab) 60%, #fff) 0%, var(--tab) 100%);
    border: none; border-radius: 2px 2px 2px 18px / 2px 2px 2px 26px;   /* פינה מתקפלת */
    color: var(--ink);
    box-shadow: 0 1px 1px rgba(0,0,0,0.06), 0 12px 18px -10px rgba(50,35,110,0.45);
    transform: rotate(var(--tilt));
    transition: transform .35s cubic-bezier(.2,.9,.3,1.2), box-shadow .35s ease;
}
div[class*="st-key-ex_"] button::after {   /* סלוטייפ */
    content: ""; position: absolute; top: -10px; left: 50%; width: 74px; height: 22px; margin-left: -37px;
    background: rgba(255,255,255,0.55); border: 1px solid rgba(255,255,255,0.7);
    box-shadow: 0 1px 2px rgba(0,0,0,0.08); transform: rotate(-4deg);
}
div[class*="st-key-ex_"] button::before {
    content: var(--label); font-family: 'Caveat', 'Gveret Levin', cursive; font-weight: 700;
    font-size: 1.35rem; line-height: 1; margin-bottom: 8px; color: rgba(30,43,79,0.7); white-space: nowrap;
}
div[class*="st-key-ex_"] button div { white-space: normal; overflow: visible; max-width: 100%; }
div[class*="st-key-ex_"] button p {
    font-size: 1.04rem; font-weight: 500; line-height: 1.45; color: var(--ink);
    unicode-bidi: plaintext; text-align: start; white-space: normal;
}
div[class*="st-key-ex_"] button:hover {
    transform: rotate(0deg) translateY(-8px) rotateX(10deg) scale(1.03);
    box-shadow: 0 2px 2px rgba(0,0,0,0.05), 0 26px 30px -14px rgba(50,35,110,0.5);
    color: var(--ink);
}
div[class*="st-key-ex_"] button:focus-visible { outline: 3px solid var(--ink-blue); outline-offset: 4px; }
.st-key-ex_python { --tab: #FFEE7A; --label: "Python"; --tilt: -2deg; }
.st-key-ex_ai     { --tab: #D9CCFF; --label: "AI"; --tilt: 1.6deg; }
.st-key-ex_sql    { --tab: #AEEFD3; --label: "SQL"; --tilt: 1.2deg; }
.st-key-ex_java   { --tab: #FFB8CB; --label: "Java"; --tilt: -1.4deg; }

/* ---------- צ'אט ---------- */
[data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessage"] [data-testid*="Avatar"] { display: none; }
[data-testid="stChatMessage"] { background: transparent; padding: 0.4rem 0; gap: 0; direction: rtl; }
[data-testid="stChatMessage"] > div { width: 100%; }
[data-testid="stChatMessage"]:has(.sb-user) [data-testid="stMarkdownContainer"] { text-align: right; }
/* השאלה שלי: כתב יד בדיו כחולה, עם קו מרקר מתחת */
[data-testid="stChatMessage"]:has(.sb-user) p {
    font-family: 'Gveret Levin', 'Rubik', sans-serif; font-size: 1.75rem; line-height: 1.3; color: var(--ink-blue);
}
[data-testid="stChatMessage"]:has(.sb-user) .stMarkdown:last-child p {
    display: inline; background: linear-gradient(transparent 62%, rgba(255,238,122,0.85) 62%);
}
/* התשובה: כרטיס מודפס שמהודק לדף עם אטב */
[data-testid="stChatMessage"]:has(.sb-bot) {
    position: relative; background: #FFFFFF; padding: 1.4rem 1.4rem 1rem;
    border-radius: 4px; margin: 1.6rem 0 1.4rem;
    box-shadow: 0 1px 2px rgba(0,0,0,0.06), 0 14px 26px -16px rgba(50,35,110,0.45);
    animation: card-in .5s cubic-bezier(.2,.9,.3,1.1) both;
}
@keyframes card-in { from { opacity: 0; transform: translateY(14px) rotate(-1deg); } to { opacity: 1; transform: none; } }
[data-testid="stChatMessage"]:has(.sb-bot)::before {   /* אטב מתכתי */
    content: ""; position: absolute; top: -14px; left: 28px; width: 16px; height: 46px;
    border: 3px solid #9AA0B8; border-radius: 10px; border-bottom-color: #B5BACB;
    transform: rotate(8deg); box-shadow: inset 0 0 0 4px transparent;
}
[data-testid="stChatMessage"]:has(.sb-bot)::after {
    content: ""; position: absolute; top: -6px; left: 33px; width: 8px; height: 30px;
    border: 3px solid #9AA0B8; border-top: none; border-radius: 0 0 8px 8px; transform: rotate(8deg);
}
/* התשובה: גופן "מודפס" של ספר - מתאים לכרטיס המודפס ונוח לקריאה ארוכה */
[data-testid="stChatMessage"]:has(.sb-bot) p, [data-testid="stChatMessage"]:has(.sb-bot) li {
    font-family: 'Frank Ruhl Libre', serif; font-size: 1.14rem; line-height: 1.85; color: #1B2440;
}
[data-testid="stChatMessage"]:has(.sb-bot) [data-testid="stExpander"] summary p {
    font-family: 'Gveret Levin', 'Rubik', sans-serif; font-size: 1.4rem; color: var(--ink-blue);
}
[data-testid="stChatMessage"]:has(.sb-bot) strong { font-weight: 700; background: linear-gradient(transparent 60%, rgba(255,238,122,0.7) 60%); }
[data-testid="stChatMessage"] pre { background: #F6F7FB !important; border-radius: 8px; border: 1px solid #E6E8F2; }

/* ---------- מקורות: פתקיות קטנות בשורה ---------- */
[data-testid="stExpander"] details { border: none; background: transparent; }
[data-testid="stExpander"] summary { background: transparent !important; padding-right: 0; border: none; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary p { font-family: 'Gveret Levin', 'Rubik', sans-serif; font-size: 1.4rem; color: var(--ink-blue); }
[data-testid="stExpander"] details > div { border: none; }
.sb-notes { display: flex; flex-wrap: wrap; gap: 18px 14px; padding: 12px 2px 6px; }
.sb-note {
    position: relative; flex: 1 1 200px; max-width: 260px; padding: 1rem 0.9rem 0.8rem;
    background: linear-gradient(170deg, color-mix(in srgb, var(--tab) 55%, #fff), var(--tab));
    border-radius: 2px 2px 2px 14px / 2px 2px 2px 20px;
    box-shadow: 0 10px 14px -10px rgba(50,35,110,0.45);
    transform: rotate(var(--tilt, 0deg));
    transition: transform .3s cubic-bezier(.2,.9,.3,1.2);
}
.sb-note:hover { transform: rotate(0) translateY(-4px) scale(1.04); }
.sb-note::after {
    content: ""; position: absolute; top: -9px; right: 26px; width: 54px; height: 18px;
    background: rgba(255,255,255,0.6); transform: rotate(5deg); box-shadow: 0 1px 2px rgba(0,0,0,0.08);
}
.sb-note-title { font-weight: 700; font-size: 0.92rem; color: var(--ink); direction: ltr; text-align: right; word-break: break-all; }
.sb-note-loc { font-family: 'Gveret Levin', 'Rubik', sans-serif; font-size: 1.15rem; color: var(--ink-blue); }
.sb-meter { display: flex; align-items: center; gap: 8px; margin: 6px 0; direction: ltr; justify-content: flex-end;
            font-size: 0.78rem; color: var(--pencil); font-variant-numeric: tabular-nums; }
.sb-meter i { display: block; width: 70px; height: 5px; background: rgba(30,43,79,0.12); border-radius: 4px; overflow: hidden; }
.sb-meter i::after { content: ""; display: block; height: 100%; width: var(--w); background: var(--ink-blue); border-radius: 4px; }
.sb-note-text { font-size: 0.84rem; color: #3D4766; line-height: 1.5; unicode-bidi: plaintext; }

/* ---------- תיבת הקלט: שורת כתיבה עם עט ---------- */
[data-testid="stBottomBlockContainer"] { max-width: 780px; padding-bottom: 1.6rem; }
[data-testid="stChatInput"] > div {
    background: var(--paper); border: none; border-radius: 14px;
    box-shadow: 0 0 0 1.5px #D3CEE0, 0 16px 30px -16px rgba(50,35,110,0.5);
}
[data-testid="stChatInput"]:focus-within > div { box-shadow: 0 0 0 2px var(--ink-blue), 0 16px 30px -16px rgba(50,35,110,0.5); }
[data-testid="stChatInput"] textarea { font-family: 'Gveret Levin', 'Rubik', sans-serif; font-size: 1.35rem; color: var(--ink-blue); }
[data-testid="stChatInput"] textarea::placeholder { color: #9AA0B8; }
[data-testid="stChatInput"] button { background: var(--ink-blue); border-radius: 10px; }
[data-testid="stChatInput"] button svg { fill: #fff; color: #fff; }

/* ---------- סרגל צד: כריכה פנימית ---------- */
[data-testid="stSidebar"] { background: #F7F5FB; border-left: 1px solid #E2DDEB; }
.sb-side-title { font-family: 'Caveat', cursive; font-weight: 700; font-size: 2.4rem; color: var(--ink); margin-bottom: 1rem; text-align: right; }
.sb-stat { font-family: 'Caveat', cursive; font-weight: 700; font-size: 3rem; line-height: 0.9; color: var(--ink-blue); }
.sb-stat-label { font-family: 'Gveret Levin', 'Rubik', sans-serif; font-size: 1.25rem; color: var(--pencil); margin-bottom: 1.1rem; }
.sb-stack { font-size: 0.85rem; line-height: 1.8; color: var(--pencil); border-top: 1px dashed #CFCADB; padding-top: 0.9rem; margin-bottom: 1rem; }
[data-testid="stSidebar"] button {
    background: #FFEE7A; border: none; border-radius: 2px 2px 2px 12px; color: var(--ink);
    box-shadow: 0 8px 12px -8px rgba(50,35,110,0.5); transform: rotate(-1deg); transition: transform .25s ease;
}
[data-testid="stSidebar"] button:hover { transform: rotate(0) translateY(-2px); color: var(--ink); }

/* כפתור "שיחה חדשה" - תווית צהובה קטנה בראש הדף */
.st-key-new_chat { display: flex; justify-content: flex-end; margin-top: -0.4rem; }
.st-key-new_chat button {
    width: auto; background: #FFEE7A; border: none; border-radius: 2px 2px 2px 12px; color: var(--ink);
    font-family: 'Gveret Levin', 'Rubik', sans-serif; padding: 0.15rem 1.1rem;
    box-shadow: 0 8px 12px -8px rgba(50,35,110,0.5); transform: rotate(-1.5deg); transition: transform .25s ease;
}
.st-key-new_chat button p { font-family: 'Gveret Levin', 'Rubik', sans-serif; font-size: 1.3rem; }
.st-key-new_chat button:hover { transform: rotate(0) translateY(-2px); color: var(--ink); }

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation: none !important; transition: none !important; }
    .sb-doodle path { stroke-dashoffset: 0; } .sb-start-text { opacity: 1; }
}
@media (max-width: 760px) {
    [data-testid="stMainBlockContainer"] { padding: 2rem 2.2rem 2rem 1.2rem !important; }
    .sb-tabs, .sb-start { display: none; }
    .sb-logo { font-size: 4rem; }
}
</style>
"""


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
