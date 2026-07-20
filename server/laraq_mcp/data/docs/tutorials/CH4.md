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
        * [Basics of BigDFT: N2 molecule as example](N2.html)
        * [Handling the log files : solution to exercise on N2 molecule](N2-solution.html)
        * Running a wavelet computation on a methane molecule
        * [Usage of Dataset class, the CO molecule as example](Datasets.html)
        * [BigDFT for solid state systems](SolidState.html)
        * [Running a wavelet computation on a methane molecule, with AiiDa](CH4_aiida.html)
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
  * Running a wavelet computation on a methane molecule
  * [ View page source](../_sources/tutorials/CH4.ipynb.txt)

* * *

# Running a wavelet computation on a methane molecule

The purpose of this lesson is to get familiar with the basic variables needed to run a wavelet computation in isolated boundary conditions. At the end of the lesson, you can run a wavelet run, check the amount of needed memory and understand the important part of the output. We propose to use python in a Jupyter notebook to simplify the use of the `bigdft` executable and to have tools to combine pre-processing, execution, post-processing and analysis.

## An initial run on the methane molecule

As already explained in the [N2 molecule tutorial](N2.html), BigDFT uses dictionaries (a collection of pairs of key and value) for the input and output which are serialized by means of the yaml format. This allows us to manipulate dictionaries instead of files and define simple actions on them for the basic code operations, instead of manually modifying the input keys.

We here introduce the `BigDFT.Inputfiles.Inpufile` class, which is a generalisation of a python dictionary and that has as class methods the _same_ methods that are available in the `BigDFT.InputActions` module.
    
    
    [1]:
    
    
    
    from BigDFT import Inputfiles as I
    
    inp = I.Inputfile()
    inp.set_hgrid(0.55)
    inp.set_rmult([3.5,9.0])
    

Beside a default input file called **input.yaml** , BigDFT requires the atomic positions for the studied system and optionaly the pseudo-potential files. For the following tutorial, a methane molecule will be used. The position file is a simple XYZ file named [CH4_posinp.xyz](CH4_posinp.xyz):
    
    
    5  angstroemd0  # methane molecule
    free
    C        0           0           0
    H       -0.63169789 -0.63169789 -0.63169789
    H       +0.63169789 +0.63169789 -0.63169789
    H       +0.63169789 -0.63169789 +0.63169789
    H       -0.63169789 +0.63169789 +0.63169789
    

We can copy this file into the default posinp file **posinp.xyz** as `cp CH4_posinp.xyz posinp.xyz` or indicate it in the `posinp` keyword of the calculator options

Running BigDFT is done using the `bigdft` executable in a standard Unix way. In this notebook, we use the SystemCalculator class:
    
    
    [2]:
    
    
    
    from BigDFT import Calculators as C
    from BigDFT.Database.Molecules import get_molecule
    
    study = C.SystemCalculator(verbose=False,skip=True,mpi_run='mpirun -np 2') #Create a calculator
    ch4 = study.run(input=inp,sys=get_molecule('CH4'),name="CH4")
    
    
    
     <BigDFT> Run already performed, found final file: forces_CH4.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.004 MB
     Walltime since initialization:  00:00:00.002190579
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_CH4.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.100 MB
     Walltime since initialization:  00:00:00.002369107
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
    

All information coming from the output file **log.yaml** can now be handled easily by _ch4_ , an instance of the Logfile class. Then we can display some information as:
    
    
    [3]:
    
    
    
    print(ch4)
    
    
    
    - Atom types:
      - C
      - H
    - cell: Free BC
    - number_of_orbitals: 4
    - posinp_file: CH4.yaml
    - XC_parameter: 1
    - grid_spacing: 0.55
    - spin_polarization: 1
    - total_magn_moment: 0
    - system_charge: 0
    - rmult:
      - 3.5
      - 9.0
    - dipole:
      - -0.004520998
      - -0.004520998
      - -0.004520998
    - energy: -8.026155368542643
    - fermi_level: -0.3425340751278
    - forcemax: 0.01861869071424
    - forcemax_cv: 0.0
    - gnrm_cv: 0.0001
    - nat: 5
    - symmetry: disabled
    - No. of KS orbitals:
      - 4
    
    

## The wavelet basis set, a convergence study

Daubechies Wavelets is a systematic basis set (as plane waves are), which means than one can increase arbitrarily the accuracy of the results by varying some parameters which are defined in the `dft` dictionary (`inp['dft']`). We here explain what are the meaning and the typical values for the principal parameters, `hgrid` and `rmult`.

