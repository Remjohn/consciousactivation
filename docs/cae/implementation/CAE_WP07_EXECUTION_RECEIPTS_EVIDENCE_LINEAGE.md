# CAE WP-07 — Execution Receipts and Evidence Lineage

**Status:** `COMPLETE_PENDING_OPERATOR_REVIEW`  
**Work package:** WP-07 — execution receipts + evidence lineage  
**Environment:** disposable Supabase/PostgreSQL staging only (`E3_PRODUCTION_SHAPED`); no legacy service cutover or record migration.

## Objective and boundary

Extend the existing immutable command/event/receipt envelope so each first-slice
operation records the environment and evaluation boundaries it actually used,
and so its relation to independent evidence is queryable. PostgreSQL/Supabase
remains the sole durable state and history authority. The runbook remains
procedural doctrine only.

Allowed changes were the CAE staging schema, the bounded WP-03 semantic adapter,
its proof path, and CAE implementation records. The package does not change
legacy SQLite authority, a service/API route, Builder/Pipeline execution,
registry resolution, media bytes, or CAE ontology.

## Implemented contract

Migration `0008_cae_execution_receipt_lineage.sql` adds three append-only
objects:

| Object | Role | Boundary |
|---|---|---|
| `cae.execution_receipt` | one immutable, context-bearing extension per existing `cae.receipt` | identifies a transition claim, snapshots, environment, evaluator/validator result fields, and explicit unverified gates |
| `cae.receipt_evidence_link` | immutable many-to-many evidence lineage | points only to canonical `cae.evidence_item` rows; a database FK rejects invented evidence IDs |
| `cae.v_receipt_evidence_lineage` | read-only, security-invoker lineage projection | exposes receipt → evidence → source package → source media identity and hash; it stores no state |

`FirstSliceSemanticOperations._transition()` writes command, aggregate update,
transition, event, envelope receipt, execution receipt, and evidence links in
the same transaction. A transaction failure leaves no partial lineage.

The five current operation mappings are intentionally narrow:

| Operation | Claim ID | Lineage role |
|---|---|---|
| `cae.evidence.capture@1.0.0` | `CAE-EVID-001.capture-traceability` | `CREATED` |
| `cae.evidence.authenticate@1.0.0` | `CAE-EVID-001.authentication-lineage` | `AUTHENTICATES` |
| `cae.air.propose-assessment@1.0.0` | `CAE-EVID-001.assessment-evidence-linkage` | `SUPPORTS` |
| `cae.air.validate-assessment@1.0.0` | `CAE-EVID-001.assessment-validation-lineage` | `VALIDATES` |
| `cae.air.confirm-assessment@1.0.0` | `CAE-EVID-001.operator-confirmation-lineage` | `CONFIRMS` |

All five operations presently set `registry_scope: NOT_READ` and null registry
snapshot hash. This prevents a receipt from implying SDA/SFL/Primitive use
before a later runtime integration consumes the resolver.

## Evaluation and non-claim discipline

Each execution receipt records an input snapshot hash, output snapshot hash,
environment identity, semantic-operation version, contract-precondition result,
and independent-evidence/decision result. It deliberately records:

```yaml
reward_hack_result: UNVERIFIED
taste_integrity_result: NOT_APPLICABLE
anti_centroid_result: NOT_APPLICABLE
evidence_status: TRACEABLE
```

`TRACEABLE` means the transition has database-backed lineage to evidence. It
does **not** mean that the receipt independently proves the source claim,
semantic correctness, human truth, taste, anti-centroid quality, or E4 outcome.
Those claims remain unverified until their validators and independent evidence
are introduced in their own bounded work package.

## Evidence and verification

The guarded migration checks that `cae.receipt` is empty before applying: a
non-empty historical envelope requires a separate backfill/reconciliation
decision rather than silent partial coverage.

```yaml
migration_version: 0008_cae_execution_receipt_lineage
migration_checksum_sha256: 8902468b434dd8dc081446d138d3305ff5c55f9f419d89dce8f81956ac0083cc
preflight_existing_receipt_count: 0
apply_result: APPLIED
proof_environment: E3_PRODUCTION_SHAPED / staging_only
proof_persistence: force-rolled-back database fixture; temporary private storage object deleted
```

`scripts/cae/verify_wp07_receipt_lineage.py` exercised the actual five typed
operations against the registered staging PostgreSQL contracts and proved:

- atomic creation of five execution receipts and five receipt-to-evidence links;
- lineage projection to the verified source asset for the operator-confirmation receipt;
- idempotent replay, self-authentication rejection, stale-transition rejection,
  immutable command rejection, and hash mismatch rejection;
- execution-receipt mutation rejection and false evidence-reference rejection;
- explicit `NOT_READ` registry scope, staging identity, and no semantic/taste overclaim;
- cleanup of the temporary private source object.

| Test ID | Class | Claim | False-proof countertest | Result |
|---|---|---|---|---|
| `WP07-INT-001` | `INTEGRATION` / `EVIDENCE` | each committed first-slice transition has an immutable contextual receipt and evidence lineage | receipt count alone would pass while no evidence relation exists | PASS |
| `WP07-RH-001` | `REWARD_HACK` | a fabricated evidence reference cannot satisfy lineage presence | direct link to nonexistent evidence ID | PASS — FK rejects |
| `WP07-RH-002` | `REWARD_HACK` | receipt presence cannot be upgraded to semantic/taste proof | receipt fields must remain `UNVERIFIED` / `NOT_APPLICABLE` | PASS |
| `WP07-STATE-001` | `STATE` / `EVIDENCE` | historical context is immutable | direct execution-receipt update | PASS — trigger rejects |
| `WP07-ENV-001` | `ENVIRONMENT_FIDELITY` | receipt identifies its staging boundary and no unconsumed registry | non-null registry hash for a registry-free operation | PASS |

## Risks and next transition

This is a staging proof of one vertical slice, not deployment or production
service proof. Existing local SQLite receipts are unmodified and no API/runtime
consumer reads `v_receipt_evidence_lineage` yet. The first-slice operation
adapter has no semantic evaluator; the explicit unverified fields are therefore
correct, not a defect to conceal.

**Exact operator decision:** Promote WP-07 and authorize WP-08 to design and
execute bounded reality-contact, contrastive, and anti-reward-hacking tests for
the evidence-to-AIR first slice, without converting staging structural proof or
receipt lineage into a claim of semantic quality, taste, or real-world outcome.
