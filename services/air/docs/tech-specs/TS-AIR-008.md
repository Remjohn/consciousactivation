---
type: technical_specification
spec_id: TS-AIR-008
title: Planned Activative Intelligence and Interview Asset Contracts
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
writing_wave: 3
controlling_frs:
  - AIR-FR-043
  - AIR-FR-044
  - AIR-FR-045
  - AIR-FR-046
  - AIR-FR-047
  - AIR-FR-048
controlling_stories:
  - AIR-ST-08.01
  - AIR-ST-08.02
  - AIR-ST-08.03
upstream_draft_dependencies:
  - spec_id: TS-AIR-002
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-003
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: ce9ac739346789d115ada80c44b568c28e61ce68f0ae99bb55b0962c875d430c
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-008 - Planned Activative Intelligence and Interview Asset Contracts

This candidate specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. It preserves the substantive design of the hash-locked F08 draft while applying the governed disposition `AMEND_TO_CURRENT_AUTHORITY`: AIR owns planned semantic program meaning; Interview Expression consumes the plan and owns live state and reaction evidence; an authorized human controls live interview choices; Independent Evaluation owns evaluation receipts; Studio may project and capture corrections without becoming canonical semantic state. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`. This document does not ratify candidate authority, authorize implementation, issue a Development Capsule, or confer build, production, publication, provider, or certification authority.

`TS-AIR-002` and `TS-AIR-003` are consumed only as exact hash-pinned `WRITTEN_PENDING_AUDIT` interface drafts and are therefore labeled `DRAFT_DEPENDENCY_NOT_ACCEPTED`. They are not represented as current or accepted authority. Any change to either pinned byte stream reopens sections 3, 5, 6, 8, 9, and 10 for downstream revision-impact review.

## 1. Files and authorities read

### Authority, requirements, and workflow inputs

| Input | State | SHA-256 | Use in this specification |
|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | current registry | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Establishes Constitution V1.1 as current until a governed amendment. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Controls Activative lineage, identity, Context Premise, Resonance, Matrix, human reaction, visual semantics, and wrong-reading locks. |
| `.../CURRENT_AUTHORITY.md` | draft for ratification | `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Declares the V2.1 package candidate-only and separates specification work from implementation authority. |
| `.../doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `CANDIDATE_NOT_CURRENT` | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Candidate lifecycle, epistemic, immutable-history, independent-evaluation, and human-authority laws. |
| `.../prd/features/F08-planned-activative-intelligence-and-interview-asset-contracts.md` | `2.1.0-draft` | `52666ff05e320c6520814e52c6dd2222bc80b0f48233082a29eeea48ae344ad1` | Controlling AIR-FR-043 through AIR-FR-048, entry/terminal states, Story gates, and Primitive obligations. |
| `.../planning/EPICS_AND_VERTICAL_STORIES.md` | candidate planning | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-08.01 through AIR-ST-08.03, adversarial cases, recovery, and completion evidence. |
| `.../specs/TS-AIR-008-planned-activative-intelligence-and-interview-asset-contracts.md` | full draft pending ratification | `5439adc8952a8a15600048890063f8268db8f2d12806a46e4dc04f8b3d06fe05` | Substantive architecture retained and amended to current Program Control ownership and V3.3 lifecycle law. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SPEC_DISPOSITION_REPORT.md` | current reconciliation | `86852420631241ce6341a04d258f476473d0490274bb4e22675301cb02c13241` | Governs `AMEND_TO_CURRENT_AUTHORITY`; this is not a stylistic rewrite. |
| `.../CANONICAL_SPEC_LEDGER.csv` | current queue | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Freezes spec identity, path, lane, gate, quality target, and claim ceiling. |
| `.../CANONICAL_FR_LEDGER.csv` | current reconciliation | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Freezes the six controlling requirements and their AIR ownership. |
| `.../FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | current reconciliation | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Freezes one primary Story and specification path per active FR. |
| `.../RECONCILIATION_INPUT_HASH_LOCK.yaml` | locked | `ea28bcab299e74adb87f3bce8ab8a1d20093d4d8699e9e10c5d387383363c456` | Locks the admitted archives and source draft bytes. |
| `.../SOURCE_DISPOSITION_LEDGER.yaml` | validated | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Distinguishes required authority/evidence from optional, deferred, and superseded material. |
| `.../SOURCE_GAP_NOTICE.yaml` | current reconciliation | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | Prevents factual claims from unavailable optional sources. No unavailable source is used here. |
| `.../V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending ratification | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Separates AIR semantic compilation, Interview Expression live execution, human choice, evaluation, transport, projection, and downstream execution. |
| `.../V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending ratification | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Assigns Planned Activative Intelligence and the Interview Asset Contract to AIR, with Interview Expression as consumer. |
| `.../IMPORTED_INTERVIEW_REFERENCE_SLICE_CONTRACT.yaml` | frozen for specification | `3e0e0cf0c3fbcd65b93895cf8363f5c5422fa7cbe170ed06eb4114d153d2e21e` | Prevents invented planned history for imported interviews and preserves Interview Expression evidence ownership. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification work only | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes writing and later technical review but forbids build. |
| `.../V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | pending ratification | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Sets candidate labeling and the pre-ratification acceptance ceiling. |
| `.../V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | V3.3 recovery packet | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Freezes this one-spec scope, dependencies, path authority, and stop conditions. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | validated | `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | Classifies SDE-011 and SDE-012 as WRITE-interface edges rather than acceptance/build gates. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_WRITING_WAVE_DAG.yaml` | validated | `24b26b9820a0f2cab0cd01ab4c46e9aca476219f496644c063533ee602ccff60` | Places this specification in Wave 3 after the two required upstream drafts. |
| `.../wave-receipts/WAVE_03_DISPATCH_LOCK.yaml` | dispatched | `e8137e45a267767fd3e0b2f5bdc278ac66d570187b34b4a48ef282db84bdca65` | Pins the exact upstream draft states, bytes, hashes, and non-acceptance labels. |
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/.../skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Controls one-spec writing, ten-section completeness, receipts, and no self-audit. |

The abbreviated `...` paths above expand under the current Program Control or AIR full-bundle root stated by the leading path segment. No target-path or ancestor `AGENTS.md` exists for `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-008.md`; the packet therefore records explicit Prompt 02 and Prompt 02C path authority.

### Exact upstream draft interfaces

| Edge | Draft | State | Bytes | SHA-256 | Interface consumed | Revision impact if bytes change |
|---|---|---:|---:|---|---|---|
| SDE-011 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-002.md` | `WRITTEN_PENDING_AUDIT` | 52,295 | `258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5` | exact Identity/Brand refs, Context Premise, Resonance, Matrix, broad signal, tension, Edge Product, Primitive bindings, immutable refs, lineage, invalidation | sections 3, 5, 6, 8, 9, 10 |
| SDE-012 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-003.md` | `WRITTEN_PENDING_AUDIT` | 74,824 | `ce9ac739346789d115ada80c44b568c28e61ce68f0ae99bb55b0962c875d430c` | selected eligible hypothesis, complete portfolio, gate/evaluation/stop receipts, planned promotion, source-kind/provenance, roles, pressures, directions, participation, intended reaction, locks | sections 3, 5, 6, 8, 9, 10 |

Both interfaces are `DRAFT_DEPENDENCY_NOT_ACCEPTED`. F08 may consume their exact typed shapes for writing; it may not claim that either has passed independent audit or acceptance.

### Contract, doctrine, Primitive, and brownfield evidence

| Evidence | SHA-256 | Disposition and fact used |
|---|---|---|
| `.../contracts/01_PLANNED_ACTIVATIVE_INTELLIGENCE_PACK.md` | `addf788fc009e8ca7d81e4c99300f79066c3ce5b84eff1134473883c5ce61df0` | Candidate contract seed: planned epistemic class, rich lineage, selected hypothesis, target state, pressure, participation, intended reaction, smallest commitment, counteractivation, locks, evaluation; no Reaction Receipt required and no Expression Moment implied. |
| `.../contracts/02_INTERVIEW_ASSET_CONTRACT.md` | `815516bb5cdd63706c881edcba3ed349fd41ec37b164ec6422ead4a8a377c51d` | Candidate contract seed and `SRC-AI2-CONTRACT-001`: an IAC includes state, anchors, adaptive branches, pressure/recovery, landing, route hypotheses, and hard negatives; a question string alone is invalid. |
| `.../sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | Human-truth, Narrative State Induction, First-Line and Depth Anchor, evaluated-not-forced landing, interviewer resonance, and source-lineage doctrine. |
| `.../sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` (`SRC-INT-002`) | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | Expression-state versus output-archetype separation, route hypotheses, anchor alternatives, depth, repairs, and source-grounded asset doctrine. |
| `.../sources/doctrine/MATRIX_OF_EDGING.md` (`SRC-MOE-001`) | `7ba1858cd9238a63f32d28e9cc8e7bbe306ba82ac5fa5af4a0346128aa3b6ebb` | Broad-signal, candidate-survival, coalition/edge, anti-centroid, routeability, and fatality semantics inherited by exact F02 refs. |
| `.../persuasion/PRM-PRS-009.yaml` | `91acef681584ee72d14be51159ac5ed6d0683168dc71a95369b56d9956268caa` | McKee Inciting Incident: specific status-quo disruption; reject false jeopardy and stranded disequilibrium. |
| `.../persuasion/PRM-PRS-002.yaml` | `4fba8edcb439c296a610b53a45ce76b9a002b4a128338e3302ddbb1cc49e242e` | Tension-and-Release: pressure/relief pacing; reject unresolved tension and micro-tension exhaustion. |
| `.../psychological_diagnostics/PRM-PSY-008.yaml` | `1f63263ab6e0178e3c62feda7bfc5951ea02f1dd8bdafa96b15efd0a0381cfeb` | Attack Problem Not Person: preserve dignity while naming behavior; reject toxic positivity and passive aggression. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/interview_contracts.py` | `9f2df63314860ceb1afb4de0996870b290cb31f7fbf3a9f4f6809485cdcbea1e` | Useful predecessor vocabulary for states, anchor sets, repair followups, routes, receipts, and binding; generated UUID/time and flattened ownership are not canonical. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/interview_contract_service.py` | `2c195b677d3d838a98e068c741e8bdb109d5134836151320c12e0cb73989cb9b` | Useful compile/evaluate/approve/bind sequence; sequential mutable writes, shared service authority, and current-time identity require replacement. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/interview_contracts.py` | `eadfd6a56e869636229747e4dff6c9f0f4123c2da4f5dbe124868d9d88e41a10` | In-memory overwrite stores contracts, decks, receipts, and bindings independently; insufficient for atomic immutable history. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/dspy_programs/interview_contract_compiler.py` | `a0ab325eec61d2cbaeaa142572b314e54a82beeb80518689de0ec6e36bb71c9c` | Useful example of three anchor alternatives, repair prompts, route validation, and confusion rejection; hard-coded content, hidden time/randomness, and local score gates are non-authoritative. |

