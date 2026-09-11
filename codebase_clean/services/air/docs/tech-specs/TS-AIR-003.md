---
type: technical_specification
spec_id: TS-AIR-003
title: Activation Hypothesis Portfolio and Comparative Search
product: Activative Intelligence Runtime
version: 2.1.0-candidate
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_build_gate: RATIFICATION_OR_PRODUCT_ADOPTION_REQUIRED
document_class: CANDIDATE_CANONICAL_TECH_SPEC
output_path_class: DIRECT_PRODUCT_SPEC_PATH
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
writing_wave: 2
controlling_frs:
  - AIR-FR-013
  - AIR-FR-014
  - AIR-FR-015
  - AIR-FR-016
  - AIR-FR-017
  - AIR-FR-018
controlling_stories:
  - AIR-ST-03.01
  - AIR-ST-03.02
  - AIR-ST-03.03
upstream_draft_dependencies:
  - spec_id: TS-AIR-001
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-002
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-003 — Activation Hypothesis Portfolio and Comparative Search

This candidate specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. It preserves the substantive portfolio-and-search design of the hash-locked AIR full draft while applying its governed disposition, `AMEND_TO_CURRENT_AUTHORITY`: current product ownership, V3.3 lifecycle states, exact repository paths, closed contracts, and evidence ceilings replace conflicting or underspecified draft details. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`. This document does not ratify it, authorize implementation, issue a Development Capsule, or confer build, production, publication, certification, or provider authority.

## 1. Files and authorities read

### Authority, requirements, and workflow inputs

| Class | Exact path | Version/state | SHA-256 | Fact used |
|---|---|---|---|---|
| Current constitutional authority | `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | V1.1, current | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Identity, Context Premise, Resonance, Matrix, edge, role, participation, wrong-reading locks, and human reaction form the current rich semantic chain; subordinate drafts cannot replace it. |
| Current authority pointer | `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | current | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Constitution V1.1 remains current while V2.1 awaits ratification. |
| Candidate AIR authority pointer | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CURRENT_AUTHORITY.md` | `DRAFT_FOR_HUMAN_RATIFICATION` | `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Ratification and a separate Development Capsule are required before implementation. |
| Candidate AIR constitution | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `2.1.0-draft` | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Portfolios precede convergence; hard gates remove unsupported/duplicate/stale/wrong-scope candidates; rejected and repaired candidates remain historical evidence. |
| Controlling PRD feature | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/prd/features/F03-activation-hypothesis-portfolio-and-comparative-search.md` | `2.1.0-draft` | `731cabd67be8e7aa6680732e47fb5fcba1e5e6254628b9ceef271dbd965ed7dc` | AIR-FR-013 through AIR-FR-018, F03 entry/terminal states, hard gates, stopping laws, and downstream denial. |
| Controlling Stories | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | `2.1.0-draft` | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-03.01 through AIR-ST-03.03 and their adversarial, supersession, and evidence requirements. |
| Full source draft | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-003-activation-hypothesis-portfolio-and-comparative-search.md` | `DRAFT_AFTER_PRD_PENDING_RATIFICATION` | `88181841a988c783ad29c93fd4a53feea1a952c4d7b33b05a4050ed47ef7a9d2` | Preserved architecture amended rather than rewritten for stylistic uniformity. |
| Disposition decision | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SPEC_DISPOSITION_REPORT.md` | current reconciliation | `86852420631241ce6341a04d258f476473d0490274bb4e22675301cb02c13241` | `TS-AIR-003 = AMEND_TO_CURRENT_AUTHORITY`. |
| Canonical FR traceability | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | validated | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Each of the six FRs has AIR as primary owner, one Story, this spec, a gate, and a claim ceiling. |
| Candidate cross-product authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate, pending ratification | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | AIR owns semantic activation lifecycle; Independent Evaluation owns separate judgment receipts; Pipeline executes rather than recompiles meaning. |
| Candidate semantic ownership | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate, pending ratification | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | AIR owns activation hypotheses, Matrix/Edge meaning, and Planned Activative Intelligence; human Identity DNA and Interview Expression evidence remain externally owned. |
| Source disposition | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | validated | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | `SRC-AHP-PORTFOLIO-001` and `SRC-MOE-001` are required unique evidence; `SRC-AI2-002` and `SRC-CBAR-001` are superseded and are not used as current authority. |
| Specification authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active, specification only | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | WRITE and technical review are authorized; build and Development Capsules are forbidden. |
| Authority-stage decision | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | ratification pending | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Sets `CANDIDATE_NOT_CURRENT` and the maximum pre-ratification quality state. |
| V3.3 writer method | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Requires one-spec scope, ten sections, exact inputs, typed models, failures, evidence, and no self-audit. |

### Wave inputs and draft-dependency law

Both upstream specifications are admitted only as `DRAFT_DEPENDENCY_NOT_ACCEPTED`:

| Upstream | State | SHA-256 | Interface consumed | Downstream revision impact if bytes change |
|---|---|---|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-001.md` | `WRITTEN_PENDING_AUDIT` | `622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc` | Immutable refs, authority/actor refs, epistemic assertions, semantic versions, canonical hashing, commands, blockers, atomic history, and invalidation. | Reopen sections 3, 5, 6, 8, 9, and 10. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-002.md` | `WRITTEN_PENDING_AUDIT` | `258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5` | Exact identity/context inputs, broad signals, tension sites, Primitive bindings, Coalition Signatures, Edge Product candidates, counteractivation, and F02 handoff. | Reopen sections 3, 5, 6, 8, 9, and 10. |

`CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_02_DISPATCH_LOCK.yaml` (1,963 bytes; SHA-256 `3bfa468af8f2be9e89160c4ec3beebe47e87c90397efe18d309c6095d4c78585`) pins both paths, states, and hashes. Neither draft is ratified law. Current Constitution V1.1 remains binding, and candidate interface details remain revision-sensitive.

### Required unique evidence, exact Primitives, and brownfield evidence

