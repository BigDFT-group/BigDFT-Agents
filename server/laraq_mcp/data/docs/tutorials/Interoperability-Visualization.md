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
      * [Running The Code](../users/guide.html#running-the-code)
      * [Examining and postprocessing the output](../users/guide.html#examining-and-postprocessing-the-output)
      * [Interoperability With Other Codes](../users/guide.html#interoperability-with-other-codes)
        * Interoperability With Visualization Software
        * [Interoperability with Other Simulation Software](Interoperability-Simulation.html)
    * [Lessons and Workflows](../users/guide.html#lessons-and-workflows)

  * [PyBigDFT API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/index.html)

Developer

  * [BigDFT-suite manifesto](../devel/developers.html)

  * [Futile API](https://l_sim.gitlab.io/bigdft-suite/futile/build/html/index.html)

__[BigDFT-suite](../index.html)

  * [](../index.html)
  * [User Guide](../users/guide.html)
  * Interoperability With Visualization Software
  * [ View page source](../_sources/tutorials/Interoperability-Visualization.ipynb.txt)

* * *

# Interoperability With Visualization Software

PyBigDFT can be used in combination with various kinds of visualization software. Here we present some basic examples of this functionality.

## py3Dmol

[py3Dmol](https://pypi.org/project/py3Dmol/) is a convenient way to visualize molecules inside a notebook. First, let’s define the system to look at.
    
    
    [1]:
    
    
    
    from io import StringIO
    input_file = StringIO("""ATOM      1  N   GLU A   1      -1.154   2.418   1.060  1.00  0.00           N
    ATOM      2  CA  GLU A   1      -0.291   1.391   1.511  1.00  0.00           C
    ATOM      3  C   GLU A   1       0.988   1.375   0.674  1.00  0.00           C
    ATOM      4  O   GLU A   1       2.084   1.489   1.199  1.00  0.00           O
    ATOM      5  H1  GLU A   1      -0.808   3.356   0.900  1.00  0.00           H
    ATOM      6  HB1 ALA A   2       2.228   0.884  -3.807  1.00  0.00           H
    ATOM      7  H2  GLU A   1      -2.131   2.117   0.916  1.00  0.00           H
    ATOM      8  HA  GLU A   1      -0.012   1.610   2.555  1.00  0.00           H
    ATOM      9  CB  GLU A   1      -1.012   0.017   1.443  1.00  0.00           C
    ATOM     10  CG  GLU A   1      -1.458  -0.331  -0.002  1.00  0.00           C
    ATOM     11  HB1 GLU A   1      -1.897   0.046   2.100  1.00  0.00           H
    ATOM     12  HB2 GLU A   1      -0.338  -0.772   1.815  1.00  0.00           H
    ATOM     13  HG1 GLU A   1      -0.583  -0.365  -0.671  1.00  0.00           H
    ATOM     14  HG2 GLU A   1      -2.152   0.435  -0.382  1.00  0.00           H
    ATOM     15  CD  GLU A   1      -2.156  -1.666  -0.029  1.00  0.00           C
    ATOM     16  OE1 GLU A   1      -1.704  -2.633  -0.619  1.00  0.00           O
    ATOM     17  OE2 GLU A   1      -3.307  -1.738   0.635  1.00  0.00           O
    ATOM     18  HE2 GLU A   1      -3.662  -2.616   0.558  1.00  0.00           H
    ATOM     19  N   ALA A   2       0.783   1.228  -0.622  1.00  0.00           N
    ATOM     20  CA  ALA A   2       1.867   1.202  -1.533  1.00  0.00           C
    ATOM     21  C   ALA A   2       2.816   2.367  -1.249  1.00  0.00           C
    ATOM     22  O   ALA A   2       3.998   2.171  -1.016  1.00  0.00           O
    ATOM     23  HB2 ALA A   2       0.925   1.765  -3.471  1.00  0.00           H
    ATOM     24  H   ALA A   2       2.340   3.354  -1.287  1.00  0.00           H
    ATOM     25  H   ALA A   2      -0.144   1.131  -1.066  1.00  0.00           H
    ATOM     26  HA  ALA A   2       2.442   0.301  -1.259  1.00  0.00           H
    ATOM     27  CB  ALA A   2       1.459   0.968  -3.161  1.00  0.00           C
    ATOM     28  HB3 ALA A   2       0.877   0.168  -3.356  1.00  0.00           H""")
    
    
    
    [2]:
    
    
    
    from BigDFT.IO import read_pdb
    sys = read_pdb(input_file)
    

To use py3D mol first define an a visualization object, and then call display_system.
    
    
    [3]:
    
    
    
    from BigDFT.Visualization import InlineVisualizer
    viz = InlineVisualizer(300,200)
    viz.display_system(sys)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

We can update the system with some new fragments.
    
    
    [4]:
    
    
    
    from BigDFT.Systems import System
    from BigDFT.Fragments import Fragment
    from BigDFT.Atoms import Atom
    ion = System()
    ion["ION:0"] = Fragment([Atom({"sym":"H", "r": [0, 0, 0], "units": "bohr"})])
    

It will be easier to see if we explicitly decide the colors.
    
    
    [5]:
    
    
    
    colordict = {"GLU:1": "blue", "ALA:2": "red", "ION:0": "yellow"}
    
    
    
    [6]:
    
    
    
    viz = InlineVisualizer(300,200)
    viz.display_system(sys, colordict=colordict, show=False)
    viz.display_system(ion, colordict=colordict)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

If you want to display a movie, just pass a list of systems instead.
    
    
    [7]:
    
    
    
    from copy import deepcopy
    syslist = [sys]
    for i in range(10):
        syslist.append(deepcopy(syslist[-1]))
        syslist[-1]["GLU:1"].translate([-1, 0, 0])
    
    
    
    [8]:
    
    
    
    viz = InlineVisualizer(300,200)
    viz.display_system(*syslist, colordict=colordict)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

## VMD

We offer a simple routine for produce a VMD script allowing you to color fragments by name.
    
    
    [9]:
    
    
    
    from BigDFT.Visualization import VMDGenerator
    viz = VMDGenerator()
    colordict = {"GLU:1": "1", "ALA:2": "2"}
    viz.visualize_fragments(sys, "script.pml", "script.xyz", fragcolors=colordict)
    
    
    
    [10]:
    
    
    
    with open("script.pml") as ifile:
        for line in ifile:
            print(line,end="")
    
    
    
    mol default style CPK
    mol new script.xyz
    mol modcolor 0 0 ColorID 16
    mol addrep 0
    mol modselect 1 0 index 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
    mol modcolor 1 0 ColorID 1
    mol addrep 0
    mol modselect 2 0 index 17 18 19 20 21 22 23 24 25 26 27
    mol modcolor 2 0 ColorID 2
    
    
    
    [ ]:
    
    
    
    

[ Previous](Tight-Binding.html "Tight-binding model of graphene") [Next ](Interoperability-Simulation.html "Interoperability with Other Simulation Software")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).