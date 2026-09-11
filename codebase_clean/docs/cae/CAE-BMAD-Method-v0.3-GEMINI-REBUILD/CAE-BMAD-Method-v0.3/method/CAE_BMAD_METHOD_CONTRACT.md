# CAE-BMAD Method Contract

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL CONTRACT  
**Authority:** CAE Rebuild Program / Operator Mandate M01  
**Scope:** Formal input, output, phase transition, gate, and fidelity contracts for CAE-BMAD method execution.

---

## 1. Execution Preconditions

Before executing any CAE-BMAD workflow or mandate:
1. **Workspace Initialized:** Local project workspace contains `.caebmad/` configuration, research indices, and artifact registries.
2. **Research Baseline Mounted:** The 144 baseline sources (and active extended 72 sources) must be accessible via local repository paths or archived snapshots.
3. **Agent Registry Active:** All 19 specialized CAE agents must be routable with defined operating levels, skill bindings, and boundary rules.
4. **Historical Repositories Identified:** Brownfield legacy directories (`Conscious Activation Engine Brownfield/`, `governance/`, `services/`, `packages/`) must be mounted and readable.

---

## 2. Phase Progression and Handshake Contract

The method executes across six formal phases. Transition across phases requires satisfying explicit gating prerequisites:

```text
Phase 1: RECONSTRUCTION & RESEARCH
         ↓ (Gate 1: 216-Source Coverage & Brownfield Baseline Verified)
Phase 2: MULTI-LEVEL ENGINEERING INVESTIGATION & GRILL
         ↓ (Gate 2: Contradictions Logged & Unresolved Questions Resolved)
Phase 3: PRODUCT DEFINITION (Brief, PRD, FR)
         ↓ (Gate 3: Modular PRD & Requirement Traceability Approved)
Phase 4: ARCHITECTURE & DECOMPOSITION (Arch, Epics, Stories, UX)
         ↓ (Gate 4: Architecture Contracts & Story Readiness Certified)
Phase 5: BROWNFIELD REALITY MAP & HANDOFF
         ↓ (Gate 5: Missing Layers Mapped & Handoff Packet Generated)
Phase 6: PROOF, REVIEW & PROMOTION
         ↓ (Gate 6: Reality-Contact Tests Passed & Operator Ratification)
```

---

## 3. Phase Input/Output Deliverable Matrix

| Phase | Entry Preconditions | Primary Executing Agents | Mandatory Artifact Outputs | Exit Gate Standard |
|---|---|---|---|---|
| **Phase 1: Reconstruction** | Project initialized; research library available. | `cae-product-reconstructor`, `cae-brownfield-auditor` | `Product Reconstruction Record`, `Source Matrix` | Full historical lineage mapped; zero unverified score claims. |
| **Phase 2: Investigation & Grill** | Phase 1 outputs verified. | `cae-documentation-analyst`, `cae-code-forensics-analyst`, `cae-method-orchestrator` | `Operating Level Assessment`, `Decision Ledger` | All code-resolvable questions answered via repo; human grill questions asked 1-by-1. |
| **Phase 3: Product Definition** | Phase 2 gates passed; decisions recorded. | `cae-product-brief-agent`, `cae-prd-agent` | `Product Brief`, `PRD Index`, `PRD Modules`, `FR Matrix` | Modular PRD schema validation pass; every FR traces to intent. |
| **Phase 4: Architecture & Epics** | Phase 3 artifacts ratified. | `cae-architecture-agent`, `cae-delivery-agent`, `cae-ux-agent` | `Architecture Spec`, `Epics Matrix`, `Stories Matrix`, `UI/UX Spec` | Component boundaries typed; story acceptance criteria testable. |
| **Phase 5: Brownfield Mapping** | Phase 4 stories defined. | `cae-repository-analyst`, `cae-data-analyst`, `cae-brownfield-auditor` | `Brownfield Reality Map`, `Missing Implementation Register`, `Handoff Packet` | Explicit code-path mapping for every story; missing code logged. |
| **Phase 6: Proof & Promotion** | Implementation/handoff ready. | `cae-adversarial-reviewer`, `cae-method-orchestrator` | `Review Record`, `Proof Suite`, `Operator Gate Packet` | 100% positive/negative/counter tests pass; operator signed off. |

---

## 4. Requirement-to-Implementation Traceability Invariant

Every requirement in a PRD Module or Functional Requirement (FR) document must maintain a bidirectional trace:

```text
PRD Requirement ID (e.g. PRD-REQ-001)
         ↕ (Traced via FR Matrix)
Functional Requirement ID (e.g. FR-001)
         ↕ (Traced via Epic/Story)
Story ID (e.g. US-001)
         ↕ (Traced via Brownfield Reality Map)
Implementation Target:
  - Repository / Service Path
  - Module / Directory Path
  - File / Class / Function Path
  - Verification Test Path
```

If an implementation target does not exist, the traceability record must explicitly set:
`implementation_status: MISSING_IMPLEMENTATION` and assign a remediation ticket.

---

## 5. False-Proof Defenses and Reality Contact

To prevent synthetic compliance or hollow documentation, every milestone and delivery packet must enforce reality contact and six anti-false-proof tests:
1. **Positive Test:** Executable demonstration that the declared capability functions under valid inputs with direct Reality Contact against active code.
2. **Negative/Countertest:** Executable demonstration that invalid inputs, out-of-bounds parameters, or corrupt contracts are explicitly rejected.
3. **Stale-Reference Test:** Static and dynamic inspection verifying all referenced files, functions, and symbols actually exist in the workspace.
4. **Missing-Artifact Test:** Verification that downstream artifacts fail fast when upstream prerequisites are absent.
5. **Wrong-Level Test:** Verification that high-level abstractions do not attempt to bypass intermediate layers without explicit descent justification.
6. **Forbidden-Action Test:** Automated assertion verifying that prohibited operations (e.g. deleting lineage, muting contradictions, skipping gates) cannot succeed.
