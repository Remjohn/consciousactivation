---
type: technical_specification
spec_id: TS-INT-007
title: Live Activative State and Interview Execution
product: Interview Expression
version: 2.1.0-candidate
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_build_gate: RATIFICATION_REQUIRED
document_class: CANDIDATE_CANONICAL_TECH_SPEC
output_path_class: DIRECT_PRODUCT_SPEC_PATH
adoption_status: NOT_APPLICABLE
build_status: NOT_BUILD_READY
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
writing_wave: 5
controlling_frs:
  - AIR-FR-049
  - AIR-FR-050
controlling_stories:
  - AIR-ST-09.01
upstream_draft_dependencies:
  - spec_id: TS-AIR-008
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: e8fac04b295ec742621e92735475f2c603f16b69b26f67b5e5c840ab6ddb16a0
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-009
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: f904f8a996895917098e28f3ee99c0162dd34efdc4a07aae36f4dad069c5ca52
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-INT-007 - Live Activative State and Interview Execution

This candidate specification defines the Interview Expression-owned operating truth for a live activative interview: the evidence-bearing state projection after each meaningful event, the interviewer's genuine reaction when it changes the next useful call, the exact call actually delivered, the human pressure decision, and the resulting receipt-backed transition. It controls `AIR-FR-049`, `AIR-FR-050`, and `AIR-ST-09.01`. It does not transfer semantic-policy ownership from Activative Intelligence Runtime (AIR), does not allow AIR to execute a call, and does not convert model inference into human reaction or historical truth.

The controlling V2.1 authority is `CANDIDATE_NOT_CURRENT`. Specification writing is explicitly authorized by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`; build and production authority are false. This document may later reach no higher than `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` until attributable authority ratification occurs. It does not implement code, create a schema or contract release, adopt a product, issue a Development Capsule, activate Format 02, begin VAE Stage 5, or claim production, certification, evaluator, publication, or provider readiness.

`TS-AIR-008` and `TS-AIR-009` are consumed only as hash-pinned `WRITTEN_PENDING_AUDIT` interface drafts. Each is `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Their bytes are not current authority and have not been independently accepted. Any change to either pinned draft reopens sections 3, 5, 6, 8, 9, and 10 of this specification for explicit revision-impact review.

## 1. Files and authorities read

### 1.1 Authority, requirement, and workflow inputs

| Input | State | SHA-256 | Use in this specification |
|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | current authority registry | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Establishes that Constitution V1.1 remains current until a governed amendment is ratified. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Governs the Activative chain, human-reaction law, Expression Moments, and the existing Interview Expression boundary. |
| `.../doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `CANDIDATE_NOT_CURRENT` | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Candidate live-state, epistemic, receipt, immutable-history, product-sovereignty, and human-authority laws. |
| `.../prd/features/F09-live-narrative-state-induction-and-interviewer-resonance.md` | `2.1.0-draft`, pending ratification | `a1e1421ee23b0f30f84bffeb37bfd5b6eac74a29d4a9e24a036c85a257ec8fa5` | Controls `AIR-FR-049` and `AIR-FR-050`: update live state after meaningful events and preserve genuine interviewer reaction when operative. |
| `.../planning/EPICS_AND_VERTICAL_STORIES.md` | candidate planning | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | Controls `AIR-ST-09.01`, including armed entry, receipt-backed transitions, truthful landing/reset/stop, and no fabricated reaction. |
| `.../specs/TS-AIR-009-live-narrative-state-induction-and-interviewer-resonance.md` | split source donor | `96f25c8912ac2c334ced7220c3ee7dff9e031e5e5985bb848f93e88ddb930a0d` | Substantive donor, used only after applying the governed AIR/Interview Expression ownership split. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SPEC_DISPOSITION_REPORT.md` | frozen disposition | `86852420631241ce6341a04d258f476473d0490274bb4e22675301cb02c13241` | Requires the donor to split into AIR semantic policy (`TS-AIR-009`) and Interview Expression live state/execution evidence (`TS-INT-007`). |
| `.../CANONICAL_SPEC_LEDGER.csv` | frozen writing queue | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Freezes title, ownership, direct path, gate, two FRs, and Story count. |
| `.../CANONICAL_FR_LEDGER.csv` | frozen requirements ledger | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Assigns FR-049 and FR-050 to Interview Expression rather than AIR. |
| `.../FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | frozen traceability | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Links the controlling FRs, primary owner, `AIR-ST-09.01`, and this exact spec. |
| `.../SPEC_DEPENDENCY_DAG.yaml` | Prompt 02 DAG | `1cf4299781e76c9c80f4489291a92b0a5e1f666f91b8cf9476307a03da5257eb` | Records AIR-008 and AIR-009 upstream relationships. |
| `.../PATH_OWNERSHIP_REGISTRY.yaml` | frozen path registry | `f260e400384a67f837b67a8a8981a4b773cd8792135eeca20c94f065468296a7` | Reserves only `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-007.md`. |
| `.../V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending ratification | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Separates AIR semantic-policy meaning, Interview Expression live evidence, human choice, pipeline execution, VAE realization, Studio projection, and Delegation transport. |
| `.../V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending ratification | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Assigns authoritative live state and reaction observations to Interview Expression and planned semantic programs to AIR. |
| `.../V2_1_AUTHORITY_CONVERGENCE/PRODUCT_ROOT_REGISTRY.yaml` | intended-root registry | `bb898168c770a09d0d6974c3ed347cf07b7770ccc41da094bb325c1777baa0be` | Reserves the Interview Expression product root without authorizing a source tree. |
| `.../SOURCE_DISPOSITION_LEDGER.yaml` | validated source registry | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Admits the four F09 doctrine sources as required unique evidence. |
| `.../SOURCE_GAP_NOTICE.yaml` | zero blocking gaps | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | Prevents claims from unavailable optional/deferred sources; no such source is used here. |
| `.../RECONCILIATION_INPUT_HASH_LOCK.yaml` | locked | `ea28bcab299e74adb87f3bce8ab8a1d20093d4d8699e9e10c5d387383363c456` | Locks the four admitted archives and candidate package inputs. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | validated recovery | `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | Classifies SDE-024 and SDE-025 as write-interface dependencies, not acceptance/build blockers. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_WRITING_WAVE_DAG.yaml` | acyclic writing DAG | `24b26b9820a0f2cab0cd01ab4c46e9aca476219f496644c063533ee602ccff60` | Places this spec in Wave 5 after the two AIR drafts. |
| `.../V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | candidate pending ratification | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Requires the candidate label, build false, and pre-ratification acceptance ceiling. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | specification work only | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes writing and later independent technical review without build authority. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv` | path decision | `3fa4793ea2baca46dcfbf8e123d039a59ab2467e5814471d49b3daf65e588a73` | Records direct spec-path authority and no applicable product-local `AGENTS.md`. |
| `.../V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | V3.3 packet | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Freezes the single output, FRs, Story, dependencies, path class, lifecycle state, and claim ceiling. |
| `.../wave-receipts/WAVE_05_DISPATCH_LOCK.yaml` | `DISPATCHED` | `e135a1ddce50c52c3a03901cde6feb257c8cf73dc9f81eb02df2484d2a7ad2bf` | Pins AIR-008 and AIR-009 to the exact bytes consumed here. |
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/.../skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3 writer law | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Requires ten implementation-grade sections, source/dependency receipts, and no self-audit or acceptance. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/MASTER_STATUS.md` | current status truth | `71d7fdac3c9498c42133c95e141b31241b0fa613426417d9fd81b3d1d656f491` | Preserves candidate authority, implementation false, VAE Stage 5 unauthorized, and no production/certification claim. |

The abbreviated `...` paths expand under the Prompt 02 reconciliation/recovery or AIR full-bundle roots named by their leading item. No repository-root or ancestor `AGENTS.md` governs the target path. The exact recovery packet grants specification-only authority for this direct product spec; it grants no source-tree, schema, test, build, or production write authority.

### 1.2 Exact upstream draft interfaces

| Edge | Draft | State | Bytes | SHA-256 | Interface used | Revision impact if bytes change |
|---|---|---|---:|---|---|---|
| SDE-024 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-008.md` | `WRITTEN_PENDING_AUDIT` | 78,755 | `e8fac04b295ec742621e92735475f2c603f16b69b26f67b5e5c840ab6ddb16a0` | IAC identity/version, armed binding, planned branch, pressure envelope, recovery/landing policy, locks, source/provenance, invalidation, and replay references | sections 3, 5, 6, 8, 9, 10 |
| SDE-025 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-009.md` | `WRITTEN_PENDING_AUDIT` | 84,389 | `f904f8a996895917098e28f3ee99c0162dd34efdc4a07aae36f4dad069c5ca52` | policy proposal envelope, Activative Call options, pressure recommendation, counteractivation hypotheses, transitions, and smallest-useful-call proof | sections 3, 5, 6, 8, 9, 10 |

Both rows are `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Neither is represented as ratified authority, accepted architecture, or build-ready contract. The dispatch lock, draft receipt, and downstream revision-impact list are part of this document's reproducibility boundary.

### 1.3 Required unique doctrine and Primitive evidence

