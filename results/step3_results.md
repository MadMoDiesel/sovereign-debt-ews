# Step 3 — walk-forward, original grid and tiling coverage grid

Engine tests: 3/3. Training labels enter only through `labels_usable_at`.
Both fold grids are reported. Neither is chosen for its AUC.

## The writeable sentence

The declared walk-forward yields only one test window containing events
(8 positives), which is insufficient to discriminate between
specifications; no conclusion about relative model performance is
identified.

The tiling coverage correction (below) raises that to four windows and
21 positives. That is still insufficient to discriminate 13 indicators
from 1. The project result is sparsity, not a kitchen-sink-lost claim.

## Original §6 grid (primary declared design)

T ∈ {1950, 1960, …, 2015}, test (T, T+5]. Windows do not abut.

Live folds (test positives > 0), E0 full:

| test | pos | M1 AUC | M2 AUC |
|---|---:|---:|---:|
| 1971–75 | 8 | 0.59 | 0.80 |

Pooled closed OOS, 8 positives:

| spec | model | n | pos | AUC | Brier |
|---|---|---:|---:|---:|---:|
| full | M1 | 572 | 8 | 0.31 | 0.037 |
| full | M2 | 607 | 8 | 0.56 | 0.018 |
| R1 | M1 | 583 | 8 | 0.45 | 0.022 |
| R1 | M2 | 618 | 8 | 0.58 | 0.017 |

With n=8 events the SE on an AUC is on the order of ±0.20. 0.31 and
0.56 are indistinguishable from each other and from 0.50. The original
grid cannot tell.

## Tiling coverage correction (pre-registered 2026-08-31)

Rationale is coverage, not performance: the original grid discarded
half the post-1950 years by construction (1956–60, 66–70, 76–80, 86–90,
96–00, 06–10), including the lead years on Ireland 2010 and Portugal
2011. T ∈ {1950, 1955, …, 2015} makes test windows abut and tile
1951–2020. Written into §6 before treating either grid's AUC as a
result. File: `prereg_tiling_folds.md`.

Live folds, E0 full:

| test | pos | M1 AUC | M2 AUC |
|---|---:|---:|---:|
| 1966–70 | 1 | 0.48 | 0.82 |
| 1971–75 | 8 | 0.59 | 0.80 |
| 1976–80 | 6 | 0.55 | 0.50 |
| 2006–10 | 6 | 0.69 | 0.77 |

Four windows. Most have 1–6 events. The 2006–10 window is the GFC-era
leads the original grid threw away.

Pooled closed OOS, 21 positives:

| spec | model | n | pos | AUC | Brier |
|---|---|---:|---:|---:|---:|
| full | M1 | 1053 | 21 | 0.44 | 0.038 |
| full | M2 | 1118 | 21 | 0.59 | 0.024 |
| R1 | M1 | 1066 | 21 | 0.59 | 0.026 |
| R1 | M2 | 1131 | 21 | 0.61 | 0.022 |

21 events still cannot support a 13-vs-1 comparison. Point estimates
wobble across windows; pooled differences are smaller than any honest
standard error. Tiling fixed coverage. It did not manufacture power.

## What this project can support

Advanced-economy disorderly sovereign adjustments are too rare in the
post-1950 JST panel to support out-of-sample validation of a
multi-indicator early-warning model. That is a result arrived at by
running the declared test, not by assertion.

It is also the claim that indicts the dashboard genre, including any
framework document that colors US-like sovereigns from a kitchen sink
of fiscal/monetary/external gauges without a measured base rate.

Options that would buy power (EM as a fitting universe, h=5, pre-1950
as a test era) are different studies. They are not a rescue of this
one. Picking whichever later produces a prettier AUC is the thing this
design was built not to do.

Files: `walkforward_summary.csv`, `walkforward_predictions.csv`.
