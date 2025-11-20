
"""Toy generalized entropy and QES-like branches."""

from dataclasses import dataclass
from typing import Union, Tuple

import numpy as np

from .evap import EvapParams, mass_of_t
from .bits import B_bh_bits, B_rad_bits


ArrayLike = Union[float, "np.ndarray"]


@dataclass
class SGenParams:
    """Parameters for the toy generalized entropy.

    In this minimal implementation we use

        S_BH(t)  ∝ B_BH(M(t)),
        S_rad(t) ∝ B_rad(M(t); M0),

    and build two branches

        S_no(t)      ≈ S_rad(t),
        S_island(t)  ≈ S_BH(t) + κ S_rad(t),

    where κ is a toy mixing parameter controlling when/if there is a
    switch between the two branches.

    A more realistic implementation would replace this with the
    generalized entropy of a JT/QES setup, including explicit
    surface positions and bulk entanglement.
    """

    kappa: float = 0.0


def s_bh_of_t(t: ArrayLike, evap: EvapParams, sparams: SGenParams):
    """Toy black-hole entropy S_BH(t) in 'bit units'."""
    M = mass_of_t(t, evap)
    return B_bh_bits(M)


def s_rad_of_t(t: ArrayLike, evap: EvapParams, sparams: SGenParams):
    """Toy radiation entropy S_rad(t) in 'bit units'."""
    M = mass_of_t(t, evap)
    return B_rad_bits(M, evap.M0)


def qes_branches(t: ArrayLike, evap: EvapParams, sparams: SGenParams):
    """Toy QES branches S_no(t), S_island(t).

    S_no(t)      = S_rad(t),
    S_island(t)  = S_BH(t) + κ S_rad(t).
    """
    S_bh = s_bh_of_t(t, evap, sparams)
    S_rad = s_rad_of_t(t, evap, sparams)
    S_no = S_rad
    S_island = S_bh + sparams.kappa * S_rad
    return S_no, S_island


def s_gen_of_t(t: ArrayLike, evap: EvapParams, sparams: SGenParams):
    """Single toy 'generalized entropy' branch S_gen(t) = min(S_no,S_island)."""
    S_no, S_island = qes_branches(t, evap, sparams)
    return np.minimum(S_no, S_island)


def find_page_time(t: ArrayLike, S_bh: ArrayLike, S_rad: ArrayLike):
    """Find a Page-like time where S_BH ≈ S_rad.

    Returns (t_page, S_page), where S_page is the value at the
    crossing (or the closest approach on the discrete grid).
    """
    t_arr = np.asarray(t, dtype=float)
    S_bh_arr = np.asarray(S_bh, dtype=float)
    S_rad_arr = np.asarray(S_rad, dtype=float)

    diff = np.abs(S_bh_arr - S_rad_arr)
    idx = int(np.argmin(diff))
    return float(t_arr[idx]), float(S_bh_arr[idx])


def find_qes_switch_time(t: ArrayLike, S_no: ArrayLike, S_island: ArrayLike):
    """Find first QES-like switch time from S_no to S_island.

    We look for the first sign change in ΔS(t) = S_no - S_island and
    interpolate linearly between the bracketing points. Returns
    NaN if no switch occurs.
    """
    import math

    t_arr = np.asarray(t, dtype=float)
    S_no_arr = np.asarray(S_no, dtype=float)
    S_island_arr = np.asarray(S_island, dtype=float)

    diff = S_no_arr - S_island_arr
    sign = np.sign(diff)
    idx = np.where(sign[:-1] * sign[1:] <= 0)[0]

    if len(idx) == 0:
        return math.nan

    i = int(idx[0])
    t0, t1 = t_arr[i], t_arr[i + 1]
    d0, d1 = diff[i], diff[i + 1]

    if d1 == d0:
        return float(t0)

    frac = -d0 / (d1 - d0)
    return float(t0 + frac * (t1 - t0))