| Evidence | Bytes | SHA-256 | Governing fact used |
|---|---:|---|---|
| `.../sources/ai_v2_predecessor/07_LIFECYCLE_STATE_MACHINES.md` (`SRC-AI2-LIVE-001`) | 1,285 | `403f684a14160ac974cdfd0f45ca25645a5a0a38e07628d7096d80d87a5236cb` | Planned, armed, live, observed, and resolved are distinct states; invalidation and repair are additive. |
| `.../sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | 43,321 | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | The guest controls truth; the human interviewer creates the shared field; landing is evaluated rather than assumed. |
| `.../sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` (`SRC-INT-002`) | 24,239 | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | Contracts, anchors, capture configuration, archetype routing, and receipts stay attributable. |
| `.../sources/doctrine/MATRIX_OF_EDGING.md` (`SRC-MOE-001`) | 15,982 | `7ba1858cd9238a63f32d28e9cc8e7bbe306ba82ac5fa5af4a0346128aa3b6ebb` | Broad signal precedes sharp edge formation; evidence must survive challenge; unsupported inference is not source truth. |
| `.../psychological_diagnostics/PRM-PSY-008.yaml` | 5,916 | `1f63263ab6e0178e3c62feda7bfc5951ea02f1dd8bdafa96b15efd0a0381cfeb` | Pressure attacks the problem rather than identity and rejects toxic positivity/passive aggression. |
| `.../feedback_scoring/EXP-FBK-001.yaml` | 6,981 | `ef888d832e745444a7fcf80192548f89a40abadc77e9653bd7c76ff966cae8ec` | Feedback must be relevant, immediate, and meaningful; its example timing is not imported as an ungoverned SLA. |
| `.../persuasion/PRM-PRS-009.yaml` | 7,442 | `91acef681584ee72d14be51159ac5ed6d0683168dc71a95369b56d9956268caa` | Disequilibrium must not become false jeopardy or strand the person without a landing route. |

### 1.4 Brownfield evidence

| Existing artifact | Bytes | SHA-256 | Reuse and gap finding |
|---|---:|---|---|
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/expression_session.py` | 5,923 | `afce01302bb59f8b85b49bc12ea000ec74de8cd2f020707df6c6dd18e7ae316a` | Reuse typed organization/brand/session/status/receipt vocabulary; do not reuse random identity, wall-clock identity, or a mutable row as canonical history. |
| `.../services/expression_session_service.py` | 24,790 | `bde10d6cd18e37cb4c8bd347654a65cec4f47eaf91f8d96f93ef1bf09b6d745b` | Reuse explicit start/pause/resume/fail/close intent and readiness denial; sequential writes are not an atomic state/event/receipt boundary. |
| `.../repositories/expression_sessions.py` | 1,441 | `3fac9930a8ba9f41be8768b03f1a06a76f75eb4d0d02027ae421cf673e9f27b5` | Existing overwrite maps do not supply optimistic concurrency, idempotency, command parity, replay, invalidation, or immutable versions. |
| `.../workflows/complete_expression_session.py` | 7,756 | `dc1588dc02daef62c9676a238d2e564b3ece31545af19f191b554022a4bb0484` | Reuse explicit stage orchestration and configured-service failures; the workflow mixes source, review, routing, and package stages and is not the live-state event core. |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_complete_expression_session_creation.py` | 10,256 | `0f0d04640e1c91f8f295aaed270fb014574dff455efe04a1de599bf20a3e3668` | Preserve tests for brand scope, readiness-denial receipts, start evidence, IAC binding, and explicit lifecycle changes; add atomicity, replay, concurrency, and truth-boundary tests. |

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem

AIR can propose semantic policy, planned calls, pressure doses, and transitions, but it cannot truthfully know what a human interviewer actually said, what the interviewer genuinely felt, how the guest visibly or verbally responded, or whether the session landed. A mutable session row or a generic note field would collapse proposal, execution, observation, and interpretation into one unverifiable state. That collapse would permit at least six constitutional errors:

1. treating an AIR recommendation as a delivered call;
2. fabricating an interviewer reaction from model inference;
3. treating a provisional observation as settled historical truth;
4. changing live state without a corresponding event and receipt;
5. applying a policy proposal computed against a stale snapshot;
6. replaying a different state because time, process order, or repository insertion order changed.

The live loop also needs to remain useful under human interruption, spontaneous interviewer language, uncertainty, partial evidence, pauses, resets, landings, cancellations, and late AIR proposals. It must preserve the human's authority to lower pressure, choose a different lawful call, or stop even when AIR recommends continuing.

### 2.2 User outcome

An authorized interviewer and operator can see one current evidence-bearing projection that answers:

- what binding and IAC version are active;
- which live event has been incorporated;
- what target state and distance are currently asserted, by whom, and with what confidence/evidence;
- which anchor and landing conditions are open, hit, disputed, or resolved;
- what call was actually delivered, independent of what AIR proposed;
- what pressure was actually chosen and what ceiling governed it;
- what genuine interviewer reaction is operative, when human-attested;
- which observations remain provisional;
- which continue/deepen/reset/land/stop choices remain lawful;
- why the current projection exists and how to reproduce it.

The guest remains the authority for personal truth. The interviewer remains the authority for their own reaction and actual delivery choice. AIR remains the authority for semantic-policy proposal meaning. Interview Expression remains the authority for the live execution/evidence record and its deterministic projection.

### 2.3 Proposed solution

Implement, only after later authorization, an append-only `LiveActivativeSession` aggregate. Commands are normalized, authorized, and idempotently recorded. Each accepted command atomically stores:

1. the command record;
2. zero or more immutable live events;
3. the resulting immutable state snapshot when state changes;
4. an outcome receipt (success, denial, conflict, no-op, or cancellation);
5. a projection checkpoint or deterministic projection inputs.

The aggregate distinguishes AIR proposals from human execution. An AIR policy envelope is acknowledged only when its IAC, binding, input snapshot, observation watermark, feature requirements, and compatibility profile match the live session. A human action records the selected proposal option or a spontaneous-human origin. The transition uses the delivered-call event, pressure decision, observation references, and human authority—not the mere presence of an AIR proposal.

### 2.4 In scope

- `LiveActivativeSession` identity and append-only event stream;
- immutable `LiveActivativeStateSnapshot` and current projection;
- `InterviewerReactionState` with human attestation and evidence references;
- actual delivered-call and pressure-decision evidence;
- AIR-008 IAC/binding and AIR-009 policy-envelope consumption;
- commands for start, acknowledge, react, observe, deliver, advance, pause, reset, land, stop, cancel, and replay;
- optimistic concurrency, idempotency, atomic commit, deterministic serialization, replay, invalidation, and recovery;
- explicit epistemic states and typed `NOT_APPLICABLE`;
- product sovereignty, organization/brand/session scope, audit receipts, and error context;
- exact future implementation and test paths without creating them in this writing task.

### 2.5 Out of scope

- compiling the IAC, planned narrative program, semantic call policy, pressure recommendation, or counteractivation hypothesis (AIR owns these);
- autonomous call delivery, synthetic interviewer reaction, emotion detection presented as fact, or model-driven stop authority;
- full Reaction Receipt/outcome classification (owned by `TS-INT-006`); this spec records live observation references and transition evidence only;
- transcript ingestion, alignment, editing, source package finalization, Expression Moment governance, routing, or asset package composition;
- Pipeline execution internals, Delegation transport/envelope implementation, VAE production, Studio projection/correction UX, or Independent Evaluation semantics;
- a canonical schema, shared release, generated types, source tree, tests, code, migration execution, Development Capsule, build, production, or certification;
- Format 02 activation or any inherited certification.

### 2.6 Claim ceiling

The only completion claim permitted by this writing task is `WRITTEN_PENDING_AUDIT`. `NOT_APPLICABLE` is an explicit governed value where a concept truly does not apply; it is never represented by empty text, missing evidence, or an omitted required field.

## 3. Governing decisions and constraints

### 3.1 Ownership and authority ledger

| Object or decision | Authoritative owner | Interview Expression behavior | Forbidden substitution |
|---|---|---|---|
| Planned IAC, target state, narrative branches, pressure envelope, locks | AIR | bind exact immutable versions and preserve references | rebuilding or weakening semantic meaning locally |
| AIR policy proposal, call options, pressure recommendation, counteractivation hypothesis | AIR | validate, acknowledge, display, and preserve proposal bytes/hash | treating the proposal as an executed act or observed truth |
| Live session state and event watermark | Interview Expression | author and project from accepted live events | accepting a model-generated state overwrite |
| Interviewer's genuine reaction | human interviewer; recorded by Interview Expression | require attributable human attestation and optional evidence | inferring reaction from transcript/video/model output and labeling it genuine |
| Actual delivered call | human interviewer; recorded by Interview Expression | record exact/normalized language, origin, timing token, and evidence | backfilling an AIR proposal as delivered or rewriting spontaneous speech to match a proposal |
| Operative pressure dose, reset, landing, stop | authorized human | record the decision and constraints used | AIR auto-execution or a mandatory pressure escalation |
| Guest personal truth | guest/source authority | record attributable expression/observation without semantic override | declaring a counteractivation hypothesis as the guest's truth |
| Reaction Receipt and resolved outcome | Interview Expression under `TS-INT-006` | hold typed refs and provisional observation states | flattening outcome classification into this live-state spec |
| Persistence/execution infrastructure | future authorized implementation product | enforce these contracts without changing meaning | runtime convenience becoming semantic authority |
| Transport envelope and shared failure semantics | Delegation | consume if/when an adopted contract exists | Delegation becoming creative or execution authority |

### 3.2 Non-negotiable decisions

1. **AIR is advisory in the live loop.** An AIR proposal can narrow lawful options but cannot deliver speech, assert human reaction, advance the state, or compel pressure.
2. **Actual events outrank planned events.** The event stream records what happened. A selected proposal reference explains provenance; it does not replace delivered-call evidence.
3. **Reaction is attributable.** `InterviewerReactionState` requires an authorized interviewer assertion. Machine observations can be linked as evidence but cannot populate a human-attested reaction claim.
4. **Live is not silently historical.** Live observations can be provisional, contested, or unresolved. Only a governed resolution/persistence flow may promote them to durable source-history claims.
5. **Every meaningful transition is receipt-bearing.** No state mutation exists without command, event, snapshot, and receipt parity in one atomic boundary.
6. **The human can always de-escalate or stop.** Any path that removes reset, land, stop, or cancel is invalid, regardless of AIR recommendation.
7. **No guessed classification.** Source kind, reaction kind, call origin, target-distance profile, evidence availability, and `NOT_APPLICABLE` are explicit governed values. Unknown values fail closed.
8. **Semantic constraints are monotonic.** Locks and ceilings may be preserved or strengthened by an authorized newer version, never weakened by an adapter, projection, derivative, or local convenience.
9. **Canonical inputs are immutable.** IAC, policy proposal, live event, snapshot, receipt, and invalidation records are versioned and content-addressed. Current views are projections.
10. **Determinism excludes volatile inputs.** Wall time, randomness, environment variables, process IDs, filesystem traversal order, dictionary insertion accidents, and absolute machine paths cannot determine identifiers, hashes, ordering, or replay outputs.

### 3.3 Epistemic state law

Every assertion that can be mistaken for human or source truth carries one state:

- `HUMAN_ATTESTED`: explicitly asserted by the identified human actor;
- `DIRECTLY_OBSERVED`: tied to an attributable recording/transcript/operator observation without interpretation beyond the declared observation vocabulary;
- `MODEL_INFERRED`: generated by a model and never displayed or persisted as human truth;
- `HYPOTHESIZED`: a bounded semantic possibility requiring testing;
- `CONTESTED`: evidence or an authorized actor disputes the assertion;
- `RESOLVED`: governed evidence/decision closes the assertion for the specified scope;
- `UNKNOWN`: no lawful assertion can be made;
- `NOT_APPLICABLE`: the field is governed but does not apply for the event kind.

`MODEL_INFERRED`, `HYPOTHESIZED`, and `UNKNOWN` cannot satisfy a human-attestation requirement. `NOT_APPLICABLE` cannot satisfy a required observation, delivery, reaction, or receipt field.

### 3.4 Dependency impact covenant

The interfaces below are intentionally coupled to the pinned upstream drafts:

- AIR-008: binding identity, IAC version/hash, branch identity, pressure ceiling, locks, source/provenance references, recovery and landing conditions;
- AIR-009: policy proposal identity/hash, input snapshot/watermark, transition options, Activative Call option, pressure recommendation, counteractivation hypothesis, smallest-useful-call proof.

If either draft hash changes, the future implementation must block promotion and reopen this specification's governing decisions, workflow, models/interfaces, failure/recovery, acceptance, and tests. Mechanical compatibility alone is insufficient; semantic meaning and authority must still match.

### 3.5 Security and tenancy constraints

Technical security is operational, not generic creative-approval authority. Every command and read is scoped by organization, brand, session, actor, role, and authority grant. Cross-tenant IDs fail before content is read. Sensitive source, transcript, recording, and reaction evidence uses least-privilege references, retention policy, audit logging, encryption, and redaction. These controls do not grant a platform reviewer the right to override source authority, provenance, human delivery, product sovereignty, or semantic ownership.

## 4. Current brownfield architecture

### 4.1 Useful predecessor behavior

The CMF Studio predecessor provides typed `CompleteExpressionSession` identity, organization/brand scope, a readiness gate, lifecycle status events, start receipts, source-ingestion orchestration, and explicit pause/resume/fail/close methods. Its tests show that brand mismatch is rejected and that blocked starts produce receipts. Those are valuable behavioral seeds.

### 4.2 Gaps against the required live-state invariant

| Gap | Current manifestation | Required correction in a later authorized implementation |
|---|---|---|
| Mutable canonical session | repository overwrites one session object | append immutable events/snapshots; current state is a projection |
| Non-deterministic identity/time | UUID generation and current timestamps occur inside services | caller/command supplies normalized identity and logical time; volatile timestamps remain non-hashed metadata |
| Non-atomic persistence | session, event, and receipt are written sequentially | commit command/event/snapshot/receipt in one transaction or write batch |
| No optimistic concurrency | update follows latest row without expected version | require `expected_sequence` and `expected_projection_hash` |
| No idempotent command record | duplicate calls can create distinct artifacts | stable idempotency key and deterministic command fingerprint |
| No live semantic split | no distinction among AIR proposal, actual delivery, observation, and reaction | separate typed artifacts and owner assertions |
| No stale-proposal guard | policy inputs are not bound to live watermark | require exact input snapshot and observation watermark match |
| No replay contract | current mutable state is authoritative | deterministic fold from genesis/checkpoint plus immutable events |
| No invalidation projection | historical status changes are overwrite-like | append invalidation/revocation and recompute affected projections |
| No receipt parity check | independent dictionaries may diverge | repository invariant verifies command/event/snapshot/receipt parity |
| Combined product responsibilities | workflow spans source, extraction, review, routing, package planning | isolate live Interview Expression aggregate and reference other products/specs |

### 4.3 Brownfield reuse boundary

Names and test intents may be reused only when their semantics match. Existing random UUID/time generation, mutable row authority, sequential persistence, broad orchestration, and combined product authority are explicitly not normative. No existing code is modified by this writing task.

## 5. Proposed architecture and workflows

### 5.1 Component boundary

The future Interview Expression implementation should separate six responsibilities:

| Component | Responsibility | Must not do |
|---|---|---|
| `LiveSessionCommandService` | authenticate, authorize, normalize, fingerprint, idempotency-check, concurrency-check, and dispatch one command | persist partial state or make semantic-policy decisions |
| `LiveSessionDomain` | validate invariants and derive immutable events/snapshots/receipts from a command and prior state | call clocks, random generators, filesystems, networks, or model providers |
| `LiveSessionRepository` | atomically append command, events, snapshot, receipt, and checkpoint metadata | accept receipt-only or state-only writes |
| `LiveStateProjector` | deterministically fold valid events into a current or historical projection | reinterpret AIR meaning or invent missing evidence |
| `AIRPolicyGateway` | verify and retrieve hash-pinned AIR-008/AIR-009 artifacts | mark proposals delivered, mutate AIR artifacts, or bypass compatibility |
| `LiveEvidenceGateway` | resolve source/transcript/recording/operator evidence refs subject to tenancy and retention | promote provisional observations to historical truth by retrieval alone |

The domain core takes only canonical values and explicit configuration. External gateways run before domain evaluation or after committed outcomes. A model provider may propose observations through a separately typed `MODEL_INFERRED` input; it never invokes a human-only command.

### 5.2 Aggregate and projection topology

One `LiveActivativeSession` stream is keyed by `(organization_id, brand_id, live_session_id)`. It binds exactly one immutable Interview Asset Contract version and one active source-package scope at a time. Its append sequence begins at zero and increases by one per stored event. A command can emit multiple adjacent events, but their order is fixed in the outcome receipt.

The current projection is an optimization, not authority. It contains the hash of the exact genesis inputs and ordered event hashes used. A historical read at sequence `n` folds only effective events through `n`, applying invalidation records according to their declared scope and effective sequence. A checkpoint is usable only when its input prefix hash matches the event store.

### 5.3 Start-live-session workflow

1. Accept `StartLiveActivationLoop` with caller-supplied deterministic command ID, idempotency key, expected nonexistence, organization/brand scope, authorized human actors, IAC ref/hash, armed-binding ref/hash, source-package ref/hash, compatibility profile, and canonical logical time token.
2. Resolve AIR-008 inputs by exact immutable reference and verify their content hashes, source kind, provenance minimums, locks, planned branch set, pressure envelope, landing/recovery routes, and feature requirements.
3. Verify that the binding is `ARMED`, not superseded/revoked, and belongs to the same organization/brand/source scope.
4. Reject any missing or guessed source kind, ambiguous actor authority, nonportable URI, stale IAC/binding, or absent stop/landing route.
5. Derive `LiveSessionStarted` and initial `LiveActivativeStateSnapshot(sequence=1)` deterministically.
6. Atomically commit the command, event, snapshot, success receipt, and projection checkpoint.
7. Return the receipt and snapshot refs. A retry with the same fingerprint returns the same outcome. The same idempotency key with different normalized input returns `IDEMPOTENCY_KEY_REUSED`.

The initial snapshot uses only the armed IAC and binding. It does not claim a reaction, observation, delivered call, or anchor hit. Such fields are typed `NOT_APPLICABLE` or `UNKNOWN` according to their meaning, not omitted.

### 5.4 AIR policy acknowledgement workflow

`AcknowledgeAIRPolicyProposal` records that an authorized operator/interviewer has made a specific AIR-009 proposal portfolio available to this session. It does not advance live state by itself.

Validation requires:

- exact proposal ID, version, content hash, and AIR authority owner;
- exact IAC and armed-binding identity/hash match;
- exact `input_live_state_snapshot_ref` and `input_observation_watermark` equal to the current effective projection;
- required feature set and compatibility profile supported by the consumer;
- each call option within the bound branch, locks, pressure ceiling, and lawful transition set;
- continue/deepen choices accompanied by reset/land/stop alternatives as required by the IAC;
- every counteractivation statement labeled hypothesis, with evidence and disconfirmation routes;
- no field that asserts actual delivery, actual reaction, or actual state transition.

On success, the aggregate emits `AIRPolicyProposalAcknowledged`. A late or stale proposal emits no success event; it receives a typed denial receipt with current snapshot/watermark refs so AIR may recompute. No adapter may silently retarget a proposal to a newer state.

### 5.5 Interviewer-reaction workflow

`RecordInterviewerReaction` is a human-only command. The authenticated actor must equal the asserted interviewer or exercise an explicit transcription-on-behalf grant whose receipt is included. The command contains:

- a governed reaction kind (`CURIOSITY`, `RECOGNITION`, `UNCERTAINTY`, `DISBELIEF`, `CONCERN`, `STAKE`, `RELATIONAL_SHIFT`, `OTHER_ATTESTED`);
- the interviewer's own bounded statement or an attributable faithful transcription;
- whether it changes the next useful call (`YES`, `NO`, `UNKNOWN`);
- optional source evidence refs and a required evidence-availability state;
- event watermark observed by the interviewer;
- superseded reaction-state ref when replacing a prior operative reaction;
- explicit consent/sensitivity flags required by the current source package.

The domain rejects model-authored text submitted as human-attested, empty `OTHER_ATTESTED` detail, stale watermarks, cross-session evidence, and reaction states that overwrite rather than supersede prior state. It emits `InterviewerReactionRecorded` and, if operative, a new snapshot. A reaction marked `NO` can be preserved as evidence without changing the next-call context. A reaction marked `UNKNOWN` cannot be used as a positive policy constraint until clarified.

Machine observations such as vocal change or transcript pattern use `AppendLiveObservationSignal` with `MODEL_INFERRED` or `DIRECTLY_OBSERVED`, never `RecordInterviewerReaction`. They may prompt the human for confirmation but cannot become interviewer reaction automatically.

### 5.6 Delivered-call workflow

`RecordDeliveredActivativeCall` records the speech act that actually occurred. The authorized human provides one origin:

- `AIR_PROPOSAL_SELECTED`: exact acknowledged proposal and call-option ref/hash;
- `HUMAN_ADAPTED_FROM_AIR`: proposal/call ref plus exact delivered language and bounded adaptation reason;
- `SPONTANEOUS_HUMAN`: no false AIR call ref; an optional contextual proposal ref may state what was available but not selected;
- `OPERATOR_TRANSCRIBED`: exact interviewer actor and transcription authority receipt;
- `NOT_APPLICABLE` only for a nonverbal governed action whose action kind and evidence are present.

The command also carries the actual human pressure decision, branch, semantic-lock acknowledgement, delivery evidence state/reference, and expected projection sequence/hash. The pressure decision may be lower than AIR's recommendation. It may not exceed the IAC ceiling or weaken a lock. If the human deliberately departs from an AIR proposal within the IAC boundary, the record preserves the divergence rather than rewriting either artifact.

Acceptance emits `ActivativeCallDelivered`. It does not itself assert guest reaction or anchor hit. When the delivery changes the operational projection, it is followed in the same atomic command outcome by `LiveStateAdvanced` and a new snapshot. If evidence for a delivered call is temporarily unavailable, the event may be `HUMAN_ATTESTED` with a declared evidence gap; it cannot be mislabeled `DIRECTLY_OBSERVED`.

### 5.7 Observation and state-advance workflow

`AppendLiveObservationSignal` records a bounded signal tied to a transcript span, recording interval, direct operator observation, guest statement, or model inference. It requires an epistemic state and does not make a terminal semantic conclusion.

`AdvanceLiveActivativeState` takes the current expected version plus exact event/evidence refs and proposes changes to governed projection fields. The domain validates each delta:

- `current_expression_state` and `target_distance` must use the bound profile and include authority/evidence;
- anchor status can become `HIT` only with an eligible observation/ref and cannot be inferred from call delivery alone;
- landing status can become `LANDED` only with required evidence and human acknowledgement;
- pressure history derives only from actual delivered-call pressure decisions;
- relationship condition distinguishes observation, interviewer reaction, and AIR hypothesis;
- available next actions are the intersection of IAC constraints, acknowledged AIR proposal options, human stop authority, and current session status;
- no resolved/contested observation is silently overwritten;
- no snapshot can skip an accepted event sequence.

The command emits `LiveStateAdvanced`, an immutable snapshot, and a `LiveStateTransitionReceipt`. If supplied deltas equal the canonical projection, the command returns a deterministic `NO_EFFECT` receipt without creating an artificial transition event.

### 5.8 Pause, reset, land, stop, cancel, and fail workflows

- `PauseLiveActivationLoop` prevents call-delivery and policy-acknowledgement commands but permits evidence completion, replay, and authorized stop/cancel.
- `ResumeLiveActivationLoop` requires a non-stale expected version and revalidates binding, source availability, compatibility, and active constraints.
- `ResetLiveActivationLoop` records the human reset decision and selects an IAC-authorized recovery/reset route. It preserves prior pressure and reactions; it does not erase them.
- `LandLiveActivationLoop` records the human landing action, landing evidence, unresolved observations, and disposition. `LANDED` is not equivalent to `SUCCESSFUL_OUTCOME`; full outcome belongs to the Reaction Receipt flow.
- `StopLiveActivationLoop` records an authorized stop with a governed reason. It remains lawful regardless of AIR recommendations.
- `CancelLiveActivationLoop` records cancellation, whether before or after any call, and the effect on pending proposals/commands.
- `FailLiveActivationLoop` is an operational terminal path with error context. It does not imply semantic failure by the guest/interviewer.

All paths append events and preserve historical replay. A terminal state rejects new delivery/advance commands. Late evidence may be attached only through a governed post-terminal evidence command that does not reopen the session; reopening requires a new version/session under an authorized rule.

### 5.9 Replay and historical reproduction workflow

`ReplayLiveActivationLoop` is read-only. The caller supplies organization/brand/session, target sequence or receipt ref, and optional invalidation-view cutoff. The repository:

1. verifies tenant scope and read authority;
2. resolves the genesis IAC/binding/source refs and their historical bytes;
3. loads ordered immutable events and applicable invalidation records;
4. validates every content hash and sequence link;
5. folds through the pure projector with the pinned ruleset/profile;
6. compares the computed projection hash with the stored snapshot/checkpoint when one exists;
7. returns the state plus a `ReplayVerification` result.

Unavailable historical bytes produce `HISTORICAL_INPUT_UNAVAILABLE`, never reconstruction from current files. Invalidated or revoked artifacts remain readable to an authorized auditor with their invalidation state; they are not available for current consumption.

### 5.10 Command-processing sequence

For every mutating command:

1. parse strictly; reject unknown enum/field values where the version forbids them;
2. authenticate and tenant-scope before content resolution;
3. normalize Unicode, line endings, set/map ordering, decimal forms, and portable references;
4. calculate `command_fingerprint = sha256(canonical_command_without_transport_metadata)`;
5. return the prior outcome for an exact idempotent retry;
6. load the current effective aggregate and expected projection;
7. check expected sequence/hash and active invalidations;
8. resolve hash-pinned dependencies and compatibility features;
9. authorize the actor for the exact command;
10. derive events/snapshot/receipt without I/O;
11. atomically compare-and-append the entire outcome;
12. return committed refs and hashes.

No retry loop may silently rebase a semantic command. A concurrency conflict returns the current version so a human/system can re-evaluate intent.

## 6. Data models, contracts, schemas, and APIs

All models in this section are proposed future implementation contracts. They are not canonical schemas or released contract bytes. Exact field names should remain stable through audit; changes require versioning and migration review.

### 6.1 Common primitives

```text
PortableRef:
  artifact_kind: governed string
  artifact_id: non-empty portable identifier
  version: non-empty immutable version
  sha256: lowercase 64-hex digest
  authority_owner: governed product/actor identifier
  repository_relative_path: relative normalized path | NOT_APPLICABLE
  external_locator: governed opaque locator | NOT_APPLICABLE

