"""Sample-size calculation behind the paper's 50-100 independent-positives claim.

Assumptions (Hanley and McNeil 1982 SE for a single AUC; two-AUC comparison
with correlation rho between scores):
    AUC under the alternative near 0.60
    two-sided alpha = 0.05
    power = 0.80
    n0 >> n1  (here n0 = 1000)
    rho in {0.3, 0.5, 0.7} between M1 and M2 scores

The quantity solved for is n1, the number of independent positives needed to
detect a 0.10 (or 0.05) gap between two paired AUCs.
"""

from __future__ import annotations

import math


def hanley_mcneil_var(auc: float, n1: int, n0: int) -> float:
    q1 = auc / (2.0 - auc)
    q2 = 2.0 * auc * auc / (1.0 + auc)
    return (
        auc * (1.0 - auc)
        + (n1 - 1) * (q1 - auc * auc)
        + (n0 - 1) * (q2 - auc * auc)
    ) / (n1 * n0)


def n1_for_gap(
    gap: float = 0.10,
    auc: float = 0.60,
    n0: int = 1000,
    rho: float = 0.5,
    alpha: float = 0.05,
    power: float = 0.80,
    n1_max: int = 2000,
) -> int:
    # z_0.975 ~ 1.96, z_0.80 ~ 0.84
    z = 1.959963984540054 + 0.841621233572914
    for n1 in range(2, n1_max + 1):
        v = hanley_mcneil_var(auc, n1, n0)
        # paired difference variance ~ 2(1-rho) * v  if both AUCs share v
        se = math.sqrt(2.0 * (1.0 - rho) * v)
        if gap / se >= z:
            return n1
    return n1_max


if __name__ == "__main__":
    print("Hanley-McNeil SE at AUC=0.60, n0=1000")
    for n1 in (4, 7, 10, 21):
        se = math.sqrt(hanley_mcneil_var(0.60, n1, 1000))
        print(f"  n1={n1:4d}  SE={se:.3f}")
    print()
    print("n1 to detect a gap at 80% power, two-sided 5%, n0=1000, AUC=0.60")
    print(f"{'gap':>6} {'rho':>6} {'n1':>6}")
    for gap in (0.10, 0.05):
        for rho in (0.3, 0.5, 0.7):
            print(f"{gap:6.2f} {rho:6.1f} {n1_for_gap(gap=gap, rho=rho):6d}")