## 2. Problem, user outcome, solution, and scope

### Problem and user outcome

An eligible activation hypothesis is not yet an executable interview plan. Without a governed boundary, the selected semantic direction can collapse into a list of generic questions, a target feeling can be mistaken for an observed human state, pressure can become coercive, expression state can be confused with an output archetype, and planned route potential can be represented as proven source material. Such flattening severs the chain from Identity DNA, Context Premise, Resonance, Matrix, and selected hypothesis to the later human reaction and source package.

The user outcome is an inspectable, versioned Planned Activative Intelligence Pack plus one or more complete Interview Asset Contracts that an authorized interviewer can understand, independently evaluate, approve for a specific session context, and execute adaptively without surrendering human judgment. Each contract states the current-state hypothesis, target expression state, premise-exposing First-Line Anchor, depth movement, main question, bounded branches for foreseeable response conditions, pressure ceiling, dignity-preserving recovery, landing criteria, and only planned/unconfirmed derivative routes. The system must also be able to refuse compilation or arming without inventing a question, a human reaction, or a winning route.

### Bounded solution

F08 defines:

1. an AIR-owned `PlannedActivativeIntelligencePack` compiled from an exact F02 Matrix/Edge context and F03 selected-hypothesis promotion;
2. an AIR-owned, versioned `InterviewAssetContract` semantic program, consumed read-only by Interview Expression;
3. typed target-state, anchor, branch, pressure, recovery, landing, route-hypothesis, wrong-reading, evaluation, arming, invalidation, and replay contracts;
4. deterministic completeness, authority, source, Primitive, compatibility, canonical serialization, idempotency, concurrency, and lifecycle gates;
5. bounded proposal ports for wording alternatives, with deterministic validation and Independent Evaluation before human arming;
6. field-level ownership that keeps AIR semantic compilation separate from human live choice and Interview Expression observation/evidence.

### In scope

- compile a new immutable Planned AIP version from exact TS-AIR-002 and TS-AIR-003 interfaces;
- preserve Identity DNA, Context Premise, Resonance, Matrix, Edge Product, portfolio, selected hypothesis, role, pressure, participation, intended reaction, smallest commitment, counteractivation, source-kind/provenance, Primitive, objective, and wrong-reading lineage;
- compile complete Interview Asset Contracts, never question-only decks;
- model current and target expression states as planned hypotheses with evidence and inappropriateness conditions;
- model First-Line Anchor, Depth Anchor, main question, all required adaptive branch cases, pressure ceiling, recovery actions, landing criteria, route hypotheses, and hard negatives;
- deterministic validation, independent evaluation, attributable human arming, immutable session binding, supersession, selective invalidation, cancellation, replay, and historical reproduction;
- future repository, service, adapter, schema, fixture, migration, observability, and test requirements;
- explicit adaptation of the Studio predecessor without granting Studio semantic ownership.

### Out of scope and non-goals

- live interview execution, interviewer behavior automation, consent capture, recording, transcription, or session production;
- creation or mutation of Reaction Observations, Reaction Receipts, Expression Moments, Canonical Interview Source Packages, or live Activative State;
- coercion, concealed manipulation, scripted guest performance, fabricated jeopardy, or replacement of interviewer judgment;
- final script, archetype coalition, transfer, campaign, visual-production, pipeline-execution, Delegation-routing, or VAE-realization behavior;
- changing authorized-human Identity DNA values or operator-supplied source authority;
- declaring a route, clip, derivative, asset, landing, or reaction observed before event evidence exists;
- importing a historical interview by fabricating the planned pack or contract that might have preceded it;
- Product Stage 5, build, production, certification, provider, or release authorization;
- accepting or auditing this specification.

## 3. Governing decisions and constraints

### Authority and ownership

1. **Current constitutional precedence remains V1.1.** Candidate V2.1 material guides this authorized writing but remains `CANDIDATE_NOT_CURRENT`. A subordinate draft cannot narrow current rich lineage or silently transfer human/product sovereignty.
2. **AIR owns planned semantic meaning.** AIR is the authoritative value owner of the Planned AIP and IAC semantic content: target movement, anchors, bounded branch intent, pressure/recovery semantics, landing criteria, route hypotheses, and locks.
3. **Human authority owns live interview choice.** An authorized interviewer or operator approves and arms a pinned contract for a session, chooses whether and when to use a branch, may lower pressure, may stop, and remains authoritative for what is asked live. AIR cannot force delivery.
4. **Interview Expression owns live state and evidence.** It consumes an armed IAC, records execution events and Reaction Observations/Receipts, resolves Expression Moments under governed approval, and packages source. It may not rewrite the AIR-owned contract.
5. **Independent Evaluation owns evaluation receipts.** The compiler cannot issue the independent receipt that makes a contract eligible for arming. A human approval is not a duplicate evaluation; it is attributable permission to use the evaluated plan.
6. **Studio is a projection/correction surface.** It may show the pack, alternatives, live status, and receipts and may capture an operator command or HumanResolutionEpisode. It is not the canonical store and cannot silently edit either AIR meaning or Interview Expression evidence.
7. **Delegation transports; Builder declares; Pipeline executes later; VAE realizes later.** None may reinterpret or regenerate F08 meaning. `Activative Contract Compiler != Activative Intelligence Runtime` remains explicit.

### Semantic and epistemic laws

8. **Planned means planned.** The pack and every material IAC assertion use planned/inferred epistemic state. The object cannot contain a Reaction Receipt or Expression Moment for the future session, and its existence never implies either.
9. **Existing interview provenance is still enforced.** If the selected F03 hypothesis is grounded in `source_kind: interview_expression`, its inherited source provenance must contain at least one nonempty Reaction Receipt ref and at least one nonempty Expression Moment ref. For other source kinds, interview provenance is optional but validated when supplied. F08 neither guesses source kind nor creates missing provenance.
10. **Imported interviews do not acquire invented planning history.** The frozen imported-interview slice begins with an Interview Expression source package. An adapter must not synthesize a Planned AIP/IAC merely to make old data look complete.
11. **A question string is not an IAC.** A contract is invalid unless state, anchors, branches, pressure/recovery, landing, route hypotheses, locks, exact lineage, and evaluation profile are complete.
12. **Expression state is not an asset archetype.** `TargetExpressionState` describes a hypothesized human movement; `RouteHypothesis` names potential later artifact families. Neither can substitute for the other.
13. **Landing is evaluated, never forced.** A planned `LandingCriteria` describes observable signals and stopping conditions. A live `LandingEvaluationReceipt` belongs to Interview Expression/Independent Evaluation according to the later contract and is not embedded as if already true.
14. **No reconstruction of missing meaning.** AIR blocks absent source, identity, Context Premise, Matrix/Edge, selected-hypothesis, Primitive, or wrong-reading inputs. It does not infer them from a generic prompt.

