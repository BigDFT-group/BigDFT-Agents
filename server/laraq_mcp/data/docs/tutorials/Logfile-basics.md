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
        * Analyze a BigDFT run from a Logfile class
        * Visualization of a Linear Scaling calculation
        * [Plotting Density of States](DoS-Manipulation.html)
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
  * Analyze a BigDFT run from a Logfile class
  * [ View page source](../_sources/tutorials/Logfile-basics.ipynb.txt)

* * *

# Analyze a BigDFT run from a Logfile class

This small tutorial will show how to inspect the result of a BigDFT calculation from the `Logfile` class. An instance of this class is returned after the execution of a calculator. Technically, such instance is constructed from the `yaml` file which is associated to the logfile of the actual run of the `bigdft` core executable.

For this reason, it is possible to inspect already existing runs by manually instantiating the class from a `yaml` logfile. In order to do that we can load the Logfiles module:
    
    
    [1]:
    
    
    
    from BigDFT import Logfiles as L
    from os.path import join
    datadir = 'testfiles'
    
    
    
    [2]:
    
    
    
    from futile.Utils import data_path, untar_archive
    archive='Logfilesbasics.tar.gz'
    data_path(archive)
    untar_archive(archive,dest=datadir)
    
    
    
    Executing: wget https://raw.githubusercontent.com/BigDFT-group/resources/main/datalake/Logfilesbasics.tar.gz -O lfs.info
    --2025-01-17 17:45:22--  https://raw.githubusercontent.com/BigDFT-group/resources/main/datalake/Logfilesbasics.tar.gz
    Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 2606:50c0:8001::154, 2606:50c0:8002::154, 2606:50c0:8000::154, ...
    Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|2606:50c0:8001::154|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 132 [text/plain]
    Saving to: ‘lfs.info’
    
         0K                                                       100% 12.4M=0s
    
    2025-01-17 17:45:22 (12.4 MB/s) - ‘lfs.info’ saved [132/132]
    
    
    
    
    
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   902  100   747  100   155   2891    599 --:--:-- --:--:-- --:--:--  3496
    
    
    
    Executing: wget https://github-cloud.githubusercontent.com/alambic/media/547350918/aa/e1/aae1517fb137fb3ae7c6cacfb84a07a3e85ca12687afc3906dfa797abe665a76?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA5BA2674WPWWEFGQ5%2F20250117%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250117T174522Z&X-Amz-Expires=3600&X-Amz-Signature=c376af550f0f201242e1f7a93f021e06a9be79a87c186000815bf6cb6e869600&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=596478275&token=1 -O ./Logfilesbasics.tar.gz
    --2025-01-17 17:45:22--  https://github-cloud.githubusercontent.com/alambic/media/547350918/aa/e1/aae1517fb137fb3ae7c6cacfb84a07a3e85ca12687afc3906dfa797abe665a76?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA5BA2674WPWWEFGQ5%2F20250117%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250117T174522Z&X-Amz-Expires=3600&X-Amz-Signature=c376af550f0f201242e1f7a93f021e06a9be79a87c186000815bf6cb6e869600&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=596478275&token=1
    Resolving github-cloud.githubusercontent.com (github-cloud.githubusercontent.com)... 185.199.110.154, 185.199.108.154, 185.199.111.154, ...
    Connecting to github-cloud.githubusercontent.com (github-cloud.githubusercontent.com)|185.199.110.154|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 1074180 (1.0M) [application/x-gzip]
    Saving to: ‘./Logfilesbasics.tar.gz’
    
         0K .......... .......... .......... .......... ..........  4% 3.64M 0s
        50K .......... .......... .......... .......... ..........  9% 5.80M 0s
       100K .......... .......... .......... .......... .......... 14% 18.1M 0s
       150K .......... .......... .......... .......... .......... 19% 20.6M 0s
       200K .......... .......... .......... .......... .......... 23% 33.4M 0s
       250K .......... .......... .......... .......... .......... 28% 8.09M 0s
       300K .......... .......... .......... .......... .......... 33% 32.2M 0s
       350K .......... .......... .......... .......... .......... 38% 59.4M 0s
       400K .......... .......... .......... .......... .......... 42% 30.8M 0s
       450K .......... .......... .......... .......... .......... 47% 31.8M 0s
       500K .......... .......... .......... .......... .......... 52% 5.08M 0s
       550K .......... .......... .......... .......... .......... 57% 71.7M 0s
       600K .......... .......... .......... .......... .......... 61%  157M 0s
       650K .......... .......... .......... .......... .......... 66%  178M 0s
       700K .......... .......... .......... .......... .......... 71% 12.3M 0s
       750K .......... .......... .......... .......... .......... 76% 7.05M 0s
       800K .......... .......... .......... .......... .......... 81% 93.8M 0s
       850K .......... .......... .......... .......... .......... 85%  164M 0s
       900K .......... .......... .......... .......... .......... 90%  161M 0s
       950K .......... .......... .......... .......... .......... 95% 19.2M 0s
      1000K .......... .......... .......... .......... ......... 100%  137M=0.07s
    
    2025-01-17 17:45:23 (15.6 MB/s) - ‘./Logfilesbasics.tar.gz’ saved [1074180/1074180]
    
    
    
    
    
    [2]:
    
    
    
    ['log-mpro.yaml',
     'GEOPT-all_sqnmbiomode.out.ref.yaml',
     'log-K.yaml',
     'log-HBDMI.yaml']
    

