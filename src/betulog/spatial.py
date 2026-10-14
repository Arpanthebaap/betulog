"""Spatial autocorrelation of crown condition within a plot (Moran's I with permutation test)."""
import numpy as np


def morans_i(x, y, z, n_perm=999, seed=0):
    """Inverse-distance weights, row-standardised. Positive I: similar crown scores cluster in space."""
    pts = np.column_stack([x, y]).astype(float)
    z = np.asarray(z, float)
    n = len(z)
    if n < 8:
        return {"I": float("nan"), "p": float("nan"), "n": n}
    d = np.sqrt(((pts[:, None] - pts[None]) ** 2).sum(-1))
    np.fill_diagonal(d, np.inf)
    w = 1.0 / np.maximum(d, 1e-9)
    w /= w.sum(1, keepdims=True)

    def stat(v):
        c = v - v.mean()
        den = (c ** 2).sum()
        return n * (c @ w @ c) / (w.sum() * den) if den else 0.0

    obs = stat(z)
    rng = np.random.default_rng(seed)
    perm = np.array([stat(rng.permutation(z)) for _ in range(n_perm)])
    p = (1 + (perm >= obs).sum()) / (n_perm + 1)
    return {"I": float(obs), "p": float(p), "expected": -1.0 / (n - 1), "n": n}