### Adaptive interview and Primitive laws

15. **First-Line Anchor exposes the premise.** It gives a truthful, specific entry pattern that allows a clean content unit without dictating the guest's answer. It cannot manufacture an inciting incident.
16. **Depth Anchor moves toward lived expression.** It requests scene, cost, contradiction, decision, bodily/relational consequence, or meaning appropriate to the target state. It must not demand vulnerability for its own sake.
17. **All seven governed branch conditions are represented.** `ANCHOR_HIT`, `PARTIAL_HIT`, `DEFENSE`, `TOPIC_ESCAPE`, `CONTRADICTION`, `OVERLOAD`, and `RELATIONAL_RESET` each have a bounded response or an explicit governed no-action/stop decision. They are not replaced by a free-form followup map.
18. **Pressure is bounded and downward-safe.** The planned dose, ceiling, de-escalation, stop, and recovery are explicit. A live actor may use less pressure or stop; no automated component may exceed the ceiling.
19. **PRM-PRS-009 is evidence-bound.** The contract may open on a specific supported disruption. False jeopardy and stranded disequilibrium are hard negatives.
20. **PRM-PRS-002 preserves commensurate release.** Branch and landing structure must connect tension to an honest release or stop. Unresolved tension and micro-tension exhaustion are hard negatives.
21. **PRM-PSY-008 protects dignity without hiding the problem.** Branches address behavior, circumstance, or contradiction, not personal worth. Toxic positivity and passive aggression are hard negatives.
22. **Primitive applicability is explicit.** Each binding includes exact Primitive ID/version/hash, local job, evidence refs, trigger/suppression decision, misuse checks, conflicts, and outcome. A Primitive is not injected as a stylistic ornament.

### Determinism, lifecycle, and claim laws

23. **Canonical bytes are environment-independent.** Caller-supplied IDs and timestamps, normalized UTF-8, closed enums, integer-scaled scores where required, canonical map keys and unordered sets, and relative logical refs prevent random, clock, traversal-order, environment, and machine-path drift.
24. **Versions are immutable.** Editing any semantic field creates a new version. Arming pins one exact pack and IAC version. Old bytes and receipts remain replayable.
25. **State and evidence commit atomically.** Artifact version, dependency edges, lifecycle event, command record, outbox record, and receipt either all commit or none commit.
26. **Optimistic concurrency and idempotency are mandatory.** A command includes expected aggregate version and idempotency key. Same key plus same canonical input returns the original receipt; same key plus different input fails.
27. **Invalidation is selective and causal.** Material source, identity, Context Premise, Matrix/Edge, selected hypothesis, Primitive, profile, lock, or authority changes invalidate current dependent projections without deleting historical artifacts. Unrelated packs remain current.
28. **No local threshold invention.** Evaluation profile IDs, rule versions, and thresholds must come from a governed registry. Capability or parser presence is not certification.
29. **`NOT_APPLICABLE` is typed, not empty.** It is permitted only on a field declared conditionally applicable, with reason code, authority/evidence refs, and validator proof. Required F08 lineage, seven branch conditions, source-kind rule, pressure ceiling, locks, and landing criteria cannot be waived as `NOT_APPLICABLE`.
30. **Claim ceiling is fixed.** The result of this writing is `WRITTEN_PENDING_AUDIT`, build false, and at most `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` before ratification. No Development Capsule is created.

## 4. Current brownfield architecture

### Reusable predecessor behavior

The Studio predecessor supplies useful proof that an interview preparation flow can carry target expression states, a complete three-option First-Line Anchor set, a Depth Anchor, expected material, clip-start and depth rules, route targets, repair followups, plan evaluation, human approval, read-only session binding, and source-context retrieval. Its tests also demonstrate rejection when expression state is confused with an output archetype, denial when a weak plan has not passed its local gate, and preservation of contract IDs when binding to a session.

Those behaviors are evidence and migration inputs, not current ownership authority. The current target is an AIR-owned semantic contract consumed by Interview Expression, not a Studio-owned deck.

### Gap and adaptation matrix

| Brownfield surface | Useful behavior | Gap or hazard | Governed disposition |
|---|---|---|---|
| `InterviewAssetContract` model | Typed states, anchors, depth, expected material, landing targets, repair followups, route targets. | Generated UUID/time; mutable status in same object; open local IDs; missing exact AIR lineage, source-kind/provenance, pressure ceiling, seven governed branches, locks, ownership refs, version/hash. | `ADAPT`: map only attributable fields into new immutable AIR candidate schemas; block missing mandatory meaning. |
| `FirstLineAnchorSet` | Cinematic, emotional, and reel-hook alternatives; explicit completeness property. | Three alternatives are treated as a fixed local shape without a governed profile; no selection/authority/evidence metadata. | `ADAPT`: a selected anchor is required; alternative-set cardinality is profile-governed, never globally guessed. |
| `RepairFollowups` | Specific repairs for historical, abstract, flat, and non-clip-ready answers. | Does not cover the seven controlling branch conditions and has no dose, ceiling, stop, or dignity evidence. | `ADAPT_AS_BRANCH_EVIDENCE`; never migrate as complete `BranchProgram`. |
| `ContractRouteTarget` | Separates expression state from core archetype and derivative/render possibilities. | Routes can look confirmed before any expression evidence exists; list fields lack reason/status/compatibility refs. | `ADAPT` to `RouteHypothesis` with `PLANNED_UNCONFIRMED`; later source evidence decides eligibility. |
| compiler | Produces anchors, depth, routes, expected material, and repairs. | Hard-coded content, first-edge selection, current clock, random UUIDs, and model/service local assumptions defeat portable reproducibility. | `REPLACE_FOR_PRODUCTION`; retain fixtures as negative/positive migration evidence. |
| quality gate | Rejects generic questions, missing evidence/routes, and expression/archetype confusion. | Derives local float ratios and hidden all-or-nothing thresholds; evaluator runs beside compiler with no independent authority receipt. | `ADAPT`: deterministic hard gates plus governed, profile-pinned Independent Evaluation; no unregistered threshold. |
| service | Compile, evaluate, approve, bind sequence and brand-scope checks. | One service mutates many records sequentially; evaluator and approval roles can collapse; partial failure can leave mismatched artifacts/receipts. | `SPLIT`: AIR compile service, independent evaluator port, human arming command, Interview Expression binding consumer, transactional repository. |
| in-memory repository | Simple local lookup for tests. | Overwrites by ID; no immutable versions, aggregate revision, atomic batch, command record, outbox parity, idempotency, replay, or descendant invalidation. | `REPLACE_FOR_PRODUCTION`; test double must implement the same transactional port and invariants. |
| tests | Happy/adversarial compile/evaluate/approve/bind and extraction-context checks. | No canonical hashing, clock/random denial, rollback fault injection, concurrency, replay, supersession, invalidation, source-kind/provenance, authority denial, or historical-byte reproduction. | `ACTIVATE_AS_REGRESSION_INPUT`; add the evidence suite in section 10. |

### Brownfield migration boundary

Migration may preserve a predecessor contract only if an attributable mapping can supply every mandatory AIR field and distinguish semantic plan from lifecycle projection. Existing `created_at`, UUID, route list, status, evaluation floats, and approval flag are evidence, not canonical identity. If a predecessor item lacks the current-state hypothesis, target transition, full branch program, pressure/recovery, locks, exact F02/F03 refs, source-kind/provenance, or ownership, migration returns a typed blocker and preserves the legacy bytes. It must never fill gaps with a model-generated question or inferred classification.

## 5. Proposed architecture and workflows

### Components and boundaries

