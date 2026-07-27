---
document_type: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-AHP-003
title: Source-Backed Content Batch, Archetype Routing, and Derivative Job Contracts
product: Atomic Harness Pipeline
version: 2.1.0-candidate
issued_on: '2026-07-22'
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: INDEPENDENT_AUDIT_REQUIRED
writing_wave: 11
output_path_class: DIRECT_PRODUCT_SPEC_PATH
controlling_frs: [FR-133, FR-134, FR-135, FR-136]
controlling_stories: [ST-03.02, ST-03.03]
upstream_draft_dependencies:
  - {edge_id: SDE-040, spec_id: TS-AHP-002, quality_state: WRITTEN_PENDING_AUDIT, sha256: 3e76ee7e4ec8f3b288a58bb8b8eb886195d9ad17097c67ded613c22fbb3dccd4, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {edge_id: SDE-041, spec_id: TS-INT-005, quality_state: WRITTEN_PENDING_AUDIT, sha256: ffdac05544b34230765c0e3f0eca32f77a471886fdb1871ecec4ba7b536f6416, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {edge_id: SDE-042, spec_id: TS-AIR-015, quality_state: WRITTEN_PENDING_AUDIT, sha256: 58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {edge_id: SDE-043, spec_id: TS-AIR-016, quality_state: WRITTEN_PENDING_AUDIT, sha256: 5e4437baff399f65a2b0b63c6f3a43e91145fbd188dbcb503bf67cc09e24cddc, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
---

# TS-AHP-003 — Source-Backed Content Batch, Archetype Routing, and Derivative Job Contracts

This document is a specification-only candidate. It does not authorize implementation, a Development Capsule, product adoption, external execution, production spend, publication, certification, or `ACCEPTED_FOR_BUILD`.

## 1. Files and authorities read

The writer consumed four exact Wave 11 inputs under the mandatory label `DRAFT_DEPENDENCY_NOT_ACCEPTED`:

| Upstream draft | Frozen state and SHA-256 | Interface admitted for writing | Mandatory revision impact |
|---|---|---|---|
| `TS-AHP-002` | `WRITTEN_PENDING_AUDIT`; `3e76ee7e4ec8f3b288a58bb8b8eb886195d9ad17097c67ded613c22fbb3dccd4` | Exact `AtomicHarnessDefinition` intake, four-part compiler-profile dispatch, read-only `HarnessRequirementGraphProjection`, and immutable `HarnessExecutionBindingManifest`. | Reopen sections 3, 5, 6, 8, 9, and 10 if the hash changes. |
| `TS-INT-005` | `WRITTEN_PENDING_AUDIT`; `ffdac05544b34230765c0e3f0eca32f77a471886fdb1871ecec4ba7b536f6416` | Approved `ExpressionIngredientInventoryVersion`, `AssetPackageSpecVersion`, exact `EvidencePointer` and package restriction/approval/handoff semantics. | Reopen sections 3, 5, 6, 8, 9, and 10 if the hash changes. |
| `TS-AIR-015` | `WRITTEN_PENDING_AUDIT`; `58946bef28d60b991fd2897429f199534c104b9096b977125f2e5b6a710a03d8` | AIR-owned `SemanticProductionPackage`, approved Final Script, Primitive/archetype coalition, role/tension, category/profile, evaluation and wrong-reading-lock references. | Reopen sections 3, 5, 6, 8, 9, and 10 if the hash changes. |
| `TS-AIR-016` | `WRITTEN_PENDING_AUDIT`; `5e4437baff399f65a2b0b63c6f3a43e91145fbd188dbcb503bf67cc09e24cddc` | AIR-owned `ActivationTransferContract`, exact transformation law, five checkpoints, source lineage, transfer evaluation, repair, supersession and invalidation. | Reopen sections 3, 5, 6, 8, 9, and 10 if the hash changes. |

Those drafts are not accepted authority. Current Constitution V1.1 and current product PRDs remain binding. Candidate V2.1 ownership records may define this writing interface because Prompt 02C explicitly authorizes specification work, but candidate authority remains `CANDIDATE_NOT_CURRENT`.

| Source | State / SHA-256 | Class | Fact used |
|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | required authority | Harnesses preserve upstream Activative meaning; Pipeline executes rather than becoming the compiler or source of meaning. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | candidate ownership | AIR, Interview Expression, Builder, Pipeline, VAE, Delegation, and Studio retain distinct sovereign responsibilities. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | candidate object ownership | Pipeline owns execution plans, jobs, runtime state, and receipts but references source and semantic objects owned elsewhere. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification-only authorization; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | required write gate | Writing and later technical convergence are permitted; build, production, and certification are not. |
| F23 `Source-Backed Content Batch and Archetype Routing` | candidate; `94833575d71b8c04fb0bcab11ca02e99865502bbb7c8445d25a41c9c985d816d` | controlling feature | Defines FR-133 through FR-136 and the laws: no route is manufactured, each job retains its Harness/evidence, and shared changes invalidate only dependents. |
| AHP `EPICS_AND_VERTICAL_STORIES.md` | candidate; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | controlling Stories | ST-03.02 compiles immutable jobs; ST-03.03 routes supported archetypes and reuses source analysis without duplicates. |
| `SRC-AM-001` Studio Architecture Amendment V2.1 archive | required authority input; `9059fe3cad98c5d6ca0f9584f091ac503a5e5a9279a4a476821db816dc7603b8` | required authority | Format 02 is deferred; Studio supervises and issues typed corrections without changing Harness meaning. |
| `SRC-INT-001` Interview-First Expression Engine | required unique evidence; `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | required unique evidence | Human activation produces approved source expression and reusable multi-format source ingredients; the backend multiplies rather than replaces it. |
| `SRC-INT-003` Expression Capture and Archetype Routing Update | required unique evidence; `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | required unique evidence | Assets are traceable to Expression Moments, archetype/derivative routes, exact capture evidence, and evaluation requirements. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/atomic_harness_definition.py` | current Builder implementation; `8d4d174eb3c54f152a099053302dd631f686c27b070b7dde989c4901afd8e4c6` | required current implementation | Builder definitions are immutable, canonical-hashed, execution-free, section-complete and explicitly non-production/non-certified. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_runtime_rules.py` | current Builder implementation; `cef3bf6673bde2ec501c01099f0efee12b7ad47cb8379c68a58b074a13c35512` | required current implementation | Category operating rules preserve category identity, category-native runtime/evaluation/repair units, selective rerun, non-inherited certification, and evidence-bearing generic inapplicability. |
| `SRC-AM-002` seven-day parallel-production amendment | bytes available but `DEFERRED_REFERENCE` | deferred reference | No factual claim in this spec depends on it. |
| `SRC-EXT-023` external AI shorts repository | unavailable and `DEFERRED_REFERENCE` | deferred reference | No claim, algorithm, threshold, or implementation decision is attributed to it; `SOURCE-GAP-SRC-EXT-023` remains research backlog only. |

The exact output path is authorized as `DIRECT_PRODUCT_SPEC_PATH`. No target-local or ancestor `AGENTS.md` exists. The obsolete assignment path under `04_ATOMIC_HARNESS_PIPELINE` is superseded by the frozen Prompt 02/02C path under `05_ATOMIC_HARNESS_PIPELINE`.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem

One approved interview package can support several useful derivatives, but naive batch orchestration creates four correctness failures. It can duplicate expensive analysis, manufacture a plausible archetype route unsupported by the source, allow jobs to read material outside their grant, or flatten AIR-owned semantic intent into free-form scheduler notes. Those errors waste production spend and, more seriously, create assets whose source, role, tension, Primitive function, Final Script, transfer law, Harness, or review authority cannot be proven.

The Pipeline currently has no implementation. The current Builder provides immutable Harness contracts and category rules, not batch execution. Interview Expression and AIR candidate drafts define source and semantic handoffs, but they are not Pipeline batch/job models. A complete Pipeline specification is therefore required before code can exist.

### 2.2 User and system outcome

A Conscious Content Operator selects an exact accepted source package, a valid AIR semantic package, authorized output objectives, and Builder-defined Harness bindings. Pipeline deterministically compiles one immutable `ContentBatchOrchestrationProgram`, explains eligible and excluded derivative routes, shares exact read-only analysis by reference, and emits one independently cancelable `ContentDerivativeJob` per selected output. Every admission, denial, reuse, conflict, selection, invalidation, and replay is attributable and hash-pinned.

### 2.3 Bounded solution

The solution defines:

1. strict admission of approved Interview Expression, AIR, and Builder/Pipeline binding inputs;
2. a deterministic batch compiler that represents targets, dependencies, budgets, deadlines, review modes, shared source bindings, and claim ceilings without changing upstream meaning;
3. an eligibility-only archetype/Harness router that ranks only routes already admitted by AIR, source evidence, category/profile registries, and current Harness availability;
4. immutable derivative-job contracts with exact source grants, semantic refs, Harness binding, capabilities, evaluation, review, and transfer requirements;
5. deterministic reuse, overlap, duplicate, conflict, and diversity-plan compilation before external spend;
6. atomic persistence, replay, cancellation, supersession, selective invalidation, and historical reproduction.

### 2.4 In scope

- FR-133 through FR-136 and Stories ST-03.02 and ST-03.03.
- Source-backed batch compilation across authorized short video, Carousel, SuperVisual, animation, and other registered categories/profiles.
- Route eligibility, evidence explanation, exclusions, human choice among genuine alternatives, and immutable route receipts.
- Shared read-only source-analysis bindings, exact reuse keys, duplicate/conflict detection, and diversity planning.
- Derivative job admission and pre-execution state; no renderer/provider work.
- Typed commands, objects, failures, events, repositories, APIs, tests, future implementation paths, and completion evidence.

### 2.5 Out of scope and non-goals

- Capturing, transcribing, approving, correcting, or reconstructing Interview Expression evidence.
- Compiling Primitive/archetype meaning, Matrix of Edging, psychological role/tension, Final Script, Activation Transfer Contract, Visual Semantic Pack, Visual Narrative Program, or Composition Intent.
- Editing Builder-owned `AtomicHarnessDefinition`, category rules, Feature Contracts, or the execution binding.
- Making VAE production decisions, selecting models/LoRAs/conditioning, generating candidates, or accepting visual production.
- Delegation transport, Studio UI/direct manipulation, publication, production certification, or Format 02 activation.
- Inventing route-score thresholds, source-overlap thresholds, diversity quotas, cost coefficients, or evaluation policy absent a governed profile.
- Treating a generated summary, cache entry, transcript embedding, or batch plan as source or semantic authority.

## 3. Governing decisions and constraints

### 3.1 Current and candidate authority

Constitution V1.1 and current PRDs remain binding. Candidate V2.1 matrices, the AHP feature/Stories, and all four upstream specs are `CANDIDATE_NOT_CURRENT`. Prompt 02C authorizes their use for specification writing only. This document cannot be accepted for build above `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` until the required ratification/adoption receipt exists.

### 3.2 Product sovereignty

| Product | Owns | Pipeline may do | Pipeline must never do |
|---|---|---|---|
| Interview Expression | live source, source authorization, Reaction Receipts, Expression Moments, evidence graph, ingredient inventory, Asset Package Spec and IE approvals | Verify and pin approved exact refs; consume restrictions and source grants | Invent/repair quotes, classify missing evidence, loosen restrictions, or turn proposals into approved source truth |
| AIR | semantic lifecycle and production-program meaning, including role/tension, Matrix, Primitive/archetype coalition, Brand/Voice/Visual DNA, Final Script, Activation Transfer Contract and semantic package | Validate, reference, schedule and preserve AIR-owned values | Re-rank semantic truth, choose a new coalition, rewrite the Final Script, or reconstruct missing meaning |
| Builder | `AtomicHarnessDefinition`, category/profile execution-free requirements, Feature Contract dependencies and wrong-reading inheritance law | Consume an eligible exact `HarnessExecutionBindingManifest` | Mutate a Harness, infer a missing Harness, change category/profile, or absorb VAE production choices |
| Pipeline | batch program, route-eligibility projection, derivative jobs, shared-analysis binding, execution state, conflict/dedupe decisions, receipts | Compile and execute within all admitted contracts | Become source, semantic, Harness, visual-production, transport, or human-decision authority |
| VAE | Visual Production Plan, visual production route and realization, production evaluation/repair/acceptance and visual lineage | Receive separately authorized visual demands through later specs | Have its choices preselected by this batch spec or treat job eligibility as production acceptance |
| Delegation | validation, compatibility negotiation, immutable routing, replay protection and audit receipts | Transport later immutable contracts | Create meaning or change payload bytes |
| Studio / human operator | projection, typed commands, attributable resolution and authority where assigned | Select among eligible alternatives and authorize bounded commands | Mutate stored upstream truth through presentation state |

`Activative Contract Compiler != Activative Intelligence Runtime`. Pipeline is neither.

### 3.3 No route is manufactured

A route is eligible only when all of the following independently pass:

- the source package is approved/current and grants the intended use/platform;
- the referenced Expression Moments/ingredients are approved and source-supported;
- AIR supplies the exact archetype coalition, viewer role/tension, derivative function, transfer constraints and category/profile intent;
- Builder supplies a current compatible Harness and Pipeline binding for that category/profile;
- required capabilities/evaluation/review owners are available;
- no lifecycle state, wrong-reading lock, source restriction, supersession, revocation or conflict forbids use.

Pipeline may order eligible alternatives using a versioned `RouteRankingProfile`. It may not create an archetype, semantic purpose, target audience role, source claim, or Harness to make a request pass. If multiple genuine alternatives remain, the route decision is `HUMAN_SELECTION_REQUIRED`. If none remain, it is `NO_ELIGIBLE_ROUTE` and the job is blocked without blocking unrelated jobs.

### 3.4 Exact lineage is not a note

Every batch and job carries exact immutable references to the source package, inventory, ingredient/Moment evidence, Semantic Production Package, Activation Transfer Contract, approved Final Script, role/tension, Matrix/Edge, Primitive and archetype coalitions, category/profile, Harness definition/binding, evaluation profile, restrictions and wrong-reading locks. A text summary cannot replace any required ref. Unknown, stale, mismatched, nonportable, or unresolved refs fail before identity is assigned.

### 3.5 Source-grant and privacy boundary

Jobs use a closed `SourceUseGrant` compiled from the IE package and its effective restrictions. It names allowed ingredients/spans, derivative/use classes, audiences/platforms, expiry/revocation state, required disclosure, redaction, and forbidden uses. A job cannot access arbitrary transcript/session storage. Pipeline stores source refs and authorized bounded excerpts only where the package permits; it must not leak a participant source through logs, cache keys, error text, or model prompts.

### 3.6 Shared analysis is immutable and subordinate

Transcript parses, phrase packs, shot maps, keyframes, tags and approved Moments may be reused only by exact version/hash and declared analysis profile. Cache identity includes source package/version/hash, authorized ingredient closure, analysis profile/version/hash, producer implementation/version/hash and normalization profile. Cache hits never upgrade evidence, expand source grants, carry across revoked authority, or become source truth. A cache miss may incur work only after a separately authorized execution command.

### 3.7 Determinism and no invented thresholds

Canonical identities never depend on clock, random state, process environment, machine path, locale, dictionary insertion, filesystem traversal, service response order, or provider ID. Set-semantic arrays are unique and lexically sorted; ordered semantic arrays preserve declared order. Timestamps are caller-supplied evidence outside semantic hashes.

Exact duplicate detection is deterministic. Near-duplicate, source-overlap, diversity, cost and ranking judgments require versioned policy/evaluation profiles. This spec defines their interfaces and fail-closed behavior; it does not invent numeric thresholds.

### 3.8 `NOT_APPLICABLE` is evidence-bearing

No required field is satisfied by null, omission, empty text or a bare string `NOT_APPLICABLE`. Conditional requirements use `ApplicabilityDecision {requirement_id, decision, rule_ref, evidence_refs, owner, reason_code}`. A `NOT_APPLICABLE` decision requires a version/hash-pinned rule proving conditionality and cannot suppress source, authority, lineage, Harness, transfer, wrong-reading, review, or evaluation requirements that the chosen derivative/profile declares.

### 3.9 Category/profile and Format 02 truth

Category and profile are exact governed identifiers. Compatibility is semantic, not parse-only. A structurally accepted schema or `contract_compatible` profile is not benchmarked, limited-production-certified, production-certified, or production-authorized. Format 02 remains `DEFERRED_AWAITING_CURRENT_ATOMIC_HARNESS`; no batch may produce an eligible Format 02 job until the amendment's exact gates are satisfied by later authority and evidence.

### 3.10 Immutability, separation and claim ceiling

Every admitted mutation produces a new immutable object version plus command record, event, receipt, dependency edges, idempotency record and outbox entry in one atomic commit. Producers cannot evaluate or approve their own judgment output where separation is required. Job compilation is not execution authorization; route selection is not production acceptance; batch completion is not downstream consumption authorization.

## 4. Current brownfield architecture

There is no `05_ATOMIC_HARNESS_PIPELINE` source implementation. Its current product tree contains specification drafts only. This is a greenfield implementation target with governed brownfield interfaces.

| Existing evidence | Current behavior | Disposition | Constraint |
|---|---|---|---|
| `atomic_harness_definition.py::AtomicHarnessDefinition` | Frozen canonical-hashed synthetic Builder definition with 20 governed sections, explicit authority/lineage and false production/certification flags. | `REUSE_CONTRACT` | Consume exact portable Builder bytes through TS-AHP-002; never import Builder domain code or treat the synthetic profile as production proof. |
| `category_runtime_rules.py::CategoryOperatingRules` | Five category laws, profile ownership, exact evaluation/repair units, selective rerun, migration/compatibility constraints and explicit generic `NOT_APPLICABLE`. | `REUSE_CONTRACT` | Bind exact current rule/version/hash; do not collapse category-native plans or inherit certification. |
| `TS-AHP-002` | Candidate safe package intake and immutable Harness execution binding. | `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Batch admission requires an exact eligible non-stale binding; a future audit change reopens this spec's dependency-sensitive sections. |
| `TS-INT-005` | Candidate source-evidence inventory/package, restrictions, approval, handoff, acknowledgement and selective invalidation contracts. | `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Pipeline consumes an exact approved package; it cannot approve or repair IE evidence. |
| `TS-AIR-015` / `TS-AIR-016` | Candidate semantic package and transfer-fidelity contracts. | `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Pipeline preserves exact semantic and transfer values; it cannot rebuild AIR meaning. |
| V9/V9.1 interview doctrines | Complete Expression Session, Expression Moment, archetype/derivative routing and multi-format asset concepts. | `ADAPT_AS_SOURCE_EVIDENCE` | Current typed IE/AIR contracts supersede free-form predecessor shapes; human activation and exact evidence remain source. |
| Studio Architecture Amendment V2.1 | Agentic order-to-ship supervision, typed correction and Format 02 deferral. | `REUSE_DECISION` | Studio projection cannot mutate Harness/job truth; Format 02 remains inactive. |

The external `SRC-EXT-023` bytes are unavailable and no current requirement depends solely on them. Accordingly, this specification does not reuse its implementation or attribute chunking, overlap, cache, crop, dedupe or structured-output behavior to it.

## 5. Proposed architecture and workflows

### 5.1 Components and boundaries

| Component | Responsibility | Forbidden responsibility |
|---|---|---|
| `BatchInputAdmissionService` | Resolve exact IE, AIR and Harness/binding refs; verify state/hash/owner/compatibility/source grants. | Filling a missing source/semantic/Harness field. |
| `SourceUseGrantValidator` | Prove every intended job use is inside package restrictions and authorization scope. | Widening or guessing authority. |
| `BatchProgramCompiler` | Compile immutable target jobs, dependencies, shared bindings, budget/deadline/review policy and claim ceiling. | Choosing new semantic intent or starting execution. |
| `DerivativeRouteEligibilityEngine` | Intersect source support, AIR-approved routes, category/profile rules, Harness availability and capability/evaluation readiness. | Manufacturing an archetype/Harness fit or converting ranking into authority. |
| `RouteRankingEngine` | Deterministically order already eligible alternatives under an exact profile and evidence. | Inventing thresholds or changing eligibility. |
| `SharedSourceAnalysisRegistry` | Register exact immutable analysis artifacts and compile bounded reuse bindings. | Treating cache state as source evidence or expanding grants. |
| `DerivativeConflictAnalyzer` | Detect exact duplicate signatures, profile-governed overlap/near-duplicate risks and incompatible source uses before spend. | Erasing distinct purposes merely because spans overlap. |
| `DerivativeJobCompiler` | Emit immutable independently cancelable jobs with exact Harness/source/semantic/evaluation/review contracts. | Executing jobs or changing a binding. |
| `BatchAggregateRepository` | Atomic compare-and-swap persistence, receipts, dependency graph, exact-version reads and historical reconstruction. | In-place overwrite or history deletion. |
| `BatchInvalidationProjector` | Traverse typed dependency edges and mark only affected current descendants ineligible. | Blanket regeneration or deletion of historical bytes. |

### 5.2 Workflow A — admit and freeze a batch request

1. `CompileContentBatchCommand` supplies the operator request, expected aggregate version, actor/delegation, exact authority snapshot, accepted IE package ref, AIR package/transfer refs, target output requests, eligible Harness/binding refs, budget/deadline/review policy refs and idempotency key.
2. Admission verifies all refs by exact schema/version/hash/owner and current lifecycle state. It verifies package approval and handoff, but does not confuse handoff/acknowledgement with production acceptance.
3. Each target is checked against the source-use grant, AIR target category/profile and transfer policy, Builder category/profile, and Harness binding. Unknown values and ambiguous mappings fail.
4. The service computes `admitted_input_digest` and freezes it with the exact authority/registry/profile snapshot. No mutable `latest` lookup is allowed after compilation begins.
5. A single invalid target yields a typed target blocker while unrelated targets remain compilable when shared mandatory inputs are valid. Invalid shared input blocks the batch.

### 5.3 Workflow B — compile the batch program

1. Normalize target requests by stable caller-supplied target ID; do not reorder declared semantic sequence.
2. Create one `DerivativeJobSeed` per target with source purpose, derivative kind, target platform/profile, sequence role, intended Activative function and exact consumer requirements.
3. Bind shared immutable source/analysis candidates and explicit dependency edges.
4. Compile budgets and deadlines as operational ceilings. A job with missing required budget policy is blocked; budget values never alter semantic purpose.
5. Compile review modes and approval/evaluation owners from the Harness and target profile. Missing owner separation blocks only affected jobs unless the owner is batch-wide.
6. Emit a candidate `ContentBatchOrchestrationProgram` and `BatchCompilationReceipt`; no execution side effect occurs.

### 5.4 Workflow C — compute route eligibility and ranking

1. Start from AIR-approved route/archetype/derivative candidates referenced by the exact Semantic Production Package and Activation Transfer Contract. Pipeline never searches for a new archetype.
2. Intersect those candidates with approved IE ingredients/Moments and source restrictions.
3. Exclude wrong category/profile, unsupported source role, absent Harness/binding, unavailable required capability/evaluator, stale dependency, transfer-policy violation, wrong-reading-lock conflict and production-state conflict.
4. Emit a `RouteEligibilityDecision` for every considered route, including source support, expected viewer function, ingredient requirements, exclusions and exact evidence refs.
5. If a governed ranking profile is present, rank only `ELIGIBLE` routes. Every score/dimension includes its rule/evidence; aggregation cannot override a hard exclusion.
6. If one admissible route is deterministically selected by current policy, emit its receipt. If genuine alternatives require taste or new meaning, emit `HUMAN_SELECTION_REQUIRED`. The human selection references eligible route IDs and cannot add an ineligible route.

### 5.5 Workflow D — compile immutable derivative jobs

For each selected route, the compiler binds exactly one Harness definition/version/hash and execution-binding manifest/version/hash; one closed source grant; exact source package/inventory/ingredient/Moment refs; AIR semantic and transfer refs; derivative kind/category/profile/platform; Activative/sequence function; output constraints; runtime capability requirements; evaluation profile/dimensions/evaluator owner; wrong-reading locks; review policy; budget/deadline; dependency edges; claim ceiling; and cancellation/invalidation law.

The resulting job starts `COMPILED_PENDING_ADMISSION`. `AdmitDerivativeJobCommand` revalidates the frozen closure against current revocation/supersession status and atomically moves it to `ADMITTED_NOT_EXECUTION_AUTHORIZED` or `BLOCKED`. A later execution specification and authorization are required to schedule work.

### 5.6 Workflow E — compile shared analysis and dedupe/conflict plan

1. Group analysis requests only when their exact cache key and effective source grants match. A broader job cannot reuse a restricted artifact merely because source bytes match.
2. Select an existing accepted analysis artifact only when all exact input/profile/producer hashes match and it is not revoked, stale or outside grant.
3. Emit `SharedSourceAnalysisBinding` with consumers and a read-only constraint. Reuse avoids duplicate work but never changes job-specific Harness/evaluation requirements.
4. Compute an exact `DerivativeIdentitySignature` from the source-use closure, AIR purpose/route, derivative kind, category/profile/platform, Harness binding, Final Script/Composition refs and transfer contract. Identical active signatures are exact duplicates and one is blocked or linked as an explicit replacement.
5. Evaluate overlap, near-duplicate and conflict dimensions only under exact governed profiles. Missing profiles yield `REVIEW_REQUIRED` or `EVALUATOR_UNAVAILABLE`, never an invented decision.
6. Preserve distinct derivatives when source overlap serves demonstrably different AIR-owned purposes/routes and both remain allowed. Emit an `AcceptedDiversityPlan` that proves distinction or names unresolved conflicts.
7. No provider/render execution is admitted until all blocking duplicate/conflict results resolve.

### 5.7 Workflow F — lifecycle, cancellation, replay and selective invalidation

- Idempotency identity includes command type, canonical request, actor/delegation scope, exact aggregate/version and frozen authority/profile snapshots. Same key/same bytes returns the original receipt; same key/different bytes fails.
- Compare-and-swap prevents two route selections, admissions, amendments or supersessions from becoming current for the same expected version.
- Cancellation before commit leaves no current artifact. Cancellation after commit creates a new cancellation/supersession event and never erases history.
- Source/semantic/Harness/profile changes create new objects. Typed edges determine affected jobs, shared analyses, route decisions and descendants. Unaffected accepted work remains usable.
- Revoked source authority blocks new use immediately and invalidates current jobs that depend on that grant. Historical records remain reproducible with the invalidation/revocation receipt.
- Replay uses exact historical bytes and profiles. If a dependency is unavailable, replay fails `AHP_BATCH_REPLAY_DEPENDENCY_UNAVAILABLE`; it never substitutes a newer version.

### 5.8 States and events

```text
Batch:   REQUESTED -> INPUTS_ADMITTED -> COMPILED -> ROUTING_COMPLETE -> JOBS_COMPILED
              |              |              |               |
              +-> BLOCKED    +-> CANCELLED  +-> REVIEW_REQUIRED
JOBS_COMPILED -> READY_FOR_SEPARATE_EXECUTION_AUTHORIZATION
              -> SUPERSEDED | INVALIDATED | REVOKED | CANCELLED

Job:     PROPOSED -> COMPILED_PENDING_ADMISSION -> ADMITTED_NOT_EXECUTION_AUTHORIZED
              |                 |                         |
              +-> BLOCKED       +-> REVIEW_REQUIRED       +-> SUPERSEDED
                                                        -> INVALIDATED | REVOKED | CANCELLED
```

Required events include `BatchInputsAdmitted`, `BatchCompilationBlocked`, `ContentBatchCompiled`, `RouteEligibilityEvaluated`, `RouteSelectionRequired`, `RouteSelected`, `SharedAnalysisBound`, `DerivativeConflictDetected`, `DiversityPlanAccepted`, `DerivativeJobCompiled`, `DerivativeJobAdmissionDenied`, `DerivativeJobAdmitted`, `BatchSuperseded`, `BatchInvalidated`, `BatchRevoked`, `BatchCommandCancelled`, and `BatchHistoricalReplayVerified`.

## 6. Data models, contracts, schemas, and APIs

All models are immutable, closed (`additionalProperties: false`), versioned and validated before identity/storage. No `Any`, arbitrary dictionaries, untyped notes, implied defaults, absolute paths or environment-derived locators are allowed.

### 6.1 Common strict types and canonicalization

`ImmutableRef` requires `object_id`, `schema_id`, `schema_version`, immutable `version`, lowercase 64-hex `content_sha256`, `owner_product`, `lifecycle_state_at_use`, and `authority_ref`. `OwnerRef`, `ActorRef`, `PolicyRef`, `ProfileRef`, `CategoryProfileRef`, and `ReceiptRef` are closed refinements.

Canonical JSON uses UTF-8, NFC-normalized strings, lexicographically sorted object keys, decimal integers, no floating NaN/Infinity, and a single terminal newline. Set-semantic arrays sort by canonical identity; workflow order, target order, route ranking and lineage order remain declared. `canonical_hash` excludes itself, materialization path and evidence timestamps. IDs are caller-supplied logical IDs plus immutable version or content-derived IDs; random defaults are forbidden.

### 6.2 `ContentBatchOrchestrationProgram`

Schema `ca.pipeline.content-batch-orchestration-program/2.1.0-candidate`:

```text
batch_program_id, version, lifecycle_state
organization_id, brand_id, campaign_ref
authority_snapshot_ref, admitted_input_digest
source_package_ref, inventory_ref, package_approval_receipt_ref
semantic_production_package_ref, activation_transfer_contract_refs
target_requests: nonempty ordered DerivativeTargetRequest[]
job_seed_refs: nonempty ordered ImmutableRef[]
shared_analysis_requirement_refs: ordered ImmutableRef[]
dependency_graph_ref, category_profile_registry_snapshot_ref
harness_binding_refs: nonempty ordered ImmutableRef[]
route_ranking_profile_ref_or_not_applicable
duplicate_conflict_profile_ref, review_policy_ref
budget_policy_ref, total_budget_ceiling, deadline_policy_ref
source_lineage_obligations: nonempty ordered LineageObligation[]
wrong_reading_lock_refs: nonempty ordered ImmutableRef[]
limitations, maximum_claim
production_eligible: false
certified: false
supersedes_ref, dependency_refs, canonical_hash
```

`DerivativeTargetRequest` contains target ID, derivative kind, category/profile/platform, AIR-owned intended Activative/sequence function refs, source-use purpose, requested output constraints, priority, budget/deadline allocation, review mode and required consumer features. Free-form semantic intent is forbidden. The program is invalid if any ref owner conflicts, a shared required input is stale, or target and AIR/Harness category/profile do not match.

### 6.3 `SourceUseGrant` and shared analysis

Schema `ca.pipeline.source-use-grant-projection/2.1.0-candidate` is a read-only Pipeline projection:

```text
grant_projection_id, source_package_ref, package_slot_refs
allowed_ingredient_refs, allowed_source_span_refs
allowed_derivative_kinds, allowed_use_classes
allowed_platform_profile_refs, audience_scope_refs
required_disclosure_refs, effective_restriction_refs
source_wrong_reading_risk_refs
expiry_or_not_applicable, revocation_state
projection_rule_ref, source_owner: INTERVIEW_EXPRESSION
canonical_hash
```

`SharedSourceAnalysisArtifactRef` requires analysis kind, exact source/package/ingredient closure, analysis profile and producer refs, result ref/hash, restrictions, lifecycle state and maximum claim. `SharedSourceAnalysisBinding` requires binding ID/version, cache-key digest, artifact ref, consumer job IDs, effective-grant digest per consumer, read-only flag `true`, reuse-decision receipt, dependency refs and canonical hash. It cannot embed mutable analysis bytes or claim that an inferred analysis is approved source evidence.

### 6.4 Route eligibility and ranking contracts

`DerivativeRouteCandidate` is an exact projection of already-authorized inputs:

```text
candidate_id
air_archetype_coalition_ref, air_derivative_function_ref
viewer_role_tension_ref, primitive_coalition_ref, edge_product_ref
source_support_refs, expression_moment_refs
category_profile_ref, platform_profile_ref
harness_definition_ref, harness_binding_ref
required_ingredient_kinds, required_capability_refs
required_evaluation_dimension_refs, wrong_reading_lock_refs
authority_owner_refs, canonical_hash
```

`RouteEligibilityDecision`:

```text
decision_id, candidate_ref, batch_program_ref
eligibility: ELIGIBLE | EXCLUDED | BLOCKED | REVIEW_REQUIRED
rule_results: nonempty ordered ApplicabilityDecision[]
source_support_refs, expected_viewer_function_ref
exclusion_reason_codes, missing_requirement_refs
evidence_refs, evaluator_or_rule_identity
authority_snapshot_ref, canonical_input_hash, canonical_hash
```

`RouteRankingResult` requires an exact ranking-profile ref, ordered eligible route refs, per-dimension rule/evidence results, hard-gate results, unresolved-equivalence groups and claim ceiling. It cannot rank excluded routes. `RouteSelectionReceipt` identifies deterministic policy selection or attributable human selection among eligible routes; it stores considered alternatives and does not mutate candidate bytes.

### 6.5 `ContentDerivativeJob`

Schema `ca.pipeline.content-derivative-job/2.1.0-candidate`:

```text
job_id, version, lifecycle_state
batch_program_ref, target_request_ref, selected_route_ref
harness_definition_ref, harness_execution_binding_manifest_ref
source_use_grant_ref, source_package_ref, inventory_ref
ingredient_refs, expression_moment_refs, reaction_receipt_refs
semantic_production_package_ref, activation_transfer_contract_ref
approved_final_script_ref, animation_scene_package_ref_or_not_applicable
matrix_result_ref, primitive_coalition_ref, coalition_signature_ref
edge_product_ref, viewer_role_tension_ref, archetype_coalition_ref
brand_context_ref, voice_dna_ref, visual_dna_ref
derivative_kind, category_profile_ref, platform_profile_ref
activative_function_ref, sequence_function_ref
output_constraint_refs, composition_intent_ref_or_not_applicable
runtime_capability_requirement_refs
shared_analysis_binding_refs, job_dependency_refs
evaluation_profile_ref, evaluation_dimension_refs, evaluator_owner_ref
wrong_reading_lock_refs, source_restriction_refs
review_policy_ref, approval_owner_refs
budget_allocation, deadline_policy_ref
claim_ceiling, production_eligible: false, certified: false
supersedes_ref, dependency_refs, canonical_hash
```

For `source_kind: interview_expression`, `reaction_receipt_refs` and `expression_moment_refs` are both nonempty. For non-interview source kinds, interview provenance is optional but validated when supplied. Missing AIR/IE meaning is not reconstructable. `composition_intent_ref` is AIR/upstream-owned when applicable; Pipeline references it and does not author it. `animation_scene_package_ref_or_not_applicable` uses an evidence-bearing decision when the derivative is not animation.

### 6.6 Duplicate, overlap, conflict and diversity contracts

`DerivativeIdentitySignature` contains exact source-grant digest; source/Moment/ingredient refs; AIR purpose, route, role/tension, Primitive/archetype and Final Script/Composition refs; derivative/category/platform; Harness binding; transfer contract; and output-constraint digest. The signature hash is deterministic and excludes scheduling/budget metadata.

`DerivativeComparisonResult`:

```text
comparison_id, left_job_seed_ref, right_job_seed_ref
exact_signature_equal: boolean
source_overlap_result: ProfileDimensionResult
semantic_near_duplicate_result: ProfileDimensionResult
route_distinction_result: ProfileDimensionResult
sequence_role_conflict_result: ProfileDimensionResult
source_use_conflict_result: ProfileDimensionResult
decision: DISTINCT | EXACT_DUPLICATE | CONFLICT | REVIEW_REQUIRED | EVALUATOR_UNAVAILABLE
profile_refs, evidence_refs, limitations, canonical_hash
```

`ProfileDimensionResult` is either a deterministic exact result or a governed evaluation result with profile/rule/evidence refs. It never embeds an ungoverned scalar cutoff. `AcceptedDiversityPlan` lists accepted job refs, blocked duplicate refs, replacement/supersession refs, unresolved review refs, distinction evidence, operator resolution receipt refs and canonical hash.

### 6.7 Commands, events, repository and API boundary

Commands:

```text
CompileContentBatch
EvaluateDerivativeRouteEligibility
RankEligibleDerivativeRoutes
SelectDerivativeRoute
BindSharedSourceAnalysis
EvaluateDerivativeConflicts
AcceptDerivativeDiversityPlan
CompileContentDerivativeJobs
AdmitContentDerivativeJob
BlockContentDerivativeJob
RequestBatchCorrection
SupersedeContentBatch
RevokeContentBatch
InvalidateBatchDescendants
CancelBatchCommand
ReplayContentBatchDecision
```

Every command contains command ID, idempotency key, canonical request hash, actor/delegation, organization/brand, aggregate/version, causation/correlation, authority/profile/registry snapshots and cancellation ref. Caller-supplied approval, lifecycle or certification fields are forbidden.

`ContentBatchRepository` exposes exact-version get, compare-and-swap append, atomic artifact/event/receipt/command/dependency/outbox commit, dependency traversal, idempotency lookup and historical reconstruction. A mutable `put_current` overwrite is forbidden. Current-head queries may serve projections but cannot execute or replay a pinned job.

Future APIs are command-oriented and exact-versioned, for example:

```text
POST /v2/pipeline/content-batches:compile
POST /v2/pipeline/content-batches/{id}/versions/{version}:route
POST /v2/pipeline/content-batches/{id}/versions/{version}:compile-jobs
POST /v2/pipeline/content-jobs/{id}/versions/{version}:admit
POST /v2/pipeline/content-batches/{id}/versions/{version}:supersede
GET  /v2/pipeline/content-batches/{id}/versions/{version}
GET  /v2/pipeline/content-batches/{id}/versions/{version}/lineage
GET  /v2/pipeline/content-batches/{id}/versions/{version}/receipts
```

HTTP success alone is not acceptance evidence. Responses identify the exact artifact/receipt/hash and current claim ceiling.

### 6.8 Compatibility, migration and invalid examples

Compatibility requires all required contract features, semantic fields, authority owners, source-kind/provenance rules, category/profile, Harness compiler profile, transfer checkpoints, evaluation dimensions and wrong-reading locks. Parsing without enforcement fails. Adapters are read-only projections that preserve every required field and constraint; they cannot coerce unknown enum values, downgrade restrictions or change owners.

Migrations create new immutable artifacts with predecessor, mapping profile, field-by-field proof, loss report and approval. They never guess source classification, route, archetype, missing provenance or `NOT_APPLICABLE`. An active job stays pinned to its accepted dependency versions; a deprecated profile does not rewrite historical jobs. A revoked source authorization still blocks new use immediately.

Invalid examples include:

```yaml
# Invalid: Pipeline manufactures meaning.
archetype: MythDebunk
evidence_refs: []
```

```yaml
# Invalid: free-form flattening replaces exact lineage.
semantic_notes: "Use the emotional part of the interview."
```

```yaml
# Invalid: arbitrary source access.
transcript_path: D:\\recordings\\guest.txt
```

```yaml
# Invalid: a cache artifact is promoted to source truth.
source_package_ref: cache://latest-analysis
```

```yaml
# Invalid: applicability hides a required evaluator.
evaluation_profile: NOT_APPLICABLE
```

```yaml
# Invalid: route capability is treated as certification.
production_eligible: true
certified: true
```

## 7. Implementation stages and exact target paths

These are proposed future paths only. No path is created or modified by this writing task.

### 7.1 Stage 0 — contract and profile lock

Proposed paths:

- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/contracts/content_batch.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/contracts/derivative_job.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/contracts/route_eligibility.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/contracts/source_use_grant.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/ca_pipeline/contracts/duplicate_conflict.py`

Gate: ratified/adopted authority as required, accepted upstream contracts, schema registry decision and Development Capsule. No contract release bytes may be produced during this specification lifecycle.

### 7.2 Stage 1 — immutable domain models

- `src/ca_pipeline/domain/content_batch.py`
- `src/ca_pipeline/domain/derivative_job.py`
- `src/ca_pipeline/domain/route_decision.py`
- `src/ca_pipeline/domain/shared_analysis.py`
- `src/ca_pipeline/domain/diversity_plan.py`

Gate: strict model, canonical hash, invalid-object and property tests pass without external side effects.

### 7.3 Stage 2 — application services and ports

- `src/ca_pipeline/application/compile_content_batch.py`
- `src/ca_pipeline/application/route_derivatives.py`
- `src/ca_pipeline/application/compile_derivative_jobs.py`
- `src/ca_pipeline/application/evaluate_derivative_conflicts.py`
- `src/ca_pipeline/ports/source_package_reader.py`
- `src/ca_pipeline/ports/semantic_package_reader.py`
- `src/ca_pipeline/ports/harness_binding_reader.py`
- `src/ca_pipeline/ports/batch_repository.py`

Gate: product sovereignty and no-source/no-semantic-reconstruction architecture tests pass.

### 7.4 Stage 3 — persistence, atomic commands and replay

- `src/ca_pipeline/infrastructure/persistence/content_batch_repository.py`
- `src/ca_pipeline/infrastructure/persistence/dependency_graph.py`
- `src/ca_pipeline/infrastructure/persistence/idempotency_store.py`
- `src/ca_pipeline/infrastructure/persistence/outbox.py`

Gate: atomic commit/rollback, optimistic concurrency, identical replay, altered replay denial and historical reproduction pass in fresh processes.

### 7.5 Stage 4 — governed adapters and evaluation bindings

- `src/ca_pipeline/adapters/interview_expression_asset_package.py`
- `src/ca_pipeline/adapters/air_semantic_production_package.py`
- `src/ca_pipeline/adapters/harness_execution_binding.py`
- `src/ca_pipeline/evaluation/route_eligibility.py`
- `src/ca_pipeline/evaluation/duplicate_conflict.py`

Gate: adapters are lossless or block; missing profile/evaluator does not produce a guessed result.

### 7.6 Stage 5 — API/projections and separately authorized execution handoff

- `src/ca_pipeline/api/content_batch_commands.py`
- `src/ca_pipeline/api/content_batch_queries.py`
- `src/ca_pipeline/projections/content_batch_status.py`
- `src/ca_pipeline/handoffs/job_execution_request.py`

Gate: a later accepted execution specification and authorization. This spec cannot authorize Stage 5, external spend or production.

### 7.7 Future exact test roots

- `tests/unit/content_batch/`
- `tests/unit/derivative_job/`
- `tests/unit/route_eligibility/`
- `tests/unit/duplicate_conflict/`
- `tests/contract/interview_expression/`
- `tests/contract/air/`
- `tests/contract/builder_binding/`
- `tests/integration/content_batch/`
- `tests/architecture/test_product_authority_boundaries.py`
- `tests/replay/test_content_batch_historical_reproduction.py`

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Code | Cause / owner | Effect and next admissible action |
|---|---|---|
| `AHP_BATCH_REQUIRED_REF_MISSING` | Caller or upstream product omitted an exact required ref | Block before identity; obtain the owner-issued artifact. |
| `AHP_BATCH_UPSTREAM_HASH_MISMATCH` | Supplied bytes do not match pinned ref | Quarantine/deny; resupply exact bytes, never rehash as accepted. |
| `AHP_BATCH_SOURCE_NOT_APPROVED` | IE package/inventory/Moment is not approved/current | Block affected batch/target; IE owner resolves. |
| `AHP_BATCH_SOURCE_USE_OUT_OF_SCOPE` | Target exceeds source grant/platform/use scope | Block affected target before execution; authorized source owner may issue a new grant. |
| `AHP_BATCH_SEMANTIC_INPUT_INCOMPLETE` | AIR role/Matrix/Primitive/archetype/Final Script/transfer data missing or inconsistent | Block; AIR corrects with a new version. Pipeline does not reconstruct. |
| `AHP_BATCH_HARNESS_UNAVAILABLE` | No current exact compatible Harness/binding | Block affected job only; Builder/Pipeline binding lifecycle supplies a governed successor. |
| `AHP_BATCH_ROUTE_MANUFACTURE_ATTEMPT` | Candidate route lacks AIR/source authority | Deny and record evidence; human cannot override by free text. |
| `AHP_BATCH_ROUTE_PROFILE_UNAVAILABLE` | Required ranking/eligibility profile unavailable | `REVIEW_REQUIRED` or block per profile; do not invent rules. |
| `AHP_BATCH_DUPLICATE` | Exact derivative signature already active | Block or require explicit replacement/supersession. |
| `AHP_BATCH_CONFLICT_UNRESOLVED` | Source-use, route, sequence-role or near-duplicate conflict remains | Block involved jobs, preserve unrelated jobs. |
| `AHP_BATCH_EVALUATOR_UNAVAILABLE` | Required independent evaluation binding absent | Block affected transition; capability presence is not certification. |
| `AHP_BATCH_WRONG_READING_LOCK_CONFLICT` | Planned use would remove/weaken inherited lock | Deny; only an authorized upstream new demand/program version may relax it. |
| `AHP_BATCH_NOT_APPLICABLE_UNEVIDENCED` | N/A lacks rule/evidence | Deny before identity. |
| `AHP_BATCH_IDEMPOTENCY_CONFLICT` | Same key, different canonical request | Return conflict without mutation. |
| `AHP_BATCH_CONCURRENCY_CONFLICT` | Expected aggregate/version stale | Return current exact ref; caller consciously retries. |
| `AHP_BATCH_ATOMIC_COMMIT_FAILED` | Any artifact/receipt/event/dependency/outbox write fails | Roll back the entire command; no partial visible success. |
| `AHP_BATCH_REPLAY_DEPENDENCY_UNAVAILABLE` | Exact historical bytes/profile unavailable | Fail replay explicitly; never use current/latest. |
| `AHP_BATCH_PORTABILITY_VIOLATION` | Machine path, environment locator or unstable bytes present | Deny export/handoff; produce portable refs. |
| `AHP_BATCH_AUTHORIZATION_CEILING_EXCEEDED` | Request implies build/production/certification beyond authority | Deny and report required gate. |

Failures contain code, human-readable message, owner, aggregate/command/correlation refs, exact offending object refs, failed rule/profile, retryability, next admissible action and evidence refs. Logs redact source text and secrets.

### 8.2 Atomic rollback and partial batch behavior

A batch command commits program/jobs/decisions/receipts/events/dependencies/idempotency/outbox together or none. The compiler may produce a truthful partial planning result containing eligible and blocked targets, but that partial result is one atomic artifact and cannot silently omit blockers. An invalid shared source/AIR input blocks the whole batch; an unsupported target/Harness blocks only that target. No success receipt may exist without its artifact and no current artifact without its creation receipt.

### 8.3 Supersession, invalidation, revocation and recovery

Corrections create successors. Dependency edges carry `CONTENT_IDENTITY`, `SOURCE_GRANT`, `SEMANTIC_PROGRAM`, `HARNESS_BINDING`, `CATEGORY_PROFILE`, `EVALUATION_PROFILE`, `SHARED_ANALYSIS`, `ROUTE_DECISION`, or `OPERATIONAL_ONLY` impact. Changed/revoked source grants invalidate all current uses they no longer authorize. Semantic/Harness/profile changes invalidate only jobs depending on the changed ref. Budget/deadline changes produce a new operational program version and do not rewrite semantic identity unless a governed rule says the schedule is semantic.

Recovery begins from the last immutable accepted checkpoint, reruns affected components, and retains unaffected work. A failed cache/analysis service may degrade to `RECOMPUTE_REQUIRED` only after separate execution authorization; it cannot fabricate a hit. Revocation or invalidation after completion blocks new consumption while preserving exact historical artifacts and receipts.

### 8.4 Migration and compatibility

Adapters pin source/target schema/profile/validator versions and emit a migration receipt. Lossless proof is field-level; otherwise migration is blocked with unresolved fields. Source kind is never guessed. Restrictions and wrong-reading locks may only remain equal or become stricter. Active historical jobs remain pinned; deprecation affects new compilation according to the registry and does not mutate old bytes.

### 8.5 Observability and technical security

Metrics and traces include command/event/receipt IDs; batch/job versions; source/semantic/Harness ref hashes; route considered/eligible/excluded counts; reuse hit/miss with exact cache profile; duplicate/conflict decision codes; blocked owner; invalidation affected/unaffected counts; deterministic replay digest; and latency/cost without source content. Security is operational: least-privilege ports, bounded source grants, encrypted secret references, path/archive validation, source-redacted logs, authenticated actors/delegations and auditable authorization. It does not add generic content-rights or creative-safety authority.

## 9. Behavior-specific acceptance criteria

### AC-01 — FR-133 / ST-03.02: compile a coordinated batch

Given one approved interview package, exact AIR programs, and requests for two shorts plus one Carousel, compilation emits one versioned program and three independently attributable job seeds with explicit dependencies, budgets, deadlines, review modes, source lineage and separate Harness/evaluation requirements.

### AC-02 — FR-133: unsupported target isolation

Given one target with no current Harness and two valid targets, compilation records a typed blocker for the unsupported target while preserving the eligible target plans. It never manufactures a Harness or blocks unrelated work without a shared-input reason.

### AC-03 — FR-134 / ST-03.03: source-supported route

Given an approved Expression Moment and AIR route supporting a myth-debunk sequence, routing proposes only category/profile-compatible current Harness routes, explains source and viewer-function evidence, and records every exclusion.

### AC-04 — FR-134: no manufactured route

Given a strong quote without the evidence required by a data-story route, the route is excluded. An operator cannot select it through free text; a new IE/AIR version is required.

### AC-05 — FR-135: immutable complete job

Every admitted job pins one Harness/binding, exact source grant/package/ingredients, derivative/category/platform, AIR Activative/sequence function, output constraints, capabilities, evaluation, source authority, review policy, transfer contract, locks, claim ceiling and dependency closure.

### AC-06 — FR-135: source-authority denial

Given a requested platform outside the source grant, admission fails `AHP_BATCH_SOURCE_USE_OUT_OF_SCOPE` before any external side effect and identifies Interview Expression/source owner as the resolution owner.

### AC-07 — FR-136: exact analysis reuse

Given three jobs requesting the same exact source analysis under the same grant/profile/producer hashes, one immutable accepted analysis artifact is bound read-only to all three, while each job retains its own Harness and evaluation requirements.

### AC-08 — FR-136: no unsafe reuse

Given the same source bytes but different restrictions or analysis profiles, no cache hit occurs across the boundary. The system records separate analysis requirements or a typed blocker.

### AC-09 — FR-136: exact duplicates and distinct purposes

Identical derivative signatures are blocked or explicitly related as replacements. Shared source spans do not alone collapse two derivatives with distinct AIR-owned route/purpose and sufficient governed distinction evidence.

### AC-10 — No invented overlap or ranking threshold

When a required near-duplicate, overlap, diversity or ranking profile is missing, the result is `REVIEW_REQUIRED` or `EVALUATOR_UNAVAILABLE`; no embedded number, model intuition or external-reference assumption creates a decision.

### AC-11 — Interview Expression sovereignty

For interview expression, jobs contain nonempty Reaction Receipt and Expression Moment refs and exact source evidence. Pipeline never creates, edits, upgrades or reconstructs them.

### AC-12 — AIR sovereignty and transfer fidelity

Pipeline preserves the exact role/tension, Matrix/Edge, Primitive/archetype coalition, Final Script, Activation Transfer Contract, semantic package and source-fidelity laws. No required lineage is flattened into notes.

### AC-13 — Builder/Harness sovereignty

Jobs bind an exact current non-stale Harness and execution binding and cannot override category/profile, purpose, acceptance tests, Feature Contracts, T/V routes, wrong-reading locks or repair law.

### AC-14 — Wrong-reading inheritance

All applicable generative/transformative jobs retain inherited locks. Derivatives may add stricter locks but cannot remove or weaken parent locks. Relaxation requires a new authorized upstream version.

### AC-15 — Evidence-bearing applicability

A conditional animation-scene, evaluation, profile or ingredient requirement can be `NOT_APPLICABLE` only with an exact profile rule/evidence/owner decision. Null/omission/bare N/A fails.

### AC-16 — Determinism and portability

The same exact inputs and frozen profiles in clean processes produce byte-identical programs, decisions, jobs and receipts. No output contains an absolute path, environment value, current time in semantic identity, random ID or traversal-order dependency.

### AC-17 — Atomicity and optimistic concurrency

Injected failure at every persistence boundary leaves no partial state. Concurrent commands against one expected version permit exactly one current commit; identical replay returns the original result.

### AC-18 — Selective invalidation and historical reproduction

A corrected Expression Moment invalidates only jobs using it; an unrelated keyframe change leaves independent jobs current. All historical versions remain reconstructable with original hashes and invalidation receipts.

### AC-19 — Consumption and production boundaries

Package handoff/acknowledgement, batch compilation, route selection, job admission and later production acceptance remain distinct. This spec never makes production eligibility/certification true.

### AC-20 — Format 02 deferral and category truth

Format 02 cannot become an eligible job while its current Harness gate is unsatisfied. Other registered categories/profiles retain their exact independent structural, benchmark and certification states.

### AC-21 — Candidate-authority ceiling

The document and every future writing receipt preserve `CANDIDATE_NOT_CURRENT`, `specification_work_authorized: true`, `build_authority: false`, and `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` as the maximum pre-ratification later acceptance state.

## 10. Testing and completion evidence

### 10.1 Unit and property tests

- strict required fields, owner/schema/version/hash validation and unknown-field rejection for every Section 6 model;
- canonical serialization across insertion order, locale, timezone, environment, process and filesystem-order perturbations;
- exact source-grant containment and redaction/log-safety properties;
- route eligibility intersection and hard-exclusion precedence;
- exact duplicate signature stability and symmetry of comparison results;
- no cross-grant/cache-profile reuse;
- evidence-bearing `NOT_APPLICABLE` and no optional-field bypass;
- restriction/wrong-reading-lock monotonicity;
- category/profile/Harness mismatch denial;
- claim-ceiling and production/certification false invariants.

### 10.2 Contract and architecture tests

- IE adapter preserves every Asset Package, ingredient, evidence, restriction, approval and lifecycle field or blocks;
- AIR adapter preserves every semantic package/transfer/lineage/lock field or blocks;
- Harness adapter pins exact definition/binding/profile and rejects mutation/shape guessing;
- architecture imports forbid IE/AIR/Builder domain implementations from becoming Pipeline ownership;
- no Pipeline module exposes commands to create source truth, semantic meaning, Harness definitions or VAE production decisions;
- draft-dependency hashes remain exact and are never represented as ratified authority;
- Format 02 deferral and candidate-authority ceiling remain enforced.

### 10.3 Workflow and integration tests

The mandatory golden slice uses one approved imported-interview Asset Package, nonempty Reaction Receipt/Moment evidence, an exact AIR Semantic Production Package and Activation Transfer Contract, and current Builder Harness bindings. It compiles two short-video jobs and one Carousel job that share one admitted transcript analysis but retain separate route, Harness, transfer, evaluation and review requirements.

Adversarial variants prove:

- one unsupported target is isolated;
- stale/revoked source, AIR or Harness inputs fail before side effects;
- platform outside grant is denied;
- an unsupported archetype cannot be selected;
- identical jobs are deduplicated;
- distinct AIR purposes survive source overlap;
- missing ranking/dedupe evaluator yields typed uncertainty rather than a fabricated PASS;
- partial batch result lists all blockers;
- producer cannot self-evaluate/approve where segregation applies.

### 10.4 Atomicity, concurrency, replay and invalidation tests

Inject failure before/after artifact, receipt, event, dependency, idempotency and outbox persistence. After every failure, visible state is either entirely pre-command or entirely committed. Test same-key/same-request replay, same-key/different-request conflict, expected-version races, cancellation before and after commit, exact historical replay in fresh processes, missing historical dependency failure, source-grant revocation, selective Moment correction and unaffected-job preservation.

### 10.5 Determinism and portability matrix

Run golden compilation in at least two fresh processes with varied `TZ`, locale, hash seed, working directory, temporary directory, environment order and source-file discovery order. Compare every byte/hash. Search all programs, jobs, receipts, manifests and diagnostics for drive letters, UNC paths, user/home/temp paths and environment secrets. Caller timestamps may differ only in evidence fields excluded from semantic identity.

### 10.6 Required completion evidence from a future build

Future implementation completion requires source files at the authorized paths, tests, schemas, deterministic fixtures, migration fixtures, architecture/import evidence, full regression, clean-room reproduction, atomicity fault matrix, replay corpus, invalidation graph evidence, security/path scan, source traceability, independent audit, revision, independent re-audit/acceptance, ratification/adoption gate and an authorized Development Capsule. A synthetic or local PASS cannot imply production readiness.

### 10.7 Specification traceability

| Requirement / Story | Primary design | Required evidence |
|---|---|---|
| FR-133 / ST-03.02 | Sections 5.2–5.3 and 6.2 | batch schema/graph, budgets, Harness bindings, compilation/partial-blocker receipts |
| FR-134 / ST-03.03 | Sections 5.4 and 6.4 | eligibility/exclusion, profile-bound ranking, route-selection receipt, no-manufacture tests |
| FR-135 / ST-03.02 | Sections 5.5 and 6.5 | strict job contract, source-grant validation, admission/denial receipt |
| FR-136 / ST-03.03 | Sections 5.6 and 6.3/6.6 | reuse bindings, cache isolation, overlap/dedupe/conflict/diversity evidence |
| Shared Story replay/recovery | Sections 5.7, 8 and 10.4 | atomicity, concurrency, replay, invalidation and historical reproduction |

### 10.8 Writing-stage completion state

This document ends at `WRITTEN_PENDING_AUDIT`. The writer performed no audit, revision, acceptance, implementation, build, schema publication, contract release, Development Capsule, production action or certification. All four upstream drafts remain `DRAFT_DEPENDENCY_NOT_ACCEPTED`. The next lifecycle action is independent audit by a different agent.
