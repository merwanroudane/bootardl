"""مختبر مونت كارلو: قياس الحجم والقوّة حيّاً."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.ui import hero, card, note, plotly, table, steps, PALETTE
from core.anim import anim_size_bars
from core.engine import size_experiment, TESTS

hero(
    "مختبر مونت كارلو",
    "لا تُصدّقني — تحقّق بنفسك. هذه الصفحة تُشغّل تجربة مونت كارلو حقيقية "
    "أمامك: نُولّد مئات العيّنات من عملية نعرف أنّ الفرضية الصفرية صحيحة فيها، "
    "ونعدّ كم مرّة يرفضها كل اختبار. اختبار سليم يرفض 5٪ فقط.",
    "التحقّق التجريبي",
    "#E2F7FB", "#E8F0FE",
)

# ============================================================== الشرح
st.header("١. كيف تعمل تجربة مونت كارلو؟")

steps([
    "<b>نُحدّد عملية توليد بيانات</b> نعرف حقيقتها تماماً: "
    "y<sub>t</sub> = 0.2 + ρ·y<sub>t−1</sub> + x<sub>t</sub> + u<sub>t</sub>، "
    "وأخطاؤها <b>تحقّق الفرضية الصفرية</b> المختبَرة.",
    "<b>نسحب منها عيّنة</b> بحجم n ونُقدّر النموذج.",
    "<b>نُجري الاختبار</b> بنسختيه: التقاربية والبوتستراب.",
    "<b>نُسجّل</b>: هل رفض كل منهما عند 5٪؟ "
    "(الرفض هنا <b>خطأ</b> دائماً — فالصفرية صحيحة بالبناء.)",
    "<b>نُكرّر</b> مئات المرّات ونحسب <b>نسبة الرفض</b>.",
    "<b>المقارنة:</b> النسبة المثالية 5٪. أعلى = إفراط في الرفض "
    "(تُعلن مشاكل وهمية). أقل = نقص (تتجاهل مشاكل حقيقية).",
])

note(
    "<b>مصطلحان:</b> نسبة الرفض تحت صفرية <b>صحيحة</b> تُسمّى "
    "<b>الحجم</b> (<span class='bs-en'>size</span>). "
    "ونسبة الرفض تحت صفرية <b>خاطئة</b> تُسمّى "
    "<b>القوّة</b> (<span class='bs-en'>power</span>). "
    "الاختبار الجيّد: حجمه = المستوى الاسمي، وقوّته أعلى ما يمكن. "
    "<b>والحجم أولاً</b> — فاختبار مشوّه الحجم قوّته بلا معنى.",
    "blue", "📏",
)

# ============================================================== التجربة
st.header("٢. شغّل التجربة")

st.warning(
    "⏱️ هذه حسابات حقيقية ثقيلة. الإعدادات الافتراضية تستغرق نحو دقيقة. "
    "ابدأ بإعدادات صغيرة ثم ارفعها."
)

c1, c2, c3 = st.columns(3)
with c1:
    test_mc = st.selectbox(
        "الاختبار",
        ["koenker", "bp", "white", "arch", "bg", "bg_hr", "mlm_hr", "jb", "reset"],
        format_func=lambda s: f"{TESTS[s][0]} — {TESTS[s][1]}",
        key="mc_test",
    )
    dgp_mc = st.selectbox(
        "عملية توليد البوتستراب",
        ["wild", "residual", "normal", "sieve", "stationary", "fixed"],
        index=1,
        key="mc_dgp",
    )
with c2:
    n_mc = st.select_slider("حجم العيّنة n", [30, 40, 50, 60, 80, 100, 150, 200],
                            60, key="mc_n")
    rho_mc = st.select_slider("المثابرة ρ", [0.0, 0.3, 0.5, 0.7, 0.9, 0.95],
                              0.9, key="mc_rho")
with c3:
    reps_mc = st.select_slider("عدد تكرارات مونت كارلو",
                               [50, 100, 150, 200, 300], 100, key="mc_reps")
    B_mc = st.select_slider("عدد تكرارات البوتستراب B",
                            [99, 199, 399, 999], 199, key="mc_B")

c4, c5 = st.columns(2)
with c4:
    err_mc = st.segmented_control(
        "توزيع الأخطاء",
        ["normal", "t5", "chi2", "mixture"],
        default="normal",
        format_func=lambda s: {"normal": "طبيعي", "t5": "t(5) ذيول ثقيلة",
                               "chi2": "χ²(2) ملتوٍ",
                               "mixture": "مزيج (قيم متطرّفة)"}[s],
        key="mc_err",
    )
with c5:
    alpha_mc = st.segmented_control("المستوى الاسمي α", [0.10, 0.05, 0.01],
                                    default=0.05,
                                    format_func=lambda a: f"{a:.0%}",
                                    key="mc_alpha")

run = st.button("🧪  شغّل تجربة مونت كارلو", type="primary", key="mc_run")

if run:
    bar = st.progress(0.0, "جارٍ التشغيل…")
    with st.spinner(
        f"تشغيل {reps_mc} تكرار × {B_mc} عيّنة بوتستراب "
        f"= {reps_mc * B_mc:,} تقدير…"
    ):
        res = size_experiment(test_mc, int(n_mc), float(rho_mc), 0.0,
                              int(reps_mc), int(B_mc), dgp_mc,
                              float(alpha_mc), err_mc, seed=2026)
    bar.progress(1.0, "اكتمل")
    bar.empty()

    st.session_state["mc_last"] = dict(res=res, test=test_mc, n=n_mc,
                                       rho=rho_mc, dgp=dgp_mc, err=err_mc,
                                       reps=reps_mc, B=B_mc, alpha=alpha_mc)

if "mc_last" in st.session_state:
    L = st.session_state["mc_last"]
    res, a = L["res"], L["alpha"]

    st.subheader("النتيجة")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("المستوى الاسمي", f"{a:.0%}")
    m2.metric("الحجم الفعلي — التقاربي",
              f"{res['asymptotic']:.1%}",
              delta=f"{res['asymptotic'] - a:+.1%}",
              delta_color="inverse")
    m3.metric("الحجم الفعلي — البوتستراب",
              f"{res['bootstrap']:.1%}",
              delta=f"{res['bootstrap'] - a:+.1%}",
              delta_color="inverse")
    m4.metric("تكرارات ناجحة", f"{res['reps']}")

    # الخطأ المعياري لمونت كارلو
    se = float(np.sqrt(a * (1 - a) / max(res["reps"], 1)))
    st.caption(
        f"الخطأ المعياري لمونت كارلو عند هذا العدد من التكرارات هو "
        f"±{se:.3f} تقريباً. أي فرق أصغر من ±{1.96*se:.3f} عن المستوى الاسمي "
        f"لا يُعدّ دليلاً على تشوّه."
    )

    plotly(
        anim_size_bars(
            [f"{TESTS[L['test']][0]}<br>n={L['n']}, ρ={L['rho']}"],
            [res["asymptotic"]], [res["bootstrap"]], a),
        key="mc_bars",
    )

    # التفسير الآلي
    da = res["asymptotic"] - a
    db = res["bootstrap"] - a
    verdict = []
    if abs(da) > 1.96 * se:
        verdict.append(
            f"❌ **النسخة التقاربية مشوّهة**: ترفض بنسبة "
            f"{res['asymptotic']:.1%} بدل {a:.0%} — "
            + ("**إفراط في الرفض**، أي أنّها ستُعلن مشاكل غير موجودة."
               if da > 0 else
               "**نقص في الحجم**، أي أنّها ستتجاهل مشاكل حقيقية.")
        )
    else:
        verdict.append(
            f"✅ النسخة التقاربية مقبولة في هذا الإعداد "
            f"({res['asymptotic']:.1%})."
        )
    if abs(db) > 1.96 * se:
        verdict.append(
            f"⚠️ **نسخة البوتستراب أيضاً بعيدة** ({res['bootstrap']:.1%}). "
            + ("جرّب عملية توليد أخرى: "
               "راجع جدول المطابقة في صفحة «الاختبارات بالبوتستراب» — "
               "فاختيار عملية التوليد غير المناسبة للفرضية المختبَرة "
               "هو السبب الأشيع."
               if L["dgp"] == "wild" and L["test"] in
               ("koenker", "bp", "white", "arch")
               else "جرّب زيادة B أو عدد تكرارات مونت كارلو.")
        )
    else:
        verdict.append(
            f"✅ **نسخة البوتستراب على المستوى الاسمي** "
            f"({res['bootstrap']:.1%}) — وهذا هو المطلوب."
        )
    for v in verdict:
        if v.startswith("❌"):
            st.error(v)
        elif v.startswith("⚠️"):
            st.warning(v)
        else:
            st.success(v)

# ============================================================== مقارنة
st.header("٣. مقارنة عمليات التوليد على الاختبار نفسه")

st.markdown(
    "هذا هو التمرين الأهم في الصفحة: **عملية التوليد الصحيحة ليست واحدة لكل "
    "الاختبارات**. شغّل المقارنة وستراه بنفسك."
)

c1, c2, c3 = st.columns(3)
with c1:
    t_cmp = st.selectbox("الاختبار", ["koenker", "bp", "bg", "jb", "arch"],
                         format_func=lambda s: TESTS[s][0], key="cmp_t")
with c2:
    n_cmp = st.select_slider("n", [40, 50, 60, 80, 100], 50, key="cmp_n")
with c3:
    reps_cmp = st.select_slider("تكرارات مونت كارلو", [50, 80, 100, 150], 80,
                                key="cmp_r")

if st.button("⚖️  قارن أربع عمليات توليد", key="cmp_run"):
    dgps = ["wild", "residual", "normal", "sieve"]
    rows, asy_v, boot_v = [], [], []
    pb = st.progress(0.0)
    for i, g in enumerate(dgps):
        r = size_experiment(t_cmp, int(n_cmp), 0.9, 0.0, int(reps_cmp), 199,
                            g, 0.05, "normal", seed=333)
        rows.append([f"<code>{g}</code>", f"{r['asymptotic']:.1%}",
                     f"<b style='color:"
                     f"{'#10B981' if abs(r['bootstrap']-0.05) < 0.025 else '#E8536B'}'>"
                     f"{r['bootstrap']:.1%}</b>"])
        asy_v.append(r["asymptotic"])
        boot_v.append(r["bootstrap"])
        pb.progress((i + 1) / len(dgps), f"{g} …")
    pb.empty()
    st.session_state["cmp_res"] = (rows, dgps, asy_v, boot_v, t_cmp)

if "cmp_res" in st.session_state:
    rows, dgps, asy_v, boot_v, tc = st.session_state["cmp_res"]
    table(["عملية التوليد", "الحجم التقاربي", "حجم البوتستراب"], rows)
    plotly(
        anim_size_bars([g for g in dgps], asy_v, boot_v, 0.05),
        key="cmp_bars",
    )
    best = dgps[int(np.argmin([abs(b - 0.05) for b in boot_v]))]
    st.success(
        f"الأقرب للمستوى الاسمي 5٪ هنا هو "
        f"**`{best}`** لاختبار **{TESTS[tc][0]}**."
    )

# ============================================================== النتائج
st.header("٤. نتائج مرجعية من الأدبيات")

st.markdown(
    "لمن لا يريد انتظار المحاكاة، هذه النتائج المنشورة. "
    "كلّها تحت فرضية صفرية صحيحة عند مستوى اسمي محدّد:"
)

table(
    ["المصدر", "الإعداد", "النتيجة"],
    [
        ["<b>حزمة bootdiag</b><br>(300 تكرار، 5٪)",
         "AR(1)-X، n=60، ρ=0.9",
         "Koenker تقاربي: <span style='color:#E8536B'>19.7٪</span><br>"
         "Koenker بوتستراب: <span style='color:#10B981'>6.0٪</span>"],
        ["<b>Kilian &amp; Demiroglu (2000)</b>",
         "VAR متكامل، JB، 10٪",
         "التقاربي قد ينزل إلى <span style='color:#3B82F6'>3٪</span>؛ "
         "البوتستراب شبه مضبوط حتى عند T=40 وρ حتى 0.9999. "
         "<b>التشوّه يبقى عند T=5000</b>"],
        ["<b>O'Reilly &amp; Whelan (2005)</b>",
         "SupW، كسر في التباين، ρ=0.95",
         "الغربال: <span style='color:#E8536B'>19٪</span><br>"
         "الوايلد المُعدَّل للتحيّز: "
         "<span style='color:#10B981'>9–11٪</span> لكل ρ&lt;0.99"],
        ["<b>Domínguez &amp; Lobato (2019)</b>",
         "اختبار تحديد، تباين متغيّر، 10٪",
         "تجاهل تقدير متغيّر الشرط: "
         "<span style='color:#E8536B'>31–32٪</span><br>"
         "اختبارا C_n و K_n: على المستوى"],
        ["<b>Cribari-Neto &amp; Zarkos (1999)</b>",
         "Breusch–Pagan، تصميم غير مواتٍ",
         "BP <b>ناقص الحجم</b>؛ التصحيحات التحليلية (LM¹⁺…LM³⁺) "
         "تُصلحه عادةً، <b>لكن البوتستراب وحده يبقى موثوقاً عند تفرطح عالٍ "
         "في x₁</b>"],
        ["<b>Godfrey &amp; Tremayne (2005)</b>",
         "BG الحصين، تباين متغيّر",
         "القيم الحرجة التقاربية تُعطي اختبارات <b>ناقصة الحجم</b> "
         "و«لا يُنصح بها»؛ الوايلد بـ Rademacher يضبط الحجم"],
    ],
)

# ============================================================== القوة
st.header("٥. ملاحظة على القوّة")

card(
    "لا تنسَ الوجه الآخر",
    "<p>ضبط الحجم ليس كل شيء. اختبار يرفض 0٪ دائماً حجمه مضبوط تماماً "
    "عند أي مستوى — وهو عديم الفائدة لأنّ قوّته صفر.</p>"
    "<p>لهذا نُقارن أيضاً <b>القوّة المعدّلة للحجم</b> "
    "(<span class='bs-en'>size-adjusted power</span>): "
    "نضبط القيمة الحرجة لكل اختبار حتى يصبح حجمه 5٪ بالضبط، "
    "ثم نقارن قوّتها.</p>"
    "<p><b>والنتيجة المستقرّة في الأدبيات:</b> اختبارات البوتستراب "
    "لا تخسر قوّة تُذكر مقابل ضبط الحجم. بل إنّ "
    "<span class='bs-en'>O'Reilly &amp; Whelan</span> يُظهران أنّ الوايلد "
    "«بلا كلفة كفاءة» حتى تحت ضوضاء بيضاء — "
    "أي أنّك لا تدفع ثمناً مقابل الحصانة.</p>"
    "<p><b>والنقاش المفتوح:</b> "
    "<span class='bs-en'>Mantalos</span> و"
    "<span class='bs-en'>Jeong &amp; Chung</span> يُظهران أنّ البوتستراب "
    "<b>غير المقيّد</b> (تحت البديلة) له قوّة أعلى في العيّنات الصغيرة "
    "حتى بعد تعديل الحجم. فالمقايضة حقيقية، والحزمة الجيّدة تعرض الخيارين.</p>",
    "amber",
)

st.divider()
st.markdown(
    "**الصفحة التالية:** المختبر التفاعلي — ارفع بياناتك أو ولّدها، "
    "وشغّل البطارية الكاملة."
)
