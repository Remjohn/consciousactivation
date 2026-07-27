# BQA P0/P1 Trust Correction Implementation Report

Verdict: `PASS`

## Authorized boundary

This implementation applies only `BQA-P0-P1-TRUST-CORRECTION`. It restores
previously governed Builder invariants under the existing Constitution V1.1,
Builder PRD V1.2, confirmed Stories and schemas. No authority text, shared
contract, schema, dependency, external product, production claim or certification
claim changed.

## Defects reproduced and corrected

| Finding | Pre-correction reproduction | Smallest sufficient repair |
|---|---|---|
| `BQA-P0-001` | A material definition semantic or section projection could be rewritten, recanonicalized, rehashed and accepted. | Definition validation now reconstructs fixed semantics and all 20 section projections, binds every upstream reference to active governed objects, binds compiler actor to the immutable attachment and receipt, verifies the pinned definition input, and requires current deterministic-code authority before target validation. Repository commit repeats the structural/upstream binding. |
| `BQA-P1-003` | A sink exception after the validation commit raised to the caller and falsely attempted a `NOT_COMMITTED` rejection. | Ten deterministic observation intents commit atomically with report, receipt, event and command record. A synchronized pending/in-flight/delivered outbox drains after commit. Delivery failure leaves queryable pending evidence and returns the committed receipt; duplicate invocation retries only pending intents. |
| `BQA-P1-004` | Two same-version writers could both return success while one accepted event was lost. | All in-memory stream-writing commits now hold one reentrant transaction lock from version comparison through validation and assignment. The atomic lifecycle command retains exactly one winner event and matching command record. |
| `BQA-P1-005` | Lifecycle events and optional checkpoints were stored before their receipt-bearing command record. | Create, transition, waiver, checkpoint and resume now use one `commit_run_command` transaction. Three governed injected failure gates prove zero partial events, checkpoints or records and clean retry. |
| `BQA-P1-006` | ZIP candidate hash came from one read while member descriptors came from a reopened path. | ZIP hashing and member inspection now consume the same immutable byte buffer through `BytesIO`; all existing member and resource-safety checks remain active. |

## Affected-artifact revalidation report

- Original Story Completion Receipts for `ST-01.01`, `ST-01.02`, `ST-07.02`
  and `ST-07.04` remain byte-identical at their governed hashes. They are retained
  as historical completion evidence and are not rewritten.
- Current active synthetic definition, target-validation report, receipts,
  observation evidence and generated Development Capsule were reconstructed in
  fresh test contexts from governed inputs. Semantic authority, complete lineage,
  deterministic identity, replay, idempotency, invalidation and rollback all pass.
- The former final integration-gate `FAIL` is superseded by the separate correction
  and integration-gate receipts in this completion directory. Historical audit
  findings remain preserved in `_PARALLEL_REPORTS`; their current disposition is
  derived from the new regression evidence.
- No persisted active product artifact required destructive mutation. Test/development
  in-memory descendants are rebuilt from their immutable parents; the historical
  instances remain reproducible.

## Validation summary

- Pre-correction full regression: `475/475 PASS`.
- Red correction reproduction: `109 failed, 3 passed`, exhibiting all five defects.
- Correction-specific suite, fresh process 1: `125/125 PASS`.
- Correction-specific suite, fresh process 2: `125/125 PASS`.
- Unchanged affected predecessor suites: `128/128 PASS`.
- Complete repository regression, fresh process 1: `600/600 PASS`.
- Complete repository regression, fresh process 2: `600/600 PASS`.
- Python source compilation without bytecode writes: `178/178 PASS`.
- Mandatory skips: `0`.
- Capsule immutable inputs: `18/18 PASS`.
- Original affected receipt hashes: `4/4 PASS`.

`BQA-P2-007`, `BQA-P2-008`, `BQA-P2-009` and `BQA-P3-010` remain deferred,
non-P0/P1 productization findings. They were not silently resolved by this package.
