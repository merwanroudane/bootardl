"""توثيق حزمة bootdiag في Stata."""

import streamlit as st

from core.ui import hero, card, note, table, steps, tiles, PALETTE

hero(
    "حزمة bootdiag",
    "كل ما شرحته هذه المنصّة، جاهزاً للتنفيذ في Stata بأمر واحد. "
    "ثمانية وعشرون اختباراً، وثماني عمليات توليد، وعشر رسوم — "
    "بعد regress أو newey أو ardl أو عائلة ARDL الكاملة.",
    "التطبيق في Stata · إعداد د. مروان رودان",
    "#E8F0FE", "#E3F8F0",
)

card(
    "بطاقة الحزمة",
    "<table class='bs-table' style='margin:0'>"
    "<tr><td style='width:35%'><b>الاسم</b></td>"
    "<td><code>bootdiag</code></td></tr>"
    "<tr><td><b>العنوان</b></td>"
    "<td>Bootstrap and Monte Carlo post-estimation diagnostic tests</td></tr>"
    "<tr><td><b>الإصدار</b></td><td>1.0.0</td></tr>"
    "<tr><td><b>المتطلّبات</b></td><td>Stata 16 أو أحدث</td></tr>"
    "<tr><td><b>المؤلّف</b></td>"
    "<td>د. مروان رودان — Merwan Roudane</td></tr>"
    "<tr><td><b>الأرشيف</b></td>"
    "<td>SSC — Statistical Software Components</td></tr>"
    "</table>",
    "blue",
)

# ============================================================== التثبيت
st.header("١. التثبيت")

st.code("ssc install bootdiag, replace", language="stata")
st.code("help bootdiag", language="stata")

note(
    "الحزمة تعتمد على مكتبة Mata مُصرَّفة "
    "(<code style='direction:ltr'>lbootdiag.mlib</code>) "
    "تُثبَّت تلقائياً مع الأوامر، فلا حاجة لأي إعداد إضافي.",
    "teal", "💾",
)

# ============================================================== الصيغة
st.header("٢. الصيغة")

st.code("bootdiag subcommand [, options]", language="stata")

st.subheader("الأوامر الفرعية")

table(
    ["الأمر الفرعي", "ماذا يُشغّل"],
    [
        ["<code>serial</code>", "اختبارات الارتباط الذاتي"],
        ["<code>het</code>", "اختبارات عدم تجانس التباين"],
        ["<code>norm</code>", "اختبارات اعتدالية الأخطاء"],
        ["<code>stab</code>", "اختبارات استقرار المعالم"],
        ["<code>spec</code>", "اختبارات الشكل الدالي"],
        ["<code>all</code>", "<b>البطارية الكاملة (الافتراضي)</b>"],
        ["<code>nhi</code>", "اختبار Jarque–Bera المشترك وكل الاختبارات الفرعية الستة"],
        ["<code>fdb</code>", "البوتستراب المزدوج السريع، أو اختيار B بالاختبار المسبق"],
    ],
)

st.subheader("الخيارات")

tabs = st.tabs(["تصميم البوتستراب", "ضبط الاختبارات", "اختيار B",
                "تحديد النموذج", "المخرجات"])

with tabs[0]:
    table(
        ["الخيار", "الافتراضي", "الوصف"],
        [
            ["<code>reps(#)</code>", "<code>999</code>", "عدد التكرارات B"],
            ["<code>dgp(type)</code>", "<code>wild</code>",
             "عملية توليد البوتستراب — ثمانية خيارات، انظر القسم ٣"],
            ["<code>weight(dist)</code>", "<code>rademacher</code>",
             "التوزيع المساعد للوايلد: <code>rademacher</code> (F2) أو "
             "<code>mammen</code> (F1) أو <code>normal</code>"],
            ["<code>ftrans(form)</code>", "<code>hc3</code>",
             "تحويل البواقي: <code>hc0</code> … <code>hc3</code>"],
            ["<code>block(#)</code>", "مبني على البيانات",
             "طول الكتلة لعمليات التوليد الكتلية"],
            ["<code>continuous</code>", "—",
             "قيمة p المتّصلة لـ Racine &amp; MacKinnon — "
             "منتظمة تماماً لأي B منتهٍ"],
            ["<code>seed(#)</code>", "—",
             "البذرة العشوائية — <b>اضبطها دائماً</b> لإمكانية التكرار"],
        ],
    )
