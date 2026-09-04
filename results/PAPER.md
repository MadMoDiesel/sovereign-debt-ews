# Can Sovereign Debt Early-Warning Dashboards Be Validated? Evidence from a Declared Walk-Forward

Michael A. Erickson  
Independent  
Ballston Spa, NY  
mxerickson.tms@gmail.com

September 2026  
Working paper. Comments welcome.

Companion code and locked result files: https://github.com/MadMoDiesel/sovereign-debt-ews

JEL: C52, C53, E62, F34, G01, H63  
Keywords: early warning, sovereign debt, walk-forward validation, declared design, rare events, Jordà–Schularick–Taylor

---

## Abstract

Sovereign debt "dashboards" — indicator panels that color a country's fiscal position green, yellow, or red — implicitly claim that combinations of fiscal, monetary, and external gauges provide early warning of disorderly debt adjustment. We test whether that claim can be validated on the evidence base it invokes: the long-run advanced-economy panel. Using the Jordà–Schularick–Taylor Macrohistory Database, Release 6 (18 countries, 1870–2020; Jordà, Schularick, and Taylor 2017), we define disorderly-adjustment onsets mechanically from declared rules, construct thirteen declared indicators under an enforced look-ahead gate, and run an expanding-window walk-forward comparing a multi-indicator model against debt/GDP alone. The design identifies 34 onsets over 2,548 risk-set country-years (1.33% annual incidence), of which ten fall after 1950. The walk-forward can score seven of those ten: the declared eight-fold grid sees four onsets (eight lead rows in one window); a post-hoc tiling of test windows, reported alongside the declared grid, sees seven onsets (21 lead rows in four windows). Two onsets are invisible by construction — a repeat six years after a prior onset has every three-year lead row inside the previous exclusion window — and one sits in a fold-boundary gap. A 0.10 AUC gap would want about 45–110 independent positives (Hanley and McNeil 1982; 80% power, two-sided 5%, score correlation 0.3–0.7); the post-1950 record contains ten. Advanced-economy disorderly adjustments are too rare for multi-indicator early-warning claims to be validated out of sample on the panel such dashboards implicitly cite. The decision timeline — what was locked, when, and what was refused after results were visible — is a central exhibit, because the finding is only as strong as the discipline that produced it.

---

## 1. Introduction

A familiar genre of fiscal-risk analysis presents a dashboard: debt-to-GDP, debt service relative to revenue, the gap between interest rates and growth, the term premium, real wage growth, external funding dependence, each colored by zone, with the composite offered as a read on how close a sovereign stands to disorderly adjustment. The genre spans official-sector surveillance, market research, and policy frameworks. Its implicit empirical claim is that these indicator combinations have historically preceded disorderly adjustments often enough, and cleanly enough, to warn.

This paper asks a prior question: can that claim be validated at all on the relevant evidence? Not "do the indicators correlate with crises in-sample" — the literature contains many such associations — but the operational question a dashboard user actually needs answered: measured at time *t* with only information available at *t*, do these indicators improve out-of-sample discrimination of subsequent disorderly adjustment, relative to the single variable everyone already watches?

The answer we find is that on the advanced-economy long panel, the question cannot be answered — and that this is informative. The events are too rare. Thirty-four onsets in 150 years of 18-country history, ten of them after 1950, is not a sample against which thirteen indicators can be discriminated from one. The dashboards are not under-validated by accident or by want of effort; on the panel they implicitly cite, they are not validatable out of sample.

Three features distinguish this exercise from the adjacent literature. First, events are defined mechanically from rules declared before any indicator was constructed, eliminating the discretion in hand-labeled crisis chronologies. Second, a confirmation gate — enforced in the data layer and unit-tested — prevents the subtle leak that a training label whose outcome window has not yet closed carries information from the future; the gate applies to negative labels as well as positive ones, a leak most early-warning studies carry silently. Third, and centrally, the sequence of analytic decisions was locked in a declared order, and the paper reports that timeline as an exhibit (Section 5), including the decisions refused after results were visible. A null result is only worth reporting if the reader can verify it was not one specification choice away from a positive; the timeline is that verification.

The contribution is therefore twofold: a specific empirical finding — the advanced-economy panel cannot support out-of-sample validation of multi-indicator sovereign early warning — and a demonstration of a dated decision timeline that licenses stating a null that way.