| Class / ID | Exact path | SHA-256 | Specific fact used |
|---|---|---|---|
| `SRC-AHP-PORTFOLIO-001` | `.../sources/doctrine/AHP_F08_CANDIDATE_SEARCH.md` | `645bbd86cea223842661ecfa03ccd21f046a9470cecb98735e2da9f46ec15a11` | Meaningful diversity changes strategy rather than seed; invalid candidates precede comparison; evaluator independence and explicit stopping are mandatory. |
| `SRC-MOE-001` | `.../sources/doctrine/MATRIX_OF_EDGING.md` | `7ba1858cd9238a63f32d28e9cc8e7bbe306ba82ac5fa5af4a0346128aa3b6ebb` | Candidates arise from broad signal and tension sites, survive evidence/execution tests, preserve anti-centroid force, and retain fatality evidence. |
| `PRM-PSY-001` | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-001.yaml` | `77c09b403aca66e77b2c71b1faa4dbeacd410d9d6c69685f9c2222dc65bf8ca7` | Match practical, emotional, or social layer; suppress performative or inflexible matching. |
| `PRM-PRS-015` | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-015.yaml` | `b05b6aabef1d48f0a3bf07f5b4a43febe2fb53445df5e1a8524a6ba0f78f48d5` | Preserve current/future tension without utopian hype or demoralizing pain saturation. |
| `PRM-HUM-021` | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/humor_distortion/PRM-HUM-021.yaml` | `53712577ba9f27112afce11fd022a94033f44ceca5f910c6eec2e3c8fae39253` | Irony requires real subtext and sustained conviction; literal-harm and low-literacy contexts suppress it. |
| Brownfield service | `.../reference_implementation/activative_intelligence_v2/candidate_search.py` | `29ab8d37833ea99c8b5ade16ce184708a58d85a5fea71fa752e82356ee1e0b33` | Current predecessor has a useful filter/rank shape but hard-coded float weights, hidden margin default, no receipts, and no governed stopping history. |
| Brownfield models | `.../reference_implementation/activative_intelligence_v2/models.py` | `d75529f08416db1648e95e6762c273aa18fd9f56bbe6c4a6805efbae3909a3b3` | Existing strict hypothesis and portfolio models preserve evidence, roles, locks, candidates, selection, rejections, diversity axes, and stop reason, but flatten lifecycle and lineage. |
| Brownfield contract test | `.../tests/test_contracts.py` | `e727526d363dd87bda00b39beb4e3fce987d43b4a49d18ab59894f8f9cbc2dbb` | Only validates example parsing; it does not prove search, gates, receipts, atomicity, or replay. |
| Brownfield portfolio fixture | `.../examples/08_james_relationship_activation_portfolio.json` | `c7df4d047af815790ca2de8694f1b354b4cc9594bb32a4117ce458e3ce41ac53` | Supplies a reusable relationship-domain fixture and exposes selected/rejected history and float/determinism gaps. |

The `...` AIR paths expand beneath `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE`. No target or ancestor `AGENTS.md` exists for `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-003.md`; the recovery packet records direct Program Control writing authority for this exact path. No unavailable optional or deferred source supports a claim in this specification.

## 2. Problem, user outcome, solution, and scope

### Problem and outcome

A first fluent answer can satisfy surface plausibility while collapsing the live tension into a familiar centroid. The operator then cannot see whether alternatives genuinely differ in psychological role, tension, direction, pressure path, Primitive coalition, relationship move, or counteractivation. The system must instead expose a bounded, reproducible portfolio; remove illegal candidates before comparison; compare eligible candidates under an explicit profile; stop for an evidenced reason; and preserve every rejected, repaired, superseded, and promoted path.

The user outcome is an inspectable decision: either one decisive eligible hypothesis is promoted into a new Planned Activative Intelligence version, or the search stops with a shared defect, exhausted diversity, budget boundary, or operator-owned ambiguity and an exact next action. No fluent candidate is silently treated as a winner.

### Bounded solution

Implement F03 as five separated responsibilities:

1. an AIR-owned hypothesis proposer that emits typed candidates from exact F01/F02 refs and a governed search policy;
2. a deterministic, producer-isolated gate engine that removes candidates failing source fidelity, epistemic legality, identity fit, domain fit, operator constraints, fatal Primitive conflicts, lock preservation, or freshness;
3. an independently identified comparative evaluator that scores only eligible candidates against an exact versioned evaluation profile;
4. a search controller that applies explicit stopping laws without forcing a winner; and
5. an AIR lifecycle service/repository that atomically preserves portfolios, decisions, receipts, dependency edges, repairs, promotion, invalidation, and replay.

### In scope

- immutable `ActivationHypothesis`, `ActivationHypothesisPortfolio`, gate, evaluation, stopping, promotion, command, event, blocker, and receipt contracts;
- strategic diversity proof based on declared semantic axes rather than random seed;
- non-compensable deterministic gates before comparative scoring;
- profile-pinned integer-micros comparison without hidden thresholds;
- bounded search budgets and five governed stopping reasons;
- additive rejection, repair, supersession, and selected-hypothesis promotion history;
- canonical serialization, SHA-256 identity, idempotency, optimistic concurrency, atomic commit/rollback, cancellation, late-result denial, selective invalidation, and historical replay;
- explicit AIR, Independent Evaluation, human, Interview Expression, Pipeline, and Program Control boundaries;
- lossless adaptation or typed rejection of named V2 evidence; and
- an exact F03 handoff that F04 can validate or deny from public contracts and receipts.

### Out of scope and non-goals

- authority ratification, product adoption, implementation, build, a Development Capsule, production, publication, or certification;
- live interview execution, Reaction Observation/Receipt creation, Expression Moment resolution, or source-package mutation;
- canonical Identity DNA mutation or invented audience/relationship evidence;
- final Primitive Coalition Contract compilation, archetype selection, Final Script, composition, rendering, VAE production, Pipeline execution, or Delegation transport;
- treating a provisional Primitive-coalition hypothesis as the later approved Primitive Coalition Contract;
- optimizing one hidden scalar at the expense of failed hard gates;
- learning automatically from rejected portfolios or promoting them to recipes/models without a separate scoped evidence path;
- activating Format 02 or VAE Stage 5; and
- treating the Activative Contract Compiler as the Activative Intelligence Runtime.

## 3. Governing decisions and constraints

### Authority and semantic ownership

Current Constitution V1.1 controls until attributable ratification. The candidate V2.1 package may guide this writing but remains visibly non-current. AIR is the authoritative value owner of hypothesis meaning, portfolio history, selected semantic direction, and Planned Activative Intelligence. Independent Evaluation is the authoritative value owner of gate and comparative-evaluation receipts used for eligibility. A `SearchStoppingReceipt` is an AIR lifecycle record whose gate evidence is evaluator-owned; an operator-owned ambiguity can be resolved only by an attributable `HumanResolutionEpisode`, never by evaluator confidence.

Interview Expression retains live source and reaction evidence. The authorized human retains canonical Identity DNA value authority. AIR consumes exact immutable refs and may not rebuild either. Builder may declare the future F03 dependency, Pipeline may execute an approved derivative program, Delegation may transport the typed package, and Studio may project alternatives and capture commands; none may mutate the AIR portfolio directly.

### Candidate, evidence, and Primitive laws

1. **Portfolio before convergence.** A promotable F03 path contains at least two distinct candidate refs. A single candidate may be retained as incomplete search evidence but cannot be promoted under AIR-FR-013.
2. **Semantic difference, not seed difference.** Every candidate carries a `DiversitySignature`. At least one governed axis value must differ from every otherwise equivalent candidate. Random seed, model sampling ID, punctuation, wording, or cosmetic format does not count.
3. **F02 lineage is exact.** Every candidate references the exact Context Premise, Matrix of Edging, broad signal/tension, Edge Product candidate, source, identity, objective, and registry snapshot used. Generic notes cannot replace refs.
4. **Hypothesis is not observation.** Candidate roles, intended reactions, and state transitions remain `planned` or `inferred`. They cannot be marked `observed` without externally owned direct evidence.
5. **Primitive references are exact.** A candidate may reference an F02 `CoalitionSignature` or a provisional coalition hypothesis. It may not claim a final `PrimitiveCoalitionContract`; F04 owns that later compilation. Exact Primitive ID/version/hash, local job, suppression, conflicts, and misuse survive the handoff.
6. **Hard gates are non-compensable.** A failing gate cannot be outweighed by fluency, model confidence, popularity, average score, deadline pressure, or operator urgency.
7. **Wrong-reading locks survive.** Candidate locks inherit all applicable upstream semantic locks. A candidate may add stricter locks but cannot remove or weaken an inherited lock.
8. **Comparison is profile-governed.** Score dimensions, weights, decisive-margin rule, tie law, applicability, evaluator identity constraints, and calibration evidence live in an exact `ComparativeEvaluationProfileRef`; no implementation default is authoritative.
9. **No forced winner.** Shared defect, exhausted diversity, budget boundary, and operator-owned ambiguity terminate without a selected hypothesis unless a later authorized command cites the necessary repair or human resolution.
10. **Negative evidence remains first-class.** Rejected, repaired, and superseded candidates remain immutable and replayable. Repair creates a new candidate with causal refs; it never edits the rejected bytes.
11. **Promotion is additive.** Promotion creates a new Planned Activative Intelligence object referencing the complete portfolio, gate/evaluation/stopping receipts, and selected candidate. Alternatives remain reachable.
12. **Failure attribution precedes repair.** A repair names the responsible layer and frozen upstream truth. It cannot regenerate valid upstream AIR, Interview Expression, Builder, Pipeline, or VAE objects merely to make scoring pass.

### Active Primitive obligations

- `PRM-PSY-001` applies to hypothesis-role/layer alignment. The portfolio must include evidence for practical, emotional, or social-layer claims and must reject performative or frozen-layer matching.
- `PRM-PRS-015` applies to comparative tension. Current reality cannot be overwhelmed by speculative future promise, and present pain cannot be over-weighted into demoralization.
- `PRM-HUM-021` applies only when exact applicability and subtext exist. Low media literacy, literal-harm context, missing subtext, or broken conviction suppresses the candidate rather than lowering a compensable score.

These are exact bindings when invoked, not mandatory stylistic ingredients for every hypothesis. A candidate that does not invoke a Primitive must not fabricate its binding merely because the F03 package lists it as active evidence.

### Claim ceiling

This output is `WRITTEN_PENDING_AUDIT`; candidate authority is `CANDIDATE_NOT_CURRENT`; specification work is authorized; build authority is false. Before ratification, the maximum later quality state is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. Independent audit may proceed, but no `ACCEPTED_FOR_BUILD`, Development Capsule, implementation, production, or certification claim may be issued.

## 4. Current brownfield architecture

No current `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/` tree exists. The source bundle contains a complete draft, predecessor models/service, tests, and fixtures; they are evidence, not current implementation or build authorization.

| Exact component | Actual behavior | Disposition | Reason and migration constraint |
|---|---|---|---|
| Full source `TS-AIR-003` draft | Defines portfolio, hard gating, evaluation, stopping, promotion, schemas, paths, migration, and tests. | `ADAPT` | Preserve substantive architecture; correct candidate/current authority, ownership, typed completeness, V3.3 receipts, and exact paths. |
| `.../candidate_search.py::CandidateScore` | Nine float dimensions and locally hard-coded weights. | `ADAPT` | Replace binary floats and hidden weights with profile-owned integer micros and exact version/hash. Preserve dimension intent only where AIR-FR-015 authorizes it. |
| `.../candidate_search.py::mechanically_eligible` | Boolean check for evidence, roles, locks, and commitment. | `ADAPT` | Preserve fail-first shape; emit one result per governed hard gate with evidence and reason, not one opaque Boolean. |
| `.../candidate_search.py::select_candidate` | Filters, sorts by weighted total, returns top ID if a default `0.03` margin is met. | `REPLACE` | Hidden float margin, tie dependence, no evaluator identity, no search budget/stopping receipt, no history, and no atomicity violate F03. |
| `.../models.py::ActivationHypothesis` | Strict immutable candidate with domain, pressure, edge, direction, roles, stance, stakes, dose, participation, locks, evidence, freshness, and confidence. | `ADAPT` | Reuse useful semantics; replace floats, add F01/F02 refs, epistemic assertions, diversity proof, Primitive applicability, owner, schema, lineage, and lifecycle identity. |
| `.../models.py::ActivationHypothesisPortfolio` | At least two candidates; validates unique IDs and known selected/rejected IDs. | `ADAPT` | Preserve uniqueness and minimum portfolio intent; replace embedded mutable-like status lists with immutable candidate/decision refs and additive versions. |
| `.../tests/test_contracts.py::test_portfolio` | Parses one JSON fixture. | `ACTIVATE` | Retain as migration regression only; it proves neither semantics nor execution. |
| `.../08_james_relationship_activation_portfolio.json` | Two relationship candidates with evidence, locks, selected ID, diversity axes, and free-text stop reason. | `ACTIVATE` | Use as V2 migration fixture. Convert scores only under explicit numeric policy and retain original bytes/hash. |
| `SRC-AHP-PORTFOLIO-001` | Defines Pipeline candidate-search execution doctrine. | `ADAPT_AS_EVIDENCE` | Reuse diversity/filter/evaluator/stop laws; current candidate ownership places semantic F03 compilation in AIR and later execution in Pipeline. |
| `SRC-MOE-001` | Defines broad signal, candidate survival, coalition signature, Edge Product, anti-centroid, routeability, and fatality. | `REUSE_AS_REQUIRED_EVIDENCE` | Preserve ontology and anti-centroid laws; F03 consumes exact F02 refs rather than rebuilding Matrix meaning. |

The historical `source://ai2_predecessor/...` notation is not a portable implementation path. All future migration and regression work must use the exact repository paths named here and in the later Development Capsule. Historical bytes remain unchanged.

