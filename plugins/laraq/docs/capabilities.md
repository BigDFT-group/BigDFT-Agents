# BigDFT Capabilities Reference

## What BigDFT Is

BigDFT is a **density functional theory (DFT) electronic structure code** that uses
wavelets as its basis set. It is designed for quantum mechanical calculations on
molecules, periodic solids, surfaces, and wires. The Python interface (PyBigDFT)
provides tools for constructing systems, configuring and running calculations, and
analysing results.

BigDFT operates on quantum mechanical wavefunctions. It does **not** do classical
mechanics, force fields, or empirical potentials. All energies and forces come from
solving the Kohn-Sham equations.

---

## Capabilities

### 1. Atomic Structure Construction and Manipulation

Create individual atoms with element symbol and 3D coordinates. Positions can be
given in bohr (default) or angstrom. Access atomic properties such as atomic
number, atomic weight, valence electron count, and forces (after a calculation).
Convert positions between unit systems.

**Modules:** `BigDFT.Atoms`

---

### 2. Fragment and System Assembly

Build molecular or periodic systems from atoms. A **Fragment** is an ordered
collection of atoms (a molecule, residue, or any grouping). A **System** is a
named dictionary of fragments, optionally with a periodic unit cell.

Operations include: computing centroids, net charge, electron count,
inter-fragment distances, geometric transformations (translation, rotation,
alignment, RMSD), and exporting to XYZ, PDB, YAML, or DataFrame formats.
Import structures from XYZ, PDB, MOL2, or directly from a BigDFT logfile.

**Modules:** `BigDFT.Fragments`, `BigDFT.Systems`

---

### 3. Input File Construction

Build BigDFT input parameter sets in Python. Set the DFT exchange-correlation
functional (LDA, PBE, PBE0, HF), real-space grid spacing (hgrids), SCF
convergence thresholds, spin polarisation, magnetic moments per atom,
k-point sampling for periodic systems, dispersion corrections (Grimme D3),
boundary conditions (free/isolated, bulk/periodic, surface, wire), and
pseudopotential selection.

**Modules:** `BigDFT.Inputfiles`

---

### 4. Running DFT Calculations

Execute BigDFT calculations from Python using `SystemCalculator`. Supports a
**dry run mode** (`dry_run=True`) to validate inputs and estimate memory usage
before real HPC submission, which is the recommended first step for any new
calculation. Calculation output is returned as a `Logfile` object.

**Modules:** `BigDFT.Calculators`, `BigDFT.Inputfiles`

---

### 5. Output and Logfile Analysis

Parse and query BigDFT output files. Extract total energy, Hartree energy,
XC energy, atomic forces, stress tensors, DFT parameters, k-points, SCF
convergence history, walltime, and memory usage. Properties that are absent
from the output return `None` rather than raising exceptions.

Multi-step outputs (geometry optimisations, molecular dynamics trajectories)
are handled as indexed containers, supporting iteration over steps and
convergence monitoring.

**Modules:** `BigDFT.Logfiles`

---

### 6. Geometry Optimisation

Relax atomic positions to minimise forces. Configured via the input file with
geometry optimisation settings (method, force threshold, maximum steps).
Convergence history and final geometry are accessible through the logfile.

**Modules:** `BigDFT.Calculators`, `BigDFT.Inputfiles`, `BigDFT.Logfiles`

---

### 7. Molecular Dynamics

Run Born-Oppenheimer molecular dynamics. Configured via the input file with
MD parameters (timestep, thermostat, number of steps). The resulting
trajectory is accessible as a multi-step logfile.

**Modules:** `BigDFT.Calculators`, `BigDFT.Inputfiles`, `BigDFT.Logfiles`

---

### 8. Linear-Scaling Calculations for Large Systems

Run calculations with the linear-scaling solver for systems too large for
conventional cubic-scaling DFT. Requires configuring localisation radii
(rloc) and the number of support functions per atom (nbasis) based on the
element and pseudopotential. Built-in parameters exist for H, C, N, O, F,
Si, P, S, Cl, Na, K, Sn, Ca, Zn, Ni, Cu, Fe, W.

**Modules:** `BigDFT.Calculators`, `BigDFT.Inputfiles`

---

### 9. Fragment Analysis and Complexity Reduction

Analyse large systems by decomposing them into fragments. Compute fragment
purity (quality of fragmentation), fragment bond order (quantifying
inter-fragment interaction), and build interaction graphs. Automatically
partition a system into fragments. Extract charge and multipole moments
from logfiles per fragment. Compute electrostatic interaction energies
between fragments.

