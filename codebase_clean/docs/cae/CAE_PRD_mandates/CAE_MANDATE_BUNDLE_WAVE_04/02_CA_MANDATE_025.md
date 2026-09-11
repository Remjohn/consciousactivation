# CA-M025 — Configurable Campaign Authorization Policy

## 1. Identity and status

- **Mandate ID:** `CA-M025`
- **Canonical question:** `Q24`
- **Wave:** `04`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `FR-AUTH-001 / Stage 12 Human Authorization`
- **Dependency set:** `Q08, Q11, Q16, Q23`
- **Primary physical surfaces:** `program_operator_runtime.py; apps/web/src/api/types.ts; docs/cae/CAE_Product_Brief/12_Human_Authorization.md`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → EXECUTE → VERIFY → RECORD EVIDENCE → COMMIT → OPERATOR DECISION → STOP`

This mandate is an execution contract. It authorizes one bounded implementation phase and does not authorize architecture redesign, adjacent canonical questions, or interpretation of undocumented behavior as permission.

## 2. Decision / objective being authorized

This mandate authorizes implementation of the campaign-level authorization policy contract for CAE. The permitted decision is that an Operator can configure a bounded delegation mode for a campaign or governed execution object, with the canonical modes described by the existing system such as YOLO, Checkpoint, Strict, and an explicitly represented Custom policy. The decision is not permission to redesign the whole authorization subsystem, invent new autonomy modes, or make constitutional safeguards optional. The objective is to make the already-ratified policy choice executable, inspectable, version-addressable, and fail-closed at the canonical runtime boundary. A policy setting is meaningful only if the runtime actually consults it when deciding whether an action may proceed without a new human gate. A UI control or YAML field that never reaches the runtime is not evidence of implementation.

The authorization model must preserve the distinction between policy preference and constitutional authority. A campaign may choose to reduce routine Operator intervention, but that preference cannot waive security invariants, provenance requirements, evidence admissibility, release integrity, or any other requirement marked non-waivable by the architecture. The implementation therefore needs an explicit policy representation with a stable identity or revision, a deterministic mapping from policy mode to authorization behavior, and a clear evaluation boundary that answers what action is being requested, which object/revision is in scope, which policy revision governs it, and whether an operator intervention is mandatory. Where a Custom mode exists, it must not devolve into arbitrary booleans. Its predicates should be typed, bounded, and validated against the same constitutional floor used by the canonical modes.

The state transition is bounded: source state is the current campaign configuration or inherited default policy, operation is a validated policy update, target state is a new policy revision associated with the campaign. The actor is the Operator or authorized control-plane caller. Preconditions include a valid campaign identifier, valid policy schema, and permission to change the campaign configuration. Validators must reject unknown modes, malformed custom rules, contradictory requirements, and attempts to disable constitutional controls. The resulting state must be retrievable through the runtime/API path that execution uses. The UI may project the state and provide editing controls, but it cannot become the source of truth. A browser-local choice that differs from runtime state is a stale view, not an authorization policy.

The implementation should inspect existing runtime policy logic before introducing new abstractions. Extend the canonical policy types when possible. If an existing policy package or program manifest already has semantically compatible fields, normalize around it rather than creating a second authority model. The executor should map each mode to observable behavior: for example, a routine non-consequential action may pass automatically under YOLO, the same action may pause at a checkpoint under Checkpoint, and the same action may require explicit approval under Strict. The exact action taxonomy must come from existing CAE policy sources, not be invented from intuition. Where the repository lacks a complete mapping, the mandate should implement only the already-defined predicates and record missing cases as limitations rather than guessing.

The strongest proof is not that the settings page renders four options. The proof is that a real execution reaches the authorization evaluator, receives the configured policy, and produces the expected gate or non-gate outcome while still rejecting an attempt to suppress a constitutional invariant. A convincing false proof would be a unit test that calls a policy parser in isolation and asserts that `strict` parses successfully. That shows syntax only; it does not prove runtime enforcement. Another false proof would be a UI snapshot test showing a selected mode without verifying that the runtime received the same revision. Both must be explicitly rejected as incomplete evidence.

This mandate must also protect against policy drift caused by duplicated defaults. There should be one canonical default, one canonical serialization, and one authoritative read path. If a legacy caller has a fallback that silently overrides the configured policy, the executor must either route it through the canonical evaluator or document the collision and stop. The correct behavior for ambiguity is fail-closed, not heuristic merging. A campaign that requests an unsupported policy must become blocked or rejected with an evidence-bearing reason; it must never silently downgrade to YOLO because a legacy code path does not understand the requested configuration.

Operator-facing behavior is part of the contract but is not itself authority. The UI should show the current policy, relevant revision identity, non-waivable constraints, and enough context to explain the consequence of changing the setting. It must not claim that a mode change is active until the runtime confirms persistence. If the architecture uses a state version or digest, that value should be visible where consequential actions are initiated so stale changes can be detected. The mandate does not authorize a visual redesign beyond what is required to make the policy executable and inspectable.

The executor must produce a focused proof suite covering positive behavior for each supported mode, negative rejection of invalid policy values, protection of constitutional invariants, persistence/reload of the chosen policy, and runtime enforcement. Include a false-proof countercase in the test report. Also distinguish documented behavior from executable proof. A repository document saying that four modes exist is `DOCUMENT` evidence until the actual runtime path demonstrates those modes. A schema definition is `SCHEMA`; a migration is `MIGRATION`; a passing end-to-end policy gate is `EXECUTABLE` or `TEST`; an unresolved mapping is `HYPOTHESIS` or `OPERATOR_DECISION_REQUIRED`. The report must not upgrade the evidence class by assertion.

The change boundary is strictly this campaign authorization policy. Do not implement durable authorization receipts as a separate mandate, prospective policy binding as a separate mandate, release authorization, composition semantics, or distribution. Interfaces may be prepared only where necessary for this policy evaluator to function. Shared migrations or state changes with later mandates require one integration owner and must not be parallelized. If the work discovers that the current runtime cannot represent the required policy semantics without changing a shared state machine, stop at the smallest safe boundary and report the dependency rather than widening scope.

Completion means the configured policy exists at the canonical authority boundary, the supported policy modes behave as specified, constitutional invariants remain non-waivable, invalid or stale policy updates fail closed, executable evidence proves runtime behavior, limitations are recorded, and the exact commit is captured. The executor must then stop and request the Operator decision. It must not proceed automatically into CA-M026.

## 3. Governing doctrine and authority sources

The governing doctrine is the CAE supreme causal law: downstream realization cannot legitimately invent upstream meaning. Runtime authority belongs to the canonical CAE runtime and its durable state/receipt mechanisms, not to browser state, cached projections, prose, or an agent's interpretation. Semantic authority is established by the Master Canon, Product Brief/PRDs, and the relevant question decision. Mutation and promotion authority are governed by runtime authorization policy. Evidence authority is established by admitted evidence and executable verification.

Primary authority sources for this mandate are:

1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar, scope, authority, evidence, anti-centroid, activation, parallelism, and stop rules.
2. `docs/cae/cae_master_57_question_convergence_canon.md; docs/cae/UI.md; docs/cae/Architecture.md; Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md; Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
3. Q-specific source paths named in Sections 4 and 5 below.

