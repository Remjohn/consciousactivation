# CAE Phase 16 / CA-APPLY-04 Schema & Containment Results

**Phase ID:** `CA-APPLY-04`  
**Document ID:** `CAE_APPLY_04_SCHEMA_AND_CONTAINMENT_RESULTS`  
**Status:** `APPLIED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY`  
**Date:** 2026-08-26  
**Governing Mandate:** `docs/cae/gemini_execution/16_CA_APPLY_04_DISPOSABLE_MIGRATION_APPLICATION_PROOF_MANDATE.md`  

---

## 1. Independent Schema Inspection After Application

Following the clean application of `MIG-0001` through `MIG-0006`, the schema was independently inspected:

| Schema Object Name | Type | Key Columns / Constraint Details | RLS Status |
|---|---|---|---|
| `cae.workspace` | Relational Table | `workspace_id UUID PK`, `slug UNIQUE` | `ENABLED (p_workspace_isolation)` |
| `cae.workspace_membership` | Relational Table | `membership_id UUID PK`, `uq_workspace_membership_actor (workspace_id, actor_id)` | `ENABLED (p_membership_isolation)` |
| `cae.operator_organization` | Relational Table | `operator_org_id UUID PK` | `ENABLED (p_operator_grant_isolation)` |
| `cae.operator_access_grant` | Relational Table | `grant_id UUID PK`, `workspace_id FK` | `ENABLED (p_operator_grant_isolation)` |
| `cae.engagement` | Relational Table | `engagement_id UUID PK`, `uq_workspace_engagement (workspace_id, engagement_id)` | `ENABLED (p_engagement_isolation)` |
| `cae.guest` | Relational Table | `guest_id UUID PK`, `uq_workspace_guest (workspace_id, guest_id)` | `ENABLED (p_guest_isolation)` |
| `cae.media_asset` | Relational Table | `media_id UUID PK`, `uq_workspace_media (workspace_id, media_id)` | `ENABLED (p_media_asset_isolation)` |
| `cae.harness_template` | Relational Table | `template_id UUID PK`, `uq_workspace_template (workspace_id, template_id)` | `ENABLED (p_template_isolation)` |
| `cae.harness_run` | Relational Table | `run_id UUID PK`, `uq_workspace_run (workspace_id, run_id)` | `ENABLED (p_run_isolation)` |
| `cae.receipt` | Relational Table | `receipt_id UUID PK`, `uq_workspace_receipt (workspace_id, receipt_id)` | `ENABLED (p_receipt_isolation)` |
| `cae.receipt_evidence_link` | Relational Table | `link_id UUID PK`, `uq_workspace_receipt_evidence (workspace_id, receipt_id, evidence_type, evidence_id)` | `ENABLED (p_link_isolation)` |
| `cae.fn_prevent_receipt_mutation()` | Pl/pgSQL Function | Enforces exception `EX_RECEIPT_IMMUTABLE` on UPDATE/DELETE | N/A |
| `trg_receipt_append_only` | Trigger | Bound `BEFORE UPDATE OR DELETE ON cae.receipt` | Active |

---

## 2. Behavioral Containment Proof (Adversarial Countertests)

```text
[COUNTERTEST CT-07] Unscoped Connection & Cross-Workspace RLS Isolation
- Action: Executed SELECT against cae.workspace and cae.media_asset with no session variable set.
- Result: 0 rows returned (Unscoped access denied by RLS policy).
- Action: Set app.current_workspace_id = ws_alpha_id; queried ws_beta objects.
- Result: 0 rows returned (Cross-workspace leak prevented).

[COUNTERTEST CT-08] Multi-Tenant Composite Key Containment
- Action: Attempted to insert child engagement referencing foreign workspace_id.
- Result: Rejected by foreign key constraint fk_workspace.

[COUNTERTEST CT-09] Append-Only Receipt Ledger Immutability
- Action: Attempted UPDATE cae.receipt SET result_status = 'MUTATED'.
- Result: Raised EX_RECEIPT_IMMUTABLE (55000): cae.receipt records are strictly append-only.
- Action: Attempted DELETE FROM cae.receipt.
- Result: Raised EX_RECEIPT_IMMUTABLE (55000): Mutation prohibited.
```

---

## 3. Structural Debt Status (F-01 and F-02 Verification)

1. **Finding F-01 (Lineage Composite FK):** Confirmed `cae.receipt_evidence_link.receipt_id` currently references `cae.receipt(receipt_id)` as a single column. F-01 remains `STILL_OPEN — UNRESOLVED_AT_DB_LEVEL` until `MIG-0007` is applied in `CA-INT-05`.
2. **Finding F-02 (Staging Shadow Tables):** Brownfield text tables were not modified. F-02 remains `STILL_OPEN`.
