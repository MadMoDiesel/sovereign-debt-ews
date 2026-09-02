# Research Design: Historically Calibrated Early Warning for Disorderly Sovereign Debt Adjustment

*A backtest specification. Same discipline as the CCDF walk-forward work: explicit event definitions, look-ahead gates, degrees-of-freedom accounting, and inference that survives the search. The output is calibrated probabilities ("this indicator combination historically raised 3-year disorderly-adjustment probability from X% to Y%"), not thresholds asserted from intuition.*

---

## 1. Research question

Can a small set of observable fiscal/monetary/external indicators, measured at time t using only data available at t, meaningfully shift the estimated probability of a **disorderly debt adjustment** within the following h years — out of sample, across countries, and after accounting for the indicator search?

Secondary question (the Household Resilience tie-in): conditional on stress resolving, do the same indicators predict **which resolution channel** absorbs the adjustment (inflation/repression vs. default vs. austerity vs. growth)? This is the distributional-incidence question made empirical.

---

## 2. Data

**Backbone: Jordà-Schularick-Taylor Macrohistory Database (JST).**
~18 advanced economies, annual, ~1870–present. Contains: public debt/GDP, government revenue/expenditure, long and short rates, CPI, real GDP, credit aggregates, house prices, current account, exchange rates, and — critically — dated systemic financial crisis indicators. Annual frequency is a limitation (see §8) but the only game in town at this historical depth.

**Crisis/event overlays:**
- Reinhart-Rogoff crisis dates (sovereign default external/domestic, inflation crises, currency crashes, banking crises) — for event labeling and cross-checking.
- IMF/BIS debt-service ratios and fiscal monitors for the modern subsample (post-1980), where quarterly data allows a higher-frequency robustness check.

**Coverage decision, made now, not after seeing results:** primary universe = the JST 18 (advanced economies). Emerging markets enter only as a pre-registered out-of-sample transfer test (§7.4), never in fitting. Rationale: the framework's target (US-like reserve-currency sovereigns) is closest to the advanced-economy generating process; mixing EM defaults into fitting would let Argentina-style events dominate the likelihood and produce a model calibrated for the wrong regime.

---

## 3. Event definition — the label (the part everything else depends on)

"Disorderly debt adjustment" must be defined **mechanically from data, before any indicator work**, exactly as the algorithmic bottom labels replaced hand-picked bottoms in the CCDF work. Hand-labeling crises invites the same leakage.

**A country-year t is a disorderly-adjustment ONSET if any of the following begins in t, having not been active in t−1:**

- **D1 Sovereign default/restructuring** (external or domestic), per Reinhart-Rogoff coding; or
- **D2 Inflation resolution**: CPI inflation ≥ 20% annual (RR inflation-crisis threshold) while public debt/GDP was ≥ 60% at t−1 — the debt-context gate distinguishes debt-driven inflation from pure monetary events; or
- **D3 Forced real repricing**: real long-term government bond return ≤ −15% in a single year (annual JST holding-period return deflated by CPI) while debt/GDP ≥ 60% at t−1 — captures term-premium blowouts and repression-onset that D1/D2 miss; or
- **D4 IMF-program/external rescue** (post-1945 subsample) with fiscal conditionality.

**Non-events that must NOT count:** banking crises resolved without sovereign stress (2008 US is a banking crisis, not a disorderly *sovereign* adjustment — the label must respect this or the model learns the wrong thing); currency crashes without debt context; wartime inflation with debt/GDP < 60%.

