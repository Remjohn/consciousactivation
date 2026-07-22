---
type: technical_specification
spec_id: TS-AIR-011
title: Expression Moments and Observed Activative Intelligence
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
adoption_status: NOT_APPLICABLE
build_status: NOT_BUILD_READY
gate: GATE_B_VERTICAL_RUNTIME_AND_INTEGRATION
writing_wave: 8
controlling_frs:
  - AIR-FR-065
controlling_stories:
  - AIR-ST-11.03
upstream_draft_dependencies:
  - spec_id: TS-INT-004
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: e6147fc8ca8f8d6d3a0ff8954336fe9b844c8e18e45c41b330c558f7d87a0d5a
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-INT-006
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 3fb216913d8e0c52e3a51db65b6a3c848240cc3d040f9806fd8d3c85a443f58d
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-011 - Expression Moments and Observed Activative Intelligence

This candidate specification defines the Activative Intelligence Runtime (AIR) compilation of one immutable `ObservedActivativeIntelligencePack` from approved, exact, Interview Expression-owned evidence. AIR owns the semantic compilation: what actually activated or failed to activate; evidence-bounded roles, directions, pressures, urges, edges, Primitive and archetype implications; reactions and limitations; the planned-observed delta interpretation; unresolved inferences; transfer requirements; and wrong-reading updates. Interview Expression (IE) remains the authoritative owner of source packages, Reaction Observations and Receipts, tag/Anchor Hit/Expression Moment evidence, approvals, and source-evidence handoffs. AIR references those bytes and never mutates or locally normalizes them.

The exact packet controls only `AIR-FR-065` and `AIR-ST-11.03`. The Story's `AIR-FR-066` source-handoff duty remains implemented by `TS-INT-004` and is consumed here as an interface constraint, not re-owned. The V2.1 authority package is `CANDIDATE_NOT_CURRENT`. Writing is authorized by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`; build authority is false, and no pre-ratification lifecycle may exceed `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. This document creates no code, schema, generated type, contract release, product adoption, Development Capsule, build, production, publication, provider, evaluation-certification, Format 02, or VAE Stage 5 authority.

`TS-INT-004` and `TS-INT-006` are exact hash-pinned `WRITTEN_PENDING_AUDIT` interface drafts and are therefore `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Their bytes are not ratified or accepted architecture. A change to either pinned draft reopens sections 3, 5, 6, 8, 9, and 10 for recorded downstream revision-impact review.

## 1. Files and authorities read

### 1.1 Current and candidate authority

All digests are SHA-256 over the exact bytes read.

| Input | State | Bytes | SHA-256 | Specific use |
|---|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | current authority registry | 791 | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Confirms Constitution V1.1 remains current until governed ratification. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | highest current constitutional authority | 40,830 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Preserves Activative semantic lineage, human-reaction/source truth, Expression Moment, Primitive, wrong-reading, and product-boundary law. |
| `.../doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `CANDIDATE_NOT_CURRENT` | 51,243 | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Candidate sections 17-18 require approved source-backed moments, separate planned/observed intelligence, explicit actual/nonactual outcomes, unresolved inference, source refs, and planned-observed delta. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending human ratification | 4,289 | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | AIR owns semantic lifecycle/Primitive/archetype programs; IE owns reaction/moment/source evidence. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending human ratification | 4,263 | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Assigns `Observed_Activative_Intelligence` to AIR and its source evidence to IE. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/PRODUCT_ROOT_REGISTRY.yaml` | intended-root registry | 1,621 | `bb898168c770a09d0d6974c3ed347cf07b7770ccc41da094bb325c1777baa0be` | Reserves the AIR root without authorizing a source tree. |

The current V1.1 Constitution takes precedence. Candidate V2.1 detail is usable only under the explicit specification-work authorization and cannot be represented as current law.

### 1.2 Requirement, Story, reconciliation, and writing inputs

| Input | Bytes | SHA-256 | Specific use |
|---|---:|---|---|
| `.../prd/features/F11-expression-moments-and-observed-activative-intelligence.md` | 40,218 | `7362192f28832e0ab745e0c57adfa5af6c30183990c39b0c49d360ab4bbcc09a` | Candidate FR text, evidence, invariants, and denial case for `AIR-FR-065`. |
| `.../planning/EPICS_AND_VERTICAL_STORIES.md` | 301,040 | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | Exact `AIR-ST-11.03`, recovery, CBAR, terminal state, and required evidence. |
| `.../specs/TS-AIR-011-expression-moments-and-observed-activative-intelligence.md` | 27,991 | `5052b69a297d71480b3cb070836d20799477a7c1d5850bd0d85dfd818107c386` | Full donor, split at the current AIR semantic/IE source-evidence boundary. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SPEC_DISPOSITION_REPORT.md` | 15,463 | `86852420631241ce6341a04d258f476473d0490274bb4e22675301cb02c13241` | Requires `SPLIT_FOR_IMPLEMENTATION`: AIR owns Observed AIP compilation; IE owns Expression Moment evidence/provenance. |
| `.../CANONICAL_SPEC_LEDGER.csv` | 23,269 | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Freezes exact spec identity, AIR owner, path, Wave 8, one FR, one Story, and claim ceiling. |
| `.../CANONICAL_FR_LEDGER.csv` | 104,516 | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Assigns `AIR-FR-065` to AIR/this spec and `AIR-FR-066` to IE/TS-INT-004. |
| `.../FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | 236,715 | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Freezes FR/Story/owner/spec/source/evidence/claim-ceiling trace. |
| `.../SPEC_DEPENDENCY_DAG.yaml` | 9,178 | `1cf4299781e76c9c80f4489291a92b0a5e1f666f91b8cf9476307a03da5257eb` | Identifies the two upstream write interfaces. |
| `.../PATH_OWNERSHIP_REGISTRY.yaml` | 11,589 | `f260e400384a67f837b67a8a8981a4b773cd8792135eeca20c94f065468296a7` | Reserves only `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-011.md`. |
| `.../SOURCE_DISPOSITION_LEDGER.yaml` | 134,201 | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Classifies expression contract and interview doctrine as required unique evidence and source-first predecessor as superseded. |
| `.../SOURCE_GAP_NOTICE.yaml` | 17,743 | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | Confirms no unavailable required input supports this spec. |
| `.../RECONCILIATION_INPUT_HASH_LOCK.yaml` | 24,593 | `ea28bcab299e74adb87f3bce8ab8a1d20093d4d8699e9e10c5d387383363c456` | Locks admitted archive/member bytes. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | 107,141 | `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | Classifies SDE-032/033 as write-interface dependencies, not acceptance/build blockers. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_WRITING_WAVE_DAG.yaml` | 5,260 | `24b26b9820a0f2cab0cd01ab4c46e9aca476219f496644c063533ee602ccff60` | Places this spec in Wave 8. |
| `.../V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | 1,221 | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Requires candidate label, build false, and acceptance ceiling. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | 1,462 | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes specification writing/review but no build. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv` | 18,768 | `3fa4793ea2baca46dcfbf8e123d039a59ab2467e5814471d49b3daf65e588a73` | Confirms direct AIR spec path and no applicable `AGENTS.md`. |
| `.../V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact `CA-P03-WRITE-TS-AIR-011-RECOVERY` one-spec packet. |
| `.../wave-receipts/WAVE_08_DISPATCH_LOCK.yaml` | 898 | `3d0b252c245e2f671b9b319afeb09893b4d89995ae506aa02b9097abf8a13797` | Pins both IE drafts to exact state and hash. |
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/.../skills/CA_TECH_SPEC_WRITE_SKILL.md` | 9,624 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | V3.3 one-spec writer law and ten-section/receipt requirements. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/MASTER_STATUS.md` | 4,809 | `71d7fdac3c9498c42133c95e141b31241b0fa613426417d9fd81b3d1d656f491` | Preserves implementation/production/certification false. |

The F11 candidate PRD row labels `AIR-FR-065` as IE-owned, which conflicts with its own “Runtime shall compile” behavior and the later Prompt 02 canonical reconciliation. The attributable reconciliation explicitly assigns semantic compilation to AIR while IE owns source evidence. This document records that conflict and follows the frozen packet/ownership ledgers; it does not silently treat the subordinate owner label as current.

### 1.3 Exact upstream draft interfaces

| Edge | Draft | State | Bytes | SHA-256 | Interface consumed | Hash-change revision impact |
|---|---|---|---:|---|---|---|
| SDE-032 | `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-004.md` | `WRITTEN_PENDING_AUDIT` | 99,774 | `e6147fc8ca8f8d6d3a0ff8954336fe9b844c8e18e45c41b330c558f7d87a0d5a` | `ObservedActivativeEvidenceHandoff`, approved moment refs, tag provenance/lifecycle, rejected/borderline evidence, source authority, limitations, wrong-reading risks, maximum claim, handoff receipt | sections 3, 5, 6, 8, 9, 10 |
| SDE-033 | `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-006.md` | `WRITTEN_PENDING_AUDIT` | 84,791 | `3fb216913d8e0c52e3a51db65b6a3c848240cc3d040f9806fd8d3c85a443f58d` | exact Reaction Receipts, planned-observed delta evidence, observations/outcomes/counteractivation, evaluator, maximum claim, lifecycle, source authority | sections 3, 5, 6, 8, 9, 10 |

Both are `DRAFT_DEPENDENCY_NOT_ACCEPTED`. AIR may consume immutable refs and exact evidence-bearing interfaces; it may not import IE's write services, change lifecycle, or reproduce an AIR-local authoritative copy.

### 1.4 Required source and Primitive evidence

| Source | State | Bytes | SHA-256 | Use |
|---|---|---:|---|---|
| `.../sources/ai_v2_predecessor/contracts/04_EXPRESSION_MOMENT.md` (`SRC-AI2-EXPRESSION-001`) | `REQUIRED_UNIQUE_EVIDENCE` | 436 | `049fdb1711f3aa0cddc3d85e48491c9e0aa8f2b878e0f3fbb25dbc1b6a755802` | Exact source span, speaker, context, Reaction Receipt, qualities, lifecycle, approval, wrong-reading, and rejected/borderline preservation. |
| `.../sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` (`SRC-INT-002`) | `REQUIRED_UNIQUE_EVIDENCE` | 24,239 | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | Human activation remains source; assets are traceable to expression moments, archetypes, derivatives, routes, and evaluation. Historical fixed deliverable claims are not imported. |
| `.../sources/doctrine/AHP_PRD_V1_1_SOURCE_FIRST.md` (`SRC-SOURCE-FIRST-001`) | `SUPERSEDED` | 517,771 | `cc1cfa721238b999adb1612e805fad60c61c07c566df19d5044fc9e069651508` | Historical context only; no active claim depends on it. |
| `.../voice_audio_intimacy/PRM-VOC-009.yaml` | exact Primitive | 7,583 | `90405cef54e303ca87c2f274e6ac6a39b77cf261b86166a385e2ffb6420d5b80` | Preserve source-specific sensory premise; deny generic or overloaded anchors. |
| `.../visual_sonic_guidance/PRM-VSG-021.yaml` | exact Primitive | 8,179 | `06c75355f5f2bb083c09140e4af6994548e8d59fb544bf18553bc52966436cda` | Preserve source-backed friction/felt truth; deny manufactured messiness or distracting flaws. |
| `.../persuasion/PRM-PRS-002.yaml` | exact controlling CBAR Primitive | 6,893 | `4fba8edcb439c296a610b53a45ce76b9a002b4a128338e3302ddbb1cc49e242e` | Interpret source-backed tension/release without removing premise/tail or manufacturing a payoff. |

The spec references exact Primitive identity, bindings, applicability, conflicts, misuse, and suppression. It does not hard-code prose summaries as Primitive law or infer a coalition from name similarity.

### 1.5 Brownfield evidence

