"""قاموس المصطلحات والمراجع."""

import pandas as pd
import streamlit as st

from core.ui import hero, card, note, table, PALETTE

hero(
    "المصطلحات والمراجع",
    "قاموس عربي-إنجليزي لكل مصطلح ورد في المنصّة، وقائمة المراجع الكاملة "
    "التي بُنيت عليها — مع أرقام DOI حيثما توفّرت.",
    "المرجع",
    "#E8F0FE", "#F2ECFE",
)

# ============================================================== القاموس
st.header("١. قاموس المصطلحات")

GLOSS = [
    ("Bootstrap", "البوتستراب / إعادة المعاينة",
     "منهج نُولّد به توزيع المعاينة بإعادة السحب من البيانات نفسها بدل "
     "الاعتماد على نظرية تقاربية. المصطلح الإنجليزي شائع كما هو."),
    ("Resampling", "إعادة المعاينة",
     "سحب عيّنات جديدة من العيّنة الأصلية."),
    ("Sampling with replacement", "السحب مع الإرجاع",
     "بعد سحب مشاهدة نُعيدها إلى الصندوق، فقد تُسحب مرّة أخرى."),
    ("Sampling distribution", "توزيع المعاينة",
     "توزيع الإحصاء لو كرّرنا جمع العيّنة مرّات لا تُحصى. "
     "هو هدف الاستدلال الإحصائي كلّه."),
    ("Empirical distribution F̂", "التوزيع التجريبي",
     "التوزيع الذي يُعطي كل مشاهدة في عيّنتك احتمال 1/n."),
    ("Plug-in principle", "مبدأ الإحلال",
     "إحلال F̂ محلّ F المجهول — الأساس المنطقي للبوتستراب."),
    ("Asymptotic", "تقاربي",
     "ما يصحّ عند حجم عيّنة لانهائي. يبقى المصطلح الإنجليزي شائعاً."),
    ("Nominal size", "الحجم الاسمي",
     "المستوى المُعلن للاختبار، مثل 5٪."),
    ("Actual / empirical size", "الحجم الفعلي",
     "نسبة الرفض الحقيقية تحت فرضية صفرية صحيحة عند حجم عيّنتك."),
    ("Size distortion / ERP", "تشوّه الحجم",
     "الفرق بين الحجمين. ERP = Error in Rejection Probability."),
    ("Power", "قوّة الاختبار",
     "نسبة الرفض تحت فرضية صفرية خاطئة — أي قدرته على كشف المشكلة."),
    ("Size-adjusted power", "القوّة المعدّلة للحجم",
     "القوّة بعد ضبط القيمة الحرجة ليصبح الحجم الفعلي مساوياً للاسمي."),
    ("Bootstrap DGP", "عملية توليد بيانات البوتستراب",
     "الوصفة التي نُولّد بها y* في كل تكرار. القرار الأهم في التطبيق."),
    ("Restricted / null-imposed", "مقيّد / بفرض الصفرية",
     "تقدير وتوليد تحت الفرضية الصفرية — الصحيح لاختبار الفرضيات."),
    ("Unrestricted", "غير مقيّد",
     "تقدير تحت الفرضية البديلة — الصحيح لمجالات الثقة."),
    ("Pivotal statistic", "إحصاء محوري",
     "إحصاء توزيعه لا يعتمد على معالم مجهولة. حين يكون كذلك، "
     "يصبح اختبار مونت كارلو مضبوطاً تماماً."),
    ("Exact test", "اختبار مضبوط",
     "اختبار حجمه الفعلي يساوي الاسمي بالضبط في أي حجم عيّنة."),
    ("Monte Carlo test", "اختبار مونت كارلو",
     "نسخة من البوتستراب تُولّد الأخطاء من توزيع محدّد تماماً."),
    ("Wild bootstrap", "الوايلد بوتستراب",
     "ضرب كل باقٍ في وزن عشوائي في مكانه. لا ترجمة مستقرّة — "
     "يُستعمل المصطلح الإنجليزي."),
    ("Rademacher distribution", "توزيع راديماخر",
     "وزن ±1 باحتمال ½ لكل منهما. الافتراضي للوايلد. يُسمّى F2 أو PD2."),
    ("Mammen distribution", "توزيع مامن",
     "التوزيع ثنائي النقطة غير المتماثل الذي يُصحّح الالتواء. F1 أو PD1."),
    ("Pairs / case bootstrap", "بوتستراب الأزواج",
     "سحب الأزواج (y,x) معاً. غير متّسق في الانحدار — تجنّبه."),
    ("Residual bootstrap", "بوتستراب البواقي",
     "إعادة سحب البواقي بحرّية ثم إعادة بناء y*."),
    ("Recursive generation", "التوليد التكراري",
     "توليد y* مشاهدةً بمشاهدة مع إعادة بناء عمود y*_{t-1}. "
     "ضروري في النماذج الديناميكية."),
    ("Sieve bootstrap", "بوتستراب الغربال",
     "تقريب السلسلة بنموذج AR(p) ثم إعادة توليدها منه."),
    ("Moving block bootstrap", "بوتستراب الكتل المتحرّكة",
     "سحب كتل متتالية من المشاهدات ولصقها."),
    ("Stationary bootstrap", "البوتستراب الساكن",
     "كتل بأطوال هندسية عشوائية مع التفاف دائري."),
    ("Block wild bootstrap", "الوايلد الكتلي",
     "وزن Rademacher واحد لكل كتلة كاملة."),
    ("Fixed-regressor bootstrap", "بوتستراب المتغيّرات المُثبّتة",
     "لا يُولّد المتغيّر التابع المُبطّأ تكرارياً — يفشل عند المثابرة العالية."),
    ("Double bootstrap / FDB", "البوتستراب المزدوج / المزدوج السريع",
     "بوتستراب فوق البوتستراب لخفض رتبة الخطأ."),
    ("Leverage h_t", "الرافعة",
     "قدرة المشاهدة t على جذب خط الانحدار نحوها."),
    ("HCCME", "مقدّر مصفوفة التغاير الحصين لعدم تجانس التباين",
     "Heteroskedasticity-Consistent Covariance Matrix Estimator — "
     "عائلة HC0 إلى HC3."),
    ("Heteroskedasticity", "عدم تجانس التباين",
     "تباين الخطأ غير ثابت عبر المشاهدات."),
    ("Serial correlation / autocorrelation", "الارتباط الذاتي",
     "ارتباط الخطأ بقيمه السابقة."),
    ("Structural break", "الكسر الهيكلي",
     "تغيّر المعالم في نقطة زمنية."),
    ("Recursive residuals", "البواقي التكرارية",
     "أخطاء التنبؤ خارج العيّنة المُقيَّسة من تقدير تكراري متزايد."),
    ("Trimming", "التشذيب",
     "استبعاد طرفَي العيّنة من البحث عن تاريخ الكسر، عادةً 15٪."),
    ("Marked empirical process", "العملية التجريبية الموسومة",
     "مجموع تراكمي للبواقي مرتّبةً حسب متغيّر الشرط."),
    ("Cointegration", "التكامل المشترك",
     "تركيبة خطّية ساكنة من سلاسل غير ساكنة — علاقة توازن طويل الأجل."),
    ("ARDL", "نموذج الانحدار الذاتي للإبطاءات الموزّعة",
     "Autoregressive Distributed Lag — يُستعمل المختصر عادةً كما هو."),
    ("Bounds test", "اختبار الحدود",
     "اختبار PSS بحدّين حرجين I(0) وI(1)، وبينهما منطقة غير حاسمة."),
    ("Degenerate case", "الحالة المتدهورة",
     "رفض F الإجمالي ناتج عن طرف واحد من حدّ تصحيح الخطأ — لا تكامل مشترك."),
    ("Error correction term", "حدّ تصحيح الخطأ",
     "المعامل الذي يقيس سرعة العودة إلى التوازن طويل الأجل."),
    ("Weak exogeneity", "الخارجية الضعيفة",
     "غياب التغذية الراجعة من y إلى x في المستويات."),
    ("Marginal process", "العملية الهامشية",
     "النموذج الذي يُولّد x داخل بوتستراب ARDL."),
    ("Unconditional bootstrap", "البوتستراب غير المشروط",
     "فرضية مقيّدة واحدة تُولَّد منها العيّنات وتُحسب منها الإحصاءات الثلاثة جميعاً — McNown, Sam & Goh (2018)."),
    ("Conditional bootstrap", "البوتستراب المشروط",
     "ثلاث فرضيات صفرية منفصلة مع نموذج VECM هامشي، فتكون توزيعات البوتستراب مُستهدَفة لكل اختبار — Bertelli, Vacca & Zoia (2022)."),
    ("Fourier terms", "حدود Fourier",
     "حدّا جيب وجيب تمام بتردّد k يُقرّبان أي تغيّر هيكلي ناعم دون معرفة عدد الكسور أو تواريخها."),
    ("Fractional frequency", "التردّد الكسري",
     "قيمة k غير صحيحة (مثل 0.7) تسمح بالتقاط جزء من دورة، أي انتقال مستوى تدريجي لا يعود."),
    ("FA-ARDL", "Fourier Augmented ARDL",
     "الاختبارات الثلاثة المُعزَّزة مع حدود Fourier، بقيم حرجة من الجداول."),
    ("FBA-ARDL", "Fourier Bootstrap Augmented ARDL",
     "الأشمل: الاختبارات الثلاثة + حدود Fourier + قيم حرجة بالبوتستراب."),
    ("Response surface critical values", "قيم حرجة من سطح الاستجابة",
     "قيم حرجة مضبوطة للعيّنات المنتهية مُستخرَجة من انحدارات على محاكاة ضخمة — Kripfganz & Schneider (2020)."),
    ("Spurious regression", "الانحدار الزائف",
     "علاقة معنوية ظاهرياً بين سلسلتين غير ساكنتين لا علاقة بينهما."),
]

