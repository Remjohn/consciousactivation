# CA-M028 — Prospective Policy Revisions and Execution Binding

## 1. Identity and status

- **Mandate ID:** `CA-M028`
- **Canonical question:** `Q27`
- **Wave:** `04`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-POL-001 / Stage 12 Human Authorization`
- **Dependency set:** `Q24–Q26, Q11`
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/program_registry.py; policy/state binding path; relevant execution record schema`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → EXECUTE → VERIFY → RECORD EVIDENCE → COMMIT → OPERATOR DECISION → STOP`

This mandate is an execution contract. It authorizes one bounded implementation phase and does not authorize architecture redesign, adjacent canonical questions, or interpretation of undocumented behavior as permission.

## 2. Decision / objective being authorized

This mandate establishes prospective policy revision semantics. The governing rule is that policy changes apply to future executions while an active or in-flight execution remains bound to the exact policy revision under which it was authorized. This prevents a campaign that began under one policy from silently inheriting a later policy during execution. The mandate is specifically about temporal and revision binding of authorization policy; it is not permission to redesign the whole execution engine or rework every state transition.

The canonical transition is: source state `PREPARED/READY` with policy revision Pn → operation `bind policy revision to execution` → target state `EXECUTION_BOUND` referencing immutable policy revision digest Pn. A later Operator update creates Pn+1 as the campaign's current prospective policy. The active execution continues to resolve Pn. New executions resolve Pn+1. Preconditions include a valid execution creation request, a valid admitted policy package/configuration, and a stable policy identity. Validators must reject attempts to mutate the policy referenced by an existing execution or to rebind an active execution implicitly. Postconditions include a durable execution-to-policy reference and a resolvable policy revision. The error route for a missing or unverifiable revision is fail-closed.

The most important property is that “current campaign policy” and “policy governing this execution” are intentionally different concepts. A UI showing the newest policy does not mean an in-flight run should change. The runtime must read the execution-bound policy when it evaluates authorization. This may require a narrow extension to execution records or state, but the executor should reuse existing revision/digest infrastructure from program manifests and sealed snapshots rather than add duplicate identifiers. If the repository already binds program executions to immutable revision hashes, extend that binding model to policy rather than introducing a new parallel pinning scheme.

A good-looking but wrong implementation is one that stores `policy_mode=Strict` on the campaign and reads that live field for every gate evaluation. The campaign can be changed from Strict to YOLO while a run is executing, and the run then quietly changes behavior mid-flight. Tests that only inspect the campaign row after the update will pass, but the causal contract is broken. The anti-centroid test must explicitly start an execution under Pn, update the campaign to Pn+1, and verify that the active execution still uses Pn while a new execution uses Pn+1.

The implementation should also defend against stale or ambiguous revision references. A policy digest that resolves to different bytes later is invalid. A registry that overwrites an existing policy package in place is therefore incompatible with this mandate. Historical policy revisions must remain addressable and immutable for as long as active or auditable executions require them. If storage retention makes deletion necessary, the architecture must specify a verifiable archival mechanism; this mandate should not invent one. In the absence of such a mechanism, stop and report the retention collision.

The UI should make policy binding visible to Operators. When an execution is inspected, show the policy revision/digest that governs that execution, not merely the campaign's current policy. When a campaign policy is changed prospectively, the UI should communicate that active runs remain pinned. This is important because operators commonly reason from the current campaign configuration. The projection must therefore reveal the temporal distinction without allowing the UI to change runtime authority.

Verification requires at least four paths: a positive initial binding path, a prospective update path, a negative attempt to mutate or rebind an active execution, and a restart/recovery path proving that the binding survives process or worker restart. Where the runtime can spawn a second execution, also prove that the second execution binds to the new revision. Evidence must include exact state records, test locators, and policy artifact identities. A test that mocks `get_policy_for_execution()` to return a fixed object is insufficient because it can pass without proving persistence and revision immutability.

The mandate must preserve policy receipts and historical auditability established by Q25. A later policy revision does not invalidate a previous authorization receipt. The executor must not rewrite old receipts to point at Pn+1. Instead, the receipt and execution record should continue to reference the revision that was actually used. This provides a coherent chain from campaign configuration → policy package → execution binding → authorization receipt.

Prohibitions are narrow but consequential. Do not implement release manifests, external distribution, outcome attribution, memory promotion, or unrelated runtime refactors. Do not reinterpret policy semantics. The mandate assumes Q24–Q26 define the available policy predicates; its job is to bind those predicates to execution time. Shared migrations or registry edits that would be consumed by unrelated later questions require explicit coordination and one integration owner.

Rollback must preserve historical execution-policy links. If the binding mechanism is defective, revert the bounded implementation or disable the new path for new executions without mutating old execution records. Historical active runs must remain interpretable. The executor stops once prospective binding is proven and requests the Operator decision.

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
- `docs/cae/cae_master_57_question_convergence_canon.md` and the Q-specific decision text for `Q27`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
- the current implementation files named in Section 1 and the Q-specific physical surfaces
- any directly referenced schema, migration, manifest, validator, or receipt implementation required to establish the real authority path

The executor must inspect the current repository state before choosing an edit location. It must not rely solely on documentation examples or historical claims.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M028` / `Q27` as defined by the ratified canon and the physical surfaces named above.

**Inputs.** Existing canonical runtime state, policy/evidence/release artifacts from the immediate upstream questions, current schemas/manifests, and the existing runtime/API/UI boundaries.

**Outputs.** The smallest direct runtime, schema, test, receipt, migration, API, and operator-projection changes required to make the `Q27` decision executable and independently verifiable.

**Dependencies.** `Q24–Q26, Q11`. Dependencies are inputs and proof conditions, not permission to rewrite their implementations.

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

The requested decision is: **Approve or reject `CA-M028` based on whether the executable evidence proves the ratified `Q27` contract at the canonical authority boundary.** The executor must not infer approval from a green test suite.

## 13. 200–300 word activation prompt

Execute `CA-M028` only. Read the Mandate Authoring Protocol, Q27, the Master Canon, `docs/cae/UI.md`, `docs/cae/Architecture.md`, the Q27 ledger entry, and the current program registry/execution revision implementation. Implement `INV-POL-001`: active executions remain bound to the exact authorization policy revision under which they were authorized; later campaign policy changes are prospective only. Scope is execution-to-policy binding, immutable revision lookup, persistence/recovery, and minimum UI/API projection of the bound revision. Do not implement release, distribution, or outcome work. Do not read the live campaign policy for in-flight authorization decisions once execution binding exists. Prove the key contrastive case: start under Pn, update campaign to Pn+1, verify the active execution still uses Pn and a new execution uses Pn+1. Also prove stale/unknown revision rejection and persistence after restart. Required evidence is executable state/runtime proof with exact locators plus policy artifact identity evidence. Never mutate historical receipts or old policy revisions. Stop on retention or registry-authority collisions. Completion requires changed files, tests, evidence, limitations, commit SHA, and Operator approval/rejection request for `CA-M028`. Before editing, identify how semantic units are represented and how admitted evidence is referenced today. Do not invent a broad semantic classifier. The verifier must fail at the actual composition boundary when a material claim lacks admissible support, and the report must identify any connective-transformation limits explicitly.