| Artifact | Bytes | SHA-256 | Disposition and reason |
|---|---:|---|---|
| `.../sources/ai_v2_predecessor/reference_implementation/models.py` | 24,677 | `f392c940349c3c5f9586a359fd8497ce1b8368de1b6654357deb146a686efd97` | `ADAPT`: strict models and an OAI pack seed are useful; flat confirmed strings, embedded delta, defaults, and absent claim/evaluator/dependency lifecycle are insufficient. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/expression_session_service.py` | 24,790 | `bde10d6cd18e37cb4c8bd347654a65cec4f47eaf91f8d96f93ef1bf09b6d745b` | `ARCHIVE_AS_PREDECESSOR_EVIDENCE`: explicit scoped session actions are useful but Studio is not OAI semantic owner and random/time/sequential persistence cannot be reused as canonical compilation. |

`04_ACTIVATIVE_INTELLIGENCE_RUNTIME` currently contains candidate specifications only; it has no product source or tests to extend. No current implementation behavior is inferred from the donor or historical Studio code.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem

Approved source evidence is not yet semantic understanding. IE can prove what was said, observed, approved, rejected, or left unresolved. AIR must compile what that evidence means for activation without converting plans into observations, inferences into facts, model confidence into approval, or downstream opportunity into permission.

A weak compiler can:

- copy a planned role, edge, pressure, or route into the observed pack because labels match;
- treat an approved Expression Moment as proof that the planned activation succeeded;
- omit rejected/borderline evidence and falsely present a clean success narrative;
- rewrite an IE Reaction Receipt or planned-observed delta to fit AIR's prior hypothesis;
- assign an “actual role” without exact evidence, epistemic state, alternatives, and evaluator;
- treat Primitive or archetype name similarity as an applied semantic program;
- remove the qualifying premise/reaction tail to make tension and release look complete;
- claim source-backed felt truth from a visually striking but non-semantic proposal;
- collapse `UNKNOWN`, `NOT_APPLICABLE`, `UNRESOLVED`, `REJECTED`, and `SUPERSEDED`;
- publish a mutable “latest” pack whose historical input bytes cannot be replayed; or
- grant a derivative producer authority to reinterpret the guest, source, or approved Moment.

These errors propagate semantic corruption into source packages, transfer contracts, campaigns, Final Scripts, Harnesses, and visual demands.

### 2.2 User and system outcome

An Activative Interview operator and downstream product can inspect one immutable OAI Pack and determine:

- the exact IE handoff, source package, approved moments, Reaction Receipts, tags, rejected/borderline evidence, and planned-observed deltas used;
- what the evidence supports as activated, partially activated, not activated, unexpected, contradicted, or unresolved;
- which actual roles, directions, pressures, urges, edges, stakes, and stances AIR compiled and at what epistemic/claim level;
- which Primitive and archetype implications were supported, conflicted, suppressed, or inapplicable;
- which limitations, wrong-reading risks, and source-authority restrictions bind every downstream use;
- which planned hypotheses survived, failed, or remain untestable;
- who/what proposed, evaluated, resolved, superseded, or invalidated each claim; and
- how to reproduce the exact pack from historical bytes without calling a current model or reading “latest.”

IE evidence remains unchanged and authoritative. AIR's pack is a separately owned semantic artifact that points back to it.

### 2.3 Bounded solution

After later authorization, implement an event-sourced `ObservedActivativeCompilationCase`. It admits one exact IE evidence handoff plus eligible exact Reaction Receipt/delta refs; resolves required AIR-owned planned/Primitive/archetype objects by immutable ref; freezes a compilation input manifest; builds a candidate portfolio of evidence-bounded semantic claims; applies deterministic authority, source, epistemic, claim-ceiling, Primitive, CBAR, lineage, and compatibility gates; obtains independent evaluation; records attributable human resolution when required; and atomically publishes or denies one immutable `ObservedActivativeIntelligencePack` with a compilation receipt and dependency graph.

### 2.4 In scope

- exact validation and consumption of IE-owned handoff, Expression Moment, tag, negative-evidence, Reaction Receipt, observation/delta, source-authority, and source-package refs;
- AIR-owned compilation of actual/failed/unexpected activation claims;
- evidence-bounded actual roles, directions, pressures, urges, edges, stakes, stances, reactions, limitations, and unresolved inference;
- exact Primitive Binding, Primitive Coalition evidence, Coalition Signature/Edge Product relationship, archetype evidence, and misuse/suppression handling where supported;
- planned-observed interpretation without changing planned or observed artifacts;
- candidate portfolios, independent evaluation, human resolution, immutable publication, supersession, selective invalidation, replay, idempotency, concurrency, and receipts;
- downstream read-only handoff with source-sovereignty/claim constraints;
- exact future implementation/test paths, subject to later ratification and capsule.

### 2.5 Out of scope and non-goals

- discovering, bounding, evaluating, approving, rejecting, or mutating Expression Moments/tags/Anchor Hits (`TS-INT-004`);
- observing/classifying reactions, issuing Reaction Receipts, or changing planned-observed evidence (`TS-INT-006`);
- source admission/transcript/visual indexes/live interview execution/source package mutation;
- compiling Planned Activative Intelligence, delivering calls, or altering the live state;
- approving source rights, creative safety, publication, production, derivative consumption, or model training;
- compiling an Activation Transfer Contract, Final Script, Campaign Program, category composition, Harness, Visual Asset Demand, or VAE Production Plan;
- selecting a model/provider or inventing evaluator thresholds/certification;
- direct Studio/UI mutation or producer self-acceptance;
- code, schemas, types, tests, migrations, releases, capsules, build, production, or certification in this prompt.

### 2.6 Claim ceiling

This writing result can be only `WRITTEN_PENDING_AUDIT`. `NOT_APPLICABLE` must always be evidence-bearing and policy-governed; it cannot be empty, null, or a shortcut around a required source or evaluation.

## 3. Governing decisions and constraints

### 3.1 Product sovereignty and ownership

| Object/decision | Authoritative owner | AIR action | Prohibited action |
|---|---|---|---|
| Source package, transcript/media/keyframe refs | Interview Expression/source authority | verify exact refs and cite | copy, correct, normalize, or infer missing source |
| Reaction Observations/Receipts and planned-observed evidence | Interview Expression; evaluator receipt by Independent Evaluation | consume exact eligible versions and respect maximum claim | create an AIR-local evidence fork or upgrade claim |
| Tag/Anchor/Expression Moment evidence, approval, negative evidence, handoff | Interview Expression | preserve refs/lifecycle/limitations | approve, relabel, suppress, or mutate |
| Planned AIP and AIR semantic hypotheses | AIR | resolve exact owned refs and compare through IE delta | represent planned claims as observed |
| Observed Activative Intelligence Pack and semantic claims | AIR | compile/version/evaluate/supersede | delegate semantic ownership to IE, Pipeline, Studio, VAE, Builder, or Delegation |
| Guest personal truth and operator source scope | guest/authorized source authority | preserve attribution and restrictions | infer identity fact or grant new rights |
| Independent semantic evaluation receipt | Independent Evaluation | request and apply exact verdict under lifecycle rules | producer self-approval or hidden score threshold |
| HumanResolutionEpisode | Studio captures; scoped promotion governed by AIR/Program Control | reference attributable resolution when semantic choice is human | universal automatic promotion or direct UI mutation |
| Derivative semantic/production authorization | owning later product/gate | expose constraints only | claim handoff, build, publication, or production approval |

### 3.2 Ownership conflict disposition

The F11 candidate PRD's `AIR-FR-065` owner line says Interview Expression, while the requirement says “The Runtime shall compile” and the Prompt 02 reconciliation assigns Observed Activative Intelligence to AIR. The frozen canonical FR/spec/ownership ledgers are the attributable correction for specification work: IE owns the evidence; AIR owns the semantic pack. The unresolved candidate ratification state remains explicit. No product implementation may rely on this correction until the required ratification/adoption and later build gate occur.

### 3.3 Evidence does not equal semantic conclusion

Every material OAI claim has:

- exact supporting and contradicting IE evidence refs;
- claim kind and governed value;
- owner product;
- epistemic state: `OBSERVED_DERIVATION`, `OPERATOR_CONFIRMED`, `HYPOTHESIZED`, `CONTESTED`, `RESOLVED`, `REJECTED`, `SUPERSEDED`, `UNKNOWN_WITH_EVIDENCE`, or `NOT_APPLICABLE_WITH_EVIDENCE`;
- evaluator and evaluation profile refs;
- maximum supported claim inherited from every dependency;
- alternatives and disconfirmation evidence;
- source authority/use scope;
- lineage and descendant edges.

`OBSERVED_DERIVATION` means AIR's semantic conclusion is derived from exact observed evidence; it does not transfer ownership of that evidence or turn interpretation into direct source fact. A claim cannot exceed the lowest applicable upstream maximum claim.

### 3.4 Planned and observed remain separate

The pack contains an immutable ref to any relevant planned AIR object plus exact IE planned-observed delta refs. It never copies a planned field into an observed field. Each planned dimension resolves to `SUPPORTED`, `PARTIALLY_SUPPORTED`, `DIVERGED`, `UNEXPECTED_OBSERVED`, `NOT_OBSERVED_WITH_SUFFICIENT_COVERAGE`, `INDETERMINATE_EVIDENCE_GAP`, or `NOT_APPLICABLE_WITH_EVIDENCE`. AIR may compile the semantic implication of that relation; it may not edit the relation or its evidence.

### 3.5 Negative and incomplete evidence is load-bearing

Rejected, borderline, contested, superseded, unavailable, and inapplicable evidence is not discarded. The pack records which candidate/claim it constrained and why. Absence of positive evidence is not evidence of failure unless the governing coverage profile supports `NOT_OBSERVED_WITH_SUFFICIENT_COVERAGE`. Missing evidence produces an indeterminate/blocking state, never a clean activation-null semantic conclusion.

### 3.6 Primitive, coalition, archetype, and CBAR law

- Primitive evidence resolves exact registry version/hash and an AIR-owned Primitive Binding; fuzzy names/prose are invalid.
- A Primitive `core_move` is not sufficient evidence of activation. Applicability, activation, conflict, misuse, and suppression conditions are evaluated against exact source evidence.
- A Primitive Coalition Contract, Coalition Signature, Edge Product, or archetype coalition is referenced or compiled under its own accepted AIR contracts. This spec does not invent their schemas or bypass their lifecycle.
- `PRM-PRS-002` is controlling for `AIR-ST-11.03`: the pack must preserve the actual tension/release evidence and must not create a satisfying release by removing the premise, qualifier, unresolved tension, or reaction tail.
- `PRM-VOC-009` prevents genericized sensory “truth” when the source supports a specific scene and prevents sensory overload.
- `PRM-VSG-021` protects genuine source-backed friction but forbids manufactured messiness, distracting flaws, and beauty/polish bias.
- If a Primitive/archetype input is absent or inapplicable, the pack says so with evidence; it never fills the slot from similarity or a default coalition.

### 3.7 Source fidelity, wrong-reading, and derivative sovereignty

The OAI Pack carries exact source/moment refs, source-authority scope, limitations, wrong-reading risks/updates, quote/context dependencies, and prohibited reinterpretations. A downstream product may use the pack only within those constraints and its own adopted contract. It cannot rewrite the guest, turn an AIR hypothesis into a quote, remove a Reaction Receipt limitation, or treat the pack as derivative production acceptance.

### 3.8 Candidate portfolios and independent evaluation

The compiler produces a portfolio, not an unexplained winner. Candidate semantic readings include evidence, alternatives, conflict, unknowns, negative evidence, expected downstream effects, and stopping evidence. Deterministic gates precede learned judgment. The final evaluator must be independent of compiler/proposer identity. A human resolution is additive, attributable, scoped, and cannot erase candidate/evaluator evidence.

### 3.9 Determinism, portability, and atomicity

Canonical identity excludes current time, random state, environment, process ID, hostname, locale, timezone, filesystem traversal, insertion order, provider callback order, absolute paths, and unresolved checkout roots. All accepted state, command, candidate portfolio, evaluation, pack, receipt, dependency edges, idempotency result, invalidation, and outbox intent commit atomically. A model proposal can be nondeterministic only as a stored proposal artifact; deterministic admission and exact proposal bytes govern the canonical result.

### 3.10 Explicitly forbidden behavior

- AIR writing or redefining IE artifacts;
- a parser that drops lifecycle, epistemic state, evidence, authority, maximum claim, negative evidence, limitations, or wrong-reading constraints;
- producer/evaluator identity collapse;
- “latest” reads in compilation or replay;
- automatic semantic acceptance because a source moment is approved;
- model confidence, score, or label match used as authority;
- local schema forks of IE evidence;
- mutation or deletion during correction/supersession;
- guessed imported-source planning history;
- generic creative-safety/content-rights approval authority;
- build, production, Format 02, VAE Stage 5, or certification claim from this spec.

### 3.11 Draft-dependency covenant

TS-INT-004 controls the exact evidence handoff and Moment/tag/negative-evidence constraints. TS-INT-006 controls Reaction Receipt/delta/maximum-claim/evaluator semantics. If either hash changes, this specification is not silently rebased. Sections 3, 5, 6, 8, 9, and 10 reopen, all dependent fixtures/hashes are refreshed, and independent audit determines whether the AIR interface remains compatible.

## 4. Current brownfield architecture

### 4.1 Current AIR repository state

The intended AIR root contains candidate specifications and no source/test implementation. There is no current compiler, repository, schema, API, evaluator, worker, or release to reuse. Proposed paths in section 7 are future-only.

### 4.2 Full donor split

The donor `TS-AIR-011` combines Expression Moment discovery/lifecycle and Observed AIP compilation. Its immutable objects, field-level epistemic state, deterministic gates, independent evaluation, HumanResolution, replay, and selective invalidation are `ADAPT`. Its ownership of `ExpressionMomentCandidate`, `ExpressionMoment`, and their decisions is `REPLACE_BY_TS_INT_004`; its Observed AIP compilation is retained here. Donor mappings that place FR-064/065 outputs incorrectly are superseded by Prompt 02 traceability.

### 4.3 AI2 model seed

The predecessor `ObservedActivativeIntelligencePack` includes planned/source refs, reaction/moment refs, confirmed roles/stances/stakes, unresolved inferences, identity candidate observations, a delta, transfer requirements, campaign opportunities, and wrong-reading updates. This is `ADAPT`, not direct reuse. It lacks exact per-claim evidence/epistemic/evaluator/authority, negative evidence, candidate portfolio, Primitive/archetype evidence status, immutable dependency lifecycle, idempotency, atomic receipts, invalidation, and portable canonical identity. Flat strings and default empty tuples cannot represent governed unknown/inapplicability.

### 4.4 Studio predecessor

Studio's expression-session service is `ARCHIVE_AS_PREDECESSOR_EVIDENCE` for this AIR compiler. It demonstrates scoped commands and status receipts but combines projection/orchestration concerns, generates random/time identity, and writes state/events/receipts sequentially. Studio remains a projection/correction surface and cannot host authoritative OAI semantic state.

### 4.5 Migration boundary

No donor, AI2 model, Studio record, or historical source-first object becomes current OAI state by copying fields. Migration creates a new AIR-owned immutable artifact only when every semantic claim, source/evidence ref, authority, evaluator, epistemic state, maximum claim, lifecycle, and dependency can be mapped losslessly. Otherwise it preserves a typed historical/unresolved artifact or blocks.

## 5. Proposed architecture and workflows

### 5.1 Components

| Component | Responsibility | Must not do |
|---|---|---|
| `ObservedCompilationApplicationService` | normalize/authenticate/authorize commands, enforce idempotency/concurrency, orchestrate one case | infer evidence or partially persist |
| `InterviewEvidenceAdmissionPort` | resolve exact IE refs/hashes/lifecycle/claim/source scope and produce a frozen view | use latest, mutate IE, or accept parse-only compatibility |
| `ObservedInputManifestCompiler` | freeze exact handoff, receipts, deltas, moments, tags, negative evidence, planned refs, profiles, bindings, authority | omit adverse evidence or copy mutable payloads |
| `ActivativeClaimPortfolioCompilerPort` | propose evidence-bounded semantic claim candidates and alternatives | self-evaluate, approve, or emit authoritative IE evidence |
| `DeterministicObservedClaimValidator` | enforce ownership, evidence, epistemic, maximum-claim, source-authority, lineage, and schema invariants | invent semantics to repair a candidate |
| `PrimitiveArchetypeEvidenceResolver` | resolve exact bindings/contracts and test activation/conflict/misuse/suppression evidence | infer a Primitive/archetype from names or vibes |
| `PlannedObservedSemanticInterpreter` | compile semantic implications of exact IE deltas while preserving both owners | rewrite planned or observed inputs |
| `IndependentObservedPackEvaluatorPort` | issue independent evidence-sufficiency, claim-fit, alternative, CBAR, and boundary verdict | share producer identity or become source authority |
| `ObservedCompilationLifecycleService` | apply evaluator/human resolution and publish/supersede/invalidate packs | accept hidden UI edits or erase history |
| `ObservedCompilationRepositoryPort` | atomically compare-and-append command, artifacts, state, receipts, dependencies, idempotency, invalidation, outbox | expose state without receipts or exact historical inputs |
| `ObservedDependencyProjector` | compute typed direct/transitive descendants and unaffected proof | globally invalidate unrelated artifacts |
| `ObservedPackQueryPort` | return exact/current eligible or historical labeled views | return noneligible evidence as current |
| `StudioObservedProjectionPort` | present reconstructable views and accept typed HumanResolution commands | own canonical state |

Domain compilation and canonicalization are pure: no clock, randomness, filesystem, network, provider SDK, Studio, Pipeline, VAE, Builder, or Delegation import. External proposals/evaluations are stored as exact input artifacts before deterministic admission.

### 5.2 Open and freeze compilation case

`OpenObservedActivativeCompilation` requires:

- organization/brand/source authority scope;
- exact TS-INT-004 `ObservedActivativeEvidenceHandoff` ref/hash;
- exact eligible TS-INT-006 Reaction Receipt and planned-observed delta refs/hashes, either directly named by the handoff or explicitly reconciled;
- exact IE handoff receipt and current lifecycle/consumption state;
- AIR planned-object refs when available and required by the delta;
- exact Primitive registry, Primitive Binding/Coalition, archetype evidence, epistemic-policy, evaluation-profile, compatibility-profile, and compiler-binding refs;
- actor/authority assertion, command/idempotency identity, expected nonexistence or case version/hash, and logical time.

Admission performs these steps:

1. Verify tenant/source scope before returning content.
2. Resolve each ref by exact owner/version/hash; never substitute latest.
3. Require the IE handoff lifecycle to be current/eligible and confirm `source_evidence_owner: INTERVIEW_EXPRESSION`, `semantic_compilation_owner: ACTIVATIVE_INTELLIGENCE_RUNTIME`, and `downstream_reinterpretation_authorized: false`.
4. Resolve every approved Moment, current eligible tag, Reaction Receipt/delta, limitation, wrong-reading risk, negative/borderline evidence ref, and their decision/evaluation/authority refs.
5. Verify that rejected, borderline, contested, invalidated, superseded, and missing evidence named by the handoff has not been filtered from the compilation view.
6. Verify current source-authority scope permits semantic compilation while preserving restrictions on publication, derivative use, training, identity/voice, and retention.
7. Negotiate required semantic features; a consumer that only parses fields fails.
8. Create immutable `ObservedCompilationInputManifest` and `ObservedCompilationCaseOpened`.
9. Atomically commit command, case, manifest, event, receipt, dependency edges, idempotency, and outbox.

An approved Moment or validated Reaction Receipt is necessary evidence where required but never alone sufficient for an OAI claim. If a handoff contains no approved moments or eligible receipts, the case may record a truthful `NO_COMPILABLE_OBSERVED_SEMANTICS` result when the profile permits; it cannot invent them.

### 5.3 Build semantic candidate portfolio

`ProposeObservedActivativeClaimPortfolio` takes the frozen manifest, not mutable IE services. It generates zero or more candidate claims for governed dimensions:

- activation result (`ACTIVATED`, `PARTIALLY_ACTIVATED`, `NOT_ACTIVATED_WITH_SUFFICIENT_EVIDENCE`, `UNEXPECTED_ACTIVATION`, `INDETERMINATE`);
- actual psychological role inside a tension;
- activation direction;
- pressure and human response to pressure;
- urge and stance;
- edge and unexpected edge;
- source-backed stake;
- reaction/counteractivation significance;
- Primitive evidence status and coalition implication;
- archetype evidence status and role potential;
- Identity DNA candidate observation (never canonical Identity DNA mutation);
- transfer requirement/opportunity;
- campaign opportunity;
- wrong-reading update;
- limitation or unresolved inference.

Each candidate contains exact support and contradiction refs, alternative candidate refs, disconfirmation rule, claim/evidence owner, epistemic state, confidence only through a governed score, maximum claim, source scope, compiler binding, and stopping evidence. The compiler does not collapse mutually plausible readings. A zero-candidate portfolio is lawful when it records evidence insufficiency/stopping conditions.

The raw portfolio is `PROPOSED_NONAUTHORITATIVE`. A model cannot mark an OAI claim confirmed, resolved, or eligible.

### 5.4 Deterministic claim validation

`ValidateObservedActivativeClaimPortfolio` rejects or bounds each candidate by:

- exact source/moment/receipt/tag/delta lifecycle eligibility;
- evidence span and source continuity;
- IE maximum claim and downstream constraints;
- observation versus interpretation and planned versus observed separation;
- source-authority and sensitivity scope;
- closed dimension/value/epistemic vocabularies;
- requirement that a claim has nonempty direct support unless typed unknown/N/A;
- preservation of contradicting/rejected/borderline evidence;
- evaluator/compiler independence requirements;
- exact Primitive/archetype registry and binding identity;
- wrong-reading inheritance/strengthening and no lock weakening;
- no downstream production/certification/route authorization;
- canonical/reference portability and dependency graph completeness.

The validator emits per-claim `ADMISSIBLE_FOR_EVALUATION`, `BOUNDED_FOR_EVALUATION`, or `REJECTED` with reasons. `BOUNDED` creates a new candidate version referencing the original; it does not edit proposal bytes.

### 5.5 Compile Primitive and archetype evidence

For every claimed Primitive or archetype implication:

1. Resolve exact Primitive/coalition/archetype contract refs and hashes under AIR authority.
2. Check declared applicability against exact IE evidence, source authority, and profile.
3. Record activation, conflict, misuse risk, suppression, or evidence-bearing not-applicable result.
4. Require candidate coalition/signature/Edge Product semantics to use accepted AIR-owned interfaces; if unavailable, keep the result as evidence and block that higher semantic claim.
5. Preserve the source evidence refs; do not embed a rewritten Expression Moment or Reaction Receipt.
6. For `PRM-PRS-002`, prove that tension and release both exist where claimed and that premise, qualification, and reaction tail remain intact. A tension with no source-backed release remains unresolved/limited.

The Primitive resolver can deny a misuse; it cannot repair source evidence or choose a derivative composition.

### 5.6 Interpret planned-observed delta

`CompilePlannedObservedSemanticDelta` consumes each IE-owned dimension relation by exact ref. AIR creates a separate semantic interpretation record containing:

- exact planned AIR assertion ref and owner;
- exact IE delta and observed evidence refs/owners;
- relation copied only as a ref plus verified value;
- semantic implication candidates;
- what the relation does not prove;
- unresolved alternatives and required evidence;
- affected actual-role/edge/pressure/urge/route-hypothesis claims;
- evaluator and maximum-claim requirements.

If the planned object has been superseded after the evidence was recorded, the historical relation remains reproducible but current compilation requires an explicit compatibility/reconciliation decision. AIR cannot recalculate the IE relation invisibly.

### 5.7 Independent evaluation and human resolution

`EvaluateObservedActivativePackCandidate` receives the immutable manifest, portfolio, validated claims, Primitive/archetype evidence, delta interpretations, and candidate pack. The evaluator identity must differ from the compiler/proposer and any model/agent that created material claims. It assesses:

- exact input completeness and eligibility;
- source-evidence/semantic-owner separation;
- claim fit and evidence sufficiency per dimension;
- planned/observed separation;
- negative/contradictory/unknown evidence retention;
- Primitive/archetype applicability, misuse, suppression, and CBAR;
- source context, premise, reaction tail, and quote/summary fidelity;
- wrong-reading and downstream constraint completeness;
- alternative interpretations and disconfirmation;
- maximum supported pack/claim level;
- descendant dependency completeness.

Verdicts are `VALIDATED`, `REJECTED`, `CONTESTED`, or `NEEDS_MORE_EVIDENCE`. No ungoverned score decides. `ApplyObservedPackEvaluation` can publish only a validated candidate whose deterministic gates pass and whose evaluator maximum claim is not exceeded.

Where the profile requires a human semantic choice or evaluator disagreement remains resolvable, `ResolveObservedPackContest` consumes an attributable Studio-captured `HumanResolutionEpisode`. The command declares scope, alternatives considered, decision, rationale, authority, and whether the resolution is local or a scoped learning candidate. It does not erase evaluator disagreement or automatically promote learning globally.

### 5.8 Publish immutable OAI Pack

`PublishObservedActivativeIntelligencePack` requires:

- exact case/input manifest/portfolio/validated claim/evaluation refs;
- candidate state `VALIDATED` and no unresolved blocking failure;
- source authority still permitting the requested compilation/use scope;
- expected case version/hash and idempotency key;
- all direct/transitive dependency edges and downstream constraints.

It atomically commits the immutable pack, `ObservedPackCompilationReceipt`, case transition, event, current alias, dependency graph, idempotency result, and outbox intent. Publication here means AIR semantic artifact publication to its governed repository. It is not source publication, derivative authorization, downstream consumption acknowledgement, production acceptance, or certification.

The pack lifecycle is `CANDIDATE -> EVALUATION_REQUIRED -> VALIDATED -> PUBLISHED`; exact versions may later become `SUPERSEDED`, `INVALIDATED`, or `REVOKED`. `REJECTED`, `CONTESTED`, and `NEEDS_MORE_EVIDENCE` are non-published terminal/waiting states for that candidate version.

### 5.9 Downstream consumption workflow

A downstream consumer requests an exact pack ref plus compatibility profile and required features. AIR returns a read-only `ObservedPackConsumptionView` with:

- pack and compilation/evaluation refs/hashes;
- exact IE source/evidence refs and owner flags;
- each semantic claim with epistemic/maximum claim;
- limitations, wrong-reading constraints, source-authority use scope, and prohibited reinterpretations;
- lifecycle/supersession/invalidation state;
- required next owner/gate.

The consumer issues a distinct acknowledgement. Acknowledgement means bytes/constraints were received and accepted for that declared operation; it is not AIR publication, IE source approval, derivative production acceptance, or permission to reinterpret. Stale, invalidated, revoked, or feature-incompatible packs cannot be consumed for new work.

### 5.10 Supersession, invalidation, replay, and cancellation

- A corrected IE Moment/tag/Reaction Receipt/delta/handoff invalidates only OAI claims/packs that cite the changed ref or field, then propagates to typed descendants.
- A Primitive/binding/archetype correction invalidates only claims using that semantic dependency.
- A changed planned AIR assertion reopens affected delta interpretations, not IE observations.
- An evaluator/profile revocation affects evaluation/eligibility, not historical source evidence.
- A source-authority restriction/revocation blocks prohibited current/new use while keeping lawful historical audit evidence.
- Supersession creates a new pack and link; no bytes are edited.
- `ReplayObservedCompilationCase` resolves exact historical bytes, proposal/evaluation artifacts, rulesets, and invalidation view; it never calls current models or reads latest.
- Cancellation checks precede expensive compiler/evaluator work and commit. Late results after cancellation are quarantined; if commit wins, cancellation is a successor event.

### 5.11 Command-processing invariant

Every mutating command follows: strict parse -> tenant/security scope -> canonical normalization/fingerprint -> idempotency lookup -> exact aggregate load -> optimistic sequence/hash check -> immutable dependency resolution -> authority/compatibility check -> pure domain derivation -> atomic compare-and-append -> committed outcome return. No automatic retry may rebase semantic intent. Operational transport retry uses the same idempotency key and returns the prior result.

## 6. Data models, contracts, schemas, and APIs

These are normative logical contracts for a future implementation. This prompt creates no schema or release bytes. Every object rejects unknown fields, open dictionaries, untyped `Any`, bare floats, implied defaults, random/time identity, and nonportable refs.

### 6.1 Common values

```text
ImmutableRef {
  object_type: governed nonempty identifier
  object_id: nonempty identifier
  version: positive integer or governed semantic version
  sha256: lowercase 64-hex digest
  owner_product: governed product identifier
  lifecycle_state_at_use: governed enum
}

