# DATA 608 Story 3: Do stricter gun laws reduce firearm gun deaths?

Muhammad Suffyan Khan · Fall 2026 · Professor Peter Kowalchuk

## Start here

The story is in `presentation/` and `submission/`. The notebook explains and audits the calculation. `figures/` contains the original R heat maps as both PNG and PDF. No additional data needs to be downloaded or computed to view the finished story.

| Folder | Contents |
| --- | --- |
| `data/raw/` | Preserved CDC API response, its schema metadata, and the source HTML of the GIFFORDS 2024 scorecard |
| `data/processed/` | 50-state mortality table, 50-state five-level law scale, joined analysis, group summary, and statistic summary |
| `scripts/` | Python source ingestion / validation and R heat-map generation |
| `notebooks/` | Explanatory Jupyter notebook, with reproducible checks and rendered figures |
| `figures/` | Three heat maps in PNG and PDF format |
| `presentation/` |PowerPoint story |
| `submission/` | Final slide PDF |
| `sources/` | Source URLs, definitions, citations, and methods |

## How to reproduce

1. From this folder, run `python scripts/fetch_and_prepare.py` with Python packages `pandas`, `lxml`, and `scipy`. This re-requests the CDC open-data API and 2024 GIFFORDS page and rebuilds processed CSV/JSON files. The original response is already stored, so a fresh fetch is optional and may reflect a later CDC revision.
2. Open this folder in RStudio, then run `source("scripts/create_heatmaps.R")` at the R console. This uses **base R** to regenerate the three heat maps and needs no R package installation. The package's charts were actually produced by R 4.3.3. R/RStudio is the new analysis and visualization application; prior Stories used Python/Matplotlib/Seaborn and Python/Plotly. PowerPoint is a presentation file, not the chart-generating application.
3. Open `notebooks/Story_3_Gun_Laws_Firearm_Mortality.ipynb` in VS Code or Jupyter to inspect the full explanation and saved output. The supplied PNGs and PDF work offline.

## Result in one sentence

In a descriptive comparison of 50 states, states graded A/A- for their 2024 gun laws averaged **8.4** age-adjusted firearm deaths per 100,000 in 2024, compared with **18.6** among F-graded states; the state-level association does not establish that a change in law caused a change in deaths.

## Important interpretation

The five-level scale is an **ordinal recoding of published grades**, not a survey of opinions: F = 1 (most lax), D = 2, C = 3, B = 4, A = 5 (strictest). A `+` or `-` remains in the saved raw grade and is dropped only for the five-level category. Category sizes vary: 22, 3, 5, 7, and 13 states. The CDC outcome counts all firearm-related injury deaths, including suicides; it is not a homicide-only measure. The 2024 law scorecard and 2024 mortality are contemporaneous and cannot isolate policy effects or account for other state characteristics. The GIFFORDS organization advocates gun-safety laws; use the classification with that source perspective in mind.