**Modules:** `BigDFT.Fragments`, `BigDFT.Systems`, `BigDFT.Interactingfragments`

---

### 10. Density of States and Band Structure

Compute and manipulate the electronic density of states (DoS), including
projected density of states (PDoS) per fragment or atom type. For periodic
systems, extract band structures and k-point-resolved properties from
logfiles.

**Modules:** `BigDFT.DoS`, `BigDFT.Logfiles`

---

### 11. Implicit Solvation

Run calculations with a continuum solvation model. Two cavity types are
available: soft-sphere (fixed van der Waals geometry) and SCCS (cavity
adapts to the electron density self-consistently). Solvation free energy
includes electrostatic, cavitation, dispersion, and repulsion contributions.

**Modules:** `BigDFT.Calculators`, `BigDFT.Inputfiles`

---

### 12. TDDFT Linear Response

Run time-dependent DFT in the linear response regime to compute optical
absorption spectra and excited state properties. Configured via the input
file with TDDFT-specific settings.

**Modules:** `BigDFT.Calculators`, `BigDFT.Inputfiles`, `BigDFT.Logfiles`

---

### 13. File I/O and Interoperability

Read and write structures in XYZ, PDB, MOL2, and YAML formats. Export
results to pandas DataFrames. Interoperate with ASE (Atomic Simulation
Environment). Read and write cube files and other volumetric field formats.
Import/export logfile data as JSON.

**Modules:** `BigDFT.Systems`, `BigDFT.Fragments`, `BigDFT.Logfiles`

---

### 14. Remote HPC Execution

Submit and monitor calculations on remote HPC systems via SSH. Supports
systems with SLURM job schedulers. Configure node count, walltime, partition,
and account. Transfer input files and retrieve results automatically.

**Modules:** `remotemanager` (URL, Computer classes)

---

### 15. Dataset and Parameter Sweep Workflows

Execute Python functions (including BigDFT calculations) across parameter
sweeps on remote HPC systems. Functions are serialised and submitted as
batch jobs. Results are retrieved and stored persistently in YAML databases.
Supports chaining datasets (upstream results feed downstream functions).

**Modules:** `remotemanager` (Dataset class)

---

### 16. Machine Learning Potential Workflows

Train and apply machine learning interatomic potentials using BigDFT
calculations as reference data. Workflows for dataset generation,
training, and validation.

**Modules:** `BigDFT.ML` (and associated training utilities)

---

### 17. Pseudopotential Configuration

Select and configure pseudopotentials used in calculations. Affects the
number of valence electrons (and thus computational cost), accuracy of
core-valence interactions, and linear scaling basis configuration.
Supported types: HGH, HGH-K, HGH-K with NLCC (recommended), Krack,
all-electron.

**Modules:** `BigDFT.Inputfiles`

---

## Not Supported

The following are **not available** in BigDFT. Requests involving these
should be marked not feasible:

- **Spin-orbit coupling** — explicitly not implemented in the current version
- **Classical force fields or molecular mechanics (MM)** — BigDFT is a pure QM code
- **QM/MM hybrid simulations** — not available
- **Projector-augmented wave (PAW) pseudopotentials** — BigDFT uses GTH/HGH pseudopotentials only
- **Arbitrary Gaussian or plane-wave basis sets** — the basis set is wavelets; it cannot be changed
- **Non-DFT wavefunction methods** (MP2, CCSD, etc.) — not available
- **NMR chemical shifts or EPR parameters** — not computed
- **Optical spectra beyond TDDFT linear response** (e.g. GW, BSE) — not available
- **Phonon calculations or lattice dynamics** — not directly available

---

## Module Index

| Module | What it provides |
|---|---|
| `BigDFT.Atoms` | Atom creation, position access and manipulation, unit conversion |
| `BigDFT.Fragments` | Fragment construction, geometric operations, centroid, charge, I/O |
| `BigDFT.Systems` | Multi-fragment system assembly, unit cells, format export |
| `BigDFT.Inputfiles` | DFT input parameter construction and validation |
| `BigDFT.Calculators` | Running DFT calculations, dry-run mode |
| `BigDFT.Logfiles` | Parsing calculation output, energies, forces, convergence |
| `BigDFT.DoS` | Density of states and projected DoS extraction and manipulation |
| `BigDFT.Interactingfragments` | Fragment bond order, purity, interaction graphs, auto-partitioning |
| `BigDFT.ML` | Machine learning potential training and application |
| `remotemanager` | Remote HPC connections, SLURM job submission, dataset workflows |