![CH4-grid](../_images/CH4-grid.png)

**``hgrids``** are used to set up the basis set. In free boundary conditions, the basis set is characterised by a spatial expansion and a grid step, as shown in the side figure. There is ‘’one float value’’ describing the ‘’grid steps’’ in the three space directions (‘’i.e.’’ x, y and z) or a 3D array is also accepted. These values are in bohr unit and typically range from 0.3 to 0.65. The harder the pseudo-potential, the lower value should be set up. These values are called `hgrids` in the input dictionary, and can be set by the `set_hgrid` method of the `Inpufile` class.

**``rmult``** contains an array of two float values that are two multiplying factors. They multiply quantities that are chemical species dependent. The first factor is the most important since it describes ‘’the spatial expansion’’ of the basis set (in yellow on the figure beside). Indeed the basis set is defined as a set of real space points with non-zero values. These points are on a global regular mesh and located inside spheres centered on atoms. The first multiplying factor is called `crmult` for Coarse grid Radius MULTiplier. Increasing it means that further spatial expansion is possible for the wavefunctions. Typical values are 5 to 7. The second one called `frmult` for Fine grid Radius MULTiplier is related to the fine resolution. This parameter is less pertinent for the convergence of energy and can be ignored. It is possible to indicate only one float value, the `crmult` parameter. Such parameters can be set by the method `set_rmult` of `Inputfile` class.

### Objective

Let us run BigDFT for the following values of _hgrid_ and _crmult_ and plot the total energy convergence versus `hgrids`. The final total energy can be retrieved using the method `energy` from the result of each of the runs. The unit of the energies is in Hartree. This tutorial also explains how to use the `Dataset` class.
    
    
    [4]:
    
    
    
    hgrids = [0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2] #bohr
    crmult = [3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]
    

This precision plot shows the systematicity of the wavelet basis set: by improving the basis set, we improve the absolute value of the total energy.

Indeed, there are two kind of errors arising from the basis set. The first one is due to the fact the basis set can’t account for quickly varying wavefunctions (value of `hgrids` should be decreased). The second error is the fact that the wavefunctions are constrained to stay inside the defined basis set (output values are zero). In the last case `crmult` should be raised.

### Construction of the input dataset dictionaries

Let us build three different dataset of inputfiles, the first two varying `hgrid` and `crmult` and the last by varying the two together. We also label each of the input dictionaries by a unique name identifying the run.
    
    
    [5]:
    
    
    
    from BigDFT import Datasets as D
    from copy import deepcopy
    # study = C.SystemCalculator(verbose=False,skip=True,mpi_run='mpirun -np 2')
    pos = ch4.log['posinp']
    
    h_and_c_dataset = D.Dataset('h_and_c')
    for h,c in zip(hgrids,crmult):
        inp_run = deepcopy(inp)
        inp_run.set_hgrid(h)
        inp_run.set_rmult([c,9.0])
        h_and_c_dataset.append_run(id={'h':h,'c':c},run_dir='conv-CH4',input=inp_run,posinp=pos,runner=study)
    
    
    
    [6]:
    
    
    
    h_only_dataset = D.Dataset('h_only')
    for h in hgrids:
        inp_run = deepcopy(inp)
        inp_run.set_hgrid(h)
        h_only_dataset.append_run(id={'h':h},run_dir='conv-CH4',input=inp_run,posinp=pos,runner=study)
    
    
    
    [7]:
    
    
    
    c_only_dataset = D.Dataset('c_only')
    for c in crmult:
        inp_run = deepcopy(inp)
        inp_run.set_rmult([c,9.0])
        c_only_dataset.append_run(id={'c':c},run_dir='conv-CH4',input=inp_run,posinp=pos,runner=study)
    

