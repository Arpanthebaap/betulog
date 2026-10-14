"""Association models and isolation summaries."""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from .icp import SYMPTOMS


def tidy_trees(df):
    df = df.copy()
    for s in SYMPTOMS + ["dead"]:
        df[s] = df[s].astype(str).str.lower().eq("true").astype(int)
    return df


def symptom_model(df, symptoms=None):
    """Linear mixed model: defoliation ~ symptoms + (1 | plot). Falls back to OLS with one plot."""
    df = tidy_trees(df)
    use = [s for s in (symptoms or SYMPTOMS) if df[s].nunique() > 1]
    if not use:
        raise ValueError("No symptom varies across trees.")
    f = "defol ~ " + " + ".join(use)
    if df["plot"].nunique() < 2:
        return smf.ols(f, df).fit(), "OLS (single plot; no random effect)"
    return smf.mixedlm(f, df, groups=df["plot"]).fit(), "Mixed model, random intercept for plot"


def isolation_table(trees, iso):
    """Isolates per tissue, with the number of distinct trees sampled."""
    m = iso.merge(trees[["id", "plot", "class"]], left_on="tree", right_on="id", how="left")
    return m.groupby("tissue").agg(isolates=("id_x", "count"), trees=("tree", "nunique")).reset_index()
