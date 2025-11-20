
# HOLE full spectral simulator (F(T))

This directory contains a minimal but complete implementation of the
greybody-based F(T) evaporation model used in the HOLE analysis. It
is intended to make all quantitative results based on the "full F(T)"
background (including the reference trajectory and Page mass
M_Page/M0 ≈ 0.708) numerically reproducible.fileciteturn0file1turn0file2

## Contents

- `fullsim/greybody.py`:
  particle content and spin-dependent greybody factors χ_s(y), as
  described in the FEID-QIH F(T) report.
- `fullsim/ft_model.py`:
  evaluation of the spectral integral I(T) and efficiency F(T).
- `fullsim/evap_fullsim.py`:
  evaporation law dM/dt ∝ -F(T_H(M))/M^2 and generation of the
  trajectory `{tau, M/M0, T/T0, S_BH, S_rad}`.
- `fullsim/generate_trajectory.py`:
  command-line script producing `fullsim_trajectory.csv`.

## Usage

Install dependencies:

```bash
pip install numpy
```

Generate a trajectory matching the one used in the paper:

```bash
python -m fullsim.generate_trajectory \
    --M0 1.0 --T0 1.227e12 --n-steps 8000 \
    --output files/fullsim/fullsim_trajectory.csv
```

The resulting CSV file has the columns

```text
tau, M_over_M0, T_over_T0, S_bits, bits_emitted
```

and can be used directly by the HOLE analysis notebooks and by the
`HOLE_QIH_FullSim_Report_EN.pdf` report.fileciteturn0file2
