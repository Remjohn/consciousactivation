# Gemini Execution Mandate — Phase 07 / CA-SPEC-01

**Status:** `DRAFT — BLOCKED UNTIL CA-CAN-01C OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-SPEC-01`  
**Title:** Tenant/Guest Operational Module PRD and Functional-Requirement Reconciliation  
**Execution classification:** PRD/FR authoring only; no Tech Spec, schema, or runtime implementation  
**Required decision:** Ratify CA-CAN-01C and authorize CA-SPEC-01 only  
**Gate:** `OPERATOR_REVIEW`

## 1. Authority and purpose

This mandate is governed by CAE Governance & Specification Bridge Bundle v3; the Phase 0 Object Constitution Protocol; accepted CA-MAP-01 and CA-AUTH-01 outputs; ratified CA-CAN-01A/B/C constitutions, relation map, and contradiction closure; [the CAE Multi-Tenant Authority and Canonicalization Plan](../implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md); and [the 12-phase Gemini execution program](00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md).

CA-SPEC-01 converts the ratified first-slice constitutional dependency chain into one operational module PRD and implementation-grade Functional Requirements. It establishes required behavior, not physical implementation. It must preserve the separation:

```text
ratified object law
  -> module product purpose and boundaries
  -> functional behaviors and acceptance propositions
  -> later authority/migration contract
  -> later Tech Spec
  -> later implementation
```

The module is limited to internally managed, client-isolated operational work for the first slice:

```text
Workspace -> Membership / OperatorAccess -> Engagement -> Guest
  -> verified media/evidence boundary -> HarnessRun -> Receipt lineage
```

It does not define all CAE domains. World Intelligence, Audience/Guest dynamic state, ContextPremise, relational intelligence, Matrix of Edging, primitive/coalition/edge, SDA/SFL runtime resolution, SemanticProgram, scenes, compositions, Builder IR, Pipeline, outcomes, analytics, bulk import, client portal design, and generic agent orchestration remain out of scope unless a ratified predecessor explicitly requires a narrow interface reference.

The PRD and FRs must not reverse the constitutional decisions. If a desired behavior needs an object, relation, authority, scope, or semantic term that has not been ratified, that behavior is `DEFERRED` or `BLOCKED`; it is not added as a “future-compatible” requirement. The agent shall distinguish target behavior from current repository proof, and shall not call a requirement implemented because a document, table, script, or provisional staging slice exists.

## 2. Mandatory reading before action

Gemini SHALL read in full before planning or editing:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
2. All accepted CA-MAP-01 artifacts and the CA-AUTH-01 requirement-traceability authoring Skill package.
3. Every ratified CA-CAN-01A/B/C constitution, `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`, and `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`.
4. `docs/cae/implementation/CAE_WP05_PRD_FR_TECHSPEC_RECONCILIATION.md` and `TS-CAE-EVID-001_EVIDENCE_TO_AIR_FIRST_SLICE.md` to preserve prior scope and non-claims.
5. `docs/cae/implementation/CAE_WP00_TO_WP09_REVIEW_EVIDENCE_HANDOFF.md` and WP-02/03/06/07/08/09 proof records where a current-capability claim is considered.
6. The v3 `01_CAE_PHASE_VALIDATION_PROTOCOL.md`, `02_CAE_TECH_SPEC_WRITING_PROTOCOL.md`, `03_CAE_OBJECT_TO_SPEC_TRACEABILITY_PROTOCOL.md`, `04_CAE_SPEC_ACCEPTANCE_AND_EVIDENCE_MATRIX.md`, `08_CAE_IMPLEMENTATION_GATE.md`, `10_CAE_TEST_GOVERNANCE_AND_REWARD_HACKING.md`, and `21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md`.
7. `docs/PRD/CURRENT.md` and relevant existing service documentation as brownfield inputs only. Do not modify them.

If the accepted constitutions contain `BLOCKED` or unresolved `CONTRACT_CONFLICT` findings that affect a proposed requirement, Gemini SHALL record the requirement as blocked/deferred and stop the affected requirement path. It shall not fill a gap with generic tenant terminology, SQL assumptions, or a new object definition.

