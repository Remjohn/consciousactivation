# CAE-BMAD Product Reconstruction Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M04  
**Scope:** Architecture, agent responsibilities, lineage synthesis pipelines, and brownfield crosswalk standards for reconstructing CAE product intent prior to PRD authoring.

---

## 1. Mandate Assignment and Role Architecture

Before writing modular PRDs, functional requirements, or system architectures, CAE-BMAD requires full **Product Reconstruction**.

Reconstruction is executed by a coordinated cluster of specialized agents:
1. **Primary Agent (`cae-product-reconstructor`):**
   - Operating Level: `Level 01: PRODUCT / INTENT`.
   - Core Mission: Ingests the 216-source research corpus, extracts core product intent, preserves historical lineage, and maps foundational capabilities.
2. **Supporting Agent (`cae-brownfield-auditor`):**
   - Operating Level: `Level 06: REPOSITORY` down through `Level 13: LINE / BLOCK`.
   - Core Mission: Cross-checks reconstructed product concepts against active services (`builder`, `delegation`, `vae`, `world-intelligence`) to establish whether capabilities exist or are missing.
3. **Supporting Agent (`cae-documentation-analyst`):**
   - Operating Level: `Level 02: DOCUMENTATION`.
   - Core Mission: Audits previous PRD modules (e.g. `docs/prd/modules/`, `docs/PRD/CURRENT.md`) and historical specs to detect terminology evolution.

---

## 2. The 5 Core Product Capability Pillars

CAE product reconstruction synthesizes 216 sources into 5 non-negotiable capability pillars:

```text
Pillar 1: AUDIENCE & GUEST INTELLIGENCE
  - Guest identity vectors, stance profiles, psychological coordinates, and workspace membership.
  - Lineage: CMF Mood States, CCP Guest Genesis, CA-CAN-01B Guest Constitution.

Pillar 2: QUESTION & INTERVIEW INTELLIGENCE
  - Semantic hypothesis formation, dynamic interview turns, question telemetry, and operator studio.
  - Lineage: Question Intelligence Synthesis, TS-INTERVIEW-PROGRAM-001, CA-CAN-02 Interview Session.

Pillar 3: EVIDENCE & RECEIPT PROVENANCE
  - Immutable media spans, multi-engine consensus, de-inflation, and cryptographic receipt links.
  - Lineage: World Signal Ingestion (SPEC-RSRCH-001), CA-CAN-01C Receipt, CA-CAN-02 Evidence Item.

Pillar 4: EDITORIAL & STORYBOARD PRODUCTION
  - Collision discovery, candidate formation, storyboard harnesses, and visual derivative rendering.
  - Lineage: CCF Trigger-First Engine, Atomic Harnesses Visual Syntax, Video Edit Program.

Pillar 5: MULTI-AGENT RUNTIME & FACTORY SCHEDULING
  - JIT context capsule assembly, deterministic scheduler, typed handoff validation, and execution CAS.
  - Lineage: ca_runtime, cmf_pipeline, SSSF Factory Patterns, CA-CAN-04 Workflow Primitives.
```

---

## 3. Lineage Preservation and Crosswalk Invariants

1. **Anti-Flattening Invariant:** Every reconstructed capability pillar must explicitly cite its historical ancestors (CCP, CMF, CCF) and its modern runtime implementation path.
2. **Fidelity Mapping:** Each crosswalk entry must carry a strict fidelity status (`KNOWN`, `INHERITED`, `VERIFIED`, `PROPOSED`, `INFERRED`, `MISSING`, `CONTRADICTED`, `DEPRECATED`).
3. **Contradiction Preservation:** Any mismatch between historical ambition and modern implementation must be preserved as an open item in the Decision Ledger.
