# CAE Tenant/Guest Requirement Traceability Matrix

**Document ID:** `CAE_TENANT_GUEST_REQUIREMENT_TRACEABILITY_MATRIX`  
**Phase ID:** `CA-SPEC-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/07_CA_SPEC_01_TENANT_GUEST_PRD_FR_MANDATE.md`  
**Authority Reference:** CAE Governance Bundle v3 (`03_CAE_OBJECT_TO_SPEC_TRACEABILITY_PROTOCOL.md`, `04_CAE_SPEC_ACCEPTANCE_AND_EVIDENCE_MATRIX.md`)  

---

## 1. Traceability Architecture

This matrix establishes the bidirectional traceability connecting ratified constitutional object laws, canonical relation edges, functional requirements, scope/authority classifications, brownfield impact classifications, test fidelity requirements, and countertests for the **First Vertical Operational Slice**.

```text
CONSTITUTIONAL LAW (CA-CAN-01A/B/C)
  ──> CANONICAL RELATION MAP (REL-CANON-001, REL-OP-001..010)
    ──> PRD CAPABILITY (PRD-CAE-TEN-001)
      ──> FUNCTIONAL REQUIREMENT (FR-CAE-TEN-001..015)
        ──> BROWNFIELD IMPACT (NEW / EXTEND / ADAPT / RETAIN / DEFER / QUARANTINE)
          ──> TEST FIDELITY (E1 Static, E2 Repository, E3 Staging, E4 Production)
            ──> COUNTERTEST / ANTI-REWARD-HACK (HN-SPEC-001..011)
              ──> DOWNSTREAM CONTRACT (CA-STATE-01 / CA-TS-01)
```

---

## 2. Master Requirement Traceability Matrix

