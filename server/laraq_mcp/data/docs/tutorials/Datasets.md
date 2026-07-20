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
        * [Running a wavelet computation on a methane molecule](CH4.html)
        * Usage of Dataset class, the CO molecule as example
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
  * Usage of Dataset class, the CO molecule as example
  * [ View page source](../_sources/tutorials/Datasets.ipynb.txt)

* * *

# Usage of Dataset class, the CO molecule as example

In this tutorial, the basics of the `Dataset` class are briefly reviewed in a convergence study of the CO molecule, before presenting an example of application where the polarizability tensor \\(\alpha\\) is computed. It is advised to have done the [tutorial](CH4.html) on the methane molecule before in order to be familiar with the fundamentals of `Dataset` calculations.
    
    
    [145]:
    
    
    
    from BigDFT import Datasets as D
    from BigDFT import Calculators as C
    from BigDFT import Inputfiles as I
    import numpy as np
    import matplotlib.pyplot as plt
    

## Convergence of the ground state of the CO molecule

In this example, the convergence analysis of the Ground State (GS) energy of the CO molecule is performed with respect to the size of the simulation domain.

First, we instantiate both the calculator and the Dataset objects.
    
    
    [146]:
    
    
    
    calc = C.SystemCalculator(omp=2,mpi_run='mpirun -np 4',skip=True,verbose=False)
    study = D.Dataset(label='CO',run_dir='conv-CO',posinp='CO_posinp.xyz',molecule_shape='linear')
    

The object `study` is characterized by its label ‘CO_GS’ and contains the path `run_dir` in which all the calculations of the dataset will be performed. The variable `molecule_shape` has been introduced to show how further information can be passed to the dataset instances. For reminder, global options can be extracted as follows
    
    
    [147]:
    
    
    
    print(study.global_options())
    
    
    
    {'label': 'CO', 'run_dir': 'conv-CO', 'posinp': 'CO_posinp.xyz', 'molecule_shape': 'linear'}
    

Next, the input file is created while essential computational parameters are provided.
    
    
    [148]:
    
    
    
    # Define the default parameters of the input file
    inp = I.Inputfile()
    inp.set_hgrid(0.37)
    inp.set_scf_convergence(gnrm=1.0e-5)
    

The convergence analysis will be performed on the values of rmult.

We prepare the study for the convergence analysis by appending the run associated to the values of rmult. Each run is characterized by an `id` and contains the `InputFile` object as input as well as the runner used to perform the calculation. If the same `id` is provided more than once, the function gives a `Value Error`.
    
    
    [149]:
    
    
    
    rmult = [5.0,6.0,7.0,8.0]
    
    for r in rmult:
        inp.set_rmult(coarse=r,fine=9.0)
        study.append_run(id={'rmult':r},runner=calc,input=inp)
    

The following member of the `Dataset` class shows how to refer to the various calculation of `study`.
    
    
    [150]:
    
    
    
    print(study.calculators)
    print(study.ids)
    
    
    
    [{'calc': <BigDFT.Calculators.SystemCalculator object at 0x7fab00f522d0>, 'runs': [0, 1, 2, 3]}]
    [{'rmult': 5.0}, {'rmult': 6.0}, {'rmult': 7.0}, {'rmult': 8.0}]
    

A particular instance is accessed by
    
    
    [151]:
    
    
    
    print(study.ids[2])
    print(study.runs[2])
    
    
    
    {'rmult': 7.0}
    {'label': 'CO', 'run_dir': 'conv-CO', 'posinp': 'CO_posinp.xyz', 'molecule_shape': 'linear', 'input': {'dft': {'hgrids': 0.37, 'gnrm_cv': 1e-05, 'rmult': [7.0, 9.0]}, 'lin_general': {'rpnrm_cv': 'default'}, 'mix': {'rpnrm_cv': 'default'}}}
    

`study.names` contains a list of strings with the ids of the run. May be useful for labelling.
    
    
    [152]:
    
    
    
    study.names
    
    
    
    [152]:
    
    
    
    ['rmult__5.0', 'rmult__6.0', 'rmult__7.0', 'rmult__8.0']
    

