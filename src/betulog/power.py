"""Simulation-based power for a plot-level design, including observer error.
Design: in each plot, a symptom affects a fraction of trees and raises true defoliation by `effect` points.
Analysis: within-plot mean difference (symptomatic - not), one-sample t-test across plots."""
import numpy as np
from scipy import stats


def simulate_power(n_plots=15, trees=30, prevalence=0.3, effect=10.0, sd_plot=8.0, sd_tree=12.0,
                   sd_obs=6.0, base=25.0, n_sim=500, alpha=0.05, seed=1):
    rng = np.random.default_rng(seed)
    hits = 0
    valid = 0
    for _ in range(n_sim):
        diffs = []
        for _p in range(n_plots):
            sym = rng.random(trees) < prevalence
            if sym.sum() < 2 or (~sym).sum() < 2:
                continue
            true = base + rng.normal(0, sd_plot) + effect * sym + rng.normal(0, sd_tree, trees)
            obs = np.clip(np.round((true + rng.normal(0, sd_obs, trees)) / 5) * 5, 0, 100)
            diffs.append(obs[sym].mean() - obs[~sym].mean())
        if len(diffs) >= 3:
            valid += 1
            hits += stats.ttest_1samp(diffs, 0).pvalue < alpha
    return hits / valid if valid else float("nan")
