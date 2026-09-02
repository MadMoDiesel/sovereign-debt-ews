"""
Step 2 — indicator construction from JST (research design §4).

Thirteen pre-registered indicators, all measured at t with data through t
only. Trailing windows never look forward. Full-sample HP filters are
not used (they leak).

Not in JST, flagged proxies:
  * interest expense / revenue  →  debt/GDP × long rate × GDP / revenue
  * external-funding share      →  3-year trailing mean of CA/GDP

Item 8 is two columns (inflation level and 3-year change) under one
declared indicator.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

from debt_labels import COLS, prepare_panel

# Declared list, in design order. Do not append after seeing results.
INDICATORS = [
    "debt_gdp",
    "d_debt_gdp_3y",
    "int_rev",
    "primary_bal_gdp",
    "r_minus_g_3y",
    "slope",
    "real_ltrate_3y",
    "infl",
    "d_infl_3y",
    "ca_gdp",
    "ca_persist_3y",
    "rer_usd_chg_3y",
    "real_wage_g_3y",
    "credit_gap_5y",
]

# Pre-registered 2026-08-31. Primary list is INDICATORS. Robustness drops
# the two thinnest risk-set series. Credit-gap windows built alongside.
REDUCED_DROP = ("credit_gap_5y", "d_debt_gdp_3y")
REDUCED_INDICATORS = [c for c in INDICATORS if c not in REDUCED_DROP]
CREDIT_GAP_WINDOWS = (5, 7, 10)

PROXY_FLAGS = ["int_rev_is_proxy", "primary_bal_uses_int_proxy", "ca_persist_is_ext_proxy"]


def _safe_div(a: pd.Series, b: pd.Series) -> pd.Series:
    out = a / b.replace(0, np.nan)
    return out.replace([np.inf, -np.inf], np.nan)


def _trailing_mean(g: pd.Series, window: int) -> pd.Series:
    return g.rolling(window, min_periods=window).mean()


def construct_indicators(jst: pd.DataFrame) -> pd.DataFrame:
    """Return one row per country-year with the §4 indicator set."""
    raw = jst.copy().sort_values(["country", "year"]).reset_index(drop=True)
    # reuse official debt scale + inflation from the labeler
    prep = prepare_panel(raw)
    df = raw.merge(
        prep[["country", "year", "_infl", "_debt"]],
        on=["country", "year"],
        how="left",
    )

    g = df.groupby("country", sort=False)

    # --- 1. debt/GDP level (ratio) ---
    df["debt_gdp"] = df["_debt"]

    # --- 2. 3-year change in debt/GDP ---
    df["d_debt_gdp_3y"] = g["debt_gdp"].diff(3)

    # --- 8. inflation level (also needed for r-g, real rate, RER) ---
    df["infl"] = df["_infl"]
    df["d_infl_3y"] = g["infl"].diff(3)

    # nominal GDP growth via real growth + inflation, avoids currency rebases
    # that make raw gdp.pct_change() explode (France 1940s, etc.)
    if "rgdpmad" in df.columns:
        df["_g_real"] = g["rgdpmad"].pct_change()
    else:
        df["_g_real"] = np.nan
    df["_g_nom"] = (1 + df["_g_real"]) * (1 + df["infl"]) - 1
    # guard rebase / hyperinflation artifacts already present as numbers;
    # do not winsorize — those years are real, just ugly.

    # long rate as decimal
    df["_r"] = pd.to_numeric(df.get("ltrate"), errors="coerce")
    med_r = df["_r"].median(skipna=True)
    if pd.notna(med_r) and med_r > 1:
        df["_r"] = df["_r"] / 100.0

    # short rate as decimal (same unit logic)
    df["_stir"] = pd.to_numeric(df.get("stir"), errors="coerce")
    med_s = df["_stir"].median(skipna=True)
    if pd.notna(med_s) and med_s > 1:
        df["_stir"] = df["_stir"] / 100.0

    # --- 3. interest / revenue (always a proxy in JST) ---
    # interest ≈ debt_gdp * r * gdp ; ratio to revenue = debt_gdp * r * gdp / revenue
    gdp = pd.to_numeric(df.get("gdp"), errors="coerce")
    rev = pd.to_numeric(df.get("revenue"), errors="coerce")
    exp = pd.to_numeric(df.get("expenditure"), errors="coerce")
    df["_int"] = df["debt_gdp"] * df["_r"] * gdp
    df["int_rev"] = _safe_div(df["_int"], rev)
    df["int_rev_is_proxy"] = df["int_rev"].notna()

    # --- 4. primary balance / GDP ---
    # overall balance/GDP + interest/GDP, assuming expenditure is total
    df["_ob_gdp"] = _safe_div(rev - exp, gdp)
    df["_int_gdp"] = df["debt_gdp"] * df["_r"]
    df["primary_bal_gdp"] = df["_ob_gdp"] + df["_int_gdp"]
    df["primary_bal_uses_int_proxy"] = df["primary_bal_gdp"].notna()

    # --- 5. r - g, 3-year trailing means ---
    df["_r_3y"] = g["_r"].transform(lambda s: _trailing_mean(s, 3))
    df["_g_3y"] = g["_g_nom"].transform(lambda s: _trailing_mean(s, 3))
    df["r_minus_g_3y"] = df["_r_3y"] - df["_g_3y"]

    # --- 6. long-short slope ---
    df["slope"] = df["_r"] - df["_stir"]

    # --- 7. real long rate (long rate − trailing 3y inflation) ---
    df["_infl_3y"] = g["infl"].transform(lambda s: _trailing_mean(s, 3))
    df["real_ltrate_3y"] = df["_r"] - df["_infl_3y"]

    # --- 9. current account / GDP ---
    ca = pd.to_numeric(df.get("ca"), errors="coerce")
    df["ca_gdp"] = _safe_div(ca, gdp)

    # --- 10. external-funding proxy: CA/GDP persistence ---
    df["ca_persist_3y"] = g["ca_gdp"].transform(lambda s: _trailing_mean(s, 3))
    df["ca_persist_is_ext_proxy"] = df["ca_persist_3y"].notna()

    # --- 11. real exchange rate vs USD, 3-year percent change ---
    # xrusd is local currency per USD. RER = e * P_US / P_i
    xrusd = pd.to_numeric(df.get("xrusd"), errors="coerce")
    us = df.loc[df["country"] == "USA", ["year", "cpi"]].rename(columns={"cpi": "cpi_us"})
    df = df.merge(us, on="year", how="left")
    df["_rer"] = xrusd * df["cpi_us"] / df["cpi"].replace(0, np.nan)
    df["_rer_l3"] = df.groupby("country", sort=False)["_rer"].shift(3)
    df["rer_usd_chg_3y"] = _safe_div(df["_rer"], df["_rer_l3"]) - 1.0
    # USA vs itself is identically ~0 aside from floating error; keep the number.

    # --- 12. real wage, 3-year growth ---
    wage = pd.to_numeric(df.get("wage"), errors="coerce")
    df["_rw"] = _safe_div(wage, pd.to_numeric(df.get("cpi"), errors="coerce"))
    df["_rw_l3"] = df.groupby("country", sort=False)["_rw"].shift(3)
    df["real_wage_g_3y"] = _safe_div(df["_rw"], df["_rw_l3"]) - 1.0

    # --- 13. credit/GDP gap vs trailing 5-year mean ---
    tloans = pd.to_numeric(df.get("tloans"), errors="coerce")
    df["_credit_gdp"] = _safe_div(tloans, gdp)
    # Pre-registered window sweep {5,7,10}; primary remains credit_gap_5y.
    for w in CREDIT_GAP_WINDOWS:
        tr = df.groupby("country", sort=False)["_credit_gdp"].transform(
            lambda s, win=w: _trailing_mean(s, win)
        )
        df[f"credit_gap_{w}y"] = df["_credit_gdp"] - tr

    extra_gaps = [f"credit_gap_{w}y" for w in CREDIT_GAP_WINDOWS if f"credit_gap_{w}y" not in INDICATORS]
    keep = ["country", "year"] + INDICATORS + extra_gaps + PROXY_FLAGS
    out = df[keep].copy()
    out.attrs["indicators"] = list(INDICATORS)
    out.attrs["proxies"] = {
        "int_rev": "debt_gdp * ltrate * gdp / revenue (JST has no interest-expense series)",
        "primary_bal_gdp": " (revenue-expenditure)/gdp + debt_gdp*ltrate ; expenditure treated as total",
        "ca_persist_3y": "3y mean CA/GDP; JST has no external-funding share of sovereign debt",
    }
    return out


def coverage_table(ind: pd.DataFrame, indicators: Iterable[str] | None = None) -> pd.DataFrame:
    """Per country, per indicator: n, first year, last year, share non-null."""
    indicators = list(indicators or INDICATORS)
    rows = []
    years_all = ind.groupby("country")["year"]
    n_years = years_all.nunique().to_dict()
    for country, g in ind.groupby("country", sort=False):
        rec = {"country": country, "n_years": int(n_years[country])}
        for col in indicators:
            s = g[col]
            ok = s.notna()
            rec[f"{col}_n"] = int(ok.sum())
            rec[f"{col}_share"] = float(ok.mean())
            rec[f"{col}_first"] = int(g.loc[ok, "year"].min()) if ok.any() else pd.NA
            rec[f"{col}_last"] = int(g.loc[ok, "year"].max()) if ok.any() else pd.NA
        rows.append(rec)
    return pd.DataFrame(rows)


def coverage_share_matrix(ind: pd.DataFrame, indicators: Iterable[str] | None = None) -> pd.DataFrame:
    """Country × indicator matrix of non-null shares (easy to print)."""
    indicators = list(indicators or INDICATORS)
    return (
        ind.groupby("country", sort=False)[indicators]
        .apply(lambda g: g.notna().mean())
        .round(3)
    )


def complete_case_mask(ind: pd.DataFrame, indicators: Iterable[str] | None = None) -> pd.Series:
    indicators = list(indicators or INDICATORS)
    return ind[indicators].notna().all(axis=1)
