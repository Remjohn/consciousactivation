# TS-INT-006 — Reaction Observation and Reaction Receipt Evidence

```yaml
spec_id: TS-INT-006
title: Reaction Observation and Reaction Receipt Evidence
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product_owner: Interview Expression
writing_wave: 6
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
controlling_frs:
  - AIR-FR-055
  - AIR-FR-056
  - AIR-FR-057
  - AIR-FR-058
  - AIR-FR-059
  - AIR-FR-060
controlling_stories:
  - AIR-ST-10.01
  - AIR-ST-10.02
  - AIR-ST-10.03
upstream_draft:
  spec_id: TS-INT-007
  path: 06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-007.md
  quality_state: WRITTEN_PENDING_AUDIT
  sha256: 98978c560ba216707fcc7d26305de1f2c42e9391f09db20aa4fc97a69fe08dbc
  label: DRAFT_DEPENDENCY_NOT_ACCEPTED
```

This candidate specification is authorized for technical writing and later independent review only. It grants no implementation, schema, contract-release, build, certification, publication, production, or Development Capsule authority. Interview Expression owns the observed human evidence and immutable Reaction Receipts defined here. Activative Intelligence Runtime (AIR) may consume exact eligible evidence and compile downstream semantic meaning; AIR may not manufacture, rewrite, or retroactively relabel the observed evidence.

## 1. Files and authorities read

### 1.1 Workflow, authority, path, and status inputs

All hashes below are SHA-256 of the exact bytes read.

| File | Bytes | SHA-256 | State and use |
|---|---:|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | 9,624 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Current V3.3 one-spec writer law |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_06_DISPATCH_LOCK.yaml` | 601 | `ca5fb43a1c7531f416683bad06e5e25e3842990f466e2d4444521ab537c09b3e` | Wave 6 path and upstream lock |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact `TS-INT-006` packet |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | 1,221 | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate state and claim ceiling |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | 1,462 | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Specification-work-only authority |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | 791 | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Current constitutional pointer |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | 40,830 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Highest current human-reaction and semantic-lineage authority |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | 4,289 | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Candidate product boundaries |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | 4,263 | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Candidate evidence and semantic ownership |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/PRODUCT_ROOT_REGISTRY.yaml` | 1,621 | `bb898168c770a09d0d6974c3ed347cf07b7770ccc41da094bb325c1777baa0be` | Reserved Interview Expression root; no implementation authority |

No `AGENTS.md` governs `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-006.md`. The recovery packet classifies it as `DIRECT_PRODUCT_SPEC_PATH` and allows no second specification or product artifact.

### 1.2 Reconciliation and controlling product inputs

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | 23,269 | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Canonical ID, title, owner, path, donor disposition |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | 104,516 | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | `AIR-FR-055`–`AIR-FR-060` primary ownership |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | 236,715 | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | FR → Story → `TS-INT-006` trace |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | 134,201 | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Current source classification |
| AIR bundle `prd/features/F10-reaction-observation-and-reaction-receipts.md` | 40,862 | `cec5bb822df7e63f6eb3d342bb0a19917948ed1f3b56d981f6140fa4ec748ab4` | Controlling candidate requirements |
| AIR bundle `planning/EPICS_AND_VERTICAL_STORIES.md` | 301,040 | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | `AIR-ST-10.01`–`AIR-ST-10.03` and CBAR mandates |
| AIR bundle `specs/TS-AIR-010-reaction-observation-and-reaction-receipts.md` | 28,018 | `3a23bb2035a331837f1f4b0877dff3ddd863353c1a3334a584d3b16f6d4ce070` | Full donor split and adapted to current owner |

The canonical ledger disposition is `SPLIT_FULL_DRAFT_DONOR`: the AIR-located donor supplies behavior and predecessor evidence, but the current candidate ownership ledger assigns Reaction Observations and Reaction Receipts to Interview Expression. Donor language saying AIR captures or manufactures observations is superseded by this split. AIR retains its own planned semantic objects and downstream compilation authority.

### 1.3 Exact upstream draft interface

| Draft | Bytes | SHA-256 | State | Interface consumed |
|---|---:|---|---|---|
| `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-007.md` | 90,725 | `98978c560ba216707fcc7d26305de1f2c42e9391f09db20aa4fc97a69fe08dbc` | `WRITTEN_PENDING_AUDIT`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Live session scope, evidence refs, exact delivered call, pressure decision, live observation signal, state snapshots/watermarks, command/event/receipt atomicity, post-terminal evidence, replay |

`TS-INT-007` is a draft interface, not ratified law. A change to its exact hash reopens this specification’s governing decisions; proposed architecture and workflows; data models, contracts, schemas, and APIs; failure/migration/rollback/recovery/observability; acceptance criteria; and testing/completion evidence.

### 1.4 Required unique evidence, candidate contracts, and brownfield

| File | Bytes | SHA-256 | Disposition |
|---|---:|---|---|
| AIR bundle `sources/ai_v2_predecessor/contracts/03_REACTION_OBSERVATION_AND_RECEIPT.md` (`SRC-AI2-REACTION-001`) | 519 | `491d08c9ee2c89bfb79a53eaca625eaf5fd77048680b909698e5424e597349f3` | `REQUIRED_UNIQUE_EVIDENCE`; adapt concrete signal and call-effect receipt concepts |
| AIR bundle `sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | 43,321 | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | `REQUIRED_UNIQUE_EVIDENCE`; source/reaction fidelity |
| AIR bundle `sources/doctrine/AHP_PRD_V1_1_SOURCE_FIRST.md` (`SRC-SOURCE-FIRST-001`) | 517,771 | `cc1cfa721238b999adb1612e805fad60c61c07c566df19d5044fc9e069651508` | `SUPERSEDED`; historical only, not current authority |
| AIR bundle `contracts/03_REACTION_OBSERVATION_AND_RECEIPT.md` | 519 | `491d08c9ee2c89bfb79a53eaca625eaf5fd77048680b909698e5424e597349f3` | Candidate contract seed; `ADAPT`, no release created |
| AIR bundle `contracts/schemas/reaction_observation.schema.json` | 2,083 | `1dc03420b167b7732c61a6656df8d071ba015c5926faeee3db4e0bffd2b182d3` | Candidate donor schema; `REPLACE_BY_ACCEPTED_TYPED_CONTRACT` later |
| AIR bundle `contracts/schemas/reaction_receipt.schema.json` | 5,467 | `f59a1b22020d37a9e27b172cf5066d2149a39233b4cf909f17933e7db0127a0f` | Candidate donor schema; `REPLACE_BY_ACCEPTED_TYPED_CONTRACT` later |
| AIR bundle `examples/03_julie_reaction_receipt.json` | 2,134 | `2a60f9093e3f0f55158bc2f6cf947fec013c7b14992cfe53d7242e4b613883ce` | Historical fixture input; does not prove current validity |
| AIR bundle `sources/ai_v2_predecessor/reference_implementation/models.py` | 24,677 | `f392c940349c3c5f9586a359fd8497ce1b8368de1b6654357deb146a686efd97` | `ADAPT`; strict-model evidence with incomplete lifecycle/ownership |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/expression_session.py` | 5,923 | `afce01302bb59f8b85b49bc12ea000ec74de8cd2f020707df6c6dd18e7ae316a` | `ADAPT`; session/receipt evidence with random/time-dependent identity |

### 1.5 Primitive evidence

| Primitive source | Bytes | SHA-256 | Bound use |
|---|---:|---|---|
| `EXP-FBK-001.yaml` — RIM Feedback Discipline | 6,981 | `ef888d832e745444a7fcf80192548f89a40abadc77e9653bd7c76ff966cae8ec` | Meaningful evidence feedback without vanity scores or interruptive spam |
| `PRM-PSY-001.yaml` — Matching Principle | 5,950 | `77c09b403aca66e77b2c71b1faa4dbeacd410d9d6c69685f9c2222dc65bf8ca7` | Conversation-layer evidence is preserved without diagnosis or performative matching |
| `PRM-VSG-021.yaml` — Punctum, Air, and Felt Truth | 8,179 | `06c75355f5f2bb083c09140e4af6994548e8d59fb544bf18553bc52966436cda` | Protect source-backed micro-expression/friction evidence without staging or manufacturing it |

Primitive sources are referenced by exact identity and applicability. Their summaries are not hard-coded substitutes for their bytes. Interview Expression records evidence under those constraints; AIR retains responsibility for compiling Primitive coalition and semantic implications.

No required source is missing. No unavailable optional source supports a factual claim in this specification.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem

A transcript is not a human reaction. An interview response can change through latency, silence, breath, vocal energy, laughter, gaze, posture, facial/body motion, hesitation, self-correction, contradiction, topic escape, defensive closure, recovery, landing, or a delayed reaction tail. Absence of a meaningful transition can itself be evidence. A weak implementation can:

- infer an Anchor Hit from fluent transcript wording while the person remains flat or defensive;
- call missing capture data an `ACTIVATION_NULL`;
- collapse directly observed, human-attested, model-inferred, hypothesized, contested, and resolved assertions;
- attribute an AIR-proposed call instead of the call actually delivered by the human;
- copy planned state/role/edge/route into the observed side of a delta;
- allow the call proposer or receipt compiler to self-evaluate;
- emit a receipt without exact source spans, reaction tail, counteractivation, uncertainty, or evaluator identity;
- turn an intense emotion into intended activation without proving outcome fit;
- overwrite a corrected observation and invalidate unrelated evidence; or
- let AIR, Pipeline, Studio, or a model manufacture the source observation to make downstream compilation pass.

These failures corrupt the evidence chain used to resolve Expression Moments and later semantic programs.

### 2.2 User and system outcome

An operator can inspect exactly what happened after an actual call or historical source interaction, distinguish reaction from inference and capture gaps, preserve null/partial/wrong reaction, and obtain an independently evaluated immutable Reaction Receipt. AIR and later consumers can use the receipt without rediscovering or rewriting the source evidence.

