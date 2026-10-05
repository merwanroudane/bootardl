"""
عناصر الواجهة المشتركة: اتجاه RTL، الشريط الجانبي على اليمين، لوحة الألوان،
وبطاقات العرض المستعملة في كل صفحات المنصة.

منصة البوتستراب — د. مروان رودان
"""

from __future__ import annotations

import streamlit as st

# ----------------------------------------------------------------------------
# لوحة الألوان — ألوان فاتحة متعددة، لا لون داكن واحد
# ----------------------------------------------------------------------------
PALETTE = {
    "blue": "#3B82F6",
    "indigo": "#6366F1",
    "teal": "#14B8A6",
    "green": "#10B981",
    "amber": "#F59E0B",
    "orange": "#FB923C",
    "rose": "#F43F5E",
    "violet": "#8B5CF6",
    "cyan": "#06B6D4",
    "pink": "#EC4899",
    "lime": "#84CC16",
    "slate": "#64748B",
}

SOFT = {
    "blue": "#E8F0FE",
    "indigo": "#ECECFE",
    "teal": "#E0F7F4",
    "green": "#E3F8F0",
    "amber": "#FEF4E2",
    "orange": "#FEF0E4",
    "rose": "#FEECEF",
    "violet": "#F2ECFE",
    "cyan": "#E2F7FB",
    "pink": "#FDEAF4",
    "lime": "#F2FAE1",
    "slate": "#EEF2F7",
}

SEQ = ["#3B82F6", "#14B8A6", "#F59E0B", "#F43F5E", "#8B5CF6",
       "#10B981", "#FB923C", "#06B6D4", "#EC4899", "#84CC16"]

PLOT_FONT = dict(family="Cairo, Tajawal, sans-serif", size=14, color="#17233B")


# ----------------------------------------------------------------------------
# CSS: الاتجاه من اليمين لليسار + الشريط الجانبي على اليمين
# ----------------------------------------------------------------------------
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

/* ----- الاتجاه العام: عربي من اليمين إلى اليسار ----- */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    direction: rtl;
}

/* الشريط الجانبي على جهة اليمين.
   ملاحظة: مع direction:rtl يكفي flex-direction:row — فأول عنصر يذهب لليمين.
   وإضافة row-reverse هنا تُلغي أثر RTL وتُعيد الشريط لليسار. */
[data-testid="stAppViewContainer"] {
    flex-direction: row !important;
}
section[data-testid="stSidebar"] {
    direction: rtl;
    border-left: 1px solid #D6E2F6;
    border-right: none;
}
[data-testid="stSidebarCollapsedControl"] {
    right: 0.75rem;
    left: auto;
}
[data-testid="stSidebarCollapseButton"] {
    transform: scaleX(-1);
}
[data-testid="stHeader"] { direction: ltr; }
[data-testid="stToolbar"] { direction: ltr; }

/* النصوص محاذاة لليمين، والشفرة البرمجية تبقى LTR */
[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] h5 {
    text-align: right;
}
[data-testid="stMain"] pre,
[data-testid="stMain"] code,
[data-testid="stCode"],
[data-testid="stCodeBlock"] {
    direction: ltr;
    text-align: left;
}
[data-testid="stMarkdownContainer"] .katex,
[data-testid="stMarkdownContainer"] .katex-display {
    direction: ltr;
}
[data-testid="stDataFrame"], [data-testid="stTable"] { direction: ltr; }
[data-testid="stMetric"] { direction: rtl; text-align: right; }