ActorAssertion:
  actor_id: non-empty identifier
  actor_role: governed role
  authority_grant_ref: PortableRef
  assertion_kind: HUMAN_ATTESTED | OPERATOR_TRANSCRIBED | SYSTEM_OBSERVED
  asserted_at_logical_time: LogicalTime

LogicalTime:
  session_tick: non-negative integer
  source_timecode: canonical decimal seconds | NOT_APPLICABLE
  wall_clock_observed_at: RFC3339 string | NOT_APPLICABLE  # metadata; excluded from identity/hash ordering

EvidenceRef:
  evidence_id: non-empty identifier
  evidence_kind: TRANSCRIPT_SPAN | RECORDING_INTERVAL | GUEST_STATEMENT | INTERVIEWER_ATTESTATION |
                 OPERATOR_OBSERVATION | MODEL_OBSERVATION | SOURCE_PACKAGE_MEMBER
  artifact_ref: PortableRef
  selector: canonical typed selector
  epistemic_state: HUMAN_ATTESTED | DIRECTLY_OBSERVED | MODEL_INFERRED | HYPOTHESIZED |
                   CONTESTED | RESOLVED | UNKNOWN | NOT_APPLICABLE
  sensitivity_class: governed value
```

Absolute drive paths, `file://` URLs, process-local object addresses, and unresolved repository roots are forbidden in a portable ref. Either relative path or external locator can be `NOT_APPLICABLE`; both cannot be unavailable when the evidence is required.

