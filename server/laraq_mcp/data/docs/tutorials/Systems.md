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
      * [Building Systems Programmatically](../users/guide.html#building-systems-programmatically)
        * Building A System
        * [Input and Output in PyBigDFT](IO.html)
        * [Building Systems with Roto-Translations](Rototranslations.html)
      * [Running The Code](../users/guide.html#running-the-code)
      * [Examining and postprocessing the output](../users/guide.html#examining-and-postprocessing-the-output)
      * [Interoperability With Other Codes](../users/guide.html#interoperability-with-other-codes)
    * [Lessons and Workflows](../users/guide.html#lessons-and-workflows)

  * [PyBigDFT API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/index.html)

Developer

  * [BigDFT-suite manifesto](../devel/developers.html)

  * [Futile API](https://l_sim.gitlab.io/bigdft-suite/futile/build/html/index.html)

__[BigDFT-suite](../index.html)

  * [](../index.html)
  * [User Guide](../users/guide.html)
  * Building A System
  * [ View page source](../_sources/tutorials/Systems.ipynb.txt)

* * *

# Building A System

In PyBigDFT, systems are built in three layers. On the lowest layer are Atoms. Atoms inherit from dictionaries, and can be manipulated as such so that you can store any needed information. Collections of Atoms are stored as Fragments. Fragments inherit from lists, allowing you to combine and slice them. Finally, at the top layer we have a system, which is a named collection of Fragments. Like Atoms, Systems inherit from dictionaries, so that you can manipulate them as key value pairs.

## Atoms

First we begin with atoms. To describe an atom, you should define an atomic symbol, and a position.
    
    
    [1]:
    
    
    
    from BigDFT.Atoms import Atom
    at = Atom({'r': [1.0, 0.0, 0.0], 'sym': "He", 'units': 'bohr'})
    print(dict(at))
    
    
    
    {'r': [1.0, 0.0, 0.0], 'sym': 'He', 'units': 'bohr'}
    

As mentioned above, a BigDFT atom can store any supplementary information you need.
    
    
    [2]:
    
    
    
    at["source"] = "tutorial"
    print(dict(at))
    
    
    
    {'r': [1.0, 0.0, 0.0], 'sym': 'He', 'units': 'bohr', 'source': 'tutorial'}
    

There are helper routines to let you access these dictionary elements.
    
    
    [3]:
    
    
    
    print(at.get_position())
    print(at.get_position(units="angstroem"))
    
    
    
    [1.0, 0.0, 0.0]
    [0.52917721092, 0.0, 0.0]
    
    
    
    [4]:
    
    
    
    at.set_position([1.0, 1.0, 1.0], units="angstroem")
    print(at.get_position(units="angstroem"))
    
    
    
    [1.0, 1.0, 1.0]
    
    
    
    [5]:
    
    
    
    print(at.sym)
    print(at.atomic_number)
    
    
    
    He
    2
    

By default, the atoms in PyBigDFT don’t know how many electrons they have. This is because the pseudopotential approximation means the number of electrons used could depend on our choice of pseudopotential. However, we can set this ourself if we’d like.
    
    
    [6]:
    
    
    
    at.nel = 2
    print(at.nel)
    
    
    
    2
    

## Fragments

Now we look at fragments, which are collections of atoms. Fragments might be built by simply appending atoms to an empty Fragment.
    
    
    [7]:
    
    
    
    at1 = Atom({'r': [1.0, 0.0, 0.0], 'sym': "He", 'units': 'bohr', "nzion": 2})
    at2 = Atom({'r': [3.0, 0.0, 0.0], 'sym': "He", 'units': 'bohr', "nzion": 2})
    
    
    
    [8]:
    
    
    
    from BigDFT.Fragments import Fragment
    frag = Fragment()
    frag.append(at1)
    frag.append(at2)
    
    for at in frag:
        print(dict(at))
    
    
    
    {'r': [1.0, 0.0, 0.0], 'sym': 'He', 'units': 'bohr', 'nzion': 2}
    {'r': [3.0, 0.0, 0.0], 'sym': 'He', 'units': 'bohr', 'nzion': 2}
    

There are also some helper routines associated with fragments.
    
    
    [9]:
    
    
    
    print(frag.centroid)
    print(frag.nel)
    
    
    
    [2. 0. 0.]
    4
    
    
    
    [10]:
    
    
    
    from copy import deepcopy
    frag2 = deepcopy(frag)
    frag2.translate(vec=[0.0, 5.0, 0.0])
    
    
    
    [11]:
    
    
    
    from BigDFT.Fragments import distance
    print(distance(frag, frag2))
    
    
    
    5.0
    

## Systems

Systems are named collections of fragments. In general, we use a naming convention for systems that goes “NAME:ID” where name is a string and ID is a number. This can help with maintaining ordering, or distinguishing between the types of fragments.
    
    
    [12]:
    
    
    
    from BigDFT.Systems import System
    sys = System()
    sys["FRA:1"] = frag
    sys["FRA:2"] = frag2
    

Now that we’ve reached the top level, we can begin interacting with other parts of the code. For example, the Visualization module.
    
    
    [13]:
    
    
    
    # NBVAL_IGNORE_OUTPUT
    from BigDFT.Visualization import InlineVisualizer
    viz = InlineVisualizer(500,400)
    
    viz.display_system(sys)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

Notice how the code was able to color the different fragments using this representation. The System module offers helper routines for dealing with the stored fragments.
    
    
    [14]:
    
    
    
    print(sys.get_nearest_fragment("FRA:1"))
    print(sys.centroid)
    
    
    
    FRA:2
    [2.  2.5 0. ]
    

To access the atoms in a system, try the following double loop pattern:
    
    
    [15]:
    
    
    
    for fragid, frag in sys.items():
        print(fragid)
        for at in frag:
            print(dict(at))
    
    
    
    FRA:1
    {'r': [1.0, 0.0, 0.0], 'sym': 'He', 'units': 'bohr', 'nzion': 2}
    {'r': [3.0, 0.0, 0.0], 'sym': 'He', 'units': 'bohr', 'nzion': 2}
    FRA:2
    {'r': [1.0, 5.0, 0.0], 'sym': 'He', 'units': 'bohr', 'nzion': 2}
    {'r': [3.0, 5.0, 0.0], 'sym': 'He', 'units': 'bohr', 'nzion': 2}
    

## Solid State Systems

A system has a unit cell associated with it that you can use to define solid state systems. The UnitCell class is available to manage the cell.
    
    
    [16]:
    
    
    
    from BigDFT.UnitCells import UnitCell
    sys.cell = UnitCell([5, 5, 5], units="bohr")
    
    
    
    [17]:
    
    
    
    print(sys.cell.get_posinp())
    
    
    
    [5.0, 5.0, 5.0]
    

BigDFT is able to handle several boundary conditions. If the cell is None, it will be a free boundary. If all three values are set, you get a periodic system. For a wire boundary condition, set the y and x values to infinity.
    
    
    [18]:
    
    
    
    sys.cell = UnitCell([float("inf"), float("inf"), 5], units="angstroem")
    print(sys.cell.get_posinp("bohr"))
    
    
    
    [inf, inf, 9.44863062282531]
    

For the surface condition, set just the Y value to infinity.
    
    
    [19]:
    
    
    
    sys.cell = UnitCell([5, float("inf"), 5], units="bohr")
    print(sys.cell.get_posinp("bohr"))
    
    
    
    [5.0, inf, 5.0]
    

In the context of solid state systems, we can utilize reduced (fractional) positions as another way of specifying the location of atoms.
    
    
    [20]:
    
    
    
    cell = UnitCell([10, 10, 10], units="bohr")
    
    
    
    [21]:
    
    
    
    at = Atom({'r': [0.5, 0.25, 0.0], 'sym': "He", 'units': 'reduced'})
    print(at.get_position("reduced", cell))
    print(at.get_position("bohr", cell))
    print(at.get_position("angstroem", cell))
    
    
    
    [0.5, 0.25, 0.0]
    [5.0, 2.5, 0.0]
    [2.6458860546, 1.3229430273, 0.0]
    
    
    
    [22]:
    
    
    
    at = Atom({'r': [5.0, 2.5, 0.0], 'sym': "He", 'units': 'bohr'})
    print(at.get_position("reduced", cell))
    print(at.get_position("bohr", cell))
    print(at.get_position("angstroem", cell))
    
    
    
    [0.5, 0.25, 0.0]
    [5.0, 2.5, 0.0]
    [2.6458860546, 1.3229430273, 0.0]
    

Passing the cell to `get_position` also helps enforce the minimum image convention.
    
    
    [23]:
    
    
    
    at = Atom({'r': [15.0, 12.5, 0.0], 'sym': "He", 'units': 'bohr'})
    print(at.get_position("reduced", cell))
    print(at.get_position("bohr", cell))
    print(at.get_position("angstroem", cell))
    
    
    
    [0.5, 0.25, 0.0]
    [5.0, 2.5, 0.0]
    [2.6458860546, 1.3229430273, 0.0]
    

## Conclusion

In this tutorial, we presented the three layers of system representation in PyBigDFT: Atoms, Fragments, and Systems. By looking at the rest of the documentation, you can discover advanced features of these representations and how to connect them to the rest of the code.

[ Previous](../users/guide.html "User Guide") [Next ](IO.html "Input and Output in PyBigDFT")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).