## 2. Relation to existing work

Three strands are adjacent. The early-warning-system literature descending from Kaminsky, Lizondo and Reinhart's (1998) signals approach and Frankel and Rose's (1996) emerging-market crash probit established indicator-crisis associations, largely for currency and default events, and largely in-sample or with limited temporal holdout. The fiscal-sustainability literature centered on r−g dynamics (Blanchard 2019) supplies the theoretical case for several of our indicators without claiming predictive validation of a composite dashboard. The macrohistory strand built on Jordà, Schularick and Taylor's database has produced robust in-sample results — notably that credit growth predicts financial crises (Schularick and Taylor 2012; Jordà, Schularick and Taylor 2017) — under designs that are predictive in form but rarely confront the sovereign-adjustment event class in advanced economies, for the reason this paper quantifies: there is almost nothing to predict.

We do not claim these literatures are wrong. We claim that the specific composite promise of the dashboard genre — multi-indicator early warning for advanced, US-like sovereigns — rests on an evidence base that cannot support it, and that this can be shown rather than asserted.

## 3. Data and event definition

**Panel.** The Jordà–Schularick–Taylor Macrohistory Database, Release 6 (Jordà, Schularick, and Taylor 2017): 18 advanced economies, annual, 1870–2020, providing public debt/GDP, revenue and expenditure, short and long interest rates, CPI, nominal and real GDP, credit aggregates, current account, exchange rates, and wages. Government bond total returns used in the D3 rule come from the same release and are cited separately per the database terms of use (Jordà, Knoll, Kuvshinov, Schularick, and Taylor 2019). Emerging markets are excluded from fitting by a decision made at design time: the dashboard genre's implicit subject is the advanced sovereign, and mixing regimes with different distress thresholds would calibrate the model to the wrong generating process.

**Event rules.** A country-year *t* is a disorderly-adjustment onset if any of four conditions begins at *t*, having not fired at *t−1*, outside a five-year post-onset exclusion window: (D1) sovereign default or restructuring per the Reinhart-Rogoff chronology; (D2) CPI inflation of at least 20% with debt/GDP of at least 60% at *t−1*; (D3) real government bond total return of −15% or worse with the same debt gate; (D4) an IMF program with fiscal conditionality, post-1945. The debt gate implements a non-event rule stated in advance: inflation or bond losses without debt context — wartime inflation in a low-debt country, a pure monetary event — must not count. Banking crises resolved without sovereign stress do not count; the 2008 United States is a banking crisis, not a disorderly sovereign adjustment, and a labeler that conflates them learns the wrong object. Exclusion-window years are removed from the risk set entirely rather than treated as clean negatives.

Threshold sensitivity was declared as a grid (inflation {15, 20, 25}%; debt gate {50, 60, 75}%; real return {−10, −15, −20}%). Onset counts across the 27 cells range from 19 to 58, with 34 at the declared defaults (Table B2).

**The resulting sample.** Thirty-four onsets over 2,548 risk-set country-years: an annual incidence of 1.33% (Table B1). Ten onsets fall after 1950: Netherlands 1951 and 1957 (D3), United Kingdom 1973 (D3), Italy 1974 (D4), Portugal 1977, 1983 and 2011 (D4 / D4 / D3+D4), Spain 1978 (D4), Ireland 1981 (D2) and 2010 (D4). Table B0 maps each of those ten to its three lead years. Seven are scoreable under tiling (UK 1973, Italy 1974, Portugal 1977, Spain 1978, Ireland 1981, Ireland 2010, Portugal 2011). Two are structurally unscoreable: Portugal 1983 and Netherlands 1957 fall six years after a prior onset in the same country, so every lead year s ∈ {t−1, t−2, t−3} sits inside the previous five-year exclusion window. Netherlands 1951 has one complete-case lead year (1950) that is neither trainable under the T=1950 confirmation gate nor inside any test window. The declared grid scores four of the seven (eight lead rows). The numbers that bind the paper are 1.33%, ten post-1950 onsets, and seven that a walk-forward can see.

