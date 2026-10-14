#!/usr/bin/env python3
"""Run the standard Betulog analysis on exports.
Usage: python3 analysis/analyse.py data/example_trees.csv [data/example_isolates.csv]"""
import sys, os, warnings
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from betulog import symptom_model, morans_i, isolation_table, tidy_trees, CLASS_NAMES
warnings.filterwarnings("ignore")

def main(tp, ip=None):
    df = pd.read_csv(tp)
    print(f"{len(df)} trees, {df["plot"].nunique()} plots")
    for p, g in df.groupby("plot"):
        c = g["class"].value_counts().reindex(range(5), fill_value=0)
        print(f"\nPlot {p}: mean defol {g.defol.mean():.1f}%; classes " + ", ".join(f"{CLASS_NAMES[i]} {c[i]}" for i in range(5)))
        gg = g.dropna(subset=["x", "y"])
        m = morans_i(gg.x, gg.y, gg.defol)
        print(f"  Moran's I = {m['I']:.3f} (expected {m.get('expected', float('nan')):.3f}), permutation p = {m['p']:.3f}")
    fit, label = symptom_model(df)
    print(f"\n{label}\n{fit.summary().tables[1]}")
    if ip:
        print("\nIsolation effort by tissue\n" + isolation_table(df, pd.read_csv(ip)).to_string(index=False))

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(*sys.argv[1:3])
