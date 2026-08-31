# Mandate 26 — Audience Context Program

Status: PROPOSED — OPERATOR-RATIFICATION-REQUIRED
Phase: 3 — PHASE 3 — INTELLIGENCE AND PROGRAMS
Parallel group: P3-A
PRD ownership: Relevant PRD sections are owned by this mandate; update the relevant section in the same execution session and record the change.

## 1. Decision / Objective

Operationalize Audience setup, current state and Cognitive Islands as a supervised Program using existing Audience authorities.

## 2. Governing doctrine and authority

The mandate is subordinate to:
- Current CAE constitutions and object constitutions.
- Current PRD and Tech Specs.
- Canonical Skill Authoring & Authority Lane Governance Constitution.
- Harness Authoring Master Prompts & Execution Guide.
- Harness Gap Analysis & Build Skill.
- CAE Mandate Authoring Protocol.
- CAE Gemini Mandate Execution Skill.
- Existing ProgrammedModel/workflow/state/receipt authorities discovered during mandatory reading.
- Explicit operator decisions.

For external research, use only for implementation patterns; never as a CAE authority.

## 3. Mandatory reading before action

Baseline:
`00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`

Mandate-specific:
M2/M4; relevant audience specs/services; state contracts

Before editing, enumerate the files read. For relevant directories, inspect the exact symbols/callers
that establish current behavior. If current code contradicts the expected shape, STOP and classify the
conflict; do not silently redesign.

## 4. Exact scope

### Allowed work
Implement retrieval/update flow and Program state.

### Prohibited work
- No new canonical object unless the authority reconciliation proves it is required and the operator authorizes it.
- No replacement of existing CAE state, receipt, Skill, Harness, or workflow authorities with framework-local equivalents.
- No mass conversion of services into agents.
- No Skill-to-Skill invocation.
- No collapse of Hunter/Analyst/Composer/Commander authority.
- No cross-workspace state/retrieval/cache/background-job leakage.
- No synthetic/placeholder output presented as production evidence.
- No widening into adjacent mandates.

## 5. Required implementation behavior

Use the smallest change that closes the verified gap. Reuse existing objects, operations, registries,
schemas, tests, and services. Agent reasoning must terminate in typed, auditable outputs. Deterministic
guarantees should be Hooks/validators/operations rather than prose when technically enforceable.

Where state changes:
`source state → actor/operation → validators → target state → receipt → error/recovery route`.

Where an Agent/Team is involved:
`lane → agent → allowed Skills/tools → output contract → receipt`.

Where a Hook is involved:
`event → matcher → allow/block/observe → idempotency/recovery → evidence`.

## 6. Verification and evidence

At minimum:
- exact commands;
- exact environment;
- relevant fixture class;
- pass/fail result;
- limitation;
- runtime trace where applicable;
- artifact/receipt IDs where applicable;
- exact commit SHA.

For semantic/content claims, include at least one contrastive false-proof test and state what automation
cannot establish. Operator review is required where the mandate claims taste, authenticity, meaning or
production readiness.

## 7. Completion / stop condition

Acceptance:
Real Audience context can be inspected, updated and safely scoped to the Workspace.

Stop immediately if:
- a constitution conflicts with implementation;
- a new canonical authority appears necessary;
- an existing write owner must change;
- typed operation boundaries cannot be preserved;
- a Skill would need to call another Skill;
- a lane boundary would collapse;
- a test cannot distinguish false proof from genuine completion;
- the required runtime environment is unavailable.

After reporting evidence and limitations, STOP. Do not begin the next mandate.

## 8. Rollback / recovery

Prefer reversible changes. Schema/data mutations require an explicit rollback or forward-only migration
plan. Runtime side effects must be idempotent or reconcilable. If the mandate introduces a failure,
restore the previous known-good behavior before stopping unless the operator explicitly authorizes leaving
the repository in the intermediate state.

## 9. Operator decision

Accept the mandate evidence or provide a correction. Do not treat the next mandate as implicitly authorized.