Let us now load a file into a instance of a Logfile class. Imagine that our logfile corresponds to a single-point run, and it is present in a file named name `log-HBDMI.yaml`:
    
    
    [3]:
    
    
    
    HBDMI = L.Logfile(join(datadir,'log-HBDMI.yaml'))
    

From this instance it is also possible to visualize the system associated
    
    
    [4]:
    
    
    
    from BigDFT import Systems as S
    
    sys = S.system_from_log(HBDMI,fragmentation='atomic')
    
    
    
    [5]:
    
    
    
    sys.display(by_types=True)
    

3Dmol.js failed to load for some reason. Please check your browser console for error messages.  

    
    
    [5]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x1238203c1070>
    

The run is now loaded. To inspect its behaviour we might print it down to inspect the usual information:
    
    
    [6]:
    
    
    
    print(HBDMI)
    
    
    
    - Atom types:
      - C
      - N
      - O
      - H
    - cell: Free BC
    - number_of_orbitals: 41
    - posinp_file: HBDMI.xyz
    - XC_parameter: 1
    - grid_spacing: 0.3
    - spin_polarization: 1
    - total_magn_moment: 0
    - system_charge: 0
    - rmult:
      - 5.0
      - 8.0
    - dipole:
      - -0.19551
      - -0.61908
      - -0.096593
    - energy: -127.35074499502582
    - fermi_level: -0.1921099447862
    - forcemax: 0.01730347812308
    - forcemax_cv: 0.0
    - gnrm_cv: 0.0001
    - nat: 28
    - symmetry: disabled
    - No. of KS orbitals:
      - 41
    
    

The above information can also be accessed separately, by having a look at the attributes of the HBDMI object:
    
    
    [7]:
    
    
    
    list(HBDMI.__dict__) #you may also type: dir(HBDMI)
    
    
    
    [7]:
    
    
    
    ['label',
     'srcdir',
     'log',
     'number_of_orbitals',
     'posinp_file',
     'XC_parameter',
     'grid_spacing',
     'spin_polarization',
     'total_magn_moment',
     'system_charge',
     'rmult',
     'astruct',
     'data_directory',
     'dipole',
     'energy',
     'hartree_energy',
     'ionic_energy',
     'XC_energy',
     'trVxc',
     'evals',
     'forcemax',
     'forcemax_cv',
     'forces',
     'gnrm_cv',
     'memory_peak',
     'nat',
     'symmetry',
     'fermi_level',
     'memory',
     'datadir',
     'timefile']
    

