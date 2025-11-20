
\"\"\"Evaporation trajectory using the full spectral efficiency F(T).

We integrate a simplified mass-loss law of the form

    dM/dt = - C * F(T_H(M)) / M^2,

where F(T) is the spectral efficiency defined in :mod:`ft_model`.
The overall constant C cancels when we rescale time to the
dimensionless variable τ = t/t_evap, so we set C=1 in code.fileciteturn0file1turn0file2

The output trajectory is expressed in terms of

    τ ∈ [0,1],
    M(τ)/M0,
    T_H(τ)/T_H(M0),
    S_BH(τ) and S_rad(τ),

in the same format as ``fullsim_trajectory.csv`` used in the paper.
\"\"\"

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Tuple

import numpy as np
import math

from .ft_model import F_of_T


@dataclass
class FullSimParams:
    \"\"\"Parameters of the full F(T) evaporation.

    Attributes
    ----------
    M0 : float
        Initial mass (in arbitrary units).
    T0 : float
        Initial Hawking temperature (Kelvin) used for normalization.
        For a 4D Schwarzschild black hole we would have
        T_H(M) ∝ 1/M, so T0 ∝ 1/M0.
    n_steps : int
        Number of time steps in the evolution.
    \"\"\"

    M0: float = 1.0
    T0: float = 1.227e12
    n_steps: int = 8000


def T_H(M: float, T0: float, M0: float) -> float:
    \"\"\"Toy Hawking temperature T_H(M) with T_H ∝ 1/M.\"\"\"
    return T0 * (M0 / M)


def evolve_trajectory(params: FullSimParams) -> Dict[str, Any]:
    \"\"\"Evolve M(t) using the full F(T) and return the trajectory.

    The integration is performed with an adaptive step that keeps
    the relative mass change per step at the few-per-mille level.
    Time is then rescaled to τ ∈ [0,1].
    \"\"\"
    M0 = params.M0
    T0 = params.T0

    # Storage lists
    t_list = [0.0]
    M_list = [M0]
    T_list = [T_H(M0, T0, M0)]
    S_bh_list = []
    S_rad_list = []

    # Initial entropy
    LOG2 = math.log(2.0)
    S_bh0 = 4.0 * math.pi * M0**2 / LOG2
    S_bh_list.append(S_bh0)
    S_rad_list.append(0.0)

    t = 0.0
    M = M0
    S_bh = S_bh0
    S_rad = 0.0

    # Integrate until M ≈ 0
    while M > 1e-4 * M0:
        T = T_H(M, T0, M0)
        F = F_of_T(T)

        dMdt = -F / (M**2 + 1e-30)

        # adaptive dt: limit relative mass change per step
        dt = 1e-3 * abs(M / (dMdt + 1e-30))
        if not np.isfinite(dt) or dt <= 0:
            break

        # Euler step (sufficient for our purposes)
        M_new = max(M + dMdt * dt, 1e-6 * M0)
        t_new = t + dt

        # Entropy update: S_BH ∝ M^2
        S_bh_new = 4.0 * math.pi * M_new**2 / LOG2
        dS_bh = S_bh_new - S_bh
        S_rad_new = S_rad - dS_bh  # enforce S_BH + S_rad = const

        # store
        t_list.append(t_new)
        M_list.append(M_new)
        T_list.append(T_H(M_new, T0, M0))
        S_bh_list.append(S_bh_new)
        S_rad_list.append(S_rad_new)

        # advance
        t, M, S_bh, S_rad = t_new, M_new, S_bh_new, S_rad_new

        if len(t_list) >= params.n_steps:
            break

    t_arr = np.array(t_list)
    M_arr = np.array(M_list)
    T_arr = np.array(T_list)
    S_bh_arr = np.array(S_bh_list)
    S_rad_arr = np.array(S_rad_list)

    t_evap = t_arr[-1]
    tau_arr = t_arr / t_evap
    M_norm = M_arr / M0
    T_norm = T_arr / T0

    # locate Page point: S_BH ≈ S_rad
    diff = np.abs(S_bh_arr - S_rad_arr)
    idx_page = int(np.argmin(diff))
    tau_page = float(tau_arr[idx_page])
    M_page = float(M_norm[idx_page])

    return {
        "t": t_arr,
        "tau": tau_arr,
        "M_over_M0": M_norm,
        "T_over_T0": T_norm,
        "S_bits": S_bh_arr,
        "bits_emitted": S_rad_arr,
        "t_evap": t_evap,
        "tau_page": tau_page,
        "M_page_over_M0": M_page,
    }


def generate_trajectory(params: FullSimParams, path: str) -> None:
    \"\"\"Generate a CSV trajectory file in the format used by the paper.

    The columns are:

        tau, M_over_M0, T_over_T0, S_bits, bits_emitted

    which matches the structure of ``fullsim_trajectory.csv``.fileciteturn0file2
    \"\"\"
    import csv

    traj = evolve_trajectory(params)

    tau = traj["tau"]
    M_over_M0 = traj["M_over_M0"]
    T_over_T0 = traj["T_over_T0"]
    S_bits = traj["S_bits"]
    bits_emitted = traj["bits_emitted"]

    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tau", "M_over_M0", "T_over_T0", "S_bits", "bits_emitted"])
        for i in range(len(tau)):
            w.writerow([
                f"{tau[i]:.8e}",
                f"{M_over_M0[i]:.8e}",
                f"{T_over_T0[i]:.8e}",
                f"{S_bits[i]:.8e}",
                f"{bits_emitted[i]:.8e}",
            ])