EvidenceBearingNotApplicable {
  reason_code: governed identifier
  policy_ref: ImmutableRef
  decision_actor_or_method_ref: ImmutableRef
  inspected_evidence_refs: canonical ordered ImmutableRef[]
  effect_on_claim: NONE | LIMITS_CLAIM | BLOCKS_CLAIM | BLOCKS_PACK
}

GovernedScore {
  value: canonical decimal string
  scale_id: governed identifier
  calibration_profile_ref: ImmutableRef
  interpretation: governed band
}
```

An `ImmutableRef` never uses an absolute path as identity. A portable repository-relative content locator may accompany it but is excluded when the content hash/ref is sufficient.

### 6.2 Input manifest

`ObservedCompilationInputManifest` - `ca.air.observed-compilation-input/2.1.0-candidate`:

```text
manifest_id: deterministic identifier
version: positive integer
tenant_and_brand_scope: exact governed scope
source_authority_ref: ImmutableRef
observed_evidence_handoff_ref: ImmutableRef
handoff_receipt_ref: ImmutableRef
source_package_ref: ImmutableRef
approved_expression_moment_refs: nonempty canonical ordered ImmutableRef[] | EvidenceBearingNotApplicable
reaction_receipt_refs: canonical ordered ImmutableRef[]
planned_observed_delta_refs: canonical ordered ImmutableRef[]
tag_assertion_refs: canonical ordered ImmutableRef[]
rejected_or_borderline_evidence_refs: canonical ordered ImmutableRef[]
planned_air_object_refs: canonical ordered ImmutableRef[]
primitive_registry_ref: ImmutableRef
primitive_binding_refs: canonical ordered ImmutableRef[]
primitive_coalition_contract_refs: canonical ordered ImmutableRef[]
archetype_evidence_registry_ref: ImmutableRef
compiler_binding_ref: ImmutableRef
evaluation_profile_ref: ImmutableRef
compatibility_profile_id: governed identifier
required_feature_ids: canonical sorted set
source_limitations: canonical governed set
wrong_reading_risks: nonempty canonical governed set
upstream_maximum_supported_claim: governed claim enum
frozen_dependency_edges: canonical ordered DependencyEdge[]
manifest_sha256: sha256
```

The manifest references exact IE artifacts rather than embedding mutable copies. A missing evidence class is a typed N/A/absence artifact only where the profile permits it; otherwise admission blocks.

### 6.3 Evidence-bounded semantic claim

```text
ObservedActivativeClaim {
  claim_id: deterministic identifier
  version: positive integer
  dimension: ACTIVATION_RESULT | ACTUAL_ROLE_IN_TENSION | DIRECTION | PRESSURE | URGE | EDGE |
             STAKE | STANCE | REACTION_SIGNIFICANCE | COUNTERACTIVATION_SIGNIFICANCE |
             PRIMITIVE_IMPLICATION | ARCHETYPE_IMPLICATION | IDENTITY_DNA_CANDIDATE_OBSERVATION |
             TRANSFER_REQUIREMENT | CAMPAIGN_OPPORTUNITY | WRONG_READING_UPDATE |
             LIMITATION | UNRESOLVED_INFERENCE
  value: closed typed union owned by dimension
  source_evidence_owner: INTERVIEW_EXPRESSION | AUTHORIZED_HUMAN_SOURCE
  semantic_claim_owner: ACTIVATIVE_INTELLIGENCE_RUNTIME
  supporting_evidence_refs: nonempty canonical ordered ImmutableRef[]
  contradicting_evidence_refs: canonical ordered ImmutableRef[]
  rejected_or_borderline_evidence_refs: canonical ordered ImmutableRef[]
  planned_assertion_refs: canonical ordered ImmutableRef[]
  planned_observed_delta_refs: canonical ordered ImmutableRef[]
  epistemic_state: OBSERVED_DERIVATION | OPERATOR_CONFIRMED | HYPOTHESIZED | CONTESTED |
                   RESOLVED | REJECTED | SUPERSEDED | UNKNOWN_WITH_EVIDENCE |
                   NOT_APPLICABLE_WITH_EVIDENCE
  confidence: GovernedScore | EvidenceBearingNotApplicable
  alternative_claim_refs: canonical ordered ImmutableRef[]
  disconfirmation_rule: governed typed rule
  maximum_supported_claim: governed claim enum
  source_authority_scope_ref: ImmutableRef
  evaluator_receipt_ref: ImmutableRef | EvidenceBearingNotApplicable
  lifecycle_state: PROPOSED | ADMISSIBLE | BOUNDED | VALIDATED | REJECTED | CONTESTED |
                   SUPERSEDED | INVALIDATED
  supersedes_ref: ImmutableRef | EvidenceBearingNotApplicable
  dependency_edges: nonempty canonical ordered DependencyEdge[]
  content_sha256: sha256
}
```

An actual-role claim is a semantic observed derivation, not a directly observed string. It must cite source evidence and state the tension/role ontology version. An Identity DNA candidate observation never mutates canonical Guest Identity DNA; promotion requires its separate human/source-authority lifecycle.

### 6.4 Primitive and archetype evidence

```text
PrimitiveEvidenceResult {
  primitive_ref: ImmutableRef
  primitive_binding_ref: ImmutableRef
  status: ACTIVATED_WITH_EVIDENCE | PARTIALLY_ACTIVATED | CONFLICTED | MISUSE_RISK |
          SUPPRESSED | INDETERMINATE | NOT_APPLICABLE_WITH_EVIDENCE
  activation_evidence_refs: canonical ordered ImmutableRef[]
  conflict_or_misuse_evidence_refs: canonical ordered ImmutableRef[]
  suppression_evidence_refs: canonical ordered ImmutableRef[]
  coalition_contract_ref: ImmutableRef | EvidenceBearingNotApplicable
  coalition_signature_ref: ImmutableRef | EvidenceBearingNotApplicable
  edge_product_ref: ImmutableRef | EvidenceBearingNotApplicable
  maximum_supported_claim: governed claim enum
  evaluator_ref: ImmutableRef
}

