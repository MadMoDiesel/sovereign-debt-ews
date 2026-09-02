#!/usr/bin/env python3
"""Go/no-go run against real JST using the official debt_labels.py (§3)."""

from pathlib import Path

import pandas as pd

from debt_labels import (
    COLS,
    label_onsets,
    labels_usable_at,
    prepare_panel,
    sweep_event_counts,
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OVER = ROOT / "overlays"
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)


def load_jst() -> pd.DataFrame:
    dta = DATA / "JSTdatasetR6.dta"
    xlsx = DATA / "JSTdatasetR6.xlsx"
    if dta.exists():
        return pd.read_stata(dta)
    return pd.read_excel(xlsx)


def main() -> None:
    jst = load_jst()
    print("=== schema check ===")
    print("shape", jst.shape)
    print("file columns:", list(jst.columns))
    print("COLS mapping:", COLS)
    for k, v in COLS.items():
        print(f"  {k} -> {v!r} present={v in jst.columns}")
    print("countries:", sorted(jst["country"].astype(str).unique()))
    print("years:", int(jst["year"].min()), int(jst["year"].max()), "rows", len(jst))

    prep = prepare_panel(jst)
    print("debt scale check: raw median", float(jst["debtgdp"].median(skipna=True)),
          "prepared median", float(prep["_debt"].median(skipna=True)))
    print("d3_proxy flag", prep.attrs.get("d3_proxy", False))
    print("bond_tr coverage by country:")
    print(jst.groupby("country")["bond_tr"].apply(lambda s: int(s.notna().sum())).to_string())

    rr = pd.read_csv(OVER / "rr_defaults.csv")
    imf = pd.read_csv(OVER / "imf_programs.csv")
    print("\nRR overlay:\n", rr.to_string(index=False))
    print("IMF overlay:\n", imf.to_string(index=False))

    labels = label_onsets(jst, rr_defaults=rr, imf_programs=imf)
    print("\nparams", labels.attrs.get("params"))
    onsets = labels[labels.onset].copy()
    # attach diagnostics from prepared panel
    diag = prep[["country", "year", "_infl", "_debt", "_debt_lag", "_real_bond_ret"]].copy()
    onsets = onsets.merge(diag, on=["country", "year"], how="left")
    onsets.to_csv(OUT / "onsets_default.csv", index=False)
    labels.to_csv(OUT / "labels_full.csv", index=False)

    print("\n=== Onsets at defaults (infl 20%, debt 60%, real TR -15%, excl 5) ===")
    print(onsets.to_string(index=False))
    print("total onsets:", int(onsets.shape[0]))
    print("by country:\n", onsets.groupby("country").size().to_string())
    print("by rule:\n", onsets["rule"].value_counts().to_string())

    sweep = sweep_event_counts(jst, rr, imf)
    sweep.to_csv(OUT / "sweep.csv", index=False)
    print("\n=== Sweep ===")
    print(sweep.to_string(index=False))
    print("sweep range", int(sweep.n_onsets.min()), "–", int(sweep.n_onsets.max()))

    # US sensitivity
    rr_us = pd.concat([rr, pd.DataFrame({"country": ["USA"], "year": [1933]})], ignore_index=True)
    n_us = int(label_onsets(jst, rr_defaults=rr_us, imf_programs=imf).onset.sum())
    print("\nUS 1933 sensitivity total onsets:", n_us)

    # confirmation-gate smoke: fold T=1978, h=3 → 1975 first usable
    usable = labels_usable_at(labels, train_end=1978, horizon=3)
    print("usable rows at train_end=1978 h=3:", len(usable),
          "max year", int(usable.year.max()) if len(usable) else None)

    print("\n=== Sanity slices ===")
    merged = labels.merge(diag, on=["country", "year"], how="left")
    checks = [
        ("USA", 1933), ("USA", 1971), ("USA", 2008), ("USA", 2009),
        ("UK", 1973), ("UK", 1974), ("UK", 1975), ("UK", 1976),
        ("France", 1945), ("France", 1946), ("France", 1947),
        ("Japan", 1942), ("Japan", 1945), ("Japan", 1946),
        ("Germany", 1923), ("Germany", 1932), ("Germany", 1948),
        ("Italy", 1974), ("Italy", 1977),
        ("Portugal", 1892), ("Portugal", 2010), ("Portugal", 2011),
        ("Ireland", 2010), ("Spain", 1936),
    ]
    for c, y in checks:
        row = merged[(merged.country == c) & (merged.year == y)]
        if row.empty:
            print(f"  {c} {y}: not in panel")
            continue
        r = row.iloc[0]
        print(
            f"  {c} {y}: onset={bool(r.onset)} rule={r.rule or '-'} "
            f"fired_raw={r.rule or ('excl' if r.in_exclusion else '-')} "
            f"excl={bool(r.in_exclusion)} infl={r._infl} "
            f"debt_lag={r._debt_lag} real_btr={r._real_bond_ret}"
        )

    recent = onsets[onsets.year >= 2008]
    print("\n2008-present onsets:")
    print(recent[["country", "year", "rule"]].to_string(index=False) if len(recent) else "  none")


if __name__ == "__main__":
    main()
