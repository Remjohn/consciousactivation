# Phase 3 Real-Generation Gates

A Phase 3 capability is not production-capable if it only:
- stores a payload;
- returns a precomputed fixture;
- emits synthetic candidates;
- compiles a graph but never executes it;
- has an API endpoint that only wraps persistence.

Known repository pattern from CURRENT.md:
- AIR F17/F28/F29/F30 services exist but their generation logic is absent/unreachable.
- Candidate comparison is real, but the registered candidate producer is synthetic.
- Interview Intelligence and Composer are substantially built and tested.
- VAE is downstream and should not be rebuilt by Phase 3.

Every mandate must identify the boundary between existing implementation and missing real generation.
