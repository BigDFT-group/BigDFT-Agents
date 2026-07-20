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
        * [Plotting Density of States](DoS-Manipulation.html)
        * [Projected Density of States](PDoS.html)
        * Tight-binding model of graphene
      * [Interoperability With Other Codes](../users/guide.html#interoperability-with-other-codes)
    * [Lessons and Workflows](../users/guide.html#lessons-and-workflows)

  * [PyBigDFT API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/index.html)

Developer

  * [BigDFT-suite manifesto](../devel/developers.html)

  * [Futile API](https://l_sim.gitlab.io/bigdft-suite/futile/build/html/index.html)

__[BigDFT-suite](../index.html)

  * [](../index.html)
  * [User Guide](../users/guide.html)
  * Tight-binding model of graphene
  * [ View page source](../_sources/tutorials/Tight-Binding.ipynb.txt)

* * *

# Tight-binding model of graphene

This tutorial aims at introducing the tight-binding functionalities available in PyBigDFT. The TB module currently enables to:

  * define the geometry of a given system

  * extract the corresponding matrix elements from a linear-scaling calculation

  * compute the subsequent band structure

In a nutshell, a comparison is performed between a sub-system (sys_cs) and a supercell (sys_ls) on which a LS run was carried out. This process depends on the local electronic environment, thus enabling to probe the variation due to defects in a solid-state system.
    
    
    [1]:
    
    
    
    from BigDFT import Systems, Fragments, Logfiles, TB
    from BigDFT.PostProcessing import BigDFTool
    from BigDFT.Spillage import MatrixMetadata
    
    
    
    [2]:
    
    
    
    from matplotlib import cm
    from matplotlib import pyplot as plt
    from matplotlib.colors import LogNorm, Normalize
    
    
    
    [3]:
    
    
    
    import numpy as np
    from scipy.constants import value
    
    sq3 = np.sqrt(3)
    Ha2eV = value('Hartree energy in eV') # (A)
    
    
    
    /opt/intel/oneapi/intelpython/latest/lib/python3.9/site-packages/scipy/__init__.py:146: UserWarning: A NumPy version >=1.16.5 and <1.23.0 is required for this version of SciPy (detected version 1.23.5
      warnings.warn(f"A NumPy version >={np_minversion} and <{np_maxversion}"
    

## Geometry definition

Importantly, consistency is required between both systems lattice constants, so that geometrical correspondence can be established.
    
    
    [4]:
    
    
    
    a0 = 2.5 # lattice parameter
    name = 'gr_scell' # supercell label
    

Definition of the primitive and conventional cells of an hexagonal lattice. The primitive cell is used to browse the TB workflow, while the conventional one is employed for the recap at the end of this tutorial.
    
    
    [5]:
    
    
    
    coord = {'prim': np.array([[0,0,0],
                               [a0/sq3,0,0]]),
             'conv': np.array([[0,0,0],
                               [a0/sq3,0,0],
                               [a0*sq3/2,0,a0/2],
                               [a0*5/sq3/2,0,a0/2]])}
    
    cell = {'prim': np.array([[a0*sq3/2,0,a0/2],
                              [0,float("inf"),0],
                              [a0*sq3/2,0,-a0/2]]),
            'conv': np.array([[a0*sq3,0,0],
                              [0,float("inf"),0],
                              [0,0,a0]])}
    

From the definitions of atomic coordinates and the unit cell, the sub-system is constructed. Remember that `Systems` are collections of `Fragments` in BigDFT. In the following, the solid-state system is defined as one fragment.
    
    
    [6]:
    
    
    
    positions = [{'C':list(j)} for j in coord['prim']]
    posinp = {'positions': positions, 'units': 'angstroem'}
    
    frag = Fragments.Fragment(posinp=posinp)
    sys_cs = Systems.System()
    sys_cs["FRA:1"] = frag
    

Since non-orthorombic cells are not yet handled in BigDFT, the following procedure is required when defining the unit cell
    
    
    [7]:
    
    
    
    sys_cs.cell.cell = cell['prim']
    

### Tight-binding parameters

The TB parametrization relies on definition on interaction region, where electronic contributions are added to the Hamiltonian. This approach is similar to the localization constraint employed in linear scaling. In addition to a `Systems.System`, a TB object need an interaction radius \\(d\\).
    
    
    [8]:
    
    
    
    d = 5 # 1nn or 3nn are advised for graphene
    tb = TB.TightBinding(sys_cs, d=d)
    

### Mapping between sites and Bravais vectors

From the previous parametrization, a mapping is established between atoms in the unit cell and their periodic images within a distance \\(d\\). The Bravais vectors connecting those sites are denoted \\(R_{ij}\\). The TB object therefore contains a dictionary \\(R_{sh}\\) defined such as:

\\(R_{sh}\\) = {…, {(\\(i\\),\\(j\\),(\\(n_{ij}\\))): \\(R_{ij}\\)}, …}

where \\(i\\), \\(j\\) are atoms sites, \\(n_{ij}\\) are the Bravais indices.

For example, the nearest-neighbors (\\(1nn\\)) model in graphene is defined as a dictionary of 8 entries, i.e. 2 on-site terms and 3 pairs of 1\\(nn\\) terms.
    
    
    [9]:
    
    
    
    tb._sites_in_shell(d=1.5)
    
    
    
    [9]:
    
    
    
    {(0, 0, (0, 0, 0)): [0.0, 0.0, 0.0],
     (0, 1, (-1, 0, 0)): [-0.7216878364870318, 0.0, -1.25],
     (0, 1, (0, 0, -1)): [-0.7216878364870318, 0.0, 1.25],
     (0, 1, (0, 0, 0)): [1.4433756729740645, 0.0, 0.0],
     (1, 0, (0, 0, 0)): [-1.4433756729740645, 0.0, 0.0],
     (1, 0, (0, 0, 1)): [0.7216878364870318, 0.0, -1.25],
     (1, 0, (1, 0, 0)): [0.7216878364870318, 0.0, 1.25],
     (1, 1, (0, 0, 0)): [0.0, 0.0, 0.0]}
    

It can often be insightful to visualize the selected atoms of the TB model
    
    
    [10]:
    
    
    
    fig = plt.figure(figsize=(4,4))
    ax = plt.gca()
    x0,_,z0 = coord['prim'][0]
    circle = plt.Circle((x0,z0), d, color='g', fill=False)
    ax.add_patch(circle)
    for (i,j,idk),r_ij in tb.R_sh.items():
        if i>j:
            continue
        xi,_,zi = coord['prim'][i]
        xj,_,zj = coord['prim'][i]+r_ij
        plt.plot([xi,xj], [zi,zj], 'bo')
    plt.plot([0,cell['prim'][0,0]], [0,cell['prim'][0,2]], 'r-')
    plt.plot([0,cell['prim'][2,0]], [0,cell['prim'][2,2]], 'r-')
    plt.axis('equal'); plt.axis('off'); plt.show()
    

![../_images/tutorials_Tight-Binding_18_0.png](../_images/tutorials_Tight-Binding_18_0.png)

### Structure wrapping with supercell

Once the TB model is parametrized, a geometrical matching is established between the supercell and the sub-system
    
    
    [11]:
    
    
    
    if 'log' not in locals():
        log = Logfiles.Logfile(f'log-{name}.yaml')
    

From the logfile, a `Systems.System` is loaded
    
    
    [12]:
    
    
    
    posinp = Logfiles.Logfile(f'{name}.yaml').astruct #['posinp']
    sys_ls = Systems.system_from_dict_positions(posinp['positions'])
    

The primitive cell is then connected to the supercell through an atoms mapping. The supercell indices establish the correspondence between the two systems, with the associated MSE given to assess the matching quality.
    
    
    [13]:
    
    
    
    m_idx = tb.matching_index(sys_ls);
    idx = m_idx['idx']; print(m_idx)
    
    
    
    {'idx': [626, 209], 'mse': 8.845044099689063e-18}
    

## Hamiltonian extraction

Now, the matrices elements of the associated atoms need to be extracted.

First, the hamiltonian and overlap matrices are loaded, as well as the metadata. We copy these matrices from the resource repository of BigDFT
    
    
    [14]:
    
    
    
    from futile.Utils import data_path, untar_archive
    archive=f'data-{name}.tar.xz'
    data_path(archive)
    untar_archive(archive)
    
    
    
    Executing: wget https://raw.githubusercontent.com/BigDFT-group/resources/main/datalake/data-gr_scell.tar.xz -O lfs.info
    --2024-04-12 14:06:44--  https://raw.githubusercontent.com/BigDFT-group/resources/main/datalake/data-gr_scell.tar.xz
    Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 2606:50c0:8003::154, 2606:50c0:8002::154, 2606:50c0:8000::154, ...
    Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|2606:50c0:8003::154|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 133 [text/plain]
    Saving to: ‘lfs.info’
    
         0K                                                       100% 1.89M=0s
    
    2024-04-12 14:06:44 (1.89 MB/s) - ‘lfs.info’ saved [133/133]
    
    
    
    
    
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   904  100   748  100   156   1897    395 --:--:-- --:--:-- --:--:--  2294
    
    
    
    Executing: wget https://github-cloud.githubusercontent.com/alambic/media/547350918/80/c0/80c09b6c1f74f890e4608c5780432295ff23f6a27f29b240f0bb37b9607b84de?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA5BA2674WPWWEFGQ5%2F20240412%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240412T140644Z&X-Amz-Expires=3600&X-Amz-Signature=58323c4ed9ca636868156d39a68977f56dcad8351dab538fe4b3d989f290e5e0&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=596478275&token=1 -O ./data-gr_scell.tar.xz
    --2024-04-12 14:06:44--  https://github-cloud.githubusercontent.com/alambic/media/547350918/80/c0/80c09b6c1f74f890e4608c5780432295ff23f6a27f29b240f0bb37b9607b84de?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA5BA2674WPWWEFGQ5%2F20240412%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240412T140644Z&X-Amz-Expires=3600&X-Amz-Signature=58323c4ed9ca636868156d39a68977f56dcad8351dab538fe4b3d989f290e5e0&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=596478275&token=1
    Resolving github-cloud.githubusercontent.com (github-cloud.githubusercontent.com)... 185.199.111.154, 185.199.110.154, 185.199.109.154, ...
    Connecting to github-cloud.githubusercontent.com (github-cloud.githubusercontent.com)|185.199.111.154|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 12322968 (12M) [application/octet-stream]
    Saving to: ‘./data-gr_scell.tar.xz’
    
         0K .......... .......... .......... .......... ..........  0% 1.32M 9s
        50K .......... .......... .......... .......... ..........  0% 3.51M 6s
       100K .......... .......... .......... .......... ..........  1% 4.12M 5s
       150K .......... .......... .......... .......... ..........  1% 4.93M 4s
       200K .......... .......... .......... .......... ..........  2% 11.0M 4s
       250K .......... .......... .......... .......... ..........  2% 4.48M 3s
       300K .......... .......... .......... .......... ..........  2% 5.97M 3s
       350K .......... .......... .......... .......... ..........  3% 7.67M 3s
       400K .......... .......... .......... .......... ..........  3% 4.48M 3s
       450K .......... .......... .......... .......... ..........  4% 22.1M 3s
       500K .......... .......... .......... .......... ..........  4% 4.58M 3s
       550K .......... .......... .......... .......... ..........  4% 3.68M 3s
       600K .......... .......... .......... .......... ..........  5% 4.14M 3s
       650K .......... .......... .......... .......... ..........  5% 56.6M 2s
       700K .......... .......... .......... .......... ..........  6% 4.03M 2s
       750K .......... .......... .......... .......... ..........  6% 55.4M 2s
       800K .......... .......... .......... .......... ..........  7% 3.98M 2s
       850K .......... .......... .......... .......... ..........  7% 4.00M 2s
       900K .......... .......... .......... .......... ..........  7% 51.1M 2s
       950K .......... .......... .......... .......... ..........  8% 3.94M 2s
      1000K .......... .......... .......... .......... ..........  8% 4.04M 2s
      1050K .......... .......... .......... .......... ..........  9% 29.9M 2s
      1100K .......... .......... .......... .......... ..........  9% 3.86M 2s
      1150K .......... .......... .......... .......... ..........  9%  217M 2s
      1200K .......... .......... .......... .......... .......... 10% 3.78M 2s
      1250K .......... .......... .......... .......... .......... 10% 3.37M 2s
      1300K .......... .......... .......... .......... .......... 11%  315M 2s
      1350K .......... .......... .......... .......... .......... 11% 3.60M 2s
      1400K .......... .......... .......... .......... .......... 12%  117M 2s
      1450K .......... .......... .......... .......... .......... 12% 3.81M 2s
      1500K .......... .......... .......... .......... .......... 12% 4.07M 2s
      1550K .......... .......... .......... .......... .......... 13% 36.5M 2s
      1600K .......... .......... .......... .......... .......... 13% 3.97M 2s
      1650K .......... .......... .......... .......... .......... 14% 3.34M 2s
      1700K .......... .......... .......... .......... .......... 14% 93.8M 2s
      1750K .......... .......... .......... .......... .......... 14% 3.62M 2s
      1800K .......... .......... .......... .......... .......... 15% 24.9M 2s
      1850K .......... .......... .......... .......... .......... 15% 3.88M 2s
      1900K .......... .......... .......... .......... .......... 16% 4.04M 2s
      1950K .......... .......... .......... .......... .......... 16% 3.76M 2s
      2000K .......... .......... .......... .......... .......... 17% 22.9M 2s
      2050K .......... .......... .......... .......... .......... 17% 3.70M 2s
      2100K .......... .......... .......... .......... .......... 17% 4.60M 2s
      2150K .......... .......... .......... .......... .......... 18% 17.7M 2s
      2200K .......... .......... .......... .......... .......... 18% 4.98M 2s
      2250K .......... .......... .......... .......... .......... 19% 3.93M 2s
      2300K .......... .......... .......... .......... .......... 19% 15.4M 2s
      2350K .......... .......... .......... .......... .......... 19% 4.82M 2s
      2400K .......... .......... .......... .......... .......... 20% 16.6M 2s
      2450K .......... .......... .......... .......... .......... 20% 3.99M 2s
      2500K .......... .......... .......... .......... .......... 21% 4.09M 2s
      2550K .......... .......... .......... .......... .......... 21% 43.3M 2s
      2600K .......... .......... .......... .......... .......... 22% 4.26M 2s
      2650K .......... .......... .......... .......... .......... 22% 34.0M 2s
      2700K .......... .......... .......... .......... .......... 22% 4.05M 2s
      2750K .......... .......... .......... .......... .......... 23% 3.33M 2s
      2800K .......... .......... .......... .......... .......... 23% 49.8M 2s
      2850K .......... .......... .......... .......... .......... 24% 3.88M 2s
      2900K .......... .......... .......... .......... .......... 24% 29.7M 2s
      2950K .......... .......... .......... .......... .......... 24% 4.41M 2s
      3000K .......... .......... .......... .......... .......... 25% 25.5M 2s
      3050K .......... .......... .......... .......... .......... 25% 3.91M 2s
      3100K .......... .......... .......... .......... .......... 26% 4.49M 2s
      3150K .......... .......... .......... .......... .......... 26% 23.7M 2s
      3200K .......... .......... .......... .......... .......... 27% 4.47M 2s
      3250K .......... .......... .......... .......... .......... 27% 23.3M 2s
      3300K .......... .......... .......... .......... .......... 27% 4.50M 2s
      3350K .......... .......... .......... .......... .......... 28% 4.02M 2s
      3400K .......... .......... .......... .......... .......... 28% 24.6M 1s
      3450K .......... .......... .......... .......... .......... 29% 4.31M 1s
      3500K .......... .......... .......... .......... .......... 29% 31.8M 1s
      3550K .......... .......... .......... .......... .......... 29% 4.38M 1s
      3600K .......... .......... .......... .......... .......... 30% 29.0M 1s
      3650K .......... .......... .......... .......... .......... 30% 3.95M 1s
      3700K .......... .......... .......... .......... .......... 31% 4.02M 1s
      3750K .......... .......... .......... .......... .......... 31% 30.0M 1s
      3800K .......... .......... .......... .......... .......... 31% 4.36M 1s
      3850K .......... .......... .......... .......... .......... 32% 26.4M 1s
      3900K .......... .......... .......... .......... .......... 32% 4.41M 1s
      3950K .......... .......... .......... .......... .......... 33% 3.85M 1s
      4000K .......... .......... .......... .......... .......... 33% 33.0M 1s
      4050K .......... .......... .......... .......... .......... 34% 4.25M 1s
      4100K .......... .......... .......... .......... .......... 34% 32.3M 1s
      4150K .......... .......... .......... .......... .......... 34% 4.21M 1s
      4200K .......... .......... .......... .......... .......... 35% 3.96M 1s
      4250K .......... .......... .......... .......... .......... 35% 32.6M 1s
      4300K .......... .......... .......... .......... .......... 36% 4.25M 1s
      4350K .......... .......... .......... .......... .......... 36% 25.6M 1s
      4400K .......... .......... .......... .......... .......... 36% 4.20M 1s
      4450K .......... .......... .......... .......... .......... 37% 35.4M 1s
      4500K .......... .......... .......... .......... .......... 37% 4.00M 1s
      4550K .......... .......... .......... .......... .......... 38% 3.76M 1s
      4600K .......... .......... .......... .......... .......... 38% 28.2M 1s
      4650K .......... .......... .......... .......... .......... 39% 3.72M 1s
      4700K .......... .......... .......... .......... .......... 39% 31.0M 1s
      4750K .......... .......... .......... .......... .......... 39% 4.06M 1s
      4800K .......... .......... .......... .......... .......... 40% 3.98M 1s
      4850K .......... .......... .......... .......... .......... 40% 46.4M 1s
      4900K .......... .......... .......... .......... .......... 41% 4.10M 1s
      4950K .......... .......... .......... .......... .......... 41% 57.3M 1s
      5000K .......... .......... .......... .......... .......... 41% 3.99M 1s
      5050K .......... .......... .......... .......... .......... 42% 67.6M 1s
      5100K .......... .......... .......... .......... .......... 42% 3.89M 1s
      5150K .......... .......... .......... .......... .......... 43% 4.05M 1s
      5200K .......... .......... .......... .......... .......... 43% 66.1M 1s
      5250K .......... .......... .......... .......... .......... 44% 3.89M 1s
      5300K .......... .......... .......... .......... .......... 44% 66.8M 1s
      5350K .......... .......... .......... .......... .......... 44% 3.83M 1s
      5400K .......... .......... .......... .......... .......... 45% 3.91M 1s
      5450K .......... .......... .......... .......... .......... 45% 77.4M 1s
      5500K .......... .......... .......... .......... .......... 46% 3.97M 1s
      5550K .......... .......... .......... .......... .......... 46% 4.11M 1s
      5600K .......... .......... .......... .......... .......... 46% 4.05M 1s
      5650K .......... .......... .......... .......... .......... 47% 4.05M 1s
      5700K .......... .......... .......... .......... .......... 47% 25.4M 1s
      5750K .......... .......... .......... .......... .......... 48% 4.32M 1s
      5800K .......... .......... .......... .......... .......... 48% 36.1M 1s
      5850K .......... .......... .......... .......... .......... 49% 4.13M 1s
      5900K .......... .......... .......... .......... .......... 49% 3.95M 1s
      5950K .......... .......... .......... .......... .......... 49% 48.1M 1s
      6000K .......... .......... .......... .......... .......... 50% 3.97M 1s
      6050K .......... .......... .......... .......... .......... 50% 4.19M 1s
      6100K .......... .......... .......... .......... .......... 51% 36.8M 1s
      6150K .......... .......... .......... .......... .......... 51% 4.20M 1s
      6200K .......... .......... .......... .......... .......... 51% 32.2M 1s
      6250K .......... .......... .......... .......... .......... 52% 4.13M 1s
      6300K .......... .......... .......... .......... .......... 52% 4.14M 1s
      6350K .......... .......... .......... .......... .......... 53% 4.00M 1s
      6400K .......... .......... .......... .......... .......... 53% 41.6M 1s
      6450K .......... .......... .......... .......... .......... 54% 4.10M 1s
      6500K .......... .......... .......... .......... .......... 54% 37.4M 1s
      6550K .......... .......... .......... .......... .......... 54% 4.17M 1s
      6600K .......... .......... .......... .......... .......... 55% 3.99M 1s
      6650K .......... .......... .......... .......... .......... 55% 52.4M 1s
      6700K .......... .......... .......... .......... .......... 56% 3.84M 1s
      6750K .......... .......... .......... .......... .......... 56%  118M 1s
      6800K .......... .......... .......... .......... .......... 56% 3.82M 1s
      6850K .......... .......... .......... .......... .......... 57% 3.13M 1s
      6900K .......... .......... .......... .......... .......... 57%  125M 1s
      6950K .......... .......... .......... .......... .......... 58% 3.51M 1s
      7000K .......... .......... .......... .......... .......... 58% 27.1M 1s
      7050K .......... .......... .......... .......... .......... 58% 3.79M 1s
      7100K .......... .......... .......... .......... .......... 59% 4.07M 1s
      7150K .......... .......... .......... .......... .......... 59% 13.9M 1s
      7200K .......... .......... .......... .......... .......... 60% 4.14M 1s
      7250K .......... .......... .......... .......... .......... 60% 4.67M 1s
      7300K .......... .......... .......... .......... .......... 61% 19.4M 1s
      7350K .......... .......... .......... .......... .......... 61% 4.13M 1s
      7400K .......... .......... .......... .......... .......... 61% 46.7M 1s
      7450K .......... .......... .......... .......... .......... 62% 3.97M 1s
      7500K .......... .......... .......... .......... .......... 62% 4.19M 1s
      7550K .......... .......... .......... .......... .......... 63% 4.36M 1s
      7600K .......... .......... .......... .......... .......... 63% 26.5M 1s
      7650K .......... .......... .......... .......... .......... 63% 4.53M 1s
      7700K .......... .......... .......... .......... .......... 64% 3.83M 1s
      7750K .......... .......... .......... .......... .......... 64% 4.31M 1s
      7800K .......... .......... .......... .......... .......... 65% 30.6M 1s
      7850K .......... .......... .......... .......... .......... 65% 3.96M 1s
      7900K .......... .......... .......... .......... .......... 66% 3.87M 1s
      7950K .......... .......... .......... .......... .......... 66% 78.5M 1s
      8000K .......... .......... .......... .......... .......... 66% 3.95M 1s
      8050K .......... .......... .......... .......... .......... 67% 4.73M 1s
      8100K .......... .......... .......... .......... .......... 67% 17.6M 1s
      8150K .......... .......... .......... .......... .......... 68% 3.51M 1s
      8200K .......... .......... .......... .......... .......... 68% 4.01M 1s
      8250K .......... .......... .......... .......... .......... 68% 55.5M 1s
      8300K .......... .......... .......... .......... .......... 69% 3.97M 1s
      8350K .......... .......... .......... .......... .......... 69% 48.5M 1s
      8400K .......... .......... .......... .......... .......... 70% 4.00M 1s
      8450K .......... .......... .......... .......... .......... 70% 4.17M 1s
      8500K .......... .......... .......... .......... .......... 71% 4.14M 1s
      8550K .......... .......... .......... .......... .......... 71% 34.6M 1s
      8600K .......... .......... .......... .......... .......... 71% 4.13M 1s
      8650K .......... .......... .......... .......... .......... 72% 54.3M 1s
      8700K .......... .......... .......... .......... .......... 72% 3.97M 1s
      8750K .......... .......... .......... .......... .......... 73% 3.91M 1s
      8800K .......... .......... .......... .......... .......... 73% 46.4M 1s
      8850K .......... .......... .......... .......... .......... 73% 4.00M 1s
      8900K .......... .......... .......... .......... .......... 74% 61.2M 1s
      8950K .......... .......... .......... .......... .......... 74% 3.86M 1s
      9000K .......... .......... .......... .......... .......... 75% 3.90M 1s
      9050K .......... .......... .......... .......... .......... 75% 55.7M 0s
      9100K .......... .......... .......... .......... .......... 76% 4.02M 0s
      9150K .......... .......... .......... .......... .......... 76% 3.99M 0s
      9200K .......... .......... .......... .......... .......... 76% 69.6M 0s
      9250K .......... .......... .......... .......... .......... 77% 3.94M 0s
      9300K .......... .......... .......... .......... .......... 77% 3.89M 0s
      9350K .......... .......... .......... .......... .......... 78% 60.7M 0s
      9400K .......... .......... .......... .......... .......... 78% 4.03M 0s
      9450K .......... .......... .......... .......... .......... 78% 54.1M 0s
      9500K .......... .......... .......... .......... .......... 79% 3.98M 0s
      9550K .......... .......... .......... .......... .......... 79% 4.08M 0s
      9600K .......... .......... .......... .......... .......... 80% 44.6M 0s
      9650K .......... .......... .......... .......... .......... 80% 4.01M 0s
      9700K .......... .......... .......... .......... .......... 81% 44.0M 0s
      9750K .......... .......... .......... .......... .......... 81% 4.01M 0s
      9800K .......... .......... .......... .......... .......... 81% 62.2M 0s
      9850K .......... .......... .......... .......... .......... 82% 3.92M 0s
      9900K .......... .......... .......... .......... .......... 82% 3.83M 0s
      9950K .......... .......... .......... .......... .......... 83% 11.2M 0s
     10000K .......... .......... .......... .......... .......... 83% 5.45M 0s
     10050K .......... .......... .......... .......... .......... 83% 4.02M 0s
     10100K .......... .......... .......... .......... .......... 84% 13.2M 0s
     10150K .......... .......... .......... .......... .......... 84% 5.45M 0s
     10200K .......... .......... .......... .......... .......... 85% 11.7M 0s
     10250K .......... .......... .......... .......... .......... 85% 3.82M 0s
     10300K .......... .......... .......... .......... .......... 86% 5.74M 0s
     10350K .......... .......... .......... .......... .......... 86% 11.0M 0s
     10400K .......... .......... .......... .......... .......... 86% 5.03M 0s
     10450K .......... .......... .......... .......... .......... 87% 3.83M 0s
     10500K .......... .......... .......... .......... .......... 87%  105M 0s
     10550K .......... .......... .......... .......... .......... 88% 3.79M 0s
     10600K .......... .......... .......... .......... .......... 88% 21.3M 0s
     10650K .......... .......... .......... .......... .......... 88% 4.41M 0s
     10700K .......... .......... .......... .......... .......... 89% 21.3M 0s
     10750K .......... .......... .......... .......... .......... 89% 4.54M 0s
     10800K .......... .......... .......... .......... .......... 90% 3.97M 0s
     10850K .......... .......... .......... .......... .......... 90% 29.5M 0s
     10900K .......... .......... .......... .......... .......... 90% 4.28M 0s
     10950K .......... .......... .......... .......... .......... 91% 22.8M 0s
     11000K .......... .......... .......... .......... .......... 91% 4.32M 0s
     11050K .......... .......... .......... .......... .......... 92% 28.9M 0s
     11100K .......... .......... .......... .......... .......... 92% 3.28M 0s
     11150K .......... .......... .......... .......... .......... 93% 5.53M 0s
     11200K .......... .......... .......... .......... .......... 93% 11.8M 0s
     11250K .......... .......... .......... .......... .......... 93% 5.54M 0s
     11300K .......... .......... .......... .......... .......... 94% 10.7M 0s
     11350K .......... .......... .......... .......... .......... 94% 6.05M 0s
     11400K .......... .......... .......... .......... .......... 95% 4.05M 0s
     11450K .......... .......... .......... .......... .......... 95% 8.94M 0s
     11500K .......... .......... .......... .......... .......... 95% 6.20M 0s
     11550K .......... .......... .......... .......... .......... 96% 9.69M 0s
     11600K .......... .......... .......... .......... .......... 96% 6.11M 0s
     11650K .......... .......... .......... .......... .......... 97% 3.95M 0s
     11700K .......... .......... .......... .......... .......... 97% 9.91M 0s
     11750K .......... .......... .......... .......... .......... 98% 5.64M 0s
     11800K .......... .......... .......... .......... .......... 98% 3.95M 0s
     11850K .......... .......... .......... .......... .......... 98% 12.8M 0s
     11900K .......... .......... .......... .......... .......... 99% 5.49M 0s
     11950K .......... .......... .......... .......... .......... 99% 3.91M 0s
     12000K .......... .......... .......... ....                 100%  107M=2.0s
    
    2024-04-12 14:06:47 (5.93 MB/s) - ‘./data-gr_scell.tar.xz’ saved [12322968/12322968]
    
    
    
    
    
    [14]:
    
    
    
    ['data-gr_scell',
     'data-gr_scell/sparsematrix_metadata.dat',
     'data-gr_scell/overlap_sparse.mtx',
     'data-gr_scell/hamiltonian_sparse.mtx']
    
    
    
    [15]:
    
    
    
    if 'h' and 's' not in locals():
        tool = BigDFTool()
        h = tool.get_matrix_h(log)
        s = tool.get_matrix_s(log)
    
    metadatafile = f'data-{name}/sparsematrix_metadata.dat'
    metadata = MatrixMetadata(metadatafile)
    

The matrices elements are extracted using the `shell_matrix` function, returning \\(H\\) and \\(S\\) inside a dictionary that also contains information on the basis set.
    
    
    [16]:
    
    
    
    m_sh = tb.shell_matrix(sys_ls, [h,s], metadata)
    list(m_sh.keys())
    
    
    
    [16]:
    
    
    
    ['id', 'h', 's']
    

The basis set is defined by the atoms mapping and their orbitals. In this case, the 626\\(^{th}\\) and 209\\(^{th}\\) atoms (corresponding to the \\(A\\) and \\(B\\) lattices) have 4 orbitals each, starting from the 0\\(^{th}\\) and the 4\\(^{th}\\) index, respectively. The last entry in the orbitals definition therefore give the total number of orbitals.
    
    
    [17]:
    
    
    
    m_sh['id']
    
    
    
    [17]:
    
    
    
    {'atoms': [626, 209], 'orbs': [0, 4, 8]}
    

The Hamiltonian \\(H_{ij}\\) between sites \\(i\\) and \\(j\\) is defined in a similar way to \\(R_{ij}\\). Visualizing the different matrix elements is therefore straightforwards. In this example, the on-site and \\(1nn\\) terms are displayed.
    
    
    [18]:
    
    
    
    fig,axs = plt.subplots(1,2,figsize=(10,4))
    axs[0].imshow(abs(m_sh['h'][(0,0,(0,0,0))]),
                  norm=LogNorm(vmin=1e-3,vmax=1e0),
                  # norm=Normalize(vmin=0,vmax=.4),
                  cmap=cm.Blues,aspect='equal')
    axs[1].imshow(abs(m_sh['h'][(0,1,(0,0,0))]),
                  norm=LogNorm(vmin=1e-3,vmax=1e0),
                  # norm=Normalize(vmin=0,vmax=.4),
                  cmap=cm.Blues,aspect='equal')
    plt.show()
    

![../_images/tutorials_Tight-Binding_35_0.png](../_images/tutorials_Tight-Binding_35_0.png)

## Band structure computation

Once the Hamiltonian extraction is completed, the band structure is obtained in a few steps.

First, the \\(k\\)-path is defined
    
    
    [19]:
    
    
    
    hsp = {'G1': [0., 0., 0.],
           'M': [0.5, 0., 0.5],
           'K': [0.666666, 0., 0.333333],
           'G2': [0., 0., 0.]}
    k = tb.k_path(hsp)
    

The eigenvalues are then computed by solving the Schrodinger’s equation. The `k_matrix` functions returns the k-resolved matrices and their corresponding eigenvalues.
    
    
    [20]:
    
    
    
    Hk,Sk,Ek = tb.k_matrix(k, m_sh)
    

Finally, the band structure is plotted
    
    
    [21]:
    
    
    
    Ef = log.fermi_level
    TB.plot_bs(k, Ek-Ef)
    plt.ylim([-14,14])
    plt.show()
    

![../_images/tutorials_Tight-Binding_42_0.png](../_images/tutorials_Tight-Binding_42_0.png)

## In a nutshell

To summarize the tight-binding workflow, the conventional cell is studied.

First, the sub-system is updated with the proper geometry
    
    
    [22]:
    
    
    
    positions = [{'C':list(j)} for j in coord['conv']]
    posinp = {'positions': positions, 'units': 'angstroem'}
    
    frag = Fragments.Fragment(posinp=posinp)
    sys_cs = Systems.System()
    sys_cs["FRA:1"] = frag
    
    sys_cs.cell.cell = cell['conv']
    

The corresponding TB object is defined
    
    
    [23]:
    
    
    
    tb = TB.TightBinding(sys_cs, d=5)
    

The matrix description is extracted
    
    
    [24]:
    
    
    
    m_sh = tb.shell_matrix(sys_ls, [h,s], metadata)
    

The band structure is then computed for the associated k-points
    
    
    [25]:
    
    
    
    hsp = {'G': [0., 0., 0.],
           'Y': [0., 0., 0.5]}
    k = tb.k_path(hsp)
    
    
    
    [26]:
    
    
    
    Hk,Sk,Ek = tb.k_matrix(k, m_sh)
    
    
    
    [27]:
    
    
    
    Ef = log.fermi_level
    TB.plot_bs(k, Ek-Ef)
    plt.ylim([-14,10])
    plt.show()
    

![../_images/tutorials_Tight-Binding_53_0.png](../_images/tutorials_Tight-Binding_53_0.png)
    
    
    [ ]:
    
    
    
    
    
    
    [ ]:
    
    
    
    

[ Previous](PDoS.html "Projected Density of States") [Next ](Interoperability-Visualization.html "Interoperability With Visualization Software")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).