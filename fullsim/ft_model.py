
\"\"\"Spectral integral I(T) and efficiency F(T).

This module evaluates

    I(T) = sum_i g_i ∫_{x=μ_i}^∞ x^3 χ_{s_i}(x/4π) / (e^x ± 1) dx,

with μ_i = m_i c^2/(k_B T), and defines an effective efficiency

    F(T) ∝ I(T),

up to an overall normalization that cancels when working with
F(T)/F(T_0) and with normalized evaporation time τ=t/t_evap.fileciteturn0file1
\"\"\"

from __future__ import annotations

from typing import Tuple

import numpy as np

from .greybody import Species, species_set, chi_s_y, k_B_eV_per_K


def _I_species(T: float, spec: Species, n_x: int = 600) -> float:
    \"\"\"Integral contribution I_i(T) of a single species.

    Parameters
    ----------
    T : float
        Hawking temperature in Kelvin.
    spec : Species
        Particle species (g, m, spin, fermion/boson).
    n_x : int
        Number of points in the x-grid.

    Returns
    -------
    I_i(T) : float
        Dimensionless integral contribution of this species.
    \"\"\"
    m_eV = spec.mass_eV
    s = spec.spin
    fermion = spec.fermion
    g = spec.g

    if m_eV <= 0.0:
        mu = 0.0
    else:
        mu = m_eV / (k_B_eV_per_K * T)

    x_min = max(mu, 1e-6)
    x_max = max(mu + 40.0, 40.0)
    xs = np.linspace(x_min, x_max, n_x)

    y = xs / (4.0 * np.pi)
    chi = chi_s_y(y, s)

    den = np.exp(xs)
    if fermion:
        den = den + 1.0
    else:
        den = den - 1.0
        den[den <= 0] = np.exp(xs[den <= 0])

    integrand = xs**3 * chi / den
    integral = np.trapz(integrand, xs)
    return g * integral


def I_of_T(T: float, n_x: int = 600) -> float:
    \"\"\"Total dimensionless spectral integral I(T).\"\"\"
    return sum(_I_species(T, spec, n_x=n_x) for spec in species_set)


def F_of_T(T: float, n_x: int = 600) -> float:
    \"\"\"Effective spectral efficiency F(T).

    Overall geometric and numerical prefactors are absorbed into the
    units of time; what matters for the evaporation law is the
    relative variation of F(T) along the trajectory.
    \"\"\"
    return I_of_T(T, n_x=n_x)


def normalized_efficiency(T_grid: np.ndarray, T0: float) -> Tuple[np.ndarray, np.ndarray]:
    \"\"\"Return F(T)/F(T0) on a grid.

    Parameters
    ----------
    T_grid : array_like
        Temperatures (Kelvin) where the efficiency is evaluated.
    T0 : float
        Reference temperature (Kelvin).

    Returns
    -------
    T_grid : ndarray
        Same as input, cast to float.
    F_norm : ndarray
        Normalised efficiency F(T)/F(T0).
    \"\"\"
    T_grid = np.asarray(T_grid, dtype=float)
    F_vals = np.array([F_of_T(T) for T in T_grid])
    F0 = F_of_T(T0)
    return T_grid, F_vals / F0