### 6.2 `LiveActivativeSession`

```text
LiveActivativeSession:
  live_session_id: stable caller-supplied identifier
  organization_id: required
  brand_id: required
  source_authority_id: required
  interviewer_actor_ids: non-empty ordered set
  operator_actor_ids: ordered set
  interview_asset_contract_ref: PortableRef
  armed_binding_ref: PortableRef
  source_package_ref: PortableRef
  compatibility_profile_id: required
  required_feature_ids: canonical sorted set
  ruleset_ref: PortableRef
  status: ARMED_NOT_STARTED | LIVE | PAUSED | RESETTING | LANDED | STOPPED | CANCELLED | FAILED
  current_sequence: non-negative integer
  current_event_watermark: lowercase digest
  current_snapshot_ref: PortableRef | NOT_APPLICABLE
  supersession_state: CURRENT | SUPERSEDED | INVALIDATED | REVOKED
```

Invariants:

- the three controlling AIR/source refs are immutable and tenant-compatible;
- exactly one status is active;
- `LIVE`, `PAUSED`, and `RESETTING` require a snapshot;
- terminal statuses cannot return to `LIVE` in the same session version;
- the current sequence and watermark equal the committed effective event prefix;
- revoked/superseded dependencies block new commands but not historical reads.

### 6.3 `LiveActivativeStateSnapshot`

```text
LiveActivativeStateSnapshot:
  snapshot_id: deterministic identifier
  live_session_id: required
  sequence: positive integer
  previous_snapshot_ref: PortableRef | NOT_APPLICABLE
  event_watermark: lowercase digest
  input_event_refs: non-empty canonical ordered list[PortableRef]
  iac_ref: PortableRef
  armed_binding_ref: PortableRef
  active_branch_id: governed identifier
  current_expression_state: StateAssertion
  target_expression_state_ref: PortableRef
  target_distance: TargetDistanceAssertion
  anchor_statuses: canonical map[anchor_id, AnchorState]
  landing_status: LandingState
  operative_interviewer_reaction_ref: PortableRef | NOT_APPLICABLE
  recent_observation_refs: canonical ordered list[PortableRef]
  actual_pressure_history: canonical ordered list[PressureDoseDecisionRef]
  recent_delivered_call_refs: canonical ordered list[PortableRef]
  relationship_condition: StateAssertion
  active_counteractivation_hypothesis_refs: canonical ordered list[PortableRef]
  acknowledged_air_policy_refs: canonical ordered list[PortableRef]
  available_next_actions: canonical sorted set[CONTINUE | DEEPEN | RESET | LAND | STOP]
  unresolved_assertion_refs: canonical ordered list[PortableRef]
  active_wrong_reading_lock_refs: non-empty canonical ordered list[PortableRef]
  projection_ruleset_ref: PortableRef
  canonical_payload_sha256: lowercase digest
```

