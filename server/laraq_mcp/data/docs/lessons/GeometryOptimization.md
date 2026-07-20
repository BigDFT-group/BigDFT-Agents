[ BigDFT-suite ![Logo](../_static/logo-bigdft-white.svg) ](../index.html)

Overview

  * [Available Functionalities](../overview/functionality.html)

  * [The BigDFT-suite Package](../overview/package.html)

  * [Publications](../overview/publications.html)

  * [License](../overview/license.html)

Basic Usage

  * [Installation](../users/install.html)

  * [Quick Start - From Python](../school/QuickStart.html)

  * [Quick Start - Command Line](../school/CMDStart.html)

User Guide

  * [User Guide](../users/guide.html)
    * [Environment Variables](../users/guide.html#environment-variables)
    * [BigDFT Training Lessons](../users/guide.html#bigdft-training-lessons)
    * [Tutorials](../users/guide.html#tutorials)
    * [Lessons and Workflows](../users/guide.html#lessons-and-workflows)
      * Geometry Optimization
        * Molecule Example
        * Slab Example
      * [Molecular Dynamics](MolecularDynamics.html)
      * [Complexity Reduction](ComplexityReduction.html)
      * [Comparison To Gaussian Orbitals](Gaussian.html)
      * [Machine Learning](MachineLearning.html)

  * [PyBigDFT API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/index.html)

Developer

  * [BigDFT-suite manifesto](../devel/developers.html)

  * [Futile API](https://l_sim.gitlab.io/bigdft-suite/futile/build/html/index.html)

__[BigDFT-suite](../index.html)

  * [](../index.html)
  * [User Guide](../users/guide.html)
  * Geometry Optimization
  * [ View page source](../_sources/lessons/GeometryOptimization.ipynb.txt)

* * *

# Geometry Optimization

This tutorial will demonstrate the use of PyBigDFT for performing geometry optimization. We will start with a simple example of a molecular system. Then we will move to an advanced example involving a slab of NaCl.

## Molecule Example

Let’s begin with a simple example of an Aflatoxin B1 molecule.
    
    
    [1]:
    
    
    
    cano = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
    

We can use openbabel to create a system from its cannonical smiles representation.
    
    
    [2]:
    
    
    
    from openbabel.openbabel import OBMol, OBConversion, OBBuilder
    conv = OBConversion()
    conv.SetInFormat("can")
    
    mol = OBMol()
    conv.ReadString(mol, cano)
    mol.AddHydrogens()
    
    builder = OBBuilder()
    builder.Build(mol)
    
    
    
    [2]:
    
    
    
    True
    

Then we convert from babel to PyBigDFT. An openbabel structure after calling build is usually not a good starting point. Normally you would do some combination of optimization and conformer search. For our case, we will do geometry optimization followed by a short molecular dynamics run. This will give us a decent geometry, but one that is not the actual minimum.
    
    
    [3]:
    
    
    
    from BigDFT.Interop.BabelInterop import convert_babel_to_system, molecular_dynamics, optimize_system
    sys_start = convert_babel_to_system(mol)
    sys_opt = optimize_system(sys_start)
    sys = molecular_dynamics(sys_opt, 10000, 300)
    
    
    
    /Users/wddawson/Documents/CEA/binaries/bds/install/lib/python3.7/site-packages/BigDFT/IO.py:371: UserWarning: Unsupported bond type had to be set to 1 (i.e. aromatic)
      UserWarning)
    /Users/wddawson/Documents/CEA/binaries/bds/install/lib/python3.7/site-packages/BigDFT/IO.py:371: UserWarning: Unsupported bond type had to be set to 1 (i.e. aromatic)
      UserWarning)
    
    
    
    [4]:
    
    
    
    from BigDFT.Visualization import InlineVisualizer
    viz = InlineVisualizer(400, 300)
    viz.display_system(sys_start, colordict={x: "black" for x in sys_start}, show=False)
    viz.display_system(sys, colordict={x: "blue" for x in sys}, show=True)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

Now we are ready to optimize the geometry of this system suing BigDFT. First, set up a basic calculator and input file.
    
    
    [5]:
    
    
    
    from BigDFT.Calculators import SystemCalculator
    code = SystemCalculator(verbose=False, skip=True)
    
    
    
    [6]:
    
    
    
    from BigDFT.Inputfiles import Inputfile
    inp = Inputfile()
    inp.set_xc("PBE")
    inp.set_hgrid("0.37")
    

BigDFT has a number of built-in geometry optimization methods which we can probe from the documentation.
    
    
    [7]:
    
    
    
    from BigDFT.InputActions import optimize_geometry
    help(optimize_geometry)
    
    
    
    Help on function optimize_geometry in module BigDFT.InputActions:
    
    optimize_geometry(inp, method='FIRE', nsteps=50, betax=4.0, frac_fluct=1.0, forcemax=0)
        Optimize the geometry of the system
    
        Args:
           nsteps (int): maximum number of atomic steps.
           method (str): Geometry optimizer. Available keys:
              * SDCG:   A combination of Steepest Descent and Conjugate Gradient
              * VSSD:   Variable Stepsize Steepest Descent method
              * LBFGS:  Limited-memory BFGS
              * BFGS:   Broyden-Fletcher-Goldfarb-Shanno
              * PBFGS:  Same as BFGS with an initial Hessian obtained from a force
                        field
              * DIIS:   Direct inversion of iterative subspace
              * FIRE:   Fast Inertial Relaxation Engine as described by Bitzek et
                        al.
              * SBFGS:  SQNM minimizer, keyword deprecated, will be replaced by
                        SQNM in future release
              * SQNM:   Stabilized quasi-Newton minimzer
           betax (float): the step size for the optimization method.
              This stepsize is system dependent and it has therefore to be
              determined for each system.
           frac_fluct (float): Fraction of force fluctuations. Stop if
              fmax < forces_fluct*frac_fluct.
           forcemax (float): Max forces criterion when stop.
    
    

Let’s activate the SQNM method. The important parameter to adjust is `betax` which is the step length, and the appropriate value can be sensitive to the method and system being computed. BigDFT automatically computes a measure of the force fluctations that come from the discretization and SCF error. This is used as a convergence measure. If you want to converge tighter, you should consider decreasing hgrid and the wavefunction convergence (`set_wavefunction_convergence`)
    
    
    [8]:
    
    
    
    inp.optimize_geometry(method="SQNM", betax=1.0)
    

And run.
    
    
    [9]:
    
    
    
    log = code.run(input=inp, posinp=sys.get_posinp(), name="caf", run_dir="work")
    
    
    
    Found 27 different runs
    

We will also do a calculation using implicit solvent.
    
    
    [10]:
    
    
    
    from copy import deepcopy
    inp2 = deepcopy(inp)
    inp2.set_implicit_solvent()
    
    
    
    [11]:
    
    
    
    log_imp = code.run(input=inp2, posinp=sys.get_posinp(), name="caf-imp", run_dir="work")
    
    
    
    Found 55 different runs
    

The first thing we want to do is extract the energies at each step of the geometry optimization and plot them.
    
    
    [12]:
    
    
    
    energy = []
    forces = []
    for run in log:
        energy.append(run.energy)
        forces.append(run.forcemax)
    
    
    
    [13]:
    
    
    
    from matplotlib import pyplot as plt
    fig, axs = plt.subplots(1,1)
    axs2 = axs.twinx()
    axs.plot(energy, 'kx', label="energy")
    axs2.plot(forces, 'r+', label="force")
    axs.set_xlabel("Iteration", fontsize=12)
    axs.set_ylabel("Energy (Hartree)", fontsize=12)
    axs2.set_ylabel("Force (A.U.)", fontsize=12)
    axs.legend(loc="upper center")
    axs2.legend(loc="upper right")
    axs.ticklabel_format(useOffset=False)
    

![../_images/lessons_GeometryOptimization_21_0.png](../_images/lessons_GeometryOptimization_21_0.png)

We have to take some care with plotting the values from the calculation using implicit solvent. This is because sometimes BigDFT restarts a calculation if it senses that the extrapolated geometry guess is not working good. In that case, one of our logfile instances won’t have an energy attribute. A try catch can handle this smoothly.
    
    
    [14]:
    
    
    
    energy = []
    forces = []
    for run in log_imp:
        try:
            energy.append(run.energy)
            forces.append(run.forcemax)
        except AttributeError as e:
            pass
    
    
    
    [15]:
    
    
    
    from matplotlib import pyplot as plt
    fig, axs = plt.subplots(1,1)
    axs2 = axs.twinx()
    axs.plot(energy, 'kx', label="energy")
    axs2.plot(forces, 'r+', label="force")
    axs.set_xlabel("Iteration", fontsize=12)
    axs.set_ylabel("Energy (Hartree)", fontsize=12)
    axs2.set_ylabel("Force (A.U.)", fontsize=12)
    axs.legend(loc="upper center")
    axs2.legend(loc="upper right")
    axs.ticklabel_format(useOffset=False)
    

![../_images/lessons_GeometryOptimization_24_0.png](../_images/lessons_GeometryOptimization_24_0.png)

Next we will extract the geometry.
    
    
    [16]:
    
    
    
    systems = []
    for step in log:
        systems.append(deepcopy(sys))
        systems[-1].update_positions_from_dict(step.astruct)
    
    
    
    [17]:
    
    
    
    systems_imp = []
    for step in log_imp:
        systems_imp.append(deepcopy(sys))
        systems_imp[-1].update_positions_from_dict(step.astruct)
    

We can create a picture now with all three computed geometries overlapping.
    
    
    [18]:
    
    
    
    viz = InlineVisualizer(400, 300)
    viz.display_system(systems[0], colordict={x: "black" for x in systems[-1]}, show=False)
    viz.display_system(systems[-1], colordict={x: "red" for x in systems[-1]}, show=False)
    viz.display_system(systems_imp[-1], colordict={x: "blue" for x in systems[-1]}, show=True)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

## Slab Example

In this section, we will study a more sophisticated example using a slab of NaCl as our test case. Here will show how to do a constrained optimization by fixing the positions or our slab, and allowing a molecule to move freely on top of it. First, will create a slab of NaCl built with the helper of the Atomic Simulation Environment.
    
    
    [19]:
    
    
    
    from ase.build import bulk
    
    atoms = bulk('NaCl', 'rocksalt', a=5.64, orthorhombic=True)
    atoms *= [4, 4, 4]
    

Now we convert to the BigDFT system format. Note that we set the middle cell value to infinity so that we can explore this system as a surface (instead of the bulk).
    
    
    [20]:
    
    
    
    from BigDFT.Interop.ASEInterop import ase_to_bigdft
    from BigDFT.Systems import System
    from BigDFT.UnitCells import UnitCell
    sys = System()
    sys["SUR:1"] = ase_to_bigdft(atoms)
    sys.cell = UnitCell([float(atoms.cell[0, 0]), float("inf"), float(atoms.cell[2, 2])], units="angstroem")
    

We won’t be optimizing the lattice constant, instead we want to optimize something that is sticking to the surface.
    
    
    [21]:
    
    
    
    from BigDFT.IO import XYZReader
    from BigDFT.Fragments import Fragment
    with XYZReader("O2") as ifile:
        sys["ABS:2"] = Fragment(xyzfile=ifile)
    sys["ABS:2"].translate([x - y for x, y in zip(sys["SUR:1"].centroid, sys["ABS:2"].centroid)])
    sys["ABS:2"].translate([0, 0.4*sys.cell[2, 2], 0])
    
    
    
    [22]:
    
    
    
    viz = InlineVisualizer(400, 300)
    viz.display_system(sys)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

Also, we will try fixing the positions of our NaCl atoms and just allow the optimizer to operate on the oxygen molecule.
    
    
    [23]:
    
    
    
    sys["SUR:1"].frozen = "fxyz"
    

Build our input file.
    
    
    [24]:
    
    
    
    inp = Inputfile()
    inp.set_xc("LDA")
    inp.set_hgrid("0.37")
    inp.optimize_geometry(method="SQNM", betax=1.0)
    

And now we’re ready to run.
    
    
    [25]:
    
    
    
    log = code.run(input=inp, posinp=sys.get_posinp(), name="geom-opt-slab", run_dir="work")
    
    
    
    Found 51 different runs
    

Let’s look at how the geometry optimization procedure went. We know from the above print statement “Found 51 different runs” that the optimization did not converge, and instead just ran the maximum number of states. For a real study, we would need to continue the run, or perhaps tweak our optimization parameters.

Let’s look at how the energy changes at each step. We can also monitor the distance between the O2 molecule and the surface.
    
    
    [26]:
    
    
    
    from BigDFT.Fragments import pairwise_distance
    
    systems = []
    energy = []
    distance = []
    for step in log:
        systems.append(deepcopy(sys))
        systems[-1].update_positions_from_dict(step.astruct)
        energy.append(step.energy)
        distance.append(pairwise_distance(systems[-1]["SUR:1"], systems[-1]["ABS:2"]))
    
    
    
    [28]:
    
    
    
    fig, axs = plt.subplots(1,1)
    axs.plot(energy, 'kx', label="energy")
    axs.set_ylabel("Energy (Hartree)", fontsize=12)
    axs2 = axs.twinx()
    axs2.plot(distance, 'r+', label="Distance")
    axs2.set_ylabel("Distance (Bohr)", fontsize=12)
    axs.set_xlabel("Iteration", fontsize=12)
    axs.legend(loc="upper center")
    axs2.legend(loc="upper right")
    axs.ticklabel_format(useOffset=False)
    

![../_images/lessons_GeometryOptimization_45_0.png](../_images/lessons_GeometryOptimization_45_0.png)

[ Previous](../tutorials/Interoperability-Simulation.html "Interoperability with Other Simulation Software") [Next ](MolecularDynamics.html "Molecular Dynamics")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).