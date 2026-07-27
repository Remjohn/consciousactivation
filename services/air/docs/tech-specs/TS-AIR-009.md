---
type: technical_specification
spec_id: TS-AIR-009
title: Live Narrative Policy, Bounded Activative Calls, Pressure Dose, and Counteractivation
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
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
writing_wave: 4
controlling_frs:
  - AIR-FR-051
  - AIR-FR-052
  - AIR-FR-053
  - AIR-FR-054
controlling_stories:
  - AIR-ST-09.02
  - AIR-ST-09.03
upstream_draft_dependencies:
  - spec_id: TS-AIR-008
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: e8fac04b295ec742621e92735475f2c603f16b69b26f67b5e5c840ab6ddb16a0
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-009 - Live Narrative Policy, Bounded Activative Calls, Pressure Dose, and Counteractivation

This candidate specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. It specifies only the AIR-owned semantic policy required by `AIR-FR-051` through `AIR-FR-054`: propose the smallest useful next Activative Call, recommend a bounded pressure dose, represent evidence-bounded counteractivation hypotheses, and expose lawful continue/deepen/reset/land/stop options. It does not assign AIR ownership of the live interview, the guest's actual state, the interviewer's genuine reaction, the delivered call, or the resulting Reaction Receipt. Interview Expression owns live state and observed reaction evidence; the authorized human interviewer owns delivery and the operative pressure/stop decision.

The controlling V2.1 authority remains `CANDIDATE_NOT_CURRENT`. This document does not ratify it, authorize implementation, create a Development Capsule, adopt a cross-product contract, or claim build, production, publication, provider, evaluator-certification, or product-readiness authority.

`TS-AIR-008` is consumed only as the exact hash-pinned `WRITTEN_PENDING_AUDIT` interface draft recorded above and is therefore `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Its Interview Asset Contract, armed binding, branch, pressure-envelope, recovery, landing, source/provenance, and immutable-reference shapes are draft inputs rather than accepted law. A change to its pinned bytes reopens sections 3, 5, 6, 8, 9, and 10 for revision-impact review.

## 1. Files and authorities read

### Authority, requirements, and workflow inputs

| Input | Lifecycle / authority state | SHA-256 | Specific use |
|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | current authority registry | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Confirms Constitution V1.1 remains current until governed amendment. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Controls the rich semantic chain, Activative Call definition, human-reaction law, and current Interview Expression boundary. |
| `.../doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `CANDIDATE_NOT_CURRENT` | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Candidate temporal, epistemic, live-state, dose, counteractivation, immutable-history, and product-sovereignty laws. |
| `.../prd/features/F09-live-narrative-state-induction-and-interviewer-resonance.md` | `2.1.0-draft`, pending ratification | `a1e1421ee23b0f30f84bffeb37bfd5b6eac74a29d4a9e24a036c85a257ec8fa5` | Controlling behavior, terminal condition, Primitive duties, and AIR-FR-051 through 054. |
| `.../planning/EPICS_AND_VERTICAL_STORIES.md` | candidate planning | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-09.02 and AIR-ST-09.03 positive, adversarial, recovery, and evidence requirements. |
| `.../specs/TS-AIR-009-live-narrative-state-induction-and-interviewer-resonance.md` | source draft pending ratification | `96f25c8912ac2c334ced7220c3ee7dff9e031e5e5985bb848f93e88ddb930a0d` | Substantive donor; corrected to the Prompt 02 ownership split and V3.3 lifecycle. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | current frozen queue | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Freezes identity, exact path, Wave 4, gate, and specification-only claim ceiling. |
| `.../CANONICAL_FR_LEDGER.csv` | current reconciliation | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Assigns AIR-FR-051 through 054 to AIR while assigning AIR-FR-049/050 to Interview Expression. |
| `.../FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | current reconciliation | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Freezes the primary Story and spec relationship for every controlling FR. |
| `.../SPEC_DEPENDENCY_DAG.yaml` | Prompt 02 DAG | `1cf4299781e76c9c80f4489291a92b0a5e1f666f91b8cf9476307a03da5257eb` | Records TS-AIR-008 as the upstream interface dependency. |
| `.../PATH_OWNERSHIP_REGISTRY.yaml` | frozen path registry | `f260e400384a67f837b67a8a8981a4b773cd8792135eeca20c94f065468296a7` | Reserves only `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-009.md`. |
| `.../V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending ratification | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Assigns AIR semantic policy, Interview Expression live source evidence, human choice, Independent Evaluation receipts, Studio projection, and transport boundaries. |
| `.../V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending ratification | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Assigns `Live_Activative_State` and reactions to Interview Expression and planned program meaning to AIR. |
| `.../SOURCE_DISPOSITION_LEDGER.yaml` | validated source registry | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Classifies all four F09 doctrine inputs as `REQUIRED_UNIQUE_EVIDENCE`. |
| `.../SOURCE_GAP_NOTICE.yaml` | current, zero blocking notices | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | Prevents claims from 28 unavailable optional/deferred sources; none is used here. |
| `.../RECONCILIATION_INPUT_HASH_LOCK.yaml` | locked | `ea28bcab299e74adb87f3bce8ab8a1d20093d4d8699e9e10c5d387383363c456` | Locks the four admitted source archives and candidate package members. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | validated V3.3 recovery | `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | Classifies SDE-022 as a WRITE-interface edge; build and acceptance do not block writing. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_WRITING_WAVE_DAG.yaml` | acyclic, 23 waves | `24b26b9820a0f2cab0cd01ab4c46e9aca476219f496644c063533ee602ccff60` | Places TS-AIR-009 in Wave 4 after TS-AIR-008. |
| `.../V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | candidate pending ratification | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Requires `CANDIDATE_NOT_CURRENT`, build false, and the pre-ratification quality ceiling. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification work only | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes WRITE and later independent technical review, but forbids a capsule or build. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv` | current path decision | `3fa4793ea2baca46dcfbf8e123d039a59ab2467e5814471d49b3daf65e588a73` | Records direct AIR spec path authority and no applicable `AGENTS.md`. |
| `.../V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | exact V3.3 packet | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Freezes the one-spec path, four FRs, two Stories, dependency, stop conditions, and claim ceiling. |
| `.../wave-receipts/WAVE_04_DISPATCH_LOCK.yaml` | `DISPATCHED` | `bf0ed7cf77ae548fd7262e030ee8bc4e9f28f501db28d2a06ca7bd10a62be442` | Pins TS-AIR-008 at the exact state and hash used below. |
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/.../skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3 writer law | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Controls ten-section completeness, receipts, draft-dependency handling, and no self-audit. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/MASTER_STATUS.md` | current status truth | `71d7fdac3c9498c42133c95e141b31241b0fa613426417d9fd81b3d1d656f491` | Confirms candidate authority, implementation false, VAE Stage 5 unauthorized, and no production/certification claim. |

The abbreviated `...` paths expand under the Program Control reconciliation/recovery root or the AIR full-bundle root identified by the leading segment. No repository-root or ancestor `AGENTS.md` applies to `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-009.md`; the frozen packet supplies explicit Prompt 02 and Prompt 02C specification-path authority.

### Exact upstream draft interface

| Edge | Draft | State | Bytes | SHA-256 | Interface consumed | Revision impact if bytes change |
|---|---|---|---:|---|---|---|
| SDE-022 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-008.md` | `WRITTEN_PENDING_AUDIT` | 78,755 | `e8fac04b295ec742621e92735475f2c603f16b69b26f67b5e5c840ab6ddb16a0` | exact armed binding; immutable IAC, branch, pressure, recovery, landing, Primitive, lock, source/provenance, lifecycle, compatibility, and replay contracts | sections 3, 5, 6, 8, 9, 10 |

This input is `DRAFT_DEPENDENCY_NOT_ACCEPTED`. No field from it is represented as independently audited, ratified, or accepted for build.

### Required unique doctrine, Primitive, and brownfield evidence