| Component | Owns | Must not do |
|---|---|---|
| `PlannedAIPCompiler` | Resolve exact F02/F03 and authority inputs; compile immutable planned pack and complete lineage. | Re-select the F03 winner, mutate Identity DNA, create live evidence, or approve itself. |
| `InterviewAssetContractCompiler` | Compile one or more complete IAC candidates from the pack, interview objective, profile, Primitive registry, and bounded proposal outputs. | Emit question-only decks, execute interviews, invent source truth, or confirm routes. |
| `F08DeterministicValidator` | Closed-schema, reference, source/provenance, Primitive, branch, pressure, lock, compatibility, and lifecycle checks. | Apply learned judgment or unregistered thresholds. |
| `InterviewPlanProposalPort` | Return typed wording/branch candidates within an exact context and capability envelope. | Write artifacts, select authority, evaluate its own proposal, or access undeclared context/tools. |
| `F08IndependentEvaluationPort` | Produce a profile-pinned evaluation request and store an externally owned evaluation receipt ref. | Share compiler identity or convert a score into human arming authority. |
| `PlannedInterviewProgramService` | Command authorization, idempotency, concurrency, transaction, lifecycle, invalidation, replay, and handoff. | Own live session state or update artifacts in place. |
| `PlannedInterviewRepository` | Immutable artifacts, edges, receipts, command records, outbox, snapshots, and historical bytes under one transaction. | Accept partial artifact/receipt commits. |
| `InterviewExpressionHandoffAdapter` | Project exact armed pack/IAC bytes and declared capabilities for read-only consumption. | Flatten semantic fields, rename source kind, synthesize provenance, or accept on behalf of Interview Expression. |
| `StudioProjectionAdapter` | Reconstruct read models and translate attributable correction commands. | Become canonical AIR state or silently patch contracts. |

### Workflow A - compile the Planned Activative Intelligence Pack

1. `CompilePlannedActivativeIntelligenceCommand` supplies caller-generated IDs/times, expected aggregate version, authority/actor refs, exact F02 Context Premise/Resonance/Matrix/Edge refs, exact F03 portfolio/selected-hypothesis/gate/evaluation/stop/promotion refs, source context, Primitive registry snapshot, interview objective, relationship/interviewer context, policy/profile refs, and inherited locks.
2. The service resolves every `ImmutableRef` by ID, version, SHA-256, owner, and lifecycle. A stale, invalidated, cross-brand, or unresolved ref blocks before proposal work.
3. The validator confirms the F03 selection is decisive and current, its complete portfolio remains reachable, its source-kind/provenance is legal, and its F02 lineage matches the exact selected hypothesis. It cannot recompute or replace either draft interface.
4. The compiler constructs a planned pack containing broad signal, intended state transition, roles, pressures, directions, coalition/Primitive hypotheses, participation invitation, intended reaction, smallest commitment, counteractivation, evidence expectations, limits, and inherited/additive locks.
5. Material assertions remain `planned` or `inferred` with evidence refs. No future Reaction Receipt or Expression Moment field is populated.
6. Deterministic validation runs. On success the repository atomically commits pack bytes, dependency edges, command record, event, outbox item, and `PlannedAIPCompilationReceipt`. The pack state is `COMPILED_PENDING_IAC` and not session-eligible.

### Workflow B - compile complete Interview Asset Contracts

1. `CompileInterviewAssetContractsCommand` pins the pack version, objective, interview profile, source/relationship/interviewer context, Primitive registry, evaluation profile, route taxonomy, compatibility profile, and an explicit requested contract count or bounded portfolio policy.
2. A deterministic context assembler exposes only admitted fields to the proposal port. It includes required source spans and semantic refs, `PRM-PRS-009`, `PRM-PRS-002`, and `PRM-PSY-008` applicability envelopes, hard negatives, and prohibited claims.
3. The proposal port may suggest state wording, anchors, questions, branches, landings, and route hypotheses in the closed candidate shape. It cannot emit IDs/times/hashes, statuses, evaluation decisions, approvals, or live facts.
4. For each candidate, the compiler builds a complete IAC. A selected First-Line Anchor and Depth Anchor are mandatory. Any alternative anchor set follows the pinned profile; the legacy three-option pattern is not silently generalized into a constitutional threshold.
5. Every one of the seven branch conditions is present with a bounded action, allowed pressure delta, recovery/stop behavior, and reason. A no-action branch is permitted only as an explicit `HOLD_OR_STOP` outcome with rationale; omission is not permitted.
6. Route possibilities are stored as `PLANNED_UNCONFIRMED`. They cannot make an asset family, clip, derivative, or visual demand eligible.
7. Deterministic validation rejects generic/question-only, fabricated, coercive, identity-attacking, over-ceiling, unlanded, route-confused, or lineage-incomplete candidates.
8. The repository atomically commits candidate IAC versions, edges, compiler receipt, and events. State becomes `COMPILED_PENDING_EVALUATION`.

### Workflow C - independent evaluation and human arming

1. `RequestInterviewPlanEvaluationCommand` pins exact pack/IAC hashes, evaluation profile ID/version/hash, validator result, and all evidence refs. The compiler principal cannot be the independent evaluator principal.
2. Deterministic checks are repeated before dispatch. The evaluator returns a signed/attributable receipt with per-rule outcomes, disagreements, blockers, limitations, and evaluated hashes. The receipt remains owned by Independent Evaluation.
3. A failed or unavailable evaluation leaves the candidate immutable and ineligible. Repair requires a new IAC version linked to the failed result and bounded repair scope.
4. A passing receipt permits, but does not itself perform, human arming. `ArmInterviewProgramCommand` requires an authorized human actor, exact evaluation receipt, exact pack/IAC hashes, session-context ref, declared deviations, consent/readiness dependency refs owned by Interview Expression, and caller-supplied event time.
5. The human may select among validated anchor alternatives, lower the starting pressure, disable an optional route hypothesis, or choose a stricter stop condition. Any semantic change outside the allowed arming envelope requires a new AIR contract version and evaluation.
6. The service appends an `InterviewProgramArmReceipt` and immutable `ArmedInterviewProgramBinding`; it does not mutate the pack or IAC. Interview Expression acknowledges consumption separately.

### Workflow D - live adaptive consumption without authority leakage

1. Interview Expression resolves the exact armed binding and validates its declared compatibility/capability set. It cannot consume stale or superseded current projections.
2. During the session, the authorized interviewer chooses whether to use the main question, anchor, branch, recovery, pause, or stop. The contract is guidance plus bounded constraints, not an autonomous controller.
3. Interview Expression records live execution state and receipts against exact IAC/branch refs. AIR receives immutable refs later; it does not own the live event stream.
4. If the observed answer contradicts the planned current state, exceeds a safety/consent boundary, or shows target-state inappropriateness, the live system stops or recovers under its own governed specification. It must not alter F08 bytes.
5. A landing decision is recorded after evidence. Route eligibility is evaluated from the eventual Expression Moment/source package, not inferred from the plan.

### Workflow E - repair, supersession, cancellation, invalidation, and replay

1. Deterministic/evaluator failure yields a typed blocker and a repair envelope naming only failed fields. `CreateInterviewContractRepairCommand` creates a new version with `repairs_contract_ref`, `failed_receipt_refs`, `frozen_upstream_refs`, and `repair_scope`.
2. Human correction arriving through Studio is captured as a command or HumanResolutionEpisode ref. Promotion into AIR requires an explicit authorized AIR command and produces a new version; it never edits history.
3. Superseding source, identity, Context Premise, Resonance, Matrix/Edge, selected hypothesis, Primitive binding, authority, evaluation profile, compatibility profile, or required lock appends invalidation receipts for dependent current projections.
4. An armed binding remains pinned to the accepted versions negotiated at arming. A material revocation or invalidation before/during a session prevents new consumption and triggers an Interview Expression lifecycle action; historical records remain reproducible.
5. Cancellation appends a receipt and stops future use; it does not delete packs, IACs, evaluation receipts, arm receipts, or session references.
6. Replay resolves stored canonical bytes by hash, replays command/event order, and reproduces the historical artifact and receipt hashes without current registries, clock, random state, environment, or absolute paths.

## 6. Data models, contracts, schemas, and APIs

### Shared scalar and reference rules

All schemas are closed (`additionalProperties: false`). Nonempty text is Unicode NFC, trimmed, and rejects control-only or whitespace-only values. IDs are caller-supplied opaque strings. `ImmutableRef` contains `{object_type, object_id, version, sha256, authoritative_owner, lifecycle_state_at_use}`. Ordered narrative sequences retain order. Semantically unordered sets are deduplicated and sorted by their canonical key. Scores, when a governed profile requires them, use integer micros from `0` to `1_000_000`; no binary floats contribute to identity.

Every root artifact contains `schema_id`, `schema_version`, `artifact_id`, `artifact_version`, `aggregate_id`, `aggregate_version`, `authority_ref`, `owner_product`, `created_by_actor_ref`, `effective_at`, `canonicalization_profile`, `dependency_refs`, `artifact_sha256`, and `lifecycle_state`. `effective_at` is caller supplied and excluded from business ordering unless the governing lifecycle explicitly uses it.

### `PlannedActivativeIntelligencePack`

Schema ID: `ca.air.planned-activative-intelligence-pack/2.1.0-candidate`.

