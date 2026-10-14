"""Defoliation classes as used in ICP Forests style crown assessment.
Verify the thresholds against Part IV of the ICP Forests manual for the survey year you report."""
import numpy as np

CLASS_NAMES = ["none", "slight", "moderate", "severe", "dead"]
SYMPTOMS = ["canker", "bleed", "fruit", "crack", "insect", "browse", "root"]


def defol_class(defol, dead=False):
    d = np.asarray(defol, dtype=float)
    c = np.where(d <= 10, 0, np.where(d <= 25, 1, np.where(d <= 60, 2, np.where(d < 100, 3, 4))))
    return np.where(np.asarray(dead, dtype=bool), 4, c)
