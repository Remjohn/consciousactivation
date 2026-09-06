# CA-M030 — Immutable Digest-Backed Release Manifest Contract

## 1. Identity and status

- **Mandate ID:** `CA-M030`
- **Canonical question:** `Q29`
- **Wave:** `04`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-REL-001 / Stage 13 Release Manifest`
- **Dependency set:** `Q24–Q28, Q11`
- **Primary physical surfaces:** `services/pipeline/src/cmf_pipeline/application.py; release manifest schema/builder; release verification path`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → EXECUTE → VERIFY → RECORD EVIDENCE → COMMIT → OPERATOR DECISION → STOP`

This mandate is an execution contract. It authorizes one bounded implementation phase and does not authorize architecture redesign, adjacent canonical questions, or interpretation of undocumented behavior as permission.

## 2. Decision / objective being authorized

This mandate authorizes the release manifest as an immutable, digest-backed distribution contract. The manifest is the boundary between a verified composition and the package that is permitted to leave the system. It must freeze artifact identities, artifact hashes, evidence lineage, composition revisions, authorization decisions, relevant policy revision, release metadata, and a cryptographic integrity seal. The objective is not to make a convenient JSON summary. It is to establish a canonical release object whose integrity can be independently checked and whose mutation invalidates the release.

The source state is an eligible, verified production artifact set. The operation is canonical manifest assembly followed by deterministic serialization, digest calculation, and sealing. The target state is `RELEASE_SEALED` with an immutable manifest identity and integrity root. The actor is the release pipeline or governed release operation. Preconditions include successful composition grounding, required authorization receipts, applicable policy revision, evidence lineage, and all required QA/readiness gates. Validators must ensure every declared artifact exists and matches its recorded digest; every required upstream dependency is present; authorization decisions are current and bound to the correct object/revision; and the manifest seal is valid. Postconditions include a persistent manifest and a verifier that can recompute the integrity result.

The release manifest must be deterministic. If field ordering, serialization, or inclusion rules vary across runs, two semantically identical releases may receive different identities without a legitimate difference, while worse, a byte mutation might go undetected if verification normalizes data too aggressively. The executor should therefore use the repository's canonical serialization conventions and existing hashing utilities. Do not invent a novel Merkle implementation if one already exists. The ledger states a SHA-256 Merkle-root contract; use the established project implementation or its smallest extension. Cryptographic language must be precise: hashing proves byte identity, while signatures or trusted seals provide authority where required by the existing architecture.

The anti-centroid case is especially important. A release manifest may contain correct top-level metadata and a correct-looking root while one referenced artifact file has been modified after sealing. If the verifier only checks the manifest's own bytes or trusts recorded hashes without recomputing them from the actual artifact, it creates a false sense of integrity. Another false proof is a manifest that includes evidence references but not the exact evidence revision/digest, allowing later substitution. The tests must mutate real bytes after sealing and prove that verification fails closed.

The manifest should preserve lineage to the exact composition revisions and policy/authorization decisions that made release eligibility possible. If Q25 generated an `AuthorizationDecisionReceipt`, the release manifest should reference its stable identifier/revision rather than copying only a human-readable “approved” string. Likewise, the policy reference must identify the revision governing the release. This keeps the causal chain reconstructible. The manifest may include metadata that is not semantic content, but it must not become an excuse to omit the authoritative upstream identifiers.

External distribution is downstream and is not implemented here. The release manifest is the input contract to distribution, but the mandate stops before adapter execution. This separation is essential: once a release is sealed, later layers must not rewrite semantic content inside the package. The manifest therefore needs a clear declared payload boundary and a verification rule that distinguishes permitted transport/container metadata from semantic artifacts where the product architecture requires that distinction.

The UI should expose release readiness and manifest identity, including evidence sufficiency, composition validity, QA, provenance, authorization, policy compliance, and integrity/seal status. The `SHIP` action must not be enabled solely from browser-calculated readiness. The runtime must report the release as eligible only after manifest sealing and verification. The mandate does not authorize a full release-console redesign; only the minimum projection and gate wiring are in scope.

