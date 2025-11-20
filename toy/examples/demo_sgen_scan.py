
"""Example: toy generalized entropy and Page-like crossing."""

import numpy as np
import matplotlib.pyplot as plt

from hole.models.jt import default_jt_params
from hole.evap import lifetime
from hole.sgen import s_bh_of_t, s_rad_of_t, s_gen_of_t, find_page_time


def main():
    evap, chaos, sparams = default_jt_params()
    t_evap = lifetime(evap)
    t = np.linspace(0.0, t_evap, 400)

    S_bh = s_bh_of_t(t, evap, sparams)
    S_rad = s_rad_of_t(t, evap, sparams)
    S_gen = s_gen_of_t(t, evap, sparams)

    t_page, S_page = find_page_time(t, S_bh, S_rad)

    plt.plot(t / t_evap, S_bh, label="S_BH (toy)")
    plt.plot(t / t_evap, S_rad, label="S_rad (toy)")
    plt.plot(t / t_evap, S_gen, label="S_gen = min(S_no,S_island)", alpha=0.7)
    plt.axvline(t_page / t_evap, ls="--", color="k", label="Page-like crossing")

    plt.xlabel("t / t_evap")
    plt.ylabel("entropy (arbitrary units)")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