The appended simulation can be executed with the run method. The `skip=True` in the runner instance guarantees that computation already performed are not executed again.
    
    
    [153]:
    
    
    
    study.run()
    
    
    
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.240 MB
     Walltime since initialization:  00:00:00.002416237
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
         Memory Peak of process: 13.172 MB
     Walltime since initialization:  00:00:00.002035260
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.984 MB
     Walltime since initialization:  00:00:00.002722207
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.168 MB
     Walltime since initialization:  00:00:00.001309965
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.948 MB
     Walltime since initialization:  00:00:00.001916676
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.044 MB
     Walltime since initialization:  00:00:00.003671661
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
         Memory Peak of process: 12.996 MB
     Walltime since initialization:  00:00:00.003537731
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.852 MB
     Walltime since initialization:  00:00:00.002670475
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.964 MB
     Walltime since initialization:  00:00:00.003039964
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.920 MB
     Walltime since initialization:  00:00:00.002309739
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.944 MB
     Walltime since initialization:  00:00:00.002341033
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.036 MB
     Walltime since initialization:  00:00:00.001929867
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.040 MB
     Walltime since initialization:  00:00:00.002977071
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.096 MB
     Walltime since initialization:  00:00:00.003468013
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.164 MB
     Walltime since initialization:  00:00:00.002740734
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.064 MB
     Walltime since initialization:  00:00:00.002684471
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
    
    
    
    [153]:
    
    
    
    {0: <BigDFT.Logfiles.Logfile at 0x7fab096d15d0>,
     1: <BigDFT.Logfiles.Logfile at 0x7fab00f01e10>,
     2: <BigDFT.Logfiles.Logfile at 0x7fab0946c290>,
     3: <BigDFT.Logfiles.Logfile at 0x7fab00ec2fd0>}
    

### Analyzing the dataset output

The class member `study.results` contains a dictionary with the logfiles of the computations performed by the run method, returned in the order of which the `append_run` was performed.
    
    
    [154]:
    
    
    
    results = study.results
    

Several operation can be performed on the results by using the methods of the `Logfile` class.

For example, the total energy w.r.t. the domain size is obtained as
    
    
    [155]:
    
    
    
    for ci in study.calculators[0]['runs']:
        print(study.ids[ci]['rmult'],results[ci].energy,study.names[ci])
        plt.scatter(study.ids[ci]['rmult'],results[ci].energy,label=study.names[ci])
    plt.legend()
    plt.title('Energy',size=12)
    plt.ylim(-21.661,-21.662)
    plt.show()
    
    
    
    5.0 -21.661153985020135 rmult__5.0
    6.0 -21.66134584205134 rmult__6.0
    7.0 -21.6613579335895 rmult__7.0
    8.0 -21.661359464443258 rmult__8.0
    

![../_images/tutorials_Datasets_22_1.png](../_images/tutorials_Datasets_22_1.png)

Other useful quantities can be extract using the methods of the `Logfile` class, for instance
    
    
    [156]:
    
    
    
    print(results[0].dipole)
    print(results[0].evals[0][0])
    print(results[0].log['dft']['rmult'])
    print(results[0].log['Electric Dipole Moment (AU)'])
    
    
    
    [-0.0002296574, -0.0002296574, 0.09288163]
    [-1.07897861 -0.5212773  -0.44461433 -0.44461428 -0.33423529]
    [5.0, 9.0]
    {'P vector': [-0.0002296574, -0.0002296574, 0.09288163], 'norm(P)': 0.0928822004}
    
    
    
    [157]:
    
    
    
    dos = results[0].get_dos(label=study.names[0])
    dos.append_from_bandarray(results[2].evals,label=study.names[2])
    dos.plot(sigma=0.2)
    
    
    
    [157]:
    
    
    
    <AxesSubplot:xlabel='Energy [eV]', ylabel='DoS'>
    

![../_images/tutorials_Datasets_25_1.png](../_images/tutorials_Datasets_25_1.png)

Alternatively, results associated to specific id and/or attribute can be extracted as follows:
    
    
    [158]:
    
    
    
    study.fetch_results()
    
    
    
    [158]:
    
    
    
    [<BigDFT.Logfiles.Logfile at 0x7fab096d15d0>,
     <BigDFT.Logfiles.Logfile at 0x7fab00f01e10>,
     <BigDFT.Logfiles.Logfile at 0x7fab0946c290>,
     <BigDFT.Logfiles.Logfile at 0x7fab00ec2fd0>]
    

If an attribute and/or an id is provided, `fetch_results` extracts only the wanted results, for instance
    
    
    [159]:
    
    
    
    print(study.fetch_results(attribute='energy'))
    print(study.fetch_results({'rmult': 8.0},attribute='energy'))
    
    
    
    [-21.661153985020135, -21.66134584205134, -21.6613579335895, -21.661359464443258]
    [-21.661359464443258]
    

### Post processing analysis

