
"""Minimal HOLE-style toy pipeline.

This package exposes a small, composable API for toy black-hole evaporation,
bit accounting, and generalized-entropy scans inspired by the HOLE framework.
"""

from .evap import EvapParams, lifetime, mass_of_t, temperature_of_t, area_of_t
from .bits import B_bh_bits, B_rad_bits, B_acc_bits
from .chaos import ChaosParams, lyapunov_of_t
from .sgen import (
    SGenParams,
    s_bh_of_t,
    s_rad_of_t,
    s_gen_of_t,
    qes_branches,
    find_page_time,
    find_qes_switch_time,
)
from .pipeline import compute_thresholds
from .config import (
    default_config,
    save_config,
    load_config,
    build_params_from_config,
    run_from_config,
)

__all__ = [
    "EvapParams",
    "ChaosParams",
    "SGenParams",
    "lifetime",
    "mass_of_t",
    "temperature_of_t",
    "area_of_t",
    "B_bh_bits",
    "B_rad_bits",
    "B_acc_bits",
    "lyapunov_of_t",
    "s_bh_of_t",
    "s_rad_of_t",
    "s_gen_of_t",
    "qes_branches",
    "find_page_time",
    "find_qes_switch_time",
    "compute_thresholds",
    "default_config",
    "save_config",
    "load_config",
    "build_params_from_config",
    "run_from_config",
]

__version__ = "0.1.0"
