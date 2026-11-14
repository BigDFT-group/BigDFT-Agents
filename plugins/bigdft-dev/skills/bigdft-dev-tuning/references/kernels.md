# Kernel mathematics and cost descriptions

These descriptions cover established operations and mechanisms from source-level
investigations. They do not declare every implementation optimal. Verify the
current source and active branch before reusing a model. Count an FMA as two FLOPs;
state whether counts are source operations, executed instructions, or estimates.

When a new kernel is fully understood, add: operation/equations and normalization;
inputs/outputs, shapes and layout; operation and byte counts with assumptions;
reuse/lifetime, dependencies, masks and boundary cases; measured baseline and
calibration; observed assembly/counters; the floor/prediction; and application
validation status. Keep machine-specific observations separate from the model.

## Density contraction: `sumrho_for_TMBs`

**Operation.** For a real collinear spin block and active support functions at
point `p`, the implemented symmetric contraction is

```text
rho[p] = v^-1 (epsilon + sum_i K[i,i] phi_i[p]^2
                      + 2 sum_(i<j,stored) K[i,j] phi_i[p] phi_j[p])
v = (hx/2)(hy/2)(hz/2), epsilon = 1e-20 in this source path
```

Preserve the actual spin offsets, compressed task-group matrix offsets and absent
entry mask. The small floor is initialized before scaling in the inspected code.
The routine also accumulates total charge and counts negative density points.
Complex/spinor paths need their own derivation.

**Work.** Let `n_p` be the orbital count and `P_p` the number of present strict
upper-triangle pairs. The inspected scalar source evaluates about `4*n_p + 3*P_p`
FLOPs for diagonal/off-diagonal accumulation, plus scaling/charge work per point.
This includes forming `2*phi_i` per orbital; dead operations and reassociation
can change executed counts. There are `n_p(n_p+1)/2` potential pairs including
diagonals, but absent entries still incur lookup/branch work. Distinguish
`sum n_p`, pair counts, empty points and descriptor accesses; equal pair totals
need not imply equal cost.

**Data/reuse.** Point offsets/counts index packed orbital identifiers and values.
Coefficients use sparse row/section lookup spans. A hot off-diagonal step reads
an orbital identifier, a presence/index mask, a kernel value and an orbital value;
these are logical accesses, not necessarily off-chip bytes. Packing existing
sparse spans costs O(number of lookup entries) time/storage per refresh; a dense
orbital-squared cache changes the memory model. Reuse lifetime depends on geometry,
lookup metadata, matrix/spin state and task groups.

**Known mechanisms.** Pointer-chain lookup overhead, scalar dependent accumulation,
short inner loops, setup scans and team launch/barriers all matter. A packed
coefficient/mask representation can preserve the original `i,j` order. Diagonal
and row metadata can be packed separately, but require their own replay and
application gate. Weighted thread cuts themselves have a setup cost. In one
Fujitsu build, a work scan emitted SVE integer division by two, and partition
thresholds repeated variable integer divisions per point. Exact shifts for
nonnegative triangular counts and boundary-only threshold updates removed that
work without changing cuts. This is an assembly observation, not a language-wide
claim about integer division.

In inspected GCC/Genoa and Fujitsu/A64FX builds, the hot pair contraction remained
scalar on both CPUs. GCC's vectorized cut-index initialization did not vectorize
the contraction. Scalar FMA using an XMM or AArch64 FP register is not packed SIMD.
Compare the same executed specialization before attributing a performance gap to
one compiler's vectorization.

**Next SIMD hypothesis.** Batch independent grid points into vector lanes, keeping
each point's original `i,j` accumulation order. Equal orbital counts allow a
common loop shape even when orbital identifiers differ by lane. Bucketing within
the original thread cuts can improve lane occupancy, but coefficient gathers,
packing, tails and temporary storage must enter the model and measurements.
Store completed densities by original point index and retain original-order
charge accumulation when that reduction order must be preserved. This is a
proposed experiment, not an established kernel speedup.

**Correctness/floor.** Check both split sections, non-unit lower bounds, absent
entries, empty points, spin blocks, charge/negative counts and original reduction
semantics. A FLOP-only roofline misses integer/address overhead and the accumulation
chain. Calibrate packing and setup as well as contraction before predicting a gain.

