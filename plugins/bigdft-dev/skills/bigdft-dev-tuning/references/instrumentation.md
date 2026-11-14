# Detailed measurement without changing the calculation

Use instrumentation to answer a specific attribution question, then compare its
scientific work/results and overhead with the unchanged executable. Keep diagnostic
and uninstrumented timing binaries distinct. Trace records, compiler reports and
raw samples should remain tied to source and executable hashes.

## Phase clocks and worker time

Futile provides nanosecond clocks. Use direct clocks when nested category timers
make it difficult to measure an inclusive caller scope:

```fortran
use f_precisions, only: f_long, f_double
use f_utils, only: f_time
! Declarations in the routine's specification section:
integer(f_long) :: started, elapsed
real(f_double) :: phase_seconds

started = f_time()
! FILL: unchanged operation whose inclusive duration is required.
elapsed = f_time() - started
phase_seconds = real(elapsed, f_double) * 1.d-9
! Store the value; write the report after the timed operation.
```

Confirm exported module names in the installed Futile version; existing routines
may already import `f_time` through `futile` or their profiling module. Use standard
Futile category creation/ON/OF conventions when adding production timer categories,
rather than hardcoded numeric IDs. Trace-only clocks need not introduce new input
variables or production categories.

Split both setup and arithmetic: allocation/first touch, metadata/packing, work
counting, partition construction, worker loop, cleanup and redistribution. Avoid a
single "kernel" timer that silently changes its boundaries between variants.

For OpenMP, give each thread a disjoint timestamp/count slot and measure the end
of its useful loop **before** the existing join barrier. Otherwise fast workers
appear equally busy. Write records after leaving the team. `omp_get_wtime` is
suitable for a thread's own elapsed duration; do not assume different threads'
absolute clock readings are synchronized. Keep team size and ownership visible.
Do not add barriers merely to make the picture easier to interpret.

Measure clock/event overhead at the required granularity. Buffer events; formatted
I/O inside a tight loop can become the bottleneck. A root-only report/flush can
also delay a subsequent collective. Trace that possibility instead of assuming it.
Buffered files may stay empty during a running job: validate completion markers
and do not mistake unflushed traces for absent execution.

## Capture an actual kernel invocation

Capture metadata, initial state and expected output for selected calls/ranks,
including a representative slow rank and an interior rank. Record call IDs and
layout. Keep snapshot writing outside the kernel clock. Preserve:

- Values, types/kinds, shapes, strides, lower bounds and pointer association.
- Sparse masks, section bounds, index bases and task-group/spin offsets.
- Boundary/cell geometry, masks, ownership, branch flags and output bounds.
- Initial accumulators/output state when updates are cumulative.
- Setup/planning lifetime, call counts, working-set size and realistic reuse.

Fortran unformatted stream I/O can store arrays and scalar metadata explicitly;
do not dump raw derived-type/pointer descriptors as a portable serialization.
Version the format and validate each record. Match compiler integer/real widths
and byte order, or use a defined portable encoding when moving between platforms.

A replay must reset mutated state between trials. Put resets outside timing only
when the application also does so. Include reference/candidate allocation and
packing fairly. Consume/check outputs so optimization cannot eliminate the work.
Do not time a compiler-hoisted identical loop as repeated execution. Extract the
production routine where feasible instead of reimplementing its "equivalent" math.

Compare original per-call timing and profile/counters with matching application
measurements. If serial/threaded launch, data temperature, NUMA placement or
missing setup differs, resolve or quantify the discrepancy. Capturing the right
shape with synthetic values does not necessarily reproduce sparse branches or
coefficient/descriptor reuse.

## Isolated object and link overrides

An existing configured suite can build diagnostic copies of selected modules and
link their objects before the original static archives. Keep interfaces unchanged
or rebuild all affected users of changed `.mod` interfaces. Use a private object
and module-output directory; put its module search path before baseline paths.
Inspect the final link and verify the intended symbols/objects are actually used.

A small supplementary make target can reuse the configured dependency list:

```make
.PHONY: tuning-link
tuning-link:
	$(FC) $(AM_FCFLAGS) $(FCFLAGS) $(AM_LDFLAGS) $(LDFLAGS) -o $(TRIAL_OUTPUT) BigDFT.o $(TRIAL_OBJECTS) $(bigdft_LDADD) $(LIBS)
```

Here `BigDFT.o` is the unchanged main object in the inspected build. Adapt the
object list and variable names to that Makefile; a replaced main must appear
exactly once. `TRIAL_OBJECTS` contains only the intended overrides and diagnostic
helpers. This is a build pattern, not a substitute for checking module ABI and
archive resolution. Preserve installed/reference checksums before and after.

Compile assembly from the same target compiler, flags, includes and source as the
object being measured. Changing LTO, floating-point flags or helper inlining can
change both performance and numerical behavior. Check the actual hot specialization,
trip counts and tails. Inspect lanes/predicates, gathers, shuffles/reductions,
integer divisions, transcendental/power helpers, spills, calls and synchronization.
Do not count an unreachable generic unroll as the executed path.

## MPI event traces

Local elapsed clocks measure a rank's phase duration without synchronizing clocks.
Cross-rank arrival comparisons require either documented globally comparable
clocks or explicit calibration. Never compare arbitrary `MPI_Wtime` values as if
they share an epoch.

One practical diagnostic scheme is a duplicated communicator and repeated root/peer
ping-pongs at startup and shutdown. A minimum-RTT midpoint gives an offset estimate
and a half-RTT uncertainty indicator. Record endpoints and interpolate measured
drift offline. Endpoint estimates do not bound arbitrary nonlinear drift or
systematic asymmetric latency. Check causality and sensitivity against plausible
clock error; avoid excessive precision in small service-tail estimates. Keep
calibration barriers outside the phases being investigated.

Record stable labels and call-site IDs, per-site occurrence, rank, local time,
context and relevant sizes/work counts. Match asynchronous POST/GATHER operations
using request identity **and operation order**: handles can be reused. Verify
participation/counts and detect unmatched requests rather than silently pairing
different collectives.

For a collective with rank entry `a_r`, exit `b_r`, and latest entry `L`:

```text
pre_r  = max(0, min(b_r,L) - a_r)
tail_r = max(0, b_r - max(a_r,L))
```

The first interval contains early arrival and possibly overlapped communication;
it is not directly recoverable wall time. The tail includes MPI service, progress
and scheduling, not just network latency. A long wait after every rank has posted
can come from intervening work or progress behavior. Trace compute scopes between
post and wait; compare the late path's substeps and message volumes.

Use these events to locate expensive dependency paths. Do not insert a barrier,
remove a collective, or change ownership merely to reduce the reported wait.

## Validate profiles and timing accounting

Record sampling interval, collection duration, target processes/threads and
counter definitions. Check lost/overflow samples, empty streams and symbolization.
For FIPP, request reports for data actually collected: a non-MPI replay can have
valid CPU/call data but no MPI cost data, causing an MPI-inclusive report request
to fail. Recover valid reports before rerunning an expensive calculation.

Retain broad timer coverage alongside detailed scopes so costs do not disappear
when focus changes. Expand "other" into named routines and list any unresolved
accounting separately. Nested timing categories, rank synthesis, reporting-rank
phase clocks and thread-summed samples have different meanings.

Validate diagnostic versus unchanged runs for actual iteration/polynomial work,
energies, forces, stress/multipoles as applicable, branch use and memory tracking.
Then use uninstrumented A/B timings for acceptance. A fast diagnostic run is not
itself the production performance result.