q = st.text_input("ابحث في القاموس (بالعربية أو الإنجليزية)", "",
                  key="gl_q", placeholder="مثلاً: wild، أو تشوّه، أو pivotal")

rows = GLOSS
if q.strip():
    s = q.strip().lower()
    rows = [g for g in GLOSS
            if s in g[0].lower() or s in g[1] or s in g[2]]

if rows:
    table(["المصطلح الإنجليزي", "المقابل العربي", "الشرح"],
          [[f"<code style='direction:ltr'>{a}</code>", f"<b>{b}</b>", c]
           for a, b, c in rows])
    st.caption(f"عدد النتائج: {len(rows)} من أصل {len(GLOSS)}.")
else:
    st.info("لا توجد نتائج مطابقة. جرّب كلمة أقصر.")

# ============================================================== المراجع
st.header("٢. المراجع")

st.markdown(
    "رُتّبت حسب الموضوع. المراجع المُعلَّمة بـ ⭐ هي الأساسية التي يُنصح "
    "بقراءتها أولاً."
)

REFS = {
    "منهج البوتستراب — المراجع الأساسية": [
        ("⭐ MacKinnon, J. G. (2007). <i>Bootstrap Hypothesis Testing</i>. "
         "Queen's Economics Department WP 1127 (rev. 2009).",
         "المرجع الرئيسي: صيغ قيمة p، اختيار عملية التوليد، البوتستراب المزدوج."),
        ("MacKinnon, J. G. (2006). <i>Bootstrap Methods in Econometrics</i>. "
         "QED WP 1028.",
         "مسح عام؛ مصدر حكم «شبه-معلمي يتفوّق على لا-معلمي بالكامل»."),
        ("⭐ Davidson, R. &amp; MacKinnon, J. G. (2000). Bootstrap tests: "
         "how many bootstraps? <i>Econometric Reviews</i> 19, 55–68.",
         "اختيار B، وخوارزمية الاختبار المسبق."),
        ("Davidson, R. &amp; MacKinnon, J. G. (2007). Improving the reliability "
         "of bootstrap tests with the fast double bootstrap. "
         "<i>CSDA</i> 51, 3259–3281. "
         "<span dir='ltr'>doi:10.1016/j.csda.2006.04.001</span>",
         "مصدر FDB."),
        ("Racine, J. &amp; MacKinnon, J. G. (2007). Simulation-based tests that "
         "can use any number of simulations. "
         "<i>Communications in Statistics</i> 36, 357–365.",
         "قيمة p المتّصلة."),
        ("Efron, B. (1979). Bootstrap methods: another look at the jackknife. "
         "<i>Annals of Statistics</i> 7, 1–26.",
         "الورقة المؤسِّسة."),
        ("Efron, B. (1987). Better bootstrap confidence intervals. "
         "<i>JASA</i> 82, 171–185.",
         "مجالات BCa."),
    ],
    "الوايلد بوتستراب": [
        ("⭐ Davidson, R. &amp; Flachaire, E. (2008). The wild bootstrap, "
         "tamed at last. <i>Journal of Econometrics</i> 146, 162–169. "
         "<span dir='ltr'>doi:10.1016/j.jeconom.2008.08.003</span>",
         "التوصية الحاسمة: Rademacher + بواقي مقيّدة + HC3."),
        ("Mammen, E. (1993). Bootstrap and wild bootstrap for high dimensional "
         "linear models. <i>Annals of Statistics</i> 21(1), 255–285.",
         "التوزيع ثنائي النقطة F1 والتأسيس النظري."),
        ("Härdle, W. &amp; Mammen, E. (1993). Comparing nonparametric versus "
         "parametric regression fits. "
         "<i>Annals of Statistics</i> 21(4), 1926–1947.",
         "الورقة التي صاغت تسمية «wild bootstrap»."),
        ("Wu, C. F. J. (1986). Jackknife, bootstrap and other resampling "
         "methods in regression analysis. "
         "<i>Annals of Statistics</i> 14, 1261–1295.",
         "أصل المخطّط المُرجَّح."),
        ("Liu, R. Y. (1988). Bootstrap procedures under some non-i.i.d. models. "
         "<i>Annals of Statistics</i> 16, 1696–1708.",
         "شرط E(ε³)=1، ونتيجة «لا حاجة لتوسيط البواقي»."),
        ("Flachaire, E. (2005). Bootstrapping heteroskedastic regression "
         "models: wild bootstrap vs. pairs bootstrap. "
         "<i>CSDA</i> 49, 361–376.",
         "الحجّة المفاهيمية لتفضيل الوايلد على الأزواج."),
        ("White, H. (1980). A heteroskedasticity-consistent covariance matrix "
         "estimator and a direct test for heteroskedasticity. "
         "<i>Econometrica</i> 48(4), 817–838.",
         "أصل HCCME واختبار White."),
        ("MacKinnon, J. G. &amp; White, H. (1985). Some "
         "heteroskedasticity-consistent covariance matrix estimators with "
         "improved finite sample properties. "
         "<i>Journal of Econometrics</i> 29, 305–325.",
         "تعريفات HC1 وHC2 وHC3."),
    ],
    "إعادة المعاينة في السلاسل الزمنية": [
        ("Bühlmann, P. (1997). Sieve bootstrap for time series. "
         "<i>Bernoulli</i> 3, 123–148.",
         "بوتستراب الغربال."),
        ("Künsch, H. R. (1989). The jackknife and the bootstrap for general "
         "stationary observations. <i>Annals of Statistics</i> 17, 1217–1241.",
         "بوتستراب الكتل المتحرّكة."),
        ("Politis, D. N. &amp; Romano, J. P. (1994). The stationary bootstrap. "
         "<i>JASA</i> 89(428), 1303–1313.",
         "البوتستراب الساكن."),
        ("Shao, X. (2010). The dependent wild bootstrap. "
         "<i>JASA</i> 105, 218–235.",
         "الوايلد المعتمِد — أصل فكرة BWB."),
        ("Gonçalves, S. &amp; Kilian, L. (2004). Bootstrapping autoregressions "
         "with conditional heteroskedasticity of unknown form. "
         "<i>Journal of Econometrics</i> 123, 89–120.",
         "صلاحية الوايلد في النماذج الانحدارية الذاتية."),
    ],
    "الارتباط الذاتي": [
        ("⭐ Godfrey, L. G. &amp; Tremayne, A. R. (2005). The wild bootstrap "
         "and heteroskedasticity-robust tests for serial correlation in "
         "dynamic regression models. <i>CSDA</i> 49, 377–395.",
         "LM_HR وMLM_HR، وتوصية الوايلد بـ Rademacher."),
        ("Breusch, T. S. (1978). Testing for autocorrelation in dynamic linear "
         "models. <i>Australian Economic Papers</i> 17, 334–355.", "أصل BG."),
        ("Godfrey, L. G. (1978). Testing against general autoregressive and "
         "moving average error models when the regressors include lagged "
         "dependent variables. <i>Econometrica</i> 46, 1303–1310.", "أصل BG."),
        ("Jeong, J. &amp; Chung, S. (2001). Bootstrap tests for autocorrelation. "
         "<i>CSDA</i> 38, 49–69.",
         "BDW وB-ρ̂ وBCa-ρ̂؛ القضاء على المنطقة غير الحاسمة."),
        ("Mantalos, P. &amp; Shukur, G. (2008). Bootstrap methods for "
         "heteroskedastic regression models. "
         "<i>Economic Modelling</i> 25, 1040–1050.",
         "أخطاء غير مترابطة لكن غير مستقلّة؛ نجاة البوتستراب الساكن والوايلد."),
    ],
    "عدم تجانس التباين": [
        ("⭐ Dufour, J.-M., Khalaf, L., Bernard, J.-T. &amp; Genest, I. (2004). "
         "Simulation-based finite-sample tests for heteroskedasticity and ARCH "
         "effects. <i>Journal of Econometrics</i> 122, 317–347.",
         "الاختبارات المضبوطة؛ محورية كل إحصاءات تجانس التباين."),
        ("Breusch, T. S. &amp; Pagan, A. R. (1979). A simple test for "
         "heteroscedasticity and random coefficient variation. "
         "<i>Econometrica</i> 47(5), 1287–1294.",
         "اختبار BP، وملاحظتهما المبكّرة عن مونت كارلو."),
        ("Koenker, R. (1981). A note on studentizing a test for "
         "heteroscedasticity. <i>Journal of Econometrics</i> 17, 107–112.",
         "النسخة المُستودنة."),
        ("Cribari-Neto, F. &amp; Zarkos, S. G. (1999). Bootstrap methods for "
         "heteroskedastic regression models: evidence on estimation and "
         "testing. <i>Econometric Reviews</i> 18(2), 211–228.",
         "مقارنة أربعة مخطّطات؛ تفوّق البوتستراب عند التصاميم غير المواتية."),
        ("Engle, R. F. (1982). Autoregressive conditional heteroscedasticity "
         "with estimates of the variance of United Kingdom inflation. "
         "<i>Econometrica</i> 50, 987–1007.", "اختبار ARCH LM."),
    ],
    "الاعتدالية": [
        ("⭐ Jarque, C. M. &amp; Bera, A. K. (1980). Efficient tests for "
         "normality, homoscedasticity and serial independence of regression "
         "residuals. <i>Economics Letters</i> 6, 255–259.",
         "التفكيك المشترك NHI — الورقة الأصلية."),
        ("Kilian, L. &amp; Demiroglu, U. (2000). Residual-based tests for "
         "normality in autoregressions: asymptotic theory and simulation "
         "evidence. <i>JBES</i> 18(1), 40–50.",
         "صلاحية JB في VAR المتكاملة؛ البوتستراب المعلمي."),
        ("Psaradakis, Z. &amp; Vávra, M. (2020). Normality tests for dependent "
         "data: large-sample and bootstrap approaches. "
         "<i>Communications in Statistics – Simulation and Computation</i> "
         "49(2), 283–304.",
         "مقارنة تسعة اختبارات؛ تفوّق بوتستراب JB."),
        ("Lobato, I. N. &amp; Velasco, C. (2004). A simple test of normality "
         "for time series. <i>Econometric Theory</i> 20, 671–689.",
         "الاختبار بلا نواة ولا عرض نطاق."),
        ("Bai, J. &amp; Ng, S. (2005). Tests for skewness, kurtosis, and "
         "normality for time series data. <i>JBES</i> 23, 49–60.", ""),
    ],
    "الاستقرار الهيكلي": [
        ("⭐ MacKinnon (2007), §7 — انظر أعلاه.",
         "المقارنة الشاملة لمخطّطات البوتستراب في اختبارات supF."),
        ("⭐ O'Reilly, G. &amp; Whelan, K. (2005). Testing parameter stability: "
         "a wild bootstrap approach. Central Bank of Ireland 8/RT/05.",
         "الوايلد المُعدَّل للتحيّز هو الأفضل إجمالاً."),
        ("Diebold, F. X. &amp; Chen, C. (1996). Testing structural stability "
         "with endogenous breakpoint: a size comparison of analytic and "
         "bootstrap procedures. "
         "<i>Journal of Econometrics</i> 70, 221–241.",
         "أول تقييم منهجي؛ تفوّق بوتستراب البواقي التكراري."),
        ("Krämer, W., Ploberger, W. &amp; Alt, R. (1988). Testing for "
         "structural change in dynamic models. "
         "<i>Econometrica</i> 56(6), 1355–1369.",
         "Theorem 1 وTheorem 2 — نتيجة القوّة التافهة عند التعامد."),
        ("Ploberger, W., Krämer, W. &amp; Alt, R. (1989). A modification of "
         "the CUSUM test in the linear regression model with lagged dependent "
         "variables. <i>Empirical Economics</i> 14, 65–75.", ""),
        ("Andrews, D. W. K. (1993). Tests for parameter instability and "
         "structural change with unknown change point. "
         "<i>Econometrica</i> 61, 821–856.",
         "القيم الحرجة التقاربية لـ supF."),
        ("Hansen, B. E. (2000). Testing for structural change in conditional "
         "models. <i>Journal of Econometrics</i> 97, 93–115.",
         "بوتستراب المتغيّرات المُثبّتة."),
        ("Lee, S. &amp; Baek, C. (2020). A CUSUM test for change points in "
         "nonlinear time series with the block wild bootstrap. "
         "<i>CSDA</i> 150, 106996.", "CUSUM-BWB."),
        ("Jin, H., Tian, Z. &amp; Qin, R. (2009). Bootstrap tests for "
         "structural change with infinite variance observations. "
         "<i>Statistics &amp; Probability Letters</i> 79, 1985–1995.", ""),
        ("Oh, H. &amp; Lee, S. (2018). On score vector- and residual-based "
         "CUSUM tests in ARMA–GARCH models. "
         "<i>Journal of the Korean Statistical Society</i>.", ""),
        ("Dufour, J.-M. &amp; Kiviet, J. F. (1996). Exact tests for structural "
         "change in first-order dynamic models. "
         "<i>Journal of Econometrics</i> 70, 39–68.",
         "الطريق المضبوط الوحيد للنماذج الديناميكية."),
        ("Brown, R. L., Durbin, J. &amp; Evans, J. M. (1975). Techniques for "
         "testing the constancy of regression relationships over time. "
         "<i>JRSS-B</i> 37, 149–192.", "أصل CUSUM وCUSUM-of-squares."),
    ],
    "الشكل الدالي واختبارات التحديد": [
        ("⭐ Stute, W., González Manteiga, W. &amp; Presedo Quindimil, M. "
         "(1998). Bootstrap approximations in model checks for regression. "
         "<i>JASA</i> 93(441), 141–149.",
         "عدم اتّساق بوتستراب الأزواج؛ اتّساق الوايلد."),
        ("Domínguez, M. A. &amp; Lobato, I. N. (2019). Specification testing "
         "with estimated variables. <i>Econometric Reviews</i> 39(5). "
         "<span dir='ltr'>doi:10.1080/07474938.2019.1687116</span>",
         "النسخ اللامعلمية من BG وRESET واختبار Wooldridge."),
        ("Ramsey, J. B. (1969). Tests for specification errors in classical "
         "linear least-squares regression analysis. "
         "<i>JRSS-B</i> 31, 350–371.", "اختبار RESET."),
    ],
    "عائلة ARDL والتكامل المشترك": [
        ("⭐ Pesaran, M. H., Shin, Y. &amp; Smith, R. J. (2001). Bounds testing "
         "approaches to the analysis of level relationships. "
         "<i>Journal of Applied Econometrics</i> 16, 289–326. "
         "<span dir='ltr'>doi:10.1002/jae.616</span>",
         "اختبار الحدود الأصلي."),
        ("⭐ McNown, R., Sam, C. Y. &amp; Goh, S. K. (2018). Bootstrapping the "
         "autoregressive distributed lag test for cointegration. "
         "<i>Applied Economics</i> 50(13), 1509–1521. "
         "<span dir='ltr'>doi:10.1080/00036846.2017.1366643</span>",
         "الاختبار الثالث والقيم الحرجة بالبوتستراب."),
        ("⭐ Sam, C. Y., McNown, R. &amp; Goh, S. K. (2019). An augmented "
         "autoregressive distributed lag bounds test for cointegration. "
         "<i>Economic Modelling</i> 80, 130–141. "
         "<span dir='ltr'>doi:10.1016/j.econmod.2018.11.001</span>",
         "القيم الحرجة الجاهزة للعيّنات الصغيرة والتقاربية."),
        ("Yilanci, V., Bozoklu, S. &amp; Gorus, M. S. (2020). Are BRICS "
         "countries pollution havens? Evidence from a bootstrap ARDL bounds "
         "testing approach with a Fourier function. "
         "<i>Sustainable Cities and Society</i> 55, 102035. "
         "<span dir='ltr'>doi:10.1016/j.scs.2020.102035</span>",
         "إدخال دالّة Fourier."),
        ("Bertelli, S., Vacca, G. &amp; Zoia, M. (2022). Bootstrap "
         "cointegration tests in ARDL models. "
         "<i>Economic Modelling</i> 116, 105987. "
         "<span dir='ltr'>doi:10.1016/j.econmod.2022.105987</span>",
         "اشتقاق تحت عدّة عمليات توليد بما فيها الحالات المتدهورة."),
        ("Gallant, A. R. &amp; Souza, G. (1991). On the asymptotic normality "
         "of Fourier flexible form estimates. "
         "<i>Journal of Econometrics</i> 50, 329–353.",
         "أساس تقريب Fourier للتغيّر الهيكلي."),
        ("Kripfganz, S. &amp; Schneider, D. C. (2020). Response surface "
         "regressions for critical value bounds and approximate p-values in "
         "equilibrium correction models. "
         "<i>Oxford Bulletin of Economics and Statistics</i> 82(6), "
         "1456–1481. "
         "<span dir='ltr'>doi:10.1111/obes.12377</span>",
         "القيم الحرجة المضبوطة للعيّنات المنتهية المستعملة في "
         "<code style='direction:ltr'>type(fardl)</code>."),
        ("Granger, C. W. J. &amp; Newbold, P. (1974). Spurious regressions in "
         "econometrics. <i>Journal of Econometrics</i> 2, 111–120.", ""),
    ],
    "الحزم البرمجية": [
        ("Roudane, M. (2026). <code>bootdiag</code>: Bootstrap and Monte Carlo "
         "post-estimation diagnostic tests. "
         "Statistical Software Components, Boston College.",
         "<code style='direction:ltr'>ssc install bootdiag</code>"),
        ("Roudane, M. <code>aardl</code>: Augmented ARDL cointegration analysis "
         "with Fourier terms, bootstrap inference and asymmetric dynamics. SSC.",
         "<b>ثمانية أنواع</b>: aardl, baardl, <b>faardl</b>, <b>fbaardl</b>, "
         "nardl, banardl, <b>fanardl</b>, <b>fbanardl</b>. "
         "<code style='direction:ltr'>ssc install aardl</code>"),
        ("Roudane, M. <code>fbardl</code>: Fourier Bootstrap ARDL "
         "cointegration test. SSC.",
         "<b>ثلاثة إجراءات</b>: <code>fardl</code> (سطح استجابة)، "
         "<code>fbardl_mcnown</code> (بوتستراب غير مشروط)، "
         "<code>fbardl_bvz</code> (بوتستراب مشروط). "
         "<code style='direction:ltr'>ssc install fbardl</code>"),
        ("Roudane, M. <code>fbnardl</code>: Fourier Bootstrap Nonlinear "
         "ARDL. SSC.",
         "نوعان: <code>fnardl</code> و<code>fbnardl</code>. "
         "<code style='direction:ltr'>ssc install fbnardl</code>"),
        ("Roudane, M. <code>mtnardl</code>: Multiple-threshold NARDL. SSC.",
         "<code style='direction:ltr'>ssc install mtnardl</code>"),
        ("Kripfganz, S. &amp; Schneider, D. C. <code>ardl</code>: "
         "Estimating autoregressive distributed lag and equilibrium correction "
         "models. SSC.",
         "<code style='direction:ltr'>ssc install ardl</code>"),
        ("Vacca, G. &amp; Zoia, M. <code>bootCT</code>: Bootstrap "
         "cointegration tests in ARDL models. R package, CRAN.", ""),
    ],
}

