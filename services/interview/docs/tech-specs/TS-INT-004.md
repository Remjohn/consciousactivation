# TS-INT-004 — Tag Provenance, Anchor Hit, and Expression Moment Governance

```yaml
spec_id: TS-INT-004
title: Tag Provenance, Anchor Hit, and Expression Moment Governance
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product_owner: Interview Expression
writing_wave: 7
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
controlling_frs:
  - AIR-FR-061
  - AIR-FR-062
  - AIR-FR-063
  - AIR-FR-064
  - AIR-FR-066
  - FR-127
  - FR-130
  - FR-131
controlling_stories:
  - AIR-ST-11.01
  - AIR-ST-11.02
  - AIR-ST-11.03
  - ST-02.01
  - ST-02.03
upstream_drafts:
  - spec_id: TS-INT-002
    path: 06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-002.md
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 1aff9aca4776d0dbb8254882814b6277303258924990a0f75640798768f4123d
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-INT-003
    path: 06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-003.md
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: d6075ebbc317a2e9f363bebfedda78dcf7d8d31dc1377dbc15b212f7800bd1d6
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-INT-006
    path: 06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-006.md
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 3fb216913d8e0c52e3a51db65b6a3c848240cc3d040f9806fd8d3c85a443f58d
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
```

This candidate specification is authorized for technical writing and later independent review only. It creates no product implementation, schema release, build, production, publication, certification, or Development Capsule authority. Interview Expression owns tag-provenance records, source-backed Anchor Hit evidence, Expression Moment discovery, evaluation, approval, and lifecycle. It consumes exact transcript, visual-index, and Reaction Receipt evidence without taking ownership of those upstream artifacts. Activative Intelligence Runtime (AIR) owns the semantic compilation of Observed Activative Intelligence; this specification emits a source-evidence handoff and does not compile or mutate an Observed Activative Intelligence Pack.

## 1. Files and authorities read

### 1.1 Writer, dispatch, and claim-ceiling inputs

All digests are SHA-256 over the exact bytes read.

| File | Bytes | SHA-256 | State and use |
|---|---:|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | 9,624 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Current one-spec writer law |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_07_DISPATCH_LOCK.yaml` | 1,077 | `c24768d1d2ea36d08138b9beefe9b83c7b2f8b767c34641edf89be55b7289f67` | Wave 7 path and three-upstream lock |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012 | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact `CA-P03-WRITE-TS-INT-004-RECOVERY` packet |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | 1,221 | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate authority and acceptance ceiling |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | 1,462 | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Specification-work-only authorization |

No `AGENTS.md` governs `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-004.md`. The recovery packet classifies the target as `DIRECT_PRODUCT_SPEC_PATH` and grants this writer only the one exact specification path plus its Program Control writer receipts.

### 1.2 Current constitutional and candidate ownership inputs

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | 791 | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Current constitutional pointer |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | 40,830 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Highest current authority for source truth, human reaction, Expression Moments, and semantic lineage |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | 4,289 | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Candidate product boundaries; Interview Expression owns Expression Moment resolution |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | 4,263 | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Candidate one-owner ledger; AIR owns Observed Activative Intelligence while IE owns its source evidence |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/PRODUCT_ROOT_REGISTRY.yaml` | 1,621 | `bb898168c770a09d0d6974c3ed347cf07b7770ccc41da094bb325c1777baa0be` | Intended IE root; implementation remains unauthorized |

The candidate ownership package remains `CANDIDATE_NOT_CURRENT`. It is usable for this explicitly authorized writing pass, not as a claim of ratification or current adoption.

### 1.3 Reconciliation, requirements, Stories, and donor

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | 23,269 | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Canonical ID, title, owner, path, and merged-donor disposition |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | 104,516 | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Eight controlling FRs and the AIR/IE ownership split |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | 236,715 | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Exact FR, Story, source, evidence, and claim-ceiling trace |
| AIR bundle `prd/features/F11-expression-moments-and-observed-activative-intelligence.md` | 40,218 | `7362192f28832e0ab745e0c57adfa5af6c30183990c39b0c49d360ab4bbcc09a` | Candidate AIR requirements; split at source-evidence versus semantic compilation ownership |
| AIR bundle `planning/EPICS_AND_VERTICAL_STORIES.md` | 301,040 | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | `AIR-ST-11.01` through `AIR-ST-11.03` and their CBAR mandates |
| AIR bundle `specs/TS-AIR-011-expression-moments-and-observed-activative-intelligence.md` | 27,991 | `5052b69a297d71480b3cb070836d20799477a7c1d5850bd0d85dfd818107c386` | Full donor; Expression Moment portion merged here, Observed AIP compilation remains AIR-owned |
| AHP bundle `prd/features/F22-activative-tags-expression-moments-keyframes-and-asset-package-spec.md` | 17,347 | `d93b5c4fb09d6ba3f35cf84a2206b1100fa457abf94acd384ca703dc4ca5cd6e` | `FR-127`, `FR-130`, and `FR-131` behavior |
| AHP bundle `planning/EPICS_AND_VERTICAL_STORIES.md` | 190,553 | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | `ST-02.01` and `ST-02.03` with Hunter/Analyst boundary |
| AHP bundle `planning/spec_assignments/TS-INT-004.md` | 3,097 | `79453095795dc935d1bc30cf36ec817dc8e7f8be45d43913b82f49bc03ebfd05` | Assignment brief only; superseded output path corrected by Program Control |
| AHP bundle `governance/CURRENT_WRITING_PROFILE.md` | 11,536 | `ba88c5572ae3f7571daac9991a0d325a20f491cb9c0ea7c3816deb3ff3d32956` | Source-first, CBAR, owner, and claim-ceiling writing laws |
| AHP bundle `sources/EXACT_SOURCE_REUSE_CROSSWALK.csv` | 21,449 | `c8c97f5d2003d070180a7061484609b2f9c8ef990efa116914f05b4e400e7820` | Predecessor use requires bounded review and disposition |

`AIR-FR-065` is intentionally not a controlling FR here. Its canonical owner/spec is AIR/`TS-AIR-011`. `AIR-ST-11.03` is controlling only for `AIR-FR-066`—the exact source-evidence handoff boundary. This specification must not compile the AIR-owned Observed Activative Intelligence Pack.

### 1.4 Exact non-accepted upstream drafts

| Draft | Bytes | SHA-256 | Exact interface consumed |
|---|---:|---|---|
| `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-002.md` | 41,708 | `1aff9aca4776d0dbb8254882814b6277303258924990a0f75640798768f4123d` | `WRITTEN_PENDING_AUDIT`; exact words, speakers, audio events, rational source time, packed phrases, tag refs, limitations, correction, and replay |
| `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-003.md` | 76,365 | `d6075ebbc317a2e9f363bebfedda78dcf7d8d31dc1377dbc15b212f7800bd1d6` | `WRITTEN_PENDING_AUDIT`; shot map, keyframes, visual references, source-frame identity, technical uncertainty, and non-semantic candidate evidence |
| `06_INTERVIEW_EXPRESSION/docs/tech-specs/TS-INT-006.md` | 84,791 | `3fb216913d8e0c52e3a51db65b6a3c848240cc3d040f9806fd8d3c85a443f58d` | `WRITTEN_PENDING_AUDIT`; Reaction Receipt, observation stream, outcome, reaction tail, planned–observed delta, evaluator, and maximum claim |

All three inputs are labeled `DRAFT_DEPENDENCY_NOT_ACCEPTED`. A hash change in any one reopens this specification’s governing decisions; proposed architecture and workflows; data models, contracts, schemas, and APIs; failure/migration/rollback/recovery/observability; acceptance criteria; and testing/completion evidence. None is represented as ratified authority.

### 1.5 Required unique evidence and source dispositions

| Source | Bytes | SHA-256 | Current disposition and use |
|---|---:|---|---|
| AIR bundle `sources/ai_v2_predecessor/contracts/04_EXPRESSION_MOMENT.md` (`SRC-AI2-EXPRESSION-001`) | 436 | `049fdb1711f3aa0cddc3d85e48491c9e0aa8f2b878e0f3fbb25dbc1b6a755802` | `REQUIRED_UNIQUE_EVIDENCE`; exact span, speaker, context, Reaction Receipt, qualities, route, lifecycle, approval, risks |
| AIR bundle `sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` (`SRC-INT-001`) | 43,321 | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | `REQUIRED_UNIQUE_EVIDENCE`; human expression is the source and derivatives follow extraction |
| AIR bundle `sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` (`SRC-INT-002`) | 24,239 | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | `REQUIRED_UNIQUE_EVIDENCE`; complete session, anchor, Expression Moment, and downstream routing predecessor |
| `THE_CMF_STUDIO(2)/CCP V9.1 Expression Capture & Archetype Routing Update.md` (`SRC-INT-003`) | 24,239 | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | `REQUIRED_UNIQUE_EVIDENCE`; second registered occurrence with identical bytes, retained as provenance alias rather than duplicate doctrine |
| AIR bundle `sources/brownfield/CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1.zip` (`SRC-AM-001`) | 13,678 | `9059fe3cad98c5d6ca0f9584f091ac503a5e5a9279a4a476821db816dc7603b8` | `REQUIRED_AUTHORITY`; Studio is projection/command surface; HumanResolution is captured, not hidden mutation |
| AIR bundle `sources/doctrine/AHP_PRD_V1_1_SOURCE_FIRST.md` (`SRC-SOURCE-FIRST-001`) | 517,771 | `cc1cfa721238b999adb1612e805fad60c61c07c566df19d5044fc9e069651508` | `SUPERSEDED`; historical context only, never current authority |

`SRC-AM-002` is `DEFERRED_REFERENCE`. Its named production-activation archive is not present at an active workspace path, it is not unique authority for these FRs, and no claim in this spec is attributed to it. `SOURCE_GAP_NOTICE.yaml` (17,743 bytes; `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886`) preserves the non-blocking gap. The current `SOURCE_DISPOSITION_LEDGER.yaml` is 134,201 bytes with digest `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3`.

### 1.6 Primitive evidence

| Primitive source | Bytes | SHA-256 | Bound use |
|---|---:|---|---|
| `PRM-VOC-009.yaml` — Sensory Scene Anchoring | 7,583 | `90405cef54e303ca87c2f274e6ac6a39b77cf261b86166a385e2ffb6420d5b80` | Preserve sensory premise/context; do not extract an abstract quote that destroys the lived scene |
| `PRM-VSG-021.yaml` — Punctum, Air, and Felt Truth | 8,179 | `06c75355f5f2bb083c09140e4af6994548e8d59fb544bf18553bc52966436cda` | Preserve source-backed friction/micro-expression evidence; do not manufacture or over-polish it |
| `PRM-PRS-002.yaml` — Tension-and-Release Narrative Engine | 6,893 | `4fba8edcb439c296a610b53a45ce76b9a002b4a128338e3302ddbb1cc49e242e` | Preserve the evidence-bearing premise, turn, and release without fabricating dramatic structure |

IE validates evidence preservation and applicability. It does not hard-code these summaries as substitutes for the Primitive bytes and does not compile a Primitive Coalition, archetype coalition, Edge Product, or downstream semantic program; those remain AIR-owned.

### 1.7 Brownfield implementation evidence

