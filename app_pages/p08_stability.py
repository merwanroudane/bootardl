"""الاستقرار الهيكلي: CUSUM وsupF بالبوتستراب."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.ui import hero, card, note, plotly, table, steps, PALETTE
from core.anim import anim_supf, anim_cusum
from core.engine import (simulate_dgp, design_from, ols, sup_f,
                         recursive_residuals, cusum_path, cusumsq_path,
                         bootstrap_sample)

hero(
    "الاستقرار الهيكلي — Parameter stability",
    "أخطر عائلة من الاختبارات البعدية، لأنّ فشلها يُبطل النتائج كلّها ولا "
    "تُصلحه الأخطاء المعيارية الحصينة. وهي أيضاً أكثر العائلات احتياجاً "
    "للبوتستراب: الحدود التقاربية هنا غير موثوقة بشكل موثّق جيداً.",
    "العائلة الأخطر",
    "#ECECFE", "#E8F0FE",
)

# ============================================================== 1. المشكلة
st.header("١. ما المقصود بـ «كسر هيكلي»؟")

card(
    "التعريف",
    "<p>نموذج الانحدار يفترض ضمناً أنّ المعالم <span dir='ltr'>β</span> "
    "<b>واحدة لكل المشاهدات</b>. لكن ماذا لو تغيّرت السياسة النقدية عام 2008؟ "
    "أو دخلت الدولة اتحاداً جمركياً؟ أو وقعت جائحة؟</p>"
    "<p>عندها تكون العلاقة الحقيقية:</p>"
    r"<p style='direction:ltr;text-align:center;background:#fff;padding:12px;"
    r"border-radius:10px'>"
    r"y<sub>t</sub> = X<sub>t</sub>β₁ + u<sub>t</sub>&nbsp;&nbsp;for t ≤ k<br>"
    r"y<sub>t</sub> = X<sub>t</sub>β₂ + u<sub>t</sub>&nbsp;&nbsp;for t &gt; k</p>"
    "<p>وتقديرك <span dir='ltr'>β̂</span> سيكون <b>متوسّطاً مرجّحاً</b> "
    "لعلاقتين مختلفتين — رقم لا يصف أياً منهما. والتنبؤ به كارثي.</p>"
    "<p><b>لماذا لا تُصلحه الأخطاء الحصينة؟</b> لأنّ المشكلة ليست في التباين "
    "بل في <b>المتوسّط الشرطي نفسه</b>. "
    "<span dir='ltr'>Newey–West</span> لن يُنقذك من نموذج مُشوّه.</p>",
    "rose",
)

st.subheader("حالتان مختلفتان تماماً")

c1, c2 = st.columns(2)
with c1:
    card(
        "تاريخ الكسر معلوم — Known breakpoint",
        "<p>تعرف التاريخ مسبقاً من المعرفة الاقتصادية (أزمة 2008 مثلاً).</p>"
        "<p><b>الاختبار:</b> Chow (1960) — إحصاء F بسيط:</p>"
        r"<p style='direction:ltr;text-align:center;font-size:.95em'>"
        r"F = [(SSR − SSR₁ − SSR₂)/k] ⁄ [(SSR₁+SSR₂)/(n−2k)]</p>"
        "<p>توزيعه <span dir='ltr'>F(k, n−2k)</span> — قياسي تماماً.</p>",
        "blue",
    )
with c2:
    card(
        "تاريخ الكسر مجهول — Unknown breakpoint",
        "<p>وهذه هي الحالة الواقعية في 95٪ من الأبحاث.</p>"
        "<p><b>الاختبار:</b> احسب Chow F عند <b>كل</b> تاريخ محتمل، "
        "ثم خذ الأقصى: <span dir='ltr'>supF</span>.</p>"
        "<p style='color:#B4455C'><b>المشكلة:</b> أخذُ الحدّ الأقصى عبر "
        "مئات الاختبارات يُفسد التوزيع تماماً. "
        "<span dir='ltr'>supF</span> <b>لا يتبع F</b> ولا "
        "<span dir='ltr'>χ²</span>. توزيعه غير قياسي، "
        "من Andrews (1993) وHansen (1997).</p>",
        "orange",
    )

note(
    "<b>التشذيب (Trimming):</b> لا يمكن اختبار كل التواريخ: "
    "قرب الطرفين لا توجد مشاهدات كافية في أحد الجانبين. "
    "لذلك نقتصر على <span dir='ltr'>τ ∈ [π, 1−π]</span> حيث "
    "<span dir='ltr'>π = 0.15</span> عادةً — أي نتجاهل أول وآخر 15٪ من العيّنة. "
    "هذا الاختيار <b>يؤثّر على التوزيع الصفري</b>، "
    "فاذكره دائماً في ورقتك.",
    "amber", "✂️",
)

# ============================================================== 2. supF
st.header("٢. supF بالأنيميشن")

c1, c2, c3 = st.columns(3)
with c1:
    n_s = st.slider("حجم العيّنة T", 50, 300, 120, key="st_n")
with c2:
    rho_s = st.slider("المثابرة ρ", 0.0, 0.95, 0.6, 0.05, key="st_rho")
with c3:
    brk_s = st.slider("حجم الكسر في المنتصف", 0.0, 3.0, 1.2, 0.2, key="st_brk")

trim_s = st.slider("نسبة التشذيب π", 0.05, 0.30, 0.15, 0.05, key="st_trim")


@st.cache_data(show_spinner="جارٍ حساب حِزَم البوتستراب…")
def _stab(n, rho, brk, trim, B=399, seed=909):
    rng = np.random.default_rng(seed)
    d = simulate_dgp(n, rho, 1.0, 0.0, "normal", brk, rng)
    y, X = design_from(d["y"], d["x"])
    r = ols(y, X)
    sup, ave, exp_, Fs, dates = sup_f(y, X, trim)

    # توزيع supF الصفري وحِزَم CUSUM من البوتستراب
    w0 = recursive_residuals(y, X)
    path0 = cusum_path(w0)
    sq0 = cusumsq_path(w0)
    L = len(path0)

    sups, paths, sqs = [], [], []
    for _ in range(B):
        ys, Xs = bootstrap_sample(X, r["b"], r["u"], r["h"], "wild",
                                  "rademacher", "hc3", rng, 1)
        s, _, _, _, _ = sup_f(ys, Xs, trim)
        sups.append(s)
        ws = recursive_residuals(ys, Xs)
        if len(ws) == L:
            paths.append(cusum_path(ws))
            sqs.append(cusumsq_path(ws))
    P = np.array(paths)
    Q = np.array(sqs)
    return dict(
        y=d["y"], Fs=Fs, dates=dates, sup=sup, ave=ave, exp=exp_,
        sup_boot=np.array(sups), path=path0, sq=sq0,
        band_lo=np.quantile(P, 0.025, 0), band_hi=np.quantile(P, 0.975, 0),
        sq_lo=np.quantile(Q, 0.025, 0), sq_hi=np.quantile(Q, 0.975, 0),
        L=L,
    )


S = _stab(int(n_s), float(rho_s), float(brk_s), float(trim_s))

crit_b = float(np.quantile(S["sup_boot"], 0.95))
m1, m2, m3, m4 = st.columns(4)
m1.metric("supF المحسوب", f"{S['sup']:.3f}")
m2.metric("القيمة الحرجة 5٪ — بوتستراب", f"{crit_b:.3f}")
m3.metric("p — بوتستراب", f"{float((S['sup_boot'] > S['sup']).mean()):.3f}")
m4.metric("تاريخ الكسر المقدَّر",
          f"t = {int(S['dates'][int(np.argmax(S['Fs']))])}" if len(S["dates"]) else "—")

plotly(anim_supf(S["dates"], S["Fs"], crit_b), key="st_supf")

note(
    "راقب كيف يتسلّق الخط ثم يبلغ ذروته. موضع الذروة هو "
    "<b>تقديرك لتاريخ الكسر</b> — وهذه معلومة قيّمة بحدّ ذاتها، "
    "لا مجرّد ناتج ثانوي للاختبار.",
    "indigo", "📍",
)

# السلسلة نفسها
figy = go.Figure()
figy.add_trace(go.Scatter(y=S["y"], mode="lines", name="السلسلة y",
                          line=dict(color=PALETTE["blue"], width=2)))
if len(S["dates"]):
    bk = int(S["dates"][int(np.argmax(S["Fs"]))])
    figy.add_vline(x=bk, line=dict(color=PALETTE["rose"], width=2.5, dash="dash"),
                   annotation_text="الكسر المقدَّر")
figy.add_vline(x=int(n_s) // 2, line=dict(color=PALETTE["green"], width=2,
                                          dash="dot"),
               annotation_text="الكسر الحقيقي", annotation_position="bottom right")
figy.update_layout(height=280, margin=dict(l=40, r=30, t=50, b=40),
                   title=dict(text="السلسلة المولّدة", x=0.98, xanchor="right"),
                   showlegend=False,
                   xaxis=dict(title="t", gridcolor="#E9EFF9"),
                   yaxis=dict(title="y", gridcolor="#E9EFF9"))
plotly(figy, key="st_series")

st.subheader("عائلة Andrews–Ploberger: supF و aveF و expF")

table(
    ["الإحصاء", "الصيغة", "ضد أي بديل هو الأقوى"],
    [
        ["<b>supF</b>", "<span dir='ltr'>max<sub>τ</sub> F(τ)</span>",
         "كسر <b>مفاجئ وحاد</b> في تاريخ واحد"],
        ["<b>aveF</b>", "<span dir='ltr'>mean<sub>τ</sub> F(τ)</span>",
         "تغيّر <b>تدريجي</b> أو عدّة كسور صغيرة"],
        ["<b>expF</b>", "<span dir='ltr'>log mean<sub>τ</sub> exp(F(τ)/2)</span>",
         "حلّ وسط — الأمثل ضد بدائل محلّية بعيدة"],
    ],
)

note(
    "<b>تحذير تقني مهم:</b> قيم p البوتستراب ثابتة تحت التحويلات الرتيبة، "
    "لذا <span dir='ltr'>BootSupW ≡ BootSupLR ≡ BootSupLM</span>. "
    "<b>لكن هذا لا ينطبق على aveF وexpF</b> — فهما ليسا تحويلين رتيبين، "
    "ولهما توزيعان بوتستراب مختلفان فعلاً "
    "(Diebold &amp; Chen 1996).",
    "amber", "⚠️",
)

# ============================================================== 3. CUSUM
st.header("٣. CUSUM — المجموع التراكمي")

card(
    "الفكرة: البواقي التكرارية",
    "<p>بدل تقدير النموذج مرّة واحدة على كل العيّنة، نُقدّره <b>تكرارياً</b>: "
    "على أول k مشاهدة، ثم k+1، ثم k+2…</p>"
    "<p>في كل خطوة، نتنبّأ بالمشاهدة <b>التالية</b> ونقيس خطأ التنبؤ مُقيَّساً:</p>"
    r"<p style='direction:ltr;text-align:center;background:#fff;padding:12px;"
    r"border-radius:10px;font-size:.95em'>"
    r"w<sub>r</sub> = (y<sub>r</sub> − z'<sub>r</sub>δ̂<sup>(r−1)</sup>) ⁄ f<sub>r</sub><br>"
    r"f<sub>r</sub> = [1 + z'<sub>r</sub>(Z<sup>(r−1)'</sup>Z<sup>(r−1)</sup>)<sup>−1</sup>"
    r"z<sub>r</sub>]<sup>1/2</sup></p>"
    "<p>هذه هي <b>البواقي التكرارية</b> "
    "(<span class='bs-en'>recursive residuals</span>)، "
    "وهي iid بتباين σ² تحت الاستقرار.</p>"
    "<p>ثم نجمعها تراكمياً. <b>إن كانت المعالم مستقرّة</b> فالمجموع يتجوّل حول "
    "الصفر كمسار عشوائي. <b>وإن حدث كسر</b> فأخطاء التنبؤ تصبح منحازة في "
    "اتجاه واحد فينجرف المجموع بعيداً.</p>"
    "<p>الإحصاء الرسمي (Krämer, Ploberger &amp; Alt 1988):</p>"
    r"<p style='direction:ltr;text-align:center;font-size:.92em'>"
    r"S = max<sub>r</sub> |W(r)| ⁄ [√(T−K−1) + 2(r−K−1)/√(T−K−1)]</p>",
    "violet",
)

st.subheader("المشكلة التقاربية — ولماذا الحِزَم البوتستراب ضرورية")

card(
    "ثلاث نتائج من Krämer, Ploberger &amp; Alt (1988) و Ploberger et al. (1989)",
    "<p><b>Theorem 1 — خبر جيّد:</b> اختبار CUSUM الديناميكي المباشر "
    "<b>يحتفظ بمستواه التقاربي</b> حتى مع وجود متغيّر تابع مُبطّأ. "
    "وكذلك تعديل Dufour (1982).</p>"
    "<p><b>لكن في العيّنات المنتهية:</b> كلاهما <b>ناقص الحجم</b>. "
    "والمفاجأة أنّ التقريب التقاربي يعمل <b>أفضل</b> لـ CUSUM الديناميكي "
    "البسيط، بينما اختبار Dufour <b>غير متشابه بشدّة</b> "
    "(<span class='bs-en'>extremely non-similar</span>) — "
    "أي أنّ حجمه يعتمد اعتماداً حاسماً على γ.</p>"
    "<p style='background:#FEECEF;padding:12px;border-radius:10px'>"
    "<b>Theorem 2 — النتيجة الأهم عملياً:</b> "
    "إذا كان الانزياح <span dir='ltr'>g(z)</span> "
    "<b>متعامداً على متوسّط متّجه المتغيّرات d</b>، "
    "فإنّ لاختبار CUSUM <b>قوّة محلّية تافهة فقط</b>. "
    "وتنخفض القوّة كلّما كبرت الزاوية بين <span dir='ltr'>Δδ</span> و"
    "<span dir='ltr'>d</span>؛ وعند 90° (كسر في الميل فقط) "
    "<b>تساوي القوّة الحجم</b> — أي أنّ الاختبار أعمى تماماً.</p>"
    "<p>وهذا يُفسّر النتيجة الصفرية الشهيرة لـ Garbade (1977): "
    "تصميمه كان <span dir='ltr'>d = 0</span>!</p>"
    "<p><b>نصيحة تقنية:</b> استعمل σ̂ على طريقة Harvey (1975) — "
    "المبنية على البواقي التكرارية حول <b>متوسّطها هي</b> "
    "<span dir='ltr'>w̄</span> — لا صيغة OLS. "
    "لأنّ <span dir='ltr'>w̄ ≠ 0</span> تحت الكسر، وهذا يرفع القوّة.</p>",
    "rose",
)

st.subheader("شاهد CUSUM مع الحِزَم البوتستراب")

st.markdown(
    "المنطقة الفيروزية هي **حِزَم البوتستراب**: مئينات 2.5٪ و97.5٪ لمسارات "
    "CUSUM المولّدة **تحت الاستقرار** من نموذجك أنت. "
    "قارنها بالخطوط التقاربية المستقيمة لـ Brown–Durbin–Evans."
)

L = S["L"]
a = 0.948  # ثابت BDE عند 5%
r_idx = np.arange(1, L + 1)
asy_hi = a * (np.sqrt(L) + 2 * r_idx / np.sqrt(L))
asy_lo = -asy_hi

plotly(anim_cusum(S["path"], (S["band_lo"], S["band_hi"]),
                  (asy_lo, asy_hi)), key="st_cusum")

out_b = int(((S["path"] > S["band_hi"]) | (S["path"] < S["band_lo"])).sum())
out_a = int(((S["path"] > asy_hi) | (S["path"] < asy_lo)).sum())
c1, c2 = st.columns(2)
c1.metric("نقاط خارج حزمة البوتستراب", out_b)
c2.metric("نقاط خارج الحزمة التقاربية", out_a)

note(
    "لاحظ شكل الحزمتين: الحزمة التقاربية <b>مستقيمة ومتباعدة</b> لأنّها "
    "مشتقّة من حركة براونية مثالية. أمّا حزمة البوتستراب فهي "
    "<b>منحنية وتتبع تذبذب بياناتك الفعلي</b> — لأنّها مبنية من مسارات مولّدة "
    "من نموذجك بمثابرته وتباينه. "
    "هذا بالضبط ما تُنتجه حزمة bootdiag بالخيار "
    "<code style='direction:ltr'>stab, graph</code>، وليس له نظير قياسي في Stata.",
    "teal", "📊",
)

# CUSUM of squares
st.subheader("CUSUM of squares — للكسر في التباين")

figsq = go.Figure()
t_sq = np.arange(1, L + 1)
figsq.add_trace(go.Scatter(x=t_sq, y=S["sq_hi"], mode="lines",
                           name="حزمة البوتستراب 95٪",
                           line=dict(color=PALETTE["teal"], width=2)))
figsq.add_trace(go.Scatter(x=t_sq, y=S["sq_lo"], mode="lines", showlegend=False,
                           line=dict(color=PALETTE["teal"], width=2),
                           fill="tonexty", fillcolor="rgba(20,184,166,.10)"))
figsq.add_trace(go.Scatter(x=t_sq, y=S["sq"], mode="lines",
                           name="CUSUM of squares",
                           line=dict(color=PALETTE["orange"], width=3)))
figsq.add_trace(go.Scatter(x=t_sq, y=t_sq / L, mode="lines",
                           name="الخط المتوقّع r/m",
                           line=dict(color=PALETTE["slate"], width=2, dash="dot")))
figsq.update_layout(height=360, margin=dict(l=40, r=30, t=55, b=45),
                    title=dict(text="CUSUM of squares — حسّاس لتغيّر التباين",
                               x=0.98, xanchor="right"),
                    legend=dict(orientation="h", y=1.12, x=0),
                    xaxis=dict(title="الزمن", gridcolor="#E9EFF9"),
                    yaxis=dict(title="S_r", gridcolor="#E9EFF9"))
plotly(figsq, key="st_cusumsq")

note(
    "فرق عملي مهم (Dufour &amp; Kiviet 1996): "
    "<b>Chow وCUSUM أكثر حساسية للانزياحات الدائمة</b>، "
    "بينما <b>الاختبار التنبؤي وCUSUM-of-squares يكشفان الانزياحات المؤقّتة "
    "بسهولة أكبر</b>. فاستعملهما معاً.",
    "amber", "💡",
)

# ============================================================== 4. الأدلة
st.header("٤. سلسلة الأدلّة: أي بوتستراب يعمل هنا؟")

st.markdown(
    "هذه هي النقطة التي اجتمعت فيها ثلاث أوراق مستقلّة على نتيجة واحدة:"
)

table(
    ["الورقة", "ما أضافته", "النتيجة"],
    [
        ["<b>Diebold &amp; Chen (1996)</b>",
         "أول تقييم منهجي",
         "الحجم التقاربي لـ supLM/supW/supLR <b>يتدهور بشدّة</b> مع T صغيرة "
         "وρ عالية. و<b>بوتستراب البواقي التكراري «يؤدّي أداءً ممتازاً، "
         "حتى في العيّنات الصغيرة مع ارتباط ذاتي عالٍ»</b>"],
        ["<b>MacKinnon (2007, §7)</b>",
         "مقارنة شاملة للمخطّطات",
         "✅ بوتستراب البواقي التكراري: <b>جيّد</b><br>"
         "❌ بوتستراب Hansen بالمتغيّرات المُثبّتة: "
         "<b>سيّئ تقريباً كالاختبار التقاربي</b><br>"
         "❌ بوتستراب الأزواج: نقص رفض يسوء مع تزايد k<br>"
         "❌ كتلة-الكتل: سيّئ<br>"
         "⚠️ <b>يجب فرض |ρ̂| &lt; 0.99</b><br>"
         "✅ FDB يُحسّنه أكثر؛ ❌ التصحيح الساذج 2ρ̂−ρ̄ لا يُفيد"],
        ["<b>O'Reilly &amp; Whelan (2005)</b>",
         "إضافة عدم تجانس التباين",
         "❌ التقاربي: سيّئ<br>"
         "❌ المتغيّرات المُثبّتة: <b>مفرط في الحجم بشدّة</b> عند ρ متوسّطة/عالية<br>"
         "⚠️ الغربال: جيّد تحت أخطاء كروية، لكن "
         "<b>مفرط تحت كسر في التباين (19٪ عند ρ=.95)</b><br>"
         "✅ <b>الوايلد (Rademacher، Davidson–Flachaire): الأفضل من الأربعة</b>، "
         "بلا كلفة كفاءة تحت الضوضاء البيضاء<br>"
         "🏆 <b>الوايلد المُعدَّل للتحيّز: الأفضل إجمالاً</b> — "
         "حجم ≈ .09–.11 لكل ρ &lt; .99"],
    ],
)

card(
    "لماذا يفشل بوتستراب المتغيّرات المُثبّتة بالذات؟",
    "<p>السبب مباشر ومفيد لفهم المبدأ العام:</p>"
    "<p>في بوتستراب Hansen (2000)، نُولّد "
    "<span dir='ltr'>u*_t ~ N(0,1)</span>، نضربها في البواقي، "
    "ونُعيد الانحدار. لكن المتغيّر التابع المُبطّأ "
    "<span dir='ltr'>y_{t−1}</span> <b>يبقى كما هو من البيانات الأصلية</b> — "
    "لا يُولَّد تكرارياً. ولهذا سُمّي «المتغيّرات المُثبّتة».</p>"
    "<p><b>والنتيجة:</b> عيّنات البوتستراب لا تحمل <b>مثابرة</b> بياناتك. "
    "فالتوزيع الصفري الذي تُنتجه هو توزيع عالم بلا مثابرة — "
    "وهو بالضبط التوزيع التقاربي. "
    "لهذا أداؤه «سيّئ تقريباً كالاختبار التقاربي»: "
    "<b>لأنّه هو الاختبار التقاربي، بطريق آخر.</b></p>"
    "<p style='background:#E3F8F0;padding:10px;border-radius:8px'>"
    "<b>الدرس العام:</b> كل خاصّية من بياناتك لا تُدخلها في عملية التوليد، "
    "هي خاصّية يفترض البوتستراب ضمنياً أنّها غير موجودة.</p>",
    "slate",
)

st.subheader("تعديل التحيّز في المثابرة")

card(
    "مشكلة Hurwicz والحل",
    "<p>مقدّر OLS لـ ρ في نموذج AR <b>متحيّز للأسفل</b> منهجياً في العيّنات "
    "المنتهية. وإذا بنيتَ عملية التوليد بـ <span dir='ltr'>ρ̂</span> المتحيّزة، "
    "فعيّناتك ستكون أقل مثابرة من الواقع — فيُخطئ البوتستراب.</p>"
    "<p><b>الحل الموصى به (O'Reilly &amp; Whelan):</b> استعمل "
    "<span dir='ltr'>ρ̂^u</span> <b>وسيطي-عديم التحيّز</b>:</p>"
    "<ul>"
    "<li><b>Andrews (1993b):</b> تقدير AR عديم التحيّز وسيطياً بالضبط</li>"
    "<li><b>Hansen (1999) grid bootstrap:</b> نسختهما العملية المفضّلة</li>"
    "</ul>"
    "<p style='color:#B4455C'><b>وما لا يعمل:</b> التصحيح الساذج "
    "<span dir='ltr'>2ρ̂ − ρ̄</span> — جرّبه MacKinnon ولم يُفد.</p>"
    "<p><b>وفي كل الأحوال: افرض الاستقرارية</b> "
    "<span dir='ltr'>|ρ̂| &lt; 0.99</span>، "
    "وإلا تولّدت عيّنات متفجّرة تُفسد التوزيع الصفري كلّه.</p>",
    "indigo",
)

# ============================================================== 5. متقدم
st.header("٥. تطويرات حديثة (للمتقدّمين)")

with st.expander("CUSUM-BWB — Lee & Baek (2020)"):
    st.markdown(
        "**الوايلد بوتستراب الكتلي** لاختبارات CUSUM:\n\n"
        "نقسم السلسلة المُوسَّطة إلى كتل بطول m، ونضرب **كل الكتلة** في وزن "
        "Rademacher واحد <span dir='ltr'>w_i</span>.\n\n"
        "**الخصائص (Remark 2.1):**\n"
        "- <span dir='ltr'>E(X*) = 0</span> دائماً → **لا كسر في المتوسّط** "
        "في العيّنة المولّدة ✓ (وهذا هو فرض الصفرية)\n"
        "- التغاير **داخل** الكتلة محفوظ → المثابرة محفوظة ✓\n"
        "- التغاير **عبر** الكتل = 0\n"
        "- **تغاير السلسلة المربّعة محفوظ لكل i,j** → "
        "تقلّب التباين محفوظ ✓\n\n"
        "**اختيار طول الكتلة:**\n"
        "- لاختبار المتوسّط (BWBA): "
        "<span dir='ltr'>m₁ = min([1.147(4Tρ̂²/(1−ρ̂²)²)^⅓], 100)</span> — تكيّفي\n"
        "- لاختبار التباين (BWBS): "
        "<span dir='ltr'>m₂ = min(√T, 100)</span>\n\n"
        "**تفصيل حاسم:** اختبار المتوسّط يُجرى على "
        "<span dir='ltr'>X_t</span> مباشرة، أمّا اختبار التباين فيُجرى على "
        "<span dir='ltr'>Y_t = (X_t − X̂_t)²</span> **بعد تعديل المتوسّط عند "
        "الكسر المقدَّر <span dir='ltr'>k̂_μ</span>** — "
        "وإلا حَجَب تغيّرُ المتوسّط تغيّرَ التباين.\n\n"
        "⚠️ عند <span dir='ltr'>m = 1</span> يصبح وايلد عادياً، "
        "وهذا يُحدث **تشوّهاً خطيراً في الحجم**. الكتلة ضرورية."
    )

with st.expander("CUSUM تحت التباين اللانهائي — Jin, Tian & Qin (2009)"):
    st.markdown(
        "لبيانات ذات **ذيول ثقيلة جداً** (توزيعات مستقرّة بدليل "
        "<span dir='ltr'>α ∈ (1,2)</span>، أي **بلا تباين منتهٍ**):\n\n"
        "- التوزيع الحدّي لإحصاء CUSUM-of-squares على البواقي هو **دالّة في "
        "عملية Lévy** تعتمد على دليل الذيل المجهول α.\n"
        "- **بوتستراب البواقي يتجاوز α كلّياً** — لا تحتاج تقديره إطلاقاً.\n"
        "- الإعدادات: حجم جزئي <span dir='ltr'>m ≈ 10–15٪ من T</span>، "
        "تشذيب <span dir='ltr'>δ = 0.02</span>، "
        "و**يُشدّدون على <span dir='ltr'>B ≥ T</span>**."
    )

with st.expander("CUSUM لنماذج ARMA–GARCH — Oh & Lee (2018)"):
    st.markdown(
        "لنموذج <span dir='ltr'>ARMA(p,q)–GARCH(r,s)</span>:\n\n"
        "- CUSUM على البواقي **يفوّت تغيّرات معالم ARMA**.\n"
        "- CUSUM على التقديرات **مفرط في الحجم بشدّة**.\n"
        "- **الحل: CUSUM على متّجه النقاط (score vector)**: "
        "<span dir='ltr'>max_k ‖·‖</span> مع "
        "<span dir='ltr'>Î_n⁻¹</span>، والتوزيع الحدّي "
        "<span dir='ltr'>sup‖W_m(s)‖²</span> حيث "
        "<span dir='ltr'>m = p+q+r+s+2</span>.\n"
        "- مقدّر <span dir='ltr'>Î_n</span> الخاص بهما يحتاج **العزم الرابع** "
        "فقط (بدل السادس للمقدّر الساذج).\n"
        "- بوتستراب البواقي والوايلد كلاهما متّسق ضعيفاً (Thms 1–2)؛ "
        "**الوايلد أفضل قليلاً وأسهل وأسرع**."
    )

with st.expander("الاستدلال المضبوط — Dufour & Kiviet (1996)"):
    st.markdown(
        "الطريق الوحيد **المضبوط تماماً** للنماذج الديناميكية في هذه الأدبيات. "
        "ثلاث تقنيات مُجمَّعة:\n\n"
        "1. **مجموعة ثقة مضبوطة لـ λ** من انحدار Kiviet–Phillips الموسّع.\n"
        "2. **اختبار اتحاد-تقاطع / حدود مُعمَّم** (Lemma 1): "
        "يجمع اختبارات شرطية معطى <span dir='ltr'>λ = λ₀</span> مع تلك "
        "المجموعة. القرار: نرفض إذا "
        "<span dir='ltr'>Q_L(y) ≥ c(α₁)</span>، "
        "نقبل إذا <span dir='ltr'>Q_U(y) < c(α'₂)</span>، "
        "و**غير حاسم فيما بينهما** — مع "
        "<span dir='ltr'>α₁ + α₂ = α</span>.\n"
        "3. **نسخ مُعشّاة (مونت كارلو)** حين يستعصي التوزيع الصفري الشرطي "
        "(Lemma 2) — **مضبوطة لأي N**.\n\n"
        "تغطّي اختبارات Chow والتنبؤي وCUSUM وCUSUM-of-squares."
    )

st.divider()
st.markdown(
    "**الصفحة التالية:** مختبر مونت كارلو — شغّل التجربة بنفسك وتحقّق من "
    "كل ما سبق."
)