ArchetypeEvidenceResult {
  archetype_ref: ImmutableRef
  psychological_role_inside_tension_ref: ImmutableRef | EvidenceBearingNotApplicable
  status: SUPPORTED | PARTIALLY_SUPPORTED | CONFLICTED | INDETERMINATE |
          NOT_APPLICABLE_WITH_EVIDENCE
  evidence_refs: canonical ordered ImmutableRef[]
  contradicting_refs: canonical ordered ImmutableRef[]
  source_expression_moment_refs: canonical ordered ImmutableRef[]
  derivative_route_authorized: false
  maximum_supported_claim: governed claim enum
}
```

`derivative_route_authorized` is always false here. Evidence of role potential is not an approved archetype coalition, Final Script, or derivative route.

### 6.5 Planned-observed semantic interpretation

```text
PlannedObservedSemanticInterpretation {
  interpretation_id: deterministic identifier
  ie_delta_ref: ImmutableRef
  planned_air_assertion_refs: canonical ordered ImmutableRef[]
  observed_ie_evidence_refs: canonical ordered ImmutableRef[]
  verified_relation: SUPPORTED_BY_OBSERVATION | PARTIALLY_SUPPORTED | DIVERGED |
                     UNEXPECTED_OBSERVED | NOT_OBSERVED_WITH_SUFFICIENT_COVERAGE |
                     INDETERMINATE_EVIDENCE_GAP | NOT_APPLICABLE_WITH_EVIDENCE
  semantic_implication_claim_refs: canonical ordered ImmutableRef[]
  non_implications: nonempty canonical governed set
  unresolved_alternative_refs: canonical ordered ImmutableRef[]
  maximum_supported_claim: governed claim enum
  interpretation_owner: ACTIVATIVE_INTELLIGENCE_RUNTIME
  evidence_relation_owner: INTERVIEW_EXPRESSION
  content_sha256: sha256
}
```

This object cannot edit the IE delta or planned AIR object. A verified relation is copied only for conformance and remains tied to the exact IE ref/hash.

### 6.6 Candidate portfolio

```text
ObservedActivativeClaimPortfolio {
  portfolio_id: deterministic identifier
  input_manifest_ref: ImmutableRef
  compiler_binding_ref: ImmutableRef
  compiler_actor_or_program_ref: ImmutableRef
  candidate_claim_refs: canonical ordered ImmutableRef[]
  rejected_candidate_refs: canonical ordered ImmutableRef[]
  alternative_set_refs: canonical ordered ImmutableRef[]
  stopping_evidence_ref: ImmutableRef
  unknown_or_missing_dimension_results: canonical map[dimension, typed result]
  portfolio_state: PROPOSED_NONAUTHORITATIVE | DETERMINISTICALLY_ADMITTED |
                   REJECTED | SUPERSEDED | INVALIDATED
  content_sha256: sha256
}
```

A portfolio must cover every dimension required by the profile with a candidate, explicit unknown/N/A result, or blocker. Empty omission is invalid.

### 6.7 Observed Activative Intelligence Pack

`ObservedActivativeIntelligencePack` - `ca.air.observed-activative-intelligence-pack/2.1.0-candidate`:

```text
pack_id: deterministic identifier
version: positive integer
owner_product: ACTIVATIVE_INTELLIGENCE_RUNTIME
input_manifest_ref: ImmutableRef
source_evidence_handoff_ref: ImmutableRef
source_package_ref: ImmutableRef
planned_activative_intelligence_refs: canonical ordered ImmutableRef[]
approved_expression_moment_refs: canonical ordered ImmutableRef[]
reaction_receipt_refs: canonical ordered ImmutableRef[]
tag_assertion_refs: canonical ordered ImmutableRef[]
rejected_or_borderline_evidence_refs: canonical ordered ImmutableRef[]
activation_result_claim_refs: nonempty canonical ordered ImmutableRef[]
actual_role_claim_refs: canonical ordered ImmutableRef[]
direction_claim_refs: canonical ordered ImmutableRef[]
pressure_claim_refs: canonical ordered ImmutableRef[]
urge_claim_refs: canonical ordered ImmutableRef[]
edge_claim_refs: canonical ordered ImmutableRef[]
stake_and_stance_claim_refs: canonical ordered ImmutableRef[]
reaction_and_counteractivation_claim_refs: canonical ordered ImmutableRef[]
primitive_evidence_result_refs: canonical ordered ImmutableRef[]
archetype_evidence_result_refs: canonical ordered ImmutableRef[]
planned_observed_semantic_interpretation_refs: canonical ordered ImmutableRef[]
identity_dna_candidate_observation_refs: canonical ordered ImmutableRef[]
transfer_requirement_claim_refs: canonical ordered ImmutableRef[]
campaign_opportunity_claim_refs: canonical ordered ImmutableRef[]
unresolved_inference_refs: canonical ordered ImmutableRef[]
limitation_claim_refs: canonical ordered ImmutableRef[]
wrong_reading_update_refs: nonempty canonical ordered ImmutableRef[]
source_authority_scope_ref: ImmutableRef
evaluation_receipt_ref: ImmutableRef
human_resolution_refs: canonical ordered ImmutableRef[]
maximum_supported_claim: governed claim enum
downstream_constraints: nonempty canonical governed set
semantic_compilation_owner: ACTIVATIVE_INTELLIGENCE_RUNTIME
source_evidence_owner: INTERVIEW_EXPRESSION
downstream_reinterpretation_authorized: false
lifecycle_state: CANDIDATE | EVALUATION_REQUIRED | VALIDATED | PUBLISHED |
                 REJECTED | CONTESTED | NEEDS_MORE_EVIDENCE | SUPERSEDED |
                 INVALIDATED | REVOKED