| File | Bytes | SHA-256 | Observed disposition |
|---|---:|---|---|
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/extraction.py` | 5,912 | `b3341f5e8e851d1ad80f64c887cdf4af4336afd1eeaceae1e2e953f5b6b825d3` | `ADAPT`; useful candidate shapes, but random UUIDs, wall-clock fields, floats, and free-form evidence are noncanonical |
| `THE_CMF_STUDIO(2)/src/ccp_studio/dspy_programs/extraction_compilers.py` | 5,717 | `aa41490ab06ee28c5f78f307d113d2147621fdff7a23a73944bd78a35820f7fa` | `ARCHIVE_AS_HEURISTIC`; first-guest-segment and keyword behavior cannot establish truth |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/extraction_service.py` | 15,679 | `b75ea88dc3b7981df3ad9a65ed3eb70d343514ff078d10f630dc8b64d6737d23` | `ADAPT`; command vocabulary and orchestration evidence, not atomic canonical authority |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/expression_review.py` | 10,893 | `a737d4bad778bab135e9b4cd5c60933f7566251607d99dfec6a2359af59b6c3f` | `ADAPT`; boundaries and review decisions, with owner/lifecycle/canonicalization corrections |
| `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/expression_review.py` | 2,450 | `4733ad27a685e11737f81287c58e05d358d8639c12e50af9666587c14dfcf166` | `REPLACE`; in-memory partial stores do not prove atomic state/receipt/dependency history |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/expression_review_service.py` | 32,393 | `de02c017a3a23fce66a9dacc389abe8bf6239a35e8be3940135aba6bbbda82db` | `ADAPT`; split/merge/approve/reject/supersede workflows remain useful predecessor evidence |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_anchor_hit_and_expression_moment_candidate_detection.py` | 8,248 | `85bec08209e8adb9019a98ef8f4bb36a584fbd6d5f05a4070d731b0436db49f0` | `ADAPT`; demonstrates candidate flow but not exact upstream lineage or deterministic identity |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_expression_moment_review_and_boundary_control.py` | 10,108 | `1d0ee6fac2dc0f18d87330993daa459d6fc5c67828713b3277c8e732ee5f9412` | `ADAPT`; review behaviors require current owner, atomic receipt, replay, and evidence gates |
| AIR predecessor `sources/ai_v2_predecessor/reference_implementation/models.py` | 24,677 | `f392c940349c5f9586a359fd8497ce1b8368de1b6654357deb146a686efd97` | `ADAPT`; strict Expression Moment shape is useful, but millisecond floats/strings and missing current lifecycle are insufficient |

The intended `06_INTERVIEW_EXPRESSION` root currently contains specifications only. There is no current product implementation or test suite to reuse, and this writing pass creates none.

## 2. Problem, user outcome, solution, and scope

### 2.1 Problem

An Expression Moment is not a catchy substring, a high detector score, a planned interview tag, a shot boundary, or an `ANCHOR_HIT` label copied from a Reaction Receipt. It is a governed, complete, source-backed unit of human expression whose speaker, premise, turn, reaction tail, source continuity, uncertainty, approval, and route limitations survive extraction.

A weak implementation can:

- treat planned `authority_conflict` as observed because it appeared in an Interview Asset Contract;
- normalize an inferred tag into a confirmed tag because the model score is high;
- select the first guest segment once per contract and call it an Anchor Hit;
- turn a visually striking keyframe into semantic importance;
- turn a Reaction Receipt outcome into an approved Expression Moment without context review;
- cut a catchy partial quote before the qualification that reverses its meaning;
- omit the silence, hesitation, premise, or reaction tail that makes the expression true;
- let the Hunter approve its own proposal or let a numeric score decide approval;
- discard rejected or borderline candidates, eliminating negative evidence and historical truth;
- permit a downstream router to query “latest” and silently consume a superseded moment;
- let Studio projection state overwrite the canonical moment; or
- compile AIR-owned Observed Activative Intelligence inside the source-evidence product.

Any of these failures propagates false or flattened human meaning into every later derivative.

### 2.2 User and system outcome

An expression analyst can inspect why a tag, Anchor Hit, or Expression Moment exists; which exact words, speakers, audio events, frames, observations, and Reaction Receipts support or contradict it; what was planned versus observed or inferred; who proposed, evaluated, approved, rejected, corrected, superseded, or revoked it; and which routes are technically/evidentially eligible. Approved moments can be handed to AIR without transferring source-evidence ownership or granting a derivative producer authority to reinterpret the guest.

### 2.3 Bounded solution

Interview Expression SHALL provide an immutable `ExpressionGovernanceCase` that:

1. registers typed tag assertions with separate epistemic provenance and lifecycle;
2. discovers source-backed `TimestampedAnchorHitCandidate` records without promotion authority;
3. assembles complete `ExpressionMomentCandidate` evidence from exact upstream refs;
4. validates premise, cause, expression turn, and reaction-tail boundaries;
5. independently evaluates completeness, specificity, identity signal, pressure survival, emotional/cognitive turn, audiovisual usability, and routeability under pinned profiles;
6. moves candidates through explicit proposed, observed, borderline, approved, rejected, superseded, and revoked states;
7. preserves rejected, incomplete, invalid, low-confidence, and borderline evidence with future admissibility conditions;
8. binds current approved/tag/negative-evidence refs to a successor Canonical Interview Source Package through its owning interface; and
9. emits an exact `ObservedActivativeEvidenceHandoff` for AIR to consume and semantically compile.

### 2.4 In scope

- Planned, observed, inferred, operator-confirmed, rejected, superseded, and revoked tag state without silent collapse.
- Exact tag evidence, authority, applicability, confidence/calibration, and lifecycle.
- Source-backed Anchor Hit proposal and independent validation.
- Expression Moment candidate discovery from phrase, audio, visual, Reaction Receipt, planned-context, observed-tag, and source-continuity evidence.
- Boundary assembly that preserves premise/cause, phrase, expression turn, and reaction tail.
- Typed qualities and evidential routeability under immutable profiles.
- Hunter, Analyst, approver, evaluator, and operator-resolution role separation.
- Approval, rejection, borderline, split, merge, boundary adjustment, supersession, revocation, and re-evaluation.
- Immutable decisions, receipts, dependencies, idempotency, optimistic concurrency, replay, cancellation, late evidence, and selective invalidation.
- Exact source-package binding and AIR handoff.

### 2.5 Out of scope and non-goals

- Transcript alignment, word/speaker evidence, phrase packing, or audio-event ownership (`TS-INT-002`).
- Shot detection, keyframe selection, visual evidence ownership, or source-frame semantics (`TS-INT-003`).
- Reaction Observation, Reaction Receipt, reaction outcome, or planned–observed delta ownership (`TS-INT-006`).
- Live interview execution, call choice, or pressure decision (`TS-INT-007`).
- AIR compilation of Observed Activative Intelligence, Primitive/archetype meaning, Matrix/role-tension meaning, Final Script, or transfer programs.
- Asset Package Spec compilation, derivative composition, Pipeline execution, VAE production, or Studio canonical state.
- Inventing evaluator thresholds, route certifications, publication approval, generic creative-safety/content-rights approval, or production readiness.
- Activating Format 02, VAE Stage 5, implementation, schema publication, model training, or a Development Capsule.

## 3. Governing decisions and constraints

### 3.1 Product sovereignty and object ownership

1. Interview Expression owns `TagAssertion`, `TimestampedAnchorHitCandidate`, `ExpressionMomentCandidate`, `ExpressionMomentDecision`, canonical `ExpressionMoment`, negative/borderline evidence, and the source-evidence handoff.
2. `TS-INT-002` owns exact transcript, word, speaker, phrase, and audio-event evidence. This service references those immutable records and cannot normalize, correct, or replace them.
3. `TS-INT-003` owns shot, keyframe, and visual-reference evidence. A keyframe marked `EXPRESSION_SIGNAL_CANDIDATE` remains a `NON_SEMANTIC_PROPOSAL`; this service must establish its relevance with other evidence.
4. `TS-INT-006` owns Reaction Observations, Reaction Receipts, outcomes, counteractivation, and planned–observed deltas. This service may cite an eligible receipt but cannot relabel its outcome or maximum claim.
5. AIR owns planned semantic objects and Observed Activative Intelligence compilation. `AIR-FR-065` stays outside this specification. IE emits exact approved source evidence for `AIR-FR-066`; AIR decides what that evidence means in its own versioned object.
6. Studio owns projection, typed review/correction commands, and HumanResolutionEpisode capture. It cannot write an Expression Moment directly. Pipeline, VAE, Builder, and Delegation do not become source-expression authorities.

### 3.2 Tag provenance is not one flat status

Every tag has two independent state axes:

- `provenance_kind`: `PLANNED`, `OBSERVED`, `INFERRED`, or `OPERATOR_CONFIRMED`;
- `lifecycle_state`: `CURRENT`, `REJECTED`, `SUPERSEDED`, or `REVOKED`.

The required compatibility projection `effective_tag_state` is derived as follows:

- a `CURRENT` planned, observed, inferred, or operator-confirmed tag projects to `PLANNED`, `OBSERVED`, `INFERRED`, or `CONFIRMED` respectively;
- any `REJECTED` tag projects to `REJECTED` while retaining its original provenance kind;
- any `SUPERSEDED` tag projects to `SUPERSEDED` while retaining its original provenance kind; and
- any `REVOKED` tag projects to `REVOKED` and is never route-eligible.

No update may transform `PLANNED` into `OBSERVED`, `INFERRED` into `CONFIRMED`, or `REJECTED` into current. Confirmation and correction create successor assertions with explicit edges. A tag’s confidence cannot change its provenance kind. Planned tags may guide discovery but cannot count as actual expression evidence.

### 3.3 Anchor Hit meanings remain distinct

`TimestampedAnchorHitCandidate` means a source-aligned candidate that a declared first-line, depth, landing, state-shift, or unexpected-source signal may have occurred. It is not:

- `TS-INT-006`’s human-reaction outcome `ANCHOR_HIT`;
- an approved Expression Moment;
- proof of a target state, psychological role, Primitive, archetype, route, or audience effect; or
- production or publication eligibility.

If a Reaction Receipt reports `ANCHOR_HIT`, the exact receipt may support a timestamped candidate but does not promote it. If a planned anchor text matches transcript words, that is planned-versus-observed relationship evidence, not proof that the intended activation landed.

### 3.4 Hunters propose; Analysts and authorized approvers govern promotion

- A Hunter may create tags, Anchor Hit candidates, Moment candidates, alternatives, and stopping evidence.
- A Hunter cannot emit `APPROVED`, route a candidate as production-ready, or serve as the candidate’s final independent evaluator.
- An Analyst checks source truth, completeness, boundary integrity, contradiction, uncertainty, source authority, and routeability under a pinned profile. An Analyst verdict is evidence, not necessarily final human approval.
- Only an actor with exact `expression_moment_approval` authority may approve. The approval command identifies the actor, scope, source-authority declaration, exact candidate/evaluation versions, and decision rationale.
- A model program cannot be the final approval actor. The same execution identity cannot propose and independently evaluate the same candidate. The Hunter workflow role cannot approve its own candidate even when the underlying human identity holds another role.
- Every Studio approval, rejection, boundary change, split, merge, supersession, or revocation emits both an IE decision receipt and a Studio-owned `HumanResolutionEpisode` ref where Studio mediated the decision. Capture is automatic; promotion into global learning or doctrine is not.

### 3.5 Complete source evidence and boundary law

An eligible candidate cites exact versions/hashes for:

- source package and primary media;
- transcript alignment and packed phrase transcript;
- ordered phrase and raw-word refs for the core expression;
- speaker assertions and audio-event refs;
- visual index and any keyframe/visual refs used;
- relevant Reaction Receipt(s), including reaction window/tail and maximum claim;
- planned tag/Brief/IAC refs only when present; imported sources retain absent-planning evidence;
- observed/inferred/confirmed tag assertions;
- source authority and restrictions; and
- profile/binding/evaluator/decision refs.

