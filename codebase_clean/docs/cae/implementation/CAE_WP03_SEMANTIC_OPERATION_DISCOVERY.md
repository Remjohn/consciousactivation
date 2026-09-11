# CAE WP-03 Semantic-Operation Discovery

**Work package:** WP-03 — State Transition and Semantic Operation Layer
**Status:** `RESOLVED_BY_WP03A_AND_EXECUTED_PENDING_OPERATOR_REVIEW`
**Date:** 2026-08-24

## Intended bounded slice

```text
source package / evidence span
  -> evidence captured
  -> evidence authenticated
  -> AIR semantic assessment validated
  -> operator-confirmed assessment
  -> command, event, transition, and receipt evidence
```

The intended typed operations are:

| Operation | Transition contract | Authoritative effect | Required independent evidence |
|---|---|---|---|
| `cae.evidence.authenticate@1.0.0` | `STC-EVID-001` | `evidence_item: CAPTURED -> AUTHENTICATED` | verified source package/spans plus evaluator distinct from capture actor |
| `cae.air.validate_assessment@1.0.0` | `STC-AIR-001` | `semantic_assessment: PROPOSED -> VALIDATED` | authenticated evidence links, AIR validator/version, resolvable registry snapshots |
| `cae.air.confirm_assessment@1.0.0` | `STC-AIR-002` | validated assessment becomes operator-confirmed for downstream use | named operator decision and reviewed evidence set |

## Discovery requiring a contract decision

The staging foundation currently stores only `payload_sha256` in `cae.command` and `cae.event`, and only an evidence-summary hash in `cae.receipt`. It does not retain the corresponding canonical command payload, event payload, or receipt/evidence envelope.

That is not sufficient for CAE's required immutable historical record, replayability, receipt inspection, or independent anti-reward-hack review. A hash proves equality only when the underlying canonical bytes are retained and available for comparison.

## Proposed controlled amendment: WP-03A

Add an expand-only migration before registering or executing the first typed operation:

| Table | New required field | Role |
|---|---|---|
| `cae.command` | `payload jsonb NOT NULL` | canonical typed operation input, actor context, and idempotency context |
| `cae.event` | `payload jsonb NOT NULL` | immutable transition/effect representation |
| `cae.receipt` | `payload jsonb NOT NULL` | outcome, evidence/decision refs, verifier identity, and proof classification |

The existing SHA-256 fields remain and must equal the canonical JSON hash of their respective payload/envelope. The migration must add check/trigger-level enforcement through the operation service, structural tests, and a rollback-only adversarial test that attempts a hash/payload mismatch.

No existing CAE operational records have been imported, and the WP-02a staging proof left no fixture records, so this is an expand-only model correction rather than data migration. This assertion must be reverified immediately before applying the amendment.

## Resolution

The operator authorized WP-03A. Migration `0003_cae_immutable_evidence_payloads` was applied to the otherwise empty staging evidence tables. It adds canonical JSON text and JSONB payloads to commands, events, and receipts; database triggers reject a payload whose canonical SHA-256 does not match, and reject update/delete mutation after insertion.

Migration `0004_cae_first_slice_semantic_operations` then registered the five bounded operations and their five transition contracts. The full first slice was executed against staging in a forced-rollback transaction, with an independently uploaded private source object deleted at the end. Its detailed result is recorded in `CAE_WP03_SEMANTIC_OPERATION_PROOF.md`.

This resolves the persistent-evidence contract gap for the bounded slice only. It does not create a runtime SDA/SFL/Primitive registry resolver, and no validation result may be represented as a resolved CAE semantic-direction judgment until WP-04 supplies that authority.

## Exact decision required

**Promote WP-03 and authorize WP-04 to reconcile and migrate the inherited SDA, SFL, and Primitive registries as lineage-preserving registry inputs—without inventing missing SFL family records or rerouting existing services?**
