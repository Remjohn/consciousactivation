# ST-02.05 implementation report

## Outcome delivered

`ST-02.05 / DECLARED_BOUNDARY` is implemented as a bounded, category-neutral Builder Core vertical slice. Starting from the exact immutable `ST-01.02` Source Lock and the capsule-pinned declared-boundary input, an authorized human can approve, request revision, reject, or formally reopen the atomic boundary. Approval atomically produces a frozen versioned boundary, attributable `AtomicityRatification`, transparent `DraftHarnessModel`, `HG-003=PASS`, lifecycle transition, observations, and deterministic receipt.

The model preserves explicit value, authority status, knowledge status, provenance, confidence/disposition, alternatives, gaps, decisions required, and `NOT_APPLICABLE` fields. Consumers that request unavailable authority fail closed. Revision and rejection preserve attributable history without freezing a model. Reopen preserves history, invalidates the former boundary/model, and requires a new immutable version.

## Implementation boundary

Builder-owned implementation is limited to:

- typed atomicity, decision, boundary, model, invalidation, readiness, and receipt contracts;
- human-only decision/reopen command handling;
- repository-local, hash-verified declared-input loading;
- atomic development/test persistence, idempotency, optimistic concurrency, replay, and injected-failure seams;
- additive run references/events and synthetic-profile lifecycle support;
- deterministic Story observations and completion evidence.

No schema, database, migration, dependency, external runtime, provider, evaluator, production content, publication, or task-execution behavior was added. Format 02, VAE, Delegation runtime, GPU/ComfyUI, conversational activation, and later Stories remain outside this implementation.

## Requirements and acceptance

Owned obligations `FR-036` through `FR-040` and hard gate `HG-003` pass. Acceptance criteria `AC-01` through `AC-11` pass through the Story tests and full regression. Human authority owns semantic decisions; deterministic code validates, compiles, hashes, persists, replays, and emits receipts.

## Files

The exact 17 implementation paths and their hashes are recorded in `FILE_CHANGE_MANIFEST.yaml`. Two capsule authorization outputs were updated only to record the supplied exact phrase and granted bounded state. The six completion files are separate Story evidence.

## Validation summary

- Capsule immutable inputs: `19/19 PASS`
- Capsule bundle digest: `PASS`
- Preimplementation regression: `57/57 PASS`
- Test-first red seam: `5` expected collection errors before the three new source modules existed
- ST-02.05 suite: `27/27 PASS`, including two deterministic fresh-context reruns
- Prior isolated suites: `20/20`, `18/18`, and `19/19 PASS`
- Full repository regression: `84/84 PASS`
- Architecture-boundary subset: `10/10 PASS`
- Skipped mandatory tests: `0`
- Exact allowlist: `PASS`
- External dependencies added: none
- Prohibited files changed: none

The only warning is the pre-existing `pytest-asyncio` default-loop-scope deprecation notice; it does not alter results or Story behavior.

## Limitations

This is an in-memory development/test implementation for the repository-owned synthetic Builder Core path. It does not execute a Harness, compile canonical Harness IR, claim certification, or authorize production. `ST-03.03` requires a separate readiness decision, capsule, and human authorization.
