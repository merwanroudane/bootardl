"""الصفحة الرئيسية."""

import numpy as np
import streamlit as st

from core.ui import hero, card, tiles, table, note, plotly, PALETTE
from core.anim import diagram_two_worlds, anim_build_distribution

hero(
    "منصّة البوتستراب والاختبارات البعدية",
    "دليل عربي شامل يأخذك من الصفر: ما هو البوتستراب (Bootstrap)، لماذا وُجد، "
    "كيف يعمل، أنواعه، ومتى تستعمل كل نوع — ثم كيف يُصلح الاختبارات البعدية "
    "(Post-estimation diagnostic tests) التي يعتمد عليها كل بحث تطبيقي.",
    "دليل الباحث · من المستوى صفر",
    "#E8F0FE", "#E0F7F4",
)

st.html(
    '<div style="background:#FFFFFF;border:1px solid #E2EAF7;border-radius:16px;'
    'padding:16px 22px;margin-bottom:18px;box-shadow:0 2px 10px rgba(16,32,63,.05)">'
    '<p style="margin:0;font-size:1.02rem;color:#2A3C5F;line-height:2">'
    '<b>إعداد:</b> د. مروان رودان — <span style="direction:ltr;unicode-bidi:embed;'
    'font-family:monospace">Dr Merwan Roudane</span><br>'
    'مؤلّف حزم <span style="font-family:monospace;direction:ltr;unicode-bidi:embed">'
    'bootdiag</span>، <span style="font-family:monospace;direction:ltr;'
    'unicode-bidi:embed">aardl</span>، <span style="font-family:monospace;'
    'direction:ltr;unicode-bidi:embed">fbardl</span>، '
    '<span style="font-family:monospace;direction:ltr;unicode-bidi:embed">fbnardl</span>، '
    '<span style="font-family:monospace;direction:ltr;unicode-bidi:embed">mtnardl</span> '
    'في أرشيف <span style="direction:ltr;unicode-bidi:embed">SSC</span> الخاص ببرنامج '
    '<span style="direction:ltr;unicode-bidi:embed">Stata</span>.</p></div>'
)

# ---------------------------------------------------------------- الفكرة في سطر
st.subheader("الفكرة كلّها في سطر واحد")

card(
    "ما الذي يفعله البوتستراب؟",
    "<p>عندك <b>عيّنة واحدة</b> فقط. والسؤال الذي يؤرّق كل باحث هو: "
    "«لو كنت قد جمعت عيّنة أخرى، كم كانت ستختلف نتيجتي؟»</p>"
    "<p>لا يمكنك العودة لجمع ألف عيّنة. لكن <b>البوتستراب</b> يقول لك: "
    "عيّنتك نفسها هي أفضل صورة متاحة عن المجتمع. فلنعامِلها كأنّها المجتمع، "
    "ونسحب منها آلاف العيّنات الجديدة بالحاسوب، ونرى بأعيننا كيف يتذبذب "
    "تقديرك. هذا كل شيء.</p>"
    "<p>الاسم نفسه من المثل الإنجليزي "
    "<span class='bs-en'>to pull yourself up by your own bootstraps</span> — "
    "أن ترفع نفسك بنفسك. لأن البيانات هنا ترفع نفسها بنفسها دون أن تستعين "
    "بأي جدول إحصائي خارجي.</p>",
    "blue",
)

plotly(diagram_two_worlds(), key="home_worlds")

note(
    "هذا المخطّط هو العمود الفقري للمنصّة كلّها: في الصف الأعلى ما يحدث في "
    "الواقع مرّة واحدة، وفي الصف الأسفل ما نُقلّده في الحاسوب <b>B</b> مرّة. "
    "كل ما تبقّى تفاصيل.",
    "teal", "🧭",
)

# ---------------------------------------------------------------- لماذا يهمّك
st.subheader("لماذا يهمّ هذا الباحث التطبيقي؟")

st.markdown(
    "بعد أن تُقدّر نموذجك، تُجري عادةً مجموعة من الاختبارات البعدية: هل الأخطاء "
    "مترابطة؟ هل تباينها ثابت؟ هل هي معتدلة التوزيع؟ هل المعالم مستقرّة؟ "
    "كل هذه الاختبارات تعطيك قيمة <span dir='ltr'>p</span> مأخوذة من جدول "
    "<span dir='ltr'>χ²</span> أو <span dir='ltr'>F</span>. **المشكلة:** ذلك "
    "الجدول صحيح فقط عندما يكون حجم العيّنة لانهائياً. وعيّناتنا ليست لانهائية."
)

st.markdown("هذه نتيجة تجربة مونت كارلو حقيقية، **تحت فرضية صفرية صحيحة** عند مستوى اسمي 5٪:")

table(
    ["الاختبار", "n=60, ρ=0.5", "n=60, ρ=0.9", "n=150, ρ=0.9"],
    [
        ["<b>Koenker</b> — النسخة التقاربية",
         "<span style='color:#E8536B'>11.3٪</span>",
         "<span style='color:#E8536B'>19.7٪</span>",
         "<span style='color:#E8536B'>16.3٪</span>"],
        ["<b>Koenker</b> — نسخة البوتستراب",
         "<span style='color:#10B981'>2.0٪</span>",
         "<span style='color:#10B981'>6.0٪</span>",
         "<span style='color:#10B981'>3.0٪</span>"],
        ["<b>Jarque–Bera</b> — النسخة التقاربية", "4.0٪", "2.7٪", "2.7٪"],
        ["<b>Jarque–Bera</b> — نسخة البوتستراب", "3.3٪", "3.7٪", "5.0٪"],
        ["<b>supF</b> — نسخة البوتستراب", "5.7٪", "5.0٪", "5.7٪"],
    ],
)