supersedes_ref: ImmutableRef | EvidenceBearingNotApplicable
replacement_ref: ImmutableRef | EvidenceBearingNotApplicable
dependency_edges: nonempty canonical ordered DependencyEdge[]
content_sha256: sha256
```

The pack contains references to source evidence and semantic claim objects, not generic notes. Empty claim collections are legal only when profile coverage provides evidence-bearing absence and the activation-result/limitation claims explain it. `PUBLISHED` requires `VALIDATED`, exact evaluation, and no blocking source/authority/invalidation state.

### 6.8 Independent evaluation

```text
ObservedPackEvaluationReceipt {
  evaluation_receipt_id: deterministic identifier
  candidate_pack_ref: ImmutableRef
  input_manifest_ref: ImmutableRef
  portfolio_ref: ImmutableRef
  compiler_actor_or_program_ref: ImmutableRef
  evaluator_actor_or_program_ref: ImmutableRef
  independence_check: PASS | FAIL
  profile_ref: ImmutableRef
  input_completeness: PASS | FAIL | INDETERMINATE
  ownership_boundary: PASS | FAIL
  claim_fit_results: canonical map[claim_ref, PASS | CONCERNS | FAIL | INDETERMINATE]
  negative_evidence_retention: PASS | FAIL
  planned_observed_separation: PASS | FAIL
  primitive_archetype_cbar_results: canonical ordered CheckResult[]
  source_context_and_tail_preservation: PASS | FAIL | INDETERMINATE
  source_authority_check: PASS | FAIL
  wrong_reading_constraint_check: PASS | FAIL
  alternative_interpretation_refs: canonical ordered ImmutableRef[]
  maximum_supported_claim: governed claim enum
  verdict: VALIDATED | REJECTED | CONTESTED | NEEDS_MORE_EVIDENCE
  failure_refs: canonical ordered ImmutableRef[]
  content_sha256: sha256
}
```

Independent Evaluation owns the verdict artifact. AIR owns the pack lifecycle applying it. Evaluator capability presence does not imply certification.

### 6.9 Compilation receipt

```text
ObservedPackCompilationReceipt {
  receipt_id: deterministic identifier
  command_ref: ImmutableRef
  case_ref: ImmutableRef
  input_manifest_ref: ImmutableRef
  portfolio_ref: ImmutableRef
  admitted_claim_refs: canonical ordered ImmutableRef[]
  rejected_claim_refs: canonical ordered ImmutableRef[]
  evaluation_receipt_ref: ImmutableRef
  human_resolution_refs: canonical ordered ImmutableRef[]
  resulting_pack_ref: ImmutableRef | EvidenceBearingNotApplicable
  outcome: PUBLISHED | NO_COMPILABLE_OBSERVED_SEMANTICS | REJECTED |
           CONTESTED | NEEDS_MORE_EVIDENCE | DENIED | CONFLICT | CANCELLED | FAILED
  maximum_supported_claim: governed claim enum
  applied_constraint_refs: nonempty canonical ordered ImmutableRef[]
  atomic_commit_id: deterministic identifier | EvidenceBearingNotApplicable
  failure_ref: ImmutableRef | EvidenceBearingNotApplicable
  content_sha256: sha256
}
```

The receipt cannot exist as success without every referenced artifact. A `NO_COMPILABLE_OBSERVED_SEMANTICS` outcome is truthful evidence, not a fabricated empty success pack unless the profile explicitly defines such a published object.

### 6.10 Aggregate, commands, events, and repository

```text
ObservedActivativeCompilationCase {
  case_id: deterministic identifier
  version: positive integer
  tenant_and_brand_scope: exact governed scope
  current_input_manifest_ref: ImmutableRef
  current_portfolio_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_candidate_pack_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_published_pack_ref: ImmutableRef | EvidenceBearingNotApplicable
  state: OPEN | INPUTS_FROZEN | PORTFOLIO_PROPOSED | CLAIMS_ADMITTED |
         EVALUATION_REQUIRED | VALIDATED | PUBLISHED | REJECTED | CONTESTED |
         NEEDS_MORE_EVIDENCE | CANCELLED | FAILED | SUPERSEDED | INVALIDATED
  supersedes_ref: ImmutableRef | EvidenceBearingNotApplicable
  case_sha256: sha256
}
```

Normative commands:

- `OpenObservedActivativeCompilation`;
- `ProposeObservedActivativeClaimPortfolio`;
- `ValidateObservedActivativeClaimPortfolio`;
- `CompilePrimitiveArchetypeEvidence`;
- `CompilePlannedObservedSemanticDelta`;
- `AssembleObservedActivativeIntelligencePackCandidate`;
- `EvaluateObservedActivativePackCandidate`;
- `ApplyObservedPackEvaluation`;
- `ResolveObservedPackContest`;
- `PublishObservedActivativeIntelligencePack`;
- `SupersedeObservedActivativeIntelligencePack`;
- `InvalidateObservedActivativeDescendants`;
- `RevokeObservedActivativeIntelligencePack`;
- `CancelObservedActivativeCompilation`;
- `ReplayObservedCompilationCase` (read-only query command).

Each mutating command has schema/command ID, idempotency key, tenant/brand/source scope, actor assertion, authority decision ref, expected case/object version/hash, logical time, canonical payload, and cancellation token where applicable. Generic patch commands are forbidden.

Events mirror successful transitions: `ObservedCompilationCaseOpened`, `ObservedInputsFrozen`, `ObservedClaimPortfolioProposed`, `ObservedClaimsValidated`, `PrimitiveArchetypeEvidenceCompiled`, `PlannedObservedSemanticsCompiled`, `ObservedPackCandidateAssembled`, `ObservedPackEvaluated`, `ObservedPackEvaluationApplied`, `ObservedPackContestResolved`, `ObservedPackPublished`, `ObservedPackSuperseded`, `ObservedDescendantsInvalidated`, `ObservedPackRevoked`, and `ObservedCompilationCancelled`.

Repository interface:

```text
load_exact(ref: ImmutableRef) -> ImmutableArtifact
load_case(case_id, version, sha256) -> ObservedActivativeCompilationCase
lookup_idempotency(case_id, command_kind, key) -> IdempotencyRecord | NOT_FOUND
commit(bundle: ObservedCompilationCommitBundle, expected_case_ref) -> CommandOutcome
list_claims(pack_ref, dimension, lifecycle, cursor) -> page[ObservedActivativeClaim]
list_descendants(root_refs, edge_types, cursor) -> page[DependencyEdge]
get_consumption_view(pack_ref, compatibility_profile_id, required_features) -> ObservedPackConsumptionView
replay(case_ref, through_version, invalidation_view) -> ReplayResult
verify_parity(case_ref) -> ParityReport
```

`commit` atomically stores command, case, every artifact, evaluation/application result, receipt, dependency/invalidation edge, idempotency result, current alias, and outbox. It rejects state without receipt, receipt without exact artifacts, pack without evaluation/claims, event without command, or dependency graph that omits consumed IE refs.

### 6.11 Canonical serialization and hashing

Canonical JSON uses UTF-8, Unicode NFC, LF, lexicographically ordered keys, explicit enum spellings, canonical decimal strings, rational/integer source coordinates, semantic list ordering, and sorted-set normalization. Hashes use domain separators including product/object/schema version. `content_sha256` excludes itself and declared nonidentity operational metadata. Current time, random values, environment, locale, process/machine identity, filesystem order, absolute paths, and provider response arrival order cannot affect identity.

```text
artifact_hash = SHA256(domain_separator || canonical_payload_without_hash)
command_fingerprint = SHA256(command_domain || canonical_normalized_command)
event_hash = SHA256(event_domain || previous_event_hash || canonical_event_payload)
case_projection_hash = SHA256(ruleset_hash || genesis_hash || ordered_effective_event_hashes)
```

The same frozen manifest, exact proposal/evaluation bytes, decisions, and rulesets must reproduce byte-identical outputs in fresh processes and roots.

### 6.12 Compatibility and invalid examples

Semantic compatibility requires exact preservation/enforcement of owner, refs/hashes, IE lifecycle/epistemic state, maximum claim, negative evidence, limitations, source authority, wrong-reading risks, Primitive/archetype binding, evaluator independence, claim alternatives, supersession/invalidation, and consumption state. Parsing without behavior enforcement is incompatible.

Invalid examples:

- `{ "actual_role": "challenger" }` - no source, tension ontology, evidence, epistemic state, owner, evaluator, or alternative.
- `{ "planned_edge": "authority", "observed_edge": "authority" }` - copied labels without exact distinct refs and IE relation.
- `{ "expression_moment": "em-7", "activation": "success" }` - approval does not prove activation and exact version/hash is absent.
- `{ "primitive": "felt truth", "active": true }` - fuzzy name, no registry/binding/applicability/misuse/suppression evidence.
- `{ "reaction": "anchor_hit", "confidence": 0.94 }` - no exact Reaction Receipt/evaluation/profile/maximum claim; bare float.
- `{ "limitations": [] }` when the handoff names rejected/borderline evidence - adverse evidence dropped.
- AIR-serialized copies of IE Moment/Receipt fields presented as AIR-owned evidence - forbidden local fork.
- a pack published by the compiler that proposed it without independent evaluation - self-acceptance.
- a current query that returns a superseded/invalidated pack because it is “latest by timestamp” - lifecycle failure.

### 6.13 Read APIs

Future logical endpoints may include:

- `POST /observed-activative-compilations` typed command submission;
- `GET /observed-activative-compilations/{case_id}?version=&sha256=` exact case;
- `GET /observed-activative-intelligence-packs/{pack_id}?version=&sha256=` exact pack;
- `GET /observed-activative-intelligence-packs/{pack_id}/claims?dimension=&lifecycle=` claim page;
- `GET /observed-activative-intelligence-packs/{pack_id}/lineage` dependency/source view;
- `POST /observed-activative-intelligence-packs/{pack_id}/consumption-view` compatibility-gated read;
- `GET /observed-activative-compilations/{case_id}/replay-verification` historical proof.

Every response carries exact version/hash/owner/lifecycle/epistemic/maximum-claim/invalidation state and source restrictions. APIs do not expose a generic mutable patch.

## 7. Implementation stages and exact target paths

All paths are proposed future targets. No file in this section is created or authorized by Prompt 03. Final paths require ratification/adoption, independent audit/revision/re-audit/acceptance, repository instructions, and a bounded Development Capsule.

### 7.1 Stage 0 - accepted source and interface lock

- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-011/SOURCE_LOCK.yaml`
- Lock accepted TS-AIR-011, adopted TS-INT-004/006 interfaces, source authority, Primitive/archetype/planned-AIP contracts, evaluator profile, compatibility features, implementation allowlist, and claim ceiling.
- Maps: `AIR-FR-065`, `AIR-ST-11.03`; acceptance AC-01, AC-02, AC-20.