We then run the three datasets:
    
    
    [23]:
    
    
    
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
         Memory Peak of process: 13.172 MB
     <BigDFT> Run already performed, found final file: forces_h__0.55.yaml
     Walltime since initialization:  00:00:00.001698076
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.988 MB
     Walltime since initialization:  00:00:00.001490718
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
         Memory Peak of process: 12.992 MB
     Walltime since initialization:  00:00:00.001515348
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
         Memory Peak of process: 13.064 MB
     Walltime since initialization:  00:00:00.001507999
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
         Memory Peak of process: 12.996 MB
     Walltime since initialization:  00:00:00.001682716
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
         Memory Peak of process: 13.084 MB
     Walltime since initialization:  00:00:00.001619002
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.4.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
     <BigDFT> Run already performed, found final file: forces_h__0.4.yaml
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.248 MB
     Walltime since initialization:  00:00:00.001527633
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.156 MB
     Walltime since initialization:  00:00:00.001563816
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
         Memory Peak of process: 13.240 MB
     Walltime since initialization:  00:00:00.001326137
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
         Memory Peak of process: 12.996 MB
     Walltime since initialization:  00:00:00.001441626
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
         Memory Peak of process: 13.184 MB
     <BigDFT> Run already performed, found final file: forces_h__0.3.yaml
     Walltime since initialization:  00:00:00.001690333
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.248 MB
     Walltime since initialization:  00:00:00.001546023
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.25.yaml
     <BigDFT> Run already performed, found final file: forces_h__0.25.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.176 MB
     Walltime since initialization:  00:00:00.002103872
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.184 MB
     Walltime since initialization:  00:00:00.001524949
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_h__0.2.yaml
     <BigDFT> Run already performed, found final file: forces_h__0.2.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
     Memory Consumption Report:
       Remaining Memory (B):  0
       Memory occupation:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.996 MB
         for the array: null
         in the routine: null
         Memory Peak of process: 13.200 MB
     Walltime since initialization:  00:00:00.001664154
     Max No. of dictionaries used:  1127 Walltime since initialization:  00:00:00.001912211
     #( 1052 still in use)
     Number of dictionary folders allocated:  1
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
         Memory Peak of process: 13.256 MB
     Walltime since initialization:  00:00:00.001981150
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
         Memory Peak of process: 13.016 MB
     Walltime since initialization:  00:00:00.002668089
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__4.0.yaml
     <BigDFT> Run already performed, found final file: forces_c__4.0.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.244 MB
     Walltime since initialization:  00:00:00.001412816
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.188 MB
     Walltime since initialization:  00:00:00.001349545
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__4.5.yaml
     <BigDFT> Run already performed, found final file: forces_c__4.5.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.120 MB
     Walltime since initialization:  00:00:00.001477466
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.068 MB
     Walltime since initialization:  00:00:00.001418465
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__5.0.yaml
     <BigDFT> Run already performed, found final file: forces_c__5.0.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.068 MB
     Walltime since initialization:  00:00:00.001418233
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.184 MB
     Walltime since initialization:  00:00:00.001589820
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
         Memory Peak of process: 13.172 MB
     Walltime since initialization:  00:00:00.001658198
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
         Memory Peak of process: 13.004 MB
     Walltime since initialization:  00:00:00.001729590
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
         Memory Peak of process: 13.020 MB
     Walltime since initialization:  00:00:00.001622083
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
         Memory Peak of process: 13.232 MB
     Walltime since initialization:  00:00:00.002389479
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
         Memory Peak of process: 13.092 MB
     Walltime since initialization:  00:00:00.001614621
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
         Memory Peak of process: 12.908 MB
     Walltime since initialization:  00:00:00.002074298
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
         Memory Peak of process: 12.932 MB
     Walltime since initialization:  00:00:00.001451341
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
         Memory Peak of process: 13.260 MB
     Walltime since initialization:  00:00:00.001538055
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
         Memory Peak of process: 13.204 MB
     Walltime since initialization:  00:00:00.001743304
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
         Memory Peak of process: 13.124 MB
     Walltime since initialization:  00:00:00.001281943
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
         Memory Peak of process: 13.156 MB
     Walltime since initialization:  00:00:00.001476633
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
         Memory Peak of process: 13.036 MB
     Walltime since initialization:  00:00:00.001665277
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
         Memory Peak of process: 13.248 MB
     Walltime since initialization:  00:00:00.001468183
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
         Memory Peak of process: 13.028 MB
     Walltime since initialization:  00:00:00.001519230
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
         Memory Peak of process: 13.204 MB
     Walltime since initialization:  00:00:00.002425679
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
         Memory Peak of process: 13.112 MB
     Walltime since initialization:  00:00:00.002324924
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__5.5,h__0.35.yaml
     <BigDFT> Run already performed, found final file: forces_c__5.5,h__0.35.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.092 MB
     Walltime since initialization:  00:00:00.001443078
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.032 MB
     Walltime since initialization:  00:00:00.001495005
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
         Memory Peak of process: 12.984 MB
     Walltime since initialization:  00:00:00.001357514
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
         Memory Peak of process: 13.012 MB
     Walltime since initialization:  00:00:00.001379205
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
         Memory Peak of process: 13.000 MB
     Walltime since initialization:  00:00:00.001506376
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
         Memory Peak of process: 13.244 MB
     Walltime since initialization:  00:00:00.001675729
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_c__7.0,h__0.2.yaml
     <BigDFT> Run already performed, found final file: forces_c__7.0,h__0.2.yaml
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.952 MB
     Walltime since initialization:  00:00:00.001755290
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.196 MB
     Walltime since initialization:  00:00:00.001649410
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
    