The boundary is a typed union of premise/cause, core expression, turn/landing, and reaction tail ranges. It uses exact rational source time and phrase/word/frame refs. The minimum boundary is the smallest complete window that preserves meaning, not the shortest quotable window. A missing required premise or reaction tail blocks approval; it is never filled with a semantic summary.

### 3.6 Expression qualities and routeability are evidence, not AIR meaning

IE may evaluate closed, source-evidence qualities such as completeness, specificity, identity signal, pressure survival, emotional/cognitive turn, audiovisual usability, source continuity, and quote fidelity. Each assessment names exact evidence, contradictions, profile, calibration, uncertainty, and maximum claim.

Routeability records which declared consumer route families can technically and evidentially consume the moment under exact constraints. It does not select an archetype coalition, compose an asset, choose a Final Script, or grant production certification. An unsupported or deferred route is `NOT_ELIGIBLE` or evidence-bearing `NOT_APPLICABLE`, never an omitted field or permissive default.

### 3.7 Primitive and CBAR constraints

- `PRM-VOC-009`: preserve the specific sensory premise and scene when applicable; generic abstraction is a denial condition.
- `PRM-VSG-021`: preserve genuine source-backed friction and micro-expression evidence; a polished or staged substitute is forbidden.
- `PRM-PRS-002`: preserve the source’s actual tension/turn/release; missing payoff, forced drama, or micro-tension exhaustion is recorded rather than repaired by invention.
- `ST-02.01` and `ST-02.03`: a Hunter cannot approve, unsupported/context-stripped moments cannot reach the archetype router or derivative job compiler, and rejected evidence remains retrievable only as negative evidence.

Primitive applicability points to the exact Primitive source and an AIR-owned binding or an evidence-bearing absence. IE may enforce misuse/suppression constraints applicable to source extraction. It does not compile Primitive semantic coalitions.

### 3.8 Applicability and `NOT_APPLICABLE`

Every material optional field uses either a typed value or `EvidenceBearingNotApplicable { reason_code, policy_ref, decision_actor_or_method_ref, inspected_evidence_refs, effect_on_eligibility }`. Null, empty string, empty untyped list, and “not needed” are invalid substitutes.

Examples:

- a historical/imported source can make planned-IAC comparison `NOT_APPLICABLE` with absent-planning evidence;
- a source with no usable face imagery can make visual micro-expression evidence `NOT_APPLICABLE` while transcript/audio evidence remains usable;
- a route family outside the declared profile is `PROFILE_DOES_NOT_DECLARE_ROUTE`, not routeable by default; and
- a Reaction Receipt can be absent only when the moment profile explicitly permits source-only historical evidence and states the resulting maximum claim.

### 3.9 Determinism, canonicalization, and portability

Canonical records use normalized UTF-8 JSON, lexicographically ordered map keys, closed enum spellings, integers and rational time, and semantically ordered arrays. Set-like collections are sorted by declared canonical keys. IDs derive from exact owner/scope/input/policy/version content, never UUID randomness. Authority-supplied logical time may be recorded but current time cannot affect identity. Bare floats, machine paths, usernames, hostnames, environment variables, filesystem iteration, provider callback order, locale, and random state are forbidden from canonical hashes.

An implementation that emits nondeterministic proposals may submit them as noncanonical Hunter evidence. Deterministic validation and canonical compilation decide the stored identity. Same accepted inputs, profiles, bindings, commands, and decisions must reproduce byte-identical artifacts and receipts.

### 3.10 Immutability, source authority, and claim ceiling

All tags, candidates, boundaries, assessments, decisions, approved moments, negative evidence, handoffs, receipts, dependencies, and invalidations are immutable. Correction creates a successor. Exact reads never substitute latest.

The operator-supplied source authority declaration governs processing, publication, derivative route, identity/voice use, model-training, retention, and restricted evidence. IE enforces that declaration; it does not create a generic creative-safety or content-rights approver. Technical security remains operational.