`StateAssertion` contains a governed value, epistemic state, asserting owner, evidence refs, confidence representation if governed by the profile, and `valid_for_event_watermark`. Generic notes cannot substitute for these fields.

`TargetDistanceAssertion` records profile ID/version, dimension values, calculation owner, evidence, and epistemic state. No ungoverned numeric threshold is invented here. Until a ratified profile exists, a typed qualitative distance with exact profile ref is required.

`AnchorState` is `UNOBSERVED`, `PARTIAL`, `HIT`, `CONTESTED`, `REVOKED`, or `NOT_APPLICABLE`; every non-initial state has evidence and transition refs. `LandingState` is `NOT_STARTED`, `AVAILABLE`, `IN_PROGRESS`, `LANDED`, `FAILED_TO_LAND`, `CONTESTED`, or `NOT_APPLICABLE` with analogous evidence.

### 6.4 `InterviewerReactionState`

```text
InterviewerReactionState:
  reaction_state_id: deterministic identifier
  live_session_id: required
  interviewer_actor_id: required
  reaction_kind: CURIOSITY | RECOGNITION | UNCERTAINTY | DISBELIEF | CONCERN | STAKE |
                 RELATIONAL_SHIFT | OTHER_ATTESTED
  bounded_statement: non-empty human assertion
  affects_next_useful_call: YES | NO | UNKNOWN
  epistemic_state: HUMAN_ATTESTED
  actor_assertion: ActorAssertion
  evidence_refs: canonical ordered list[EvidenceRef]
  evidence_availability: PRESENT | HUMAN_ATTESTATION_ONLY | TEMPORARILY_UNAVAILABLE
  observed_event_watermark: lowercase digest
  supersedes_reaction_state_ref: PortableRef | NOT_APPLICABLE
  sensitivity_class: governed value
  canonical_payload_sha256: lowercase digest
```

Only `HUMAN_ATTESTED` is legal in this artifact. Model and operator observations use separate signal artifacts. Empty evidence is lawful only with `HUMAN_ATTESTATION_ONLY` or `TEMPORARILY_UNAVAILABLE`; it never upgrades to direct observation. A later correction supersedes and links the prior artifact.

### 6.5 `LiveObservationSignal`

```text
LiveObservationSignal:
  signal_id: deterministic identifier
  live_session_id: required
  signal_kind: VERBAL_CONTENT | VOCAL_CHANGE | SOMATIC_CUE | SILENCE | CONTRADICTION |
               ANCHOR_CANDIDATE | LANDING_CANDIDATE | RELATIONAL_CUE | OTHER_GOVERNED
  normalized_observation: bounded non-empty value
  epistemic_state: DIRECTLY_OBSERVED | MODEL_INFERRED | HYPOTHESIZED | CONTESTED | UNKNOWN
  asserting_owner: human, operator, or system owner
  evidence_refs: non-empty canonical ordered list[EvidenceRef] unless epistemic state is UNKNOWN
  event_watermark_context: lowercase digest
  resolution_state: OPEN | CONFIRMED | CONTESTED | RESOLVED | INVALIDATED
  canonical_payload_sha256: lowercase digest
```

The signal is descriptive evidence, not a Reaction Receipt, target-state conclusion, diagnosis, or personal-truth override.

### 6.6 `DeliveredActivativeCallRecord` and pressure decision

```text
DeliveredActivativeCallRecord:
  delivered_call_id: deterministic identifier
  live_session_id: required
  interviewer_actor_id: required
  call_origin: AIR_PROPOSAL_SELECTED | HUMAN_ADAPTED_FROM_AIR | SPONTANEOUS_HUMAN |
               OPERATOR_TRANSCRIBED | NONVERBAL_GOVERNED_ACTION
  air_policy_proposal_ref: PortableRef | NOT_APPLICABLE
  air_call_option_ref: PortableRef | NOT_APPLICABLE
  exact_delivered_expression: non-empty text | NOT_APPLICABLE
  nonverbal_action_kind: governed value | NOT_APPLICABLE
  adaptation_reason: governed bounded text | NOT_APPLICABLE
  branch_id: required
  pressure_decision_ref: PortableRef
  lock_acknowledgement_refs: non-empty canonical ordered list[PortableRef]
  actor_assertion: ActorAssertion
  delivery_evidence_refs: canonical ordered list[EvidenceRef]
  evidence_availability: PRESENT | HUMAN_ATTESTATION_ONLY | TEMPORARILY_UNAVAILABLE
  logical_time: LogicalTime
  canonical_payload_sha256: lowercase digest

PressureDoseDecision:
  pressure_decision_id: deterministic identifier
  live_session_id: required
  human_decision_maker_id: required
  air_recommendation_ref: PortableRef | NOT_APPLICABLE
  selected_dose_profile_id: required
  selected_dose_value: governed profile value
  iac_ceiling_ref: PortableRef
  decision: FOLLOW_RECOMMENDATION | LOWER_THAN_RECOMMENDED | HUMAN_SELECTED_WITHOUT_RECOMMENDATION |
            RESET | LAND | STOP
  rationale: bounded human assertion | NOT_APPLICABLE
  within_ceiling: true
  canonical_payload_sha256: lowercase digest
```

For AIR-derived origins, proposal and option refs are required and must already be acknowledged. For spontaneous human origins, both AIR refs are `NOT_APPLICABLE`; a contextual availability ref, if retained, cannot imply selection. A decision above ceiling is not representable as an accepted record.

### 6.7 AIR proposal consumption view

Interview Expression stores an immutable consumption view rather than mutating AIR output:

```text
AcknowledgedAIRPolicy:
  acknowledgement_id: deterministic identifier
  live_session_id: required
  proposal_ref: PortableRef
  iac_ref: PortableRef
  binding_ref: PortableRef
  input_live_state_snapshot_ref: PortableRef
  input_observation_watermark: lowercase digest
  compatibility_profile_id: required
  verified_feature_ids: canonical sorted set
  acknowledgement_status: AVAILABLE | STALE | SUPERSEDED | INVALIDATED
  acknowledged_by: ActorAssertion
  canonical_payload_sha256: lowercase digest
```

`AVAILABLE` means available for human consideration, not accepted semantic truth and not delivered. If the live state advances before selection, the proposal becomes `STALE`; it is never silently rebound.

### 6.8 Events

Every event has `event_id`, `event_type`, tenant/session scope, sequence, previous-event hash, command ref, actor ref, logical time, payload, payload hash, ruleset ref, and event hash. Event types are:

- `LiveSessionStarted`;
- `AIRPolicyProposalAcknowledged`;
- `InterviewerReactionRecorded`;
- `LiveObservationSignalAppended`;
- `ActivativeCallDelivered`;
- `LiveStateAdvanced`;
- `LiveLoopPaused`;
- `LiveLoopResumed`;
- `LiveLoopReset`;
- `LiveLoopLanded`;
- `LiveLoopStopped`;
- `LiveLoopCancelled`;
- `LiveLoopFailed`;
- `LiveArtifactInvalidated`;
- `LiveArtifactSuperseded`;
- `PostTerminalEvidenceAttached`.

Event payload schemas are versioned. Unknown event versions block projection. Projectors do not skip unknown events to achieve availability.

### 6.9 Commands and command records

Mutating command contracts are:

- `StartLiveActivationLoop`;
- `AcknowledgeAIRPolicyProposal`;
- `RecordInterviewerReaction`;
- `AppendLiveObservationSignal`;
- `RecordDeliveredActivativeCall`;
- `AdvanceLiveActivativeState`;
- `PauseLiveActivationLoop`;
- `ResumeLiveActivationLoop`;
- `ResetLiveActivationLoop`;
- `LandLiveActivationLoop`;
- `StopLiveActivationLoop`;
- `CancelLiveActivationLoop`;
- `FailLiveActivationLoop`;
- `InvalidateLiveArtifact`;
- `AttachPostTerminalEvidence`.

Each command includes:

```text
command_id
command_type
command_schema_version
idempotency_key
organization_id
brand_id
live_session_id
actor_assertion
expected_sequence
expected_projection_sha256
logical_time
payload
```

The persisted `CommandRecord` adds normalized command hash, authorization decision ref, dependency refs/hashes, outcome receipt ref/hash, processing state, and committed event refs. A denial or conflict still has a command record and outcome receipt unless authentication fails before tenant-safe recording is allowed; in that case a security audit record is produced outside the semantic stream.

### 6.10 Outcome and transition receipts

```text
LiveCommandOutcomeReceipt:
  receipt_id: deterministic identifier
  command_ref: PortableRef
  outcome: APPLIED | NO_EFFECT | DENIED | CONFLICT | CANCELLED | FAILED
  error_code: governed code | NOT_APPLICABLE
  error_context: redacted structured context | NOT_APPLICABLE
  prior_snapshot_ref: PortableRef | NOT_APPLICABLE
  committed_event_refs: canonical ordered list[PortableRef]
  resulting_snapshot_ref: PortableRef | NOT_APPLICABLE
  atomic_commit_id: deterministic identifier | NOT_APPLICABLE
  canonical_payload_sha256: lowercase digest

LiveStateTransitionReceipt:
  transition_receipt_id: deterministic identifier
  live_session_id: required
  from_snapshot_ref: PortableRef
  to_snapshot_ref: PortableRef
  causative_command_ref: PortableRef
  causative_event_refs: non-empty ordered list[PortableRef]
  evidence_refs: canonical ordered list[EvidenceRef]
  human_decision_refs: canonical ordered list[PortableRef]
  air_proposal_refs: canonical ordered list[PortableRef]
  applied_constraint_refs: non-empty ordered list[PortableRef]
  unresolved_assertion_refs: canonical ordered list[PortableRef]
  canonical_payload_sha256: lowercase digest
```

Receipt IDs derive from canonical content and namespace, never clock or randomness. A receipt cannot exist without its referenced command and committed artifacts; a state-changing event cannot exist without a transition receipt.

### 6.11 Repository contract and atomicity