### Handling the dataset dictionaries

We now store the energies of each of the dataset runs, and identify the minimum as the minimum value from the `h_and_c` dataset:
    
    
    [9]:
    
    
    
    from numpy import array as arr
    
    energies_h = arr(h_only_dataset.fetch_results(attribute='energy'))
    energies_c = arr(c_only_dataset.fetch_results(attribute='energy'))
    energies_hc = arr(h_and_c_dataset.fetch_results(attribute='energy'))
    #find the minimum
    emin = min(energies_hc)
    

We plot the energy values varying the grid spacing or the extension
    
    
    [10]:
    
    
    
    import matplotlib.pyplot as plt
    %matplotlib inline
    
    plt.xlabel('Grid step (Bohr)')
    plt.plot(hgrids,energies_h-emin,label='crmult=3.5')
    plt.plot(hgrids,energies_hc-emin,label='varying hgrids+crmult')
    plt.yscale('log')
    plt.legend(loc='best')
    
    
    
    [10]:
    
    
    
    <matplotlib.legend.Legend at 0x7f1a5f3d4bd0>
    

![../_images/tutorials_CH4_21_1.png](../_images/tutorials_CH4_21_1.png)
    
    
    [11]:
    
    
    
    plt.xlabel('Crmult value')
    plt.plot(crmult,energies_c-emin,label='hgrid=0.55')
    plt.plot(crmult,energies_hc-emin,label='varying hgrids+crmult')
    plt.yscale('log')
    plt.legend(loc='best')
    
    
    
    [11]:
    
    
    
    <matplotlib.legend.Legend at 0x7f1a5700bf10>
    

![../_images/tutorials_CH4_22_1.png](../_images/tutorials_CH4_22_1.png)

### Considerations

We see that _both_ the parameters `hgrids` and `rmult` have to be decreased and increased (respectively) in order to achieve convergence. Increasing only one of the two parameter will eventually lead to saturation of the absolute error on the energy.

For a more detailed description of `Dataset`, go to this [tutorial](Datasets.html)

## Fine tuning of the basis set

The multi-scale property of the wavelets is used in BigDFT and a two level grid is used for the calculation. We’ve seen previously the coarse grid definition using the the multiplying factor `rmult`. The second multiplying value on this line of the input file is used for the fine grid and is called `frmult`. Like `crmult`, it defines a factor for the radii used to define the fine grid region where the number of degrees of freedom is indeed eight times the one of the coarse grid. It allows to define region near the atoms where the wavefunctions are allowed to vary more quickly. Typical values for this factor are 8 to 10. It’s worth to note that even if the value of the multiplier is greater than `crmult` it defines a smaller region due to the fact that the units which are associated to these radii are significantly different.

The physical quantities used by `crmult` and `frmult` can be changed in the pseudo-potential by adding an additional line with two values in bohr. The two values that the code is using (either computed or read from the pseudo-potential files) are output in the following way in the screen output:
    
    
     - Symbol                              : C #Type No.  01
       No. of Electrons                    :  4
       No. of Atoms                        :  1
       Radii of active regions (AU):
         Coarse                            :  1.58437
         Fine                              :  0.30452
         Coarse PSP                        :  1.30510
         Source                            : Hard-Coded
     - Symbol                              : H #Type No.  02
       No. of Electrons                    :  1
       No. of Atoms                        :  4
       Radii of active regions (AU):
         Coarse                            :  1.46342
         Fine                              :  0.20000
         Coarse PSP                        :  0.00000
         Source                            : Hard-Coded

## Analysing the output

The output of BigDFT is divided into four parts:

  * Input values are printed out, including a summary of the different input files (DFT calculation parameters, atom positions, pseudo-potential values…);

  * Input wavefunction creation, usually called “input guess”;

  * The SCF (Self-Consistent Field) loop itself;

  * The post SCF calculations including the forces calculation and other possible treatment like a finite size effect estimation or a virtual states determination.

### The system parameters output

