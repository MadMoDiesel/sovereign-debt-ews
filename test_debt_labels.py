"""
Tests for debt_labels. Synthetic panel with known ground truth: the tests
prove rule firing, the debt gate, onset-vs-continuation, exclusion windows,
and — the load-bearing one — the confirmation gate on BOTH positives and
negatives.
"""

import numpy as np
import pandas as pd
from debt_labels import label_onsets, labels_usable_at, sweep_event_counts


def make_panel():
    """
    Two countries, 1990-2019.
    ALPHA: debt high (80%) from 2000; inflation spike 25% in 2005-2006;
           calm otherwise -> one D2 onset at 2005, continuation 2006 not an
           onset, exclusion through 2010.
    BETA:  debt low (30%) throughout; same 25% inflation spike 2005 -> debt
           gate blocks it; NO onsets. Real bond return crash -20% in 2012 ->
           also blocked by gate.
    """
    rows = []
    for ctry, debt_hi in [("ALPHA", True), ("BETA", False)]:
        cpi = 100.0
        for yr in range(1990, 2020):
            infl = 0.02
            if yr in (2005, 2006):
                infl = 0.25
            cpi *= (1 + infl)
            debt = 0.80 if (debt_hi and yr >= 2000) else 0.30
            btr = 0.05
            if ctry == "BETA" and yr == 2012:
                btr = -0.18  # nominal crash; real ~ -20% but debt gate blocks
            rows.append(dict(country=ctry, year=yr, cpi=cpi,
                             debtgdp=debt * 100,  # in percent: tests autodetect
                             bond_tr=btr, ltrate=5.0))
    return pd.DataFrame(rows)


def test_d2_fires_with_gate_and_not_without():
    lab = label_onsets(make_panel())
    a = lab[(lab.country == "ALPHA") & lab.onset]
    b = lab[(lab.country == "BETA") & lab.onset]
    assert list(a.year) == [2005], f"expected ALPHA 2005 only, got {list(a.year)}"
    assert "D2" in a.iloc[0].rule
    assert len(b) == 0, "BETA fired despite low debt — gate broken"


def test_continuation_is_not_onset():
    lab = label_onsets(make_panel())
    row_2006 = lab[(lab.country == "ALPHA") & (lab.year == 2006)].iloc[0]
    assert not row_2006.onset, "2006 continuation wrongly counted as onset"


def test_exclusion_window():
    lab = label_onsets(make_panel())
    excl = lab[(lab.country == "ALPHA") & (lab.year.between(2007, 2010))]
    assert excl.in_exclusion.all(), "post-onset years not marked excluded"
    post = lab[(lab.country == "ALPHA") & (lab.year == 2011)].iloc[0]
    assert not post.in_exclusion


def test_d1_overlay():
    rr = pd.DataFrame([dict(country="BETA", year=1995)])
    lab = label_onsets(make_panel(), rr_defaults=rr)
    b95 = lab[(lab.country == "BETA") & (lab.year == 1995)].iloc[0]
    assert b95.onset and "D1" in b95.rule


def test_confirmation_gate_blocks_unclosed_windows():
    lab = label_onsets(make_panel())
    horizon = 3
    # train_end 2006: a 2005 example needs 2005+3=2008 <= 2006 -> blocked
    usable = labels_usable_at(lab, train_end=2006, horizon=horizon)
    assert 2005 not in set(usable[usable.country == "ALPHA"].year), \
        "leak: 2005 example usable before its 3y window closed"
    # negatives gated too: 2004 (a negative) also needs 2007 <= train_end
    assert 2004 not in set(usable.year), "leak: negative label before window closed"
    # train_end 2008: 2005 now usable
    usable2 = labels_usable_at(lab, train_end=2008, horizon=horizon)
    assert 2005 in set(usable2[usable2.country == "ALPHA"].year)


def test_e1_excluded_year_does_not_set_continuation():
    """E1: a raw firing inside the exclusion window must not suppress the
    first post-window firing. E0 (default) keeps current behavior."""
    rows = []
    cpi = 100.0
    for yr in range(2000, 2016):
        infl = 0.25 if yr in (2005, 2006, 2010, 2011) else 0.02
        cpi *= 1 + infl
        rows.append(dict(country="ALPHA", year=yr, cpi=cpi,
                         debtgdp=80.0, bond_tr=0.05, ltrate=5.0))
    panel = pd.DataFrame(rows)
    e0 = label_onsets(panel, continuation="E0")
    e1 = label_onsets(panel, continuation="E1")
    assert list(e0.loc[e0.onset, "year"]) == [2005], list(e0.loc[e0.onset, "year"])
    assert list(e1.loc[e1.onset, "year"]) == [2005, 2011], list(e1.loc[e1.onset, "year"])


def test_sweep_monotonicity():
    # stricter gates can't produce MORE onsets
    sw = sweep_event_counts(make_panel())
    loose = sw[(sw.infl_thresh == 0.15) & (sw.debt_gate == 0.50) &
               (sw.real_ret_thresh == -0.10)].n_onsets.iloc[0]
    tight = sw[(sw.infl_thresh == 0.25) & (sw.debt_gate == 0.75) &
               (sw.real_ret_thresh == -0.20)].n_onsets.iloc[0]
    assert tight <= loose


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
