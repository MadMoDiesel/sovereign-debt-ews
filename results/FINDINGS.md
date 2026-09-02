# Findings: Historically Calibrated Early Warning for Disorderly Sovereign Debt Adjustment

JST Macrohistory Database R6, 18 advanced economies, 1870–2020.
Primary label set E0, no wartime debt fill. Horizon h = 3.
Walk-forward declared in the research design, run as written, then
re-run under a pre-registered coverage correction that tiles test
windows. No specification was chosen after seeing an AUC.

---

## 1. Headline

Advanced-economy disorderly sovereign adjustments are too rare in the
post-1950 JST panel to support out-of-sample validation of a
multi-indicator early-warning model.

That is not a failed backtest. It is the result the declared test
produced. The kitchen sink does not lose to debt/GDP; the comparison
is not identified. Dashboards that color US-like sovereigns from a
vector of fiscal, monetary, and external gauges, without a measured
base rate and without an out-of-sample event count, are making a
claim this panel cannot support.

---

## 2. What was held fixed

Event rules, the 13-indicator list, M1 vs M2, the confirmation gate
(`labels_usable_at`), and the original fold grid were declared before
any model score. After labels and indicators existed, and still before
treating AUC as a result, three further choices were locked:

- Continuation coding E0 (primary) vs E1 (excluded years do not set
  continuation state).
- Reduced-indicator robustness R1: drop `credit_gap_5y` and
  `d_debt_gdp_3y`.
- Credit-gap windows {5, 7, 10}, primary 5.
- Tiling fold grid as a *coverage* correction, not a performance
  correction. Original grid remains primary. Both are reported.

Germany 1923 was left as a non-event. Last observed debt/GDP (1913)
is 47%, below the 60% gate. Filling 1920–26 would be a new series.

---

## 3. Labels and base rate

At the default gates (inflation ≥ 20%, debt/GDP ≥ 60%, real bond
total return ≤ −15%, 5-year exclusion), E0 produces **34 onsets**
over **2,548 risk-set country-years**.

Onset-year incidence: **34 / 2,548 = 1.33%**.

That is the incidence of onset *years*, not the 3-year-ahead
probability a model predicts. The model outcome is “onset in (s, s+h]”.
Calibration, if it is ever identified, has to use that h-year
frequency inside each test window.

The pre-registered threshold sweep stays inside 19–58 onsets. 34 is
below the 40–80 planning band and inside the viable range that was
used as a go.

Post-1950 onsets on the primary list — the events the walk-forward
can actually test — are eight:

Ireland 1981 D2, Ireland 2010 D4, Italy 1974 D4, Portugal 1977 D4,
Portugal 1983 D4, Portugal 2011 D3+D4, Spain 1978 D4, UK 1973 D3.

The rest sit in the training-only seed.

E1 on raw JST is identical to E0 (34). E1 combined with look-ahead-safe
wartime debt LOCF re-dates France (1914, 1920, 1926, 1937, 1943 instead
of 1914, 1924, 1937) and raises the count to 36. That crossed cell is
the named robustness path, not the primary.

---

## 4. Effective positives

A complete 14-column indicator vector at s−1 exists for **22 of 34**
E0 onsets. Ten events contribute no usable pre-onset row under
complete-case features (Belgium 1923, Finland 1945, Germany 1948,
Japan 1942, Portugal 1873/1916/1922, Spain 1873/1882/1947).

22 positives versus 13 indicators plus country fixed effects is the
sample the fold engine had to respect. L1 is load-bearing by
construction. Adding interactions beyond the one declared r−g × debt
term is not supportable.

---

## 5. Walk-forward

Outcome: y = 1 iff an onset occurs in (s, s+3]. The contemporaneous
onset year is a negative for the forward outcome. Training rows enter
only through `labels_usable_at`. Within-country z-scores are fit on
train and frozen for test.

### Original declared grid (primary)

T ∈ {1950, 1960, …, 2015}, test (T, T+5]. Windows do not abut. Years
1956–60, 66–70, 76–80, 86–90, 96–00, 06–10 are never scored.

