# CA-M027 — Declarative Policy Rule Packages

## 1. Identity and status

- **Mandate ID:** `CA-M027`
- **Canonical question:** `Q26`
- **Wave:** `04`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `FR-AUTH-002 / Stage 12 Human Authorization`
- **Dependency set:** `Q24–Q25`
- **Primary physical surfaces:** `programs/script_program/CAE.md; programs/editorial_storyboard_program/program_manifest.yaml; relevant policy package schemas/loaders`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → EXECUTE → VERIFY → RECORD EVIDENCE → COMMIT → OPERATOR DECISION → STOP`

This mandate is an execution contract. It authorizes one bounded implementation phase and does not authorize architecture redesign, adjacent canonical questions, or interpretation of undocumented behavior as permission.

## 2. Decision / objective being authorized

This mandate authorizes the declarative representation of authorization rules as versioned, inspectable policy packages. The desired result is not a second policy engine; it is a canonical package format that expresses layer-specific delegation, escalation conditions, and evidence prerequisites in a structured, deterministic form. Existing program manifests and CAE program contracts already express governance concepts. The mandate must establish a clear package boundary so the runtime can load and validate policy rules without relying on prose parsing, hidden defaults, or model interpretation.

A valid policy package must be machine-readable, schema-valid, versioned, and explicit about authority predicates. Where the repository already supports YAML or JSON manifests, the implementation should extend those conventions. A package should identify its schema/version, applicable program or scope, rule identifiers, required authority lane or actor class, escalation conditions, evidence prerequisites, and any references to immutable policy dependencies. Unknown fields should either be explicitly ignored under a documented compatibility contract or rejected; the executor must follow existing repository conventions rather than inventing permissive behavior. The critical invariant is that a package cannot silently weaken constitutional requirements. The package is a declarative expression of permissible delegation, not a permission to rewrite the CAE constitution.

The state grammar is: source state `UNLOADED/UNKNOWN_POLICY_PACKAGE` → operation `load + schema-validate + semantic-validate + canonicalize + digest` → target state `ADMITTED_POLICY_PACKAGE` with stable package identity and revision/digest. Actor is the runtime policy loader or governed deployment process. Preconditions include a known package schema, correct program binding, valid required fields, and any cryptographic or registry checks required by the existing architecture. Validators must reject malformed rule structures, ambiguous predicates, missing rule identifiers, unsupported schema versions, and any rule that attempts to disable non-waivable controls. Postconditions are that the runtime can retrieve one canonical policy package and that policy evaluation references its revision/digest. Error routes are fail-closed package rejection with an evidence-bearing reason.

The executor must distinguish package declaration from runtime authority. A YAML file existing in the repository is `REGISTRY_SOURCE`/`DOCUMENT` evidence. It becomes runtime authority only when the canonical loader validates it and the runtime evaluation path actually uses the loaded representation. A particularly dangerous false proof is to write a schema file and a fixture that validate successfully while leaving the runtime to continue using hardcoded defaults. That implementation looks complete in a code review because all artifacts exist, but policy changes have no effect. The mandate must therefore include a test that changes a declared rule and demonstrates an observable authorization decision difference in the real runtime path, subject to the current policy semantics.

Another anti-centroid failure is a permissive parser that accepts contradictory rules and resolves them using rule order, accidental dictionary iteration, or “last one wins.” Policy is too consequential for implicit conflict resolution. If two rules conflict and the architecture has not defined precedence, the safe behavior is to reject the package and request an Operator decision or an owned specification correction. Similarly, a package containing a wildcard that effectively means “allow everything” must not be accepted as equivalent to YOLO unless the canonical policy model explicitly defines that mapping. Policy semantics must be deliberate and testable.

The package should be canonicalizable so that equivalent logical packages have deterministic serialization where the architecture requires digest identity. The mandate does not authorize a global signing infrastructure redesign. If package signatures are already part of the system, verify them; if not, do not invent a new trust root solely for this mandate. Instead, establish the package validation and identity boundary and document the remaining trust mechanism. A digest can identify bytes, but it does not by itself prove that the package came from an authorized source. The completion report must not overstate the assurance level.

The program manifest examples should be updated only as direct exemplars of the new package contract. Do not edit every program in the repository. Use one or two representative existing manifests to prove the integration path. Preserve current program semantics unless the mandate specifically requires them to be expressed through the new package representation. If compatibility adapters are needed, they should translate legacy forms into the canonical package at a clearly bounded boundary, with tests proving that they cannot silently bypass validation.

The UI and operator projection should make policy package identity, revision, scope, and validation status visible wherever an Operator is asked to reason about consequential delegation. This is a projection requirement, not a new source of policy. A user selecting an option in the UI must ultimately reference the same canonical package/revision that the runtime evaluates. Any stale cached package must be detected when a consequential action begins.

Verification must include positive package validation, rejection of malformed or contradictory packages, rejection of attempts to weaken constitutional invariants, runtime consumption of the admitted package, deterministic identity/digest behavior where required, and a compatibility regression test for existing policy-bearing programs. Evidence must include schema and executable classes with exact file/test locators. A test that only validates the schema is insufficient because the property of interest includes runtime consumption. Environment fidelity requires using the actual loader and runtime path, not a mock that bypasses package admission.

Rollback must not invalidate historical decisions by mutating old policy packages in place. Policy packages are versioned artifacts. A correction should create a new revision/package and preserve the old one for historical reference. If the package loader finds an unknown schema version, fail closed rather than guessing. If a shared registry collision occurs with a later mandate, stop and identify the integration owner.

Completion occurs when at least one real program path loads a canonical versioned policy package, applies its declared predicates at runtime, rejects unsafe or ambiguous packages, and exposes enough identity/provenance to explain the decision. After evidence is recorded and the exact commit captured, the executor stops and requests Operator approval or rejection. It must not start Q27 automatically.

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
- `docs/cae/cae_master_57_question_convergence_canon.md` and the Q-specific decision text for `Q26`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
- the current implementation files named in Section 1 and the Q-specific physical surfaces
- any directly referenced schema, migration, manifest, validator, or receipt implementation required to establish the real authority path

The executor must inspect the current repository state before choosing an edit location. It must not rely solely on documentation examples or historical claims.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M027` / `Q26` as defined by the ratified canon and the physical surfaces named above.