note(
    "اقرأ الصف الأول جيّداً: اختبار عدم تجانس التباين التقاربي يرفض فرضية صحيحة "
    "في <b>واحدة من كل خمس حالات</b> بدل واحدة من عشرين. أي أنّك ستُعلن وجود "
    "مشكلة في نموذجك وتُعيد تقديره وتُغيّر استنتاجك الاقتصادي… بسبب خطأ في "
    "الجدول، لا في بياناتك. وكلّما ازداد الارتباط الذاتي ρ ساء الوضع. "
    "<br><br><span style='font-size:.9em;color:#51637F'>المصدر: تجربة مونت كارلو "
    "ضمن حزمة <span dir='ltr' style='font-family:monospace'>bootdiag</span>، "
    "300 تكرار. والتشوّهات نفسها موثّقة في Cribari-Neto &amp; Zarkos (1999)، "
    "Dufour et al. (2004)، وKilian &amp; Demiroglu (2000).</span>",
    "rose", "⚠️",
)

# ---------------------------------------------------------------- خريطة المنصة
st.subheader("خريطة المنصّة")

tiles([
    {"num": "١", "title": "لماذا نحتاج البوتستراب؟",
     "text": "النظرية التقاربية ووعدها المؤجّل، مشاكل العيّنات الصغيرة، "
             "ومشاكل العيّنات الكبيرة التي لا ينتبه لها أحد.", "color": "rose"},
    {"num": "٢", "title": "الفكرة من الصفر",
     "text": "مبدأ الإحلال، السحب مع الإرجاع، وبناء التوزيع — "
             "بأنيميشن خطوة بخطوة.", "color": "blue"},
    {"num": "٣", "title": "أنواع البوتستراب",
     "text": "أحد عشر نوعاً: الفكرة، ومتى يُستعمل، ولماذا، وما يجب تجنّبه.",
     "color": "teal"},
    {"num": "٤", "title": "الوايلد بوتستراب",
     "text": "النوع الأهم في الاقتصاد القياسي: Rademacher مقابل Mammen، "
             "وHC0 حتى HC3.", "color": "violet"},
    {"num": "٥", "title": "قيمة p وعدد التكرارات",
     "text": "الصيغ الأربع، تصحيح +1، كم يلزم من B، والبوتستراb المزدوج السريع.",
     "color": "amber"},
    {"num": "٦", "title": "الاختبارات العادية",
     "text": "Durbin–Watson، Breusch–Godfrey، Breusch–Pagan، White، "
             "Jarque–Bera، CUSUM، RESET… وأين تُخطئ.", "color": "orange"},
    {"num": "٧", "title": "الاختبارات بالبوتستراب",
     "text": "الإحصاء نفسه، التوزيع الصفري مختلف — و28 اختباراً جاهزاً.",
     "color": "green"},
    {"num": "٨", "title": "الاستقرار الهيكلي",
     "text": "CUSUM وsupF بحِزَم بوتستراب بدل الخطوط التقاربية غير الموثوقة.",
     "color": "indigo"},
    {"num": "٩", "title": "مختبر مونت كارلو",
     "text": "شغّل التجربة بنفسك وشاهد التشوّه يحدث أمامك.", "color": "cyan"},
    {"num": "١٠", "title": "المختبر التفاعلي",
     "text": "ارفع بياناتك أو ولّدها، وشغّل بطارية الاختبارات كاملة.",
     "color": "pink"},
    {"num": "١١", "title": "حزمة bootdiag",
     "text": "التوثيق الكامل للحزمة في Stata: الصيغة، الخيارات، الأمثلة.",
     "color": "blue"},
    {"num": "١٢", "title": "عائلة Bootstrap ARDL",
     "text": "من اختبار الحدود PSS إلى Bootstrap ARDL وAugmented ARDL "
             "وFourier ARDL.", "color": "lime"},
], cols=3)

# ---------------------------------------------------------------- عيّنة حيّة
st.divider()
st.subheader("تذوّق سريع: شاهد توزيعاً بوتستراب يُبنى أمامك")

st.markdown(
    "اضغط **▶ تشغيل** تحت الرسم. كل خطوة تضيف المزيد من عيّنات البوتستراب، "
    "وستلاحظ كيف يتبلور شكل التوزيع تدريجياً من الفوضى إلى منحنى واضح. "
    "هذا هو التوزيع الذي سنقارن به إحصاءك بدل جدول <span dir='ltr'>χ²</span>."
)

rng = np.random.default_rng(7)
demo = rng.chisquare(2, 1200) * 1.1
plotly(
    anim_build_distribution(demo, stat=6.2, steps=22,
                            title="توزيع بوتستراب يُبنى تكراراً بعد تكرار",
                            color="blue"),
    key="home_build",
)

note(
    "الخط الوردي هو إحصاؤك المحسوب من بياناتك. قيمة <span dir='ltr'>p</span> "
    "ببساطة هي: <b>ما نسبة الأعمدة الواقعة إلى يمين هذا الخط؟</b> "
    "لا جدول، لا نظرية تقاربية، لا افتراض عن شكل التوزيع.",
    "blue", "🎯",
)

st.divider()
st.caption(
    "للانتقال بين الأقسام استعمل القائمة على يمين الشاشة. "
    "كل صفحة مستقلّة ويمكن قراءتها وحدها، لكن الترتيب مصمّم للقراءة المتسلسلة."
)
