
# HOLE Toy Pipeline

This repository provides a minimal, self-contained Python implementation of a toy HOLE-style
information pipeline for black hole evaporation and information thresholds.

The goal is not high-precision numerics, but a clean, readable reference implementation that
mirrors the conceptual structure of the HOLE framework:

- an evaporation law for the black hole mass `M(t)`,
- bit budgets (`B_BH`, `B_rad`, `B_acc`) and Page points,
- a toy generalized entropy `S_gen(t)` with Page/QES-like transitions.

The core design principle is **separation of concerns**:

- `hole.evap`      — background evaporation (`M(t)`, `T_H(t)`, `A(t)`),
- `hole.bits`      — entropy/bit accounting and operational Page masses,
- `hole.chaos`     — Lyapunov exponents and scrambling parameters,
- `hole.sgen`      — generalized entropy and QES-like transitions,
- `hole.pipeline`  — a high-level `compute_thresholds(...)` orchestration API,
- `hole.config`    — a JSON-based configuration layer,
- `hole.models.*`  — presets for toy JT/SYK-like effective models.

Everything is written to be easy to extend with more realistic spectral models, SYK/JT-inspired
effective parameters, or observational priors (e.g. from shadows / photon rings).

## Installation

```bash
git clone https://github.com/ordovacui/hole-toy.git
cd hole-toy
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Quickstart

The simplest way to see the pipeline in action is to run the example:

```bash
python examples/demo_full_pipeline.py
```

This will:

- construct a simple evaporation law for a Schwarzschild-like black hole,
- compute geometric and operational Page points,
- evaluate a toy generalized entropy and a QES-like switch,
- plot the corresponding curves.

Alternatively, you can drive the pipeline via a JSON configuration file:

```bash
python examples/demo_config_pipeline.py         --config examples/hole_config_example.json
```

## Core API

The main entry point is:

```python
from hole import compute_thresholds

def chi_const(M: float) -> float:
    return 0.8  # toy visibility profile χ(M)

result = compute_thresholds(M0=1.0, chi_func=chi_const)

print("Geometric Page mass:", result["M_page_geom"])
print("Operational Page mass:", result["M_page_op"])
print("Toy QES switch time:", result["t_qes_switch"])
```

The returned `result` dictionary contains:

- `t`          — time grid from `t=0` to the evaporation time `t_evap`,
- `M`          — mass history `M(t)`,
- `B_bh`       — black hole entropy/bit budget as a function of time,
- `B_rad`      — radiated bits,
- `B_acc`      — accessible/operational bits for the chosen `χ(M)`,
- `t_page_geom`, `M_page_geom` — geometric Page time/mass,
- `t_page_op`,   `M_page_op`   — operational Page time/mass,
- `t_hp`        — a toy proxy for a Hayden–Preskill-like threshold,
- `S_bh`, `S_rad`, `S_gen`     — toy generalized-entropy branches,
- `t_page_qes`                  — Page-like crossing in the entropy picture,
- `S_no`, `S_island`            — toy QES branches,
- `t_qes_switch`                — toy QES switch time.

The parameters used are returned under:

```python
result["params"]["evap"]   # EvapParams
result["params"]["chaos"]  # ChaosParams
result["params"]["sgen"]   # SGenParams
```

Users who want to connect this to more microscopic models (SYK, JT, etc.) are expected to
modify or extend:

- `EvapParams` (for evaporation rate and geometry),
- `ChaosParams` (for scrambling strength and Lyapunov exponents),
- `SGenParams` (for the generalized entropy map).

## Config-driven universes

To make it easy to exchange and replay complete scenarios without editing
notebooks, the repository includes a small configuration layer in
`hole/config.py` and JSON files under `examples/` and `configs/`.

A typical configuration looks like:

```json
{
  "evap": {
    "M0": 1.0,
    "k_hawk": 0.001,
    "model": "4D_schw"
  },
  "chaos": {
    "alpha_scr": 1.0
  },
  "sgen": {
    "kappa": 0.0
  },
  "visibility": {
    "type": "constant",
    "chi0": 0.8
  }
}
```

The helper

```python
from hole import run_from_config

result = run_from_config("examples/hole_config_example.json", n_steps=800)
```

runs the full `compute_thresholds` pipeline with parameters specified in
the JSON file. Different universes (different evaporation/scattering
assumptions, visibility profiles, or toy JT/SYK presets) correspond to
different JSON files.

For reproducibility of the paper-level scenarios, the directory
`configs/paper/` contains named configurations such as
`paper_figure_7_schw.json` and `paper_figure_9_kerr.json`, which can be
aligned with specific figures in the main text.

This mirrors the conceptual picture of a **universal threshold operator**:
we treat

```python
compute_thresholds(M0, chi_func, evap_params, chaos_params, sgen_params)
```

as the abstract operator that maps effective model data to information
thresholds, and the JSON files as concrete instantiations of that data.

## Toy nature and limitations

This code is deliberately minimal and pedagogical:

- The evaporation law uses a simple `dM/dt ∝ -1/M^2` model with a tunable constant,
  providing the correct qualitative scaling without committing to a specific spectral model.
- The bit accounting follows the usual `S_BH ∝ M^2` scaling and implements the operational
  Page mass in terms of a visibility-weighted bit budget.
- The generalized entropy module implements a one-dimensional toy model:
  two branches `S_no(t)` and `S_island(t)` built from `S_BH(t)` and `S_rad(t)` with a tunable
  mixing parameter.

None of this should be mistaken for a precision numerical implementation of a concrete
holographic or SYK/JT model. It is a **reference pipeline** that makes the logic of HOLE-like
information thresholds explicit and testable in code.

## License

MIT, or whatever you prefer for your project. This file is a template; adjust authorship,
references, and license texts to match your paper and collaboration.