```text
LiveSessionRepository:
  load_effective(session_scope, at_sequence?) -> AggregateView
  find_command_outcome(session_scope, idempotency_key) -> CommandOutcome | NOT_FOUND
  compare_and_append(
      expected_sequence,
      expected_projection_sha256,
      command_record,
      events,
      snapshot_or_not_applicable,
      outcome_receipt,
      transition_receipt_or_not_applicable
  ) -> CommitResult
  replay(session_scope, target_sequence, invalidation_cutoff?) -> ReplayResult
  verify_parity(session_scope) -> ParityReport
```

`compare_and_append` is all-or-nothing. The repository must reject:

- state without command/receipt;
- receipt without command;
- event without command;
- transition event without snapshot and transition receipt;
- snapshot whose event watermark or sequence does not match the appended prefix;
- outcome receipt whose artifact list differs from the write batch;
- duplicate idempotency key with a different command hash;
- sequence/hash mismatch.

An in-memory repository used in tests must implement exactly the same invariant checks and atomic visibility as the durable adapter. It cannot be a permissive dictionary substitute.

### 6.12 Canonical serialization and hashing

Canonical payloads use UTF-8, Unicode NFC, LF line endings, lexicographically sorted object keys, declared list ordering, sorted-set normalization, canonical decimal strings, lowercase enum values only if the schema defines them, and no insignificant whitespace. Map insertion order and filesystem enumeration order never affect bytes. Wall-clock metadata, hostnames, absolute paths, process IDs, random seeds, memory addresses, and environment variables are excluded from canonical identity.

```text
artifact_hash = SHA-256(canonical_json(artifact_without_hash_and_nonidentity_metadata))
event_hash = SHA-256(domain_separator || previous_event_hash || canonical_event_payload)
projection_hash = SHA-256(ruleset_hash || genesis_hash || ordered_effective_event_hashes)
command_fingerprint = SHA-256(domain_separator || canonical_normalized_command)
```

The domain separator includes product, artifact kind, and schema version. Identifiers derived from hashes are stable across machines and fresh processes. Hash collisions are fatal and observable; the system never substitutes a new random ID.

### 6.13 Read APIs

Future product APIs may expose:

- `GET /live-activation-sessions/{id}` current effective projection;
- `GET /live-activation-sessions/{id}/snapshots/{sequence}` historical projection;
- `GET /live-activation-sessions/{id}/events?after_sequence=` authorized ordered events;
- `GET /live-activation-sessions/{id}/receipts/{receipt_id}` exact receipt;
- `GET /live-activation-sessions/{id}/replay-verification?sequence=` deterministic verification;
- `GET /live-activation-sessions/{id}/available-actions` human-facing lawful action set.

Responses include artifact version/hash, projection watermark, authority owner, epistemic state, invalidation/supersession state, and redaction markers. APIs must not flatten these into generic notes.

### 6.14 Failure taxonomy

| Code | Meaning | Retry semantics |
|---|---|---|
| `AUTHORITY_DENIED` | actor lacks exact command authority | do not retry unchanged |
| `TENANT_SCOPE_MISMATCH` | organization/brand/session or artifact scope differs | do not disclose foreign content |
| `STALE_PROJECTION` | expected sequence/hash differs | reload and require intent re-evaluation |
| `STALE_AIR_POLICY` | proposal inputs do not equal current snapshot/watermark | request recomputation; never retarget |
| `DEPENDENCY_HASH_MISMATCH` | immutable upstream bytes differ | block and investigate |
| `UNSUPPORTED_COMPATIBILITY_FEATURE` | required semantic feature absent | block; no parse-only fallback |
| `IDEMPOTENCY_KEY_REUSED` | same key, different command fingerprint | reject and alert |
| `FABRICATED_HUMAN_REACTION` | nonhuman inference submitted as genuine reaction | reject and audit |
| `DELIVERY_PROVENANCE_INVALID` | origin/ref/evidence combination is contradictory | reject |
| `PRESSURE_CEILING_EXCEEDED` | human or system input exceeds IAC ceiling | reject; preserve attempt receipt |
| `LOCK_WEAKENING_ATTEMPT` | inherited semantic lock is removed/weakened | reject and alert |
| `MISSING_STOP_OR_LANDING_ROUTE` | no lawful de-escalation/termination route | reject session/proposal |
| `EVIDENCE_SCOPE_MISMATCH` | evidence belongs to another scope/version | reject |
| `EVENT_RECEIPT_PARITY_FAILURE` | stored artifacts disagree | quarantine write/read path |
| `HISTORICAL_INPUT_UNAVAILABLE` | exact historical dependency bytes cannot be resolved | fail replay explicitly |
| `UNKNOWN_EVENT_VERSION` | projector cannot interpret an event | stop projection; require migration/adoption |
| `TERMINAL_STATE_CONFLICT` | command attempts prohibited mutation after terminal state | reject |
| `ATOMIC_COMMIT_FAILED` | no full batch committed | safe exact retry with same idempotency key |

Error context includes safe IDs, versions, expected/observed hashes, authority decision ref, failing invariant, and correlation ID. It excludes sensitive source content unless the caller has explicit evidence-read authority.

## 7. Implementation stages and exact target paths

This section defines a later, bounded implementation sequence. It authorizes nothing in the present prompt. No listed path is created now.

### 7.1 Proposed future paths

```text
06_INTERVIEW_EXPRESSION/
  src/interview_expression/
    live_state/models.py
    live_state/commands.py
    live_state/events.py
    live_state/receipts.py
    live_state/domain.py
    live_state/projector.py
    live_state/repository.py
    live_state/service.py
    live_state/errors.py
    live_state/canonicalization.py
    integrations/air_policy_gateway.py
    integrations/live_evidence_gateway.py
  tests/
    unit/live_state/
    contract/live_state/
    integration/live_state/
    adversarial/live_state/
    replay/live_state/
```

Exact final locations remain subject to ratification, repository instructions, accepted architecture, and a separately issued Development Capsule.

### 7.2 Staged implementation plan

| Stage | Deliverable | Entry gate | Exit evidence |
|---|---|---|---|
| 1 | Pure canonicalization, common refs, errors, event and receipt models | ratified/adopted authority; accepted spec; capsule | golden-byte and cross-process hash fixtures |
| 2 | Aggregate commands, invariants, pure event derivation, projector | Stage 1 accepted interfaces | unit/property tests for every transition and forbidden path |
| 3 | In-memory repository with atomic/parity semantics | Stage 2 | fault-injection, idempotency, concurrency, and replay parity tests |
| 4 | Durable adapter and transaction boundary | accepted persistence decision | rollback/crash/restart/historical reproduction evidence |
| 5 | AIR gateways using adopted, versioned interfaces | AIR-008/AIR-009 independently accepted and adopted | stale proposal, compatibility, hash drift, and authority tests |
| 6 | Evidence integration and post-terminal behavior | accepted evidence/source contracts | tenant, retention, redaction, provisional-truth tests |
| 7 | Vertical session proof | upstream/downstream adopted specs | deterministic fresh-context run with start, call, observation, reaction, reset/land/stop, replay |

No stage may start because this spec is merely written. AIR draft state cannot be promoted by an Interview Expression implementation. Full Reaction Receipt integration waits for `TS-INT-006`; source/capture and other downstream specs retain their own gates.

### 7.3 Architecture import boundaries

- domain models and projector import no service, repository adapter, web framework, provider SDK, filesystem, or clock/random module;
- services depend on domain and abstract ports;
- adapters depend inward on ports/models, never the reverse;
- product code may consume adopted AIR/Delegation contracts but may not copy schemas into local forks;
- tests may use builders/fakes, but fakes must enforce the same atomic and compatibility constraints;
- Studio may project or correct through adopted APIs; Interview Expression does not import Studio service code as authority.

### 7.4 Completion artifacts for a later build

A future implementation completion package must include source manifest, exact hashes, tests, coverage by requirement/invariant, architecture-boundary result, dependency/adoption receipts, migration/rollback proof, replay proof, deterministic fresh-process proof, security/tenancy proof, and a claim-ceiling receipt. It must not be confused with this writing receipt.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Failure handling principles

The system fails closed on authority, tenant scope, semantic compatibility, evidence classification, hash integrity, and event/receipt parity. It may degrade operationally only when the degraded state is explicit and cannot be mistaken for semantic success. For example, unavailable recording evidence may leave a human-attested delivery record with an evidence gap, but it cannot be relabeled directly observed; an unavailable AIR provider may leave the human with IAC-authorized reset/land/stop routes, but it cannot manufacture a policy proposal.

Every failure belongs to one of four boundaries:

1. **Pre-record security failure** — authentication/tenant failure before semantic content can be safely recorded; write a minimal operational security event outside the session stream.
2. **Recorded denial/conflict** — parse, authority, compatibility, stale version, pressure, lock, or terminal-state denial; persist command outcome where safe, with no semantic state event.
3. **Atomic persistence failure** — transaction produces no visible artifact; exact retry is safe.
4. **Post-commit delivery failure** — committed outcome exists but response/notification failed; retry resolves the existing idempotent outcome rather than writing again.

### 8.2 Atomic rollback

The repository transaction boundary includes the command record, all derived events, snapshot, transition receipt if applicable, outcome receipt, stream head, and checkpoint metadata. Failure at any internal write point rolls back all components. Tests must inject failure before and after each write operation and prove:

- no new stream head becomes visible;
- no artifact can be read by ID;
- the idempotency index is not reserved without a retrievable outcome;
- a retry produces the same canonical bytes and hashes;
- an existing successful commit is returned unchanged after response loss.

For stores without native multi-record transactions, the implementation must use an accepted atomic append protocol with a commit marker and readers that expose only committed batches. This specification does not select that architecture.

### 8.3 Optimistic-concurrency recovery

A command with stale sequence or projection hash returns `STALE_PROJECTION` and the current safe head reference. The service does not automatically rebase, replay the command against new state, or select another AIR call. The authorized actor must inspect the changed context and resubmit a new command with a new command ID/idempotency key. An exact transport retry uses the original key and receives its original outcome.

Concurrent examples that must remain lawful:

- reaction and observation commands against the same head: exactly one commits; the other re-evaluates;
- stop racing with delivered call: ordering decides; if stop commits first, delivery is rejected; if delivery commits first, stop may still append next;
- reset racing with late AIR proposal: reset commits and advances watermark; proposal is stale;
- evidence attachment racing with invalidation: both histories remain attributable and the effective projection follows sequence/invalidation law.

### 8.4 Invalidation, supersession, and revocation

Invalidation is additive. `InvalidateLiveArtifact` records:

- invalidated artifact ref/hash;
- reason and authority decision ref;
- scope (`ARTIFACT_ONLY`, `DESCENDANTS`, `PROJECTION_FROM_SEQUENCE`, or governed selective set);
- effective sequence/time;
- whether current consumption is blocked;
- required replacement ref or `NOT_APPLICABLE`;
- affected descendant refs computed from recorded lineage.

The system calculates descendants through explicit lineage edges: proposal -> acknowledgement -> delivered call (if selected) -> transition -> snapshot -> downstream receipt references. It must not invalidate unrelated spontaneous-human delivery merely because an AIR proposal was present. A parent IAC/binding revocation blocks current operation and invalidates dependent current projections according to the authority decision, while retaining historical bytes.

Supersession provides a newer immutable artifact and link; it never edits old bytes. Revocation prevents current use. Historical replay can select the as-observed historical view or the later governed effective view, and must label which view was requested.

### 8.5 Historical reproducibility

Reproduction requires the exact event bytes, ruleset, schemas, IAC, armed binding, AIR proposal inputs, compatibility profile, and referenced evidence metadata that affected projection. Mutable source-manifest drift is not treated as corruption when the historically distributed bytes and content hashes remain available. Conversely, a current file with the same path but different bytes cannot satisfy an immutable historical ref.

Replay validation compares:

- sequence continuity and previous-event hashes;
- event payload hashes;
- artifact availability and content hashes;
- ruleset/profile identity;
- invalidation-view choice;
- computed snapshot/projection hash;
- stored transition and outcome receipt refs.

Any mismatch returns a typed nonconformance report. The projector never repairs history during read.

### 8.6 Migration from brownfield session records

Migration creates a new immutable imported stream; it never mutates source records or pretends the predecessor emitted the new artifacts. Every imported session receives a `LegacyMigrationReceipt` containing source system/version, source record IDs/hashes, exporter/importer versions, mapping ruleset hash, omissions, unresolved fields, and output stream hash.

Migration rules:

- organization, brand, session, actor, status, and exact available receipt/event evidence may map when attributable;
- random predecessor IDs remain legacy IDs and are linked, not recomputed as if content-addressed;
- wall-clock timestamps remain observation metadata and do not become logical sequence identity;
- missing IAC, armed binding, source kind, reaction, delivered-call provenance, pressure, or live-state history is `UNKNOWN` or blocks import where required;
- migrations never guess source classification or reconstruct calls/reactions from generic notes;
- a predecessor `closed` state does not automatically mean `LANDED` or successful reaction;
- imported mutable snapshots are evidence artifacts, not equivalent to a verified event-derived projection;
- partial mappings are quarantined `LEGACY_IMPORTED_UNRESOLVED` and cannot enter a current live loop;
- lossless migration is proven by source-to-output field accounting; otherwise migration is explicitly blocked or bounded with named omissions.

No migration runs during Prompt 03.

### 8.7 Adapter compatibility and parse-without-enforcement rejection

An adapter is compatible only if it both parses and behaviorally enforces the required feature set. Required features include, at minimum:

- immutable IAC/binding/proposal refs and hash verification;
- snapshot/watermark staleness checks;
- human-only reaction and delivery assertions;
- pressure ceiling and lock enforcement;
- reset/land/stop availability;
- atomic command/event/snapshot/receipt parity;
- idempotency and optimistic concurrency;
- deterministic replay and invalidation projection;
- explicit epistemic and `NOT_APPLICABLE` handling.

An adapter that accepts fields but drops evidence, ownership, epistemic state, locks, or lineage is incompatible. Unknown required features fail negotiation. Active sessions remain pinned to the compatibility/ruleset versions accepted at start; deprecation does not rewrite them, though revocation can prevent new commands under a governed decision.

### 8.8 Recovery paths

| Condition | Recovery |
|---|---|
| AIR unavailable | retain current state; human may use already acknowledged lawful options or reset/land/stop; no fabricated proposal |
| Evidence provider unavailable | record explicit evidence availability/gap; do not upgrade epistemic state; retry attachment idempotently |
| Projection cache corrupt | discard cache and replay from immutable stream; compare hash before re-publishing |
| Repository head/parity mismatch | quarantine session, stop mutations, run parity/replay verification, preserve all bytes |
| Unknown event/schema version | stop projection and require adopted reader/migration; never skip |
| Late AIR proposal | typed stale denial with current snapshot/watermark; request recompute |
| Operator response lost after commit | exact idempotent retry returns existing receipt |
| Binding/IAC revoked during pause | resume denied; human may record stop/cancel under governed terminal authority |
| Sensitive evidence becomes inaccessible | retain content hash/metadata and explicit availability state; do not substitute current evidence |
| Human corrects reaction/delivery transcription | append superseding artifact/event and recompute later effective projections; retain original history |

### 8.9 Observability

Operational telemetry must expose behavior without leaking source content:

- command counts and outcomes by type/error code;
- idempotent replay hits and key-reuse conflicts;
- optimistic concurrency conflicts;
- stale AIR proposal denials;
- pressure-ceiling and lock-weakening denials;
- model-inference-to-human-attestation rejection attempts;
- transaction rollback and post-commit response recovery;
- event/receipt parity failures;
- replay duration and hash mismatches;
- evidence unavailability by governed class;
- pause/reset/land/stop/cancel rates without interpreting human success;
- invalidation fan-out and affected projection counts.

Logs use stable correlation, command, session, event, and receipt IDs; they omit raw transcripts, recordings, reactions, and exact delivered language unless a separately governed secure audit sink is authorized. Metrics cannot become evaluator thresholds or production certification evidence by themselves.

### 8.10 Operational safeguards

- rate limits cannot prevent an authorized stop/cancel command;
- model/provider timeouts cannot hold a transaction open;
- background retries must use the original idempotency key and cannot rebase semantic intent;
- retention deletion preserves a tombstone/content hash and governed unavailability state where lawful;
- backups and restores are verified through replay and parity, not row counts alone;
- disaster recovery cannot promote an older projection head over a later committed stream;
- administrator repair uses append-only governed correction/invalidation commands, never direct row edits.

## 9. Behavior-specific acceptance criteria

These criteria are for later independent audit and authorized implementation. Their presence is not a self-audit or PASS claim.

### 9.1 Requirement and Story coverage

| ID | Required observable behavior | Evidence required |
|---|---|---|
| `AIR-FR-049` | after every meaningful accepted event, current expression state, target distance, anchor status, observed signals, actual pressure history, relationship condition, and lawful next actions are represented in one immutable projection with evidence/epistemic state | state-transition tests, golden snapshots, event/receipt parity, replay proof |
| `AIR-FR-050` | a genuine interviewer reaction is stored only with attributable human attestation and can influence the next-call context only when the human marks it operative | human-vs-model authority tests, supersession tests, source evidence tests |
| `AIR-ST-09.01` | entry requires an armed IAC; each delivered call and meaningful state transition is recorded; reset/land/stop are truthful; no reaction is fabricated | vertical session proof including positive, adversarial, recovery, terminal, and replay paths |

### 9.2 Ownership and truth criteria

1. Given an AIR proposal without a delivery command, no delivered-call event, pressure history entry, reaction, or state transition is created.
2. Given model-inferred interviewer curiosity, `RecordInterviewerReaction` is rejected unless the human separately attests it; the model observation remains labeled `MODEL_INFERRED`.
3. Given spontaneous human wording, the record uses `SPONTANEOUS_HUMAN` and does not create an AIR call-option link.
4. Given adapted AIR wording, both the AIR source option and exact delivered language remain recoverable; neither is mutated.
5. Given a counteractivation hypothesis, it remains AIR-owned/hypothesized and cannot populate guest truth or Reaction Receipt outcome.
6. Given a human pressure decision lower than recommendation, the lower actual value is accepted when within constraints.
7. Given any recommendation to deepen, the human can reset, land, stop, or cancel when allowed by the governing IAC; AIR cannot override.
8. Given a live observation, its epistemic state and evidence owner survive serialization, adapter passage, replay, and projection.

### 9.3 State and lifecycle criteria

1. Start fails unless the exact IAC/binding/source refs resolve, hashes match, binding is armed/current, actor scope matches, and lawful terminal routes exist.
2. Initial state does not assert unobserved reaction, call, anchor hit, or landing.
3. Every accepted meaningful event increments the sequence with an unbroken previous-event hash.
4. Every state change has a snapshot and transition receipt in the same atomic commit.
5. `NO_EFFECT` produces a receipt without an artificial state transition.
6. Paused sessions reject delivery/advance but allow evidence completion and stop/cancel.
7. Reset preserves historical calls, pressure, reactions, and observations.
8. Land records landing evidence and unresolved assertions without declaring a successful outcome.
9. Terminal states reject new delivery/state-advance commands.
10. Post-terminal evidence appends without reopening or changing historical event bytes.

### 9.4 AIR dependency criteria

1. AIR-008 and AIR-009 inputs are verified by exact version/hash and authority owner.
2. An AIR proposal whose snapshot ref or observation watermark differs from current state is denied `STALE_AIR_POLICY`.
3. A proposal requiring an unsupported semantic feature is rejected even if its JSON parses.
4. A proposal that exceeds pressure ceiling, weakens locks, lacks landing/stop options, or asserts actual human reaction is rejected.
5. Acknowledgement means available for consideration, never delivered or accepted as truth.
6. A live-state advance stales prior proposals unless their governed validity rule explicitly remains true; no silent retargeting occurs.
7. A hash change to either draft dependency blocks downstream promotion until the recorded sections are reviewed and receipts refreshed.

### 9.5 Determinism and portability criteria

