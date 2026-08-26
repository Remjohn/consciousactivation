# CAE Governance 02 Ratification Register

**Phase ID:** `CA-GOV-02`  
**Document ID:** `CAE_GOV_02_RATIFICATION_REGISTER`  
**Status:** `OPERATOR_REVIEW`  
**Date:** 2026-08-26  
**Governing Mandate:** `docs/cae/gemini_execution/14_CA_GOV_02_RATIFICATION_AND_CONTROL_STATE_MANDATE.md`  

---

## 1. Governance Principles and Decision Vocabulary

This register reconciles the governance status of all authored specifications, constitutions, requirements, migration contracts, and implementation milestones.

### Four Independent Evaluation Axes
1. **Artifact Ratification:** `DRAFT` $\rightarrow$ `REVIEWED` $\rightarrow$ `OPERATOR_RATIFIED` $\rightarrow$ `SUPERSEDED` / `RETIRED`
2. **Implementation Verification:** `NOT_IMPLEMENTED` $\rightarrow$ `IMPLEMENTED` $\rightarrow$ `VERIFIED_LOCAL` $\rightarrow$ `VERIFIED_E3_RECORDED`
3. **Operational Authority:** `LEGACY_AUTHORITATIVE_SQLITE` / `DUAL_VERIFY` $\rightarrow$ `POSTGRES_AUTHORITATIVE_STAGING_ONLY`
4. **Environment Class:** `LOCAL` / `STAGING` $\rightarrow$ `PRODUCTION`

### Permitted Dispositions (Strict Subset)
- `RECORDED_RATIFIED`: An explicit, attributable operator decision exists in the record with documented scope, date, and artifact hash.
- `PENDING_OPERATOR_RATIFICATION`: Authored and validated artifact awaiting formal operator ratification in `CA-GOV-02`.
- `DEFERRED`: Explicitly declared out-of-scope domain held for future planned phases.
- `HISTORICAL_RESOLVED`: Prior pending state that was subsequently resolved by a recorded downstream decision.
- `SUPERSEDED`: Historical artifact or decision replaced by a newer version.
- `CONTRADICTORY`: Material divergence between documents that cannot be silently resolved.
- `REJECTED`: Explicitly rejected proposal.
- `NOT_APPLICABLE`: Structural or non-decisional entry.

---

## 2. Comprehensive Ratification Ledger

