# Step 1 results — official labeler vs JST R6

Code: original `debt_labels.py` / `test_debt_labels.py` (6/6 PASS).
Spec: `debt_ews_research_design.md` §3.
Panel: JST R6, 18 countries, 1870–2020, 2,718 country-years.
Overlays: `overlays/rr_defaults.csv`, `overlays/imf_programs.csv`
(ledger in `overlays/overlay_notes.md`).

## Schema check

| COLS key | JST R6 name | present | notes |
|---|---|---|---|
| country | country | yes | values include `UK`, `USA` |
| year | year | yes | 1870–2020 |
| cpi | cpi | yes | index **level**; inflation via `pct_change` |
| debtgdp | debtgdp | yes | **ratio** (median 0.45, max 2.70) — autodetect correct |
| bond_tr | bond_tr | yes | decimal total return; **Canada 0 / Ireland 0** non-null |
| ltrate | ltrate | yes | not used for D3 because `bond_tr` exists as a column (gaps stay NaN; the coupon proxy only engages if the *column* is absent) |

`d3_proxy` flag: False. Ireland/Canada therefore cannot fire D3.

## Defaults and count

Pre-registered defaults: inflation ≥ 20%, debt/GDP lag ≥ 60%, real bond TR ≤ −15%, 5-year exclusion.

**Onsets at defaults: 34**

HANDOFF / design expected band: ~40–80. 34 is just under the floor, not single digits.

Sweep over the pre-registered grid `{15,20,25}% × {50,60,75}% × {−10,−15,−20}%`:

| cell | n_onsets |
|---|---|
| loosest (15 / 50 / −10) | 57 |
| **default (20 / 60 / −15)** | **34** |
| tightest (25 / 75 / −20) | 19 |
| full grid range | **19–58** |

The count moves with the debt gate and the D3 threshold, as designed. It does not collapse to single digits at the tight corner.

## Onset list (defaults)

| country | year | rule | infl | debt_lag | real bond TR |
|---|---|---|---:|---:|---:|
| Belgium | 1923 | D3 | 15% | 141% | −25% |
| Belgium | 1938 | D3 | 4% | 72% | −15% |
| Finland | 1945 | D2,D3 | 40% | 71% | −25% |
| France | 1914 | D3 | 2% | 66% | −16% |
| France | 1924 | D3 | 14% | 217% | −15% |
| France | 1937 | D2,D3 | 26% | 141% | −24% |
| Germany | 1932 | D1 | −11% | 35% | +40% |
| Germany | 1948 | D1 | 15% | missing | missing |
| Ireland | 1981 | D2 | 20% | 67% | no bond_tr |
| Ireland | 2010 | D4 | −1% | 62% | no bond_tr |
| Italy | 1915 | D3 | 7% | 80% | −16% |
| Italy | 1940 | D1 | 17% | 81% | −8% |
| Italy | 1974 | D4 | 19% | 49% | −24% |
| Japan | 1942 | D1 | 3% | 93% | +1% |
| Netherlands | 1915 | D3 | 15% | 64% | −18% |
| Netherlands | 1939 | D3 | 1% | 118% | −19% |
| Netherlands | 1951 | D3 | 12% | 137% | −18% |
| Netherlands | 1957 | D3 | 6% | 75% | −16% |
| Portugal | 1873 | D2,D3 | 32% | 62% | −17% |
| Portugal | 1890 | D3 | 13% | 65% | −18% |
| Portugal | 1916 | D2 | 22% | 62% | −13% |
| Portugal | 1922 | D2 | 21% | 74% | −8% |
| Portugal | 1977 | D4 | 33% | 26% | −37% |
| Portugal | 1983 | D4 | 26% | 43% | −6% |
| Portugal | 2011 | D3,D4 | 4% | 100% | −34% |
| Spain | 1873 | D1 | 8% | missing | missing |
| Spain | 1882 | D1 | 4% | 144% | missing |
| Spain | 1936 | D1 | 2% | 66% | −6% |
| Spain | 1947 | D2,D3 | 20% | 61% | −17% |
| Spain | 1978 | D4 | 20% | 13% | −20% |
| UK | 1917 | D2,D3 | 25% | 66% | −18% |
| UK | 1947 | D3 | 7% | 270% | −20% |
| UK | 1973 | D3 | 9% | 62% | −17% |
| USA | 1947 | D3 | 14% | 119% | −15.1% |

