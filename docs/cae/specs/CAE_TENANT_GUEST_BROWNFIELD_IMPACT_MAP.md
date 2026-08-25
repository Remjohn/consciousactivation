# CAE Tenant/Guest Brownfield Impact Map

**Document ID:** `CAE_TENANT_GUEST_BROWNFIELD_IMPACT_MAP`  
**Phase ID:** `CA-SPEC-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/07_CA_SPEC_01_TENANT_GUEST_PRD_FR_MANDATE.md`  

---

## 1. Executive Summary

This Brownfield Impact Map classifies every existing repository subsystem, legacy SQLite database, service package, API endpoint, and registry asset affected by the **First Vertical Operational Slice** (`PRD-CAE-TEN-001` and `FR-CAE-TEN-001` through `FR-CAE-TEN-015`).

It enforces non-destructive evolution: existing legacy components are retained or adapted via explicit bridge contracts, preventing accidental premature cutover or runtime regressions.

---

## 2. Component Impact Classification

| Subsystem / Path | Current Brownfield State | Impact Classification | Impact Details & Architectural Boundary | Downstream Phase / Contract |
|---|---|---|---|---|
| `api/main.py` | Single-tenant FastAPI application; no workspace context | `ADAPT` | Add workspace context extraction middleware (`X-Workspace-ID`, actor token); preserve SQLite endpoints for development until aggregate cutover. | `CA-STATE-01` / `CA-TS-01` |
| `api/domain/campaign.py` | Local campaign models and state | `ADAPT` | Align campaign fields with `Engagement` (`CA-ENT-004`) entity; enforce workspace foreign key containment. | `CA-STATE-01` |
| `packages/ca_runtime` | Shared database, receipt, and utility library | `EXTEND` | Add tenant-scoped idempotency keys, receipt evidence link helpers, and composite key validations; maintain backward compatibility. | `CA-IMPL-01A` |
| `services/pipeline` | Local SQLite workflow execution service (`cmf_pipeline`) | `RETAIN` | Retained as legacy development engine; NO premature cutover. Operates in parallel until `CA-IMPL-02` aggregate cutover. | `CA-STATE-01` |
| `services/interview` | External interview capture & expression database | `ADAPT` | Wrap interview export records in `EvidenceSource` (`CA-REL-004`) bridge via WP-09 protocol; read-only access. | `CA-STATE-01` |
| `services/interview-composer` | Sequential dynamic interview planner | `DEFER` | Phase-5 sequential replanning and brief compilation deferred from first slice. | Future Planning Phase |
| `services/air` | Qualitative analysis and evidence span parser | `ADAPT` | Interface with staging `cae.evidence_item` tables via typed operations; remove direct database write mutations. | `CA-IMPL-01B` |
| `services/vae` | Aesthetic/visual activation engine | `DEFER` | Phase-7 visual activation and archetype selection runtime deferred from first slice. | Future VAE Phase |
| `services/studio` | Frontend visualization workspace | `NOT_IN_SCOPE` | UI client portal and studio interfaces out of scope for first vertical backend slice. | Future UI Phase |
| `storage/harness-library` | Local directory for procedural YAML runbooks | `NEW` / `ADAPT` | Formalized as canonical versioned structural template repository (`HarnessTemplate`, `CA-STR-001`). | `CA-STATE-01` |
| `inherited_registries/SDA` | Static YAML semantic direction geometry | `ADAPT` | Maintained on Canonical Plane as global read-only geometric reference (WP-04). | `CA-STATE-01` |
| `inherited_registries/SFL` | SFL perceptual modulation definitions | `QUARANTINE` | 5 failure assets referencing missing families (`005, 006, 007, 009, 012`) quarantined; valid assets retained. | `CA-MAP-01` / `CA-STATE-01` |
| `inherited_registries/Primitives` | Lexical & perceptual primitives (241 valid, 1 dup) | `QUARANTINE` | Duplicate ID `EXP-TRG-001` quarantined; 241 valid primitives retained on Canonical Plane. | `CA-MAP-01` / `CA-STATE-01` |
| `sqlite_databases/*` | Service-local SQLite files (`*.db`) | `RETAIN` | Retained as local cache, test fixtures, and non-authoritative fallback during staging validation. | `CA-STATE-01` |
| `supabase/storage` | Target object storage infrastructure | `NEW` | Provision private tenant-isolated buckets (`cae-media/{workspace_id}/...`) with SHA-256 content addressing. | `CA-IMPL-01A` |

---

## 3. Impact Analysis by Classification Category

### 3.1 `NEW` Components
- **Workspace Tenancy Root:** Introduces explicit multi-tenant partition key (`workspace_id`) and relational RLS boundary.
- **Private Media Storage:** Introduces content-addressed private object storage replacing raw filesystem paths.
- **Receipt Evidence Lineage:** Introduces immutable junction tracking connecting operational receipts to verified media spans.

### 3.2 `EXTEND` Components
- **`packages/ca_runtime`:** Extended to support tenant context propagation, cryptographic hashing, and atomic receipt emission.

### 3.3 `ADAPT` Components
- **`api/`:** Adapted to accept and validate workspace authorization tokens without breaking existing test harnesses.
- **`services/interview` & `services/air`:** Adapted to use typed semantic operation contracts for evidence ingestion and analysis.

### 3.4 `RETAIN` Components
- **`services/pipeline` & SQLite DBs:** Retained without modification to preserve existing development velocity and legacy test fixtures. Cutover occurs aggregate-by-aggregate in later phases.

### 3.5 `DEFER` Components
- **Dynamic Replanning, Brief Compilers, VAE Runtime:** Explicitly deferred to prevent scope explosion beyond the first vertical slice.

### 3.6 `QUARANTINE` Components
- **Corrupted Registry Entries:** Specific missing SFL families and duplicate Primitive keys remain quarantined and blocked from runtime resolution.
