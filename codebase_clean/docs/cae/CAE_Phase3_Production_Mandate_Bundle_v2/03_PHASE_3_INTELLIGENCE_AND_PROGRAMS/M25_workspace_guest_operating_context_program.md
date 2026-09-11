# M25 — Workspace + Guest Operating Context Program

Status: PROPOSED — OPERATOR-RATIFICATION-REQUIRED
Phase: 3 — Intelligence and Programs
PRD ownership: Update relevant CURRENT.md section in the same execution session and record the verification date.

## 1. Decision / Objective
Make the existing Workspace/Guest setup an operator-addressable Program using the live tenancy authority. Resolve and document the one-Workspace/one-active-Guest operating model; support Persona/Brand Context as a subordinate derived dimension only if the live constitution and current model justify it.

## 2. Mandatory reading before action
Baseline: `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`
Mandate-specific:
M2 Program inventory; `docs/PRD/CURRENT.md` tenancy §1.4; workspace/guest constitutions; `SPEC-TWC-UI-001`; `SPEC-GST-UI-001`; `api/routers/v1_tenancy.py`; `packages/ca_runtime/src/ca_runtime/workspace_core.py`; relevant 121 tenancy tests.

## 3. Existing-state rule
The live repository is authoritative over older bundle prose. Read the live implementation,
exact symbols/callers and current tests before editing. Do not rebuild capabilities already
verified in CURRENT.md. Where a service is persistence-only/unreachable, do not claim that
its domain feature is implemented merely because the module exists.

## 4. Constitutional constraints
- Preserve canonical CAE ontology, source sovereignty, Workspace isolation and operator authority.
- Preserve four Authority Lanes.
- Skills are passive, independently routable and flat; never Skill→Skill.
- Protect authenticated Guest evidence, historical memory and constitutionally protected Audience cognition.
- Derived semantic expressions may be versioned/rebuilt only with lineage.
- Typed CAE operations remain the mutation boundary.
- OKF is knowledge representation; Supabase/Postgres is operational authority.
- Do not introduce Redis as canonical knowledge/state.
- Synthetic/placeholder output can never satisfy production acceptance.
- Do not widen into downstream Phase 4 production work.

## 5. Allowed work
Reuse the live PostgreSQL/RLS Workspace authority. Do not create a parallel Guest-tenant layer. Implement only the missing Program/orchestration surface and state gates proven by inventory.

## 6. Required state/hook behavior
Use `00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md`.
Every Program must have explicit state entry/exit conditions and recovery/resume semantics.
Agent completion text is never proof. Hooks/validators enforce deterministic conditions.

## 7. Required verification
- exact commit;
- exact files read;
- exact tests/commands;
- real or approved fixture class;
- runtime trace where applicable;
- artifact/receipt IDs;
- contrastive/negative test;
- limitations;
- PRD section verification/update.

## 8. Acceptance
A real controlled Workspace can be created/configured, one active Guest operating context initialized, scope enforced in runtime, and any Persona/Brand Context representation is subordinate and lineage-safe.

## 9. Stop conditions
STOP on authority conflict, unexplained current-code contradiction, new canonical-object pressure,
protected-source mutation, lane collapse, Skill nesting, synthetic output presented as real,
unverifiable semantic completion, or inability to preserve Workspace/receipt boundaries.

## 10. Operator gate
Report evidence and request explicit operator acceptance/correction. Do not implicitly start the next mandate.
