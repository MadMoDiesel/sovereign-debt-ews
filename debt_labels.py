"""
Disorderly sovereign debt adjustment labeler (research design section 3).

Runs against the Jorda-Schularick-Taylor Macrohistory Database. JST ships as
Excel/Stata (macrohistory.net); load it to a DataFrame and pass it in.

IMPORTANT — schema mapping: JST column names vary slightly across releases
(R4/R5/R6). All column access goes through the COLS mapping below. On first
run against the real file, verify each mapping (a one-minute check) and adjust
strings there — nothing else in the pipeline touches raw names. Any column
you can't map: set it to None and the dependent rule degrades gracefully
(D1 needs the external default overlay; D2 needs cpi+debt; D3 needs bond_tr
or ltrate+cpi fallback; D4 needs the IMF overlay).

Event definitions (pre-registered; sweep grids in section 3 of the design):
  D1: sovereign default/restructuring onset (from Reinhart-Rogoff overlay CSV)
  D2: CPI inflation >= 20% while debt/GDP >= 60% at t-1
  D3: real gov-bond total return <= -15% while debt/GDP >= 60% at t-1
  D4: IMF program with fiscal conditionality (overlay CSV, post-1945)

Onset = any rule fires at t with none active at t-1, country not inside the
5-year exclusion window after a prior onset.

CONFIRMATION GATE (the leak most EWS papers carry): a training example at
year s with horizon h is usable only by folds with train_end >= s + h.
`labels_usable_at(df_labels, train_end, horizon)` is the single sanctioned
accessor, mirroring labels_visible_at() in bottom_labels.py.
"""

from __future__ import annotations
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- schema map
COLS = {
    "country": "country",      # or "iso"
    "year": "year",
    "cpi": "cpi",              # CPI index level (inflation computed from it)
    "debtgdp": "debtgdp",      # public debt / GDP (ratio or %; autodetected)
    "bond_tr": "bond_tr",      # nominal total return on long gov bonds; None if absent
    "ltrate": "ltrate",        # long rate (fallback for D3 if bond_tr missing)
}

# pre-registered thresholds + sweep grids (design section 3)
DEFAULTS = dict(infl_thresh=0.20, debt_gate=0.60, real_ret_thresh=-0.15,
                exclusion_years=5)
SWEEP = dict(infl_thresh=[0.15, 0.20, 0.25], debt_gate=[0.50, 0.60, 0.75],
             real_ret_thresh=[-0.10, -0.15, -0.20])


def _col(df, key):
    name = COLS.get(key)
    return df[name] if name and name in df.columns else None


def prepare_panel(jst: pd.DataFrame) -> pd.DataFrame:
    """Sort, derive inflation / real bond return / lagged debt. Idempotent."""
    df = jst.copy()
    c, y = COLS["country"], COLS["year"]
    df = df.sort_values([c, y]).reset_index(drop=True)
    g = df.groupby(c, sort=False)

    cpi = _col(df, "cpi")
    if cpi is None:
        raise ValueError("cpi column required (fix COLS mapping)")
    df["_infl"] = g[COLS["cpi"]].pct_change()

    debt = _col(df, "debtgdp")
    if debt is None:
        raise ValueError("debtgdp column required (fix COLS mapping)")
    # autodetect % vs ratio: median > 3 means it's in percent
    scale = 100.0 if df[COLS["debtgdp"]].median(skipna=True) > 3 else 1.0
    df["_debt"] = df[COLS["debtgdp"]] / scale
    df["_debt_lag"] = g["_debt"].shift(1)

    btr = _col(df, "bond_tr")
    if btr is not None:
        df["_real_bond_ret"] = (1 + df[COLS["bond_tr"]]) / (1 + df["_infl"]) - 1
    else:
        lt = _col(df, "ltrate")
        if lt is not None:
            # crude proxy: coupon-only real return; flag in output
            df["_real_bond_ret"] = (1 + df[COLS["ltrate"]] / 100.0) / (1 + df["_infl"]) - 1
            df.attrs["d3_proxy"] = True
        else:
            df["_real_bond_ret"] = np.nan
    return df


