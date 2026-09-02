#!/usr/bin/env python3
"""Walk-forward on E0: original §6 grid and tiling coverage grid, side by side."""

from pathlib import Path

import pandas as pd
from debt_indicators import INDICATORS, REDUCED_INDICATORS, construct_indicators
from debt_labels import label_onsets
from debt_walkforward import (
    HORIZON,
    brier_score_loss,
    default_folds,
    roc_auc_score,
    run_walkforward,
    tiling_folds,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)


def pooled(preds, spec, model):
    d = preds[(preds.spec == spec) & (preds.model == model) & (preds.outcome_closed)]
    if d.empty or d.y.nunique() < 2:
        return f"{spec} {model}: insufficient (n={len(d)} pos={0 if d.empty else int(d.y.sum())})"
    return (
        f"{spec} {model}: n={len(d)} pos={int(d.y.sum())} "
        f"auc={roc_auc_score(d.y, d.p):.3f} "
        f"brier={brier_score_loss(d.y, d.p):.4f} "
        f"base={d.y.mean():.3f} mean_p={d.p.mean():.3f}"
    )


def main() -> None:
    jst = pd.read_stata(ROOT / "data" / "JSTdatasetR6.dta")
    rr = pd.read_csv(ROOT / "overlays" / "rr_defaults.csv")
    imf = pd.read_csv(ROOT / "overlays" / "imf_programs.csv")
    labels = label_onsets(jst, rr, imf, continuation="E0")
    ind = construct_indicators(jst)

    grids = [
        ("original", default_folds()),
        ("tiling", tiling_folds()),
    ]
    specs = [
        ("E0_full", INDICATORS),
        ("E0_R1", REDUCED_INDICATORS),
    ]
    print("horizon", HORIZON, "E0 onsets", int(labels.onset.sum()))
    all_summ, all_pred = [], []
    for grid_name, folds in grids:
        print(f"\n##### GRID {grid_name} ({len(folds)} folds) #####")
        print([f.name for f in folds])
        for spec_name, cols in specs:
            tag = f"{grid_name}:{spec_name}"
            summ, pred = run_walkforward(ind, labels, feature_cols=cols, folds=folds)
            summ["spec"] = spec_name
            summ["grid"] = grid_name
            if len(pred):
                pred["spec"] = spec_name
                pred["grid"] = grid_name
                all_pred.append(pred)
            all_summ.append(summ)
            live = summ[summ.n_test_pos > 0]
            print(f"--- {tag} live folds (test pos > 0) ---")
            if live.empty:
                print("  none")
            else:
                print(live[["fold", "model", "n_train_pos", "n_test",
                            "n_test_pos", "auc", "brier"]].to_string(index=False))

    summary = pd.concat(all_summ, ignore_index=True)
    preds = pd.concat(all_pred, ignore_index=True)
    summary.to_csv(OUT / "walkforward_summary.csv", index=False)
    preds.to_csv(OUT / "walkforward_predictions.csv", index=False)

    print("\n===== pooled closed OOS =====")
    for grid in ("original", "tiling"):
        for spec in ("E0_full", "E0_R1"):
            sub = preds[(preds.grid == grid) & (preds.spec == spec)]
            for model in ("M1", "M2"):
                print(grid, pooled(sub.assign(spec=spec), spec, model))


if __name__ == "__main__":
    main()
