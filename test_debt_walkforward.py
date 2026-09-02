"""Look-ahead and outcome tests for the Step 3 engine."""

from __future__ import annotations

import pandas as pd

from debt_labels import label_onsets, labels_usable_at
from debt_walkforward import Fold, attach_outcome, run_fold, risk_set


def _panel():
    rows = []
    cpi = 100.0
    for yr in range(1990, 2021):
        infl = 0.25 if yr in (2005, 2006) else 0.02
        cpi *= 1 + infl
        rows.append(dict(
            country="ALPHA", year=yr, cpi=cpi, debtgdp=80.0,
            bond_tr=0.05, ltrate=5.0,
        ))
    return pd.DataFrame(rows)


def test_outcome_is_forward_not_contemporaneous():
    lab = label_onsets(_panel())
    # ALPHA D2 onset at 2005. Feature year 2004 should be y=1 for h=3
    # (onset in 2005 is in (2004, 2007]). Feature year 2005 should be y=0
    # (next onset not inside (2005, 2008] because of exclusion).
    frame = lab[["country", "year"]].copy()
    out = attach_outcome(frame, lab, horizon=3)
    assert int(out.loc[out.year == 2004, "y"].iloc[0]) == 1
    assert int(out.loc[out.year == 2005, "y"].iloc[0]) == 0
    assert int(out.loc[out.year == 2002, "y"].iloc[0]) == 1  # (2002, 2005] includes 2005
    assert int(out.loc[out.year == 2001, "y"].iloc[0]) == 0


def test_usable_at_is_the_train_door():
    lab = label_onsets(_panel())
    usable = labels_usable_at(lab, train_end=2006, horizon=3)
    assert usable["year"].max() <= 2003
    # risk set still drops exclusion years
    rs = risk_set(usable)
    assert not set(rs.year) & set(lab.loc[lab.in_exclusion, "year"])


def test_fold_train_does_not_include_unclosed_windows():
    """A 2005 feature row is illegal for train_end=2006, h=3."""
    lab = label_onsets(_panel())
    usable = labels_usable_at(lab, train_end=2006, horizon=3)
    assert 2005 not in set(usable.year)
    assert 2004 not in set(usable.year)
    assert 2003 in set(usable.year)


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
