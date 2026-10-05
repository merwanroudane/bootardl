"""المختبر التفاعلي: ارفع بياناتك وشغّل البطارية الكاملة."""

import io

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy import stats as sps

from core.ui import hero, card, note, plotly, table, PALETTE
from core.anim import anim_build_distribution, anim_cusum
from core.engine import (simulate_dgp, design_from, ols, run_boot_test,
                         recursive_residuals, cusum_path, bootstrap_sample,
                         TESTS, lagmat)

hero(
    "المختبر التفاعلي",
    "ضع بياناتك هنا — أو ولّد بيانات اصطناعية — وشغّل بطارية الاختبارات "
    "البعدية كاملةً بنسختيها التقاربية والبوتستراب، في جدول واحد قابل للتحميل.",
    "التطبيق العملي",
    "#FDEAF4", "#E8F0FE",
)

# ============================================================== البيانات
st.header("١. البيانات")

src = st.segmented_control(
    "مصدر البيانات",
    ["بيانات اصطناعية", "ارفع ملف CSV"],
    default="بيانات اصطناعية",
    key="lab_src",
)

df = None

if src == "بيانات اصطناعية":
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        n_g = st.slider("عدد المشاهدات", 30, 400, 100, key="lab_n")
        rho_g = st.slider("المثابرة ρ", 0.0, 0.95, 0.6, 0.05, key="lab_rho")
    with c2:
        het_g = st.slider("عدم تجانس التباين", 0.0, 0.8, 0.0, 0.1, key="lab_het")
        brk_g = st.slider("كسر هيكلي", 0.0, 3.0, 0.0, 0.2, key="lab_brk")
    with c3:
        err_g = st.selectbox(
            "توزيع الأخطاء", ["normal", "t5", "chi2", "mixture"],
            format_func=lambda s: {"normal": "طبيعي", "t5": "t(5) ذيول ثقيلة",
                                   "chi2": "χ²(2) ملتوٍ",
                                   "mixture": "مزيج (قيم متطرّفة)"}[s],
            key="lab_err")
    with c4:
        seed_g = st.number_input("البذرة", 1, 99999, 2026, key="lab_seed")

    d = simulate_dgp(int(n_g), float(rho_g), 1.0, float(het_g), err_g,
                     float(brk_g), np.random.default_rng(int(seed_g)))
    df = pd.DataFrame({"t": np.arange(1, len(d["y"]) + 1),
                       "y": d["y"], "x": d["x"]})
    st.caption(
        "النموذج الحقيقي: "
        "`y[t] = 0.2 + rho*y[t-1] + x[t] + u[t]` — "
        "فأي مشكلة يكشفها الاختبار أدناه تكون مشكلة حقيقية وضعتها أنت."
    )
else:
    up = st.file_uploader("ارفع ملف CSV (الصف الأول أسماء الأعمدة)",
                          type=["csv"], key="lab_up")
    if up is not None:
        try:
            df = pd.read_csv(up)
        except Exception as e:
            st.error(f"تعذّرت قراءة الملف: {e}")
    else:
        st.info(
            "ارفع ملفاً، أو عُد إلى «بيانات اصطناعية» للتجربة فوراً. "
            "الملف يجب أن يحتوي عموداً للمتغيّر التابع وعموداً أو أكثر "
            "للمتغيّرات المستقلّة، بقيم رقمية وبلا قيم مفقودة."
        )

if df is None:
    st.stop()

with st.expander("👁️ معاينة البيانات", expanded=False):
    st.dataframe(df.head(20), width="stretch")
    st.caption(f"عدد المشاهدات: {len(df)} · عدد الأعمدة: {df.shape[1]}")

# ============================================================== النموذج
st.header("٢. النموذج")

num_cols = [c for c in df.columns
            if pd.api.types.is_numeric_dtype(df[c])]
if len(num_cols) < 2:
    st.error("يلزم عمودان رقميان على الأقل.")
    st.stop()

c1, c2, c3 = st.columns(3)
with c1:
    ycol = st.selectbox("المتغيّر التابع y", num_cols,
                        index=num_cols.index("y") if "y" in num_cols else 0,
                        key="lab_y")
with c2:
    xcols = st.multiselect(
        "المتغيّرات المستقلّة X",
        [c for c in num_cols if c != ycol],
        default=[c for c in num_cols if c not in (ycol, "t")][:2],
        key="lab_x",
    )
with c3:
    ylags = st.slider("عدد إبطاءات المتغيّر التابع", 0, 4, 1, key="lab_lags")

if not xcols:
    st.warning("اختر متغيّراً مستقلاً واحداً على الأقل.")
    st.stop()

