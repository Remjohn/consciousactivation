# CAE Gemini 12-Phase Execution Program

**Status:** `GOVERNING DELIVERY PLAN — NOT AN IMPLEMENTATION AUTHORIZATION`  
**Prepared:** 2026-08-25  
**Execution agent:** Gemini, acting only under one phase mandate at a time  
**Predecessor:** [CAE Multi-Tenant Authority and Canonicalization Plan](../implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md)

## Purpose

This program converts the post-WP-09 CAE plan into twelve small, legally bounded mandates. Gemini must never receive a broad instruction such as “implement multi-tenancy” or “finish CAE.” It receives exactly one approved phase document, its stated references, and a 200–300-word activation prompt. It may plan and execute only the permitted scope, then must stop at the named operator gate.

The package order is intentional:

```text
evidence boundary
  -> scope/authority map
  -> authoring controls
  -> object constitutions
  -> PRD/FR
  -> state/migration contract
  -> Tech Spec/gate
  -> foundation
  -> typed runtime proof
  -> one aggregate cutover
```

PostgreSQL/Supabase remains the intended CAE operational authority. This does not make every existing SQLite/service-local aggregate migrated or retired. Canonical-definition source, runtime projection, and change/promotion authority remain separate authority axes.

## Mandatory execution rules for every phase

1. Read the assigned mandate in full and every required reference before creating a plan or touching a file.
2. Reconcile claims against executable brownfield evidence; documentation alone does not prove runtime state.
3. Modify only the files explicitly allowed by that mandate. If required files do not exist, create only the listed artifacts.
4. Do not widen a package to solve an adjacent architectural problem. Record it as `BLOCKED`, `DEFERRED`, `QUARANTINED`, or a proposed next-phase dependency.
5. Never expose secrets, change `.env`, use production credentials, provision infrastructure, or apply database migrations unless the phase explicitly authorizes it.
6. For stateful work, normal agent actions go through typed semantic operations; ad-hoc direct writes are prohibited except controlled migration/repair code defined in an approved Tech Spec.
7. Record exact evidence, test environment, receipts, limitations, and non-claims. A green test is not proof beyond its declared fidelity.
8. Update the CAE control state and commit only files within scope. Do not include unrelated working-tree changes.
9. At the exit gate provide: what changed, why, what was proven, what was not proven, risks, operator inspection targets, and the exact next decision.
10. Stop. Do not start the next phase without explicit operator authorization.

## Phase register

| Phase | ID | Objective | Hard dependency | Exit / operator decision |
|---:|---|---|---|---|
| 1 | WP-10A | Contain and reproduce the WP-00–WP-09 evidence boundary | Existing handoff and staging proof | Accept bounded evidence and authorize CA-MAP-01? |
| 2 | CA-MAP-01 | Create the Canonical/Operational Plane Map, Scope & Authority Matrix, and Collision Register | WP-10A acceptance | Approve source/runtime/promotion authority and Workspace boundary? |
| 3 | CA-AUTH-01 | Create authoring-control Skills and static validators | Approved CA-MAP-01 | Approve authoring controls for pilot constitutions? |
| 4 | CA-CAN-01A | Constitute boundary/access objects | CA-AUTH-01 | Ratify Workspace/access/Engagement definitions? |
| 5 | CA-CAN-01B | Constitute Guest and media/evidence boundary | CA-CAN-01A | Ratify Guest/evidence boundaries and no-merge policy? |
| 6 | CA-CAN-01C | Constitute HarnessTemplate, HarnessRun, Receipt and reconcile relations | CA-CAN-01A/B | Ratify first-slice object graph? |
| 7 | CA-SPEC-01 | Tenant/Guest module PRD and traceable FR registry | CA-CAN-01A/B/C | Approve required behavior and deliberate deferrals? |
| 8 | CA-STATE-01 | Per-aggregate authority and migration contracts | CA-MAP-01 plus Phase 7 terms | Approve each aggregate disposition and first cutover candidate? |
| 9 | CA-TS-01 | Implementation-authorizing Tech Spec and Gate A–I evaluation | Phases 7 and 8 | Is CA-IMPL-01A the only work ready for development? |
| 10 | CA-IMPL-01A | Staging relational, RLS, and private Storage foundation | Phase 9 approval | Accept E3 foundation/isolation evidence and authorize typed path? |
| 11 | CA-IMPL-01B | Typed operations, narrow runtime path, and E3 adversarial proof | Phase 10 acceptance | Accept a tenant-scoped working slice and authorize one cutover? |
| 12 | CA-IMPL-02 | Cut over one approved CAE-owned aggregate only | Phase 11 + aggregate decision | Promote that aggregate to PostgreSQL authority? |

## Safe parallelism

Parallel work is allowed only when it cannot create competing authority, conflicting source files, or a false sense that an unapproved decision is ratified.