| Evidence | Bytes | SHA-256 | Disposition and fact used |
|---|---:|---|---|
| `.../sources/ai_v2_predecessor/07_LIFECYCLE_STATE_MACHINES.md` (`SRC-AI2-LIVE-001`) | 1,285 | `403f684a14160ac974cdfd0f45ca25645a5a0a38e07628d7096d80d87a5236cb` | `REQUIRED_UNIQUE_EVIDENCE`; preserves planned/armed/live/observed/resolved distinctions and additive repair/invalidation flow. |
| `.../sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | 43,321 | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | `REQUIRED_UNIQUE_EVIDENCE`; Narrative State Induction is structured facilitation, the guest controls truth, landing is evaluated, and the human creates the shared field. |
| `.../sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` (`SRC-INT-002`) | 24,239 | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | `REQUIRED_UNIQUE_EVIDENCE`; contracts, anchors, capture configuration, archetype routing, and receipts remain traceable rather than free-form. |
| `.../sources/doctrine/MATRIX_OF_EDGING.md` (`SRC-MOE-001`) | 15,982 | `7ba1858cd9238a63f32d28e9cc8e7bbe306ba82ac5fa5af4a0346128aa3b6ebb` | `REQUIRED_UNIQUE_EVIDENCE`; broad signal precedes sharp edge formation, candidates must survive evidence, and pressure must resist both flattening and unsupported invention. |
| `.../psychological_diagnostics/PRM-PSY-008.yaml` | 5,916 | `1f63263ab6e0178e3c62feda7bfc5951ea02f1dd8bdafa96b15efd0a0381cfeb` | Exact dignity safeguard: attack the problem, not identity; reject toxic positivity and passive aggression. |
| `.../feedback_scoring/EXP-FBK-001.yaml` | 6,981 | `ef888d832e745444a7fcf80192548f89a40abadc77e9653bd7c76ff966cae8ec` | Exact RIM discipline: feedback must be relevant, immediate, and meaningful; reject notification spam and vanity metrics. Its example latency is not imported as an ungoverned F09 threshold. |
| `.../persuasion/PRM-PRS-009.yaml` | 7,442 | `91acef681584ee72d14be51159ac5ed6d0683168dc71a95369b56d9956268caa` | Exact disequilibrium move; reject false jeopardy and stranded disequilibrium. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/expression_session.py` | 5,923 | `afce01302bb59f8b85b49bc12ea000ec74de8cd2f020707df6c6dd18e7ae316a` | Predecessor typed session/status/quality/receipt vocabulary; generated UUID/time and mutable lifecycle projection are not canonical identity. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/expression_session_service.py` | 24,790 | `bde10d6cd18e37cb4c8bd347654a65cec4f47eaf91f8d96f93ef1bf09b6d745b` | Predecessor start/pause/resume/fail/close and readiness behavior; sequential writes, clock/random identity, and combined authorities are not sufficient. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/expression_sessions.py` | 1,441 | `3fac9930a8ba9f41be8768b03f1a06a76f75eb4d0d02027ae421cf673e9f27b5` | In-memory overwrite maps lack immutable versions, transactions, command parity, concurrency, idempotency, replay, and invalidation. |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_complete_expression_session_creation.py` | 10,256 | `0f0d04640e1c91f8f295aaed270fb014574dff455efe04a1de599bf20a3e3668` | Useful regression evidence for brand scope, readiness denial, receipt-backed start, and explicit pause/resume/fail/close transitions. |

## 2. Problem, user outcome, solution, and scope

### Problem

An armed Interview Asset Contract is a plan, not a live decision engine. During an interview, Interview Expression observes a changing human situation: the guest may hit the anchor, partially answer, resist, become overloaded, contradict the premise, reveal an unexpected edge, complete a landing, or need a relational reset. If the system simply advances through prepared questions, pressure becomes performative or coercive, the guest's authorship is displaced, a landed answer is interrupted, and inference is recorded as human truth.

The architectural failure is not merely a poor question. It is authority and evidence corruption: AIR may mistake an inferred state for an observation, an automated recommendation for a delivered call, or a pressure proposal for human authorization. A model can also optimize for intensity, invent defense motives, or use fluent language to hide that no safe transition is supported.

### User and system outcome

For every meaningful live-state snapshot, the interviewer receives a small, inspectable portfolio of lawful next actions tied to the exact armed IAC, observed evidence, current state, branch, expected transition, pressure envelope, recovery route, and stopping law. The portfolio makes the smallest useful proposal visible while always preserving lower-pressure, reset, land, and stop authority. The interviewer can accept, modify within the authorized envelope, defer, reset, land, or stop. Interview Expression records what actually happened; AIR never fabricates it.

### Bounded solution

F09 defines an AIR-owned, immutable `LiveNarrativePolicyProposal` aggregate composed of:

1. exact refs to the armed TS-AIR-008 program and Interview Expression-owned live snapshot;
2. an evidence-bounded `CounteractivationProfileProposal` that remains inferred;
3. a portfolio of `ActivativeCallProposal` objects rather than a claim that a call was delivered;
4. one `PressureDoseRecommendation` per actionable call;
5. a `TransitionOptionSet` containing lawful `CONTINUE`, `DEEPEN`, `RESET`, `LAND`, `STOP`, or `HOLD` options supported by evidence;
6. a `SmallestUsefulCallProof` showing why the recommended call asks for no more semantic scope or pressure than needed;
7. deterministic hard-gate and externally owned evaluation references;
8. immutable proposal, human-decision acknowledgement, cancellation, supersession, invalidation, and replay receipts.

### In scope

- consume an exact armed IAC/binding and an immutable Interview Expression live-state snapshot;
- validate owner, source, provenance, session, event watermark, epistemic state, branch, pressure ceiling, recovery, stop, lock, and compatibility refs;
- propose bounded call alternatives and explicit non-call options;
- recommend dose, expected gain, overload risk, relief/reset path, and stop law for each actionable option;
- identify probable denial, reactance, shame shutdown, projection, tribal defense, topic escape, performative agreement, contradiction, overload, or supported profile extensions as hypotheses only;
- preserve interviewer resonance as attributable human/Interview Expression evidence rather than model-created empathy;
- deterministic gating, bounded language proposal, independent evaluation boundary, human decision acknowledgement, and Interview Expression handoff;
- immutable persistence, canonical hashing, idempotency, optimistic concurrency, cancellation, supersession, selective invalidation, replay, and observability;
- versioned migration of attributable predecessor session evidence without inventing live-policy history;
- exact future implementation and test paths.

### Out of scope and non-goals

- maintaining or owning the canonical `LiveActivativeState`, AIR-FR-049, or AIR-FR-050;
- observing audio, video, transcript, gaze, silence, breath, body, or interviewer reaction directly;
- delivering a question, changing pressure live, diagnosing a guest, compelling disclosure, or overriding a stop;
- creating Reaction Observations, Reaction Receipts, Expression Moments, source packages, or landing evidence;
- rewriting, arming, approving, or mutating the TS-AIR-008 Planned AIP or IAC;
- selecting final archetypes, Final Scripts, derivatives, visual demands, VAE routes, or campaign publication;
- making a generic creative-safety/content-rights approval authority; operator-provided source authority and product sovereignty remain preserved;
- imposing a local latency, confidence, or pressure threshold not supplied by a governed profile;
- activating Format 02, VAE Stage 5, implementation, build, production, certification, or provider operation;
- auditing, revising, accepting, or issuing a Development Capsule for this specification.

## 3. Governing decisions and constraints

### Authority and field-level ownership

1. **Current authority remains V1.1.** Current V1.1 says Interview Expression compiles Guest Identity DNA, Context Premise, Interviewer Resonance, and Edge Pressure into Activative Calls. Candidate V2.1 proposes a product split in which AIR owns planned/live semantic policy while Interview Expression owns live execution and evidence. This candidate spec may describe that split for technical convergence, but it cannot make the candidate current or buildable.
2. **AIR owns proposal meaning, not lived truth.** AIR owns `LiveNarrativePolicyProposal`, `ActivativeCallProposal`, `PressureDoseRecommendation`, `CounteractivationProfileProposal`, and `TransitionOptionSet` values at the inferred/planned proposal layer.
3. **Interview Expression owns live evidence.** `LiveActivativeState`, `InterviewerReactionState`, Reaction Observations/Receipts, delivered-call records, source spans, and observed state transitions are external immutable refs owned by Interview Expression.
4. **The human interviewer owns operative choice.** The human decides whether to ask, rephrase, lower pressure, pause, reset, land, or stop. AIR's selected recommendation is not authorization. A human can always choose a lower dose or stop; raising beyond the armed envelope is forbidden.
5. **Independent Evaluation owns evaluation receipts.** AIR's compiler and language proposer cannot issue the independent receipt governing eligibility. Capability presence does not imply evaluator certification.
6. **Studio projects and captures corrections.** Studio may show options and submit an attributable human command or HumanResolutionEpisode. It cannot edit AIR or Interview Expression state directly.
7. **Delegation transports; it does not interpret.** Any cross-product message preserves exact fields, owners, hashes, epistemic states, and lifecycle. Parser success without enforcement is incompatible.
8. **The source F09 owner table is phase-qualified.** Its human ownership of `ActivativeCall`, `PressureDoseDecision`, `CounteractivationProfile`, and `StateTransitionReceipt` is preserved for operative live decisions and receipts. AIR creates explicitly suffixed proposals/recommendations only. The actual delivered call, actual dose decision, and observed transition remain non-AIR values.

### Epistemic and source-fidelity laws

9. Every observation remains `observed`; every AIR defense/meaning interpretation remains `inferred`; every human choice is `operator_confirmed`; rejected and superseded candidates remain available by hash.
10. Silence, gaze, hesitation, contradiction, laughter, or tone is not a motive. AIR can propose an interpretation only with exact observation refs, alternatives, limitations, and a maximum supported claim.
11. The guest's response and the interviewer's genuine resonance cannot be synthesized. Missing or ambiguous evidence produces `EVIDENCE_INSUFFICIENT`, `HOLD`, `RESET`, or `STOP`, not an invented state.
12. The exact source kind and provenance inherited through the armed program remain intact. F09 neither reclassifies source kind nor invents interview provenance.
13. Operator-supplied source authority, permitted use, retention, route scope, and revocation are referenced and enforced. No new generic approval body is created.
14. A live proposal cannot rewrite Identity DNA, Context Premise, Resonance, Matrix, Edge Product, Primitive binding, IAC, or source truth. A material semantic correction requires a new upstream version and causal invalidation.

### Call, pressure, counteractivation, and landing laws

15. **Smallest useful means bounded and provable.** The selected proposal must be minimal under the governed profile's ordering of semantic scope, requested disclosure, number of moves, pressure delta, and expected information gain. AIR does not invent a universal scalar threshold.
16. **No call is a valid option.** `HOLD`, `PAUSE`, `RESET`, `LAND`, and `STOP` are first-class. The engine may not generate a question merely to return nonempty output.
17. **Pressure is calibrated, never maximized.** Every actionable proposal declares starting/current dose, proposed dose, delta, expected gain, overload risk, relief/reset route, escalation preconditions, and stop conditions from exact profile/contract refs.
18. **Downward safety is unconditional.** The human may lower pressure or stop. Automated escalation cannot exceed the IAC ceiling, require vulnerability, or proceed when overload/counteractivation evidence requires relief.
19. **Counteractivation is a hypothesis portfolio.** Denial, reactance, shame shutdown, projection, tribal defense, topic escape, performative agreement, overload, and contradiction use closed profile-governed codes with evidence and alternatives. They are not diagnoses or identity labels.
20. **Landing is evidence-led.** A landed/partially landed observation causes AIR to prefer `LAND`, `HOLD`, or one bounded clarification where supported. It cannot continue to exhaust a deck.
21. **The intended premise is not forced.** Unexpected but truthful material can supersede the prepared path. AIR must surface the conflict and lawful options instead of steering the guest back to an expected conclusion.
22. **PRM-PSY-008 is non-compensable.** Calls identify behavior, circumstance, or contradiction without attacking identity and without hiding the issue in toxic positivity or passive aggression.
23. **EXP-FBK-001 is contextual.** The recommendation must explain immediately why the observed event changes the next option. The governed profile supplies any latency budget. Notification spam, arbitrary scores, and the Primitive file's example-specific three-second rule are not imported as F09 law.
24. **PRM-PRS-009 is evidence-bound.** A disruption may be named only when supported; false jeopardy fails. A call that opens disequilibrium must expose an honest relief, landing, or stop path so it does not strand the guest.

### Determinism, lifecycle, compatibility, and claim constraints

25. IDs and semantic times are caller supplied. Random UUIDs, current clock, filesystem traversal, environment variables, locale, machine paths, map insertion order, and model-provider metadata cannot affect canonical bytes.
26. Artifacts and decisions are immutable. Any semantic change creates a successor linked by `supersedes_ref`; no `model_copy` overwrite is canonical history.
27. Proposal artifact, dependency edges, command record, lifecycle event, outbox record, and receipt commit atomically. Receipt-without-artifact and artifact-without-receipt are invalid.
28. Every command carries expected aggregate version and idempotency key. Same key/same canonical input returns the original result; same key/different input is a conflict.
29. Invalidation follows exact dependency edges. A changed IAC, live snapshot, observation, profile, Primitive, lock, source authority, or human revocation invalidates only dependent current proposals while historical bytes remain reproducible.
30. Compatibility is behavioral: owner enforcement, epistemic preservation, all action/defense codes, pressure envelope, stop behavior, lock inheritance, source/provenance, evaluation, and lifecycle semantics must be supported. An adapter may not flatten to a question string.
31. `NOT_APPLICABLE` is a typed value only for a field declared conditionally applicable, with reason, authority/evidence refs, and validator proof. A current state ref, expected transition, dose, overload risk, relief/reset route, stop law, evidence set, owner, or epistemic state cannot be N/A on an actionable call.
32. The claim ceiling is `WRITTEN_PENDING_AUDIT`; build false; no pre-ratification state above `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`; no Development Capsule.

## 4. Current brownfield architecture

### Existing useful behavior

The Studio predecessor contains typed Complete Expression Session identity, recording configuration, pre-session gate, session status, status events, start receipts, brand-scope checks, consent/deck readiness, and explicit start/pause/resume/fail/close operations. Its tests prove that an unready session is blocked with a receipt, a started session binds the approved deck, wrong-brand access fails, and live capture transitions are explicit.

It does not implement F09's evidence-bounded next-call policy. It stores a mutable `CompleteExpressionSession` projection, produces IDs with `uuid4()`, writes time with `utc_now()`, writes session/event/receipt sequentially, and keeps independent overwrite maps in memory. A failure between writes can leave state without matching receipts. There is no canonical hash, expected aggregate version, idempotency record, outbox parity transaction, exact observation watermark, call proposal portfolio, dose recommendation, counteractivation evidence, selective invalidation, or historical replay proof.

### Disposition matrix

| Brownfield path / component | Actual useful behavior | Gap / risk | Disposition |
|---|---|---|---|
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/expression_session.py` | Closed session statuses, typed configuration and quality refs, session events, start receipts. | Generated IDs/times; mutable status in root; open strings; no hashes, versions, epistemic states, evidence watermarks, AIR/IE ownership split, or F09 policy objects. | `ADAPT` vocabulary and negative fixtures; never reuse canonical identity or ownership unchanged. |
| `.../services/expression_session_service.py` | Validates consent/deck/setup; starts, pauses, resumes, fails, closes; emits events and receipts. | One service combines orchestration and decisions; sequential writes; current-time/random identity; mutable overwrite; no idempotency/concurrency/atomicity; no F09 next-call logic. | `ADAPT` transition evidence behind the Interview Expression port; `REPLACE` persistence/transaction semantics for AIR. |
| `.../repositories/expression_sessions.py` | Minimal test double and brand query. | Separate overwrite dictionaries; no immutable version or parity; no descendants, replay, optimistic concurrency, command records, or outbox. | `REPLACE_FOR_PRODUCTION`; a future test double must implement the exact transactional port. |
| `.../tests/cmf_studio/test_complete_expression_session_creation.py` | Brand boundary, blocked readiness receipt, start binding, and explicit transition tests. | No live observation, call proposal, dose, defense, stop law, deterministic identity, rollback, replay, or ownership denial. | `ACTIVATE_AS_REGRESSION_EVIDENCE`; supplement with section 10 suites. |
| `SRC-AI2-LIVE-001` lifecycle | Planned/armed/live/observed/resolved and additive repair sequence. | High-level only; no field ownership or transaction contract. | `REUSE_AS_EVIDENCE`, implemented only through current typed contracts. |
| V9 Narrative State Induction / anchors | Human field, adaptive questioning, truthful landing, state/action loop. | Historical examples can imply fixed anchor counts, loose schemas, or Studio ownership. | `REUSE_AS_EVIDENCE`; current profiles and owners control. |
| V9.1 Complete Expression Session | Structured capture configuration, asset contracts, routing, evaluation. | Operational doctrine mixes source, semantic, capture, production, and provider concerns. | `ADAPT`; Interview Expression owns capture and source evidence; AIR receives refs only. |