# بناء مصفوفة التصميم
dat = df[[ycol] + xcols].dropna().reset_index(drop=True)
yv = dat[ycol].to_numpy(dtype=float)
Xv = dat[xcols].to_numpy(dtype=float)

if ylags > 0:
    Lg = lagmat(yv, int(ylags))
    yy = yv[int(ylags):]
    XX = np.column_stack([np.ones(len(yy)),
                          Lg[int(ylags):],
                          Xv[int(ylags):]])
    names = ["_cons"] + [f"L{j}.{ycol}" for j in range(1, int(ylags) + 1)] + xcols
    dyn_col = 1
else:
    yy = yv
    XX = np.column_stack([np.ones(len(yy)), Xv])
    names = ["_cons"] + xcols
    dyn_col = None

fit = ols(yy, XX)
se = np.sqrt(np.diag(fit["XtXi"]) * fit["s2"])
tv = fit["b"] / np.maximum(se, 1e-12)
pv = 2 * sps.t.sf(np.abs(tv), max(fit["n"] - fit["k"], 1))

r2 = 1 - fit["rss"] / float(((yy - yy.mean()) ** 2).sum())

m1, m2, m3, m4 = st.columns(4)
m1.metric("المشاهدات n", fit["n"])
m2.metric("المعالم k", fit["k"])
m3.metric("R²", f"{r2:.4f}")
m4.metric("الجذر التربيعي لمتوسّط مربّع الخطأ", f"{np.sqrt(fit['s2']):.4f}")

st.subheader("نتائج التقدير بالمربّعات الصغرى")
res_df = pd.DataFrame({
    "variable": names,
    "coef": np.round(fit["b"], 5),
    "std_err": np.round(se, 5),
    "t": np.round(tv, 3),
    "p_value": np.round(pv, 4),
})
st.dataframe(res_df, width="stretch", hide_index=True)

if dyn_col is not None:
    rho_est = float(fit["b"][1])
    if abs(rho_est) >= 0.99:
        st.error(
            f"⚠️ معامل المتغيّر التابع المُبطّأ = {rho_est:.4f}، "
            f"وهو قريب جداً من الواحد. عمليات التوليد التكرارية ستُنتج عيّنات "
            f"شبه متفجّرة. الأدبيات توصي بفرض |ρ̂| < 0.99 — "
            f"فسّر النتائج بحذر."
        )
    elif abs(rho_est) > 0.9:
        st.warning(
            f"معامل المتغيّر التابع المُبطّأ = {rho_est:.4f} — مثابرة عالية. "
            f"هذا هو بالضبط النطاق الذي تنهار فيه الاختبارات التقاربية، "
            f"فالبوتستراب هنا ليس ترفاً."
        )

# ============================================================== الإعدادات
st.header("٣. إعدادات البوتستراب")

c1, c2, c3, c4 = st.columns(4)
with c1:
    dgp_l = st.selectbox(
        "عملية التوليد",
        ["wild", "residual", "normal", "sieve", "block", "stationary",
         "blockwild", "fixed"],
        key="lab_dgp",
    )
with c2:
    wt_l = st.selectbox("توزيع الأوزان", ["rademacher", "mammen", "normal"],
                        key="lab_wt")
with c3:
    ft_l = st.selectbox("تحويل البواقي", ["hc3", "hc2", "hc1", "hc0"],
                        key="lab_ft")
with c4:
    B_l = st.select_slider("عدد التكرارات B", [99, 199, 399, 999, 1999], 399,
                           key="lab_B")

c5, c6, c7 = st.columns(3)
with c5:
    q_l = st.slider("رتبة الارتباط الذاتي Q", 1, 8, 2, key="lab_q")
with c6:
    seed_l = st.number_input("البذرة العشوائية", 1, 99999, 2026, key="lab_sd")
with c7:
    cont_l = st.toggle("قيمة p المتّصلة (Racine–MacKinnon)", key="lab_cont")

note(
    f"<b>تذكير بجدول المطابقة:</b> لاختبارات <b>تجانس التباين</b> "
    f"(Koenker، BP، White، ARCH) استعمل "
    f"<code style='direction:ltr'>residual</code> أو "
    f"<code style='direction:ltr'>normal</code> — لا الوايلد. "
    f"ولاختبارات <b>الاعتدالية</b> استعمل "
    f"<code style='direction:ltr'>normal</code>. "
    f"وللباقي الوايلد ممتاز. "
    f"اخترتَ حالياً: <code style='direction:ltr'>{dgp_l}</code>.",
    "amber", "🧭",
)

ALL = ["bg", "bg_hr", "mlm_hr", "dw", "bp", "koenker", "white", "arch",
       "szroeter", "jb", "ad", "reset", "supf", "avef"]

