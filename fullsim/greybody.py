
\"\"\"Greybody factors and particle content for the full F(T) model.

We follow the prescription summarized in the original full-simulation
report ``Ordo Vacui -- Повний симулятор F(T)``:

- The total power is
    P(T) ∝ r_s^2 (k_B T)^4 I(T),
  where I(T) is a dimensionless integral over frequency.

- The integral is
    I(T) = sum_i g_i ∫_{x=μ_i}^∞ x^3 χ_{s_i}(x/4π) / (e^x ± 1) dx,
  with μ_i = m_i c^2 / (k_B T),
  and a spin-dependent greybody profile χ_s(y) interpolating between
  low-frequency absorption and the geometric-optics cross-section.fileciteturn0file1

The spin-dependent greybody factors χ_s(y) are approximated by

    s = 0   :  χ_0(y) ≈ 4π + (27π/4 - 4π) * y^2/(1 + y^2)
    s = 1/2 :  χ_{1/2}(y) ≈ (27π/4) * y^2/(1 + y^2)
    s = 1   :  χ_1(y) ≈ (27π/4) * y^4/(1 + y^4)
    s = 2   :  χ_2(y) ≈ (27π/4) * y^6/(1 + y^6),

which reproduce the expected low-frequency scaling and high-frequency
saturation to the capture cross-section ∼ 27π r_s^2 / 4.

The particle content is taken to be

    photons   (s=1,   g=2, m≈0),
    gravitons (s=2,   g=2, m≈0),
    neutrinos (s=1/2, g=6, m≈0.1 eV),
    e±        (s=1/2, g=4, m=511 keV),
    μ±        (s=1/2, g=4, m=105.7 MeV),
    π        (s=0,   g=3, m=139.6 MeV),

matching the species listed on the first page of the full F(T) report.fileciteturn0file1
\"\"\"

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np


# Physical constants (in SI) are not needed explicitly because the
# overall normalization of F(T) cancels in the normalized quantities.
# We only need m_i c^2 / (k_B) in Kelvin units, which we encode directly.
k_B_eV_per_K = 8.617333262e-5  # Boltzmann constant in eV/K


@dataclass
class Species:
    name: str
    g: int
    mass_eV: float
    spin: float
    fermion: bool


# Particle content used in the full simulation
species_set: List[Species] = [
    Species("photon",   g=2, mass_eV=0.0,        spin=1.0, fermion=False),
    Species("graviton", g=2, mass_eV=0.0,        spin=2.0, fermion=False),
    Species("neutrino", g=6, mass_eV=0.1,        spin=0.5, fermion=True),
    Species("e_pm",     g=4, mass_eV=5.11e5,     spin=0.5, fermion=True),
    Species("mu_pm",    g=4, mass_eV=1.057e8,    spin=0.5, fermion=True),
    Species("pi",       g=3, mass_eV=1.396e8,    spin=0.0, fermion=False),
]


def chi_s_y(y: np.ndarray, s: float) -> np.ndarray:
    \"\"\"Spin-dependent greybody factor χ_s(y).

    Parameters
    ----------
    y : array_like
        Dimensionless frequency y = x / (4π), where x=ℏω/(k_B T).
    s : float
        Spin of the field (0, 1/2, 1, 2).

    Returns
    -------
    χ_s(y) : ndarray
        Dimensionless absorption factor, normalized such that for
        y→∞ it approaches 27π/4 for all spins.
    \"\"\"
    y = np.asarray(y, dtype=float)
    high = 27.0 * np.pi / 4.0

    if abs(s) < 1e-9:
        low = 4.0 * np.pi
        return low + (high - low) * (y**2 / (1.0 + y**2))

    # For s=1/2,1,2 we choose exponents that reproduce the expected
    # low-frequency scaling.
    if abs(s - 0.5) < 1e-9:
        p = 2.0
    elif abs(s - 1.0) < 1e-9:
        p = 4.0
    elif abs(s - 2.0) < 1e-9:
        p = 6.0
    else:
        p = 2.0

    return high * (y**p / (1.0 + y**p))
