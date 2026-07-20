[ BigDFT-suite ![Logo](../_static/logo-bigdft-white.svg) ](../index.html)

Overview

  * [Available Functionalities](../overview/functionality.html)

  * [The BigDFT-suite Package](../overview/package.html)

  * [Publications](../overview/publications.html)

  * [License](../overview/license.html)

Basic Usage

  * [Installation](../users/install.html)

  * [Quick Start - From Python](QuickStart.html)

  * Quick Start - Command Line
    * Input File
    * Running the Code
    * Results
    * Profiles
    * PyBigDFT Compatability

User Guide

  * [User Guide](../users/guide.html)

  * [PyBigDFT API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/index.html)

Developer

  * [BigDFT-suite manifesto](../devel/developers.html)

  * [Futile API](https://l_sim.gitlab.io/bigdft-suite/futile/build/html/index.html)

__[BigDFT-suite](../index.html)

  * [](../index.html)
  * Quick Start - Command Line
  * [ View page source](../_sources/school/CMDStart.ipynb.txt)

* * *

# Quick Start - Command Line

While we strongly recommend PyBigDFT as the way to drive BigDFT calculations, you may nonetheless want to run calculations from the command line. If you have installed from source, you should make sure you have setup the proper environment variables using the following command:
    
    
    source install/bin/bigdftvars.sh
    

## Input File

Input files are in the [yaml](https://yaml.org) format. A simple example is:
    
    
    [1]:
    
    
    
    !cat cmd_work/psys.yaml
    
    
    
    dft: {hgrids: 0.3, ixc: LDA}
    kpt:
      method: mpgrid
      ngkpt: [2, 2, 2]
    posinp:
      cell: [2.867, 2.867, 2.867]
      positions:
      - Fe: [0.0, 0.0, 0.0]
      units: angstroem
    

To use more exotic exchange and correlation potentials, you will need to:

  1. Lookup the XC code on the website of [libxc](https://tddft.org/programs/libxc/functionals/), and prepend a minus sign before the exchange and correlation code.

  2. Copy the pseudopotentials you wish to use to the calculation directory with the name `psppar.ELEMENT`. We have included some in `bigdft/utils/PSPfiles/`.

    
    
    [2]:
    
    
    
    !cat pspwork/psys.yaml
    
    
    
    dft:
      hgrids: 0.3
      ixc: -109134 # PW91
    kpt:
      method: mpgrid
      ngkpt: [2, 2, 2]
    posinp:
      cell: [2.867, 2.867, 2.867]
      positions:
      - Fe: [0.0, 0.0, 0.0]
      units: angstroem
    
    
    
    [3]:
    
    
    
    !cat pspwork/psppar.Fe
    
    
    
    Goedecker pseudopotential for Fe
       26  16  070301 zatom,zion,pspdat
    10 11  2 2 2001 0  pspcod,pspxc,lmax,lloc,mmax,r2well
         0.36000000    2     6.75678916    -0.22883251                                  rloc nloc c1 c2
        3                                                                               nnonloc
         0.27826303    2     0.62950570     7.91313242                                  rs ns hs11 hs12
                                          -10.21581002                                             hs22
         0.25138338    2    -7.93213293     7.69707888                                  rp np hp11 hp12
                                           -9.10730654                                             hp22
                             0.09786820     0.08070002                                        kp11 kp12
                                           -0.09548555                                             kp22
         0.22285578    1   -12.38579937                                                 rd nd hd11
                             0.01036288                                                       kd11
    

## Running the Code

To run the code, use a line like this:
    
    
    [4]:
    
    
    
    !cd cmd_work ; $BIGDFT_ROOT/bigdft -n psys ; cd ..
    
    
    
     <BigDFT> log of the run will be written in logfile: ./log-psys.yaml
    

Notice the `-n` option gives the name of the input file. If nothing is given, bigdft will look for `default.yaml`.

The skip command will check if the calculation has completed, and if so will immediately exit.
    
    
    [5]:
    
    
    
    !cd cmd_work ; $BIGDFT_ROOT/bigdft -n psys -s yes ; cd ..
    
    
    
     <BigDFT> Run already performed, found final file: forces_psys.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: unknown
     Walltime since initialization:  00:00:00.272820000
     Max No. of dictionaries used:  1119 #( 1044 still in use)
     Number of dictionary folders allocated:  1
    

## Results

The following files are produced by a calculation.
    
    
    [6]:
    
    
    
    !ls cmd_work/*psys*
    
    
    
    cmd_work/forces_psys.yaml  cmd_work/psys_minimal.yaml
    cmd_work/log-psys.yaml     cmd_work/time-psys.yaml
    cmd_work/psys.yaml
    

The log file contains the essential calculation information in a `yaml` format.
    
    
    [7]:
    
    
    
    !grep "Energy (Hartree)" cmd_work/log-psys.yaml
    
    
    
     Energy (Hartree)                      : -2.05484837694368423E+01
    

The log file contains a list of all input variables and their values, not just the ones you set. They have comments beside them. This can be useful when trying to find out how to modify the calculation. For example, what was the spin of the calculation?
    
    
    [8]:
    
    
    
    !grep "nspin" cmd_work/log-psys.yaml
    
    
    
       nspin                               : 1 #      Spin polarization treatment
    

In the case of geometry optimization, each step can be found in the same logfile.
    
    
    [9]:
    
    
    
    !cat cmd_work/geom.yaml
    
    
    
    dft: {hgrids: 0.35, ixc: PBE}
    geopt: {"method": SQNM}
    posinp:
      cell: [.inf, .inf, .inf]
      positions:
      - H: [0.0, 0.0, 0.0]
      - H: [0.0, 0.0, 0.741]
      - He: [5.292, 0.0, 0.0]
      units: angstroem
    
    
    
    [10]:
    
    
    
    !cd cmd_work ; $BIGDFT_ROOT/bigdft -n geom -s yes ; cd ..
    
    
    
     <BigDFT> log of the run will be written in logfile: ./log-geom.yaml
    

The details of the geometry optimization procedure are also available in the data directory.
    
    
    [11]:
    
    
    
    !ls cmd_work/data-geom
    
    
    
    geopt.mon        posout_0002.yaml posout_0005.yaml posout_0008.yaml
    posout_0000.yaml posout_0003.yaml posout_0006.yaml posout_0009.yaml
    posout_0001.yaml posout_0004.yaml posout_0007.yaml time-geom.yaml
    
    
    
    [12]:
    
    
    
    !cat cmd_work/data-geom/geopt.mon
    
    
    
      #-------------- Geopt file opened, name: ./data-geom/geopt.mon, timestamp: 2022-07-29 15:26:53.157
    # COUNT  IT  GEOPT_METHOD  ENERGY                 DIFF       FMAX       FNRM      FRAC*FLUC FLUC      ADD. INFO
        0     0  GEOPT_SQNM   0.00000000000000E+00   0.00E+00  6.497E-03  9.18E-03  0.00E+00  0.00E+00   beta=1.00E+00 dim=000 maxd=0.0E+00 dsplr=0.00000E+00 dsplp=0.00000E+00
        1     1  GEOPT_SQNM  -4.05551003369715E+00  -4.06E+00  1.758E-03  2.54E-03  5.45E-04  5.45E-04   beta=1.00E+00 dim=000 maxd=6.5E-03 dsplr=9.17854E-03 dsplp=9.17854E-03
        2     2  GEOPT_SQNM  -4.05551478890277E+00  -4.76E-06  6.313E-04  7.75E-04  5.42E-04  5.42E-04   beta=1.10E+00 dim=001 maxd=2.4E-03 dsplr=1.26091E-02 dsplp=1.26091E-02
        3     3  GEOPT_SQNM  -4.05552404700316E+00  -9.26E-06  5.266E-04  8.33E-04  5.05E-04  5.05E-04   beta=1.21E+00 dim=002 maxd=1.1E-02 dsplr=2.63921E-02 dsplp=2.63921E-02
        4     4  GEOPT_SQNM  -4.05552808416222E+00  -4.04E-06  7.414E-05  1.11E-04  4.20E-04  4.20E-04   beta=1.33E+00 dim=002 maxd=2.0E-02 dsplr=5.13985E-02 dsplp=5.13985E-02
        5     5  GEOPT_SQNM  -4.05553137818127E+00  -3.29E-06  8.332E-06  1.13E-05  3.48E-04  3.48E-04   beta=1.13E+00 dim=002 maxd=3.4E-03 dsplr=5.55781E-02 dsplp=5.55781E-02
        6     6  GEOPT_SQNM  -4.05553064847653E+00   7.30E-07  6.759E-06  9.24E-06  2.91E-04  2.91E-04   beta=1.24E+00 dim=002 maxd=4.0E-04 dsplr=5.60659E-02 dsplp=5.60659E-02
        7     7  GEOPT_SQNM  -4.05553065682987E+00  -8.35E-09  7.833E-06  1.01E-05  2.46E-04  2.46E-04   beta=1.06E+00 dim=002 maxd=2.7E-04 dsplr=5.63927E-02 dsplp=5.63927E-02
        8     8  GEOPT_SQNM  -4.05553138514531E+00  -7.28E-07  3.377E-06  4.35E-06  2.09E-04  2.09E-04   beta=1.16E+00 dim=002 maxd=4.0E-04 dsplr=5.68876E-02 dsplp=5.68876E-02
        9     9  GEOPT_SQNM  -4.05553138634947E+00  -1.20E-09  3.719E-06  4.61E-06  1.80E-04  1.80E-04   beta=1.00E+00 dim=002 maxd=1.2E-04 dsplr=5.70406E-02 dsplp=5.70406E-02
    SQNM converged at iteration  9. Needed bigdft calls:  9
    

## Profiles

A number of profiles are available which can be useful for more advanced calculations. For example, the `linear` profile for O(N) calculations or the `mixing` profile can be imported for difficult to converge systems.
    
    
    [13]:
    
    
    
    !cat cmd_work/*mixing*
    
    
    
    dft: {hgrids: 0.3, ixc: LDA}
    kpt:
      method: mpgrid
      ngkpt: [2, 2, 2]
    posinp:
      cell: [2.867, 2.867, 2.867]
      positions:
      - Fe: [0.0, 0.0, 0.0]
      units: angstroem
    import: "mixing"
    
    
    
    [14]:
    
    
    
    !cd cmd_work ; $BIGDFT_ROOT/bigdft -n mixing -s yes ; cd ..
    
    
    
     <BigDFT> log of the run will be written in logfile: ./log-mixing.yaml
    

Full details are available in `bigdft/src/input_variables_definition.yaml`

## PyBigDFT Compatability

All of these calculations are compatabile with the PyBigDFT approach. For example, we can build a Logfile manually:
    
    
    [15]:
    
    
    
    from BigDFT.Logfiles import Logfile
    from os.path import join
    
    log = Logfile(join("cmd_work", "log-psys.yaml"))
    print(log.energy)
    
    
    
    -20.548483769436842
    

And even get access to the system.
    
    
    [17]:
    
    
    
    from BigDFT.Systems import system_from_log
    sys = system_from_log(log)
    for fragid, frag in sys.items():
        print(fragid)
        for at in frag:
            print(at.sym, at.get_position())
    
    
    
    ATOM:0
    Fe [0.0, 0.0, 0.0]
    

[ Previous](QuickStart.html "Quick Start - From Python") [Next ](../users/guide.html "User Guide")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).