| decision_id | subject/version | current documented status | evidence reference | decision type | eligible decision owner | proposed disposition | operator decision record | effective date | supersedes / preserves | implementation relationship | authority/environment boundary | open risk | next permitted phase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `DEC-GOV-MAP-01` | Scope & Authority Matrix v1.0 (`CAE_SCOPE_AND_AUTHORITY_MATRIX.md`) | `REVIEWED_PASS` | `scripts/cae/verify_ca_map_01.py` | Scope & Plane Mapping | System Architect / Operator | `PENDING_OPERATOR_RATIFICATION` | PENDING | 2026-08-26 | Preserves WP-01 role ontology; supersedes unmapped brownfield assumptions | Implemented via tenancy models | LOCAL / STAGING / PROD (Logical Doctrine) | Unratified boundary drift | `CA-GOV-02` |
| `DEC-GOV-AUTH-01` | Authoring Controls & 7 Skills v1.0 (`docs/cae/authoring_skills/`) | `REVIEWED_PASS` | `scripts/cae/authoring/verify_authoring_skills.py` | Governance Authoring Tools | Process Custodian / Operator | `PENDING_OPERATOR_RATIFICATION` | PENDING | 2026-08-26 | Preserves skill packages; uncertified at runtime | Tooling only; no runtime authority | LOCAL ONLY | Accidental runtime invocation | `CA-GOV-02` |
| `DEC-GOV-CAN-01A` | Boundary & Access Constitutions (6 YAMLs) v1.0 (`docs/cae/constitutions/CA-CAN-01A_*.yaml`) | `REVIEWED_PASS` | `CAE_CA_CAN_01A_CONSTITUTION_REVIEW.md` | Object Constitution | Tenancy Architect / Operator | `PENDING_OPERATOR_RATIFICATION` | PENDING | 2026-08-26 | Formalizes OperatorOrg, Workspace, Membership, Engagement, Policy, Grant | Implemented in `models/tenancy.py` & DDL | LOCAL / STAGING ONLY | Single-column FK on grants | `CA-GOV-02` |
| `DEC-GOV-CAN-01B` | Guest & Media Constitutions (5 YAMLs) v1.0 (`docs/cae/constitutions/CA-CAN-01B_*.yaml`) | `REVIEWED_PASS` | `CAE_CA_CAN_01B_CONSTITUTION_REVIEW.md` | Object Constitution | Domain Custodian / Operator | `PENDING_OPERATOR_RATIFICATION` | PENDING | 2026-08-26 | Formalizes Guest, Profile, CampaignGuest, MediaAsset, Lineage | Implemented in `models/tenancy.py` & DDL | LOCAL / STAGING ONLY | Brownfield SQLite guest duality | `CA-GOV-02` |
| `DEC-GOV-CAN-01C` | Harness & Receipt Constitutions (4 YAMLs) v1.0 (`docs/cae/constitutions/CA-CAN-01C_*.yaml`) | `REVIEWED_PASS` | `CAE_CA_CAN_01C_CONSTITUTION_AND_RELATION_REVIEW.md` | Object Constitution | Pipeline Architect / Operator | `PENDING_OPERATOR_RATIFICATION` | PENDING | 2026-08-26 | Formalizes HarnessTemplate, HarnessRun, Receipt, Contradiction Closure | Implemented in `models/tenancy.py` & DDL | LOCAL / STAGING ONLY | `F-01` single-column receipt FK | `CA-GOV-02` |
| `DEC-GOV-SPEC-01` | Operational PRD & 15 FRs v1.0 (`PRD-CAE-TEN-001`, `docs/cae/specs/fr/`) | `REVIEWED_PASS` | `CAE_CA_SPEC_01_RECONCILIATION_AND_REVIEW.md` | Functional Requirements | Product Owner / Operator | `PENDING_OPERATOR_RATIFICATION` | PENDING | 2026-08-26 | Bridges PRD/CURRENT.md to tenant operational slice | Guides `TenantScopedSemanticOperations` | LOCAL / STAGING ONLY | Scope forgery bypass via raw SQL | `CA-GOV-02` |
| `DEC-GOV-STATE-01` | Aggregate Authority Matrix & 7 Contracts v1.0 (`docs/cae/state/`) | `REVIEWED_PASS` | `CAE_CA_STATE_01_RECONCILIATION_AND_REVIEW.md` | State Authority Contracts | State Architect / Operator | `PENDING_OPERATOR_RATIFICATION` | PENDING | 2026-08-26 | Defines 22 aggregate progression stages | Directs cutover orchestration | LOCAL / STAGING ONLY | Premature unpromoted cutover | `CA-GOV-02` |
| `DEC-GOV-TS-01` | Tech Spec & Gate A–I Review v1.0 (`TS-CAE-TEN-001`) | `REVIEWED_PASS` | `CAE_CA_TS_01_RECONCILIATION_AND_REVIEW.md` | Technical Specification | Lead Engineer / Operator | `PENDING_OPERATOR_RATIFICATION` | PENDING | 2026-08-26 | 14-section specification; Gate A–I passed | Directs CA-IMPL-01A/01B/02 implementation | LOCAL / STAGING ONLY | DDL drift from specification | `CA-GOV-02` |
| `DEC-GOV-IMPL-01A` | Tenant Foundation Staging Verification (`CAE_CA_IMPL_01A_FOUNDATION_PROOF.md`) | `VERIFIED_E3_RECORDED` | `verify_ca_impl_01a_staging.py` | Foundation Infrastructure | Infrastructure Lead / Operator | `HISTORICAL_RESOLVED` | `OPERATOR_SECTION6_PROMOTE_APPROVED_2026-08-25` | 2026-08-25 | Established staging DDL, Pydantic models, RLS policies | Implemented in PostgreSQL staging | STAGING ONLY | Schema recreation script `F-04` | `CA-GOV-02` |
| `DEC-GOV-IMPL-01B` | Typed Runtime Path & E3 Staging Proof (`CAE_CA_IMPL_01B_TYPED_RUNTIME_AND_E3_PROOF.md`) | `VERIFIED_E3_RECORDED` | `verify_ca_impl_01b_staging.py` | Runtime Operations | Runtime Architect / Operator | `HISTORICAL_RESOLVED` | `OPERATOR_SECTION6_PROMOTE_APPROVED_2026-08-25` | 2026-08-25 | 10 strongly-typed operations, fresh-read SHA-256 | Implemented in `operations/tenant_scoped.py` | STAGING ONLY | API bypass (`F-03`) | `CA-GOV-02` |
| `DEC-GOV-IMPL-02` | One-Aggregate Cutover Execution Proof (`CAE_CA_IMPL_02_MC_CAE_MED_001_CUTOVER_PROOF.md`) | `VERIFIED_E3_RECORDED` | `rcpt_cae_receipt_commit_53b744f7ad35f3998ea6937e` | Cutover Verification | Migration Lead / Operator | `HISTORICAL_RESOLVED` | `OPERATOR_SECTION6_PROMOTE_APPROVED_2026-08-25` | 2026-08-25 | Cutover of `MC-CAE-MED-001` in two staging workspaces | Implemented in staging migration | STAGING ONLY | Table duality (`F-02`) | `CA-GOV-02` |
| `DEC-GOV-IMPL-02P` | Promotion of `MC-CAE-MED-001` to Staging Postgres Authority (`CAE_CA_IMPL_02P_PROMOTION_RECORD.md`) | `RECORDED_RATIFIED` | `rcpt_cae_receipt_commit_00c2b3f7341e59af1292fda7` | Operational Authority Promotion | Primary Operator | `RECORDED_RATIFIED` | `OPERATOR_SECTION6_PROMOTE_APPROVED_2026-08-25` | 2026-08-25 | Promoted `MC-CAE-MED-001` to `POSTGRES_AUTHORITATIVE_STAGING_ONLY` | Staging authority active for media only | STAGING ONLY (`MC-CAE-MED-001` ONLY) | Operator over-generalization risk | `CA-GOV-02` |
| `DEC-GOV-AUDIT-01` | Post-Execution Governance & Reality Audit (`CAE_POST_EXECUTION_GOVERNANCE_AUDIT.md`) | `RECORDED_RATIFIED` | `73837fc` / Operator YES | Audit & Evidence Reconciliation | Primary Operator | `RECORDED_RATIFIED` | `OPERATOR_ACCEPT_CA_AUDIT_01_2026-08-26` | 2026-08-26 | Authoritative Phase 1–12 baseline; zero authority mutated | Full audit verification passed | LOCAL / REPOSITORY TRUTH | Unratified spec sprawl | `CA-GOV-02` |
| `DEC-DEF-SQLITE-MIG` | Broad SQLite Database Retirement & Cutover | `DEFERRED` | `CAE_POSTGRES_MIGRATION_EXECUTION_PLAN.md` | Data Migration | Database Administrator / Operator | `DEFERRED` | DEFERRED_UNTIL_CA_MIG_03 | N/A | Preserves brownfield SQLite databases (`cmf_pipeline.db`, etc.) | Brownfield SQLite remains active authority | LOCAL BROWNFIELD | Data divergence during migration | `CA-MIG-03+` |
| `DEC-DEF-SFL-SDA-RUN` | SFL/SDA Failure Taxonomy Runtime Migration | `DEFERRED` | `CAE_WP04_REGISTRY_MIGRATION_PROOF.md` | Registry Authority | Registry Custodian / Operator | `DEFERRED` | DEFERRED_UNTIL_REGISTRY_CLEANUP | N/A | Quarantines 5 missing families and duplicate primitive | Registries in staging snapshot only | STAGING SNAPSHOT ONLY | Upstream lineage defect | `CA-REG-01+` |
| `DEC-DEF-SEM-ENG` | Generic CAE Semantic Engine & StateM Gateway | `DEFERRED` | `CAE_OBJECT_ONTOLOGY_RECONCILIATION.md` | Architecture Promotion | Architecture Lead / Operator | `DEFERRED` | DEFERRED_UNTIL_VERTICAL_SLICES_COMPLETE | N/A | StateM retained as reference semantics only | Local state machines in services | LOCAL SERVICES | Premature abstraction | `CA-STATE-02+` |
| `DEC-DEF-PROD-AUTH` | Production Environment Cutover & Routing | `DEFERRED` | `TS-CAE-TEN-001` Section 14 | Production Authority | Principal Operator | `DEFERRED` | DEFERRED_UNTIL_PROD_READINESS_GATE | N/A | Production authority strictly unauthorized | Staging testbed only | PRODUCTION AUTHORIZED: NO | Staging-to-prod assumption | `CA-PROD-01+` |
| `DEC-DEF-E4-TASTE` | E4 Operator Taste & Aesthetic Verdict Proof | `DEFERRED` | `TS-CAE-TEN-001` Section 11 | Quality & Safety Governance | Lead Producer / Operator | `DEFERRED` | DEFERRED_UNTIL_E4_PROTOCOL | N/A | Taste integrity defaults to `NOT_APPLICABLE` | Receipts prove mechanical facts only | LOCAL / STAGING | Reward hacking / vanity metrics | `CA-EVAL-01+` |