with tabs[1]:
    table(
        ["الخيار", "الافتراضي", "الوصف"],
        [
            ["<code>lags(numlist)</code>", "<code>1 2 4</code>",
             "رتب الارتباط الذاتي لاختبار Breusch–Godfrey"],
            ["<code>archlags(#)</code>", "<code>2</code>",
             "رتبة اختبار ARCH LM"],
            ["<code>trim(#)</code>", "<code>0.15</code>",
             "نسبة التشذيب لـ supF / aveF / expF"],
            ["<code>resetpow(#)</code>", "<code>4</code>",
             "أعلى قوّة لـ ŷ في اختبار RESET"],
            ["<code>nhilags(#)</code>", "<code>1</code>",
             "عدد الإبطاءات في مكوّن الاستقلال من اختبار NHI"],
            ["<code>fdbtest(name)</code>", "<code>koenker</code>",
             "الاختبار الذي يُطبَّق عليه البوتستراب المزدوج السريع"],
        ],
    )
with tabs[2]:
    table(
        ["الخيار", "الافتراضي", "الوصف"],
        [
            ["<code>pretest</code>", "—",
             "اختيار B بالاختبار المسبق بدل تثبيته"],
            ["<code>prealpha(#)</code>", "<code>0.05</code>",
             "مستوى الاهتمام α"],
            ["<code>prebeta(#)</code>", "<code>0.01</code>",
             "مستوى الاختبار المسبق β"],
            ["<code>premin(#)</code>", "<code>99</code>", "قيمة B الابتدائية"],
            ["<code>premax(#)</code>", "<code>12799</code>", "الحدّ الأقصى لـ B"],
        ],
    )
    st.info(
        "الخوارزمية: ابدأ بـ B = 99، اختبر ما إذا كانت قيمة p محسومة عند "
        "مستوى β، وإن لم تُحسم فضاعِف B ← 2B+1 واسحب B+1 عيّنة إضافية. "
        "هذا يُبقي α(B+1) عدداً صحيحاً في كل مرحلة، "
        "ويتفوّق على B ثابتة عند التكلفة الحاسوبية نفسها."
    )
with tabs[3]:
    table(
        ["الخيار", "الوصف"],
        [
            ["<code>ylev(varname)</code>", "المتغيّر التابع في المستويات"],
            ["<code>xlev(varlist)</code>", "متغيّرات الأجل الطويل في المستويات"],
            ["<code>p(#)</code>", "الرتبة الانحدارية الذاتية في المستويات"],
            ["<code>q(numlist)</code>", "رتبة إبطاء كل متغيّر مستقل"],
            ["<code>case(#)</code>", "الحالة الحتمية لـ PSS، من 1 إلى 5"],
            ["<code>tolerance(#)</code>",
             "تسامح فحص إعادة البناء — الافتراضي <code>1e-4</code>"],
            ["<code>noverify</code>",
             "تخطّي فحص إعادة البناء (لا يُنصح به)"],
        ],
    )
with tabs[4]:
    table(
        ["الخيار", "الوصف"],
        [
            ["<code>notable</code>", "إخفاء الجدول"],
            ["<code>noasymptotic</code>",
             "إخفاء لوحة المقارنة بين البوتستراب والتقاربي"],
            ["<code>graph</code>", "إنتاج الرسوم التشخيصية العشرة"],
            ["<code>gname(name)</code>", "بادئة أسماء الرسوم"],
            ["<code>saving(filename)</code>", "تصدير اللوحة المجمّعة"],
        ],
    )