Rule mix: D3 13, D1 7, D2+D3 5, D4 5, D2 3, D3+D4 1.

## Sanity against design §3 / HANDOFF step 5

Recognizable:
- Interwar / wartime defaults: Germany 1932, Italy 1940, Japan 1942, Spain 1936, Portugal 1890 (D3 into the 1892 D1, which is absorbed by exclusion).
- 1970s UK/Italy: UK 1973 D3 (gilts); 1976 IMF sits inside the exclusion window. Italy 1974 D4.
- Euro-crisis: Ireland 2010 D4, Portugal 2011 D3+D4.
- 2008-09 US/UK: **no onset.** USA 2009 real bond TR = **−14.9%** with debt_lag 68% — knife-edge under the −15% cut, does not fire. At the −10% sweep corner it would.

Misses the design itself flagged as should-be-recognizable:
- **France 1945-48 inflation adjustment does not fire.** Inflation 48-59% and real bond TR −31% to −47%, but JST `debtgdp` is missing 1939-1948, so the t-1 debt gate is NaN and D2/D3 are silent. Same hole: Germany 1923 hyperinflation (debt missing). Japan 1945-46 inflation is inside the 1942 D1 exclusion, so it is dated as a continuation, not a miss.
- This is a **data-gap**, not a threshold problem. Filling it after seeing the list (e.g. last-observation-carried-forward on debt through wartime holes) would be a new researcher degree of freedom and must be labeled a named sensitivity, not folded into the default.

US question (design §8):
- Base overlay has no US D1. 1933 gold clause does not fire. 1971 does not fire.
- **USA 1947 does fire D3** (real TR −15.1%, debt_lag 119%). The design text said the US “never appears as a positive label … arguably 1933/1971.” Under the *mechanical* §3 rules it does appear once. Report 1947 as the US positive; do not delete it.

Non-events that correctly did not count:
- USA/UK 2008 banking crisis.
- Wartime inflation with debt_lag < 60% (blocked by the gate).

## Overlay notes that affected the count

- Italy 1977 and UK 1976 are in the IMF file but absorbed by earlier onsets. Correct exclusion behavior.
- Portugal 1892 D1 absorbed by 1890 D3. Same.
- USA 1933 / 1971 left out of the base D1 file on purpose (named sensitivity). Adding 1933 raises the total from 34 to 35.

## Confirmation gate

`labels_usable_at(labels, train_end=1978, horizon=3)` max year = 1975. A 1975 training row is unusable until T >= 1978. Unit test `test_confirmation_gate_blocks_unclosed_windows` covers positives and negatives.

## Go / no-go

| rule in HANDOFF | observed |
|---|---|
| ~40-80 onsets | **34** (grid 19-58) |
| reasonably stable across the grid | moves with debt gate and D3 cut; no collapse |
| events recognizable | yes, with the France-1940s hole called out |
| 2008 US/UK must not fire | holds at defaults; knife-edge at USA 2009 −14.9% |

**Decision: proceed to Step 2 (indicator construction, design §4), with these three items carried forward in every write-up:**

1. Event count is 34, slightly below the 40-80 planning number — cap model complexity even harder than §5 already does.
2. France 1945-48 is a missing-debt hole, not a non-event. Named sensitivity only: carry last debt/GDP across wartime gaps.
3. USA 1947 is a real D3 hit. The “US has zero positives” sentence in §8 is false under the mechanical rule and must be rewritten.

Do not tune thresholds to push the count through 40. Do not add hand-picked events.

## Base-rate arithmetic (added 2026-08-31)

JST R6 panel: 2,718 country-years.
Exclusion window removes 170 rows.
**Risk set = 2,548 country-years. Onset-year incidence = 34 / 2,548 = 1.33%.**

This is the incidence of onset *years*, not the h-year-ahead probability
the model predicts. Calibration must use the fold-wise empirical
frequency of "onset in (t, t+h]" on the same risk set.

Continuation-coding addendum (E0 primary, E1 named variant) is in
`prereg_e0_e1.md`. Declared before any model score.