| Field | Type | Owner / invariant |
|---|---|---|
| `planned_pack_ref` | `ImmutableRef` | AIR; immutable version identity. |
| `epistemic_class` | literal `planned` | Required; observed is forbidden. |
| `source_context` | `SourceContext` | Exact inherited F03 source kind and provenance. Unknown/ambiguous kind blocks. |
| `identity_dna_refs` | tuple of `ImmutableRef`, 1..n | Human-owned canonical values; AIR references only. |
| `brand_context_ref`, `voice_dna_ref`, `visual_dna_ref` | `ImmutableRef` | Exact aligned context version; no cross-brand mixing. |
| `context_premise_ref` | `ImmutableRef` | Exact TS-AIR-002 planned Context Premise. |
| `resonance_context_refs` | tuple of `ImmutableRef`, 1..n | Exact audience/relationship/interviewer resonance used. |
| `matrix_of_edging_ref`, `broad_signal_refs`, `tension_site_refs`, `edge_product_ref` | exact refs | Must match selected F03 hypothesis lineage. |
| `portfolio_ref`, `selected_hypothesis_ref` | `ImmutableRef` | Complete F03 portfolio stays reachable; selected ref must be decisive and eligible. |
| `selection_receipt_refs` | tuple of refs | Current gate, comparative evaluation, stopping, and promotion receipts. |
| `interview_objective` | `EpistemicAssertion<InterviewObjective>` | Planned purpose, audience/relationship movement, limits, and success evidence. |
| `selected_activation_hypothesis` | `SelectedActivationProgram` | Broad signal, role, pressure path, activation directions, coalition hypothesis, evidence expectations, and limitations. |
| `target_expression_state` | `TargetExpressionState` | Pack-level intended movement; not observed state. |
| `participation_invitation` | `EpistemicAssertion<NonEmptyText>` | Preserves audience/guest agency. |
| `intended_reaction` | `EpistemicAssertion<NonEmptyText>` | Planned reaction only; no Reaction Receipt implied. |
| `smallest_commitment` | `EpistemicAssertion<NonEmptyText>` | Smallest intended participatory move. |
| `counteractivation_program` | `CounteractivationProgram` | Anticipated resistance, prevention, recovery, and stop boundaries. |
| `primitive_bindings` | tuple of `PrimitiveApplicabilityBinding`, 1..n | Exact registry refs; F08 local jobs and misuse checks. |
| `wrong_reading_locks` | tuple of `WrongReadingLock`, 1..n | Inherited locks plus additive stricter locks; no weakening/removal. |
| `evaluation_profile_ref`, `compatibility_profile_ref` | exact refs | Required and hash-pinned; no local profile fork. |
| `interview_asset_contract_refs` | tuple of refs | Empty only in `COMPILED_PENDING_IAC`; otherwise exact current candidate set. |

`SourceContext.source_kind` is exactly one of `interview_expression`, `public_comment`, `direct_message_reply`, `authored_source`, `live_premise`, `research_synthesis`, `operator_supplied`, or `legacy_migrated`. When it is `interview_expression`, `source_context.interview_provenance` contains at least one nonempty Reaction Receipt ref and one nonempty Expression Moment ref from the already-existing source. This rule does not create evidence for the future planned interview.

### `TargetExpressionState`

Schema ID: `ca.air.target-expression-state/2.1.0-candidate`.

| Field | Type | Rule |
|---|---|---|
| `state_id` | nonempty ID | Stable inside the pack version. |
| `current_state_hypothesis` | `EpistemicAssertion<StateDescription>` | Evidence-linked and planned/inferred; never a persona fact. |
| `target_state` | `EpistemicAssertion<StateDescription>` | Desired expression topology, not exact words or performance. |
| `transition_signals` | tuple of `ObservableSignal`, 1..n | Observable, source-groundable signals; no hidden mind-reading. |
| `inappropriate_conditions` | tuple of `Condition`, 1..n | Conditions under which the target must be abandoned, lowered, or replaced. |
| `relationship_requirements` | tuple of assertions | Trust, context, and interviewer-resonance prerequisites. |
| `pressure_envelope` | `PressureEnvelope` | Starting dose, ceiling, permitted decrease, reset, and stop conditions. |
| `evidence_refs` | tuple of refs, 1..n | Exact premise/Matrix/selected-hypothesis evidence. |

State descriptions use typed dimensions such as specificity, scene access, emotional proximity, contradiction tolerance, meaning articulation, authority, invitation, or teaching only when supported. They cannot label a person globally. `NOT_APPLICABLE` may be used only for an optional dimension and must name why the dimension is irrelevant; it cannot replace the current or target state.

### `InterviewAssetContract`

Schema ID: `ca.air.interview-asset-contract/2.1.0-candidate`.

| Field | Type | Rule |
|---|---|---|
| `contract_ref`, `planned_pack_ref` | exact refs | Same aggregate and exact pack version. |
| `contract_role` | closed enum | `PRIMARY`, `ALTERNATE_ENTRY`, `RECOVERY`, or a profile-governed value. |
| `source_premise_ref`, `matrix_edge_refs`, `selected_hypothesis_ref` | exact refs | Required lineage; generic notes forbidden. |
| `target_expression_state_ref` | exact embedded/ref | Must resolve to a state in the pack. |
| `first_line_anchor_program` | `FirstLineAnchorProgram` | Selected anchor required; alternatives profile-governed. |
| `depth_anchor` | `DepthAnchor` | Required, evidence-linked, dignity-preserving. |
| `main_question` | `QuestionMove` | Specific and natural; cannot be the whole contract. |
| `branch_program` | `BranchProgram` | Contains all seven governed conditions. |
| `pressure_envelope` | `PressureEnvelope` | Cannot exceed pack state envelope. |
| `recovery_program` | `RecoveryProgram` | Pause, clarify, lower pressure, relationship reset, and stop options. |
| `landing_criteria` | `LandingCriteria` | Planned signals and stop law; no prefilled landing result. |
| `expected_source_material` | tuple of `MaterialExpectation`, 1..n | Scene, cost, contradiction, principle, decision, image, or other governed types with evidence rationale. |
| `route_hypotheses` | tuple of `RouteHypothesis` | `PLANNED_UNCONFIRMED`; no production eligibility. |
| `primitive_bindings` | tuple of exact refs | Includes applicable F08 Primitive jobs and constraints. |
| `wrong_reading_locks`, `hard_negatives` | nonempty tuples | Inherit all pack locks; may add stricter locks. |
| `evaluation_profile_ref`, `compatibility_profile_ref` | exact refs | Must match pack or an explicitly compatible governed version. |
| `producer_identity_ref` | authority ref | Cannot equal independent evaluator identity. |

### Anchor, pressure, branch, recovery, landing, and route contracts

`FirstLineAnchorProgram` contains a required `selected_anchor` plus zero or more `alternative_anchors`. Each `FirstLineAnchor` has `{anchor_id, anchor_kind, natural_language_pattern, premise_ref, intended_entry_state, evidence_refs, prohibited_implications, selection_rationale}`. The anchor may invite a scene or truthful first sentence; it may not prescribe the answer, assert an unsupported event, or require a false performance. Where the pinned profile requires cinematic/emotional/reel-hook alternatives, all required alternatives must be present and distinguishable; profiles that do not require three alternatives cannot be failed by a hidden legacy threshold.

`DepthAnchor` has `{anchor_id, depth_move, source_or_tension_refs, intended_transition_signals, maximum_pressure_delta, recovery_if_missed, dignity_guard, misuse_checks}`. The `depth_move` is a closed enum such as `REQUEST_SCENE`, `REQUEST_COST`, `REQUEST_CONTRADICTION`, `REQUEST_DECISION`, `REQUEST_RELATIONAL_EFFECT`, or `REQUEST_MEANING`. It never contains a target answer.

`PressureEnvelope` has `{scale_profile_ref, starting_dose, maximum_dose, permitted_live_direction, reset_dose, escalation_preconditions, deescalation_conditions, stop_conditions}`. Dose values use the pinned profile's closed integer scale. F08 does not define an arbitrary universal numeric threshold. `permitted_live_direction` always allows `LOWER` and `STOP`; `RAISE` is permitted only to the declared maximum and only by an authorized human under satisfied preconditions.

`BranchProgram` contains exactly one `BranchRule` for each required condition:

| Condition | Required intent | Forbidden shortcut |
|---|---|---|
| `ANCHOR_HIT` | Stay with the truth, deepen only if useful, or move to landing. | Interrupt a landed answer merely to use another prepared question. |
| `PARTIAL_HIT` | Preserve what landed and ask one bounded clarifier/depth move. | Restart the whole induction or erase the partial evidence. |
| `DEFENSE` | Lower pressure, externalize the pattern, protect dignity, offer choice. | Attack identity, diagnose motive, or intensify automatically. |
| `TOPIC_ESCAPE` | Name the drift neutrally, reconnect to premise, or accept the new truth if authorized. | Force the guest back to the planned narrative. |
| `CONTRADICTION` | Surface the contradiction as evidence and invite clarification. | Resolve contradiction on the guest's behalf. |
| `OVERLOAD` | Stop escalation, regulate/pause, reduce scope, or terminate. | Treat distress as productive depth. |
| `RELATIONAL_RESET` | Restore shared field, clarify intent/choice, and resume only with human consent. | Use rapport language as a concealed pressure tactic. |

