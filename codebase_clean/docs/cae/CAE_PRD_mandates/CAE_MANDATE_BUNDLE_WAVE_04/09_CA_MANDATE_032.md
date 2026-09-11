# CA-M032 — Causal Outcome Measurement Attribution

## 1. Identity and status

- **Mandate ID:** `CA-M032`
- **Canonical question:** `Q31`
- **Wave:** `04`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `FR-MEAS-001 / Stage 15 Outcome Measurement`
- **Dependency set:** `Q28–Q30, Q01–Q02, Q07–Q08`
- **Primary physical surfaces:** `docs/cae/CAE_Product_Brief/15_Outcome_Measurement.md; outcome telemetry schema/ingestion path; release/campaign attribution boundary`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → EXECUTE → VERIFY → RECORD EVIDENCE → COMMIT → OPERATOR DECISION → STOP`

This mandate is an execution contract. It authorizes one bounded implementation phase and does not authorize architecture redesign, adjacent canonical questions, or interpretation of undocumented behavior as permission.

## 2. Decision / objective being authorized

This mandate authorizes causal outcome attribution for released CAE artifacts. The objective is to make outcome telemetry traceable to the exact release manifest, creative/composition revision, audience hypothesis or tension lineage, and relevant campaign objective rather than collapsing performance into unattributed vanity metrics. Outcome measurement is downstream of release; it must not retroactively rewrite the meaning of a release or treat raw engagement observations as new canonical truth.

The state grammar is: source state `RELEASED / DISTRIBUTED` with immutable release identity → operation `ingest outcome event / normalize / attribute` → target state `ATTRIBUTED_OUTCOME_OBSERVATION` linked to the exact release manifest and causal references. Actor is the outcome measurement ingestion/runtime subsystem. Preconditions include a valid release identity, recognized distribution event or campaign context, valid event schema, and sufficient identifiers to attribute the observation. Validators must reject events that cannot be traced to a real release or that contain impossible revision combinations. Postconditions include durable observations whose attribution fields can be queried and verified. The error route for unresolvable attribution is quarantine or rejection, not silent assignment to the current campaign.

The mandate should establish a clear distinction between observation and interpretation. A click, completion, share, comment, or conversion is an observation. A conclusion such as “tension X caused the lift” is a higher-order interpretation that requires evidence and is outside the authority of raw telemetry. The system may compute causal metrics defined by the current Product Brief, but it must not silently convert a correlated metric into a canonical learning statement. This separation protects the later governed Memory Write-back stage and keeps outcome evidence auditable.

Attribution must be revision-specific. Suppose release R1 uses composition C1 grounded in tension T1, then R2 uses C2. A later outcome event must not be attributed to whichever release is currently active. The event needs an explicit release reference or a deterministic mapping from the distribution record. If the platform has several destination adaptations derived from one sealed release, the measurement model should preserve the common release identity and optionally include destination-specific execution identifiers. This enables comparison without losing provenance.

The anti-centroid case is a dashboard that shows excellent “campaign engagement” and assigns it to the current campaign, but cannot distinguish which exact creative revision or release generated the event. Such a dashboard may be visually persuasive while being causally useless. Another false proof is to join events to a campaign by name and infer the latest release. This fails whenever campaigns have multiple releases or overlapping distributions. The negative suite must include two releases under the same campaign and verify that events remain correctly partitioned by exact release identity.

The executor should inspect the existing outcome telemetry contracts, distribution receipts, campaign identifiers, and release manifest structure. Reuse exact IDs already established. Do not invent a second event identity namespace. If an existing event payload lacks a stable release identifier, add the smallest compatible field or explicit mapping at the canonical ingestion boundary. Avoid broad analytics schema redesign. The mandate's job is attribution correctness, not maximizing dashboard richness.

The system should support late-arriving and duplicated events using existing idempotency or event identity mechanisms where present. If the repository does not yet define a durable event identity, document that gap rather than fabricate deduplication semantics that may conflict with later runtime requirements. Where events cannot be attributed with high confidence, classify them as unresolved and keep them out of causal aggregates that claim exact release attribution. A lower count with clear provenance is preferable to a larger number created by heuristic guessing.

The UI should allow Operators to move from an outcome metric to the exact release, composition revision, audience hypothesis/tension, and distribution event that produced it, at least for the fields already supported by the architecture. The UI must not imply causality from a raw metric alone. Labels should distinguish “observed,” “attributed,” and any stronger verified analytical status defined by the current contracts. This is a projection requirement and must use the canonical runtime state.

Verification must include positive attribution for a real distributed release, negative attribution for unknown or mutated release IDs, two-release separation under one campaign, duplicate/late event behavior where the current event contract supports it, and a trace query from outcome back to release and upstream causal identifiers. Tests must use the actual ingestion/attribution path. A fixture that directly writes an attributed outcome row bypassing the event validator is a false proof. Environment fidelity requires at least one canonical pipeline/API path.

The evidence report must explicitly state what the outcome measurement proves and what it does not. It can prove that an event was attributed to a particular release and causal object. It cannot by itself prove that the creative caused the outcome unless a separate causal-analysis contract says so. This boundary is important because later learning and memory promotion must require additional evidence and governance.

Rollback must preserve raw observations and historical attribution records. If an attribution rule is defective, create a corrected attribution revision or reprocessing record using the established mechanism rather than silently rewriting history. Do not delete events to make metrics look consistent. If a release identity has been corrupted, quarantine affected observations and report the evidence gap.

Completion requires deterministic release-level attribution, durable traceability, negative proof against campaign-name/latest-release heuristics, exact evidence locators, recorded limitations, and commit SHA. Then stop and request explicit Operator approval or rejection. Q32 Memory Write-back is not authorized by this mandate.

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
- `docs/cae/cae_master_57_question_convergence_canon.md` and the Q-specific decision text for `Q31`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
- the current implementation files named in Section 1 and the Q-specific physical surfaces
- any directly referenced schema, migration, manifest, validator, or receipt implementation required to establish the real authority path

The executor must inspect the current repository state before choosing an edit location. It must not rely solely on documentation examples or historical claims.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M032` / `Q31` as defined by the ratified canon and the physical surfaces named above.

