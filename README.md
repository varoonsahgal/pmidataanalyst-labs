Student lab guides for the PMI Data Analyst Future Skills class (Project HORIZON, fictional and training-only): a start page, one page per session (WA3899 · WA3900 · WA3901 · WA3902) and a glossary.
Live at https://varoonsahgal.github.io/pmidataanalyst-labs/ (GitHub Pages serves this folder as-is; `.nojekyll` keeps Jekyll out of it).
The pages are built from `_src/pages/*.html` by `python3 _src/build.py` (art in `_src/art.py`, charts in `_src/charts.py`; needs Pillow). Every number in the guides was run against the HORIZON warehouse.
To view locally, run `python3 -m http.server 8000` in this folder and open http://localhost:8000/.