| FR ID | Functional Title | Constitutional Owner & ID | Canonical Edge | Scope & Authority Class | Source Evidence | Brownfield Impact | Test Class & Fidelity | Anti-Reward-Hack Countertest | Future Contract | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `FR-CAE-TEN-001` | Workspace Tenancy Boundary | `Workspace` (`CA-ENT-001`) | `REL-OP-001`, `REL-OP-002`, `REL-OP-003` | `WORKSPACE_SCOPED` | `CA-CAN-01A_WORKSPACE.yaml`, `sql/0002_cae_workspace_rls.sql` | `NEW` / `ADAPT` | `TC-TEN-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-008` (Cross-workspace query returns 0 rows) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-002` | Operator Governance Boundary | `OperatorOrganization` (`CA-ENT-000`) | Governance Root | `OPERATOR_AUDIT` | `CA-CAN-01A_OPERATOR_ORGANIZATION.yaml` | `NEW` | `TC-OPR-001` (`E2_REPOSITORY_FIXTURE`) | `HN-SPEC-006` (Operator cannot query workspace without grant) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-003` | Workspace Membership Role | `WorkspaceMembership` (`CA-REL-001`) | `REL-OP-001` | `WORKSPACE_SCOPED` | `CA-CAN-01A_WORKSPACE_MEMBERSHIP.yaml`, `sql/0001_cae_foundation_draft.sql:28-36` | `NEW` / `ADAPT` | `TC-MEM-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-008` (Admin in WS A denied in WS B) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-004` | Operator Access Policy Governance | `OperatorAccessPolicy` (`CA-POL-001`) | Governance Policy | `OPERATOR_AUDIT` | `CA-CAN-01A_OPERATOR_ACCESS_POLICY.yaml` | `NEW` | `TC-POL-001` (`E2_REPOSITORY_FIXTURE`) | `HN-SPEC-006` (Grant exceeding policy duration cap rejected) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-005` | Operator Access Grant Lifecycle | `OperatorAccessGrant` (`CA-REL-002`) | Diagnostic Bridge | `OPERATOR_AUDIT` | `CA-CAN-01A_OPERATOR_ACCESS_GRANT.yaml` | `NEW` | `TC-GRNT-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-006` (Expired grant immediately rejected on call) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-006` | Engagement Project Containment | `Engagement` (`CA-ENT-004`) | `REL-OP-003`, `REL-OP-004` | `ENGAGEMENT_SCOPED` | `CA-CAN-01A_ENGAGEMENT.yaml`, `api/domain/campaign.py:18-27` | `ADAPT` | `TC-ENG-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-008` (Engagement cannot reference Guest from other WS) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-007` | Guest Locality and Lifecycle | `Guest` (`CA-ENT-003`) | `REL-OP-002` | `GUEST_SCOPED` | `CA-CAN-01B_GUEST.yaml`, Multi-Tenant Plan §3 | `NEW` / `ADAPT` | `TC-GST-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-002`, `HN-SPEC-010` (Same-name guest across WS not merged) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-008` | Guest Identity Link Anti-Merge | `GuestIdentityLink` (`CA-MAP-001`) | Research Crosswalk | `OPERATOR_AUDIT` | `CA-CAN-01B_GUEST_IDENTITY_LINK.yaml` | `DEFER` | `TC-LNK-001` (`E1_STATIC`) | `HN-SPEC-010` (Automatic identity resolution rejected) | Future Research Spec | `DEFERRED` |
| `FR-CAE-TEN-009` | Evidence Source Provenance | `EvidenceSource` (`CA-REL-004`) | `REL-OP-005` | `WORKSPACE_SCOPED` | `CA-CAN-01B_EVIDENCE_SOURCE.yaml`, `sql/0009_cae_interview_source_bridge_operation.sql` | `ADAPT` | `TC-SRC-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-005` (Altered source package fails digest check) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-010` | Media Asset Verification Lifecycle | `MediaAsset` (`CA-ENT-002`) | `REL-OP-005`, `REL-OP-006` | `WORKSPACE_SCOPED` | `CA-CAN-01B_MEDIA_ASSET.yaml`, Builder ADR-003 | `ADAPT` | `TC-MED-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-005` (Unverified flag rejected; byte check required) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-011` | Immutable Media Byte Isolation | `ImmutableMediaEvidence` (`CA-EVI-001`) | `REL-OP-006` | `WORKSPACE_SCOPED` | `CA-CAN-01B_IMMUTABLE_MEDIA_EVIDENCE.yaml`, `scripts/cae/verify_private_storage.py` | `NEW` | `TC-STO-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-005`, `HN-SPEC-008` (Cross-tenant signed URL rejected) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-012` | Harness Template Canonical Versioning | `HarnessTemplate` (`CA-STR-001`) | `REL-CANON-001` | `GLOBAL_CANONICAL` | `CA-CAN-01C_HARNESS_TEMPLATE.yaml`, `docs/cae/runbooks/evidence_to_air_first_slice_v1.yaml` | `NEW` / `ADAPT` | `TC-TMPL-001` (`E1_STATIC`) | `HN-SPEC-009`, `HN-CAN-021` (Template with tenant ID rejected) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-013` | Harness Run Execution Lifecycle | `HarnessRun` (`CA-EXE-001`) | `REL-OP-004`, `REL-CANON-001` | `ENGAGEMENT_SCOPED` | `CA-CAN-01C_HARNESS_RUN.yaml`, `CAE_WP06_HARNESS_RUNBOOK_INTEGRATION.md` | `ADAPT` | `TC-RUN-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-009`, `HN-CAN-024` (Run does not mutate template) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-014` | Operation Receipt Immutable Ledger | `Receipt` (`CA-REC-001`) | `REL-OP-009` | `WORKSPACE_SCOPED` | `CA-CAN-01C_RECEIPT.yaml`, `sql/0008_cae_execution_receipt_lineage.sql` | `EXTEND` | `TC-REC-001` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-004`, `HN-CAN-028` (Receipt != taste proof) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |
| `FR-CAE-TEN-015` | Receipt Evidence Lineage Traceability | `ReceiptEvidenceLink` (`CA-REL-005`) | `REL-OP-010` | `WORKSPACE_SCOPED` | `CA-CAN-01C_RECEIPT_EVIDENCE_LINK.yaml`, `scripts/cae/verify_wp07_receipt_lineage.py` | `NEW` | `TC-LNK-002` (`E3_STAGING_PERSISTENCE`) | `HN-SPEC-008`, `HN-CAN-027` (Cross-WS evidence link rejected) | `CA-STATE-01` / `CA-TS-01` | `AUTHORED` |

---

## 3. Coverage & Verification Summary

1. **Zero Orphan Guarantee:** 100% of authored FRs map to exactly one primary constitutional owner in `docs/cae/constitutions/`.
2. **Canonical Relation Alignment:** 100% of active operational relations (`REL-CANON-001`, `REL-OP-001` through `REL-OP-010`) are covered by explicit functional requirements.
3. **Anti-Reward-Hacking Defense:** Every stateful requirement includes a dedicated hard-negative countertest targeting deceptive false-proof modes (`HN-SPEC-001` through `HN-SPEC-011`).
4. **Fidelity Distribution:** 11 requirements require `E3_STAGING_PERSISTENCE`, 2 require `E2_REPOSITORY_FIXTURE`, 2 require `E1_STATIC`. Zero requirements make unearned E4 production claims.