This specification’s state is `WRITTEN_PENDING_AUDIT`. Before ratification, its later maximum is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`; build authority remains false.

## 4. Current brownfield architecture

### 4.1 Current target state

`06_INTERVIEW_EXPRESSION` has no implementation source or tests. Its present files are candidate specifications. Therefore there is no current canonical repository, API, database, model, or schema to extend. All future implementation paths in section 7 remain proposals requiring later ratification/adoption, independent acceptance, and a bounded Development Capsule.

### 4.2 AIR-located donor split

`TS-AIR-011` defines `ExpressionMomentCandidate`, `ExpressionMoment`, `ExpressionMomentDecision`, `ObservedActivativeIntelligencePack`, and `ExpressionResolutionReceipt` together. Its complete-source, lifecycle, independent-evaluation, replay, and invalidation principles are `ADAPT`. Its former AIR ownership of Expression Moment discovery/approval is `REPLACE_BY_CURRENT_OWNERSHIP`. Its Observed AIP compilation remains AIR-owned and is not copied here.

The donor’s `AIR-FR-065` implementation plan is out of scope. Its `AIR-FR-066` handoff invariant is retained: downstream derivative producers receive exact source/moment refs without authority to reinterpret the guest.

### 4.3 AI2 predecessor contract and models

The 436-byte Expression Moment contract is `ADAPT`: it correctly requires exact span, speaker, quote/summary, context, source package, Reaction Receipt refs where relevant, qualities, role potential, route eligibility, epistemic/lifecycle state, approval, and wrong-reading risks; rejected/borderline candidates retain the same source identity and reasons.

The predecessor Python `ExpressionMoment` model is also `ADAPT`, not reuse authority. It enforces approved→approval and rejected→reason, but uses integer milliseconds, free strings, a flat object state, and optional fields that cannot distinguish missing, unknown, restricted, and not applicable. It lacks the current product split, independent Analyst/evaluator evidence, source continuity proof, command/event atomicity, idempotency, selective invalidation, and deterministic identity.

### 4.4 Studio extraction predecessor

The Studio predecessor has useful workflow concepts but cannot be canonical source state:

- `AnchorHitDetector` chooses the first guest transcript segment per contract, caps a float confidence, and changes anchor type by keyword. This is `ARCHIVE_AS_HEURISTIC`; it would create duplicated false hits and ignore complete evidence.
- `ExpressionMomentCandidateCompiler` copies one segment, generates UUIDs/current time, writes free-form emotional-shift and route rationale strings, uses floats, and treats induction-context presence as readiness. This is `REPLACE` for canonical compilation.
- extraction contracts and receipts use mutable lists/maps, wall-clock timestamps, random identity, untyped evaluator strings, and no exact policy/calibration/dependency graph. Their object names are `ADAPT`; their bytes and authority are not reusable.
- the service’s command vocabulary and explicit candidate queue are `ADAPT`, but canonical state must be atomically persisted with events, evidence, receipts, idempotency, and outbox.

### 4.5 Studio review predecessor

The review service demonstrates approve, reject, boundary adjust, split, merge, supersede, route denial, and view-model behavior. These flows are `ADAPT`. The current V2.1 design must correct:

- Studio ownership: Studio projects and commands; IE owns canonical Moment state;
- random/time-based identity and float/millisecond canonical data;
- partial in-memory repositories with separate moment and decision writes;
- implicit “latest” access and insufficient exact ref/hash validation;
- missing tag provenance, upstream draft identities, Reaction Receipt maximum claim, and evidence-bearing `NOT_APPLICABLE`;
- approval/evaluator role separation and source-authority enforcement; and
- replay, cancellation races, late evidence, atomic outbox, descendant invalidation, and historical reproducibility.

The predecessor tests are behavior seeds only. They do not prove current ownership, portability, atomicity, deterministic replay, or cross-product conformance.

### 4.6 Source and amendment predecessors

The interview doctrines supply “Complete Expression Session → Expression Moment → downstream route” evidence and the distinction between capture and editing. Their historical fixed deliverable counts and named render modes do not become current route certification. `SRC-AM-001` corrects Studio to a supervisory projection/command surface and requires HumanResolution capture; its statement that every resolution becomes programming material is constrained by the current ownership matrix: capture/indexing may be automatic, universal promotion is prohibited.

`SRC-AM-002` contributes no claim because it is a deferred missing reference. `SRC-SOURCE-FIRST-001` remains historical only.

## 5. Proposed architecture and workflows

### 5.1 Components

1. **ExpressionGovernanceApplicationService** — validates commands, exact expected case/source-package version/hash, actor authority, and orchestration state.
2. **TagAssertionCompiler** — creates typed planned/observed/inferred/operator-confirmed assertions and derived effective states without promotion.
3. **TagEligibilityResolver** — applies lifecycle, evidence, source authority, applicability, and consumer-profile rules; it never changes a tag.
4. **AnchorHitHunterPort** — proposes source-aligned candidates under an immutable model/program profile and records alternatives/stopping evidence.
5. **MomentHunterPort** — proposes complete moment spans from exact bounded evidence; it has no approval method.
6. **MomentEvidenceAssembler** — resolves TS-INT-002 phrase/word/speaker/audio, TS-INT-003 visual, TS-INT-006 receipt, planned-context, and source-authority refs.
7. **MomentBoundaryValidator** — verifies phrase continuity, rational time, speaker, premise/cause, core turn, and reaction-tail completeness.
8. **MomentQualityEvaluatorPort** — independently evaluates exact dimensions under a pinned profile; numeric measurements cannot decide alone.
9. **MomentAnalystService** — applies deterministic gates plus independent evaluation to produce an attributable `ExpressionMomentDecision`.
10. **MomentApprovalService** — validates exact approval authority and creates the approved canonical `ExpressionMoment` or a typed denial.
11. **ExpressionGovernanceRepositoryPort** — atomically compares and appends cases, records, events, receipts, dependencies, idempotency, invalidations, and outbox.
12. **SourcePackageBindingPort** — asks the Canonical Interview Source Package owner to bind current tag/moment/negative-evidence refs into a successor package.
13. **AIREvidenceHandoffPort** — emits exact approved source evidence and constraints; AIR acknowledges consumption separately.
14. **StudioProjectionPort** — exposes reconstructable views and accepts typed commands; no projection write is canonical.

### 5.2 Register and evolve tag assertions

1. `RegisterTagAssertion` names one source package, tag definition/namespace, provenance kind, exact evidence, asserted value, applicability, confidence/calibration or evidence-bearing N/A, asserting actor/program, source-authority scope, and expected case version/hash.
2. For `PLANNED`, at least one exact AIR/Brief/IAC planned assertion ref is required. Planned assertions cannot cite source observations as proof that the plan occurred.
3. For `OBSERVED`, exact TS-INT-002/003/006 source evidence is required. A model interpretation alone cannot produce observed state.
4. For `INFERRED`, the program/binding/profile, evidence refs, alternatives, uncertainty, and maximum claim are required.
5. For `OPERATOR_CONFIRMED`, the prior assertion, exact confirming evidence, typed operator decision, authority, and HumanResolutionEpisode ref are required. Confirmation does not overwrite the prior assertion.
6. `RejectTagAssertion`, `SupersedeTagAssertion`, or `RevokeTagAssertion` creates a successor decision/edge and preserves the assertion’s original provenance.
7. The repository commits assertion, lifecycle decision, dependency edges, command/event/idempotency, receipt, and outbox atomically.

### 5.3 Discover and validate Anchor Hit candidates

1. `DiscoverAnchorHitCandidates` freezes exact source-package, phrase pack, visual index, Reaction Receipt set, planned-context/tag set, profiles, bindings, authority, and source range.
2. The Hunter retrieves minimum complete context: relevant phrases plus raw words/events when authorized, source continuity, visual evidence only where needed, eligible Reaction Receipts, planned and observed tags as separate sets, and negative examples.
3. The Hunter emits zero or more candidates. Each identifies kind (`FIRST_LINE_MATCH`, `DEPTH_RESPONSE`, `STATE_SHIFT`, `REACTION_LANDING`, `UNEXPECTED_SOURCE_SIGNAL`, `OTHER_GOVERNED`), exact span, evidence/contradiction refs, related planned anchor if any, uncertainty, alternatives, and stopping reason.
4. Deterministic validation rejects unsupported quote text, guessed speaker/time, source-root mismatch, stale refs, out-of-range spans, missing model/profile identity, or a candidate based solely on visual salience/planned text.
5. The Analyst produces `AnchorHitDecision` with `VALIDATED_EVIDENCE`, `BORDERLINE`, `REJECTED`, or `NEEDS_MORE_EVIDENCE`. This does not approve an Expression Moment.

### 5.4 Discover Expression Moment candidates

1. `DiscoverExpressionMomentCandidates` consumes an exact source package and current eligible tag/anchor sets plus the three upstream evidence contracts.
2. The Hunter proposes a core expression range and separately proposes premise/cause, turn/landing, and reaction-tail ranges. It includes rejected alternatives and why the chosen boundary is minimally complete.
3. `MomentEvidenceAssembler` verifies every ref and produces `ExpressionMomentEvidenceBundle`. The bundle carries contradictions and missing modalities rather than filtering them out.
4. `MomentBoundaryValidator` enforces source order, non-overlap/declared overlap, same source root, speaker continuity or explicit speaker transitions, exact quote reconstruction, and required premise/reaction tail under the profile.
5. A catchy core whose complete context reverses, qualifies, weakens, or contests it is denied or widened; quoteability is not a correctness criterion.
6. The result is `PROPOSED`, `OBSERVED`, `BORDERLINE`, or `REJECTED`. Only exact evidence and an Analyst decision can establish `OBSERVED`; a Hunter model cannot self-promote.

### 5.5 Evaluate quality and routeability

The independent evaluator receives the immutable candidate/evidence bundle and a profile. It evaluates:

- source and speaker truth;
- premise/cause completeness;
- core quote/summary fidelity;
- reaction-tail completeness;
- source continuity and temporal boundary validity;
- specificity and identity signal;
- pressure survival and planned–observed divergence;
- emotional/cognitive turn evidence without diagnosis;
- audiovisual usability and limitations;
- tag provenance consistency;
- source-authority scope;
- Primitive applicability/misuse/suppression evidence;
- alternative interpretations and missing evidence; and
- route-by-route technical/evidential eligibility and maximum claim.

Every dimension returns `PASS`, `CONCERNS`, `FAIL`, or evidence-bearing `NOT_APPLICABLE`. A final Analyst verdict is `APPROVABLE`, `BORDERLINE`, `REJECTED`, or `NEEDS_MORE_EVIDENCE`. No threshold is invented here; the immutable profile owns measurement rules, calibration, required human sampling, and aggregation. A high score cannot override a failed source, authority, independence, or context gate.

### 5.6 Approve, reject, or preserve borderline evidence

1. `ApproveExpressionMoment` requires the exact current candidate/evidence/evaluation/Analyst-decision refs, `APPROVABLE`, source-authority eligibility, approval scope, expected aggregate version/hash, and an authorized human approval assertion.
2. Approval emits an immutable canonical `ExpressionMoment` plus `ExpressionMomentApprovalReceipt`; it does not mutate the candidate.
3. `RejectExpressionMomentCandidate` requires typed reasons, responsible failure layer, evidence, future admissibility conditions, and actor/authority. It remains retrievable as negative evidence but is excluded from production-ready queries.
4. `MarkExpressionMomentBorderline` records unresolved dimensions and the exact evidence or decision that could make re-evaluation admissible. Borderline is not approved.
5. `AdjustExpressionMomentBoundary`, `SplitExpressionMoment`, and `MergeExpressionMoments` produce successor candidates and re-run all affected boundary/evaluation gates. They cannot inherit approval automatically.
6. `SupersedeExpressionMoment` names the approved replacement and invalidates dependent current aliases. `RevokeExpressionMoment` records authority/reason/scope; it does not delete historical bytes.

### 5.7 Bind source package and hand off to AIR

1. `BindExpressionGovernanceComponents` requests a successor source package that binds the exact current tag registry, approved/borderline/rejected moment index, and approval/decision receipts.
2. Package binding is distinct from Moment approval. Failure to bind does not rewrite approved evidence; it blocks current package publication.
3. `PublishObservedActivativeEvidenceHandoff` contains exact source package, approved Moment, eligible Reaction Receipt, tag, planned–observed delta, source-authority, wrong-reading-risk, limitation, and decision refs.
4. The handoff explicitly states `semantic_compilation_owner: ACTIVATIVE_INTELLIGENCE_RUNTIME` and `source_evidence_owner: INTERVIEW_EXPRESSION`.
5. AIR consumption acknowledgement is a separate receipt. AIR may compile its `ObservedActivativeIntelligencePack`; it cannot rewrite the IE evidence. IE cannot populate AIR roles, directions, pressures, urges, Edge Product, Primitive/archetype coalition, or transfer semantics.

### 5.8 Correction, late evidence, and selective invalidation

- A TS-INT-002 word/speaker/phrase correction invalidates only tags, anchors, candidates, moments, and handoffs citing affected refs/ranges.
- A TS-INT-003 boundary/keyframe/visual correction invalidates only consumers of affected visual refs; a moment independent of those refs remains valid with proof.
- A TS-INT-006 receipt supersession/invalidation reopens only dependent Moment decisions and AIR handoffs.
- A tag correction reopens only candidates/routeability decisions using that tag.
- A boundary correction reopens the candidate evaluation and approved Moment descendants; it does not alter upstream evidence.
- A source-authority restriction/revocation invalidates newly prohibited use scopes while historical evidence stays reproducible.
- Late evidence creates a successor evidence bundle/candidate/evaluation. It cannot attach invisibly to an approved historical Moment.

Every invalidation record names changed exact ref/field, direct and transitive descendants, unaffected proof, reason, owner, replacement if available, and next admissible action.

### 5.9 State machines

`ExpressionGovernanceCase` states:

`OPEN` → `EVIDENCE_FROZEN` → `DISCOVERY_ACTIVE` → `CANDIDATES_AVAILABLE` → `ANALYSIS_REQUIRED` → (`MOMENTS_RESOLVED` | `NEEDS_MORE_EVIDENCE`) → `PACKAGE_BINDING_REQUIRED` → `HANDOFF_ELIGIBLE`.

Side/terminal states: `CANCELLED`, `FAILED`, `SUPERSEDED`, `INVALIDATED`.

Expression Moment lifecycle transitions:

- `PROPOSED` → `OBSERVED | BORDERLINE | REJECTED`;
- `OBSERVED` → `BORDERLINE | APPROVED | REJECTED`;
- `BORDERLINE` → successor `OBSERVED | APPROVED | REJECTED` after the declared admissibility condition;
- `APPROVED` → `SUPERSEDED | REVOKED`;
- `REJECTED` → successor candidate only; the rejected record stays rejected;
- `SUPERSEDED` and `REVOKED` are terminal for that exact version.

No model callback, file appearance, projection mutation, or route request changes lifecycle state.

### 5.10 Atomicity, idempotency, concurrency, replay, and cancellation

One successful command atomically persists the command record, aggregate version, created artifacts, lifecycle decisions, evaluation/approval receipts, dependency edges, invalidations, idempotency result, events, and outbox intent. State without receipt, receipt without artifact/evidence, approval without Analyst/evaluator evidence, event without command, or handoff without exact Moment refs is corruption and must fail closed.

Identical idempotency key plus identical canonical command hash returns the original receipt. Same key with different bytes fails. Mutation commands compare exact expected aggregate and affected-object versions/hashes; stale commands commit nothing.

Replay resolves exact historical source package, three upstream drafts/contracts as adopted, profiles, bindings, tags, candidates, decisions, approvals, and source authority. It never substitutes current aliases or latest profiles. Cancellation checks occur before expensive Hunter/evaluator work and before commit. A late result after cancellation is quarantined noncanonical evidence; if commit wins, cancellation becomes a successor event.

## 6. Data models, contracts, schemas, and APIs

These are normative logical contracts. This writing prompt creates no schema or release bytes. All models are immutable, reject unknown fields, use nonempty normalized strings, closed enums/tagged unions, integer/rational time, and portable exact refs. No `Any`, open dictionary, bare float, implied default, random ID, or current-time identity is allowed.

### 6.1 Common values

```text
ImmutableRef {
  object_type: governed identifier
  object_id: non-empty identifier
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
  effect_on_eligibility: NONE | LIMITS_CLAIM | BLOCKS_ROUTE | BLOCKS_APPROVAL
}

GovernedMeasure {
  value: canonical decimal string
  scale_id: governed identifier
  calibration_profile_ref: ImmutableRef
  interpretation: governed band
}
```

Canonical time reuses TS-INT-002 `SourceInterval` and TS-INT-003 `FrameCoordinate` by exact adopted interface. This specification creates no parallel seconds/milliseconds locator.

### 6.2 Tag assertion contracts

`TagAssertion` — `ca.interview.tag-assertion/2.1.0-candidate`:

| Field | Type | Owner and validation |
|---|---|---|
| `tag_assertion_id` | deterministic identifier | IE; derived from source scope, tag definition, provenance, evidence, actor/profile, and version |
| `version` | positive integer | IE immutable version |
| `source_package_ref` | `ImmutableRef` | exact TS-INT-001 package root/version |
| `tag_definition_ref` | `ImmutableRef` | owning registry/namespace/version; no free invented tags |
| `asserted_value` | closed typed value owned by definition | unknown fields forbidden |
| `provenance_kind` | `PLANNED | OBSERVED | INFERRED | OPERATOR_CONFIRMED` | IE record; source owner remains in evidence refs |
| `lifecycle_state` | `CURRENT | REJECTED | SUPERSEDED | REVOKED` | IE decision lifecycle |
| `effective_tag_state` | derived closed enum | must match provenance/lifecycle derivation |
| `source_selectors` | ordered TS-INT-002/003/006 selectors or N/A | observed requires nonempty source evidence |
| `planned_assertion_refs` | ordered refs or N/A | required for planned; never copied into observed |
| `evidence_refs` / `contradicting_evidence_refs` | canonical ordered refs | exact source/evaluation evidence |
| `asserting_actor_or_program_ref` | `ImmutableRef` | required identity |
| `inference_profile_ref` | `ImmutableRef | N/A` | required for inferred |
| `confidence` | `GovernedMeasure | N/A` | not authority or lifecycle |
| `applicability` | typed applicability envelope | scope, conditions, evidence, exclusions |
| `source_authority_scope_ref` | `ImmutableRef` | processing/use restrictions |
| `decision_ref` | `ImmutableRef | N/A` | rejection/supersession/revocation/confirmation |
| `supersedes_ref` | `ImmutableRef | N/A` | never in-place correction |
| `content_sha256` | SHA-256 | canonical payload excluding itself |

`TagLifecycleDecision` records prior/new refs, command, actor authority, reason codes, evidence, consumer impact, invalidated descendants, and receipt hash. An inferred tag cannot cite itself as evidence. A planned tag with observed-looking value remains planned.

### 6.3 Anchor Hit contracts

```text
TimestampedAnchorHitCandidate {
  anchor_candidate_id: deterministic identifier
  version: positive integer
  source_package_ref: ImmutableRef
  candidate_kind: FIRST_LINE_MATCH | DEPTH_RESPONSE | STATE_SHIFT | REACTION_LANDING |
                  UNEXPECTED_SOURCE_SIGNAL | OTHER_GOVERNED
  core_source_span: ExpressionSourceSpan
  planned_anchor_ref: ImmutableRef | EvidenceBearingNotApplicable
  transcript_phrase_refs: non-empty canonical ordered ImmutableRef[]
  raw_word_refs: canonical ordered ImmutableRef[]
  audio_event_refs: canonical ordered ImmutableRef[]
  visual_evidence_refs: canonical ordered ImmutableRef[]
  reaction_receipt_refs: canonical ordered ImmutableRef[]
  supporting_tag_refs: canonical ordered ImmutableRef[]
  contradicting_evidence_refs: canonical ordered ImmutableRef[]
  observable_basis: closed typed union
  proposed_by: ImmutableRef
  hunter_profile_ref: ImmutableRef
  confidence: GovernedMeasure | EvidenceBearingNotApplicable
  uncertainty_codes: canonical governed set
  alternative_candidate_refs: canonical ordered ImmutableRef[]
  stopping_evidence_ref: ImmutableRef
  state: PROPOSED | VALIDATED_EVIDENCE | BORDERLINE | REJECTED | SUPERSEDED | REVOKED
  supersedes_ref: ImmutableRef | EvidenceBearingNotApplicable
  content_sha256: sha256
}