All the read values from the different input files are printed out at the program startup. Some additional values are provided there also, like the memory consumption. Values are given for one process, which corresponds to one core in an MPI environment.
    
    
    [12]:
    
    
    
    print('Memory',ch4.memory)
    print('Estimated Memory Peak',ch4.memory_peak,'MB')
    
    
    
    Memory {'Accumulated memory requirements during principal run stages (MiB.KiB)': {'Kernel calculation': 39.271, 'Density Construction': 23.692, 'Poisson Solver': 36.173, 'Hamiltonian application': 23.891, 'Orbitals Orthonormalization': 23.891}, 'Memory requirements for principal quantities (MiB.KiB)': {'Subspace Matrix': 0.1, 'Single orbital': 0.94, 'All (distributed) orbitals': 0.745, 'Wavefunction storage size': 5.92, 'Nonlocal Pseudopotential Arrays': 0.46, 'Full Uncompressed (ISF) grid': 3.224, 'Workspaces storage size': 0.211}, 'Estimated Memory Peak (MB)': 39}
    Estimated Memory Peak 39 MB
    

The overall memory requirement needed for this calculation is thus: 39 MB (Estimated Memory Peak) which is provided by the`memory_peak` attribute.

In this example, the memory requirement is given for one process run and the peak of memory will be in the initialisation during the Kernel calculation, while the SCF loop will reach 36MB during the Poisson solver calculation. For bigger systems, with more orbitals, the peak of memory is usually reached during the Hamiltonian application.

### Exercise

Run a script to estimate the memory requirement of a run before submitting it to the queue system of a super-computer using the `dry_run` option.

It reads the same input, and is thus convenient to validate inputs.

Try several values from 1 to 6 and discuss the memory distribution.

### Solution
    
    
    [13]:
    
    
    
    study = C.SystemCalculator(dry_run=True,verbose=False) #Create a calculator
    peak = []
    for i in range(1,7):
        dry = study.run(input=inp,sys=get_molecule('CH4'),dry_mpi=i,name="CH4_mem")
        # p = dry.memory_peak
        print(dry.memory,'\n')
    # for i,p in enumerate(peak):
    #     print("mpi=",i+1,"Estimated memory peak (MB)",p)
    
    
    
     <BigDFT> log of the run will be written in logfile: ./log-CH4_mem.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-CH4_mem.23:08:46.800.yaml
    {'Accumulated memory requirements during principal run stages (MiB.KiB)': {'Kernel calculation': 39.271, 'Density Construction': 23.692, 'Poisson Solver': 36.173, 'Hamiltonian application': 23.891, 'Orbitals Orthonormalization': 23.891}, 'Memory requirements for principal quantities (MiB.KiB)': {'Subspace Matrix': 0.1, 'Single orbital': 0.94, 'All (distributed) orbitals': 0.745, 'Wavefunction storage size': 5.92, 'Nonlocal Pseudopotential Arrays': 0.46, 'Full Uncompressed (ISF) grid': 3.224, 'Workspaces storage size': 0.211}, 'Estimated Memory Peak (MB)': 39}
    
     <BigDFT> log of the run will be written in logfile: ./log-CH4_mem.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-CH4_mem.23:08:47.009.yaml
    {'Accumulated memory requirements during principal run stages (MiB.KiB)': {'Kernel calculation': 39.271, 'Density Construction': 23.692, 'Poisson Solver': 36.173, 'Hamiltonian application': 23.891, 'Orbitals Orthonormalization': 23.891}, 'Memory requirements for principal quantities (MiB.KiB)': {'Subspace Matrix': 0.1, 'Single orbital': 0.94, 'All (distributed) orbitals': 0.745, 'Wavefunction storage size': 5.92, 'Nonlocal Pseudopotential Arrays': 0.46, 'Full Uncompressed (ISF) grid': 3.224, 'Workspaces storage size': 0.211}, 'Estimated Memory Peak (MB)': 39}
    
     <BigDFT> log of the run will be written in logfile: ./log-CH4_mem.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-CH4_mem.23:08:47.206.yaml
    {'Accumulated memory requirements during principal run stages (MiB.KiB)': {'Kernel calculation': 39.271, 'Density Construction': 23.692, 'Poisson Solver': 36.173, 'Hamiltonian application': 23.891, 'Orbitals Orthonormalization': 23.891}, 'Memory requirements for principal quantities (MiB.KiB)': {'Subspace Matrix': 0.1, 'Single orbital': 0.94, 'All (distributed) orbitals': 0.745, 'Wavefunction storage size': 5.92, 'Nonlocal Pseudopotential Arrays': 0.46, 'Full Uncompressed (ISF) grid': 3.224, 'Workspaces storage size': 0.211}, 'Estimated Memory Peak (MB)': 39}
    
     <BigDFT> log of the run will be written in logfile: ./log-CH4_mem.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-CH4_mem.23:08:47.402.yaml
    {'Accumulated memory requirements during principal run stages (MiB.KiB)': {'Kernel calculation': 39.271, 'Density Construction': 23.692, 'Poisson Solver': 36.173, 'Hamiltonian application': 23.891, 'Orbitals Orthonormalization': 23.891}, 'Memory requirements for principal quantities (MiB.KiB)': {'Subspace Matrix': 0.1, 'Single orbital': 0.94, 'All (distributed) orbitals': 0.745, 'Wavefunction storage size': 5.92, 'Nonlocal Pseudopotential Arrays': 0.46, 'Full Uncompressed (ISF) grid': 3.224, 'Workspaces storage size': 0.211}, 'Estimated Memory Peak (MB)': 39}
    
     <BigDFT> log of the run will be written in logfile: ./log-CH4_mem.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-CH4_mem.23:08:47.586.yaml
    {'Accumulated memory requirements during principal run stages (MiB.KiB)': {'Kernel calculation': 39.271, 'Density Construction': 23.692, 'Poisson Solver': 36.173, 'Hamiltonian application': 23.891, 'Orbitals Orthonormalization': 23.891}, 'Memory requirements for principal quantities (MiB.KiB)': {'Subspace Matrix': 0.1, 'Single orbital': 0.94, 'All (distributed) orbitals': 0.745, 'Wavefunction storage size': 5.92, 'Nonlocal Pseudopotential Arrays': 0.46, 'Full Uncompressed (ISF) grid': 3.224, 'Workspaces storage size': 0.211}, 'Estimated Memory Peak (MB)': 39}
    
     <BigDFT> log of the run will be written in logfile: ./log-CH4_mem.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-CH4_mem.23:08:47.768.yaml
    {'Accumulated memory requirements during principal run stages (MiB.KiB)': {'Kernel calculation': 39.271, 'Density Construction': 23.692, 'Poisson Solver': 36.173, 'Hamiltonian application': 23.891, 'Orbitals Orthonormalization': 23.891}, 'Memory requirements for principal quantities (MiB.KiB)': {'Subspace Matrix': 0.1, 'Single orbital': 0.94, 'All (distributed) orbitals': 0.745, 'Wavefunction storage size': 5.92, 'Nonlocal Pseudopotential Arrays': 0.46, 'Full Uncompressed (ISF) grid': 3.224, 'Workspaces storage size': 0.211}, 'Estimated Memory Peak (MB)': 39}
    
    