### Brownfield migration boundary

A predecessor session can be referenced as historical Interview Expression evidence only when its organization/brand/session/guest/operator/deck/configuration/status/event/receipt values and original byte hash are attributable. It cannot be migrated into a `LiveNarrativePolicyProposal` unless current evidence supplies an exact armed binding, immutable live snapshot, observation watermark, current pressure history, branch status, source authority, Primitive/profile refs, and actor/owner identities. Missing values remain absent and return `AIR_F09_MIGRATION_MEANING_MISSING`; no adapter backfills them from a question deck, status name, current time, or model inference.

## 5. Proposed architecture and workflows

### Components and boundaries

| Component | Responsibility | Explicit prohibition |
|---|---|---|
| `LivePolicyInputResolver` | Resolve exact armed binding, IAC, live snapshot, observation watermark, interviewer-resonance evidence, profile, Primitive, authority, and lock refs. | Read raw media directly, guess missing refs, or mutate either source product. |
| `F09DeterministicValidator` | Enforce ownership, freshness, sequence, epistemic, branch, pressure, recovery, stopping, lock, source/provenance, and compatibility gates. | Apply learned judgment or local thresholds. |
| `CounteractivationInferencePort` | Return typed evidence-linked hypothesis candidates and alternatives within a pinned capability/profile envelope. | Diagnose a person, write live state, hide uncertainty, or set operative pressure. |
| `ActivativeCallProposalPort` | Suggest bounded wording/actions for already lawful policy moves using a minimum-complete context. | Generate IDs/times/status/authority, call provider tools outside grants, deliver a call, or self-evaluate. |
| `SmallestUsefulCallSelector` | Compare validated options under the governed partial order and produce a proof or a typed non-decision. | Convert fluency or intensity into authority; force one winner when options are incomparable. |
| `PressureDosePolicy` | Apply exact IAC/current-state/profile constraints and produce recommendations with downward-safe paths. | Raise beyond ceiling, invent a scale, or disable stop. |
| `LiveNarrativePolicyCompiler` | Assemble immutable proposal, defense profile proposal, call portfolio, transition options, provenance, limitations, and invalidation edges. | Claim a call occurred or a state changed. |
| `F09IndependentEvaluationPort` | Request/record externally owned profile-pinned evaluation of exact proposal bytes. | Share producer identity or imply certification. |
| `LiveNarrativePolicyService` | Authorize commands; coordinate idempotency, concurrency, transactions, lifecycle, human-decision acknowledgement, cancellation, invalidation, and replay. | Own human choice or Interview Expression state. |
| `LiveNarrativePolicyRepository` | Store immutable artifacts, command records, edges, events, receipts, outbox, snapshots, and historical bytes atomically. | Commit any parity-incomplete transaction. |
| `InterviewExpressionPolicyHandoffAdapter` | Receive read-only live refs and return proposal/human-decision refs without semantic flattening. | Transport raw hidden context unnecessarily, alter observed evidence, or acknowledge for the human. |
| `StudioLivePolicyProjection` | Reconstruct proposal/status and translate attributable operator actions. | Become canonical state or silently edit proposal/evidence. |

### Workflow A - admit one live decision context

