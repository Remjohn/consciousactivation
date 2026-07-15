---
title: F20 — Constraint Conflicts, Feasibility Evidence, and Amendment Proposals
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F20
governing_decisions:
- D002
- D003
- D009
- D018
- D024
- D027
user_journeys:
- UJ-03
- UJ-07
- UJ-12
- UJ-16
functional_requirement_count: 8
---


# F20 — Constraint Conflicts, Feasibility Evidence, and Amendment Proposals

**User outcome:** When an authorized demand cannot be fulfilled, the editor explains the exact conflict and offers bounded alternatives without returning an attractive but semantically compromised approximation.

## Description

Constraint conflicts preserve the immutable demand and distinguish internal plan amendments from demand-level and constitutional amendments.

## Brownfield baseline

V2.1 includes asset amendment requests; the new product needs autonomous conflict detection after repairs/fallbacks and a typed cross-product amendment lifecycle.

## Required product delta

Define conflict codes, evidence, internal versus external authority, amendment options, impact analysis, new demand versions, reuse after amendment, degraded acceptance, and upstream governance.

## Traceability

- **Decisions:** D002, D003, D009, D018, D024, D027
- **User journeys:** UJ-03, UJ-07, UJ-12, UJ-16
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-153 — Detect and classify blocking demand conflicts

**Requirement:** The system must identify contradictory semantic, composition, continuity, control, capability, budget, timing, or delivery constraints that remain infeasible after authorized routes and repairs.

**Consequences (testable):

- The conflict contract identifies code, severity, evidence, attempts, and responsible authority.

- The editor cannot hide a conflict by producing the closest-looking result.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-154 — Preserve the accepted demand during conflict handling

**Requirement:** Conflict analysis and amendment options must reference but never mutate the accepted demand version.

**Consequences (testable):

- The Control Tower shows the unchanged demand and all proposed changes separately.

- An amendment proposal cannot become effective through plan or UI state alone.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-155 — Allow internal production amendments within demand authority

**Requirement:** The editor may version its plan to change approved workflow, model, LoRA, controls, runtime, candidate strategy, or permitted route when all demand constraints remain satisfied.

**Consequences (testable):

- The plan amendment states reason, invalidation, budget impact, and preserved authority.

- Internal amendments cannot relax semantic or out-of-tolerance composition requirements.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-156 — Return demand-level amendment proposals to the owner

**Requirement:** Changes to subject, visible action, Activative function, sequence role, identity, continuity, wrong-reading locks, protected geometry outside tolerance, or quality threshold must be proposed to the owning Content Harness.

**Consequences (testable):

- Each option describes expected feasibility, semantic/Activative impact, cost, and evidence.

- The editor cannot approve or select the owner’s demand amendment.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-157 — Route constitutional amendments upstream

**Requirement:** Proposals that alter asset ontology, category grammar, authority boundaries, production hard gates, Builder architecture, or canonical shared doctrine must enter the validated Builder governance process.

**Consequences (testable):

- The editor provides evidence without modifying upstream constitutions.

- A local release cannot redefine a category or Builder law.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-158 — Create a new demand version for accepted amendments

**Requirement:** When the owner accepts an option, the caller must submit a new Visual Asset Demand version with supersession, amendment source, reason, preserved authority, and changed fields.

**Consequences (testable):

- Dependency analysis determines which prior work can be reused.

- The original failed demand and conflict remain immutable.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-159 — Govern degraded acceptance

**Requirement:** A below-threshold result may be accepted only through a new demand version or owner-authorized exception identifying the relaxed requirement, risk, limitation, and downstream visibility, and only when no constitutional hard gate is violated.

**Consequences (testable):

- The Asset Result Contract records degradation explicitly.

- A standard operator approval cannot bypass meaning-related gates.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

### FR-160 — Benchmark conflict and amendment behavior

**Requirement:** The portfolio must include impossible geometry, contradictory identity/continuity, unsupported capability, inadequate budget, and semantic-relaxation cases to verify correct conflict classification and authority routing.

**Consequences (testable):

- The system is scored on refusing silent substitution and proposing useful bounded options.

- A model that always rejects or always compromises fails the benchmark.

**Traceability:** Decisions D002, D003, D009, D018, D024, D027; journeys UJ-03, UJ-07, UJ-12, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
