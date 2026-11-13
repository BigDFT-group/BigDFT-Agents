# Periodic silicon with localized support functions

Use this when preparing bulk Si in linear mode or diagnosing its convergence.
It recommends a starting point; it does not establish basis, grid, cell-size or
k-point convergence for a new scientific calculation.

## Starting recipe

For a four-valence-electron Si pseudopotential:

```yaml
import: [linear, linear_convergence]
dft:
  inputpsiid: linear
  disablesym: Yes
lin_basis_params:
  Si:
    nbasis: 9
    rloc: 8.0              # bohr; verify the actual localization grids fit
ig_occupation:
  Si:
    3s: 2.0
    3p: 2.0
    3d: 0.0
perf:
  hamapp_radius_incr: 6    # preserve the profile's Hamiltonian padding
```

Supply the user's geometry/cell, XC, grid and pseudopotential explicitly. The
validated example used PBE, HGH-K + NLCC, `hgrids: 0.5` bohr and Gamma-point
periodic Si216 in a 16.293 angstrom cubic cell. These describe that benchmark,
not universal accuracy settings. Select the pseudopotential using
`bigdft-pseudopotentials`; neither the convergence profile nor `3d: 0.0`
selects NLCC. Do not change the PSP electron count to fill the polarization shell.

The s, p and d shells provide 1+3+5 = 9 initial orbitals. Their initial
occupations still sum to 2+2+0 = 4 electrons/Si; the zero d occupation is
intentional. Include it even if the built-in Si occupation lists only s/p.
The source rejects `nbasis` larger than the available initial atomic-orbital
count. An upstream Si regression input also uses nine functions with an empty
d shell; its molecular-test radii and confinement are not bulk defaults.

## Cell fit and initialization

Check the expanded input and memory-estimation/dry-run output for both the
support-function grid and its extended Hamiltonian grid. Wavelet buffers and
Hamiltonian padding matter; a check using only `2*rloc < cell length` is
insufficient. More MPI ranks do not make a geometrically oversized grid fit.

In the tested Si64 cell, `rloc: 8.0` failed before SCF because the support grid
was 95 cubed while the global grid was 84 cubed. Reducing the radius to 6.5
still failed: the extended Hamiltonian grid was 107 cubed. Reducing the radius
to 6 and padding to 1 made the run fit but produced extensive boundary/trace
warnings and poor convergence. Avoid that workaround. If a requested cell
cannot accommodate the intended localization, explain the conflict and propose
a compatible supercell; preserve the user's atom-count limit and geometry.

## What was measured

At the same Si216 geometry, PBE/NLCC, hgrid 0.5, radius 8, padding 6 and
`[linear, linear_convergence]` profiles:

| Basis per Si | Outer iterations | Exit result | Final printed energy (Ha) |
| --- | ---: | --- | ---: |
| 4 (s+p) | 100 | Not converged, infocode 1 | -1519.615173759780 |
| 9 (s+p+d, initially empty d) | 35 | Success, infocode 0 | -1519.741587582107 |

The four-function run used 8 nodes; the nine-function run used 16. These data
support choosing the larger basis for this bulk starting point, not a timing
speedup or a claim that four functions can never converge. The nine-function
run's final outer residual was 1.539e-12 and support gradient about 1.99e-3;
there were no support-boundary warnings. Its trace relative error remained
about 2.41e-4 and inner-optimization warnings occurred. Successful termination
does not establish scientific accuracy: inspect these diagnostics and converge
basis/radii/grid separately for the intended observable.

After initialization, verify the expanded basis count and valence electron
count (Si216: 1,944 support functions, 864 valence electrons). Follow outer
energies/residuals and support gradients, and inspect boundary/Tr(H) warnings.
Require successful process exit and `BigDFT infocode: 0` before treating the
run as a completed benchmark. Keep inputs and convergence work equal in code
A/B comparisons; report iteration changes rather than attributing them to speed.

Source references for the tested build:

- [Input-guess orbital-count check](https://gitlab.com/l_sim/bigdft-suite/-/blob/213bc56f51b9e990fe5b9f035402f36d01b19816/bigdft/src/linear/inputguessLinear.f90)
- [Si nine-function regression input](https://gitlab.com/l_sim/bigdft-suite/-/blob/213bc56f51b9e990fe5b9f035402f36d01b19816/bigdft/tests/DFT/linear/base/input.yaml)
