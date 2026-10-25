# DATA 608 — Story 4: How Much Do We Get Paid?
**Muhammad Suffyan Khan | Fall 2026 | Due October 25, 2026**

## Start here
- Presentation: `submission/Muhammad_Suffyan_Khan_DATA608_Story4.pdf`
- Editable slides: `presentation/Muhammad_Suffyan_Khan_DATA608_Story4.pptx`
- Methods, sources, visual choices: `submission/Story4_Methods_and_Visual_Choices.pdf`
- Code notebook: `notebooks/Story4_Salary_Analysis.ipynb`
- Python pipeline: `scripts/build_all_story4_files.py`
- Figures: `figures/` (PNG, interactive HTML) and `presentation/slide_pngs/`
- Source documentation: `sources/SOURCES.md`
- AI-use statement: `AI_USE_DISCLOSURE.md`
- File inventory: `FILE_MANIFEST.csv`

## Story and design choices
The story compares the variation of **annual mean pay across six BLS occupational categories and U.S. jurisdictions**. 
1. Role ranking: compares occupational annual mean wage across **16 selected states, equally weighted** (not a national mean).
2. Role × state heatmap: compares six roles simultaneously across those same selected states.
3. Geographic extremes: highlights the highest and lowest reported Data Scientist salary jurisdictions in a 49-jurisdiction source.
4. Within-state role difference: compares Data Scientists vs Computer Systems Analysts to reveal whether the salary gap changes by state.
5. Dedicated concluding slide summarizes takeaways and limitations, following professor feedback on Story 3.

## Reproduction
Use Python 3.10+ and install `pandas numpy matplotlib plotly python-pptx reportlab nbformat`.
Start Jupyter at this project root and run `notebooks/Story4_Salary_Analysis.ipynb`.
Run `python scripts/build_all_story4_files.py` from the root to regenerate the primary presentation and figures. The PDF export was generated from the slide deck; update that export if slides are regenerated. 

## Data provenance / honest limits
The official statistical program is BLS OEWS May 2025. The provided figures were transcribed from **third-party BLS-attributed wage tables** (linked in `sources/SOURCES.md`), not directly verified against downloaded official BLS bulk files. No official raw input is included; `data/raw/` documents that limitation.

Six-role comparisons cover **16 selected states**; only Data Scientists have a 49-jurisdiction state profile. These analyses are not a complete 50-state × six-role census. One wage is missing rather than imputed. Wages are nominal and not cost-of-living adjusted. Informal data-practitioner titles cannot map precisely to SOC codes. The selected-state average is not the BLS national occupational mean.