# ============================================================== DGPs
st.header("٣. عمليات التوليد الثماني")

table(
    ["<code>dgp()</code>", "الوصف", "متى"],
    [
        ["<code>wild</code>", "الوايلد التكراري — <b>الافتراضي</b>",
         "تباين متغيّر مجهول الشكل"],
        ["<code>residual</code>", "بوتستراب بواقي تكراري، سحب iid",
         "أخطاء iid؛ <b>وكذلك لاختبار تجانس التباين نفسه</b>"],
        ["<code>fixed</code>", "وايلد بمتغيّرات مُثبّتة",
         "<b>للمقارنة فقط</b> — ليراه المستخدم يفشل بنفسه"],
        ["<code>sieve</code>", "غربال AR برتبة مختارة بـ AIC",
         "ترابط زمني مع ابتكارات متجانسة"],
        ["<code>block</code>", "كتل متحرّكة", "ترابط عام"],
        ["<code>stationary</code>", "ساكن، أطوال كتل هندسية",
         "ترابط مجهول الشكل، مع الحاجة لسكون"],
        ["<code>blockwild</code>", "وايلد كتلي، وزن واحد لكل كتلة",
         "اختبار كسر في المتوسّط أو التباين"],
        ["<code>normal</code>", "معلمي غاوسي",
         "اختبار الاعتدالية؛ أو اختبار مونت كارلو مضبوط"],
    ],
)

card(
    "لماذا <code>wild</code> هو الافتراضي؟",
    "<p>لأنّه الخيار الأسلم في الحالة العامة. وبالتحديد، لأنّ "
    "<b>التوليد التكراري ضروري</b>:</p>"
    "<p>MacKinnon (2007، §7) يُظهر أنّه لاختبار supF في نموذج AR(1)، "
    "يعمل بوتستراب البواقي التكراري <b>عند كل قيمة للمعامل الانحداري الذاتي</b>، "
    "بينما يؤدّي بوتستراب المتغيّرات المُثبّتة <b>بسوء الاختبار التقاربي نفسه</b>. "
    "وO'Reilly وWhelan (2005) يصلان إلى الخلاصة ذاتها، ويُضيفان أنّ النسخة "
    "الوايلد ضرورية حالما يتوقّف تباين الخطأ عن الثبات.</p>"
    "<p>وخيار <code>dgp(fixed)</code> موجود في الحزمة تحديداً "
    "<b>لكي يرى المستخدمون ذلك بأنفسهم</b>.</p>",
    "teal",
)

# ============================================================== الأمثلة
st.header("٤. أمثلة عملية")

st.subheader("البداية السريعة")
st.code("""* البطارية كاملةً بعد انحدار ديناميكي
regress y L.y x z
bootdiag all

* عائلة واحدة بتكرارات أكثر
bootdiag serial, reps(1999)

* مع الرسوم العشرة
bootdiag all, graph

* بعد نموذج تصحيح الخطأ ARDL
ardl y x z, maxlags(4) ec
bootdiag all, graph""", language="stata")

st.subheader("مقارنة الإجابة التقاربية بالبوتستراب")
st.code("""regress y L.y x z

* الإجابة التقاربية
estat bgodfrey, lags(1 2 4)
estat hettest, iid
estat imtest, white

* إجابة البوتستراب
bootdiag serial, reps(1999) seed(2026)
bootdiag het,    reps(1999) seed(2026) dgp(residual)""", language="stata")

note(
    "اقرأ صفوف <code>MLM_HR</code>: هي الحصينة وذات أقل تقلّب في مقدّر "
    "التغاير. وانظر إلى لوحة «<span dir='ltr'>Bootstrap vs asymptotic</span>»: "
    "الفرق الموجب الكبير يعني أنّ الاختبار التقاربي كان <b>يُفرط في الرفض</b>.",
    "amber", "👁️",
)

