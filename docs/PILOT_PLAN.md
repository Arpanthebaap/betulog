# Observer Calibration and Pilot Survey Plan

## Overview
This document outlines the step-by-step protocol for conducting an observer calibration trial and an initial pilot plot for birch crown health surveys using **Betulog**. 

Before undertaking extensive field surveys, visual assessments must be calibrated across observers to prevent observer bias from confounding site or stand comparisons.

---

## Phase 1: 30-Tree Observer Calibration Trial

### 1.1 Objective
Calibrate two independent observers on 30 standing birch trees (*Betula pendula* / *Betula pubescens*) across a gradient of crown health (healthy, moderate thinning, severe dieback, dead).

### 1.2 Tree Selection & Setup
1. Identify 30 accessible birch trees within the stand.
2. Number the trees from 1 to 30 using temporary tree tags or chalk (do not damage bark).
3. Ensure each tree can be viewed unobstructed from at least two opposite directions at a distance roughly equal to one tree height.
4. Establish a local reference tree (or reference photograph) for an optimal, fully foliated crown on the site.

### 1.3 Independent Scoring Protocol
1. **No Collaboration:** Observer 1 and Observer 2 must score all 30 trees independently without discussing scores or comparing notes during assessment.
2. **Standard Distance & Angle:** Both observers view each tree from the same designated viewpoints in consistent lighting.
3. **Scoring Increments:** Record defoliation percentage in 5% steps (0%, 5%, 10%, ..., 95%, 100%), comparing needle/leaf loss against the local reference standard.
4. **Recording:** Enter raw percentages directly into the observer calibration template.

### 1.4 Observer Scores CSV Template
Save the paired observations into a CSV file (e.g., `data/pilot_observers.csv`) formatted as follows:

```csv
tree,observer1,observer2
PILOT-T001,10,10
PILOT-T002,15,20
PILOT-T003,20,15
PILOT-T004,5,5
PILOT-T005,25,25
...
PILOT-T030,100,100
```

### 1.5 Computing Observer Agreement
Run the Betulog agreement analysis from the command line:

```bash
python analysis/observer_agreement.py data/pilot_observers.csv
```

Alternatively, to invoke `betulog.pair_summary` and `quadratic_weighted_kappa` directly from a Python script or shell:

```python
import pandas as pd
from betulog.agreement import pair_summary, quadratic_weighted_kappa
from betulog.icp import defol_class

df = pd.read_csv("data/pilot_observers.csv")
summary = pair_summary(df["observer1"], df["observer2"])
print("Pair Summary:", summary)

cls1 = defol_class(df["observer1"])
cls2 = defol_class(df["observer2"])
qw_kappa = quadratic_weighted_kappa(cls1, cls2)
print("Quadratic Weighted Kappa:", qw_kappa)
```

### 1.6 Calibration Acceptance Criteria
Acceptable calibration thresholds prior to operational surveying:
- **Mean Bias**: Within $\pm 5.0$ percentage points.
- **Mean Absolute Difference (MAD)**: $\le 10.0$ percentage points.
- **Tolerance Share**: $\ge 85\%$ of trees within 10 percentage points difference.
- **Intraclass Correlation Coefficient (ICC(2,1))**: $\ge 0.85$.
- **Quadratic Weighted Kappa ($\kappa_w$)**: $\ge 0.75$ on ICP Forests classes.

If criteria are not met:
- Observers jointly review trees with discrepancies $>10$ points to align visual standards.
- Repeat the 30-tree calibration on a new set of trees until thresholds are reached.

---

## Phase 2: Fully Recorded Pilot Plot

Once calibration is achieved, proceed to one fully recorded operational plot to validate data entry, mapping, and isolate logging workflows.

### 2.1 Plot Setup
1. Establish a circular (e.g. 20–25 m radius) or square plot (e.g. $30 \times 30\text{ m}$).
2. Record Plot ID (e.g., `ALN-01`), Site name, Stand type (`Young plantation` or `Older stand`), Stand age, Assessment date, and Observer name.

### 2.2 Tree Assessment (Betulog Tab 1)
For all tagged birch trees within the plot:
1. **Position (X, Y in metres):** Measured from the plot origin (corner or centre).
2. **Stem Size:** DBH in centimetres.
3. **Crown Scoring:** Defoliation %, Crown dieback %, Foliage discolouration %.
4. **Symptom Flags:** Check visible symptoms:
   - Stem lesion or canker
   - Sap bleeding
   - Fruiting bodies
   - Bark cracks / frost injury
   - Insect damage (defoliators, borers)
   - Browsing damage
   - Root-collar rot / visible mycelium
   - Tree dead
5. **Notes & GPS:** Enter field observations and press "Save GPS to notes" if browser geolocation is enabled.

### 2.3 Isolate Logging (Betulog Tab 2)
For trees exhibiting active lesions, decay, or decline symptoms:
1. Collect tissue samples at the margin between healthy and symptomatic tissue using sterile tools.
2. Log isolate ID (e.g. `ISO-ALN01-001`), corresponding Tree ID, tissue type (`Bark lesion margin`, `Inner bark`, `Root`, `Xylem`, etc.), medium, and morphotype notes.
3. Update culture status as samples move through plating, pure culture, DNA extraction, and sequencing.

### 2.4 Data Export & Quality Check
1. Export `betulog_trees.csv` and `betulog_isolates.csv` at the end of the field session.
2. Run diagnostic checks:
   ```bash
   python analysis/analyse.py betulog_trees.csv betulog_isolates.csv
   ```
3. Inspect spatial distribution (Moran's I), defoliation-symptom contrasts, and isolate link integrity.
