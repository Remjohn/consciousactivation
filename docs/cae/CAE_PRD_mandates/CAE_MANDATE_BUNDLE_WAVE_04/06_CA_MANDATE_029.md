# CA-M029 — No-Unanchored-Semantic-Invention Invariant

## 1. Identity and status

- **Mandate ID:** `CA-M029`
- **Canonical question:** `Q28`
- **Wave:** `04`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-NO-INVENT-001 / Stage 10 Composition`
- **Dependency set:** `Q15–Q16, Q17–Q23, Q11`
- **Primary physical surfaces:** `cae_collision_intelligence/composer.py; programs/script_program/CAE.md; evidence reference validators`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → EXECUTE → VERIFY → RECORD EVIDENCE → COMMIT → OPERATOR DECISION → STOP`

This mandate is an execution contract. It authorizes one bounded implementation phase and does not authorize architecture redesign, adjacent canonical questions, or interpretation of undocumented behavior as permission.

## 2. Decision / objective being authorized

This mandate authorizes enforcement of the no-unanchored-semantic-invention invariant at the composition boundary. The governing rule is that substantive factual or semantic claims in composed scripts, storyboards, and other downstream creative artifacts must trace to admitted upstream evidence or be explicitly classified as an authorized connective transformation. Composition is downstream realization, not a new source of meaning. The mandate therefore targets the point where semantic content is assembled into an output artifact and must reject unsupported invention before release-oriented downstream work.

The critical distinction is between evidence-backed statements and connective language. A connective transformation may organize, sequence, summarize, or stylistically bridge already-admitted material when the program contract permits it. A new factual claim, attributed statement, numeric assertion, or causal conclusion that is not supported by admitted evidence is not automatically made acceptable merely because it sounds plausible. The composer needs a machine-checkable representation of evidence references or an explicit connective classification. Free-form prose alone cannot be the authority because an evaluator cannot reliably determine whether a sentence is grounded from text aesthetics.

State grammar is: source state `COMPOSITION_DRAFT` with evidence references and semantic units → operation `validate grounding / resolve evidence lineage / compile` → target state `COMPOSITION_ADMITTED` only when every substantive semantic unit passes the grounding predicate. Actor is the composition/runtime verifier. Preconditions include admitted evidence identifiers, valid evidence hashes or revision references, and a known composition schema. Validators must reject unresolved evidence references, mismatched evidence revisions, missing provenance for substantive claims, and prohibited semantic transformations. Postconditions include a composition artifact whose semantic units carry their grounding classification and whose validation state can be inspected later. The error route is a fatal composition block, not a warning, when an unanchored factual claim is encountered.

A central anti-centroid failure is a script that uses verified evidence references on 80% of its claims and contains one plausible, polished sentence with no anchor. A superficial coverage score might pass because most claims are grounded. The mandate must instead define the gate at the semantic-unit level for material claims: one fatal unanchored claim is enough to block compilation when the contract requires it. Another false proof is to anchor an entire paragraph to one evidence segment even though the paragraph contains multiple independent factual claims. Evidence linkage must be specific enough to establish support, or the claim must be decomposed or classified appropriately.

The executor should inspect how the existing composer represents candidate content, evidence segments, expression moments, and validation state. Reuse existing types such as evidence references and expression moments where available. Do not create a generic “truth score” that collapses the grounding predicate into a soft ranking. The required invariant is a hard admissibility rule. Likewise, do not ask a model to decide its own grounding without independent structural validation. Model-produced rationales can be supporting `HYPOTHESIS` evidence; they are not sufficient by themselves for deterministic admission.

The mandate should also define what it does not prove. An anchor can establish provenance linkage, but an anchor does not automatically prove that the evidence actually supports every semantic inference derived from it. Where the repository already has evidence acceptance or collision verification logic, composition grounding should consume that admitted evidence state instead of re-verifying source authenticity from scratch. The composer should reject unadmitted evidence references even if the underlying media exists. This preserves the causal order: capture/admission first, composition second.