## 5. Proposed architecture and workflows

### Components and responsibilities

| Component | Responsibility | Forbidden behavior |
|---|---|---|
| `HypothesisProposalPort` | Receives minimum-complete Hunter context and returns typed candidate proposals plus model/program binding evidence. | Selection, self-evaluation, source mutation, or untyped prose output. |
| `HypothesisPortfolioCompiler` | Resolves exact F01/F02 refs, validates diversity signatures, creates immutable AIR hypotheses/portfolio versions, and stages lineage. | Rebuilding Matrix, Edge Product, Identity DNA, or live evidence. |
| `F03GateEngine` | Executes deterministic hard-gate profile from an evaluator-isolated identity and emits `HypothesisGateResult` records. | Weighted compensation or candidate mutation. |
| `F03ComparativeEvaluator` | Compares only eligible candidates under an exact profile and emits one immutable `ComparativeEvaluationReceipt`. | Generating candidates, changing profile values, or promoting a winner. |
| `HypothesisSearchController` | Applies budget, requests bounded additional diversity/repair, detects stop condition, and emits a stop command. | Arbitrary loop count, hidden threshold, or forced winner. |
| `HypothesisPortfolioService` | Enforces commands, lifecycle, concurrency, idempotency, cancellation, promotion, and authority boundaries. | Provider calls inside a transaction or hidden state mutation. |
| `HypothesisPortfolioRepository` | Atomically appends artifacts, edges, command records, receipts, and projections; supports exact replay. | Update/delete of historical objects or artifact/receipt asymmetry. |
| `F03InvalidationProjector` | Traverses typed material dependencies and appends stale projections/receipts. | Invalidating unrelated descendants or deleting history. |
| `F03HandoffAdapter` | Emits exact eligible package for F04 with all limitations and dependency hashes. | Converting provisional coalition references into a final Primitive Coalition Contract. |

### Lifecycle and state transitions

The AIR-owned portfolio aggregate uses `OPEN -> GATED -> COMPARED -> STOPPED -> PROMOTED`. `CANCELLED` and `SUPERSEDED` are terminal projections. A new immutable portfolio version is appended for each accepted candidate batch, repair, gate set, comparison, or stop decision; state is never edited in place.

Allowed transitions are:

- `OPEN -> OPEN`: append a strategically distinct candidate batch or a causally linked repair;
- `OPEN -> GATED`: every current candidate has an exact gate result;
- `GATED -> COMPARED`: at least two eligible candidates and one independent comparative receipt exist;
- `GATED -> STOPPED`: shared defect, diversity exhausted, budget boundary, or operator-owned ambiguity is proven without a comparison winner;
- `COMPARED -> OPEN`: a governed search decision requests one bounded additional batch and budget remains;
- `COMPARED -> STOPPED`: one of the five stop laws is proven;
- `STOPPED -> PROMOTED`: stop reason is `DECISIVE_ELIGIBLE_WINNER`, selected candidate is eligible/current, and promotion refs are complete;
- any nonterminal state `-> CANCELLED`: attributable cancellation wins before commit; and
- any nonhistorical projection `-> SUPERSEDED`: an authorized successor replaces the current head while preserving the old path.

There is no `COMPARED -> PROMOTED` shortcut. A stopping receipt is mandatory.

### Workflow A — open and populate a strategically diverse portfolio

1. `OpenHypothesisPortfolioCommand` supplies caller-generated command/idempotency IDs, expected aggregate version, exact authority/actor refs, F01/F02 contract refs, source/identity/context/Matrix/Edge/objective refs, search policy, budget, evaluation-profile refs, and caller-supplied event time.
2. The service resolves every ref by ID, version, and SHA-256. Stale, absent, ineligible, or owner-mismatched dependencies block before proposal.
3. The compiler creates a minimum-complete Hunter capsule: source spans permitted for this use; planned Context Premise; broad signals/tension sites; exact Edge Product candidates; Primitive applicability; relationship state; objective; required locks; diversity axes; and no approval authority.
4. Proposal calls execute outside the repository transaction. Each attempt is bound to an exact implementation/model/harness version, context hash, tool grant, budget reservation, and `attempt_id` derived from command ID plus ordinal.
5. Returned candidates are parsed as closed contracts. IDs are content-addressed from canonical proposal bytes plus the stable attempt coordinate; current time, random UUIDs, filesystem paths, or response arrival order cannot affect identity.
6. The compiler rejects semantic duplicates, proves each surviving candidate's declared difference axes, and stages new immutable hypotheses, the next portfolio version, lineage edges, command record, and receipt atomically.

### Workflow B — apply hard eligibility gates before scoring

1. `GateHypothesisPortfolioCommand` pins the portfolio and exact gate profile.
2. `F03GateEngine` evaluates, in a deterministic order, source fidelity, epistemic legality, identity fit, domain fit, operator constraints, fatal Primitive conflict, upstream-lock preservation, lineage completeness, current-version freshness, and semantic-duplicate denial.
3. Every gate emits `PASS`, `FAIL`, or `NOT_APPLICABLE` with reason and evidence. `NOT_APPLICABLE` is legal only when the gate profile defines its applicability rule and evidence proves the condition; absence or parser inability is not `NOT_APPLICABLE`.
4. Any `FAIL` makes the candidate ineligible. No weighted score is computed for it. The candidate and result remain in portfolio history.
5. The complete gate set and portfolio state commit atomically. Partial gate sets cannot become current.

### Workflow C — compare eligible candidates independently