## Solid-harmonic application: `apply_Slm` / row harmonic operator

**Operation.** Apply `out(r) = factor * R_lm(r-r0) * phi(r)`, with the code's real
solid-harmonic convention. This is an operator application, not by itself the
multipole-moment integral. For `l=0..2`, polynomials are constants; `x,y,z`;
and `xy,yz,zx,2z^2-x^2-y^2,x^2-y^2`, with harmonic-specific normalization.
Preserve signs, normalization, masks and floating-point multiplication grouping.

**Work/data.** For one harmonic, application is O(N) polynomial work over selected
grid points, with at least one input value and one output value per point. For
FP64, that payload is 16N bytes before coordinates, masks, write allocation and
cache effects. Do not equate it with HBM traffic. Generic geometry access,
wrapping, temporary arrays and allocation tracking can cost more than polynomial
arithmetic. Count the actual polynomial separately for each `(l,m)` specialization.

**Known mechanism.** For an orthogonal box, separable axes can move coordinate
preparation from O(Nx*Ny*Nz) to O(Nx+Ny+Nz) per region; the volume application
remains O(N). Row-polynomial application exposes contiguous work and avoids
per-point temporary geometry. Periodic x rows may cross seams or wrap repeatedly.
Retain production minimum-image/half-cell conventions, y/z iteration, slab
ownership and clipping. Nonorthogonal cells, masks or unsupported harmonics may
need a fallback. Test those paths explicitly.

**Floor.** Once geometry is removed, test whether polynomial instruction throughput,
loads/stores or short-row overhead limits the actual working set. Reuse axes only
at a lifetime where cell, origin and localization geometry remain valid.

## Gaussian-to-wavelet projector construction

**Operation.** A separable Cartesian term uses one-dimensional factors

```text
g_d(x) = A (x-x0)^d exp(-alpha (x-x0)^2)
c_k = sum_q F[k,q] g_d(x_q)
P[kx,ky,kz] = sum_terms C_term cx[kx] cy[ky] cz[kz]
```

Actual sampling/quadrature and wavelet filters determine `F`; preserve production
normalization, crop bounds and exponent conventions. The resulting projectors
enter `V_NL psi = sum_ab |p_a> h_ab <p_b|psi>`. Construction and this application
are different costs. Use the projector developer guide for PSP conventions.

**Work/data.** Each sampled point includes a displacement, square, exponent
formation, an exponential and a degree-dependent polynomial. Count exponentials
separately from basic FLOPs; generic integer power may call a runtime helper.
A filter stage with output-dependent tap count `L_k` has approximately
`2*sum_k L_k` FLOPs; compose all stages/axes and tensor-product writes explicitly.
Intermediate arrays, clipping and output bounds belong in the replay.

**Known mechanism.** The measured real degree-0/2 path spent heavily in scalar
safe-exponential sampling and tiny threaded filters. Specialized/vector Gaussian
sampling and serial execution of very short filters reduced cost. The original
assembly's scalar active predicate and the candidate's full-vector exponential
path were checked, rather than inferred from a vectorization flag. A vector
exponential instruction sequence is compiler/architecture-specific. Do not apply
real/cropped-path assumptions to complex or other exponent branches.

After specialization, both inspected compilers vectorized the selected fast
sampler: GCC used vector exponential library calls and Fujitsu used a full-vector
SVE exponential sequence. Missed-vectorization reports for the safe-exp fallback
did not describe that fast path. Profile the remaining construction/application
stages before repeating an already completed scalar-exponential optimization.

**Correctness/floor.** Test all used degrees, exponents, centers, filter/crop bounds
and output coefficients. Preserve safe-exp behavior in fallback cases. The floor
includes exponential throughput and short-stage overhead, not only filter FLOPs.
Do not assume an on-the-fly/all-projectors cache toggle is supported by every
linear-scaling or force path.

## Compressed-matrix bounds: `get_minmax_lines`

**Operation.** For each grid point's list of `n` orbital identifiers, update each
participating row's ordinary min/max column bounds and its wrapped min/max bounds.
The inspected wrap split is strict `j > nfvctr/2 + 1`; the other half uses
`j + nfvctr`. Existing bounds are cumulative across points and communication lists.

