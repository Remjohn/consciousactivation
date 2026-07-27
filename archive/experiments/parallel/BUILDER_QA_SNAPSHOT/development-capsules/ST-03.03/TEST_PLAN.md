# Test plan

Run every command with `PYTHONPATH=src`, deterministic clocks/UUIDv7 providers, the existing repository-owned synthetic fixtures, and the in-memory development/test adapter. Network, external runtimes, model calls, and task execution are prohibited.

The new Story suite must contain at least 24 independently named tests across these seams:

1. Acceptance: exact active upstream package compiles one revision; all required sections exist; snapshot, canonical bytes, and receipt are deterministic.
2. Provenance: every material value has governed metadata; Source Lock, boundary, ratification, model, constitution, and decision refs are preserved; missing provenance is rejected.
3. Lineage: all five rich Activative reference keys remain separate; synthetic absence is explicit `NOT_APPLICABLE`; generic-notes flattening and semantic invention fail.
4. Compatibility: version `1.0.0` read/write succeeds; empty migration/deprecation sets validate; unknown version, in-place version mutation, missing migration, and malformed deprecation fail.
5. Aggregate boundary: Workflow IR fields and direct product-semantic copies outside Harness IR fail; no compiler/artifact-set behavior from `ST-03.04` appears.
6. Authority: compilation is code-owned from ratified inputs; agent/evaluator/external/direct human writes fail; upstream unratified or invalidated state fails.
7. Replay and failure: identical replay is idempotent; changed payload, stale stream, same-version rewrite, and injected atomic commit fail without partial state.
8. Invalidation: authorized upstream reopen explicitly invalidates the IR descendant and replay preserves history/state identity.
9. Observability: success, replay, rejection, atomic failure, and invalidation observations contain every required field and link to receipts.
10. Architecture: exact source set, standard-library-only imports, no external product/runtime imports, no schema/dependency changes, and no later Story behavior.

Required commands:

- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_03_03`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_01_01`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_01_01_synthetic_proof`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_01_02`
- `$env:PYTHONPATH='src'; python -m pytest -q tests/stories/st_02_05`
- `$env:PYTHONPATH='src'; python -m pytest -q`

Passing thresholds: all mandatory tests pass with no skips; preimplementation `84/84` passes; the new suite has at least 24 tests; architecture tests pass; two fresh-context Story reruns are deterministic; receipt/capsule/hash/file-scope validation passes.
