# Installing BigDFT on Fugaku

Use this reference for a Fujitsu cross build from an x86_64 login node to
A64FX compute nodes. Start with the selected source tree's
`rcfiles/fugaku_cross.rc`; native compute-node builds use a different recipe.
Keep changes in the rcfile wherever they express compiler or library choices.

## Check the recipe before building

- The Autotools host must describe AArch64, for example
  `aarch64-unknown-linux-gnu`. Older Fugaku rcfiles still contain
  `sparc-fujitsu-linux` and obsolete Spack setup examples.
- Use Fujitsu cross wrappers (`mpifrtpx`, `fccpx`, `FCCpx`) and SSL2
  consistently. Do not select the login node's GNU compilers for a dependency.
- Inspect `modulesets/hpc-upstream.modules`: libxc 7 uses CMake. Give libxc
  explicit Fujitsu C/Fortran compilers and an AArch64 target in
  `module_cmakeargs['libxc']`. Do the same for NTPoly, preserving the recipe's
  SSL2, OpenMP, and Fortran module-directory settings. Autotools flags alone
  leave CMake free to select host compilers.
- On a shared login node, choose modest build parallelism instead of the
  installer's automatic CPU-count-plus-one setting. Four build processes
  were used for the validated installation; follow the site's build policy.
- Use a separate build directory, with enough project storage for objects,
  installed libraries, and runtime output.

## Installer Python environment

Use an isolated host-side virtual environment. Avoid inheriting system site
packages: inaccessible package metadata can break pip before it installs
anything. Check the interpreter and pip versions before selecting dependencies.

For a login node whose available interpreter is Python 3.6.8, this combination
was used successfully:

```bash
python3 -m venv /path/to/bigdft-tools  # FILL: host-side tools environment
/path/to/bigdft-tools/bin/python -m pip install --upgrade \
    pip==21.3.1 setuptools==59.6.0 wheel==0.37.1
/path/to/bigdft-tools/bin/python -m pip install \
    six future==0.18.3 PyYAML==6.0.1 cmake==3.22.6
```

These pins are a compatibility example for that older interpreter, not a
requirement for a newer Python. This environment's Python extension wheels
and CMake executable target the login node; do not assume they run on A64FX.

## Build and diagnose

Run `Installer.py autogen -y` for a Git checkout, then build with the selected
rcfile and the host tools environment on `PATH`. Record the source commit,
recipe, build output, and exit status. For a long build, use the site's
supported execution mechanism and persistent logs so a client disconnect
does not discard the evidence.

Check these observed failure modes before changing unrelated source code:

- **Futile cannot find libyaml after skipping PyYAML:** Futile needs the
  target C libyaml even when the host Python already imports `yaml`.
  Inspect the expanded dependency list. It must include libyaml independently
  of the skipped Python package. A host PyYAML installation is not a target
  libyaml installation.
- **libABINIT cannot import libxc modules:** inspect libxc's CMake cache and
  module producer first. GNU-generated host modules cannot be consumed by
  Fujitsu Fortran. Reconfigure and rebuild libxc with the corrected rcfile;
  do not bypass the module/link checks.
- **PSolver's Fock utility fails to link `main`:** compare its Fortran link
  recipe with PSolver's other programs. With TCS 1.2.43, removing the extra
  `$(FCLIBS)` from `Fock_LDADD` resolved this failure; the Fortran driver
  already supplies its runtime libraries.

When changing CMake compiler settings in an existing tree, force the affected
dependency to reconfigure rather than relying on the default update policy
or a previous successful host installation. Inspect the resulting cache.

## Validate on compute nodes

Before benchmarking, check that the executable is AArch64, its runtime
libraries resolve, the SCF calculation reports success, and the logfile's MPI
and OpenMP counts match the requested layout. Compare one-rank and multi-node
results and run an upstream numerical regression case. A scheduler `completed`
state alone does not establish application success.

The validated baseline used Fujitsu Fortran 4.12.2 / TCS 1.2.43 and source
commit `213bc56f51b9e990fe5b9f035402f36d01b19816`, with the libyaml dependency
and Fock link fixes described above. Water energies across one rank and two
nodes agreed within `5e-14` Ha; the upstream silane reference energy agreed
within `2.1e-8` Ha. This validates those cubic calculations, not every optional
backend or pseudopotential mode.