1. `ProposeNextActivativeCallsCommand` supplies caller-generated command/proposal IDs and issued time, idempotency key, expected aggregate version, actor/authority refs, exact armed-program binding and IAC refs, Interview Expression live-snapshot ref, observation watermark, last delivered-call/Reaction Receipt refs where available, interviewer-resonance evidence ref, source-authority ref, profile refs, and requested decision horizon of one call.
2. The resolver verifies every `ImmutableRef` by object type, ID, version, SHA-256, owner, lifecycle, and applicability. The armed binding and live session IDs must agree. The live snapshot must be newer than the last consumed watermark and must not be superseded, revoked, or invalidated.
3. The validator checks source/provenance, operator source authority, event continuity, current/target state, branch state, pressure history, anchor/landing signals, contradictions, counter-signals, locks, profile support, and exact Primitive bindings. It refuses ambiguous ownership or epistemic state.
4. Raw transcript/audio/video is not copied into AIR. Exact evidence refs and only the minimum governed excerpts/features required for this decision enter the JIT capsule. Private or restricted evidence remains in Interview Expression and is referenced by hash/authorization.
5. If evidence is missing, stale, discontinuous, or contradictory beyond the profile's resolvable envelope, the service emits a typed blocker plus lawful `HOLD`, `RESET`, `PAUSE`, or `STOP` options. It does not call a model merely to fill the gap.

### Workflow B - infer counteractivation without diagnosing the guest

1. Deterministic signals identify which profile-governed classes are eligible for consideration: `DENIAL`, `REACTANCE`, `SHAME_SHUTDOWN`, `PROJECTION`, `TRIBAL_DEFENSE`, `TOPIC_ESCAPE`, `PERFORMATIVE_AGREEMENT`, `CONTRADICTION`, `OVERLOAD`, or `NO_SUPPORTED_COUNTERACTIVATION`.
2. The inference port receives exact evidence features, candidate classes, alternatives, Primitive constraints, relationship/interviewer context, and the maximum supported claim. It returns a portfolio; it cannot emit a global personality label or hidden motive as fact.
3. Every `CounteractivationHypothesis` includes supporting and counterevidence refs, alternative codes, confidence representation defined by the pinned profile, epistemic state `inferred`, limitations, prohibited interpretations, and action constraints.
4. Deterministic validation enforces PRM-PSY-008 and the IAC recovery/stop law. `OVERLOAD` or strong closing evidence cannot route to automatic deepening. Unsupported hypotheses are preserved as rejected candidates with reasons.
5. The resulting `CounteractivationProfileProposal` remains AIR-owned inference. Only the human/Interview Expression evidence path can confirm what action occurred or how the guest responded.

### Workflow C - compile the smallest useful call and dose portfolio

1. The policy compiler derives lawful transition moves from the exact IAC branch rule, current state, landing criteria, current pressure history, recovery program, stop law, and inferred profile. It includes non-call moves where applicable.
2. For each actionable move, the proposal port may suggest natural-language wording constrained by source truth, interviewer credibility, current relationship, dignity guard, supported disruption, and a single-call semantic horizon. It cannot prescribe the guest's answer.
3. The compiler creates `ActivativeCallProposal` objects with expected transition, evidence, one primary move, branch ref, intended pressure effect, scope limits, alternate interpretation, and stop/recovery consequences.
4. `PressureDosePolicy` creates a `PressureDoseRecommendation` using only the profile's scale and current/maximum dose. It declares expected gain, overload risk, relief/reset path, escalation preconditions, and stop conditions. Any unavailable required value makes the call ineligible.
5. `SmallestUsefulCallSelector` computes a profile-governed partial-order proof over semantic scope, requested disclosure, move count, pressure delta, evidence gain, and reversibility. A lower-pressure equally useful option dominates a higher-pressure one. Incomparable candidates remain a portfolio for human judgment.
6. Deterministic validation rejects a repeated question after a landed answer, unsupported depth request, false jeopardy, identity attack, passive-aggressive reset, toxic-positive non-question, hidden compound question, over-ceiling dose, absent relief/stop path, or a proposal that treats defense as permission to intensify.
7. The repository atomically stores exact proposal bytes, candidates and rejections, dependency edges, command record, event, outbox item, and compilation receipt. State becomes `PROPOSED_PENDING_EVALUATION` or `BLOCKED`.

### Workflow D - independent evaluation and human choice

1. `RequestLivePolicyEvaluationCommand` pins exact proposal bytes, validator receipt, evaluation profile, and evidence refs. The producer and evaluator principals must differ.
2. The evaluator returns an externally owned receipt with rule outcomes, disagreements, maximum supported claim, limitations, and exact evaluated hashes. Unavailability or failure does not create a pass; the profile controls whether a deterministic-only degraded path may be shown as non-eligible guidance.
3. An evaluation pass makes options display-eligible; it does not authorize delivery. Studio/Interview Expression presents the portfolio, evidence, pressure, recovery, and why-this-now feedback to the interviewer.
4. The interviewer may select an eligible proposal, choose a lower dose, make an allowed natural-language adjustment, choose another lawful option, pause, reset, land, or stop. Any semantic or above-envelope change is rejected as a new proposal requirement. Stop never requires AIR approval.
5. Interview Expression owns the actual delivery command/event and records the delivered call, actual dose, human actor, source/session position, and resulting observations. AIR receives immutable refs later.
6. `AcknowledgeHumanLiveDecisionCommand` stores only the external decision/execution refs and causal relation to the proposal. It cannot rewrite proposal bytes or manufacture a `StateTransitionReceipt`.

### Workflow E - next cycle, cancellation, supersession, invalidation, and replay

1. A later decision command must present a live snapshot whose watermark causally follows the previously acknowledged delivered-call/Reaction Receipt refs. Gaps or duplicate event positions block.
2. Cancellation appends a receipt and prevents new display/delivery eligibility. If delivery was already recorded by Interview Expression, cancellation is late and cannot erase it; the receipt records the race and next recovery action.
3. Superseding the IAC, armed binding, live state, observation, source authority, Primitive/profile, wrong-reading lock, or human revocation invalidates only proposals whose stored edges depend on it.
4. A human correction submitted through Studio produces an attributable command/HumanResolutionEpisode ref. Promotion into AIR policy creates a new version under scoped authority; it never globally changes behavior from one session.
5. Replay loads stored bytes, registry snapshots, command order, and external refs by hash. It reproduces the historical proposal and receipts without calling current providers or consulting current registries, clock, random state, environment, or absolute paths.

### State machine

`LiveNarrativePolicyProposal` lifecycle is append-only:

```text
REQUESTED
  -> BLOCKED
  or
  -> PROPOSED_PENDING_EVALUATION
       -> EVALUATED_BLOCKED
       or
       -> EVALUATED_ELIGIBLE
            -> HUMAN_DECISION_ACKNOWLEDGED
            -> EXPIRED
            -> CANCELLED
            -> SUPERSEDED
            -> INVALIDATED
```

`HUMAN_DECISION_ACKNOWLEDGED` means AIR has stored a ref to an attributable external decision. It does not mean the call was delivered, a reaction occurred, or the state transitioned unless Interview Expression supplies the corresponding exact refs.

## 6. Data models, contracts, schemas, and APIs

### Shared scalar, reference, and canonicalization rules

All root and embedded schemas are closed (`additionalProperties: false`). Nonempty text is Unicode NFC, trimmed, and rejects empty/control-only values. IDs and timestamps are caller supplied. `ImmutableRef` is:

```text
ImmutableRef {
  object_type: NonEmptyText
  object_id: NonEmptyText
  version: NonEmptyText
  sha256: Sha256Hex
  authoritative_owner: ProductOrHumanAuthorityId
  lifecycle_state_at_use: NonEmptyText
}
```

Every root artifact also includes `schema_id`, `schema_version`, `artifact_id`, `artifact_version`, `aggregate_id`, `aggregate_version`, `authority_ref`, `owner_product`, `created_by_actor_ref`, `effective_at`, `canonicalization_profile`, `dependency_refs`, `artifact_sha256`, and `lifecycle_state`.

Canonical JSON uses UTF-8 without BOM, Unicode NFC, LF normalization for semantic text, lexicographic object keys, preserved list order where sequence is meaningful, canonical key sorting for declared sets, no insignificant whitespace, base-10 integer rendering, and no absolute path. Artifact identity excludes storage location, provider request IDs, worker IDs, and runtime telemetry. Scores use governed integer micros (`0..1_000_000`) only where the exact profile declares them; no binary float enters identity.

### `LivePolicyDecisionContext`

Schema ID: `ca.air.live-policy-decision-context/2.1.0-candidate`.

| Field | Type | Owner and invariant |
|---|---|---|
| `armed_program_binding_ref` | `ImmutableRef` | AIR/human-armed F08 binding; exact current session binding. |
| `interview_asset_contract_ref` | `ImmutableRef` | AIR-owned candidate contract ref, exact hash; read-only. |
| `live_activative_state_ref` | `ImmutableRef` | Interview Expression-owned snapshot; required and immutable. |
| `state_snapshot_sequence` | `NonNegativeInt` | Interview Expression; must advance monotonically for new context. |
| `observation_watermark` | `EventWatermark` | Interview Expression; exact last admitted event identity/hash/sequence. |
| `recent_reaction_receipt_refs` | ordered tuple of `ImmutableRef` | Interview Expression; empty only before any meaningful call and explicitly proven by session sequence. |
| `last_delivered_call_ref` | `ImmutableRef?` | Interview Expression; required after a call is delivered. |
| `interviewer_resonance_evidence_ref` | `ImmutableRef` | Interview Expression/human source; AIR cannot fabricate it. |
| `current_expression_state` | `EpistemicAssertion<ExpressionStateCode>` | Observed/inferred provenance preserved; no global guest label. |
| `target_expression_state_ref` | `ImmutableRef` | Exact F08 target state; read-only. |
| `anchor_and_landing_status` | `AnchorLandingStatus` | Evidence-linked current assessment with alternatives/limits. |
| `pressure_history` | ordered tuple of `DeliveredDoseEvidence` | Exact delivered-call refs; proposals are not history. |
| `relationship_condition` | `EpistemicAssertion<RelationshipCondition>` | Evidence and validity window required. |
| `source_authority_ref` | `ImmutableRef` | Operator-provided source authority and route scope. |
| `policy_profile_ref`, `evaluation_profile_ref`, `compatibility_profile_ref` | `ImmutableRef` | Required hashes; no local fork or implicit default. |
| `primitive_binding_refs`, `wrong_reading_lock_refs` | nonempty tuple of exact refs | Must include applicable inherited constraints; cannot weaken them. |