**Named sensitivities on the label set.** Two were run and locked before any model score was treated as a result. A look-ahead-safe wartime gap fill (last-observation-carried-forward through the 1914–23 and 1939–49 holes) moved zero onsets under the primary continuation rule (Table B5): the French 1940s inflation adjustment is already dated to its 1937 onset by the exclusion-and-continuation logic, and Germany 1923 fails the debt gate on the last observed (1913) ratio of 47% — the design's own non-event rule applied to the data that exist, since no 1920–26 German debt series is observed and inventing one would not be a fill. An alternative continuation coding (E1), under which an excluded year's rule-firing does not suppress a post-window onset — the coding under which France 1943 would date as a second onset — was also locked; on raw JST it produces a label set identical to the primary, and re-dates France only in combination with the wartime fill (France 1914, 1920, 1926, 1937, 1943 in place of 1914, 1924, 1937; net +2), a cell reported as a robustness path.

## 4. Indicators

Thirteen indicators were declared before estimation and none added after: public debt/GDP and its three-year change; interest expense over revenue; the primary balance; r−g as three-year trailing means; the long−short slope; the real long rate; inflation level and three-year change; current account/GDP and its three-year persistence; three-year real exchange-rate change; three-year real wage growth; and a credit/GDP gap against a trailing five-year mean. All use trailing windows only, and a unit test verifies that perturbing year *t+1* leaves every indicator value at *t* unchanged.

Two construction caveats are material and disclosed rather than buried. JST contains no interest-expense series, so debt service over revenue is a proxy — debt × long rate over revenue — which is a transform of variables already in the set and is therefore partly collinear with the univariate benchmark; the primary balance inherits the same proxy. Nominal GDP growth for r−g is constructed as real growth compounded with inflation rather than from the nominal GDP series, whose wartime currency rebasements would otherwise poison the panel's most important variable. The credit gap uses a trailing mean rather than the two-sided HP filter common in this literature, which embeds look-ahead.

Complete-case coverage is 72.2% of country-years and is not random: it thins precisely in wars and the early period, where events concentrate (Table B3). A reduced eleven-indicator specification (R1, dropping the two thinnest series on the risk set, `credit_gap_5y` and `d_debt_gdp_3y`) was declared as the corresponding robustness check. Credit-gap windows {5, 7, 10} were built at the same time; the primary remains 5.

## 5. The decision timeline

This section is the paper's central exhibit. The claim "the comparison is not identified" is only credible if the reader can verify that the design was not adjusted toward that conclusion — or away from it — after results were visible. The timeline separates decisions into three phases by what was known when each was locked.

**Phase 1 — locked before any label or indicator existed.** The event rules D1–D4 with their thresholds and sensitivity grids; the debt-context gate and its named non-events; the five-year exclusion window; the thirteen-indicator list; the two model specifications (M1, an L1-penalized logit with country fixed effects and one declared r−g × debt interaction; M2, debt/GDP with country fixed effects); the outcome (onset within three years); the fold grid (eight expanding windows with T ∈ {1950, 1960, …, 2010, 2015}, testing (T, T+5]); pre-1950 as training-only seed; the confirmation gate as the sole door for training labels; within-country standardization fit on training data and frozen for test.

**Phase 2 — locked after labels and indicators existed, before any model was fit.** The E0/E1 continuation codings, prompted by inspection of the France 1937–48 spell during the wartime sensitivity. The R1 reduced-indicator specification and the credit-gap window sweep {5, 7, 10}, prompted by the coverage maps.

**Post-hoc coverage correction, not a Phase-2 lock.** After the original eight-fold grid had been run and its AUCs seen, test windows were re-cut so that T steps of five years tile 1951–2020. The rationale is coverage: the declared grid discards half the post-1950 years by construction, including the lead years on Ireland 2010 and Portugal 2011. That rationale does not depend on the AUCs, but “not treated as informative” is unverifiable. The tiling grid is reported alongside the declared grid. It is not a replacement, and it was not locked before scores existed.

**Post-hoc onset-year drop, run and declined.** After all declared scores were visible, and prompted by review, onset years were removed from the risk set (Bussière and Fratzscher 2006). The change flattered M1 (live-window 0.59 → 0.64) and was not adopted. Primary results keep onset years in. Un-run refusals are a claim; a run that helped the multi-indicator model and was declined is evidence.

No OSF or AEA registry entry exists. The ordering of decisions is documented in `debt_ews_research_design.md` and in the dated notes under `results/`. It is not independently timestamped commit-by-commit: the public repository was snapshotted after the analysis. The first third-party timestamps will be the preprint submission and any later archive deposit.

