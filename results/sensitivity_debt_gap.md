# Named sensitivity: wartime debt/GDP gap fill

Default labeler is unchanged. This run only answers: *if we carry the last
observed debt/GDP forward through wartime holes (look-ahead-safe, no
interpolation), does the onset list move?*

## Method

- Fill `debtgdp` within country from the last earlier observation.
- Primary variant: fill only missing spells that overlap 1914–23 or 1939–49.
- Check variant: unrestricted within-country LOCF (still no back-fill).
- Then call official `label_onsets()` at default thresholds
  (infl 20%, debt gate 60%, real TR −15%, exclusion 5).

Spells filled (wartime variant):

| country | gap | years | value carried | from |
|---|---|---|---|---|
| Belgium | 1914–19 | 6 | 49.5% | 1913 |
| Belgium | 1940–45 | 6 | 71.7% | 1939 |
| Denmark | 1947–52 | 6 | 10.0% | 1946 |
| France | 1914–19 | 6 | 66.4% | 1913 |
| France | 1939–48 | 10 | 101.6% | 1938 |
| Germany | 1914–26 | 13 | 47.0% | 1913 |
| Germany | 1944–49 | 6 | 174.0% | 1943 |
| Japan | 1945 | 1 | 204.0% | 1944 |
| Netherlands | 1940–45 | 6 | 110.8% | 1939 |
| Norway | 1940–46 | 7 | 24.4% | 1939 |
| Spain | 1936–39 | 4 | 65.9% | 1935 |

## Result

**Onset count does not move. Base 34 = wartime LOCF 34 = full LOCF 34.
Added onsets: none. Lost onsets: none.**

The holes the sensitivity was meant to recover stay off the onset list
for two different mechanical reasons. Neither is a coding bug.

## Why France 1945–48 still is not an onset

After the fill, the debt gate *opens*. Raw flags:

| year | infl | debt_lag | real TR | raw rules |
|---|---:|---:|---:|---|
| 1937 | 26% | 141% | −24% | D2,D3 **onset (already in base)** |
| 1938–41 | 6–19% | 102–107% | mixed | none |
| 1942 | 21% | 102% | −13% | D2, inside 1937 exclusion |
| 1943 | 24% | 102% | −18% | D2,D3 |
| 1944 | 22% | 102% | −12% | D2 |
| 1945 | 48% | 102% | −31% | D2,D3 |
| 1946 | 52% | 102% | −38% | D2,D3 |
| 1947 | 49% | 102% | −47% | D2,D3 |
| 1948 | 59% | 102% | −40% | D2,D3 |

Official onset rule is: fires now AND nothing fired last year AND not in
the 5-year exclusion. 1937 starts the clock (exclusion through 1942).
1942 still fires D2 *while excluded*, which sets `prev_fired=True`.
1943–48 are therefore dated as continuation of an already-open spell,
not a new onset.

So the 1940s French inflation adjustment is already represented by
**France 1937**. Filling wartime debt does not create a second onset.
That is the exclusion + continuation logic working as written in
`debt_labels.py`.

WWI France is the same shape: 1914 D3 is already in the base list;
1918–20 raw D2/D3 sit inside or adjacent to that spell.

## Why Germany 1923 still is not an onset

Carried debt is **47% from 1913**, below the 60% gate. Raw 1922–23
inflation is astronomical and real bond TR is ≈ −100%, but D2/D3
require debt_lag ≥ 60%. They do not fire.

This is the design’s own non-event rule — “wartime inflation with
debt/GDP < 60% must not count” — applied to the last *observed* debt.
We do not observe 1920–26 German debt/GDP in JST, so the gate never
sees a high debt ratio. Inventing one would not be a fill; it would
be a new series.

Germany 1948 remains D1 (currency reform). Official CPI inflation in
1944–48 is 2–15%, so D2 would not fire even with debt_lag = 174%.

## Other holes, same pattern

| hole | after fill | why not a new onset |
|---|---|---|
| Japan 1945 (infl 976%, real TR −90%, debt_lag 204%) | raw D2+D3 | inside Japan 1942 D1 exclusion |
| Belgium 1940 (infl 48%, debt_lag 72%) | raw D2 | inside Belgium 1938 D3 exclusion |
| Belgium 1915 (infl 40%) | raw nothing | carried debt 49.5% < 60% gate |
| Netherlands 1940–45 | raw nothing at 20%/−15% | already have Netherlands 1939 D3 |
| Norway 1940–46 | raw nothing | carried debt 24% < 60% |

## What this does *not* justify

- Changing default thresholds to pick up France 1943 or Germany 1923.
- Switching `prev_fired` off so an excluded D2 year does not block the
  first post-window year. That would be a §3 rewrite, not a data fill.
  (It would date France 1943 as a second onset. Pre-register it if you
  want it; do not sneak it in.)
- Interpolating post-war debt backward into the hole. 1949 France debt
  is 44% — using it as 1945’s lag would be look-ahead and would
  *close* the gate, not open it.

## Carry-forward into Step 2

Use the base 34-onset list. Report in the paper that a look-ahead-safe
wartime debt fill was run as a named sensitivity and moved **zero**
onsets, because the French 1940s spell is already dated at 1937 and
the German 1923 spell fails the 60% debt-context gate on the last
observed (1913) ratio.
