# CA-M031 — External Distribution as Execution-Only Delivery

## 1. Identity and status

- **Mandate ID:** `CA-M031`
- **Canonical question:** `Q30`
- **Wave:** `04`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `FR-DIST-001 / Stage 14 External Distribution`
- **Dependency set:** `Q29, Q24–Q27`
- **Primary physical surfaces:** `docs/cae/CAE_Product_Brief/14_External_Distribution.md; distribution adapter boundary; pipeline delivery execution path`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → EXECUTE → VERIFY → RECORD EVIDENCE → COMMIT → OPERATOR DECISION → STOP`

This mandate is an execution contract. It authorizes one bounded implementation phase and does not authorize architecture redesign, adjacent canonical questions, or interpretation of undocumented behavior as permission.

## 2. Decision / objective being authorized

This mandate authorizes the external distribution boundary as an execution-only delivery layer. Its governing rule is that distribution consumes an already sealed Release Manifest and may perform only the technical transformations explicitly permitted for destination delivery, such as container or codec adaptation. Distribution must not alter the semantic content, evidence lineage, composition meaning, authorization state, or release identity. The purpose is to prevent the last mile from becoming an uncontrolled semantic rewrite layer.

The source state is `RELEASE_SEALED` with verified manifest and eligible delivery configuration. The operation is `DISTRIBUTE` through an authorized adapter using the sealed release package. The target state is a distribution event referencing the same release manifest and a destination-specific delivery result. Actor is the distribution runtime/adapter under the established authority lane. Preconditions include a valid sealed release, current authorization, destination configuration, and any required policy gate. Validators must verify the manifest before transmission and establish that the adapter's changes are limited to the allowed technical transform class. The target receipt must identify the release manifest, destination, adapter version/configuration, delivery result, and relevant integrity evidence.

Distribution adapters must not get a writable view of semantic source objects. The clean boundary is immutable release input plus destination transformation output. An adapter may rewrap a video into another container or transcode according to an approved technical profile, but it must not edit captions, spoken words, script text, narrative order, evidence references, or other semantic payloads unless the product contract explicitly defines that transformation as non-semantic and verifiable. When in doubt, the adapter should fail closed and require an explicit policy decision rather than assume the change is harmless.

A strong anti-centroid failure is an adapter that “fixes” a problematic title, subtitle, audio phrase, or metadata field because a destination API rejects the package. The delivery succeeds and may even look better, but the released semantic artifact has changed after sealing. The mandate must prevent such behavior. Another false proof is to test only that an HTTP upload endpoint was called. That proves transport, not execution-only semantics. The required test must compare the semantically relevant payload before and after adaptation and demonstrate that only allowed container/codec transformations occurred.

The executor must inspect existing destination adapters and identify which transformations are already supported. Do not create a generalized transformation framework. Implement or harden only the canonical boundary needed to consume the sealed Release Manifest. Where a destination requires technical changes, represent the transformation class explicitly and log it in the delivery receipt. If the adapter needs a semantic transformation that has not been ratified, stop before implementing it. This is a direct application of the supreme causal law: downstream delivery cannot invent upstream meaning.

The distribution operation should be idempotent where the existing architecture permits safe retries. A retry should not silently create multiple logically distinct release revisions. The executor should use established delivery identifiers or idempotency keys if present. It must not create an ad-hoc retry mechanism that weakens release integrity. If a destination acknowledges delivery but the local receipt write fails, recovery should follow the repository's existing reconciliation pattern rather than marking the release delivered based solely on the remote UI response.

The Operator UI should make the relationship explicit: this shipment consumes a particular sealed release manifest, and the adapter/version used for delivery is visible. The user should not be led to believe that “Ship” means “edit and upload.” Readiness should originate from runtime state. The delivery result should link back to the exact release identity so later outcome measurement can attribute events to the correct artifact.

Verification should include: successful delivery from a valid sealed release; rejection when the manifest is mutated or fails verification; a semantic payload immutability test across adapter execution; rejection of an unsupported semantic transformation; idempotent retry behavior where supported; and a receipt/audit test showing the exact release manifest and adapter identity. A unit test that mocks the adapter and asserts it was called is insufficient. Environment fidelity requires at least one real or repository-native integration path through the distribution boundary.

Evidence classes must distinguish transport success from semantic integrity. `EXECUTABLE` evidence can prove actual adapter behavior; `TEST` can prove specific predicates; destination API responses can be `EXECUTABLE` only if captured through the canonical path. Documentation about allowed codec changes is `DOCUMENT` until enforced by code. If a destination-specific limitation prevents complete end-to-end delivery in the current environment, record the exact limitation and stop without claiming general distribution is verified.

Rollback and recovery must preserve the sealed release. If an adapter bug is found, disable or revoke that adapter path and retry from the unchanged release manifest after the correction. Never modify the release artifact to accommodate a broken adapter. Historical delivery receipts should remain intact. If a destination requires re-upload after failure, use a new distribution attempt identifier while retaining the same release identity when no semantic change occurred.

Completion means the distribution layer demonstrably consumes sealed releases, applies only permitted technical transformations, refuses semantic rewriting, records auditable delivery evidence, and fails closed on invalid release integrity. Then stop and request Operator approval/rejection. Do not proceed to outcome attribution or memory work.

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
- `docs/cae/cae_master_57_question_convergence_canon.md` and the Q-specific decision text for `Q30`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
- the current implementation files named in Section 1 and the Q-specific physical surfaces
- any directly referenced schema, migration, manifest, validator, or receipt implementation required to establish the real authority path

The executor must inspect the current repository state before choosing an edit location. It must not rely solely on documentation examples or historical claims.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M031` / `Q30` as defined by the ratified canon and the physical surfaces named above.

