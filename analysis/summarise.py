#!/usr/bin/env python3
"""Summarise a Betulog trees CSV export: per-plot class distribution and symptom contrasts.

Usage: python3 analysis/summarise.py data/example_trees.csv
Needs pandas. Descriptive only; use a mixed model (plot as random effect) for inference.
"""
import sys
import pandas as pd

SYMPTOMS = ["canker", "bleed", "fruit", "crack", "insect", "browse", "root"]
NAMES = ["none", "slight", "moderate", "severe", "dead"]

def main(path):
    df = pd.read_csv(path)
    for s in SYMPTOMS + ["dead"]:
        df[s] = df[s].astype(str).str.lower().eq("true")
    for plot, g in df.groupby("plot"):
        n = len(g)
        print(f"\nPlot {plot}: {n} trees, mean defoliation {g.defol.mean():.1f}%, mortality {100*g.dead.mean():.0f}%")
        counts = g["class"].value_counts().reindex(range(5), fill_value=0)
        print("  classes: " + ", ".join(f"{NAMES[i]} {counts[i]}" for i in range(5)))
        for s in SYMPTOMS:
            w, o = g[g[s]], g[~g[s]]
            if len(w):
                print(f"  {s:8s} n={len(w):3d} mean defol with {w.defol.mean():5.1f} vs without {o.defol.mean() if len(o) else float('nan'):5.1f}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