**Event windowing:** after an onset, the country is excluded from the risk set for 5 years (an ongoing adjustment can't "onset" again). This prevents one multi-year crisis from contributing many correlated positive labels.

**Continuation coding (pre-registered 2026-08-31, before any model score):**

- **E0 (primary):** `prev_fired` is updated by every raw firing, including years inside the exclusion window. This is the original `debt_labels.py` rule.
- **E1 (named variant):** excluded years do not set continuation state. The first post-window firing is a new onset. Motivated by France 1937–48: under E0, a D2 fire in 1942 (still excluded) suppresses 1943–48, so the 1940s inflation/repression spell is dated to 1937. E1 dates that spell at 1943 *if and only if* the wartime debt/GDP hole is filled with look-ahead-safe LOCF so the 60% gate can see it.

Primary confirmatory path is E0 with no debt fill. The single pre-registered robustness path is E1 × wartime LOCF. Both label sets are generated now. No further continuation rule after model scores exist. Germany 1923 is not on this axis (last observed debt 47%, below the gate).

**Sensitivity (pre-registered):** the 60% debt gate swept over {50, 60, 75}; the D3 return threshold over {−10%, −15%, −20%}; D2 inflation over {15%, 20%, 25%}. Reported as a stability table, same as (L, N, θ) in the bottom-labeling work. If the headline result only holds at one corner of this grid, it's fragile and gets said plainly.

**Expected event count (order of magnitude):** with 18 countries × ~150 years ≈ 2,700 country-years, historical base rates suggest roughly 40–80 onsets. Realized E0 count on JST R6 is 34 onsets over 2,548 risk-set years (1.33% onset-year incidence). Effective positives with a complete indicator vector at s−1: 22. That is the number that caps §5.

---

## 4. Indicators — fixed list, declared before estimation

All measured at t using only data through t. Annual data means "available at t" = available by end of year t; predictions apply to t+1…t+h.

**Fiscal core:**
1. Public debt/GDP (level)
2. Δ(debt/GDP), 3-year
3. Interest expense / government revenue (the roll-cost variable; where interest expense is missing, proxy = debt × effective rate, flagged)
4. Primary balance / GDP
5. **r − g**: effective nominal financing cost minus nominal GDP growth, 3-year trailing means (the smoothing is essential — annual r−g flips sign constantly and is mostly noise)

**Monetary/market:**
6. Long−short rate slope (term-premium proxy; true term premium doesn't exist historically)
7. Real long rate (long rate − trailing 3y inflation)
8. Inflation level and 3-year change

**External (the currency layer from the framework):**
9. Current account / GDP
10. External-funding share of sovereign debt where available; else current-account persistence as proxy
11. Real exchange-rate 3-year change

**Real-economy / household:**
12. Real wage growth, 3-year (JST has this — it's the Household Resilience hook)
13. Credit/GDP gap (private credit, 5-year trend deviation — the Schularick-Taylor banking-crisis predictor, included because banking stress is a *pathway* to sovereign stress)

**Thirteen indicators, declared now.** No additions after seeing results. Any indicator added later restarts the multiple-testing accounting from zero and gets reported as exploratory, not confirmatory.

**Reduced-indicator robustness (pre-registered 2026-08-31, before any model score):** drop the two thinnest series by risk-set coverage, `credit_gap_5y` (86.3%) and `d_debt_gdp_3y` (88.7%). The 88.7% slot is a three-way tie with `int_rev` and `primary_bal_gdp`; the 3-year debt change is the drop because it is a transform of indicator 1, already in both M1 and M2. This reduced set is a declared robustness spec, not a search. It is not permitted to pick a different drop-pair after seeing AUC.

**Credit-gap window sweep (pre-registered 2026-08-31):** trailing mean over {5, 7, 10} years. Primary is 5. The 7- and 10-year series are built now, before modeling. If skill exists only at one window, that is fragility, not a reason to switch the primary.

---

## 5. Model — deliberately boring

The realized effective-positive count (22 of 34 E0 onsets have a complete indicator vector at s−1) dictates simplicity even more than the original 40–80 planning band. Two specifications, both pre-registered:

**M1 (primary): pooled logit with country fixed effects**, h-year-ahead onset as the outcome (h = 3 primary; h = {2, 5} sensitivity). Indicators standardized within-country (a country's own history defines "elevated" — 100% debt/GDP means something different for Japan than for Australia). L1 penalty chosen by *temporal* cross-validation within the training window only.

**M2 (benchmark): the naive model** — debt/GDP level alone. M1 must beat M2 out of sample or the framework's added indicators are decoration. This is the "beats buy-and-hold" test of this domain and it is the honest bar: most early-warning papers never show their kitchen sink beats the one obvious variable.

**Explicitly excluded:** trees/boosting/NN (40 events cannot discipline them), interaction terms beyond r−g × debt-level (one pre-registered interaction, motivated by the framework's own logic), and any specification search beyond the two models above. The DOF ledger (§7.3) counts everything anyway.

---

## 6. Temporal validation — the walk-forward

Expanding-window, same architecture as the CCDF refit engine:

- **Folds (original, still primary):** train on all country-years ≤ T, predict onsets in (T, T+5], for T ∈ {1950, 1960, …, 2015}. Pre-1950 is training-only seed data (too few countries with full indicator coverage to test on). These windows do not abut: years 1956–60, 66–70, 76–80, 86–90, 96–00, 06–10 are never scored.
- **Folds (tiling coverage correction, pre-registered 2026-08-31 on coverage grounds, not performance):** T ∈ {1950, 1955, …, 2015}, test (T, T+5]. Windows abut and tile 1951–2020. Declared because discarding half the country-years has no methodological justification; declared before treating either grid's AUC as a result. Both grids are reported. The original grid is not replaced.
- **Leakage gates, enforced in the data layer, not by convention:**
  - Indicator values at t use vintage-style construction where possible; where only revised data exists (most of JST), the limitation is stated, and indicators avoid components with known heavy revision (hence ratios and multi-year changes rather than levels of real-time-sensitive series).
  - Event labels use the §3 mechanical definitions computed on data through the fold's test end — but a *training* label at year s requires the event window (s to s+h) to close by T. Same confirmed_date discipline as the bottom labels: **a 1975 training example with a 3-year horizon is only usable when T ≥ 1978.** This is the subtle leak most early-warning papers carry.
  - Standardization parameters (country means/sds) computed on training window only, frozen for the test window.
- **Output per fold:** predicted 3-year onset probabilities for each country-year in the test window, plus realized outcomes.

---

## 7. Evaluation and inference

**7.1 Discrimination:** out-of-sample AUC, M1 vs M2, pooled across folds. Also time-stratified (does skill exist post-1980, or only in the gold-standard era?) — reported either way.

**7.2 Calibration (the actual deliverable):** reliability curve of predicted vs realized frequencies, and the headline table the framework wants: for indicator-combination deciles, "baseline 3-year onset probability X%; top-decile combination Y%." If Y/X < 2 out of sample, the honest conclusion is that these indicators provide little early warning beyond debt level — and that null is publishable too.

**7.3 Multiple-testing / DOF ledger:** every choice logged — 13 indicators, 2 models, 1 interaction, 3 horizons, the event-definition grid (§3 sensitivity), the debt-gate sweep. Inference via a block bootstrap (resampling country-blocks, preserving within-country dependence) on the OOS AUC difference M1−M2, plus a White's-reality-check-style adjustment across the horizon/definition grid. The claim must survive: "the indicator set adds discrimination beyond debt/GDP, after accounting for everything we tried."

**7.4 Pre-registered transfer test:** fit on JST advanced economies, predict Reinhart-Rogoff EM episodes. Expected to degrade; the *degree* of degradation measures regime-specificity, which is itself framework-relevant (the Japan/Argentina/US distinction, quantified).

**7.5 Channel prediction (secondary):** conditional on onset, multinomial outcome {default, inflation/repression, austerity-led, growth-escape} coded from what followed each historical onset (mechanical rules: which channel moved most in the 5 post-onset years). Small-n, exploratory, labeled as such — but this is the distributional-incidence question, and even descriptive results (e.g., "external-funded sovereigns default; domestically-funded sovereigns inflate") directly feed the framework's §7 currency layer.

---

## 8. Known limitations, stated before results exist

- **Annual data, revised not vintage.** Real-time performance would be worse than measured. Say so in the paper; the modern quarterly subsample (post-1980, IMF/BIS) is the robustness check.
- **The US question is an extrapolation.** The US never appears as a positive label in the primary universe (no post-1870 US disorderly adjustment under §3's definitions — arguably 1933/1971 gold events; run with and without those codings as a named sensitivity). The model can say "US indicators resemble/don't resemble pre-onset configurations elsewhere"; it cannot assign a US-specific probability with any authority. This must be stated with the same bluntness as the CCDF paper's 3-SPX-trades caveat.
- **Reserve-currency status is one country, one era.** n=1 on the most decision-relevant regime. No dataset fixes this.
- **Survivorship:** JST's 18 are countries that stayed rich. The transfer test (§7.4) partially addresses this; it can't fully.

---

## 9. Deliverables and order of work

1. **Label pipeline** (§3) with the event-window/confirmation gates — the direct analog of `bottom_labels.py`, with the same style of unit tests proving no training label's window extends past the fold boundary.
2. **Indicator construction** from JST raw series, with per-indicator coverage maps (which country-years exist).
3. **Walk-forward engine** — adapt `walkforward_refit.py`'s fold/gate structure; the machinery carries over almost directly.
4. **Results:** discrimination, calibration table, sensitivity grids, DOF-adjusted inference, transfer test, channel analysis.
5. **Paper:** "Historically Calibrated Early Warning for Disorderly Sovereign Debt Adjustment, 1870–present." The framework document then cites *this* instead of asserting thresholds — the dashboard stops being a mood ring because its colors have measured base rates attached.

**First concrete step:** download JST (freely available, macrohistory.net), verify coverage of the 13 indicators by country-year, and run the §3 labeler to see the actual event count. Everything downstream depends on whether that number is ~40 or ~80, and it's a one-day task.

---

*The pre-registration discipline in this document is the contribution as much as any result. An early-warning model that reports its full search, its null-if-null, and its US-extrapolation limits honestly would be differentiated from most of this literature — the same way the CCDF paper's honest version beats its inflated version.*