A source is not authoritative merely because it exists in the repository. The executor must verify the canonical runtime boundary before claiming implementation.

## 4. Mandatory reading before action

Before editing, the executor MUST read the entire contents, not excerpts, of the following where present:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` and the Q-specific decision text for `Q24`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
- the current implementation files named in Section 1 and the Q-specific physical surfaces
- any directly referenced schema, migration, manifest, validator, or receipt implementation required to establish the real authority path

The executor must inspect the current repository state before choosing an edit location. It must not rely solely on documentation examples or historical claims.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M025` / `Q24` as defined by the ratified canon and the physical surfaces named above.

**Inputs.** Existing canonical runtime state, policy/evidence/release artifacts from the immediate upstream questions, current schemas/manifests, and the existing runtime/API/UI boundaries.

**Outputs.** The smallest direct runtime, schema, test, receipt, migration, API, and operator-projection changes required to make the `Q24` decision executable and independently verifiable.

**Dependencies.** `Q08, Q11, Q16, Q23`. Dependencies are inputs and proof conditions, not permission to rewrite their implementations.

**Operators allowed.** Repository executor for implementation/testing; Operator for approval/rejection or explicitly required governance decisions. No autonomous expansion of scope is permitted.

**Validators required.** Positive executable acceptance, negative/fail-closed acceptance, persistence/reload or revision integrity where applicable, integration proof at the canonical boundary, and exact evidence locators.

**Prohibited surfaces.** Adjacent canonical questions; unrelated programs; global redesigns; new authority models; silent compatibility changes; unrelated UI refactors; destructive historical rewrites; and any semantic bypass intended merely to improve apparent success or yield.

## 6. Allowed artifacts and file boundary

Allowed changes are limited to the physical surfaces named in Section 1, their direct tests, and the minimum supporting schema/migration/API/UI projection needed to make the decision executable. New files are allowed only when they are the smallest direct implementation or proof artifact. Reuse existing types, state, receipt, hashing, policy, evidence, release, and program-registry infrastructure where semantically compatible.

Shared registries, migrations, receipt schemas, or state machines have one integration owner. Parallel read-only inspection is permitted; conflicting writes are not. A downstream mandate may consume an upstream contract but may not silently alter its authority.

## 7. Prohibitions and collision procedure

Do not treat UI state, documentation assertions, model-generated prose, cache contents, or a non-canonical registry as runtime truth. Do not weaken a constitutional invariant to make a happy path pass. Do not invent undefined policy precedence, semantic exceptions, or cryptographic guarantees. Do not mutate historical release, policy, authorization, or evidence objects in place when the contract requires immutability.