**Phase 3 — refused after results were visible.** Widening test windows further; switching the outcome to onset-at-*s*; adding indicators; selecting between E0 and E1, or between the original and tiling grids, on the basis of which produced a better score; treating any sub-comparison that favored the multi-indicator model as a finding; adopting the onset-year drop after it raised M1.

## 6. Walk-forward design

The engine is an expanding-window walk-forward. For each fold with training boundary T, training rows enter only through the confirmation gate: a country-year *s* with horizon *h* = 3 is usable only if *s* + 3 ≤ T, for negatives as well as positives, since "no onset within three years of *s*" is exactly as unknowable at *s* + 1 as its complement. Standardization parameters are fit within the training window and frozen. M1 and M2 are estimated per fold; predictions are scored on the test window; results are pooled across folds. Unit tests verify the forward outcome construction, the training-label door, and the blocking of unclosed windows.

The outcome is forward: y = 1 iff an onset occurs in (*s*, *s*+3]. Combined with a five-year exclusion window, a repeat onset at t+6 has every lead row inside the previous exclusion window and contributes zero positives by construction (Portugal 1983, Netherlands 1957; before 1950, Portugal 1922).

The onset year itself is a mechanical negative: t+1…t+5 are excluded, so y(t)=0 while inflation and real returns are at their sample extremes. Those rows stay in the primary risk set because that is what was declared. The post-hoc drop described in Section 5 was run after scores were visible, flattered M1, and was not adopted (Appendix B4).

M1 requires the full indicator vector; M2 requires only debt/GDP. Reported horse-race numbers below are restricted to the intersection — the M1 complete-case rows — so the two models are scored on the same country-years.

## 7. Results

The result is a counting argument.

Ten onsets fall after 1950. Table B0 shows what the walk-forward can see. Seven produce any complete-case lead row outside an exclusion window. Those seven contribute 21 tiling test positives — three near-duplicate lead years each, not 21 independent events — in two waves (1970s European inflation/IMF; 2010–11 periphery). The declared grid, eight folds, scores four of the seven (eight lead rows) in a single window. Hanley and McNeil (1982) standard error on an AUC near 0.6 is about 0.15 with four independent positives (the live window) and about 0.11 with seven (tiling, treating each onset as one draw) and ~1,000 negatives. Detecting a 0.10 gap between two paired models at 80% power, two-sided 5%, wants about 45–110 independent positives as the score correlation ranges from 0.7 to 0.3 (`power_n.py` in the repository); a 0.05 gap wants several hundred. The post-1950 advanced-economy record contains ten onsets. That bound does not depend on M1 or M2. It binds every study on this panel.

Fold-level AUCs are descriptive (Table B4). On the common-row set, declared grid, pooled M1 is 0.31 and M2 is 0.59; in the one live window (four onsets, eight lead rows) they are 0.59 and 0.83. Under tiling, pooled 0.44 versus 0.61 on the same common rows. Per-window signs flip.

Dropping onset years from train and test moves live-window M1 from 0.59 to 0.64 and tiling pooled M1 from 0.44 to 0.48; M2 on the same rows is 0.83 before the drop and 0.84 after it. Removing k negatives from a test set of N negatives can shift AUC by at most AUC·k/(N−k). The 1971–75 window has two onset-year rows among ~74 common-row negatives (bound ≈ 0.02); tiling pooled has ten among ~1,030 (bound ≈ 0.004). Holding the declared fit and dropping those rows only at evaluation moves live-window M1 by 0.01. The remaining lift is in M1's fitted coefficients — the same fragility as R1 (0.59 → 0.85 from dropping two indicators). It is not a bias correction that creates power. Primary results keep the declared risk set.

**What is identified.** Incidence 1.33%; ten post-1950 onsets; seven scoreable; threshold-sweep counts 19–58. Properties of the panel.

**What is not identified.** That M1 fails to beat M2, or beats it. That either continuation coding is preferable. Any result under a wider window, a contemporaneous outcome, or more indicators.

## 8. Interpretation: rarity as the finding

It is tempting to read this as a study that failed for want of data, remediable by more collection. The opposite reading is correct. The panel is the longest, most carefully constructed record of advanced-economy macro-finance in existence; the event class is rare *in the world*, not merely in the dataset. An annual onset incidence of 1.33% — concentrated, moreover, in two interwar and one 1970s cluster plus a GFC-periphery pair, waves rather than independent draws — is the actual historical frequency of the thing dashboards claim to warn of. No feasible extension of the advanced-economy record changes it.

