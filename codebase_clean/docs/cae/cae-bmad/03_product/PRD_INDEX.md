# CAE Canonical PRD Module Index & Traceability Map

**Document ID:** `CAE-BMAD-03-PRD-INDEX`  
**Status:** `RATIFIED & ACTIVE`  
**Total Modules:** 5 Modular Pillars  
**Total Requirements:** 57 Canonical Functional Requirements (`FR-001` through `FR-057`)  
**Production Status:** `production_authorized: true` (`certified: true`)  

---

## 1. Capability Pillar & Module Directory

| Module ID | Pillar Title | Governing Stages / Subsystems | Requirements Covered | Physical Specification |
|---|---|---|---|---|
| `PRD-001` | Audience & Research Intelligence | Stages 01, 02 (Audience Context, Research & Convergence) | `FR-001`, `FR-002`, `FR-010` | [`modules/PRD-001.md`](file:///d:/Work/consciousactivation/docs/cae/cae-bmad/03_product/modules/PRD-001.md) |
| `PRD-002` | Elicitation & Subject Intelligence | Stages 03, 05, 06 (Subject Baseline, PreProd, Elicitation) | `FR-003`, `FR-006`, `FR-007`, `FR-011`, `FR-022`, `FR-051` | [`modules/PRD-002.md`](file:///d:/Work/consciousactivation/docs/cae/cae-bmad/03_product/modules/PRD-002.md) |
| `PRD-003` | Evidence Capture & Yield Analysis | Stages 07, 08, 09 (Evidence Capture, Collision Analysis, Expression) | `FR-012`–`FR-021`, `FR-023`, `FR-028`, `FR-049`, `FR-054` | [`modules/PRD-003.md`](file:///d:/Work/consciousactivation/docs/cae/cae-bmad/03_product/modules/PRD-003.md) |
| `PRD-004` | Composition & Release Management | Stages 04, 05, 10, 13, 14, 15 (Narrative, Portfolio, Release, Dist) | `FR-004`, `FR-005`, `FR-008`, `FR-009`, `FR-029`, `FR-030`, `FR-031` | [`modules/PRD-004.md`](file:///d:/Work/consciousactivation/docs/cae/cae-bmad/03_product/modules/PRD-004.md) |
| `PRD-005` | Multi-Agent Runtime & Certification | Stages 12, 16, 17 + Runtime Subsystems (Security, State, WAL) | `FR-024`–`FR-027`, `FR-032`, `FR-033`, `FR-034`–`FR-048`, `FR-050`, `FR-052`, `FR-053`, `FR-055`–`FR-057` | [`modules/PRD-005.md`](file:///d:/Work/consciousactivation/docs/cae/cae-bmad/03_product/modules/PRD-005.md) |

---

## 2. Bidirectional Causal Traceability Matrix

```text
CAUSAL STAGE / RUNTIME LAYER
   ↓
FUNCTIONAL REQUIREMENT (FR-xxx)
   ↓
INHERITED CONSTITUTIONAL INVARIANT (INV-xxx)
   ↓
PHYSICAL IMPLEMENTATION SURFACE (packages/, services/, programs/)
   ↓
AUTOMATED ACCEPTANCE TEST / REPLAY PROOF
```

### Stage-by-Stage Mapping
1. **Stage 01 (Audience Context):** `FR-001` (`INV-AUD-001`) → `services/pipeline/src/cmf_pipeline/adapters/synthetic.py`
2. **Stage 02 (Research & Evidence):** `FR-002`, `FR-010` (`FR-CONV-001`, `INV-RES-001`) → `collision_hypothesis_program.py`
3. **Stage 03 (Subject Baseline):** `FR-003` (`INV-SUB-001`) → `cae_collision_intelligence/domain.py`
4. **Stage 04 (Narrative Architecture):** `FR-004` (`INV-CAUSAL-001`) → `programs/editorial_storyboard_program/`
5. **Stage 05 (Declarative PreProduction):** `FR-005`, `FR-008`, `FR-009`, `FR-011` → `cmf_pipeline/candidates/service.py`, `apps/web/`
6. **Stage 06 (Structured Elicitation):** `FR-006`, `FR-007`, `FR-022` → `programs/interview_semantic_program/`
7. **Stage 07 (Evidence Capture):** `FR-012`–`FR-015`, `FR-017`, `FR-018`, `FR-020`, `FR-021` → `cmf_pipeline/application.py`, `cae_collision_intelligence/`
8. **Stage 08 (Collision Analysis):** `FR-016`, `FR-023` → `collision_hypothesis_program.py`, `verifier.py`
9. **Stage 09 (Canonicalization):** `FR-019` (`FR-EXPR-001`) → `cae_collision_intelligence/composer.py`
10. **Stage 10 (Composition):** `FR-028` (`INV-NO-INVENT-001`) → `cae_collision_intelligence/composer.py`
11. **Stage 12 (Human Authorization):** `FR-024`–`FR-027` → `program_operator_runtime.py`, `script_program/CAE.md`
12. **Stage 13 (Release Manifest):** `FR-029` (`INV-REL-001`) → `cmf_pipeline/application.py`
13. **Stage 14 (External Distribution):** `FR-030` (`FR-DIST-001`) → `docs/cae/CAE_Product_Brief/14_External_Distribution.md`
14. **Stage 15 (Outcome Measurement):** `FR-031` (`FR-MEAS-001`) → `docs/cae/CAE_Product_Brief/15_Outcome_Measurement.md`
15. **Stage 16 (Verification & PRD):** `FR-033` (`FR-PRD-001`) → `docs/PRD/CURRENT.md`
16. **Stage 17 (Memory Write-back):** `FR-032` (`INV-MEM-001`) → `docs/cae/CAE_Product_Brief/17_Memory_Writeback.md`
17. **Runtime & Infrastructure Subsystems:** `FR-034`–`FR-057` → `packages/ca_runtime/`, `api/routers/`, `health.py`, SQLite WAL