[ BigDFT-suite ![Logo](../_static/logo-bigdft-white.svg) ](../index.html)

Overview

  * [Available Functionalities](../overview/functionality.html)

  * [The BigDFT-suite Package](../overview/package.html)

  * [Publications](../overview/publications.html)

  * [License](../overview/license.html)

Basic Usage

  * [Installation](../users/install.html)

  * [Quick Start - From Python](QuickStart.html)

  * [Quick Start - Command Line](CMDStart.html)

User Guide

  * [User Guide](../users/guide.html)

  * [PyBigDFT API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/index.html)

Developer

  * [BigDFT-suite manifesto](../devel/developers.html)

  * [Futile API](https://l_sim.gitlab.io/bigdft-suite/futile/build/html/index.html)

__[BigDFT-suite](../index.html)

  * [](../index.html)
  * Introduction
  * [ View page source](../_sources/school/Introduction.ipynb.txt)

* * *

# Introduction

In this series of tutorials, the fundamental aspects of a BigDFT calculation are inspected.

The **topics** addressed are:

  * building a system

  * running a simple calculation

  * reading a Logfile

Those subjects are then each followed by **exercises**.

The **prerequisites** are:

  * beginner level in python programming (1)

  * fundamental understanding of _ab initio_ methods (2)

In the following, PyBigDFT is used to build systems and then compute their first-principles properties using BigDFT.

## (1) python programming

In python, two datastructures are very common: **lists** and **dictionaries**.
    
    
    [1]:
    
    
    
    my_list = [0, 1, 2, 3]
    print(my_list[-1])
    my_dict = {"a": "word", "c": 4}
    print(my_dict["c"])
    
    
    
    3
    4
    

Those objects are easily built and manipulated using comprehensions
    
    
    [2]:
    
    
    
    my_list2 = [x*3 for x in my_list]
    print(my_list2)
    my_dict2 = {k+"2": v for k,v in my_dict.items()}
    print(my_dict2)
    
    
    
    [0, 3, 6, 9]
    {'a2': 'word', 'c2': 4}
    

Additionally, those objects are serializable in yaml format for improved readability
    
    
    [3]:
    
    
    
    from yaml import dump
    
    print(dump(my_dict2))
    
    
    
    a2: word
    c2: 4
    
    

## (2) _ab initio_ methods

Ab initio quantum chemistry methods attempt to solve Schrödinger’s equation given the **positions** of the nuclei and the **number of electrons** , yielding useful information such as electron densities, energies and other properties of the system.

A first-principles calculation therefore requires:

  * a geometry (along with a lattice for solid-state)

  * an exchange-correlation (XC) functional

# Building a system

In PyBigDFT, geometries are build upon different layers:

  * Atoms: stores any information (dict)

  * Fragments: are collection of Atoms (list)

  * Systems: are collection of Fragments (dict)

Any system is composed of atoms, which require both a **symbol** and a **position**.

The most appropriate way to store such information (or any other) about an atom is inside a `dict`
    
    
    [4]:
    
    
    
    at = {"sym": "H", "r": [1, 0, 0], "units": "angstroem"}
    print(dump(at))
    
    
    
    r:
    - 1
    - 0
    - 0
    sym: H
    units: angstroem
    
    

The `Atoms` class wraps up `dict` in order to provide helpful subroutines.
    
    
    [5]:
    
    
    
    from BigDFT.Atoms import Atom
    
    atom = Atom(at)
    print(dump(atom))
    
    
    
    !!python/object:BigDFT.Atoms.Atom
    store:
      r:
      - 1
      - 0
      - 0
      sym: H
      units: angstroem
    
    

Some of the built in subroutines are demonstrated below.
    
    
    [6]:
    
    
    
    print(atom.sym)
    print(atom.atomic_number)
    print(atom.get_position("angstroem"))
    print(atom.get_position("bohr"))
    
    
    
    H
    1
    [1.0, 0.0, 0.0]
    [1.8897261245650618, 0.0, 0.0]
    

With this approach, the flexibility of a `dict` is retained.
    
    
    [7]:
    
    
    
    atom["source"] = "tutorial"
    print(atom["source"])
    for k,v in atom.items():
        print(k,v)
    
    
    
    tutorial
    sym H
    r [1, 0, 0]
    units angstroem
    source tutorial
    

As mentioned above, DFT codes requires to specify **the number of electrons** for each atom. This information is given by the type of pseudopotential employed. We’ll see later on how to access it.

Calculations involve not single atoms but instead **groups of atoms**. In this case, lists are used as model data structures, with the wrapper class referred to as a `Fragment`.
    
    
    [8]:
    
    
    
    at1 = Atom({"sym": "O", "r": [2.3229430273, 1.3229430273, 1.7139430273], "units": "angstroem"})
    at2 = Atom({"sym": "H", "r": [2.3229430273, 2.0801430273, 1.1274430273], "units": "angstroem"})
    at3 = Atom({"sym": "H", "r": [2.3229430273, 0.5657430273000001, 1.1274430273], "units": "angstroem"})
    
    
    
    [9]:
    
    
    
    from BigDFT.Fragments import Fragment
    
    frag1 = Fragment([at1, at2, at3])
    print(len(frag1))
    print(frag1.centroid)
    
    
    
    3
    [4.38972612 2.5        2.5       ]
    

It’s also possible to build up a fragment in a more step by step process.
    
    
    [10]:
    
    
    
    frag1 = Fragment()
    frag1.append(at1)
    frag1 += Fragment([at2])
    frag1.extend(Fragment([at3]))
    

The fragment properties are then visualized in yaml format
    
    
    [11]:
    
    
    
    print(dump(frag1))
    
    
    
    !!python/object:BigDFT.Fragments.Fragment
    atoms:
    - !!python/object:BigDFT.Atoms.Atom
      store:
        r:
        - 2.3229430273
        - 1.3229430273
        - 1.7139430273
        sym: O
        units: angstroem
    - !!python/object:BigDFT.Atoms.Atom
      store:
        r:
        - 2.3229430273
        - 2.0801430273
        - 1.1274430273
        sym: H
        units: angstroem
    - !!python/object:BigDFT.Atoms.Atom
      store:
        r:
        - 2.3229430273
        - 0.5657430273000001
        - 1.1274430273
        sym: H
        units: angstroem
    conmat: null
    frozen: null
    q1: null
    q2: null
    
    

In PyBigDFT, we have the `System` class at the top, based on a `dict`. Systems are **named collections of fragments** , with the convention for naming fragments as “NAME:ID” (where name is a string and ID is a number).
    
    
    [12]:
    
    
    
    from BigDFT.Systems import System
    
    sys = System()
    sys["WAT:0"] = frag1
    

Similarly, systems are easily readable
    
    
    [13]:
    
    
    
    print(dump(sys))
    
    
    
    !!python/object:BigDFT.Systems.System
    cell: !!python/object:BigDFT.UnitCells.UnitCell
      cell:
      - - .inf
        - 0
        - 0
      - - 0
        - .inf
        - 0
      - - 0
        - 0
        - .inf
    conmat: null
    store:
      WAT:0: !!python/object:BigDFT.Fragments.Fragment
        atoms:
        - !!python/object:BigDFT.Atoms.Atom
          store:
            r:
            - 2.3229430273
            - 1.3229430273
            - 1.7139430273
            sym: O
            units: angstroem
        - !!python/object:BigDFT.Atoms.Atom
          store:
            r:
            - 2.3229430273
            - 2.0801430273
            - 1.1274430273
            sym: H
            units: angstroem
        - !!python/object:BigDFT.Atoms.Atom
          store:
            r:
            - 2.3229430273
            - 0.5657430273000001
            - 1.1274430273
            sym: H
            units: angstroem
        conmat: null
        frozen: null
        q1: null
        q2: null
    
    

Here, additional properties are displayed, i.e. the **connectivity matrix** and the **unit cell**.

It is extremely convenient to visualize `System` objects, just do
    
    
    [14]:
    
    
    
    sys.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [14]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x7f472d1be5e0>
    

It is equally convenient to manipulate fragments within systems.

Let us **rotate** and **translate** the previous water fragment and add it to the system.
    
    
    [15]:
    
    
    
    from copy import deepcopy
    
    frag2 = deepcopy(frag1)
    frag2.translate([10, 0, 0])
    frag2.rotate(x=90, units="degrees")
    sys["WAT:1"] = frag2
    
    
    
    [16]:
    
    
    
    sys.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [16]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x7f4700f407f0>
    

The visualization module has identified that there are two separate fragments, coloring them accordingly (merging fragments would render a uniform visualization).

To summarize the hierarchy, let’s iterate over our `System`.
    
    
    [17]:
    
    
    
    for fragid, frag in sys.items():
        print(fragid)
        for atm in frag:
            print(dict(atm))
    
    
    
    WAT:0
    {'sym': 'O', 'r': [2.3229430273, 1.3229430273, 1.7139430273], 'units': 'angstroem'}
    {'sym': 'H', 'r': [2.3229430273, 2.0801430273, 1.1274430273], 'units': 'angstroem'}
    {'sym': 'H', 'r': [2.3229430273, 0.5657430273000001, 1.1274430273], 'units': 'angstroem'}
    WAT:1
    {'sym': 'O', 'r': [14.389726124565062, 1.7611170852950608, 2.499999999999999], 'units': 'bohr'}
    {'sym': 'H', 'r': [14.389726124565062, 2.86944145735247, 3.930900621520664], 'units': 'bohr'}
    {'sym': 'H', 'r': [14.389726124565062, 2.86944145735247, 1.0690993784793343], 'units': 'bohr'}
    

The cell attribute of the `System` object enables to investigate systems ranging from **molecular biology** to **condensed matter physics** , by fixing the periodic boundaries conditions.

The `UnitCell` class is available to manage the cell.
    
    
    [18]:
    
    
    
    from BigDFT.UnitCells import UnitCell
    
    sys.cell = UnitCell([5, 5, 5], units="bohr")
    
    
    
    [19]:
    
    
    
    print(sys.cell.get_posinp())
    
    
    
    [5, 5, 5]
    

BigDFT is able to handle several boundary conditions, depending on the cell.

  * if set to `None`: free boundary

  * if \\(x\\) and \\(y\\) are set to `inf`: 1D system

  * if \\(y\\) is set to `inf`: 2D system

  * if all values are `float`: fully periodic system.

For wire boundary conditions
    
    
    [20]:
    
    
    
    sys.cell = UnitCell([float("inf"), float("inf"), 5], units="bohr")
    print(sys.cell.get_posinp("bohr"))
    
    
    
    [inf, inf, 5]
    

For the surface condition
    
    
    [21]:
    
    
    
    sys.cell = UnitCell([5, float("inf"), 5], units="bohr")
    print(sys.cell.get_posinp("bohr"))
    
    
    
    [5, inf, 5]
    

Note that **reduced** (fractional) coordinates can be employed to alternatively specify the locations of atoms (_for fully periodic boundary conditions_).
    
    
    [22]:
    
    
    
    cell = UnitCell([10, 10, 10], units="bohr")
    
    
    
    [23]:
    
    
    
    at = Atom({'r': [0.5, 0.25, 0.0], 'sym': "He", 'units': 'reduced'})
    
    print(at.get_position("reduced", cell))
    print(at.get_position("bohr", cell))
    print(at.get_position("angstroem", cell))
    
    
    
    [0.5, 0.25, 0.0]
    [5.0, 2.5, 0.0]
    [2.6458860546, 1.3229430273, 0.0]
    

A wide range of standard files can easily be manipulated with PyBigDFT.

The `XYZReader` class enables to access the some built in molecules in the database (available [here](https://gitlab.com/l_sim/bigdft-suite/-/tree/devel/PyBigDFT/BigDFT/Database/XYZs)). Otherwise, a path for the filename is required.
    
    
    [2]:
    
    
    
    from BigDFT.IO import XYZReader
    
    sys = System()
    sys["CH4:0"] = Fragment()
    with XYZReader("CH4") as ifile:
        for atom in ifile:
            sys["CH4:0"].append(atom)
    
    sys["CH2F:1"] = Fragment()
    with XYZReader("CH2F") as ifile:
        for atom in ifile:
            sys["CH2F:1"].append(atom)
    
    sys["CH2F:1"].translate([-5, 0, 0])
    

The resulting system is
    
    
    [4]:
    
    
    
    sys.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [4]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x7f9bdc0cce50>
    

Afterwards, the `XYZWriter` class enables to write down our data in the `xyz` format.
    
    
    [7]:
    
    
    
    from BigDFT.IO import XYZWriter
    
    natoms = sum([len(x) for x in sys.values()])
    with XYZWriter("sys.xyz", natoms=natoms) as ofile:
        for frag in sys.values():
            for at in frag:
                ofile.write(at)
    

Or, similarly
    
    
    [9]:
    
    
    
    from BigDFT import IO
    
    with open('sys.xyz','w') as infile:
        IO.write_xyz(sys,infile)
    

The advantage of the `XYZreader` (or `XYZwriter`) approach is to directly yield the following attributes: `units`, `natoms` and `cell`.

Warning: when reading an `xyz` file, **there is no fragment information available**

The system is either defined as one fragment (`single`) or each atoms are a single fragment (`atomic`)
    
    
    [18]:
    
    
    
    with open('sys.xyz','r') as ifile:
        sys_a = IO.read_xyz(ifile,fragmentation="single")
    sys_a.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [18]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x7f9b75692fa0>
    
    
    
    [17]:
    
    
    
    with open('sys.xyz','r') as ifile:
        sys_b = IO.read_xyz(ifile,fragmentation="atomic")
    sys_b.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [17]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x7f9b7563a8e0>
    

Similarly to `xyz` files, let us write a PDB file (for example).
    
    
    [24]:
    
    
    
    with open('sys.pdb', 'w') as ofile:
        IO.write_pdb(sys, ofile)
    

Let us then inspect this pdb file
    
    
    [25]:
    
    
    
    with open('sys.pdb','r') as ifile:
        for line in ifile:
            print(line, end="")
    
    
    
    HETATM    1 C    CH4 A   0       0.000   0.000   0.000  1.00  0.00       B   C
    HETATM    2 H    CH4 A   0       0.628   0.628   0.628  1.00  0.00       B   H
    HETATM    3 H    CH4 A   0       0.628  -0.628  -0.628  1.00  0.00       B   H
    HETATM    4 H    CH4 A   0      -0.628   0.628  -0.628  1.00  0.00       B   H
    HETATM    5 H    CH4 A   0      -0.628  -0.628   0.628  1.00  0.00       B   H
    HETATM    6 C    CH2 A   1      -2.675   0.655   0.000  1.00  0.00       B   C
    HETATM    7 F    CH2 A   1      -2.675  -0.682   0.000  1.00  0.00       B   F
    HETATM    8 H    CH2 A   1      -2.431   1.104   0.947  1.00  0.00       B   H
    HETATM    9 H    CH2 A   1      -2.431   1.104  -0.947  1.00  0.00       B   H
    

Of course, a pdb system is also readable
    
    
    [28]:
    
    
    
    for fragid, frag in IO.read_pdb(open('sys.pdb','r')).items():
        print(fragid)
        for at in frag:
            print(dict(at))
    
    
    
    CH4:0
    {'sym': 'C', 'r': [0.0, 0.0, 0.0], 'name': 'C', 'units': 'angstroem'}
    {'sym': 'H', 'r': [0.628, 0.628, 0.628], 'name': 'H', 'units': 'angstroem'}
    {'sym': 'H', 'r': [0.628, -0.628, -0.628], 'name': 'H', 'units': 'angstroem'}
    {'sym': 'H', 'r': [-0.628, 0.628, -0.628], 'name': 'H', 'units': 'angstroem'}
    {'sym': 'H', 'r': [-0.628, -0.628, 0.628], 'name': 'H', 'units': 'angstroem'}
    CH2:1
    {'sym': 'C', 'r': [-2.675, 0.655, 0.0], 'name': 'C', 'units': 'angstroem'}
    {'sym': 'F', 'r': [-2.675, -0.682, 0.0], 'name': 'F', 'units': 'angstroem'}
    {'sym': 'H', 'r': [-2.431, 1.104, 0.947], 'name': 'H', 'units': 'angstroem'}
    {'sym': 'H', 'r': [-2.431, 1.104, -0.947], 'name': 'H', 'units': 'angstroem'}
    

Notice how the **information on fragments is conserved**

  1. Construct a complex of C2H4 molecules, arranged in a equilateral triangle, using the molecule database (available [here](https://gitlab.com/l_sim/bigdft-suite/-/tree/devel/PyBigDFT/BigDFT/Database/XYZs))

  2. Construct a carbon chain of inter-atomic distance of 1.5 angstroem.

  3. Construct a graphene lattice using a rectangular cell and a carbon-carbon bond of 1.42 angstroem. (**Advanced**)

# A first-principles calculation : N2 molecule

Let us go through the fundamentals of simple BigDFT calculation.

The following parameters need to addressed one by one:

  * the atomic positions

  * the exchange-correlation functional

  * the proper converged parameters

Atomic positions can be obtained from the BigDFT database (available [here](https://gitlab.com/l_sim/bigdft-suite/-/tree/devel/PyBigDFT/BigDFT/Database/XYZs)).
    
    
    [24]:
    
    
    
    from BigDFT.Systems import System
    from BigDFT.Fragments import Fragment
    from BigDFT.IO import XYZReader
    
    N2 = System()
    with XYZReader("N2") as ifile:
        N2["N:0"] = Fragment([next(ifile)])
        N2["N:1"] = Fragment([next(ifile)])
    

The atomic positions are then
    
    
    [25]:
    
    
    
    print(N2.get_posinp())
    
    
    
    {'positions': [{'N': [0.0, 0.0, 0.5488], 'frag': ['N', '0']}, {'N': [0.0, 0.0, -0.5488], 'frag': ['N', '1']}], 'units': 'angstroem', 'cell': [inf, inf, inf]}
    

A calculation is run using the `Calculator` class.
    
    
    [26]:
    
    
    
    from BigDFT import Calculators as C
    
    study = C.SystemCalculator(verbose=False) #Create a calculator
    log = study.run(posinp=N2.get_posinp(),name="N2") #run the code
    
    
    
     <BigDFT> log of the run will be written in logfile: ./log-N2.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-N2.14:47:51.184.yaml
    

An instance of the `Logfile` class is returned, containing information about the electronic structure (and more) of the system.

For example, the total energy of the system is
    
    
    [27]:
    
    
    
    log.energy #this value is in Ha
    
    
    
    [27]:
    
    
    
    -19.884615273242716
    

Similarly, the eigenvalues and the DoS are obtained as
    
    
    [28]:
    
    
    
    log.evals[0].tolist() # the eigenvalues in Ha ([0] stands for the first K-point, here meaningless)
    
    
    
    [28]:
    
    
    
    [[-1.041353673208,
      -0.4926440819324,
      -0.4357815638016,
      -0.4357812404171,
      -0.3818323179544]]
    
    
    
    [29]:
    
    
    
    log.get_dos().plot(); #the density of states
    

![../_images/school_Introduction_80_0.png](../_images/school_Introduction_80_0.png)

let us look closer at the SystemCalculator that was presented above.
    
    
    [30]:
    
    
    
    calc = C.SystemCalculator(verbose=False,omp=1,mpi_run='mpirun -np 2')
    

This allows to set the computational parameters such as the OpenMP and MPI parallelisations, which is of **crucial importance** for memory and time efficiency.

The global options of the runner (or calculator) can then be accessed by
    
    
    [31]:
    
    
    
    calc.global_options()
    
    
    
    [31]:
    
    
    
    {'omp': '1',
     'mpi_run': 'mpirun -np 2',
     'dry_run': False,
     'skip': False,
     'verbose': False}
    

To specify non-default input parameters to the code, we should employ a `Inputfile` object.

For instance, the XC functional can be chosen via the `set_xc` method. All methods are accessible [here](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/BigDFT.InputActions.html)
    
    
    [32]:
    
    
    
    from BigDFT import Inputfiles as I
    
    inp = I.Inputfile()
    inp.set_xc('LDA')
    

In the same spirit, a Hartree-Fock calculation is performed using.
    
    
    [33]:
    
    
    
    inp.set_xc('HF')
    HF = study.run(name="HF",input=inp) #Run the code with the name scheme HF
    
    
    
     <BigDFT> log of the run will be written in logfile: ./log-HF.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-HF.14:47:57.312.yaml
    
    
    
    STOP  MPIFAKE: MPI_ABORT
    

An **error** occurred !

Let us identify the issue by opening [debug/bigdft-err-0.yaml](./debug/bigdft-err-0.yaml)
    
    
     Additional Info:
       The pseudopotential parameter file "psppar.N" is lacking, and no registered pseudo found
       for "N"

The issue is that the pseudopotential is assigned by default in the code **only for LDA and PBE** XC approximations.

Therefore, one simply needs to specify it.
    
    
    [34]:
    
    
    
    inp['psppar.N']={'Pseudopotential XC': 1} #here 1 stands for LDA as per the XC codes
    HF = study.run(name="HF",input=inp)
    
    
    
     <BigDFT> log of the run will be written in logfile: ./log-HF.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-HF.14:47:58.344.yaml
    

One should be careful in **choosing a pseudopotential** which has been **generated with the same XC approximation** used.

At present, Hartwigsen-Goedeker-Hutter (HGH) data are unfortunately only available for semilocal functionals. For example, the same exercise as follows could have been done with Hybrid XC functionals (e.g. PBE0 (ixc=-406)).

In the case of Hartree-Fock calculations, using semilocal functionals generally yield accurate results (see [Physical Review B 37.5 (1988): 2674](https://journals.aps.org/prb/pdf/10.1103/PhysRevB.37.2674)).

In BigDFT, XC functionals are specified using the built in named functionals, or using the [LibXC codes](https://www.tddft.org/programs/libxc/functionals/).

Daubechies Wavelets is a systematic basis set (as plane waves are), where accuracy is arbitrarily increased by varying some parameters, i.e. (typically) `hgrid` and `rmult`.

**``hgrids``** set up the grid step for the basis set spatial expansion. There is **one float value** describing the grid steps in the three space directions (i.e. \\(x\\), \\(y\\) and \\(z\\)) or a **3D array** is also accepted. These values are in bohr unit and typically range from 0.3 to 0.65. The harder the pseudo-potential, the lower value should be set up. These values are set using the `set_hgrid` method of the `Inpufile` class.

**``rmult``** set up the basis set spatial expansion. It contains an array of two float values that are **two multiplying factors** defining chemical-species-dependent quantities. The first factor is the most important since it describes the spatial expansion of the basis set, defined as a set of real space points with non-zero values inside spheres centered on atoms. The first multiplying factor is called `crmult` for Coarse grid Radius MULTiplier, with typical values of 5 to 7. The second one called `frmult` for Fine grid Radius MULTiplier is related to the fine resolution. This parameter is less pertinent for the convergence of energy and can be ignored. It is possible to indicate only one float value, the `crmult` parameter. Such parameters can be set by the method `set_rmult` of `Inputfile` class.

Let us find the appropriate parameters to characterize a N2 molecule using the `Dataset`class, by comparing the extracted energies depending on `hgrid` and `rmult`.
    
    
    [35]:
    
    
    
    hgrids = [0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2] #bohr
    rmult = [3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]
    

Let us build three different datasets, by varying:

  * `hgrid` and `rmult` together.

  * only `hgrid`

  * only `rmult`

Each input dictionary is also labeled by a unique name.
    
    
    [36]:
    
    
    
    from BigDFT import Datasets as D
    
    inp = I.Inputfile()
    pos = N2.get_posinp()
    study = C.SystemCalculator(verbose=False)
    
    h_and_c_dataset = D.Dataset('h_and_c')
    for h,c in zip(hgrids,rmult):
        inp_run = deepcopy(inp)
        inp_run.set_hgrid(h)
        inp_run.set_rmult([c,9.0])
        h_and_c_dataset.append_run(id={'h':h,'c':c},run_dir='conv-N2',input=inp_run,posinp=pos,runner=study)
    
    
    
    [37]:
    
    
    
    h_only_dataset = D.Dataset('h_only')
    for h in hgrids:
        inp_run = deepcopy(inp)
        inp_run.set_hgrid(h)
        h_only_dataset.append_run(id={'h':h},run_dir='conv-N2',input=inp_run,posinp=pos,runner=study)
    
    
    
    [38]:
    
    
    
    c_only_dataset = D.Dataset('c_only')
    for c in rmult:
        inp_run = deepcopy(inp)
        inp_run.set_rmult([c,9.0])
        c_only_dataset.append_run(id={'c':c},run_dir='conv-N2',input=inp_run,posinp=pos,runner=study)
    

Each dataset is then run
    
    
    [39]:
    
    
    
    %%capture
    
    h_only_dataset.calculators[0]['calc'] = C.SystemCalculator(skip=True,verbose=False)
    c_only_dataset.calculators[0]['calc'] = C.SystemCalculator(skip=True,verbose=False)
    h_and_c_dataset.calculators[0]['calc'] = C.SystemCalculator(skip=True,verbose=False)
    h_only_dataset.run();
    c_only_dataset.run();
    h_and_c_dataset.run();
    
    
    
     <BigDFT> Run already performed, found final file: forces_h__0.55.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.484 MB
     Walltime since initialization:  00:00:00.001300971
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.5.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.580 MB
     Walltime since initialization:  00:00:00.001354704
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.45.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.532 MB
     Walltime since initialization:  00:00:00.001374697
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.4.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.552 MB
     Walltime since initialization:  00:00:00.001479010
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.35.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.556 MB
     Walltime since initialization:  00:00:00.001223437
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.3.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.416 MB
     Walltime since initialization:  00:00:00.001560655
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.25.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.424 MB
     Walltime since initialization:  00:00:00.001189205
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.2.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.468 MB
     Walltime since initialization:  00:00:00.001264324
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__3.5.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.516 MB
     Walltime since initialization:  00:00:00.001039844
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__4.0.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.548 MB
     Walltime since initialization:  00:00:00.001044584
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__4.5.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.496 MB
     Walltime since initialization:  00:00:00.001046881
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__5.0.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.532 MB
     Walltime since initialization:  00:00:00.001366479
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__5.5.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.384 MB
     Walltime since initialization:  00:00:00.001108488
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__6.0.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.476 MB
     Walltime since initialization:  00:00:00.001046731
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__6.5.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.384 MB
     Walltime since initialization:  00:00:00.001039710
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__7.0.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.428 MB
     Walltime since initialization:  00:00:00.001147400
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__3.5,h__0.55.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.364 MB
     Walltime since initialization:  00:00:00.001029106
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__4.0,h__0.5.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.576 MB
     Walltime since initialization:  00:00:00.001155525
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__4.5,h__0.45.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.580 MB
     Walltime since initialization:  00:00:00.001097446
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__5.0,h__0.4.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.464 MB
     Walltime since initialization:  00:00:00.001512872
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__5.5,h__0.35.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.460 MB
     Walltime since initialization:  00:00:00.001077780
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__6.0,h__0.3.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.456 MB
     Walltime since initialization:  00:00:00.001288873
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__6.5,h__0.25.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.496 MB
     Walltime since initialization:  00:00:00.001129750
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__7.0,h__0.2.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.472 MB
     Walltime since initialization:  00:00:00.001266063
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
    

We now store the energies of each of the dataset runs, and identify the minimum as the minimum value from the `h_and_c` dataset:
    
    
    [40]:
    
    
    
    from numpy import array
    
    energies_h = array(h_only_dataset.fetch_results(attribute='energy'))
    energies_c = array(c_only_dataset.fetch_results(attribute='energy'))
    energies_hc = array(h_and_c_dataset.fetch_results(attribute='energy'))
    #find the minimum
    emin = min(energies_hc)
    

We plot the energy values varying the grid spacing or the wavelet extension
    
    
    [41]:
    
    
    
    import matplotlib.pyplot as plt
    %matplotlib inline
    
    plt.xlabel('Grid step (Bohr)')
    plt.plot(hgrids,energies_h-emin,label='rmult=3.5')
    plt.plot(hgrids,energies_hc-emin,label='varying hgrids+rmult')
    plt.yscale('log')
    plt.legend(loc='best');
    

![../_images/school_Introduction_104_0.png](../_images/school_Introduction_104_0.png)

Likewise, we plot the energy values for the grip spacing
    
    
    [42]:
    
    
    
    plt.xlabel('Rmult value')
    plt.plot(rmult,energies_c-emin,label='hgrid=0.55')
    plt.plot(rmult,energies_hc-emin,label='varying hgrids+crmult')
    plt.yscale('log')
    plt.legend(loc='best');
    

![../_images/school_Introduction_106_0.png](../_images/school_Introduction_106_0.png)

Importantly, both hgrids and rmult have to be decreased and increased (respectively) in order to achieve convergence. Increasing only one of the two parameter will eventually lead to **saturation of the absolute error** on the energy.

Compare the values of the HOMO and HOMO-1 eigenvalues for the LDA, PBE, HF and PBE0 functionals. The corresponding outputs are already available in the directory `xc-N2`.

The calculation were run with `hgrid=.3` and `rmult=6` using the `Dataset` class, as detailed below.

**Hint** : the attributes of a `Logfile` object are listed [here](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/_modules/BigDFT/Logfiles.html#get_logs)
    
    
    [43]:
    
    
    
    xc_list = ['LDA','PBE','HF','PBE0']
    
    
    
    [44]:
    
    
    
    from BigDFT import Datasets as D
    
    inp = I.Inputfile()
    inp.set_hgrid(.3)
    inp.set_rmult(6)
    pos = N2.get_posinp()
    study = C.SystemCalculator(skip=True,verbose=False)
    
    xc_dataset = D.Dataset('xc')
    for xc in xc_list:
        inp_run = deepcopy(inp)
        inp_run.set_xc(xc)
        if xc in ['HF','PBE0']:
            inp_run['psppar.N']={'Pseudopotential XC': 1}
        xc_dataset.append_run(id={'xc':xc},run_dir='xc-N2',input=inp_run,posinp=pos,runner=study)
    
    
    
    [45]:
    
    
    
    xc_dataset.run()
    
    
    
     <BigDFT> log of the run will be written in logfile: ./log-xc__LDA.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-xc__LDA.14:48:30.018.yaml
     <BigDFT> log of the run will be written in logfile: ./log-xc__PBE.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-xc__PBE.14:48:50.011.yaml
     <BigDFT> log of the run will be written in logfile: ./log-xc__HF.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-xc__HF.14:49:19.079.yaml
     <BigDFT> log of the run will be written in logfile: ./log-xc__PBE0.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-xc__PBE0.14:51:12.696.yaml
    
    
    
    [45]:
    
    
    
    {0: <BigDFT.Logfiles.Logfile at 0x7f46bb5fc280>,
     1: <BigDFT.Logfiles.Logfile at 0x7f46bb60d640>,
     2: <BigDFT.Logfiles.Logfile at 0x7f46bb5fce80>,
     3: <BigDFT.Logfiles.Logfile at 0x7f46bb5d0e80>}
    
    
    
    [46]:
    
    
    
    from numpy import array
    
    evals = array(xc_dataset.fetch_results(attribute='evals'))
    
    plt.plot(xc_list,evals[:,0,0,:],'o');
    

![../_images/school_Introduction_113_0.png](../_images/school_Introduction_113_0.png)

  1. Compare other attributes of the `Logfile` instance of N2, such as the energy contributions (Hartree, ions, XC, …), depending on the XC functional

  2. Compare the convergence characteristics (`hgrid` and `rmult`) of N2 depending on the XC functional (semilocal vs non-local)

  3. Compute the dissociation energies of CH4 (data [here](https://aip.scitation.org/doi/10.1063/1.469843)) (**Advanced**)

# Logfiles analysis

Let us inspect the result of a BigDFT calculation from the `Logfile` class.

An instance is returned after the execution is finished in the form of a `yaml` file, from which the `Logfile` object is extracted.

Let us for example investigate the logfile of the LDA calculation of N2.
    
    
    [98]:
    
    
    
    from BigDFT import Logfiles as L
    
    logfile = L.Logfile('./xc-N2/log-xc__LDA.yaml')
    

From this instance, it is first possible to visualize the associated system
    
    
    [104]:
    
    
    
    from BigDFT import Systems as S
    
    sys = S.system_from_log(logfile,fragmentation='full')
    sys.display();
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

The information of the logfile are presented clearly
    
    
    [105]:
    
    
    
    print(logfile)
    
    
    
    - Atom types:
      - N
    - cell: Free BC
    - number_of_orbitals: 5
    - posinp_file: xc__LDA.yaml
    - XC_parameter: -20
    - grid_spacing: 0.3
    - spin_polarization: 1
    - total_magn_moment: 0
    - system_charge: 0
    - rmult: 6
    - dipole:
      - -7.546821e-05
      - -7.546821e-05
      - -0.0001150379
    - energy: -19.889158366113875
    - fermi_level: -0.382575362697
    - forcemax: 0.01184049963069
    - forcemax_cv: 0.0
    - gnrm_cv: 0.0001
    - nat: 2
    - symmetry: disabled
    - No. of KS orbitals:
      - 5
    
    

The `yaml` serialization is easily obtainable by calling the `log` attribute, in the form of a `dict`
    
    
    [106]:
    
    
    
    print(dump(logfile.log))
    
    
    
    Accumulated memory requirements during principal run stages (MiB.KiB):
      Density Construction: 192.2
      Hamiltonian application: 193.614
      Kernel calculation: 268.641
      Orbitals Orthonormalization: 193.614
      Poisson Solver: 274.794
    Atomic Forces (Ha/Bohr):
    - N:
      - 0.0
      - -3.388131789017e-21
      - -0.01184049963069
    - N:
      - 0.0
      - 3.388131789017e-21
      - 0.01184049963069
    Atomic System Properties:
      Boundary Conditions: Free
      Number of Symmetries: 0
      Number of atomic types: 1
      Number of atoms: 2
      Space group: disabled
      Types of atoms:
      - N
    Atomic structure:
      Rigid Shift Applied (AU):
      - 8.1
      - 8.1
      - 9.15
      position offset:
      - -8.1
      - -8.1
      - -9.15
      positions:
      - N:
        - 4.286335408
        - 4.286335408
        - 5.39077148
      - N:
        - 4.286335408
        - 4.286335408
        - 4.29317148
      units: angstroem
    Average noise forces:
      total: 2.6498158e-05
      x: -1.62783873e-05
      y: -1.62783874e-05
      z: 1.31217602e-05
    Basis set definition:
      Coarse and Fine Radii Multipliers:
      - 6.0
      - 6.0
      Suggested Grid Spacings (a0):
      - 0.3
      - 0.3
      - 0.3
    BigDFT infocode: 0
    Box Grid spacings:
    - 0.3
    - 0.3
    - 0.3
    Calculate Non Local forces: true
    Calculate local forces: true
    Clean forces norm (Ha/Bohr):
      fnrm2: 0.0002803948630088
      maxval: 0.01184049963069
    Code logo: '__________________________________ A fast and precise DFT wavelet code
      |     |     |     |     |     | |     |     |     |     |     |      BBBB         i       gggggg
      |_____|_____|_____|_____|_____|     B    B               g |     |  :  |  :  |     |     |    B     B        i     g
      |     |-0+--|-0+--|     |     |    B    B         i     g        g |_____|__:__|__:__|_____|_____|___
      BBBBB          i     g         g |  :  |     |     |  :  |     |    B    B         i     g         g
      |--+0-|     |     |-0+--|     |    B     B     iiii     g         g |__:__|_____|_____|__:__|_____|    B     B        i      g        g
      |     |  :  |  :  |     |     |    B BBBB        i        g      g |     |-0+--|-0+--|     |     |    B        iiiii          gggggg
      |_____|__:__|__:__|_____|_____|__BBBBB |     |     |     |  :  |     |                           TTTTTTTTT
      |     |     |     |--+0-|     |  DDDDDD          FFFFF        T |_____|_____|_____|__:__|_____|
      D      D        F        TTTT T |     |     |     |  :  |     |D        D      F        T     T
      |     |     |     |--+0-|     |D         D     FFFF     T     T |_____|_____|_____|__:__|_____|D___      D     F         T    T
      |     |     |  :  |     |     |D         D     F          TTTTT |     |     |--+0-|     |     |
      D        D     F         T    T |_____|_____|__:__|_____|_____|          D     F        T     T
      |     |     |     |     |     |         D               T    T |     |     |     |     |     |   DDDDDD       F         TTTT
      |_____|_____|_____|_____|_____|______                    www.bigdft.org   '
    Communication checks:
      Reverse transpositions: true
      Transpositions: true
    Compilation options:
      Compiler flags:
        CFLAGS: -g -O2
        CXXFLAGS: -g -O2
        FCFLAGS: -O2 -Wno-error -fbounds-check -fbacktrace -ffpe-trap=invalid,zero,overflow
          -fopenmp -m64 -g -Wl,--no-as-needed -ldl -fallow-argument-mismatch
      Compilers (CC, FC, CXX):
      - gcc
      - mpifort
      - g++
      Configure arguments: (...)
    DFT parameters:
      eXchange Correlation:
        Exchange-Correlation reference: 'XC: Teter 93'
        Reference Papers:
        - Comput. Phys. Commun. 183, 2272 (2012)
        - S. Goedecker, M. Teter, and J. Hutter, Phys. Rev. B 54, 1703 (1996)
        Spin polarization: false
        XC ID: -20
        XC functional implementation: libXC
    Data Writing directory: ./
    Electric Dipole Moment (AU):
      P vector:
      - -7.546821e-05
      - -7.546821e-05
      - -0.0001150379
      norm(P): 0.00015692235
    Electric Dipole Moment (Debye):
      P vector:
      - -0.000191821
      - -0.000191821
      - -0.0002923972
      norm(P): 0.000398856792
    Energy (Hartree): -19.889158366113875
    Estimated Memory Peak (MB): 274
    Force Norm (Hartree/Bohr): 0.016744995162996684
    GPU acceleration: false
    Geometry Optimization Parameters:
      Algorithm: none
      Fluctuation in forces: 1.0
      Maximum in forces: 0.0
      Maximum steps: 1
      Random atomic displacement: 0.0
      Steepest descent step: 4.0
    Ground State Optimization:
    - Hamiltonian Optimization:
      - Subspace Optimization:
          Non-Hermiticity of Hamiltonian in the Subspace: 1.1e-29
          Orbitals:
          - e: -1.041921681617
            f: 2.0
          - e: -0.4931878871014
            f: 2.0
          - e: -0.4364601439754
            f: 2.0
          - e: -0.4364600985988
            f: 2.0
          - e: -0.382575362697
            f: 2.0
          Wavefunctions Iterations:
          - D: 0.0108
            DIIS weights:
            - 1.0
            - 1.0
            EKS: -19.599442009873712
            Energies:
              EH: 26.4374284056
              EXC: -4.59353822458
              Ekin: 13.1903000846
              Enl: 1.87025796309
              Epot: -21.6971880749
              EvXC: -6.01510228509
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999991874
            gnrm: 0.327
            iter: 1
          - D: -0.267
            DIIS weights:
            - -0.0193
            - 1.02
            - -0.00444
            EKS: -19.86603074686917
            Energies:
              EH: 28.0070497949
              EXC: -4.83337440271
              Ekin: 14.5862099594
              Enl: 1.87459079009
              Epot: -21.8711736933
              EvXC: -6.33171403218
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999991103
            gnrm: 0.112
            iter: 2
          - D: -0.0197
            DIIS weights:
            - -0.0496
            - -0.311
            - 1.36
            - -0.000167
            EKS: -19.88574559888267
            Energies:
              EH: 27.8466684777
              EXC: -4.79736322355
              Ekin: 14.5652554957
              Enl: 1.75939315938
              Epot: -21.9036916524
              EvXC: -6.28427673737
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999991363
            gnrm: 0.0465
            iter: 3
          - D: -0.00319
            DIIS weights:
            - 0.0074
            - 0.00227
            - -0.163
            - 1.15
            - -1.17e-05
            EKS: -19.888938639401168
            Energies:
              EH: 27.8580241523
              EXC: -4.79644006663
              Ekin: 14.650953604
              Enl: 1.76326525276
              Epot: -21.984858617
              EvXC: -6.28311297722
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990899
            gnrm: 0.0147
            iter: 4
          - D: -0.000175
            DIIS weights:
            - 0.000392
            - 0.0201
            - -0.0779
            - -0.194
            - 1.25
            - -1.4e-06
            EKS: -19.889113592353517
            Energies:
              EH: 27.8467924008
              EXC: -4.79473286047
              Ekin: 14.6632488885
              Enl: 1.75246638581
              Epot: -21.9972192265
              EvXC: -6.28086325865
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990778
            gnrm: 0.00417
            iter: 5
          - D: -3.15e-05
            DIIS weights:
            - -0.000504
            - -0.00289
            - 0.0237
            - -0.0483
            - -0.349
            - 1.38
            - -2.32e-07
            EKS: -19.889145072041345
            Energies:
              EH: 27.8474270849
              EXC: -4.79498675479
              Ekin: 14.6734260845
              Enl: 1.75179027165
              Epot: -22.0061999013
              EvXC: -6.28119995034
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990731
            gnrm: 0.00208
            iter: 6
          - D: -8.62e-06
            DIIS weights:
            - -0.00117
            - 0.00272
            - 0.00774
            - 0.0534
            - -0.679
            - 1.62
            - -6.3e-08
            EKS: -19.88915368972063
            Energies:
              EH: 27.8475331181
              EXC: -4.79509022639
              Ekin: 14.6773557191
              Enl: 1.75059978639
              Epot: -22.0088750039
              EvXC: -6.28133679073
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990723
            gnrm: 0.0012
            iter: 7
          - D: -3.38e-06
            DIIS weights:
            - 0.000933
            - -0.00748
            - 0.00505
            - 0.12
            - -0.829
            - 1.71
            - -1.73e-08
            EKS: -19.88915706546748
            Energies:
              EH: 27.8474618626
              EXC: -4.79512344364
              Ekin: 14.6788591005
              Enl: 1.74992235176
              Epot: -22.0097864012
              EvXC: -6.28138082733
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990725
            gnrm: 0.000625
            iter: 8
          - D: -1.1e-06
            DIIS weights:
            - -0.00254
            - -0.00483
            - 0.121
            - -0.342
            - -0.0805
            - 1.31
            - -2.52e-09
            EKS: -19.88915816781627
            Energies:
              EH: 27.847315648
              EXC: -4.79512716638
              Ekin: 14.6794324855
              Enl: 1.74951890641
              Epot: -22.0101049665
              EvXC: -6.28138585872
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990726
            gnrm: 0.000264
            iter: 9
          - D: -1.83e-07
            DIIS weights:
            - -0.00216
            - 0.00429
            - 0.0526
            - -0.01
            - -0.481
            - 1.44
            - -4.05e-10
            EKS: -19.889158351154023
            Energies:
              EH: 27.8472885182
              EXC: -4.79513511046
              Ekin: 14.6796604001
              Enl: 1.74936581972
              Epot: -22.0102097031
              EvXC: -6.28139639829
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990726
            gnrm: 8.56e-05
            iter: 10
          - &id001
            D: -1.5e-08
            EKS: -19.889158366113875
            Energies:
              EH: 27.8472608482
              EXC: -4.79513251984
              Eion: 12.0530523624
              Ekin: 14.6796478684
              Enl: 1.7493457461
              Epot: -22.0102039625
              EvXC: -6.28139298747
            GPU acceleration: false
            Hamiltonian Applied: true
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Total electronic charge: 9.999999990726
            gnrm: 8.56e-05
            iter: 11
    High Res. box is treated separately: true
    Input Hamiltonian:
      Accuracy estimation for this run:
        Convergence Criterion: 2.98e-05
        Energy: 0.000149
      Atomic Input Orbital Generation:
      - Atom Type: N
        Electronic configuration:
          p:
          - 1.0
          - 1.0
          - 1.0
          s:
          - 2.0
      Deviation from normalization: 5.49e-07
      EKS: -19.610209365963435
      Energies:
        EH: 27.4148935003
        EXC: -4.70955110299
        Ekin: 13.9049636532
        Enl: 2.36627080396
        Epot: -21.978325416
        EvXC: -6.16827383377
      Expected kinetic energy: 13.904814679
      GPU acceleration: false
      IG wavefunctions defined: true
      Input Guess Overlap Matrices:
        Calculated: true
        Diagonalized: true
      Orbitals:
      - e: -1.055295241538
        f: 2.0
      - e: -0.526343538307
        f: 2.0
      - e: -0.4497660615404
        f: 2.0
      - e: -0.4497660067994
        f: 2.0
      - e: -0.3984990982962
        f: 2.0
      - e: -0.09753192536927
        f: 0.0
      - e: -0.09753187279788
        f: 0.0
      - e: 0.7245931378153
        f: 0.0
      Poisson Solver:
        BC: Free
        Box:
        - 139
        - 139
        - 153
        MPI tasks: 1
      Policy: Wavefunctions from PSP Atomic Orbitals
      Total No. of Atomic Input Orbitals: 8
      Total electronic charge: 9.99999999057
      Wavelet conversion succeeded: true
    Input Occupation Numbers:
    - Occupation Numbers:
        Orbitals No. 1-5: 2.0
    Interaction energy ions multipoles: 0.0
    Interaction energy multipoles multipoles: 0.0
    Ion-Ion interaction energy: 12.0530523624271
    Last Iteration: *id001
    Material acceleration: false
    Max No. of dictionaries used: 4938
    Maximal OpenMP threads per MPI task: 1
    Memory Consumption Report:
      Memory occupation:
        Memory Peak of process: 327.764 MB
        Peak Value (MB): 298.198
        for the array: zt
        in the routine: G_PoissonSolver
      Remaining Memory (B): 0
      Tot. No. of Allocations: 3546
      Tot. No. of Deallocations: 3546
    Memory requirements for principal quantities (MiB.KiB):
      All (distributed) orbitals: 8.416
      Full Uncompressed (ISF) grid: 22.567
      Nonlocal Pseudopotential Arrays: 0.113
      Single orbital: 0.861
      Subspace Matrix: 0.1
      Wavefunction storage size: 58.859
      Workspaces storage size: 1.1012
    Multipole analysis origin:
    - 8.1
    - 8.1
    - 9.15
    NonLocal PSP Projectors Descriptors:
      Creation strategy: On-the-fly
      Cumulative size of masking arrays: 3984
      Maximum size of masking arrays for a projector: 1992
      Percent of zero components: 14
      Size of workspaces: 57504
      Total number of components: 14372
      Total number of projectors: 2
    Number of MPI tasks: 1
    Number of dictionary folders allocated: 1
    OpenMP parallelization: true
    Orbitals Repartition:
      MPI tasks  0- 0: 5
    Poisson Kernel Creation:
      Boundary Conditions: Free
      Memory Requirements per MPI task:
        Density (MB): 23.93
        Full Grid Arrays (MB): 22.55
        Kernel (MB): 24.42
    Poisson Kernel Initialization:
      MPI tasks: 1
      OpenMP threads per MPI task: 1
      environment:
        cavity: none
        fd_order: 16
        itermax: 200
        minres: 1.0e-08
        pb_method: none
      kernel:
        isf_order: 16
        screening: 0
        stress_tensor: true
      setup:
        accel: none
        global_data: false
        output: none
        taskgroup_size: 0
        verbose: true
    Poisson Solver:
      BC: Free
      Box:
      - 139
      - 139
      - 153
      MPI tasks: 1
    Post Optimization Parameters:
      Finite-Size Effect estimation:
        Scheduled: false
    Properties of atoms in the system:
    - Grid Spacing threshold (AU): 0.64
      Local Pseudo Potential (HGH convention):
        Coefficients (c1 .. c4):
        - -12.23482
        - 1.76641
        - 0.0
        - 0.0
        Rloc: 0.28918
      No. of Atoms: 2
      No. of Electrons: 5
      No. of projectors: 1
      NonLocal PSP Parameters:
      - Channel (l): 0
        Rloc: 0.2566
        h_ij matrix:
        - - 13.55224
          - 0.0
          - 0.0
        - - 0.0
          - 0.0
          - 0.0
        - - 0.0
          - 0.0
          - 0.0
      - Channel (l): 1
        Rloc: 0.27013
        h_ij matrix:
        - - 0.0
          - 0.0
          - 0.0
        - - 0.0
          - 0.0
          - 0.0
        - - 0.0
          - 0.0
          - 0.0
      PSP XC: 'XC: Teter 93'
      Pseudopotential type: HGH-K
      Radii of active regions (AU):
        Coarse: 1.37026
        Coarse PSP: 0.67533
        Fine: 0.2566
        Source: Hard-Coded
      Symbol: N
    Quadrupole Moment (AU):
      Q matrix:
      - - 1.136
        - -6.0873e-07
        - -0.0002684
      - - -6.0873e-07
        - 1.136
        - -0.0002684
      - - -0.0002684
        - -0.0002684
        - -2.272
      trace: 0.0
    Raw forces norm (Ha/Bohr):
      fnrm2: 0.0002803969784791
      maxval: 0.01184985563241
    Reference Paper: The Journal of Chemical Physics 129, 014109 (2008)
    Root process Hostname: localhost
    Self-Consistent Cycle Parameters:
      Density/Potential:
        Max. Iterations: 1
      Wavefunction:
        CG Steps for Preconditioner: 6
        DIIS History length: 6
        Gradient Norm Threshold: 0.0001
        Input wavefunction policy: INPUT_PSI_LCAO
        Max. Subspace Diagonalizations: 1
        Max. Wfn Iterations: 50
        Number of plotted density orbitals: 0
        Output grid policy: NONE
        Output wavefunction policy: NONE
        Virtual orbitals: 0
    Sizes of the simulation domain:
      AU:
      - 16.2
      - 16.2
      - 18.3
      Angstroem:
      - 8.5727
      - 8.5727
      - 9.6839
      Grid Spacing Units:
      - 54
      - 54
      - 61
      High resolution region boundaries (GU):
        From:
        - 22
        - 22
        - 22
        To:
        - 32
        - 32
        - 39
    Spin treatment: Averaged
    Spreads of the electronic density (AU):
    - 0.8724061
    - 0.8724061
    - 1.396506
    Timestamp of this run: 2022-09-07 14:48:30.018000
    Timings for root process:
      CPU time (s): 19.73
      Elapsed time (s): 19.83
    Total Number of Electrons: 10
    Total Number of Orbitals: 5
    Total electronic charge: 9.999999990726
    Total ionic charge: -10.0
    Version Number: 1.9.2
    Walltime since initialization: 19.878042757
    Wavefunctions Descriptors, full simulation domain:
      Coarse resolution grid:
        No. of points: 102710
        No. of segments: 2746
      Fine resolution grid:
        No. of points: 1066
        No. of segments: 154
    Wavefunctions memory occupation for root MPI process: 4 MB 207 KB 608 B
    chess:
      foe:
        accuracy_entropy: 0.0001
        accuracy_foe: 1.0e-05
        accuracy_ice: 1.0e-08
        accuracy_penalty: 1.0e-05
        adjust_fscale: true
        betax_foe: -1000.0
        betax_ice: -1000.0
        ef_interpol_chargediff: 1.0
        ef_interpol_det: 1.0e-12
        eval_range_foe:
        - -0.5
        - 0.5
        evbounds_nsatur: 3
        evboundsshrink_nsatur: 4
        fscale: 0.05
        fscale_ediff_low: 5.0e-05
        fscale_ediff_up: 0.0001
        fscale_lowerbound: 0.005
        fscale_upperbound: 0.05
        matmul_optimize_load_balancing: false
        occupation_function: 102
      lapack:
        blocksize_pdgemm: -8
        blocksize_pdsyev: -8
        maxproc_pdgemm: 4
        maxproc_pdsyev: 4
      ntpoly:
        convergence_density: 1.0e-10
        convergence_overlap: 1.0e-10
        threshold_density: 0.0
        threshold_overlap: 0.0
    dft:
      alpha_hf: -1.0
      calculate_strten: true
      disablesym: false
      dispersion: 0
      elecfield:
      - 0.0
      - 0.0
      - 0.0
      external_potential: 0.0
      gnrm_cv: 0.0001
      gnrm_cv_virt: 0.0001
      hgrids: 0.3
      idsx: 6
      inputpsiid: 0
      itermax: 50
      itermax_occ_ctrl: 0
      itermax_virt: 50
      itermin: 0
      ixc: -20
      mpol: 0
      ncong: 6
      ncongt: 30
      ngrids:
      - 0
      - 0
      - 0
      norbv: 0
      nplot: 0
      nrepmax: 1
      nrepmax_occ_ctrl: 1
      nspin: 1
      nvirt: 0
      occupancy_control: None
      output_denspot: 0
      plot_mppot_axes:
      - -1
      - -1
      - -1
      plot_pot_axes:
      - -1
      - -1
      - -1
      projection: gaussian
      qcharge: 0
      rbuf: 0.0
      rmult: 6
    geopt:
      beta_stretchx: 5e-1
      betax: 4.0
      forcemax: 0.0
      frac_fluct: 1.0
      method: none
      ncount_cluster_x: 1
      randdis: 0.0
    kpt:
      bands: false
      kpt:
      - - 0.0
        - 0.0
        - 0.0
      method: manual
      wkpt:
      - 1.0
    lin_basis:
      alpha_diis: 1.0
      alpha_sd: 1.0
      correction_orthoconstraint: 1
      deltae_cv: 0.0001
      extended_ig: false
      fix_basis: 1.0e-10
      gnrm_cv:
      - 0.01
      - 0.0001
      gnrm_dyn: 0.0001
      gnrm_ig: 0.001
      idsx:
      - 6
      - 6
      min_gnrm_for_dynamic: 0.001
      nit:
      - 4
      - 5
      nit_ig: 50
      nstep_prec: 5
      orthogonalize_ao: true
      orthogonalize_sfs: true
      reset_DIIS_history: false
    lin_basis_params:
      ao_confinement: 0.0083
      confinement:
      - 0.0083
      - 0.0
      nbasis: 4
      rloc:
      - 7.0
      - 7.0
      rloc_kernel: 9.0
      rloc_kernel_foe: 14.0
    lin_general:
      calc_dipole: false
      calc_quadrupole: false
      calculate_FOE_eigenvalues:
      - 0
      - -1
      calculate_onsite_overlap: false
      cdft_add_w_guess: 0.0
      charge_multipoles: 0
      check_multipoles: true
      conf_damping: -0.5
      consider_entropy: false
      extra_states: 0
      frag_neighbour_cutoff: 12.0d0
      frag_num_neighbours: 0
      hybrid: false
      kernel_restart_mode: 0
      kernel_restart_noise: 0.0d0
      max_inversion_error: 1.d0
      multipole_centers: 0.0
      nit:
      - 100
      - 100
      output_coeff: 0
      output_fragments: 0
      output_mat: 0
      output_matmul: false
      output_multipole_matrices: true
      output_wf: 0
      plot_locreg_grids: false
      precision_FOE_eigenvalues: 0.005
      rpnrm_cv:
      - 1.0e-12
      - 1.0e-12
      subspace_diag: false
      support_function_multipoles: false
      taylor_order: 0
    lin_kernel:
      alpha_fit_coeff: false
      alpha_sd_coeff: 0.2
      alphamix:
      - 0.5
      - 0.5
      coeff_scaling_factor: 1.0
      delta_pnrm: -1.0
      diag_start: false
      gnrm_cv_coeff:
      - 1.0e-05
      - 1.0e-05
      idsx:
      - 0
      - 0
      idsx_coeff:
      - 0
      - 0
      linear_method: DIAG
      mixing_method: DEN
      nit:
      - 5
      - 5
      nstep:
      - 1
      - 1
      rpnrm_cv:
      - 1.0e-10
      - 1.0e-10
    logfile: true
    md:
      always_from_scratch: false
      mdsteps: 0
      no_translation: false
      print_frequency: 1
      restart_nose: false
      restart_pos: false
      restart_vel: false
      temperature: 300.d0
      thermostat: none
      timestep: 20.d0
      wavefunction_extrapolation: 0
    mix:
      alphadiis: 2.0
      alphamix: 0.0
      diis_sd_switch_tolerance: 0
      iscf: 0
      itrpmax: 1
      norbsempty: 0
      occopt: 1
      rpnrm_cv: 0.0001
      tel: 0.0
    mode:
      add_coulomb_force: false
      method: dft
    outdir: ./
    output:
      apply_coeffs: true
      atomic_density_matrix: None
      coupling_matrix: complete
      orbitals: None
      outputpsiid: wavefunction
      sdos: false
      verbosity: 2
    perf:
      FOE_restart: 0
      accel: false
      adjust_kernel_iterations: true
      adjust_kernel_threshold: true
      blas: false
      calculate_KS_residue: true
      calculate_forces: true
      calculate_gap: false
      check_matrix_compression: true
      check_overlap: 1
      check_sumrho: 1
      coeff_weight_analysis: false
      correction_co_contra: true
      debug: false
      domain: null
      enable_matrix_taskgroups: true
      exctxpar: OP2P
      experimental_mode: false
      explicit_locregcenters: false
      fftcache: 8192
      foe_gap: false
      hamapp_radius_incr: 8
      ig_blocks:
      - 300
      - 800
      ig_diag: true
      ig_norbp: 5
      ig_tol: 0.0001
      imethod_overlap: 1
      inguess_geopt: 0
      intermediate_forces: false
      iterative_orthogonalization: false
      kappa_conv: 0.1
      linear: false
      loewdin_charge_analysis: false
      methortho: 0
      mixing_after_inputguess: 1
      mp_isf: 16
      multipole_preserving: false
      ocl_devices: null
      ocl_platform: null
      projrad: 15.0
      psp_onfly: true
      rho_commun: DEF
      signaling: false
      signaltimeout: 0
      store_index: true
      store_overlap_matrices: true
      tolsym: 1.0e-08
      unblock_comms: false
      wf_extent_analysis: false
    posinp:
      cell:
      - .inf
      - .inf
      - .inf
      positions:
      - N:
        - 0.0
        - 0.0
        - 0.5488
        frag:
        - N
        - 0
      - N:
        - 0.0
        - 0.0
        - -0.5488
        frag:
        - N
        - 1
      properties:
        format: yaml
        source: xc__LDA.yaml
      units: angstroem
    psolver:
      environment:
        cavity: none
        fd_order: 16
        itermax: 200
        minres: 1.0e-08
        pb_method: none
      kernel:
        isf_order: 16
        screening: 0
        stress_tensor: true
      setup:
        accel: none
        global_data: false
        output: none
        taskgroup_size: 0
        verbose: true
    psppar.N:
      Atomic number: 7
      Local Pseudo Potential (HGH convention):
        Coefficients (c1 .. c4):
        - -12.23481988
        - 1.76640728
        - 0.0
        - 0.0
        Rloc: 0.28917923
      No. of Electrons: 5
      NonLocal PSP Parameters:
      - Channel (l): 0
        Rloc: 0.25660487
        h_ij terms:
        - 13.55224272
        - 0.0
        - 0.0
        - 0.0
        - 0.0
        - 0.0
      - Channel (l): 1
        Rloc: 0.27013369
        h_ij terms:
        - 0.0
        - 0.0
        - 0.0
        - 0.0
        - 0.0
        - 0.0
      Pseudopotential XC: 1
      Pseudopotential type: HGH-K
      Radii of active regions (AU):
        Coarse: 1.370256482166319
        Coarse PSP: 0.675334225
        Fine: 0.25660487
        Source: Hard-Coded
      Source: Hard-Coded
    radical: xc__LDA
    run_from_files: true
    sic:
      sic_alpha: 0.0
      sic_approach: none
    skip: false
    tddft:
      decompose_perturbation: none
      tddft_approach: none
    
    

For example, information on the Poisson solver is accessible by
    
    
    [107]:
    
    
    
    logfile.log["Poisson Solver"]
    
    
    
    [107]:
    
    
    
    {'BC': 'Free', 'Box': [139, 139, 153], 'MPI tasks': 1}
    

Or similarly, the self-consistent field cycle
    
    
    [109]:
    
    
    
    print(dump(logfile.log['Ground State Optimization']))
    
    
    
    - Hamiltonian Optimization:
      - Subspace Optimization:
          Non-Hermiticity of Hamiltonian in the Subspace: 1.1e-29
          Orbitals:
          - e: -1.041921681617
            f: 2.0
          - e: -0.4931878871014
            f: 2.0
          - e: -0.4364601439754
            f: 2.0
          - e: -0.4364600985988
            f: 2.0
          - e: -0.382575362697
            f: 2.0
          Wavefunctions Iterations:
          - D: 0.0108
            DIIS weights:
            - 1.0
            - 1.0
            EKS: -19.599442009873712
            Energies:
              EH: 26.4374284056
              EXC: -4.59353822458
              Ekin: 13.1903000846
              Enl: 1.87025796309
              Epot: -21.6971880749
              EvXC: -6.01510228509
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999991874
            gnrm: 0.327
            iter: 1
          - D: -0.267
            DIIS weights:
            - -0.0193
            - 1.02
            - -0.00444
            EKS: -19.86603074686917
            Energies:
              EH: 28.0070497949
              EXC: -4.83337440271
              Ekin: 14.5862099594
              Enl: 1.87459079009
              Epot: -21.8711736933
              EvXC: -6.33171403218
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999991103
            gnrm: 0.112
            iter: 2
          - D: -0.0197
            DIIS weights:
            - -0.0496
            - -0.311
            - 1.36
            - -0.000167
            EKS: -19.88574559888267
            Energies:
              EH: 27.8466684777
              EXC: -4.79736322355
              Ekin: 14.5652554957
              Enl: 1.75939315938
              Epot: -21.9036916524
              EvXC: -6.28427673737
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999991363
            gnrm: 0.0465
            iter: 3
          - D: -0.00319
            DIIS weights:
            - 0.0074
            - 0.00227
            - -0.163
            - 1.15
            - -1.17e-05
            EKS: -19.888938639401168
            Energies:
              EH: 27.8580241523
              EXC: -4.79644006663
              Ekin: 14.650953604
              Enl: 1.76326525276
              Epot: -21.984858617
              EvXC: -6.28311297722
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990899
            gnrm: 0.0147
            iter: 4
          - D: -0.000175
            DIIS weights:
            - 0.000392
            - 0.0201
            - -0.0779
            - -0.194
            - 1.25
            - -1.4e-06
            EKS: -19.889113592353517
            Energies:
              EH: 27.8467924008
              EXC: -4.79473286047
              Ekin: 14.6632488885
              Enl: 1.75246638581
              Epot: -21.9972192265
              EvXC: -6.28086325865
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990778
            gnrm: 0.00417
            iter: 5
          - D: -3.15e-05
            DIIS weights:
            - -0.000504
            - -0.00289
            - 0.0237
            - -0.0483
            - -0.349
            - 1.38
            - -2.32e-07
            EKS: -19.889145072041345
            Energies:
              EH: 27.8474270849
              EXC: -4.79498675479
              Ekin: 14.6734260845
              Enl: 1.75179027165
              Epot: -22.0061999013
              EvXC: -6.28119995034
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990731
            gnrm: 0.00208
            iter: 6
          - D: -8.62e-06
            DIIS weights:
            - -0.00117
            - 0.00272
            - 0.00774
            - 0.0534
            - -0.679
            - 1.62
            - -6.3e-08
            EKS: -19.88915368972063
            Energies:
              EH: 27.8475331181
              EXC: -4.79509022639
              Ekin: 14.6773557191
              Enl: 1.75059978639
              Epot: -22.0088750039
              EvXC: -6.28133679073
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990723
            gnrm: 0.0012
            iter: 7
          - D: -3.38e-06
            DIIS weights:
            - 0.000933
            - -0.00748
            - 0.00505
            - 0.12
            - -0.829
            - 1.71
            - -1.73e-08
            EKS: -19.88915706546748
            Energies:
              EH: 27.8474618626
              EXC: -4.79512344364
              Ekin: 14.6788591005
              Enl: 1.74992235176
              Epot: -22.0097864012
              EvXC: -6.28138082733
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990725
            gnrm: 0.000625
            iter: 8
          - D: -1.1e-06
            DIIS weights:
            - -0.00254
            - -0.00483
            - 0.121
            - -0.342
            - -0.0805
            - 1.31
            - -2.52e-09
            EKS: -19.88915816781627
            Energies:
              EH: 27.847315648
              EXC: -4.79512716638
              Ekin: 14.6794324855
              Enl: 1.74951890641
              Epot: -22.0101049665
              EvXC: -6.28138585872
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990726
            gnrm: 0.000264
            iter: 9
          - D: -1.83e-07
            DIIS weights:
            - -0.00216
            - 0.00429
            - 0.0526
            - -0.01
            - -0.481
            - 1.44
            - -4.05e-10
            EKS: -19.889158351154023
            Energies:
              EH: 27.8472885182
              EXC: -4.79513511046
              Ekin: 14.6796604001
              Enl: 1.74936581972
              Epot: -22.0102097031
              EvXC: -6.28139639829
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990726
            gnrm: 8.56e-05
            iter: 10
          - D: -1.5e-08
            EKS: -19.889158366113875
            Energies:
              EH: 27.8472608482
              EXC: -4.79513251984
              Eion: 12.0530523624
              Ekin: 14.6796478684
              Enl: 1.7493457461
              Epot: -22.0102039625
              EvXC: -6.28139298747
            GPU acceleration: false
            Hamiltonian Applied: true
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Total electronic charge: 9.999999990726
            gnrm: 8.56e-05
            iter: 11
    
    

All `keys` elements are listed afterwards
    
    
    [108]:
    
    
    
    print(logfile.log.keys())
    
    
    
    dict_keys(['Code logo', 'Reference Paper', 'Version Number', 'Timestamp of this run', 'Root process Hostname', 'Number of MPI tasks', 'OpenMP parallelization', 'Maximal OpenMP threads per MPI task', 'Compilation options', 'radical', 'outdir', 'logfile', 'run_from_files', 'skip', 'dft', 'psolver', 'chess', 'output', 'kpt', 'geopt', 'md', 'mix', 'sic', 'tddft', 'mode', 'perf', 'lin_general', 'lin_basis', 'lin_kernel', 'lin_basis_params', 'psppar.N', 'posinp', 'Data Writing directory', 'Atomic System Properties', 'Geometry Optimization Parameters', 'Material acceleration', 'DFT parameters', 'Basis set definition', 'Self-Consistent Cycle Parameters', 'Post Optimization Parameters', 'Properties of atoms in the system', 'Atomic structure', 'Box Grid spacings', 'Sizes of the simulation domain', 'High Res. box is treated separately', 'Wavefunctions Descriptors, full simulation domain', 'Poisson Kernel Initialization', 'Poisson Kernel Creation', 'Total Number of Electrons', 'Spin treatment', 'Orbitals Repartition', 'Total Number of Orbitals', 'Input Occupation Numbers', 'Wavefunctions memory occupation for root MPI process', 'NonLocal PSP Projectors Descriptors', 'Communication checks', 'Memory requirements for principal quantities (MiB.KiB)', 'Accumulated memory requirements during principal run stages (MiB.KiB)', 'Estimated Memory Peak (MB)', 'Ion-Ion interaction energy', 'Total ionic charge', 'Poisson Solver', 'Interaction energy ions multipoles', 'Interaction energy multipoles multipoles', 'Input Hamiltonian', 'Ground State Optimization', 'Last Iteration', 'GPU acceleration', 'Total electronic charge', 'Multipole analysis origin', 'Electric Dipole Moment (AU)', 'Electric Dipole Moment (Debye)', 'Quadrupole Moment (AU)', 'Spreads of the electronic density (AU)', 'Calculate local forces', 'Calculate Non Local forces', 'Timings for root process', 'BigDFT infocode', 'Average noise forces', 'Clean forces norm (Ha/Bohr)', 'Raw forces norm (Ha/Bohr)', 'Atomic Forces (Ha/Bohr)', 'Energy (Hartree)', 'Force Norm (Hartree/Bohr)', 'Memory Consumption Report', 'Walltime since initialization', 'Max No. of dictionaries used', 'Number of dictionary folders allocated'])
    

Let us inspect a simple example of a solid state calculation by considering a two-dimensional (2D) materials, graphene.
    
    
    [113]:
    
    
    
    gr = L.Logfile("log-graphene.yaml")
    

[Graphene](https://en.wikipedia.org/wiki/Graphene) is a 2D carbon allotrope in the form of a honeycomb network that consists of a two inequivalent triangular lattices, with a C-C bond of 1.42\\(~\\)angstroem, or equivalently, a lattice parameter such that \\(a_0 = 2.46~\\)angstroem.
    
    
    [129]:
    
    
    
    # or gr.log["Atomic structure"]
    gr.astruct
    
    
    
    [129]:
    
    
    
    {'units': 'angstroem',
     'cell': [4.330127018922193, inf, 2.5],
     'positions': [{'C': [0.0, 4.127582245, 1.25]},
      {'C': [2.165063509, 4.127582245, 0.0]},
      {'C': [0.7216878365, 4.127582245, 0.0]},
      {'C': [2.886751346, 4.127582245, 1.25]}],
     'position offset': [0.0, -7.8, 0.0],
     'Rigid Shift Applied (AU)': [0.0, 7.8, 0.0],
     'forces': [{'C': [3.725158813391e-05, 0.0, -1.280528231035e-18]},
      {'C': [3.725158813391e-05, 0.0, 2.817162108277e-18]},
      {'C': [-3.725158813391e-05, 0.0, -2.048845169656e-18]},
      {'C': [-3.725158813391e-05, 0.0, -2.048845169656e-18]}]}
    
    
    
    [118]:
    
    
    
    sys = S.system_from_log(gr,fragmentation='full')
    sys.display();
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

In order to properly characterize extended systems, a \\(k\\)-points mesh is required to handle periodicity.
    
    
    [120]:
    
    
    
    gr.kpt_mesh
    
    
    
    [120]:
    
    
    
    [15, 1, 27]
    

Additionally, mixing is sometimes needed for convergence, such that the effect of abrupt changes in the density are smoothened away.
    
    
    [126]:
    
    
    
    print(dump(gr.log["mix"]))
    # inp["import"] = "mixing"
    
    
    
    alphadiis: 1.d0
    alphamix: 0.8
    diis_sd_switch_tolerance: 0
    iscf: 17
    itrpmax: 200
    norbsempty: 10
    occopt: 1
    rpnrm_cv: 1.0e-10
    tel: 0.01
    
    

The interested reader is invited to go through this [tutorial](../tutorials/SolidState.html)

When analyzing electronic properties, the \\(k\\)-dependence is obtained by plotting the band structure. This is done along a given path, that can be specified by the user.
    
    
    [131]:
    
    
    
    BZ_gr = gr.get_brillouin_zone()
    
    hsp = BZ_gr.special_points # high symmetry points
    [print(i) for i in hsp.items()]
    paths = BZ_gr.special_paths # high symmetry path list
    print(paths)
    
    
    
    spacegroup P6/mmm (191)
    Lattice found: orthorhombic
    irreductible k-points 112
    
    
    
    /home/sam/Software/miniconda/miniconda3/lib/python3.9/site-packages/ase/dft/kpoints.py:655: UserWarning: Please call this function with cell as the first argument
      warnings.warn('Please call this function with cell as the first '
    
    
    
    Interpolation bias 1.0852849288836878e-08
    ('G', array([0., 0., 0.]))
    ('R', array([0.5, 0.5, 0.5]))
    ('S', array([0. , 0.5, 0.5]))
    ('T', array([0.5, 0. , 0.5]))
    ('U', array([0.5, 0.5, 0. ]))
    ('X', array([0. , 0.5, 0. ]))
    ('Y', array([0. , 0. , 0.5]))
    ('Z', array([0.5, 0. , 0. ]))
    [['G', 'X', 'S', 'Y', 'G', 'Z', 'U', 'R', 'T', 'Z'], ['Y', 'T'], ['U', 'X'], ['S', 'R']]
    

Here we choose half the first path, since the 2D character of our system implies no dependence in \\(k_x\\).
    
    
    [132]:
    
    
    
    path = paths[0][:5]
    

Eventually, the band structure is plotted using the `BZ` class by giving a list of special \\(k\\)-points (i.e. the `path` defined above)
    
    
    [133]:
    
    
    
    import BigDFT.BZ as BZ
    
    npts = 200
    path_bs = BZ.BZPath(BZ_gr.lattice,path,hsp,npts=npts)
    
    ax = BZ_gr.plot(path=path_bs,npts=npts)
    ax.set_ylim([-10,5]);
    
    
    
    /home/sam/Software/miniconda/miniconda3/lib/python3.9/site-packages/ase/dft/kpoints.py:357: UserWarning: Please do not use (kpts, x, X) = bandpath(...).  Use path = bandpath(...) and then kpts = path.kpts and (x, X, labels) = path.get_linear_kpoint_axis().
      warnings.warn('Please do not use (kpts, x, X) = bandpath(...).  '
    

![../_images/school_Introduction_143_1.png](../_images/school_Introduction_143_1.png)

From the previous analysis on XC functionals of N2, compare the following physical or numerical properties:

  * the density of states

  * the wavefunction convergence

  * the memory employed

  * …

**Hint** : the `Logfile` are obtained with the fetch_results() method
    
    
    [110]:
    
    
    
    logfiles = xc_dataset.fetch_results()
    
    
    
    [92]:
    
    
    
    from matplotlib import *
    
    fig,ax = plt.subplots(figsize=(8,6))
    for log in logfiles[1:]:
        dos = log.get_dos()
        dos.plot(ax=ax)
    colors = ['tab:blue','tab:orange','tab:green']
    lines = [lines.Line2D([0],[0],color=c) for c in colors]
    ax.legend(lines,xc_list[1:]);
    

![../_images/school_Introduction_147_0.png](../_images/school_Introduction_147_0.png)
    
    
    [95]:
    
    
    
    from matplotlib import *
    
    fig,ax = plt.subplots(figsize=(8,6))
    for log in logfiles[1:]:
        log.wfn_plot()
    colors = ['tab:blue','tab:orange','tab:green']
    lines = [lines.Line2D([0],[0],color=c) for c in colors]
    ax.legend(lines,xc_list[1:]);
    

![../_images/school_Introduction_148_0.png](../_images/school_Introduction_148_0.png)
    
    
    [49]:
    
    
    
    print(logfiles[0])
    print('-------------\n')
    print(dump(logfiles[0].log))
    
    
    
    - Atom types:
      - N
    - cell: Free BC
    - number_of_orbitals: 5
    - posinp_file: xc__LDA.yaml
    - XC_parameter: -20
    - grid_spacing: 0.3
    - spin_polarization: 1
    - total_magn_moment: 0
    - system_charge: 0
    - rmult: 6
    - dipole:
      - -7.546821e-05
      - -7.546821e-05
      - -0.0001150379
    - energy: -19.889158366113875
    - fermi_level: -0.382575362697
    - forcemax: 0.01184049963069
    - forcemax_cv: 0.0
    - gnrm_cv: 0.0001
    - nat: 2
    - symmetry: disabled
    - No. of KS orbitals:
      - 5
    
    -------------
    
    Accumulated memory requirements during principal run stages (MiB.KiB):
      Density Construction: 192.2
      Hamiltonian application: 193.614
      Kernel calculation: 268.641
      Orbitals Orthonormalization: 193.614
      Poisson Solver: 274.794
    Atomic Forces (Ha/Bohr):
    - N:
      - 0.0
      - -3.388131789017e-21
      - -0.01184049963069
    - N:
      - 0.0
      - 3.388131789017e-21
      - 0.01184049963069
    Atomic System Properties:
      Boundary Conditions: Free
      Number of Symmetries: 0
      Number of atomic types: 1
      Number of atoms: 2
      Space group: disabled
      Types of atoms:
      - N
    Atomic structure:
      Rigid Shift Applied (AU):
      - 8.1
      - 8.1
      - 9.15
      position offset:
      - -8.1
      - -8.1
      - -9.15
      positions:
      - N:
        - 4.286335408
        - 4.286335408
        - 5.39077148
      - N:
        - 4.286335408
        - 4.286335408
        - 4.29317148
      units: angstroem
    Average noise forces:
      total: 2.6498158e-05
      x: -1.62783873e-05
      y: -1.62783874e-05
      z: 1.31217602e-05
    Basis set definition:
      Coarse and Fine Radii Multipliers:
      - 6.0
      - 6.0
      Suggested Grid Spacings (a0):
      - 0.3
      - 0.3
      - 0.3
    BigDFT infocode: 0
    Box Grid spacings:
    - 0.3
    - 0.3
    - 0.3
    Calculate Non Local forces: true
    Calculate local forces: true
    Clean forces norm (Ha/Bohr):
      fnrm2: 0.0002803948630088
      maxval: 0.01184049963069
    Code logo: '__________________________________ A fast and precise DFT wavelet code
      |     |     |     |     |     | |     |     |     |     |     |      BBBB         i       gggggg
      |_____|_____|_____|_____|_____|     B    B               g |     |  :  |  :  |     |     |    B     B        i     g
      |     |-0+--|-0+--|     |     |    B    B         i     g        g |_____|__:__|__:__|_____|_____|___
      BBBBB          i     g         g |  :  |     |     |  :  |     |    B    B         i     g         g
      |--+0-|     |     |-0+--|     |    B     B     iiii     g         g |__:__|_____|_____|__:__|_____|    B     B        i      g        g
      |     |  :  |  :  |     |     |    B BBBB        i        g      g |     |-0+--|-0+--|     |     |    B        iiiii          gggggg
      |_____|__:__|__:__|_____|_____|__BBBBB |     |     |     |  :  |     |                           TTTTTTTTT
      |     |     |     |--+0-|     |  DDDDDD          FFFFF        T |_____|_____|_____|__:__|_____|
      D      D        F        TTTT T |     |     |     |  :  |     |D        D      F        T     T
      |     |     |     |--+0-|     |D         D     FFFF     T     T |_____|_____|_____|__:__|_____|D___      D     F         T    T
      |     |     |  :  |     |     |D         D     F          TTTTT |     |     |--+0-|     |     |
      D        D     F         T    T |_____|_____|__:__|_____|_____|          D     F        T     T
      |     |     |     |     |     |         D               T    T |     |     |     |     |     |   DDDDDD       F         TTTT
      |_____|_____|_____|_____|_____|______                    www.bigdft.org   '
    Communication checks:
      Reverse transpositions: true
      Transpositions: true
    Compilation options:
      Compiler flags:
        CFLAGS: -g -O2
        CXXFLAGS: -g -O2
        FCFLAGS: -O2 -Wno-error -fbounds-check -fbacktrace -ffpe-trap=invalid,zero,overflow
          -fopenmp -m64 -g -Wl,--no-as-needed -ldl -fallow-argument-mismatch
      Compilers (CC, FC, CXX):
      - gcc
      - mpifort
      - g++
      Configure arguments: (...)
    DFT parameters:
      eXchange Correlation:
        Exchange-Correlation reference: 'XC: Teter 93'
        Reference Papers:
        - Comput. Phys. Commun. 183, 2272 (2012)
        - S. Goedecker, M. Teter, and J. Hutter, Phys. Rev. B 54, 1703 (1996)
        Spin polarization: false
        XC ID: -20
        XC functional implementation: libXC
    Data Writing directory: ./
    Electric Dipole Moment (AU):
      P vector:
      - -7.546821e-05
      - -7.546821e-05
      - -0.0001150379
      norm(P): 0.00015692235
    Electric Dipole Moment (Debye):
      P vector:
      - -0.000191821
      - -0.000191821
      - -0.0002923972
      norm(P): 0.000398856792
    Energy (Hartree): -19.889158366113875
    Estimated Memory Peak (MB): 274
    Force Norm (Hartree/Bohr): 0.016744995162996684
    GPU acceleration: false
    Geometry Optimization Parameters:
      Algorithm: none
      Fluctuation in forces: 1.0
      Maximum in forces: 0.0
      Maximum steps: 1
      Random atomic displacement: 0.0
      Steepest descent step: 4.0
    Ground State Optimization:
    - Hamiltonian Optimization:
      - Subspace Optimization:
          Non-Hermiticity of Hamiltonian in the Subspace: 1.1e-29
          Orbitals:
          - e: -1.041921681617
            f: 2.0
          - e: -0.4931878871014
            f: 2.0
          - e: -0.4364601439754
            f: 2.0
          - e: -0.4364600985988
            f: 2.0
          - e: -0.382575362697
            f: 2.0
          Wavefunctions Iterations:
          - D: 0.0108
            DIIS weights:
            - 1.0
            - 1.0
            EKS: -19.599442009873712
            Energies:
              EH: 26.4374284056
              EXC: -4.59353822458
              Ekin: 13.1903000846
              Enl: 1.87025796309
              Epot: -21.6971880749
              EvXC: -6.01510228509
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999991874
            gnrm: 0.327
            iter: 1
          - D: -0.267
            DIIS weights:
            - -0.0193
            - 1.02
            - -0.00444
            EKS: -19.86603074686917
            Energies:
              EH: 28.0070497949
              EXC: -4.83337440271
              Ekin: 14.5862099594
              Enl: 1.87459079009
              Epot: -21.8711736933
              EvXC: -6.33171403218
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999991103
            gnrm: 0.112
            iter: 2
          - D: -0.0197
            DIIS weights:
            - -0.0496
            - -0.311
            - 1.36
            - -0.000167
            EKS: -19.88574559888267
            Energies:
              EH: 27.8466684777
              EXC: -4.79736322355
              Ekin: 14.5652554957
              Enl: 1.75939315938
              Epot: -21.9036916524
              EvXC: -6.28427673737
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999991363
            gnrm: 0.0465
            iter: 3
          - D: -0.00319
            DIIS weights:
            - 0.0074
            - 0.00227
            - -0.163
            - 1.15
            - -1.17e-05
            EKS: -19.888938639401168
            Energies:
              EH: 27.8580241523
              EXC: -4.79644006663
              Ekin: 14.650953604
              Enl: 1.76326525276
              Epot: -21.984858617
              EvXC: -6.28311297722
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990899
            gnrm: 0.0147
            iter: 4
          - D: -0.000175
            DIIS weights:
            - 0.000392
            - 0.0201
            - -0.0779
            - -0.194
            - 1.25
            - -1.4e-06
            EKS: -19.889113592353517
            Energies:
              EH: 27.8467924008
              EXC: -4.79473286047
              Ekin: 14.6632488885
              Enl: 1.75246638581
              Epot: -21.9972192265
              EvXC: -6.28086325865
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990778
            gnrm: 0.00417
            iter: 5
          - D: -3.15e-05
            DIIS weights:
            - -0.000504
            - -0.00289
            - 0.0237
            - -0.0483
            - -0.349
            - 1.38
            - -2.32e-07
            EKS: -19.889145072041345
            Energies:
              EH: 27.8474270849
              EXC: -4.79498675479
              Ekin: 14.6734260845
              Enl: 1.75179027165
              Epot: -22.0061999013
              EvXC: -6.28119995034
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990731
            gnrm: 0.00208
            iter: 6
          - D: -8.62e-06
            DIIS weights:
            - -0.00117
            - 0.00272
            - 0.00774
            - 0.0534
            - -0.679
            - 1.62
            - -6.3e-08
            EKS: -19.88915368972063
            Energies:
              EH: 27.8475331181
              EXC: -4.79509022639
              Ekin: 14.6773557191
              Enl: 1.75059978639
              Epot: -22.0088750039
              EvXC: -6.28133679073
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990723
            gnrm: 0.0012
            iter: 7
          - D: -3.38e-06
            DIIS weights:
            - 0.000933
            - -0.00748
            - 0.00505
            - 0.12
            - -0.829
            - 1.71
            - -1.73e-08
            EKS: -19.88915706546748
            Energies:
              EH: 27.8474618626
              EXC: -4.79512344364
              Ekin: 14.6788591005
              Enl: 1.74992235176
              Epot: -22.0097864012
              EvXC: -6.28138082733
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990725
            gnrm: 0.000625
            iter: 8
          - D: -1.1e-06
            DIIS weights:
            - -0.00254
            - -0.00483
            - 0.121
            - -0.342
            - -0.0805
            - 1.31
            - -2.52e-09
            EKS: -19.88915816781627
            Energies:
              EH: 27.847315648
              EXC: -4.79512716638
              Ekin: 14.6794324855
              Enl: 1.74951890641
              Epot: -22.0101049665
              EvXC: -6.28138585872
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990726
            gnrm: 0.000264
            iter: 9
          - D: -1.83e-07
            DIIS weights:
            - -0.00216
            - 0.00429
            - 0.0526
            - -0.01
            - -0.481
            - 1.44
            - -4.05e-10
            EKS: -19.889158351154023
            Energies:
              EH: 27.8472885182
              EXC: -4.79513511046
              Ekin: 14.6796604001
              Enl: 1.74936581972
              Epot: -22.0102097031
              EvXC: -6.28139639829
            GPU acceleration: false
            Hamiltonian Applied: true
            Orthoconstraint: true
            Orthogonalization Method: 0
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Preconditioning: true
            Total electronic charge: 9.999999990726
            gnrm: 8.56e-05
            iter: 10
          - &id001
            D: -1.5e-08
            EKS: -19.889158366113875
            Energies:
              EH: 27.8472608482
              EXC: -4.79513251984
              Eion: 12.0530523624
              Ekin: 14.6796478684
              Enl: 1.7493457461
              Epot: -22.0102039625
              EvXC: -6.28139298747
            GPU acceleration: false
            Hamiltonian Applied: true
            Poisson Solver:
              BC: Free
              Box:
              - 139
              - 139
              - 153
              MPI tasks: 1
            Total electronic charge: 9.999999990726
            gnrm: 8.56e-05
            iter: 11
    High Res. box is treated separately: true
    Input Hamiltonian:
      Accuracy estimation for this run:
        Convergence Criterion: 2.98e-05
        Energy: 0.000149
      Atomic Input Orbital Generation:
      - Atom Type: N
        Electronic configuration:
          p:
          - 1.0
          - 1.0
          - 1.0
          s:
          - 2.0
      Deviation from normalization: 5.49e-07
      EKS: -19.610209365963435
      Energies:
        EH: 27.4148935003
        EXC: -4.70955110299
        Ekin: 13.9049636532
        Enl: 2.36627080396
        Epot: -21.978325416
        EvXC: -6.16827383377
      Expected kinetic energy: 13.904814679
      GPU acceleration: false
      IG wavefunctions defined: true
      Input Guess Overlap Matrices:
        Calculated: true
        Diagonalized: true
      Orbitals:
      - e: -1.055295241538
        f: 2.0
      - e: -0.526343538307
        f: 2.0
      - e: -0.4497660615404
        f: 2.0
      - e: -0.4497660067994
        f: 2.0
      - e: -0.3984990982962
        f: 2.0
      - e: -0.09753192536927
        f: 0.0
      - e: -0.09753187279788
        f: 0.0
      - e: 0.7245931378153
        f: 0.0
      Poisson Solver:
        BC: Free
        Box:
        - 139
        - 139
        - 153
        MPI tasks: 1
      Policy: Wavefunctions from PSP Atomic Orbitals
      Total No. of Atomic Input Orbitals: 8
      Total electronic charge: 9.99999999057
      Wavelet conversion succeeded: true
    Input Occupation Numbers:
    - Occupation Numbers:
        Orbitals No. 1-5: 2.0
    Interaction energy ions multipoles: 0.0
    Interaction energy multipoles multipoles: 0.0
    Ion-Ion interaction energy: 12.0530523624271
    Last Iteration: *id001
    Material acceleration: false
    Max No. of dictionaries used: 4938
    Maximal OpenMP threads per MPI task: 1
    Memory Consumption Report:
      Memory occupation:
        Memory Peak of process: 327.764 MB
        Peak Value (MB): 298.198
        for the array: zt
        in the routine: G_PoissonSolver
      Remaining Memory (B): 0
      Tot. No. of Allocations: 3546
      Tot. No. of Deallocations: 3546
    Memory requirements for principal quantities (MiB.KiB):
      All (distributed) orbitals: 8.416
      Full Uncompressed (ISF) grid: 22.567
      Nonlocal Pseudopotential Arrays: 0.113
      Single orbital: 0.861
      Subspace Matrix: 0.1
      Wavefunction storage size: 58.859
      Workspaces storage size: 1.1012
    Multipole analysis origin:
    - 8.1
    - 8.1
    - 9.15
    NonLocal PSP Projectors Descriptors:
      Creation strategy: On-the-fly
      Cumulative size of masking arrays: 3984
      Maximum size of masking arrays for a projector: 1992
      Percent of zero components: 14
      Size of workspaces: 57504
      Total number of components: 14372
      Total number of projectors: 2
    Number of MPI tasks: 1
    Number of dictionary folders allocated: 1
    OpenMP parallelization: true
    Orbitals Repartition:
      MPI tasks  0- 0: 5
    Poisson Kernel Creation:
      Boundary Conditions: Free
      Memory Requirements per MPI task:
        Density (MB): 23.93
        Full Grid Arrays (MB): 22.55
        Kernel (MB): 24.42
    Poisson Kernel Initialization:
      MPI tasks: 1
      OpenMP threads per MPI task: 1
      environment:
        cavity: none
        fd_order: 16
        itermax: 200
        minres: 1.0e-08
        pb_method: none
      kernel:
        isf_order: 16
        screening: 0
        stress_tensor: true
      setup:
        accel: none
        global_data: false
        output: none
        taskgroup_size: 0
        verbose: true
    Poisson Solver:
      BC: Free
      Box:
      - 139
      - 139
      - 153
      MPI tasks: 1
    Post Optimization Parameters:
      Finite-Size Effect estimation:
        Scheduled: false
    Properties of atoms in the system:
    - Grid Spacing threshold (AU): 0.64
      Local Pseudo Potential (HGH convention):
        Coefficients (c1 .. c4):
        - -12.23482
        - 1.76641
        - 0.0
        - 0.0
        Rloc: 0.28918
      No. of Atoms: 2
      No. of Electrons: 5
      No. of projectors: 1
      NonLocal PSP Parameters:
      - Channel (l): 0
        Rloc: 0.2566
        h_ij matrix:
        - - 13.55224
          - 0.0
          - 0.0
        - - 0.0
          - 0.0
          - 0.0
        - - 0.0
          - 0.0
          - 0.0
      - Channel (l): 1
        Rloc: 0.27013
        h_ij matrix:
        - - 0.0
          - 0.0
          - 0.0
        - - 0.0
          - 0.0
          - 0.0
        - - 0.0
          - 0.0
          - 0.0
      PSP XC: 'XC: Teter 93'
      Pseudopotential type: HGH-K
      Radii of active regions (AU):
        Coarse: 1.37026
        Coarse PSP: 0.67533
        Fine: 0.2566
        Source: Hard-Coded
      Symbol: N
    Quadrupole Moment (AU):
      Q matrix:
      - - 1.136
        - -6.0873e-07
        - -0.0002684
      - - -6.0873e-07
        - 1.136
        - -0.0002684
      - - -0.0002684
        - -0.0002684
        - -2.272
      trace: 0.0
    Raw forces norm (Ha/Bohr):
      fnrm2: 0.0002803969784791
      maxval: 0.01184985563241
    Reference Paper: The Journal of Chemical Physics 129, 014109 (2008)
    Root process Hostname: localhost
    Self-Consistent Cycle Parameters:
      Density/Potential:
        Max. Iterations: 1
      Wavefunction:
        CG Steps for Preconditioner: 6
        DIIS History length: 6
        Gradient Norm Threshold: 0.0001
        Input wavefunction policy: INPUT_PSI_LCAO
        Max. Subspace Diagonalizations: 1
        Max. Wfn Iterations: 50
        Number of plotted density orbitals: 0
        Output grid policy: NONE
        Output wavefunction policy: NONE
        Virtual orbitals: 0
    Sizes of the simulation domain:
      AU:
      - 16.2
      - 16.2
      - 18.3
      Angstroem:
      - 8.5727
      - 8.5727
      - 9.6839
      Grid Spacing Units:
      - 54
      - 54
      - 61
      High resolution region boundaries (GU):
        From:
        - 22
        - 22
        - 22
        To:
        - 32
        - 32
        - 39
    Spin treatment: Averaged
    Spreads of the electronic density (AU):
    - 0.8724061
    - 0.8724061
    - 1.396506
    Timestamp of this run: 2022-09-07 14:48:30.018000
    Timings for root process:
      CPU time (s): 19.73
      Elapsed time (s): 19.83
    Total Number of Electrons: 10
    Total Number of Orbitals: 5
    Total electronic charge: 9.999999990726
    Total ionic charge: -10.0
    Version Number: 1.9.2
    Walltime since initialization: 19.878042757
    Wavefunctions Descriptors, full simulation domain:
      Coarse resolution grid:
        No. of points: 102710
        No. of segments: 2746
      Fine resolution grid:
        No. of points: 1066
        No. of segments: 154
    Wavefunctions memory occupation for root MPI process: 4 MB 207 KB 608 B
    chess:
      foe:
        accuracy_entropy: 0.0001
        accuracy_foe: 1.0e-05
        accuracy_ice: 1.0e-08
        accuracy_penalty: 1.0e-05
        adjust_fscale: true
        betax_foe: -1000.0
        betax_ice: -1000.0
        ef_interpol_chargediff: 1.0
        ef_interpol_det: 1.0e-12
        eval_range_foe:
        - -0.5
        - 0.5
        evbounds_nsatur: 3
        evboundsshrink_nsatur: 4
        fscale: 0.05
        fscale_ediff_low: 5.0e-05
        fscale_ediff_up: 0.0001
        fscale_lowerbound: 0.005
        fscale_upperbound: 0.05
        matmul_optimize_load_balancing: false
        occupation_function: 102
      lapack:
        blocksize_pdgemm: -8
        blocksize_pdsyev: -8
        maxproc_pdgemm: 4
        maxproc_pdsyev: 4
      ntpoly:
        convergence_density: 1.0e-10
        convergence_overlap: 1.0e-10
        threshold_density: 0.0
        threshold_overlap: 0.0
    dft:
      alpha_hf: -1.0
      calculate_strten: true
      disablesym: false
      dispersion: 0
      elecfield:
      - 0.0
      - 0.0
      - 0.0
      external_potential: 0.0
      gnrm_cv: 0.0001
      gnrm_cv_virt: 0.0001
      hgrids: 0.3
      idsx: 6
      inputpsiid: 0
      itermax: 50
      itermax_occ_ctrl: 0
      itermax_virt: 50
      itermin: 0
      ixc: -20
      mpol: 0
      ncong: 6
      ncongt: 30
      ngrids:
      - 0
      - 0
      - 0
      norbv: 0
      nplot: 0
      nrepmax: 1
      nrepmax_occ_ctrl: 1
      nspin: 1
      nvirt: 0
      occupancy_control: None
      output_denspot: 0
      plot_mppot_axes:
      - -1
      - -1
      - -1
      plot_pot_axes:
      - -1
      - -1
      - -1
      projection: gaussian
      qcharge: 0
      rbuf: 0.0
      rmult: 6
    geopt:
      beta_stretchx: 5e-1
      betax: 4.0
      forcemax: 0.0
      frac_fluct: 1.0
      method: none
      ncount_cluster_x: 1
      randdis: 0.0
    kpt:
      bands: false
      kpt:
      - - 0.0
        - 0.0
        - 0.0
      method: manual
      wkpt:
      - 1.0
    lin_basis:
      alpha_diis: 1.0
      alpha_sd: 1.0
      correction_orthoconstraint: 1
      deltae_cv: 0.0001
      extended_ig: false
      fix_basis: 1.0e-10
      gnrm_cv:
      - 0.01
      - 0.0001
      gnrm_dyn: 0.0001
      gnrm_ig: 0.001
      idsx:
      - 6
      - 6
      min_gnrm_for_dynamic: 0.001
      nit:
      - 4
      - 5
      nit_ig: 50
      nstep_prec: 5
      orthogonalize_ao: true
      orthogonalize_sfs: true
      reset_DIIS_history: false
    lin_basis_params:
      ao_confinement: 0.0083
      confinement:
      - 0.0083
      - 0.0
      nbasis: 4
      rloc:
      - 7.0
      - 7.0
      rloc_kernel: 9.0
      rloc_kernel_foe: 14.0
    lin_general:
      calc_dipole: false
      calc_quadrupole: false
      calculate_FOE_eigenvalues:
      - 0
      - -1
      calculate_onsite_overlap: false
      cdft_add_w_guess: 0.0
      charge_multipoles: 0
      check_multipoles: true
      conf_damping: -0.5
      consider_entropy: false
      extra_states: 0
      frag_neighbour_cutoff: 12.0d0
      frag_num_neighbours: 0
      hybrid: false
      kernel_restart_mode: 0
      kernel_restart_noise: 0.0d0
      max_inversion_error: 1.d0
      multipole_centers: 0.0
      nit:
      - 100
      - 100
      output_coeff: 0
      output_fragments: 0
      output_mat: 0
      output_matmul: false
      output_multipole_matrices: true
      output_wf: 0
      plot_locreg_grids: false
      precision_FOE_eigenvalues: 0.005
      rpnrm_cv:
      - 1.0e-12
      - 1.0e-12
      subspace_diag: false
      support_function_multipoles: false
      taylor_order: 0
    lin_kernel:
      alpha_fit_coeff: false
      alpha_sd_coeff: 0.2
      alphamix:
      - 0.5
      - 0.5
      coeff_scaling_factor: 1.0
      delta_pnrm: -1.0
      diag_start: false
      gnrm_cv_coeff:
      - 1.0e-05
      - 1.0e-05
      idsx:
      - 0
      - 0
      idsx_coeff:
      - 0
      - 0
      linear_method: DIAG
      mixing_method: DEN
      nit:
      - 5
      - 5
      nstep:
      - 1
      - 1
      rpnrm_cv:
      - 1.0e-10
      - 1.0e-10
    logfile: true
    md:
      always_from_scratch: false
      mdsteps: 0
      no_translation: false
      print_frequency: 1
      restart_nose: false
      restart_pos: false
      restart_vel: false
      temperature: 300.d0
      thermostat: none
      timestep: 20.d0
      wavefunction_extrapolation: 0
    mix:
      alphadiis: 2.0
      alphamix: 0.0
      diis_sd_switch_tolerance: 0
      iscf: 0
      itrpmax: 1
      norbsempty: 0
      occopt: 1
      rpnrm_cv: 0.0001
      tel: 0.0
    mode:
      add_coulomb_force: false
      method: dft
    outdir: ./
    output:
      apply_coeffs: true
      atomic_density_matrix: None
      coupling_matrix: complete
      orbitals: None
      outputpsiid: wavefunction
      sdos: false
      verbosity: 2
    perf:
      FOE_restart: 0
      accel: false
      adjust_kernel_iterations: true
      adjust_kernel_threshold: true
      blas: false
      calculate_KS_residue: true
      calculate_forces: true
      calculate_gap: false
      check_matrix_compression: true
      check_overlap: 1
      check_sumrho: 1
      coeff_weight_analysis: false
      correction_co_contra: true
      debug: false
      domain: null
      enable_matrix_taskgroups: true
      exctxpar: OP2P
      experimental_mode: false
      explicit_locregcenters: false
      fftcache: 8192
      foe_gap: false
      hamapp_radius_incr: 8
      ig_blocks:
      - 300
      - 800
      ig_diag: true
      ig_norbp: 5
      ig_tol: 0.0001
      imethod_overlap: 1
      inguess_geopt: 0
      intermediate_forces: false
      iterative_orthogonalization: false
      kappa_conv: 0.1
      linear: false
      loewdin_charge_analysis: false
      methortho: 0
      mixing_after_inputguess: 1
      mp_isf: 16
      multipole_preserving: false
      ocl_devices: null
      ocl_platform: null
      projrad: 15.0
      psp_onfly: true
      rho_commun: DEF
      signaling: false
      signaltimeout: 0
      store_index: true
      store_overlap_matrices: true
      tolsym: 1.0e-08
      unblock_comms: false
      wf_extent_analysis: false
    posinp:
      cell:
      - .inf
      - .inf
      - .inf
      positions:
      - N:
        - 0.0
        - 0.0
        - 0.5488
        frag:
        - N
        - 0
      - N:
        - 0.0
        - 0.0
        - -0.5488
        frag:
        - N
        - 1
      properties:
        format: yaml
        source: xc__LDA.yaml
      units: angstroem
    psolver:
      environment:
        cavity: none
        fd_order: 16
        itermax: 200
        minres: 1.0e-08
        pb_method: none
      kernel:
        isf_order: 16
        screening: 0
        stress_tensor: true
      setup:
        accel: none
        global_data: false
        output: none
        taskgroup_size: 0
        verbose: true
    psppar.N:
      Atomic number: 7
      Local Pseudo Potential (HGH convention):
        Coefficients (c1 .. c4):
        - -12.23481988
        - 1.76640728
        - 0.0
        - 0.0
        Rloc: 0.28917923
      No. of Electrons: 5
      NonLocal PSP Parameters:
      - Channel (l): 0
        Rloc: 0.25660487
        h_ij terms:
        - 13.55224272
        - 0.0
        - 0.0
        - 0.0
        - 0.0
        - 0.0
      - Channel (l): 1
        Rloc: 0.27013369
        h_ij terms:
        - 0.0
        - 0.0
        - 0.0
        - 0.0
        - 0.0
        - 0.0
      Pseudopotential XC: 1
      Pseudopotential type: HGH-K
      Radii of active regions (AU):
        Coarse: 1.370256482166319
        Coarse PSP: 0.675334225
        Fine: 0.25660487
        Source: Hard-Coded
      Source: Hard-Coded
    radical: xc__LDA
    run_from_files: true
    sic:
      sic_alpha: 0.0
      sic_approach: none
    skip: false
    tddft:
      decompose_perturbation: none
      tddft_approach: none
    
    
    
    
    [112]:
    
    
    
    for log,xc in zip(logfiles,xc_list):
        print(xc,log.log['Estimated Memory Peak (MB)'])
    
    
    
    LDA 274
    PBE 274
    HF 274
    PBE0 274
    

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).