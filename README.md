# Betulog

A browser-based field and lab log for birch health surveys. Score crowns in the ICP Forests defoliation classes, record stem and root symptoms, map affected trees, and link every tree to the fungal isolates taken from it.

> **Status: research prototype (v0.1.0).** It has not yet been tested in the field. It records and summarises observations; it does **not** diagnose disease. Identification of causal agents requires culture and DNA sequencing.

## Why
Birch is increasingly used in Swedish forestry, but young plantations suffer browsing, insects, pathogens and abiotic stress, and older stands show a decline syndrome whose causes are unresolved. Untangling interacting causes needs consistent scoring, symptom records and a clean link from each tree to its isolates and sequences. Betulog keeps those linked from the first plot visit.

## Features
- Plot and tree records: defoliation, dieback and discolouration percentages, DBH, X/Y position, optional GPS note
- Automatic ICP Forests class per tree: 0 none (0-10%), 1 slight (11-25%), 2 moderate (26-60%), 3 severe (61-99%), 4 dead
- Symptom flags: stem lesion or canker, sap bleeding, fruiting bodies, bark cracks, insect damage, browsing, root-collar rot, dead
- Isolate log tied to tree IDs: tissue, date, medium, morphotype, sequence accession, status from plated to identified
- Plot summary: class distribution, mortality, tree map coloured by class, mean defoliation with and without each symptom
- Sampling prompts for common symptoms (prompts, not diagnoses)
- CSV export for trees and isolates; data never leaves the browser
- Works offline once loaded; no account, server or API key

## Quick start
Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

Hosting: push to GitHub, then Settings > Pages > Source: GitHub Actions. The included workflow publishes the site on every push to `main`.

## Data
Everything is stored in your browser's localStorage, per device and browser. **Export CSVs after each field day**; clearing browser data deletes the log. Column meanings are in [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md). Example files in `data/` are **synthetic** and exist only to show the format.

Quick descriptive summary of an export:

```bash
pip install pandas
python3 analysis/summarise.py data/example_trees.csv
```

For inference, model defoliation or class against symptoms with plot (and site) as random effects in R or Python.

## Field method
See [docs/FIELD_PROTOCOL.md](docs/FIELD_PROTOCOL.md) for a suggested protocol covering plot layout, crown scoring, observer calibration, sampling for isolation and chain of custody.

## Limitations
- Crown scoring is visual and differs between observers; calibrate and report it
- Transparency depends on season and leaf flush; record assessment dates
- Sampling prompts come from general forest-pathology knowledge and have not been reviewed by a specialist; verify against the literature
- localStorage is not a database: no sync, no multi-user editing, no backups
- No tests for the web app yet; only the example script was run

## Roadmap
1. Field test on real plots and refine fields with forest pathologists
2. Photo attachments per tree and per lesion
3. Export in a format ready for GenBank and common mixed-model workflows
4. Optional sync to a shared database for teams
5. Crown photo analysis (see the sister project [Leyloom](https://github.com/Arpanthebaap/leyloom) for the rule-based starting point)

## Repository layout
```
index.html                  the app (HTML, CSS, JS in one file)
data/                       synthetic example CSVs
analysis/summarise.py       descriptive summary of an export
docs/FIELD_PROTOCOL.md      suggested field and lab protocol
docs/DATA_DICTIONARY.md     every exported column
.github/                    Pages workflow, issue templates
CITATION.cff, LICENSE       citation and MIT licence
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Feedback from forest pathologists is especially welcome.

## Citation
See [CITATION.cff](CITATION.cff).

## License
MIT. See [LICENSE](LICENSE).
