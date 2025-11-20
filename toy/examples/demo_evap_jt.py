
"""Example: evaporation law for a toy JT-like setup."""

import numpy as np
import matplotlib.pyplot as plt

from hole.models.jt import default_jt_params
from hole.evap import lifetime, mass_of_t, temperature_of_t


def main():
    evap, chaos, sgen = default_jt_params()
    t_evap = lifetime(evap)
    t = np.linspace(0.0, t_evap, 400)

    M = mass_of_t(t, evap)
    T = temperature_of_t(t, evap)

    fig, ax1 = plt.subplots()

    ax1.plot(t / t_evap, M / evap.M0, label="M/M0")
    ax1.set_xlabel("t / t_evap")
    ax1.set_ylabel("M/M0")

    ax2 = ax1.twinx()
    ax2.plot(t / t_evap, T, ls="--", label="T_H")
    ax2.set_ylabel("T_H (arb. units)")

    ax1.legend(loc="upper right")
    ax2.legend(loc="upper left")

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