BigDFT distributes the orbitals over the available processes. The value `All (distributed) orbitals` does not decrease anymore after 4 processes since there are only 4 bands in our example). This means that running a parallel job with more processors than orbitals will result in a bad speedup. The number of cores involved in the calculation might be however increased via OMP parallelisation.

### The input guess

The initial wavefunctions in BigDFT are calculated using the atomic orbitals for all the electrons of the \\(s\\), \\(p\\), \\(d\\) shells, obtained from the solution of the PSP self-consistent equation for the isolated atom.
    
    
    [14]:
    
    
    
    ch4.log['Input Hamiltonian']
    
    
    
    [14]:
    
    
    
    {'Policy': 'Wavefunctions from PSP Atomic Orbitals',
     'Total No. of Atomic Input Orbitals': 8,
     'Atomic Input Orbital Generation': [{'Atom Type': 'C',
       'Electronic configuration': {'s': [2.0], 'p': ['2/3', '2/3', '2/3']}},
      {'Atom Type': 'H', 'Electronic configuration': {'s': [1.0]}}],
     'Wavelet conversion succeeded': True,
     'Deviation from normalization': 0.000301,
     'GPU acceleration': False,
     'Total electronic charge': 7.999998896328,
     'Poisson Solver': {'BC': 'Free', 'Box': [75, 75, 75], 'MPI tasks': 1},
     'Expected kinetic energy': 7.2067994418,
     'Energies': {'Ekin': 7.2112355851,
      'Epot': -10.6242728776,
      'Enl': 0.77958992358,
      'EH': 15.0808904199,
      'EXC': -3.15395493145,
      'EvXC': -4.12420760879},
     'EKS': -7.166513305115721,
     'Input Guess Overlap Matrices': {'Calculated': True, 'Diagonalized': True},
     'Orbitals': [{'e': -0.6524376770958, 'f': 2.0},
      {'e': -0.3649369847215, 'f': 2.0},
      {'e': -0.3649369847215, 'f': 2.0},
      {'e': -0.3648107610829, 'f': 2.0},
      {'e': 0.4030001433315, 'f': 0.0},
      {'e': 0.4030001433315, 'f': 0.0},
      {'e': 0.403297797035, 'f': 0.0},
      {'e': 0.6121760122025, 'f': 0.0}],
     'IG wavefunctions defined': True,
     'Accuracy estimation for this run': {'Energy': 0.00444,
      'Convergence Criterion': 0.00111}}
    