AnchorHitDecision {
  decision_id: deterministic identifier
  candidate_ref: ImmutableRef
  analyst_ref: ImmutableRef
  independence_check: PASS | FAIL
  source_truth: PASS | FAIL | INDETERMINATE
  context_integrity: PASS | FAIL | INDETERMINATE
  relation_to_reaction_outcome: SAME_WINDOW_SUPPORT | DIFFERENT_CONCEPT | NOT_APPLICABLE
  verdict: VALIDATED_EVIDENCE | BORDERLINE | REJECTED | NEEDS_MORE_EVIDENCE
  reasons: non-empty governed reason set
  evidence_refs: non-empty canonical ordered ImmutableRef[]
  maximum_supported_claim: governed claim enum
  content_sha256: sha256
}
```

`relation_to_reaction_outcome` prevents conflating this object with `TS-INT-006` `ANCHOR_HIT`.

### 6.4 Source span and evidence bundle

```text
ExpressionSourceSpan {
  source_package_ref: ImmutableRef
  media_ref: ImmutableRef
  phrase_pack_ref: ImmutableRef
  phrase_refs: non-empty source-ordered ImmutableRef[]
  raw_word_refs: non-empty source-ordered ImmutableRef[]
  speaker_assertion_refs: non-empty canonical ordered ImmutableRef[]
  interval: TS-INT-002 SourceInterval
  visual_index_ref: ImmutableRef | EvidenceBearingNotApplicable
  keyframe_or_visual_refs: canonical ordered ImmutableRef[]
  audio_event_refs: canonical ordered ImmutableRef[]
  source_continuity_receipt_ref: ImmutableRef
  exact_text_reconstruction_sha256: sha256
}

ExpressionMomentBoundary {
  premise_or_cause_span: ExpressionSourceSpan
  core_expression_span: ExpressionSourceSpan
  turn_or_landing_span: ExpressionSourceSpan | EvidenceBearingNotApplicable
  reaction_tail_span: ExpressionSourceSpan | EvidenceBearingNotApplicable
  boundary_profile_ref: ImmutableRef
  completeness_evidence_refs: non-empty canonical ordered ImmutableRef[]
  omitted_context_assertion: NO_MATERIAL_CONTEXT_OMITTED | MATERIAL_CONTEXT_PRESENT
  limitations: canonical governed set
  boundary_sha256: sha256
}
```

Ranges may overlap only when the profile explicitly declares semantic roles over the same exact source range. Their combined union must be source-contiguous unless an evidence-bearing discontinuity record explains and blocks/limits approval.

`ExpressionMomentEvidenceBundle` includes the boundary, exact tag/anchor/Reaction Receipt/planned-context refs, source-authority scope, visual/audio/transcript limitations, alternative interpretations, Primitive applicability refs, wrong-reading risks, profile/binding refs, and dependency edges. It cannot embed mutable copies of upstream objects.

### 6.5 Expression Moment candidate

`ExpressionMomentCandidate` — `ca.interview.expression-moment-candidate/2.1.0-candidate`:

| Field | Type | Rule |
|---|---|---|
| `candidate_id` / `version` | deterministic ID / positive int | immutable IE identity |
| `case_ref` / `source_package_ref` | exact refs | one owner scope/root |
| `boundary_ref` | `ImmutableRef` | exact complete boundary |
| `speaker_refs` | non-empty ordered refs | no guessed speaker |
| `quote` | `VerbatimQuote | EvidenceBearingNotApplicable` | must reconstruct exactly when present |
| `semantic_summary` | typed attributed summary or N/A | never represented as verbatim quote; epistemic state required |
| `tag_assertion_refs` | canonical ordered refs | retains each tag state |
| `anchor_hit_refs` | canonical ordered refs | validated/borderline/rejected roles explicit |
| `reaction_receipt_refs` | canonical ordered refs | exact eligible receipts; max claim inherited |
| `evidence_bundle_ref` | `ImmutableRef` | complete evidence/contradiction inventory |
| `quality_assessment_ref` | ref or N/A | absent until evaluated |
| `routeability_assessment_ref` | ref or N/A | absent until evaluated |
| `hunter_actor_or_program_ref` / `hunter_profile_ref` | exact refs | proposal identity |
| `candidate_state` | `PROPOSED | OBSERVED | BORDERLINE | APPROVED | REJECTED | SUPERSEDED | REVOKED` | governed lifecycle |
| `epistemic_state` | `INFERRED | OBSERVED | OPERATOR_CONFIRMED | CONTESTED | RESOLVED` | independent from lifecycle |
| `wrong_reading_risks` | non-empty governed set | cannot be generic notes |
| `source_authority_scope_ref` | exact ref | required |
| `supersedes_ref` / `replacement_ref` | refs or N/A | additive history |
| `content_sha256` | SHA-256 | canonical content identity |

`APPROVED` in a candidate input is rejected; only the approval command/service creates the approved canonical version.

### 6.6 Quality, routeability, Analyst, and approval receipts

```text
MomentDimensionResult {
  dimension: SOURCE_TRUTH | PREMISE_COMPLETENESS | QUOTE_FIDELITY | REACTION_TAIL_COMPLETENESS |
             SOURCE_CONTINUITY | SPECIFICITY | IDENTITY_SIGNAL | PRESSURE_SURVIVAL |
             EMOTIONAL_OR_COGNITIVE_TURN | AUDIOVISUAL_USABILITY | TAG_PROVENANCE |
             SOURCE_AUTHORITY | PRIMITIVE_CONSTRAINT | WRONG_READING_RISK
  verdict: PASS | CONCERNS | FAIL | NOT_APPLICABLE_WITH_EVIDENCE
  measure: GovernedMeasure | EvidenceBearingNotApplicable
  supporting_refs: canonical ordered ImmutableRef[]
  contradicting_refs: canonical ordered ImmutableRef[]
  limitations: canonical governed set
  maximum_claim: governed claim enum
}

RouteEligibilityResult {
  route_profile_id: governed identifier
  route_profile_ref: ImmutableRef
  status: ELIGIBLE | ELIGIBLE_WITH_CONSTRAINTS | NOT_ELIGIBLE | NOT_APPLICABLE_WITH_EVIDENCE
  evidence_refs: canonical ordered ImmutableRef[]
  constraint_codes: canonical governed set
  wrong_reading_risks: canonical governed set
  certification_inferred: false
}

ExpressionMomentEvaluationReceipt {
  evaluation_receipt_id: deterministic identifier
  candidate_ref: ImmutableRef
  evaluator_ref: ImmutableRef
  hunter_ref: ImmutableRef
  independence_check: PASS | FAIL
  profile_ref: ImmutableRef
  dimension_results: canonical map[dimension, MomentDimensionResult]
  route_results: canonical map[route_profile_id, RouteEligibilityResult]
  alternative_interpretation_refs: canonical ordered ImmutableRef[]
  verdict: APPROVABLE | BORDERLINE | REJECTED | NEEDS_MORE_EVIDENCE
  failure_refs: canonical ordered ImmutableRef[]
  maximum_supported_claim: governed claim enum
  content_sha256: sha256
}

ExpressionMomentDecision {
  decision_id: deterministic identifier
  candidate_ref: ImmutableRef
  evaluation_receipt_ref: ImmutableRef
  analyst_ref: ImmutableRef
  decision: OBSERVED | BORDERLINE | REJECTED | NEEDS_MORE_EVIDENCE
  reason_codes: non-empty governed set
  future_admissibility_conditions: canonical ordered typed conditions[]
  responsible_failure_layers: canonical governed set
  HumanResolutionEpisode_ref: ImmutableRef | EvidenceBearingNotApplicable
  content_sha256: sha256
}