---

## 3. Findings Allocation and Ownership

| Finding ID | Title / Nature | Root Cause | Safety Guard Active | Planned Owner Phase |
|---|---|---|---|---|
| `F-01` | Single-Column FK on Lineage Link | CA-IMPL-01A DDL referenced `receipt_id` without `workspace_id` | Enforced in Python typed runtime path (`TenantScopedSemanticOperations`) | `CA-MIG-03` (Forward-only composite FK migration) |
| `F-02` | Staging Schema Table Name Duality | WP-03 text-keyed tables shadow CA-IMPL-01B uuid-keyed tables | Bypassed via explicit `verify_media_asset` typed runtime call | `CA-MIG-03` (Disposable migration & topology cleanup) |
| `F-03` | Brownfield API Router Disconnect | `api/routers/campaigns.py` not routed through typed context | Brownfield API explicitly bounded to SQLite operational authority | `CA-API-01` (Router contextual middleware integration) |
| `F-04` | Destructive Scaffolding Script | `apply_ca_impl_01a_scaffolding.py` drops and recreates schema | Script restricted to non-authoritative scratch initialization | `CA-MIG-03` (Non-destructive migration harness) |
| `F-05` | Quarantined SFL/Primitive Deficiencies | 5 missing families and duplicate primitive in inherited seeds | Explicitly quarantined; inaccessible to runtime operations | Lineage Governance / Upstream Seed Correction |
