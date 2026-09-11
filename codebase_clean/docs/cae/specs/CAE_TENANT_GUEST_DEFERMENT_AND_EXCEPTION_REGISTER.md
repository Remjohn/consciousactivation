# CAE Tenant/Guest Deferment and Exception Register

**Document ID:** `CAE_TENANT_GUEST_DEFERMENT_AND_EXCEPTION_REGISTER`  
**Phase ID:** `CA-SPEC-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/07_CA_SPEC_01_TENANT_GUEST_PRD_FR_MANDATE.md`  
**Authority References:** `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`, `CAE_SCOPE_AND_AUTHORITY_MATRIX.md`, `CAE_CANONICAL_OPERATIONAL_PLANE_MAP.md`  

---

## 1. Executive Purpose

This register formally documents every deferred architectural decision, quarantined defect, out-of-scope capability, and boundary exception for the **First Vertical Operational Slice** (`PRD-CAE-TEN-001`).

It prevents the unratified introduction of unvetted features, maintains explicit boundary discipline, and ensures downstream implementation phases (`CA-STATE-01`, `CA-TS-01`, `CA-IMPL-01A/B`) do not implement deferred or quarantined scope under the guise of "future compatibility".

---

## 2. Contradiction & Collision Closures (CA-MAP-01 through CA-CAN-01C)

| Collision ID | Term / Domain | Competing Interpretations | Resolution & Status | Operational Boundary in First Slice |
|---|---|---|---|---|
| `COL-MAP-001` | `OperatorAccessPolicy` vs `OperatorAccessGrant` | Policy vs individual access session | `SPLIT & RATIFIED` | Separate global policy (`CA-POL-001`) from ephemeral, time-bounded, audited grant (`CA-REL-002`). |
| `COL-MAP-002` | `HarnessTemplate` vs `HarnessRun` | Procedural definition vs runtime state | `SPLIT & RATIFIED` | Template is stateless canonical grammar (`CA-STR-001`); Run is engagement-scoped operational execution (`CA-EXE-001`). |
| `COL-MAP-003` | `MediaAsset` vs `ImmutableMediaEvidence` | Relational metadata vs binary storage | `SPLIT & RATIFIED` | Asset is relational entity with lifecycle & SHA-256 (`CA-ENT-002`); Evidence is private object storage bytes (`CA-EVI-001`). |
| `COL-MAP-004` | `Receipt` as proof vs audit record | Execution log vs qualitative truth | `SPLIT & RATIFIED` | Receipt proves transactional commit (`CA-REC-001`); semantic evaluation requires independent evaluator records. |
| `COL-MAP-005` | `Guest` identity vs `GuestIdentityLink` | Local profile vs cross-tenant identity | `SPLIT & DEFERRED` | Guest is workspace-local (`CA-ENT-003`); cross-workspace link (`CA-MAP-001`) is an exceptional crosswalk with runtime execution `DEFERRED`. |
| `COL-MAP-006` | Single authority vs three authority axes | Conflating source, runtime, & promotion | `RESOLVED` | All objects declare Definition Source, Target Runtime Representation, and Promotion Authority separately. |
| `COL-MAP-007` | Tenancy Key (`guest_id` vs `workspace_id`) | Guest as tenant vs Workspace as tenant | `RESOLVED` | `workspace_id` is the sole tenant root; `guest_id` is workspace-local and never a universal partition key. |
| `COL-MAP-008` | Registry Authority (ZIP/YAML vs DB) | Unvetted files vs PostgreSQL projection | `RESOLVED` | ZIP/YAML bytes are migration inputs; PostgreSQL relational schema is target runtime authority. |
| `COL-CAN-009` | Runbooks vs Autonomous Agents | Bounded procedure vs general agent | `QUARANTINED` | Runbooks are bounded procedural doctrine for the first slice, not proof of general agent autonomy. |
| `COL-CAN-010` | Mechanical Log vs Semantic Proof | Operation receipt vs cognitive truth | `RATIFIED INVARIANT` | Anti-Self-Attestation law: mechanical receipts cannot prove subjective, qualitative, or taste validity. |
| `COL-CAN-011` | In-Flight Template Modification | Dynamic runbook edits during run | `QUARANTINED` | Templates are strictly immutable once published; in-flight mutations rejected. |
| `COL-CAN-012` | SQLite Cutover vs Coexistence | Immediate migration vs aggregate cutover | `DEFERRED` | SQLite runtime authority retained during initial staging; cutover deferred to aggregate-by-aggregate contracts in `CA-STATE-01`. |

---

## 3. Formal Out-of-Scope and Deferred Capability Register

| Feature / Domain | Description & Reason for Deferment | Impacted FRs | Target Phase / Spec |
|---|---|---|---|
| **Cross-Workspace Guest Link Execution** | Runtime execution of `GuestIdentityLink` crosswalks is deferred to prevent unconsented participant tracking and premature cross-tenant complexity. | `FR-CAE-TEN-008` | Future Enterprise Research Spec |
| **Phase-5 Dynamic Replanning** | Real-time adaptive replanning of interview questions based on in-flight dialogue analysis is deferred. | `FR-P05-08` | Future Interactive Planning Spec |
| **Phase-5 Interview Brief Compiler** | Automated compilation of qualitative interview briefs into question grammars is deferred. | `FR-P05-01` | Future Interview Compiler Spec |
| **Phase-6 Candidate Synthesis & Edge Derivation** | Automated synthesis of candidate semantic activations and graph edge derivation is deferred. | `FR-P06-03`, `FR-P06-08` | Future Graph Derivation Spec |
| **Phase-7 Archetype Selection & SFL Stack** | Dynamic archetype scoring, SFL perceptual stack resolution, and SemanticProgram compilation are deferred. | `FR-P07-03`, `FR-P07-09` | Future VAE / Synthesis Spec |
| **General Multi-Agent Orchestration** | General autonomous agent coordination and self-orchestration frameworks are explicitly out of scope. | General Engine | Not Authorized in CAE Scope |
| **Client Portal & Studio UI** | Public-facing client web portals, guest login workflows, and interactive studio canvases are out of scope for the backend operational slice. | UI Domain | Future Web Application Spec |
| **Automated Data Migration / Backfill** | Moving legacy SQLite databases to PostgreSQL in bulk is strictly prohibited in this phase. | Database Ops | `CA-STATE-01` / `CA-IMPL-02` |

---

## 4. Quarantined Registry Defects

| Asset / Registry | Defect Description | Quarantine Policy | Target Remediation |
|---|---|---|---|
| **SFL Failure Assets** | 5 failure assets citing missing family IDs: `005, 006, 007, 009, 012`. | `QUARANTINED`: Resolvers must reject references to these 5 missing family IDs and emit typed configuration warnings. | Future SFL Registry Refresh |
| **Primitive Registry Duplicate** | Duplicate primitive identifier: `EXP-TRG-001`. | `QUARANTINED`: Resolver maintains primary entry; duplicate variant rejected on load. | Future Primitive Clean-up |

---

## 5. Non-Claims and Operational Guardrails

1. **No Production Authorization:** This register authorizes zero production deployments, database migrations, or infrastructure provisioning.
2. **No Schema Finalization:** Physical table names, column constraints, and SQL queries are NOT finalized by this register and must be formally authored in `CA-STATE-01` and `CA-TS-01`.
3. **No Autonomous Operation:** All operational runs must execute under human or authorized service runner supervision with explicit receipt lineage.
