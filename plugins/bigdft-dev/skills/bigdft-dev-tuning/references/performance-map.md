# Locate the actual work

Paths and symbol names below identify source families in the measured BigDFT
suite. Confirm them in the checkout being tuned; compiler-generated OpenMP suffixes
and library boundaries change. Search by routine before relying on line numbers.

| Timer or profile symbol | Source family / operation | What to separate |
|---|---|---|
| `ApplyProj`, `NonLocalHamiltonianApplication` | `bigdft/src/modules/hamiltonian.f90`; projector iterators and `gauss_to_daub_k` | Projector construction, Gaussian sampling/filtering, overlaps, coupling, back projection; the small contraction need not be the expensive part. |
| Multipoles, `apply_Slm` | `atlab/src/multipole.f90`, `harmonics.f90`; liborbs orbital application | Geometry, periodic wrapping, masks, temporary arrays and polynomial application; not just harmonic FLOPs. |
| `sumrho_TMB`, `sumrho_for_TMBs` | `bigdft/src/modules/rhopotential.f90` | Sparse coefficient packing, point-weight scan, thread cuts, contraction and following density redistribution. |
| `sumrho_allred` | Nested communication under the same density routine | Counts reduction, RMA window setup/fences, actual transfers, charge/negative-density reductions. Nested timers may suspend the parent's category. |
| `init_matrCompr`, `get_minmax_lines` | `bigdft/src/modules/bigdft_matrices.f90` | Repeated integer bound reductions versus sparse communication metadata setup. |
| `ApplyLocPot`, `ApplyLocPotKin` | `hamiltonian.f90` → orbital basis → `liborbs/src/views.f90`, `daubisf.f90` | Wavelet/ISF conversions, potential setup, multiplication/confinement, reverse conversion and any extra unconstrained output. Finite-water hot loops are not FFTs. |
| `PSolver Computation` | PSolver `H_potential`, FFT/convolution and boundary-specific kernels | Planning, transform execution, layout/scatter, factors, boundary padding and requested stress. |
| `Sparse matrix multiplication`, `sparsemm_new`, `my_dot` | `CheSS/sparsematrix/sparsematrix.f90` | Sparse segment/index processing, packed operands, arithmetic dot loops and compression communication. |
| `highlevel matrix operations` | `CheSS/src/matrix_operations.f90` | Overlap powers, input/output preparation and auxiliary work; subalgorithms switch timing categories. Trace its active segments, not just whole inclusive routines. |
| `matrixindex_in_compressed_lowlevel` | `CheSS/sparsematrix/sparsematrix_init.f90` | Segment search and index arithmetic at callers; distinguish repeated runtime lookups from one-time initialization. |
| `ovrlptransComp`, `calculate_overlap_transposed` | `bigdft/src/modules/transposed_operations.f90` | Coarse/fine overlap contractions, setup and reductions. |
| `lincombtrans`, `build_linear_combination_transposed` | Same module | Transposed sparse matrix/orbital combinations, coarse/fine loops, sparse lookups and packing. |
| `commbasis4dens` | `bigdft/src/modules/communications.f90` | Packing/switching before communication as well as data exchange; a communication-class timer can contain compute. |
| `convolQuartic`, `convolquartic4` | Wavelet preconditioner convolution family | Actual filter lengths, grow/shrink geometry, intermediate storage and team overhead. |
| `Array allocations`, `Init to Zero`, `Vector copy`, `buildgrad_mcpy`, `Routine Profiling` | Futile and calling algorithm scopes | Allocation versus tracking, first touch, clearing, copying and call/profiling bookkeeping. Locate callers before removing work. |
| Allreduce, Wait, RMA fences | Futile MPI wrappers and their callers | Late arrival, posted versus completed communication, progress, bytes and service tails. Large wait time alone does not select a load-balancing fix. |

## Timer and profiler accounting

- Label any manually grouped tail **remaining named timers**, list its members,
  and keep accounting differences separate. It is not a new BigDFT category.
  BigDFT also has its own class named `Other`; that class includes known routines
  such as projectors/density/overlap and differs from a shortened table's tail.
- Futile's category entries are synthesized across ranks. In the inspected
  `futile/flib/time.f90`, the `Total` time field uses the reporting rank's phase
  clock, while category times use rank synthesis. Check the implementation and
  fields before treating a category sum, phase total or full launch wall time
  as the same denominator. Printed values are rounded as well.
- Direct clocks around a routine can include allocation, clearing or MPI work
  assigned to other categories by nested timers. Explain the scope difference
  instead of forcing the totals to agree.
- Sum like phases deliberately (`INIT`, `WFN_OPT`, `LAST`), preserve phase splits,
  and distinguish launch/build/init work from the scientific calculation.
- FIPP's procedure cost basis can sum all threads. Read Base, Barrier and MPI
  fields separately and inspect report headers; do not add overlapping counts.
  In one A64FX profile, almost all of a huge `__?unknown` entry was explicitly
  marked barrier cost. Unknown symbols are not automatically unknown compute.
- OpenMP worker call stacks may be detached at a runtime microtask wrapper.
  A missing parent on worker threads does not prove a routine has no caller.
  Use explicit phase scopes to connect detached samples to the application.
- Use sample counts/counters to rank candidates and test mechanisms. Exact
  elapsed-time attribution needs appropriately scoped clocks/events. Normalize
  repeated replay profiles by each rank's repetitions, not one global guess.

## Choosing the next target

Prioritize an expensive operation with a plausible mechanism and a consequential
application saving. Expand broad categories before selecting one. For example,
allocation + clearing + copies across a hot loop may justify a lifetime change,
but avoiding required initialization or changing first touch can corrupt results
or worsen NUMA placement. Conversely, a library FFT can be efficient while an
unrelated matrix search dominates the region's elapsed time.

For communication, speeding the preceding kernel is often a candidate even when
its wait percentage rises. Repartitioning is a separate hypothesis, useful only
when the measured cost model and critical path support it. Do not compensate for
avoidable setup work by blindly fitting new ownership weights.