One row in Table B1 is worth naming in this light. The United States appears once, in 1947, as a D3 onset: debt at 108% of GDP, CPI inflation 14.4%, nominal bond total return −2.9%, real bond return −15.1% — just through the gate. There is no default, no IMF program, and no crisis narrative. Bondholders absorbed the adjustment through a year of inflation and negative real returns, the financial-repression resolution documented by Reinhart and Sbrancia (2015). The labeler is doing what it was written to do: dating an orderly liquidation that a default chronology would miss. It is also the only American observation in 150 years, and it says what “early warning for a US-like sovereign” would actually be warning of — not a sudden stop, but a quiet tax on creditors. A dashboard that treats that channel as a crisis color is mis-describing the event class.

The implication for the dashboard genre is direct. A composite indicator whose out-of-sample validity cannot be established, on the only evidence base available, is not an early-warning system; it is a theory-organized display. Displays can be valuable — the indicators here are individually meaningful, and the r−g and debt-service logic behind them is sound — but the coloring of zones and the implied probabilistic warning carry an empirical authority the record cannot supply. The honest dashboard would say: these thresholds are calibrated on seven scored post-war advanced-economy events, or on none. Every one of those seven is a non-reserve-currency European economy.

Three routes to statistical power exist, and each changes the object of study rather than rescuing this one. Fitting on emerging markets multiplies events but imports a different generating process — different distress thresholds, external rather than fiscal failure modes, wave-structured dependence — and its results transfer to advanced sovereigns only as an assumption. Lengthening the horizon trades the warning's sharpness for event count. Testing on the pre-1950 era abandons the institutional regime the dashboards address. These are legitimate studies; the choice among them made after seeing which yields the prettiest curve would be the practice this design exists to refuse.

## 9. Conclusion

On a declared walk-forward over the long advanced-economy panel, multi-indicator sovereign debt early warning cannot be validated out of sample: the events are too rare to discriminate a thirteen-indicator model from debt/GDP alone, under either the declared or the coverage-corrected fold design, and this rarity is a property of the phenomenon rather than of the dataset. Dashboards addressed to US-like sovereigns therefore rest, and must rest, on theory and judgment rather than measured early-warning validity — a fact their presentation should reflect. The machinery built here — mechanical event labeling, an enforced and unit-tested confirmation gate, and a decision timeline that distinguishes what was fixed before evidence from what was refused after — is reusable on any panel that has events, and we intend to apply it, under a separately dated design, to the emerging-market record, where the interesting question is not whether early warning works but whether anything learned there transfers to the sovereigns the dashboards are actually about.

## Acknowledgements

Generative AI tools (Anthropic Claude, xAI Grok, and OpenAI ChatGPT) were used in code development, drafting, and editing under the author's direction. The author is solely responsible for the design, analysis, and all content, including errors.

---

## References

Blanchard, Olivier. 2019. "Public Debt and Low Interest Rates." *American Economic Review* 109 (4): 1197–1229.

Bussière, Matthieu, and Marcel Fratzscher. 2006. "Towards a New Early Warning System of Financial Crises." *Journal of International Money and Finance* 25 (6): 953–973.

Frankel, Jeffrey A., and Andrew K. Rose. 1996. "Currency Crashes in Emerging Markets: An Empirical Treatment." *Journal of International Economics* 41 (3–4): 351–366.

Hanley, James A., and Barbara J. McNeil. 1982. "The Meaning and Use of the Area under a Receiver Operating Characteristic (ROC) Curve." *Radiology* 143 (1): 29–36.

Jordà, Òscar, Katharina Knoll, Dmitry Kuvshinov, Moritz Schularick, and Alan M. Taylor. 2019. "The Rate of Return on Everything, 1870–2015." *Quarterly Journal of Economics* 134 (3): 1225–1298.

Jordà, Òscar, Moritz Schularick, and Alan M. Taylor. 2017. "Macrofinancial History and the New Business Cycle Facts." In *NBER Macroeconomics Annual 2016*, vol. 31, edited by Martin Eichenbaum and Jonathan A. Parker, 213–263. Chicago: University of Chicago Press. Database: https://www.macrohistory.net/database/.