1. `CompareEligibleHypothesesCommand` supplies exact portfolio, eligible-candidate, evaluation-profile, producer, and evaluator refs.
2. Producer and evaluator actor/implementation authority identities must differ. The evaluator loads all exact evidence and contradictions; it receives no provider-private ranking.
3. The evaluator scores source alignment, audience fit, relationship-stage fit, desired-state-transition fit, counteractivation control, freshness, and downstream derivative potential in integer micros under the profile's declared weights and applicability rules.
4. The profile defines lexicographic tie-break behavior and a decisive-margin rule. No library default exists. If the profile cannot distinguish the top candidates, the receipt reports `AMBIGUOUS`, not a fabricated winner.
5. The receipt preserves dimension results, hard-gate refs, candidate ordering, uncertainty, limitations, calibration refs, model/harness binding, baseline comparison, fallback, and applicability envelope.

### Workflow D — repair, continue, or stop

`HypothesisSearchController` evaluates the current portfolio and remaining budget after each gate/comparison cycle. It may request a bounded next batch only when the request names the missing diversity axis or attributable failed layer. A repair creates a new candidate with `repairs_hypothesis_ref`, `failed_result_refs`, `frozen_upstream_refs`, and `repair_scope`; it cannot edit the original or regenerate valid upstream work.

Exactly one primary `StopReason` is allowed:

- `DECISIVE_ELIGIBLE_WINNER`: one current eligible candidate satisfies the profile's exact decisive rule;
- `SHARED_DEFECT`: every eligible route shares the same attributable upstream or local defect;
- `DIVERSITY_EXHAUSTED`: all governed axes permitted by evidence/search policy have been attempted or ruled inapplicable;
- `BUDGET_BOUNDARY`: the next admissible attempt would exceed an explicit candidate, round, token, or provider-cost budget; or
- `OPERATOR_OWNED_AMBIGUITY`: remaining choice depends on new meaning, taste, identity interpretation, or policy owned by an authorized human.

The last four reasons require `selected_hypothesis_ref: null`. `OPERATOR_OWNED_AMBIGUITY` includes the decision question and allowed choices but does not manufacture a `HumanResolutionEpisode`.

### Workflow E — promote, hand off, invalidate, and replay

`PromoteSelectedHypothesisCommand` requires the stopped portfolio, decisive selected candidate, all gate/evaluation/stop receipts, exact F01/F02 refs, and expected Planned Activative Intelligence head. AIR creates a new immutable Planned Activative Intelligence object marked planned, links the entire portfolio, and emits a promotion receipt. It does not erase alternatives or assert observation.

F04 receives only exact refs plus public receipts and may deny stale, unevaluated, unsupported, or provisional-meaning misuse. Superseding a material source, identity, Context Premise, Matrix, Edge Product, Primitive binding, objective, profile, evaluator contract, or candidate appends invalidation receipts for dependent current projections. Historical replay resolves stored dependency bytes and reproduces the original decision even after current invalidation.

### Atomicity, idempotency, concurrency, cancellation, and late results

Every command computes a canonical payload hash. An identical command ID/payload/dependency snapshot returns the original receipt. Reusing an ID with different bytes returns `AIR_F03_IDEMPOTENCY_CONFLICT`. `expected_aggregate_version` is compared at commit; a stale command returns `AIR_F03_STALE_EXPECTED_VERSION` and commits no semantic artifact. Artifact, portfolio, decisions, edges, command record, and receipt become visible in one transaction or not at all.

Cancellation before commit yields `AIR_F03_CANCELLED_NO_COMMIT`. Cancellation after a successful commit returns the committed receipt and may append a later cancellation command; it cannot erase state. A model/evaluator result arriving after cancellation, supersession, budget closure, or dependency drift is retained as noncurrent attempt evidence and cannot be attached to the current portfolio.

## 6. Data models, contracts, schemas, and APIs

All contracts are immutable, reject unknown fields, require nonempty strings, and use closed enums/tagged unions. Shared `ImmutableRef`, `AuthorityRef`, `ActorRef`, `EvidenceRef`, `EpistemicAssertion`, and `SemanticObjectVersion` follow the exact pinned F01 draft; F02 references follow the exact pinned F02 draft. Those shapes remain revision-sensitive until independent audit and ratification.

### Shared scalar and reference rules

- `StableId`: lowercase ASCII `[a-z0-9][a-z0-9._:-]{2,127}`.
- `Sha256`: lowercase hexadecimal string of exactly 64 characters.
- `SemanticVersion`: governed semantic-version string, never `latest`.
- `Micros`: integer `0..1_000_000`; no binary float appears in canonical objects.
- `CanonicalTimestamp`: caller-supplied RFC 3339 UTC at second precision. It is receipt evidence, not a semantic-content input unless the schema explicitly says so.
- Ordered semantic collections are tuples. Set-like refs are deduplicated and sorted by `(object_id, version, sha256)`. Meaningful order is stored explicitly and never derived from map or filesystem iteration.

### `ActivationHypothesis` — `ca.air.activation-hypothesis/2.1.0-candidate`

| Field | Type | Owner and validation |
|---|---|---|
| `semantic_object` | `SemanticObjectVersion` | AIR; owner product must be AIR and lifecycle starts `PROPOSED`. |
| `domain` | `SOURCE | RELATIONSHIP | AUDIENCE | CAMPAIGN | DERIVATIVE` | AIR under F01; exactly one. |
| `source_kind` | `interview_expression | public_comment | direct_message_reply | authored_source | live_premise | research_synthesis | operator_supplied | legacy_migrated` | Upstream source authority; mandatory, unknown values rejected, never guessed by migration. |
| `source_refs` | `tuple<ImmutableRef, 1..n>` | Source owner/operator authority; exact admitted lineage for interview, public comment, DM, authored, live-premise, research, operator-supplied, or legacy-migrated inputs. |
| `canonical_interview_source_package_refs` | `tuple<ImmutableRef, 0..n>` | Interview Expression; required for interview-derived candidates and empty for non-interview sources unless a real package is present. |
| `interview_provenance` | `InterviewProvenance?` | Required when `source_kind = interview_expression`; contains at least one nonempty Reaction Receipt ref and at least one nonempty Expression Moment ref. Optional for other kinds and fully validated when present. |
| `identity_dna_ref` | `ImmutableRef` | Human-owned value; AIR read-only. |
| `context_premise_ref` | `ImmutableRef` | AIR F02 current eligible version. |
| `matrix_of_edging_ref` | `ImmutableRef` | AIR F02 current evaluated version. |
| `broad_signal_refs` | `tuple<ImmutableRef, 1..n>` | AIR F02; each resolves inside the Matrix. |
| `tension_site_refs` | `tuple<ImmutableRef, 1..n>` | AIR F02; required for the proposed edge. |
| `edge_product_candidate_ref` | `ImmutableRef` | AIR F02; current, survival-passing, and not final F04 contract. |
| `objective_ref` | `ImmutableRef` | Owning program/human authority; exact version. |
| `psychological_role` | `EpistemicAssertion<NonEmptyText>` | AIR hypothesis; must be planned/inferred, not observed absent direct evidence. |
| `tension` | `EpistemicAssertion<NonEmptyText>` | AIR; traces to tension-site refs. |
| `activation_directions` | `tuple<MIRROR | TARGET | MORAL | ASPIRATION | CONTRADICTION | CURIOSITY, 1..n>` | AIR; unique, declared order. |
| `pressure_path` | `NonEmptyText` | AIR; must identify source pressure -> role -> intended movement. |
| `stance` | `NonEmptyText` | AIR; identity-fit gated. |
| `identity_urges` | `tuple<NonEmptyText, 1..n>` | AIR; evidence-linked planned hypotheses. |
| `stakes` | `tuple<NonEmptyText, 1..n>` | AIR; each traces to source/context evidence. |
| `pressure_dose` | `integer 0..5` | AIR; bounded by source/relationship context. |
| `participation_design` | `NonEmptyText` | AIR; no manipulation authority implied. |
| `intended_state_transition` | `StateTransitionHypothesis` | AIR; `from_state`, `to_state`, evidence/uncertainty, never observed by declaration. |
| `smallest_useful_commitment` | `NonEmptyText` | AIR; executable but not an approval. |
| `expected_signal_refs` | `tuple<ExpectedSignal, 0..n>` | AIR; every signal declares owner and epistemic expectation. |
| `counteractivation_hypotheses` | `tuple<CounteractivationHypothesis, 1..n>` | AIR; risk, trigger, mitigation, evidence. |
| `inherited_wrong_reading_locks` | `tuple<ImmutableRef, 1..n>` | Upstream lock owner; all applicable locks preserved. |
| `additional_wrong_reading_locks` | `tuple<WrongReadingLock, 0..n>` | AIR; stricter only. |
| `primitive_applications` | `tuple<PrimitiveApplication, 0..n>` | AIR; exact refs/local job/applicability; never a final F04 contract. |
| `diversity_signature` | `DiversitySignature` | AIR; mechanically proves semantic difference. |
| `proposal_binding_ref` | `ImmutableRef` | Producing implementation/model/harness owner. |
| `proposal_attempt_ref` | `ImmutableRef` | AIR attempt ledger; exact context/tools/budget/result. |
| `repairs_hypothesis_ref` | `ImmutableRef?` | Required only for repair; prior candidate remains immutable. |

