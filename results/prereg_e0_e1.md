# Pre-registration addendum — continuation coding E0 / E1

Date: 2026-08-31.
Status: declared after Step 1 labels and Step 2 *construction*, before any
indicator–outcome model, AUC, or calibration number exists.

## Why this exists

Under the original coding (E0), a raw D2/D3 firing *inside* the 5-year
exclusion window sets `prev_fired=True`. The first year after the window
is then treated as continuation rather than a new onset, even when that
year is the economically distinct spell.

On raw JST this is latent: France 1943–48 have missing debt/GDP, so
D2/D3 cannot fire and E0 = E1. It becomes visible only if debt is
carried forward through the wartime hole (the named LOCF sensitivity).
Then France 1942 fires D2 while still excluded from the 1937 onset, and
E0 dates the 1945–48 inflation/repression spell back to 1937. That is
mis-dating, not conservative dating.

Changing the continuation rule is a §3 rewrite, not a data fill. It is
registered here instead of being chosen after seeing model scores.

## Definitions

**E0 (primary, original `debt_labels.py`):**
`prev_fired = bool(fired)` every year, excluded or not.

**E1 (named variant):**
Excluded years do not set continuation state
(`prev_fired = False` if `in_exclusion`, else `bool(fired)`).
The first post-window firing is a new onset.

Germany 1923 is not part of this axis. Last observed debt (1913) is 47%,
below the 60% gate. E1 does not fabricate a 1920–26 debt series.

## What the four cells do on JST R6

Defaults: infl 20%, debt gate 60%, real TR −15%, exclusion 5 years.

| coding | wartime debt LOCF | onsets | risk-set years | base rate |
|---|---|---:|---:|---:|
| E0 (primary) | no | 34 | 2,548 | 1.33% |
| E1 | no | 34 | 2,548 | 1.33% |
| E0 | yes | 34 | 2,548 | 1.33% |
| E1 | yes | 36 | 2,538 | 1.42% |

E1 without the fill is identical to E0 on this panel. The only cell that
moves is **E1 × wartime LOCF**:

- France 1914 D3 stays
- France 1920 D2,D3 **added**; France 1924 D3 **drops** (now inside the
  1920 window)
- France 1926 D2 **added**
- France 1937 D2,D3 stays
- France 1943 D2,D3 **added** (the 1940s spell, dated at the first
  post-1937-window year that actually fires)

Net +2 onsets, all French, all in spells E0 was already trying to
capture and was dating early.

## How they will be used

- Primary confirmatory path: **E0, no debt fill.**
- Pre-registered robustness: carry **E1 × wartime LOCF** through the
  same walk-forward, same indicators, same models. No other label
  variant.
- If OOS discrimination and calibration are stable across the two,
  report that. If they diverge, that divergence is a result about
  event-dating conventions, not a reason to pick the kinder coding.

No other continuation rule will be added after model scores exist.

## Base-rate arithmetic (belongs on the Step 1 ledger)

JST R6: 2,718 country-years.
E0 exclusion window removes 170 rows from the risk set.
Risk set = 2,548 country-years (onsets + clean negatives).
Unconditional 3-year-adjacent base rate on that set, treating each
onset year as one positive: **34 / 2,548 = 1.33%**.

That 1.33% is *not* the 3-year-ahead onset probability the model
predicts. The model outcome is "onset in (t, t+h]"; with h=3 the
unconditional probability is higher than 1.33% because three lead
years can share one event. The calibration table must use the
h-year empirical frequency on the same risk set, computed inside
each fold's test window. The 34/2548 figure is the onset-year
incidence, reported so the denominator is not implicit.

Usable under the confirmation gate at T=2020, h=3, not excluded:
2,494 rows, still 34 onsets (every onset year is ≤ 2017).