It is also possible to define a post-processing function that is passed to the `Dataset` instance. This function is called after the run and the output of `study.run` and contains the output of the post-processing function. We show some examples.

  1. Extraction of the ground state dipole

    
    
    [160]:
    
    
    
    def get_dipole(dataset):
        dipole = dataset.fetch_results(attribute='dipole')
        return dipole
    
    study.set_postprocessing_function(get_dipole)
    
    
    
    [161]:
    
    
    
    dipole_GS = study.run();
    
    
    
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.188 MB
     Walltime since initialization:  00:00:00.002320176
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
         Memory Peak of process: 13.116 MB
     Walltime since initialization:  00:00:00.001857607
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.880 MB
     Walltime since initialization:  00:00:00.002457699
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.920 MB
     Walltime since initialization:  00:00:00.001436096
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.136 MB
     Walltime since initialization:  00:00:00.001975332
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.192 MB
     Walltime since initialization:  00:00:00.002590704
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
         Memory Peak of process: 13.024 MB
     Walltime since initialization:  00:00:00.004530220
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.972 MB
     Walltime since initialization:  00:00:00.001923389
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.976 MB
     Walltime since initialization:  00:00:00.003120294
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
         Memory Peak of process: 12.968 MB
     Walltime since initialization:  00:00:00.003271214
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.192 MB
     Walltime since initialization:  00:00:00.003475566
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.140 MB
     Walltime since initialization:  00:00:00.001982148
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.068 MB
     Walltime since initialization:  00:00:00.003002721
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.948 MB
     Walltime since initialization:  00:00:00.002069531
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.040 MB
     Walltime since initialization:  00:00:00.002824836
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.864 MB
     Walltime since initialization:  00:00:00.002868074
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
    
    
    
    [162]:
    
    
    
    dipole_GS
    
    
    
    [162]:
    
    
    
    [[-0.0002296574, -0.0002296574, 0.09288163],
     [-3.391146e-05, -3.391146e-05, 0.09150228],
     [-2.716707e-06, -2.716707e-06, 0.09138863],
     [-1.027985e-05, -1.027985e-05, 0.09137423]]
    

  2. Extraction of the box size

    
    
    [163]:
    
    
    
    def get_size(dataset): # how to do def get_size(study,unit)
        sizes = []
        results = dataset.fetch_results()
        for calc,res in enumerate(results):
            sizes.append(res.log['Sizes of the simulation domain']['AU'])
        return sizes
    
    study.set_postprocessing_function(get_size)
    
    
    
    [164]:
    
    
    
    boxsize = study.run();
    
    
    
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.096 MB
     Walltime since initialization:  00:00:00.001892042
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.912 MB
     Walltime since initialization:  00:00:00.002937710
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.148 MB
     Walltime since initialization:  00:00:00.002323018
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__5.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.040 MB
     Walltime since initialization:  00:00:00.002103268
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     Memory Consumption Report:
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
       Tot. No. of Deallocations:  0
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.132 MB
       Remaining Memory (B):  0
       Memory occupation:
     Walltime since initialization:  00:00:00.001781993
     Max No. of dictionaries used:  1127     Peak Value (MB):  0.000
     #( 1052 still in use)
     Number of dictionary folders allocated:  1
         for the array: null
         in the routine: null
         Memory Peak of process: 13.124 MB
     Walltime since initialization:  00:00:00.001959716
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.020 MB
     Walltime since initialization:  00:00:00.002936658
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__6.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.848 MB
     Walltime since initialization:  00:00:00.001439685
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.124 MB
     Walltime since initialization:  00:00:00.002528723
     Memory Consumption Report:
       Tot. No. of Allocations:  0
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.076 MB
     Walltime since initialization:  00:00:00.002172121
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
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
         Memory Peak of process: 13.144 MB
     <BigDFT> Run already performed, found final file: forces_rmult__7.0.xyz
     Walltime since initialization:  00:00:00.002709484
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
         Memory Peak of process: 13.096 MB
     Walltime since initialization:  00:00:00.003000579
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.024 MB
     Walltime since initialization:  00:00:00.001800861
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.000 MB
     Walltime since initialization:  00:00:00.002194757
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
         Memory Peak of process: 13.096 MB
     Walltime since initialization:  00:00:00.002099085
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_rmult__8.0.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.228 MB
     Walltime since initialization:  00:00:00.001375382
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
    
    
    
    [165]:
    
    
    
    boxsize
    
    
    
    [165]:
    
    
    
    [[15.54, 15.54, 15.91],
     [18.87, 18.87, 18.87],
     [21.83, 21.83, 21.83],
     [25.16, 25.16, 25.16]]
    

## Computation of the statical polarizability tensor \\(\alpha\\)