If the executor encounters a collision with an existing invariant, authority rule, schema, migration, or state transition:

1. stop before making the conflicting change;
2. identify the controlling source;
3. classify the collision as implementation defect, stale documentation, dependency gap, or unresolved `OPERATOR_DECISION_REQUIRED`;
4. make the minimum correction only if this mandate clearly owns it;
5. otherwise record the collision and stop.

**Contrastive failure requirement.** A convincing implementation that satisfies a UI assertion, a parser test, a mocked runtime call, or a top-level score while failing the canonical property is a false proof and must be rejected. The executor must name the applicable false-proof case in the completion report.

## 8. Required work / implementation behavior

1. Inventory the existing implementation and identify the authoritative runtime boundary before editing.
2. Map the Q-specific decision to the smallest existing types/state transitions/registries that can enforce it.
3. Implement the minimal contract without creating a parallel authority model.
4. Preserve backward-compatible behavior when it does not conflict with the new invariant; otherwise fail closed and document the collision.
5. Add or update positive and negative tests that exercise the actual boundary.
6. Exercise persistence/reload, revision/digest integrity, or adapter behavior where this mandate requires those properties.
7. Expose only the minimum operator-readable state needed to inspect the decision and its evidence; the UI remains a projection.
8. Record evidence classes (`EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, `OPERATOR_DECISION_REQUIRED`) for every material claim.
9. Run focused tests first, then the relevant integration/regression suite.
10. Record exact commands, exact evidence locators, residual limitations, and the exact commit SHA.

## 9. Verification and evidence standard

Every material claim must be proven at the level where the property actually exists. A schema test can prove schema validity. It cannot prove runtime enforcement. A UI snapshot can prove presentation. It cannot prove authority. A mock can prove a call contract. It cannot prove integration with the canonical state machine.

Required verification includes:

- one positive acceptance path;
- one negative/fail-closed path;
- the mandate-specific contrastive false-proof case;
- environment-fidelity proof at the real runtime/API/persistence/release boundary as applicable;
- regression coverage for directly affected existing behavior;
- exact evidence locators;
- a statement of what remains unproven.

The executor must not claim `VERIFIED` solely because documentation, fixtures, snapshots, or local mocks pass.

## 10. Completion and stop condition

The mandate is complete only when the requested artifact/behavior exists, its declared proof standard passes, negative cases fail closed, no prohibited surface was changed, limitations are recorded, the exact commit SHA is captured, the control-state record is updated if one exists, and the Operator decision is explicitly requested.

The executor MUST STOP after this mandate. It must not begin the next canonical question automatically. A failing dependency, unresolved authority collision, or missing environment-fidelity proof is a stop condition, not permission to weaken the requirement.

## 11. Rollback / recovery

Prefer an isolated implementation commit and the repository's existing migration/revision/recovery mechanism. Preserve historical authorization, policy, release, distribution, evidence, and outcome records. Do not repair an invalid historical artifact by rewriting it in place. When a new revision is required, create a new immutable revision and retain the old record for auditability.

If a migration is introduced, follow repository migration conventions and document downgrade/forward-only behavior. If recovery requires an Operator decision outside the mandate's authority, stop with `OPERATOR_DECISION_REQUIRED`.

## 12. Operator decision

The completion report must present a concise evidence package containing: changed files, exact tests/commands, evidence classes and locators, false-proof countercase result, residual limitations, control-state impact, and exact commit SHA.

The requested decision is: **Approve or reject `CA-M025` based on whether the executable evidence proves the ratified `Q24` contract at the canonical authority boundary.** The executor must not infer approval from a green test suite.

## 13. 200–300 word activation prompt

Execute `CA-M025` only. Load `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`, the Master 57-Question Canon Q24, `docs/cae/UI.md`, `docs/cae/Architecture.md`, the Q24 entry in `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`, and the current policy/authorization implementation. Implement only `FR-AUTH-001`: configurable campaign authorization policy with the existing bounded modes (YOLO, Checkpoint, Strict, Custom where already defined), while constitutional invariants remain non-waivable. Scope is the canonical policy model, persistence/API path, runtime evaluation, and the minimum operator projection required to inspect and set it. Do not implement Q25 durable receipts, Q26 declarative policy packages, Q27 prospective binding, composition, release, or distribution. Do not let browser state, ad-hoc defaults, or LLM output become authority. Prove positive behavior for supported policy modes and negative behavior for invalid policy values and attempts to disable constitutional controls. Required evidence is executable runtime/test evidence plus schema/persistence evidence and exact locators; UI evidence alone is insufficient. Stop on unresolved authority collisions or missing dependencies. Completion requires changed files, exact tests, evidence classes and locators, limitations, commit SHA, and an explicit Operator decision request: approve or reject `CA-M025`. Before editing, name the exact runtime function or API boundary that will enforce the selected policy and identify the existing constitutional controls that must remain above configuration. Do not create a new authority source merely because the current implementation is incomplete.