Verification must include positive sealing and verification, negative artifact-byte mutation, negative manifest mutation, missing lineage references, mismatched authorization/policy revisions, and persistence/reload of the sealed manifest. A test that creates a manifest from strings and verifies its hash in memory is insufficient. Environment fidelity requires building the manifest from actual repository artifacts and verifying it through the production release path or its canonical equivalent. Evidence classes must state the difference between schema validation, executable verification, and human/operator review.

Rollback must never rewrite a sealed manifest in place. A defective release is a historical artifact. Create a new release revision or mark the old release invalid using the existing lifecycle. Do not delete or overwrite the previous manifest so that historical decisions remain auditable. If an artifact requires regeneration, that creates a new artifact identity and therefore a new manifest. This mandate must resist “fixing” an already sealed package by editing one file and recalculating the root while pretending it is the same release.

Completion requires a stable release manifest format, deterministic sealing, byte-level mutation detection, complete dependency/lineage binding, runtime readiness enforcement, and exact evidence locators. The executor must record limitations such as any missing trusted-signing mechanism if the current repository only supports hashing. It must capture the exact commit SHA and request explicit Operator approval or rejection before stopping. It must not execute external distribution or outcome measurement.

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
- `docs/cae/cae_master_57_question_convergence_canon.md` and the Q-specific decision text for `Q29`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
- the current implementation files named in Section 1 and the Q-specific physical surfaces
- any directly referenced schema, migration, manifest, validator, or receipt implementation required to establish the real authority path

The executor must inspect the current repository state before choosing an edit location. It must not rely solely on documentation examples or historical claims.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M030` / `Q29` as defined by the ratified canon and the physical surfaces named above.

**Inputs.** Existing canonical runtime state, policy/evidence/release artifacts from the immediate upstream questions, current schemas/manifests, and the existing runtime/API/UI boundaries.

**Outputs.** The smallest direct runtime, schema, test, receipt, migration, API, and operator-projection changes required to make the `Q29` decision executable and independently verifiable.

**Dependencies.** `Q24–Q28, Q11`. Dependencies are inputs and proof conditions, not permission to rewrite their implementations.

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

The requested decision is: **Approve or reject `CA-M030` based on whether the executable evidence proves the ratified `Q29` contract at the canonical authority boundary.** The executor must not infer approval from a green test suite.

## 13. 200–300 word activation prompt

Execute `CA-M030` only. Read the Mandate Authoring Protocol, Q29, the Master Canon, `docs/cae/Architecture.md`, `docs/cae/UI.md`, the Q29 ledger entry, `services/pipeline/src/cmf_pipeline/application.py`, and the current release-manifest/sealing implementation. Implement `INV-REL-001`: an immutable, digest-backed Release Manifest binding artifacts, hashes, evidence lineage, composition revisions, authorization decisions, policy revision, and release metadata. Scope is manifest construction, deterministic serialization, cryptographic sealing/verification, mutation detection, persistence, and minimum release-readiness projection. Do not implement external distribution or outcome measurement. Reuse established project hashing/Merkle mechanisms; do not invent a parallel integrity system. Prove positive verification and negative real-byte mutation of an artifact and the manifest itself. Also reject missing or mismatched lineage/authorization/policy references. Schema-only or in-memory hash tests are insufficient; evidence must exercise the canonical release boundary. Preserve historical manifests; never mutate sealed releases in place. Stop on unresolved seal-authority or shared-release-schema collisions. Completion requires changed files, exact tests and evidence locators, evidence classes, limitations, commit SHA, and the Operator decision request: approve or reject `CA-M030`. Before editing, identify which adapter transformations are already considered technical rather than semantic. Do not infer that because a destination accepts a payload, a transformation is authorized. The decisive proof must compare semantic content across the delivery boundary and retain the sealed release identity.
