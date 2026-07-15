# ST-03.03 implementation report

Completion verdict: `PASS`

## Outcome

The bounded `PRE_RATIFIED_SYNTHETIC_INPUT` branch now compiles the exact active repository-owned synthetic Source Lock, frozen atomic boundary, attributable human ratification, and Draft Harness Model into one immutable `cmf-builder-harness-ir/v1@1.0.0` revision. The snapshot carries 15 typed sections and 43 governed material values, preserves separate Activative lineage fields as explicit `NOT_APPLICABLE` values, advances the run from `ATOMICITY_RATIFICATION` to `GENESIS`, and emits an independently reproducible compilation receipt.

The compiler recomputes the immutable hashes of every upstream artifact before use. It rejects missing, stale, invalidated, mismatched, or altered inputs; non-code authority; unsupported versions; Workflow IR ownership; missing provenance; stale concurrency; changed idempotency payloads; and atomic commit failure. Replays return the original snapshot and receipt without another authoritative event. An authorized upstream reopen preserves the snapshot and history while invalidating the descendant IR and blocking further consumption.

## Implementation boundary

Added the typed Harness IR aggregate, compatibility/migration registry, compile command service, atomic development/test persistence, run reference/replay/invalidation support, synthetic-profile lifecycle prerequisite, observations, receipts, and capsule-defined tests. Existing architecture source-set tests received only the three new module paths.

No schema file, dependency file, authority policy, database, API, UI, external runtime, task execution, generated artifact set, Atomic Harness Definition, Development Capsule generator, Format 02 behavior, category adapter, VAE behavior, Delegation runtime behavior, GPU/provider/evaluator behavior, conversational behavior, Control Tower behavior, certification, publication, or production claim was added.

## Validation

- Capsule manifest: `3fab1cea6ac5006745b309112ebc9278d959f41114f9e7bbaf727906b774df6d` — PASS.
- Capsule bundle: `ce2c8ef3e72be41b4f4e74ef4dfab77155ec99e02c3559b43d864aa719ebfc82` — PASS, 17/17 immutable inputs.
- Four predecessor completion receipts: PASS and unchanged.
- Preimplementation regression: 84/84 PASS.
- Final ST-03.03 suite: 28/28 PASS twice in fresh processes.
- Isolated predecessor suites: 20/20, 18/18, 19/19, and 27/27 PASS.
- Architecture-boundary subset: 12/12 PASS.
- Full repository regression: 112/112 PASS with no skips.
- File-scope and prohibited-boundary audit: PASS.
- Deterministic compile, replay, atomic failure, authority rejection, altered-input rejection, and non-destructive invalidation evidence: PASS.

The only warning is the pre-existing `pytest-asyncio` default fixture loop-scope deprecation warning; it has no behavioral or test-result impact.

## Limitations preserved

This is a synthetic, repository-owned, non-production, non-certified Builder Core proof using the in-memory development/test adapter. It does not compile the later ST-03.04 artifact set, create an Atomic Harness Definition, generate a Development Capsule, execute a Harness, or authorize Release 1, full-product, or production readiness.
