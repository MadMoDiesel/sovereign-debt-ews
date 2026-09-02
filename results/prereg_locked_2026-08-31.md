# Locked before Step 3 — 2026-08-31

No model score exists yet. These choices cannot be revised after AUC.

## Labels
- Primary: E0, no wartime debt fill, 34 onsets, risk set 2,548, incidence 1.33%.
  File: `results/labels_e0.csv`, `results/onsets_e0.csv`.
- Named variant: E1 (continuation not set by excluded years).
  File: `results/labels_e1.csv`, `results/onsets_e1.csv`.
- Robustness path through the walk-forward: E1 × wartime LOCF (36 onsets,
  France 1943 dated). File: `results/labels_e1_wartime_locf.csv`.
- Written into design §3.

## Indicators
- Primary list: the original 13 (14 columns). No additions.
- Reduced robustness R1: drop `credit_gap_5y` and `d_debt_gdp_3y`
  (two thinnest on the risk set; tie at 88.7% broken by dropping the
  transform of debt/GDP, already in M1 and M2).
- Credit-gap windows {5, 7, 10}, primary 5. Columns now in
  `results/indicators.csv`.
- Written into design §4.

## Effective positives
- 22 of 34 E0 onsets have a complete vector at s−1.
- That is the sample size the fold engine must respect.
- File: `results/effective_positives.md`.
