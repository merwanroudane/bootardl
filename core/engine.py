"""
محرّك البوتستراب: توليد البيانات، إحصاءات الاختبارات البعدية،
وعمليات إعادة المعاينة (Bootstrap DGPs).

كل الصيغ مكتوبة كما وردت في الأوراق الأصلية المذكورة في صفحة المراجع.
منصة البوتستراب — د. مروان رودان
"""

from __future__ import annotations

import numpy as np
from scipy import stats as sps

# ============================================================================
# 1) أدوات الانحدار الأساسية
# ============================================================================


def ols(y: np.ndarray, X: np.ndarray) -> dict:
    """انحدار المربعات الصغرى العادية — Ordinary Least Squares."""
    XtX = X.T @ X
    XtXi = np.linalg.pinv(XtX)
    b = XtXi @ (X.T @ y)
    u = y - X @ b
    n, k = X.shape
    dof = max(n - k, 1)
    s2 = float(u @ u) / dof
    h = np.einsum("ij,jk,ik->i", X, XtXi, X)       # leverage h_t
    return {"b": b, "u": u, "n": n, "k": k, "s2": s2, "XtXi": XtXi,
            "h": np.clip(h, 0.0, 0.9999), "fit": X @ b, "rss": float(u @ u)}


def add_const(X: np.ndarray) -> np.ndarray:
    return np.column_stack([np.ones(len(X)), X])


def lagmat(x: np.ndarray, lags: int) -> np.ndarray:
    """مصفوفة الإبطاءات 1..lags مع تصفير القيم الأولى."""
    n = len(x)
    out = np.zeros((n, lags))
    for j in range(1, lags + 1):
        out[j:, j - 1] = x[:-j]
    return out


# ============================================================================
# 2) توليد البيانات للمحاكاة
# ============================================================================


def simulate_dgp(n: int = 60, rho: float = 0.5, beta: float = 1.0,
                 het: float = 0.0, err: str = "normal",
                 brk: float = 0.0, rng: np.random.Generator | None = None) -> dict:
    """
    عملية توليد البيانات: y_t = c + rho*y_{t-1} + beta*x_t + u_t

    het : شدة عدم تجانس التباين (0 = متجانس)
    err : normal | t5 | chi2 | mixture
    brk : حجم الكسر الهيكلي في منتصف العينة
    """
    rng = rng or np.random.default_rng()
    burn = 50
    N = n + burn

    x = rng.normal(0, 1, N)
    x = np.cumsum(rng.normal(0, 1, N)) * 0.0 + x      # x مستقر

    if err == "t5":
        e = rng.standard_t(5, N) / np.sqrt(5 / 3)
    elif err == "chi2":
        e = (rng.chisquare(2, N) - 2) / 2.0
    elif err == "mixture":
        m = rng.random(N) < 0.1
        e = rng.normal(0, 1, N) * (~m) + rng.normal(0, 4, N) * m
        e = e / np.std(e)
    else:
        e = rng.normal(0, 1, N)

    if het > 0:
        e = e * np.exp(het * x)                       # تباين متغيّر دالّة في x

    y = np.zeros(N)
    for t in range(1, N):
        shift = brk if t > burn + n // 2 else 0.0
        y[t] = 0.2 + shift + rho * y[t - 1] + beta * x[t] + e[t]

    y, x = y[burn:], x[burn:]
    return {"y": y, "x": x}


def design_from(y: np.ndarray, x: np.ndarray, dynamic: bool = True) -> tuple:
    """بناء y و X لنموذج ديناميكي y_t على ثابت و y_{t-1} و x_t."""
    if dynamic:
        yy = y[1:]
        X = np.column_stack([np.ones(len(yy)), y[:-1], x[1:]])
    else:
        yy = y
        X = np.column_stack([np.ones(len(y)), x])
    return yy, X


# ============================================================================
# 3) إحصاءات الاختبارات البعدية
# ============================================================================


def bg_lm(u: np.ndarray, X: np.ndarray, q: int = 2) -> float:
    """Breusch–Godfrey LM لاختبار الارتباط الذاتي حتى الرتبة q."""
    n = len(u)
    E = lagmat(u, q)
    W = np.column_stack([X, E])
    r = ols(u, W)
    tss = float(u @ u)
    if tss <= 0:
        return 0.0
    r2 = 1.0 - r["rss"] / tss
    return float(n * max(r2, 0.0))


