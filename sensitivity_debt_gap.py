#!/usr/bin/env python3
"""Named sensitivity: look-ahead-safe last-observation-carried-forward on
debt/GDP so the t-1 60% gate can see wartime holes.

Does not change default label_onsets(). Official rules stay as written.
Filling uses only past values within country (no interpolation, no
back-fill — those would peek at post-war debt).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from debt_labels import label_onsets, prepare_panel

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

WARTIME_WINDOWS = ((1914, 1923), (1939, 1949))


def load_jst() -> pd.DataFrame:
    return pd.read_stata(ROOT / "data" / "JSTdatasetR6.dta")


def locf_debt(jst: pd.DataFrame, wartime_only: bool = False) -> pd.DataFrame:
    df = jst.copy().sort_values(["country", "year"])
    filled_rows = []

    def in_wartime_spell(y0: int, y1: int) -> bool:
        for a, b in WARTIME_WINDOWS:
            if y0 <= b and y1 >= a:
                return True
        return False

    pieces = []
    for country, g in df.groupby("country", sort=False):
        g = g.copy()
        debt = g["debtgdp"]
        if wartime_only:
            # Identify missing spells; fill only those overlapping wartime windows
            # and only from a prior observed value.
            s = debt.copy()
            is_miss = s.isna().to_numpy()
            years = g["year"].to_numpy()
            n = len(s)
            i = 0
            while i < n:
                if not is_miss[i]:
                    i += 1
                    continue
                j = i
                while j < n and is_miss[j]:
                    j += 1
                y0, y1 = int(years[i]), int(years[j - 1])
                if in_wartime_spell(y0, y1) and i > 0 and pd.notna(s.iloc[i - 1]):
                    s.iloc[i:j] = s.iloc[i - 1]
                    filled_rows.append(
                        dict(
                            country=country,
                            gap_start=y0,
                            gap_end=y1,
                            n=j - i,
                            carried_value=float(s.iloc[i - 1]),
                            from_year=int(years[i - 1]),
                        )
                    )
                i = j
            g["debtgdp"] = s
        else:
            before = int(debt.isna().sum())
            g["debtgdp"] = debt.ffill()
            after = int(g["debtgdp"].isna().sum())
            if after < before:
                last = g.loc[g["debtgdp"].notna() & debt.isna(), ["year", "debtgdp"]]
                if len(last):
                    filled_rows.append(
                        dict(
                            country=country,
                            gap_start=int(g.loc[debt.isna(), "year"].min()),
                            gap_end=int(g.loc[debt.isna(), "year"].max()),
                            n=before - after,
                            carried_value=None,
                            from_year=None,
                        )
                    )
        pieces.append(g)

    out = pd.concat(pieces, ignore_index=True)
    out.attrs["fills"] = pd.DataFrame(filled_rows)
    out.attrs["mode"] = "wartime_only" if wartime_only else "full_locf"
    return out


def attach_diag(labels: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    prep = prepare_panel(panel)
    diag = prep[["country", "year", "_infl", "_debt", "_debt_lag", "_real_bond_ret"]]
    return labels.merge(diag, on=["country", "year"], how="left")


def onset_key(df: pd.DataFrame) -> set[tuple]:
    on = df[df.onset]
    return set(zip(on.country, on.year.astype(int), on.rule.fillna("")))


def main() -> None:
    jst = load_jst()
    rr = pd.read_csv(ROOT / "overlays" / "rr_defaults.csv")
    imf = pd.read_csv(ROOT / "overlays" / "imf_programs.csv")

    base_panel_labels = label_onsets(jst, rr, imf)
    base = attach_diag(base_panel_labels, jst)

    war = locf_debt(jst, wartime_only=True)
    war_labels = label_onsets(war, rr, imf)
    war_d = attach_diag(war_labels, war)

    full = locf_debt(jst, wartime_only=False)
    full_labels = label_onsets(full, rr, imf)
    full_d = attach_diag(full_labels, full)

    def summarize(name, lab, orig_panel):
        on = lab[lab.onset].copy()
        print(f"\n=== {name}: {int(on.shape[0])} onsets ===")
        cols = ["country", "year", "rule", "_infl", "_debt_lag", "_real_bond_ret"]
        print(on[cols].to_string(index=False))
        return on

    b = summarize("BASE (no fill)", base, jst)
    w = summarize("WARTIME LOCF", war_d, war)
    f = summarize("FULL LOCF", full_d, full)

    def diff(new, old, title):
        nk = set(zip(new.country, new.year.astype(int)))
        ok = set(zip(old.country, old.year.astype(int)))
        added = sorted(nk - ok)
        lost = sorted(ok - nk)
        print(f"\n=== {title} ===")
        print(f"added {len(added)}: {added}")
        print(f"lost  {len(lost)}: {lost}")
        return added, lost

    add_w, lost_w = diff(w, b, "wartime-only minus base")
    add_f, lost_f = diff(f, b, "full LOCF minus base")

    fills = war.attrs["fills"]
    fills.to_csv(OUT / "sensitivity_debt_gap_fills.csv", index=False)
    print("\n=== wartime fills applied ===")
    print(fills.to_string(index=False))

    # Did the famous holes now have a debt_lag, and did they fire?
    print("\n=== hole diagnostics (wartime LOCF panel) ===")
    holes = [
        ("France", 1945), ("France", 1946), ("France", 1947), ("France", 1948),
        ("Germany", 1922), ("Germany", 1923), ("Germany", 1945), ("Germany", 1948),
        ("Belgium", 1915), ("Belgium", 1940),
        ("Netherlands", 1940), ("Japan", 1945),
        ("Spain", 1936),
    ]
    for c, y in holes:
        row = war_d[(war_d.country == c) & (war_d.year == y)]
        if row.empty:
            print(f"  {c} {y}: missing row")
            continue
        r = row.iloc[0]
        print(
            f"  {c} {y}: onset={bool(r.onset)} rule={r.rule or '-'} "
            f"excl={bool(r.in_exclusion)} infl={r._infl} "
            f"debt_lag={r._debt_lag} real_btr={r._real_bond_ret}"
        )

    # save comparison table
    def tag(lab, col):
        x = lab.loc[lab.onset, ["country", "year", "rule"]].copy()
        x[col] = x["rule"]
        return x.drop(columns="rule")

    cmp = (
        tag(base, "base")
        .merge(tag(war_d, "wartime_locf"), on=["country", "year"], how="outer")
        .merge(tag(full_d, "full_locf"), on=["country", "year"], how="outer")
        .sort_values(["country", "year"])
    )
    cmp.to_csv(OUT / "sensitivity_debt_gap_onsets.csv", index=False)
    b.to_csv(OUT / "onsets_default.csv", index=False)  # unchanged content
    w.to_csv(OUT / "onsets_wartime_locf.csv", index=False)
    f.to_csv(OUT / "onsets_full_locf.csv", index=False)

    print("\nCOUNTS  base", len(b), "wartime", len(w), "full", len(f))


if __name__ == "__main__":
    main()
