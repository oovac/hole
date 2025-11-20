
"""Example: drive the pipeline from a JSON configuration file."""

import argparse

import matplotlib.pyplot as plt

from hole import run_from_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        default="examples/hole_config_example.json",
        help="Path to HOLE configuration JSON file.",
    )
    parser.add_argument(
        "--n-steps",
        type=int,
        default=800,
        help="Number of time steps in the evaporation history.",
    )
    args = parser.parse_args()

    result = run_from_config(args.config, n_steps=args.n_steps)

    t = result["t"]
    B_bh = result["B_bh"]
    B_rad = result["B_rad"]
    B_acc = result["B_acc"]

    t_pg_geom = result["t_page_geom"]
    t_pg_op = result["t_page_op"]
    t_hp = result["t_hp"]
    t_qes = result["t_qes_switch"]

    # Bit budgets
    plt.figure()
    plt.plot(t, B_bh, label="B_BH (bits)")
    plt.plot(t, B_rad, label="B_rad (bits)")
    plt.plot(t, B_acc, label="B_acc (bits)")

    if not (t_pg_geom != t_pg_geom):
        plt.axvline(t_pg_geom, ls="--", color="k", label="t_Page^geom")
    if not (t_pg_op != t_pg_op):
        plt.axvline(t_pg_op, ls=":", color="k", label="t_Page^op")
    if not (t_hp != t_hp):
        plt.axvline(t_hp, ls="-.", color="r", label="t_HP (toy)")

    plt.xlabel("t")
    plt.ylabel("bits (arb. units)")
    plt.legend()
    plt.title("Bit budgets from config")
    plt.tight_layout()

    # QES branches
    S_no = result["S_no"]
    S_island = result["S_island"]
    S_gen = result["S_gen"]

    plt.figure()
    plt.plot(t, S_no, label="S_no (toy)")
    plt.plot(t, S_island, label="S_island (toy)")
    plt.plot(t, S_gen, label="S_gen = min(no,island)", lw=2)

    if not (t_qes != t_qes):
        plt.axvline(t_qes, ls="--", color="k", label="t_QES (toy)")

    plt.xlabel("t")
    plt.ylabel("entropy (arb. units)")
    plt.legend()
    plt.title("Toy QES from config")
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