def bg_lm_hr(u: np.ndarray, X: np.ndarray, q: int = 2) -> float:
    """
    النسخة الحصينة لعدم تجانس التباين — Godfrey & Tremayne (2005) eq.(5).
    LM_HR = u'E { E'M(W) Omega M(W) E }^-1 E'u  مع Omega = diag(u_t^2) المقيّدة.
    """
    E = lagmat(u, q)
    M = np.eye(len(u)) - X @ np.linalg.pinv(X.T @ X) @ X.T
    ME = M @ E
    Om = np.diag(u ** 2)
    A = ME.T @ Om @ ME
    v = E.T @ u
    try:
        return float(v @ np.linalg.solve(A + 1e-12 * np.eye(q), v))
    except np.linalg.LinAlgError:
        return 0.0


def bg_mlm_hr(u: np.ndarray, X: np.ndarray, q: int = 2) -> float:
    """
    النسخة المعدّلة MLM_HR — Godfrey & Tremayne (2005) eq.(6):
    تُسقط الحدود المهملة تقاربياً فتقلّ تقلّبات مقدّر HCCME.
    """
    E = lagmat(u, q)
    Et = E * u[:, None]
    v = E.T @ u
    A = Et.T @ Et
    try:
        return float(v @ np.linalg.solve(A + 1e-12 * np.eye(q), v))
    except np.linalg.LinAlgError:
        return 0.0


def durbin_watson(u: np.ndarray) -> float:
    d = np.diff(u)
    return float((d @ d) / (u @ u)) if (u @ u) > 0 else 2.0


def rho_hat(u: np.ndarray) -> float:
    return float((u[1:] @ u[:-1]) / (u @ u)) if (u @ u) > 0 else 0.0


def breusch_pagan(u: np.ndarray, Z: np.ndarray) -> float:
    """Breusch & Pagan (1979): نصف مجموع المربعات المفسّر من g على Z."""
    s2 = float(u @ u) / len(u)
    g = u ** 2 / s2
    r = ols(g - g.mean(), Z)
    ess = float(((Z @ r["b"]) ** 2).sum())
    return 0.5 * ess


def koenker(u: np.ndarray, Z: np.ndarray) -> float:
    """Koenker (1981): T*R^2 من انحدار u^2 على Z — نسخة مُستودنتة حصينة."""
    y = u ** 2
    yc = y - y.mean()
    r = ols(yc, Z)
    tss = float(yc @ yc)
    if tss <= 0:
        return 0.0
    return float(len(u) * max(1.0 - r["rss"] / tss, 0.0))


def white_test(u: np.ndarray, X: np.ndarray) -> float:
    """White (1980): T*R^2 على المستويات والمربعات والتفاعلات."""
    cols = [X[:, j] for j in range(1, X.shape[1])]
    extra = []
    for i in range(len(cols)):
        for j in range(i, len(cols)):
            extra.append(cols[i] * cols[j])
    Z = np.column_stack(cols + extra) if cols else np.zeros((len(u), 1))
    Z = Z - Z.mean(0)
    return koenker(u, Z)


def arch_lm(u: np.ndarray, q: int = 2) -> float:
    """Engle (1982) ARCH LM: T*R^2 من u^2 على إبطاءاتها."""
    y = u ** 2
    Z = lagmat(y, q)
    yc = y - y.mean()
    Zc = np.column_stack([np.ones(len(y)), Z])
    r = ols(yc, Zc)
    tss = float(yc @ yc)
    if tss <= 0:
        return 0.0
    return float(len(u) * max(1.0 - r["rss"] / tss, 0.0))


def szroeter(u: np.ndarray) -> float:
    """Szroeter SKH: مُرجّح جيبي للمربعات المرتّبة."""
    T = len(u)
    t = np.arange(1, T + 1)
    w = 2.0 * (1.0 - np.cos(np.pi * t / (T + 1)))
    return float((w * u ** 2).sum() / (u ** 2).sum())


