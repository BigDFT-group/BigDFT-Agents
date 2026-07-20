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

  * [PyBigDFT API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/index.html)

Developer

  * [BigDFT-suite manifesto](../devel/developers.html)

  * [Futile API](https://l_sim.gitlab.io/bigdft-suite/futile/build/html/index.html)

__[BigDFT-suite](../index.html)

  * [](../index.html)
  * Usage of SystemCalculator instance
  * [ View page source](../_sources/tutorials/CalculatorsExamples.ipynb.txt)

* * *

# Usage of SystemCalculator instance

We here provide some examples on how to run the code with system calculator. Let us consider a very simple inputfile and a small system, that can be give from file and from a dictionary of atomic positions.
    
    
    [1]:
    
    
    
    from BigDFT import Inputfiles as I
    from BigDFT.Calculators import SystemCalculator
    from futile.Utils import write
    inp=I.Inputfile()
    inp.set_xc('PBE')
    inp.set_rmult(coarse=3) #very very little, only for test
    inp
    
    
    
    [1]:
    
    
    
    {'dft': {'ixc': 'PBE', 'rmult': [3, 8.0]}}
    

We initalize the SystemCalculator instance by specifying the number of OMP threads and the _command_ to be used for the mpirun calculation.
    
    
    [2]:
    
    
    
    code=SystemCalculator(omp=1,mpi_run='mpirun -np 2')
    
    
    
    Initialize a Calculator with OMP_NUM_THREADS=1 and command mpirun -np 2 /home/marco/Applications/BigDFT/binaries/v1.8.3/install/bin/bigdft
    

Let us define the function for validating the runs:
    
    
    [3]:
    
    
    
    def validate_run(inputfile,logfile):
        """
        Checks that the inputfile and the logfiles exists and have recent dates.
        """
        import os.path as P
        from futile.Utils import write,file_time
        from time import time
        write('Input and log existing',P.isfile(inputfile),P.isfile(logfile))
        write('Created since',time()-file_time(inputfile),time()-file_time(logfile))
      
    

Basic run, no name and atomic positions from a file:
    
    
    [4]:
    
    
    
    result=code.run(input=inp,posinp='CH4_posinp.xyz')
    write('Energy',result.energy)
    validate_run('input.yaml','log.yaml')
    
    
    
    Creating the yaml input file "./input.yaml"
    Executing command:  mpirun -np 2 /home/marco/Applications/BigDFT/binaries/v1.8.3/install/bin/bigdft
    Energy -8.09733985003
    Input and log existing True True
    Created since 2.02708792686 0.0871000289917
    

Now let us provide a naming scheme. The inputfile and the logfile will have different names:
    
    
    [5]:
    
    
    
    result=code.run(input=inp,posinp='CH4_posinp.xyz',name='test1')
    write('Energy',result.energy)
    validate_run('test1.yaml','log-test1.yaml')
    
    
    
    Creating the yaml input file "./test1.yaml"
    Executing command:  mpirun -np 2 /home/marco/Applications/BigDFT/binaries/v1.8.3/install/bin/bigdft -n test1
    Energy -8.09733985003
    Input and log existing True True
    Created since 1.93355202675 0.0256290435791
    

Let us now provide a output directory. To do that there are two different options:

  * Provide the `outdir` command to the `bigdft` executable

  * Define a `run_dir` for the run of the calculator instance. The difference between the two is the position of the input files. In the first case they will be in the Current Working Directory, whereas in the second one they will be placed in the run_directory.

    
    
    [6]:
    
    
    
    from os.path import join as j
    #first case
    result=code.run(input=inp,posinp='CH4_posinp.xyz',name='test2',outdir='out1')
    write('Energy',result.energy)
    validate_run('test2.yaml',j('out1','log-test2.yaml'))
    #second case
    result=code.run(input=inp,posinp='CH4_posinp.xyz',name='test3',run_dir='out2')
    write('Energy',result.energy)
    validate_run(j('out2','test3.yaml'),j('out2','log-test3.yaml'))
    #combine the two
    result=code.run(input=inp,posinp='CH4_posinp.xyz',name='test4',run_dir='out3',outdir='out4')
    write('Energy',result.energy)
    validate_run(j('out3','test4.yaml'),j('out3','out4','log-test4.yaml'))
      
    
    
    
    Creating the yaml input file "./test2.yaml"
    Executing command:  mpirun -np 2 /home/marco/Applications/BigDFT/binaries/v1.8.3/install/bin/bigdft -n test2 -d out1
    Energy -8.09733985003
    Input and log existing True True
    Created since 1.86937189102 0.0214099884033
    Create the sub-directory 'out2'
    Copy the posinp file 'CH4_posinp.xyz' into 'out2'
    Creating the yaml input file "out2/test3.yaml"
    Run directory out2
    Executing command:  mpirun -np 2 /home/marco/Applications/BigDFT/binaries/v1.8.3/install/bin/bigdft -n test3
    Energy -8.06514886077
    Input and log existing True True
    Created since 1.96282911301 0.0228381156921
    Create the sub-directory 'out3'
    Copy the posinp file 'CH4_posinp.xyz' into 'out3'
    Creating the yaml input file "out3/test4.yaml"
    Run directory out3
    Executing command:  mpirun -np 2 /home/marco/Applications/BigDFT/binaries/v1.8.3/install/bin/bigdft -n test4 -d out4
    Energy -8.06514886077
    Input and log existing True True
    Created since 1.95026421547 0.0226290225983
    
    
    
    [ ]:
    
    
    
    

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).