ExpressionMomentApprovalReceipt {
  approval_receipt_id: deterministic identifier
  candidate_ref: ImmutableRef
  evidence_bundle_ref: ImmutableRef
  evaluation_receipt_ref: ImmutableRef
  analyst_decision_ref: ImmutableRef
  approver_actor_ref: ImmutableRef
  approval_authority_ref: ImmutableRef
  source_authority_scope_ref: ImmutableRef
  resulting_expression_moment_ref: ImmutableRef
  route_constraints: canonical governed set
  dependency_edges: canonical ordered DependencyEdge[]
  HumanResolutionEpisode_ref: ImmutableRef
  content_sha256: sha256
}
```

The evaluator, Hunter, and final approval workflow roles must pass identity separation. Capability presence does not prove evaluator calibration or certification.

### 6.7 Canonical Expression Moment and negative evidence

`ExpressionMoment` — `ca.interview.expression-moment/2.1.0-candidate` contains:

- deterministic `moment_id`, positive `version`, owner `INTERVIEW_EXPRESSION`, and exact source-package ref;
- immutable boundary, speaker, quote/summary, tag, validated Anchor Hit, eligible Reaction Receipt, evidence-bundle, quality/evaluation, Analyst-decision, and approval refs;
- closed qualities and route eligibility refs rather than free route rationale;
- epistemic state `OBSERVED | OPERATOR_CONFIRMED | CONTESTED | RESOLVED`;
- lifecycle `APPROVED | SUPERSEDED | REVOKED` for canonical approved Moment records;
- source-authority scope, wrong-reading risks, downstream constraints, dependency edges, supersedes/replacement refs, and content hash.

An approved Moment cannot omit the approval receipt or required boundary segments. It cannot carry a route marked ineligible. It does not embed AIR roles, Primitive coalition, Edge Product, Final Script, or Observed AIP fields.

`ExpressionCandidateNegativeEvidence` stores candidate/source identity, state `BORDERLINE | REJECTED | INVALID | INCOMPLETE | LOW_CONFIDENCE | SUPERSEDED`, evidence/evaluation/decision refs, reasons, responsible failure layer, retrieval scope `NEGATIVE_EVIDENCE_ONLY`, future admissibility conditions, source-authority scope, and content hash. Production-ready query APIs must exclude it mechanically.

### 6.8 AIR handoff

```text
ObservedActivativeEvidenceHandoff {
  handoff_id: deterministic identifier
  handoff_version: positive integer
  source_package_ref: ImmutableRef
  approved_expression_moment_refs: non-empty canonical ordered ImmutableRef[]
  reaction_receipt_refs: canonical ordered ImmutableRef[]
  planned_observed_delta_refs: canonical ordered ImmutableRef[]
  current_tag_assertion_refs: canonical ordered ImmutableRef[]
  rejected_or_borderline_evidence_refs: canonical ordered ImmutableRef[]
  source_authority_scope_ref: ImmutableRef
  limitations: canonical governed set
  wrong_reading_risks: canonical governed set
  maximum_supported_claim: governed claim enum
  source_evidence_owner: INTERVIEW_EXPRESSION
  semantic_compilation_owner: ACTIVATIVE_INTELLIGENCE_RUNTIME
  downstream_reinterpretation_authorized: false
  handoff_receipt_ref: ImmutableRef
  supersedes_ref: ImmutableRef | EvidenceBearingNotApplicable
  content_sha256: sha256
}
```

An AIR acknowledgement references the exact handoff; it cannot alter it. Handoff success is not AIR semantic acceptance, derivative consumption authorization, production acceptance, or publication approval.

### 6.9 Aggregate, commands, events, and repository

```text
ExpressionGovernanceCase {
  case_id: deterministic identifier
  version: positive integer
  source_package_ref: ImmutableRef
  current_tag_registry_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_anchor_index_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_moment_index_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_source_package_binding_ref: ImmutableRef | EvidenceBearingNotApplicable
  current_air_handoff_ref: ImmutableRef | EvidenceBearingNotApplicable
  state: governed case state
  supersedes_ref: ImmutableRef | EvidenceBearingNotApplicable
  case_sha256: sha256
}
```

Normative commands:

- `OpenExpressionGovernanceCase`
- `RegisterTagAssertion`
- `ConfirmTagAssertion`
- `RejectTagAssertion`
- `SupersedeTagAssertion`
- `RevokeTagAssertion`
- `DiscoverAnchorHitCandidates`
- `EvaluateAnchorHitCandidate`
- `DiscoverExpressionMomentCandidates`
- `ValidateExpressionMomentBoundary`
- `EvaluateExpressionMomentCandidate`
- `ApplyExpressionMomentAnalystDecision`
- `ApproveExpressionMoment`
- `RejectExpressionMomentCandidate`
- `MarkExpressionMomentBorderline`
- `AdjustExpressionMomentBoundary`
- `SplitExpressionMoment`
- `MergeExpressionMoments`
- `SupersedeExpressionMoment`
- `RevokeExpressionMoment`
- `AttachLateExpressionEvidence`
- `BindExpressionGovernanceComponents`
- `PublishObservedActivativeEvidenceHandoff`
- `InvalidateExpressionGovernanceDescendants`
- `CancelExpressionGovernanceCase`
- `ReplayExpressionGovernanceCase`

Every command includes schema/command ID, idempotency key, source/tenant scope, actor assertion, authority decision, expected case/object version/hash, authority-supplied logical time, canonical payload, and cancellation token where applicable. Generic patch commands are prohibited.

Events mirror successful transitions, including `TagAssertionRegistered`, `TagAssertionConfirmed`, `TagAssertionRejected`, `TagAssertionSuperseded`, `TagAssertionRevoked`, `AnchorHitCandidateProposed`, `AnchorHitCandidateEvaluated`, `ExpressionMomentCandidateProposed`, `ExpressionMomentBoundaryValidated`, `ExpressionMomentCandidateEvaluated`, `ExpressionMomentObserved`, `ExpressionMomentMarkedBorderline`, `ExpressionMomentRejected`, `ExpressionMomentApproved`, `ExpressionMomentSuperseded`, `ExpressionMomentRevoked`, `ExpressionEvidenceAttached`, `ExpressionGovernanceComponentsBound`, `ObservedActivativeEvidenceHandoffPublished`, `ExpressionGovernanceDescendantsInvalidated`, and `ExpressionGovernanceCaseCancelled`.

Repository interface:

```text
load_exact(ref: ImmutableRef) -> ImmutableArtifact
load_case(case_id, version, sha256) -> ExpressionGovernanceCase
commit(bundle: ExpressionGovernanceCommitBundle, expected_case_ref) -> ExpressionGovernanceCommandReceipt
lookup_idempotency(case_id, command_kind, key) -> IdempotencyRecord | null
list_tag_assertions(source_package_ref, effective_states, cursor) -> page[TagAssertion]
list_moment_candidates(source_package_ref, states, cursor) -> page[ExpressionMomentCandidate]
list_production_eligible_moments(source_package_ref, route_profile_ref, cursor) -> page[ExpressionMoment]
list_negative_evidence(source_package_ref, reason_codes, cursor) -> page[ExpressionCandidateNegativeEvidence]
list_descendants(root_refs, edge_types) -> tuple[ImmutableRef, ...]
replay(case_id, through_version) -> ReplayResult
```

Exact reads never fall back to latest. `list_production_eligible_moments` excludes borderline, rejected, invalid, superseded, revoked, stale, source-restricted, and unbound records.

### 6.10 Canonical serialization, compatibility, and invalid examples

Canonical JSON is normalized UTF-8, lexicographically keyed, integer/rational only, with arrays ordered by explicit source/semantic order. `content_sha256` excludes itself. Portable logical/content URIs replace absolute paths.

Semantic compatibility requires preserving exact upstream refs, words/speakers/time, source continuity, visual proposal status, Reaction Receipt maximum claim, tag provenance/lifecycle, candidate/decision/evaluation/approval identity, boundary roles, source authority, wrong-reading risks, applicability, negative evidence, supersession/revocation, and invalidation. Parsing while dropping one of these is incompatible.

Invalid examples:

- `{ "tag": "authority_conflict", "status": "confirmed" }` — no definition, source, prior state, evidence, actor, authority, or lifecycle.
- `{ "quote": "I was free", "start_ms": 4200, "confidence": 0.94 }` — no rational source interval, phrase/word/speaker refs, context, profile, or scale.
- `{ "keyframe": "frame-91", "importance": "expression_moment" }` — forbidden technical-to-semantic promotion.
- `{ "reaction_outcome": "ANCHOR_HIT", "moment_state": "APPROVED" }` — Reaction outcome does not approve a Moment.
- `{ "planned_tag": "vulnerability", "observed_tag": "vulnerability" }` — copied label without exact distinct planned/observed evidence.
- `{ "reaction_tail": null }` — cannot distinguish unavailable, inapplicable, restricted, not inspected, or missing-required evidence.
- a Hunter-generated candidate whose evaluator/approver identity is the Hunter — fails independence/authority.
- a rejected candidate returned by the production-eligible query — repository conformance failure.
- an IE object containing AIR-owned confirmed roles, Edge Product, Primitive coalition, or Observed AIP semantics — ownership violation.

## 7. Implementation stages and exact target paths

These are future adoption targets, not files created or authorized by this prompt.

### 7.1 Stage 0 — source, contract, and profile lock

- Future path: `06_INTERVIEW_EXPRESSION/development-capsules/TS-INT-004/SOURCE_LOCK.yaml`.
- Lock this accepted spec, all eight FRs/five Stories, source dispositions, three upstream accepted/adopted specs, required source bytes, Primitive bytes, source authority, evaluator profiles, and exact implementation allowlist.
- Gate: ratified/adopted authority, independent spec acceptance, and bounded Development Capsule.
- Maps: every FR; AC-01, AC-02, AC-21, AC-24.

### 7.2 Stage 1 — immutable domain models and canonicalization

- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/domain/tag_assertion.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/domain/anchor_hit.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/domain/expression_moment.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/domain/expression_governance_case.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/canonical/expression_governance_json.py`
- Maps: FR-127, FR-130, FR-131, AIR-FR-061 through AIR-FR-064; AC-03 through AC-15.

### 7.3 Stage 2 — application services and ports

- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/services/tag_assertion_service.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/services/anchor_hit_service.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/services/expression_moment_service.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/ports/moment_hunter.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/ports/moment_evaluator.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/ports/source_evidence.py`
- Maps: FR-127, FR-130, AIR-FR-061 through AIR-FR-064; AC-04 through AC-14, AC-18.

### 7.4 Stage 3 — repository, dependency, replay, and outbox

- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/repositories/expression_governance.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/services/expression_dependency_service.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/services/expression_replay_service.py`
- Maps: FR-131, AIR-FR-064; AC-15 through AC-20.

### 7.5 Stage 4 — upstream and cross-product adapters

- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/adapters/transcript_evidence.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/adapters/visual_index_evidence.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/adapters/reaction_receipt_evidence.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/adapters/source_package_binding.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/adapters/air_observed_evidence_handoff.py`
- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/projections/studio_expression_review.py`
- Maps: AIR-FR-061, AIR-FR-062, AIR-FR-066, FR-130; AC-01, AC-05 through AC-09, AC-21, AC-22.

### 7.6 Stage 5 — migration and fixtures

- `06_INTERVIEW_EXPRESSION/src/cmf_interview_expression/migrations/studio_expression_moment_v1_to_v2_1.py`
- `06_INTERVIEW_EXPRESSION/tests/fixtures/expression_governance/`
- Migration creates new immutable artifacts and receipts; it never edits Studio records or guesses missing provenance/classification.
- Maps: FR-127, FR-130, FR-131; AC-17 through AC-20, AC-23.

### 7.7 Stage 6 — exact future test paths

- `06_INTERVIEW_EXPRESSION/tests/unit/test_tag_assertion.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_anchor_hit_governance.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_expression_moment_boundary.py`
- `06_INTERVIEW_EXPRESSION/tests/unit/test_expression_moment_lifecycle.py`
- `06_INTERVIEW_EXPRESSION/tests/contract/test_expression_governance_contracts.py`
- `06_INTERVIEW_EXPRESSION/tests/contract/test_air_observed_evidence_handoff.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_expression_moment_discovery.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_expression_moment_approval.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_expression_governance_repository.py`
- `06_INTERVIEW_EXPRESSION/tests/integration/test_expression_governance_replay.py`
- `06_INTERVIEW_EXPRESSION/tests/architecture/test_product_ownership_boundaries.py`
- `06_INTERVIEW_EXPRESSION/tests/migration/test_studio_expression_moment_migration.py`
- `06_INTERVIEW_EXPRESSION/tests/cleanroom/test_expression_governance_portability.py`

No Stage may begin until a later accepted/adopted spec and Development Capsule authorize its exact paths.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures

| Code | Responsible owner | Meaning | Next admissible action |
|---|---|---|---|
| `EXPR_SOURCE_REF_MISSING_OR_STALE` | source evidence owner | exact package/phrase/visual/receipt ref unavailable or drifted | obtain exact current or historical ref; never use latest |
| `EXPR_TAG_PROVENANCE_INVALID` | Interview Expression | evidence cannot support requested provenance kind | register corrected successor assertion |
| `EXPR_TAG_STATE_COLLAPSE` | adapter/consumer | planned/inferred/rejected/superseded state would be flattened | reject adapter and preserve axes |
| `EXPR_ANCHOR_REACTION_CONFLATION` | Interview Expression | timestamped anchor candidate confused with Reaction Receipt outcome | create distinct evidence relation |
| `EXPR_BOUNDARY_INCOMPLETE` | Interview Expression | premise/cause or required reaction tail missing | widen boundary or mark borderline/rejected |
| `EXPR_QUOTE_RECONSTRUCTION_FAILED` | transcript evidence owner | quote does not reconstruct from exact words | correct upstream evidence or candidate |
| `EXPR_VISUAL_SEMANTIC_PROMOTION` | Hunter/adapter | technical visual salience used as meaning | reject candidate input |
| `EXPR_REACTION_CLAIM_EXCEEDED` | Hunter/Analyst | candidate exceeds receipt maximum claim | constrain claim or collect evidence |
| `EXPR_HUNTER_SELF_APPROVAL` | approval service | Hunter/evaluator/approver separation fails | route to independent Analyst/authorized approver |
| `EXPR_SOURCE_AUTHORITY_DENIED` | operator/source authority | requested use outside declared scope | deny route or obtain new scoped declaration |
| `EXPR_EVALUATOR_PROFILE_UNSUPPORTED` | evaluator owner | required dimension/calibration unavailable | mark needs evidence; no silent fallback |
| `EXPR_NOT_APPLICABLE_UNEVIDENCED` | producer | N/A lacks reason/profile/evidence/effect | reject record |
| `EXPR_STALE_EXPECTED_VERSION` | command caller | optimistic concurrency mismatch | reload and issue a new command |
| `EXPR_IDEMPOTENCY_COLLISION` | command caller | same key with different command hash | issue a new key after reconciliation |
| `EXPR_ATOMIC_COMMIT_FAILED` | repository | complete state/receipt/outbox bundle not committed | roll back all visibility and retry exact command |
| `EXPR_HANDOFF_OWNERSHIP_VIOLATION` | IE/AIR adapter | IE compiles AIR semantics or AIR rewrites IE evidence | reject handoff/acknowledgement |
| `EXPR_DEPENDENCY_INVALIDATION_INCOMPLETE` | dependency service | affected descendant left current | quarantine aliases and recompute scope |
| `EXPR_REPLAY_DIVERGENCE` | implementation owner | historical exact inputs do not reproduce hash | block current release and retain evidence |