1. Identical normalized commands and dependencies in two fresh processes produce byte-identical events, snapshots, and receipts.
2. Changing wall clock, timezone, locale, environment, process ID, random seed, dictionary insertion order, or filesystem creation/traversal order does not change canonical bytes/hashes.
3. Repository artifacts contain no absolute drive path, username, temporary directory, host name, or process-local locator.
4. Canonical lists and sorted sets serialize consistently; semantically ordered lists retain declared order.
5. Replay from genesis produces the same projection hash as replay from a valid checkpoint.
6. Replay at an earlier sequence remains reproducible after later invalidation, with the selected historical/effective view labeled.
7. Unknown schema/event versions stop projection rather than being ignored.

### 9.6 Atomicity, idempotency, and concurrency criteria

1. Fault injection at every repository write boundary leaves either the complete outcome or no visible outcome.
2. There is no stored state without receipt, receipt without command, event without command, or transition without snapshot/transition receipt.
3. An exact retry returns the original receipt and artifact hashes without a new event.
4. Same idempotency key plus different command fingerprint returns `IDEMPOTENCY_KEY_REUSED`.
5. Two commands against one expected head cannot both commit.
6. The losing command receives `STALE_PROJECTION`; the system does not auto-rebase it.
7. Response loss after commit followed by retry returns the committed outcome.
8. In-memory and durable repositories pass one shared conformance suite.

### 9.7 Invalidation, migration, and recovery criteria

1. Invalidation records reason, authority, scope, effective point, and descendants; historical bytes remain readable to authorized auditors.
2. Invalidating a selected AIR proposal propagates to its acknowledgement and dependent projections without invalidating unrelated spontaneous-human events.
3. Revoked IAC/binding blocks current operation but does not erase history.
4. Migration never guesses source kind, IAC, live state, reaction, call origin, pressure, anchor, or landing.
5. Incomplete legacy records become typed unresolved imports and cannot drive a current session.
6. Cache loss recovers through deterministic replay; a hash mismatch quarantines rather than repairs.
7. Unavailable historical inputs return `HISTORICAL_INPUT_UNAVAILABLE` with exact missing refs.
8. A corrected reaction/transcription supersedes rather than overwrites the original.

### 9.8 Security and sovereignty criteria

1. Cross-organization or cross-brand access is rejected before content disclosure.
2. Actor grants are checked for the exact command; generic operator access does not authorize interviewer reaction or delivery.
3. Raw sensitive content is absent from default logs and metrics.
4. Technical security rules do not create generic creative-safety/content-rights approval authority.
5. Guest/source authority, interviewer authority, AIR policy ownership, Interview Expression evidence ownership, and product sovereignty remain distinct in every artifact and adapter.
6. Retention/redaction actions remain receipt-bearing and do not create substitute meaning.

### 9.9 Typed non-applicability criteria

1. A field declared required cannot be satisfied by empty string/list/null when its semantics apply.
2. `NOT_APPLICABLE` is accepted only for enum-governed cases identified in the contract.
3. `UNKNOWN` and `NOT_APPLICABLE` are not interchangeable.
4. Nonverbal delivered action may use `exact_delivered_expression: NOT_APPLICABLE` only with governed action kind and evidence.
5. Spontaneous human delivery requires AIR refs `NOT_APPLICABLE`; it cannot omit origin.
6. Initial unobserved anchor/reaction/landing values are represented explicitly and cannot appear as positive evidence.

### 9.10 Claim and lifecycle criteria

1. The completed writing artifact states `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, specification work authorized, build false, and the pre-ratification ceiling.
2. No writer-issued audit, acceptance receipt, capsule, code, schema, release, certification, or production claim exists.
3. Future technical acceptance before ratification can be only `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
4. A separately attributable ratification and later build authorization are required before implementation.

## 10. Testing and completion evidence

### 10.1 Test strategy for a later authorized build

The future test suite must use exact source/dependency fixtures and exercise the pure domain independently from adapters. Every test asserts artifact bytes/hashes as well as business outcome where determinism or receipt trust is involved.

| Suite | Required cases |
|---|---|
| Unit model validation | all enum/required-field combinations; epistemic rules; `NOT_APPLICABLE`; portable refs; tenant scope; pressure/lock constraints |
| Command/domain | each command positive path, every denial code, no-effect semantics, human-only reaction/delivery, stale policy, terminal commands |
| State machine | all legal transitions and every illegal transition; reset/land/stop/cancel; post-terminal evidence |
| Property-based | event fold invariants; canonicalization under map/set order permutations; arbitrary retry/concurrency schedules; descendant invalidation |
| Golden serialization | canonical bytes and hashes across Python/runtime versions selected by the build contract and across two fresh processes |
| Repository conformance | in-memory and durable parity, atomic batch, rollback at every failpoint, response-loss retry, command/event/snapshot/receipt parity |
| Replay | genesis vs checkpoint, sequence cutoff, historical vs effective invalidation view, missing dependency, unknown event version |
| AIR integration | exact AIR-008/009 hash, stale watermark, unsupported feature, pressure/locks, acknowledgement-not-delivery, proposal supersession |
| Evidence integration | human attestation, direct observation, model inference isolation, inaccessible evidence, correction/supersession, sensitivity/redaction |
| Security | cross-tenant/brand/session IDs, actor grants, log redaction, evidence read scope, authority-denial context |
| Migration | complete legacy mapping, missing IAC/source kind/reaction/call provenance, wall-clock isolation, unresolved quarantine, reproducibility |
| Architecture | import graph, domain purity, adapters point inward, no local AIR/Delegation schema fork |
| Portability | no absolute path leakage in spec-defined outputs, receipts, archives, fixtures, logs, snapshots, or exported proof packages |

### 10.2 Mandatory vertical proof

The later synthetic proof must start from an exact armed IAC and source package, then:

1. start the live loop;
2. acknowledge a matching AIR policy proposal;
3. record a human interviewer reaction that changes the next useful call;
4. record an AIR-derived delivered call with a lower human pressure choice;
5. append a guest/source observation without upgrading it to resolved truth;
6. advance anchor, distance, relationship, pressure history, and lawful next actions with evidence;
7. reject a stale AIR proposal after the state advances;
8. record a spontaneous human call without false AIR provenance;
9. exercise reset and resume or landing/stop according to the bound route;
10. attach/correct evidence by supersession;
11. replay at multiple historical sequences and the current effective view;
12. rerun in a fresh process and compare all canonical output hashes.

An adversarial companion proof must attempt fabricated interviewer reaction, auto-delivery by AIR, pressure above ceiling, lock weakening, stale projection, cross-tenant evidence, invalid source kind, unknown required compatibility feature, receipt-only persistence, and an absolute-path reference. Every attempt must fail with its typed code and without partial semantic state.

### 10.3 Traceability matrix

| Requirement / invariant | Model/workflow sections | Primary tests |
|---|---|---|
| AIR-FR-049 live-state completeness | 5.7, 6.3, 6.8-6.10 | state transition, golden snapshot, replay, parity |
| AIR-FR-050 interviewer reaction | 5.5, 6.4 | human authority, model isolation, supersession, evidence gap |
| AIR-ST-09.01 receipt-bearing loop | 5.3-5.10, 6.8-6.11 | vertical proof, state machine, atomicity, terminal truth |
| AIR/Interview Expression ownership split | 3.1, 5.4-5.6, 6.7 | acknowledgement-not-delivery, spontaneous origin, immutable AIR refs |
| human pressure/stop authority | 3.2, 5.6, 5.8, 6.6 | lower-dose, ceiling denial, reset/land/stop, race tests |
| epistemic truth and no fabrication | 3.3, 6.4-6.5 | enum/model tests, model-vs-human adversarial cases |
| deterministic receipt trust | 5.10, 6.10-6.12 | golden bytes, fresh-process reproduction, environment/order perturbation |
| atomic history and replay | 5.2, 5.9, 6.11, 8.2-8.5 | fault injection, concurrency, parity, historical replay |
| lossless-or-blocked migration | 8.6 | field-accounting and unresolved quarantine tests |
| semantic compatibility | 5.4, 8.7 | unsupported features, parse-only adapter rejection, dependency drift |

### 10.4 Completion evidence required from a future writer-to-audit handoff

For this Prompt 03 writing task, the controller must receive:

- the exact spec file path, byte count, and SHA-256;
- a `SPEC_WRITING_RECEIPT.yaml` with `WRITTEN_PENDING_AUDIT` and claim ceiling;
- a `FILES_READ_RECEIPT.yaml` with every admitted authority/source/dependency and exact hash;
- a `SOURCE_TRACEABILITY.yaml` linking the two FRs and Story to sections and evidence;
- a `DRAFT_DEPENDENCY_RECEIPT.yaml` with both AIR drafts, exact bytes/hashes, `DRAFT_DEPENDENCY_NOT_ACCEPTED`, and revision-impact sections;
- a `WRITER_FILE_MANIFEST.json` with exact created-file bytes/hashes;
- structural confirmation of exactly ten numbered sections and no out-of-scope edits.

The independent auditor, reviser, and re-auditor must be different lifecycle executions from this writer. This writer makes no quality PASS assertion beyond structural writing completion.

### 10.5 Evidence exclusions and blockers

The following cannot satisfy completion or later acceptance:

- assignment headings or summaries substituted for exact source bytes;
- optional/deferred sources used for factual claims while unavailable;
- a parser-only compatibility test;
- a mutable in-memory dictionary implementation that bypasses atomic/parity constraints;
- a demo whose output depends on current time, randomness, environment, or absolute paths;
- manually edited receipts or snapshots without command/event provenance;
- AIR proposal presence treated as call execution;
- model output treated as interviewer reaction;
- a Story receipt treated as independent technical audit;
- a passing synthetic proof treated as production certification;
- pending ratification represented as current authority.

### 10.6 Writing completion state

When the five external writing receipts and manifest verify this file, `TS-INT-007` is:

```yaml
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
adoption_status: NOT_APPLICABLE
build_status: NOT_BUILD_READY
next_lifecycle_action: INDEPENDENT_TECH_SPEC_AUDIT_BY_DIFFERENT_AGENT
```

This is a specification-writing result only. It grants no implementation, product adoption, production, release, certification, VAE Stage 5, Format 02, or Development Capsule authority.
