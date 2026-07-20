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
  * System Generation
  * [ View page source](../_sources/school/System-Generation.ipynb.txt)

* * *

# System Generation

In this lesson, we will describe the data structures available in PyBigDFT for manipulating the systems we want to study (whether molecular or solid state). This will also be a moment for us to introduce one of the main philosophy’s of this framework. In python, we have two very common datastructures: lists and dictionaries.
    
    
    [1]:
    
    
    
    my_list = [0, 1, 2, 3]
    print(my_list[-1])
    my_dict = {"a": "word", "c": 4}
    print(my_dict["c"])
    
    
    
    3
    4
    

These two datastructures have some nice features. First, they are serializable in human readable formats like [json](https://en.wikipedia.org/wiki/JSON) or [yaml](https://en.wikipedia.org/wiki/JSON).
    
    
    [2]:
    
    
    
    from yaml import dump
    print(dump(my_list))
    print(dump(my_dict))
    
    
    
    - 0
    - 1
    - 2
    - 3
    
    a: word
    c: 4
    
    

The second is that they can be quickly built and manipulated using comprehensions ([list](https://peps.python.org/pep-0202/) and [dict](https://peps.python.org/pep-0274/)).
    
    
    [3]:
    
    
    
    my_list2 = [x * 3 for x in my_list]
    print(my_list2)
    my_dict2 = {k + "2": v for k, v in my_dict.items()}
    print(my_dict2)
    
    
    
    [0, 3, 6, 9]
    {'a2': 'word', 'c2': 4}
    

## Atom Class

Any system we want to study is going to be made up of Atoms. What is the best way to store information about an atom? From our previous discussion, a `dict` seems most appropriate.
    
    
    [4]:
    
    
    
    datm = {"sym": "H", "r": [1, 0, 0], "units": "angstroem"}
    # the following also works
    # datm = {"H": [1, 0, 0], "units": "angstroem"}
    print(dump(datm))
    
    
    
    r:
    - 1
    - 0
    - 0
    sym: H
    units: angstroem
    
    

Nonetheless, just manipulating a `dict` by itself is error prone, and you might want some helpful subroutines. For this reasons, we’ve wrapped up a `dict` in our Atom class.
    
    
    [5]:
    
    
    
    from BigDFT.Atoms import Atom
    atom = Atom(datm)
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
    

With this approach, we nonetheless retain the flexibility of a `dict`.
    
    
    [7]:
    
    
    
    atom["source"] = "tutorial"
    print(atom["source"])
    for k, v in atom.items():
        print(k, v)
    
    
    
    tutorial
    sym H
    r [1, 0, 0]
    units angstroem
    source tutorial
    

## Fragments

We won’t do many calculations involving a single atom, instead we want to put together groups of atoms. In this case, we will use a list as our model data structure, with the wrapper class refered to as a `Fragment`.
    
    
    [8]:
    
    
    
    atm1 = Atom({"sym": "O", "r": [2.3229430273, 1.3229430273, 1.7139430273], "units": "angstroem"})
    atm2 = Atom({"sym": "H", "r": [2.3229430273, 2.0801430273, 1.1274430273], "units": "angstroem"})
    atm3 = Atom({"sym": "H", "r": [2.3229430273, 0.5657430273000001, 1.1274430273], "units": "angstroem"})
    
    
    
    [9]:
    
    
    
    from BigDFT.Fragments import Fragment
    frag1 = Fragment([atm1, atm2, atm3])
    print(len(frag1))
    print(frag1.centroid)
    
    
    
    3
    [4.38972612 2.5        2.5       ]
    

It’s also possible to build up a fragment in a more step by step process.
    
    
    [10]:
    
    
    
    frag1 = Fragment()
    frag1.append(atm1)
    frag1 += Fragment([atm2])
    frag1.extend(Fragment([atm3]))
    

We added the feature to translate and rotate a fragment.
    
    
    [11]:
    
    
    
    from copy import deepcopy
    frag2 = deepcopy(frag1)
    frag2.translate([10, 0, 0])
    frag2.rotate(x=90, units="degrees")
    
    
    
    [12]:
    
    
    
    print(dump(frag2))
    
    
    
    !!python/object:BigDFT.Fragments.Fragment
    atoms:
    - !!python/object:BigDFT.Atoms.Atom
      store:
        r:
        - 14.389726124565062
        - 1.7611170852950608
        - 2.499999999999999
        sym: O
        units: bohr
    - !!python/object:BigDFT.Atoms.Atom
      store:
        r:
        - 14.389726124565062
        - 2.86944145735247
        - 3.930900621520664
        sym: H
        units: bohr
    - !!python/object:BigDFT.Atoms.Atom
      store:
        r:
        - 14.389726124565062
        - 2.86944145735247
        - 1.0690993784793343
        sym: H
        units: bohr
    conmat: null
    frozen: null
    q1: null
    q2: null
    
    

## Systems

Many Quantum Mechanical codes top off at the list of atoms level, but in PyBigDFT we go one step further. At the top, we have the `System` class which is based on a `dict`.
    
    
    [13]:
    
    
    
    from BigDFT.Systems import System
    sys = System()
    sys["WAT:0"] = frag1
    sys["WAT:1"] = frag2
    
    
    
    [14]:
    
    
    
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
      WAT:1: !!python/object:BigDFT.Fragments.Fragment
        atoms:
        - !!python/object:BigDFT.Atoms.Atom
          store:
            r:
            - 14.389726124565062
            - 1.7611170852950608
            - 2.499999999999999
            sym: O
            units: bohr
        - !!python/object:BigDFT.Atoms.Atom
          store:
            r:
            - 14.389726124565062
            - 2.86944145735247
            - 3.930900621520664
            sym: H
            units: bohr
        - !!python/object:BigDFT.Atoms.Atom
          store:
            r:
            - 14.389726124565062
            - 2.86944145735247
            - 1.0690993784793343
            sym: H
            units: bohr
        conmat: null
        frozen: null
        q1: null
        q2: null
    
    

In principle, any dictionary key is fine to use for our `System` class, but in practice we follow the convention of giving it a name and identifier separated by a colon. To summarize the hierarchy, let’s iterate over our `System`.
    
    
    [15]:
    
    
    
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
    

Now that we’ve reached the top level, let’s visualize the system we have built.
    
    
    [16]:
    
    
    
    # NBVAL_IGNORE_OUTPUT
    sys.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [16]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x14a76e233fa0>
    

The visualization module has identified that there are two separate fragments, and colored them accordingly. Of course if we merged our fragments, the visualization would look different.
    
    
    [17]:
    
    
    
    sys2 = System()
    sys2["COM:0"] = sum(sys.values())
    
    
    
    [18]:
    
    
    
    # NBVAL_IGNORE_OUTPUT
    sys2.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [18]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x14a76d3527c0>
    

## Shallow Copies and Multiple Views

It is worth recalling the copy semantics of python when dealing with complex objects.
    
    
    [19]:
    
    
    
    a = {"x": "1"}
    b = {"x": "2"}
    my_list = [a, b]
    print(my_list)
    a["x"] = 3
    print(my_list)
    
    
    
    [{'x': '1'}, {'x': '2'}]
    [{'x': 3}, {'x': '2'}]
    

We can take advantage of this to construct multiple views of the same molecule. For example, we might want to have two separate views of the same set of atoms. In one view, we’ve split the set into two molecules, and the other we have just one big fragment. This might be convenient if, for example, we want to be able to rotate the entire system as a group.
    
    
    [20]:
    
    
    
    sep = deepcopy(sys)
    joint = System()
    joint["COM:0"] = sum(sep.values())
    
    
    
    [21]:
    
    
    
    joint["COM:0"].rotate(y=90, units="degrees")
    
    
    
    [22]:
    
    
    
    # NBVAL_IGNORE_OUTPUT
    sep.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [22]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x14a7a40dd730>
    
    
    
    [23]:
    
    
    
    # NBVAL_IGNORE_OUTPUT
    joint.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [23]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x14a7a4329fa0>
    

## Extended Systems

For extended systems, the extra ingredient required is a `UnitCell`.
    
    
    [24]:
    
    
    
    from BigDFT.UnitCells import UnitCell
    sys.cell = UnitCell([7.0, 7.0, 7.0], units="angstroem")
    
    
    
    [25]:
    
    
    
    # NBVAL_IGNORE_OUTPUT
    sys.display()
    

You appear to be running in JupyterLab (or JavaScript failed to load for some other reason). You need to install the 3dmol extension:   
`jupyter labextension install jupyterlab_3dmol`
    
    
    [25]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x14a76d352dc0>
    

We see that the minimum image convention has wrapped the red fragment around so that it is now on the left side. We can inspect this position values closer from the `Atom` class.
    
    
    [26]:
    
    
    
    for fragid, frag in sys.items():
        print(fragid)
        for at in frag:
            print(at.get_position("angstroem"), at.get_position("angstroem", cell=sys.cell))
    
    
    
    WAT:0
    [2.3229430273, 1.3229430273, 1.7139430273] [2.3229430273, 1.3229430273, 1.7139430273]
    [2.3229430273, 2.0801430273, 1.1274430273] [2.3229430273, 2.0801430273, 1.1274430273]
    [2.3229430273, 0.5657430273000001, 1.1274430273] [2.3229430273, 0.5657430273000001, 1.1274430273]
    WAT:1
    [7.6147151365, 0.9319430273000001, 1.3229430272999996] [0.6147151365000005, 0.9319430273000001, 1.3229430272999996]
    [7.6147151365, 1.5184430273000002, 2.0801430272999997] [0.6147151365000005, 1.5184430273000002, 2.0801430272999997]
    [7.6147151365, 1.5184430273000002, 0.5657430272999997] [0.6147151365000005, 1.5184430273000002, 0.5657430272999997]
    

We also can get accessed to fractional units this way.
    
    
    [27]:
    
    
    
    for fragid, frag in sys.items():
        print(fragid)
        for at in frag:
            print(at.get_position("reduced", cell=sys.cell))
    
    
    
    WAT:0
    [0.3318490039, 0.18899186104285715, 0.2448490039]
    [0.3318490039, 0.29716328961428573, 0.1610632896142857]
    [0.3318490039, 0.08082043247142859, 0.1610632896142857]
    WAT:1
    [0.08781644807142865, 0.1331347181857143, 0.1889918610428571]
    [0.08781644807142865, 0.21692043247142861, 0.2971632896142857]
    [0.08781644807142865, 0.21692043247142861, 0.08082043247142852]
    

The `sys.get_posinp()` method provides the information written in `YAML` markup format:
    
    
    [28]:
    
    
    
    sys.get_posinp()
    
    
    
    [28]:
    
    
    
    {'positions': [{'O': [2.3229430273, 1.3229430273, 1.7139430273],
       'frag': ['WAT', '0']},
      {'H': [2.3229430273, 2.0801430273, 1.1274430273], 'frag': ['WAT', '0']},
      {'H': [2.3229430273, 0.5657430273000001, 1.1274430273],
       'frag': ['WAT', '0']},
      {'O': [0.6147151365000005, 0.9319430273000001, 1.3229430272999996],
       'frag': ['WAT', '1']},
      {'H': [0.6147151365000005, 1.5184430273000002, 2.0801430272999997],
       'frag': ['WAT', '1']},
      {'H': [0.6147151365000005, 1.5184430273000002, 0.5657430272999997],
       'frag': ['WAT', '1']}],
     'units': 'angstroem',
     'cell': [7.0, 7.0, 7.0]}
    

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).