**Inputs.** Existing canonical runtime state, policy/evidence/release artifacts from the immediate upstream questions, current schemas/manifests, and the existing runtime/API/UI boundaries.

**Outputs.** The smallest direct runtime, schema, test, receipt, migration, API, and operator-projection changes required to make the `Q26` decision executable and independently verifiable.

**Dependencies.** `Q24–Q25`. Dependencies are inputs and proof conditions, not permission to rewrite their implementations.

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

The requested decision is: **Approve or reject `CA-M027` based on whether the executable evidence proves the ratified `Q26` contract at the canonical authority boundary.** The executor must not infer approval from a green test suite.

## 13. 200–300 word activation prompt

Execute `CA-M027` only. Read the Mandate Authoring Protocol, Q26, the CAE Canon, `docs/cae/UI.md`, `docs/cae/Architecture.md`, Q26 ledger entry, `programs/script_program/CAE.md`, and `programs/editorial_storyboard_program/program_manifest.yaml` plus the current policy loader. Implement `FR-AUTH-002`: versioned declarative JSON/YAML policy packages with explicit, typed authorization predicates, validation, canonical identity/digest, and runtime consumption. Do not implement Q27 prospective binding or later release/distribution work. Do not create a second policy engine or let prose, UI state, model output, or hardcoded defaults become authority. Prove positive loading and runtime effect, rejection of malformed/contradictory packages, rejection of constitutional-policy weakening, and compatibility for at least one existing program manifest. Required evidence is schema plus executable runtime proof with exact locators; schema-only validation is insufficient. Preserve historical packages by revision rather than mutation. Stop on undefined precedence or shared-registry collisions. Completion requires changed files, tests, evidence classes, limitations, commit SHA, and the Operator decision request: approve or reject `CA-M027`. Before editing, identify the canonical policy artifact identity and the exact execution record or state that can safely carry its revision. Do not substitute a live campaign lookup for a pinned execution reference. The decisive proof must show two executions under different prospective revisions behaving independently.