def harrison_mccabe(u: np.ndarray) -> float:
    """Harrison–McCabe: نسبة مربعات النصف الأول إلى الكل."""
    m = len(u) // 2
    return float((u[:m] ** 2).sum() / (u ** 2).sum())


def jarque_bera(u: np.ndarray) -> float:
    """Jarque & Bera (1980): T[b1/6 + (b2-3)^2/24]."""
    T = len(u)
    z = u - u.mean()
    m2 = (z ** 2).mean()
    if m2 <= 0:
        return 0.0
    b1 = ((z ** 3).mean() / m2 ** 1.5) ** 2
    b2 = (z ** 4).mean() / m2 ** 2
    return float(T * (b1 / 6.0 + (b2 - 3.0) ** 2 / 24.0))


def anderson_darling(u: np.ndarray) -> float:
    z = np.sort((u - u.mean()) / (u.std(ddof=1) + 1e-12))
    T = len(z)
    F = sps.norm.cdf(z)
    F = np.clip(F, 1e-10, 1 - 1e-10)
    i = np.arange(1, T + 1)
    s = ((2 * i - 1) * (np.log(F) + np.log(1 - F[::-1]))).sum()
    return float(-T - s / T)


def reset_test(y: np.ndarray, X: np.ndarray, power: int = 3) -> float:
    """Ramsey RESET: اختبار F على قوى القيمة المقدّرة."""
    r = ols(y, X)
    f = r["fit"]
    f = f / (np.abs(f).max() + 1e-12)
    extra = np.column_stack([f ** p for p in range(2, power + 1)])
    Xa = np.column_stack([X, extra])
    ra = ols(y, Xa)
    m = extra.shape[1]
    dof = len(y) - Xa.shape[1]
    if dof <= 0 or ra["rss"] <= 0:
        return 0.0
    return float(((r["rss"] - ra["rss"]) / m) / (ra["rss"] / dof))


def sup_f(y: np.ndarray, X: np.ndarray, trim: float = 0.15) -> tuple:
    """
    supF على تاريخ كسر مجهول — Andrews (1993).
    يُرجع (supF, aveF, expF, مصفوفة F عبر التواريخ، التواريخ).
    """
    n, k = X.shape
    lo, hi = int(np.floor(trim * n)), int(np.ceil((1 - trim) * n))
    lo = max(lo, k + 1)
    hi = min(hi, n - k - 1)
    r0 = ols(y, X)
    Fs, dates = [], []
    for b in range(lo, hi + 1):
        r1 = ols(y[:b], X[:b])
        r2 = ols(y[b:], X[b:])
        den = (r1["rss"] + r2["rss"]) / max(n - 2 * k, 1)
        if den <= 0:
            continue
        F = ((r0["rss"] - r1["rss"] - r2["rss"]) / k) / den
        Fs.append(max(F, 0.0))
        dates.append(b)
    if not Fs:
        return 0.0, 0.0, 0.0, np.array([]), np.array([])
    Fs = np.array(Fs)
    sup = float(Fs.max())
    ave = float(Fs.mean())
    exp = float(np.log(np.mean(np.exp(np.clip(Fs / 2.0, None, 300.0)))))
    return sup, ave, exp, Fs, np.array(dates)


def recursive_residuals(y: np.ndarray, X: np.ndarray) -> np.ndarray:
    """البواقي التكرارية w_r — Brown, Durbin & Evans (1975)."""
    n, k = X.shape
    w = []
    for r in range(k, n):
        Xr, yr = X[:r], y[:r]
        G = np.linalg.pinv(Xr.T @ Xr)
        b = G @ (Xr.T @ yr)
        xr = X[r]
        f = np.sqrt(max(1.0 + xr @ G @ xr, 1e-12))
        w.append((y[r] - xr @ b) / f)
    return np.array(w)


def cusum_path(w: np.ndarray) -> np.ndarray:
    s = w.std(ddof=1)
    return np.cumsum(w - w.mean()) / (s + 1e-12)


def cusumsq_path(w: np.ndarray) -> np.ndarray:
    c = np.cumsum(w ** 2)
    return c / (c[-1] + 1e-12)


# ============================================================================
# 4) عمليات توليد بيانات البوتستراب — Bootstrap DGPs
# ============================================================================


