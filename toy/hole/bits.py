
"""Bit/entropy accounting for the toy HOLE pipeline."""

import math
from typing import Union

import numpy as np

ArrayLike = Union[float, "np.ndarray"]
LOG2 = math.log(2.0)


def B_bh_bits(M: ArrayLike):
    """Black-hole entropy/bit budget in bits.

    B_BH(M) = 4π M^2 / ln 2  (toy 4D Schwarzschild, Planck units).
    """
    M_arr = np.asarray(M, dtype=float)
    return (4.0 * math.pi / LOG2) * M_arr**2


def B_rad_bits(M: ArrayLike, M0: float):
    """Radiated bits between M0 and M.

    B_rad(M) = B_BH(M0) - B_BH(M).
    """
    M_arr = np.asarray(M, dtype=float)
    return (4.0 * math.pi / LOG2) * (M0**2 - M_arr**2)


def B_acc_bits(M_array, M0: float, chi_func=lambda M: 1.0):
    """Accessible bits with a visibility profile χ(M).

    We implement

        B_acc(M) = (8π/ln 2) ∫_M^{M0} χ(M') M' dM'

    on a grid M_array that is assumed to be monotonically decreasing
    from M0 to a final mass. The returned array has B_acc(M0) = 0 and
    grows as M decreases.
    """
    M = np.asarray(M_array, dtype=float)
    if M[0] < M[-1]:
        raise ValueError(
            "M_array is expected to be monotonically decreasing from M0."
        )

    h = np.array([chi_func(m) * m for m in M], dtype=float)

    I = np.zeros_like(M)
    for i in range(1, len(M)):
        dM = M[i - 1] - M[i]  # > 0
        I[i] = I[i - 1] + 0.5 * (h[i - 1] + h[i]) * dM

    return (8.0 * math.pi / LOG2) * I
