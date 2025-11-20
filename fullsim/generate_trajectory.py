
"""Command-line entry point to generate fullsim_trajectory.csv.

Usage
-----
python -m fullsim.generate_trajectory --M0 1.0 --T0 1.227e12 \
    --n-steps 8000 --output files/fullsim/fullsim_trajectory.csv
"""

import argparse
from pathlib import Path

from .evap_fullsim import FullSimParams, generate_trajectory


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--M0", type=float, default=1.0)
    p.add_argument("--T0", type=float, default=1.227e12)
    p.add_argument("--n-steps", type=int, default=8000)
    p.add_argument("--output", type=str, default="fullsim_trajectory.csv")
    args = p.parse_args()

    params = FullSimParams(M0=args.M0, T0=args.T0, n_steps=args.n_steps)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    generate_trajectory(params, str(out_path))
    print(f"Wrote trajectory to {out_path}")


if __name__ == "__main__":
    main()