**Inputs.** Existing canonical runtime state, policy/evidence/release artifacts from the immediate upstream questions, current schemas/manifests, and the existing runtime/API/UI boundaries.

**Outputs.** The smallest direct runtime, schema, test, receipt, migration, API, and operator-projection changes required to make the `Q31` decision executable and independently verifiable.

**Dependencies.** `Q28–Q30, Q01–Q02, Q07–Q08`. Dependencies are inputs and proof conditions, not permission to rewrite their implementations.

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

The requested decision is: **Approve or reject `CA-M032` based on whether the executable evidence proves the ratified `Q31` contract at the canonical authority boundary.** The executor must not infer approval from a green test suite.

## 13. 200–300 word activation prompt

Execute `CA-M032` only. Read the Mandate Authoring Protocol, Q31, the Master Canon, `docs/cae/Architecture.md`, `docs/cae/UI.md`, `docs/cae/CAE_Product_Brief/15_Outcome_Measurement.md`, the Q31 ledger entry, and the current release/distribution/outcome telemetry implementation. Implement `FR-MEAS-001`: outcome events must attribute to the exact release manifest and creative/composition revision plus the relevant upstream audience/tension identifiers supported by the current contract. Scope is event schema/validation, canonical ingestion and attribution, durable querying, and minimum UI projection of the causal chain. Do not implement Q32 memory promotion. Do not infer attribution from campaign name or “latest release.” Prove positive exact-release attribution and negative handling for unknown/mutated release IDs, plus separation of two releases under one campaign. Distinguish raw observation from causal interpretation; raw telemetry must not become canonical learning merely by ingestion. Use the real event/ingestion path rather than direct fixture writes. Preserve historical observations; correct via governed revision/reprocessing rather than mutation. Required evidence is executable attribution proof with exact locators plus schema/persistence evidence and explicit limitations. Stop on unresolved event-identity or attribution-authority gaps. Completion requires changed files, exact tests/evidence, evidence classes, limitations, commit SHA, and the Operator decision request: approve or reject `CA-M032`.