### `CounteractivationProfileProposal`

Schema ID: `ca.air.counteractivation-profile-proposal/2.1.0-candidate`.

| Field | Type | Rule |
|---|---|---|
| `profile_proposal_id` | stable ID | Caller supplied; immutable within aggregate version. |
| `epistemic_state` | literal `inferred` | Cannot be `observed` or `operator_confirmed`. |
| `hypotheses` | tuple of `CounteractivationHypothesis`, 1..n | Includes `NO_SUPPORTED_COUNTERACTIVATION` where evidence supports none. |
| `supporting_observation_refs` | nonempty tuple of refs | Interview Expression-owned observations. |
| `counterevidence_refs` | tuple of refs | Must not be hidden when present. |
| `alternative_interpretations` | nonempty tuple of typed alternatives | At least one unless the profile supplies deterministic certainty proof. |
| `maximum_supported_claim` | closed profile-governed code | Prevents diagnosis or motive certainty. |
| `action_constraints` | nonempty tuple of `ActionConstraint` | May force lower/hold/reset/stop; never grants escalation alone. |
| `limitations` | nonempty tuple of `Limitation` | Missing modality, ambiguity, timing, or context limits. |
| `inference_profile_ref`, `producer_identity_ref` | exact refs | Required; producer cannot be evaluator. |

`CounteractivationHypothesis.code` is one of the exact profile-supported closed codes, including the minimum set in section 5. It includes `{code, confidence_micros_or_qualitative_band, evidence_refs, counterevidence_refs, alternative_codes, prohibited_interpretations, eligible_policy_moves, ineligible_policy_moves}`. A confidence representation is accepted only when the profile declares its semantics and calibration evidence.

### `ActivativeCallProposal`

Schema ID: `ca.air.activative-call-proposal/2.1.0-candidate`.

| Field | Type | Rule |
|---|---|---|
| `proposal_id` | stable ID | Caller supplied; not a delivered-call ID. |
| `action_kind` | enum | `ASK`, `CLARIFY`, `REFLECT`, `LOWER_PRESSURE`, `PAUSE`, `RELATIONAL_RESET`, `HOLD`, `LAND`, or `STOP`; extensions require exact profile support. |
| `call_text` | `NonEmptyText?` | Required for `ASK/CLARIFY/REFLECT`; forbidden for pure `PAUSE/HOLD/LAND/STOP` unless profile defines a closing phrase field. |
| `contract_branch_ref` | `ImmutableRef` | Exact IAC branch or landing/stop rule. |
| `live_state_ref`, `observation_watermark` | exact values | The evidence horizon this proposal used. |
| `problem_not_person_target` | `BehaviorOrSituationRef?` | Required when naming a conflict; identity target forbidden. |
| `expected_transition` | `EpistemicAssertion<TransitionExpectation>` | Inferred/planned only; includes failure/counter-signals. |
| `pressure_recommendation_ref` | embedded exact ref | Required for every actionable proposal. |
| `expected_information_or_expression_gain` | `GovernedGainClaim` | Evidence, limits, and profile unit required; no vanity score. |
| `recovery_if_missed` | `RecoveryOption` | Required for ASK/CLARIFY/REFLECT. |
| `stop_law_ref` | `ImmutableRef` | Required for all proposals. |
| `source_and_semantic_refs` | nonempty tuple | Exact Identity/Context/Matrix/Edge/IAC refs needed for the call; no flattened notes. |
| `primitive_constraint_refs`, `wrong_reading_lock_refs` | nonempty tuples | Exact inherited constraints. |
| `prohibited_implications` | nonempty tuple | Unsupported motive, answer, jeopardy, identity judgment, or forced landing. |
| `human_choice_required` | literal `true` | No proposal self-executes. |

### `PressureDoseRecommendation`

Schema ID: `ca.air.pressure-dose-recommendation/2.1.0-candidate`.

| Field | Type | Rule |
|---|---|---|
| `scale_profile_ref` | `ImmutableRef` | Governs units and comparisons. |
| `last_delivered_dose` | profile dose + evidence ref | Required after prior delivery; cannot use prior proposal. |
| `recommended_dose`, `maximum_permitted_dose`, `dose_delta` | profile dose | Recommendation cannot exceed IAC ceiling; human may lower. |
| `expected_gain` | `GovernedGainClaim` | Relevant and meaningful explanation tied to current progression. |
| `overload_risk` | `EpistemicAssertion<RiskBandOrMicros>` | Evidence, alternatives, limits, and profile semantics required. |
| `escalation_preconditions` | tuple of conditions | Required for positive delta; all must be satisfied. |
| `deescalation_conditions` | nonempty tuple | Includes evidence that forces lower/reset/stop. |
| `relief_or_affinity_reset` | `RecoveryOption` | Required; `NOT_APPLICABLE` forbidden. |
| `stop_conditions` | nonempty tuple | Required and inherited from IAC/profile. |
| `operator_override_envelope` | `OverrideEnvelope` | Allows lower/stop; semantic or upward change outside envelope creates new proposal. |

### `TransitionOptionSet` and `SmallestUsefulCallProof`

`TransitionOptionSet` contains one or more `TransitionOption` values with `{option_id, transition_kind, triggering_evidence_refs, required_preconditions, expected_effect, pressure_effect, recovery_effect, landing_effect, counteractivation_constraints, eligibility, ineligibility_reasons}`. `transition_kind` is `CONTINUE`, `DEEPEN`, `RESET`, `LAND`, `STOP`, or `HOLD`. Options unsupported by evidence remain visible as rejected candidates when needed for audit; they are not offered as eligible.

`SmallestUsefulCallProof` contains `{candidate_refs, governed_order_profile_ref, compared_dimensions, dominance_edges, incomparable_pairs, selected_or_portfolio_result, selection_reason, evidence_gain_claim, higher_pressure_rejection_reasons}`. `compared_dimensions` may include semantic scope, requested disclosure, move count, pressure delta, reversibility, and expected evidence gain only when the profile governs their meaning. If no unique minimum exists, `selected_or_portfolio_result` is `PORTFOLIO_REQUIRES_HUMAN_CHOICE`; the engine may not invent a score to force one winner.

### Root `LiveNarrativePolicyProposal`

Schema ID: `ca.air.live-narrative-policy-proposal/2.1.0-candidate`.

Required semantic fields are `decision_context_ref`, `counteractivation_profile_proposal`, `transition_options`, `call_proposals`, `smallest_useful_call_proof`, `recommended_option_refs`, `rejected_candidate_refs`, `deterministic_validation_receipt_ref`, `independent_evaluation_receipt_ref?`, `human_decision_required: true`, `limitations`, `expiry_or_freshness_policy_ref`, and `invalidation_parent_refs`. An evaluated receipt may be absent only in `PROPOSED_PENDING_EVALUATION` or an explicitly profile-governed degraded state that is not display/delivery eligible.

### Commands, events, receipts, and service API

Command envelope:

```text
CommandEnvelope {
  command_id: NonEmptyId
  idempotency_key: NonEmptyId
  command_type: ClosedCommandType
  aggregate_id: NonEmptyId
  expected_aggregate_version: NonNegativeInt
  actor_ref: ImmutableRef
  authority_ref: ImmutableRef
  issued_at: RFC3339Utc
  input_refs: NonEmptyOrderedTuple<ImmutableRef>
  canonical_payload_sha256: Sha256Hex
}
```

Commands are `ProposeNextActivativeCallsCommand`, `RequestLivePolicyEvaluationCommand`, `RecordLivePolicyEvaluationCommand`, `AcknowledgeHumanLiveDecisionCommand`, `CancelLivePolicyProposalCommand`, `SupersedeLivePolicyProposalCommand`, `InvalidateLivePolicyProposalCommand`, and `ReplayLivePolicyProposalCommand`.

Events are `LiveDecisionContextAdmitted`, `LivePolicyProposalBlocked`, `LivePolicyProposalCompiled`, `LivePolicyEvaluationRequested`, `LivePolicyEvaluated`, `HumanLiveDecisionAcknowledged`, `LivePolicyProposalCancelled`, `LivePolicyProposalSuperseded`, `LivePolicyProposalInvalidated`, and `LivePolicyProposalExpired`.

Receipts include exact command/input/output hashes; actor, authority, owner, aggregate/version; live snapshot sequence and watermark; IAC/profile/Primitive/lock refs; candidate and rejection refs; validator/evaluator results; human/execution refs when externally supplied; limitations; dependency edges; transaction/event/outbox refs; decision code; and written time supplied by the command or infrastructure event contract. A receipt never converts a recommendation into a delivered call.

The future service API is:

```text
LiveNarrativePolicyService.execute(command: CommandEnvelope) -> F09CommandReceipt
LiveNarrativePolicyRepository.get(ref: ImmutableRef) -> CanonicalArtifact
LiveNarrativePolicyRepository.get_by_hash(sha256: Sha256Hex) -> CanonicalArtifact
LiveNarrativePolicyRepository.resolve_dependencies(ref: ImmutableRef) -> DependencyGraph
LiveNarrativePolicyRepository.current_projection(aggregate_id: Id) -> Projection
LiveNarrativePolicyRepository.verify_artifact_receipt_parity(transaction_id: Id) -> ParityResult
LiveNarrativePolicyRepository.replay(aggregate_id: Id, through_event_ref: ImmutableRef?) -> ReplayResult
```

These are proposed future interfaces, not current code signatures or implementation authorization.

### Positive example

Given an armed IAC `iac-v7`, an Interview Expression snapshot showing a partial anchor hit, one exact contradiction, stable relationship temperature, and delivered dose 2 under a governed 0..5 profile with ceiling 3, the output may contain:

- `CLARIFY` at dose 2, preserving the landed part and asking one evidence-linked distinction;
- `LAND` at dose 0 if the existing source already meets landing criteria;
- `HOLD` at dose 0 when the contradiction needs human interpretation;
- a proof that a dose-3 deepening question is dominated by the dose-2 clarification because both seek the same evidence and the lower-dose option is more reversible.

The human chooses. The example does not mean those numeric scale semantics are universal; the exact profile defines them.

### Negative example

A payload containing only `{"next_question": "Why are you avoiding the truth?", "confidence": 0.91}` is invalid because it has no exact IAC/live-state/evidence refs, assigns a motive as fact, attacks identity/intent, uses an ungoverned float, omits alternatives, dose, overload risk, recovery, stop law, ownership, evaluation, and human-choice boundary, and cannot be canonically replayed.

## 7. Implementation stages and exact target paths

All paths below are future implementation targets only. They cannot be created or modified until ratification/adoption and a separately authorized Development Capsule names an exact allowlist.