### 7.2 Stage 1 - immutable domain and canonicalization

- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/models.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/claims.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/commands.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/events.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/receipts.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/canonicalization.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/errors.py`
- Maps: AC-03 through AC-13, AC-16, AC-20.

### 7.3 Stage 2 - compilers, validators, and ports

- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/input_manifest.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/portfolio.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/claim_validator.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/primitive_archetype_evidence.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/planned_observed_interpreter.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/ports/evidence_admission.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/ports/portfolio_compiler.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/ports/independent_evaluator.py`
- Maps: AC-02 through AC-12.

### 7.4 Stage 3 - lifecycle, repository, dependency, replay

- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/service.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/repository.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/dependencies.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/replay.py`
- Maps: AC-13 through AC-19.

### 7.5 Stage 4 - adopted external adapters and projections

- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/adapters/interview_expression_evidence.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/adapters/primitive_archetype_registry.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/adapters/evaluation.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/adapters/downstream_consumption.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/projections/studio.py`
- Maps: AC-01, AC-02, AC-07, AC-11, AC-12, AC-19.

### 7.6 Stage 5 - migration and fixtures

- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/observed_intelligence/migrations/ai2_observed_pack_to_v2_1.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/fixtures/observed_intelligence/`
- Migration creates new immutable AIR artifacts, never rewrites AI2/Studio/IE bytes and never guesses missing evidence/authority/epistemic state.
- Maps: AC-18, AC-20.

### 7.7 Exact future test paths

- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/observed_intelligence/test_input_manifest.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/observed_intelligence/test_observed_claims.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/observed_intelligence/test_primitive_archetype_evidence.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/observed_intelligence/test_planned_observed_interpretation.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/observed_intelligence/test_pack_lifecycle.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/observed_intelligence/test_interview_expression_handoff.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/observed_intelligence/test_reaction_receipt_and_delta.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/observed_intelligence/test_downstream_consumption_view.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/observed_intelligence/test_compilation_vertical.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/observed_intelligence/test_atomic_repository.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/observed_intelligence/test_selective_invalidation.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/observed_intelligence/test_replay_and_cancellation.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_observed_intelligence_ownership.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_ai2_observed_pack_migration.py`
- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/cleanroom/test_observed_intelligence_portability.py`

### 7.8 Stage gates

No stage starts from `WRITTEN_PENDING_AUDIT`. Stage 0 requires ratified/adopted authority, independently accepted spec/interfaces, and capsule. Stages 2/4 require adopted IE and evaluation contracts rather than draft imports. Later pack publication remains a semantic artifact claim; it does not authorize derivative build, production, certification, Format 02, or VAE Stage 5.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Code | Meaning | Responsible boundary | Next admissible action |
|---|---|---|---|
| `AIR_OBSERVED_SOURCE_SCOPE_MISMATCH` | tenant/brand/source authority differs | admission/security | correct authorized scope; do not disclose foreign content |
| `AIR_OBSERVED_HANDOFF_MISSING_OR_STALE` | exact IE handoff/ref/hash/lifecycle unavailable | IE interface/admission | obtain exact current or historical eligible ref |
| `AIR_OBSERVED_EVIDENCE_OWNER_MISMATCH` | IE evidence presented as AIR-owned or vice versa | adapter/claim validator | reject fork and restore exact owner refs |
| `AIR_OBSERVED_EVIDENCE_INELIGIBLE` | rejected/superseded/invalidated/revoked dependency used positively | admission/validator | use lawful successor or preserve as negative evidence |
| `AIR_OBSERVED_NEGATIVE_EVIDENCE_DROPPED` | handoff adverse evidence absent from manifest/pack | input compiler | rebuild full manifest; no publication |
| `AIR_OBSERVED_PLANNED_FIELD_PROMOTED` | planned/inferred value copied as observed | compiler/validator | reject claim and use exact delta/evidence |
| `AIR_OBSERVED_CLAIM_UNSUPPORTED` | semantic claim lacks sufficient exact evidence | validator | add evidence or reject/bound candidate |
| `AIR_OBSERVED_MAXIMUM_CLAIM_EXCEEDED` | claim/pack exceeds upstream/evaluator ceiling | validator/lifecycle | lower claim or obtain eligible successor evidence |
| `AIR_OBSERVED_PRIMITIVE_REF_INVALID` | unknown/fuzzy/stale Primitive or binding | Primitive resolver | resolve exact registry/binding version/hash |
| `AIR_OBSERVED_PRIMITIVE_MISUSE` | claim conflicts with misuse/suppression/CBAR evidence | Primitive resolver | reject/bound; never force activation |
| `AIR_OBSERVED_ARCHETYPE_EVIDENCE_INSUFFICIENT` | archetype/role implication exceeds evidence | archetype resolver | keep hypothesis/unknown or gather evidence |
| `AIR_OBSERVED_PREMISE_OR_TAIL_COLLAPSED` | context removal creates false tension/release | CBAR/source validator | restore complete source context or reject |
| `AIR_OBSERVED_WRONG_READING_WEAKENED` | source/parent lock is removed or relaxed | validator/adapter | reject; only authorized upstream successor may relax |
| `AIR_OBSERVED_EVALUATOR_NOT_INDEPENDENT` | compiler/proposer and evaluator identities overlap | evaluation gateway | route to independent evaluator |
| `AIR_OBSERVED_SELF_ACCEPTANCE_ATTEMPT` | producer attempts final lifecycle acceptance | lifecycle | deny and preserve attempt receipt |
| `AIR_OBSERVED_COMPATIBILITY_FEATURE_UNSUPPORTED` | required semantic feature absent | compatibility | reject; no parse-only fallback |
| `AIR_OBSERVED_SOURCE_AUTHORITY_DENIED` | requested use violates source scope | source authority | deny or obtain attributable new scoped authority |
| `AIR_OBSERVED_NOT_APPLICABLE_UNEVIDENCED` | N/A lacks policy/reason/evidence/effect | model/validator | provide evidence-bearing union or fail |
| `AIR_OBSERVED_NONPORTABLE_REF` | path/locator is machine-specific | canonicalization | replace with portable immutable ref |
| `AIR_OBSERVED_STALE_EXPECTED_VERSION` | optimistic case/object mismatch | caller/repository | reload and submit newly evaluated intent |
| `AIR_OBSERVED_IDEMPOTENCY_COLLISION` | same key with different normalized command | caller/repository | reconcile and use a new key |
| `AIR_OBSERVED_ATOMIC_COMMIT_FAILED` | full bundle did not commit | repository | roll back all visibility; exact retry allowed |
| `AIR_OBSERVED_DEPENDENCY_INVALIDATION_INCOMPLETE` | affected descendant remains current | dependency projector | quarantine aliases and resume idempotent traversal |
| `AIR_OBSERVED_LATE_RESULT_AFTER_CANCELLATION` | proposal/evaluation returns after cancellation | orchestration | quarantine noncanonical result |
| `AIR_OBSERVED_REPLAY_DIVERGENCE` | exact historical inputs do not reproduce | repository/ruleset | quarantine case/release and report first divergence |
| `AIR_OBSERVED_MIGRATION_LOSSY_OR_AMBIGUOUS` | predecessor cannot map without invention | migration | block or preserve typed unresolved historical artifact |

Failure records contain safe exact IDs, versions/hashes, failing invariant/field, owner, source/evaluation context refs, retryability, affected descendants, and next action. Sensitive evidence content is redacted unless explicitly authorized.

### 8.2 Retry versus semantic repair

Operational storage/transport failure may retry exact bytes with the same idempotency key. Model/evaluator retry is allowed only when the pinned binding declares the retry semantics; each returned proposal/evaluation byte set remains separately identifiable. Source gaps, ownership mismatch, stale evidence, unsupported claims, Primitive misuse, evaluator disagreement, source-authority denial, premise/tail collapse, and wrong-reading risk are not transient. They require a new source/evidence/claim/evaluation/human-resolution command and immutable successors. AIR cannot “repair” IE evidence.

### 8.3 Atomic rollback and partial results

The atomic bundle comprises command record, case version, input manifest, candidate/claim/Primitive/archetype/delta artifacts, evaluation application, pack or typed nonpublication result, compilation receipt, dependency/invalidation edges, idempotency result, current alias, events, and outbox intent. Fault at any internal boundary leaves either every artifact visible with one commit ID or none visible.

Raw external compiler/evaluator results may be retained in a quarantined run store with `NONCANONICAL_UNADMITTED`. They are never available through OAI/current queries and cannot become negative evidence until an accepted command binds them. Response loss after a successful commit is recovered by exact idempotent lookup, not by recompilation.

### 8.4 Optimistic concurrency and cancellation races

Two commands against one expected case head cannot both commit. The loser receives current safe version/hash and must re-evaluate intent; the service never auto-rebases a semantic decision. Required race behavior:

- IE evidence invalidation versus pack publication: ordering decides; publication after effective invalidation is denied; later invalidation stales the published pack/descendants additively.
- human contest resolution versus evaluator successor: one commits; the other reloads and may create a new resolution/evaluation version.
- cancellation versus compiler/evaluator callback: cancellation-first quarantines late result; commit-first makes cancellation a successor event.
- source-authority revocation versus consumption acknowledgement: revocation-first denies; acknowledgement-first remains historical and current use becomes blocked by successor revocation.

### 8.5 Selective invalidation

Dependency edges are typed at field/claim granularity, including:

- `USES_HANDOFF`, `USES_SOURCE_PACKAGE`, `USES_EXPRESSION_MOMENT`, `USES_REACTION_RECEIPT`, `USES_TAG_ASSERTION`, `USES_NEGATIVE_EVIDENCE`;
- `INTERPRETS_PLANNED_OBSERVED_DELTA`, `INTERPRETS_PLANNED_ASSERTION`;
- `USES_PRIMITIVE`, `USES_PRIMITIVE_BINDING`, `USES_COALITION`, `USES_ARCHETYPE_EVIDENCE`;
- `SUPPORTED_BY`, `CONTRADICTED_BY`, `BOUNDED_BY_MAXIMUM_CLAIM`, `CONSTRAINED_BY_WRONG_READING`;
- `EVALUATED_BY`, `RESOLVED_BY`, `PUBLISHED_AS`, `CONSUMED_BY`.

Invalidation traverses only edges affected by the exact changed field/ref. A corrected Reaction Receipt outcome may stale reaction-significance and related activation/edge claims without staling an unrelated sensory-scene claim if an unaffected proof exists. A changed Moment boundary stales every claim that used the removed/added span. A planned-object change affects semantic delta interpretations, not raw IE observations. Descendant traversal is resumable/idempotent; pending or incomplete invalidation blocks new consumption.

Historical artifacts remain readable to authorized auditors with their invalidation/supersession state. No invalidation deletes or rewrites source evidence, evaluations, HumanResolutionEpisodes, or prior packs.

### 8.6 Replay and historical reproduction

Replay resolves exact case commands/events; IE handoff/Moment/Receipt/delta/tag/negative-evidence bytes; AIR planned/Primitive/coalition/archetype bytes; compiler proposal bytes; deterministic validator/ruleset; evaluator/profile bytes; human resolutions; source authority; and invalidation view. It verifies every hash, owner, lifecycle-at-use, event chain, dependency edge, receipt/artifact parity, and pack hash.

If an external compiler/evaluator cannot be regenerated, replay uses stored exact outputs and replays deterministic admission/application. It never calls a newer model. An unavailable exact historical dependency produces `HISTORICAL_INPUT_UNAVAILABLE`, not reconstruction from current content. Mutable source-manifest drift does not imply distributed-byte corruption when historical content hashes remain available.

### 8.7 Migration and compatibility

An AI2/donor/Studio migration emits a new `ObservedPackMigrationAssessment` with exact predecessor path/ref/hash, source owner, adapter/ruleset, field disposition, unresolved omissions, output refs, and receipt. Rules:

- predecessor planned/source/receipt/moment refs map only when exact owner/version/hash resolves;
- flat `confirmed_roles`, `confirmed_stances`, `confirmed_stakes`, transfer/campaign strings become claim candidates, never validated claims, unless exact evidence/evaluator/lifecycle can be reconstructed;
- embedded `PlannedObservedDelta` strings cannot replace IE-owned delta evidence;
- empty tuples/defaults cannot be interpreted as `NOT_APPLICABLE` or negative evidence;
- missing Primitive/archetype binding, source authority, wrong-reading, evaluator, alternatives, maximum claim, dependency, or lifecycle blocks current publication;
- random/time IDs remain legacy metadata and never become canonical content identity;
- a predecessor resolved state is not automatically `VALIDATED`/`PUBLISHED` V2.1;
- migration does not create an IE artifact, source fact, or human decision;
- lossy/ambiguous input is preserved `LEGACY_IMPORTED_UNRESOLVED` or blocked.

Compatibility is semantic. An adapter that parses but drops/relabels any material field fails. Active historical consumers remain pinned to their accepted pack/version/features. Deprecation alone does not invalidate historical work; governed supersession/revocation/invalidation controls current use. No local IE schema fork is allowed.

### 8.8 Deployment rollback and recovery

Deployment rollback restores the last known-good compiler/validator/evaluator adapter/ruleset and current alias while retaining all artifacts created under the failed version. It never rewrites outputs to resemble the old version. New commands are blocked when required bindings are revoked or incompatible.

After crash, recovery:

1. verifies atomic commit markers and command/artifact/receipt/outbox parity;
2. rebuilds projections/current aliases from immutable events;
3. reconciles idempotency records and response-loss outcomes;
4. resumes invalidation from the last committed checkpoint;
5. replays affected cases and compares hashes;
6. quarantines on the first divergence rather than choosing a semantically similar replacement.

### 8.9 Degraded behavior

- IE evidence temporarily unavailable: new compilation/consumption requiring it blocks; no cached unverified “latest” fallback.
- Compiler unavailable: manifest may remain `INPUTS_FROZEN`; no generic model substitution.
- Evaluator unavailable: deterministic gates may run, candidate remains `EVALUATION_REQUIRED`/`NEEDS_MORE_EVIDENCE`.
- Studio unavailable: canonical AIR commands/APIs may continue if authorized; projection/HumanResolution waits.
- Downstream consumer unavailable: published pack remains published; acknowledgement is pending and distinct.
- Optional/inapplicable dimension: evidence-bearing N/A may allow bounded publication if the profile and maximum claim permit.
- Required evidence gap: case records a blocker or truthful no-compilable result; it does not emit an apparently complete pack.

### 8.10 Observability and security

Metrics/logs/events expose safe identifiers and governed classifications:

- admission outcomes by exact failure class;
- handoff/Receipt/Moment lifecycle and claim-ceiling denials;
- candidate/admitted/rejected/contested/unknown claim counts by dimension;
- negative-evidence retention failures;
- planned-field promotion attempts;
- Primitive/archetype activation/conflict/misuse/suppression/N/A;
- premise/reaction-tail collapse and wrong-reading weakening denials;
- compiler/evaluator disagreement and independence failures;
- publication/nonpublication outcomes and maximum claim;
- idempotency/concurrency/atomic rollback;
- invalidation fan-out/lag and consumption blocks;
- replay duration/divergence and historical-input gaps;
- nonportable ref and cross-scope access attempts.

Default logs exclude transcript/media content, quotes, identity observations, human reaction details, credentials, and restricted source data. Technical security enforces tenant isolation, least privilege, redaction, encryption, retention, audit integrity, and secret management. It does not create generic creative/content-rights approval authority or override operator source sovereignty.

## 9. Behavior-specific acceptance criteria

These are later implementation/audit requirements, not this writer's PASS claims.

### AC-01 - Exact draft, source, and authority inputs

**Governs:** `AIR-FR-065`, `AIR-ST-11.03`. **Given** the Wave 8 inputs, **when** admission/source lock runs, **then** TS-INT-004 and TS-INT-006 exact paths/states/bytes/hashes and `DRAFT_DEPENDENCY_NOT_ACCEPTED` labels match, required source/Primitive bytes resolve, and candidate/build ceilings remain explicit. A drifted draft or missing required unique source blocks. **Evidence:** source-lock/draft-dependency receipts and hash matrix. **Layer:** contract/clean-room.

### AC-02 - IE evidence and AIR semantics remain separate

**Governs:** `AIR-FR-065`, Story ownership/denial. **Given** an eligible IE handoff, **when** AIR compiles, **then** every IE evidence object remains exact/ref-owned by IE and every new semantic claim/pack is AIR-owned. An AIR-local “normalized Reaction Receipt” or an IE-authored OAI semantic claim fails. **Evidence:** ownership conformance receipt/import graph. **Layer:** architecture/contract.

### AC-03 - Complete frozen input manifest

**Governs:** FR trigger/preconditions. **Given** handoff, moments, receipts/deltas, tags, negative evidence, source authority, profiles, and semantic dependencies, **when** the case opens, **then** the manifest includes every exact eligible and adverse ref with owner/lifecycle/hash/max claim. Omitting a rejected/borderline ref named by the handoff fails `AIR_OBSERVED_NEGATIVE_EVIDENCE_DROPPED`. **Evidence:** manifest and dependency graph. **Layer:** integration.

### AC-04 - Approved source evidence is not automatic activation

**Governs:** FR actual-activation compilation. **Given** an approved Expression Moment whose Reaction Receipt is partial/needs-evidence, **when** claims compile, **then** AIR may preserve a bounded hypothesis/partial claim but cannot assert activation success beyond the receipt ceiling. “Moment approved therefore activation succeeded” fails. **Evidence:** claim/evaluator/maximum-claim chain. **Layer:** unit/integration.

### AC-05 - Planned fields cannot become observed

**Governs:** FR invariant and adversarial denial. **Given** planned role/edge/pressure values matching a source label but no supporting observed evidence, **when** the portfolio compiles, **then** the values remain planned refs and observed claims are unknown/rejected. Copying the plan into actual role fails. **Evidence:** planned-observed separation fixture and typed denial. **Layer:** adversarial/contract.

### AC-06 - Actual role, direction, pressure, urge, edge, stake, and stance are evidence-bounded

**Governs:** FR required output. **Given** complete source evidence, **when** each dimension claim validates, **then** it carries exact support/contradiction, ontology, owner, epistemic state, alternatives, evaluator, maximum claim, and dependencies. A flat unreferenced string fails. **Evidence:** per-dimension claim matrix. **Layer:** unit/schema/integration.

### AC-07 - What failed and what remained unresolved are first-class

**Governs:** Story terminal “what emerged and what did not.” **Given** a planned activation that did not occur with sufficient coverage and an inference lacking sufficient evidence, **when** the pack publishes, **then** it contains distinct failed/not-observed and unresolved-inference claims. Dropping them to make a clean success pack fails. **Evidence:** negative/unknown evidence fixture and pack snapshot. **Layer:** integration.

### AC-08 - Primitive identity and applicability

**Governs:** Story Primitive requirement. **Given** exact Primitive/binding refs, **when** Primitive evidence compiles, **then** activation/conflict/misuse/suppression/N/A is tested from exact bytes/evidence. A fuzzy “felt truth” label or a hard-coded prose summary fails. **Evidence:** registry hash/binding/applicability receipt. **Layer:** unit/contract.

### AC-09 - Tension and release preserve premise and tail

**Governs:** `PRM-PRS-002`, Story CBAR. **Given** a line that appears resolved only after its qualifier/reaction tail is removed, **when** OAI compilation runs, **then** the claim remains unresolved/limited or is rejected; full source context remains linked. A manufactured payoff fails `AIR_OBSERVED_PREMISE_OR_TAIL_COLLAPSED`. **Evidence:** before/after source-boundary and CBAR denial. **Layer:** reference-slice/adversarial.

### AC-10 - Felt truth is source-backed, not manufactured

**Governs:** `PRM-VSG-021`, source fidelity. **Given** genuine source friction and a cleaner synthetic substitute, **when** semantic evidence is assessed, **then** the source-backed ref remains authoritative and synthetic visual salience cannot prove felt truth. Manufactured messiness or a distracting technical flaw treated as activation fails. **Evidence:** exact source visual/audio refs and Primitive evaluation. **Layer:** integration/adversarial.

### AC-11 - Sensory specificity is preserved without overload

**Governs:** `PRM-VOC-009`, source context. **Given** a specific sensory scene supporting a claim, **when** the pack compiles, **then** it preserves the exact source context and marks generic substitution or overload/misuse. Replacing it with “imagine a beach” fails. **Evidence:** moment span and Primitive misuse fixture. **Layer:** unit/reference slice.

### AC-12 - Planned-observed delta is interpreted, not rewritten

**Governs:** FR planned-observed output. **Given** an IE-owned `DIVERGED` or `UNEXPECTED_OBSERVED` delta, **when** AIR compiles semantic implications, **then** exact planned and observed refs/owners and relation remain unchanged; AIR emits a separate interpretation with non-implications. Editing the IE relation fails. **Evidence:** producer/consumer byte preservation. **Layer:** contract/integration.

### AC-13 - Candidate portfolio precedes convergence

**Governs:** candidate authority lifecycle. **Given** evidence supporting multiple plausible edge/role readings, **when** the compiler runs, **then** it retains alternatives, contradiction, disconfirmation, stopping evidence, and unknowns before evaluation. Selecting the highest score and deleting alternatives fails. **Evidence:** portfolio fixture and candidate hashes. **Layer:** model-program/integration.

### AC-14 - Independent evaluation controls publication

**Governs:** Story evaluator evidence. **Given** a pack candidate, **when** evaluator identity equals compiler/proposer or no evaluation exists, **then** publication fails. With independent `VALIDATED` evidence and all deterministic gates passing, publication may proceed within maximum claim. **Evidence:** evaluator-independence and lifecycle receipts. **Layer:** architecture/security/integration.

### AC-15 - Human resolution is attributable and scoped

**Governs:** semantic contest recovery. **Given** a contest requiring human choice, **when** Studio submits an exact HumanResolutionEpisode-backed command, **then** AIR records the scoped decision and preserves all prior candidates/evaluation disagreement. Hidden direct UI mutation or automatic global-learning promotion fails. **Evidence:** HumanResolution lineage and replay. **Layer:** integration/architecture.

### AC-16 - Atomic publication, idempotency, and concurrency

**Governs:** receipt trust/recovery. **Given** fault injection and concurrent commands, **when** publication commits, **then** command/case/manifest/claims/evaluation/pack/receipt/dependencies/idempotency/current alias/event/outbox are all visible or none are. Exact retry returns original outcome; same key/different bytes or stale head commits nothing. **Evidence:** fault/race matrix. **Layer:** repository.

### AC-17 - Selective invalidation and unaffected proof

**Governs:** Story supersession. **Given** one Reaction Receipt, Moment boundary, planned assertion, Primitive binding, or evaluator profile changes, **when** dependency projection runs, **then** only field-dependent claims/packs/descendants stale and unrelated evidence remains current with proof. Global invalidation or raw-evidence mutation fails. **Evidence:** typed dependency graph and invalidation receipt. **Layer:** integration/replay.

### AC-18 - Exact historical replay

**Governs:** Story recovery. **Given** superseded/rejected/invalidated history, **when** replay runs in a fresh process with exact view cutoff, **then** all canonical bytes/hashes/events/receipts reconstruct without current models/latest refs. Missing bytes return exact typed failure. **Evidence:** replay hash matrix. **Layer:** replay/clean-room.

### AC-19 - Downstream sovereignty and acknowledgement separation

**Governs:** Story/FR-066 boundary. **Given** a published OAI Pack, **when** a downstream product consumes it, **then** source/semantic owners, exact refs, limitations, wrong-reading constraints, maximum claim, and `downstream_reinterpretation_authorized:false` survive; acknowledgement is distinct from production/derivative authorization. Rewriting guest meaning or treating acknowledgement as production acceptance fails. **Evidence:** consumer conformance receipt. **Layer:** contract/integration.

### AC-20 - Portability and truthful claim ceiling

**Governs:** all packet/status requirements. **Given** two roots/fresh processes with altered clock/random/environment/order/locale, **when** compilation/replay uses identical exact inputs, **then** canonical bytes/hashes match and contain no absolute machine path. Status remains `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, build false; production/certification claims fail. **Evidence:** clean-room reproduction/absolute-path/status scan. **Layer:** clean-room/architecture.