Each `BranchRule` has `{condition, evidence_pattern, action_kind, question_or_action, pressure_delta, maximum_uses, recovery_ref, landing_effect, stop_effect, primitive_constraint_refs, operator_choice_required}`. `action_kind` is one of `ASK`, `CLARIFY`, `REFLECT`, `LOWER_PRESSURE`, `PAUSE`, `RELATIONAL_RESET`, `HOLD_OR_STOP`, or a profile-governed extension. Empty strings and unconstrained free-form action names fail.

`RecoveryProgram` contains ordered, non-coercive options and names which conditions activate them. It must include a stop path. `PRM-PSY-008` enforcement requires problem/behavior wording, dignity protection, clear issue naming, and checks against both toxic positivity and passive aggression.

`LandingCriteria` contains `{candidate_landing_types, observable_signals, minimum_evidence, counter_signals, stop_law, source_capture_expectations, evaluator_profile_ref}`. Types may include principle, emotional recognition, question, decision, relational truth, or profile-governed values. The contract stores criteria only. A later `LandingEvaluationReceipt` has its own owner, exact observed-evidence refs, evaluator/human authority, result, limitations, and timestamp.

`RouteHypothesis` contains `{route_id, asset_family_or_category_ref, semantic_rationale, required_expression_signals, required_source_spans, required_feature_contract_refs, compatibility_profile_ref, status, prohibited_inferences}`. `status` is always `PLANNED_UNCONFIRMED` in F08. Format 02 is not activated by this field. No route inherits certification from another profile.

### Primitive applicability and wrong-reading locks

`PrimitiveApplicabilityBinding` contains `{primitive_id, registry_version, primitive_sha256, local_job, trigger_evidence_refs, suppression_decision, conflict_refs, misuse_checks, applicability_result}`. Required active bindings are:

- `PRM-PRS-009`: use supported status-quo disruption; block `FALSE_JEOPARDY` and `STRANDED_DISEQUILIBRIUM`;
- `PRM-PRS-002`: preserve tension-to-release structure; block `UNRESOLVED_TENSION` and `MICRO_TENSION_EXHAUSTION`;
- `PRM-PSY-008`: separate person from problem while naming the issue; block `TOXIC_POSITIVITY` and `PASSIVE_AGGRESSION`.

If a Primitive is suppressed by its exact source condition, the binding uses a typed `SUPPRESSED_WITH_EVIDENCE` result; it is not silently omitted and is not marked globally inapplicable.

Each IAC inherits every pack `WrongReadingLock` by exact parent-lock ref and hash. A child may add a stricter lock but cannot remove, weaken, reinterpret, or replace a parent lock. Relaxation requires an authorized new upstream pack version. Realization evidence is not F08-owned.

### Lifecycle, commands, events, receipts, and repository API

Pack lifecycle: `COMPILED_PENDING_IAC -> IAC_COMPILED -> PENDING_EVALUATION -> EVALUATED_ELIGIBLE | EVALUATED_BLOCKED -> ARMED | CANCELLED | SUPERSEDED | INVALIDATED`. IAC lifecycle mirrors the relevant candidate/evaluation states. An artifact does not transition by mutation; lifecycle projections are derived from append-only events and receipts.

Commands:

- `CompilePlannedActivativeIntelligenceCommand`;
- `CompileInterviewAssetContractsCommand`;
- `RequestInterviewPlanEvaluationCommand`;
- `RecordInterviewPlanEvaluationCommand`;
- `CreateInterviewContractRepairCommand`;
- `ArmInterviewProgramCommand`;
- `AcknowledgeInterviewProgramConsumptionCommand`;
- `SupersedePlannedInterviewProgramCommand`;
- `InvalidatePlannedInterviewProgramCommand`;
- `CancelPlannedInterviewProgramCommand`;
- `ReplayPlannedInterviewProgramCommand`.

Each command envelope contains `{command_id, idempotency_key, command_type, aggregate_id, expected_aggregate_version, actor_ref, authority_ref, issued_at, input_refs, canonical_payload_sha256}`. Authorization is checked before semantic compilation.

Events include `PlannedAIPCompiled`, `InterviewAssetContractsCompiled`, `InterviewPlanEvaluationRequested`, `InterviewPlanEvaluated`, `InterviewContractRepairCreated`, `InterviewProgramArmed`, `InterviewProgramConsumptionAcknowledged`, `PlannedInterviewProgramSuperseded`, `PlannedInterviewProgramInvalidated`, and `PlannedInterviewProgramCancelled`.

Receipts include exact input/output hashes, actor/authority, command and aggregate versions, dependency edges, validator/evaluator profile refs, decision code, limitations, event/outbox refs, and transaction ID. Production acceptance and downstream consumption acknowledgement are not concepts collapsed here: human arming authorizes a session-specific plan; Interview Expression separately acknowledges consumption; later asset production/consumption remains outside F08.

The repository port exposes transactional `execute(command, expected_version)`, immutable `get(ref)`, `get_by_hash`, `resolve_dependencies`, `current_projection`, `append_invalidation`, `replay(aggregate_id, through_event)`, and `verify_artifact_receipt_parity`. A transaction stages artifacts, edges, command record, lifecycle events, receipts, and outbox records, validates all hashes, and then commits once.

### Canonical serialization and compatibility

Canonical JSON uses UTF-8 without BOM, Unicode NFC, LF normalization for semantic text, lexicographic object keys, preserved list order where order is meaningful, canonical sorting for declared sets, no insignificant whitespace, base-10 integer rendering, and no absolute filesystem path. Artifact identity excludes storage location and runtime metadata. A positive replay on another machine must reproduce the same canonical bytes and SHA-256.

Compatibility is semantic, not parser-only. A consumer declares required schema IDs/versions, source-kind/profile support, seven branch conditions, pressure-envelope behavior, lock inheritance, route-state semantics, evaluation receipt support, and owner/authority enforcement. Unsupported required features fail before arming. An adapter cannot drop a condition, downgrade a lock, flatten an epistemic state, rename an owner, or map `PLANNED_UNCONFIRMED` to eligible.

## 7. Implementation stages and exact target paths

This section defines a future implementation plan only. It is not a Development Capsule or authorization to create these paths.

