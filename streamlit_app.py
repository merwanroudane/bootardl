"""
منصّة البوتستراب والاختبارات البعدية
=====================================
دليل شامل للباحث: من فكرة إعادة المعاينة حتى الاختبارات البعدية
المعتمدة على البوتستراب وعائلة Bootstrap ARDL.

المؤلف: د. مروان رودان — Dr Merwan Roudane
التشغيل:  streamlit run streamlit_app.py
"""

import streamlit as st

from core.ui import setup_page, inject_css, signature

setup_page("منصّة البوتستراب — د. مروان رودان")
inject_css()

if "seed" not in st.session_state:
    st.session_state.seed = 2026

PAGES = {
    "البداية": [
        st.Page("app_pages/p00_home.py", title="الصفحة الرئيسية",
                icon=":material/home:", default=True),
        st.Page("app_pages/p01_why.py", title="لماذا نحتاج البوتستراب؟",
                icon=":material/help:"),
    ],
    "أساسيات البوتستراب": [
        st.Page("app_pages/p02_idea.py", title="الفكرة من الصفر",
                icon=":material/lightbulb:"),
        st.Page("app_pages/p03_types.py", title="أنواع البوتستراب",
                icon=":material/category:"),
        st.Page("app_pages/p04_wild.py", title="الوايلد بوتستراب",
                icon=":material/bolt:"),
        st.Page("app_pages/p05_pvalue.py", title="قيمة p وعدد التكرارات B",
                icon=":material/functions:"),
    ],
    "الاختبارات البعدية": [
        st.Page("app_pages/p06_classic.py", title="الاختبارات العادية",
                icon=":material/fact_check:"),
        st.Page("app_pages/p07_boot_tests.py", title="الاختبارات بالبوتستراب",
                icon=":material/verified:"),
        st.Page("app_pages/p08_stability.py", title="الاستقرار الهيكلي",
                icon=":material/show_chart:"),
    ],
    "التطبيق": [
        st.Page("app_pages/p09_montecarlo.py", title="مختبر مونت كارلو",
                icon=":material/science:"),
        st.Page("app_pages/p10_lab.py", title="المختبر التفاعلي",
                icon=":material/biotech:"),
    ],
    "الحزم البرمجية": [
        st.Page("app_pages/p11_bootdiag.py", title="حزمة bootdiag",
                icon=":material/terminal:"),
        st.Page("app_pages/p12_bardl.py", title="عائلة Bootstrap ARDL",
                icon=":material/timeline:"),
    ],
    "مراجع": [
        st.Page("app_pages/p13_glossary.py", title="المصطلحات والمراجع",
                icon=":material/menu_book:"),
    ],
}

st.logo("assets/logo.svg", size="large")

page = st.navigation(PAGES, position="sidebar")

signature()
st.sidebar.caption("جميع الصيغ مأخوذة من الأوراق الأصلية المذكورة في صفحة المراجع.")

page.run()