### 2.3 Bounded solution

Interview Expression SHALL implement an immutable `ReactionEvidenceCase` aggregate that:

1. binds an exact live delivered-call record or an evidence-bearing historical source trigger;
2. opens a governed pre-call/response/reaction-tail observation window;
3. aligns multimodal concrete observations to exact source spans;
4. records modality coverage and capture gaps distinctly from non-reaction;
5. proposes one typed reaction outcome and counteractivation assessment;
6. compares exact AIR-owned planned expectations with IE-owned observed evidence without changing either;
7. compiles an immutable Reaction Receipt candidate;
8. requires an independent evaluator to test evidence sufficiency, outcome fit, alternative interpretations, and maximum supported claim; and
9. publishes only an eligible evaluated receipt while preserving rejected, contested, null, partial, superseded, and invalidated evidence.

AIR may consume the resulting refs and evidence-bounded deltas. AIR cannot create or alter the observation stream, receipt outcome, evaluator verdict, source spans, or epistemic states.

### 2.4 In scope

- Live and post-session reaction evidence for Brief-led interviews.
- Historical/imported interview interaction triggers without invented live-call history.
- Exact verbal, vocal, temporal, visual, somatic, interactional, and technical observations.
- Reaction-tail capture and modality-coverage accounting.
- The governed outcome set: anchor hit, partial hit, unexpected edge, state transition, flat answer, defensive reaction, topic escape, silence, contradiction, landing reached, and activation null.
- Counteractivation evidence as a separate typed assessment.
- Immutable Reaction Receipts and independent evaluation receipts.
- Planned–observed evidence deltas that preserve planned and observed ownership.
- Field-level epistemic state, uncertainty, alternative interpretation, claim ceiling, and applicability.
- Commands, events, state machine, atomic persistence, idempotency, optimistic concurrency, replay, cancellation, correction, supersession, selective invalidation, and observability.
- Typed handoff to AIR, Expression Moment resolution, and the Canonical Interview Source Package after their own contract gates.

### 2.5 Out of scope and non-goals

- Selecting, generating, delivering, or changing an Activative Call. `TS-INT-007` records the call actually delivered; AIR owns proposal meaning.
- Executing the live interview loop, pressure decision, pause/reset/land/stop, or live-state projection.
- Creating or approving Expression Moments. A valid Reaction Receipt is required evidence, not automatic moment approval.
- Compiling an Observed Activative Intelligence Pack, Activation Contract, Primitive coalition, archetype, Matrix of Edging, Context Premise, Final Script, Visual Semantic Pack, Visual Narrative Program, or derivative route. AIR owns those semantics.
- Diagnosing a person, inferring personal truth, measuring clinical state, or treating facial/vocal signals as identity facts.
- Recommending the next semantic call or route. AIR may compile a policy from the evidence; IE may only expose operational blockers and evidence constraints.
- Creating generic creative-safety, legal-rights, content-rights, evaluator-certification, publication, production, or model-training approval authority.
- Naming a model/provider, score threshold, benchmark target, latency SLO, or confidence cutoff without governed evidence.
- Creating code, schemas, tests, generated types, release bytes, or capsules in this writing stage.

## 3. Governing decisions and constraints

### 3.1 Product sovereignty

1. Interview Expression owns `ReactionObservation`, `ReactionObservationStream`, `ReactionOutcomeEvidence`, `ReactionReceipt`, `PlannedObservedDeltaEvidence`, and `ReactionEvaluationReceipt` because they record what a human actually expressed and what the evidence supports.
2. AIR owns planned semantic objects, including expected state, psychological role inside tension, Matrix/edge hypotheses, planned route, Activative Call meaning, Primitive/archetype implications, and downstream semantic compilation.
3. IE may compare exact AIR-owned planned refs with observed evidence. The delta reports relation and evidence; it does not revise the planned object or compile a new AIR object.
4. AIR consumes exact current evaluated receipts. It may produce separately owned interpretations and programs with explicit references. It cannot backfill an observation, upgrade inference to observation, or replace an IE receipt with an AIR-local copy.
5. The call actually delivered, human pressure choice, live snapshot, and evidence watermark come from `TS-INT-007`; an AIR proposal is not proof of delivery.
6. Independent Evaluation owns the evaluator verdict as an evaluation artifact while IE owns the receipt lifecycle that applies the verdict. The evaluator and call proposer MUST have distinct implementation/actor identities; the producer cannot accept its own result.
7. Studio projects and sends typed review/resolution commands. Pipeline executes declared workflows. Delegation transports exact refs. VAE owns visual production. None becomes the source-evidence owner.
8. `Activative Contract Compiler != Activative Intelligence Runtime`, and neither equals Interview Expression.

### 3.2 Observation, interpretation, and human truth

Each material assertion has one epistemic state:

- `DIRECTLY_OBSERVED`
- `HUMAN_ATTESTED`
- `MODEL_INFERRED`
- `HYPOTHESIZED`
- `CONTESTED`
- `RESOLVED`
- `REJECTED`
- `SUPERSEDED`
- evidence-bearing `UNKNOWN`
- evidence-bearing `NOT_APPLICABLE`

An observation record contains a concrete signal. Interpretation is a separate assertion linked to observations. A model output cannot be submitted as a directly observed or human-attested fact. Human resolution adds provenance and lifecycle; it does not erase the original evidence or magically change a machine inference into direct observation.

No reaction type is a diagnosis. `DEFENSIVE_REACTION`, `TOPIC_ESCAPE`, `CONTRADICTION`, and `COUNTERACTIVATION` are evidence-bounded interaction outcomes, not fixed claims about identity or intent.

### 3.3 Multimodal sufficiency

The observation stream declares coverage for every modality required by its profile. “Available” means exact source evidence exists and was inspected under the declared method. “Not captured,” “corrupt,” “restricted,” “not applicable,” and “not yet processed” are distinct typed states.

Transcript text alone is insufficient when other governed modalities are available and material to the claimed outcome. Conversely, a missing optional modality does not force fabrication. The evaluator sets a maximum claim from actual coverage.

### 3.4 Non-reaction versus missing evidence

`ACTIVATION_NULL` and `PARTIAL_HIT` are positive evidence classifications, not default fallbacks. They require a complete governed reaction window, sufficient coverage, and evidence that no intended meaningful transition or only a partial transition occurred.

If capture failed, the correct state is `EVIDENCE_GAP`, `OBSERVATION_INCOMPLETE`, or `INDETERMINATE`, not `ACTIVATION_NULL`. Silence is an outcome only when source timing proves a silence event and context supports that bounded classification; missing audio is not silence.

### 3.5 Outcome and counteractivation separation

The closed reaction outcome vocabulary is:

`ANCHOR_HIT`, `PARTIAL_HIT`, `UNEXPECTED_EDGE`, `STATE_TRANSITION`, `FLAT_ANSWER`, `DEFENSIVE_REACTION`, `TOPIC_ESCAPE`, `SILENCE`, `CONTRADICTION`, `LANDING_REACHED`, `ACTIVATION_NULL`.

Operational failures such as capture loss, evaluator outage, or operator interruption are not reaction outcomes. They are typed case failures/states. Counteractivation is a separately evidenced assessment because multiple outcomes can contain counteractivation evidence. This prevents one enum from collapsing outcome, process failure, and semantic interpretation.

### 3.6 Trigger fidelity

For a live session, a receipt binds the exact `DeliveredActivativeCallRecord`, pressure decision, pre-call live snapshot, and event watermark. An AIR call option alone is invalid.

For an imported source with no trustworthy live-call record, `HistoricalSourceTrigger` binds an exact prompt/question/interaction source span and declares `LIVE_CALL_RECORD_NOT_AVAILABLE_FOR_IMPORTED_SOURCE`. It MUST NOT invent an IAC, call ID, pressure choice, pre-state, or AIR proposal. The maximum claim reflects the missing live context.

### 3.7 Primitive and CBAR constraints

- `EXP-FBK-001`: immediate feedback may expose capture state and evidence gaps, but speed never justifies a premature outcome or vanity score.
- `PRM-PSY-001`: conversation-layer evidence is recorded and may bound alternatives; it does not authorize psychological diagnosis or performative labeling.
- `PRM-VSG-021`: lived-in micro-expression and source friction remain visible, while manufactured messiness, beauty/polish bias, and distracting technical failure do not become felt-truth claims.

Exact Primitive applicability, suppression, misuse, conflict, and binding refs are preserved. AIR compiles coalition meaning; IE does not replace the registry with prose.

### 3.8 Canonicalization, portability, and atomicity

- Canonical records use governed UTF-8 JSON, Unicode normalization, sorted object keys, explicit list order, sorted-set normalization, integer/rational source coordinates, stable enums, and no insignificant whitespace.
- Canonical identity does not depend on current time, random state, dictionary insertion, filesystem traversal, machine path, hostname, process environment, locale, timezone, or model callback order.
- Wall-clock metadata is nonidentity unless the authority explicitly declares it semantic. Session logical order and source time are canonical.
- Portable refs prohibit drive paths, UNC paths, `file://`, traversal, unresolved checkout roots, or process-local addresses.
- Commands, events, aggregate state, observations, receipts, dependency edges, idempotency result, invalidation, and outbox intent commit atomically.
- A duplicate idempotency key with identical canonical command bytes returns the original result. Changed bytes under that key fail.
- State-changing commands require exact expected case version/hash and relevant live-session watermark.

### 3.9 Claim ceiling and forbidden behavior

