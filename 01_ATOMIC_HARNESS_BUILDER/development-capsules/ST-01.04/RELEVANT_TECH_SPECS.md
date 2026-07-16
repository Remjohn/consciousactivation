# Relevant Technical Specifications

- `TS-02-CONFIGURED-EVIDENCE-WORKSPACE.md` owns saturation contracts, gaps,
  conflicts, deterministic evaluation, invalidation, resume, scale and typed failure.
- `TS-03-VISUAL-SYNTAX-FIRST.md` is relevant only for the prohibition against
  inventing semantic or visual claims; visual parsing is not implemented here.
- `TS-10-BEHAVIORAL-EVALUATION-AND-BENCHMARKS.md` supplies the evidence-backed
  evaluation boundary; benchmarks and certification remain excluded.
- `TS-13-IMPLEMENTATION-AUTHORIZATION-AND-DEVELOPMENT-CAPSULE.md` preserves the
  hard-gate distinction between a Story outcome and product readiness.

Implementation owner: evidence workspace. Component boundary: active Source Lock,
active Evidence Index, and a local versioned Saturation Contract. Failure behavior:
typed fail-closed outcome without atomicity, Genesis, readiness, or external action.
Test seam: public application command plus repository query and observation seams.
Compatibility: existing immutable artifacts are referenced, never mutated.