Generic “validation failed” is not sufficient. A failure record includes exact failed object/ref, layer, owner, evidence, frozen upstreams, retryability, affected descendants, and next action.

### 8.2 Retry versus semantic repair

Retry is allowed only for explicitly transient storage/transport/provider failures and must reuse the same canonical command/idempotency key. Missing source evidence, unsupported provenance, incomplete boundary, evaluator disagreement, source-authority denial, or wrong-reading risk is not transient. It requires a new evidence/correction/decision command and immutable successor.

No fallback model or profile may silently replace the pinned Hunter/evaluator. A fallback binding is eligible only when the governing profile declares semantic compatibility and records a distinct binding/receipt.

### 8.3 Atomic rollback and partial results

Repository transaction failure leaves no new current state, artifact, decision, receipt, idempotency result, or outbox event visible. Expensive Hunter/evaluator proposals may be retained in a quarantined run scope with explicit noncanonical status and retention/source-authority enforcement. They cannot be queried as candidates or negative evidence until an accepted command binds them.

Rollback of implementation/service deployment restores the last known-good binding/profile and current alias while preserving artifacts created under the failed version. It never rewrites or deletes historical evidence.

### 8.4 Cancellation and late evidence

Cancellation is receipt-backed. If cancellation wins before commit, the command records `CANCELLED` with no accepted result. A late Hunter/evaluator result is quarantined and cannot bind automatically. If commit wins, cancellation is a successor lifecycle event. Late source evidence uses `AttachLateExpressionEvidence` to create a new bundle/candidate/evaluation; it does not mutate an approved Moment.

### 8.5 Migration and compatibility

Studio and AI2 predecessor records migrate through a new immutable `MigrationAssessment`:

- exact source record path/ref/hash and owner are required;
- UUID/time/free-score values remain historical metadata, not canonical identity;
- missing tag provenance, rational time, source continuity, evaluator independence, authority, reaction tail, or source scope is marked unavailable or blocks migration;
- no planned/observed classification is guessed;
- an approved predecessor cannot become current approved V2.1 state without a current source/evidence/authority/approval assessment;
- rejected/borderline records remain negative evidence with source scope;
- every output names the source predecessor and adapter version/hash.

Semantic compatibility, not parsing, governs adapters. Deprecated versions remain reproducible for historical delegations; current jobs pin exact accepted versions. No local schema fork is permitted.

### 8.6 Selective invalidation

Dependency edges include `USES_WORD`, `USES_PHRASE`, `USES_AUDIO_EVENT`, `USES_VISUAL_REF`, `USES_REACTION_RECEIPT`, `USES_TAG`, `USES_ANCHOR`, `USES_BOUNDARY`, `USES_EVALUATION`, `APPROVED_BY`, `BOUND_IN_SOURCE_PACKAGE`, and `HANDED_TO_AIR`. Invalidation traverses only typed edges from exact changed refs. Unrelated Moments remain current only with an explicit unaffected proof.

Approved historical artifacts remain readable after supersession/revocation. Current aliases and production-eligible queries exclude stale descendants. AIR handoffs derived from stale/revoked Moments are invalidated; AIR decides how its own semantic descendants are repaired under its authority.

### 8.7 Replay and historical reproduction

Replay takes exact case/version/hash and reconstructs commands, events, three upstream evidence versions, profiles/bindings, source authority, decisions, HumanResolution refs, package binding, and handoff. It compares canonical bytes, hashes, event order, dependency graph, and receipts. Current aliases, environment state, random/time, filesystem order, and network/provider freshness are excluded.

When an external model output cannot be regenerated, replay uses the exact stored proposal bytes and proves deterministic admission/evaluation/decision behavior. It must not call a newer model and claim equivalence.

### 8.8 Recovery and degraded behavior

- Transcript/visual/Reaction Receipt evidence unavailable: affected discovery blocks; no reconstruction.
- Visual evidence legitimately unavailable under profile: evidence-bearing N/A can permit transcript/audio/receipt-based review with a limited claim.
- Reaction Receipt absent for an approved profile requiring it: approval blocks.
- Evaluator unavailable: deterministic gates may run, but candidate remains `NEEDS_MORE_EVIDENCE`; no self-evaluation fallback.
- Studio unavailable: canonical API commands can continue if authorized; projections rebuild later from events.
- AIR unavailable: IE can preserve approved source evidence; handoff/acknowledgement waits without changing Moment status.

### 8.9 Observability, privacy, and security

Metrics use nonsemantic labels and governed cardinality: command/result counts, stage latency, candidate state, denial codes, tag provenance/lifecycle, boundary expansion, evaluator disagreement, stale command, invalidation scope, replay divergence, handoff acknowledgement, and atomic rollback. Logs contain command/correlation IDs, exact ref hashes, profile/binding IDs, actor authorization decision, and failure codes—not unrestricted transcript text, identity DNA, credentials, raw media, or sensitive observations.

Audit events are immutable and source-scope aware. Access control separates Hunter, Analyst, approver, source-authority operator, projection user, and AIR consumer. Technical security protects artifacts, secrets, tenant boundaries, and audit integrity; it does not invent creative approval authority.

## 9. Behavior-specific acceptance criteria

### AC-01 — Exact draft and source inputs

**Governs:** all FRs and Stories. **Given** the three upstream specs and required unique/authority sources, **when** writing/implementation admission runs, **then** exact paths, bytes, hashes, states, source dispositions, and `DRAFT_DEPENDENCY_NOT_ACCEPTED` labels match. A drifted TS-INT-002 hash or missing required source blocks. **Evidence:** source-lock and draft-dependency receipts. **Layer:** contract/clean-room.

### AC-02 — No ownership collapse

**Governs:** AIR-FR-066, AIR-ST-11.03. **Given** an approved Moment handoff, **when** IE publishes it, **then** IE owns source evidence and AIR owns Observed AIP semantic compilation. An IE handoff containing compiled roles/Edge Product/Primitive coalition or an AIR acknowledgement rewriting the Moment fails. **Evidence:** ownership conformance receipt. **Layer:** architecture/contract.

### AC-03 — Planned tag remains planned

**Governs:** FR-127, ST-02.01. **Given** a planned `authority_conflict` tag and an unrelated observed answer, **when** eligibility resolves, **then** the planned tag stays `PLANNED` and cannot drive an observed route without a separate observed/confirmed successor. Copying the planned value into observed state fails. **Evidence:** tag provenance graph and exclusion receipt. **Layer:** unit/integration.

### AC-04 — Inferred tag cannot self-confirm

**Governs:** FR-127, ST-02.01. **Given** a model-inferred tag with high score but no source span or operator decision, **when** confirmation is requested, **then** confirmation is denied and inference remains explicit. Score-only promotion fails. **Evidence:** typed denial and immutable original assertion. **Layer:** unit/adversarial.

### AC-05 — Rejected and superseded tag history

**Governs:** FR-127, FR-131. **Given** a rejected tag later replaced by a supported assertion, **when** supersession occurs, **then** both exact records remain, original provenance is retained, current queries return only eligible successor state, and negative-evidence queries can retrieve the rejected record. In-place status mutation fails. **Evidence:** lifecycle/replay receipt. **Layer:** repository/integration.

### AC-06 — Anchor Hit concepts do not conflate

**Governs:** FR-130, AIR-FR-061, ST-02.03. **Given** a Reaction Receipt outcome `ANCHOR_HIT`, **when** an Anchor Hit candidate is assembled, **then** the receipt is supporting evidence and a separate `TimestampedAnchorHitCandidate`/decision is required. Auto-creating an approved Moment from the outcome fails. **Evidence:** relation record and denial fixture. **Layer:** contract/integration.

### AC-07 — Exact phrase and speaker evidence

**Governs:** AIR-FR-061, FR-130, AIR-ST-11.01. **Given** a candidate quote, **when** validation runs, **then** ordered phrase/raw-word/speaker refs reconstruct exact text and rational source time. Guessed speaker, float-only timestamp, or normalized-away hesitation fails. **Evidence:** reconstruction proof hash. **Layer:** integration.

### AC-08 — Visual salience remains nonsemantic

**Governs:** AIR-FR-061, FR-130. **Given** a striking keyframe marked `EXPRESSION_SIGNAL_CANDIDATE`, **when** no corroborating transcript/audio/receipt evidence supports a Moment, **then** the candidate stays nonsemantic or is rejected. Promoting detector salience as meaning fails. **Evidence:** visual-reference relation and Analyst receipt. **Layer:** architecture/adversarial.

### AC-09 — Reaction Receipt maximum claim is inherited

**Governs:** AIR-FR-061 through AIR-FR-063, FR-130. **Given** a receipt with `NEEDS_MORE_EVIDENCE` or `NO_EXPRESSION_MOMENT_PROMOTION`, **when** Moment evaluation runs, **then** the candidate cannot exceed that constraint without an exact successor receipt. Ignoring the maximum claim fails. **Evidence:** receipt dependency and blocker. **Layer:** integration.

### AC-10 — Premise and reaction tail survive extraction

**Governs:** AIR-FR-062, AIR-ST-11.01, PRM-VOC-009. **Given** a catchy phrase whose qualifier and reaction tail change its meaning, **when** boundary validation runs, **then** the boundary widens to preserve the smallest complete source context or blocks approval. Shortest-quote extraction fails. **Evidence:** before/after boundary proof and source reconstruction. **Layer:** integration/reference slice.

### AC-11 — Source-backed felt truth is not manufactured

**Governs:** AIR-FR-063, AIR-ST-11.02, PRM-VSG-021. **Given** a real hesitation/micro-expression and a cleaner substitute frame, **when** evidence review runs, **then** the exact source friction remains visible with uncertainty; no staged or generated evidence replaces it. Manufactured messiness fails. **Evidence:** exact visual/audio refs and evaluation. **Layer:** adversarial/integration.

### AC-12 — Tension/release remains source-true

**Governs:** AIR-FR-063, AIR-ST-11.03, PRM-PRS-002. **Given** a source with tension but no actual landing, **when** Moment quality is evaluated, **then** the missing release remains a limitation/borderline reason. Inventing a payoff or cutting before the unresolved tension is disclosed fails. **Evidence:** source spans, alternative interpretation, and verdict. **Layer:** evaluator/reference slice.