## 3. Exact PRD scope

The single module PRD SHALL answer, using the ratified object model:

- what the tenant/Guest operational slice is for and which operator/client problems it solves;
- its canonical objects, direct relations, scope classes, authority axes, state/evidence boundaries, and user/operator roles;
- shared canonical doctrine versus Workspace-scoped operational facts;
- legal first-slice lifecycle from creating/accessing a Workspace through a bounded HarnessRun and Receipt lineage;
- what is allowed, prohibited, deferred, quarantined, or dependent on later operator decisions;
- brownfield adaptation decisions and the boundary with legacy SQLite/service-local authority;
- expected receipts, evidence requirements, privacy/isolation rules, failure/repair routes, evaluation posture, and non-claims;
- dependency and handoff boundaries for CA-STATE-01 and CA-TS-01.

The PRD SHALL not specify table names, DDL, Python/Pydantic models, SQL/RLS expressions, endpoint signatures, background-worker topology, physical Storage policy, implementation files, migration commands, or production deployment. It may define a required operation semantically—for example, “register a verified media asset”—but must defer its exact contract/signature to CA-TS-01 after CA-STATE-01 is accepted.

## 4. Functional Requirement rules

Each FR must have a stable ID and exactly one primary constitutional owner. It may reference related objects but must not become a hidden cross-domain architecture document. The agent SHALL create only requirements necessary to specify the approved first slice, such as Workspace boundary, membership/access decision, Engagement containment, Guest locality, no-implicit-merge, verified media/evidence boundary, HarnessTemplate/Run separation, receipt lineage, scoped failure/recovery, and first-slice evaluation requirements.

Each material FR SHALL contain:

```text
FR ID and title
authoritative source and constitutional owner
problem / decision being protected
required behavior and explicit boundary
inputs and outputs at semantic level
objects, relations, scope, and authority axes
state/transition implication, if applicable
authorized operation family, if applicable
evidence, receipt, and provenance requirement
validation and typed failure classes
acceptance propositions and measurable completion condition
test class, minimum E0–E4 fidelity, and reward-hack countertest
brownfield impact: NEW / EXTEND / ADAPT / RETAIN / DEFER / QUARANTINE
migration/rollback dependency or explicit non-applicability
open decision and prohibited interpretation
```

FR depth is determined by ambiguity and implementation risk, not line count. A trivial boundary statement may be concise; access, evidence, transition, containment, or cutover behavior must be detailed enough that a later Tech Spec agent cannot silently invent its meaning. “The system SHALL be multi-tenant” is insufficient. “The system SHALL use PostgreSQL” is insufficient without aggregate authority, transition, proof, and rollback details that belong in CA-STATE-01/CA-TS-01.

An FR must never make a general `guest_id` rule. It shall declare its scope class and legal Workspace parent chain. Likewise, an FR must not convert a receipt into independent proof, a URL into verified evidence, an operator into an unrestricted bypass, a template into an execution, or a Guest identity link into automatic merge.

## 5. Authorized artifacts and file boundary

Gemini MAY create or update only:

