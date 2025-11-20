
"""High-level HOLE-style toy pipeline.

The central object here is :func:`compute_thresholds`, which acts as a
universal operator mapping effective evaporation and visibility data
to information-theoretic thresholds (Page mass, HP-like time, QES-like
switch).
"""

import math
from typing import Callable, Optional, Dict, Any

import numpy as np

from .evap import EvapParams, lifetime, mass_of_t
from .bits import B_bh_bits, B_rad_bits, B_acc_bits
from .chaos import ChaosParams
from .sgen import (
    SGenParams,
    s_bh_of_t,
    s_rad_of_t,
    s_gen_of_t,
    qes_branches,
    find_page_time,
    find_qes_switch_time,
)


def compute_thresholds(
    M0: float,
    chi_func: Callable[[float], float],
    evap_params: Optional[EvapParams] = None,
    chaos_params: Optional[ChaosParams] = None,
    sgen_params: Optional[SGenParams] = None,
    n_steps: int = 1000,
) -> Dict[str, Any]:
    """High-level HOLE-style toy pipeline.

    Parameters
    ----------
    M0 :
        Initial black-hole mass in Planck units.
    chi_func :
        Visibility profile χ(M) used in the accessible bit budget B_acc.
        It should satisfy 0 <= χ(M) <= 1 in realistic scenarios, but we
        do not enforce this in the toy implementation.
    evap_params :
        Evaporation parameters. If None, a default EvapParams(M0=M0) is used.
    chaos_params :
        Scrambling/Lyapunov parameters. Currently only stored in the output;
        the present toy implementation of B_acc does not depend explicitly
        on λ_L. This is where a more detailed model could be inserted.
    sgen_params :
        Generalized-entropy parameters. If None, SGenParams() is used.
    n_steps :
        Number of time steps in the evaporation history.

    Returns
    -------
    result : dict
        A dictionary containing time and mass grids, bit budgets, Page-point
        estimates, and toy QES-like transition times. See README for a
        summary of the keys.
    """
    evap = evap_params or EvapParams(M0=M0)
    chaos = chaos_params or ChaosParams()
    sparams = sgen_params or SGenParams()

    # Time and mass grids
    t_evap = lifetime(evap)
    t = np.linspace(0.0, t_evap, n_steps)
    M = mass_of_t(t, evap)

    # Bit budgets
    B_bh = B_bh_bits(M)
    B_rad = B_rad_bits(M, M0)
    B_acc = B_acc_bits(M, M0, chi_func)

    # Geometric Page mass/time
    M_page_geom = M0 / math.sqrt(2.0)
    t_page_geom = float(np.interp(M_page_geom, M[::-1], t[::-1]))

    # Operational Page mass/time from B_acc = 1/2 B_BH(M0)
    B_half = 0.5 * B_bh_bits(M0)
    if B_acc[-1] >= B_half:
        M_page_op = float(np.interp(B_half, B_acc, M))
        t_page_op = float(np.interp(M_page_op, M[::-1], t[::-1]))
    else:
        M_page_op = math.nan
        t_page_op = math.nan

    # Toy BH and radiation entropies
    S_bh = s_bh_of_t(t, evap, sparams)
    S_rad = s_rad_of_t(t, evap, sparams)
    S_gen = s_gen_of_t(t, evap, sparams)

    # Page-like crossing in entropy picture
    t_page_qes, S_page_val = find_page_time(t, S_bh, S_rad)

    # Toy QES branches and switch
    S_no, S_island = qes_branches(t, evap, sparams)
    t_qes_switch = find_qes_switch_time(t, S_no, S_island)

    # Toy Hayden–Preskill-like threshold:
    # we take the first time when B_acc >= B_BH(M), i.e. when the
    # accessible bit budget overtakes the remaining black-hole bits.
    diff_hp = B_acc - B_bh
    idx_hp = np.where(diff_hp >= 0.0)[0]
    if len(idx_hp) > 0:
        t_hp = float(t[int(idx_hp[0])])
    else:
        t_hp = math.nan

    return {
        "t": t,
        "M": M,
        "B_bh": B_bh,
        "B_rad": B_rad,
        "B_acc": B_acc,
        "t_page_geom": t_page_geom,
        "M_page_geom": M_page_geom,
        "t_page_op": t_page_op,
        "M_page_op": M_page_op,
        "t_hp": t_hp,
        "S_bh": S_bh,
        "S_rad": S_rad,
        "S_gen": S_gen,
        "t_page_qes": t_page_qes,
        "S_page_val": S_page_val,
        "S_no": S_no,
        "S_island": S_island,
        "t_qes_switch": t_qes_switch,
        "params": {
            "evap": evap,
            "chaos": chaos,
            "sgen": sparams,
        },
    }