/* ----- الطباعة ----- */
html, body, [class*="st-"] {
    font-family: 'Cairo', 'Tajawal', sans-serif;
}
/* استثناء أيقونات Material حتى لا تتحوّل إلى كلمات حرفية */
[data-testid="stIconMaterial"],
span[translate="no"][data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-symbols-outlined,
[class*="material-symbols"] {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
    direction: ltr;
}
[data-testid="stMain"] p, [data-testid="stMain"] li {
    font-size: 1.03rem;
    line-height: 2.05;
    color: #243352;
}
h1 { font-weight: 900 !important; letter-spacing: 0 !important; }
h2, h3 { font-weight: 700 !important; }

/* ----- ترويسة الصفحة ----- */
.bs-hero {
    border-radius: 20px;
    padding: 26px 32px;
    margin-bottom: 22px;
    color: #0F2246;
    box-shadow: 0 10px 28px rgba(37, 99, 235, 0.10);
    border: 1px solid rgba(255,255,255,0.65);
}
.bs-hero h1 {
    margin: 0 0 6px 0;
    font-size: 2.0rem;
    font-weight: 900;
    color: #10203F;
}
.bs-hero p {
    margin: 0;
    font-size: 1.05rem;
    color: #35496F;
    line-height: 1.9;
}
.bs-hero .bs-kicker {
    display: inline-block;
    background: rgba(255,255,255,0.78);
    border-radius: 999px;
    padding: 3px 14px;
    font-size: 0.82rem;
    font-weight: 700;
    color: #1D4ED8;
    margin-bottom: 10px;
    letter-spacing: 0.3px;
}

/* ----- بطاقة المفهوم ----- */
.bs-card {
    border-radius: 16px;
    padding: 18px 22px;
    margin: 12px 0;
    border-right: 6px solid var(--bs-accent, #3B82F6);
    background: var(--bs-bg, #F3F6FC);
    box-shadow: 0 2px 10px rgba(16, 32, 63, 0.05);
}
.bs-card h4 {
    margin: 0 0 8px 0;
    font-size: 1.08rem;
    font-weight: 800;
    color: #13254A;
}
.bs-card p, .bs-card li {
    margin: 0 0 6px 0;
    font-size: 0.99rem;
    line-height: 1.95;
    color: #2A3C5F;
}
.bs-card ul { margin: 4px 0 0 0; padding-right: 20px; }
.bs-card .bs-en {
    font-family: 'JetBrains Mono', monospace;
    direction: ltr;
    unicode-bidi: embed;
    font-size: 0.86em;
    color: #1D4ED8;
}

/* ----- بطاقات شبكية ----- */
.bs-grid { display: grid; gap: 14px; margin: 10px 0 18px 0; }
.bs-tile {
    border-radius: 16px;
    padding: 16px 18px;
    border: 1px solid #E2EAF7;
    background: #FFFFFF;
    box-shadow: 0 2px 10px rgba(16, 32, 63, 0.05);
    transition: transform .15s ease, box-shadow .15s ease;
}
.bs-tile:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(37,99,235,.12); }
.bs-tile .bs-num {
    display: inline-flex; align-items: center; justify-content: center;
    width: 34px; height: 34px; border-radius: 10px;
    font-weight: 800; font-size: 0.95rem; color: #fff; margin-bottom: 8px;
}
.bs-tile h5 { margin: 0 0 4px 0; font-size: 1.02rem; font-weight: 800; color: #13254A; }
.bs-tile p { margin: 0; font-size: 0.92rem; color: #51637F; line-height: 1.8; }

/* ----- شريط المصطلح ----- */
.bs-term {
    display: inline-block;
    background: #EDF3FE;
    border: 1px solid #D4E2FB;
    border-radius: 8px;
    padding: 1px 9px;
    margin: 0 2px;
    font-family: 'JetBrains Mono', monospace;
    direction: ltr;
    unicode-bidi: embed;
    font-size: 0.85em;
    color: #1D4ED8;
}

/* ----- جدول مبسط ----- */
.bs-table { width: 100%; border-collapse: collapse; margin: 10px 0 18px 0; font-size: 0.95rem; }
.bs-table th {
    background: #EDF3FE; color: #16294F; font-weight: 800;
    padding: 10px 12px; text-align: right; border-bottom: 2px solid #D4E2FB;
}
.bs-table td {
    padding: 9px 12px; border-bottom: 1px solid #E8EEF8; color: #2A3C5F;
    text-align: right; vertical-align: top; line-height: 1.8;
}
.bs-table tr:nth-child(even) td { background: #FAFCFF; }
.bs-table code { direction: ltr; unicode-bidi: embed; font-size: 0.86em; }

/* ----- خطوات مرقمة ----- */
.bs-steps { counter-reset: bsstep; padding: 0; margin: 8px 0 18px 0; list-style: none; }
.bs-steps li {
    counter-increment: bsstep;
    position: relative;
    padding: 12px 56px 12px 16px;
    margin-bottom: 10px;
    border-radius: 14px;
    background: #F7FAFF;
    border: 1px solid #E2EAF7;
    line-height: 1.95;
    color: #27395B;
}
.bs-steps li::before {
    content: counter(bsstep);
    position: absolute; right: 14px; top: 12px;
    width: 30px; height: 30px; border-radius: 9px;
    background: #2563EB; color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 0.9rem;
}

/* ----- توقيع المؤلف في الشريط الجانبي ----- */
.bs-sign {
    margin-top: 10px; padding: 14px 16px; border-radius: 14px;
    background: linear-gradient(135deg, #EAF1FD 0%, #E0F7F4 100%);
    border: 1px solid #D6E2F6; text-align: center;
}
.bs-sign .n { font-weight: 800; color: #13254A; font-size: 0.98rem; }
.bs-sign .r { font-size: 0.82rem; color: #51637F; margin-top: 2px; line-height: 1.7; }

/* تنظيف */
[data-testid="stMain"] .block-container { padding-top: 2.2rem; max-width: 1180px; }
hr { border-color: #E4EBF7; }
</style>
"""


def setup_page(title: str = "منصة البوتستراب") -> None:
    """تُستدعى مرة واحدة من ملف الدخول."""
    st.set_page_config(
        page_title=title,
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_css() -> None:
    st.html(_CSS)


# ----------------------------------------------------------------------------
# مكوّنات العرض
# ----------------------------------------------------------------------------
def hero(title: str, subtitle: str, kicker: str = "", c1: str = "#E8F0FE",
         c2: str = "#E0F7F4") -> None:
    """ترويسة الصفحة بتدرج لوني فاتح."""
    k = f'<span class="bs-kicker">{kicker}</span>' if kicker else ""
    st.html(
        f'<div class="bs-hero" style="background:linear-gradient(120deg,{c1} 0%,{c2} 100%)">'
        f'{k}<h1>{title}</h1><p>{subtitle}</p></div>'
    )


def card(title: str, body_html: str, color: str = "blue") -> None:
    """بطاقة مفهوم ملوّنة."""
    st.html(
        f'<div class="bs-card" style="--bs-accent:{PALETTE[color]};--bs-bg:{SOFT[color]}">'
        f"<h4>{title}</h4>{body_html}</div>"
    )


def tiles(items: list[dict], cols: int = 3) -> None:
    """شبكة بطاقات: كل عنصر {num, title, text, color}."""
    html = f'<div class="bs-grid" style="grid-template-columns:repeat({cols},1fr)">'
    for it in items:
        c = PALETTE.get(it.get("color", "blue"), PALETTE["blue"])
        html += (
            f'<div class="bs-tile">'
            f'<div class="bs-num" style="background:{c}">{it["num"]}</div>'
            f'<h5>{it["title"]}</h5><p>{it["text"]}</p></div>'
        )
    html += "</div>"
    st.html(html)


def table(headers: list[str], rows: list[list[str]]) -> None:
    """جدول HTML بسيط يحترم الاتجاه العربي."""
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = ""
    for r in rows:
        b += "<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>"
    st.html(f'<table class="bs-table"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>')


def steps(items: list[str]) -> None:
    """قائمة خطوات مرقّمة."""
    li = "".join(f"<li>{x}</li>" for x in items)
    st.html(f'<ol class="bs-steps">{li}</ol>')


def term(en: str) -> str:
    """إرجاع المصطلح الإنجليزي داخل شارة."""
    return f'<span class="bs-term">{en}</span>'


def signature() -> None:
    st.sidebar.html(
        '<div class="bs-sign">'
        '<div class="n">د. مروان رودان</div>'
        '<div class="r">Dr Merwan Roudane<br>'
        'مؤلّف حزم <span style="font-family:monospace">bootdiag</span> · '
        '<span style="font-family:monospace">aardl</span> · '
        '<span style="font-family:monospace">fbardl</span></div></div>'
    )


def plotly(fig, key: str | None = None) -> None:
    """عرض شكل Plotly بإعدادات موحّدة."""
    fig.update_layout(font=PLOT_FONT, paper_bgcolor="#FFFFFF", plot_bgcolor="#FBFCFE")
    st.plotly_chart(fig, key=key, config={"displayModeBar": False})


def note(text: str, color: str = "amber", icon: str = "💡") -> None:
    st.html(
        f'<div class="bs-card" style="--bs-accent:{PALETTE[color]};--bs-bg:{SOFT[color]}">'
        f"<p><b>{icon}</b> {text}</p></div>"
    )
