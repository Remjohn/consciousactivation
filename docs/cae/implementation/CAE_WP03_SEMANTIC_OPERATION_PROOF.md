# CAE WP-03 First-Slice Semantic-Operation Proof

**Work package:** WP-03 — State Transition and Semantic Operation Layer
**Status:** `COMPLETE_PENDING_OPERATOR_REVIEW`
**Environment:** Supabase staging PostgreSQL 17.6 and private `cae-media` Storage bucket
**Date:** 2026-08-24

## Bounded objective

Prove one authorized, evidence-bearing transition slice without importing legacy data, redirecting a running service, or claiming registry-derived semantic direction:

```text
verified private source asset
  -> evidence captured
  -> independently authenticated
  -> assessment proposed
  -> assessment validated
  -> operator-confirmed assessment
```

## What changed and why

1. `0003_cae_immutable_evidence_payloads` was applied after proving the three evidence tables were empty. It adds canonical JSON text and JSONB payloads to `cae.command`, `cae.event`, and `cae.receipt`, preserving their SHA-256 values. Database triggers reject canonical-text/hash/payload disagreement and reject later mutation or deletion.
2. `0004_cae_first_slice_semantic_operations` registered five typed operations and contracts `STC-EVID-000`, `STC-EVID-001`, `STC-AIR-000`, `STC-AIR-001`, and `STC-AIR-002`.
3. `ca_runtime.semantic_operations.FirstSliceSemanticOperations` provides the bounded PostgreSQL adapter. Each operation atomically writes its command, state transition, event, and receipt. It is intentionally not wired into existing API or SQLite service paths.

## Registration evidence

| Migration | SHA-256 | Result |
|---|---|---|
| `0003_cae_immutable_evidence_payloads` | `3d331989fd74af1ccfec71d6087b481f4369debe5045d4e7d4dbaed1c1373124` | Applied to staging |
| `0004_cae_first_slice_semantic_operations` | `ad6ccc6f08d3e46cfdff42fc9a2be52b9998eea4c62a21fa9c044c5a4c69df8d` | Applied to staging |

## Executed proof

`python scripts/cae/verify_wp03_first_slice.py` executed against the approved Supavisor session-pooler URL. It uploaded one unique text object to the private `cae-media` bucket, then created every database fixture inside a forced-rollback transaction. The object was deleted in `finally` after the test.

| Check | Result | What it falsifies |
|---|---|---|
| Capture transition | PASS | An evidence aggregate cannot merely be declared captured without transition artifacts. |
| Idempotent replay | PASS | A repeated command does not duplicate the transition. |
| Self-authentication rejection | PASS | Capture actor cannot self-attest authentication. |
| Authentication transition | PASS | Independent authentication creates the guarded state change. |
| Proposal / validation / operator confirmation | PASS | The intended state sequence and expected versions execute only in order. |
| Stale transition rejection | PASS | An obsolete expected version cannot advance state. |
| Event and receipt count | PASS (5 each) | A state change cannot pass while silently omitting its event or receipt. |
| Direct command update rejection | PASS | Stored evidence cannot be rewritten after insertion. |
| Hash/payload mismatch rejection | PASS | A valid-looking hash cannot be paired with different stored payload bytes. |
| Temporary source cleanup | PASS | The proof did not leave its storage object behind. |

## What was proven

- Staging PostgreSQL is the durable authority for this isolated transition slice.
- The five registered operation/contract pairs can enforce actor distinction, authenticated-evidence preconditions, optimistic concurrency, idempotency, operator confirmation, immutable historical records, and receipt creation as one transaction.
- The proof exercised real private Supabase Storage for the source object's existence and cleanup. Database fixtures were rolled back, so no proof data or legacy record was retained.

## What was not proven

- Existing API and local SQLite services still use their current paths; no write authority was cut over.
- No legacy data was migrated, dual-read, or reconciled.
- No SDA, SFL, or Primitive registry was imported or resolved. The validation operation proves lifecycle governance only; it does **not** prove a valid semantic-direction decision.
- Authentication relies on the supplied evaluator identity and evidence span relation; external human-review UI and role provisioning remain later work.
- This is staging E3-style integration evidence, not production E4 reality-contact evidence.

## Remaining risks and inspection targets

- Inspect the operation/contract names and authority boundary in `sql/0004_cae_first_slice_semantic_operations.sql`.
- Inspect the immutable trigger design in `sql/0003_cae_immutable_evidence_payloads.sql` before adding any future writer.
- Registry authority remains blocked by the known SFL missing-family references. WP-04 must preserve original IDs, versions, hashes, sources, and crosswalks, while quarantining rather than synthesizing missing definitions.
- The receipt itself is database evidence, not independent proof that an external evaluator's judgment was correct; later reality-contact testing must keep that distinction.

## Exact operator decision

**Promote WP-03 and authorize WP-04 to reconcile and migrate the inherited SDA, SFL, and Primitive registries as lineage-preserving registry inputs—without inventing missing SFL family records or rerouting existing services?**