def label_onsets(
    panel: pd.DataFrame,
    rr_defaults: pd.DataFrame | None = None,   # columns: country, year (D1 onsets)
    imf_programs: pd.DataFrame | None = None,  # columns: country, year (D4)
    infl_thresh: float = DEFAULTS["infl_thresh"],
    debt_gate: float = DEFAULTS["debt_gate"],
    real_ret_thresh: float = DEFAULTS["real_ret_thresh"],
    exclusion_years: int = DEFAULTS["exclusion_years"],
    continuation: str = "E0",
) -> pd.DataFrame:
    """
    Returns one row per country-year in the risk set with:
      country, year, onset (bool), rule ('' or comma-joined of D1..D4),
      in_exclusion (bool). Rows inside a post-onset exclusion window have
      onset=False, in_exclusion=True (they are OUT of the risk set: exclude
      from model fitting entirely, don't treat as clean negatives).
    """
    if continuation not in ("E0", "E1"):
        raise ValueError("continuation must be 'E0' or 'E1'")
    df = prepare_panel(panel)
    c, y = COLS["country"], COLS["year"]

    def overlay_set(ov):
        if ov is None:
            return set()
        return {(r["country"], int(r["year"])) for _, r in ov.iterrows()}

    d1 = overlay_set(rr_defaults)
    d4 = overlay_set(imf_programs)

    rows = []
    for country, gdf in df.groupby(c, sort=False):
        gdf = gdf.sort_values(y)
        excl_until = -np.inf
        prev_fired = False
        for _, r in gdf.iterrows():
            yr = int(r[y])
            fired = []
            if (country, yr) in d1:
                fired.append("D1")
            if (r["_infl"] >= infl_thresh and r["_debt_lag"] >= debt_gate):
                fired.append("D2")
            if (r["_real_bond_ret"] <= real_ret_thresh and r["_debt_lag"] >= debt_gate):
                fired.append("D3")
            if (country, yr) in d4 and yr >= 1945:
                fired.append("D4")

            in_excl = yr <= excl_until
            # onset = fires now, nothing fired last year, not in exclusion
            onset = bool(fired) and not prev_fired and not in_excl
            if onset:
                excl_until = yr + exclusion_years
            rows.append(dict(country=country, year=yr, onset=onset,
                             rule=",".join(fired) if onset else "",
                             in_exclusion=in_excl and not onset))
            # E0: any raw firing sets continuation, including years inside
            #     the exclusion window (current / original coding).
            # E1: excluded years do not set continuation state, so the first
            #     post-window firing is a new onset. Pre-registered 2026-08-31
            #     before any indicator–outcome model was fit.
            if continuation == "E0":
                prev_fired = bool(fired)
            else:
                prev_fired = False if in_excl else bool(fired)
    out = pd.DataFrame(rows)
    out.attrs["params"] = dict(infl_thresh=infl_thresh, debt_gate=debt_gate,
                               real_ret_thresh=real_ret_thresh,
                               exclusion_years=exclusion_years,
                               continuation=continuation,
                               d3_proxy=df.attrs.get("d3_proxy", False))
    return out


def labels_usable_at(labels: pd.DataFrame, train_end: int, horizon: int) -> pd.DataFrame:
    """
    THE CONFIRMATION GATE. For fold training through year train_end with an
    h-year-ahead outcome, a country-year s is a usable training example only
    if its full outcome window closes inside the training period:
        s + horizon <= train_end
    Both positives and negatives need the gate: a 'no onset within h years'
    label is equally unknowable before s+horizon. Model-fitting code obtains
    training rows ONLY through this function.
    """
    return labels[labels["year"] + horizon <= train_end].copy()


def sweep_event_counts(panel, rr_defaults=None, imf_programs=None) -> pd.DataFrame:
    """Section 3 sensitivity: onset counts across the pre-registered grid."""
    import itertools
    recs = []
    for it, dg, rr in itertools.product(SWEEP["infl_thresh"], SWEEP["debt_gate"],
                                        SWEEP["real_ret_thresh"]):
        lab = label_onsets(panel, rr_defaults, imf_programs,
                           infl_thresh=it, debt_gate=dg, real_ret_thresh=rr)
        recs.append(dict(infl_thresh=it, debt_gate=dg, real_ret_thresh=rr,
                         n_onsets=int(lab["onset"].sum())))
    return pd.DataFrame(recs)


if __name__ == "__main__":
    print("Run test_debt_labels.py for verification; "
          "load JST + overlays and call label_onsets() for real counts.")
