
"""Toy SYK-like model presets.

The parameters here are placeholders; in a realistic setup they would be
derived from explicit SYK numerics (e.g. via OTOCs or spectral form factors)
and then mapped to effective evaporation and scrambling parameters.

The goal of this file is to demonstrate how one might hook a microscopic
model into the HOLE-style pipeline by returning consistent (EvapParams,
ChaosParams, SGenParams).
"""

from ..evap import EvapParams
from ..chaos import ChaosParams
from ..sgen import SGenParams


def default_syk_params(N: int = 32, q: int = 4):
    """Return (EvapParams, ChaosParams, SGenParams) for a toy SYK setup.

    Parameters
    ----------
    N :
        Number of SYK Majorana fermions (placeholder; used only to label
        the configuration).
    q :
        Interaction degree in SYK_q (placeholder).

    Notes
    -----
    The numerical values are not calibrated to an actual SYK simulation.
    They simply demonstrate how one might embed model dependence into
    the parameter objects used by the evaporation and scrambling modules.
    """
    # Example: slightly faster evaporation and stronger scrambling
    evap = EvapParams(M0=1.0, k_hawk=2e-3, model=f"SYK(N={N},q={q})")
    chaos = ChaosParams(alpha_scr=1.2)
    sgen = SGenParams(kappa=0.0)
    return evap, chaos, sgen