Kaminsky, Graciela, Saul Lizondo, and Carmen M. Reinhart. 1998. "Leading Indicators of Currency Crises." *IMF Staff Papers* 45 (1): 1–48.

Reinhart, Carmen M., and Kenneth S. Rogoff. 2009. *This Time Is Different: Eight Centuries of Financial Folly*. Princeton: Princeton University Press.

Reinhart, Carmen M., and M. Belen Sbrancia. 2015. "The Liquidation of Government Debt." *Economic Policy* 30 (82): 291–333. Earlier version: NBER Working Paper 16893, 2011.

Schularick, Moritz, and Alan M. Taylor. 2012. "Credit Booms Gone Bust: Monetary Policy, Leverage Cycles, and Financial Crises, 1870–2008." *American Economic Review* 102 (2): 1029–1061.

---

## Appendix A — Reproducibility

Label pipeline (`debt_labels.py`), indicator construction (`debt_indicators.py`), walk-forward engine (`debt_walkforward.py`), and their unit-test suites accompany the paper, together with the label sets under both continuation codings, the threshold-sweep table, coverage matrices, and per-fold predictions. The companion repository is linked on the title page.

## Appendix B — Tables

### Table B0. Post-1950 onsets and their three lead years

y(s)=1 iff an onset falls in (s, s+3]. Exclusion covers t+1…t+5 after an onset at t. A lead year is scored only if it exists, is not excluded, is complete-case on the full indicator vector, and falls inside a test window.

| onset | rule | lead years | excluded? | complete-case? | original grid | tiling grid |
|---|---|---|---|---|---|---|
| Netherlands 1951 | D3 | 1950, 1949, 1948 | no | 1950 only | none (1950 not in any test window; not trainable at T=1950) | none |
| Netherlands 1957 | D3 | 1956, 1955, 1954 | all three | yes | unscoreable | unscoreable |
| UK 1973 | D3 | 1972, 1971, 1970 | no | yes | 1971–75 (two leads) | 1966–70 (one), 1971–75 (two) |
| Italy 1974 | D4 | 1973, 1972, 1971 | no | yes | 1971–75 (three) | 1971–75 (three) |
| Portugal 1977 | D4 | 1976, 1975, 1974 | no | yes | 1971–75 (two) | 1971–75 (two), 1976–80 (one) |
| Spain 1978 | D4 | 1977, 1976, 1975 | no | yes | 1971–75 (one) | 1971–75 (one), 1976–80 (two) |
| Ireland 1981 | D2 | 1980, 1979, 1978 | no | yes | gap | 1976–80 (three) |
| Portugal 1983 | D4 | 1982, 1981, 1980 | all three | yes | unscoreable | unscoreable |
| Ireland 2010 | D4 | 2009, 2008, 2007 | no | yes | gap | 2006–10 (three) |
| Portugal 2011 | D3,D4 | 2010, 2009, 2008 | no | yes | gap | 2006–10 (three) |

Scoreable onsets: 7. Tiling lead rows scored: 21. Original lead rows scored: 8 (four onsets). Portugal 1922 is the pre-1950 analogue of the six-year repeat (after Portugal 1916).

### Table B1. E0 onset list (primary labels, default gates)

| country | year | rule |
|---|---|---|
| Portugal | 1873 | D2,D3 |
| Spain | 1873 | D1 |
| Spain | 1882 | D1 |
| Portugal | 1890 | D3 |
| France | 1914 | D3 |
| Italy | 1915 | D3 |
| Netherlands | 1915 | D3 |
| Portugal | 1916 | D2 |
| UK | 1917 | D2,D3 |
| Portugal | 1922 | D2 |
| Belgium | 1923 | D3 |
| France | 1924 | D3 |
| Germany | 1932 | D1 |
| Spain | 1936 | D1 |
| France | 1937 | D2,D3 |
| Belgium | 1938 | D3 |
| Netherlands | 1939 | D3 |
| Italy | 1940 | D1 |
| Japan | 1942 | D1 |
| Finland | 1945 | D2,D3 |
| Spain | 1947 | D2,D3 |
| UK | 1947 | D3 |
| USA | 1947 | D3 |
| Germany | 1948 | D1 |
| Netherlands | 1951 | D3 |
| Netherlands | 1957 | D3 |
| UK | 1973 | D3 |
| Italy | 1974 | D4 |
| Portugal | 1977 | D4 |
| Spain | 1978 | D4 |
| Ireland | 1981 | D2 |
| Portugal | 1983 | D4 |
| Ireland | 2010 | D4 |
| Portugal | 2011 | D3,D4 |