st.subheader("مطابقة عملية التوليد مع الفرضية المختبَرة")
st.code("""* الارتباط الذاتي: الوايلد يُعطي حصانة لعدم تجانس التباين كمُزعج
bootdiag serial, dgp(wild) weight(rademacher) ftrans(hc3) reps(1999)

* تجانس التباين: يجب فرض الصفرية، فلا وايلد
bootdiag het, dgp(residual) reps(1999)

* الاعتدالية: نولّد أخطاءً معتدلة بالضبط
bootdiag norm, dgp(normal) reps(1999)
bootdiag norm, dgp(sieve)  reps(1999)   // بديل Psaradakis-Vavra

* الاستقرار: الوايلد التكراري
bootdiag stab, dgp(wild) trim(0.15) graph

* للمقارنة فقط — متوقّع أن يكون غير موثوق
bootdiag stab, dgp(fixed)""", language="stata")

st.subheader("التحكّم الدقيق في التكلفة والدقّة")
st.code("""* البوتستراب المزدوج السريع على اختبار Koenker
bootdiag fdb, fdbtest(koenker) reps(999) seed(2026)

* اختيار B بالاختبار المسبق
bootdiag fdb, pretest prealpha(0.05) prebeta(0.001) ///
              premin(99) premax(12799)

* قيمة p المتّصلة — لا تحتاج شرط العدد الصحيح
bootdiag het, reps(199) continuous dgp(residual)

* الاختبار المشترك NHI وكل فروعه من حلقة واحدة
bootdiag nhi, reps(1999) nhilags(2)""", language="stata")

# ============================================================== الرسوم
st.header("٥. الرسوم العشرة")

st.code("bootdiag all, graph gname(fig)", language="stata")

table(
    ["اسم الرسم", "المحتوى"],
    [
        ["<code>_null</code>", "كثافة التوزيع الصفري البوتستراب، القيمة "
         "المُشاهدة، والقيمة الحرجة 5٪"],
        ["<code>_pdisc</code>", "مخطّط تباين قيمة p"],
        ["<code>_hist</code>", "مدرّج البواقي مقابل التوزيع الطبيعي المُلائَم"],
        ["<code>_qq</code>", "مخطّط المئينات الطبيعي"],
        ["<code>_scat</code>", "البواقي المربّعة مقابل القيم المقدّرة، مع lowess"],
        ["<code>_cusum</code>", "<b>CUSUM بحِزَم بوتستراب</b> ⭐"],
        ["<code>_cusumsq</code>", "<b>CUSUM of squares بحِزَم بوتستراب</b> ⭐"],
        ["<code>_chow</code>", "<b>متتالية Chow F مع القيمة الحرجة البوتستراب "
         "لـ supF</b> ⭐"],
        ["<code>_corr</code>", "مخطّط الارتباط الذاتي للبواقي بحِزَم بوتستراب"],
        ["<code>_all</code>", "كل ما سبق مجمّعاً"],
    ],
)

st.subheader("ثلاثة رسوم بلا نظير قياسي في Stata")

c1, c2, c3 = st.columns(3)
with c1:
    card(
        "⭐ حِزَم CUSUM",
        "<p>Brown, Durbin &amp; Evans (1975) يرسمون <b>حدوداً تقاربية "
        "مستقيمة</b>. وKrämer, Ploberger &amp; Alt (1988) يُظهرون أنّها "
        "<b>غير موثوقة</b> حالما وُجد متغيّر تابع مُبطّأ — لأنّ البواقي "
        "التكرارية عندها ليست معتدلة ولا مستقلّة.</p>"
        "<p>الحزمة ترسم <b>المئينات النقطية لمسارات CUSUM البوتستراب تحت "
        "الصفرية</b>، فترث الحزمة سلوك العيّنة المنتهية الفعلي لنموذجك.</p>",
        "violet",
    )