`StateTransitionHypothesis` is `{from_state: NonEmptyText, to_state: NonEmptyText, epistemic_state: planned | inferred, evidence_refs: tuple<EvidenceRef,1..n>, uncertainty_micros: Micros}`. `PrimitiveApplication` is `{primitive_ref, registry_snapshot_ref, local_job, activation_condition_refs, suppression_condition_refs, misuse_constraint_refs, conflict_refs, applicability: APPLIES | SUPPRESSED | NOT_APPLICABLE, evidence_refs}`. `NOT_APPLICABLE` requires an explicit profile rule and evidence.

`InterviewProvenance` is `{reaction_receipt_refs: tuple<ImmutableRef,1..n>, expression_moment_refs: tuple<ImmutableRef,1..n>}`. AIR validates and preserves these Interview Expression-owned refs; it cannot construct, amend, or infer either object. Ambiguous source kind is rejected rather than guessed.

### Diversity contracts

`DiversitySignature` contains exactly these governed axes, each as zero or one typed value: `psychological_role`, `tension`, `activation_direction_set`, `pressure_path`, `primitive_coalition_hypothesis_ref`, `relationship_move`, `stance`, `counteractivation_strategy`, and `smallest_commitment`. It also contains `compared_candidate_refs`, `differing_axes_by_candidate`, and `proof_sha256`.

`differing_axes_by_candidate` is an ordered tuple of `{other_candidate_ref, differing_axes: tuple<DiversityAxis,1..n>}`. An axis counts only when the canonical values differ and both are evidence-permitted. Wording, model ID, random seed, response ordering, formatting, or punctuation are not diversity axes. A semantic-equivalence detector may flag likely duplication, but a learned similarity score alone cannot prove difference or identity; deterministic axis comparison is authoritative.

### `ActivationHypothesisPortfolio` — `ca.air.activation-hypothesis-portfolio/2.1.0-candidate`

| Field | Type | Owner and validation |
|---|---|---|
| `semantic_object` | `SemanticObjectVersion` | AIR; immutable aggregate version. |
| `search_policy_ref` | `ImmutableRef` | AIR/Program Control-governed policy; exact version/hash. |
| `search_budget` | `SearchBudget` | Command owner; positive explicit maxima. |
| `upstream_snapshot_refs` | `tuple<ImmutableRef,1..n>` | AIR; exact F01/F02/source/identity/objective/profile snapshot. |
| `candidate_refs` | `tuple<ImmutableRef,1..n>` | AIR; unique, stable semantic order by accepted attempt ordinal. |
| `candidate_state_records` | `tuple<CandidateStateRecord,1..n>` | AIR; one current record per candidate plus complete prior records. |
| `gate_result_refs` | `tuple<ImmutableRef,0..n>` | Independent Evaluation; none missing after `GATED`. |
| `comparative_evaluation_refs` | `tuple<ImmutableRef,0..n>` | Independent Evaluation; append-only. |
| `stopping_receipt_ref` | `ImmutableRef?` | Required in `STOPPED`/`PROMOTED`. |
| `selected_hypothesis_ref` | `ImmutableRef?` | Allowed only with decisive stop and passing current refs. |
| `portfolio_state` | `OPEN | GATED | COMPARED | STOPPED | PROMOTED | CANCELLED | SUPERSEDED` | AIR lifecycle. |
| `supersedes_portfolio_ref` | `ImmutableRef?` | Required after version 1. |
| `promotion_ref` | `ImmutableRef?` | Required only in `PROMOTED`. |

`SearchBudget` is `{maximum_candidate_count: PositiveInteger, maximum_round_count: PositiveInteger, maximum_model_tokens: NonNegativeInteger, maximum_provider_cost_micros: NonNegativeInteger, consumed_candidate_count, consumed_round_count, consumed_model_tokens, consumed_provider_cost_micros}`. Zero provider/model budgets are legal for deterministic proposals. No unspecified default exists.

`CandidateStateRecord` is `{candidate_ref, state: PROPOSED | GATE_REJECTED | ELIGIBLE | REPAIRED | SUPERSEDED | SELECTED | PROMOTED, caused_by_receipt_ref, reason_codes, prior_state_record_ref}`. State changes append records; candidate bytes never change.

### Hard-gate and comparative-evaluation contracts

`HypothesisGateResult` uses schema `ca.air.hypothesis-gate-result/2.1.0-candidate` and fields:

```text
result_ref: ImmutableRef
portfolio_ref: ImmutableRef
hypothesis_ref: ImmutableRef
gate_profile_ref: ImmutableRef
evaluator_actor_ref: ActorRef
producer_actor_ref: ActorRef
checks: tuple[GateCheck, exactly all applicable profile checks]
overall: ELIGIBLE | INELIGIBLE
input_hashes: tuple<Sha256, 1..n>
evaluated_at: CanonicalTimestamp
receipt_sha256: Sha256
```

`GateCheck` is `{gate: SOURCE_FIDELITY | EPISTEMIC_LEGALITY | IDENTITY_FIT | DOMAIN_FIT | OPERATOR_CONSTRAINTS | FATAL_PRIMITIVE_CONFLICT | WRONG_READING_LOCKS | LINEAGE_COMPLETE | CURRENT_VERSION | SEMANTIC_DUPLICATE, applicability: APPLIES | NOT_APPLICABLE, verdict: PASS | FAIL | NOT_APPLICABLE, reason_code, evidence_refs}`. `overall` is eligible only when every applicable check passes. `NOT_APPLICABLE` cannot hide an error, missing input, unknown value, or unsupported validator.

`ComparativeEvaluationReceipt` uses `ca.air.comparative-evaluation-receipt/2.1.0-candidate`:

```text
receipt_ref: ImmutableRef
portfolio_ref: ImmutableRef
evaluation_profile_ref: ImmutableRef
eligible_candidate_refs: tuple[ImmutableRef, 2..n]
producer_binding_refs: tuple[ImmutableRef, 1..n]
evaluator_binding_ref: ImmutableRef
dimension_results: tuple<CandidateDimensionResults, exactly one per candidate]
ordered_candidate_refs: tuple[ImmutableRef, 2..n]
decision: DECISIVE | AMBIGUOUS | SHARED_DEFECT
provisional_winner_ref: ImmutableRef | null
decisive_margin_micros: Micros | null
limitations: tuple<NonEmptyText, 0..n>
calibration_evidence_refs: tuple<ImmutableRef, 1..n>
baseline_comparison_ref: ImmutableRef
fallback_ref: ImmutableRef
applicability_envelope_ref: ImmutableRef
receipt_sha256: Sha256
```

Each `CandidateDimensionResults` contains exactly one `DimensionResult` for `SOURCE_ALIGNMENT`, `AUDIENCE_FIT`, `RELATIONSHIP_STAGE_FIT`, `DESIRED_STATE_TRANSITION_FIT`, `COUNTERACTIVATION_CONTROL`, `FRESHNESS`, and `DOWNSTREAM_DERIVATIVE_POTENTIAL`. A result is `{dimension, applicability, score_micros: Micros | null, weight_micros: Micros | null, evidence_refs, reason_code}`. Applicable weights sum to `1_000_000`; multiplication and division use integer arithmetic and a profile-declared rounding mode. A `NOT_APPLICABLE` dimension has null score/weight and cannot be silently redistributed unless the exact profile defines normalization.

### Search stopping and promotion

`SearchStoppingReceipt` (`ca.air.search-stopping-receipt/2.1.0-candidate`) contains `receipt_ref`, `portfolio_ref`, `reason`, `selected_hypothesis_ref`, `evaluation_receipt_refs`, `budget_snapshot`, `attempted_diversity_axes`, `unattempted_axis_reasons`, `shared_defect_refs`, `operator_question`, `allowed_operator_choices`, `controller_actor_ref`, `authority_ref`, `event_time`, and `receipt_sha256`.