| Window | Safe parallel lane | Constraint |
|---|---|---|
| Phase 1 | Static evidence inventory and disposable staging reproduction | One agent owns the report; other agents may only return read-only findings. |
| Phase 2 | Brownfield source mapping and collision discovery | Both feed a single matrix/register owner; neither resolves a collision independently. |
| Phase 3 | Draft individual authoring Skills and build static validators | One owner integrates shared vocabulary and checks references. |
| Phases 4–6 | Research/draft non-overlapping constitution groups | Ratification is sequential: 4 before 5; 4/5 before 6. No parallel change to shared object register. |
| Phases 7–8 | PRD/FR drafting and current-source migration inventory | The migration contract cannot make final disposition decisions until Phase 7 terms are approved. |
| Phases 10–11 | No parallel writes to the same staging schema or runtime boundary | Parallel read-only test design is allowed; implementation remains sequential. |

No parallel task may apply migrations, alter RLS, change a semantic operation, or update the durable control record. Those actions have one designated owner per phase.

## Authoring Skills: what exists and what is missing

The Brownfield folder already contains **definition-grammar protocols** for Entity, Value Object, Relation, State, Event, Evidence, Ontology, Structural Grammar, Operator/Primitive, Policy/Contract, Derived Artifact, Execution Packet, Adversarial Asset, IR, and Longitudinal Memory. These are doctrine and meta-protocols. They are not yet usable, agent-facing authoring Skills with allowed inputs, output schemas, validators, hard negatives, escalation rules, and reproducible verification.

The only current CAE `Skills` artifact in the working documentation is the bounded runtime procedure `EVIDENCE_TO_AIR_FIRST_SLICE_SKILL.md`. It is an execution/runbook integration artifact, not a generic ontology-authoring control surface. The Phase 0 protocol itself says the object-specific Skills are an eventual “legalized ontology compiler”; they were deliberately not implemented during the WP-00–WP-09 operational slice.

Phase 3 therefore authors this minimum controlled suite:

1. `CAE_SCOPE_AUTHORITY_MAPPING_SKILL` — maps plane, scope, authority axes, parent chain, storage, and write boundary.
2. `CAE_OBJECT_COLLISION_RESOLUTION_SKILL` — records competing interpretations and makes `RATIFIED`/`SPLIT`/`DEFERRED`/`BLOCKED` outcomes.
3. `CAE_OBJECT_CONSTITUTION_AUTHORING_SKILL` — compiles the correct existing definition grammar into a 26-dimension constitution; it cannot silently resolve a collision or invent storage/runtime semantics.
4. `CAE_CONSTITUTION_COLLISION_REVIEWER_SKILL` — independently challenges class, plane, scope, authority, relationship, and nearest-neighbor collisions; it must not be authored or run in the same review lane as the constitution author.
5. `CAE_PRD_FR_TRACEABILITY_SKILL` — turns ratified objects into bounded, traceable PRD/FR requirements without inventing runtime proof.
6. `CAE_STATE_AUTHORITY_MIGRATION_CONTRACT_SKILL` — writes aggregate-by-aggregate source/target/cutover/rollback contracts and is prohibited from provisioning, backfilling, or cutting over data.
7. `CAE_TECH_SPEC_GATE_SKILL` — produces an implementation gate with exact files, operations, migrations, test and proof requirements; an independent gate-review pass is required before implementation.
8. `CAE_REALITY_CONTACT_EVALUATION_SKILL` — specifies fidelity, countertests, receipts, environmental proof, and non-claims.

These are authoring controls, not a new generalized CAE runtime. They are written only after CA-MAP-01 so they use ratified scope/authority vocabulary rather than inventing it. They are initially `development_uncertified` packages: each requires a `SKILL.md`, version/maturity declaration, input/output schema, authority/context/failure references, hard negatives, static evaluator, receipt shape, and escalation conditions. An optional `CAE_EXECUTION_MANDATE_COMPILER` may format an already-approved phase brief into the legal mandate template; it must never determine scope or manufacture operator decisions.

## Mandate structure and activation prompt requirement

Every Phase 1–12 mandate must be approximately 1,300–1,600 words **when its true scope requires that detail**. Word count is a guard against vague instructions, not permission for ceremonial prose. A mandate must contain: authority, objective, scope, explicit allowed/prohibited changes, required reading, input facts versus hypotheses, artifacts, evidence, verification, failure routes, operator decision, rollback, completion condition, and a 200–300-word activation prompt.

The activation prompt must be an execution key, not a compressed copy of the mandate. It states the phase ID, authority, allowed files/actions, non-negotiable prohibitions, proof requirements, and the exact stop condition. Gemini receives the prompt **and** the complete mandate; the prompt never replaces required reading.

## Current state

This is a preparation artifact. It does not authorize Phase 1. The next legal decision is:

> **Authorize WP-10A only: bounded acceptance and reproducibility review of WP-00 through WP-09?**