with c2:
    card(
        "⭐ حِزَم مخطّط الارتباط",
        "<p>خطوط <span dir='ltr'>±2/√n</span> المعتادة تفترض سلسلة iid. "
        "لكن بواقي نموذج ديناميكي مُقدَّر ليست كذلك: "
        "<b>ارتباطاتها الذاتية منخفضة الرتبة مُنكمِشة نحو الصفر بفعل التقدير "
        "نفسه</b>.</p>"
        "<p>حِزَم البوتستراب تُعيد إنتاج ذلك الانكماش، "
        "فتكون عادةً <b>أضيق</b> من الخطوط الاسمية عند الإبطاءات القصيرة — "
        "ما يجعل الاختبار <b>أكثر</b> حساسية لا أقل.</p>",
        "teal",
    )
with c3:
    card(
        "⭐ مخطّط تباين قيمة p",
        "<p>على نمط Davidson &amp; MacKinnon (1998): يرسم "
        "<b>نسبة الرفض الفعلية ناقص الاسمية</b> عبر كل المستويات "
        "من 1٪ إلى 40٪، باستعمال التوزيع الصفري البوتستراب كحقيقة.</p>"
        "<p>منحنى فوق الصفر = الاختبار التقاربي <b>يُفرط في الرفض</b> عند ذلك "
        "المستوى. <b>يُظهر تشوّه الحجم كاملاً</b>، لا قيمته عند 5٪ فقط.</p>",
        "amber",
    )

# ============================================================== الاسترجاع
st.header("٦. كيف تسترجع الحزمة النموذج")

steps([
    "تقرأ المعادلة المُقدَّرة من <code>e()</code>.",
    "تُحلّل قائمة المتغيّرات لاستنتاج رتبة ARDL الضمنية في المستويات.",
    "تُعيد بناء نموذج تصحيح الخطأ المشروط كإعادة معلمة <b>مضبوطة</b>.",
    "<b>تفحص</b> أنّ إعادة التقدير تُنتج مجموع مربّعات البواقي نفسه الذي "
    "أبلغ عنه أمر التقدير. وفي الحالات المدعومة يكون التطابق عند دقّة الآلة.",
    "إن اختلف الرقمان، <b>تتوقّف برسالة خطأ تُسمّي التباين</b> — "
    "بدل أن تُبلغ عن قيمة p لنموذج لم يُقدّره المستخدم.",
])

note(
    "الحزمة <b>لا تثق</b> بـ <code>e(p)</code> أو <code>e(q_*)</code>، "
    "لأنّ الأوامر المختلفة تُسمّي رتب الإبطاء بطرق مختلفة. "
    "مثال حقيقي: <code>aardl</code> يُبلغ عن «ARDL(1,0,0)» لنموذج "
    "<code>e(ecmvars)</code> فيه "
    "<code style='direction:ltr'>L.y L.x L.z L1.D.y D.x D.z</code>، "
    "وهو في المستويات <b>ARDL(2,1,1)</b>. "
    "لهذا تُعيد الحزمة الاشتقاق بنفسها وتتحقّق.",
    "rose", "🔍",
)

st.subheader("الأوامر المدعومة")

table(
    ["الأمر", "المصدر", "ملاحظة"],
    [
        ["<code>regress</code>", "Stata", "—"],
        ["<code>newey</code>", "Stata", "—"],
        ["<code>ardl</code>", "Kripfganz &amp; Schneider", "—"],
        ["<code>aardl</code>", "Roudane", "يتطلّب 2.1.1 فأحدث"],
        ["<code>fbardl</code>", "Roudane", "يتطلّب 1.3.1 فأحدث"],
        ["<code>fbnardl</code>", "Roudane", "يتطلّب 2.0.1 فأحدث"],
        ["<code>mtnardl</code>", "Roudane", "يتطلّب 1.0.1 فأحدث"],
    ],
)