- `selected_hypothesis_ref` is required only for `DECISIVE_ELIGIBLE_WINNER` and forbidden otherwise.
- `shared_defect_refs` is nonempty only for `SHARED_DEFECT`.
- `unattempted_axis_reasons` must prove evidence/policy inapplicability for `DIVERSITY_EXHAUSTED`.
- the consumed budget must meet an exact boundary for `BUDGET_BOUNDARY`.
- `operator_question` and at least two typed choices are required for `OPERATOR_OWNED_AMBIGUITY`; no operator resolution is inferred.

`PlannedActivativeIntelligencePromotion` contains `{promotion_ref, prior_planned_pack_ref, new_planned_pack_ref, selected_hypothesis_ref, complete_portfolio_ref, gate_result_refs, comparative_evaluation_ref, stopping_receipt_ref, source_and_identity_refs, matrix_and_edge_refs, authority_ref, actor_ref, command_ref, promotion_receipt_ref}`. The new Planned Pack carries planned epistemic assertions and does not claim a human reaction.

### Commands, events, and repository interface

Closed command variants are `OpenHypothesisPortfolioCommand`, `AppendHypothesisBatchCommand`, `GateHypothesisPortfolioCommand`, `CompareEligibleHypothesesCommand`, `RecordHypothesisRepairCommand`, `StopHypothesisSearchCommand`, `PromoteSelectedHypothesisCommand`, `CancelHypothesisSearchCommand`, `SupersedeHypothesisPortfolioCommand`, `InvalidateF03DescendantsCommand`, and `ReplayHypothesisSearchCommand`.

Every command requires `command_id`, `idempotency_key`, `aggregate_id`, `expected_aggregate_version`, `actor_ref`, `authority_ref`, `issued_at`, exact input refs, `dependency_snapshot_sha256`, and `command_payload_sha256`. Command-specific required fields have no implied defaults. Events are `HypothesisPortfolioOpened`, `HypothesisBatchAppended`, `HypothesesGated`, `HypothesesCompared`, `HypothesisRepairRecorded`, `HypothesisSearchStopped`, `HypothesisPromoted`, `HypothesisSearchCancelled`, `HypothesisPortfolioSuperseded`, `F03DescendantsInvalidated`, and `HypothesisSearchReplayed`.

The repository port is:

```text
load_exact(ref: ImmutableRef) -> ImmutableArtifact
load_head(aggregate_id: StableId) -> PortfolioProjection | null
load_command(command_id: StableId) -> CommandRecord | null
begin(command_id, idempotency_key, expected_version) -> F03Transaction
stage_artifact(transaction, canonical_bytes, sha256)
stage_edge(transaction, TypedLineageEdge)
stage_receipt(transaction, canonical_bytes, sha256)
stage_command_record(transaction, CommandRecord)
stage_projection(transaction, PortfolioProjection)
commit(transaction) -> AtomicCommitReceipt
rollback(transaction, reason_code) -> RollbackReceipt
list_material_descendants(root_ref, edge_types) -> tuple[ImmutableRef, ...]
replay(command_record_ref, dependency_snapshot_ref) -> ReplayReceipt
```

An artifact without its command/receipt/edges, or a receipt without its artifact when success claims one, is invalid state and triggers rollback/quarantine.

### Canonical serialization, hashing, compatibility, and examples

Canonical bytes are UTF-8 without BOM, Unicode NFC, LF newlines, I-JSON-compatible, lexicographically sorted object keys, and no insignificant whitespace. Enums use exact wire strings. Integers are base-10 JSON numbers. Absolute paths, environment variables, local hostnames, process IDs, current clock reads, random UUIDs, provider response order, dictionary insertion order, and filesystem traversal order are excluded. Schema ID/version are included. Identity/hash fields are omitted from their own preimage according to one versioned canonicalization profile.

Positive example: two candidates reference the same Matrix and objective, but one places the audience as `witness` inside a regret tension while another places it as `challenger` inside a moral-violation tension; the `DiversitySignature` records both canonical axis differences and evidence refs. Negative example: two responses differ only in phrasing and seed; semantic axis values are identical, so the second returns `AIR_F03_STRATEGIC_DIVERSITY_UNPROVEN` and is not added as eligible diversity.

Compatibility is semantic, not parse-only. Consumers negotiate schema versions, F01/F02 hashes, gate/evaluation profile features, stop reasons, and required evidence classes. Adapters may add explicit absent/unknown fields but may not drop locks, lineage, negative candidates, epistemic states, evaluator identity, or stop evidence.

## 7. Implementation stages and exact target paths

These are future paths only. Ratification/adoption, independent technical acceptance, and a bounded Development Capsule must precede any implementation.

| Stage | Exact future target paths | FR / Story evidence and gate |
|---|---|---|
| 1 — domain contracts | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/hypothesis_portfolio.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/hypothesis_search.py` | AIR-FR-013/016/017; AIR-ST-03.01–03; immutable models, diversity proof, history, budget, stopping invariants. |
| 2 — canonical schemas | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f03.activation-hypothesis.schema.json`; `.../air.f03.hypothesis-portfolio.schema.json`; `.../air.f03.gate-result.schema.json`; `.../air.f03.comparative-evaluation.schema.json`; `.../air.f03.search-stopping.schema.json`; `.../air.f03.promotion.schema.json` | All FRs; closed schemas, exact versions, positive/negative fixtures; no shared release bytes in this stage. |
| 3 — serialization/repository | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/serialization/canonical.py`; `.../repositories/hypothesis_portfolio_repository.py` | AIR-FR-016/018; deterministic identity, optimistic concurrency, idempotency, atomicity, replay. |
| 4 — proposal/compiler | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/proposals/hypothesis_proposal_port.py`; `.../services/hypothesis_portfolio_compiler.py` | AIR-FR-013; exact Hunter capsule, typed proposal parse, strategic-diversity proof, no selection authority. |
| 5 — hard gates | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/f03_gate_engine.py` | AIR-FR-014; every hard gate, `NOT_APPLICABLE` law, evaluator isolation, no score compensation. |
| 6 — independent comparison/search | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/f03_comparative_evaluator.py`; `.../search/hypothesis_search_controller.py` | AIR-FR-015/017; profile-pinned comparison, explicit five-way stopping, bounded continuation. |
| 7 — lifecycle/promotion | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/hypothesis_portfolio_service.py`; `.../invalidation/f03_invalidation_projector.py` | AIR-FR-016/018; repair lineage, complete history, stop-before-promotion, descendant-only invalidation. |
| 8 — adapters/migration | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/f02_to_f03.py`; `.../adapters/f03_to_f04.py`; `.../migrations/v2_candidate_search_to_air_f03.py` | All Stories; lossless translation or typed block, public downstream denial, no semantic fork. |
| 9 — evidence suites | Exact paths in section 10 | All FRs/Stories; two fresh processes, clean environment, fault injection, reference-slice, architecture, migration, recovery. |

