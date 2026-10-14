"""Observer agreement for visual crown scores (quality assurance)."""
import numpy as np


def quadratic_weighted_kappa(a, b, n_classes=5):
    a, b = np.asarray(a, int), np.asarray(b, int)
    O = np.zeros((n_classes, n_classes))
    for i, j in zip(a, b):
        O[i, j] += 1
    E = np.outer(O.sum(1), O.sum(0)) / O.sum()
    w = np.array([[(i - j) ** 2 for j in range(n_classes)] for i in range(n_classes)], float) / (n_classes - 1) ** 2
    den = (w * E).sum()
    return float(1 - (w * O).sum() / den) if den else float("nan")


def icc_2_1(X):
    """ICC(2,1), two-way random effects, absolute agreement. X: (targets, raters)."""
    X = np.asarray(X, float)
    n, k = X.shape
    gm = X.mean()
    msr = k * ((X.mean(1) - gm) ** 2).sum() / (n - 1)
    msc = n * ((X.mean(0) - gm) ** 2).sum() / (k - 1)
    sse = ((X - X.mean(1, keepdims=True) - X.mean(0, keepdims=True) + gm) ** 2).sum()
    mse = sse / ((n - 1) * (k - 1))
    return float((msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n))


def pair_summary(a, b, tol=(5, 10)):
    """Agreement between two observers on defoliation percentages."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = a - b
    s = d.std(ddof=1)
    out = {"n": len(a), "bias": float(d.mean()), "loa_low": float(d.mean() - 1.96 * s), "loa_high": float(d.mean() + 1.96 * s),
           "mean_abs_diff": float(np.abs(d).mean()), "icc_2_1": icc_2_1(np.column_stack([a, b]))}
    for t in tol:
        out[f"within_{t}"] = float((np.abs(d) <= t).mean())
    return out