for sec, items in REFS.items():
    with st.expander(f"📚 {sec}  ({len(items)})",
                     expanded=sec.startswith("منهج")):
        table(["المرجع", "لماذا يهمّ"],
              [[a, b] for a, b in items])

# ============================================================== خاتمة
st.divider()
st.header("٣. خريطة قراءة مقترحة")

card(
    "لو كان عندك وقت لقراءة خمس أوراق فقط",
    "<ol style='padding-right:20px;line-height:2.2'>"
    "<li><b>MacKinnon (2007)</b> — لتفهم المنهج كلّه في مكان واحد.</li>"
    "<li><b>Davidson &amp; Flachaire (2008)</b> — لتعرف أي نسخة من الوايلد "
    "تستعمل ولماذا.</li>"
    "<li><b>Dufour et al. (2004)</b> — لتكتشف أنّ كثيراً من اختباراتك "
    "يمكن أن يكون <b>مضبوطاً</b> لا تقريبياً.</li>"
    "<li><b>Godfrey &amp; Tremayne (2005)</b> — للتطبيق المباشر على اختبار "
    "الارتباط الذاتي.</li>"
    "<li><b>McNown, Sam &amp; Goh (2018)</b> — إن كنت تعمل بـ ARDL، "
    "فهذه الورقة ستُغيّر طريقة قراءتك لنتائجك.</li>"
    "</ol>",
    "blue",
)

st.html(
    '<div style="background:linear-gradient(120deg,#E8F0FE,#E0F7F4);'
    'border-radius:18px;padding:24px;margin-top:20px;text-align:center;'
    'border:1px solid #CFE6F5">'
    '<p style="margin:0;font-size:1.05rem;color:#13254A;line-height:2">'
    '<b>منصّة البوتستراب والاختبارات البعدية</b><br>'
    'إعداد: د. مروان رودان — '
    '<span style="direction:ltr;unicode-bidi:embed">Dr Merwan Roudane</span>'
    '</p>'
    '<p style="margin:10px 0 0 0;font-size:.9rem;color:#51637F">'
    'كل الصيغ في هذه المنصّة مأخوذة من الأوراق الأصلية المذكورة أعلاه، '
    'وكل الأرقام الحيّة محسوبة بمحرّك المنصّة نفسه ويمكن إعادة إنتاجها '
    'من صفحة «مختبر مونت كارلو».</p></div>'
)
