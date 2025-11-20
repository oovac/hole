
"""Toy JT-like model presets.

This module provides simple parameter presets that mimic a JT-like
near-AdS2 evaporation with effectively 4D-like scalings. In a real
implementation these would be informed by a microscopic computation.
"""

from ..evap import EvapParams
from ..chaos import ChaosParams
from ..sgen import SGenParams


def default_jt_params():
    """Return (EvapParams, ChaosParams, SGenParams) for a toy JT setup.

    The values are chosen for simplicity and do not represent a
    specific microscopic model.
    """
    evap = EvapParams(M0=1.0, k_hawk=1e-3, model="JT")
    chaos = ChaosParams(alpha_scr=1.0)
    sgen = SGenParams(kappa=0.0)
    return evap, chaos, sgen
