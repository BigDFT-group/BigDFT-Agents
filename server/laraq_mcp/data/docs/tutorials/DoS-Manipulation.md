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
        * [Analyze a BigDFT run from a Logfile class](Logfile-basics.html)
        * [Visualization of a Linear Scaling calculation](Logfile-basics.html#Visualization-of-a-Linear-Scaling-calculation)
        * Plotting Density of States
        * [Projected Density of States](PDoS.html)
        * [Tight-binding model of graphene](Tight-Binding.html)
      * [Interoperability With Other Codes](../users/guide.html#interoperability-with-other-codes)
    * [Lessons and Workflows](../users/guide.html#lessons-and-workflows)

  * [PyBigDFT API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/index.html)

Developer

  * [BigDFT-suite manifesto](../devel/developers.html)

  * [Futile API](https://l_sim.gitlab.io/bigdft-suite/futile/build/html/index.html)

__[BigDFT-suite](../index.html)

  * [](../index.html)
  * [User Guide](../users/guide.html)
  * Plotting Density of States
  * [ View page source](../_sources/tutorials/DoS-Manipulation.ipynb.txt)

* * *

# Plotting Density of States

In this short tutorial we will inspect the basic features of the `DoS` module of PyBigDFT. We employ two runs as demonstrator of the comparison between two runs. A Bulk run of a `AlN` system, followed by a Vacancy run. The Vacancy is also provided with a Spin Collinear run, for comparison.
    
    
    [1]:
    
    
    
    from BigDFT import Logfiles as L
    Vacancy = L.Logfile('/home/genovese/Downloads/VN2_last.log')
    Bulk = L.Logfile('/home/genovese/Downloads/AlN_last.log')
    VacancySpin = L.Logfile('/home/genovese/Downloads/VNspin_last.log')
    

## Description of the tests done

We will shot how to

  1. Plot the DoS with the `plot` commodity function;

  2. Get the curves from a get_curve function;

  3. Handle those curves for external plotting;

  4. Shifts the values of the curves wrt to a constant, or a dictionary of shifts;

### Simple plots of the two runs

We here show how the two runs behave.
    
    
    [2]:
    
    
    
    ax=Bulk.get_dos().plot()
    _=ax.set_title('Bulk',fontsize=18)
    

![../_images/tutorials_DoS-Manipulation_4_0.png](../_images/tutorials_DoS-Manipulation_4_0.png)
    
    
    [3]:
    
    
    
    ax=Vacancy.get_dos().plot()
    _=ax.set_title('Vacancy',fontsize=18)
    

![../_images/tutorials_DoS-Manipulation_5_0.png](../_images/tutorials_DoS-Manipulation_5_0.png)

### Plot a DoS of a collinear Spin calculation
    
    
    [4]:
    
    
    
    _=VacancySpin.get_dos().plot().set_title('Vacancy, Collinear Spin')
    

![../_images/tutorials_DoS-Manipulation_7_0.png](../_images/tutorials_DoS-Manipulation_7_0.png)
    
    
    [5]:
    
    
    
    from BigDFT.DoS import DoS
    dosspin = DoS(logfiles_dict={'SA':Vacancy, 'SC':VacancySpin})
    

Note the modification of the labels from the original definition.
    
    
    [6]:
    
    
    
    _=dosspin.plot().legend(loc='best')
    

![../_images/tutorials_DoS-Manipulation_10_0.png](../_images/tutorials_DoS-Manipulation_10_0.png)
    
    
    [7]:
    
    
    
    list(dosspin.get_curves().keys())
    
    
    
    [7]:
    
    
    
    ['SA', 'SCup', 'SCdw']
    

### Plot of the two DoS together

We would like to compare the two runs. It is possible to instanciate a `DoS` class.
    
    
    [8]:
    
    
    
    from BigDFT.DoS import DoS
    dos = DoS(logfiles_dict={'Vacancy': Vacancy, 'Bulk': Bulk},
              fermi_level=Vacancy.fermi_level,units='AU') # last two as an option
    
    
    
    [9]:
    
    
    
    dos.plot()
    
    
    
    [9]:
    
    
    
    <matplotlib.axes._subplots.AxesSubplot at 0x7f49540ac3c8>
    

![../_images/tutorials_DoS-Manipulation_14_1.png](../_images/tutorials_DoS-Manipulation_14_1.png)

The above plot show the tow DoS together. We may select a region:
    
    
    [10]:
    
    
    
    dos.set_range(e_min=2.0,e_max=10.0)
    ax= dos.plot()
    ax.legend(loc='best')
    ax.set_title('Plot with two DoS, aligned and cropped')
    ax.annotate('Note the fermi_level here', xytext=(8,160), xy=(dos.ef,100), arrowprops = dict(arrowstyle='->'))
    
    
    
    [10]:
    
    
    
    Text(8, 160, 'Note the fermi_level here')
    

![../_images/tutorials_DoS-Manipulation_16_1.png](../_images/tutorials_DoS-Manipulation_16_1.png)
    
    
    [11]:
    
    
    
    ax= dos.plot()
    ax.legend(loc='best')
    ax.set_title('Plot with two DoS, cropped externally')
    ax.set_xlim([6,8])
      
    
    
    
    [11]:
    
    
    
    (6, 8)
    

![../_images/tutorials_DoS-Manipulation_17_1.png](../_images/tutorials_DoS-Manipulation_17_1.png)

### Handle the curves explicitly

Perform the difference between the curves and plot it
    
    
    [12]:
    
    
    
    from matplotlib import pyplot as plt
    dos.set_range(e_min=-100,e_max=100) # restore full range
    curves = dos.get_curves()
    x,yB = curves['Bulk']
    x,yV = curves['Vacancy']
    plt.plot(x,yV-yB,label='DoS differences')
    plt.legend(loc='best')
    
    
    
    [12]:
    
    
    
    <matplotlib.legend.Legend at 0x7f4953f2b518>
    

![../_images/tutorials_DoS-Manipulation_19_1.png](../_images/tutorials_DoS-Manipulation_19_1.png)

### Shift the curves and plot them shifted
    
    
    [13]:
    
    
    
    dos.shift_curves([0.0,1.0])
    ax=dos.plot()
    ax.set_title('Full plot with dos shifted')
    
    
    
    [13]:
    
    
    
    Text(0.5, 1.0, 'Full plot with dos shifted')
    

![../_images/tutorials_DoS-Manipulation_21_1.png](../_images/tutorials_DoS-Manipulation_21_1.png)

## Handle curves from spin-polarized calculations

We show also an example on customized plots where DoS differences are plot next to the original curves.
    
    
    [14]:
    
    
    
    curves = dosspin.get_curves()
    differences = {'up-down': curves['SCup'].y + curves['SCdw'].y,
                   'Noncollinear-Collinear': curves['SA'].y - curves['SCup'].y}
    x = dosspin.range
    
    
    
    [15]:
    
    
    
    from matplotlib import pyplot as plt
    fig, (axT, axD) = plt.subplots(1,2,figsize=(12,4))
    dosspin.plot(ax=axT)
    axT.legend(loc='best')
    axT.set_title('Total DoS')
    for label, curve in differences.items():
        axD.plot(x,curve,label=label)
    axD.legend(loc='best')
    axD.set_title('Difference')
    fig.tight_layout()
    

![../_images/tutorials_DoS-Manipulation_24_0.png](../_images/tutorials_DoS-Manipulation_24_0.png)

[ Previous](Logfile-basics.html "Analyze a BigDFT run from a Logfile class") [Next ](PDoS.html "Projected Density of States")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).