This document remains `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, and not build-ready. Package/schema parsing, local tests, model output, or an evaluation receipt cannot imply real-human validation, evaluator certification, product certification, publication, production, or build authorization.

Forbidden behaviors include manufacturing a reaction, defaulting missing evidence to positive outcome, self-evaluation, overwriting history, flattening provenance into notes, importing superseded doctrine as current, silently replacing a model/profile, AIR-local evidence forks, and automatic Expression Moment promotion.

## 4. Current brownfield architecture

### 4.1 AIR-located donor specification

`TS-AIR-010` usefully enumerates Reaction Observation, stream, outcome, receipt, planned–observed delta, evaluation, lifecycle, replay, and Primitive evidence. It targets AIR-owned implementation paths and sometimes describes AIR as the producer of source evidence.

Disposition: `SPLIT_AND_ADAPT`. Keep the behavior requirements and evidence discipline; retarget canonical evidence ownership and future paths to Interview Expression. AIR becomes a consumer and semantic compiler, not the observation author.

### 4.2 Candidate predecessor contract

The 519-byte predecessor contract establishes two durable ideas: one concrete source-linked observation carries modality/span/value/confidence/optional interpretation, and one receipt resolves the effect of one Activative Call with pre/post state, observations, outcome, anchor status, operator resolution, and next action. It also states null reaction is valid.

Disposition: `ADAPT`. Separate observation from interpretation; replace generic confidence, pre/post narrative state, next-action recommendation, and optional nulls with governed typed refs, evidence coverage, evaluation, and ownership. Next semantic action belongs to AIR/human policy, not the IE receipt.

### 4.3 Candidate schemas and example

The candidate schemas use strict additional-property rejection and exact refs, but contain gaps:

- optional millisecond times cannot distinguish instant observation, missing timing, and inapplicability;
- `inferred_interpretations` are untyped strings embedded inside observations;
- confidence is a bare float without scale/calibration/profile;
- owner, live watermark, speaker, modality coverage, reaction tail, counteractivation, evaluator identity, alternative interpretations, maximum claim, lifecycle, and supersession are absent;
- generic `NarrativeState`, `anchor_status`, interpretation, and next-action strings collapse AIR/IE boundaries;
- `created_at` is mixed into the receipt without declared identity treatment; and
- arrays do not establish canonical order or nonempty evidence rules.

The Julie example demonstrates source-linked temporal and lexical observations, but it embeds inference in observations and a next-action recommendation, uses nullable resolution, and does not prove independent evaluation or current ownership.

Disposition: `REPLACE_BY_ACCEPTED_TYPED_CONTRACT` after ratification/adoption. Preserve as migration fixtures and historical evidence; do not edit them in place.

### 4.4 AI2 predecessor models

The predecessor model uses strict validation, enumerated outcomes, exact refs, immutable-looking tuples, and time-range validation. It lacks the required event/receipt atomicity, field-level provenance, complete multimodal coverage, evaluator separation, and owner split. It uses datetime fields and weak optional/default collections that can collapse absence.

Disposition: `ADAPT_DOMAIN_IDEAS`; no source reuse without a later capsule and field-by-field migration proof.

### 4.5 Studio expression-session contract

The Studio contract provides useful organization/brand/session scope, state enums, typed status events, source configuration, quality gates, and start receipts. It generates UUIDs and wall-clock times inside constructors and does not define Reaction Observations or Receipts.

Disposition: `ADAPT_SCOPE_AND_PROJECTION_ONLY`. Studio remains a projection/command product. Random/time-dependent constructors cannot determine canonical reaction-evidence identity.

### 4.6 Source-first predecessor

`SRC-SOURCE-FIRST-001` is preserved historical input but is explicitly `SUPERSEDED`. It supplies no current authority claim. Current Constitution and candidate V2.1 ownership/requirements take precedence.

### 4.7 Current target repository state

The intended Interview Expression product root has candidate specifications but no authorized reaction-evidence source tree. There is no current implementation, repository, schema, evaluator, test, worker, or release to reuse at the target path.

Disposition: `ACTIVATE_AFTER_RATIFICATION_AND_SEPARATE_BUILD_AUTHORITY`. Section 7 reserves future paths only.

## 5. Proposed architecture and workflows

### 5.1 Components

1. **ReactionEvidenceAdmissionService** — resolves exact source/session/trigger/authority/profile inputs and freezes an input manifest.
2. **ReactionWindowService** — opens and closes exact baseline, delivered-call, response, and reaction-tail ranges.
3. **ReactionObservationService** — records concrete observations and separate interpretation assertions with epistemic state.
4. **ModalityCoverageEvaluator** — proves available/inspected/missing/restricted/inapplicable status per modality.
5. **ReactionOutcomeClassifierPort** — proposes an evidence-bounded outcome; it has no acceptance authority.
6. **PlannedObservedDeltaService** — compares exact AIR planned assertions against IE observations without copying ownership.
7. **ReactionReceiptCompiler** — compiles an immutable candidate from exact refs and deterministic gates.
8. **IndependentReactionEvaluatorPort** — tests evidence sufficiency, outcome fit, alternatives, Primitive/CBAR constraints, and maximum supported claim.
9. **ReactionReceiptLifecycleService** — applies evaluator/human decisions, supersession, invalidation, and publication eligibility.
10. **ReactionEvidenceRepositoryPort** — atomically stores commands, state, observations, events, receipts, evaluations, dependencies, idempotency, invalidations, and outbox.
11. **LiveStateEvidenceGateway** — consumes exact `TS-INT-007` calls, snapshots, watermarks, and signals without mutating live history.
12. **AIRReactionEvidenceGateway** — exposes exact eligible receipts read-only; AIR interpretations remain separate AIR-owned artifacts.
13. **SourcePackageReactionBindingPort** — requests later binding of current receipt refs under the adopted source-package contract.
14. **ReactionEvidenceQueryPort** — retrieves exact current/historical versions, evidence spans, evaluations, and descendants.

### 5.2 Live reaction-capture workflow

1. `OpenReactionEvidenceCase` supplies exact tenant/source/session, delivered-call ref, pressure-decision ref, pre-call snapshot, live event watermark, authority, profiles, idempotency key, and expected state.
2. Admission resolves the delivered call and proves it was committed. It rejects an AIR proposal presented as actual delivery.
3. The service opens a `ReactionWindow` with baseline, call, response, and reaction-tail phases. Phase durations/rules come from immutable profiles; no threshold is invented here.
4. `AppendReactionObservation` adds concrete source-linked signals. `AppendReactionInterpretationAssertion` records interpretations separately.
5. `CloseReactionWindow` freezes exact source ranges and produces modality coverage. Missing required evidence produces a gap state, not a reaction outcome.
6. `ProposeReactionOutcome` receives the closed stream and emits one outcome proposal, counteractivation assessment, alternatives, and governed scores.
7. Deterministic gates validate source/span/session/watermark/coverage, enum legality, epistemic consistency, and claim ceiling.
8. `ComputePlannedObservedDelta` compares exact planned expectation refs with observed evidence relations.
9. `CompileReactionReceiptCandidate` creates an immutable candidate in `EVALUATION_REQUIRED`.
10. A distinct evaluator issues `ReactionEvaluationReceipt` with verdict and maximum supported claim.
11. `ApplyReactionEvaluation` moves the candidate to `VALIDATED`, `REJECTED`, `CONTESTED`, or `NEEDS_MORE_EVIDENCE`. A validated receipt becomes eligible for downstream use; this does not create an Expression Moment.

### 5.3 Imported/historical reaction workflow

An imported interview may not have a trustworthy live call, pressure decision, or pre-call snapshot. `OpenHistoricalReactionEvidenceCase` requires:

- exact source package and source kind;
- exact prompt/question/interaction span where identifiable;
- exact response and reaction-tail spans;
- speaker refs;
- a planning/call availability declaration; and
- operator source authority and evidence coverage.

The trigger state is `HISTORICAL_SOURCE_TRIGGER`; live-call fields are evidence-bearing `NOT_APPLICABLE` with reason `LIVE_CALL_RECORD_NOT_AVAILABLE_FOR_IMPORTED_SOURCE`. The workflow cannot fabricate an IAC, call, planned state, or pressure dose. Planned–observed dimensions unavailable in history become evidence-bearing `NOT_APPLICABLE` or `INDETERMINATE`, lowering the maximum claim rather than blocking preservation of valid observed evidence.

### 5.4 Observation alignment workflow

Observations may reference:

- transcript word/phrase/speaker spans;
- silence and audio-event spans;
- vocal properties and changes;
- exact visual/keyframe or recording intervals;
- gaze/posture/facial/body behavior with method provenance;
- self-correction, contradiction, topic escape, and response continuity;
- direct operator/human attestation; and
- reaction-tail evidence after the apparent answer ends.

Each observation identifies modality, source selector, observed typed value, observer/method, epistemic state, governed score if any, uncertainty, sensitivity, and lifecycle. A model may propose an interpretation but cannot change the observation’s owner or epistemic state.

### 5.5 Outcome classification workflow

The classifier receives a closed observation stream and returns a candidate, never acceptance. Deterministic validation ensures:

- exactly one primary governed outcome;
- evidence refs support the requested outcome;
- a `SILENCE` outcome points to observed silence rather than missing audio;
- `ACTIVATION_NULL` and `PARTIAL_HIT` meet coverage and window requirements;
- `ANCHOR_HIT` cannot derive from call delivery or transcript fluency alone;
- intense affect is not automatically intended activation;
- counteractivation is separately evidenced;
- alternative interpretations remain present; and
- operational failures do not appear as human reaction outcomes.

### 5.6 Planned–observed delta workflow

AIR supplies exact planned assertion refs for dimensions such as expected state, psychological role, edge, and asset-route hypothesis. IE does not duplicate them as editable fields. For each dimension it records one relation:

`SUPPORTED_BY_OBSERVATION`, `PARTIALLY_SUPPORTED`, `DIVERGED`, `UNEXPECTED_OBSERVED`, `NOT_OBSERVED_WITH_SUFFICIENT_COVERAGE`, `INDETERMINATE_EVIDENCE_GAP`, or `NOT_APPLICABLE_WITH_EVIDENCE`.

Every relation points to exact planned and observed evidence refs and states its maximum claim. A mismatch is preserved, not repaired by changing either side. AIR may later compile the semantic implication in a separately owned object.

### 5.7 Independent evaluation workflow

`EvaluateReactionReceiptCandidate` verifies evaluator independence from the call proposer and receipt producer, then evaluates:

- source and trigger integrity;
- window and modality coverage;
- observation/interpretation separation;
- outcome fit and null/partial evidence;
- counteractivation evidence;
- planned–observed relation accuracy;
- alternative interpretations and missing evidence;
- Primitive/CBAR applicability and misuse risk;
- source-authority scope; and
- maximum supported claim.

Verdicts are `VALIDATED`, `REJECTED`, `CONTESTED`, or `NEEDS_MORE_EVIDENCE`. A bare numeric score cannot decide. Disagreement is preserved; a later human resolution is an additive typed command and cannot erase the evaluator record.

### 5.8 Correction, late evidence, and supersession

`CorrectReactionObservation`, `AttachLateReactionEvidence`, `SupersedeOutcomeProposal`, and `ResolveReactionReceiptContest` always create successor records. Late post-terminal evidence is allowed only through the governed `TS-INT-007` post-terminal evidence interface or a reconciled successor; it never reopens the historical live session.

Any changed observation reopens affected outcome, delta, receipt, and evaluation descendants. Unrelated reaction cases and source spans remain valid when dependency evidence proves independence.

### 5.9 Downstream handoff

- Expression Moment resolution receives only exact eligible Reaction Receipt refs and remains responsible for complete premise/reaction-tail/context and approval.
- The Canonical Interview Source Package may bind a set of current receipt refs under its own immutable successor-version rules.
- AIR receives a read-only receipt/delta view. It may compile Observed Activative Intelligence and subsequent programs but cannot alter the IE evidence.
- Pipeline pins exact accepted versions for execution. VAE receives only downstream visual demands. Studio reads projections and sends typed commands. Delegation transports versioned refs/receipts.

Production acceptance, source-package binding, AIR consumption acknowledgement, and Expression Moment approval remain distinct lifecycle events.

### 5.10 State machine

`ReactionEvidenceCase` states:

`OPEN` → `CAPTURING` → `WINDOW_CLOSED` → (`EVIDENCE_INCOMPLETE` | `OUTCOME_PROPOSED`) → `DELTA_COMPUTED` → `RECEIPT_CANDIDATE` → `EVALUATION_REQUIRED` → (`VALIDATED` | `REJECTED` | `CONTESTED` | `NEEDS_MORE_EVIDENCE`).

Side/terminal states are `CANCELLED`, `FAILED`, `SUPERSEDED`, and `INVALIDATED`. `NEEDS_MORE_EVIDENCE` may accept a successor evidence command; no state mutates prior bytes. A validated receipt can later be superseded or invalidated but remains historically replayable.

### 5.11 Idempotency, concurrency, replay, and cancellation

Commands use exact case version/hash and, for live work, session sequence/watermark. Stale commands fail rather than retarget. Replay resolves the exact historical live record, source bytes, profiles, observations, decisions, and evaluation artifacts.

Cancellation checks occur before expensive proposal/evaluation work and before commit. A late result after cancellation is quarantined/noncanonical. If commit wins the race, cancellation becomes a successor lifecycle event; ordering is receipt-backed.

## 6. Data models, contracts, schemas, and APIs

These are normative logical contracts. No schema/release bytes are created by this prompt.

### 6.1 Common refs, source selectors, and governed scores

```text
ImmutableRef {
  object_type: governed identifier
  object_id: non-empty identifier
  version: positive integer or governed semantic version
  sha256: lowercase 64-hex digest
  owner_product: governed product identifier
  lifecycle_state_at_use: governed enum
}

