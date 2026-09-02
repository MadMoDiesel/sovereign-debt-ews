# Step 2 — indicator construction and coverage

Code: `debt_indicators.py`. Tests: `test_debt_indicators.py` (5/5 PASS),
including a look-ahead test (mutating year t+1 does not change year t).

Panel: JST R6, 2,718 country-years. Written file: `results/indicators.csv`.

## Construction (design §4, no additions)

| # | column | construction | look-ahead |
|---|---|---|---|
| 1 | `debt_gdp` | JST `debtgdp`, ratio (autodetected) | contemporaneous |
| 2 | `d_debt_gdp_3y` | `debt_gdp_t − debt_gdp_{t−3}` | trailing |
| 3 | `int_rev` | `debt_gdp × r × gdp / revenue` | contemporaneous, **proxy** |
| 4 | `primary_bal_gdp` | `(rev−exp)/gdp + debt_gdp×r` | contemporaneous, **uses interest proxy** |
| 5 | `r_minus_g_3y` | 3y mean(r) − 3y mean(g_nom); g_nom = (1+Δrgdpmad)(1+π)−1 | trailing |
| 6 | `slope` | long rate − short rate | contemporaneous |
| 7 | `real_ltrate_3y` | r − 3y mean inflation | trailing inflation |
| 8 | `infl`, `d_infl_3y` | CPI pct_change; 3y difference of that rate | trailing |
| 9 | `ca_gdp` | `ca / gdp` | contemporaneous |
| 10 | `ca_persist_3y` | 3y mean of `ca_gdp` | trailing, **proxy for external-funding share** |
| 11 | `rer_usd_chg_3y` | 3y % change of `xrusd × CPI_US / CPI_i` | trailing; US CPI matched by year |
| 12 | `real_wage_g_3y` | 3y growth of wage/CPI | trailing |
| 13 | `credit_gap_5y` | `tloans/gdp` minus its trailing 5y mean | trailing (no full-sample HP) |

r and stir stored in JST as percent points; converted to decimals.

Nominal GDP growth is **not** `gdp.pct_change()`. Raw `gdp` rebases
across wartime currency reforms (France 1938 vs 1950) and would poison
r−g. Real growth from `rgdpmad` plus CPI inflation is the look-ahead-safe
substitute.

## Proxies that must be flagged in the paper

JST has no interest-expense series and no external-share-of-public-debt
series. Items 3 and 10 are therefore proxies by construction; every row
carries `int_rev_is_proxy` and `ca_persist_is_ext_proxy`. Item 4 inherits
the interest proxy. Do not treat them as observed.

## Coverage

2,718 rows. **1,962 complete-case rows (72.2%)** across all 14 columns.

Mean non-null share by indicator (18-country average):

| indicator | share |
|---|---|
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

Weakest countries: **Ireland 59%** (series start ~1922 and fiscal/credit
thin), Finland 88% (late debt), Germany/France ~90% (wartime holes).
Strongest: Sweden, USA, UK, Italy, Portugal.

Complete-case span by country (first–last year that has every indicator):

| country | first | last | n |
|---|---|---|---|
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

Canada’s complete-case start is 1934 because `stir` (needed for slope)
is missing for most of the early sample (slope coverage 58%). Switzerland
CA is the thin series (61%). Ireland is thin on everything pre-1946.

Walk-forward §6 uses pre-1950 as training-only seed. Post-1950
complete-case coverage is usable for every country except that Ireland
is short and Japan ends 2017.

## Onset-year completeness (the 34)

20 of 34 onset years have the full indicator vector at t. The 14 holes
are almost all wartime / 19th-century credit and fiscal gaps, not a
systematic modern problem:

- credit_gap_5y missing: Belgium 1923, Portugal 1873/1916/1922, Spain 1873/1882/1936/1947
- slope missing: Italy 1915, Japan 1942, Portugal 1873
- fiscal + CA missing: France 1914, Germany 1948, Netherlands 1915, Spain 1873/1936
- Finland 1945: rates/fiscal hole

This matters less than it looks. The model predicts *from t* about
onsets in (t, t+h]; it does not need a complete vector *on the onset
year itself*. What it needs is complete vectors on the pre-onset risk
set. `in_exclusion` years are dropped anyway.

## What Step 2 does not do

- No extra indicators.
- No full-sample HP credit gap.
- No vintage reconstruction (JST is revised; said so in §8).
- No imputation of wartime debt (Step 1 sensitivity already showed that
  fill does not change labels; it would change `debt_gdp` at those years
  and is still a named sensitivity only).

Next is Step 3: walk-forward engine adapted from `walkforward_refit.py`,
using `labels_usable_at` as the only training-label accessor.