| Stage | Controlling FR / Story | Exact future targets | Required completion evidence |
|---|---|---|---|
| 0 - ratification and capsule | all | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-009/DEVELOPMENT_CAPSULE.md`; `.../SOURCE_LOCK.yaml`; `.../ALLOWED_PATHS.yaml` | Ratified/current authority, accepted/adopted upstream interfaces, exact source/Primitive hashes, and separate build authority. |
| 1 - shared domain types | AIR-FR-051..054 / both | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/live_policy_context.py`; `.../domain/live_narrative_policy.py`; `.../domain/activative_call_proposal.py`; `.../domain/pressure_dose.py`; `.../domain/counteractivation.py` | Closed immutable types, owner/epistemic rules, human-choice law, and generated schema parity. |
| 2 - canonical schemas and fixtures | all | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f09.live-policy-context.schema.json`; `.../air.f09.live-narrative-policy-proposal.schema.json`; `.../air.f09.live-policy-receipts.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/fixtures/f09/` | Positive and negative fixtures generated from one canonical type source; no local shared-release fork. |
| 3 - input and IE boundary | AIR-FR-051/052 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/ports/interview_expression_live_state.py`; `.../adapters/interview_expression_live_policy.py`; `.../validation/f09_input_validator.py` | Exact owner/session/watermark/source/profile checks and raw-evidence minimization. |
| 4 - counteractivation | AIR-FR-053 / AIR-ST-09.03 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/ports/counteractivation_inference.py`; `.../services/counteractivation_policy.py`; `.../validation/f09_counteractivation_validator.py` | Evidence/counterevidence/alternatives, no diagnosis, dignity, overload, and uncertainty fixtures. |
| 5 - call and dose policy | AIR-FR-051/052 / AIR-ST-09.02 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/live_narrative_policy_compiler.py`; `.../services/smallest_useful_call_selector.py`; `.../services/pressure_dose_policy.py`; `.../ports/activative_call_proposal.py` | Candidate portfolio, governed partial-order proof, bounded dose, RIM rationale, recovery, landing, and stop behavior. |
| 6 - lifecycle repository | all | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/repositories/live_narrative_policy_repository.py`; `.../services/live_narrative_policy_service.py`; `.../serialization/canonical.py` | Atomic parity, idempotency, optimistic concurrency, immutable history, invalidation, cancellation, and replay. |
| 7 - evaluation and human acknowledgement | all | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/f09_evaluation_port.py`; `.../services/live_policy_evaluation_service.py`; `.../adapters/studio_live_policy_projection.py` | Separate evaluator identity, exact hashes, human decision refs, no self-execution, and no certification inference. |
| 8 - migrations | all | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/migrations/studio_expression_session_v1.py`; `.../migrations/ai_v2_live_policy.py` | New immutable artifacts only for complete mappings; original hashes preserved; missing meaning blocked. |
| 9 - evidence | all | exact test paths in section 10 | Unit, property, contract, integration, architecture, migration, fault-injection, replay, privacy, and clean-room results. |

No stage may modify VAE, Delegation release bytes, Builder behavior, current constitutional authority, historical receipts, or Interview Expression-owned live evidence. Publishing a shared cross-product schema is a later governed release action.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Trigger | Required behavior |
|---|---|---|
| `AIR_F09_UPSTREAM_DRAFT_DRIFT` | TS-AIR-008 state/bytes/hash differ from Wave 4 lock. | Stop affected writing/build progression; reopen sections 3, 5, 6, 8, 9, 10. |
| `AIR_F09_AUTHORITY_NOT_CURRENT_FOR_BUILD` | Build/capsule/current-adoption requested before ratification. | Deny and preserve specification-only state. |
| `AIR_F09_PATH_OR_OWNER_MISMATCH` | Ref owner, product, session, or aggregate differs from governed boundary. | Reject before inference; name expected and observed owner. |
| `AIR_F09_ARMED_PROGRAM_REQUIRED` | Missing, unarmed, cancelled, stale, or invalidated F08 binding/IAC. | Reject; no call proposal. |
| `AIR_F09_LIVE_STATE_REQUIRED` | Exact Interview Expression snapshot is missing or unresolved. | Reject; do not reconstruct from transcript/question history. |
| `AIR_F09_EVENT_WATERMARK_GAP` | Snapshot sequence repeats, regresses, skips required causal event, or mismatches hash. | Block and request exact missing/refreshed evidence. |
| `AIR_F09_SOURCE_AUTHORITY_REVOKED` | Operator-provided source authority is revoked/out of scope. | Cancel display/new use; preserve historical artifacts and revocation receipt. |
| `AIR_F09_EPISTEMIC_COLLAPSE` | Inference is represented as observed/confirmed or proposal as delivered. | Reject and identify offending field. |
| `AIR_F09_INTERVIEWER_RESONANCE_FABRICATED` | Model/system supplies purported genuine interviewer reaction without attributable evidence. | Reject; require human/Interview Expression evidence. |
| `AIR_F09_COUNTERACTIVATION_UNSUPPORTED` | Defense code lacks support, alternatives, or profile applicability. | Reject hypothesis; preserve candidate/reason. |
| `AIR_F09_PERSON_DIAGNOSIS_FORBIDDEN` | Call/profile labels identity, pathology, or hidden motive as fact. | Reject under evidence and PRM-PSY-008 gates. |
| `AIR_F09_NO_SMALLEST_USEFUL_PROOF` | Recommended call lacks governed comparison/proof. | Return portfolio for human choice or block; do not invent rank. |
| `AIR_F09_COMPOUND_OR_UNBOUNDED_CALL` | Proposal requests multiple uncontrolled moves or disclosure beyond current horizon. | Reject; bounded repair creates a new proposal version. |
| `AIR_F09_PRESSURE_PROFILE_MISSING` | Dose scale/ceiling/current delivered dose semantics unresolved. | Reject actionable proposals; allow stop/hold only where contract permits. |
| `AIR_F09_PRESSURE_CEILING_VIOLATED` | Recommended/current delta exceeds IAC/profile ceiling. | Reject; lower/reset/stop remains available. |
| `AIR_F09_OVERLOAD_IGNORED` | Overload evidence exists but proposal deepens/escalates. | Reject; require lower, pause, reset, land, or stop option. |
| `AIR_F09_RELIEF_OR_STOP_MISSING` | Action lacks relief/reset or stop law. | Reject; required fields cannot be N/A. |
| `AIR_F09_FALSE_JEOPARDY` | Call asserts unsupported/exaggerated disruption. | Reject under PRM-PRS-009. |
| `AIR_F09_STRANDED_DISEQUILIBRIUM` | Call increases tension without honest recovery/landing/stop route. | Reject under PRM-PRS-009. |
| `AIR_F09_DIGNITY_GUARD_VIOLATED` | Call attacks person, hides critique, or uses condescending protection language. | Reject under PRM-PSY-008. |
| `AIR_F09_RIM_FEEDBACK_INVALID` | Why-now rationale is irrelevant, delayed beyond governed budget, arbitrary, or vanity-scored. | Reject display eligibility; no local threshold invention. |
| `AIR_F09_LANDED_ANSWER_OVERRIDDEN` | Proposal continues/deepens despite sufficient landing or stop evidence. | Reject and surface land/hold/stop options. |
| `AIR_F09_INTENDED_PREMISE_FORCED` | Proposal steers contradiction/unexpected truth back to planned conclusion. | Reject; preserve evidence and expose reset/land/stop/escalation. |
| `AIR_F09_EVALUATION_NOT_INDEPENDENT` | Producer/evaluator identity matches or profile/hash missing. | Reject evaluation receipt; proposal remains ineligible. |
| `AIR_F09_HUMAN_DECISION_REQUIRED` | Delivery/decision is inferred from AIR recommendation. | Deny; require attributable external decision/execution ref. |
| `AIR_F09_STATE_TRANSITION_UNPROVEN` | AIR receipt claims a human state change without Interview Expression evidence. | Reject receipt/projection; preserve proposal-only truth. |
| `AIR_F09_COMPATIBILITY_UNSUPPORTED` | Consumer drops owner, code, dose, recovery, stop, lock, epistemic, or lifecycle semantics. | Reject before handoff; parser-only support is insufficient. |
| `AIR_F09_IDEMPOTENCY_CONFLICT` | Same key, different canonical command payload. | Return conflict; no new artifact/event/receipt. |
| `AIR_F09_CONCURRENT_MODIFICATION` | Expected aggregate version differs. | Reject atomically; caller reloads current projection. |
| `AIR_F09_ATOMIC_COMMIT_FAILED` | Any artifact/edge/command/event/receipt/outbox staging operation fails. | Roll back all staged semantic writes; infrastructure telemetry only. |
| `AIR_F09_LATE_CANCELLATION` | Cancel races with externally recorded delivery. | Preserve both causal records; prevent future use and route recovery. |
| `AIR_F09_STALE_OR_INVALIDATED` | Proposal display/use against superseded/revoked parent. | Deny current use; historical replay remains. |
| `AIR_F09_MIGRATION_MEANING_MISSING` | Legacy record lacks any mandatory current semantic/owner field. | Preserve legacy bytes and block; never guess. |
| `AIR_F09_REPLAY_HASH_MISMATCH` | Replay differs from stored canonical artifact/receipt bytes. | Fail evidence gate; preserve incident and inputs. |
| `AIR_F09_ABSOLUTE_PATH_CONTAMINATION` | Canonical object or receipt contains a machine path. | Reject serialization and identify field. |

### Migration and compatibility

The Studio adapter can import attributable session status/event/receipt evidence into a new historical reference envelope, but that envelope does not become a live-state or call-policy artifact. Generated UUID/time are preserved as legacy values with the original file/object hash. Current AIR IDs/times are supplied by the migration command. An F09 proposal is produced only if the migration input independently resolves every required F08 and Interview Expression ref, watermark, profile, pressure, observation, source-authority, owner, and epistemic field.

Deprecated schemas remain readable for historical replay. They do not become current because a parser accepts them. Active live decisions stay pinned to the versions negotiated at context admission; a new profile or schema does not rewrite them. An adapter cannot drop counterevidence, coerce `HOLD/RESET/LAND/STOP` into question text, map a proposal to a delivered call, or flatten owner and epistemic state.

### Rollback, recovery, invalidation, and replay

Fault injection after every staged write must prove all-or-nothing commit. A worker crash after commit but before response is recovered by idempotency lookup and returns the original receipt. Model/evaluator timeout follows the exact profile fallback: deterministic non-call options may remain visible only when declared, while unsupported actionable proposals remain ineligible. Silent provider substitution is prohibited.

Rollback restores the last known-good implementation/profile binding for new commands; it never edits artifacts already produced. Invalidation appends descendant-specific receipts from causal edges. It does not delete rejected candidates, human decision refs, Reaction Receipts, historical sessions, or unrelated proposals. Replay uses stored canonical bytes and snapshots, not current model calls or registries.

### Observability and privacy

Structured telemetry includes command/aggregate/version, actor/authority/product IDs, input/output hashes, session pseudonymous ID, snapshot sequence/watermark, IAC/profile/Primitive/lock versions, candidate/rejection counts, transition option codes, dose direction (not private content), deterministic gate codes, counteractivation code with epistemic state, evaluator identity/profile, human-decision/execution ref presence, idempotency outcome, transaction ID, invalidation cause, cancellation race, replay result, and latency against the governed profile.

Logs must not include raw private transcript/audio/video, hidden prompts, unrestricted interviewer notes, source contents, secrets, absolute paths, or unsupported psychological labels. Metrics may report failure-code rates and lifecycle counts; they cannot establish activation effectiveness, real-human safety, production readiness, or evaluator certification.

## 9. Behavior-specific acceptance criteria

| AC | Governing FR / Story | Given / When / Then pass condition | Concrete failure example and required denial | Evidence artifact | Test layer |
|---|---|---|---|---|---|
| AC-01 | AIR-FR-051 / AIR-ST-09.02 | Given an armed current IAC and exact current IE snapshot, when proposal runs, then every option binds the IAC, state, watermark, expected transition, and stop law. | A plausible question with no exact state/watermark returns `AIR_F09_LIVE_STATE_REQUIRED`. | input-resolution and compilation receipts | contract + integration |
| AC-02 | AIR-FR-051 / AIR-ST-09.02 | Given several valid moves, when selection runs, then it emits a governed `SmallestUsefulCallProof` or an incomparable portfolio for human choice. | A model's highest confidence is silently selected without comparison; return `AIR_F09_NO_SMALLEST_USEFUL_PROOF`. | candidate portfolio, dominance graph, rejection refs | unit + property |
| AC-03 | AIR-FR-051 / AIR-ST-09.02 | Given a partial anchor hit, when one clarification preserves the landed truth, then one bounded clarification can dominate a deeper compound question. | The engine restarts the full induction or asks two disclosure questions; return `AIR_F09_COMPOUND_OR_UNBOUNDED_CALL`. | call proposal and partial-hit fixture | domain + adversarial |
| AC-04 | AIR-FR-052 / AIR-ST-09.02 | Given an exact dose profile/history/ceiling, when a call is proposed, then dose, delta, expected gain, overload risk, relief/reset, and stop conditions are complete. | `recommended_dose` exists without last delivered evidence or reset route; reject. | pressure-policy receipt | schema + unit |
| AC-05 | AIR-FR-052 / AIR-ST-09.02 | Given current dose at ceiling, when an otherwise attractive deepening call appears, then escalation is ineligible and lower/hold/reset/land/stop remain. | Model raises pressure because predicted gain is high; return `AIR_F09_PRESSURE_CEILING_VIOLATED`. | ceiling fixture and rejection receipt | boundary + property |
| AC-06 | AIR-FR-052 / AIR-ST-09.02 | Given a meaningful event, when options display, then why-now feedback is tied to current progression and delivered within a profile-governed budget. | Arbitrary `91% depth` or hard-coded three-second threshold is used; return `AIR_F09_RIM_FEEDBACK_INVALID`. | RIM explanation/profile receipt | unit + UX contract |
| AC-07 | AIR-FR-053 / AIR-ST-09.03 | Given evidence of possible defense, when inference runs, then hypotheses include evidence, counterevidence, alternatives, limitations, and `inferred` state. | `guest is defensive` is emitted as observed fact; return `AIR_F09_EPISTEMIC_COLLAPSE`. | counteractivation profile proposal | schema + adversarial |
| AC-08 | AIR-FR-053 / AIR-ST-09.03 | Given denial/reactance/shame/projection/tribal/topic/performance alternatives, when evidence supports more than one, then alternatives remain visible and action constraints are conservative. | One motive is diagnosed from a pause; return `AIR_F09_PERSON_DIAGNOSIS_FORBIDDEN`. | inference portfolio and maximum-claim receipt | model-program + independent evaluation |
| AC-09 | AIR-FR-053 / AIR-ST-09.03 | Given overload signals under exact IE evidence, when policy compiles, then deepening/escalation is rejected and pause/lower/reset/land/stop is offered. | Distress is treated as productive depth; return `AIR_F09_OVERLOAD_IGNORED`. | overload fixture and transition set | domain + integration |
| AC-10 | AIR-FR-053 / AIR-ST-09.03 | Given a contradiction, when a call names it, then it targets the statement/situation, protects dignity, and does not resolve the contradiction for the guest. | `You are dishonest` or condescending reassurance is proposed; return `AIR_F09_DIGNITY_GUARD_VIOLATED`. | PRM-PSY-008 validator receipt | Primitive + adversarial |
| AC-11 | AIR-FR-054 / AIR-ST-09.03 | Given complete landing evidence, when options compile, then `LAND/HOLD/STOP` outrank deck continuation unless one bounded clarification is explicitly necessary. | Another prepared question is asked only to exhaust the deck; return `AIR_F09_LANDED_ANSWER_OVERRIDDEN`. | landing comparison receipt | integration + Story |
| AC-12 | AIR-FR-054 / AIR-ST-09.03 | Given unexpected truthful material conflicting with the planned premise, when policy runs, then it preserves the conflict and exposes reset/land/stop/escalation-to-human. | AIR steers back to the desired conclusion; return `AIR_F09_INTENDED_PREMISE_FORCED`. | contradiction fixture and decision receipt | adversarial + ownership |
| AC-13 | all / both | Given an eligible AIR proposal, when it is evaluated, then producer and evaluator identities differ and exact bytes/profile are pinned. | Compiler self-approves or capability implies certification; return `AIR_F09_EVALUATION_NOT_INDEPENDENT`. | independent evaluation receipt | architecture + contract |
| AC-14 | all / both | Given an evaluated portfolio, when shown to the interviewer, then no delivery occurs until an attributable human decision and IE execution path. | AIR recommendation is recorded as delivered call; return `AIR_F09_HUMAN_DECISION_REQUIRED`. | human decision and IE execution refs | cross-product integration |
| AC-15 | all / both | Given a human chooses lower pressure or stop, when acknowledged, then AIR preserves the choice without requiring semantic justification or raising pressure. | System refuses stop because target state is unmet; hard fail. | external decision acknowledgement | authority + integration |
| AC-16 | all / both | Given a new IE snapshot, when sequence/watermark is stale, repeated, regressed, or gapped, then proposal blocks before inference. | Missing delivered call/reaction is silently skipped; return `AIR_F09_EVENT_WATERMARK_GAP`. | watermark continuity receipt | contract + recovery |
| AC-17 | all / both | Given identical canonical command and idempotency key, when retried after response loss, then the original artifact/receipt hashes return without reinference. | Same key/different payload creates another proposal; return `AIR_F09_IDEMPOTENCY_CONFLICT`. | command record and parity proof | repository + fault injection |
| AC-18 | all / both | Given two commands at the same expected version, when one commits, then the other fails atomically and no model call/result is committed for it. | Both overwrite current projection; return `AIR_F09_CONCURRENT_MODIFICATION`. | concurrency trace and zero-residue proof | repository |
| AC-19 | all / both | Given a fault at each staged artifact/edge/event/receipt/outbox write, when commit fails, then no partial semantic state remains. | State exists without receipt or receipt without artifact; return `AIR_F09_ATOMIC_COMMIT_FAILED`. | fault matrix and parity report | fault injection |
| AC-20 | all / both | Given a parent IAC/snapshot/profile/lock/source authority changes, when invalidation projects, then only causal current descendants become stale and old bytes remain replayable. | Unrelated session invalidates or historical proposal is deleted; test fails. | invalidation graph and replay hash matrix | recovery + historical replay |
| AC-21 | all / both | Given semantically identical input under shuffled maps/sets/traversal, different temp root, locale, clock/random/env, when compiled, then canonical bytes/hash match. | Machine path or current time changes artifact identity; return `AIR_F09_ABSOLUTE_PATH_CONTAMINATION` or replay failure. | clean-room golden hashes | property + clean-room |
| AC-22 | all / both | Given an optional field is truly inapplicable, when N/A is used, then reason, authority/evidence, and validator proof exist. | Dose, evidence, reset, stop, owner, or epistemic state is N/A; schema rejects. | N/A fixtures | schema + negative |
| AC-23 | all / both | Given a consumer that parses the schema but drops alternatives, dose, stop, owner, locks, or epistemic state, when compatibility negotiates, then handoff fails before use. | Parse-only adapter claims support; return `AIR_F09_COMPATIBILITY_UNSUPPORTED`. | producer/consumer conformance receipt | contract |
| AC-24 | all / both | Given a legacy Studio session with complete status history but no IAC/live snapshot/watermark, when migration runs, then legacy bytes remain and no F09 proposal is created. | Adapter invents state or question history; return `AIR_F09_MIGRATION_MEANING_MISSING`. | migration blocker receipt | migration |
| AC-25 | all / both | Given source authority is revoked after proposal and before delivery, when revocation projects, then current display/use is denied and history remains. | Proposal remains usable or history is erased; return `AIR_F09_SOURCE_AUTHORITY_REVOKED`. | revocation/invalidation receipt | cross-product recovery |
| AC-26 | all / both | Given this written spec and receipts, when factory validation runs, then state remains `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, build false. | A capsule, build, production, or certification claim appears; governance validation fails. | writer receipts and manifest | governance |