SourceSelector =
  TranscriptSpanSelector { transcript_ref, speaker_ref, start_word_ordinal, end_word_ordinal_exclusive }
| RecordingTimeSelector { media_ref, stream_index, start_ticks, end_ticks_exclusive, rational_timebase }
| FrameRangeSelector { visual_index_ref, first_frame_ref, end_frame_ordinal_exclusive }
| EventSequenceSelector { live_session_ref, start_sequence, end_sequence_inclusive, event_watermark }
| AttestationSelector { actor_assertion_ref, attested_event_ref }

GovernedScore {
  value: canonical decimal string
  scale_id: governed identifier
  calibration_profile_ref: ImmutableRef
  interpretation: governed band or evidence-bearing NOT_APPLICABLE
}
```

A bare float, raw local path, or selector without an exact source/version is invalid.

### 6.2 Reaction trigger

```text
ReactionTrigger =
  DeliveredCallTrigger {
    kind: LIVE_DELIVERED_CALL
    live_session_ref: ImmutableRef
    delivered_call_ref: ImmutableRef
    pressure_decision_ref: ImmutableRef
    pre_call_snapshot_ref: ImmutableRef
    post_call_snapshot_ref: ImmutableRef | EvidenceBearingNotApplicable
    event_watermark: sha256
    call_delivery_evidence_refs: canonical ordered ImmutableRef[]
  }
| HistoricalSourceTrigger {
    kind: HISTORICAL_SOURCE_TRIGGER
    source_package_ref: ImmutableRef
    interaction_span_ref: ImmutableRef
    speaker_refs: non-empty canonical ordered ImmutableRef[]
    live_call_record: EvidenceBearingNotApplicable(reason=LIVE_CALL_RECORD_NOT_AVAILABLE_FOR_IMPORTED_SOURCE)
    planning_availability: PRESENT_BY_EXACT_REF | ABSENT_NOT_CREATED | UNKNOWN_BLOCKING_DELTA
  }
```

Live mode forbids missing delivered-call evidence. Historical mode forbids fake call IDs and planned refs.

### 6.3 Reaction window and modality coverage

```text
ReactionWindow {
  window_id: deterministic identifier
  trigger_ref: ImmutableRef
  baseline_range: SourceSelector | EvidenceBearingNotApplicable
  call_or_interaction_range: SourceSelector
  response_range: SourceSelector
  reaction_tail_range: SourceSelector
  window_profile_ref: ImmutableRef
  source_continuity_receipt_ref: ImmutableRef
  lifecycle_state: OPEN | CLOSED | SUPERSEDED | INVALIDATED
}

ModalityCoverage {
  modality: LEXICAL | VOCAL | TEMPORAL | VISUAL | SOMATIC | INTERACTIONAL | TECHNICAL
  availability: AVAILABLE | NOT_CAPTURED | CORRUPT | RESTRICTED | NOT_PROCESSED | NOT_APPLICABLE
  inspected_ranges: canonical ordered SourceSelector[]
  method_profile_ref: ImmutableRef | EvidenceBearingNotApplicable
  evidence_refs: canonical ordered ImmutableRef[]
  effect_on_claim: NONE | LIMITS_CLAIM | BLOCKS_OUTCOME | BLOCKS_RECEIPT
}
```

`NOT_APPLICABLE` requires policy, decision actor/method, reason, and evidence. Empty arrays or nulls do not substitute.

### 6.4 Reaction observation and interpretation

```text
ReactionObservation {
  observation_id: deterministic identifier
  version: positive integer
  case_ref: ImmutableRef
  window_ref: ImmutableRef
  modality: governed modality enum
  observation_kind: TRANSCRIPT_CONTENT | WORD_TIMING | SILENCE_EVENT | AUDIO_EVENT | VOCAL_CHANGE |
                    FACIAL_BEHAVIOR | BODY_BEHAVIOR | GAZE_BEHAVIOR | POSTURE_BEHAVIOR |
                    SELF_CORRECTION | CONTRADICTION | TOPIC_SHIFT | RESPONSE_LATENCY |
                    REACTION_TAIL | CAPTURE_CONDITION | OTHER_GOVERNED
  source_selectors: non-empty canonical ordered SourceSelector[]
  observed_value: closed typed union owned by observation_kind
  epistemic_state: DIRECTLY_OBSERVED | HUMAN_ATTESTED | MODEL_INFERRED | CONTESTED | RESOLVED
  observer_or_method_ref: ImmutableRef
  confidence: GovernedScore | EvidenceBearingNotApplicable
  uncertainty_codes: canonical governed set
  sensitivity_class: governed value
  lifecycle_state: CURRENT | SUPERSEDED | REJECTED | INVALIDATED
  supersedes: ImmutableRef | EvidenceBearingNotApplicable
  content_sha256: sha256
}