Each of these attributes correspond to a specific quantity, which is documented in the [API](https://l_sim.gitlab.io/bigdft-suite/PyBigDFT/build/html/BigDFT.Logfiles.html). We here refer to some examples with the aim of showing some tests.

We might consider to postprocess some of the variables for study of the system. Here an example:
    
    
    [8]:
    
    
    
    print('The average energy per atom is:',HBDMI.energy/HBDMI.nat,\
        '(',HBDMI.energy,' Ha),',HBDMI.nat,' atoms)')
    print('There are also,',HBDMI.evals[0].info,' (up,down) orbitals in the run (if nspin)') #fix wrt to nspin
    
    
    
    The average energy per atom is: -4.548240892679494 ( -127.35074499502582  Ha), 28  atoms)
    There are also, [41, 0]  (up,down) orbitals in the run (if nspin)
    

It is also possible to access directly the yaml serialization of the `bigdft` logfile with the `.log` attribute.
    
    
    [9]:
    
    
    
    print(list(HBDMI.log))
    
    
    
    ['Code logo', 'Reference Paper', 'Version Number', 'Timestamp of this run', 'Root process Hostname', 'Number of MPI tasks', 'OpenMP parallelization', 'Maximal OpenMP threads per MPI task', 'MPI tasks of root process node', 'Compilation options', 'radical', 'outdir', 'logfile', 'run_from_files', 'dft', 'perf', 'lin_general', 'psolver', 'output', 'kpt', 'geopt', 'md', 'mix', 'sic', 'tddft', 'mode', 'lin_basis', 'lin_kernel', 'lin_basis_params', 'psppar.C', 'psppar.N', 'psppar.O', 'psppar.H', 'posinp', 'Data Writing directory', 'Atomic System Properties', 'Geometry Optimization Parameters', 'Material acceleration', 'DFT parameters', 'Basis set definition', 'Self-Consistent Cycle Parameters', 'Post Optimization Parameters', 'Properties of atoms in the system', 'Atomic structure', 'Box Grid spacings', 'Sizes of the simulation domain', 'High Res. box is treated separately', 'Poisson Kernel Initialization', 'Poisson Kernel Creation', 'Wavefunctions Descriptors, full simulation domain', 'Total Number of Electrons', 'Spin treatment', 'Orbitals Repartition', 'Total Number of Orbitals', 'Input Occupation Numbers', 'Wavefunctions memory occupation for root MPI process', 'NonLocal PSP Projectors Descriptors', 'Communication checks', 'Memory requirements for principal quantities (MiB.KiB)', 'Accumulated memory requirements during principal run stages (MiB.KiB)', 'Estimated Memory Peak (MB)', 'Ion-Ion interaction energy', 'Total ionic charge', 'Poisson Solver', 'Interaction energy ions multipoles', 'Interaction energy multipoles multipoles', 'Input Hamiltonian', 'Ground State Optimization', 'Last Iteration', 'GPU acceleration', 'Rho Commun', 'Total electronic charge', 'Multipole analysis origin', 'Electric Dipole Moment (AU)', 'Electric Dipole Moment (Debye)', 'Quadrupole Moment (AU)', 'Calculate local forces', 'Calculate Non Local forces', 'Timings for root process', 'BigDFT infocode', 'Average noise forces', 'Clean forces norm (Ha/Bohr)', 'Raw forces norm (Ha/Bohr)', 'Atomic Forces (Ha/Bohr)', 'Energy (Hartree)', 'Force Norm (Hartree/Bohr)', 'Memory Consumption Report', 'Walltime since initialization', 'Max No. of dictionaries used', 'Number of dictionary folders allocated']
    

We might access the Density of States of this system:
    
    
    [10]:
    
    
    
    DoS = HBDMI.get_dos(label='HBDMI molecule')
    ax = DoS.plot(sigma=0.2)
    _ = ax.set_title('Density of States, smearing 0.2 eV')
    

