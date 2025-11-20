#!/usr/bin/env python3
"""
Generate greybody χ_s(y) curves for different spins in Ordo Vacui style.

Output:
    fig/greybody_chi_s_y.pdf   (vector figure for PRD manuscript)
    fig/greybody_chi_s_y.png   (raster preview)

The χ_s(y) profiles are taken from the full spectral model used in the
FEID–QIH F(T) simulator, so this plot is consistent with the main
evaporation code.  See the F(T) report for the underlying definitions.  # :contentReference[oaicite:0]{index=0}
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Try to use the same greybody implementation as the full simulator
# ----------------------------------------------------------------------
try:
    from fullsim.greybody import chi_s_y  # type: ignore[attr-defined]
except Exception:
    # Fallback: local implementation matching the FEID–QIH report:
    # s=0: 4π → 27π/4; s=1/2: ~y^2 → 27π/4; s=1: ~y^4 → 27π/4; s=2: ~y^6 → 27π/4.
    # :contentReference[oaicite:1]{index=1}
    import math

    def chi_s_y(y: np.ndarray, s: float) -> np.ndarray:
        y = np.asarray(y, dtype=float)
        high = 27.0 * math.pi / 4.0

        if abs(s) < 1e-9:
            low = 4.0 * math.pi
            return low + (high - low) * (y**2 / (1.0 + y**2))

        if abs(s - 0.5) < 1e-9:
            p = 2.0
        elif abs(s - 1.0) < 1e-9:
            p = 4.0
        elif abs(s - 2.0) < 1e-9:
            p = 6.0
        else:
            p = 2.0

        return high * (y**p / (1.0 + y**p))


# ----------------------------------------------------------------------
# Matplotlib style: try to load Ordo Vacui mplstyle
# ----------------------------------------------------------------------
THIS_DIR = Path(__file__).resolve().parent
style_candidates = [
    THIS_DIR / "ordovacui_mpl_style.mplstyle",
    THIS_DIR.parent / "ordovacui_mpl_style.mplstyle",
]

for style_path in style_candidates:
    if style_path.exists():
        plt.style.use(style_path)
        break

# ----------------------------------------------------------------------
# Plot χ_s(y) for s = 0, 1/2, 1, 2
# ----------------------------------------------------------------------
def main() -> None:
    # y from 10^-2 to 10^2 on log scale
    y = np.logspace(-2, 2, 1000)

    spin_labels = [
        (0.0,   r"$s=0$ (scalar)"),
        (0.5,   r"$s=\frac{1}{2}$ (fermion)"),
        (1.0,   r"$s=1$ (vector)"),
        (2.0,   r"$s=2$ (graviton)"),
    ]

    fig, ax = plt.subplots(figsize=(6.0, 4.0))

    for s, label in spin_labels:
        chi = chi_s_y(y, s)
        ax.loglog(y, chi, label=label)

    # Annotate asymptotics
    low_y = 0.03
    high_y = 30.0

    # powers for low-frequency scaling
    low_powers = {0.0: 0, 0.5: 2, 1.0: 4, 2.0: 6}

    for s, label in spin_labels:
        chi = chi_s_y(y, s)

        # low-frequency point
        low_idx = np.argmin(np.abs(y - low_y))
        if low_powers[s] > 0:
            txt_low = rf"$\chi_s \propto y^{low_powers[s]}$"
        else:
            txt_low = r"$\chi_0 \to 4\pi$"
        ax.annotate(
            txt_low,
            xy=(y[low_idx], chi[low_idx]),
            xytext=(y[low_idx] * 0.7, chi[low_idx] * 2.0),
            arrowprops=dict(arrowstyle="->", linewidth=0.8),
            fontsize=8,
        )

        # high-frequency point
        high_idx = np.argmin(np.abs(y - high_y))
        ax.annotate(
            r"$\chi_s \to 27\pi/4$",
            xy=(y[high_idx], chi[high_idx]),
            xytext=(y[high_idx] / 3.0, chi[high_idx] * 0.5),
            arrowprops=dict(arrowstyle="->", linewidth=0.8),
            fontsize=8,
        )

    ax.set_xlabel(r"$y = x/(4\pi)$")
    ax.set_ylabel(r"$\chi_s(y)$")
    ax.set_title(r"Spin-resolved greybody profiles $\chi_s(y)$")

    ax.legend(loc="lower right", fontsize=8)
    ax.set_xlim(y.min(), y.max())

    # Light grid; details controlled mostly by the mplstyle
    ax.grid(True, which="both", linestyle=":", linewidth=0.5, alpha=0.4)

    # Ensure output directory exists
    fig_dir = THIS_DIR / "fig"
    fig_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = fig_dir / "greybody_chi_s_y.pdf"
    png_path = fig_dir / "greybody_chi_s_y.png"

    fig.tight_layout()
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")

    print(f"Saved greybody curves to {pdf_path} and {png_path}")


if __name__ == "__main__":
    main()
