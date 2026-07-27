# Implementation scope

The bounded outcome is profile admission on the already completed run-governance foundation. The implementation must allow `ST-01.01` lifecycle services to load the exact synthetic fixture, select `atomic_content_harness`, create a stable governed run, enforce the fixture's required-work sequence, checkpoint it, and resume it without duplicate decisions or events.

The work requires additive code changes, a fixture-backed profile repository, and tests. It is not fixtures-only. It requires no canonical category or target-registry change. Documentation changes are limited to the branch completion evidence.

Permitted behavior:

- Generalize the existing target-profile domain boundary only enough to express an authorized immutable profile definition while preserving the current Format 02 behavior.
- Add a repository adapter that reads only the capsule's pinned synthetic target-profile fixture and validates its identity and hash.
- Keep `atomic_content_harness` as one of the existing three compilation targets.
- Carry explicit `synthetic`, `repository_owned`, `non_production`, `non_certified`, and `builder_core_validation_only` markers into the run evidence.
- Enforce the exact hash-pinned empty skill registry and fail closed on undeclared skill use.
- Run the existing `ST-01.01` regression tests unchanged.

The branch stops after governed run admission and replay proof. It does not lock the synthetic task workspace, compile IR, compile an Atomic Harness Definition, or generate the task's Development Capsule; those are later confirmed Stories beginning at `ST-01.02`.