| Stage | Exact future targets | Completion boundary |
|---|---|---|
| 0 - capsule and source lock | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-008/DEVELOPMENT_CAPSULE.md`; `.../SOURCE_LOCK.yaml`; `.../ALLOWED_PATHS.yaml` | Requires ratified authority and separately issued capsule; all source/upstream hashes and owner decisions pinned. |
| 1 - domain contracts | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/planned_interview_program.py`; `.../domain/interview_asset_contract.py`; `.../domain/interview_branching.py` | Immutable closed types, epistemic states, ownership, seven branches, pressure/recovery/landing, locks, and route hypotheses. |
| 2 - canonical schemas | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f08.planned-aip.schema.json`; `.../air.f08.interview-asset-contract.schema.json`; `.../air.f08.interview-plan-receipts.schema.json` | Generated from canonical domain source; positive/negative fixtures; no shared release bytes in this stage. |
| 3 - canonical serialization and repository | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/serialization/canonical.py`; `.../repositories/planned_interview_repository.py` | Stable hashes, immutable versions, atomic commit, optimistic concurrency, idempotency, receipt parity, replay. |
| 4 - compilers and validation | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/planned_aip_compiler.py`; `.../services/interview_asset_contract_compiler.py`; `.../validation/f08_validator.py` | AIR-FR-043 through 048 deterministic behavior; model proposals remain bounded and non-authoritative. |
| 5 - independent evaluation boundary | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/f08_evaluation_port.py`; `.../services/interview_plan_evaluation_service.py` | Separate producer/evaluator identities, profile-pinned receipts, disagreement and unavailable-evaluator behavior. |
| 6 - lifecycle and invalidation | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/planned_interview_program_service.py`; `.../invalidation/f08_invalidation_projector.py` | Arm/supersede/cancel/invalidate/replay without mutation or history loss. |
| 7 - product adapters | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/interview_expression_handoff.py`; `.../adapters/studio_projection.py` | Read-only Interview Expression handoff and reconstructable Studio projection; ownership denial evidence. |
| 8 - migrations | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/migrations/studio_interview_contract_v1.py`; `.../migrations/ai_v2_planned_interview.py` | New immutable artifacts only when mapping is complete; no guessed source kind, provenance, branch, state, owner, or lock. |
| 9 - evidence suite | Paths in section 10 | Unit, property, contract, integration, architecture, migration, fault-injection, replay, and clean-room evidence. |

No Stage may edit VAE, Delegation release bytes, Builder behavior, current constitutional authority, historical receipts, or imported source history. Cross-product schema publication is a later separately governed release step.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Condition | Required behavior |
|---|---|---|
| `AIR_F08_UPSTREAM_DRAFT_DRIFT` | TS-AIR-002 or TS-AIR-003 path/state/bytes/hash differs from Wave 3 lock. | Stop writing/build advancement; reopen sections 3, 5, 6, 8, 9, 10. |
| `AIR_F08_AUTHORITY_NOT_CURRENT_FOR_BUILD` | Build/capsule requested before ratification/adoption. | Deny; preserve specification-only state. |
| `AIR_F08_UPSTREAM_LINEAGE_INCOMPLETE` | Required F02/F03/source/identity/Matrix/selection ref missing or mismatched. | Reject before proposal; name each missing/stale ref. |
| `AIR_F08_SOURCE_KIND_UNKNOWN` | Source kind is absent, ambiguous, or outside governed enum. | Reject; never guess or default. |
| `AIR_F08_INTERVIEW_PROVENANCE_REQUIRED` | Existing source kind is `interview_expression` without Reaction Receipt and Expression Moment refs. | Reject inherited source context; do not fabricate refs. |
| `AIR_F08_FUTURE_REACTION_FABRICATION` | Planned pack/IAC claims future Reaction Receipt, Expression Moment, landing, or route observation. | Reject with authority/epistemic denial receipt. |
| `AIR_F08_QUESTION_ONLY_CONTRACT` | Candidate supplies question(s) without complete state/anchor/branch/dose/landing/route/lock contract. | Reject deterministically. |
| `AIR_F08_TARGET_STATE_UNGROUNDED` | State lacks evidence, transition signals, or inappropriate conditions. | Reject; request attributable evidence or bounded repair. |
| `AIR_F08_BRANCH_SET_INCOMPLETE` | Any required branch condition is absent or duplicated. | Reject and enumerate missing/duplicate conditions. |
| `AIR_F08_PRESSURE_CEILING_VIOLATED` | Starting dose, branch delta, or automated behavior exceeds envelope. | Reject; live consumer must lower/stop. |
| `AIR_F08_DIGNITY_GUARD_VIOLATED` | Branch attacks identity, conceals critique, or uses passive aggression. | Reject under PRM-PSY-008. |
| `AIR_F08_FALSE_JEOPARDY` | Inciting event is unsupported or exaggerated as fact. | Reject under PRM-PRS-009. |
| `AIR_F08_LANDING_NOT_CONNECTED` | Tension has no commensurate honest landing/stop law. | Reject under PRM-PRS-002. |
| `AIR_F08_EXPRESSION_ROUTE_CONFUSION` | Target expression state is used as output archetype or route is treated as confirmed. | Reject and preserve distinction. |
| `AIR_F08_PARENT_LOCK_WEAKENED` | IAC omits, removes, or weakens pack lock. | Reject; require new authorized upstream pack to relax. |
| `AIR_F08_EVALUATION_NOT_INDEPENDENT` | Producer identity equals evaluator authority or evaluator profile is unpinned. | Reject evaluation receipt. |
| `AIR_F08_HUMAN_ARMING_REQUIRED` | Consumer/binding attempted without attributable human arm receipt. | Deny; evaluation alone is insufficient. |
| `AIR_F08_COMPATIBILITY_UNSUPPORTED` | Consumer lacks a required schema/branch/lock/profile capability. | Reject before binding; no parse-only compatibility. |
| `AIR_F08_IDEMPOTENCY_CONFLICT` | Same idempotency key has different canonical input hash. | Return conflict; store neither new artifact nor receipt. |
| `AIR_F08_CONCURRENT_MODIFICATION` | Expected aggregate version differs from current projection. | Reject atomically; caller reloads and issues a new command. |
| `AIR_F08_ATOMIC_COMMIT_FAILED` | Any staged artifact/edge/event/receipt/outbox write fails. | Roll back entire transaction and emit only infrastructure telemetry outside semantic store. |
| `AIR_F08_STALE_OR_INVALIDATED` | Arm/consume against superseded, cancelled, revoked, or invalidated version. | Deny current consumption; historical replay remains available. |
| `AIR_F08_MIGRATION_MEANING_MISSING` | Legacy data cannot prove mandatory meaning or owner. | Preserve legacy bytes and block migration; never fill gaps. |
| `AIR_F08_ABSOLUTE_PATH_CONTAMINATION` | Canonical artifact or receipt contains machine path. | Reject serialization and name the field. |

### Migration and compatibility

The Studio V1 adapter emits a new F08 artifact only from a complete, attributable mapping. It preserves original UUIDs/timestamps as legacy evidence, not canonical generated identity; maps known expression states, anchor alternatives, depth, expected material, landing targets, repairs, and routes; and attaches the exact legacy artifact hash. It must separately supply F02/F03 lineage, source-kind/provenance, state transition, all branch cases, pressure/recovery, locks, profile refs, and owners from current evidence. If any mandatory field is absent, `AIR_F08_MIGRATION_MEANING_MISSING` is the result.

Deprecated schemas remain readable for historical delegations and replay but cannot become current by parser success alone. Active bindings stay pinned to the versions negotiated at arming. A migration creates new immutable artifacts and a migration receipt; it never overwrites the source record or invalidates unrelated historical sessions.

### Rollback, recovery, invalidation, and replay

Fault injection after every staged write must prove all-or-nothing commit. A worker crash after commit but before response is recovered by idempotency lookup and returns the original receipt. A conflicting retry returns `AIR_F08_IDEMPOTENCY_CONFLICT`. Concurrency conflicts never invoke the proposal port twice under the same successful command identity.

Invalidation traverses stored dependency edges from the materially changed parent and appends descendant-specific receipts. It does not erase artifacts, invalidate siblings without an edge, or rewrite an armed historical binding. A current session-facing projection refuses stale versions. Historical replay uses stored bytes and registry snapshots to reproduce the earlier decision even if the current registry, profile, or source authority has changed.

### Observability

Structured telemetry includes command type/ID, aggregate/version, actor/authority IDs, artifact and dependency hashes, source kind without source contents, compiler/proposal/evaluator/profile versions, deterministic gate codes, Primitive applicability/misuse codes, branch completeness, pressure-envelope decisions, lock-inheritance result, evaluation/arming/consumption state, idempotency outcome, transaction ID, invalidation cause, replay result, and latency. Logs must not include interview answer text, hidden prompts, secrets, absolute paths, or unredacted private source material. Metrics may count failure codes and lifecycle states but may not convert local pass rates into certification claims.

## 9. Behavior-specific acceptance criteria

| AC | Requirement / Story | Positive behavior | Adversarial or recovery behavior | Evidence class |
|---|---|---|---|---|
| AC-01 | AIR-FR-043 / AIR-ST-08.01 | Given exact eligible F02/F03 refs, compilation produces a planned pack with full identity/context/Matrix/portfolio/selection/role/pressure/participation/reaction/commitment/counteractivation/lock lineage. | A selected-hypothesis text without portfolio/receipt refs returns `AIR_F08_UPSTREAM_LINEAGE_INCOMPLETE`. | contract + integration |
| AC-02 | AIR-FR-043 / AIR-ST-08.01 | Pack assertions are planned/inferred and include evidence/limitations; no future Reaction Receipt or Expression Moment exists. | A proposal emits an observed landing or fabricated future receipt and is rejected `AIR_F08_FUTURE_REACTION_FABRICATION`. | unit + epistemic contract |
| AC-03 | AIR-FR-043 / AIR-ST-08.01 | Existing `interview_expression` source context carries at least one Reaction Receipt and Expression Moment ref; all other kinds validate their optional provenance. | Missing/unknown source kind or guessed migration classification fails exactly. | schema + migration |
| AC-04 | AIR-FR-044 / AIR-ST-08.01 | Each IAC includes current/target state, selected First-Line Anchor, Depth Anchor, question, all branches, pressure/recovery, landing, routes, locks, and exact lineage. | A natural generic question or valid anchor without the remaining contract returns `AIR_F08_QUESTION_ONLY_CONTRACT`. | domain + contract |
| AC-05 | AIR-FR-045 / AIR-ST-08.02 | Target state names current hypothesis, desired movement, observable transition signals, inappropriate conditions, relationship requirements, pressure envelope, and evidence. | A global personality label or target feeling with no inappropriate conditions is rejected. | unit + adversarial |
| AC-06 | AIR-FR-046 / AIR-ST-08.02 | First-Line Anchor exposes a supported premise and Depth Anchor requests lived specificity without dictating truth. | Fabricated disruption, prescribed answer, or unsupported vulnerability demand fails PRM-PRS-009/PSY-008 checks. | Primitive fixture + evaluator |
| AC-07 | AIR-FR-047 / AIR-ST-08.03 | Branch program contains exactly one rule for all seven conditions with bounded pressure, recovery/stop, and human choice. | Missing `OVERLOAD`, duplicate `DEFENSE`, or free-form unknown branch fails `AIR_F08_BRANCH_SET_INCOMPLETE`. | schema + property |
| AC-08 | AIR-FR-047 / AIR-ST-08.03 | Defense/overload/reset branches lower pressure or stop while naming the behavioral issue without attacking identity. | Automatic escalation, toxic positivity, passive aggression, or pressure beyond ceiling is rejected. | Primitive + boundary |
| AC-09 | AIR-FR-048 / AIR-ST-08.03 | Landing criteria connect tension to honest release/meaning/decision/question or stop; live outcome remains absent. | A high-tension path without landing or stop fails `AIR_F08_LANDING_NOT_CONNECTED`. | domain + evaluator |
| AC-10 | AIR-FR-048 / AIR-ST-08.03 | Route hypotheses state required expression/source evidence and remain `PLANNED_UNCONFIRMED`. | Expression state used as an archetype or planned route treated as asset eligibility fails `AIR_F08_EXPRESSION_ROUTE_CONFUSION`. | contract + cross-product |
| AC-11 | ownership | AIR compiles semantic plan, human arms/chooses, Interview Expression owns live state/evidence, evaluator owns evaluation, Studio projects/captures correction. | Any product attempts another owner's write and receives an authority-boundary denial receipt. | architecture |
| AC-12 | evaluation/arming | Separate evaluator produces a profile-pinned pass receipt; an authorized human then arms exact hashes for one session context. | Compiler self-evaluation or evaluation-only session binding is rejected. | integration + architecture |
| AC-13 | lock inheritance | Every IAC carries exact parent-lock refs/hashes and may add a stricter child lock. | Omission, weakening, or replacement fails `AIR_F08_PARENT_LOCK_WEAKENED`. | property + contract |
| AC-14 | `NOT_APPLICABLE` | Optional profile field may be N/A only with reason, authority/evidence, and validator proof. | Required branch, landing, pressure, lock, or lineage field marked N/A is rejected. | schema + negative fixtures |
| AC-15 | determinism | Two clean processes with identical semantic inputs produce byte-identical artifacts/receipts despite shuffled map/set/traversal input. | Current time, random UUID, environment variable, filesystem order, or absolute path changes identity and test fails. | property + clean-room |
| AC-16 | idempotency/concurrency/atomicity | Identical retry returns original receipt; expected-version conflict is typed; injected write failure leaves no partial artifact/receipt/edge/outbox. | Same key/different payload and every commit-fault point are denied without residue. | repository + fault injection |
| AC-17 | invalidation/replay | Material parent change invalidates only current descendants while old pack/IAC/evaluation/arm bytes replay by hash. | Unrelated pack invalidated or old bytes deleted is a test failure. | recovery + historical replay |
| AC-18 | compatibility | Consumer proves support for exact schemas, seven branches, pressure, locks, source/provenance, evaluation, and profile semantics before binding. | Parser-only adapter that drops a field is rejected `AIR_F08_COMPATIBILITY_UNSUPPORTED`. | producer/consumer conformance |
| AC-19 | migration | Complete predecessor maps into a new immutable version with original hash and explicit owner/lineage; incomplete record blocks. | Adapter invents source kind, branch, state, route eligibility, provenance, owner, or lock and fails. | migration |
| AC-20 | imported source | Imported interview slice starts from actual Interview Expression source package without retroactive planned artifacts. | Adapter manufactures Planned AIP/IAC history and is rejected. | reference-slice |
| AC-21 | claim ceiling | Spec/receipts remain `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, build false. | Any capsule/build/production/certification claim fails factory validation. | governance |

