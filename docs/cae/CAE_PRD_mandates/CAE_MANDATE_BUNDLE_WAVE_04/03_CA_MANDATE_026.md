# CA-M026 — Durable Authorization Decision Receipts

## 1. Identity and status

- **Mandate ID:** `CA-M026`
- **Canonical question:** `Q25`
- **Wave:** `04`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-AUTH-001 / Stage 12 Human Authorization`
- **Dependency set:** `Q24, Q11, runtime state/receipt infrastructure`
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → EXECUTE → VERIFY → RECORD EVIDENCE → COMMIT → OPERATOR DECISION → STOP`

This mandate is an execution contract. It authorizes one bounded implementation phase and does not authorize architecture redesign, adjacent canonical questions, or interpretation of undocumented behavior as permission.

## 2. Decision / objective being authorized

This mandate authorizes the durable authorization decision receipt contract. The objective is to convert every consequential human approval, rejection, or equivalent governed authorization action into an immutable, cryptographically attributable runtime fact. The receipt must persist beyond the browser session and must bind the decision to the exact object or execution revision that the Operator inspected. The implementation must therefore prove not only that an approval endpoint returns success, but that the approval is represented durably, carries the actor identity and relevant revision integrity data, and can be verified after restart or through an independent read path.

The semantic rule is simple but strict: a human authorization is an event about a specific state, not a generic permission to continue. The receipt must make it possible to answer who authorized what, under which policy revision, against which object revision or state digest, at which point in the lifecycle, and what transition was authorized or denied. The browser may initiate the action, but it must not retain the sole authority for whether the action occurred. A session cookie, websocket message, or ephemeral in-memory boolean is never sufficient evidence. The canonical runtime state store and receipt chain are the durable authorities.

State grammar is: source state `AWAITING_APPROVAL` or another explicitly governed approval state → operation `authorize/approve/reject` with validated actor and freshness context → target state determined by the governing workflow, accompanied by an immutable `AuthorizationDecisionReceipt`. Preconditions include object existence, correct revision or state version, current authorization policy, actor authorization, and any required evidence gate. Validators must reject stale approvals, missing actors, mismatched revisions, duplicate conflicting decisions, and attempts to approve an object whose canonical state has changed since inspection. Postconditions include receipt persistence and a state transition that references the receipt. The receipt itself should carry a stable identity, object/revision reference, actor identity, decision, policy revision, relevant timestamps, integrity fields, and enough causal linkage to verify it later.

The implementation must reuse existing receipt and state machinery instead of creating an isolated authorization database. If the runtime already uses signed receipts or parent-hash chaining, use those capabilities. The mandate does not authorize redesign of the global Merkle scheme, but authorization receipts must participate in the existing integrity model when the architecture requires it. Cryptographic signing must be real where signing is part of the ratified contract; a fixed dummy digest, placeholder signature, or boolean `signed=true` is a false proof. The verifier must detect altered receipt content, wrong revision, or substitution of a different decision for the original receipt.

The stale-approval case is the core negative proof. An Operator inspects revision R7. Another process changes the object to R8. The Operator then submits approval derived from R7. The runtime must refuse the approval and create no misleading success state. The failure should be explicit and attributable. The browser should be able to refresh and inspect the current object rather than accidentally overriding it. A second negative proof should cover a valid actor attempting to authorize an object that is outside their authority or a policy mode that requires a different escalation path. A third should verify restart/reload: after process restart, the receipt remains present and the authorized state remains reconstructible from durable state.

An anti-centroid countercase is an approval API that returns HTTP success and even displays “Approved” in the UI while the state transition and receipt write occur asynchronously and can be lost on process failure. That implementation looks polished and works in a demo but fails the durability requirement. Another countercase is a receipt that contains actor identity but no object revision hash, allowing the same receipt to be misinterpreted as authorization for a newer state. Both must be rejected.

