# منصّة البوتستراب والاختبارات البعدية

**Bootstrap & Bootstrap-Based Diagnostic Tests — an Arabic interactive guide**

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bootardl.streamlit.app/)

🔗 **المنصّة مباشرةً:** <https://bootardl.streamlit.app/>

منصّة تعليمية تفاعلية باللغة العربية تشرح البوتستراب (Bootstrap) من الصفر،
وأنواعه، والاختبارات البعدية (post-estimation diagnostic tests) المعتمدة عليه،
وعائلة Bootstrap ARDL — مع رسوم متحرّكة، ومحرّك محاكاة حيّ، ومختبر تفاعلي.

إعداد: **د. مروان رودان** — Dr Merwan Roudane
مؤلّف حزم `bootdiag`، `aardl`، `fbardl`، `fbnardl`، `mtnardl` في أرشيف SSC
الخاص ببرنامج Stata.

---

## لماذا هذه المنصّة

كل اختبار بعدي تستعمله اليوم يقارن إحصاءه بجدول `χ²` أو `F` صحيح فقط عند حجم
عيّنة لانهائي. وعيّناتنا ليست لانهائية. النتيجة تشوّه في الحجم موثّق جيداً:

| الاختبار | n=60, ρ=0.5 | n=60, ρ=0.9 | n=150, ρ=0.9 |
|---|---|---|---|
| Koenker — تقاربي | 11.3% | **19.7%** | 16.3% |
| Koenker — بوتستراب | 2.0% | **6.0%** | 3.0% |
| Jarque–Bera — تقاربي | 4.0% | 2.7% | 2.7% |
| Jarque–Bera — بوتستراب | 3.3% | 3.7% | 5.0% |

نسبة الرفض الصحيحة تحت فرضية صفرية صحيحة هي 5٪.
المصدر: تجربة مونت كارلو ضمن حزمة `bootdiag`، 300 تكرار.

---

## المحتوى — أربع عشرة صفحة

**البداية**
1. الصفحة الرئيسية
2. لماذا نحتاج البوتستراب؟ — النظرية التقاربية، مشاكل العيّنات الصغيرة *والكبيرة*

**أساسيات البوتستراب**

3. الفكرة من الصفر — مبدأ الإحلال، السحب مع الإرجاع، بناء التوزيع
4. أنواع البوتستراب — أحد عشر نوعاً مع شجرة قرار
5. الوايلد بوتستراب — Rademacher مقابل Mammen، وHC0 حتى HC3
6. قيمة p وعدد التكرارات B — الصيغ الأربع، سرّ العدد 999، FDB

**الاختبارات البعدية**

7. الاختبارات العادية — DW، BG، BP، Koenker، White، JB، CUSUM، RESET
8. الاختبارات بالبوتستراب — الخوارزمية، جدول مطابقة DGP، الاختبار المشترك NHI
9. الاستقرار الهيكلي — CUSUM وsupF بحِزَم بوتستراب

**التطبيق**

10. مختبر مونت كارلو — شغّل تجربة الحجم بنفسك
11. المختبر التفاعلي — ارفع بياناتك وشغّل البطارية الكاملة

**الحزم البرمجية**

12. حزمة `bootdiag` — التوثيق الكامل
13. عائلة Bootstrap ARDL — من اختبار الحدود إلى FBA-ARDL

**مراجع**

14. المصطلحات والمراجع

---

## التشغيل

**على الإنترنت** — لا يحتاج أي تثبيت:
<https://bootardl.streamlit.app/>

**محلياً:**

```bash
git clone https://github.com/merwanroudane/bootardl.git
cd bootardl
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## بنية المشروع

```
streamlit_app.py          نقطة الدخول والتنقّل
.streamlit/config.toml    السمة والألوان والخطوط
assets/logo.svg           الشعار
core/
    ui.py                 اتجاه RTL، الشريط الجانبي يميناً، لوحة الألوان، المكوّنات
    anim.py               أحد عشر رسماً متحرّكاً بأزرار تشغيل/إيقاف
    engine.py             محرّك البوتستراب: الإحصاءات وعمليات التوليد وقيم p