**Inputs.** Existing canonical runtime state, policy/evidence/release artifacts from the immediate upstream questions, current schemas/manifests, and the existing runtime/API/UI boundaries.

**Outputs.** The smallest direct runtime, schema, test, receipt, migration, API, and operator-projection changes required to make the `Q30` decision executable and independently verifiable.

**Dependencies.** `Q29, Q24–Q27`. Dependencies are inputs and proof conditions, not permission to rewrite their implementations.

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

The requested decision is: **Approve or reject `CA-M031` based on whether the executable evidence proves the ratified `Q30` contract at the canonical authority boundary.** The executor must not infer approval from a green test suite.

## 13. 200–300 word activation prompt

Execute `CA-M031` only. Read the Mandate Authoring Protocol, Q30, the Canon, `docs/cae/Architecture.md`, `docs/cae/UI.md`, `docs/cae/CAE_Product_Brief/14_External_Distribution.md`, the Q30 ledger entry, and the current distribution adapters/pipeline path. Implement `FR-DIST-001`: external distribution is execution-only delivery of a sealed Release Manifest, with only explicitly permitted container/codec technical transformations. Scope is release verification at delivery, adapter boundary hardening, semantic immutability proof, delivery receipt/idempotency behavior using existing mechanisms, and minimum UI/audit projection. Do not modify semantic content, evidence lineage, authorization, composition, or release identity. Do not implement outcome measurement. Prove positive delivery from a valid sealed release and negative cases for mutated/invalid releases and unsupported semantic transformations. A mocked upload-call test is insufficient; exercise the canonical or repository-native distribution boundary. Record exact release identity, adapter identity, and evidence locators. Stop on destination requirements that imply unratified semantic changes. Completion requires changed files, tests, evidence classes/locators, limitations, commit SHA, and Operator approval/rejection request for `CA-M031`. Before editing, identify the canonical distribution/release identifier available to incoming outcome events. Do not join on campaign name or latest release. The decisive proof must isolate two releases under one campaign and demonstrate exact attribution and safe treatment of unresolvable events.
