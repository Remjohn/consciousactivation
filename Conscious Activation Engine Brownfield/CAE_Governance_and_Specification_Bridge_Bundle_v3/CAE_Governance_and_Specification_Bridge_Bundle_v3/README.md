# CAE Governance & Specification Bridge Bundle v3.0

## Purpose

This bundle establishes and extends the engineering-control layer between the existing Conscious Activation Engine (CAE) Phase 0–7 architectural documents and implementation-ready brownfield Tech Specs.

It does **not** replace Phase 0–7.
It does **not** assume Phase 0–7 is implementation-authoritative.
It does **not** redesign SDA, SFL, or the Primitive Registries.

Instead, it defines the governing process by which existing architectural claims are:

1. audited against the real repository;
2. reconciled with inherited registries and schemas;
3. classified by evidence status;
4. converted into Functional Requirements;
5. converted into implementation-ready Tech Specs;
6. verified by tests, receipts, and runtime evidence.

## Governing distinction

```text
Architecture source → Brownfield reconciliation → Functional Requirement → Tech Spec → Implementation → Test → Receipt → Outcome
```

A conceptual statement does not become an engineering requirement merely because it is well written.

## Governing quality principle

CAE treats evaluation as a separate architecture layer. Tests are instruments, not proof by themselves. Every material claim is evaluated across:

```text
STRUCTURAL VALIDITY
      +
ENVIRONMENT FIDELITY
      +
REWARD-HACKING RESISTANCE
      +
TASTE / ANTI-CENTROID INTEGRITY
      +
TRACEABLE EVIDENCE
```

The project explicitly rejects test gaming, false proof, and the substitution of proxy metrics for the underlying property.

## Bundle files

| File | Purpose |
|---|---|
| `01_CAE_PHASE_VALIDATION_PROTOCOL.md` | Audits Phases 0–7 for architectural, brownfield, ontological, execution, and verification fidelity. |
| `02_CAE_TECH_SPEC_WRITING_PROTOCOL.md` | Successor to the older Era 3 Tech-Spec protocol, adapted for CAE object/state/relationship architecture. |
| `03_CAE_OBJECT_TO_SPEC_TRACEABILITY_PROTOCOL.md` | Prevents objects, relations, states, and programs from disappearing between constitution and implementation. |
| `04_CAE_SPEC_ACCEPTANCE_AND_EVIDENCE_MATRIX.md` | Defines what evidence is required before a FR or Tech Spec can be considered authoritative. |
| `05_CAE_GRILL_ME_V2.md` | Updated one-question-at-a-time design interrogation protocol for CAE architecture decisions. |
| `06_CAE_CODING_AGENT_CONTEXT_NOTE.md` | Direct briefing for the coding agent explaining current authority boundaries and required workflow. |
| `07_CAE_REGISTRY_MIGRATION_NOTE.md` | Brownfield rules for inherited SDA/SFL/Primitive YAML registries, including ID/version/lineage preservation and migration-gap handling. |
| `08_CAE_IMPLEMENTATION_GATE.md` | Final gate that must pass before implementation begins for a specification. |
| `09_CAE_REALITY_CONTACT_EVALUATION_PROTOCOL.md` | Mandatory environment-fidelity, reward-hacking, taste, anti-centroid, and reality-contact doctrine. |
| `10_CAE_TEST_GOVERNANCE_AND_REWARD_HACKING.md` | Test taxonomy, proxy-to-intent mapping, false-proof tests, and evaluator governance. |
| `11_CAE_PHASE_PROMOTION_AND_PROOF_PROTOCOL.md` | Promotion rules from Phase 0–7 architecture through verified runtime. |
| `12_CAE_EVALUATOR_REGISTRY_AND_TASTE_CORPUS.md` | Governs evaluators and taste/anti-centroid corpora as versioned assets. |
| `13_CAE_IMPLEMENTATION_MAP_REALITY_CONTACT.md` | Maps the evaluation doctrine onto validators, tests, receipts, events, agents, and operator surfaces during brownfield reconciliation.
| `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md` | Defines authoritative PostgreSQL state, transition contracts, phase boundaries, persistence, recovery, and checked handoffs.
| `15_CAE_POSTGRES_STATE_MODEL.md` | Canonical data-model pattern for dynamic state, events, receipts, temporal history, and current-state projections.
| `16_CAE_SEMANTIC_OPERATION_API_PROTOCOL.md` | Defines the typed semantic function layer agents use instead of direct ad-hoc state mutation or raw database reasoning.
| `17_CAE_HARNESS_RUNBOOK_INTEGRATION_PROTOCOL.md` | Integrates state/transition contracts with Skills.md, JIT harness construction, reasoning programs, and runbooks.
| `18_CAE_STATEM_REFERENCE_AND_ADOPTION_BOUNDARY.md` | Records StateM as an external reference implementation and defines what CAE should borrow, adapt, or reject.
| `19_CAE_PRD_STATE_CONTROL_AMENDMENT.md` | PRD amendment plan covering cross-cutting state control, transitions, procedural contracts, receipts, and harness governance.
| `20_CAE_PHASE_STATE_CONTROL_AMENDMENTS.md` | Required updates to Phase 0–7 validation and downstream implementation planning.
| `21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md` | Testing, reward-hacking resistance, environment fidelity, and receipt requirements for state transitions.
| `22_CAE_CODING_AGENT_STATE_CONTROL_NOTE.md` | Direct implementation briefing for the coding agent.  |

## Canonical authority order

When sources disagree, use this order unless a formal architecture decision explicitly changes it:

1. Verified current repository behavior and schema evidence.
2. Ratified canonical registry data and immutable source evidence.
3. Ratified CAE constitutional/ontology documents.
4. Validated PRD and Functional Requirements.
5. Implementation Tech Specs derived from the above.
6. Runtime observations and receipts.
7. Reality-Contact Evaluation evidence.
8. Proposed ideas, hypotheses, or unvalidated notes.

External references such as StateM are design precedents, not CAE authority. They may inform implementation decisions only after brownfield reconciliation and explicit adoption decisions.

This order is intentionally brownfield-aware: existing behavior is evidence, not permission to preserve obsolete architecture blindly.

## Non-negotiable principle

**No Phase 0–7 requirement becomes implementation-authoritative until it passes the Phase Validation Protocol and is represented in a validated Functional Requirement / Tech Spec chain. No implemented capability becomes `VERIFIED` until its applicable reality-contact, environment-fidelity, reward-hacking, taste/anti-centroid, and receipt gates also pass.**


## State-control doctrine added in v3.0

CAE now adopts a cross-cutting procedural-control rule:

```text
PostgreSQL/Supabase = authoritative operational state
Runbook / Skills.md = procedural control and transition doctrine
Typed semantic functions = authorized state operations
Events + receipts = immutable execution history
Agent reasoning = broad autonomy inside a state; no silent state mutation
```

StateM is an external implementation reference for checked phase boundaries, state-local context, recoverable transitions, dynamic checks, and agent-operable runbooks. CAE does **not** adopt StateM's local runtime store as the CAE source of truth. See `18_CAE_STATEM_REFERENCE_AND_ADOPTION_BOUNDARY.md`.
