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
      * [Geometry Optimization](GeometryOptimization.html)
      * [Molecular Dynamics](MolecularDynamics.html)
      * [Complexity Reduction](ComplexityReduction.html)
      * Comparison To Gaussian Orbitals
        * PySCF Calcuations
        * BigDFT Calculations
      * [Machine Learning](MachineLearning.html)

  * [PyBigDFT API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/index.html)

Developer

  * [BigDFT-suite manifesto](../devel/developers.html)

  * [Futile API](https://l_sim.gitlab.io/bigdft-suite/futile/build/html/index.html)

__[BigDFT-suite](../index.html)

  * [](../index.html)
  * [User Guide](../users/guide.html)
  * Comparison To Gaussian Orbitals
  * [ View page source](../_sources/lessons/Gaussian.ipynb.txt)

* * *

# Comparison To Gaussian Orbitals

In this notebook, we will compare a calculation using the BigDFT code which is based on wavelets to a calculation from a code which is based on gaussian orbitals. As our representative gaussian code, we will use [PySCF](https://sunqm.github.io/pyscf/).

To do the comparison, we are going to look at a molecule composed of two fragments connected by a single bond. We will then rotate one fragment along that bond, computing the energy at each step. We will do this calculation using different basis sets, and see how the energy values converge and compare.

First, we will load in the system.
    
    
    [1]:
    
    
    
    from BigDFT.IO import XYZReader
    from BigDFT.Systems import System
    from BigDFT.Fragments import Fragment
    
    geom = "CH3SH"
    
    sys = System()
    sys["FRA:0"] = Fragment()
    sys["FRA:1"] = Fragment()
    
    with XYZReader(geom) as ifile:
        for i, at in enumerate(ifile):
            if i == 0 or i == 3 or i == 4 or i == 5:
                sys["FRA:0"] += Fragment([at])
            else:
                sys["FRA:1"] += Fragment([at])
    

We can visualize the molecule to verify that we have properly broken it into two fragments.
    
    
    [2]:
    
    
    
    from BigDFT.Visualization import InlineVisualizer
    viz = InlineVisualizer(400,300)
    viz.display_system(sys)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

We want to rotate along the bond connecting the two fragments. To do this we need to compute that vector.
    
    
    [3]:
    
    
    
    vec = [x - y for x, y in zip(sys["FRA:0"][0].get_position(), sys["FRA:1"][0].get_position())]
    

Now we can time step over 120 degrees.
    
    
    [4]:
    
    
    
    from copy import deepcopy
    
    systems = []
    angles = []
    steps = 10
    
    for i in range(steps):
        newsys = deepcopy(sys)
        newsys["FRA:0"].rotate_on_axis(angle=120/(steps-1) * i, axis=vec, units="degrees")
        systems.append(newsys)
        angles += [120/(steps-1) * i]
    

Visualize the rotation to verify.
    
    
    [5]:
    
    
    
    viz = InlineVisualizer(400,300)
    viz.display_system(*systems)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

## PySCF Calcuations

Now let’s calculate the energy of this system using the PySCF code at the Hartree-Fock level of theory. Hartree-Fock is more convenient than DFT because we do not have to consider the integration grid used for the exchange and correlation potential. We will repeat this calculation using various Karlsruhe basis sets.
    
    
    [6]:
    
    
    
    basis = ["sto-3g", "def2-SVP", "def2-TZVP", "def2-QZVP"]
    

We need a simple routine to convert to the pyscf format.
    
    
    [7]:
    
    
    
    def convert_bigdft_to_pyscf(sys, basis="sto-3g"):
        from pyscf import gto
        mol = gto.Mole()
        for frag in sys.values():
            for at in frag:
                mol.atom.append([at.sym, at.get_position("angstroem")])
        return mol
    
    mols = [convert_bigdft_to_pyscf(x) for x in systems]
    

Run and extract energy and forces.
    
    
    [8]:
    
    
    
    from pyscf.scf import HF
    from numpy.linalg import norm
    
    pyscf_forces = {}
    pyscf_energies = {}
    
    for b in basis:
        print(b)
        pyscf_energies[b] = []
        pyscf_forces[b] = []
        for m in mols:
            m.basis = b
            m.verbose = 0
            m.build()
    
            mf = HF(m)
            pyscf_energies[b].append(mf.kernel())
    
            g = mf.nuc_grad_method()
            grad = g.kernel()
            pyscf_forces[b].append(grad)
    
    
    
    sto-3g
    def2-SVP
    def2-TZVP
    def2-QZVP
    

With the calculations completed, we can now plot the values. We’ll look at how the energy changes from the starting configuration, and compute the norm of the difference in forces.
    
    
    [9]:
    
    
    
    from matplotlib import pyplot as plt
    fig, axs = plt.subplots(2,1,figsize=(8,6))
    
    markers = ["+", "x", ".", "o"]
    for m, b in zip(markers, basis):
        axs[0].plot(angles, [(x - pyscf_energies[b][0]) for x in pyscf_energies[b]], label=b, marker=m, linestyle='--')
        axs[1].plot(angles, [(norm(x - pyscf_forces[b][0])) for x in pyscf_forces[b]], label=b, marker=m, linestyle='--')
    
    axs[0].set_ylabel("Energy Change (AU)", fontsize=12)
    axs[1].set_ylabel("Forces (AU)", fontsize=12)
    axs[1].set_xlabel("Angle (degrees)", fontsize=12)
    
    axs[0].legend()
    fig.tight_layout()
    

![../_images/lessons_Gaussian_17_0.png](../_images/lessons_Gaussian_17_0.png)

We see that the energy does seem to successfully converge. We also see a good part about Gaussian basis functions: even with the small basis, the values are qualitatively correct. On the other hand, we see a weakness of this approach, where the smaller basis set (STO-3G) performs better than a bigger one (def2-SVP). Care must be taken to determine if a large enough basis was used.

## BigDFT Calculations

We will now repeat this calculation using the BigDFT code. BigDFT’s accuracy is controlled by the grid spacing. A smaller grid spacing leads to more accurate energies.
    
    
    [10]:
    
    
    
    hgrid = [0.5, 0.4, 0.35, 0.3]
    
    
    
    [11]:
    
    
    
    from BigDFT.Inputfiles import Inputfile
    inp = Inputfile()
    inp.set_xc("HF")
    
    # Set the pseudopotential functional of Hartree-Fock. We will pick the LDA built in pseudopotential.
    inp['psppar.C']={'Pseudopotential XC': 1}
    inp['psppar.O']={'Pseudopotential XC': 1}
    inp['psppar.H']={'Pseudopotential XC': 1}
    inp['psppar.S']={'Pseudopotential XC': 1}
    

Now we repeat the calculation for each grid spacing.
    
    
    [12]:
    
    
    
    from BigDFT.Calculators import SystemCalculator
    code = SystemCalculator(verbose=False, skip=True)
    
    
    
    Initialize a Calculator with OMP_NUM_THREADS=2 and command mpirun -np 2 /Users/wddawson/Documents/CEA/binaries/bigdft_suite/install/bin/bigdft
    
    
    
    [13]:
    
    
    
    from numpy import array
    
    bigdft_energies = {}
    bigdft_forces = {}
    for h in hgrid:
        print(h)
        inp.set_hgrid(h)
        bigdft_energies[h] = []
        bigdft_forces[h] = []
        for i, m in enumerate(systems):
            log = code.run(input=inp, posinp=m.get_posinp(), name=geom + "-" + str(h) + "-" + str(i), run_dir="work")
            m.set_atom_forces(log)
            bigdft_energies[h].append(log.energy)
    
            forces = []
            for frag in m.values():
                for at in frag:
                    forces.append(at.get_force())
            bigdft_forces[h].append(array(forces))
    
    
    
    0.5
    0.4
    0.35
    0.3
    

And we can plot the results.
    
    
    [14]:
    
    
    
    from matplotlib import pyplot as plt
    fig, axs = plt.subplots(2,1,figsize=(8,6))
    
    markers = ["+", "x", ".", "o"]
    for m, b in zip(markers, hgrid):
        axs[0].plot(angles, [(x - bigdft_energies[b][0]) for x in bigdft_energies[b]], label=b, marker=m, linestyle='--')
        axs[1].plot(angles, [(norm(x - bigdft_forces[b][0])) for x in bigdft_forces[b]], label=b, marker=m, linestyle='--')
    
    axs[0].set_ylabel("Energy Change (AU)", fontsize=12)
    axs[1].set_ylabel("Forces (AU)", fontsize=12)
    axs[1].set_xlabel("Angle (degrees)", fontsize=12)
    
    axs[0].legend()
    fig.tight_layout()
    

![../_images/lessons_Gaussian_27_0.png](../_images/lessons_Gaussian_27_0.png)

We see here that energy improves systematically with the choice of hgrid due to the variational formulism applied. We also see that a loose cutoff can lead to disastrous results. In the case of Gaussian basis sets, a small basis might be qualitatively right since it was fitted to similar types of systems. But a numerical basis is more “all or nothing”.

We can also plot the best energy values of the two codes on the same axis.
    
    
    [15]:
    
    
    
    fig, axs = plt.subplots(2,1,figsize=(8,6))
    
    axs[0].plot(angles, [(x - pyscf_energies[basis[-1]][0]) for x in pyscf_energies[basis[-1]]],
                     label="pyscf-" + str(basis[-1]), color='k', marker='*', linestyle='-', markersize=12)
    axs[0].plot(angles, [(x - pyscf_energies[basis[-2]][0]) for x in pyscf_energies[basis[-2]]],
                     label="pyscf-" + str(basis[-2]), color='k', marker='.', linestyle='dotted', markersize=12)
    axs[0].plot(angles, [(x - bigdft_energies[hgrid[-1]][0]) for x in bigdft_energies[hgrid[-1]]],
                     label="bigdft-" + str(hgrid[-1]), color='r', marker='x', linestyle='-', markersize=12)
    axs[0].plot(angles, [(x - bigdft_energies[hgrid[-2]][0]) for x in bigdft_energies[hgrid[-2]]],
                     label="bigdft-" + str(hgrid[-2]), color='r', marker='+', linestyle='dotted', markersize=12)
    
    axs[1].plot(angles, [(norm(x - pyscf_forces[basis[-1]][0])) for x in pyscf_forces[basis[-1]]],
                     label="pyscf-" + str(basis[-1]), color='k', marker='*', linestyle='-', markersize=12)
    axs[1].plot(angles, [(norm(x - pyscf_forces[basis[-2]][0])) for x in pyscf_forces[basis[-2]]],
                     label="pyscf-" + str(basis[-2]), color='k', marker='.', linestyle='dotted', markersize=12)
    axs[1].plot(angles, [(norm(x - bigdft_forces[hgrid[-1]][0])) for x in bigdft_forces[hgrid[-1]]],
                     label="bigdft-" + str(hgrid[-1]), color='r', marker='x', linestyle='-', markersize=12)
    axs[1].plot(angles, [(norm(x - bigdft_forces[hgrid[-2]][0])) for x in bigdft_forces[hgrid[-2]]],
                     label="bigdft-" + str(hgrid[-2]), color='r', marker='+', linestyle='dotted', markersize=12)
    
    axs[0].set_ylabel("Energy Change (AU)", fontsize=12)
    axs[1].set_ylabel("Forces (AU)", fontsize=12)
    axs[1].set_xlabel("Angle (degrees)", fontsize=12)
    
    axs[0].legend()
    fig.tight_layout()
    

![../_images/lessons_Gaussian_30_0.png](../_images/lessons_Gaussian_30_0.png)

We note that even though the two calculations are “converged”, the pseudopotential approximation remains, which leads to different energy values for these two codes.

[ Previous](ComplexityReduction.html "Complexity Reduction") [Next ](MachineLearning.html "Machine Learning")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).