- `docs/cae/specs/PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md`
- `docs/cae/specs/fr/FR-CAE-TEN-001_*.md` through `FR-CAE-TEN-0NN_*.md`
- `docs/cae/specs/CAE_TENANT_GUEST_REQUIREMENT_TRACEABILITY_MATRIX.md`
- `docs/cae/specs/CAE_TENANT_GUEST_BROWNFIELD_IMPACT_MAP.md`
- `docs/cae/specs/CAE_TENANT_GUEST_DEFERMENT_AND_EXCEPTION_REGISTER.md`
- `docs/cae/implementation/CAE_CA_SPEC_01_RECONCILIATION_AND_REVIEW.md`
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`
- a static verifier under `scripts/cae/` that reads only these artifacts and makes no runtime/database mutation.

The traceability matrix shall map every PRD capability and FR to constitutional owner, relation map edge, source evidence, scope/authority class, required future contract, test/fidelity class, and current status. The Brownfield Impact Map shall classify every existing component affected by an FR as `NEW`, `EXTEND`, `ADAPT`, `RETAIN`, `DEFER`, `QUARANTINE`, or `NOT_IN_SCOPE`, with evidence. The exception register shall preserve contradictions and consciously deferred scope rather than hiding it in generic prose.

Gemini SHALL NOT modify `docs/PRD/CURRENT.md`, brownfield bundles, existing service code, authoring Skills, constitutions, runbooks, SQL, migrations, RLS, Storage, API, environment, or data. It must not write a Tech Spec during this phase. It shall preserve unrelated working-tree changes and commit only authorized artifacts.

## 6. Required validation and anti-reward-hack review

Run the traceability author and independent review procedure. Static validation must prove:

- every FR maps to exactly one ratified constitutional owner and source evidence;
- no FR introduces an unratified object/class/scope/authority concept;
- every stateful/material FR declares operation, evidence/receipt, failure, fidelity, and countertest or gives a justified non-applicability reason;
- no current-runtime claim exceeds the WP-00–WP-09 evidence boundary;
- every dependency on CA-STATE-01 or CA-TS-01 is explicit;
- requirements do not authorize implementation, migration, or production cutover;
- every traceability matrix row has a Brownfield Impact classification;
- no cross-workspace behavior, identity merge, private media access, or operator override is vague.

Hard negatives shall include an orphan FR; an FR that introduces global Guest identity; “tenant ID on every table” as an ontology claim; a receipt-only acceptance test; a verified-flag/URL-only evidence claim; an unrestricted operator role; a generic PostgreSQL-cutover requirement; and a test passing on a mocked or same-workspace-only fixture while cross-workspace denial is untested.

The review record shall distinguish E1 structural traceability from E2/E3 runtime evidence already established. It shall state that no E4 semantic/taste/human outcome proof is made. A passing static verifier is not a development authorization.

## 7. Completion and operator gate

CA-SPEC-01 completes only when the PRD, only the required FRs, traceability matrix, brownfield impact map, deferment/exception register, review record, and static verifier exist; all material requirements are constitution-led; hard negatives pass; and all exclusions/non-claims remain visible.

Gemini SHALL request exactly:

> **Approve PRD-CAE-TEN-001 and its bounded Functional Requirements, including recorded deferrals and brownfield impacts, and authorize CA-STATE-01 only: per-aggregate authority and migration contracts?**

After asking, Gemini SHALL stop. It has no authority to write a migration contract, Tech Spec, schema, RLS policy, Storage policy, runtime operation, or implementation.

## 8. Gemini activation prompt (approximately 245 words)

You are the CAE governed execution agent for `CA-SPEC-01 — Tenant/Guest Operational PRD and Functional Requirements`. This mandate is blocked unless CA-CAN-01C and its relation model have been explicitly ratified. Read this mandate and every required reference before planning or editing. Your authorization is only to author one bounded tenant/Guest operational PRD, its required Functional Requirements, traceability matrix, Brownfield Impact Map, deferment/exception register, review record, and static verifier. You are not authorized to create a Tech Spec, migration contract, SQL/schema, RLS/Storage policy, API, runtime code, authoring Skill, constitution change, data movement, or production action.

Every requirement must be led by a ratified constitutional owner and direct evidence. Do not invent a term, class, scope, source authority, parent chain, or operation merely to make a requirement complete. Mark it deferred or blocked instead. Keep Workspace as the client boundary; Guest is workspace-local, not a universal Person or a universal tenancy key. Keep canonical source, runtime projection, and promotion authority separate. Do not let a receipt prove semantic outcome, a URL prove verified media, an access policy become a bypass, or a template become a run.

Write requirements in legal, testable language with semantic inputs/outputs, applicable state and operations, evidence/receipt, failures, acceptance propositions, fidelity, countertests, Brownfield impact, migration dependency, and prohibited interpretations. Use the traceability and independent review controls; execute hard negatives that catch orphan, vague, overreaching, and shortcut requirements. Record exact sources, validator results, limitations, and non-claims. Update control state, commit only allowed artifacts, ask exactly the Section 7 decision, and stop before CA-STATE-01.