The UI surface should display the exact object/revision, current state version/hash, policy revision, evidence status, actor authority, consequences, and the fact that a durable receipt will be generated. This does not authorize a visual overhaul. The minimum requirement is that the UI reflects runtime truth and prevents an Operator from approving a stale object without a canonical freshness check. The canonical runtime should remain able to reject or reconcile any stale or replayed browser action.

The executor must classify evidence carefully. A passing receipt parser test is `TEST` evidence for syntax or local semantics. A database persistence test is `EXECUTABLE` or `MIGRATION` evidence for durability. A cryptographic verification test is `EXECUTABLE`. A UI snapshot is `DOCUMENT`/presentation evidence only. The completion report must state what each evidence item actually proves and what it does not. In particular, do not claim “human authorization is durable” merely because a row appears in a local development database if the canonical production runtime writes to a different store or path.

The change boundary is the authorization receipt lifecycle and its minimum integration into the canonical approval operation. Do not implement Q26 policy package authoring, Q27 prospective policy revision pinning, release manifests, external distribution, or outcome attribution. Do not silently alter unrelated receipt formats if compatibility is not preserved. If a shared receipt schema needs a change, establish the smallest backward-compatible path or stop and report the migration collision.

Rollback must preserve historical authorization facts. Never delete an authorization receipt simply because a newer decision supersedes an earlier one. If a mistake is discovered, record a compensating governed action using the existing lifecycle rather than rewriting history. If migration is required, use the repository's established migration mechanism and ensure existing receipts remain verifiable. Completion requires durable positive and negative proof, limitations, exact commit SHA, control-state update where present, and explicit Operator approval/rejection before stopping.

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
- `docs/cae/cae_master_57_question_convergence_canon.md` and the Q-specific decision text for `Q25`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
- the current implementation files named in Section 1 and the Q-specific physical surfaces
- any directly referenced schema, migration, manifest, validator, or receipt implementation required to establish the real authority path

The executor must inspect the current repository state before choosing an edit location. It must not rely solely on documentation examples or historical claims.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M026` / `Q25` as defined by the ratified canon and the physical surfaces named above.

**Inputs.** Existing canonical runtime state, policy/evidence/release artifacts from the immediate upstream questions, current schemas/manifests, and the existing runtime/API/UI boundaries.

**Outputs.** The smallest direct runtime, schema, test, receipt, migration, API, and operator-projection changes required to make the `Q25` decision executable and independently verifiable.

**Dependencies.** `Q24, Q11, runtime state/receipt infrastructure`. Dependencies are inputs and proof conditions, not permission to rewrite their implementations.

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

The requested decision is: **Approve or reject `CA-M026` based on whether the executable evidence proves the ratified `Q25` contract at the canonical authority boundary.** The executor must not infer approval from a green test suite.

## 13. 200–300 word activation prompt

Execute `CA-M026` only. Read the Mandate Authoring Protocol, Q25 in the Master Canon, `docs/cae/UI.md`, `docs/cae/Architecture.md`, the Q25 ledger entry, and the current runtime receipt/state implementation. Implement `INV-AUTH-001`: every consequential human authorization emits an immutable, cryptographically attributable `AuthorizationDecisionReceipt` tied to actor identity and the exact object/revision integrity context. Scope is receipt creation, canonical persistence, verification, stale-approval protection, and the minimum approval UI/API projection needed to show and enforce freshness. Do not implement Q26 policy packages, Q27 prospective policy binding, release, distribution, or outcome work. Prove that approval survives restart, binds to the inspected revision, rejects stale/conflicting approvals, and cannot be simulated by a browser-only flag or dummy signature. Use the existing receipt/integrity machinery when available. Required evidence must include executable runtime tests, persistence evidence, cryptographic verification or equivalent integrity proof, and exact locators. Stop on unresolved shared-schema or authority collisions. Completion requires changed files, tests, evidence classes, false-proof countercase, limitations, commit SHA, and an explicit Operator decision request: approve or reject `CA-M026`. Before editing, identify where approval currently changes canonical state and where receipts are persisted. The proof must distinguish a successful request from a durable state transition. Include a restart or fresh-process verification and an integrity-tampering case.
