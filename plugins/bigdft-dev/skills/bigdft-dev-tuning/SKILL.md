---
name: bigdft-dev-tuning
description: Measure, profile, model, and optimize BigDFT source kernels, then validate their effect in the full calculation. Use for performance investigations, mini-app extraction, assembly analysis, and detailed timing instrumentation.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Tune BigDFT source code

Optimize the time to a scientifically equivalent completed calculation. A faster
mini-app, a smaller wait percentage, or a higher FLOP rate is supporting evidence;
acceptance comes from the application. Work on one hypothesis at a time and keep
an unchanged reference executable.

Infer the existing build, input, machine, and current experiment from available
artifacts before asking questions. If information is missing, ask one question at
a time while continuing independent work. Preserve the user's chosen physics and
optimization scope. Use the appropriate facility tools for remote jobs; this skill
does not grant submission, cancellation, or publication permissions.

## Investigation and acceptance

1. **Measure and profile the application first.** Record the source revision and
   dirty diff, executable checksum, compiler/flags/libraries, rcfile, input/PSPs,
   boundary conditions, allocation, affinity, MPI/OpenMP and library threading.
   Check convergence and actual work. Keep timing runs separate from profiler runs
   when collection overhead matters. Establish variability at the scale needed to
   distinguish the proposed gain; respect a user's request for an exploratory
   single result instead of withholding it until a campaign finishes.
2. **Choose a substantial measured cost.** Follow timers into source and call
   paths. Expand grouped remainders into named costs. Separate inclusive scopes,
   nested timers, rank averages, rank maxima, and thread-summed samples. A wait
   identifies a dependency; inspect preceding work before changing communication
   or ownership. Uniformly faster computation can increase the fraction in waits.
3. **Extract the unchanged kernel and calibrate it.** Use captured production
   values, shapes, strides, sparse lookup bounds, masks, boundary geometry and
   call/reuse patterns. Include allocation, packing, planning and initialization
   at their actual lifetime. Compare matching application and replay scopes,
   timings and profiles. Explain material discrepancies before trusting a replay
   to predict application performance. Correct output alone is insufficient.
4. **Understand the mathematics and generated implementation.** Describe the
   operation, counts, data movement/reuse, dependencies, branches, transcendental
   functions and synchronization. Inspect the hot executed assembly from the
   actual target compiler/flags. Measure relevant counters when available. Make
   a conditional performance-floor and application-saving estimate. Do not treat
   source loads as HBM traffic, static instruction counts as cycles, or FP peak
   as a meaningful ceiling for integer/search/runtime-heavy kernels.
5. **Change one thing in the mini-app.** Measure, profile, check numerical results,
   and inspect assembly again. Explain what improved and what now limits it.
   Test zero/short tails, masks, sparse gaps and relevant boundary cases. Keep
   reductions and accumulation order unless a justified numerical change is part
   of the experiment. Reject a mini-app regression before a large application run.
6. **Integrate privately and test the application.** Preserve the reference and
   otherwise match inputs, physics, convergence and layout. Alternate A/B order
   where repeats are needed. Check energies, forces, stress when relevant,
   multipoles, iteration/polynomial work, actual backend/path use, and memory.
   Profile both versions to explain the observed whole-application change.
7. **State a scoped decision.** Report ACCEPT, REJECT, or PENDING APPLICATION
   VALIDATION with before/after wall times, variation, numerical/work evidence,
   profile interpretation and agreement with the prediction. A changed iteration
   count is a confounder to investigate, not evidence for a kernel speedup.
   Compose separately accepted changes only after retesting their combination.

For a region with genuine wall-time fraction `f` and kernel speedup `s`, the
conditional Amdahl estimate is `1 / ((1-f) + f/s)`. Use critical-path phase clocks
where possible. Rank-average timer time is only a proxy, and accumulated waits
or independently timed parallel regions cannot simply be added as savings.

## Read only the references needed

- [Performance map](references/performance-map.md): source/timer routing and
  accounting pitfalls; start here when choosing a target or interpreting "other".
- [Kernel descriptions](references/kernels.md): established mathematics, operation
  and storage models, assembly questions and correctness constraints. Add a
  description whenever a kernel becomes fully characterized; label incomplete
  analysis explicitly rather than inventing counts or a bottleneck.
- [Detailed instrumentation](references/instrumentation.md): phase/worker clocks,
  application capture, isolated linking and calibrated MPI event traces.
- [Campaign observations](references/campaign-observations.md): examples of
  accepted/rejected approaches and workload-specific costs, not universal defaults.

For implementation conventions, use the neighboring developer skills for Futile,
ATlab, liborbs, PSolver and projectors as applicable. In particular, production
allocations/timers should follow Futile conventions, and orbital normalization,
periodic minimum images and PSP conventions must survive a rewrite.
