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
        * [Building A System](Systems.html)
        * Input and Output in PyBigDFT
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
  * Input and Output in PyBigDFT
  * [ View page source](../_sources/tutorials/IO.ipynb.txt)

* * *

# Input and Output in PyBigDFT

There are a number of standard file types that PyBigDFT can work with using its IO module. Here we will demonstrate some of that capability.

## XYZ Files

The XYZReader class has access to some built in molecules, so let’s begin there. You can access any of the molecules in the database just by opening an XYZReader with that name. Or you can specify a filename path to get something you’ve already made yourself.
    
    
    [1]:
    
    
    
    from BigDFT.IO import XYZReader
    from BigDFT.Systems import System
    from BigDFT.Fragments import Fragment
    
    sys = System()
    sys["SI4:0"] = Fragment()
    with XYZReader("CH4") as ifile:
        for atom in ifile:
            sys["SI4:0"].append(atom)
    
    sys["CH2F:1"] = Fragment()
    with XYZReader("CH2F") as ifile:
        for atom in ifile:
            sys["CH2F:1"].append(atom)
    
    sys["CH2F:1"].translate([-5, 0, 0])
    

Let’s look at what we built.
    
    
    [2]:
    
    
    
    from BigDFT.Visualization import InlineVisualizer
    viz = InlineVisualizer(500,400)
    viz.display_system(sys)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

The XYZWriter works in a similar way.
    
    
    [3]:
    
    
    
    from BigDFT.IO import XYZWriter
    natoms = sum([len(x) for x in sys.values()])
    with XYZWriter("test.xyz", units="angstroem", natoms=natoms) as ofile:
        for frag in sys.values():
            for at in frag:
                ofile.write(at)
    

Sometimes you just want to read and write systems quickly. In this case, there is the `read_xyz` and `write_xyz` functions.
    
    
    [4]:
    
    
    
    from BigDFT.IO import write_xyz
    with open("test2.xyz", "w") as ofile:
        write_xyz(sys, ofile)
    
    
    
    [5]:
    
    
    
    from BigDFT.IO import read_xyz
    with open("test2.xyz") as ifile:
        sys2 = read_xyz(ifile, fragmentation="atomic")
    

When reading in an xyz file, there is no fragment information available. By default, it creates a system where each atom will be its own fragment. You can also choose `single` to read into one big fragment.
    
    
    [6]:
    
    
    
    viz = InlineVisualizer(500,400)
    viz.display_system(sys2)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

Merging the system into one fragment yourself is also a straightforward operation.
    
    
    [7]:
    
    
    
    sys3 = System()
    sys3["FRA:0"] = sum(sys2.values())
    
    
    
    [8]:
    
    
    
    viz = InlineVisualizer(500,400)
    viz.display_system(sys3)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

## Other Formats

The other formats work much like the `read_xyz` and `write_xyz` approach. For example, let’s say we want to write a PDB file.
    
    
    [9]:
    
    
    
    from BigDFT.IO import write_pdb
    with open("test.pdb", "w") as ofile:
        write_pdb(sys, ofile)
    

Let’s test if that worked by loading the written file into a string.
    
    
    [10]:
    
    
    
    with open("test.pdb") as ifile:
        for line in ifile:
            print(line, end="")
    
    
    
    HETATM    1 C    SI4 A   0       0.000   0.000   0.000  1.00  0.00       B   C
    HETATM    2 H    SI4 A   0       0.628   0.628   0.628  1.00  0.00       B   H
    HETATM    3 H    SI4 A   0       0.628  -0.628  -0.628  1.00  0.00       B   H
    HETATM    4 H    SI4 A   0      -0.628   0.628  -0.628  1.00  0.00       B   H
    HETATM    5 H    SI4 A   0      -0.628  -0.628   0.628  1.00  0.00       B   H
    HETATM    6 C    CH2 A   1      -2.675   0.655   0.000  1.00  0.00       B   C
    HETATM    7 F    CH2 A   1      -2.675  -0.682   0.000  1.00  0.00       B   F
    HETATM    8 H    CH2 A   1      -2.431   1.104   0.947  1.00  0.00       B   H
    HETATM    9 H    CH2 A   1      -2.431   1.104  -0.947  1.00  0.00       B   H
    

And of course we can read in a system like this.
    
    
    [11]:
    
    
    
    from BigDFT.IO import read_pdb
    with open("test.pdb") as ifile:
        sys2 = read_pdb(ifile)
    
    
    
    [12]:
    
    
    
    for fragid, frag in sys2.items():
        print(fragid)
        for at in frag:
            print(dict(at))
    
    
    
    SI4:0
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
    

We see that in this case, the read function was able to break the system into fragments. This is because PDB files have fragment information in them, making them a very convenient format for using PyBigDFT.

[ Previous](Systems.html "Building A System") [Next ](Rototranslations.html "Building Systems with Roto-Translations")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).