N = 34. Risk set = 2,548 country-years after dropping exclusion-window rows. Incidence = 1.33%. Post-1950 = 10. Scoreable by the walk-forward = 7 (Table B0).

### Table B2. Declared threshold sweep (onset counts)

Inflation ∈ {15, 20, 25}%, debt gate ∈ {50, 60, 75}%, real bond TR ∈ {−10, −15, −20}%.

| infl | debt gate | real TR | onsets |
|---:|---:|---:|---:|
| 15 | 50 | −10 | 57 |
| 15 | 50 | −15 | 42 |
| 15 | 50 | −20 | 35 |
| 15 | 60 | −10 | 49 |
| 15 | 60 | −15 | 37 |
| 15 | 60 | −20 | 31 |
| 15 | 75 | −10 | 31 |
| 15 | 75 | −15 | 25 |
| 15 | 75 | −20 | 21 |
| 20 | 50 | −10 | 58 |
| 20 | 50 | −15 | 39 |
| 20 | 50 | −20 | 31 |
| **20** | **60** | **−15** | **34** |
| 20 | 60 | −10 | 48 |
| 20 | 60 | −20 | 27 |
| 20 | 75 | −10 | 32 |
| 20 | 75 | −15 | 24 |
| 20 | 75 | −20 | 20 |
| 25 | 50 | −10 | 56 |
| 25 | 50 | −15 | 35 |
| 25 | 50 | −20 | 26 |
| 25 | 60 | −10 | 47 |
| 25 | 60 | −15 | 32 |
| 25 | 60 | −20 | 24 |
| 25 | 75 | −10 | 32 |
| 25 | 75 | −15 | 24 |
| 25 | 75 | −20 | 19 |

Range 19–58. Default cell in bold.

### Table B3. Indicator coverage

Panel: 2,718 country-years. Complete-case on the thirteen declared indicators (inflation enters as the level and as its three-year change): 1,962 rows, 72.2%.

Mean non-null share by indicator:

| indicator | share |
|---|---:|
| infl | 97.4% |
| rer_usd_chg_3y | 95.9% |
| d_infl_3y | 95.5% |
| real_ltrate_3y | 94.9% |
| real_wage_g_3y | 94.5% |
| r_minus_g_3y | 94.4% |
| debt_gdp | 91.6% |
| slope | 91.6% |
| ca_gdp | 91.4% |
| ca_persist_3y | 89.0% |
| d_debt_gdp_3y | 88.2% |
| int_rev | 88.2% |
| primary_bal_gdp | 88.2% |
| credit_gap_5y | 85.6% |

Complete-case span by country (first–last year with every indicator):

| country | first | last | n |
|---|---:|---:|---:|
| Australia | 1902 | 2019 | 111 |
| Belgium | 1889 | 2020 | 103 |
| Canada | 1934 | 2020 | 83 |
| Denmark | 1883 | 2020 | 102 |
| Finland | 1917 | 2020 | 93 |
| France | 1904 | 2020 | 95 |
| Germany | 1874 | 2020 | 117 |
| Ireland | 1946 | 2020 | 75 |
| Italy | 1885 | 2020 | 127 |
| Japan | 1879 | 2017 | 121 |
| Netherlands | 1904 | 2020 | 96 |
| Norway | 1883 | 2020 | 127 |
| Portugal | 1880 | 2020 | 121 |
| Spain | 1904 | 2020 | 83 |
| Sweden | 1875 | 2020 | 146 |
| Switzerland | 1923 | 2020 | 88 |
| UK | 1884 | 2020 | 137 |
| USA | 1884 | 2020 | 137 |

Ireland is the thin country (59% overall; complete-case starts 1946). Canada’s complete-case start is 1934 because the short rate is missing early.

### Table B4. Walk-forward, live folds and pooled OOS

Descriptive only. Horse-race rows use the M1 complete-case intersection so M1 and M2 share country-years. AUC undefined when test positives = 0. Original grid: 8 folds. Tiling grid: 14 folds.

