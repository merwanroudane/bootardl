"""
الرسوم المتحرّكة (Animations) — كلّها بأزرار تشغيل/إيقاف.
مبنيّة على إطارات Plotly مع شريط تمرير زمني.

منصة البوتستراب — د. مروان رودان
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from scipy import stats as sps

from .ui import PALETTE, SOFT, SEQ

GRID = "#E9EFF9"


# ----------------------------------------------------------------------------
# أزرار التشغيل وشريط التمرير
# ----------------------------------------------------------------------------
def _controls(frames, dur=380, label="الخطوة", trans=140):
    play = dict(
        type="buttons", direction="right",
        x=0.02, y=-0.16, xanchor="left", yanchor="top",
        showactive=False, pad=dict(t=4, r=6),
        bgcolor="#FFFFFF", bordercolor="#D4E2FB", borderwidth=1,
        font=dict(size=13, color="#1D4ED8"),
        buttons=[
            dict(label="▶  تشغيل", method="animate",
                 args=[None, dict(frame=dict(duration=dur, redraw=True),
                                  fromcurrent=True, mode="immediate",
                                  transition=dict(duration=trans))]),
            dict(label="⏸  إيقاف", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    mode="immediate",
                                    transition=dict(duration=0))]),
        ],
    )
    slider = dict(
        active=0, x=0.22, y=-0.16, len=0.76, xanchor="left", yanchor="top",
        pad=dict(t=6, b=6),
        currentvalue=dict(prefix=f"{label}: ", font=dict(size=13, color="#1D4ED8"),
                          visible=True, xanchor="right"),
        transition=dict(duration=trans),
        bgcolor="#E8F0FE", bordercolor="#D4E2FB", borderwidth=1,
        tickcolor="#B9CEF3", font=dict(size=11),
        steps=[dict(method="animate", label=f.name,
                    args=[[f.name], dict(mode="immediate",
                                         frame=dict(duration=dur, redraw=True),
                                         transition=dict(duration=trans))])
               for f in frames],
    )
    return [play], [slider]


def _style(fig, title="", h=440, xtitle="", ytitle=""):
    fig.update_layout(
        title=dict(text=title, x=0.98, xanchor="right",
                   font=dict(size=16, color="#13254A")),
        height=h, margin=dict(l=40, r=30, t=60, b=92),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FBFCFE",
        showlegend=True,
        legend=dict(orientation="h", y=1.08, x=0.0, xanchor="left",
                    bgcolor="rgba(255,255,255,0)"),
        xaxis=dict(title=xtitle, gridcolor=GRID, zerolinecolor=GRID),
        yaxis=dict(title=ytitle, gridcolor=GRID, zerolinecolor=GRID),
    )
    return fig


# ============================================================================
# 1) أنيميشن إعادة المعاينة: السحب مع الإرجاع
# ============================================================================
def anim_resampling(values: np.ndarray, seed: int = 3) -> go.Figure:
    """
    يُظهر كيف تُبنى عيّنة بوتستراب واحدة: نسحب مشاهدة، نُرجعها، ونكرّر.
    الصف العلوي = العيّنة الأصلية، الصف السفلي = العيّنة المسحوبة.
    """
    rng = np.random.default_rng(seed)
    n = len(values)
    picks = rng.integers(0, n, n)
    xs = np.arange(n)

    def counts_at(step):
        c = np.zeros(n)
        for j in range(step):
            c[picks[j]] += 1
        return c

    base_txt = [f"{v:.1f}" for v in values]

    frames = []
    for s in range(n + 1):
        c = counts_at(s)
        sizes = 26 + 10 * c
        colors = [SEQ[int(min(ci, 4))] if ci > 0 else "#CBD9EF" for ci in c]
        drawn = [values[picks[j]] for j in range(s)]
        frames.append(go.Frame(
            name=str(s),
            data=[
                go.Scatter(x=xs, y=np.ones(n) * 2, mode="markers+text",
                           marker=dict(size=sizes, color=colors,
                                       line=dict(width=2, color="#FFFFFF")),
                           text=base_txt, textposition="middle center",
                           textfont=dict(size=11, color="#13254A"),
                           name="العيّنة الأصلية (الصندوق)"),
                go.Scatter(x=np.arange(len(drawn)), y=np.ones(len(drawn)),
                           mode="markers+text",
                           marker=dict(size=30, color=PALETTE["teal"],
                                       line=dict(width=2, color="#FFFFFF")),
                           text=[f"{v:.1f}" for v in drawn],
                           textposition="middle center",
                           textfont=dict(size=11, color="#FFFFFF"),
                           name="عيّنة البوتستراب *"),
            ],
        ))

    fig = go.Figure(data=frames[0].data, frames=frames)
    b, s = _controls(frames, dur=600, label="عدد السحبات", trans=200)
    fig.update_layout(updatemenus=b, sliders=s)
    _style(fig, "السحب مع الإرجاع — Resampling with replacement", 420)
    fig.update_yaxes(range=[0.4, 2.6], showticklabels=False, showgrid=False,
                     zeroline=False)
    fig.update_xaxes(range=[-0.8, n - 0.2], showticklabels=False, showgrid=False,
                     zeroline=False)
    fig.add_annotation(x=n - 0.5, y=2.45, text="العيّنة الأصلية",
                       showarrow=False, font=dict(size=13, color="#1D4ED8"))
    fig.add_annotation(x=n - 0.5, y=0.65, text="عيّنة بوتستراب جديدة",
                       showarrow=False, font=dict(size=13, color="#0F766E"))
    return fig


# ============================================================================
# 2) أنيميشن بناء توزيع البوتستراب
# ============================================================================
def anim_build_distribution(boot: np.ndarray, stat: float | None = None,
                            steps: int = 24, title: str = "",
                            xtitle: str = "قيمة الإحصاء في عيّنات البوتستراب",
                            color: str = "blue") -> go.Figure:
    """المدرّج التكراري لتوزيع البوتستراب وهو يُبنى تكراراً بعد تكرار."""
    B = len(boot)
    cuts = np.unique(np.linspace(max(B // steps, 5), B, steps).astype(int))
    lo, hi = float(np.min(boot)), float(np.max(boot))
    if stat is not None:
        lo, hi = min(lo, stat), max(hi, stat)
    pad = 0.06 * (hi - lo + 1e-9)
    edges = np.linspace(lo - pad, hi + pad, 34)
    cmax = max(np.histogram(boot, bins=edges)[0].max(), 1)

    frames = []
    for c in cuts:
        h, _ = np.histogram(boot[:c], bins=edges)
        h = h / max(c, 1) * B          # تطبيع ليبقى المقياس ثابتاً
        frames.append(go.Frame(
            name=str(c),
            data=[go.Bar(x=(edges[:-1] + edges[1:]) / 2, y=h,
                         width=(edges[1] - edges[0]) * 0.92,
                         marker=dict(color=PALETTE[color], opacity=0.82,
                                     line=dict(width=0)),
                         name=f"توزيع البوتستراب (B = {c})")],
        ))

    fig = go.Figure(data=frames[0].data, frames=frames)
    if stat is not None:
        fig.add_vline(x=stat, line=dict(color=PALETTE["rose"], width=3),
                      annotation_text="الإحصاء المحسوب من بياناتك",
                      annotation_position="top left",
                      annotation_font=dict(size=12, color=PALETTE["rose"]))
    b, s = _controls(frames, dur=260, label="عدد التكرارات B", trans=120)
    fig.update_layout(updatemenus=b, sliders=s, bargap=0.04)
    _style(fig, title or "بناء التوزيع الصفري بالبوتستراب", 450, xtitle, "التكرار")
    fig.update_yaxes(range=[0, cmax * 1.25])
    return fig


# ============================================================================
# 3) أنيميشن: التوزيع التقاربي مقابل التوزيع الحقيقي عند تكبير n
# ============================================================================
def anim_asymptotic_gap(ns: list[int], samples: dict[int, np.ndarray],
                        df: int = 2) -> go.Figure:
    """
    يقارن كثافة الإحصاء الفعلية عند كل n بالتوزيع التقاربي χ².
    الفجوة بين المنحنيين هي سبب وجود البوتستراب.
    """
    allv = np.concatenate([samples[n] for n in ns])
    hi = float(np.quantile(allv, 0.995))
    grid = np.linspace(0.01, hi, 220)
    chi = sps.chi2.pdf(grid, df)

    frames = []
    for n in ns:
        v = samples[n]
        kde = sps.gaussian_kde(v)
        frames.append(go.Frame(
            name=str(n),
            data=[
                go.Scatter(x=grid, y=kde(grid), mode="lines",
                           line=dict(color=PALETTE["rose"], width=3.2),
                           fill="tozeroy", fillcolor="rgba(244,63,94,0.12)",
                           name=f"التوزيع الحقيقي عند n = {n}"),
                go.Scatter(x=grid, y=chi, mode="lines",
                           line=dict(color=PALETTE["blue"], width=3.2,
                                     dash="dash"),
                           name=f"التوزيع التقاربي χ²({df}) — ما يفترضه الاختبار"),
            ],
        ))

    fig = go.Figure(data=frames[0].data, frames=frames)
    cv = sps.chi2.ppf(0.95, df)
    fig.add_vline(x=cv, line=dict(color=PALETTE["slate"], width=2, dash="dot"),
                  annotation_text="القيمة الحرجة 5%", annotation_position="top")
    b, s = _controls(frames, dur=750, label="حجم العيّنة n", trans=300)
    fig.update_layout(updatemenus=b, sliders=s)
    _style(fig, "الفجوة بين الواقع والنظرية التقاربية", 450,
           "قيمة الإحصاء", "الكثافة")
    return fig


# ============================================================================
# 4) أنيميشن الوايلد بوتستراب: قلب الإشارات
# ============================================================================
def anim_wild(u: np.ndarray, weight: str = "rademacher", draws: int = 10,
              seed: int = 11) -> go.Figure:
    """كل إطار = سحبة أوزان جديدة ε* تضرب البواقي الأصلية."""
    from .engine import wild_weights
    rng = np.random.default_rng(seed)
    t = np.arange(len(u))
    ymax = np.abs(u).max() * 2.1

    frames = []
    for d in range(draws + 1):
        if d == 0:
            us, lab = u.copy(), "البواقي الأصلية û"
            cols = [PALETTE["slate"]] * len(u)
        else:
            w = wild_weights(len(u), weight, rng)
            us = u * w
            lab = f"البواقي بعد الضرب في ε* — السحبة {d}"
            cols = [PALETTE["teal"] if wi > 0 else PALETTE["rose"] for wi in w]
        frames.append(go.Frame(
            name=str(d),
            data=[go.Bar(x=t, y=us, marker=dict(color=cols), name=lab)],
        ))

    fig = go.Figure(data=frames[0].data, frames=frames)
    b, s = _controls(frames, dur=720, label="السحبة", trans=250)
    fig.update_layout(updatemenus=b, sliders=s, bargap=0.25)
    _style(fig, "الوايلد بوتستراب: حجم كل باقٍ محفوظ، وإشارته تُقلب",
           420, "الزمن t", "û*ₜ = û ₜ × ε*ₜ")
    fig.update_yaxes(range=[-ymax, ymax])
    return fig


# ============================================================================
# 5) أنيميشن: مقارنة مخططات إعادة المعاينة على سلسلة زمنية
# ============================================================================
def anim_schemes(u: np.ndarray, block: int = 5, draws: int = 8,
                 seed: int = 5) -> go.Figure:
    """iid مقابل الكتل مقابل الوايلد — لماذا تهدم الأولى بنية الترابط."""
    from .engine import wild_weights
    rng = np.random.default_rng(seed)
    n = len(u)
    t = np.arange(n)
    nb = int(np.ceil(n / block))

    frames = []
    for d in range(draws):
        iid = rng.choice(u, n, replace=True)
        st = rng.integers(0, max(n - block, 1), nb)
        blk = np.concatenate([u[s:s + block] for s in st])[:n]
        if len(blk) < n:
            blk = np.resize(blk, n)
        wld = u * wild_weights(n, "rademacher", rng)
        frames.append(go.Frame(
            name=str(d + 1),
            data=[
                go.Scatter(x=t, y=iid, mode="lines", name="iid — السحب الحر",
                           line=dict(color=PALETTE["rose"], width=2)),
                go.Scatter(x=t, y=blk, mode="lines", name=f"الكتل Block (L={block})",
                           line=dict(color=PALETTE["amber"], width=2)),
                go.Scatter(x=t, y=wld, mode="lines", name="الوايلد Wild",
                           line=dict(color=PALETTE["teal"], width=2)),
                go.Scatter(x=t, y=u, mode="lines", name="البواقي الأصلية",
                           line=dict(color=PALETTE["slate"], width=2.6,
                                     dash="dot")),
            ],
        ))

    fig = go.Figure(data=frames[0].data, frames=frames)
    b, s = _controls(frames, dur=800, label="السحبة", trans=260)
    fig.update_layout(updatemenus=b, sliders=s)
    _style(fig, "ماذا تفعل كل طريقة إعادة معاينة بسلسلة مترابطة؟",
           460, "الزمن t", "القيمة")
    return fig


# ============================================================================
# 6) أنيميشن supF عبر تواريخ الكسر المحتملة
# ============================================================================
def anim_supf(dates: np.ndarray, Fs: np.ndarray, crit_boot: float,
              crit_asy: float | None = None) -> go.Figure:
    """الإحصاء F يُحسب عند كل تاريخ كسر محتمل، ثم نأخذ أعلى قيمة."""
    frames = []
    for i in range(1, len(dates) + 1, max(1, len(dates) // 30)):
        frames.append(go.Frame(
            name=str(dates[i - 1]),
            data=[
                go.Scatter(x=dates[:i], y=Fs[:i], mode="lines",
                           line=dict(color=PALETTE["blue"], width=3),
                           fill="tozeroy", fillcolor="rgba(59,130,246,0.12)",
                           name="إحصاء Chow F عند كل تاريخ"),
                go.Scatter(x=[dates[:i][np.argmax(Fs[:i])]],
                           y=[Fs[:i].max()], mode="markers",
                           marker=dict(size=15, color=PALETTE["rose"],
                                       line=dict(width=2, color="#fff")),
                           name="أعلى قيمة حتى الآن = supF"),
            ],
        ))

    fig = go.Figure(data=frames[0].data, frames=frames)
    fig.add_hline(y=crit_boot, line=dict(color=PALETTE["teal"], width=2.5),
                  annotation_text="القيمة الحرجة من البوتستراب 5%",
                  annotation_position="top left")
    if crit_asy:
        fig.add_hline(y=crit_asy, line=dict(color=PALETTE["amber"], width=2,
                                            dash="dash"),
                      annotation_text="القيمة الحرجة التقاربية",
                      annotation_position="bottom left")
    b, s = _controls(frames, dur=120, label="تاريخ الكسر المحتمل", trans=60)
    fig.update_layout(updatemenus=b, sliders=s)
    _style(fig, "supF: نجرّب كل تاريخ كسر ممكن ونأخذ الأقصى", 440,
           "موضع الكسر المفترض", "إحصاء F")
    return fig


# ============================================================================
# 7) أنيميشن مسار CUSUM مع حِزَم البوتستراب
# ============================================================================
def anim_cusum(path: np.ndarray, bands: tuple[np.ndarray, np.ndarray],
               asy: tuple[np.ndarray, np.ndarray] | None = None) -> go.Figure:
    t = np.arange(1, len(path) + 1)
    lo, hi = bands
    frames = []
    step = max(1, len(path) // 35)
    for i in range(2, len(path) + 1, step):
        frames.append(go.Frame(
            name=str(i),
            data=[go.Scatter(x=t[:i], y=path[:i], mode="lines",
                             line=dict(color=PALETTE["violet"], width=3),
                             name="مسار CUSUM")],
        ))
    frames.append(go.Frame(name=str(len(path)),
                           data=[go.Scatter(x=t, y=path, mode="lines",
                                            line=dict(color=PALETTE["violet"],
                                                      width=3),
                                            name="مسار CUSUM")]))

    fig = go.Figure(data=frames[0].data, frames=frames)
    fig.add_trace(go.Scatter(x=t, y=hi, mode="lines", name="حزمة البوتستراب 5%",
                             line=dict(color=PALETTE["teal"], width=2)))
    fig.add_trace(go.Scatter(x=t, y=lo, mode="lines", showlegend=False,
                             line=dict(color=PALETTE["teal"], width=2),
                             fill="tonexty", fillcolor="rgba(20,184,166,0.08)"))
    if asy is not None:
        fig.add_trace(go.Scatter(x=t, y=asy[1], mode="lines",
                                 name="الحزمة التقاربية (Brown–Durbin–Evans)",
                                 line=dict(color=PALETTE["amber"], width=2,
                                           dash="dash")))
        fig.add_trace(go.Scatter(x=t, y=asy[0], mode="lines", showlegend=False,
                                 line=dict(color=PALETTE["amber"], width=2,
                                           dash="dash")))
    # تثبيت الحِزَم في كل الإطارات
    extra = list(fig.data[1:])
    for f in fig.frames:
        f.data = tuple(list(f.data) + extra)
        f.traces = list(range(len(f.data)))

    b, s = _controls(frames, dur=110, label="المشاهدة", trans=50)
    fig.update_layout(updatemenus=b, sliders=s)
    _style(fig, "CUSUM: هل تخرج المعالم عن مسارها عبر الزمن؟", 450,
           "الزمن", "CUSUM")
    return fig


# ============================================================================
# 8) أنيميشن استقرار قيمة p مع تزايد B
# ============================================================================
def anim_pvalue_stability(stat: float, boot: np.ndarray,
                          grid: list[int] | None = None) -> go.Figure:
    """كيف تهدأ قيمة p كلما زاد عدد تكرارات البوتستراب."""
    rng = np.random.default_rng(99)
    grid = grid or [19, 39, 99, 199, 399, 799, 1499, 2999]
    reps = 40
    frames = []
    for g in grid:
        ps = [float((rng.choice(boot, g, replace=True) > stat).mean())
              for _ in range(reps)]
        frames.append(go.Frame(
            name=str(g),
            data=[go.Scatter(x=np.arange(1, reps + 1), y=ps, mode="markers",
                             marker=dict(size=11, color=PALETTE["indigo"],
                                         opacity=0.78,
                                         line=dict(width=1, color="#fff")),
                             name=f"قيمة p في {reps} تجربة مستقلة — B = {g}")],
        ))

    fig = go.Figure(data=frames[0].data, frames=frames)
    fig.add_hline(y=0.05, line=dict(color=PALETTE["rose"], width=2, dash="dash"),
                  annotation_text="مستوى 5%", annotation_position="top left")
    b, s = _controls(frames, dur=900, label="عدد التكرارات B", trans=320)
    fig.update_layout(updatemenus=b, sliders=s)
    _style(fig, "لماذا لا يكفي B صغير؟ تبعثر قيمة p", 430,
           "رقم التجربة", "قيمة p")
    fig.update_yaxes(range=[0, max(0.35, 0.05)])
    return fig


# ============================================================================
# 9) أنيميشن: مشكلة العيّنات الكبيرة — المعنوية الإحصائية ليست أهمية اقتصادية
# ============================================================================
def anim_large_n(effect: float = 0.02, ns: list[int] | None = None,
                 seed: int = 21) -> go.Figure:
    """أثر صغير جداً يصبح «معنوياً جداً» لمجرّد تكبير العيّنة."""
    rng = np.random.default_rng(seed)
    ns = ns or [30, 60, 120, 250, 500, 1000, 2500, 5000, 10000, 25000]
    tv, pv = [], []
    for n in ns:
        x = rng.normal(0, 1, n)
        y = effect * x + rng.normal(0, 1, n)
        b = float(np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1))
        se = np.sqrt(np.var(y - b * x, ddof=1) / (n * np.var(x, ddof=1)))
        tv.append(b / se)
        pv.append(2 * sps.norm.sf(abs(b / se)))

    frames = []
    for i in range(1, len(ns) + 1):
        frames.append(go.Frame(
            name=str(ns[i - 1]),
            data=[
                go.Scatter(x=ns[:i], y=np.abs(tv[:i]), mode="lines+markers",
                           line=dict(color=PALETTE["orange"], width=3),
                           marker=dict(size=10), name="|إحصاء t|"),
                go.Scatter(x=ns[:i], y=[effect] * i, mode="lines",
                           line=dict(color=PALETTE["slate"], width=2.5,
                                     dash="dot"),
                           name=f"حجم الأثر الحقيقي = {effect} (ثابت!)"),
            ],
        ))

    fig = go.Figure(data=frames[0].data, frames=frames)
    fig.add_hline(y=1.96, line=dict(color=PALETTE["rose"], width=2, dash="dash"),
                  annotation_text="عتبة المعنوية 1.96",
                  annotation_position="top left")
    b, s = _controls(frames, dur=620, label="حجم العيّنة n", trans=260)
    fig.update_layout(updatemenus=b, sliders=s)
    _style(fig, "مشكلة العيّنات الكبيرة: الأثر لم يتغيّر، والمعنوية انفجرت",
           430, "حجم العيّنة n (مقياس لوغاريتمي)", "القيمة")
    fig.update_xaxes(type="log")
    return fig


# ============================================================================
# 10) أنيميشن الحجم الحقيقي مقابل الاسمي
# ============================================================================
def anim_size_bars(labels: list[str], asy: list[float], boot: list[float],
                   alpha: float = 0.05) -> go.Figure:
    """أعمدة متحرّكة تقارن نسبة الرفض الفعلية بين النسخة التقاربية والبوتستراب."""
    frames = []
    k = 14
    for s in range(1, k + 1):
        f = s / k
        frames.append(go.Frame(
            name=f"{int(f*100)}%",
            data=[
                go.Bar(x=labels, y=[a * f for a in asy],
                       marker_color=PALETTE["rose"], name="النسخة التقاربية",
                       text=[f"{a:.1%}" if s == k else "" for a in asy],
                       textposition="outside"),
                go.Bar(x=labels, y=[b * f for b in boot],
                       marker_color=PALETTE["teal"], name="نسخة البوتستراب",
                       text=[f"{b:.1%}" if s == k else "" for b in boot],
                       textposition="outside"),
            ],
        ))

    fig = go.Figure(data=frames[0].data, frames=frames)
    fig.add_hline(y=alpha, line=dict(color=PALETTE["blue"], width=2.5,
                                     dash="dash"),
                  annotation_text=f"المستوى الاسمي الصحيح = {alpha:.0%}",
                  annotation_position="top left")
    b, s = _controls(frames, dur=90, label="العرض", trans=60)
    fig.update_layout(updatemenus=b, sliders=s, barmode="group")
    _style(fig, "نسبة الرفض الفعلية تحت فرضية صفرية صحيحة", 450, "",
           "نسبة الرفض")
    fig.update_yaxes(tickformat=".0%",
                     range=[0, max(max(asy), max(boot)) * 1.3])
    return fig


# ============================================================================
# 11) مخطّط ثابت: عالم الواقع مقابل عالم البوتستراب
# ============================================================================
def diagram_two_worlds() -> go.Figure:
    """دياجرام يوضّح التناظر بين العالم الحقيقي وعالم البوتستراب."""
    fig = go.Figure()
    boxes = [
        (1.0, 3.0, "المجتمع الحقيقي\nF  (مجهول)", PALETTE["blue"], SOFT["blue"]),
        (3.2, 3.0, "عيّنتك\ny₁…yₙ", PALETTE["blue"], SOFT["blue"]),
        (5.4, 3.0, "الإحصاء\nτ̂", PALETTE["blue"], SOFT["blue"]),
        (1.0, 1.0, "المجتمع البديل\nF̂  (عيّنتك نفسها)", PALETTE["teal"], SOFT["teal"]),
        (3.2, 1.0, "عيّنة بوتستراب\ny*₁…y*ₙ", PALETTE["teal"], SOFT["teal"]),
        (5.4, 1.0, "الإحصاء\nτ*", PALETTE["teal"], SOFT["teal"]),
    ]
    for x, y, txt, c, bg in boxes:
        fig.add_shape(type="rect", x0=x - 0.78, x1=x + 0.78, y0=y - 0.42,
                      y1=y + 0.42, line=dict(color=c, width=2.5),
                      fillcolor=bg, layer="below")
        fig.add_annotation(x=x, y=y, text=txt.replace("\n", "<br>"),
                           showarrow=False,
                           font=dict(size=13, color="#13254A"))
    arrows = [(1.80, 3.0, 2.40, 3.0), (3.99, 3.0, 4.60, 3.0),
              (1.80, 1.0, 2.40, 1.0), (3.99, 1.0, 4.60, 1.0)]
    for x0, y0, x1, y1 in arrows:
        fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y",
                           axref="x", ayref="y", showarrow=True,
                           arrowhead=3, arrowsize=1.3, arrowwidth=2.2,
                           arrowcolor="#8DA7D4")
    fig.add_annotation(x=1.0, y=2.1, ax=1.0, ay=2.58, xref="x", yref="y",
                       axref="x", ayref="y", showarrow=True, arrowhead=3,
                       arrowsize=1.3, arrowwidth=2.4,
                       arrowcolor=PALETTE["amber"])
    fig.add_annotation(x=1.95, y=2.05,
                       text="مبدأ الإحلال: نضع F̂ مكان F<br>"
                            "<i>Plug-in principle</i>",
                       showarrow=False,
                       font=dict(size=12, color=PALETTE["amber"]))
    fig.add_annotation(x=6.6, y=3.0, text="مرّة واحدة",
                       showarrow=False, font=dict(size=12, color=PALETTE["blue"]))
    fig.add_annotation(x=6.6, y=1.0, text="B مرّة",
                       showarrow=False, font=dict(size=12, color=PALETTE["teal"]))
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10),
                      paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                      showlegend=False,
                      xaxis=dict(visible=False, range=[0, 7.4]),
                      yaxis=dict(visible=False, range=[0.2, 3.8]))
    return fig