**Work/data.** The old row-by-column traversal repeats the same point-column
reductions for each of `n` rows: O(n^2) integer comparisons/accesses. Reduce the
point's ordinary and wrapped column bounds once, then update its `n` rows:
O(n) + O(n), using only a few scalar extrema/flags. Exact comparison counts depend
on split occupancy. Preserve empty half handling rather than replacing a missing
bound with a sentinel update.

**Known mechanism/floor.** This is redundant integer work, not an FP-peak problem.
The transformed routine scans identifiers twice and performs indexed row updates.
It needs no additional global array, MPI redistribution or numerical arithmetic.
Check duplicates, empty points, odd sizes, all split positions and cumulative
updates on coarse/fine lists. Profile cache/addressing and comparisons after
removing the quadratic work.

## Finite local-potential transform chain

**Operation.** In the measured free-boundary path, `c -> u = T c`, then real-space
potential/confinement multiplication, followed by `v -> T_back v`. Some callers
also require an unconstrained reverse conversion. Preserve normalization and
caller-requested outputs; this path is not simply an FFT application.

**Work/data.** A filter output with `L` terms is a multiply/add reduction, about
`2L` FLOPs. One inspected grow kernel performs two L=16 sums per output: 64 FLOPs,
or 256 for four full-width outputs. Edge rows have shorter bounds. Whole conversion
work is the sum of actual axis/stage outputs, with intermediate storage and layout
changes. Potential multiplication is much cheaper than the transform chain in
the measured finite-water cases.

**Assembly/floor.** The observed SVE path gathered filter/data channels and
horizontally reduced partial sums. Its register-load payload was not a measured
HBM byte count. An unroll requiring at least 24 taps was unreachable for the
normal 16-tap bounds and must not enter the executed-loop model. Vectorization
across outputs and input-window reuse remain hypotheses until a calibrated
rewrite and application check establish a gain.

## FFT-based Poisson solve and planning

**Operation.** For a compatible convolution representation, forward transform the
padded/distributed density, multiply by the boundary-specific reciprocal-space
kernel/factors, and inverse transform with the required normalization. Free,
periodic and mixed boundaries and distributed layouts need separate validation.

**Work/data.** Transform execution is O(N log N), with dimensions/factorization,
complex/real representation and strides determining its constants. Transposes,
packing, padded storage, communication and pointwise factors add O(N) work.
Planning is a separate setup cost. For `M` executions, report `T_plan + M*T_exec`
as well as execution-only time; plan reuse is beneficial only at a valid lifetime.

**Correctness/floor.** Preserve original layout, signs, normalization, stress work,
thread safety and plan/buffer ownership. Verify actual backend use: a distributed
fallback does not test the substituted FFT. Wisdom/plan reuse and a backend swap
are separate experiments. A measured kernel win does not establish a faster
application, and a memory/representation regression can outweigh faster FFTs.

## Sparse multiplication and index search: established primitives, incomplete model

For retained sparse output entries, the dot primitive in `sparsemm_new` is
`tt = sum_(k=1..n) x[k]*y[k]`, approximately `2n` FLOPs, reading 16n FP64 bytes of
operand payload before reuse. Summing segment lengths gives the arithmetic count;
packing, sparse index traversal and output accumulation need separate counts.
Changing reduction order may change floating-point rounding. The complete sparse
multiplication floor and segment-distribution model are not established here.

`matrixindex_in_compressed_lowlevel` computes a flattened `(row,column)` key,
starts at a column's segment index, and searches segment bounds until it finds
an entry or proves absence. A found entry returns a segment base plus offset.
Its cost is O(segments visited), with integer comparisons/address calculations;
repeated lookup can be expensive independently of matrix initialization. Measure
callers, hit/miss distribution and reuse before selecting binary search or a cache.

Overlap construction (`S_ij = sum_p phi_i[p]*phi_j[p]` with representation-specific
coarse/fine components) and transposed combinations (`psi'_i[p] = sum_j M_ij psi_j[p]`)
have established algebra. Exact executed operation/data counts and bottlenecks
for their current sparse implementations still require detailed tracing and
assembly. Do not label those implementation models complete merely from the formula.
