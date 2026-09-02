"""
Step 3 — expanding-window walk-forward (research design §6).

Adapters from walkforward_refit.py that carry over:
  * Fold is an explicit (train_end, test window) object.
  * Training labels enter ONLY through labels_usable_at.
  * Standardization is fit on the training window and frozen for test.

What is different from the CCDF engine: annual country panel, h-year-ahead
onset as the outcome, two pre-registered models (M1 L1 logit + country FE,
M2 debt/GDP only).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm

from debt_indicators import INDICATORS, REDUCED_INDICATORS
from debt_labels import labels_usable_at


def roc_auc_score(y, p) -> float:
    y = np.asarray(y).astype(int)
    p = np.asarray(p, dtype=float)
    pos, neg = p[y == 1], p[y == 0]
    if pos.size == 0 or neg.size == 0:
        return float("nan")
    return float(((pos[:, None] > neg).sum() + 0.5 * (pos[:, None] == neg).sum()) / (pos.size * neg.size))


def brier_score_loss(y, p) -> float:
    return float(np.mean((np.asarray(p, dtype=float) - np.asarray(y, dtype=float)) ** 2))

HORIZON = 3
TEST_SPAN = 5
FOLD_ENDS = list(range(1950, 2011, 10)) + [2015]  # §6: {1950, 1960, …, 2015}
C_GRID = (0.05, 0.1, 0.3, 1.0, 3.0, 10.0)
INTERACTION = ("r_minus_g_3y", "debt_gdp")


@dataclass(frozen=True)
class Fold:
    train_end: int
    test_start: int
    test_end: int

    @property
    def name(self) -> str:
        return f"{self.train_end}|{self.test_start}-{self.test_end}"


def default_folds(horizon: int = HORIZON, span: int = TEST_SPAN) -> list[Fold]:
    """Design §6 original: T in {1950, 1960, …, 2015}, test (T, T+5].
    These windows do not abut; half the post-1950 years are never scored."""
    return [Fold(T, T + 1, T + span) for T in FOLD_ENDS]


def tiling_folds(span: int = TEST_SPAN) -> list[Fold]:
    """Coverage correction, pre-registered 2026-08-31: T steps of `span`
    so test windows abut and tile 1951–2020. Rationale is coverage, not
    performance — the original grid discarded half the sample by construction.
    Primary reported design remains default_folds(); this runs beside it."""
    ends = list(range(1950, 2016, span))
    return [Fold(T, T + 1, T + span) for T in ends]


def attach_outcome(frame: pd.DataFrame, labels: pd.DataFrame, horizon: int = HORIZON) -> pd.DataFrame:
    """y = 1 iff an onset occurs in (year, year+horizon] in the same country."""
    onsets = labels.loc[labels.onset, ["country", "year"]].copy()
    onsets["year"] = onsets["year"].astype(int)
    by_cty = {c: set(g.year.astype(int)) for c, g in onsets.groupby("country")}
    y = []
    for c, yr in zip(frame["country"], frame["year"].astype(int)):
        future = by_cty.get(c, set())
        y.append(any((yr < t <= yr + horizon) for t in future))
    out = frame.copy()
    out["y"] = np.array(y, dtype=int)
    return out


def risk_set(labels: pd.DataFrame, drop_onset_years: bool = False) -> pd.DataFrame:
    """in_exclusion rows are out of the risk set.

    Primary design keeps onset years in (y=0 by construction for the
    forward outcome). drop_onset_years=True is the Bussière–Fratzscher
    sensitivity: the onset year is a mechanical negative at peak
    readings, so it leaves the risk set.
    """
    mask = ~labels["in_exclusion"]
    if drop_onset_years:
        mask = mask & ~labels["onset"]
    return labels.loc[mask, ["country", "year"]].copy()


def complete_case(ind: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return ind.dropna(subset=columns).copy()


def _zscore_train_test(
    train: pd.DataFrame, test: pd.DataFrame, columns: list[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Within-country mean/sd on TRAIN only. Frozen for test."""
    stats = (
        train.groupby("country")[columns]
        .agg(["mean", "std"])
    )
    stats.columns = [f"{a}__{b}" for a, b in stats.columns]

    def apply(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        for col in columns:
            mean = df["country"].map(stats[f"{col}__mean"])
            std = df["country"].map(stats[f"{col}__std"]).replace(0, np.nan)
            # country unseen in train → leave NaN, dropped later
            out[col] = (df[col] - mean) / std
        return out

    return apply(train), apply(test)


def _design(df: pd.DataFrame, feature_cols: list[str], fe_cols: list[str]) -> np.ndarray:
    X = df[feature_cols].to_numpy(dtype=float)
    if fe_cols:
        fe = df.reindex(columns=fe_cols, fill_value=0).to_numpy(dtype=float)
        X = np.hstack([X, fe])
    return X


def _fit_logit(X: np.ndarray, y: np.ndarray, C: float):
    """L1-regularized logit via statsmodels. C maps to alpha ≈ 1/C."""
    Xc = sm.add_constant(X, has_constant="add")
    alpha = 0.0 if C >= 50 else 1.0 / max(C, 1e-6)
    model = sm.Logit(y, Xc)
    try:
        res = model.fit_regularized(method="l1", alpha=alpha, disp=False, maxiter=200)
    except Exception:
        res = model.fit(disp=False, maxiter=200, skip_hessian=True)
    return res


def _predict_p(res, X: np.ndarray) -> np.ndarray:
    Xc = sm.add_constant(X, has_constant="add")
    p = np.asarray(res.predict(Xc), dtype=float)
    return np.clip(p, 1e-6, 1 - 1e-6)


def _choose_C(train: pd.DataFrame, feature_cols: list[str], fe_cols: list[str], ycol: str = "y") -> float:
    """Temporal inner split: last 10 feature-years of train as validation."""
    years = np.sort(train["year"].unique())
    if len(years) < 15 or train[ycol].nunique() < 2:
        return 1.0
    cut = years[-10]
    inner_tr = train[train["year"] < cut]
    inner_va = train[train["year"] >= cut]
    if inner_tr[ycol].nunique() < 2 or inner_va[ycol].nunique() < 2:
        return 1.0
    if len(inner_va) < 20 or inner_tr[ycol].sum() < 3:
        return 1.0
    best_C, best = 1.0, -np.inf
    for C in C_GRID:
        try:
            res = _fit_logit(_design(inner_tr, feature_cols, fe_cols), inner_tr[ycol].to_numpy(), C)
            p = _predict_p(res, _design(inner_va, feature_cols, fe_cols))
            score = roc_auc_score(inner_va[ycol], p)
        except Exception:
            continue
        if score > best:
            best_C, best = C, score
    return best_C


def run_fold(
    fold: Fold,
    indicators: pd.DataFrame,
    labels: pd.DataFrame,
    feature_cols: list[str],
    model: str,
    horizon: int = HORIZON,
    drop_onset_years: bool = False,
) -> dict:
    """Fit one model on one fold. Training rows come only from labels_usable_at."""
    usable = labels_usable_at(labels, fold.train_end, horizon)
    train_keys = risk_set(usable, drop_onset_years=drop_onset_years)
    test_keys = risk_set(labels, drop_onset_years=drop_onset_years)
    test_keys = test_keys[
        (test_keys["year"] >= fold.test_start) & (test_keys["year"] <= fold.test_end)
    ]

    cols = ["country", "year"] + feature_cols
    panel = complete_case(indicators[cols], feature_cols)
    panel = attach_outcome(panel, labels, horizon)

    train = panel.merge(train_keys, on=["country", "year"], how="inner")
    test = panel.merge(test_keys, on=["country", "year"], how="inner")
    # test outcomes whose window has not closed in the dataset stay, but we
    # flag them. Data ends 2020; horizon 3 → years >= 2018 are incomplete.
    data_end = int(labels["year"].max())
    test = test.copy()
    test["outcome_closed"] = test["year"] + horizon <= data_end

    used_features = list(feature_cols)
    if model == "M1" and INTERACTION[0] in used_features and INTERACTION[1] in used_features:
        train = train.copy()
        test = test.copy()
        train["rg_x_debt"] = train[INTERACTION[0]] * train[INTERACTION[1]]
        test["rg_x_debt"] = test[INTERACTION[0]] * test[INTERACTION[1]]
        used_features = used_features + ["rg_x_debt"]
    elif model == "M2":
        used_features = ["debt_gdp"]

    train_z, test_z = _zscore_train_test(train, test, used_features)
    train_z = train_z.dropna(subset=used_features)
    test_z = test_z.dropna(subset=used_features)

    # country FE from train countries only
    fe_train = pd.get_dummies(train_z["country"], prefix="fe", drop_first=True)
    fe_cols = list(fe_train.columns)
    train_z = pd.concat([train_z.reset_index(drop=True), fe_train.reset_index(drop=True)], axis=1)
    fe_test = pd.get_dummies(test_z["country"], prefix="fe", drop_first=True)
    for c in fe_cols:
        if c not in fe_test.columns:
            fe_test[c] = 0
    fe_test = fe_test[fe_cols]
    test_z = pd.concat([test_z.reset_index(drop=True), fe_test.reset_index(drop=True)], axis=1)

    rec = dict(
        fold=fold.name,
        train_end=fold.train_end,
        test=f"{fold.test_start}-{fold.test_end}",
        model=model,
        n_train=len(train_z),
        n_train_pos=int(train_z["y"].sum()),
        n_test=len(test_z),
        n_test_pos=int(test_z["y"].sum()),
        n_test_closed=int(test_z["outcome_closed"].sum()) if len(test_z) else 0,
        C=np.nan,
        auc=np.nan,
        brier=np.nan,
    )
    if len(train_z) < 30 or train_z["y"].nunique() < 2 or train_z["y"].sum() < 3:
        rec["status"] = "too_few_train_positives"
        return rec, pd.DataFrame()

    C = 1.0 if model == "M2" else _choose_C(train_z, used_features, fe_cols)
    # M2 is unpenalized-enough: large C
    if model == "M2":
        C = 100.0
    res = _fit_logit(_design(train_z, used_features, fe_cols), train_z["y"].to_numpy(), C)
    if len(test_z) == 0:
        rec.update(status="no_test_rows", C=C)
        return rec, pd.DataFrame()

    p = _predict_p(res, _design(test_z, used_features, fe_cols))
    pred = test_z[["country", "year", "y", "outcome_closed"]].copy()
    pred["p"] = p
    pred["fold"] = fold.name
    pred["model"] = model
    pred["train_end"] = fold.train_end

    scored = pred[pred["outcome_closed"]]
    rec["C"] = C
    rec["status"] = "ok"
    if len(scored) and scored["y"].nunique() == 2:
        rec["auc"] = float(roc_auc_score(scored["y"], scored["p"]))
    if len(scored):
        rec["brier"] = float(brier_score_loss(scored["y"], scored["p"]))
        rec["base_rate_test"] = float(scored["y"].mean())
        rec["mean_p"] = float(scored["p"].mean())
    return rec, pred


def run_walkforward(
    indicators: pd.DataFrame,
    labels: pd.DataFrame,
    feature_cols: list[str] | None = None,
    models: tuple[str, ...] = ("M1", "M2"),
    horizon: int = HORIZON,
    folds: list[Fold] | None = None,
    drop_onset_years: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    feature_cols = list(feature_cols or INDICATORS)
    folds = folds or default_folds(horizon)
    summaries, preds = [], []
    for fold in folds:
        for model in models:
            rec, pred = run_fold(
                fold, indicators, labels, feature_cols, model, horizon,
                drop_onset_years=drop_onset_years,
            )
            summaries.append(rec)
            if len(pred):
                preds.append(pred)
    return pd.DataFrame(summaries), (pd.concat(preds, ignore_index=True) if preds else pd.DataFrame())