No stage is build-ready from this document. Implementation tasks must later map to the exact accepted spec hash and Development Capsule allowlist; the path list above is not self-executing authority.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Trigger | Required behavior |
|---|---|---|
| `AIR_F03_UPSTREAM_DRAFT_DRIFT` | Either pinned F01/F02 path, state, or SHA-256 differs. | Stop advancement and reopen sections 3, 5, 6, 8, 9, and 10. |
| `AIR_F03_REQUIRED_SOURCE_UNAVAILABLE` | Required authority/current implementation/unique evidence cannot be read. | Block writing/build path; do not reconstruct it. |
| `AIR_F03_UPSTREAM_REF_STALE` | Source, identity, Context Premise, Matrix, Edge, objective, Primitive, policy, or profile ref is not current for the command. | Reject before proposal/commit and name the stale ref. |
| `AIR_F03_LINEAGE_INCOMPLETE` | A required rich object is flattened to note/text or cannot resolve. | Reject candidate; do not reconstruct missing meaning. |
| `AIR_F03_STRATEGIC_DIVERSITY_UNPROVEN` | Difference exists only in words, seed, ordering, or unsupported axis. | Retain attempt evidence; do not count/add as eligible diversity. |
| `AIR_F03_SEMANTIC_DUPLICATE` | Canonical diversity axes and intent match an existing candidate. | Reject duplicate with refs to the existing candidate. |
| `AIR_F03_HARD_GATE_FAILED` | Any applicable source/epistemic/identity/domain/operator/Primitive/lock/lineage/current/duplicate gate fails. | Mark candidate ineligible; never score it. |
| `AIR_F03_NOT_APPLICABLE_UNJUSTIFIED` | A gate/dimension is N/A without profile rule and evidence. | Treat validation as failed, not skipped. |
| `AIR_F03_WRONG_READING_LOCK_WEAKENED` | Candidate removes or weakens an inherited lock. | Reject candidate and identify missing/changed lock. |
| `AIR_F03_FINAL_COALITION_OVERCLAIM` | Candidate claims a final Primitive Coalition Contract before F04. | Reject/repair type; preserve provisional F02 refs only. |
| `AIR_F03_SELF_EVALUATION` | Producer and evaluator identity/authority contexts are not independent. | Reject eligibility and comparison receipt. |
| `AIR_F03_PROFILE_UNSUPPORTED` | Required dimensions, weights, tie/decisive law, calibration, or applicability cannot be enforced. | Block comparison; capability presence alone cannot pass. |
| `AIR_F03_NO_LAWFUL_STOP` | Controller reaches a loop/limit without proving one of five stop reasons. | Stop execution with blocker, not a `SearchStoppingReceipt`. |
| `AIR_F03_STOP_INVARIANT_VIOLATION` | Stop-specific required/forbidden fields conflict. | Reject receipt and retain prior portfolio head. |
| `AIR_F03_PROMOTION_NOT_DECISIVE` | Promotion lacks decisive stop, selected eligible current candidate, or complete receipts. | Reject with no Planned Pack. |
| `AIR_F03_REPAIR_SCOPE_UNATTRIBUTED` | Repair lacks responsible layer/frozen upstream refs or would regenerate valid upstream work. | Reject repair command. |
| `AIR_F03_STALE_EXPECTED_VERSION` | Aggregate head changed before commit. | Roll back staged state; return current ref. |
| `AIR_F03_IDEMPOTENCY_CONFLICT` | Same command/idempotency ID has different payload or dependency snapshot. | Reject mutation and receipt reuse. |
| `AIR_F03_NON_ATOMIC_STATE` | Artifact, candidate state, edge, command record, receipt, or projection set is incomplete/inconsistent. | Roll back; quarantine journal evidence; alert. |
| `AIR_F03_LATE_RESULT_NONCURRENT` | Result arrives after cancellation, stop, supersession, budget closure, or ref drift. | Preserve as attempt evidence; never attach to current portfolio. |
| `AIR_F03_MIGRATION_MEANING_MISSING` | V2 record lacks attributable domain, lineage, gate, epistemic, owner, profile, or stop semantics. | Block current eligibility; preserve source bytes and missing-field list. |

Deterministic validation failures are not retried. Transient provider/model/evaluator transport failures may retry with the same attempt ID, exact input/context hash, budget reservation, and idempotency key. A quality repair uses a new command/candidate ID and causal refs. Provider substitution requires an explicit compatible binding and emits a new attempt record; silent fallback is prohibited.

### Migration and compatibility

The V2 adapter preserves exact source files and hashes, candidate ordering, roles, locks, evidence, selected/rejected IDs, diversity labels, and stop text as migration evidence. It emits a new V2.1 object only when ownership, F01/F02 refs, epistemic state, gate/evaluation profile, and stop semantics can be supplied by attributable current evidence.

V2 binary floats are not silently copied into canonical integer micros. If original JSON lexical decimal text is available, the versioned migration profile may parse decimal text and use its declared rounding law; the receipt records original token and converted integer. A value available only as an in-memory binary float remains in a nonauthoritative attachment and blocks score-dependent eligibility. Free-text `stopping_reason` maps only when one governed reason is unambiguous; otherwise `AIR_F03_MIGRATION_MEANING_MISSING` names the required human decision.

Migration never overwrites V2 bytes, guesses source classification, promotes planned fields to observed, or treats old selected IDs as current acceptance. Deprecated schema support does not invalidate historical delegations; active commands stay pinned to the versions negotiated at acceptance.

### Rollback, recovery, invalidation, and replay

Uncommitted staging may be removed on rollback; committed semantic history may not. Recovery loads the transaction journal and content-addressed artifacts, verifies every hash and mutual reference, and either completes the same commit when all original preconditions still hold or emits a rollback/quarantine receipt. It cannot synthesize a missing success receipt.

Invalidation traverses material edge types such as `proposed_from`, `constrained_by`, `gated_by`, `evaluated_by`, `repaired_from`, `selected_from`, and `promoted_from`. It appends stale current projections for reachable descendants only. Nonmaterial reference evidence and unrelated products remain current. Exact historical replay resolves the original artifacts, profiles, producer/evaluator bindings, budget, commands, and receipts; current aliases are forbidden. Divergence emits `AIR_F03_REPLAY_DIVERGENCE` and does not rewrite history.

### Observability

Append-only structured events include refs/hashes rather than unrestricted source content: `command_id`, `correlation_id`, aggregate/version, candidate/portfolio refs, producer/evaluator refs, authority, dependency snapshot, gate reason, score profile, stop reason, budget counters, transaction/receipt refs, invalidation fan-out, and duration micros. Required metrics count candidates proposed/duplicate/gate-rejected/eligible/repaired, diversity axes, hard-gate failures, unjustified N/A, comparisons, ambiguous/shared-defect outcomes, stop reasons, budget consumption, idempotent replays/conflicts, stale versions, rollbacks, late results, invalidations, migration blocks, and replay divergence.

Alerts fire on self-evaluation, hidden profile default, missing candidate history, receipt/artifact mismatch, wrong-reading-lock weakening, promotion without decisive stop, nonterminating search, hash drift, or replay divergence. Telemetry never becomes semantic authority or production evidence by itself.

## 9. Behavior-specific acceptance criteria