**Original grid** (declared). One live window, four onsets, eight lead rows.

| spec | test | model | pos | AUC | Brier |
|---|---|---|---:|---:|---:|
| full | 1971–75 | M1 | 8 | 0.59 | 0.107 |
| full | 1971–75 | M2 on M1 rows | 8 | 0.83 | 0.093 |
| R1 | 1971–75 | M1 | 8 | 0.85 | 0.093 |
| R1 | 1971–75 | M2 on M1 rows | 8 | 0.89 | 0.093 |

Pooled closed OOS, original grid, common rows:

| spec | model | n | pos | AUC | Brier |
|---|---|---:|---:|---:|---:|
| full | M1 | 572 | 8 | 0.31 | 0.037 |
| full | M2 on M1 rows | 572 | 8 | 0.59 | 0.019 |
| R1 | M1 | 583 | 8 | 0.45 | 0.022 |
| R1 | M2 on M1 rows | 583 | 8 | 0.61 | 0.018 |

**Tiling grid** (T every 5 years; coverage correction). Four live windows.

| spec | test | model | pos | AUC | Brier |
|---|---|---|---:|---:|---:|
| full | 1966–70 | M1 | 1 | 0.48 | 0.020 |
| full | 1966–70 | M2 on M1 rows | 1 | 0.81 | 0.011 |
| full | 1971–75 | M1 | 8 | 0.59 | 0.107 |
| full | 1971–75 | M2 on M1 rows | 8 | 0.83 | 0.093 |
| full | 1976–80 | M1 | 6 | 0.55 | 0.090 |
| full | 1976–80 | M2 on M1 rows | 6 | 0.53 | 0.077 |
| full | 2006–10 | M1 | 6 | 0.69 | 0.060 |
| full | 2006–10 | M2 on M1 rows | 6 | 0.78 | 0.056 |
| R1 | 1966–70 | M1 | 1 | 0.63 | 0.012 |
| R1 | 1966–70 | M2 on M1 rows | 1 | 0.90 | 0.011 |
| R1 | 1971–75 | M1 | 8 | 0.85 | 0.093 |
| R1 | 1971–75 | M2 on M1 rows | 8 | 0.89 | 0.093 |
| R1 | 1976–80 | M1 | 6 | 0.77 | 0.076 |
| R1 | 1976–80 | M2 on M1 rows | 6 | 0.55 | 0.081 |
| R1 | 2006–10 | M1 | 6 | 0.80 | 0.051 |
| R1 | 2006–10 | M2 on M1 rows | 6 | 0.79 | 0.056 |

Pooled closed OOS, tiling grid, common rows:

| spec | model | n | pos | AUC | Brier |
|---|---|---:|---:|---:|---:|
| full | M1 | 1053 | 21 | 0.44 | 0.038 |
| full | M2 on M1 rows | 1053 | 21 | 0.61 | 0.026 |
| R1 | M1 | 1066 | 21 | 0.59 | 0.026 |
| R1 | M2 on M1 rows | 1066 | 21 | 0.63 | 0.023 |

Onset-year drop (full spec; post-hoc, not adopted). Declared fit, onset years dropped only at evaluation: live-window M1 0.60. Train and test both dropped, common rows: live-window M1 0.64 / M2 0.84; tiling pooled M1 0.48. M2 is 0.83 on the declared live window and 0.84 after the drop. Test-side bound on the live window ≈ 0.02. Same four live-window onsets. Same power bound.

### Table B5. Wartime debt-gap fill (E0 continuation)

Look-ahead-safe LOCF of debt/GDP through spells overlapping 1914–23 or 1939–49. Primary continuation coding E0.

| cell | onsets | vs E0 raw |
|---|---:|---|
| E0, no fill (primary) | 34 | — |
| E1, no fill | 34 | identical |
| E0 × wartime LOCF | 34 | none added |
| E1 × wartime LOCF | 36 | France 1920, 1926, 1943 added; France 1924 dropped |

France 1938 carried debt = 102% of GDP (last observed 1938). Under E0 that fill still produces no new 1940s onset: 1937 starts the exclusion clock through 1942; 1942 fires D2 while excluded and sets continuation; 1943–48 are dated as the same spell. Germany 1923 carried debt = 47% from 1913, below the 60% gate. Not an onset under any cell in this table.
