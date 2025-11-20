
"""Toy Lyapunov exponents and scrambling parameters."""

from dataclasses import dataclass
from typing import Union

import numpy as np

from .evap import EvapParams, temperature_of_t


ArrayLike = Union[float, "np.ndarray"]


@dataclass
class ChaosParams:
    """Parameters controlling scrambling and Lyapunov exponents.

    The main parameter is α_scr, which rescales the chaos bound

        λ_L <= (2π / β_H) / α_scr,    α_scr >= 1

    and is used here in the toy relation

        λ_L(t) = (2π / β_H(t)) / α_scr.

    More sophisticated models could add explicit time or frequency
    dependence, or draw α_scr from a distribution calibrated to SYK/JT.
    """

    alpha_scr: float = 1.0


def lyapunov_of_t(t: ArrayLike, evap: EvapParams, chaos: ChaosParams):
    """Toy Lyapunov exponent λ_L(t) from T_H(t) and α_scr.

    λ_L(t) = (2π / β_H(t)) / α_scr with β_H=1/T_H.
    """
    import math

    t_arr = np.asarray(t, dtype=float)
    T_H = temperature_of_t(t_arr, evap)
    beta_H = 1.0 / (T_H + 1e-16)
    return (2.0 * math.pi / beta_H) / chaos.alpha_scr
