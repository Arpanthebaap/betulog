#!/usr/bin/env python3
"""Compute observer agreement statistics from a paired scoring CSV.

Expects a CSV with columns: tree,observer1,observer2
Values in observer1 and observer2 are defoliation percentages (0-100).

Usage:
    python analysis/observer_agreement.py data/pilot_observers_synthetic.csv
"""
import sys
import pandas as pd
from tabulate import tabulate
from betulog.agreement import pair_summary, quadratic_weighted_kappa
from betulog.icp import defol_class, CLASS_NAMES


def compute_agreement(csv_path: str):
    df = pd.read_csv(csv_path)
    required = {"tree", "observer1", "observer2"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {', '.join(required)}. Found: {list(df.columns)}")

    obs1 = df["observer1"].astype(float).values
    obs2 = df["observer2"].astype(float).values

    # Continuous percentage metrics
    summary = pair_summary(obs1, obs2)

    # Class-based metrics (ICP Forests classes 0-4)
    cls1 = defol_class(obs1)
    cls2 = defol_class(obs2)
    qw_kappa = quadratic_weighted_kappa(cls1, cls2)

    print(f"\nObserver Agreement Analysis: {csv_path}")
    print(f"Number of evaluated trees: {summary['n']}\n")

    table_continuous = [
        ["Mean Bias (Obs 1 - Obs 2)", f"{summary['bias']:+.2f} percentage points"],
        ["95% Limits of Agreement (LoA)", f"[{summary['loa_low']:+.2f}, {summary['loa_high']:+.2f}]"],
        ["Mean Absolute Difference (MAD)", f"{summary['mean_abs_diff']:.2f} percentage points"],
        ["Share within 5% tolerance", f"{summary['within_5'] * 100:.1f}%"],
        ["Share within 10% tolerance", f"{summary['within_10'] * 100:.1f}%"],
        ["Intraclass Correlation ICC(2,1)", f"{summary['icc_2_1']:.3f}"]
    ]
    print(tabulate(table_continuous, headers=["Continuous Defoliation Metric", "Value"], tablefmt="simple"))

    print("\nCategorical Class Agreement (ICP Forests Classes 0-4):")
    print(f"Quadratic Weighted Kappa (kappa_w): {qw_kappa:.3f}\n")

    # Contingency matrix
    ct = pd.crosstab(
        pd.Series(cls1, name="Observer 1").map(lambda i: f"Class {i} ({CLASS_NAMES[i]})"),
        pd.Series(cls2, name="Observer 2").map(lambda i: f"Class {i} ({CLASS_NAMES[i]})")
    )
    print("Cross-tabulation of classes:")
    print(ct.to_string())
    print()


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    compute_agreement(sys.argv[1])


if __name__ == "__main__":
    main()
