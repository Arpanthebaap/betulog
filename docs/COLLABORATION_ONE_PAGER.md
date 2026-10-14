# Betulog: Collaboration One-Pager

**A Research Tool for Birch Crown-Health Surveys, Observer Calibration, and Design-Power Analysis**

---

## 1. The Problem
Birch (*Betula pendula*, *Betula pubescens*) is an increasingly vital component of northern and central European forestry. However, young plantations and mature stands frequently suffer from complex crown thinning, dieback, and mortality syndromes. Disentangling the abiotic stresses and biotic fungal/oomycete pathogens driving these declines presents three systemic field challenges:
1. **Subjective Visual Scoring:** Crown defoliation and dieback assessments vary significantly between individual observers, confounding comparisons across sites, stands, and observation years unless rigorous calibration is conducted.
2. **Disconnected Data Pipelines:** Tree-level symptom observations, crown classes, and laboratory isolate cultures/DNA accessions are routinely recorded in fragmented spreadsheets, losing the chain of custody from field tree to sequenced pathogen.
3. **Underpowered Study Designs:** Survey designs (number of plots, trees per plot) are rarely justified statistically prior to fieldwork, leading to studies underpowered to detect symptom-associated differences in defoliation.

---

## 2. What Betulog Does
**Betulog** (https://github.com/Arpanthebaap/betulog) is an open-source, offline-first field logging tool and Python research framework designed to standardise birch health surveys:
- **Field & Lab Web App (`index.html`):** Single-file browser tool that works entirely offline. Records plot metadata, tree positions ($X, Y$), stem diameter (DBH), crown parameters (defoliation, dieback, discolouration), standard ICP Forests crown classes (0–4), visible symptom flags, and directly links cultured isolates (tissue, medium, morphotype, sequence accession, status).
- **Observer Agreement & Calibration:** Automated computation of paired observer metrics: mean bias, 95% Limits of Agreement (Bland-Altman), Mean Absolute Difference, tolerance margins (5% and 10%), Intraclass Correlation Coefficient ($\text{ICC}(2,1)$), and quadratic-weighted kappa ($\kappa_w$) on crown classes.
- **Spatial Diagnostics:** Moran's $I$ with inverse-distance weighting and Monte Carlo permutation testing to diagnose whether crown damage is spatially clustered (suggesting point-source contagion) or dispersed (suggesting diffuse environmental stress).
- **Design-Power Simulation:** Simulation engine evaluating statistical power to detect symptom-associated defoliation differences across plot counts, sample sizes, and observer error levels.

---

## 3. What Is Verified (Honest Reporting)
> [!IMPORTANT]
> **Strict Verification Boundaries:**
> - **Verified:** Software codebase, data schema, 8 core Python unit tests, cross-language JavaScript-Python parity tests, and mathematical consistency of the simulation pipeline.
> - **Simulated:** Power calculations reflect a statistical simulation under explicit stated assumptions (within-plot design, assumed plot-level and tree-level variances).
> - **Not Yet Verified:** **No empirical field results exist yet and none are claimed.** Real-world variance components, field observer agreement, and diagnostic efficacy require empirical pilot validation.

---

## 4. What Data Is Needed
To ground-truth Betulog with real-world forest pathology research, we seek collaboration with research groups and monitoring programs holding or collecting:
1. **Observer Calibration Datasets:** Paired defoliation scores from two or more observers independently assessing the same set of $\ge 30$ birch trees.
2. **Operational Field Plots:** Survey data recording plot-level birch defoliation percentages, stem symptoms (cankers, sap bleeding, rot), and associated fungal/oomycete isolations.
3. **Empirical Variance Components:** Regional survey estimates of between-plot and within-plot defoliation variances to replace assumed simulation priors.

---

## 5. What We Offer
- **Free, Open Research Software:** Turnkey field application and Python package under MIT licence.
- **Customized Power & Sample-Size Analyses:** Pre-survey power calculations tailored to your specific stand configurations and research grant proposals.
- **Automated Data Pipelines:** Standardized CSV export formats, Moran's $I$ spatial analyses, and mixed-model symptom association routines.
- **Academic Partnership:** Enthusiastic, transparent collaboration adhering to institutional data policies, with co-authorship or formal acknowledgment on joint publications.

---

## 6. Email Template to a Forest Pathology Researcher

> **Status:** TEMPLATE ONLY — ADAPT AND REVIEW BEFORE SENDING

**Subject:** Inquiry regarding birch survey plot design & observer agreement in [Target Region / Study]

Dear Dr. [Researcher's Last Name],

I recently read your paper on [Title or Topic of their Paper, e.g., birch crown dieback / fungal pathogens in Betula stands] and found your findings regarding [mention one specific finding, e.g., the prevalence of Marssonina / Phytophthora across different stand ages] very illuminating.

I am an independent researcher developing an open-source survey framework and study-design tool for birch health monitoring called **Betulog** (https://github.com/Arpanthebaap/betulog). Our framework integrates offline ICP Forests crown condition scoring, direct tree-to-isolate tracking, and simulation-based power analysis to help researchers determine adequate plot numbers before fieldwork.

I would value your insight on one specific question regarding your survey design:

> **When assessing crown defoliation and stem lesions across your plots, did your team observe significant between-observer variation or spatial clustering within plots, and how did that inform the number of plots you chose to sample?**

We are currently validating our power simulation models using empirical variance data from active research groups. If you have any paired observer calibration scores or pilot plot data that could benefit from automated agreement statistics ($\text{ICC}(2,1)$, quadratic weighted kappa) or spatial autocorrelation testing, I would be delighted to collaborate and assist with the quantitative analysis.

Thank you very much for your time and research contributions.

Sincerely,

**Arpan Ghosh**  
Independent Researcher  
GitHub: [@Arpanthebaap](https://github.com/Arpanthebaap)  
Project Repository: https://github.com/Arpanthebaap/betulog  
Web App: https://arpanthebaap.github.io/betulog/
