# Betulog: linked crown-health, symptom and isolate records for birch surveys, with observer calibration, spatial diagnostics and design-power analysis

**Arpan Ghosh** (independent researcher, Korvanta AI) · Version 0.2.0 · MIT licence
Live tool: https://arpanthebaap.github.io/betulog/ · Code: https://github.com/Arpanthebaap/betulog

> **Status.** The software is complete and tested (8 unit tests). Section 5.2 reports a **computer simulation under stated assumptions**, not field data. **No field results exist yet and none are claimed.** Example data in `data/` are synthetic and labelled as such.

## Abstract
Birch is increasingly planted in northern Europe, yet young plantations suffer browsing, insects, pathogens and abiotic stress, and some older stands show crown decline whose causes are unresolved. Disentangling these causes needs consistent crown scores, symptom records and a reliable link between each tree and the fungal isolates taken from it. Visual crown scores are subjective, which weakens comparisons among observers, sites and years, and few studies state in advance how many plots they need. Betulog is an open, offline tool that records ICP Forests-style crown classes, symptom flags, tree positions and isolates in one linked structure, and a Python package that adds three analyses: observer-agreement statistics for calibrating scorers, spatial autocorrelation of crown condition within plots, and mixed-model and simulation tools for design planning. In a simulation of a plot-level design, power to detect a 5-point difference in defoliation associated with a symptom rose from 0.22 with 6 plots to 0.96 with 40 plots, and observer error of 15 points lowered power from 0.61 to 0.38 at 15 plots. Field validation is pending.

## 1. Introduction
Crown decline and dieback of birch have been reported in several regions. In Scotland, widespread dieback of young planted birch was reported at an increasing number of sites from about 1999-2000, and two shoot fungi, *Marssonina betulae* and *Anisogramma virgultorum*, were identified as contributing agents (Green, 2005). In Finland, crown thinning and the fungi on fallen twigs of mature silver birch have been studied together (Paavolainen et al., 2001). In western Ukraine, several *Phytophthora* species were recovered from declining broadleaved stands that included silver birch (Matsiakh et al., 2021). These studies show that decline can involve several agents and that causes differ among sites, which makes careful, comparable survey data essential.

Two practical problems recur. First, **crown scores are visual and observer dependent**, so differences between sites or years may reflect who scored them. Second, **links between a tree's symptoms, its crown score and the isolates cultured from it** are often kept in separate spreadsheets, and the study design (how many plots, how many trees) is rarely justified quantitatively. Betulog addresses both with a linked record structure and a small set of transparent analyses.

## 2. Objectives and questions
- O1. Provide an offline, open record system that links tree, symptoms, crown class, position and isolates from the first field visit.
- O2. Quantify and improve observer consistency with agreement statistics.
- O3. Test whether crown condition is spatially clustered within a plot, which bears on whether a cause spreads from a source or acts evenly.
- O4. Estimate associations between symptoms and crown condition with plot as a random effect.
- O5. Give design guidance by simulation, including the effect of observer error on power.

## 3. Methods
### 3.1 Records and classes
Per tree: plot, position (x, y in m), DBH, defoliation, dieback, discolouration (percent), symptom flags (stem lesion, sap bleeding, fruiting bodies, bark cracks, insect damage, browsing, root-collar rot, dead) and notes. Defoliation classes: 0 (0-10%), 1 (11-25%), 2 (26-60%), 3 (61-99%), 4 (dead or 100%), as commonly used in ICP Forests crown assessment. **Check these thresholds against Part IV of the ICP Forests manual for your survey year** (ICP Forests Expert Panel, 2020). Isolates link to trees by ID, with tissue, medium, morphotype, sequence accession and status.

### 3.2 Observer agreement
For two observers on the same trees: bias, 95% limits of agreement, mean absolute difference, share within 5 and 10 points, and ICC(2,1) (two-way random effects, absolute agreement) for percentages; quadratic-weighted kappa for classes.

### 3.3 Spatial diagnostics
Moran's I with inverse-distance weights (row-standardised) on defoliation within each plot, with a 999-permutation test. Positive I with a small p suggests clustering of similar crown scores.

### 3.4 Association model
Defoliation regressed on symptom flags with a random intercept for plot (linear mixed model, `statsmodels`); OLS with a warning if only one plot is present. Descriptive only; model checking is the user's responsibility.

### 3.5 Design simulation
Each plot has a random effect (SD 8 points); each tree carries the symptom with probability 0.3, which raises true defoliation by the stated effect; tree noise SD 15; observer error added with the stated SD and rounded to 5-point steps; clipped to 0-100. Analysis: within-plot difference in mean defoliation (symptomatic minus not) tested by a one-sample t-test across plots at alpha 0.05. 20 trees per plot, 400 simulations per cell, seed 5.

