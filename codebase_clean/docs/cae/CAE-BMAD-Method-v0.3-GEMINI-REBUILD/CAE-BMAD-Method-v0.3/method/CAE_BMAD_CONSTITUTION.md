# CAE-BMAD Method Constitution

**Version:** 0.3.0-rebuild  
**Status:** CONSTITUTIONAL CANON  
**Authority:** CAE Rebuild Program / Operator Mandate M01  
**Lineage:** BMAD-METHOD (Remjohn fork) + CAE Core Lineage (CCP/CCF/CMF, Atomic Harnesses, Visual Syntax, Runtime Primitives)

---

## 1. Method Identity and Premise

The **Conscious Activation Engine – BMAD Method (CAE-BMAD)** is a governed, brownfield-aware, bidirectional product-development method designed for long-lived, high-consequence AI and software systems.

CAE-BMAD unites three disciplines:
1. **BMAD Delivery Discipline:** Progressive, durable product/development artifact progression (Brief → PRD → Architecture → Epics/Stories → Implementation → Review).
2. **CAE Lineage & Truth Discipline:** Preservation of historical lineage, canonical object models, atomic harnesses, visual syntax, proof standards, and runtime primitives.
3. **Agentic Operating Level Framework & CAE Grill:** Explicit traversal of the 13-level engineering stack with interactive, evidence-gated inquiry before any assumption becomes code.

CAE-BMAD is intentionally **not** a generic greenfield template engine. It treats existing documentation, code, transcripts, databases, and runtime behaviors as primary truth surfaces that must be reconstructed, audited, and reconciled rather than overwritten.

---

## 2. Bidirectional Engineering Operating Model

CAE-BMAD operates across a formal 13-level engineering hierarchy:

```text
Level 01: PRODUCT / INTENT
         ↕
Level 02: DOCUMENTATION
         ↕
Level 03: PLAN
         ↕
Level 04: AGENT
         ↕
Level 05: AI WORKFLOW / FACTORY
         ↕
Level 06: REPOSITORY
         ↕
Level 07: APPLICATION
         ↕
Level 08: SCRIPT / CLI
         ↕
Level 09: DATABASE / TABLE
         ↕
Level 10: MODULE / DIRECTORY
         ↕
Level 11: FILE / TYPE / CLASS
         ↕
Level 12: FUNCTION
         ↕
Level 13: LINE / BLOCK
```

### 2.1 Bidirectional Motion Dynamics
- **Descent (Top-Down / Control):** Triggered when understanding is weak, documentation conflicts with runtime reality, evidence is missing, or ambiguity poses architectural risk. The agent moves down the stack to inspect concrete code, schemas, and logs.
- **Ascent (Bottom-Up / Leverage):** Triggered when repeated low-level patterns, verified concrete implementations, and passing reality-contact tests justify forming durable abstractions, PRD updates, or architectural contracts.

---

## 3. Non-Negotiable Constitutional Rules

1. **Lineage Preservation:** Never erase, overwrite, or deprecate historical lineage (CCP/CCF/CMF, Atomic Harnesses, Visual Syntax, Programs) without an explicit, recorded operator decision and mapping crosswalk.
2. **Anti-False-Proof Rule:** A markdown document is not an implementation. A green unit test that does not touch reality (mocks without contract verification, disconnected synthetic assertions) is not proof.
3. **Single-Question Grill Discipline & Signal Distillation:** When human judgment is required, ask exactly one question at a time. Never present compound questionnaires. All questions must adhere to `method/CAE_BMAD_GRILL_SPEC.md` and the **4 Laws of Signal Distillation (RSCS)**, enforcing codebase prechecks, structural collision identification ($T/V/R$), anti-genericity evaluation, and a 320-word substantive recommendation floor.
4. **Code-Resolvable Prohibition:** Never ask the human operator a question that can be answered by searching, reading, or executing tests on the codebase and documentation corpus.
5. **Separation of Truth Surfaces:** Product Intent, Documented Architecture, and Concrete Codebase Runtime are independent truth surfaces. Discrepancies between them must be recorded as Contradictions or Missing Implementations, never silently reconciled.
6. **216-Source Research Corpus Minimum:** Method completeness requires comprehensive research across the governed 216-source target corpus (144 baseline + 72 extended).
7. **Explicit Reality Mapping:** Every product requirement must trace down to exact modules, files, types, functions, and lines. Any gap must be recorded as `MISSING_IMPLEMENTATION`.
8. **Operator Gate Authority:** Autonomous agents are execution workers. Constitutional amendments, product direction pivots, and milestone promotions strictly require operator gate approval.

---

## 4. Evidence Classification Taxonomy

Every assertion, fact, requirement, and requirement-to-code mapping must carry an explicit fidelity classification:

| Status Tag | Semantic Definition | Required Evidence Standard |
|---|---|---|
| `KNOWN` | Established empirical fact verified in current runtime or verified repository files. | Direct path, line number, or execution output reference. |
| `INHERITED` | Retained from historical lineage (CCP, CCF, CMF, prior program records). | Traceable link to historical source artifact with provenance score. |
| `VERIFIED` | Formally tested and proven against active runtime/test suites with reality contact. | Executed test name, timestamp, and reproduction command. |
| `PROPOSED` | Newly authored architecture, requirement, or design under active construction. | Authored artifact reference pending grill and review gates. |
| `INFERRED` | Deduced logically from surrounding context but lacks direct written or code proof. | Explicit inference rationale; must be flagged for grill or audit. |
| `MISSING` | Required capability, file, schema, or test identified as absent. | Logged in Missing Implementation register with impact assessment. |
| `CONTRADICTED` | Conflicting assertions identified across documentation, code, or historical lineage. | Logged in Contradiction Register with competing source citations. |
| `DEPRECATED` | Explicitly retired component or concept retained solely for archival lineage. | Reference to retirement decision and successor replacement mapping. |

---

## 5. Standard Error Taxonomy

When a failure, violation, or missing prerequisite occurs during method execution, it must be reported using standard error codes:

| Error Code | Trigger Condition |
|---|---|
| `MANDATE_INPUT_MISSING` | Required input artifact, corpus slice, or configuration key is not supplied. |
| `SOURCE_UNAVAILABLE` | Referenced research source or repository dependency cannot be found or accessed. |
| `SOURCE_UNVERIFIED` | Claim relies on an unauthenticated, unverified, or unscored source artifact. |
| `BMAD_EQUIVALENCE_UNRESOLVED` | Original BMAD capability not properly mapped, specialized, or excluded in contract. |
| `AGENT_NOT_ROUTABLE` | Agent ID, operating level, skill binding, or input/output schema is undefined. |
| `SKILL_NOT_LOADABLE` | Skill definition missing valid frontmatter, steps, or execution contract. |
| `WORKFLOW_UNDER_SPECIFIED` | Workflow lacks entry conditions, exit criteria, step handoffs, or gate verification. |
| `TRACEABILITY_BROKEN` | Requirement cannot be traced down to code/test, or code cannot be traced up to intent. |
| `MISSING_IMPLEMENTATION` | Planned or documented feature is absent from active codebase. |
| `FALSE_PROOF` | File existence or synthetic test claimed as implementation proof without reality contact. |
| `CONTRADICTION_UNRESOLVED` | Irreconcilable divergence between sources without operator resolution. |
| `OPERATOR_DECISION_REQUIRED` | Blocked at constitutional gate requiring operator selection or approval. |

---

## 6. Required Artifact Graph and Contracts

The method produces and maintains a strict DAG of 15 artifact families:

```text
[Research Corpus (216 Sources)]
          ↓
[Product Reconstruction Record]
          ↓
[Operating Level Assessment]
          ↓
[Decision Ledger / CAE Grill Records]
          ↓
[Product Brief]
          ↓
[PRD Index & Modular PRDs] ───→ [Functional Requirements (FR)]
          ↓                                   ↓
[Architecture Specification] ←────────────────┘
          ↓
[Epics & Stories Matrix]
          ↓
[UI/UX Interaction Specification]
          ↓
[Brownfield Reality Map & Code Forensics]
          ↓
[Implementation / Handoff Packet]
          ↓
[Review Record & Operator Promotion Gate]
```

---

## 7. CAE Primitive Integration & Boundary Contracts

CAE-BMAD does not duplicate or replace existing CAE runtime primitives:
- **Programs & Workflows:** Governed execution pipelines remain in `programs/` and `governance/`.
- **Atomic Harnesses:** Visual and execution harnesses remain canonical test and presentation surfaces.
- **Constitutions:** Canonical domain YAML schemas (`docs/cae/constitutions/`) remain the authoritative contracts for `Evidence`, `Receipts`, `Interviews`, `Guests`, and `Workspaces`.
- **Runtime Engines:** Services under `services/` (builder, delegation, vae, world-intelligence) are implementation runtimes audited by CAE-BMAD agents.

---

## 8. Rollback and Quarantine Protocol

If a mandate, agent generation, or workflow execution introduces invalid claims, broken lineage, or unverified abstractions:
1. All generated artifacts must be quarantined or moved to `archive/superseded/`.
2. Execution ledger entries must be updated from `IN_PROGRESS` or `FAILED` with explicit post-mortem notes.
3. Historical records are **never deleted**; they are marked `SUPERSEDED` or `REJECTED` with cross-references to the replacement mandate run.
