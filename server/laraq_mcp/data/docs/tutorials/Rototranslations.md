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
        * [Input and Output in PyBigDFT](IO.html)
        * Building Systems with Roto-Translations
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
  * Building Systems with Roto-Translations
  * [ View page source](../_sources/tutorials/Rototranslations.ipynb.txt)

* * *

# Building Systems with Roto-Translations

For building systems programatically, PyBigDFT offers some helper routines based on the concept of rototranslations. Using these features, we can easily align molecules in space.

## Rotations and Translations

Let’s begin by showing the basics of rotating and translating molecules.
    
    
    [1]:
    
    
    
    from BigDFT.IO import XYZReader
    from BigDFT.Systems import System
    from BigDFT.Fragments import Fragment
    
    sys = System()
    sys["WAT:0"] = Fragment()
    with XYZReader("H2O") as ifile:
        for at in ifile:
            sys["WAT:0"] += Fragment([at])
    

Translation. Note that the units are atomic units.
    
    
    [2]:
    
    
    
    from copy import deepcopy
    sys["WAT:1"] = deepcopy(sys["WAT:0"])
    sys["WAT:1"].translate([-10, 0, 0])
    
    
    
    [3]:
    
    
    
    from BigDFT.Visualization import InlineVisualizer
    viz = InlineVisualizer(400,300)
    viz.display_system(sys)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

Rotation. We can pick our units of degrees or angstroems.
    
    
    [4]:
    
    
    
    sys["WAT:1"].rotate(x=90, units="degrees")
    viz = InlineVisualizer(400,300)
    viz.display_system(sys)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

## Fragment Interpolation

We can interpolate between two fragments if we wish to examine some intermediary states.
    
    
    [5]:
    
    
    
    from BigDFT.Fragments import interpolate_fragments
    steps = interpolate_fragments(sys["WAT:0"], sys["WAT:1"], steps=3)
    
    sys2 = System()
    for i, s in enumerate(steps):
        sys2["WAT:"+str(i)] = s
    
    
    
    [6]:
    
    
    
    viz = InlineVisualizer(400,300)
    viz.display_system(sys2)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

## Lining Up Fragments

Sometimes we have two fragments which are made of the same atoms, but one geometry is perturbed from another. We might wish to try lining up those fragments so we can figure out how big that pertubation is.
    
    
    [7]:
    
    
    
    from BigDFT.Fragments import RotoTranslation
    rtsys = System()
    rtsys["WAT:0"] = deepcopy(sys["WAT:0"])
    rtsys["WAT:1"] = deepcopy(sys["WAT:0"])
    rtsys["WAT:1"].translate([-5.0, 0, 0])
    pos = rtsys["WAT:0"][0].get_position()
    pos[1] -= 0.75
    rtsys["WAT:0"][0].set_position(pos)
    
    
    
    [8]:
    
    
    
    viz = InlineVisualizer(400,300)
    viz.display_system(rtsys)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

Using the lineup freature, we can find the best matching between these two systems.
    
    
    [9]:
    
    
    
    from BigDFT.Fragments import lineup_fragment
    rtsys["WAT:0"] = lineup_fragment(rtsys["WAT:0"])
    rtsys["WAT:1"] = lineup_fragment(rtsys["WAT:1"])
    
    
    
    [10]:
    
    
    
    viz = InlineVisualizer(400,300)
    viz.display_system(rtsys)
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`

Now compute the RMSD.
    
    
    [11]:
    
    
    
    from numpy import array
    from numpy.linalg import norm
    
    rmsd = 0
    for at1, at2 in zip(rtsys["WAT:0"], rtsys["WAT:1"]):
        rmsd += norm(array(at1.get_position("angstroem")) - array(at2.get_position("angstroem")))
    
    print(rmsd)
    
    
    
    3.681664737333418
    

[ Previous](IO.html "Input and Output in PyBigDFT") [Next ](N2.html "Basics of BigDFT: N2 molecule as example")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).