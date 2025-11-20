
"""Toy evaporation law for a 4D Schwarzschild-like black hole.

We use a simple analytic model

    dM/dt = -k_hawk / M^2,

which integrates to

    M(t)^3 = M0^3 - 3 k_hawk t.

This captures the qualitative scaling of the evaporation time without
committing to a detailed spectral model. In a more realistic HOLE
implementation, this module would be replaced by a quadrature over
greybody factors and particle content.
"""

from dataclasses import dataclass
from typing import Union

import numpy as np
import math


ArrayLike = Union[float, "np.ndarray"]


@dataclass
class EvapParams:
    """Parameters for the toy evaporation law.

    Attributes
    ----------
    M0 :
        Initial mass in Planck units.
    k_hawk :
        Effective evaporation coefficient. Larger values correspond to
        faster evaporation (e.g. more particle species or superradiant
        enhancement in a Kerr-like scenario).
    model :
        A free-form label for the effective model (e.g. "4D_schw",
        "Kerr_a0.9_toy", "JT", "SYK").
    """

    M0: float = 1.0
    k_hawk: float = 1e-3
    model: str = "4D_schw"


def lifetime(params: EvapParams) -> float:
    """Total evaporation time t_evap for the toy law.

    For dM/dt = -k/M^2 we have t_evap = M0^3 / (3k).
    """
    M0, k = params.M0, params.k_hawk
    return M0**3 / (3.0 * k)


def mass_of_t(t: ArrayLike, params: EvapParams):
    """Mass history M(t) for 0 <= t <= t_evap.

    We invert the analytic solution

        M(t)^3 = M0^3 - 3 k t

    and clip at M=0 for numerical safety.
    """
    t_arr = np.asarray(t, dtype=float)
    M0, k = params.M0, params.k_hawk
    inside = np.maximum(M0**3 - 3.0 * k * t_arr, 0.0)
    return inside ** (1.0 / 3.0)


def temperature_of_t(t: ArrayLike, params: EvapParams):
    """Hawking temperature T_H(t) (toy 4D Schwarzschild).

    In Planck units, T_H = 1 / (8π M).
    """
    M = mass_of_t(t, params)
    return 1.0 / (8.0 * math.pi * (M + 1e-16))


def area_of_t(t: ArrayLike, params: EvapParams):
    """Horizon area A(t) (toy 4D Schwarzschild).

    In Planck units, A = 16π M^2.
    """
    M = mass_of_t(t, params)
    return 16.0 * math.pi * M**2