st.info(
    "الإصدارات الأقدم من هذه الأوامر كانت تُغلّف التقدير داخل "
    "`preserve`/`restore` وتستدعي `regress` بلا متّجه معالم، "
    "فتُحذف المتغيّرات المبنية (حدود Fourier، المجاميع الجزئية غير المتماثلة، "
    "أنظمة العتبات) قبل أن يعود الأمر — فلا يبقى شيء لأمر بعدي ليقرأه. "
    "الإصدارات المذكورة أعلاه تُصلح ذلك: تنشر متّجه المعالم، وتُسجّل قائمة "
    "المتغيّرات في `e()`، وتُعيد بناء الأعمدة المبنية بعد `restore`."
)

st.markdown(
    "لأي معادلة أخرى لم تُقدّرها هذه الأوامر، ابنِ المتغيّرات بنفسك "
    "وحدّد النموذج صراحةً:"
)
st.code("""* مثال: تحديد يدوي للنموذج
regress D.y L.y L.x L.z LD.y D.x D.z
bootdiag all, ylev(y) xlev(x z) p(2) q(1 1) case(3)""", language="stata")

# ============================================================== المخرجات
st.header("٧. النتائج المحفوظة")

table(
    ["الاسم", "المحتوى"],
    [
        ["<code>e(reps)</code>", "عدد التكرارات المستعملة"],
        ["<code>e(N)</code>", "المشاهدات في المعادلة المُعاد بناؤها"],
        ["<code>e(k)</code>", "المعالم في المعادلة المُعاد بناؤها"],
        ["<code>e(dgp)</code>", "عملية التوليد المستعملة"],
        ["<code>e(weight)</code>", "التوزيع المساعد"],
        ["<code>e(ftrans)</code>", "تحويل البواقي"],
        ["<code>e(cmd0)</code>", "الأمر الذي عمل bootdiag بعده"],
        ["<code>e(source)</code>", "من أين قُرئت المعادلة"],
        ["<code>r(table)</code> / <code>e(table)</code>",
         "صف لكل اختبار، بأعمدة الإحصاء وقيم p والقيم الحرجة"],
    ],
)

st.code("""bootdiag all, reps(1999) seed(2026)
matrix list e(table)
matrix B = e(table)
esttab matrix(B) using diagnostics.tex, replace""", language="stata")

# ============================================================== التقرير
st.header("٨. التقرير في الورقة")

card(
    "جملة جاهزة لقسم المنهجية",
    "<p style='direction:ltr;text-align:left;background:#fff;padding:14px;"
    "border-radius:10px;font-family:monospace;font-size:.88em;line-height:1.9'>"
    "All diagnostic p-values are bootstrap p-values rather than asymptotic "
    "ones. The test statistics are computed exactly as in the source papers; "
    "only the null distribution is replaced by a simulated one. We use the "
    "recursive wild bootstrap with Rademacher weights and HC3-transformed "
    "restricted residuals (Davidson and Flachaire, 2008), B = 1999 "
    "replications, seed 2026. Computations use the Stata package "
    "<b>bootdiag</b> (Roudane, 2026).</p>"
    "<p>وإن كان لديك مجال، أضف جملة تُبرز الفرق:</p>"
    "<p style='direction:ltr;text-align:left;background:#fff;padding:14px;"
    "border-radius:10px;font-family:monospace;font-size:.88em;line-height:1.9'>"
    "The asymptotic and bootstrap p-values differ materially for the "
    "heteroskedasticity tests, consistent with the size distortions reported "
    "by Cribari-Neto and Zarkos (1999) and Dufour et al. (2004); "
    "we report the bootstrap values throughout.</p>",
    "blue",
)

st.divider()
st.markdown(
    "**الصفحة التالية:** عائلة Bootstrap ARDL — تطبيق الفكرة نفسها على "
    "اختبار التكامل المشترك."
)