We choose a single value of `rmult`, the lowest among the ones computed in the GS analysis for which a satisfactory convergence is obtained. The statical polarizability tensor of the CO molecule is then computed.
    
    
    [166]:
    
    
    
    ind = 2
    print('rmult value : ',study.ids[ind]['rmult'])
    
    
    
    rmult value :  7.0
    

The input file is defined for the statical polarizability computation
    
    
    [167]:
    
    
    
    inp.set_rmult(coarse=study.ids[ind]['rmult'],fine = 9.0)
    print(inp)
    
    
    
    {'dft': {'hgrids': 0.37, 'gnrm_cv': 1e-05, 'rmult': [7.0, 9.0]}, 'lin_general': {'rpnrm_cv': 'default'}, 'mix': {'rpnrm_cv': 'default'}}
    

Next, let us define a dataset (called ef, i.e. electric field) for the computation of \\(\alpha\\) using an electric field intensity of \\(1e^{-2} V/m\\), which is assumed compatible with the linear response regime.
    
    
    [168]:
    
    
    
    intensity = 1.e-2
    ef = D.Dataset(label='alpha',run_dir='CO_alpha',posinp='CO_posinp.xyz',
                   input=inp,d0=dipole_GS[ind],F=intensity)
    for idir,coord in enumerate(['x','y','z']):
        efi = np.zeros(3)
        efi[idir] = intensity
        inp.apply_electric_field(efi.tolist())
        ef.append_run({'id':coord,'F':intensity},runner=calc,input=inp)
    

This yields the following elements in the dataset
    
    
    [169]:
    
    
    
    ef.ids
    
    
    
    [169]:
    
    
    
    [{'id': 'x', 'F': 0.01}, {'id': 'y', 'F': 0.01}, {'id': 'z', 'F': 0.01}]
    

Lastly, let us write a post-processing function on how to compute \\(\alpha\\)
    
    
    [170]:
    
    
    
    def extract_alpha(ef):
        """
        alpha_ij isthe i-th component of the vector d-d0,
        computed with a field in the j-th direction,
        divided for the intensity of the field.
        """
        d0 = np.array(ef.get_global_option('d0'));
        F = ef.get_global_option('F');
        d = ef.fetch_results(attribute='dipole');
        alpha = np.mat(np.zeros(9)).reshape(3,3)
        for idir in range(3):
            alpha[idir] = (np.array(d[idir])-d0)/F
        return alpha
    
    ef.set_postprocessing_function(extract_alpha)
    
    
    
    [171]:
    
    
    
    alpha = ef.run();
    
    
    
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__x.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.044 MB
     Walltime since initialization:  00:00:00.001600831
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__x.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.176 MB
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__x.xyz
     Walltime since initialization:  00:00:00.001526451
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
     Walltime since initialization:  00:00:00.002919425
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__x.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.212 MB
     Walltime since initialization:  00:00:00.001484765
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__y.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.040 MB
     Walltime since initialization:  00:00:00.001618805
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__y.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.980 MB
     Walltime since initialization:  00:00:00.002415710
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__y.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.192 MB
     Walltime since initialization:  00:00:00.003128113
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__y.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.980 MB
     Walltime since initialization:  00:00:00.001501875
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__z.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.208 MB
     Walltime since initialization:  00:00:00.002225970
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__z.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 12.784 MB
     Walltime since initialization:  00:00:00.001519930
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__z.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.152 MB
     Walltime since initialization:  00:00:00.002236353
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
     <BigDFT> Run already performed, found final file: forces_F__0.01,id__z.xyz
     Memory Consumption Report:
       Tot. No. of Allocations:  0
       Tot. No. of Deallocations:  0
       Remaining Memory (B):  0
       Memory occupation:
         Peak Value (MB):  0.000
         for the array: null
         in the routine: null
         Memory Peak of process: 13.208 MB
     Walltime since initialization:  00:00:00.002061216
     Max No. of dictionaries used:  1127 #( 1052 still in use)
     Number of dictionary folders allocated:  1
    

The polarizability tensor is then
    
    
    [172]:
    
    
    
    alpha
    
    
    
    [172]:
    
    
    
    matrix([[ 1.26637417e+01, -2.31315400e-04,  4.23620000e-02],
            [-2.31315400e-04,  1.26637417e+01,  4.23620000e-02],
            [ 4.21875400e-04,  4.21875400e-04,  1.60751070e+01]])
    

[ Previous](CH4.html "Running a wavelet computation on a methane molecule") [Next ](SolidState.html "BigDFT for solid state systems")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).