| ID / governing FR-Story | Given / When / Then pass condition | Concrete failure example and expected denial | Evidence artifact / test layer |
|---|---|---|---|
| AC-01 `AIR-FR-013` / `AIR-ST-03.01` | Given an eligible F02 Matrix, objective, and source context, when a batch proposes witness/regret and challenger/moral-violation routes, then both candidates preserve exact lineage and their diversity proof names role and tension differences. | Two paraphrases with different seeds but identical axis values return `AIR_F03_STRATEGIC_DIVERSITY_UNPROVEN`. | Portfolio/difference receipt; contract + integration. |
| AC-02 `AIR-FR-013` / `AIR-ST-03.01` | Given candidate count two or more, when portfolio compilation completes, then every candidate differs from each semantic equivalent by at least one evidence-permitted governed axis. | A random order change is counted as diversity; architecture test fails. | Canonical diversity matrix; unit + adversarial. |
| AC-03 `AIR-FR-014` / `AIR-ST-03.01` | Given one candidate has stale source and another has a fatal Primitive conflict, when gating runs, then both are ineligible before scoring and retain distinct results/reasons. | Evaluator gives either candidate a high weighted score; comparison is denied with `AIR_F03_HARD_GATE_FAILED`. | Gate result set; deterministic integration. |
| AC-04 `AIR-FR-014` / `AIR-ST-03.01` | Given a gate profile marks a Primitive check N/A only for a candidate invoking no Primitive, when exact applicability evidence resolves, then N/A is preserved. | Parser failure is represented as N/A; `AIR_F03_NOT_APPLICABLE_UNJUSTIFIED` blocks. | Gate applicability fixtures; schema + adversarial. |
| AC-05 `AIR-FR-015` / `AIR-ST-03.02` | Given at least two eligible candidates and an exact evaluation profile, when an independent evaluator compares them, then all seven dimensions, weights, evidence, ordering, decisive law, calibration, baseline, fallback, and applicability are recorded. | Implementation uses hard-coded `0.03` margin or float weights; contract/architecture test fails. | Comparative receipt; contract + integration. |
| AC-06 `AIR-FR-015` / `AIR-ST-03.02` | Given top candidates are inside the profile's ambiguity law, when comparison ends, then decision is `AMBIGUOUS` and no provisional winner is promotion-eligible. | Stable-sort order selects the first arrival; deterministic tie fixture fails. | Ambiguity receipt; unit + fresh-process. |
| AC-07 `AIR-FR-016` / `AIR-ST-03.02` | Given a rejected candidate is repaired, when repair commits, then a new candidate ref links the original, failed results, responsible layer, frozen upstream refs, and bounded repair; original bytes remain resolvable. | Service edits original candidate or drops its rejection; history test fails. | Repair and replay receipts; repository integration. |
| AC-08 `AIR-FR-016` / `AIR-ST-03.02` | Given rejected, superseded, and repaired candidates, when portfolio history is read, then every transition and future applicability remains inspectable. | Projection lists only the winner; `AIR_F03_NON_ATOMIC_STATE`/history invariant fails. | Full candidate-state chain; integration. |
| AC-09 `AIR-FR-017` / `AIR-ST-03.03` | Given a decisive eligible winner, shared defect, exhausted diversity, budget boundary, or operator ambiguity, when stop is requested, then exactly the matching reason-specific fields are present. | `selected_hypothesis_ref` is set for budget exhaustion; `AIR_F03_STOP_INVARIANT_VIOLATION`. | Five stop fixtures; contract + unit. |
| AC-10 `AIR-FR-017` / `AIR-ST-03.03` | Given budget remains but no next request names an evidence-permitted missing axis, when controller considers another round, then it stops with proven exhaustion or a blocker. | Controller loops on arbitrary iteration or paraphrase retries; search-termination test fails. | Controller trace and budget receipt; property + integration. |
| AC-11 `AIR-FR-018` / `AIR-ST-03.03` | Given a decisive stopped portfolio, when promotion runs, then a new planned object references selected candidate, complete portfolio, all gate/evaluation/stop receipts, and exact F01/F02/source/identity refs. | Promotion copies only the winning text or marks intended reaction observed; `AIR_F03_PROMOTION_NOT_DECISIVE`/epistemic denial. | Planned pack + promotion receipt; integration + contract. |
| AC-12 `AIR-FR-018` / `AIR-ST-03.03` | Given F04 consumes the handoff, when any dependency is stale, gate/evaluation receipt missing, or provisional coalition is represented as final, then F04 can deny from public contract alone. | Consumer must inspect AIR internals to find the problem; conformance fails. | Producer/consumer conformance receipt; reference-slice. |
| AC-13 all FRs | Given identical command bytes and dependency snapshot in two fresh processes, when F03 executes, then canonical artifacts/receipts/hashes match byte-for-byte. | Time, random UUID, insertion/traversal order, locale, machine path, environment, or provider arrival order changes bytes. | Hash matrix; clean-environment + determinism. |
| AC-14 all FRs | Given an exact duplicate command, when delivered twice, then one artifact/receipt is returned; changed bytes under the same ID return `AIR_F03_IDEMPOTENCY_CONFLICT`. | Two portfolio versions commit for one command ID. | Command ledger; repository integration. |
| AC-15 all FRs | Given two commands target one expected version, when both commit, then only one succeeds and the loser changes no artifact/receipt/edge/projection. | Orphan receipt remains after stale-version rejection. | Concurrency/fault-injection receipt; repository integration. |
| AC-16 all FRs | Given failure is injected between every staged record, when transaction rolls back, then prior state remains complete and no partial current state is readable. | Candidate exists without gate receipt or receipt without artifact. | Atomicity matrix; fault-injection integration. |
| AC-17 `AIR-ST-03.01–03` | Given cancellation or supersession occurs before a provider/evaluator result arrives, when the late result returns, then it is noncurrent attempt evidence and cannot alter the portfolio. | Late high score promotes a cancelled candidate. | Cancellation/late-result receipt; async integration. |
| AC-18 `AIR-ST-03.01–03` | Given upstream F02 Matrix/Edge or evaluation profile is superseded, when invalidation runs, then material current descendants become stale, unrelated objects stay current, and old history replays by hash. | Repository deletes the old portfolio or invalidates an unrelated campaign. | Invalidation graph and replay hashes; recovery. |
| AC-19 ownership | Given AIR candidate generation, when producer attempts to write Identity DNA, Reaction Receipt, Pipeline execution, VAE state, or independent-evaluation receipt, then boundary checks deny it. | One generic agent proposes, evaluates, promotes, and mutates source truth. | Boundary denial receipt; architecture. |
| AC-20 migration | Given the James V2 fixture, when migrated with complete attributable F01/F02/profile/stop evidence, then a new immutable V2.1 record cites original bytes/hash; absent meaning blocks rather than guesses. | Free-text stop reason or float is silently promoted. | Migration result and source attachment; migration. |
| AC-21 draft dependencies | Given either F01/F02 hash changes, when this spec advances, then revision-impact review is required for sections 3, 5, 6, 8, 9, and 10. | Receipt still claims the old interface while reading new bytes. | Draft-dependency receipt; lifecycle validation. |
| AC-22 claim ceiling | Given all local tests later pass while ratification is pending, when status is projected, then maximum state is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`, build remains false, and no Development Capsule is issued. | Status claims `ACCEPTED_FOR_BUILD` or production readiness. | Status-boundary test; architecture/governance. |

Every criterion requires both the positive path and the stated failure evidence. Passing schemas or synthetic examples cannot substitute for empirical model, real-human, external-product, production, or certification evidence.

## 10. Testing and completion evidence

### Exact future test paths and named suites

| Test path | Required cases |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_activation_hypothesis.py` | Closed fields, F01/F02 refs, planned epistemology, lock inheritance, Primitive applicability, repair refs. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_hypothesis_diversity.py` | Every governed axis, semantic duplicate, wording/seed denial, unsupported axis, pairwise proof. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_hypothesis_search_stopping.py` | All five reasons, reason-specific required/forbidden fields, no arbitrary default, no forced winner. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/serialization/test_f03_canonical_hash.py` | Key order, Unicode, tuple/set law, integer micros, timestamp exclusion, no time/random/path/environment drift. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_air_f03_schemas.py` | Positive, missing, extra, unknown-enum, bad-ref/hash, unjustified N/A, invalid stop, and promotion fixtures; model/schema parity. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_activation_hypothesis_portfolio.py` | AIR-FR-013 through AIR-FR-018 end-to-end and all Story terminal conditions. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f03_hard_gate_order.py` | No scoring before complete hard gates; exact failure reason and retained negative evidence. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f03_comparative_evaluation.py` | Independent identity, seven dimensions, profile hash, ambiguity, tie law, baseline/fallback/applicability. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f03_atomic_commit_and_idempotency.py` | Duplicate/conflicting duplicate, optimistic concurrency, every commit failure point, no orphan state. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f03_cancellation_and_late_results.py` | Pre/post-commit cancellation, late proposal/evaluation, superseded dependency, closed budget. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_f03_product_boundaries.py` | AIR/Interview/human/Pipeline/VAE/Delegation/Studio/evaluator ownership and compiler/runtime identity. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_v2_candidate_search_to_air_f03.py` | Exact source hashes, lexical-decimal conversion, missing meaning, free-text stop ambiguity, no current-state promotion. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/recovery/test_f03_replay_and_invalidation.py` | Selective invalidation, historical replay, journal recovery, rollback, and divergence receipt. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/clean_environment/test_f03_portability.py` | Two extracted layouts, fresh processes, changed locale/environment, no absolute path leakage. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_f02_f03_f04_handoff.py` | F02 rich-lineage intake, F03 complete portfolio output, F04 public-contract denial of stale/incomplete/provisional inputs. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/governance/test_f03_claim_ceiling.py` | Candidate authority label, technical-acceptance ceiling, build false, no capsule/production/certification. |

### Required fixtures and evidence

Future work must create valid and invalid schema fixtures for all six primary objects; exact F01/F02 dependency snapshots; the adapted James V2 fixture; strategic-difference and paraphrase-duplicate pairs; every hard-gate outcome including justified/unjustified `NOT_APPLICABLE`; decisive, ambiguous, shared-defect, exhausted-diversity, budget, and operator-ambiguity portfolios; repair chains; inherited-lock weakening; self-evaluation; stale refs; conflicting idempotency; concurrent updates; partial transaction failures; late results; selective invalidation; replay divergence; and migration blocks.

Completion evidence requires two fresh-process full-suite passes; Python source compilation/type checks; generated-schema/model parity; canonical-hash matrices; exact source and Primitive resolution; branch/property/failure-injection results under later governed thresholds; producer/evaluator identity proof; migration and compatibility report; clean extracted-layout report; reference-slice conformance; replay/invalidation report; and independent audit/re-audit receipts. No threshold is invented by this specification where Program Control has not governed one.

A future Build Receipt must cite the ratified/adopted authority hashes, independently accepted spec hash, bounded Development Capsule, exact implementation/test/schema/profile/model/harness hashes, dataset and evaluation lineage, applicability envelope, baseline/shadow result, fallback/rollback evidence, and maximum claim. This writer issues none of those artifacts.

Final writer state: `WRITTEN_PENDING_AUDIT`. The next lifecycle action is independent audit by a different agent. Candidate authority remains `CANDIDATE_NOT_CURRENT`; specification work is authorized; build authority and production eligibility remain false; pre-ratification acceptance cannot exceed `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
