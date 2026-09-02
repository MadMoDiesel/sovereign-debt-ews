#!/usr/bin/env python3
"""Build indicators on JST R6 and write coverage maps."""

from pathlib import Path

import pandas as pd

from debt_indicators import (
    INDICATORS,
    complete_case_mask,
    construct_indicators,
    coverage_share_matrix,
    coverage_table,
)
from debt_labels import label_onsets

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)


def main() -> None:
    jst = pd.read_stata(ROOT / "data" / "JSTdatasetR6.dta")
    ind = construct_indicators(jst)
    ind.to_csv(OUT / "indicators.csv", index=False)

    share = coverage_share_matrix(ind)
    share.to_csv(OUT / "coverage_share_matrix.csv")
    cov = coverage_table(ind)
    cov.to_csv(OUT / "coverage_by_country.csv", index=False)

    cc = complete_case_mask(ind)
    print("rows", len(ind), "complete-case", int(cc.sum()), f"({cc.mean():.1%})")
    print("\ncoverage share matrix")
    print(share.to_string())

    print("\ncomplete-case rows by country")
    print(ind[cc].groupby("country").size().to_string())

    print("\nfirst/last year with complete case")
    cc_df = ind[cc]
    print(
        cc_df.groupby("country")
        .agg(first=("year", "min"), last=("year", "max"), n=("year", "size"))
        .to_string()
    )

    # how many of the 34 onsets have a complete indicator vector at t?
    rr = pd.read_csv(ROOT / "overlays" / "rr_defaults.csv")
    imf = pd.read_csv(ROOT / "overlays" / "imf_programs.csv")
    lab = label_onsets(jst, rr, imf)
    on = lab[lab.onset][["country", "year", "rule"]]
    merged = on.merge(ind, on=["country", "year"], how="left")
    merged["complete"] = complete_case_mask(merged)
    print("\nonsets with complete indicators at t:",
          int(merged.complete.sum()), "/", len(merged))
    print(merged[["country", "year", "rule", "complete"]].to_string(index=False))
    merged.to_csv(OUT / "onsets_with_indicators.csv", index=False)

    # missingness among onsets, per indicator
    print("\nmissing indicator share ON ONSET years")
    print(merged[INDICATORS].isna().mean().round(3).to_string())


if __name__ == "__main__":
    main()