One live test window: 1971–75, **8 positives**.

Pooled closed OOS, 8 events:

| spec | model | n | pos | AUC | Brier |
|---|---|---:|---:|---:|---:|
| full | M1 | 572 | 8 | 0.31 | 0.037 |
| full | M2 | 607 | 8 | 0.56 | 0.018 |
| R1 | M1 | 583 | 8 | 0.45 | 0.022 |
| R1 | M2 | 618 | 8 | 0.58 | 0.017 |

With 8 events the standard error on an AUC is on the order of ±0.20.
These numbers are indistinguishable from each other and from 0.50.
The original grid cannot tell.

### Tiling coverage correction

T ∈ {1950, 1955, …, 2015}, test (T, T+5]. Windows abut and tile
1951–2020. Locked as a coverage argument: discarding half the
country-years had no methodological justification, including the
lead years on Ireland 2010 and Portugal 2011.

Four live windows, **21 positives**:

| test | pos | M1 AUC | M2 AUC |
|---|---:|---:|---:|
| 1966–70 | 1 | 0.48 | 0.82 |
| 1971–75 | 8 | 0.59 | 0.80 |
| 1976–80 | 6 | 0.55 | 0.50 |
| 2006–10 | 6 | 0.69 | 0.77 |

Pooled closed OOS, 21 events:

| spec | model | n | pos | AUC | Brier |
|---|---|---:|---:|---:|---:|
| full | M1 | 1053 | 21 | 0.44 | 0.038 |
| full | M2 | 1118 | 21 | 0.59 | 0.024 |
| R1 | M1 | 1066 | 21 | 0.59 | 0.026 |
| R1 | M2 | 1131 | 21 | 0.61 | 0.022 |

Tiling fixed coverage. It did not manufacture power. Four windows,
most with 1–6 events, still cannot discriminate 13 indicators from 1.
Point estimates move across windows; pooled differences are smaller
than any honest standard error.

---

## 6. What is not a finding

- “M1 fails to beat M2.” Not identified.
- “M1 beats M2 on R1 under tiling.” Also not identified, and would be
  the wrong sentence even if the SEs were small, because the drop-pair
  and the tiling grid were robustness items, not a search.
- “France 1945–48 should be back-dated to 1937.” That is E0’s
  continuation rule meeting a missing-debt hole. E1 × wartime LOCF
  dates it to 1943. Both were locked before modeling. Relative
  performance across those two label sets is not identified either,
  for the same reason: too few post-1950 events.
- Widening the test window after seeing sparsity, switching the
  outcome to “onset at s,” or adding indicators after seeing AUC.

---

## 7. What would be a different study

Three routes buy events. Each changes the claim.

- Fit on an emerging-market transfer set. Different regime.
- Horizon h = 5. More positives per window, a weaker statement about
  timing.
- Test in the pre-1950 era, where events are dense. The seed-only
  decision was made because indicator coverage is thin there.

Picking whichever later produces a prettier AUC is the thing this
design was built not to do.

---

## 8. What this is worth

The literature this project sits next to routinely publishes
dashboards and in-sample associations as if they were early-warning
systems. The honest test, on the panel those dashboards implicitly
claim, cannot validate a multi-indicator model out of sample. That
sentence is the contribution. It is narrower than a working EWS and
stronger than a kitchen-sink coefficient table.

The machinery is reusable on any panel that actually has events:
same gates, same confirmation rule, same two-grid report. The
advanced-economy post-1950 JST slice is not that panel.

---

## Files

| | |
|---|---|
| Design | `debt_ews_research_design.md` |
| Labels | `results/labels_e0.csv`, `labels_e1.csv`, `onsets_e0.csv` |
| Indicators | `results/indicators.csv` |
| Effective positives | `results/effective_positives.md` |
| Walk-forward | `results/walkforward_summary.csv`, `walkforward_predictions.csv` |
| Locks | `results/prereg_locked_2026-08-31.md`, `prereg_e0_e1.md`, `prereg_tiling_folds.md` |
| Step memos | `results/step1_results.md`, `step2_coverage.md`, `step3_results.md` |
