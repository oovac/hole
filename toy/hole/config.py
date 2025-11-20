
"""Configuration helpers for HOLE-style toy universes.

This module provides a very lightweight configuration layer that reads
simple JSON files and turns them into the parameter objects used by
the core pipeline:

    EvapParams, ChaosParams, SGenParams, and a visibility profile χ(M).

The goal is to make it easy to exchange and replay complete scenarios
("universes") without editing notebooks: one simply swaps small JSON
files.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Callable, Dict, Any, Tuple, Union

from .evap import EvapParams
from .chaos import ChaosParams
from .sgen import SGenParams
from .pipeline import compute_thresholds


def default_config(M0: float = 1.0) -> Dict[str, Any]:
    """Return a minimal default configuration dictionary."""
    return {
        "evap": {
            "M0": M0,
            "k_hawk": 1e-3,
            "model": "4D_schw",
        },
        "chaos": {
            "alpha_scr": 1.0,
        },
        "sgen": {
            "kappa": 0.0,
        },
        "visibility": {
            "type": "constant",
            "chi0": 0.8,
        },
    }


def save_config(cfg: Dict[str, Any], path: Union[str, Path]) -> None:
    """Save a configuration dictionary to a JSON file."""
    path = Path(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, sort_keys=True)


def load_config(path: Union[str, Path]) -> Dict[str, Any]:
    """Load a configuration dictionary from a JSON file."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def chi_from_visibility_config(vis_cfg: Dict[str, Any]) -> Callable[[float], float]:
    """Construct a visibility profile χ(M) from a config dict.

    Supported forms:

    - type: "constant"
        χ(M) = chi0

    - type: "powerlaw"
        χ(M) = chi0 * (M / M_ref)^p

    - type: "step"
        χ(M) = chi_hi for M >= M_step
             = chi_lo for M <  M_step

    Additional forms can be added without touching the rest of the code.
    """
    vtype = vis_cfg.get("type", "constant")

    if vtype == "constant":
        chi0 = float(vis_cfg.get("chi0", 1.0))

        def chi_const(M: float, _c=chi0) -> float:
            return _c

        return chi_const

    if vtype == "powerlaw":
        chi0 = float(vis_cfg.get("chi0", 1.0))
        M_ref = float(vis_cfg.get("M_ref", 1.0))
        p = float(vis_cfg.get("p", 0.0))

        def chi_powerlaw(M: float, _c=chi0, _mr=M_ref, _p=p) -> float:
            return _c * (M / _mr) ** _p

        return chi_powerlaw

    if vtype == "step":
        chi_hi = float(vis_cfg.get("chi_hi", 1.0))
        chi_lo = float(vis_cfg.get("chi_lo", 0.0))
        M_step = float(vis_cfg.get("M_step", 0.5))

        def chi_step(M: float, _hi=chi_hi, _lo=chi_lo, _ms=M_step) -> float:
            return _hi if M >= _ms else _lo

        return chi_step

    raise ValueError(f"Unsupported visibility type: {vtype!r}")


def build_params_from_config(
    cfg: Dict[str, Any]
) -> Tuple[EvapParams, ChaosParams, SGenParams, Callable[[float], float]]:
    """Build parameter objects and χ(M) from a configuration dictionary."""
    evap_cfg = cfg.get("evap", {})
    chaos_cfg = cfg.get("chaos", {})
    sgen_cfg = cfg.get("sgen", {})
    vis_cfg = cfg.get("visibility", {"type": "constant", "chi0": 1.0})

    evap = EvapParams(**evap_cfg)
    chaos = ChaosParams(**chaos_cfg)
    sgen = SGenParams(**sgen_cfg)
    chi_func = chi_from_visibility_config(vis_cfg)

    return evap, chaos, sgen, chi_func


def run_from_config(
    cfg_or_path: Union[Dict[str, Any], str, Path],
    n_steps: int = 1000,
) -> Dict[str, Any]:
    """Run the high-level pipeline from a configuration dict or JSON file.

    This is a thin convenience wrapper around :func:`compute_thresholds`
    that constructs the parameter objects and χ(M) from a JSON spec and
    returns the full result dictionary.
    """
    if isinstance(cfg_or_path, (str, Path)):
        cfg = load_config(cfg_or_path)
    else:
        cfg = cfg_or_path

    evap, chaos, sgen, chi_func = build_params_from_config(cfg)

    result = compute_thresholds(
        M0=evap.M0,
        chi_func=chi_func,
        evap_params=evap,
        chaos_params=chaos,
        sgen_params=sgen,
        n_steps=n_steps,
    )
    result["config"] = {
        "evap": asdict(evap),
        "chaos": asdict(chaos),
        "sgen": asdict(sgen),
    }
    return result