app_pages/                الصفحات الأربع عشرة
```

### محرّك البوتستراب — `core/engine.py`

**الإحصاءات المنفّذة:** Breusch–Godfrey (LM، LM_HR، MLM_HR)، Durbin–Watson،
ρ̂، Breusch–Pagan، Koenker، White، Engle ARCH LM، Szroeter SKH،
Harrison–McCabe، Jarque–Bera، Anderson–Darling، Ramsey RESET،
supF / aveF / expF، CUSUM، CUSUM of squares.

**عمليات توليد البوتستراب:** `wild`، `residual`، `fixed`، `sieve`، `block`،
`stationary`، `blockwild`، `normal` — كلّها مع توليد تكراري وإعادة بناء عمود
`y*_{t-1}` داخل مصفوفة التصميم.

**أوزان الوايلد:** Rademacher (F2)، Mammen (F1)، N(0,1).
**تحويلات البواقي:** HC0، HC1، HC2، HC3.
**قيم p:** الذيل الأعلى، المتماثلة، الذيلان المتساويان، مونت كارلو بتصحيح +1،
والمتّصلة لـ Racine & MacKinnon.

---

## ملاحظة منهجية مهمّة

**طابِق عملية توليد البوتستراب مع الفرضية الصفرية التي تختبرها.**
نتيجة محاكاة من محرّك هذه المنصّة (اختبار Koenker، n=50، ρ=0.9، 200 تكرار،
B=199، α=5٪، تحت فرضية صفرية صحيحة):

| عملية التوليد | أخطاء طبيعية | أخطاء t(5) |
|---|---|---|
| `wild` | 2.5% | 0.5% |
| `residual` | **5.5%** | **6.0%** |

الوايلد بوتستراب يحفظ `|û_t|` لكل t، أي أنّه يحفظ نمط عدم تجانس التباين الذي
يختبره الاختبار — فيصبح محافظاً أكثر من اللازم. لاختبارات تجانس التباين
والاعتدالية يجب أن تفرض عملية التوليد الفرضيةَ الصفرية فعلاً.

---

## الحزم المرتبطة في Stata

```stata
ssc install bootdiag, replace   // الاختبارات البعدية بالبوتستراب (28 اختباراً)
ssc install aardl,    replace   // Augmented ARDL — ثمانية أنواع
ssc install fbardl,   replace   // Fourier Bootstrap ARDL — ثلاثة إجراءات
ssc install fbnardl,  replace   // Fourier Bootstrap NARDL
ssc install mtnardl,  replace   // NARDL متعدّد العتبات
```

أنواع `aardl` الثمانية: `aardl`، `baardl`، **`faardl`** (FA-ARDL)،
**`fbaardl`** (FBA-ARDL)، `nardl`، `banardl`، **`fanardl`**، **`fbanardl`**.

إجراءات `fbardl` الثلاثة: `fardl` (قيم حرجة من سطح الاستجابة)،
`fbardl_mcnown` (بوتستراب غير مشروط)، `fbardl_bvz` (بوتستراب مشروط).

---

## المراجع الأساسية

- MacKinnon, J. G. (2007). *Bootstrap Hypothesis Testing*. QED WP 1127.
- Davidson, R. & Flachaire, E. (2008). The wild bootstrap, tamed at last.
  *Journal of Econometrics* 146, 162–169.
- Dufour, J.-M., Khalaf, L., Bernard, J.-T. & Genest, I. (2004).
  Simulation-based finite-sample tests for heteroskedasticity and ARCH effects.
  *Journal of Econometrics* 122, 317–347.
- Godfrey, L. G. & Tremayne, A. R. (2005). The wild bootstrap and
  heteroskedasticity-robust tests for serial correlation in dynamic regression
  models. *CSDA* 49, 377–395.
- McNown, R., Sam, C. Y. & Goh, S. K. (2018). Bootstrapping the autoregressive
  distributed lag test for cointegration. *Applied Economics* 50(13), 1509–1521.
- Sam, C. Y., McNown, R. & Goh, S. K. (2019). An augmented ARDL bounds test for
  cointegration. *Economic Modelling* 80, 130–141.
- Yilanci, V., Bozoklu, S. & Gorus, M. S. (2020). *Sustainable Cities and
  Society* 55, 102035.
- Bertelli, S., Vacca, G. & Zoia, M. (2022). Bootstrap cointegration tests in
  ARDL models. *Economic Modelling* 116, 105987.

القائمة الكاملة داخل المنصّة، صفحة «المصطلحات والمراجع».

---

## المؤلّف

**د. مروان رودان** — Dr Merwan Roudane

- المنصّة: <https://bootardl.streamlit.app/>
- المستودع: <https://github.com/merwanroudane/bootardl>
- GitHub: <https://github.com/merwanroudane>
- البريد: <merwanroudane920@gmail.com>