## 10. Testing and completion evidence

### 10.1 Unit and property tests

`tests/unit/observed_intelligence/test_input_manifest.py` must cover complete manifests, every exact IE lifecycle, missing/adverse evidence, source scope, feature compatibility, N/A unions, and stable ordering.

`tests/unit/observed_intelligence/test_observed_claims.py` must cover every dimension/value/epistemic/lifecycle combination, support/contradiction rules, maximum-claim propagation, identity candidate nonpromotion, alternatives, and unknown/N/A.

`tests/unit/observed_intelligence/test_primitive_archetype_evidence.py` must resolve exact `PRM-VOC-009`, `PRM-VSG-021`, and `PRM-PRS-002`; test activation, conflict, misuse, suppression, and inapplicability; reject fuzzy name and no-binding input.

`tests/unit/observed_intelligence/test_planned_observed_interpretation.py` must cover all seven IE relation values, exact owner/ref preservation, non-implications, stale planned object, evidence gap, and no rewrite.

`tests/unit/observed_intelligence/test_pack_lifecycle.py` must cover every legal/illegal transition, evaluation/human-resolution gates, nonpublication outcomes, supersession, invalidation, revocation, and current/historical eligibility.

Property tests vary map insertion, set order, provider callback order, time/timezone, locale, environment/hash seed, filesystem enumeration, random seed, and machine root while requiring identical canonical results.

