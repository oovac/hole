
"""Example: full HOLE-style toy pipeline."""

import numpy as np
import matplotlib.pyplot as plt

from hole import compute_thresholds


def chi_const(M: float) -> float:
    """Toy constant visibility χ(M) = 0.8."""
    return 0.8


def main():
    result = compute_thresholds(M0=1.0, chi_func=chi_const, n_steps=800)

    t = result["t"]
    B_bh = result["B_bh"]
    B_rad = result["B_rad"]
    B_acc = result["B_acc"]

    t_pg_geom = result["t_page_geom"]
    t_pg_op = result["t_page_op"]
    t_hp = result["t_hp"]
    t_qes = result["t_qes_switch"]

    # 1) Bit budgets and Page/HP thresholds
    plt.figure()
    plt.plot(t, B_bh, label="B_BH (bits)")
    plt.plot(t, B_rad, label="B_rad (bits)")
    plt.plot(t, B_acc, label="B_acc (bits)")

    plt.axvline(t_pg_geom, ls="--", color="k", label="t_Page^geom")
    if not np.isnan(t_pg_op):
        plt.axvline(t_pg_op, ls=":", color="k", label="t_Page^op")
    if not np.isnan(t_hp):
        plt.axvline(t_hp, ls="-.", color="r", label="t_HP (toy)")

    plt.xlabel("t")
    plt.ylabel("bits (arb. units)")
    plt.legend()
    plt.title("Bit budgets and toy thresholds")
    plt.tight_layout()

    # 2) Toy QES branches
    S_bh = result["S_bh"]
    S_rad = result["S_rad"]
    S_gen = result["S_gen"]
    S_no = result["S_no"]
    S_island = result["S_island"]

    plt.figure()
    plt.plot(t, S_bh, label="S_BH (toy)")
    plt.plot(t, S_rad, label="S_rad (toy)")
    plt.plot(t, S_no, label="S_no (branch)", alpha=0.7)
    plt.plot(t, S_island, label="S_island (branch)", alpha=0.7)
    plt.plot(t, S_gen, label="S_gen = min(no,island)", lw=2)

    if not np.isnan(t_qes):
        plt.axvline(t_qes, ls="--", color="k", label="t_QES (toy)")

    plt.xlabel("t")
    plt.ylabel("entropy (arb. units)")
    plt.legend()
    plt.title("Toy QES branches and switch")
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