def wild_weights(n: int, dist: str, rng: np.random.Generator) -> np.ndarray:
    """أوزان الوايلد بوتستراب."""
    if dist == "mammen":                                 # F1 — Mammen (1993)
        a = (np.sqrt(5) - 1) / 2
        b = (np.sqrt(5) + 1) / 2
        p = (np.sqrt(5) + 1) / (2 * np.sqrt(5))
        return np.where(rng.random(n) < p, -a, b)
    if dist == "normal":
        return rng.normal(0, 1, n)
    return rng.choice([-1.0, 1.0], n)                    # F2 — Rademacher


def transform_resid(u: np.ndarray, h: np.ndarray, n: int, k: int,
                    how: str = "hc3") -> np.ndarray:
    """تحويل البواقي قبل إعادة المعاينة — HC0..HC3."""
    if how == "hc1":
        return u * np.sqrt(n / max(n - k, 1))
    if how == "hc2":
        return u / np.sqrt(np.maximum(1 - h, 1e-6))
    if how == "hc3":
        return u / np.maximum(1 - h, 1e-6)
    return u                                             # hc0


def _recursive_y(X: np.ndarray, b: np.ndarray, ustar: np.ndarray,
                 dyn_col: int | None) -> tuple[np.ndarray, np.ndarray]:
    """
    توليد y* تكرارياً عندما يحتوي النموذج على متغيّر تابع مُبطّأ،
    مع إعادة بناء عمود y*_{t-1} داخل مصفوفة التصميم.
    قيم البداية هي قيم العيّنة الفعلية (Godfrey & Tremayne 2005).

    dyn_col : موقع y_{t-1} في X، أو None لنموذج ساكن.
    """
    if dyn_col is None:
        return X @ b + ustar, X
    n = len(ustar)
    Xs = X.copy()
    ys = np.zeros(n)
    prev = float(X[0, dyn_col])          # قيمة البداية الفعلية
    for t in range(n):
        Xs[t, dyn_col] = prev
        ys[t] = Xs[t] @ b + ustar[t]
        prev = ys[t]
    return ys, Xs


