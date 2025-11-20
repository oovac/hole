
"""Full spectral evaporation simulator for HOLE.

This package implements the greybody-based F(T) model and the
resulting evaporation trajectory M(t) used in the main text.
It is designed to reproduce, within numerical accuracy, the
reference trajectory stored in ``files/fullsim/fullsim_trajectory.csv``.
"""

from .greybody import Species, species_set, chi_s_y
from .ft_model import I_of_T, F_of_T, normalized_efficiency
from .evap_fullsim import FullSimParams, evolve_trajectory, generate_trajectory

__all__ = [
    "Species",
    "species_set",
    "chi_s_y",
    "I_of_T",
    "F_of_T",
    "normalized_efficiency",
    "FullSimParams",
    "evolve_trajectory",
    "generate_trajectory",
]