The corresponding hamiltonian is then diagonalised and the n_band (`norb` in the code notations) lower eigenfunctions are used to start the SCF loop. BigDFT outputs the eigenvalues, in the following example, 8 electrons were used in the input guess and the resulting first fourth eigenfunctions will be used for a four band calculation.
    
    
    Input Guess Overlap Matrices: {Calculated: true, Diagonalized: true}
    Orbitals:
    - {e: -0.6493539153869, f: 2.0}
    - {e: -0.3625626366055, f: 2.0}
    - {e: -0.3624675839372, f: 2.0}
    - {e: -0.3624675839372, f: 2.0} -- Last InputGuess eval, H-L IG gap:  20.6959 eV
    - {e: 0.3980916655348, f: 0.0}  -- First virtual eval
    - {e: 0.3983087771728, f: 0.0}
    - {e: 0.3983087771728, f: 0.0}
    - {e: 0.5993393223683, f: 0.0}
    

### The SCF loop

The SCF loop follows a direct minimisation scheme and is made of the following steps:

  * Calculate the charge density from the previous wavefunctions.

  * Apply the Poisson solver to obtain the Hartree potential from the charges and calculate the exchange-correlation energy and the energy of the XC potential thanks to the chosen functional.

  * Apply the resulting hamiltonian on the current wavefunctions.

  * Precondition the result and apply a steepest descent or a DIIS history method. This depends on `idsx`, not specified in the present input. It is therefore set to the default value, which is 6 (for an history of 6 previous set of vectors. To perform a SD minimisation one should add “`idsx: 0`” to the _dft_ dictionary of _inp_.

  * Orthogonalise the new wavefunctions.

Finally the total energy and the square norm of the residue (gnrm) are printed out. The _gnrm_ value is the stopping criterion. It can be chosen using `gnrm_cv` in the _dft_ dictionary. The default value (1e-4) is used here and a good value can reach 1e-5.
    
    
    [15]:
    
    
    
    print('gnrm_cv by default',ch4.gnrm_cv)
    
    
    
    gnrm_cv by default 0.0001
    

The minimisation scheme coupled with DIIS (and thanks to the good preconditioner) is a very efficient way to obtain convergence for systems with a gap, even with a very small one. Usual run should reach the 1e-4 stop criterion within 15 to 25 iterations. Otherwise, there is an issue with the system, either there is no gap, or the input guess is too symmetric due to the LCAO diagonalization, specific spin polarization…
    
    
    [16]:
    
    
    
    ch4.wfn_plot()
    

![../_images/tutorials_CH4_35_0.png](../_images/tutorials_CH4_35_0.png)

### The post-SCF treatments

At the end of the SCF loop, a diagonalisation of the current hamiltonian is done to obtain Kohn-Sham eigenfunctions. The corresponding eigenvalues are also given.
    
    
    [17]:
    
    
    
    ch4.evals
    
    
    
    [17]:
    
    
    
    [BandArray([[-0.61846333, -0.34256806, -0.34256806, -0.34253408]])]
    

The forces are then calculated.
    
    
    [18]:
    
    
    
    ch4.log['Atomic Forces (Ha/Bohr)']
    
    
    
    [18]:
    
    
    
    [{'C': [7.641720525072e-06, 7.64172052622e-06, 7.641720553674e-06]},
     {'H': [-0.01069867591423, -0.01069867591424, -0.01069867591424]},
     {'H': [-0.01077871224919, 0.01073487322146, 0.01073487322145]},
     {'H': [0.01073487322145, -0.0107787122492, 0.01073487322145]},
     {'H': [0.01073487322145, 0.01073487322145, -0.01077871224921]}]
    

Some other post-SCF may be done depending on the parameters in the _dft_ dictionary of _inp_.

### Exercise

Run `bigdft` when varying the DIIS history length and discuss the memory consumption.

Reducing the DIIS history is a good way to reduce the memory consumption when one cannot increase the number of processes. Of course this implies more iterations in SCF loops.

## Adding a charge

BigDFT can treat charged system without the requirement to add a compensating background like in plane waves. The additional charge to add to the system is set in the _dft_ dictionary with the _qcharge_ key.

### Exercise

Remove the last hydrogen atom in the previous methane example and modify to add an electron. Then run BigDFT for an electronic convergence.

### Solution
    
    
    [19]:
    
    
    
    inp3 = I.Inputfile()
    inp3['dft'] = {'hgrids': 0.55, 'nrepmax': 'accurate', 'qcharge': -1.0}
    inp3['posinp'] = 'CH3-_posinp.xyz'
    
    study = C.SystemCalculator(verbose=False,skip=True,mpi_run='mpirun -np 2')
    ch3m = study.run(input=inp3,name="CH3m")
    
    
    
     <BigDFT> log of the run will be written in logfile: ./log-CH3m.yaml
     <BigDFT> log of the run will be written in logfile: ./log-CH3m.yaml
     <BigDFT> Logfile existing, renamed into: ./logfiles/log-CH3m.23:08:48.373.yaml
    

One can notice that the total charge in the system is indeed -8 thanks to the additional charge. The convergence rate is still good for this CH\\(_3^-\\) radical since it is a closed shell system.
    
    
    [20]:
    
    
    
    print(ch3m)
    ch3m.wfn_plot()
    
    
    
    - Atom types:
      - C
      - H
    - cell: Free BC
    - number_of_orbitals: 4
    - posinp_file: CH3-_posinp.xyz
    - XC_parameter: 1
    - grid_spacing: 0.55
    - spin_polarization: 1
    - total_magn_moment: 0
    - system_charge: -1.0
    - rmult:
      - 5.0
      - 8.0
    - dipole:
      - 0.326025
      - -0.3399956
      - -0.3399956
    - energy: -7.361791816825809
    - fermi_level: 0.1058352419843
    - forcemax: 0.01214557146397
    - forcemax_cv: 0.0
    - gnrm_cv: 0.0001
    - nat: 4
    - symmetry: disabled
    - No. of KS orbitals:
      - 4
    
    

![../_images/tutorials_CH4_44_1.png](../_images/tutorials_CH4_44_1.png)

## Running a geometry optimisation

In the previous charged example the geometry of the radical is kept the same than for the methane molecule, while it is likely to change. One can thus optimize the geometry with BigDFT.

To run geometry calculations (molecular dynamics, structure optimisations…) one should add another dictionary _geopt_ in the input which contains the method to use.

In the log file, all input variables are indicated with their default value.

Here, we look for a local minimum so we can use the keyword `LBFGS`. We can add also the stopping criteria. There are two stopping criteria: the first `ncount_cluster_x` being the number of loops (force evaluations) and the second `forcemax` is the maximum on forces. For isolated systems, the first criterion is well adapted while the second is good for periodic boundary conditions.

### Exercise

Take the CH\\(_3^-\\) radical [**CH3-_posinp.xyz**](./CH3-_posinp.xyz) file and run a geometry optimisation.

### Solution
    
    
    [21]:
    
    
    
    inpg = I.Inputfile()
    inpg['dft'] = {'hgrids': 0.55, 'nrepmax': 'accurate'}
    inpg['posinp'] = 'CH4_posinp.xyz'
    inpg['geopt'] = {'method': 'LBFGS', 'ncount_cluster_x': 20}
    
    study = C.SystemCalculator(verbose=False,skip=True) #Use a new calculator)
    ch4geopt = study.run(input=inpg,name="CH3m_geopt")
    
    
    
     <BigDFT> Run already performed, found final file: final_CH3m_geopt.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.948 MB
     Walltime since initialization:  00:00:00.001950643
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
    Found 19 different runs
    

The evolution of the forces during relaxation can be easily obtained using the `geop_plot` function to the result of the calculation.

At each iteration, BigDFT outputs a file **posout_XXXX.xyz** in the directory **data** with the geometry of the iteration

  30. 

    
    
    [22]:
    
    
    
    %matplotlib inline
    ch4geopt.geopt_plot();
    

![../_images/tutorials_CH4_49_0.png](../_images/tutorials_CH4_49_0.png)

[ Previous](N2-solution.html "Handling the log files : solution to exercise on N2 molecule") [Next ](Datasets.html "Usage of Dataset class, the CO molecule as example")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).