def bootstrap_sample(X: np.ndarray, b: np.ndarray, u: np.ndarray, h: np.ndarray,
                     dgp: str, weight: str, ftrans: str,
                     rng: np.random.Generator, dyn_col: int | None = 1,
                     block: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """
    يُنتج عيّنة بوتستراب (y*, X*) واحدة وفق عملية التوليد المختارة.

    dgp : wild | residual | fixed | sieve | block | stationary | blockwild | normal
    """
    n, k = X.shape
    ut = transform_resid(u, h, n, k, ftrans)

    if dgp == "wild":
        us = ut * wild_weights(n, weight, rng)
        return _recursive_y(X, b, us, dyn_col)

    if dgp == "fixed":                                   # Hansen (2000)
        us = ut * wild_weights(n, weight, rng)
        return X @ b + us, X                             # بلا توليد تكراري

    if dgp == "residual":
        c = ut - ut.mean()
        us = rng.choice(c, n, replace=True)
        return _recursive_y(X, b, us, dyn_col)

    if dgp == "normal":
        us = rng.normal(0, u.std(ddof=1), n)
        return _recursive_y(X, b, us, dyn_col)

    if dgp == "sieve":                                   # Bühlmann (1997)
        p = max(1, min(int(np.floor(4 * (n / 100) ** 0.25)), n // 5))
        Z = lagmat(u, p)[p:]
        r = ols(u[p:], np.column_stack([np.ones(len(Z)), Z]))
        phi = r["b"][1:]
        eps = r["u"] - r["u"].mean()
        e = rng.choice(eps, n + 50, replace=True)
        v = np.zeros(n + 50)
        for t in range(p, n + 50):
            v[t] = phi @ v[t - p:t][::-1] + e[t]
        us = v[50:]
        return _recursive_y(X, b, us, dyn_col)

    if dgp in ("block", "blockwild"):                    # Künsch / Lee & Baek
        L = block or max(2, int(round(n ** (1 / 3))))
        nb = int(np.ceil(n / L))
        if dgp == "block":
            starts = rng.integers(0, max(n - L, 1), nb)
            us = np.concatenate([ut[s:s + L] for s in starts])[:n]
            us = us - us.mean()
        else:
            w = wild_weights(nb, weight, rng)
            us = np.concatenate([ut[i * L:(i + 1) * L] * w[i] for i in range(nb)])[:n]
        if len(us) < n:
            us = np.resize(us, n)
        return _recursive_y(X, b, us, dyn_col)

    if dgp == "stationary":                              # Politis & Romano (1994)
        p = 1.0 / max(block or max(2, int(round(n ** (1 / 3)))), 2)
        idx = np.empty(n, dtype=int)
        idx[0] = rng.integers(0, n)
        for t in range(1, n):
            idx[t] = rng.integers(0, n) if rng.random() < p else (idx[t - 1] + 1) % n
        us = ut[idx] - ut.mean()
        return _recursive_y(X, b, us, dyn_col)

    raise ValueError(f"DGP غير معروف: {dgp}")


# ============================================================================
# 5) قيم p البوتستراب
# ============================================================================


def boot_p(stat: float, boot: np.ndarray, kind: str = "upper",
           continuous: bool = False, rng: np.random.Generator | None = None) -> float:
    """
    قيمة p البوتستراب — MacKinnon (2007).
    upper      : p = (1/B) Σ I(τ* > τ̂)
    symmetric  : على القيمة المطلقة
    equaltail  : 2·min(يسار، يمين)
    mc         : تصحيح +1 لمونت كارلو  (N·Ĝ+1)/(N+1)  — Dufour et al. (2004)
    continuous : (N + U)/(B+1)  — Racine & MacKinnon (2007)
    """
    B = len(boot)
    if B == 0:
        return np.nan
    if kind == "symmetric":
        N = int((np.abs(boot) > abs(stat)).sum())
    elif kind == "equaltail":
        up = (boot > stat).sum() / B
        lo = (boot <= stat).sum() / B
        return float(min(2 * min(up, lo), 1.0))
    else:
        N = int((boot > stat).sum())
    if continuous:
        rng = rng or np.random.default_rng()
        return float((N + rng.random()) / (B + 1))
    if kind == "mc":
        return float((N + 1) / (B + 1))
    return float(N / B)


# ============================================================================
# 6) الاختبار الكامل: إحصاء + توزيع بوتستراب + قيمتا p
# ============================================================================

TESTS = {
    "bg":       ("Breusch–Godfrey LM",  "الارتباط الذاتي"),
    "bg_hr":    ("BG robust LM_HR",     "الارتباط الذاتي (حصين)"),
    "mlm_hr":   ("BG modified MLM_HR",  "الارتباط الذاتي (معدّل)"),
    "dw":       ("Durbin–Watson d",     "الارتباط الذاتي"),
    "bp":       ("Breusch–Pagan LM",    "عدم تجانس التباين"),
    "koenker":  ("Koenker studentised", "عدم تجانس التباين"),
    "white":    ("White general",       "عدم تجانس التباين"),
    "arch":     ("Engle ARCH LM",       "عدم تجانس التباين"),
    "szroeter": ("Szroeter SKH",        "عدم تجانس التباين"),
    "jb":       ("Jarque–Bera",         "الاعتدالية"),
    "ad":       ("Anderson–Darling",    "الاعتدالية"),
    "reset":    ("Ramsey RESET",        "الشكل الدالي"),
    "supf":     ("supF",                "الاستقرار الهيكلي"),
    "avef":     ("aveF",                "الاستقرار الهيكلي"),
}


def compute_stat(name: str, y: np.ndarray, X: np.ndarray, q: int = 2,
                 trim: float = 0.15) -> float:
    r = ols(y, X)
    u = r["u"]
    Z = X[:, 1:] - X[:, 1:].mean(0)
    if name == "bg":
        return bg_lm(u, X, q)
    if name == "bg_hr":
        return bg_lm_hr(u, X, q)
    if name == "mlm_hr":
        return bg_mlm_hr(u, X, q)
    if name == "dw":
        return durbin_watson(u)
    if name == "bp":
        return breusch_pagan(u, Z)
    if name == "koenker":
        return koenker(u, Z)
    if name == "white":
        return white_test(u, X)
    if name == "arch":
        return arch_lm(u, q)
    if name == "szroeter":
        return szroeter(u)
    if name == "jb":
        return jarque_bera(u)
    if name == "ad":
        return anderson_darling(u)
    if name == "reset":
        return reset_test(y, X)
    if name in ("supf", "avef"):
        s, a, _, _, _ = sup_f(y, X, trim)
        return s if name == "supf" else a
    raise ValueError(name)


def asymptotic_p(name: str, stat: float, n: int, k: int, q: int = 2) -> float:
    """قيمة p التقاربية من الجدول المعتاد (للمقارنة فقط)."""
    if name in ("bg", "bg_hr", "mlm_hr"):
        return float(sps.chi2.sf(stat, q))
    if name in ("bp",):
        return float(sps.chi2.sf(stat, max(k - 1, 1)))
    if name in ("koenker",):
        return float(sps.chi2.sf(stat, max(k - 1, 1)))
    if name == "white":
        return float(sps.chi2.sf(stat, max(k, 1)))
    if name == "arch":
        return float(sps.chi2.sf(stat, q))
    if name == "jb":
        return float(sps.chi2.sf(stat, 2))
    if name == "reset":
        return float(sps.f.sf(stat, 2, max(n - k - 2, 1)))
    if name == "dw":
        return np.nan
    if name == "szroeter":
        return np.nan
    if name == "ad":
        return np.nan
    if name in ("supf", "avef"):
        return np.nan
    return np.nan


def run_boot_test(name: str, y: np.ndarray, X: np.ndarray, B: int = 499,
                  dgp: str = "wild", weight: str = "rademacher",
                  ftrans: str = "hc3", q: int = 2, trim: float = 0.15,
                  dyn_col: int | None = 1, seed: int = 1234,
                  continuous: bool = False) -> dict:
    """
    يُنفّذ اختباراً بعدياً واحداً بنسخته البوتستراب.
    الإحصاء كما في الورقة الأصلية؛ ما يتغيّر هو التوزيع تحت الفرضية الصفرية.
    """
    rng = np.random.default_rng(seed)
    r = ols(y, X)
    stat = compute_stat(name, y, X, q, trim)

    boot = np.empty(B)
    for i in range(B):
        ys, Xs = bootstrap_sample(X, r["b"], r["u"], r["h"], dgp, weight,
                                  ftrans, rng, dyn_col)
        try:
            boot[i] = compute_stat(name, ys, Xs, q, trim)
        except Exception:
            boot[i] = np.nan
    boot = boot[np.isfinite(boot)]

    kind = "equaltail" if name == "dw" else "upper"
    p_boot = boot_p(stat, boot, kind, continuous, rng)
    p_asy = asymptotic_p(name, stat, r["n"], r["k"], q)

    return {"name": name, "label": TESTS[name][0], "family": TESTS[name][1],
            "stat": stat, "boot": boot, "p_boot": p_boot, "p_asy": p_asy,
            "crit95": float(np.quantile(boot, 0.95)) if len(boot) else np.nan}


# ============================================================================
# 7) تجربة مونت كارلو لقياس الحجم الحقيقي
# ============================================================================


def size_experiment(name: str, n: int, rho: float, het: float, reps: int,
                    B: int, dgp: str = "wild", alpha: float = 0.05,
                    err: str = "normal", seed: int = 7) -> dict:
    """
    تجربة تحت الفرضية الصفرية: نسبة الرفض الفعلية مقابل المستوى الاسمي.
    اختبار سليم يرفض بنسبة alpha فقط.
    """
    rng = np.random.default_rng(seed)
    rej_a, rej_b, n_ok = 0, 0, 0
    for _ in range(reps):
        d = simulate_dgp(n, rho, 1.0, het, err, 0.0, rng)
        y, X = design_from(d["y"], d["x"])
        try:
            res = run_boot_test(name, y, X, B, dgp, "rademacher", "hc3",
                                seed=int(rng.integers(1, 10 ** 8)))
        except Exception:
            continue
        n_ok += 1
        if np.isfinite(res["p_asy"]) and res["p_asy"] < alpha:
            rej_a += 1
        if res["p_boot"] < alpha:
            rej_b += 1
    k = max(n_ok, 1)
    return {"asymptotic": rej_a / k, "bootstrap": rej_b / k, "reps": n_ok,
            "alpha": alpha}