### AC-13 — Complete routeability evaluation

**Governs:** AIR-FR-063, AIR-ST-11.02. **Given** declared route profiles, **when** the evaluator runs, **then** every applicable route has exact eligibility, constraints, evidence, wrong-reading risks, and no certification inference. A bare score or omitted unsupported route fails. **Evidence:** routeability receipt. **Layer:** contract/evaluator.

### AC-14 — Hunter cannot approve

**Governs:** FR-130, ST-02.03, all AIR Stories. **Given** a Hunter-proposed candidate, **when** the same workflow identity attempts evaluation or approval, **then** independence/authority checks reject it. A Hunter-set `APPROVED` field fails schema validation. **Evidence:** role-separation denial. **Layer:** unit/security/architecture.

### AC-15 — Governed approval produces immutable Moment

**Governs:** FR-130, AIR-FR-064. **Given** an `APPROVABLE` independently evaluated candidate and authorized approver, **when** approval commits, **then** candidate, evaluation, Analyst decision, approved Moment, approval receipt, dependencies, HumanResolution ref, event, idempotency, and outbox appear atomically. Any missing pair fails and leaves nothing current. **Evidence:** atomic commit receipt. **Layer:** repository/integration.

### AC-16 — Borderline and rejected evidence remains excluded and learnable

**Governs:** FR-131, ST-02.03. **Given** rejected/borderline candidates, **when** production-ready and negative-evidence retrieval run, **then** production query excludes them while authorized negative-evidence query returns exact reasons, source scope, failure layer, and future admissibility. Deletion or accidental routing fails. **Evidence:** dual-query conformance receipt. **Layer:** repository/integration.

### AC-17 — Boundary correction does not inherit approval

**Governs:** AIR-FR-062, AIR-FR-064, FR-130. **Given** an approved Moment whose boundary is adjusted, split, or merged, **when** the command succeeds, **then** successor candidates re-run evidence/evaluation/approval and the prior Moment becomes historical/superseded only through an authorized replacement. Copying approval fails. **Evidence:** successor graph and re-evaluation receipts. **Layer:** integration.

### AC-18 — Evidence-bearing `NOT_APPLICABLE`

**Governs:** AIR-FR-061 through AIR-FR-063, FR-127. **Given** imported source with no planned IAC or source with no relevant visual evidence, **when** compilation runs, **then** N/A carries reason, profile, method/actor, inspected evidence, and eligibility effect. Null or empty default fails. **Evidence:** positive/negative schema fixtures. **Layer:** unit/contract.

### AC-19 — Idempotency and stale concurrency

**Governs:** AIR-FR-064, FR-131. **Given** an identical approval command/key, **when** retried, **then** the original receipt returns without duplicate state. Same key/different bytes or stale expected case/moment hash commits nothing. **Evidence:** idempotency/concurrency test. **Layer:** repository.

### AC-20 — Selective invalidation and historical replay

**Governs:** AIR-FR-064, FR-131, every Story recovery clause. **Given** one phrase, visual ref, Reaction Receipt, or tag is superseded, **when** dependency analysis runs, **then** only citing descendants become stale, unrelated accepted work remains current with proof, and old exact path replays byte-identically. Global invalidation or historical rewrite fails. **Evidence:** invalidation graph and replay digest. **Layer:** integration/replay.

### AC-21 — AIR handoff preserves source authority

**Governs:** AIR-FR-066, AIR-ST-11.03. **Given** approved moments and eligible receipt/tag evidence, **when** IE emits the handoff, **then** exact source/package/moment versions/hashes, scope, limitations, risks, maximum claim, and ownership flags survive. A derivative producer cannot reinterpret or mutate the guest’s meaning. **Evidence:** producer/consumer conformance receipt. **Layer:** contract/integration.

### AC-22 — Source package binding and AIR acknowledgement remain distinct

**Governs:** AIR-FR-066, FR-130. **Given** an approved Moment, **when** package binding succeeds but AIR acknowledgement is pending, **then** the Moment remains approved/source-bound and handoff status remains pending. Binding is not semantic acceptance or production authorization. **Evidence:** separate receipts/state projection. **Layer:** integration.

### AC-23 — Migration never invents provenance

**Governs:** FR-127, FR-130, FR-131. **Given** a Studio v1 candidate with UUID, float score, and missing reaction tail/provenance, **when** migration runs, **then** a new artifact records exact predecessor, unavailable fields, and blocked/limited state; it is not promoted to observed/approved. Guessed classification fails. **Evidence:** migration assessment/receipt. **Layer:** migration.

### AC-24 — Claim ceiling and portability

**Governs:** all FRs/Stories. **Given** a clean machine/process, **when** canonical compilation/replay runs with exact inputs, **then** bytes/hashes match without absolute paths, clock, random, environment, filesystem order, or hidden local state. Receipts remain `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, build false. A production/certification claim fails. **Evidence:** clean-room reproducibility and claim scan. **Layer:** clean-room/architecture.

## 10. Testing and completion evidence

### 10.1 Unit and property tests

`tests/unit/test_tag_assertion.py` SHALL cover every provenance/lifecycle/effective-state combination, invalid promotions, confirmation successor, tag-definition typing, evidence-bearing N/A, and canonical hash stability. Property tests generate insertion-order/environment/time/random variations and require identical canonical bytes.

`tests/unit/test_anchor_hit_governance.py` SHALL cover candidate kinds, planned-anchor relation, Reaction `ANCHOR_HIT` distinction, alternatives/stopping evidence, source span validation, and Hunter/Analyst separation.

`tests/unit/test_expression_moment_boundary.py` SHALL cover exact quote reconstruction, premise/core/turn/tail roles, overlapping/discontinuous ranges, qualifier reversal, missing tail, speaker transition, rational time, and source continuity.

`tests/unit/test_expression_moment_lifecycle.py` SHALL cover every allowed/forbidden transition, approval prerequisites, rejection/borderline preservation, split/merge/boundary successor behavior, supersession, revocation, and exact-read semantics.

### 10.2 Contract and schema tests

`tests/contract/test_expression_governance_contracts.py` SHALL validate positive/negative examples for every logical model, reject unknown fields/floats/paths/null-as-N/A, require exact refs/hashes/owners, and prove no duplicate local TS-INT-002/003/006 schema.

`tests/contract/test_air_observed_evidence_handoff.py` SHALL prove producer/consumer preservation of every handoff field, IE/AIR owner flags, source authority, maximum claim, rejected/borderline evidence, acknowledgement separation, and prohibition on AIR evidence mutation or IE semantic compilation.

### 10.3 Discovery and Analyst integration tests

`tests/integration/test_expression_moment_discovery.py` SHALL use:

- a complete phrase/audio/visual/receipt candidate with premise and reaction tail;
- a catchy quote whose omitted qualifier reverses meaning;
- a planned tag contradicted by observed evidence;
- a visual-only salience proposal;
- an `ANCHOR_HIT` receipt that still lacks Moment context;
- imported source with absent planning;
- mixed speaker/overlap/low-confidence evidence; and
- no-candidate stopping evidence.

The portfolio must preserve alternatives, contradictions, failures, and negative examples.

`tests/integration/test_expression_moment_approval.py` SHALL cover independent evaluation, authorization, atomic approval, Hunter self-approval denial, borderline/rejection, source restriction, route constraints, HumanResolution ref, split/merge/re-evaluation, supersession, and revocation.

### 10.4 Repository, replay, cancellation, and recovery tests

`tests/integration/test_expression_governance_repository.py` SHALL inject failure after each commit member and prove no state/receipt/artifact/event/idempotency/outbox mismatch. It SHALL test duplicate command, idempotency collision, stale expected version/hash, concurrent approval, negative-evidence exclusion, pagination stability, and exact-not-latest reads.

`tests/integration/test_expression_governance_replay.py` SHALL reproduce complete accepted, rejected, borderline, superseded, revoked, cancelled, and late-evidence histories; preserve stored model proposals; and prove typed selective invalidation for each upstream edge.

### 10.5 Architecture and product-sovereignty tests

`tests/architecture/test_product_ownership_boundaries.py` SHALL inspect imports/contracts and fail if:

- IE defines local transcript/visual/Reaction Receipt authority;
- IE compiles Observed AIP/Primitive coalition/Edge Product/Final Script;
- AIR mutates IE source evidence;
- Studio writes canonical state;
- Pipeline/VAE/Builder/Delegation approves a Moment;
- a Hunter exposes an approval method; or
- a projection/model/provider callback commits lifecycle state directly.

### 10.6 Primitive and CBAR fixtures

Fixtures SHALL bind exact hashes for `PRM-VOC-009`, `PRM-VSG-021`, and `PRM-PRS-002` and test at least one activation, misuse/conflict, and suppression/inapplicability case. They must verify source-grounded evidence preservation without treating IE as semantic Primitive authority.

CBAR fixtures SHALL demonstrate that optimization for quote length, model confidence, visual polish, or fast routing cannot bypass source/context/approval gates and cannot propagate false meaning to the archetype router or derivative job compiler.

### 10.7 Migration and brownfield tests

`tests/migration/test_studio_expression_moment_migration.py` SHALL cover predecessor UUID/current-time/float fields, missing provenance, incomplete boundary, source restrictions, approved/rejected records, and duplicate source occurrences. It must create new immutable artifacts, preserve exact predecessor hashes, label unavailable fields, and never guess state.

Existing Studio tests become behavior fixtures after review; their current PASS cannot prove V2.1 ownership, deterministic identity, atomicity, or replay.

### 10.8 Clean-room, security, and portability tests

`tests/cleanroom/test_expression_governance_portability.py` SHALL run from two roots and fresh processes with varied locale/timezone/environment/dictionary insertion/filesystem enumeration/random seeds. Expected spec artifacts must be byte-identical, contain no drive/UNC/temp/user paths, and have no unstated source files.

Security tests cover source-scope/tenant isolation, role separation, command authorization, restricted transcript/log redaction, idempotency abuse, stale replay, and outbox integrity. Technical security does not add creative approval authority.

### 10.9 Imported-interview reference-slice proof

The later reference slice SHALL freeze exact hashes and prove:

`Canonical Interview Source Package` → TS-INT-002 phrase/word/speaker/audio refs → TS-INT-003 source visual refs → TS-INT-006 Reaction Receipt/limitations → tag/Anchor Hit candidates → complete Moment evidence/boundary → independent Analyst/evaluator → approved or rejected/borderline Moment → source-package binding → IE-to-AIR evidence handoff → AIR acknowledgement.

The proof SHALL also show one qualifier-reversal denial, one missing-tail borderline decision, one visual-only false positive, one rejected negative-evidence retrieval, one source-authority restriction, one selective invalidation, one historical replay, and one HumanResolution correction. It stops before AIR semantic compilation and grants no Format 02, VAE Stage 5, production, or publication authority.

### 10.10 Required later completion artifacts and handoff

A later authorized build would require, at minimum:

- exact Development Capsule and source lock;
- generated contract/schema manifests from accepted spec bytes;
- unit/contract/integration/architecture/migration/replay/security/clean-room results;
- Hunter and evaluator implementation/model/profile bindings;
- independent evaluator calibration evidence;
- source-package and AIR consumer conformance receipts;
- migration and rollback receipts;
- affected regression evidence;
- Build Receipt with exact artifact hashes and maximum supported claim; and
- explicit statement that production eligibility and certification remain false unless separately proven.

This writer issues none of those artifacts. The next lifecycle action is independent audit by a different agent. The spec remains `WRITTEN_PENDING_AUDIT`, authority `CANDIDATE_NOT_CURRENT`, specification work authorized, build authority false, and later acceptance ceiling `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