### 10.2 Contract tests

`tests/contract/observed_intelligence/test_interview_expression_handoff.py` must validate every TS-INT-004 field/owner/lifecycle/limit/negative-evidence/wrong-reading constraint, exact hash preservation, unknown-feature denial, and no IE write path.

`tests/contract/observed_intelligence/test_reaction_receipt_and_delta.py` must validate TS-INT-006 observation/receipt/delta/evaluator/maximum-claim/source-authority preservation; deny planned promotion, AIR-local normalization, parse-only adapters, and invalidated/superseded positive use.

`tests/contract/observed_intelligence/test_downstream_consumption_view.py` must prove exact pack/claim/source refs, constraints, feature negotiation, acknowledgement separation, stale-pack denial, and no reinterpretation authority.

Positive and negative vectors cover every section 6 type, reject unknown fields/open maps/bare floats/null-as-N/A/nonportable refs, and prove no local schema fork.

### 10.3 Compilation fixture portfolio

The governed portfolio must include:

1. complete source evidence supporting an actual role/direction/edge with independent evaluation;
2. approved Moment but partial/limited Reaction Receipt;
3. planned role/edge not observed with sufficient coverage;
4. unexpected observed edge absent from plan;
5. evidence gap where failure cannot be claimed;
6. contradictory/contested role candidates;
7. rejected and borderline Moment/tag evidence constraining a pack;
8. real source tension with no release;
9. qualifier/reaction tail whose removal would create false release;
10. source-backed sensory scene versus generic substitution;
11. felt-truth source friction versus manufactured/polished substitute;
12. Primitive conflict, misuse, suppression, and N/A;
13. archetype evidence insufficient for derivative route;
14. identity candidate observation that cannot mutate Identity DNA;
15. source-authority restriction blocking one downstream use;
16. zero-compilable-semantics truthful outcome;
17. evaluator disagreement requiring HumanResolution;
18. superseded evidence with selective invalidation and replay.

Each fixture pins exact source/input/profile/binding/compiler/evaluator bytes and expected portfolio/claim/pack/receipt hashes or denial code. No numeric threshold is invented by this spec.

### 10.4 Repository, replay, cancellation, and recovery tests

`tests/integration/observed_intelligence/test_atomic_repository.py` must fail after every commit member; prove no artifact/receipt/event/idempotency/outbox parity gap; test response-loss retry, collision, stale version/hash, concurrent evaluation/publication, and exact-not-latest reads.

`tests/integration/observed_intelligence/test_selective_invalidation.py` must exercise every typed upstream edge, resumable traversal, pending invalidation consumption block, unaffected proof, later source-authority revocation, and historical preservation.

`tests/integration/observed_intelligence/test_replay_and_cancellation.py` must reproduce accepted/rejected/contested/needs-evidence/superseded/invalidated/revoked/cancelled histories; store external proposal/evaluation bytes; test both cancellation race orderings, corrupt/missing dependency, checkpoint/genesis equivalence, and first-divergence reporting.

In-memory and durable repositories must run the same conformance suite. A permissive dictionary fake cannot satisfy evidence.

### 10.5 Architecture and ownership tests

`tests/architecture/test_observed_intelligence_ownership.py` must fail when:

- AIR defines or mutates authoritative IE Moment/Receipt/tag/source objects;
- IE or Studio compiles AIR OAI semantic claims;
- a compiler exposes evaluator/accept/publish shortcuts;
- evaluator identity matches compiler/proposer;
- domain imports adapter/provider/filesystem/clock/random/UI/Pipeline/VAE/Builder/Delegation code;
- Studio writes canonical state rather than typed commands/projections;
- Pipeline, VAE, Builder, or Delegation reinterprets source or semantic claims;
- current aliases/latest reads enter replay/compilation;
- generic content-rights/creative-safety approval is introduced.

### 10.6 Migration and brownfield tests

`tests/migration/test_ai2_observed_pack_migration.py` must cover flat confirmed roles/stances/stakes, empty defaults, embedded delta, missing evaluator/Primitive/archetype/authority/maximum claim/dependencies, random/time identity, exact predecessor refs, duplicate imports, and blocked current publication. It must preserve original bytes/hash and create only additive migration artifacts/receipts.

Donor/Studio behavior is a fixture, not proof of current architecture. No historical PASS, schema parsing, or local model validation counts as OAI implementation acceptance.

### 10.7 Clean-room, security, and portability tests

`tests/cleanroom/test_observed_intelligence_portability.py` must compile/replay from two extracted roots and fresh processes under varied locale/timezone/environment/order/random state. It scans packs, receipts, manifests, fixtures, logs, archives, and exports for drive/UNC/temp/user/host/process paths and undeclared file dependencies.

Security tests cover organization/brand/source scope, actor command authority, evidence-read scope, redacted logs, idempotency abuse, source-retention/training restrictions, current/historical read privilege, outbox integrity, and revocation timing. They preserve product/source sovereignty.

### 10.8 Imported-interview reference-slice proof

The later frozen reference slice must prove:

`Canonical Interview Source Package` -> exact transcript/media/keyframes/tags -> IE Reaction Receipts/deltas -> approved/rejected/borderline Expression Moment evidence -> TS-INT-004 evidence handoff -> AIR input manifest -> claim candidate portfolio -> deterministic validation -> Primitive/archetype/planned-observed compilation -> independent evaluation/HumanResolution if required -> published or truthfully blocked OAI Pack -> exact downstream consumption view -> selective invalidation -> historical replay.

It must include absent Brief-led history without invention, one qualifier/tail collapse denial, one planned-field promotion denial, one unexpected edge, one null/evidence-gap distinction, one negative-evidence constraint, one source-authority restriction, one evaluator disagreement, one HumanResolution, and one fresh-process reproduction. It stops before transfer/Final Script/derivative/production implementation and does not activate Format 02 or VAE Stage 5.

### 10.9 Required later build evidence

A separately authorized build would require:

- ratification/adoption and Development Capsule/source lock;
- accepted TS-AIR-011 and adopted TS-INT-004/006 contracts;
- exact implementation/file/dependency/build manifests;
- schema vectors and producer/consumer conformance;
- Primitive/archetype/CBAR evidence;
- compiler binding, applicability, proposal portfolio, stopping evidence, and baseline comparison;
- independent evaluator identity/profile/calibration/disagreement evidence with truthful certification state;
- complete fixture, repository atomicity, replay, cancellation, invalidation, migration, security, and clean-room results;
- HumanResolution capture/promotion-scope evidence;
- independent audit, bounded revision, independent re-audit, and attributable acceptance;
- Build Receipt with exact bytes/hashes and maximum claim.

This writer issues none of those artifacts or a Build Receipt.

### 10.10 Prompt 03 writing handoff

The controller must verify:

- this exact spec path, bytes, SHA-256, and ten numbered sections;
- `SPEC_WRITING_RECEIPT.yaml` with `WRITTEN_PENDING_AUDIT` and no build claim;
- `FILES_READ_RECEIPT.yaml` with exact source/authority/dependency states and hashes;
- `SOURCE_TRACEABILITY.yaml` mapping FR/Story/ownership/source/sections/evidence;
- `DRAFT_DEPENDENCY_RECEIPT.yaml` with both IE drafts, `DRAFT_DEPENDENCY_NOT_ACCEPTED`, dispatch lock, and six-section revision impacts;
- `WRITER_FILE_MANIFEST.json` with exact pre-manifest artifact hashes;
- no edit outside the spec and five standard receipt files.

Final state:

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

This is specification writing only. It grants no product implementation, schema/release creation, adoption, Development Capsule, build, production, publication, certification, Format 02, or VAE Stage 5 authority.