chosen = st.multiselect(
    "الاختبارات المطلوبة",
    ALL, default=ALL,
    format_func=lambda s: f"{TESTS[s][0]} ({TESTS[s][1]})",
    key="lab_tests",
)

if st.button("🚀  شغّل بطارية الاختبارات", type="primary", key="lab_run"):
    rows, store = [], {}
    pb = st.progress(0.0)
    for i, t in enumerate(chosen):
        pb.progress(i / max(len(chosen), 1), f"{TESTS[t][0]} …")
        try:
            o = run_boot_test(t, yy, XX, int(B_l), dgp_l, wt_l, ft_l,
                              int(q_l), 0.15, dyn_col, int(seed_l),
                              bool(cont_l))
            store[t] = o
            rows.append({
                "family": TESTS[t][1],
                "test": TESTS[t][0],
                "statistic": round(o["stat"], 4),
                "p_asymptotic": (round(o["p_asy"], 4)
                                 if np.isfinite(o["p_asy"]) else None),
                "p_bootstrap": round(o["p_boot"], 4),
                "crit95_bootstrap": round(o["crit95"], 4),
            })
        except Exception as e:
            rows.append({"family": TESTS[t][1], "test": TESTS[t][0],
                         "statistic": None, "p_asymptotic": None,
                         "p_bootstrap": None, "crit95_bootstrap": None})
    pb.empty()
    st.session_state["lab_rows"] = rows
    st.session_state["lab_store"] = store
    st.session_state["lab_meta"] = dict(dgp=dgp_l, wt=wt_l, ft=ft_l, B=B_l,
                                        q=q_l, seed=seed_l, n=fit["n"],
                                        k=fit["k"])

# ============================================================== النتائج
if "lab_rows" in st.session_state:
    st.header("٤. النتائج")
    out = pd.DataFrame(st.session_state["lab_rows"])

    def _mark(v):
        if v is None or (isinstance(v, float) and not np.isfinite(v)):
            return ""
        if v < 0.01:
            return "***"
        if v < 0.05:
            return "**"
        if v < 0.10:
            return "*"
        return ""

    out["sig"] = out["p_bootstrap"].map(_mark)
    st.dataframe(
        out, width="stretch", hide_index=True,
        column_config={
            "family": st.column_config.TextColumn("العائلة"),
            "test": st.column_config.TextColumn("الاختبار"),
            "statistic": st.column_config.NumberColumn("الإحصاء", format="%.4f"),
            "p_asymptotic": st.column_config.NumberColumn(
                "p تقاربية", format="%.4f"),
            "p_bootstrap": st.column_config.NumberColumn(
                "p بوتستراب", format="%.4f"),
            "crit95_bootstrap": st.column_config.NumberColumn(
                "حرجة 5٪ بوتستراب", format="%.4f"),
            "sig": st.column_config.TextColumn("المعنوية"),
        },
    )
    st.caption("*** p<0.01 · ** p<0.05 · * p<0.10 — على قيم p البوتستراب.")

    # الخلاصة التفسيرية
    st.subheader("القراءة")
    msgs = []
    for _, r in out.iterrows():
        if r["p_bootstrap"] is None:
            continue
        if r["p_bootstrap"] < 0.05:
            msgs.append(
                f"- **{r['test']}** يرفض الفرضية الصفرية "
                f"(p = {r['p_bootstrap']:.3f}) → توجد مشكلة من نوع "
                f"**{r['family']}**."
            )
    if msgs:
        st.error("**مشاكل مكتشفة عند 5٪:**\n\n" + "\n".join(msgs))
    else:
        st.success(
            "لم يرفض أي اختبار عند 5٪ باستعمال قيم p البوتستراب — "
            "النموذج يجتاز البطارية."
        )

    # الاختلافات
    diff = out.dropna(subset=["p_asymptotic", "p_bootstrap"]).copy()
    if len(diff):
        diff["gap"] = (diff["p_asymptotic"] - diff["p_bootstrap"]).abs()
        flip = diff[((diff["p_asymptotic"] < 0.05) &
                     (diff["p_bootstrap"] >= 0.05)) |
                    ((diff["p_asymptotic"] >= 0.05) &
                     (diff["p_bootstrap"] < 0.05))]
        if len(flip):
            st.warning(
                "**⚠️ اختبارات انقلب فيها القرار بين النسختين** — "
                "وهذا بالضبط ما تحذّر منه الأدبيات:\n\n" +
                "\n".join(
                    f"- **{r['test']}**: تقاربية p = {r['p_asymptotic']:.3f}، "
                    f"بوتستراب p = {r['p_bootstrap']:.3f}"
                    for _, r in flip.iterrows()
                )
            )

        fg = go.Figure()
        fg.add_trace(go.Bar(x=diff["test"], y=diff["p_asymptotic"],
                            name="p تقاربية", marker_color=PALETTE["rose"]))
        fg.add_trace(go.Bar(x=diff["test"], y=diff["p_bootstrap"],
                            name="p بوتستراب", marker_color=PALETTE["teal"]))
        fg.add_hline(y=0.05, line=dict(color=PALETTE["blue"], width=2,
                                       dash="dash"),
                     annotation_text="5٪")
        fg.update_layout(height=400, barmode="group",
                         margin=dict(l=40, r=30, t=55, b=90),
                         title=dict(text="قيم p: تقاربية مقابل بوتستراب",
                                    x=0.98, xanchor="right"),
                         legend=dict(orientation="h", y=1.12, x=0),
                         xaxis=dict(tickangle=-35, gridcolor="#E9EFF9"),
                         yaxis=dict(title="قيمة p", gridcolor="#E9EFF9",
                                    range=[0, 1]))
        plotly(fg, key="lab_pbars")

    # التوزيع لاختبار مختار
    st.subheader("توزيع البوتستراب لاختبار مختار")
    store = st.session_state["lab_store"]
    pick = st.selectbox("الاختبار", list(store.keys()),
                        format_func=lambda s: TESTS[s][0], key="lab_pick")
    o = store[pick]
    plotly(
        anim_build_distribution(o["boot"], o["stat"], steps=20,
                                title=f"التوزيع الصفري — {TESTS[pick][0]}",
                                color="violet"),
        key="lab_dist",
    )

    # التحميل
    meta = st.session_state["lab_meta"]
    buf = io.StringIO()
    buf.write("# bootdiag-style diagnostic results\n")
    buf.write(f"# n={meta['n']}, k={meta['k']}, B={meta['B']}, "
              f"dgp={meta['dgp']}, weight={meta['wt']}, "
              f"ftrans={meta['ft']}, lags={meta['q']}, seed={meta['seed']}\n")
    out.to_csv(buf, index=False)
    st.download_button("⬇️  حمّل النتائج (CSV)", buf.getvalue(),
                       "bootstrap_diagnostics.csv", "text/csv",
                       key="lab_dl")

    st.code(
        f"Diagnostic p-values are bootstrap p-values "
        f"(DGP = {meta['dgp']}, {meta['wt']} weights, "
        f"{meta['ft'].upper()}-transformed residuals, B = {meta['B']}, "
        f"seed = {meta['seed']}).",
        language="text",
    )
    st.caption("انسخ هذه الجملة إلى قسم المنهجية في ورقتك.")

