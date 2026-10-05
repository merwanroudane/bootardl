"""الوايلد بوتستراب بالتفصيل."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.ui import hero, card, note, plotly, table, steps, PALETTE, SOFT
from core.anim import anim_wild, anim_build_distribution
from core.engine import (simulate_dgp, design_from, ols, wild_weights,
                         run_boot_test)

hero(
    "الوايلد بوتستراب — The Wild Bootstrap",
    "النوع الأكثر استعمالاً في الاقتصاد القياسي الحديث، والافتراضي في معظم "
    "الحزم الجادّة. سنفكّكه بالكامل: من أين جاء الاسم، ما الصيغة، "
    "لماذا يعمل، وما هي الخيارات الأربعة التي عليك ضبطها.",
    "النوع الأهم · بالتفصيل",
    "#E0F7F4", "#F2ECFE",
)

# ============================================================== 1. المشكلة
st.header("١. المشكلة التي وُجد الوايلد لحلّها")

card(
    "عدم تجانس التباين مجهول الشكل",
    "<p>في أغلب البيانات الاقتصادية، تباين الخطأ ليس ثابتاً: "
    "الدول الكبيرة تتذبذب أكثر من الصغيرة، فترات الأزمات أكثر تقلّباً من "
    "فترات الهدوء. هذا هو <b>عدم تجانس التباين</b> "
    "(<span class='bs-en'>heteroskedasticity</span>).</p>"
    "<p>المشكلة الأعمق: نحن لا نعرف <b>شكل</b> هذا التباين. "
    "هل هو <span dir='ltr'>σ²_t = exp(x_t γ)</span>؟ أم "
    "<span dir='ltr'>σ²_t = x²_t</span>؟ لا نعرف.</p>"
    "<p>وهنا المعضلة: <b>بوتستراب البواقي الحرّ يُدمّر هذه المعلومة.</b> "
    "إذا سحبتَ البواقي بحرّية فقد خلطتَ باقياً كبيراً من فترة أزمة مع "
    "مشاهدة من فترة هدوء — فأصبحت عيّنتك الاصطناعية متجانسة التباين "
    "بينما بياناتك ليست كذلك.</p>"
    "<p><b>فكرة الوايلد العبقرية:</b> لا تُحرّك الباقي من مكانه إطلاقاً. "
    "<b>اقلب إشارته فقط.</b></p>",
    "teal",
)

st.subheader("الصيغة")

st.latex(r"y^*_t \;=\; X_t\,\tilde{\beta} \;+\; f(\tilde{u}_t)\cdot \varepsilon^*_t"
         r"\qquad\text{with}\quad E(\varepsilon^*)=0,\;\; E(\varepsilon^{*2})=1")

st.markdown(
    "- <span dir='ltr'>β̃</span> هي المعالم المقدّرة **تحت الفرضية الصفرية** "
    "(مقيّدة — <span dir='ltr'>restricted</span>).\n"
    "- <span dir='ltr'>f(ũ_t)</span> هو الباقي بعد تحويله "
    "(<span dir='ltr'>HC0…HC3</span> — انظر القسم ٤).\n"
    "- <span dir='ltr'>ε*_t</span> هو **الوزن العشوائي المساعد** — "
    "القسم ٣ مخصّص له بالكامل.\n\n"
    "لاحظ أنّ الدليل <span dir='ltr'>t</span> ثابت: الباقي رقم 17 يبقى في "
    "الموضع 17 دائماً. هذا هو مفتاح كل شيء."
)

note(
    "<b>من أين الاسم «Wild»؟</b> صاغه "
    "<span class='bs-en'>Härdle &amp; Mammen (1993)</span> عندما استعملوه "
    "لمقارنة الانحدار المعلمي باللامعلمي، ووصفوا السلوك «المتوحّش» للأوزان "
    "المساعدة التي تُقلب إشارتها عشوائياً. أمّا الأصل التقني فيعود إلى "
    "<span class='bs-en'>Wu (1986)</span> و<span class='bs-en'>Liu (1988)</span>، "
    "والتأسيس النظري في النماذج الخطّية عالية الأبعاد إلى "
    "<span class='bs-en'>Mammen (1993)</span>.",
    "violet", "📜",
)

# ============================================================== 2. الأنيميشن
st.header("٢. شاهد قلب الإشارات")

st.markdown(
    "كل عمود هو باقٍ واحد. الإطار الأول هو بواقيك الأصلية. ثم كل إطار جديد "
    "يضرب كل باقٍ في وزن ±1 جديد. اضغط **▶ تشغيل**."
)

c1, c2 = st.columns([3, 1])
with c2:
    wsel = st.radio("توزيع الأوزان", ["rademacher", "mammen", "normal"],
                    format_func=lambda s: {"rademacher": "F2 — Rademacher",
                                           "mammen": "F1 — Mammen",
                                           "normal": "N(0,1)"}[s],
                    key="w_dist")
    het_lvl = st.slider("شدّة عدم تجانس التباين", 0.0, 0.8, 0.5, 0.1,
                        key="w_het")
with c1:
    rngw = np.random.default_rng(23)
    dw = simulate_dgp(55, 0.4, 1.0, float(het_lvl), "normal", 0.0, rngw)
    yw, Xw = design_from(dw["y"], dw["x"])
    uw = ols(yw, Xw)["u"]
    plotly(anim_wild(uw, wsel, draws=10, seed=31), key="w_anim")

note(
    "راقب المحور الرأسي: <b>ارتفاع كل عمود لا يتغيّر أبداً</b> مع "
    "<span dir='ltr'>Rademacher</span> — فقط لونه واتجاهه. "
    "وهذا يعني أنّ العيّنات الاصطناعية تحمل نمط التقلّب نفسه الموجود في "
    "بياناتك، مهما كان شكله. ارفع شريط «شدّة عدم تجانس التباين» وستراه بوضوح: "
    "المناطق العالية تبقى عالية.",
    "teal", "🎯",
)

# ============================================================== 3. الأوزان
st.header("٣. التوزيعان المساعدان: F1 و F2")

st.markdown(
    "لكي يعمل الوايلد، يكفي أن يحقّق الوزن <span dir='ltr'>ε*</span> شرطين: "
    "متوسّطه صفر وتباينه واحد. لكن هناك خياران مشهوران، وبينهما نقاش محسوم:"
)

c1, c2 = st.columns(2)

with c1:
    card(
        "F2 — Rademacher (الافتراضي)",
        "<p style='direction:ltr;text-align:center;font-family:monospace;"
        "background:#fff;padding:10px;border-radius:8px'>"
        "ε* = +1 with prob. 1/2<br>ε* = −1 with prob. 1/2</p>"
        "<p>بسيط للغاية: اقلب عملة معدنية.</p>"
        "<ul>"
        "<li><span dir='ltr'>E(ε*) = 0</span> ✓</li>"
        "<li><span dir='ltr'>E(ε*²) = 1</span> ✓</li>"
        "<li><span dir='ltr'>E(ε*³) = 0</span> — <b>لا يُصحّح الالتواء</b></li>"
        "</ul>",
        "teal",
    )
with c2:
    card(
        "F1 — Mammen (1993)",
        "<p style='direction:ltr;text-align:center;font-family:monospace;"
        "background:#fff;padding:10px;border-radius:8px;font-size:.88em'>"
        "ε* = −(√5−1)/2 ≈ −0.618  w.p. (√5+1)/(2√5) ≈ 0.724<br>"
        "ε* = +(√5+1)/2 ≈ +1.618  w.p. (√5−1)/(2√5) ≈ 0.276</p>"
        "<p>توزيع ثنائي النقطة غير متماثل، مبني على النسبة الذهبية.</p>"
        "<ul>"
        "<li><span dir='ltr'>E(ε*) = 0</span> ✓</li>"
        "<li><span dir='ltr'>E(ε*²) = 1</span> ✓</li>"
        "<li><span dir='ltr'>E(ε*³) = 1</span> — <b>يُصحّح الالتواء</b></li>"
        "</ul>",
        "violet",
    )

# رسم التوزيعين
fig = go.Figure()
fig.add_trace(go.Bar(x=[-1, 1], y=[0.5, 0.5], name="F2 — Rademacher",
                     marker_color=PALETTE["teal"], width=0.14,
                     text=["½", "½"], textposition="outside"))
a = (np.sqrt(5) - 1) / 2
b = (np.sqrt(5) + 1) / 2
pb = (np.sqrt(5) - 1) / (2 * np.sqrt(5))
fig.add_trace(go.Bar(x=[-a, b], y=[1 - pb, pb], name="F1 — Mammen",
                     marker_color=PALETTE["violet"], width=0.14,
                     text=[f"{1-pb:.3f}", f"{pb:.3f}"], textposition="outside"))
fig.update_layout(height=340, barmode="group", bargap=0.3,
                  title=dict(text="أين تقع كتلة الاحتمال في كل توزيع؟",
                             x=0.98, xanchor="right"),
                  margin=dict(l=40, r=30, t=60, b=40),
                  legend=dict(orientation="h", y=1.12, x=0),
                  xaxis=dict(title="قيمة الوزن ε*", gridcolor="#E9EFF9",
                             range=[-1.5, 2.1]),
                  yaxis=dict(title="الاحتمال", gridcolor="#E9EFF9",
                             range=[0, 0.92]))
plotly(fig, key="w_weights")

card(
    "🏆 الحكم المحسوم — Davidson &amp; Flachaire",
    "<p>عبر تمديدات <span class='bs-en'>Edgeworth</span> حتى الرتبة "
    "<span dir='ltr'>O(n⁻¹)</span> ومحاكاة واسعة، خلصا إلى أنّ:</p>"
    "<p style='text-align:center;color:#0F766E;font-weight:700'>"
    "F2 (Rademacher) + بواقي مقيّدة + HC3<br>"
    "«يجب أن تُستعمل دائماً في الممارسة تفضيلاً على الصيغ الأخرى»</p>"
    "<ul>"
    "<li>معدّل خطأ الرفض <span dir='ltr'>ERP</span> يبلغ "
    "<span dir='ltr'>n^(−3/2)</span> مع أخطاء متماثلة، "
    "و<span dir='ltr'>n^(−1/2)</span> مع أخطاء ملتوية.</li>"
    "<li>F2 يتفوّق <b>حتى مع أخطاء ملتوية</b> من نوع "
    "<span dir='ltr'>χ²(2)</span>، رغم أنّه لا يُصحّح الالتواء.</li>"
    "<li>المشاهدات عالية الرافعة تأثيرها ضئيل على F2.</li>"
    "</ul>",
    "green",
)

with st.expander("🔬 نتيجة نظرية مذهلة: الاستدلال المضبوط (Theorem 3)"):
    st.markdown(
        "إذا تحقّقت الشروط التالية معاً:\n\n"
        "1. الفرضية الصفرية هي أنّ **كل** متّجه <span dir='ltr'>β = 0</span>،\n"
        "2. الأخطاء **متماثلة** حول الصفر ومستقلّة،\n"
        "3. استُعملت البواقي **المقيّدة** في كلٍّ من مقدّر HCCME وعملية توليد "
        "البوتستراب،\n\n"
        "فإنّ إحصاء <span dir='ltr'>χ²</span> ونظيره في الوايلد بوتستراب "
        "بأوزان F2 لهما **التوزيع نفسه بالضبط** شرطياً على "
        "<span dir='ltr'>|u_t|</span>، وتكون قيمة p البوتستراب **منتظمة تماماً** "
        "على المجموعة <span dir='ltr'>{i/2ⁿ}</span>.\n\n"
        "**البرهان ببساطة:** تحت F2 يكون "
        "<span dir='ltr'>u*_t = ±u_t</span>، إذن "
        "<span dir='ltr'>|u*_t| = |u_t|</span>، ومتّجه الإشارات "
        "<span dir='ltr'>s</span> له التوزيع نفسه الذي لـ "
        "<span dir='ltr'>ε*</span>. أي أنّ البوتستراب هنا ليس تقريباً — "
        "إنّه **استدلال مضبوط**.\n\n"
        "⚠️ **تحذير مهم للتطبيق:** مجالات الثقة التقليدية **لا تستطيع** "
        "استعمال هذه النسخة، لأنّها ضمنياً اختبارات Wald ببواقي **غير مقيّدة**. "
        "للحصول على مجالات ثقة موثوقة يجب **قلب مجموعة من اختبارات الوايلد F2** "
        "(<span dir='ltr'>test inversion</span>)."
    )

# ============================================================== 4. HCCME
st.header("٤. تحويل البواقي: HC0 حتى HC3")

st.markdown(
    "قبل ضرب الباقي في الوزن، نُحوّله لتعويض كونه أصغر تبايناً من الخطأ الحقيقي. "
    "هذه هي عائلة <span dir='ltr'>HCCME</span> — "
    "<span class='bs-en'>Heteroskedasticity-Consistent Covariance Matrix Estimator</span>، "
    "من White (1980) و MacKinnon & White (1985). الصيغة العامة: "
    "<span dir='ltr'>a_t · û_t</span> حيث:"
)

table(
    ["الصيغة", "المُعامل <span dir='ltr'>a_t</span>", "الفكرة", "الحكم"],
    [
        ["<code>HC0</code>", "<span dir='ltr'>1</span>",
         "لا تحويل — White (1980) الأصلي",
         "<span style='color:#E8536B'>الأضعف</span>: متحيّز للأسفل في العيّنات الصغيرة"],
        ["<code>HC1</code>", "<span dir='ltr'>√(n/(n−k))</span>",
         "تصحيح درجات الحرّية فقط", "أفضل قليلاً، لا يزال ضعيفاً"],
        ["<code>HC2</code>", "<span dir='ltr'>(1−h_t)^(−1/2)</span>",
         "يُصحّح بالرافعة — المشاهدات الجاذبة تُضخَّم",
         "<span style='color:#10B981'>جيّد</span>"],
        ["<code>HC3</code>", "<span dir='ltr'>(1−h_t)^(−1)</span>",
         "تصحيح رافعة أقوى، يُقارب حذف المشاهدة (jackknife)",
         "<span style='color:#10B981'><b>الأفضل عادةً — الافتراضي</b></span>"],
    ],
)

st.markdown(
    "حيث <span dir='ltr'>h_t = x_t(X'X)⁻¹x'_t</span> هي **الرافعة** "
    "(<span class='bs-en'>leverage</span>) للمشاهدة t: مقدار قدرتها على جذب "
    "خط الانحدار نحوها. الترتيب المستقر: "
    "<span dir='ltr'>HC0 ≺ HC1 ≺ {HC2, HC3}</span>."
)

# عرض الرافعة
r = ols(yw, Xw)
figh = go.Figure()
figh.add_trace(go.Bar(x=np.arange(len(r["h"])), y=r["h"],
                      marker_color=[PALETTE["rose"] if hh > 2 * Xw.shape[1] / len(r["h"])
                                    else PALETTE["blue"] for hh in r["h"]],
                      name="الرافعة h_t"))
figh.add_hline(y=2 * Xw.shape[1] / len(r["h"]),
               line=dict(color=PALETTE["amber"], dash="dash", width=2),
               annotation_text="عتبة التنبيه 2k/n", annotation_position="top left")
figh.update_layout(height=300, margin=dict(l=40, r=30, t=50, b=40),
                   title=dict(text="الرافعة في العيّنة المولّدة أعلاه",
                              x=0.98, xanchor="right"),
                   showlegend=False,
                   xaxis=dict(title="المشاهدة t", gridcolor="#E9EFF9"),
                   yaxis=dict(title="h_t", gridcolor="#E9EFF9"))
plotly(figh, key="w_lev")

note(
    "المشاهدات الوردية رافعتها فوق العتبة: هي التي تُفسد اختباراتك إن لم "
    "تُصحّح بـ <span dir='ltr'>HC3</span>.",
    "amber", "📍",
)

# ============================================================== 5. مقيّد
st.header("٥. البواقي المقيّدة مقابل غير المقيّدة")

c1, c2 = st.columns(2)
with c1:
    card(
        "مقيّدة — Restricted (الصحيحة للاختبار)",
        "<p>نُقدّر النموذج <b>تحت الفرضية الصفرية</b> ونأخذ بواقيه. "
        "مثال: لاختبار الارتباط الذاتي، نُقدّر النموذج بلا حدود ارتباط ذاتي.</p>"
        "<p><b>لماذا؟</b> لأنّ عالم البوتستراب يجب أن يكون عالماً "
        "<b>تصدق فيه الصفرية</b>. فإذا استعملت بواقي غير مقيّدة فقد أدخلتَ "
        "أثر البديلة في توزيعك «الصفري».</p>"
        "<p>الإجماع هنا واسع: Davidson &amp; Flachaire، Godfrey &amp; Tremayne، "
        "Flachaire، Davidson &amp; MacKinnon.</p>",
        "green",
    )
with c2:
    card(
        "غير مقيّدة — Unrestricted",
        "<p>نُقدّر النموذج الكامل (تحت البديلة) ونأخذ بواقيه.</p>"
        "<p><b>متى تكون صحيحة؟</b> لمجالات الثقة والأخطاء المعيارية — "
        "لأنّك هناك لا تختبر فرضية بل تُقدّر تذبذباً.</p>"
        "<p><b>الحجّة المضادّة:</b> Mantalos يُظهر أنّ البوتستراب غير المقيّد "
        "له <b>قوّة أعلى</b> في العيّنات الصغيرة حتى بعد تعديل الحجم. "
        "فالمقايضة حقيقية: حجم أدقّ مقابل قوّة أعلى.</p>",
        "amber",
    )

# ============================================================== 6. التطبيق
st.header("٦. جرّبه الآن على بيانات حقيقية مُولّدة")

st.markdown(
    "النموذج: <span dir='ltr'>y_t = c + ρ·y_{t−1} + β·x_t + u_t</span> "
    "مع تباين متغيّر. اختر الإعدادات وشاهد كيف يتغيّر التوزيع الصفري."
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    n_w = st.slider("حجم العيّنة n", 30, 250, 70, key="w_n")
with c2:
    het_w = st.slider("شدّة عدم التجانس", 0.0, 0.8, 0.4, 0.1, key="w_het2")
with c3:
    wt_w = st.selectbox("توزيع الأوزان", ["rademacher", "mammen", "normal"],
                        key="w_wt")
with c4:
    ft_w = st.selectbox("التحويل", ["hc3", "hc2", "hc1", "hc0"], key="w_ft")

if st.button("▶  شغّل اختبار Breusch–Godfrey بالوايلد بوتستراب",
             type="primary", key="w_run"):
    with st.spinner("جارٍ تنفيذ 999 تكرار…"):
        rr = np.random.default_rng(77)
        dd = simulate_dgp(int(n_w), 0.5, 1.0, float(het_w), "normal", 0.0, rr)
        yy, XX = design_from(dd["y"], dd["x"])
        out = run_boot_test("bg_hr", yy, XX, B=999, dgp="wild",
                            weight=wt_w, ftrans=ft_w, q=2, seed=77)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("الإحصاء LM_HR", f"{out['stat']:.3f}")
    m2.metric("قيمة p — بوتستراب", f"{out['p_boot']:.3f}")
    m3.metric("قيمة p — تقاربية χ²(2)", f"{out['p_asy']:.3f}")
    m4.metric("القيمة الحرجة 5٪ — بوتستراب", f"{out['crit95']:.3f}",
              delta=f"{out['crit95'] - 5.991:+.3f} مقابل χ²")
    plotly(
        anim_build_distribution(
            out["boot"], out["stat"], steps=22,
            title="التوزيع الصفري المولّد بالوايلد بوتستراب",
            color="teal"),
        key="w_res",
    )
    st.caption(
        "قارن القيمة الحرجة البوتستراب بقيمة χ²(2) عند 5٪ وهي 5.991. "
        "الفرق بينهما هو بالضبط مقدار الخطأ الذي كنت سترتكبه لو استعملت الجدول."
    )

st.divider()
st.markdown(
    "**الصفحة التالية:** كيف تُحسب قيمة p بالضبط، وكم تكراراً تحتاج، "
    "ولماذا العدد 999 وليس 1000."
)
