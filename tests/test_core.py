import numpy as np, pandas as pd
from betulog import *

def test_classes():
    assert list(defol_class([0, 10, 11, 25, 26, 60, 61, 99, 100])) == [0, 0, 1, 1, 2, 2, 3, 3, 4]
    assert defol_class(30, dead=True) == 4

def test_kappa_icc_identity():
    a = np.array([0, 1, 2, 3, 4, 2, 1]); assert abs(quadratic_weighted_kappa(a, a) - 1) < 1e-9
    x = np.array([10., 20, 30, 40, 50]); assert abs(icc_2_1(np.column_stack([x, x])) - 1) < 1e-9

def test_icc_penalises_bias():
    x = np.array([10., 20, 30, 40, 50]); assert icc_2_1(np.column_stack([x, x + 20])) < 0.9

def test_pair_summary_bias():
    x = np.array([10., 20, 30, 40, 50]); s = pair_summary(x + 5, x); assert abs(s["bias"] - 5) < 1e-9 and s["within_5"] == 1.0

def test_morans_detects_clustering():
    rng = np.random.default_rng(0); x, y = rng.uniform(0, 30, 80), rng.uniform(0, 30, 80)
    clustered = 20 + 3 * x + rng.normal(0, 3, 80)
    assert morans_i(x, y, clustered, 199)["p"] < 0.05
    assert morans_i(x, y, rng.normal(30, 10, 80), 199)["p"] > 0.01

def test_power_monotone_in_plots():
    assert simulate_power(n_plots=6, n_sim=150) < simulate_power(n_plots=30, n_sim=150)

def test_power_falls_with_observer_error():
    assert simulate_power(sd_obs=0, n_sim=200, seed=3) >= simulate_power(sd_obs=15, n_sim=200, seed=3)

def test_model_runs():
    rng = np.random.default_rng(1); rows = []
    for p in "ABC":
        for i in range(30):
            c = rng.random() < .3
            rows.append(dict(plot=p, defol=20 + 15 * c + rng.normal(0, 8), canker=str(c).lower(), bleed="false", fruit="false", crack=str(rng.random() < .2).lower(), insect="false", browse="false", root="false", dead="false"))
    fit, label = symptom_model(pd.DataFrame(rows))
    assert fit.params["canker"] > 5
