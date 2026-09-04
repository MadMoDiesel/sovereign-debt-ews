# Can Sovereign Debt Early-Warning Dashboards Be Validated?

Repository: https://github.com/MadMoDiesel/sovereign-debt-ews  
Replication package: https://doi.org/10.5281/zenodo.22304237  
Tag: `v1.0-preprint`

Companion to the working paper:

**Michael A. Erickson**, September 2026  
Independent, Ballston Spa, NY — mxerickson.tms@gmail.com  
ORCID: [0009-0001-4669-4939](https://orcid.org/0009-0001-4669-4939)

> Advanced-economy disorderly sovereign adjustments are too rare on the
> Jordà–Schularick–Taylor panel for a multi-indicator early-warning model
> to be validated out of sample. The paper reports a declared
> walk-forward and treats the decision timeline as part of the result.

Paper: [`results/PAPER.md`](results/PAPER.md)  
Design lock: [`debt_ews_research_design.md`](debt_ews_research_design.md)

## What is in this repo

| Path | Contents |
|---|---|
| `debt_labels.py` | Mechanical D1–D4 onset labeler (E0/E1 continuation) |
| `debt_indicators.py` | Thirteen look-ahead-safe indicators |
| `debt_walkforward.py` | Expanding-window engine, confirmation gate, both fold grids |
| `test_debt_*.py` | Unit tests for labels, indicators, outcome/gate |
| `overlays/` | Reinhart–Rogoff default years and IMF-program years |
| `results/` | Locked label sets, coverage, walk-forward scores, pre-reg notes, paper |
| `data/` | Instructions only. JST microdata is not shipped |

JST is not included. See `data/README.md`.

## Reproduce

```bash
python3 -m pip install -r requirements.txt
# download JSTdatasetR6.dta into data/
python3 -m pytest test_debt_labels.py test_debt_indicators.py test_debt_walkforward.py -q
python3 run_step1.py
python3 run_step2.py
python3 run_step3.py
```

`run_step3.py` writes `results/walkforward_summary.csv` and
`results/walkforward_predictions.csv`. The drop-onset-year sensitivity is
`drop_onset_years=True` on `run_walkforward` (see `debt_walkforward.risk_set`).

## Locked numbers (do not retune)

- 34 onsets / 2,548 risk-set country-years / 1.33% incidence
- 10 onsets after 1950; 7 scoreable by the walk-forward (Table B0)
- Registered grid: 8 folds, 4 scoreable onsets, 8 lead rows
- Tiling grid: post-hoc coverage correction, 7 onsets, 21 lead rows
- Primary labels: E0, raw JST (no wartime fill)

Pre-registration notes: `results/prereg_locked_2026-08-31.md`,
`results/prereg_e0_e1.md`, `results/prereg_tiling_folds.md`.

## License

Code is MIT. JST remains under its own terms at macrohistory.net.
The working paper text in `results/PAPER.md` may be cited as Erickson (2026).