The UI may display grounding badges, evidence references, and blocking reasons. It must never allow an Operator to bypass a constitutional grounding failure simply by clicking “continue.” A program-specific policy may define permitted connective transformations, but that policy must be explicit and versioned. If a requested transformation is not represented in the current program contract, the safe response is to block and request an owned specification decision rather than inventing a new exception.

Verification must include positive composition with fully admitted evidence, negative composition with an unanchored factual claim, negative composition with a broken/mismatched evidence hash or revision, and a regression for a valid connective transformation that should remain permitted. Tests must use the real composition/compiler boundary. A unit test that tags strings with `anchored=true` and asserts they pass is a false proof because it never verifies that the tag was derived from an admissible evidence object. Environment fidelity means using the actual evidence identifiers and verification path employed by the runtime.

The executor must preserve causal lineage into the resulting composition artifact so downstream release manifests can later identify exactly which evidence and revisions were used. This mandate does not authorize creation of the release manifest itself. It merely ensures the composition output contains the necessary grounding references. Do not modify distribution, outcome, or memory code. Do not soften a fatal grounding failure to improve yield or creative completeness.

Rollback is straightforward: revert the bounded composer/verifier changes while retaining historical composed artifacts. Never rewrite already-produced compositions to make a failed grounding check disappear. Historical artifacts should remain inspectable with their recorded validation state. Completion requires hard rejection of unanchored semantics, positive proof for allowed evidence-backed content, evidence lineage, limitations, and commit SHA, followed by explicit Operator approval/rejection.

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
- `docs/cae/cae_master_57_question_convergence_canon.md` and the Q-specific decision text for `Q28`
- `docs/cae/UI.md`
- `docs/cae/Architecture.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
- the current implementation files named in Section 1 and the Q-specific physical surfaces
- any directly referenced schema, migration, manifest, validator, or receipt implementation required to establish the real authority path

The executor must inspect the current repository state before choosing an edit location. It must not rely solely on documentation examples or historical claims.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M029` / `Q28` as defined by the ratified canon and the physical surfaces named above.

**Inputs.** Existing canonical runtime state, policy/evidence/release artifacts from the immediate upstream questions, current schemas/manifests, and the existing runtime/API/UI boundaries.

**Outputs.** The smallest direct runtime, schema, test, receipt, migration, API, and operator-projection changes required to make the `Q28` decision executable and independently verifiable.

**Dependencies.** `Q15–Q16, Q17–Q23, Q11`. Dependencies are inputs and proof conditions, not permission to rewrite their implementations.

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

The requested decision is: **Approve or reject `CA-M029` based on whether the executable evidence proves the ratified `Q28` contract at the canonical authority boundary.** The executor must not infer approval from a green test suite.

## 13. 200–300 word activation prompt

Execute `CA-M029` only. Read the Mandate Authoring Protocol, Q28, the Canon, `docs/cae/Architecture.md`, `docs/cae/UI.md`, the Q28 ledger entry, `cae_collision_intelligence/composer.py`, and `programs/script_program/CAE.md` plus the current evidence-admission interfaces. Enforce `INV-NO-INVENT-001`: substantive semantic claims in composition must be anchored to admitted evidence or explicitly classified as an authorized connective transformation. Scope is the composer/verification boundary and minimum evidence-lineage/UI projection. Do not implement release manifests, distribution, outcomes, or memory. Reject missing/unresolved/mismatched evidence references and reject the “good-looking” case where one plausible factual claim is unanchored even though the rest of the script is grounded. Do not use model self-judgment or a soft score as a substitute for the hard predicate. Required evidence is real compiler/runtime positive and negative tests plus exact evidence locators. Environment fidelity requires the canonical evidence-admission path. Stop on undefined connective semantics or authority collisions. Completion requires changed files, exact tests, evidence classes/locators, limitations, commit SHA, and Operator approval/rejection request for `CA-M029`. Before editing, identify the exact release artifact set and existing integrity utilities used by the pipeline. Verify real bytes, not only manifest text. The decisive negative test must change a referenced artifact after sealing and demonstrate that the canonical release verification path blocks the package.