## 10. Testing and completion evidence

### Exact future test paths

| Exact future path | Required cases |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_live_policy_context.py` | Exact owners, armed binding/session agreement, snapshot sequence/watermark, source/provenance, profile/Primitive/lock refs, epistemic states, required fields. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_counteractivation_profile_proposal.py` | All minimum codes, evidence/counterevidence/alternatives, no diagnosis, maximum claim, unsupported class, confidence-profile enforcement. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_activative_call_proposal.py` | Closed action kinds, text applicability, one-call horizon, expected transition, recovery/stop, source/semantic lineage, human-choice flag. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_pressure_dose_recommendation.py` | Current/recommended/ceiling/delta, expected gain, overload, de-escalation, relief/reset, stop, lower override, no N/A. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/services/test_smallest_useful_call_selector.py` | Dominance, incomparable portfolio, lower-pressure preference when utility is equal, no hidden threshold, rejected higher-pressure proof. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/validation/test_f09_primitives.py` | Exact PRM-PSY-008, EXP-FBK-001, PRM-PRS-009 hashes; identity attack, toxic positivity, passive aggression, vanity score, invented latency, false jeopardy, stranded disequilibrium. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/property/test_f09_canonical_serialization.py` | Unicode, list/set/map ordering, traversal, time/random/environment/locale/path independence, byte/hash stability. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/repository/test_live_narrative_policy_repository.py` | Immutable versions, command/artifact/receipt/outbox parity, expected-version conflict, idempotency, get-by-hash, snapshots, replay. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/fault_injection/test_f09_atomic_commit.py` | Failure after every staged write; crash after commit/before response; no residue and original receipt recovery. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f09_bounded_calls_and_dose.py` | AIR-FR-051/052 and AIR-ST-09.02: partial hit, smallest useful proof, profile dose, ceiling, RIM rationale, reset/stop. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f09_counteractivation_and_transition.py` | AIR-FR-053/054 and AIR-ST-09.03: every defense code, alternatives, overload, contradiction, landing, unexpected truth, no forced premise. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f09_human_choice_boundary.py` | Human selects/rephrases/lowers/defers/resets/lands/stops; AIR never self-delivers; above-envelope change creates new proposal. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_f09_interview_expression_boundary.py` | IE-owned state/observations/reactions/delivered calls, exact watermark, read-only refs, no raw-source flattening, state-transition evidence. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_f09_evaluation_boundary.py` | Separate producer/evaluator, exact profile/hash, unavailable/disagreement behavior, no certification inference. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_f09_compatibility.py` | Behavioral capability negotiation; rejection when owner, code, alternative, dose, stop, lock, source, epistemic, or lifecycle semantics are dropped. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_f09_product_boundaries.py` | AIR proposal meaning, IE live evidence, human delivery/decision, evaluator receipts, Studio projection, Delegation transport; VAE/Builder/Pipeline excluded. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_studio_expression_session_v1.py` | Complete historical mapping, original hash, generated-ID/time evidence, missing F09 meaning blocked, no invented state/call/source classification. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/recovery/test_f09_invalidation_cancellation_replay.py` | Selective descendant invalidation, late cancellation race, revocation, supersession, historical replay after registry/profile change. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/privacy/test_f09_observability.py` | No raw transcript/audio/video/private notes/hidden prompts/secrets/absolute paths or unsupported psychological labels in telemetry. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/clean_room/test_f09_portability.py` | Two fresh processes and different workspace roots reproduce golden artifacts/receipts with no undeclared files or hidden environment. |

### Required fixture matrix

Future fixtures must include: first meaningful event with no prior Reaction Receipt; anchor hit; partial hit; flat answer; topic escape; contradiction with two plausible interpretations; denial; reactance; shame-shutdown possibility; projection possibility; tribal defense; performative agreement; overload; no supported counteractivation; complete landing; partial landing; unexpected valuable landing; intended-premise contradiction; interviewer genuine recognition; missing interviewer-resonance evidence; unsupported interviewer reaction; exact pressure below/at/above ceiling; higher-pressure candidate dominated by lower; incomparable candidates; false jeopardy; stranded disequilibrium; identity attack; toxic positivity; passive aggression; RIM meaningful explanation; arbitrary score; invented latency threshold; complete and missing reset/stop; source authority active/revoked; stale/gapped/repeated watermark; same and conflicting idempotency retry; expected-version race; each atomic fault; independent and self-evaluator; human lower/stop; attempted self-delivery; compatibility field-dropping adapter; valid historical session import; incomplete migration; shuffled serialization input; time/random/env/path injection; selective invalidation; late cancellation; historical replay after current registry drift.

### Completion evidence contract

An eventual implementation can advance to independent build review only when it supplies:

1. an attributable ratification/current-authority receipt and a separately issued Development Capsule with exact allowed paths;
2. accepted/adopted upstream and cross-product interface hashes, including the eventual audited successor to TS-AIR-008;
3. source, Primitive, profile, schema, generated-type, fixture, migration, and implementation manifests pinned to exact bytes;
4. unit, property, contract, integration, architecture, migration, fault-injection, recovery, privacy, and clean-room results tied to exact commit/artifact hashes;
5. deterministic proposal and receipt hashes reproduced twice in fresh processes and under a different workspace root;
6. artifact/receipt/command/event/outbox parity plus rollback proof at every fault point;
7. producer/evaluator separation and evaluator-profile evidence without claiming certification from interface presence;
8. Interview Expression producer/consumer conformance proving AIR cannot mutate live state or claim delivery/reaction;
9. human-authority evidence proving lower pressure and stop remain available and AIR never self-executes;
10. Story-level evidence for AIR-ST-09.02 and AIR-ST-09.03, including adversarial and recovery paths;
11. migration receipts for complete predecessor mappings and blocker receipts for incomplete mappings;
12. an implementation completion receipt whose evidence and claim ceiling remain separate from real-human activation, production, publication, provider operation, and certification.

The writer completion evidence for this document is limited to the V3.3 `SPEC_WRITING_RECEIPT.yaml`, `FILES_READ_RECEIPT.yaml`, `SOURCE_TRACEABILITY.yaml`, `DRAFT_DEPENDENCY_RECEIPT.yaml`, and `WRITER_FILE_MANIFEST.json`. The next lifecycle action is independent audit by a different agent. No audit, revision, acceptance, build, capsule, code, schema, release, or implementation work is performed here.
