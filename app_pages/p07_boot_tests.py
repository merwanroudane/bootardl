"""الاختبارات البعدية المعتمدة على البوتستراب."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy import stats as sps

from core.ui import hero, card, note, plotly, table, steps, PALETTE, SOFT
from core.anim import anim_build_distribution
from core.engine import simulate_dgp, design_from, run_boot_test

hero(
    "الاختبارات البعدية بالبوتستراب",
    "الآن نجمع كل شيء. فكرة واحدة بسيطة تُصلح كل الاختبارات في الصفحة السابقة "
    "دفعة واحدة: احتفظ بالإحصاء، واستبدل الجدول. هنا الخوارزمية الكاملة، "
    "والقاعدة الحاسمة في مطابقة عملية التوليد للفرضية المختبَرة، "
    "وبطارية الاختبارات الثمانية والعشرين.",
    "الحلّ · التطبيق",
    "#E3F8F0", "#E8F0FE",
)

# ============================================================== 1. الفكرة
st.header("١. الفكرة في جملة واحدة")

st.html(
    '<div style="background:linear-gradient(120deg,#E3F8F0,#E8F0FE);'
    'border-radius:18px;padding:26px;text-align:center;margin:12px 0 20px 0;'
    'border:1px solid #CFE6F5">'
    '<p style="margin:0;font-size:1.25rem;font-weight:800;color:#0F5132;'
    'line-height:2">الإحصاء يبقى كما هو حرفياً.<br>'
    'ما يتغيّر هو التوزيع الذي نقارنه به.</p>'
    '<p style="margin:12px 0 0 0;font-size:.98rem;color:#51637F">'
    'لا تعديل على صيغة Breusch–Godfrey، ولا على Jarque–Bera، ولا على supF. '
    'الجدول فقط هو ما يُستبدل.</p></div>'
)

st.subheader("الخوارزمية الكاملة — سبع خطوات")

steps([
    "<b>قدّر نموذجك</b> كالعادة واحفظ: المعالم β̂، والبواقي û، "
    "ومصفوفة التصميم X، والرافعة h<sub>t</sub>.",
    "<b>احسب الإحصاء من بياناتك</b>: τ̂ = (مثلاً) إحصاء Breusch–Godfrey. "
    "هذا رقم واحد، ولن يتغيّر بعد الآن.",
    "<b>قدّر النموذج تحت الفرضية الصفرية</b> لتحصل على β̃ والبواقي المقيّدة ũ. "
    "(إن كانت الصفرية هي «لا ارتباط ذاتي»، فهذا هو نموذجك الأصلي نفسه.)",
    "<b>حوّل البواقي</b>: ū<sub>t</sub> = ũ<sub>t</sub>/(1−h<sub>t</sub>) "
    "لتصحيح الرافعة — هذا هو HC3.",
    "<b>ولّد عيّنة بوتستراب</b> y* وفق عملية التوليد المختارة. "
    "في النموذج الديناميكي: ولّدها <b>تكرارياً</b> وأعِد بناء عمود "
    "y*<sub>t−1</sub> داخل مصفوفة التصميم.",
    "<b>احسب τ* من العيّنة الجديدة</b> بالصيغة نفسها تماماً. "
    "كرّر الخطوتين ٥ و٦ عدد B مرّة.",
    "<b>قيمة p = نسبة قيم τ* التي تجاوزت τ̂.</b> "
    "والقيمة الحرجة 5٪ هي المئين 95 لتوزيع τ*.",
])

note(
    "لاحظ أنّ هذا الإجراء <b>لا يعتمد إطلاقاً على شكل الإحصاء</b>. "
    "لهذا يمكن تطبيقه على اختبار له توزيع صفري غير قياسي تماماً "
    "(مثل Szroeter أو Harrison–McCabe أو CvM) بالسهولة نفسها التي يُطبّق بها "
    "على اختبار χ² بسيط. <b>هذه هي القوّة الحقيقية</b>: "
    "تحرّرتَ من قيد «هل لهذا الإحصاء جدول؟».",
    "green", "🔓",
)

# ============================================================== 2. القاعدة
st.header("٢. القاعدة الحاسمة: طابِق عملية التوليد مع الفرضية الصفرية")

note(
    "هذه هي النقطة التي يُخطئ فيها حتى الباحثون المتمرّسون، "
    "وهي <b>قابلة للتحقّق بالمحاكاة</b> كما سنرى.",
    "rose", "🧨",
)

card(
    "المبدأ",
    "<p>عالم البوتستراب يجب أن يكون عالماً <b>تصدق فيه الفرضية الصفرية التي "
    "تختبرها بالذات</b>. ليس أي فرضية صفرية — تلك التي تختبرها.</p>"
    "<p><b>مثال على الخطأ الشائع:</b> تريد اختبار تجانس التباين، "
    "فتستعمل الوايلد بوتستراب لأنّه «الافتراضي». "
    "لكن الوايلد يحفظ <span dir='ltr'>|û_t|</span> لكل t — "
    "أي أنّه <b>يحفظ نمط عدم التجانس الذي تختبر وجوده</b>. "
    "فعالمك «الصفري» ليس متجانس التباين إطلاقاً، "
    "والاختبار يصبح محافظاً أكثر من اللازم ويفقد قوّته.</p>",
    "rose",
)

st.subheader("الدليل بالمحاكاة")

st.markdown(
    "جرّبنا اختبار Koenker تحت فرضية صفرية **صحيحة** "
    "(<span dir='ltr'>n = 50، ρ = 0.9، 200 تكرار، B = 199، α = 5٪</span>). "
    "نسبة الرفض *يجب* أن تكون 5٪:"
)

table(
    ["عملية توليد البوتستراب", "أخطاء طبيعية", "أخطاء ذات ذيول ثقيلة t(5)", "الحكم"],
    [
        ["<code>wild</code> — الوايلد",
         "<span style='color:#E8536B'>2.5٪</span>",
         "<span style='color:#E8536B'>0.5٪</span>",
         "<b>محافظ جداً</b> — يحفظ نمط عدم التجانس المختبَر"],
        ["<code>residual</code> — البواقي",
         "<span style='color:#10B981'>5.5٪</span>",
         "<span style='color:#10B981'>6.0٪</span>",
         "<b>✅ الصحيح</b> — يفرض تجانس التباين فعلاً"],
        ["<code>normal</code> — معلمي غاوسي",
         "<span style='color:#10B981'>7.0٪</span>", "—",
         "جيّد، لكنّه يضيف افتراض الاعتدالية"],
        ["التقاربي χ²", "6.0٪", "5.5٪",
         "مقبول هنا، لكنّه ينهار في تصاميم أخرى"],
    ],
)

st.caption(
    "محاكاة مُنفَّذة بمحرّك هذه المنصّة نفسه. يمكنك إعادة إنتاجها من صفحة "
    "«مختبر مونت كارلو»."
)

st.subheader("جدول المطابقة الذي يجب أن تحفظه")

table(
    ["الفرضية الصفرية التي تختبرها", "عملية التوليد الصحيحة", "السبب"],
    [
        ["<b>لا ارتباط ذاتي</b><br>(BG، DW، ρ̂)",
         "<code>wild</code> أو <code>residual</code>",
         "كلاهما يُنتج أخطاءً غير مترابطة. الوايلد يُضيف حصانة ضد عدم تجانس "
         "التباين كـ<b>مُزعج</b> (nuisance) — وهذا ما يريده Godfrey &amp; Tremayne"],
        ["<b>تجانس التباين</b><br>(BP، Koenker، White، ARCH)",
         "<code>residual</code> أو <code>normal</code>",
         "<b>يجب</b> أن تُفرض الصفرية: أخطاء متجانسة التباين. "
         "الوايلد يحفظ ما تختبره فيُفسد القوّة"],
        ["<b>الاعتدالية</b><br>(JB، AD، Lobato–Velasco)",
         "<code>normal</code> أو <code>sieve</code> بابتكارات غاوسية",
         "نُولّد أخطاءً <b>معتدلة بالضبط</b>. "
         "هذا ما فعله Kilian &amp; Demiroglu وPsaradakis &amp; Vávra"],
        ["<b>استقرار المعالم</b><br>(CUSUM، supF)",
         "<code>wild</code> (أو <code>residual</code> إن كانت الأخطاء iid)",
         "O'Reilly &amp; Whelan: الوايلد أفضل من أربعة مخطّطات، "
         "خاصّة مع كسر في التباين"],
        ["<b>كسر في المتوسّط أو التباين</b><br>(CUSUM-BWB)",
         "<code>blockwild</code>",
         "Lee &amp; Baek: يُزيل كسر المتوسّط لكنّه يحفظ المثابرة وتقلّب التباين"],
        ["<b>الشكل الدالي</b><br>(RESET، CvM، KS)",
         "<code>wild</code>",
         "Stute et al.: الوايلد هو <b>الوحيد المتّسق</b> هنا. "
         "الأزواج غير متّسق مُثبَت"],
    ],
)

# ============================================================== 3. NHI
st.header("٣. الاختبار المشترك NHI — بطارية كاملة من حلقة واحدة")

card(
    "تفكيك Jarque–Bera (1980)",
    "<p>بدل أن تُجري ثلاثة اختبارات منفصلة وتواجه مشكلة "
    "<b>الاختبارات المتعدّدة</b> (<span class='bs-en'>multiple testing</span>)، "
    "استعمل التفكيك الذي قدّمه Jarque وBera أنفسهما:</p>"
    r"<p style='direction:ltr;text-align:center;font-size:1.15em;background:#fff;"
    r"padding:14px;border-radius:10px'>"
    r"LM<sub>NHI</sub> = LM<sub>N</sub> + LM<sub>H</sub> + LM<sub>I</sub></p>"
    "<p>من <b>حلقة بوتستراب واحدة</b> تحصل على سبعة اختبارات:</p>"
    "<ul>"
    "<li><b>١ مشترك ثلاثي:</b> <span dir='ltr'>LM_NHI</span> — "
    "«هل النموذج ملائم إجمالاً؟»</li>"
    "<li><b>٣ أحادية الاتجاه:</b> "
    "<span dir='ltr'>LM_N</span> (اعتدالية)، "
    "<span dir='ltr'>LM_H</span> (تجانس تباين)، "
    "<span dir='ltr'>LM_I</span> (استقلال)</li>"
    "<li><b>٣ ثنائية الاتجاه:</b> "
    "<span dir='ltr'>LM_NH</span>، <span dir='ltr'>LM_HI</span>، "
    "<span dir='ltr'>LM_NI</span></li>"
    "</ul>"
    "<p><b>الفائدة العملية:</b> إن رفض الاختبار المشترك، تنظر إلى المكوّنات "
    "لتعرف <b>أي اتجاه</b> هو مصدر المشكلة — بدون أن تدفع ثمن تضخّم "
    "احتمال الخطأ من النوع الأول. "
    "متاح بالأمر <code style='direction:ltr'>bootdiag nhi</code>.</p>",
    "green",
)

st.subheader("دمج عدّة اختبارات: استعمل p_min لا τ_max")

card(
    "قاعدة مهمّة",
    "<p>إذا أردت دمج عدّة اختبارات في حكم واحد، <b>لا تأخذ أكبر إحصاء</b>. "
    "فالإحصاءات لها توزيعات صفرية مختلفة ومقاييس مختلفة — "
    "مقارنة إحصاء χ²(2) بإحصاء χ²(20) بلا معنى.</p>"
    "<p>بدلاً من ذلك: خذ <b>أصغر قيمة p</b>، "
    "ثم <b>بوتستِربها هي نفسها</b> — أي احسب توزيع "
    "<span dir='ltr'>min(p₁,…,p_k)</span> تحت الفرضية الصفرية.</p>"
    "<p>الصيغ المرتبطة من Dufour et al. (2004) لدمج اختبارات عند نقاط كسر "
    "تباين مجهولة:</p>"
    "<ul>"
    "<li><b>Tippett/Wilkinson:</b> "
    "<span dir='ltr'>F_min = 1 − min_τ G(BPG_τ)</span></li>"
    "<li><b>Fisher/Pearson:</b> "
    "<span dir='ltr'>F_× = 1 − Π_τ G(BPG_τ)</span></li>"
    "</ul>"
    "<p>هذه الصيغ لها توزيعات <b>مستعصية حتى تقاربياً</b> — "
    "واختبار مونت كارلو يجعلها مضبوطة.</p>",
    "violet",
)

# ============================================================== 4. البطارية
st.header("٤. بطارية الاختبارات الثمانية والعشرين")

st.markdown(
    "هذه هي التغطية الكاملة المتاحة في حزمة "
    "<span dir='ltr' style='font-family:monospace'>bootdiag</span>، "
    "موزّعة على خمس عائلات زائد امتدادين."
)

FAM = [
    ("serial", "الارتباط الذاتي", "green", [
        ("Breusch–Godfrey LM", "الانحدار المساعد الكلاسيكي، χ²(Q)"),
        ("BG robust LM_HR", "حصين لعدم تجانس التباين، Godfrey &amp; Tremayne eq.(5)"),
        ("BG modified MLM_HR", "يُسقط الحدود المهملة تقاربياً، eq.(6)"),
        ("Durbin–Watson d", "بقيمة p ذات ذيلين متساويين — "
                            "<b>تُزيل المنطقة غير الحاسمة</b>"),
        ("First-order ρ̂", "معامل الارتباط مبوتستَراً مباشرةً — Jeong &amp; Chung"),
    ]),
    ("het", "عدم تجانس التباين", "violet", [
        ("Breusch–Pagan LM", "½ × مجموع المربّعات المفسّر"),
        ("Koenker studentised", "nR² — حصين لعدم الاعتدالية"),
        ("White general", "nR² على المستويات والمربّعات والتفاعلات"),
        ("Engle ARCH LM", "nR² من û² على إبطاءاتها"),
        ("Szroeter SKH", "مُرجَّح جيبي — <b>من الأقوى</b> حسب Dufour et al."),
        ("Harrison–McCabe", "نسبة مربّعات النصف الأول"),
    ]),
    ("norm", "الاعتدالية", "cyan", [
        ("Jarque–Bera", "T[b₁/6 + (b₂−3)²/24]"),
        ("Lobato–Velasco", "مُستودَن بمجاميع قوى التغايرات — "
                           "<b>بلا نواة ولا عرض نطاق</b>"),
        ("Anderson–Darling", "مسافة EDF بوزن يُركّز على الذيول"),
    ]),
    ("stab", "الاستقرار الهيكلي", "indigo", [
        ("CUSUM", "على البواقي التكرارية، بحِزَم بوتستراب"),
        ("CUSUM of squares", "max |S_r − r/m|"),
        ("supF", "أقصى إحصاء Chow عبر تواريخ الكسر"),
        ("aveF / expF", "متوسّط وأسّي Andrews–Ploberger"),
    ]),
    ("spec", "الشكل الدالي", "pink", [
        ("Ramsey RESET", "اختبار F على قوى ŷ حتى الرتبة المختارة"),
        ("Cramér–von Mises", "على العملية التجريبية الموسومة — Stute et al."),
        ("Kolmogorov–Smirnov", "نسخة السعة العظمى للعملية نفسها"),
    ]),
    ("nhi", "الاختبار المشترك NHI", "amber", [
        ("LM_NHI", "المشترك الثلاثي"),
        ("LM_N, LM_H, LM_I", "الثلاثة أحادية الاتجاه"),
        ("LM_NH, LM_HI, LM_NI", "الثلاثة ثنائية الاتجاه"),
    ]),
    ("fdb", "البوتستراب المزدوج السريع", "rose", [
        ("FDB", "Davidson &amp; MacKinnon (2007) — 2B+1 إحصاء"),
        ("Pretest B", "اختيار B بالاختبار المسبق — Davidson &amp; MacKinnon"),
    ]),
]

tabs = st.tabs([f"{f[1]}" for f in FAM])
for tb, (cmd, ar, col, items) in zip(tabs, FAM):
    with tb:
        st.code(f"bootdiag {cmd}", language="stata")
        table(["الاختبار", "الوصف"],
              [[f"<b>{a}</b>", b] for a, b in items])

# ============================================================== 5. حي
st.header("٥. شغّله الآن: التوزيع التقاربي مقابل التوزيع البوتستراب")

st.markdown(
    "اختر اختباراً وإعداداً، واضغط التشغيل. سترى التوزيعين متراكبين — "
    "والفجوة بينهما هي الخطأ الذي كنت سترتكبه."
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    tsel = st.selectbox(
        "الاختبار",
        ["koenker", "bg", "bg_hr", "mlm_hr", "white", "arch", "jb", "reset"],
        format_func=lambda s: {
            "koenker": "Koenker (تجانس التباين)",
            "bg": "Breusch–Godfrey LM",
            "bg_hr": "BG robust LM_HR",
            "mlm_hr": "BG modified MLM_HR",
            "white": "White general",
            "arch": "Engle ARCH LM",
            "jb": "Jarque–Bera",
            "reset": "Ramsey RESET"}[s],
        key="bt_test",
    )
with c2:
    nsel = st.slider("حجم العيّنة n", 30, 250, 60, key="bt_n")
with c3:
    rsel = st.slider("المثابرة ρ", 0.0, 0.95, 0.9, 0.05, key="bt_rho")
with c4:
    dsel = st.selectbox(
        "عملية التوليد",
        ["wild", "residual", "normal", "sieve", "stationary", "fixed"],
        key="bt_dgp",
    )

DF_MAP = {"koenker": 2, "bg": 2, "bg_hr": 2, "mlm_hr": 2, "white": 5,
          "arch": 2, "jb": 2, "reset": None}

if st.button("▶  شغّل المقارنة (999 تكرار)", type="primary", key="bt_run"):
    with st.spinner("جارٍ الحساب…"):
        rr = np.random.default_rng(2026)
        dd = simulate_dgp(int(nsel), float(rsel), 1.0, 0.0, "normal", 0.0, rr)
        yy, XX = design_from(dd["y"], dd["x"])
        out = run_boot_test(tsel, yy, XX, B=999, dgp=dsel, q=2, seed=2026)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("الإحصاء المحسوب", f"{out['stat']:.3f}")
    m2.metric("p — بوتستراب", f"{out['p_boot']:.3f}")
    m3.metric("p — تقاربية",
              f"{out['p_asy']:.3f}" if np.isfinite(out["p_asy"]) else "لا جدول")
    df = DF_MAP.get(tsel)
    cv_asy = sps.chi2.ppf(0.95, df) if df else np.nan
    m4.metric("القيمة الحرجة 5٪ — بوتستراب", f"{out['crit95']:.3f}",
              delta=f"{out['crit95'] - cv_asy:+.3f} مقابل χ²({df})"
              if df else None)

    # تراكب التوزيعين
    bs = out["boot"]
    kde = sps.gaussian_kde(bs)
    hi = float(np.quantile(bs, 0.995))
    if df:
        hi = max(hi, sps.chi2.ppf(0.995, df))
    g = np.linspace(0.01, hi, 250)

    f2 = go.Figure()
    f2.add_trace(go.Scatter(x=g, y=kde(g), mode="lines", name="توزيع البوتستراب",
                            line=dict(color=PALETTE["teal"], width=3.4),
                            fill="tozeroy", fillcolor="rgba(20,184,166,.13)"))
    if df:
        f2.add_trace(go.Scatter(x=g, y=sps.chi2.pdf(g, df), mode="lines",
                                name=f"التوزيع التقاربي χ²({df})",
                                line=dict(color=PALETTE["rose"], width=3.4,
                                          dash="dash")))
        f2.add_vline(x=cv_asy, line=dict(color=PALETTE["rose"], width=2,
                                         dash="dot"),
                     annotation_text="حرجة χ²", annotation_position="top right")
    f2.add_vline(x=out["crit95"], line=dict(color=PALETTE["teal"], width=2,
                                            dash="dot"),
                 annotation_text="حرجة بوتستراب", annotation_position="top left")
    f2.add_vline(x=out["stat"], line=dict(color=PALETTE["violet"], width=3),
                 annotation_text="إحصاؤك", annotation_position="bottom right")
    f2.update_layout(height=430, margin=dict(l=40, r=30, t=60, b=50),
                     title=dict(text="أين تقع القيمة الحرجة فعلاً؟",
                                x=0.98, xanchor="right"),
                     legend=dict(orientation="h", y=1.1, x=0),
                     xaxis=dict(title="قيمة الإحصاء", gridcolor="#E9EFF9"),
                     yaxis=dict(title="الكثافة", gridcolor="#E9EFF9"))
    plotly(f2, key="bt_overlay")

    if df and np.isfinite(cv_asy):
        gap = out["crit95"] - cv_asy
        if gap > 0.3:
            st.error(
                f"القيمة الحرجة الحقيقية أعلى من جدول χ² بمقدار **{gap:.2f}**. "
                f"أي أنّ الاختبار التقاربي **يُفرط في الرفض**: سيُعلن وجود "
                f"مشكلة في نموذجك أكثر ممّا ينبغي."
            )
        elif gap < -0.3:
            st.info(
                f"القيمة الحرجة الحقيقية أقل من جدول χ² بمقدار **{abs(gap):.2f}**. "
                f"أي أنّ الاختبار التقاربي **ناقص الحجم**: سيتجاهل مشاكل حقيقية."
            )
        else:
            st.success(
                "القيمتان متقاربتان في هذا الإعداد — التقريب التقاربي جيّد هنا. "
                "جرّب رفع ρ أو خفض n لترى الانهيار."
            )

    plotly(
        anim_build_distribution(bs, out["stat"], steps=22,
                                title="التوزيع الصفري البوتستراب يُبنى",
                                color="teal"),
        key="bt_build",
    )

st.divider()
st.markdown(
    "**الصفحة التالية:** الاستقرار الهيكلي — أخطر عائلة من الاختبارات، "
    "وأكثرها احتياجاً للبوتستراب."
)
