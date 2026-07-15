# TS-00: Architecture Preservation Contract

Status: `RATIFIED_DERIVED_CONTRACT`

This contract operationalizes the Activative Intelligence Constitution V1.1, Builder PRD V1.2, D001-D033, the 22 binding anti-goals, the 15 Readiness Hard Gates, and the Architecture Handoff. The human product authority ratified this derived contract on 2026-07-14. It remains subordinate to `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml` and the locked product authority.

## Authority And Scope

Owned authority: D001-D033; AG-001-AG-022; HG-001-HG-015; all Release 1 FR/NFR implementations.

This contract governs architecture, implementation, generated artifacts, workflows, evaluators, deployment, and downstream handoff. A conflict produces `ArchitectureViolationDetected` and blocks promotion.

## Preserved Boundaries

1. Builder is a human-governed harness-development compiler, not the final harness and not a universal agent factory.
2. Harness IR is canonical product truth; Workflow IR is the separate canonical execution definition for Builder operations.
3. Deterministic code owns evidence mechanics, schemas, graph transitions, dependency resolution, compilation, validation, identity, and receipts.
4. Bounded agents own explicitly scoped semantic inference and recommendations. They cannot ratify, authorize, waive, mutate protected evidence, or promote themselves.
5. Humans own constitutional decisions, creative policy, risk acceptance, waivers, irreversible architecture, benchmark-label governance, and implementation authorization.
6. Visual Syntax First governs harness-development evidence order; Activation First governs runtime semantic order. Observation, derived function, hypothesis, human decision, and generated content remain distinct knowledge statuses.
7. Category constitutions remain isolated. Format 02 belongs to 2D Character Animation; no universal profile may flatten category behavior.
8. Content Harness semantic authority remains with the content system. Builder may compile Visual Asset Editor and Delegation target contracts but cannot implement their production behavior.
9. Phase handoffs are typed and versioned. Downstream nodes cannot silently rewrite upstream authoritative outputs.
10. Required context is blocked when over budget, never silently truncated.
11. Control Tower state is event-derived. No UI, cache, prompt, or document becomes a second authoritative store.
12. Repair occurs at the smallest responsible layer and invalidates only proven dependents.
13. Production workflows expose nodes, actors, contracts, validators, retries, budgets, sandboxes, events, tests, and human gates. A monolithic skill or conversation cannot own a production workflow.
14. Structural validity does not imply implementation readiness, and implementation readiness does not imply downstream effectiveness.

## Enforcement Components

| Component | Proposed module | Responsibility |
|---|---|---|
| Architecture policy registry | `domain/policy/architecture.py` | Versioned rules and violation codes |
| Authority guard | `application/authority.py` | Actor/action/resource authorization |
| Graph validator | `domain/graphs/validation.py` | Ownership, cycles, handoff, and invalidation constraints |
| Knowledge-status validator | `domain/evidence/knowledge_status.py` | Prevent unsupported promotion |
| Artifact drift guard | `compilers/drift.py` | Compare generated artifacts to IR/compiler identity |
| Hard-gate evaluator | `evaluation/hard_gates.py` | Evaluate HG-001-HG-015 from receipts and events |
| Boundary contract suite | `tests/architecture/` | Executable anti-goal and cross-product tests |

## Canonical Structures

`ArchitecturePolicy { policy_id, version, authority_source, applies_to, predicate, violation_code, severity, required_receipts }`

`AuthorityGrant { actor_id, actor_kind, action, resource_pattern, constraints, issued_by, expires_at }`

`ArchitectureViolation { violation_id, policy_id, run_id, artifact_refs, event_refs, detected_at, disposition }`

All structures are schema-versioned and content-hashed. Policy waivers are separate, human-signed receipts with scope and expiry; they never alter the policy record.

## Commands, Events, Persistence

- Commands: `validate_architecture`, `request_policy_waiver`, `ratify_preservation_contract`, `revoke_waiver`.
- Events: `ArchitectureValidated`, `ArchitectureViolationDetected`, `PolicyWaiverRequested`, `PolicyWaiverGranted`, `PolicyWaiverExpired`, `PreservationContractRatified`.
- Persistence: policies and receipts in authoritative relational storage; events in Run Ledger; evidence artifacts in content-addressed storage.
- Idempotency: validation key is `(policy_set_hash, subject_hash)`; repeated validation returns the existing receipt.

## Hard-Gate Mapping

| Gates | Required enforcement |
|---|---|
| HG-001, HG-003, HG-005, HG-010 | Constitution, atomic boundary, upstream authority, and anti-goal policy checks |
| HG-002, HG-008, HG-009 | Evidence identity, benchmark isolation, and readiness proof checks |
| HG-004, HG-007 | Contract contradiction and declared dependency/authority checks |
| HG-006 | Skill maturity and exact evaluated identity check |
| HG-011, HG-012 | Workflow decomposition and bounded-control validation |
| HG-013, HG-014 | Node output validation and end-to-end/fault-test promotion gates |
| HG-015 | Constitutional semantic stack, fifth-category profile, rich-lineage, and dual-order checks |

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Constitutional precedence and dual-order enforcement | architecture_policy_owner | Policy validation only; no downstream runtime execution | `CONSTITUTIONAL_PRECEDENCE_CONTRACT`, `ArchitecturePolicy`, HG-015 receipt | Block and emit `ArchitectureViolationDetected`; never select lower authority silently | precedence-conflict and Activation-First/Visual-Syntax-First inversion fixtures | Constitution hash, V1.2 amendment, five-category registry, and rich lineage all validate before promotion | Additive V1.2 policy set; existing V1.1 artifacts require alignment validation but accepted ADR decisions remain intact |

## Security, Isolation, And Least Privilege

Authority checks are deny-by-default. Generator agents cannot read protected labels or write authoritative state directly. Cross-product repositories are read through versioned contract snapshots only. Waiver signing requires a human identity, reason, expiry, and affected requirement IDs.

## Observability And Failure Recovery

Every evaluation emits policy-set hash, subject hash, duration, outcome, and evidence references. A violation quarantines affected outputs and routes to the responsible graph node. Recovery requires a new subject version and fresh validation; events are never deleted.

## Acceptance Tests

1. A workflow with hidden deterministic checks inside one agent node fails HG-011.
2. A generated artifact edited without an IR revision fails drift validation.
3. A semantic hypothesis presented as measured observation fails knowledge-status validation.
4. A Visual Asset Editor runtime component inside Builder fails the product-boundary suite.
5. An agent-issued constitutional waiver is rejected.
6. A required context overflow blocks execution rather than truncating.
7. A readiness PASS without benchmark and hard-gate receipts fails HG-009.
8. Ratifying this contract records a human-signed immutable receipt.

## Implementation Tasks

1. Ratify or replace this derived contract.
2. Encode policy and authority schemas.
3. Implement pure policy evaluators and violation codes.
4. Bind hard gates to receipt queries.
5. Add architecture and cross-product contract suites.
6. Integrate policy checks into compiler, workflow promotion, and authorization.

## Non-Goals And Migration

This contract does not select creative policy, implement downstream products, or grant implementation authorization. No V2.1 migration behavior applies while the implementation is absent.
