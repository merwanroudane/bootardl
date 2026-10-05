"""قيمة p البوتستراب وعدد التكرارات B."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.ui import hero, card, note, plotly, table, steps, PALETTE
from core.anim import anim_pvalue_stability

hero(
    "قيمة p البوتستراب وعدد التكرارات B",
    "هنا التفاصيل التقنية التي تفصل بين تطبيق صحيح وتطبيق يبدو صحيحاً. "
    "الصيغ الأربع لقيمة p، سرّ العدد 999، تصحيح +1 الذي يجعل الاختبار مضبوطاً، "
    "وكيف تُقلّل التكلفة الحاسوبية دون أن تخسر دقّة.",
    "التفاصيل الحاسمة",
    "#FEF4E2", "#E8F0FE",
)

# ============================================================== 1. الصيغ
st.header("١. الصيغ الأربع لقيمة p")

st.markdown(
    "لديك إحصاؤك <span dir='ltr'>τ̂</span> و B قيمة بوتستراب "
    "<span dir='ltr'>τ*₁ … τ*_B</span>. المرجع هنا هو "
    "<span class='bs-en'>MacKinnon (2007)</span>."
)

c1, c2 = st.columns(2)
with c1:
    card(
        "أ) الذيل الأعلى — Upper tail",
        r"<p style='direction:ltr;text-align:center'>"
        r"p̂ = (1/B) · Σ<sub>j</sub> I(τ*<sub>j</sub> &gt; τ̂)</p>"
        "<p>«ما نسبة قيم البوتستراب التي تجاوزت إحصائي؟»</p>"
        "<p><b>استعملها عندما</b> يكون الإحصاء يرفض عند القيم الكبيرة فقط: "
        "كل إحصاءات <span dir='ltr'>LM</span> و<span dir='ltr'>χ²</span> "
        "و<span dir='ltr'>F</span> و<span dir='ltr'>supF</span>. "
        "وهذه هي الحالة الغالبة في الاختبارات البعدية.</p>",
        "blue",
    )
    card(
        "ج) الذيلان المتساويان — Equal-tail",
        r"<p style='direction:ltr;text-align:center;font-size:.95em'>"
        r"p̂<sub>et</sub> = 2·min[ (1/B)ΣI(τ*≤τ̂), (1/B)ΣI(τ*&gt;τ̂) ]</p>"
        "<p>نحسب الذيلين منفصلين ونأخذ ضِعف الأصغر.</p>"
        "<p><b>استعملها عندما</b> يكون التوزيع الصفري <b>غير متماثل</b> "
        "ويمكن الرفض من الجهتين. المثال الكلاسيكي: "
        "<span class='bs-en'>Durbin–Watson</span> حيث القيم القريبة من 0 "
        "تعني ارتباطاً موجباً والقريبة من 4 ارتباطاً سالباً.</p>",
        "amber",
    )
with c2:
    card(
        "ب) المتماثلة — Symmetric two-tailed",
        r"<p style='direction:ltr;text-align:center'>"
        r"p̂<sub>s</sub> = (1/B) · Σ<sub>j</sub> I(|τ*<sub>j</sub>| &gt; |τ̂|)</p>"
        "<p>نقارن القيم المطلقة.</p>"
        "<p><b>استعملها عندما</b> يكون الإحصاء من نوع "
        "<span dir='ltr'>t</span> والتوزيع الصفري متماثلاً تقريباً. "
        "أدقّ من الذيلين المتساويين في هذه الحالة.</p>",
        "teal",
    )
    card(
        "د) مونت كارلو المضبوطة — Exact MC",
        r"<p style='direction:ltr;text-align:center;font-size:.95em'>"
        r"p̂<sub>N</sub>(S₀) = (N·Ĝ<sub>N</sub>(S₀) + 1)/(N + 1)</p>"
        "<p>لاحظ <b>+1 في البسط و+1 في المقام</b>. هذا ليس تجميلاً — "
        "هو ما يجعل الاختبار <b>مضبوطاً تماماً</b> في العيّنات المنتهية "
        "عندما يكون الإحصاء محورياً (Dufour et al. 2004، §4).</p>"
        "<p>الشرط: أن يكون <span dir='ltr'>α(N+1)</span> عدداً صحيحاً.</p>",
        "violet",
    )

note(
    "<b>خاصية جميلة ومفيدة جداً:</b> قيم p البوتستراب <b>ثابتة تحت التحويلات "
    "الرتيبة</b> للإحصاء. أي أنّ اختبار <span dir='ltr'>F</span> بالبوتستراب "
    "واختبار <span dir='ltr'>LR</span> بالبوتستراب على <b>نفس</b> عملية التوليد "
    "يُعطيان <b>النتيجة ذاتها حرفياً</b>. "
    "لذلك <span dir='ltr'>BootSupW ≡ BootSupLR ≡ BootSupLM</span> "
    "(Diebold &amp; Chen 1996). لكن انتبه: هذا <b>لا ينطبق</b> على "
    "<span dir='ltr'>BootExp</span> و<span dir='ltr'>BootAve</span>، "
    "لأنّهما ليسا تحويلين رتيبين.",
    "green", "✨",
)

# ============================================================== 2. سر 999
st.header("٢. سرّ العدد 999 — ولماذا ليس 1000")

card(
    "شرط العدد الصحيح: <span dir='ltr'>α(B+1) ∈ ℕ</span>",
    "<p>لكي يكون الاختبار مضبوطاً، يجب أن يكون "
    "<span dir='ltr'>α(B+1)</span> عدداً صحيحاً. السبب بديهي حين تراه: "
    "عندك <span dir='ltr'>B+1</span> قيمة في المجموع "
    "(قيم البوتستراب B زائد إحصاؤك أنت). ولكي تقتطع منها بالضبط "
    "النسبة <span dir='ltr'>α</span> يجب أن يكون العدد قابلاً للقسمة.</p>"
    "<table class='bs-table' style='margin-top:10px'>"
    "<tr><th>α</th><th>B المناسب</th><th>α(B+1)</th><th>الحكم</th></tr>"
    "<tr><td>0.05</td><td>99</td><td>5</td><td style='color:#10B981'>✓ صحيح</td></tr>"
    "<tr><td>0.05</td><td>199</td><td>10</td><td style='color:#10B981'>✓ صحيح</td></tr>"
    "<tr><td>0.05</td><td>999</td><td>50</td><td style='color:#10B981'>✓ صحيح</td></tr>"
    "<tr><td>0.05</td><td><b>1000</b></td><td>50.05</td>"
    "<td style='color:#E8536B'>✗ ليس صحيحاً</td></tr>"
    "<tr><td>0.01</td><td>999</td><td>10</td><td style='color:#10B981'>✓ صحيح</td></tr>"
    "<tr><td>0.01</td><td>1499</td><td>15</td><td style='color:#10B981'>✓ صحيح</td></tr>"
    "</table>"
    "<p>لهذا تجد في كل الأوراق الجادّة الأعداد 99، 199، 399، 999، 1999، 12799 "
    "— وليس 100 أو 1000 أو 5000.</p>",
    "amber",
)

# ============================================================== 3. كم B
st.header("٣. كم تكراراً تحتاج فعلاً؟")

st.markdown(
    "<span class='bs-en'>Davidson &amp; MacKinnon</span> (ورقة «كم بوتستراب؟») "
    "أثبتا أنّ فقدان القوّة الناتج عن B محدود يتناسب تقريباً مع "
    "<span dir='ltr'>(B+1)⁻¹</span> في الحالات العادية — "
    "وهذا أفضل بكثير من حدّ <span class='bs-en'>Jöckel</span> المتحفّظ "
    "<span dir='ltr'>(B+1)^(−1/2)</span>.",
    unsafe_allow_html=True,
)

table(
    ["المستوى α", "الحدّ الأدنى لإبقاء فقدان القوّة تحت 1٪", "التوصية العملية"],
    [
        ["0.10", "<b>B ≥ 199</b>", "399"],
        ["0.05", "<b>B ≥ 399</b>", "<b style='color:#10B981'>999</b> — القيمة الافتراضية المعقولة"],
        ["0.01", "<b>B ≥ 1499</b>", "1999 أو أكثر"],
        ["للنشر في مجلّة محكّمة", "—", "1999 فأعلى، واذكر العدد صراحةً"],
    ],
)

st.subheader("شاهد تبعثر قيمة p مع B الصغيرة")

st.markdown(
    "في الرسم التالي: 40 باحثاً يُجرون **نفس** الاختبار على **نفس** البيانات، "
    "والفرق الوحيد بينهم هو البذرة العشوائية. اضغط **▶ تشغيل** وراقب كيف "
    "تتجمّع النقاط كلّما زاد B."
)

rngp = np.random.default_rng(55)
boot_demo = rngp.chisquare(2, 6000)
plotly(anim_pvalue_stability(4.4, boot_demo), key="pv_stab")

note(
    "عند <span dir='ltr'>B = 19</span> يحصل بعض الباحثين على "
    "<span dir='ltr'>p = 0.00</span> وآخرون على "
    "<span dir='ltr'>p = 0.26</span> — من البيانات نفسها! "
    "وعند <span dir='ltr'>B = 1499</span> يتفقون جميعاً. "
    "<b>هذا هو السبب الوحيد لاختيار B كبيرة</b>: ليس لأنّ قيمة p تصبح "
    "«أصحّ»، بل لأنّها تصبح <b>قابلة للتكرار</b>.",
    "rose", "🎲",
)

# ============================================================== 4. حيل
st.header("٤. ثلاث حيل لخفض التكلفة الحاسوبية")

st.subheader("أ) قيمة p المتّصلة — Racine & MacKinnon (2007)")

card(
    "تحرّر من شرط العدد الصحيح تماماً",
    r"<p style='direction:ltr;text-align:center;font-size:1.1em'>"
    r"P<sup>c</sup><sub>B</sub> = (N + U)/(B + 1),&nbsp;&nbsp; U ~ Uniform[0,1]</p>"
    "<p>نضيف سحبة عشوائية واحدة <span dir='ltr'>U</span> من التوزيع المنتظم. "
    "النتيجة مذهلة: قيمة p هذه <b>منتظمة تماماً على [0,1] تحت الفرضية الصفرية "
    "لأي B منتهٍ مهما صغر</b>.</p>"
    "<ul>"
    "<li>تُزيل قيد <span dir='ltr'>α(B+1) ∈ ℕ</span> نهائياً.</li>"
    "<li>تُعطي استدلالاً مطابقاً تماماً حين يكون القيد محقّقاً أصلاً.</li>"
    "<li>مفيدة جداً حين يكون كل تكرار باهظ الثمن حاسوبياً.</li>"
    "</ul>"
    "<p><b>للمقارنة:</b> قيمة p التجريبية الساذجة "
    "<span dir='ltr'>N/B</span> <b>تُفرط في الرفض</b> عند B صغيرة، "
    "وصيغة Davison–Hinkley <span dir='ltr'>(N+1)/(B+1)</span> "
    "<b>تُفرّط في عدم الرفض</b> ولا تستطيع الرفض إطلاقاً إذا كانت B أصغر من "
    "حدّ أدنى معيّن.</p>",
    "cyan",
)

st.subheader("ب) الاختيار بالاختبار المسبق — Pretest algorithm")

steps([
    "ابدأ بـ <span dir='ltr'>B = B_min = 99</span>.",
    "احسب قيمة p. اختبر إحصائياً: هل هي أبعد من α بما يكفي لتحسم الأمر، "
    "عند مستوى اختبار مسبق β؟",
    "إذا حُسم الأمر (p بعيدة عن α بوضوح) — <b>توقّف</b>. لا داعي لمزيد من الحساب.",
    "إذا لم يُحسم، ضاعِف: <span dir='ltr'>B ← 2B+1</span>، "
    "واسحب <span dir='ltr'>B+1</span> عيّنة إضافية. لاحظ أنّ هذا يُبقي "
    "<span dir='ltr'>α(B+1)</span> عدداً صحيحاً في كل مرحلة.",
    "توقّف عند <span dir='ltr'>B_max = 12,799</span>. "
    "القيم الموصى بها: <span dir='ltr'>β = 0.01</span> أو "
    "<span dir='ltr'>0.001</span>.",
])

note(
    "هذه الخوارزمية <b>تتفوّق على B ثابتة عند نفس التكلفة الحاسوبية المتوقّعة</b>. "
    "المنطق بسيط: إذا كانت قيمة p هي 0.78، فلا حاجة لآلاف التكرارات لتأكيد "
    "أنّها ليست أقل من 0.05. وفّر الحساب للحالات الحدّية فقط. "
    "متاحة في bootdiag بالخيار "
    "<code style='direction:ltr'>fdb, pretest</code>.",
    "teal", "⚡",
)

st.subheader("ج) البوتستراب المزدوج السريع — Fast Double Bootstrap (FDB)")

card(
    "دقّة أعلى بتكلفة <span dir='ltr'>2B+1</span> بدل <span dir='ltr'>B(B+1)</span>",
    "<p>البوتستراب المزدوج الكامل يعني: لكل عيّنة بوتستراب، شغّل بوتستراباً "
    "كاملاً آخر. التكلفة <span dir='ltr'>B × B</span> — أي مليون إحصاء عند "
    "<span dir='ltr'>B = 1000</span>. غير عملي.</p>"
    "<p><b>حيلة Davidson &amp; MacKinnon (2007):</b> احسب إحصاءً واحداً فقط من "
    "المستوى الثاني لكل عيّنة من المستوى الأول. الخطوات:</p>"
    "<ol style='padding-right:20px'>"
    "<li>احسب <span dir='ltr'>p̂</span> بالبوتستراب العادي.</li>"
    "<li>احسب <span dir='ltr'>Q̂*_B(1−p̂)</span> — "
    "المئين المقابل من توزيع المستوى الثاني.</li>"
    "<li>قيمة p النهائية: "
    "<span dir='ltr'>p̂_F = (1/B) Σ I(τ*_j &gt; Q̂*_B(1−p̂))</span>.</li>"
    "</ol>"
    "<p><b>الشرط:</b> أن يكون الإحصاء مستقلاً تقاربياً عن عملية توليد البوتستراب "
    "— وهذا يتحقّق لبوتستراب البواقي والوايلد المقدّرَين تحت الصفرية، "
    "وهما بالضبط ما نستعمله.</p>"
    "<p><b>النتيجة:</b> رتبة خطأ الرفض ERP تنزل مرتبة إضافية. "
    "مفيد جداً حين تشكّ أنّ البوتستراب الأول لم يُصلح المشكلة كاملةً.</p>",
    "pink",
)

# ============================================================== 5. حاسبة
st.header("٥. حاسبة سريعة")

c1, c2, c3 = st.columns(3)
with c1:
    alpha_c = st.selectbox("المستوى α", [0.10, 0.05, 0.01], index=1, key="pv_a")
with c2:
    B_c = st.number_input("عدد التكرارات B", 9, 50000, 999, key="pv_B")
with c3:
    N_c = st.number_input("عدد قيم البوتستراب التي تجاوزت إحصاءك (N)",
                          0, 50000, 23, key="pv_N")

N_c = min(int(N_c), int(B_c))
valid = abs(alpha_c * (B_c + 1) - round(alpha_c * (B_c + 1))) < 1e-9
p_naive = N_c / B_c
p_mc = (N_c + 1) / (B_c + 1)
p_dh = (N_c + 1) / (B_c + 1)
p_cont = (N_c + np.random.default_rng(int(N_c) + int(B_c)).random()) / (B_c + 1)

m1, m2, m3, m4 = st.columns(4)
m1.metric("p — التجريبية البسيطة", f"{p_naive:.4f}")
m2.metric("p — مونت كارلو (+1)", f"{p_mc:.4f}")
m3.metric("p — المتّصلة", f"{p_cont:.4f}")
m4.metric("α(B+1)", f"{alpha_c*(B_c+1):.2f}",
          delta="عدد صحيح ✓" if valid else "ليس صحيحاً ✗",
          delta_color="normal" if valid else "inverse")

if not valid:
    st.warning(
        f"القيمة α(B+1) = {alpha_c*(B_c+1):.2f} ليست عدداً صحيحاً. "
        f"أقرب قيمة صالحة لـ B هي "
        f"**{int(round(alpha_c*(B_c+1))/alpha_c) - 1}**. "
        f"أو استعمل قيمة p المتّصلة التي لا تحتاج هذا الشرط."
    )
else:
    st.success(f"α(B+1) = {int(alpha_c*(B_c+1))} عدد صحيح — الاختبار مضبوط ✓")

# ============================================================== 6. التقرير
st.header("٦. كيف تُقدّم النتيجة في ورقتك")

card(
    "قائمة مراجعة للنشر",
    "<p>عند كتابة قسم النتائج، اذكر صراحةً:</p>"
    "<ul>"
    "<li><b>عدد التكرارات B</b> — واجعله يحقّق شرط العدد الصحيح.</li>"
    "<li><b>عملية توليد البوتستراب</b> المستعملة "
    "(وايلد؟ بواقي؟ ساكن؟) و<b>لماذا اخترتها</b>.</li>"
    "<li><b>توزيع الأوزان</b> إن كان وايلد (Rademacher عادةً).</li>"
    "<li><b>التحويل</b> المطبّق على البواقي (HC3 عادةً).</li>"
    "<li>هل فُرضت <b>الفرضية الصفرية</b> على عملية التوليد؟</li>"
    "<li><b>البذرة العشوائية</b> — لأجل إمكانية التكرار "
    "(<span class='bs-en'>reproducibility</span>).</li>"
    "<li>اعرض <b>قيمة p التقاربية وقيمة p البوتستراب معاً</b>. "
    "الفرق بينهما بحدّ ذاته نتيجة تستحقّ التعليق.</li>"
    "</ul>"
    "<p style='background:#fff;padding:10px;border-radius:8px;direction:ltr;"
    "text-align:left;font-size:.9em;font-family:monospace'>"
    "Example sentence: \"Diagnostic p-values are wild bootstrap p-values "
    "(Rademacher weights, HC3-transformed restricted residuals, recursive DGP, "
    "B = 1999, seed = 2026), computed with the Stata package bootdiag.\"</p>",
    "blue",
)

st.divider()
st.markdown(
    "**الصفحة التالية:** الاختبارات البعدية العادية — ما هي، وماذا تختبر، "
    "وأين تُخطئ بالضبط."
)