![../_images/tutorials_Logfile-basics_20_0.png](../_images/tutorials_Logfile-basics_20_0.png)

It is also possible to inspect if the run have converged correctly. The plot below shows the average wavefunction residue norm during the SCF iterations.
    
    
    [11]:
    
    
    
    _ = HBDMI.SCF_convergence()
    

![../_images/tutorials_Logfile-basics_22_0.png](../_images/tutorials_Logfile-basics_22_0.png)

## Case of a periodic system

The above case was a Free BC molecule single point run. Let us now consider the case of a periodic calculation. We take as an example a logfile coming from one run of the DeltaTest benchmark (see [this page](https://molmod.ugent.be/deltacodesdft) to know what it is all about). In any case, let us load the `log-K.yaml` file:
    
    
    [12]:
    
    
    
    K = L.Logfile(join(datadir,'log-K.yaml'))
    print(K)
    
    
    
    - Atom types:
      - K
    - cell:
      - 9.98888442684
      - 9.98888442684
      - 9.98888442684
    - number_of_orbitals: 13
    - XC_parameter: -101130
    - grid_spacing:
      - 0.332966147561
      - 0.332966147561
      - 0.332966147561
    - spin_polarization: 1
    - total_magn_moment: 0
    - rmult:
      - 10.0
      - 8.0
    - dipole:
      - -42.025
      - -42.025
      - -42.025
    - energy: -56.52301363451743
    - fermi_level: 0.0609691899665294
    - forcemax: 2.038812434232e-07
    - forcemax_cv: 0.0
    - gnrm_cv: 1e-08
    - kpt_mesh:
      - 15
      - 15
      - 15
    - nat: 2
    - stress_tensor:
      - - 5.126601876834e-07
        - 3.529303946071e-23
        - -1.058791184314e-22
      - - 3.529303946071e-23
        - 5.126601876383e-07
        - -8.215933604291e-33
      - - -1.058791184314e-22
        - -8.215933604291e-33
        - 5.126601877667e-07
    - symmetry: not prim.
    - No. of KS orbitals per k-point:
      - 13
    
    

Here we can see that there are also other attributes available, like the \\(k\\)-points and the pressure (in GPa):
    
    
    [13]:
    
    
    
    list(K.__dict__)
    
    
    
    [13]:
    
    
    
    ['label',
     'srcdir',
     'log',
     'number_of_orbitals',
     'XC_parameter',
     'grid_spacing',
     'spin_polarization',
     'total_magn_moment',
     'rmult',
     'astruct',
     'data_directory',
     'dipole',
     'energy',
     'hartree_energy',
     'ionic_energy',
     'XC_energy',
     'trVxc',
     'evals',
     'fermi_level',
     'forcemax',
     'forcemax_cv',
     'gnrm_cv',
     'kpts',
     'kpt_mesh',
     'memory_peak',
     'nat',
     'stress_tensor',
     'symmetry',
     'nkpt',
     'memory',
     'datadir',
     'timefile']
    

For example, the structural information can be accessed by:
    
    
    [14]:
    
    
    
    K.astruct
    
    
    
    [14]:
    
    
    
    {'cell': [9.98888442684, 9.98888442684, 9.98888442684],
     'positions': [{'K': [0.0, 0.0, 0.0]},
      {'K': [4.994442213, 4.994442213, 4.994442213]}],
     'Rigid Shift Applied (AU)': [0.0, 0.0, 0.0],
     'forces': [{'K': [1.721377403941e-25, 0.0, 0.0]},
      {'K': [1.721377403941e-25, 0.0, 0.0]}]}
    

Here we might also trace the density of states and the band structure, in a similar fashion:
    
    
    [15]:
    
    
    
    K.get_dos().plot()
    
    
    
    [15]:
    
    
    
    <Axes: xlabel='Energy [eV]', ylabel='DoS'>
    

![../_images/tutorials_Logfile-basics_31_1.png](../_images/tutorials_Logfile-basics_31_1.png)
    
    
    [16]:
    
    
    
    K.SCF_convergence()
    
    
    
    /opt/bigdft/install/lib/python3.12/site-packages/BigDFT/Logfiles.py:412: UserWarning: No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
      ax2.legend(loc="upper right")
    
    
    
    [16]:
    
    
    
    <Axes: title={'center': 'testfiles/log-K.yaml'}, xlabel='Inner Iterations', ylabel='Norm of Residue'>
    

![../_images/tutorials_Logfile-basics_32_2.png](../_images/tutorials_Logfile-basics_32_2.png)

We here see the different steps that the code took to optimize the density.

## Writing band structures out of a converged system

The logfile, for periodic systems, can also be employed to write band structures.
    
    
    [17]:
    
    
    
    from BigDFT import BZ
    BZ_K = K.get_brillouin_zone()
    
    
    
    spacegroup Im-3m (229)
    Lattice found: cubic
    
    
    
    /opt/upstream/lib/python3.12/site-packages/ase/dft/kpoints.py:654: UserWarning: Please call this function with cell as the first argument
      warnings.warn('Please call this function with cell as the first '
    
    
    
    irreductible k-points 120
    Interpolation bias 6.95567292478855e-09
    
    
    
    [18]:
    
    
    
    ax = BZ_K.plot(npts=300)
    ax.set_ylim([-1,3])
    
    
    
    /opt/upstream/lib/python3.12/site-packages/ase/dft/kpoints.py:356: UserWarning: Please do not use (kpts, x, X) = bandpath(...).  Use path = bandpath(...) and then kpts = path.kpts and (x, X, labels) = path.get_linear_kpoint_axis().
      warnings.warn('Please do not use (kpts, x, X) = bandpath(...).  '
    
    
    
    [18]:
    
    
    
    (-1.0, 3.0)
    

![../_images/tutorials_Logfile-basics_36_2.png](../_images/tutorials_Logfile-basics_36_2.png)

As an another example, we might inspect the \\(k\\)-points such as the \\(\Gamma\\) point:
    
    
    [19]:
    
    
    
    Gamma = K.kpts[0]
    print(Gamma)
    
    
    
    {'Rc': [0.0, 0.0, 0.0], 'Bz': [0.0, 0.0, 0.0], 'Wgt': 0.0003}
    

## Case of a Geometry optimization

For a geometry optimization the situation is similar, with the extra point that the code automatically recognize multiple runs inside the logfile. Let us see the example of the following logfile:
    
    
    [20]:
    
    
    
    geopt = L.Logfile(join(datadir,'GEOPT-all_sqnmbiomode.out.ref.yaml'))
    print(geopt)
    
    
    
    Found 11 different runs
    - cell: Free BC
    - number_of_orbitals: 7
    - posinp_file: sqnmbiomode.xyz
    - XC_parameter: 1
    - grid_spacing:
      - 0.45
      - 0.45
      - 0.45
    - spin_polarization: 1
    - total_magn_moment: 0
    - system_charge: 0
    - rmult:
      - 5.0
      - 8.0
    - energy: -14.900068217309986
    - fermi_level: -0.2935133380623
    - forcemax: 0.00376314
    - forcemax_cv: 0.01
    - force_fluct: 0.000771111
    - gnrm_cv: 0.0001
    - nat: 8
    - symmetry: disabled
    - No. of KS orbitals: []
    
    

The interesting point is that now the logfile can be iterated among the different geometry steps:
    
    
    [21]:
    
    
    
    en = [l.energy for l in geopt]
    for i,e in enumerate(en):
        print(i,e)
    
    
    
    0 -14.896095253859464
    1 -14.897377172313178
    2 -14.898482433406212
    3 -14.898861280172312
    4 -14.899264325696496
    5 -14.899589665247579
    6 -14.899694268869062
    7 -14.899781420570605
    8 -14.899830568576757
    9 -14.899987054521805
    10 -14.900068217309986
    

The `geopt_plot` function allows to plot the relation beween energy and forces, where it can be also seen that the desired criterion is reached. Errorbars show the local fluctuation of the forces, an indication of the (cleaned) center of mass drift. See the example:
    
    
    [22]:
    
    
    
    ax = geopt.geopt_plot()
    

![../_images/tutorials_Logfile-basics_45_0.png](../_images/tutorials_Logfile-basics_45_0.png)
    
    
    [23]:
    
    
    
    sys_opt = S.system_from_log(geopt,fragmentation='full')
    sys_start = S.system_from_log(geopt[0],fragmentation='full')
    sys = [S.system_from_log(l,fragmentation='full') for l in geopt]
    
    
    
    [24]:
    
    
    
    # show the start and last
    sys_opt['START:0'] = sum(sys_start.values())
    sys_opt.display(by_types=True)
    

3Dmol.js failed to load for some reason. Please check your browser console for error messages.  

    
    
    [24]:
    
    
    
    <BigDFT.Visualization.InlineVisualizer at 0x1237e859be30>
    

We can also see the animation of the geometry optimization
    
    
    [25]:
    
    
    
    from BigDFT.Visualization import InlineVisualizer
    viz=InlineVisualizer(400,300)
    viz.display_system(*sys)
    

3Dmol.js failed to load for some reason. Please check your browser console for error messages.  

# Visualization of a Linear Scaling calculation

In the Linear Scaling approach the self-consistent field has a different method for achieving convergence. It consists of a double-loop structure where the basis set of the BigDFT support functions is first optimized to minimize the band structure energy (up to a user-defined defined energy level) of the given Hamiltonian operator. Then, the Hamiltonian and Overlap matrix elements in the provided subspace are used for calculating the Density Matrix Kernel, which gives rise to a new Hamiltonian operator until convergence.

We now visualize this behavious with a logfile which is conceived for Linear Scaling. We use a ~5k atoms system (SarS-CoV-2 Mpro).
    
    
    [26]:
    
    
    
    mpro = L.Logfile(join(datadir,'log-mpro.yaml'))
    
    
    
    [27]:
    
    
    
    print(mpro)
    
    
    
    - Atom types:
      - N
      - H
      - C
      - O
      - S
      - F
    - cell: Free BC
    - number_of_orbitals: 6661
    - XC_parameter: -101130
    - grid_spacing: 0.45
    - spin_polarization: 1
    - total_magn_moment: 0
    - system_charge: -2
    - rmult:
      - 5.0
      - 8.0
    - dipole:
      - -16.6482
      - -1.404238
      - 4.437426
    - energy: -23355.30738828983
    - forcemax: 0.2424825335692
    - forcemax_cv: 0.0
    - gnrm_cv: 0.0001
    - nat: 4752
    - symmetry: disabled
    
    
    
    
    [28]:
    
    
    
    mpro.SCF_convergence()
    
    
    
    /opt/bigdft/install/lib/python3.12/site-packages/BigDFT/Logfiles.py:412: UserWarning: No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
      ax2.legend(loc="upper right")
    
    
    
    [28]:
    
    
    
    <Axes: title={'center': 'testfiles/log-mpro.yaml'}, xlabel='Inner Iterations', ylabel='Norm of Residue'>
    

![../_images/tutorials_Logfile-basics_53_2.png](../_images/tutorials_Logfile-basics_53_2.png)

We here see that the behaviour is completely different from the other approaches as the residues have actually different meanings. Also, the convergence criterion in the various loops are handled in a different way.
    
    
    [ ]:
    
    
    
    

[ Previous](CH4_aiida.html "Running a wavelet computation on a methane molecule, with AiiDa") [Next ](DoS-Manipulation.html "Plotting Density of States")

* * *

(C) Copyright 2018-%s, BigDFT developers.

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).