## 4. Implementation
Browser app `index.html` (offline, no server, photos and data stay on the device); Python package `src/betulog`; analysis script `analysis/analyse.py`; tests in `tests/`.

```bash
pip install -e ".[dev]" && pytest
python analysis/analyse.py data/example_trees.csv data/example_isolates.csv
```

## 5. Results
### 5.1 Software verification
All 8 tests pass: class boundaries; kappa and ICC identities and sensitivity to bias; Moran's I detects built-in clustering; power rises with plots and falls with observer error; the mixed model recovers a built-in symptom effect. `analysis/analyse.py` runs on the synthetic example and reports per-plot classes, Moran's I, model coefficients and isolation effort. These checks verify the code, not field behaviour.

### 5.2 Design-power simulation (assumption-based)
Power (probability of a significant result) to detect a symptom-associated difference in defoliation:

| Scenario | Plots | Effect (points) | Observer SD | Power |
|---|---|---|---|---|
| A | 6 | 5 | 6 | 0.22 |
| A | 10 | 5 | 6 | 0.37 |
| A | 15 | 5 | 6 | 0.55 |
| A | 20 | 5 | 6 | 0.69 |
| A | 30 | 5 | 6 | 0.86 |
| A | 40 | 5 | 6 | 0.96 |
| B | 15 | 5 | 0 | 0.61 |
| B | 15 | 5 | 10 | 0.49 |
| B | 15 | 5 | 15 | 0.38 |
| C | 15 | 2.5 | 6 | 0.18 |
| C | 15 | 7.5 | 6 | 0.86 |
| C | 15 | 10 | 6 | 1.00 |

Full output: `results/power_simulation.csv`. Under these assumptions the number of plots matters more than trees per plot, and reducing observer error from SD 15 to 0 raises power by about 0.23 at the same design, which motivates calibration exercises. **These numbers depend entirely on the assumed variances.** Replace them with estimates from a pilot.

### 5.3 Field results
**Pending.** To be reported from real plots: observer agreement before and after calibration, Moran's I per plot, symptom associations, isolation success by tissue.

## 6. Limitations
- Visual scores, transparency varies with season and leaf flush
- Symptoms co-occur and do not prove causation; isolates do not prove pathogenicity (needs inoculation tests)
- Moran's I with inverse-distance weights is sensitive to plot size and tree density
- The power simulation uses a simple within-plot design and assumed variances
- localStorage in the browser app is not a database; export CSVs after each field day
- Sampling prompts in the app are general and not specialist-reviewed

## 7. Reproducibility
Seeded simulations, explicit parameters, versioned code, synthetic example data and tests are included. See `docs/DATA_DICTIONARY.md`, `docs/FIELD_PROTOCOL.md` and `docs/DATASETS.md`.

## 8. Roadmap
1. Pilot on real plots with at least two observers; estimate real variances
2. Re-run the power analysis with those variances
3. Ordinal and spatial mixed models; isolate-by-symptom association tests
4. Photo attachments and GenBank-ready export
5. Optional shared database for teams

## 9. Ethics, data and AI-use statement
Obtain landowner permission for sampling, and do not publish exact private locations. *Software and documentation were drafted with AI assistance (Claude, Anthropic) and reviewed, run and edited by the author, who is responsible for the content.* Edit this sentence so it matches what you actually did.

## References
- Green, S. (2005). *Birch dieback in Scotland.* Forestry Commission Information Note FCIN072, Forest Research.
- Paavolainen, L., Hantula, J., Hallaksela, A.-M., Kurkela, T. (2001). Dynamics of crown thinning and mycobiota on fallen twigs of mature birches (*Betula pendula*) in Finland. *Scandinavian Journal of Forest Research*, 16(3), 246-252. doi:10.1080/02827580119018
- Matsiakh, I., Kramarets, V., Cleary, M. (2021). Occurrence and diversity of *Phytophthora* species in declining broadleaf forests in western Ukraine. *Forest Pathology*, 51(1), e12662. doi:10.1111/efp.12662
- ICP Forests Expert Panel on Crown Condition and Damage Causes (2020). Visual assessment of crown condition and damaging agents. Part IV of the Manual on methods and criteria for harmonized sampling, assessment, monitoring and analysis of the effects of air pollution on forests. UNECE ICP Forests Programme Co-ordinating Centre. https://www.icp-forests.net/manual

## Citing and licence
See `CITATION.cff`. MIT licence; cited works keep their own terms.