ReactionInterpretationAssertion {
  assertion_id: deterministic identifier
  observation_refs: non-empty canonical ordered ImmutableRef[]
  claim_kind: governed non-diagnostic kind
  bounded_claim: typed value
  epistemic_state: MODEL_INFERRED | HYPOTHESIZED | HUMAN_ATTESTED | CONTESTED | RESOLVED | REJECTED
  asserting_actor_or_system_ref: ImmutableRef
  alternative_assertion_refs: canonical ordered ImmutableRef[]
  maximum_claim_profile_ref: ImmutableRef
  lifecycle_state: CURRENT | SUPERSEDED | REJECTED | INVALIDATED
}
```

Direct observation and interpretation cannot share one free-text field. Model inference cannot claim `DIRECTLY_OBSERVED`.

### 6.5 Observation stream

```text
ReactionObservationStream {
  stream_id: deterministic identifier
  version: positive integer
  case_ref: ImmutableRef
  trigger_ref: ImmutableRef
  reaction_window_ref: ImmutableRef
  observation_refs: non-empty source-time ordered ImmutableRef[]
  interpretation_assertion_refs: canonical ordered ImmutableRef[]
  modality_coverage: canonical map[modality, ModalityCoverage]
  source_package_ref: ImmutableRef
  live_session_watermark: sha256 | EvidenceBearingNotApplicable
  closure_command_ref: ImmutableRef
  stream_state: OPEN | CLOSED | INCOMPLETE | SUPERSEDED | INVALIDATED
  supersedes: ImmutableRef | EvidenceBearingNotApplicable
  stream_sha256: sha256
}
```

The stream is ordered by exact source coordinates plus deterministic tie-breaker. Filesystem or callback ordering is forbidden.

### 6.6 Outcome and counteractivation

```text
ReactionOutcomeEvidence {
  outcome_id: deterministic identifier
  stream_ref: ImmutableRef
  outcome: ANCHOR_HIT | PARTIAL_HIT | UNEXPECTED_EDGE | STATE_TRANSITION | FLAT_ANSWER |
           DEFENSIVE_REACTION | TOPIC_ESCAPE | SILENCE | CONTRADICTION | LANDING_REACHED |
           ACTIVATION_NULL
  supporting_observation_refs: non-empty canonical ordered ImmutableRef[]
  contradicting_observation_refs: canonical ordered ImmutableRef[]
  interpretation_assertion_refs: canonical ordered ImmutableRef[]
  outcome_confidence: GovernedScore
  uncertainty_codes: canonical governed set
  alternative_outcomes: canonical ordered AlternativeOutcome[]
  proposal_profile_ref: ImmutableRef
  proposed_by: ImmutableRef
  state: PROPOSED | REJECTED | SUPERSEDED | INVALIDATED
}

CounteractivationAssessment {
  assessment_id: deterministic identifier
  state: NONE_OBSERVED | DEFENSIVE_CLOSURE | TOPIC_ESCAPE | RELATIONAL_WITHDRAWAL |
         PRESSURE_MISMATCH | OTHER_EVIDENCED | INDETERMINATE
  evidence_refs: canonical ordered ImmutableRef[]
  interpretation_refs: canonical ordered ImmutableRef[]
  uncertainty_codes: canonical governed set
}
```

An outcome is never accepted solely because its score is highest.

### 6.7 Planned–observed delta evidence

```text
PlannedObservedDimensionDelta {
  dimension: EXPECTED_STATE | PSYCHOLOGICAL_ROLE | EDGE | ASSET_ROUTE
  planned_assertion_ref: ImmutableRef | EvidenceBearingNotApplicable
  observed_evidence_refs: canonical ordered ImmutableRef[]
  relation: SUPPORTED_BY_OBSERVATION | PARTIALLY_SUPPORTED | DIVERGED | UNEXPECTED_OBSERVED |
            NOT_OBSERVED_WITH_SUFFICIENT_COVERAGE | INDETERMINATE_EVIDENCE_GAP |
            NOT_APPLICABLE_WITH_EVIDENCE
  relation_evidence_refs: canonical ordered ImmutableRef[]
  maximum_supported_claim: governed value
  epistemic_state: OBSERVED_COMPARISON | CONTESTED | RESOLVED
}

PlannedObservedDeltaEvidence {
  delta_id: deterministic identifier
  trigger_ref: ImmutableRef
  air_planned_object_refs: canonical ordered ImmutableRef[]
  dimensions: canonical map[dimension, PlannedObservedDimensionDelta]
  compiled_by_interview_expression: true
  semantic_interpretation_owner: ACTIVATIVE_INTELLIGENCE_RUNTIME
  supersedes: ImmutableRef | EvidenceBearingNotApplicable
  delta_sha256: sha256
}
```

IE owns the evidence comparison record. AIR owns what the relation means for later semantic compilation. Neither side mutates the other.

### 6.8 Reaction Receipt

```text
ReactionReceipt {
  receipt_id: deterministic identifier
  version: positive integer
  case_ref: ImmutableRef
  trigger_ref: ImmutableRef
  source_package_ref: ImmutableRef
  reaction_window_ref: ImmutableRef
  observation_stream_ref: ImmutableRef
  outcome_ref: ImmutableRef
  counteractivation_assessment_ref: ImmutableRef
  planned_observed_delta_ref: ImmutableRef
  source_span_refs: non-empty canonical ordered ImmutableRef[]
  primitive_binding_refs: canonical ordered ImmutableRef[]
  evaluator_receipt_ref: ImmutableRef | EvidenceBearingNotApplicable
  receipt_state: CANDIDATE | EVALUATION_REQUIRED | VALIDATED | REJECTED | CONTESTED |
                 NEEDS_MORE_EVIDENCE | SUPERSEDED | INVALIDATED
  maximum_supported_claim: governed claim enum
  downstream_constraints: canonical governed set
  operator_resolution_ref: ImmutableRef | EvidenceBearingNotApplicable
  dependency_edges: canonical ordered DependencyEdge[]
  supersedes: ImmutableRef | EvidenceBearingNotApplicable
  content_sha256: sha256
}
```

`downstream_constraints` may say `NO_EXPRESSION_MOMENT_PROMOTION`, `REVIEW_REQUIRED`, `SOURCE_SCOPE_RESTRICTED`, or `EVIDENCE_GAP`. It does not recommend the next semantic call or route.

### 6.9 Independent evaluation receipt

```text
ReactionEvaluationReceipt {
  evaluation_receipt_id: deterministic identifier
  reaction_receipt_candidate_ref: ImmutableRef
  evaluator_actor_or_program_ref: ImmutableRef
  call_proposer_ref: ImmutableRef | EvidenceBearingNotApplicable
  receipt_compiler_ref: ImmutableRef
  independence_check: PASS | FAIL
  evidence_sufficiency: PASS | FAIL | INDETERMINATE
  outcome_fit: PASS | FAIL | CONTESTED
  alternative_interpretation_refs: canonical ordered ImmutableRef[]
  primitive_cbar_checks: canonical ordered CheckResult[]
  source_authority_check: PASS | FAIL
  maximum_supported_claim: governed claim enum
  verdict: VALIDATED | REJECTED | CONTESTED | NEEDS_MORE_EVIDENCE
  failure_refs: canonical ordered ImmutableRef[]
  evaluation_profile_ref: ImmutableRef
  content_sha256: sha256
}
```

The evaluator cannot be the call proposer. A profile may additionally require separation from the receipt compiler; this specification requires it for final validation. Capability presence does not imply evaluator certification.

### 6.10 Aggregate, commands, events, repository, and APIs

```text
ReactionEvidenceCase {
  case_id: deterministic identifier
  version: positive integer
  tenant_scope: exact organization/brand/source scope
  trigger_ref: ImmutableRef
  current_window_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_stream_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_outcome_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_delta_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_reaction_receipt_ref: ImmutableRef | EvidenceBearingNotApplicable
  state: governed case state
  expected_live_watermark: sha256 | EvidenceBearingNotApplicable
  supersedes: ImmutableRef | EvidenceBearingNotApplicable
  case_sha256: sha256
}
```

Normative commands:

- `OpenReactionEvidenceCase`
- `OpenHistoricalReactionEvidenceCase`
- `AppendReactionObservation`
- `AppendReactionInterpretationAssertion`
- `CloseReactionWindow`
- `ProposeReactionOutcome`
- `ComputePlannedObservedDelta`
- `CompileReactionReceiptCandidate`
- `EvaluateReactionReceiptCandidate`
- `ApplyReactionEvaluation`
- `CorrectReactionObservation`
- `AttachLateReactionEvidence`
- `ResolveReactionReceiptContest`
- `SupersedeReactionReceipt`
- `InvalidateReactionEvidenceDescendants`
- `CancelReactionEvidenceCase`

Each uses the adopted `TS-INT-007` command envelope or a reconciled successor: command/schema ID, idempotency key, tenant/session/source scope, actor assertion, expected case version/hash, expected live watermark when applicable, logical time, canonical payload, and authorization decision.

Normative events mirror successful transitions and include `ReactionEvidenceCaseOpened`, `ReactionObservationAppended`, `ReactionInterpretationAppended`, `ReactionWindowClosed`, `ReactionOutcomeProposed`, `PlannedObservedDeltaComputed`, `ReactionReceiptCandidateCompiled`, `ReactionReceiptEvaluated`, `ReactionEvaluationApplied`, `ReactionObservationCorrected`, `LateReactionEvidenceAttached`, `ReactionReceiptContested`, `ReactionReceiptValidated`, `ReactionReceiptRejected`, `ReactionReceiptSuperseded`, `ReactionEvidenceDescendantsInvalidated`, and `ReactionEvidenceCaseCancelled`.

The repository MUST atomically compare-and-append command record, events, aggregate version, observations, receipts, evaluation, dependencies, idempotency, invalidations, and outbox. It rejects state without receipt, receipt without evidence, event without command, evaluator result without candidate, success receipt without artifacts, or version/watermark mismatch.

Logical read APIs:

- `get_reaction_case(case_id, version, sha256)`
- `get_reaction_observation(observation_id, version, sha256)`
- `list_reaction_stream(stream_ref, modality, source_range, cursor)`
- `get_reaction_receipt(receipt_id, version, sha256)`
- `get_reaction_evaluation(receipt_ref)`
- `list_reaction_receipt_descendants(exact_ref, edge_type, cursor)`
- `verify_reaction_case_replay(case_ref)`
- `get_air_consumption_view(receipt_ref, compatibility_profile_id)`

Exact reads never substitute latest.

### 6.11 Compatibility and invalid examples

Compatibility requires preservation of source selectors, modality coverage, epistemic states, outcome, uncertainty, alternatives, evaluator independence, planned/observed ownership, lifecycle, source authority, and invalidation. Parsing-only support fails.

Invalid examples:

- `{ "text": "That landed", "outcome": "anchor_hit" }` — transcript assertion without source, multimodal coverage, trigger, tail, evaluator, or uncertainty.
- `{ "outcome": "activation_null", "audio": null }` — cannot distinguish observed non-reaction from missing capture.
- `{ "confidence": 0.92 }` — no scale, calibration, profile, or meaning.
- `{ "planned_role": "challenger", "observed_role": "challenger" }` — unowned copied semantics without exact refs/evidence relation.
- `{ "call_id": "main-question" }` for imported source — fabricated live history.
- a receipt whose evaluator is the call proposer or compiler — fails independence.
- an AIR-local “normalized receipt” that drops IE lifecycle/provenance — forbidden fork.

## 7. Implementation stages and exact target paths

The following are proposed future paths under a separately authorized build. This writing task creates none of them.

### 7.1 Domain and canonicalization

- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/models.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/source_selectors.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/observations.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/outcomes.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/planned_observed_delta.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/commands.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/events.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/receipts.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/canonicalization.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/errors.py`

