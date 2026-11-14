# Lessons from an A64FX tuning campaign

These are measured examples, not portable benchmark expectations or current queue
status. They illustrate how to choose and validate an optimization. Localized
basis, pseudopotential, geometry, convergence and baseline revisions materially
change both costs and results. Large-water examples below are aggregates of
translated Water64 bubbles, not equilibrated droplets of the larger sizes.

## Where linear-mode water spent time

PBE/NLCC, hgrid 0.5 bohr, standard linear profile, finite boundaries, native Fujitsu
build on A64FX; four MPI ranks/node and twelve OpenMP threads/rank. The first
unprofiled runs used sixteen nodes for Water512 and twenty-four for Water1024.
Times below are cumulative **mean-rank category seconds**, not additive measured
critical-path wall fractions.

| Category | Water512 | Water1024 |
|---|---:|---:|
| Allreduce, small + large | 109.0 | 100.4 |
| Wait | 87.6 | 90.1 |
| Nonlocal projectors | 64.5 | 88.7 |
| Sparse matrix multiplication | 71.0 | 71.8 |
| Density construction | 66.3 | 63.8 |
| Poisson computation | 36.4 | 50.7 |
| Sparse compression communication | 34.5 | 48.5 |
| Local potential | 44.0 | 43.4 |
| Potential communication | 25.77 | 38.0 |
| High-level matrix operations | 16.0 | 26.7 |
| Overlap construction | 22.74 | 23.0 |
| Preconditioning convolutions | 20.55 | 20.74 |
| Transposed linear combinations | 17.69 | 17.93 |
| Zeroing | 17.49 | 17.66 |
| Array allocations | 14.96 | 18.70 |
| Basis-to-density communication | 12.0 | 17.7 |

Water512's first wall time was 816.67 s (two-run median 821.52 s), with 22 outer
iterations. Water1024's first wall time was 925.90 s, with 15 outer iterations.
Different outer work and node counts prevent treating their raw ratio as scaling
or optimization speedup. A shortened table's remainder must not conceal the
additional named categories or the distinction between category sums and phase
clocks. Inspect the broader work before assuming load imbalance is the next fix.

## Completed application examples

- **Packed density lookup spans:** a four-node Water64 A/B reduced median wall
  time from 224.72 to 215.31 s (three pairs), close to a prior 9.25–9.51 s replay
  prediction. Outer/inner work, energies and multipoles matched; force differences
  were around 1e-14. This supports that representation change for that workload,
  not every further density cache idea.
- **Linear-time matrix bounds:** Water64 reduced median wall time from 175.96 to
  158.28 s after calibrated replay predicted roughly 16.5 s saved. This was an
  integer-work removal, not improved FLOP utilization. It used a later baseline
  than the preceding density experiment; do not add ratios or compare them as
  otherwise identical controls.
- **Density setup divisions:** two alternating Water16 pairs measured 90.52/90.82 s
  controls versus 89.02/88.98 s candidates, a 1.67 s median saving against a prior
  1–2 s estimate. Scientific work/energies/multipoles matched, with force changes
  around 1e-15. Application profile comparison was still pending at this record.
- **Density row-metadata cache:** a fresh native replay matched baseline
  application call scopes within 6% and sped up by 1.34–1.37x. Two alternating
  Water16 application pairs reduced median wall time from 90.40 to 88.145 s:
  2.255 s saved (2.49%), matching the predicted 2–3 s. Scientific work, energies
  and multipoles matched, with force changes around 1e-14 or below. Separate
  profiles reduced the density category from 8.10 to 6.03 mean-rank seconds;
  normalized non-barrier worker samples fell from about 6.76 to 4.75 s. These
  measurements support acceptance for this one-node, four-MPI/twelve-thread
  Water16 configuration. Larger-system acceptance and composition with the
  separate setup-division change still require application tests.
- **Preconditioner plane-owner fusion:** correct extracted code slowed from about
  7.69 to 8.11 ms. Reject that candidate at the kernel gate instead of promoting
  a synchronization-count reduction as an application gain.
- **FFT substitutions:** warmed kernel execution and planning reuse did not imply
  a general application win. Some finite workloads regressed, and distributed
  paths sometimes fell back to the original backend. Treat backend use, planning,
  layout and stress semantics as distinct controlled questions.

## Mechanisms identified without claiming completed application acceptance

- Finite local potential was dominated by wavelet/ISF conversions, not the
  pointwise multiplication or an FFT. Water128 direct clocks placed about 55%
  of that caller scope in forward conversion and 26% in reverse conversions.
  Even doubling transforms gave only a conditional few-percent application
  estimate. This motivated a change of target, not an unvalidated rewrite.
- Calibrated Gaussian projector axis replay showed expensive scalar exponential
  sampling and tiny threaded filters. A specialized/vector sampler plus serial
  short filters gave roughly ninefold replay improvement with exact captured
  coefficients. The mathematical model counted exponentials and runtime/team
  work separately from filter FLOPs.
- Density metadata Allreduce traces on Water256 showed almost all of the blocking
  interval before the latest participant entered. Equal triangular pair estimates
  coexisted with very different point/orbital counts and compute durations. This
  located preceding work; it did not prove repartitioning was the best solution.
- The density pair contraction was scalar in both inspected GCC/Genoa and
  Fujitsu/A64FX assembly. This rules out an assumed GCC SIMD advantage in that
  particular loop; it does not explain the full cross-configuration timing gap.
  Wide-vector arithmetic remains a priority on A64FX.
- Density point-batching feasibility analysis found adjacent identical-list
  eight-point blocks covered only about 9–24% of pair work in two captured
  contexts. Bucketing by orbital count within existing thread cuts could fill
  eight-point batches for about 97–99% of pair work. These are lane-coverage
  estimates, not speedups: packing, gathers and the vector kernel remain untested.
- Sparse dot arithmetic, compressed index search, overlap and transposed
  combinations remained prominent after earlier optimizations. Their remaining
  full implementation floors and broad trace attribution were still under study.

Keep new pending evidence out of ACCEPT claims. Update kernel descriptions when
mathematics and executed work are established; update performance conclusions
only when the corresponding application gate is complete.
