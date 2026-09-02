"""Tests for Step 2 indicator construction."""

from __future__ import annotations

import numpy as np
import pandas as pd

from debt_indicators import (
    INDICATORS,
    complete_case_mask,
    construct_indicators,
    coverage_share_matrix,
)


def _toy(n=12, country="X"):
    rows = []
    cpi = 100.0
    gdp = 100.0
    wage = 100.0
    loans = 50.0
    for i, yr in enumerate(range(2000, 2000 + n)):
        infl = 0.02
        cpi *= 1 + infl
        gdp *= 1.04
        wage *= 1.03
        loans *= 1.06
        rows.append(
            dict(
                country=country,
                year=yr,
                cpi=cpi,
                gdp=gdp,
                rgdpmad=1000 * (1.02 ** i),
                revenue=0.3 * gdp,
                expenditure=0.32 * gdp,
                debtgdp=0.50 + 0.01 * i,
                stir=3.0,
                ltrate=5.0,
                ca=-0.02 * gdp,
                xrusd=1.5,
                wage=wage,
                tloans=loans,
            )
        )
    return pd.DataFrame(rows)


def test_columns_present():
    # need a USA row so RER can merge CPI*
    a = _toy()
    usa = _toy(country="USA")
    usa["xrusd"] = 1.0
    lab = construct_indicators(pd.concat([a, usa], ignore_index=True))
    for c in INDICATORS:
        assert c in lab.columns, c


def test_debt_change_is_3y_difference():
    lab = construct_indicators(pd.concat([_toy(), _toy(country="USA")], ignore_index=True))
    x = lab[lab.country == "X"].reset_index(drop=True)
    # debtgdp starts 0.50 and rises 0.01/year → 3y change = 0.03 once window filled
    assert pd.isna(x.loc[2, "d_debt_gdp_3y"])
    np.testing.assert_allclose(x.loc[3, "d_debt_gdp_3y"], 0.03, rtol=1e-10)


def test_no_lookahead():
    """Mutating year 2010 raw data must not change indicators at 2009."""
    base = pd.concat([_toy(n=15), _toy(n=15, country="USA")], ignore_index=True)
    alt = base.copy()
    alt.loc[(alt.country == "X") & (alt.year == 2010), "debtgdp"] = 9.99
    alt.loc[(alt.country == "X") & (alt.year == 2010), "cpi"] = 999.0
    alt.loc[(alt.country == "X") & (alt.year == 2010), "ltrate"] = 99.0
    b = construct_indicators(base)
    a = construct_indicators(alt)
    b09 = b[(b.country == "X") & (b.year == 2009)][INDICATORS].reset_index(drop=True)
    a09 = a[(a.country == "X") & (a.year == 2009)][INDICATORS].reset_index(drop=True)
    pd.testing.assert_frame_equal(b09, a09)


def test_int_rev_proxy_formula():
    lab = construct_indicators(pd.concat([_toy(), _toy(country="USA")], ignore_index=True))
    x = lab[lab.country == "X"].iloc[-1]
    # int_rev = debt_gdp * r * gdp / revenue = debt_gdp * 0.05 / 0.30
    expected = x.debt_gdp * 0.05 / 0.30
    np.testing.assert_allclose(x.int_rev, expected, rtol=1e-10)
    assert bool(x.int_rev_is_proxy)


def test_coverage_matrix_shape():
    lab = construct_indicators(pd.concat([_toy(), _toy(country="USA")], ignore_index=True))
    m = coverage_share_matrix(lab)
    assert set(m.index) == {"X", "USA"}
    assert list(m.columns) == INDICATORS
    # trailing 3y/5y windows leave the first years incomplete by design
    late = lab[lab.year >= 2006]
    assert complete_case_mask(late).all(), late.loc[~complete_case_mask(late), INDICATORS]


if __name__ == "__main__":
    import sys

    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(fns)-failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