Implement immutable unions, exact selectors, epistemic states, modality coverage, outcome vocabulary, state machine, canonical ordering/hashing, and authority invariants. Domain modules import no service, adapter, filesystem, clock, randomness, model SDK, or web framework.

### 7.2 Ports and repository

- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/ports/evidence_resolver.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/ports/outcome_classifier.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/ports/independent_evaluator.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/ports/repository.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/repositories/event_sourced_repository.py`

Define one transaction boundary and exact historical reads. An in-memory test repository enforces the same atomicity, parity, concurrency, replay, and idempotency rules as the durable adapter.

### 7.3 Services

- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/services/admission_service.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/services/observation_service.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/services/outcome_service.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/services/delta_service.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/services/receipt_service.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/services/evaluation_service.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/services/invalidation_service.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/services/replay_service.py`

Services orchestrate typed ports and pure domain behavior. They do not implement AIR semantic compilation, call proposal/delivery, Expression Moment approval, Pipeline execution, VAE production, or Studio state ownership.

### 7.4 Integrations and projections

- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/integrations/live_state_gateway.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/integrations/source_evidence_gateway.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/integrations/air_consumption_gateway.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/integrations/source_package_binding_gateway.py`
- `06_INTERVIEW_EXPRESSION/src/interview_expression/reaction_evidence/projections/studio_reaction_evidence_view.py`

Adapters preserve exact owner/version/hash/lifecycle/epistemic/source/evaluator/claim fields. AIR integration is read-only from IE evidence. Studio projection cannot mutate the repository.

### 7.5 Candidate schemas and migration

Potential later paths requiring separate schema/contract authority:

- `06_INTERVIEW_EXPRESSION/contracts/schemas/reaction-observation.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/reaction-observation-stream.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/reaction-outcome-evidence.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/planned-observed-delta-evidence.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/reaction-receipt.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/schemas/reaction-evaluation-receipt.schema.json`
- `06_INTERVIEW_EXPRESSION/contracts/migrations/air-reaction-donor-to-interview-expression-v2_1.yaml`

No schema, validator, generated type, fixture, or migration release is created now.

### 7.6 Exact future test paths

- `06_INTERVIEW_EXPRESSION/tests/unit/reaction_evidence/test_observation_epistemic_state.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/reaction_evidence/test_modality_coverage.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/reaction_evidence/test_reaction_outcomes.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/reaction_evidence/test_nonreaction_vs_evidence_gap.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/reaction_evidence/test_planned_observed_delta.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/reaction_evidence/test_evaluator_independence.py`
- `06_INTERVIEW_EXPRESSION/tests/contract/reaction_evidence/test_ts_int_007_trigger_mapping.py`
- `06_INTERVIEW_EXPRESSION/tests/contract/reaction_evidence/test_air_read_only_consumption.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/reaction_evidence/test_atomic_commit_and_rollback.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/reaction_evidence/test_replay_idempotency_concurrency.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/reaction_evidence/test_selective_invalidation.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/reaction_evidence/test_imported_historical_trigger.py`
- `06_INTERVIEW_EXPRESSION/tests/architecture/test_reaction_evidence_ownership_boundaries.py`
- `06_INTERVIEW_EXPRESSION/tests/migration/test_reaction_donor_migration.py`
- `06_INTERVIEW_EXPRESSION/tests/portability/test_reaction_evidence_clean_room.py`

### 7.7 FR and Story implementation mapping

| Requirement/Story | Future modules | Later evidence |
|---|---|---|
| `AIR-FR-055`, `AIR-ST-10.01` | admission, window, observations, coverage | multimodal alignment and source-span fixtures |
| `AIR-FR-056`, `AIR-ST-10.01` | outcome models/service | all eleven outcomes and invalid alternatives |
| `AIR-FR-057`, `AIR-ST-10.02` | coverage/outcome validation | non-reaction versus capture-gap proof |
| `AIR-FR-058`, `AIR-ST-10.02` | receipts/repository | immutable call/evidence/outcome/counteractivation/evaluator binding |
| `AIR-FR-059`, `AIR-ST-10.03` | delta service | planned/observed owner-preserving comparison fixtures |
| `AIR-FR-060`, `AIR-ST-10.03` | evaluator/evaluation service | independence, alternatives, sufficiency, maximum-claim evidence |

No implementation stage begins from this written draft.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

Minimum stable failures:

- `INT_REACTION_SOURCE_SCOPE_MISMATCH`
- `INT_REACTION_TRIGGER_NOT_DELIVERED_CALL`
- `INT_REACTION_IMPORTED_CALL_HISTORY_FABRICATED`
- `INT_REACTION_STALE_LIVE_WATERMARK`
- `INT_REACTION_WINDOW_INVALID`
- `INT_REACTION_REACTION_TAIL_MISSING`
- `INT_REACTION_OBSERVATION_SOURCE_MISMATCH`
- `INT_REACTION_OBSERVATION_EPISTEMIC_CONTRADICTION`
- `INT_REACTION_MODEL_INFERENCE_PRESENTED_AS_OBSERVED`
- `INT_REACTION_MODALITY_COVERAGE_INCOMPLETE`
- `INT_REACTION_TRANSCRIPT_ONLY_CLAIM_EXCEEDS_EVIDENCE`
- `INT_REACTION_NONREACTION_CONFUSED_WITH_CAPTURE_GAP`
- `INT_REACTION_SILENCE_CONFUSED_WITH_MISSING_AUDIO`
- `INT_REACTION_OUTCOME_UNSUPPORTED`
- `INT_REACTION_OUTCOME_VALUE_UNKNOWN`
- `INT_REACTION_COUNTERACTIVATION_EVIDENCE_MISSING`
- `INT_REACTION_PLANNED_OWNER_MISMATCH`
- `INT_REACTION_DELTA_EVIDENCE_INSUFFICIENT`
- `INT_REACTION_EVALUATOR_NOT_INDEPENDENT`
- `INT_REACTION_SELF_ACCEPTANCE_ATTEMPT`
- `INT_REACTION_MAXIMUM_CLAIM_EXCEEDED`
- `INT_REACTION_SOURCE_AUTHORITY_DENIED`
- `INT_REACTION_NONPORTABLE_EVIDENCE_REF`
- `INT_REACTION_STALE_CASE_VERSION`
- `INT_REACTION_IDEMPOTENCY_CONFLICT`
- `INT_REACTION_ATOMIC_COMMIT_FAILED`
- `INT_REACTION_LATE_RESULT_AFTER_CANCELLATION`
- `INT_REACTION_REPLAY_DIVERGENCE`
- `INT_REACTION_MIGRATION_AMBIGUOUS`
- `INT_REACTION_MIGRATION_LOSSY`

Failure context includes safe IDs, versions, expected/observed hashes, exact failing invariant, responsible layer/owner, retryability, and next admissible action. Sensitive evidence is redacted unless the caller has explicit evidence-read authority.

### 8.2 Retry versus quality repair

- Transaction/content-store failures may retry exactly with the same command/idempotency key.
- Classifier/evaluator calls retry only under a binding that declares deterministic retry semantics.
- Evidence repair uses a new command and successor case version; inputs never change under an existing command identity.
- A quality disagreement is not an operational retry. It becomes `CONTESTED`, `NEEDS_MORE_EVIDENCE`, or human resolution.
- AIR cannot repair missing IE evidence by synthesizing an AIR-local observation.

### 8.3 Atomic rollback and partial results

If any observation, event, aggregate, receipt, evaluation, dependency, idempotency, invalidation, package-binding request, or outbox record fails, no successful state transition is visible. A failure receipt may accompany a denied command but cannot claim resulting artifacts.

Classifier/evaluator proposals created before the failed canonical commit remain noncanonical/quarantined and cannot be consumed. There is no compensating delete of immutable accepted history.

### 8.4 Cancellation and late evidence

Cancellation and commit are ordered by optimistic transaction. A late classifier/evaluator callback after cancellation is quarantined. Post-terminal source evidence may be attached only through the governed command, and it creates successor observations/receipts rather than reopening or rewriting the live session.

### 8.5 Migration and backward compatibility

Migration creates new IE-owned immutable artifacts and receipts; it never edits AIR bundle schemas, examples, predecessor models, or Studio records.

The migrator MUST preserve or explicitly block:

- exact source package/media/transcript and source selectors;
- actual delivered-call or historical-trigger status;
- modality, observed value, observer/method, and epistemic state;
- observation versus interpretation;
- outcome and counteractivation evidence;
- planned and observed owner separation;
- evaluator identity/independence and maximum claim;
- lifecycle, supersession, operator resolution, source authority, and descendants; and
- canonical hash/portability.

Bare millisecond timestamps may migrate only when an exact source/timebase mapping is proven. Generic `interpretation`, `next_action_recommendation`, or narrative-state strings cannot be promoted silently. Missing evaluator evidence produces a nonvalidated historical receipt or blocks migration; it never defaults to accepted.

Deprecated versions remain readable for historical replay. Active accepted downstream work stays pinned to the version it consumed. Deprecation alone does not invalidate historical work; revocation/invalidation rules are explicit.

### 8.6 Selective invalidation

Typed dependency edges declare fields consumed. Examples:

- corrected observation invalidates its outcome, delta dimension, receipt, evaluation, and downstream moments that consumed it;
- correction to reaction-tail range invalidates only cases/descendants using that tail;
- changed planned AIR assertion invalidates affected delta dimensions and semantic descendants, not the raw observation stream;
- evaluation-profile change invalidates evaluation/receipt eligibility but not source observations;
- source-authority revocation invalidates prohibited new uses while preserving historical evidence; and
- unrelated receipt cases remain current with an explicit unaffected proof.

The invalidation projector is resumable/idempotent. Pending invalidation blocks new consumption.

### 8.7 Replay and historical reproduction

Replay resolves exact historical source bytes, live session/call/snapshots, profiles, observations, commands, evaluations, and human resolutions. It reconstructs identical canonical bytes/digests in a fresh process. It cannot read current/latest objects, current time, randomness, environment, or machine paths to fill gaps.

Cancellation, rejection, contest, supersession, invalidation, and revocation do not delete historical artifacts. A historical query returns the requested exact version plus lifecycle/nonconsumability state.

### 8.8 Recovery

After crash, recovery verifies transaction parity, rebuilds projections, reconciles outbox acknowledgements, and resumes invalidation from the last committed checkpoint. Any artifact/hash/event/receipt mismatch quarantines the case and reports the first exact divergence. Recovery never chooses a semantically similar replacement.

### 8.9 Observability and security

Required structured signals:

- cases opened/closed by live/historical trigger;
- observation counts by modality, epistemic state, and coverage state;
- reaction-tail completeness;
- proposed/validated/rejected/contested/needs-evidence outcomes;
- activation-null versus capture-gap denials;
- evaluator independence failures and disagreement;
- planned–observed relation counts by evidence state;
- claim-ceiling and source-authority denials;
- idempotency/concurrency/atomicity failures;
- invalidation fan-out/lag and replay divergence; and
- attempted nonportable or cross-scope refs.

Logs/metrics expose safe IDs and classifications, not transcript text, voice/face evidence, health inferences, participant identity, or restricted source content. Evidence access uses operational technical security and audit logs. Model training or telemetry reuse is forbidden where operator source authority prohibits it.

### 8.10 Degraded behavior

Degraded modes remain explicit:

- observation capture may continue while classifier/evaluator is unavailable;
- a case may preserve `EVIDENCE_INCOMPLETE` without a receipt outcome;
- a candidate may remain `NEEDS_MORE_EVIDENCE` or `CONTESTED`;
- a historical import may preserve observations with limited maximum claim; and
- downstream compilation is blocked unless the consumer’s required eligibility state is met.

No degraded mode claims validation, invents a reaction, or bypasses source authority.

## 9. Behavior-specific acceptance criteria

These criteria are requirements for later independent acceptance, not current pass claims.

### AC-01 — Multimodal reaction stream

- **Governing:** `AIR-FR-055`, `AIR-ST-10.01`.
- **Given** an exact delivered call and source segment with transcript, timing, audio, and visual evidence available,
- **When** the operator closes the reaction window,
- **Then** lexical, vocal, temporal, visual/somatic, interactional, and reaction-tail observations are source-aligned with explicit coverage and epistemic state.
- **Failure example:** only transcript words are stored even though audio/visual evidence was available and material.
- **Evidence/test:** multimodal alignment integration fixture and coverage report.

### AC-02 — Observation is not interpretation

- **Governing:** `AIR-FR-055`, `AIR-ST-10.01` CBAR.
- **Given** a directly observed pause and a model hypothesis about its meaning,
- **When** both are recorded,
- **Then** they are separate linked artifacts with distinct owners/epistemic states.
- **Failure example:** “defensive hesitation” is stored as the directly observed value.
- **Evidence/test:** epistemic-state unit and adversarial contract tests.

### AC-03 — Complete governed outcome vocabulary

- **Governing:** `AIR-FR-056`, `AIR-ST-10.01`.
- **Given** evidence fixtures for each governed human outcome,
- **When** classification runs,
- **Then** all eleven exact outcomes are representable and unknown values fail.
- **Failure example:** operational `observation_failure` is accepted as a human reaction outcome.
- **Evidence/test:** exhaustive outcome enum and negative fixture matrix.

### AC-04 — Non-reaction is evidence

- **Governing:** `AIR-FR-057`, `AIR-ST-10.02`.
- **Given** a complete governed window with sufficient coverage and no meaningful intended transition,
- **When** outcome classification and independent evaluation complete,
- **Then** `ACTIVATION_NULL` or evidence-supported `PARTIAL_HIT` may be validated without manufacturing an Anchor Hit.
- **Failure example:** fluent answer text automatically becomes `ANCHOR_HIT` despite flat/defensive multimodal evidence.
- **Evidence/test:** null/partial positive fixture and downstream denial proof.

### AC-05 — Missing evidence is not non-reaction

- **Governing:** `AIR-FR-057`, `AIR-ST-10.02` adversarial case.
- **Given** corrupted audio and no reaction-tail capture,
- **When** a classifier proposes `ACTIVATION_NULL`,
- **Then** deterministic validation rejects it as `INT_REACTION_NONREACTION_CONFUSED_WITH_CAPTURE_GAP`.
- **Failure example:** missing audio is labeled silence.
- **Evidence/test:** capture-gap unit and integration tests.

### AC-06 — Receipt binds actual call and evidence

- **Governing:** `AIR-FR-058`, `AIR-ST-10.02`.
- **Given** a validated live case,
- **When** a receipt candidate compiles,
- **Then** it binds the exact delivered call, pressure decision, source spans, observation stream, outcome, counteractivation, uncertainty, delta, source authority, and evaluator lifecycle.
- **Failure example:** an AIR proposal ref is used although the human delivered different wording.
- **Evidence/test:** `TS-INT-007` mapping and receipt completeness contract tests.

### AC-07 — Imported trigger does not fabricate live history

- **Governing:** `AIR-FR-058`; imported-source constitutional boundary.
- **Given** an imported interview with exact prompt/response spans but no live-call record,
- **When** a reaction case opens,
- **Then** it uses `HISTORICAL_SOURCE_TRIGGER`, records live fields as evidence-bearing not applicable, and lowers claim where planning context is unavailable.
- **Failure example:** migration invents `call_id=main-question` and a pressure dose.
- **Evidence/test:** imported historical-trigger integration and migration fixtures.

### AC-08 — Planned–observed owner separation

- **Governing:** `AIR-FR-059`, `AIR-ST-10.03`.
- **Given** exact AIR planned state/role/edge/route refs and IE observations,
- **When** the delta compiles,
- **Then** it preserves both owners, records evidence relation/mismatch, and changes neither input.
- **Failure example:** IE copies a planned role into `observed_role` without source evidence.
- **Evidence/test:** delta ownership unit and AIR read-only boundary tests.

### AC-09 — Mismatch remains visible

- **Governing:** `AIR-FR-059`, `AIR-ST-10.03`.
- **Given** a planned anchor/route not supported by sufficient observed evidence and an unexpected edge,
- **When** the delta compiles,
- **Then** both the unsupported plan and unexpected evidence are retained with exact refs and epistemic state.
- **Failure example:** the planned object is rewritten to match the observed result.
- **Evidence/test:** planned–observed divergence fixture and replay proof.

### AC-10 — Independent evaluator

- **Governing:** `AIR-FR-060`, `AIR-ST-10.03`.
- **Given** a receipt candidate,
- **When** evaluator identity equals the call proposer or receipt compiler,
- **Then** final validation fails `INT_REACTION_EVALUATOR_NOT_INDEPENDENT`.
- **Failure example:** the same model proposes the call, classifies `ANCHOR_HIT`, and approves its receipt.
- **Evidence/test:** evaluator-independence unit and architecture tests.

### AC-11 — Alternatives and maximum claim

- **Governing:** `AIR-FR-060`, `AIR-ST-10.03`.
- **Given** evidence compatible with `STATE_TRANSITION` and `UNEXPECTED_EDGE`,
- **When** independent evaluation runs,
- **Then** it records alternative interpretations, uncertainty, and the maximum supported claim rather than hiding disagreement.
- **Failure example:** highest score alone produces validated `ANCHOR_HIT`.
- **Evidence/test:** evaluator disagreement fixture and receipt assertions.

### AC-12 — Strong affect is not intended activation

- **Governing:** `AIR-FR-056`, `AIR-FR-060`, CBAR/Primitive constraints.
- **Given** intense visual/vocal affect that conflicts with the planned outcome and may reflect defensive closure,
- **When** classification/evaluation run,
- **Then** outcome fit and counteractivation are evaluated independently; intensity cannot prove activation.
- **Failure example:** raised voice becomes `ANCHOR_HIT` without context.
- **Evidence/test:** adversarial multimodal fixture.

### AC-13 — Reaction-tail preservation

- **Governing:** `AIR-FR-055`, `AIR-ST-10.01`.
- **Given** a delayed self-correction after the apparent answer,
- **When** the governed reaction tail includes it,
- **Then** the exact source span participates in outcome/evaluation and remains traceable.
- **Failure example:** capture stops at the last transcript word and misses the correction.
- **Evidence/test:** reaction-tail range fixture and source-time hash matrix.

### AC-14 — Primitive evidence without hard-coded meaning

- **Governing:** all six FRs and three Story CBAR mandates.
- **Given** exact Primitive refs and applicability,
- **When** validation/evaluation runs,
- **Then** it resolves exact bytes, tests activation/misuse/suppression, and preserves AIR coalition ownership.
- **Failure example:** a fuzzy “felt truth” prompt replaces `PRM-VSG-021` or turns a staged imperfection into observed evidence.
- **Evidence/test:** Primitive registry hash and misuse fixtures.

### AC-15 — Idempotency and optimistic concurrency

- **Governing:** all six FRs; Story recovery.
- **Given** a committed command,
- **When** identical bytes retry under the same key,
- **Then** the original result returns; different bytes or stale case/watermark fail without mutation.
- **Failure example:** two classifiers overwrite the current outcome and each emits a success receipt.
- **Evidence/test:** repository concurrency/idempotency integration test.

### AC-16 — Atomic commit and rollback

- **Governing:** `AIR-FR-058`, `AIR-FR-060`; receipt trust.
- **Given** fault injection at every persistence boundary,
- **When** commit fails,
- **Then** no state exists without command/receipt/evidence, no receipt without artifacts/evaluation, and no rolled-back outbox is published.
- **Failure example:** validated receipt stored while evaluator receipt write failed.
- **Evidence/test:** exhaustive atomic fault-injection matrix.

### AC-17 — Selective correction and invalidation

- **Governing:** all Stories’ recovery criteria.
- **Given** one corrected vocal observation in one reaction case,
- **When** the successor commits,
- **Then** only its outcome/delta/receipt/evaluation and exact downstream consumers become stale; unrelated cases remain current.
- **Failure example:** every session receipt is invalidated.
- **Evidence/test:** dependency-graph selective-invalidation test.

### AC-18 — Historical reproduction

- **Governing:** all Stories’ evidence/replay criteria.
- **Given** a superseded or rejected receipt,
- **When** exact historical replay runs in a fresh process,
- **Then** canonical bytes/digests and lifecycle reconstruct without using current/latest dependencies.
- **Failure example:** replay substitutes the current planned AIR object.
- **Evidence/test:** clean-process replay/hash matrix.

### AC-19 — Portable evidence

- **Governing:** source fidelity and contract compatibility.
- **Given** a clean extracted layout on another machine root,
- **When** the case and evidence package load,
- **Then** every portable ref resolves by governed locator/hash and no machine path/environment value appears in canonical bytes.
- **Failure example:** a local recording path is the only evidence identity.
- **Evidence/test:** clean-room export/import and absolute-path scan.

### AC-20 — AIR consumes but cannot manufacture

- **Governing:** product sovereignty for all six FRs.
- **Given** AIR requests an eligible receipt,
- **When** the gateway serves it,
- **Then** AIR receives an exact read-only view with owner, lifecycle, source, epistemic, evaluation, and claim fields; AIR cannot write or normalize a local evidence fork.
- **Failure example:** AIR creates an “observed receipt” from planned expectations because IE evidence is incomplete.
- **Evidence/test:** architecture import boundary and consumer conformance tests.

### AC-21 — Receipt does not auto-approve an Expression Moment

- **Governing:** Stories’ terminal condition and product boundary.
- **Given** a validated Reaction Receipt,
- **When** Expression Moment resolution begins,
- **Then** the receipt is required evidence but no moment is approved until its separate source-span/context/authority/evaluation gates pass.
- **Failure example:** `ANCHOR_HIT` receipt automatically publishes a quote card.
- **Evidence/test:** downstream denial fixture.

### AC-22 — Claim ceiling remains truthful

- **Governing:** recovery authority and packet claim ceiling.
- **Given** passing local structural tests or a candidate evaluation,
- **When** status is reported,
- **Then** this spec remains `WRITTEN_PENDING_AUDIT`, candidate authority remains non-current, and build/certification/production remain false.
- **Failure example:** candidate receipt validation is reported as evaluator or production certification.
- **Evidence/test:** receipt/status-policy validation.

## 10. Testing and completion evidence

### 10.1 Unit and property tests

Required future cases include:

- `test_observation_epistemic_state.py::test_model_inference_cannot_be_direct_observation`
- `test_modality_coverage.py::test_every_profile_modality_has_typed_coverage`
- `test_modality_coverage.py::test_missing_audio_is_not_silence`
- `test_reaction_outcomes.py::test_exact_eleven_outcomes_and_unknown_rejected`
- `test_nonreaction_vs_evidence_gap.py::test_activation_null_requires_sufficient_coverage`
- `test_planned_observed_delta.py::test_planned_and_observed_owners_do_not_collapse`
- `test_planned_observed_delta.py::test_mismatch_and_unexpected_evidence_coexist`
- `test_evaluator_independence.py::test_call_proposer_and_compiler_cannot_accept`
- canonical serialization property tests varying map insertion, callback order, source ordering, locale, timezone, and hash seed.

### 10.2 Contract and schema tests

- Positive/negative canonical vectors for every type in section 6.
- Exact `TS-INT-007` live call, snapshot, watermark, evidence selector, command, event, and post-terminal mapping.
- Imported historical trigger with no fabricated live fields.
- Exact owner/version/hash/lifecycle/epistemic/evaluator/source-authority preservation through AIR, package, Pipeline, Studio, and Delegation adapters.
- Parse-without-enforcement denial.
- Candidate donor fixtures treated as migration inputs, not accepted current schemas.

### 10.3 Multimodal fixture portfolio

Governed fixtures must cover:

1. anchor hit with complete premise, response, and reaction tail;
2. partial hit;
3. unexpected edge;
4. state transition;
5. flat answer;
6. defensive reaction;
7. topic escape;
8. observed silence;
9. contradiction/self-correction;
10. landing reached;
11. activation null with sufficient coverage;
12. missing-audio/visual evidence gap;
13. intense affect that is not intended activation;
14. delayed reaction tail changing the outcome;
15. imported interaction with absent live planning/call; and
16. contested alternatives requiring human resolution.

Each fixture has exact source hashes, spans, speaker refs, coverage, profiles, observation/interpretation refs, expected outcome/alternatives, delta, evaluator verdict, maximum claim, and denial reason where applicable.

### 10.4 Repository, replay, cancellation, and recovery tests

- Fault-inject every command/event/aggregate/observation/receipt/evaluation/dependency/idempotency/invalidation/outbox boundary.
- Retry after unknown commit outcome and prove one logical result.
- Race stale concurrent observation/outcome/evaluation commands.
- Cancel before/after classifier/evaluator callbacks and prove late results cannot publish.
- Attach late post-terminal evidence and prove a successor without reopening the session.
- Rebuild projections in a fresh process and compare every canonical hash.
- Corrupt one artifact and prove quarantine reports the first exact divergence.
- Resume selective invalidation from a checkpoint without duplicating effects.

### 10.5 Architecture and sovereignty tests

- Domain/repository modules do not import AIR semantic compiler, Pipeline executor, VAE, Studio persistence, Delegation implementation, provider SDK, filesystem, clock, or randomness.
- AIR integration is read-only and cannot construct IE observation/receipt types as authoritative writes.
- Call proposal, call delivery, reaction evidence, independent evaluation, AIR compilation, Expression Moment resolution, and source-package binding remain distinct services/artifacts.
- Human resolution is a typed additive command; direct UI mutation cannot change canonical state.
- No generic rights/safety authority or product certification is introduced.

### 10.6 Primitive and CBAR evidence

For `EXP-FBK-001`, prove meaningful immediate capture feedback without premature/vanity scoring and respect continuous-recording suppression. For `PRM-PSY-001`, prove layer evidence and shifts without diagnosis/performative matching. For `PRM-VSG-021`, preserve real micro-expression/friction evidence and reject manufactured or technically unusable “felt truth.” Every test resolves exact Primitive bytes/hash and applicability.

### 10.7 Migration and portability tests

- Preserve donor bytes and hashes before/after migration.
- Map exact legacy observations/receipts only when source, trigger, timing, epistemic state, outcome, evaluator, and owner can be proven.
- Block generic interpretation, next-action, float confidence, missing call, missing evaluator, ambiguous null, and local-path-only evidence unless resolved by attributable exact evidence.
- Export/import under a different root with no absolute paths, undeclared files, environment dependency, random identity, or current-time identity.

### 10.8 Independent evaluation evidence

A future evaluator-validation package must include:

- evaluator identity and separation proof;
- evaluation profile/implementation/dataset lineage where applicable;
- evidence-sufficiency and outcome-fit confusion portfolio;
- alternative-interpretation and maximum-claim calibration;
- false-positive/false-negative review across null, partial, defensive, and intense-affect cases;
- disagreement and HumanResolution fixtures; and
- explicit certification state. Capability implementation/contract compatibility does not imply certification.

No evaluator threshold or certification is invented by this document.

### 10.9 Reference-slice proof

The frozen imported-interview slice must demonstrate:

- truthful absent live-call/planning history;
- exact source observation and reaction-tail evidence;
- an independently evaluated Reaction Receipt or typed evidence blocker;
- later Expression Moment resolution without automatic promotion;
- AIR read-only semantic consumption;
- source package and derivative lineage;
- operator correction/HumanResolution and selective replay; and
- no Format 02 certification inheritance or VAE Stage 5 implication.

### 10.10 Required later completion artifacts and handoff

A separately authorized build requires exact source/build manifests, schema/adapter conformance, multimodal fixture matrix, Primitive evidence, evaluator independence/calibration, atomic fault-injection, deterministic fresh-context replay, selective invalidation, migration losslessness/blocked evidence, clean-room portability, absolute-path scan, dependency/license disposition, security/redaction proof, independent audit, bounded revision where required, independent re-audit, and attributable acceptance.

This specification consumed `TS-INT-007` at SHA-256 `98978c560ba216707fcc7d26305de1f2c42e9391f09db20aa4fc97a69fe08dbc`, state `WRITTEN_PENDING_AUDIT`, labeled `DRAFT_DEPENDENCY_NOT_ACCEPTED`. A hash change triggers the recorded six-section revision impact.

The next lifecycle action is independent audit by a different agent. The writer has not audited, revised, accepted, implemented, built, released, certified, or issued a Development Capsule.