## 10. Testing and completion evidence

### Required future test suites

| Exact future path | Required coverage |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_planned_aip.py` | Full lineage, planned epistemology, source-kind/provenance, selection receipts, roles/pressure/participation/reaction/commitment/counteractivation, lock completeness. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_target_expression_state.py` | Current/target state, observable signals, inappropriate conditions, relationship requirements, pressure envelope, typed N/A denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_interview_asset_contract.py` | Complete contract versus question-only, anchors, expected material, route state, hard negatives, closed enums. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_interview_branch_program.py` | Exactly seven conditions, bounded actions, dose ceiling, stop path, dignity, no duplicates/unknowns. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_f08_primitive_applicability.py` | Exact PRM-PRS-009/002 and PRM-PSY-008 hashes, trigger/suppression, false jeopardy, stranded disequilibrium, unresolved tension, micro-tension exhaustion, toxic positivity, passive aggression. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_f08_lock_inheritance.py` | Parent lock preservation, stricter additions, weakening/removal denial, authorized new-version relaxation. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/property/test_f08_canonical_serialization.py` | Unicode, key/set order, traversal order, time/random/env/path independence, stable bytes and hashes. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/repository/test_planned_interview_repository.py` | Immutable versions, idempotency, expected-version conflicts, command/artifact/receipt parity, replay. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/fault_injection/test_f08_atomic_commit.py` | Failure after every staged artifact/edge/event/receipt/outbox operation leaves no partial semantic state. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f08_compile_and_arm.py` | AIR-FR-043 through 048, all Story terminal conditions, evaluator separation, human arming, read-only handoff. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f08_invalidation_and_replay.py` | Selective descendant invalidation, cancellation, supersession, historical byte reproduction, pinned active binding. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_f08_interview_expression_handoff.py` | Source/provenance, exact refs, branch/pressure/lock/profile support, consumption acknowledgement, stale denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_f08_evaluation_boundary.py` | Independent identity, profile hash, no self-approval, no certification inference, unavailable/disagreement behavior. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_studio_interview_contract_v1.py` | Lossless attributable mapping, blocked missing meaning, no guessed classifications, preserved legacy hash. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_imported_interview_no_planned_history.py` | Imported source starts from actual Interview Expression evidence and never fabricates F08 history. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_f08_product_boundaries.py` | AIR/human/Interview Expression/evaluator/Studio/Builder/Pipeline/VAE/Delegation ownership and `Activative Contract Compiler != AIR`. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/clean_room/test_f08_portability.py` | Fresh-process reproduction with different temp roots, locale-safe UTF-8, no absolute path or hidden environment dependency. |

### Required fixtures and adversarial matrix

Future fixtures must include: complete direct-interview plan; existing interview-derived plan with valid provenance; each other governed source kind; unknown and ambiguous source kind; missing Reaction Receipt/Expression Moment; question-only candidate; generic journey question; unsupported inciting event; false jeopardy; stranded disequilibrium; complete/partial/defensive/topic-escape/contradictory/overloaded/reset responses; missing and duplicate branch; over-ceiling dose; forced vulnerability; identity attack; toxic-positive non-critique; passive-aggressive recovery; valid landing; unresolved tension; expression/archetype confusion; planned route falsely eligible; missing/inherited/weakened locks; evaluator self-approval; absent human arm; stale pack/IAC/evaluation/profile; unsupported consumer capability; valid and incomplete Studio migration; imported source with no invented plan; idempotent retry; conflicting retry; concurrent write; each transaction-fault point; shuffled canonical input; injected time/random/environment/path; selective invalidation; historical replay after registry change.

### Completion evidence contract

An eventual implementation may be considered technically complete for independent review only when it provides:

1. a ratified/current authority receipt and a separately authorized Development Capsule with exact allowed paths;
2. source/Primitive/upstream locks and a generated-schema manifest;
3. unit, property, contract, integration, architecture, migration, fault-injection, replay, and clean-room test results tied to exact commit and artifact hashes;
4. deterministic artifact/receipt golden hashes reproduced twice in fresh processes and once under a different workspace root;
5. artifact/receipt/command/outbox parity proof and rollback evidence for every injected fault point;
6. Independent Evaluation evidence showing distinct producer/evaluator identities and profile versions, without converting local evidence into certification;
7. Interview Expression producer/consumer conformance using exact pinned schemas and semantic features;
8. an ownership-boundary report proving AIR cannot write live reaction/source state and consumers cannot mutate AIR meaning;
9. migration receipts for every converted predecessor plus blocked receipts for incomplete cases;
10. an implementation completion receipt whose claim ceiling remains separate from production, publication, provider, and certification authority.

The writer completion evidence for this document is limited to the V3.3 writing receipt, files-read receipt, source traceability, draft-dependency receipt, and writer file manifest. The next lifecycle action is independent audit by a different agent. No audit, revision, acceptance, build, capsule, code, schema, or release work is performed here.