# ============================================================== CUSUM
st.header("٥. فحص الاستقرار الهيكلي")

if st.button("📈  ارسم CUSUM بحِزَم البوتستراب", key="lab_cusum"):
    with st.spinner("جارٍ توليد حِزَم البوتستراب…"):
        rngc = np.random.default_rng(int(seed_l))
        w0 = recursive_residuals(yy, XX)
        p0 = cusum_path(w0)
        L = len(p0)
        paths = []
        for _ in range(399):
            ys, Xs = bootstrap_sample(XX, fit["b"], fit["u"], fit["h"],
                                      dgp_l, wt_l, ft_l, rngc, dyn_col)
            ws = recursive_residuals(ys, Xs)
            if len(ws) == L:
                paths.append(cusum_path(ws))
        P = np.array(paths)
    if len(P) > 20:
        lo = np.quantile(P, 0.025, 0)
        hi = np.quantile(P, 0.975, 0)
        a = 0.948
        ri = np.arange(1, L + 1)
        ahi = a * (np.sqrt(L) + 2 * ri / np.sqrt(L))
        plotly(anim_cusum(p0, (lo, hi), (-ahi, ahi)), key="lab_cusum_fig")
        nout = int(((p0 > hi) | (p0 < lo)).sum())
        if nout > 0:
            st.error(
                f"المسار يخرج عن حزمة البوتستراب في **{nout}** نقطة → "
                f"دليل على عدم استقرار المعالم."
            )
        else:
            st.success("المسار يبقى داخل حزمة البوتستراب → المعالم مستقرّة.")
    else:
        st.warning("تعذّر توليد عدد كافٍ من المسارات بنفس الطول.")

st.divider()
st.markdown(
    "**الصفحة التالية:** حزمة `bootdiag` في Stata — التوثيق الكامل، "
    "لتُطبّق كل ما سبق على بياناتك الحقيقية داخل Stata."
)
