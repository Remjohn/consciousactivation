---
type: technical_specification
spec_id: TS-AIR-013
title: Campaign Activation, Freshness, and Audience Reaction
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
writing_wave: 3
controlling_frs:
  - AIR-FR-073
  - AIR-FR-074
  - AIR-FR-075
  - AIR-FR-076
  - AIR-FR-077
  - AIR-FR-078
controlling_stories:
  - AIR-ST-13.01
  - AIR-ST-13.02
  - AIR-ST-13.03
upstream_draft_dependencies:
  - spec_id: TS-AIR-002
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-003
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: ce9ac739346789d115ada80c44b568c28e61ce68f0ae99bb55b0962c875d430c
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-005
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 5dcf631efc4f68f40edd0991ca3ae4be9073da68aa441c52d37e874e70a43e49
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-013 - Campaign Activation, Freshness, and Audience Reaction

This candidate specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. It preserves the substantive F13 design of the hash-locked full draft while applying its governed disposition `AMEND_TO_CURRENT_AUTHORITY`. Under the current candidate ownership package, AIR owns campaign semantic meaning, freshness interpretation, fatigue inference, and additive semantic revision; Atomic Harness Pipeline consumes that meaning to compile and execute operational batch/jobs and to capture publishing observations; publishing adapters are evidence producers, not independent semantic authorities; Independent Evaluation owns evaluation receipts; Studio projects state and captures attributable human resolutions. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`.

`TS-AIR-002`, `TS-AIR-003`, and `TS-AIR-005` are admitted solely as exact hash-pinned `WRITTEN_PENDING_AUDIT` writing interfaces and carry `DRAFT_DEPENDENCY_NOT_ACCEPTED`. This specification does not represent their details as ratified or accepted authority. A byte change in any pinned draft reopens sections 3, 5, 6, 8, 9, and 10 for recorded downstream revision impact. This document does not audit or accept itself, authorize implementation, issue a Development Capsule, create shared release bytes, or confer build, production, publication, provider, or certification authority.

## 1. Files and authorities read

### Authority, reconciliation, packet, and status inputs

| Input | State | SHA-256 | Specific use |
|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | current registry | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | Constitution V1.1 remains current until a governed amendment. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | Rich Identity, Context, Resonance, Matrix, role/tension, reaction, visual, format, and wrong-reading lineage cannot be flattened by a campaign. |
| `.../CURRENT_AUTHORITY.md` | draft for human ratification | `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Candidate authority is not current and implementation requires a separate authorized capsule. |
| `.../doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `CANDIDATE_NOT_CURRENT` | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Campaign coordination, freshness/fatigue, counteractivation/dose, semantic ownership, immutable evidence, Final Script, and evaluation laws. |
| `.../prd/features/F13-campaign-activation-freshness-and-audience-reaction.md` | `2.1.0-draft` | `87ead22b946615750776f892843b4dd6c6a85a642034fe623686e9cc7def9e6c` | Controls AIR-FR-073 through AIR-FR-078, feature entry/terminal state, invariants, denials, sources, and active Primitives. |
| `.../planning/EPICS_AND_VERTICAL_STORIES.md` | candidate planning | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-EP-10 and AIR-ST-13.01 through 13.03 acceptance, adversarial, recovery, CBAR, and evidence requirements. |
| `.../specs/TS-AIR-013-campaign-activation-freshness-and-audience-reaction.md` | full draft pending ratification | `78aa6543d657395dfc5b94074e948b46506d88f73a0b06787c3296a344281928` | Full substantive draft amended to current Program Control ownership, exact dependencies, and V3.3 lifecycle/claim controls. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SPEC_DISPOSITION_REPORT.md` | current reconciliation | `86852420631241ce6341a04d258f476473d0490274bb4e22675301cb02c13241` | Requires `AMEND_TO_CURRENT_AUTHORITY`; accepted AIR specs are not rewritten for uniformity. |
| `.../CANONICAL_SPEC_LEDGER.csv` | current queue | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | Freezes title, AIR owner, exact path, Gate B, lane, Wave 3, and claim ceiling. |
| `.../CANONICAL_FR_LEDGER.csv` | current reconciliation | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | Assigns each active F13 requirement to one AIR Story and this specification. |
| `.../FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | current reconciliation | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | Preserves exact FR language, authority, source IDs, gates, and evidence ceilings. |
| `.../RECONCILIATION_INPUT_HASH_LOCK.yaml` | locked | `ea28bcab299e74adb87f3bce8ab8a1d20093d4d8699e9e10c5d387383363c456` | Locks the admitted archives and source-draft bytes. |
| `.../SOURCE_DISPOSITION_LEDGER.yaml` | validated | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Classifies all three F13 sources as available `REQUIRED_UNIQUE_EVIDENCE`. |
| `.../SOURCE_GAP_NOTICE.yaml` | current reconciliation | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | No unavailable optional/deferred source supports a claim in this specification. |
| `.../V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending ratification | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | AIR compiles campaign meaning; Pipeline executes; Studio projects/corrects; Delegation transports; evaluators remain independent. |
| `.../V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending ratification | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Assigns Activation Transfer and Audience/Campaign Program meaning to AIR and runtime execution state to Pipeline. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification work only | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes writing/technical review while build remains forbidden. |
| `.../V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | pending ratification | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Controls candidate labeling and the pre-ratification acceptance ceiling. |
| `.../V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | recovery packet | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Freezes this one-spec scope, exact path, three dependencies, Wave 3, and stop conditions. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | validated | `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | Classifies SDE-017, SDE-018, and SDE-019 as WRITE-interface dependencies, not acceptance/build gates. |
| `.../V2_1_SPEC_WRITING_RECOVERY/SPEC_WRITING_WAVE_DAG.yaml` | validated | `24b26b9820a0f2cab0cd01ab4c46e9aca476219f496644c063533ee602ccff60` | Places TS-AIR-013 in Wave 3 after AIR-002/003/005 drafts exist. |
| `.../wave-receipts/WAVE_03_DISPATCH_LOCK.yaml` | dispatched in maximal batches | `e8137e45a267767fd3e0b2f5bdc278ac66d570187b34b4a48ef282db84bdca65` | Pins exact draft paths, states, and hashes for dispatch. |
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/.../skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3 | `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | Requires one spec, ten sections, typed fields, exact paths, receipts, and no self-audit. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/MASTER_STATUS.md` | current status | `71d7fdac3c9498c42133c95e141b31241b0fa613426417d9fd81b3d1d656f491` | V2.1 candidates remain pending; AIR implementation, production, and certification authority are absent. |

The abbreviated `...` paths expand under the AIR full-bundle or named Program Control directory established by the leading row. No `AGENTS.md` exists at the target directory or any ancestor to the workspace root. The exact packet therefore governs the direct product spec path under explicit Prompt 02 and Prompt 02C specification authority.

### Exact upstream draft interfaces

| Edge | Upstream draft | State | Bytes | SHA-256 | Interface used | Revision impact on drift |
|---|---|---:|---:|---|---|---|
| SDE-017 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-002.md` | `WRITTEN_PENDING_AUDIT` | 52,295 | `258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5` | Identity/Brand refs, Context Premise, Resonance, Matrix, broad signal, audience context, psychological role/tension, Edge lineage, immutable refs, invalidation | sections 3, 5, 6, 8, 9, 10 |
| SDE-018 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-003.md` | `WRITTEN_PENDING_AUDIT` | 74,824 | `ce9ac739346789d115ada80c44b568c28e61ce68f0ae99bb55b0962c875d430c` | complete hypothesis portfolio, selected semantic direction, planned promotion, role/direction/pressure/counteractivation, source-kind/provenance, history and stopping evidence | sections 3, 5, 6, 8, 9, 10 |
| SDE-019 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-005.md` | `WRITTEN_PENDING_AUDIT` | 44,990 | `5dcf631efc4f68f40edd0991ca3ae4be9073da68aa441c52d37e874e70a43e49` | exact Primitive Coalition Contract, Coalition Signature, Edge Product, misuse/fatality/routeability findings, transfer invariants and Steering Recipe candidate boundaries | sections 3, 5, 6, 8, 9, 10 |

All three are `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Their interface details are usable for dependency-safe writing but cannot establish current authority or build eligibility.

### Required unique evidence, exact Primitives, and brownfield inputs

| Evidence | State | SHA-256 | Specific fact used |
|---|---|---|---|
| `.../sources/ai_v2_predecessor/contracts/08_CAMPAIGN_ACTIVATION_PROGRAM.md` (`SRC-AI2-CAMPAIGN-001`) | `REQUIRED_UNIQUE_EVIDENCE` | `902d0a9aea819a16388bac2283b6e15a6414ae73dda32270f22f06ee942f866d` | Campaign coordinates source package, audience segments, asset programs, role/direction portfolio, sequence, fatigue/repetition, affinity reset, source reuse, publication order, and campaign evaluation. |
| `.../sources/doctrine/AHP_F23_BATCH_ARCHETYPE_ROUTING.md` (`SRC-AHP-F23-001`) | `REQUIRED_UNIQUE_EVIDENCE` | `94833575d71b8c04fb0bcab11ca02e99865502bbb7c8445d25a41c9c985d816d` | Pipeline operational batch/job ownership, source-backed routing, immutable jobs, dedupe, bounded roles, and selective invalidation; does not transfer AIR semantic authority. |
| `.../sources/doctrine/CCV_COMBINATORIAL_CONTROLLED_VARIATION.md` (`SRC-CCV-001`) | `REQUIRED_UNIQUE_EVIDENCE` | `0869ff50e4bdaba3dc1854183100826d0de9568b9ed5558bf68b4590834a62c4` | Axis-labeled controlled variation, anti-centroid, Primitive-before-Edge, coalition geometry/fatality, routeability, and benchmark laws. |
| `.../sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion/PRM-PRS-002.yaml` | exact Primitive source | `4fba8edcb439c296a610b53a45ce76b9a002b4a128338e3302ddbb1cc49e242e` | Tension-and-Release; block unresolved tension and micro-tension exhaustion. |
| `.../sources/cmf_primitive_registry_snapshot/meaning_plane/humor_distortion/PRM-HUM-021.yaml` | exact Primitive source | `53712577ba9f27112afce11fd022a94033f44ceca5f910c6eec2e3c8fae39253` | Irony Inversion; block broken conviction, absent subtext, sustained irony fatigue, low-literacy/harmful contexts. |
| `.../sources/cmf_primitive_registry_snapshot/experience_plane/trust_branding/EXP-TRS-003.yaml` | exact Primitive source | `1281a1ec4bc9301951224dbf93409bd4bbd01656b068c873f25b6214147b876d` | Reflective Social Proof; only applicable to supported status/share contexts; block overt marketing, generic assets, and forced sharing. |
| `.../contracts/schemas/campaign_activation_program.schema.json` | predecessor schema evidence | `aee3bfa9a1110f20d9b10c30eb2fb0c320fc73d38edcf3b57ea7f50aea2bdc1d` | Useful closed program/asset/ref shape; hard-coded integer minima, float fatigue, defaults, and shallow lineage are not current canonical design. |
| `.../examples/10_campaign_activation_program.json` | predecessor fixture evidence | `2fe04a237a33d2c9e10cd27457af39d3081e4d0b035b72a4951ec69c413c7301` | Three-asset ordered campaign fixture suitable for migration and negative testing, not production or effectiveness evidence. |
| `.../reference_implementation/activative_intelligence_v2/freshness.py` | predecessor implementation | `8e6d1c5834bdd198a62fd4cdae1a4efc082fac48dca779aeaa8818def0754776` | Frozen exposure record and deterministic arithmetic seed; hard-coded 30-day window/weights and binary floats lack profile/evidence/version semantics. |
| `.../reference_implementation/activative_intelligence_v2/models.py` | predecessor implementation | `d75529f08416db1648e95e6762c273aa18fd9f56bbe6c4a6805efbae3909a3b3` | Strict/frozen program, asset, audience receipt, and freshness model seeds; open dictionaries, floats, defaults, shallow lineage, and mixed ownership require adaptation. |
| `.../tests/test_contracts.py` | predecessor test evidence | `e727526d363dd87bda00b39beb4e3fce987d43b4a49d18ab59894f8f9cbc2dbb` | Only proves the example parses; it does not prove sequencing, freshness, reaction separation, authority, atomicity, replay, or effectiveness. |

## 2. Problem, user outcome, solution, and scope

### Problem and user outcome

An individually activative asset can become counteractivating inside a sequence. If a campaign independently ranks each local candidate, it can publish repeated accusation, regret, irony, high-pressure contrast, one coalition geometry, one archetype formula, or one visual operator until the audience recognizes the template before feeling the human pressure. Local engagement can also be misread as source truth, an audience reaction can be confused with the guest's Reaction Receipt, and platform performance can silently rewrite semantic authority.

The operator needs a reproducible campaign-level program that sequences only eligible, source-backed derivative programs across exact audiences, roles, tensions, activation directions, Edges, Primitive/archetype coalitions, formats, stances, relationship movements, pressure/relief, affinity resets, and publication functions. It must carry a context-specific freshness profile, reject non-compensable repetition, accept audience observations as a separate limited evidence stream, infer fatigue/counteractivation without causal overclaim, and create additive, selective revisions without erasing published history or changing upstream meaning.

### Bounded solution

F13 specifies:

1. an AIR-owned immutable `CampaignActivationProgram` and embedded AIR-owned semantic `CampaignAssetPlan` sequence;
2. profile-pinned diversity, repetition, exposure, pressure/relief, affinity-reset, and freshness gates before Pipeline handoff;
3. a context-specific `ActivationFreshnessProfile` derived from exact historical asset/program/exposure evidence rather than a universal novelty score;
4. a distinct `PublishingObservationEnvelope` produced operationally by Pipeline/platform adapters and an AIR-owned `AudienceReactionReceipt` that preserves raw ownership, measurement limits, and epistemic separation from source reaction;
5. typed `FatigueSignal` and `CampaignCounteractivationAssessment` objects with independent evaluation and no silent semantic rewrite;
6. immutable `CampaignRevision` programs that supersede only affected sequence/asset-plan decisions, retain all prior bytes/evidence, and route upstream semantic defects to the owning product/layer;
7. transactional command/event/receipt, compatibility, idempotency, concurrency, cancellation, invalidation, replay, migration, and clean-room requirements.

### In scope

- exact campaign source package, Identity/Brand/Context/Matrix, hypothesis, coalition/signature/Edge, approved Final Script, derivative program, audience, relationship, profile, and wrong-reading lineage;
- semantic sequence, role/direction/Edge/archetype/Primitive/format/stance/relationship portfolios;
- policy-driven non-compensable diversity and repetition gates;
- exposure/freshness memory by exact audience context, platform, profile, time window, and asset lineage;
- publishing observation admission with measurement definition, denominator, scope, limits, and correction history;
- audience-role evidence, wrong-role evidence, counteractivation/fatigue inference, and planned-observed campaign delta;
- bounded proposal ports and independent evaluation without producer self-acceptance;
- additive resequencing, replacement, reset, hold, split-audience, lower-pressure, and retire-pattern revisions;
- selective invalidation and historically reproducible published campaigns;
- future implementation files, schemas, adapters, migrations, observability, tests, and evidence contract.

### Out of scope and non-goals

- creating or modifying a Canonical Interview Source Package, Reaction Observation, Reaction Receipt, Expression Moment, Identity DNA, Context Premise, Matrix, Primitive/coalition, archetype coalition, Final Script, Derivative Activation Program, or source fact;
- compiling Pipeline's operational `ContentBatchOrchestrationProgram`, immutable derivative jobs, execution bindings, publication schedules, provider jobs, or runtime receipts inside AIR;
- performing publication, media rendering, VAE production, Delegation transport, or platform API collection;
- letting audience metrics, engagement, a score, or a model evaluation automatically alter upstream semantic authority;
- treating correlation as causation, inferring private audience identity/state, or fabricating an audience segment from aggregate telemetry;
- generic creative-safety/content-rights authority; operator-supplied source authority, provenance, lineage, approvals, and product sovereignty remain explicit while technical security remains operational;
- hard-coding universal freshness/effectiveness thresholds or inheriting certification from any format profile;
- activating Format 02, beginning VAE Stage 5, issuing a capsule, or granting implementation, production, publication, model-training, provider, or certification authority.

## 3. Governing decisions and constraints

### Authority and product sovereignty

1. **V1.1 remains current.** Candidate V2.1 documents may guide authorized specification work but remain `CANDIDATE_NOT_CURRENT`. A lower draft cannot narrow V1.1 semantic lineage or create new sovereignty.
2. **AIR owns campaign semantic meaning.** The `CampaignActivationProgram`, its semantic `CampaignAssetPlan` entries, freshness interpretation, fatigue/counteractivation findings, and additive semantic revision are AIR objects. The F13 PRD's local owner labels for Pipeline consumers/publishing adapters are corrected by the higher Program Control matrices.
3. **Pipeline owns operational batch and execution state.** Pipeline consumes an evaluated AIR campaign program, compiles its own typed batch/jobs, binds Harnesses, schedules/executes/publication work, captures platform observations, and owns execution receipts. It cannot reinterpret AIR role/tension/Edge/coalition/Final Script meaning.
4. **A publishing adapter is an evidence producer, not semantic authority.** It owns the authenticity of its signed raw observation payload and platform mapping. AIR owns only the immutable campaign-domain receipt that references those bytes and states their limitations. An adapter cannot issue campaign revision or semantic acceptance.
5. **Independent Evaluation owns judgment receipts.** AIR compilers/detectors do not accept their own work. Passing evaluation is eligibility evidence, not publication or production authorization.
6. **Studio projects and captures human resolution.** It may display sequence/freshness/reaction evidence and translate an attributable operator correction into a typed command/HumanResolutionEpisode. It cannot mutate canonical AIR/Pipeline state or promote a local preference globally.
7. **Builder, VAE, and Delegation stay bounded.** Builder declares exact dependencies and compiles AtomicHarnessDefinition; Pipeline executes; VAE realizes typed demands; Delegation transports. `Activative Contract Compiler != Activative Intelligence Runtime` remains explicit.

### Semantic, source, and reaction laws

8. **Source reaction and audience reaction are different domains.** A source `ReactionReceipt` records a guest/coach response during source activation and is owned by Interview Expression. `AudienceReactionReceipt` records post-publication audience evidence and is an AIR campaign-domain object grounded in external/Pipeline observations. IDs, schemas, owners, lifecycle, and consumers are disjoint.
9. **Campaign inputs are exact, not copied prose.** Every item references the exact source package, source kind/provenance, audience/context, Matrix/Edge, selected hypothesis, Primitive Coalition Contract, Coalition Signature, archetype coalition, operator-approved Final Script, Voice/Visual DNA, derivative program, transfer contract, profile, and evaluation bytes required for that asset.
10. **No route or fit is manufactured.** Campaign compilation may sequence only current, source-supported, category/profile-compatible derivative opportunities. Unsupported items are excluded with reasons before ranking.
11. **Audience performance cannot rewrite truth.** An audience receipt may support freshness/fatigue inference or a revision proposal; it cannot change a quote, Expression Moment, source package, Identity DNA, Primitive meaning, Edge Product, Final Script, or observed source reaction.
12. **Observation and inference remain separate.** Raw counts/events are `observed` under stated measurement scope. Audience-role attribution, counteractivation, habituation, formula visibility, and causal hypotheses are `inferred` unless independently established. A single object status cannot collapse the distinction.
13. **Measurement limitations are mandatory.** Asset version, audience context, platform/profile, exposure/observation windows, denominator, organic/paid/unknown distribution, missing-data conditions, bot/filter policy, sampling/aggregation, metric definition versions, and attribution limitations remain explicit.
14. **Unknown is preserved.** Missing platform data, ambiguous audience, unavailable denominator, mixed paid/organic exposure, or non-identifiable sequence effects become typed unknown/limited evidence. They are not zero, no-reaction, or proof of fatigue.

### Campaign diversity, freshness, and Primitive laws

15. **Campaign quality is non-local.** No sum or average of local asset scores may compensate for a repeated-role, repeated-direction, repeated-Edge, repeated-coalition, repeated-archetype, relief-deficit, or fatigue hard gate.
16. **Diversity policy is governed and context-specific.** Minimums, repetition maxima, distance rules, windows, budgets, and exceptions come from an exact `CampaignDiversityPolicyRef`; no implementation default or historical example becomes universal law.
17. **Freshness is not novelty for novelty's sake.** It is a new entrance into still-relevant human pressure. Superficial wording, random visual changes, or format shuffling cannot count as semantic diversity when role/tension/Edge/coalition geometry remains unchanged.
18. **Freshness is scoped.** A pattern can be exhausted for one audience/platform/window and available for another. The profile never becomes a global statement about an archetype, Primitive, person, or brand.
19. **CCV axes stay independent.** Role, tension, direction, stance, archetype, Primitive coalition/signature, format, visual operator, pressure, relief, and relationship movement remain separable labeled coordinates. Variation cannot centroid-smear them.
20. **PRM-PRS-002 governs campaign rhythm.** Sequence logic must distribute real tension and commensurate relief. Unresolved campaign tension and micro-tension exhaustion are hard negatives.
21. **PRM-HUM-021 is conditional, not mandatory style.** Irony Inversion applies only when its trigger/evidence and audience literacy/harm context permit it. Broken conviction, absent subtext, and sustained irony fatigue are hard negatives. A campaign cannot count repeated irony with different wording as fresh.
22. **EXP-TRS-003 is share-context conditional.** Reflective Social Proof applies only to evidence-supported status/share functions. Overt marketing, generic status assets, forced sharing, private-loop misuse, and humiliating share conditions are forbidden. Campaign sequencing never creates a share gate.
23. **Primitive applicability is exact.** Each binding carries ID/version/hash, local job, triggers, suppression, conflicts, misuse modes, evidence, and outcome. `NOT_APPLICABLE` is typed and evidenced; omission and filename similarity are invalid.
24. **Final Script and transfer locks survive sequencing.** A campaign can sequence or hold an approved derivative; it cannot rewrite Final Script language, Voice DNA, Visual DNA, transfer invariants, wrong-reading locks, or Composition Intent. A required change routes to the owning upstream layer and returns only through a new version.

### Lifecycle, evidence, and claim laws

25. **Versions are immutable and history is additive.** Program, asset plan, profile, receipt, signal, and revision bytes never update in place. Corrections and revisions create successors with exact supersession/causal links.
26. **Revision is selective.** A revision names exact affected entries/decisions and invalidates only descendants that depend on them. Published artifacts, raw observations, prior receipts, and unaffected sequence entries remain historically reproducible.
27. **Current and historical views are separate.** A current projection refuses stale/cancelled/revoked dependencies; replay resolves historical bytes by hash even after current invalidation.
28. **Transactions preserve artifact/receipt parity.** Artifact versions, dependency edges, command record, lifecycle events, receipts, and outbox entries commit atomically or not at all.
29. **Idempotency and optimistic concurrency are mandatory.** Same key and same canonical input returns the original result; same key with different input fails. Expected aggregate version prevents lost updates.
30. **Determinism excludes hidden machine state.** Caller-supplied IDs/times, canonical UTF-8, canonical collections, fixed-point metrics where identity requires them, and logical refs prevent current time, random state, dictionary order, filesystem traversal, environment, locale, and absolute-path leakage.
31. **No parser-only compatibility.** A consumer must support semantic roles, policy rules, observation limits, reaction separation, lock inheritance, invalidation, and lifecycle. An adapter cannot drop or weaken them.
32. **Claim ceiling is fixed.** This writing ends `WRITTEN_PENDING_AUDIT`, candidate not current, build false, with a later pre-ratification ceiling of `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.

## 4. Current brownfield architecture

### Evidence worth retaining

The V2 predecessor already demonstrates four useful structural ideas: immutable reference-shaped campaign entries; an ordered three-asset campaign example with distinct roles/directions/formats; strict/frozen model configuration; and a deterministic freshness arithmetic seed. The AHP F23 doctrine separately defines operational batch/job concerns, exact Harness bindings, shared read-only analysis, deduplication, bounded actor roles, and selective invalidation. Those surfaces are useful only after ownership is split: AIR compiles semantic campaign meaning; Pipeline compiles and executes operational batches.

### Brownfield disposition matrix

| Exact component | Actual behavior | Gap or hazard | Disposition |
|---|---|---|---|
| `contracts/08_CAMPAIGN_ACTIVATION_PROGRAM.md` | Lists core campaign coordination concerns. | No ownership, field types, epistemic state, lifecycle, audience-reaction separation, policy refs, revision, or replay. | `REUSE_AS_CONTRACT_SEED`; expand under current authority. |
| `contracts/schemas/campaign_activation_program.schema.json` | Closed schema with exact refs, ordered assets, role/direction minimums, repetition limit, fatigue budget, resets, and evaluation ref. | Floats/defaults; no source-kind/owner/hashes on program; shallow asset lineage; universal numbers; no coalition/archetype/Final Script/reaction/revision contracts. | `ADAPT`; do not publish predecessor schema as current. |
| `examples/10_campaign_activation_program.json` | Three distinct ordered assets and one source/evaluation ref. | Synthetic IDs/hashes and no proof of freshness, audience reaction, authority, or production. | `ACTIVATE_AS_MIGRATION_FIXTURE`; never effectiveness evidence. |
| `reference_implementation/.../freshness.py` | Frozen `PatternExposure` and a repeatable weighted score. | Hard-coded 30-day window, denominator 10, weights 0.35/0.35/0.30, float drift, single scalar collapse, no policy/profile/version/evidence/owner/receipt. | `REPLACE_FOR_CANONICAL`; retain arithmetic as adversarial migration fixture. |
| `reference_implementation/.../models.py::CampaignAssetPlan` | Asset ref, sequence, role, direction, Edge text, format. | Edge flattened to text; missing tension, coalition/signature, archetype, Final Script, audience, relationship, profile, locks, rationale, dependency hash. | `ADAPT` to AIR semantic plan with exact refs. |
| `...::CampaignActivationProgram` | Source, audiences, assets, diversity numbers, fatigue float, reset indices, publication-order flag, evaluation ref; validates two minima. | Local numeric minima can pass a semantically repetitive campaign; no policy version, direction/role evidence, other axes, relief, lifecycle, owner, history, atomic receipt. | `ADAPT_AND_DEEPEN`; local scores never compensate hard gates. |
| `...::AudienceReactionReceipt` | Asset ref, segment, observed reactions, role evidence, wrong roles, counteractivation strings, metrics, epistemic state. | Open dicts/strings/floats; no platform/exposure/measurement definition/denominator/limits/raw owner/correction/sequence context; observation and inference can mix. | `ADAPT_AND_SPLIT_RAW_FROM_INTERPRETATION`. |
| `...::ActivationFreshnessProfile` | Recent linguistic/visual/role/direction counts, qualitative signals, freshness float, update time. | Open maps, no exact pattern taxonomy or asset refs, universal score, current time, no audience/platform/window/profile/unknown state. | `REPLACE` with context-scoped evidence ledger and derived findings. |
| `tests/test_contracts.py::test_campaign` | Parses one JSON example. | No behavior, denial, authority, determinism, atomicity, concurrency, revision, invalidation, replay, or measurement tests. | `ACTIVATE_AS_SMOKE_REGRESSION` only. |
| `sources/doctrine/AHP_F23_BATCH_ARCHETYPE_ROUTING.md` | Pipeline batch compilation, route eligibility, immutable jobs, source sharing/dedupe, bounded roles, selective invalidation. | Local sentence says Pipeline owns batch compilation; without object distinction it could absorb AIR Campaign Program meaning. | `REUSE_AS_OPERATIONAL_EVIDENCE`; distinguish AIR semantic program from Pipeline batch execution program. |
| `sources/doctrine/CCV_COMBINATORIAL_CONTROLLED_VARIATION.md` | Axis variation, coalition geometry/fatality, routeability, anti-centroid, benchmark learning. | Contains historical implementation/provider suggestions and absolute local links that are not current authority or portable contract bytes. | `REUSE_REQUIRED_LAWS`; exclude historical provider/path assumptions. |

### Migration boundary

A V2 campaign migrates only when attributable evidence supplies every mandatory owner, source/context, role/tension, Edge/coalition, archetype/Final Script, policy, profile, lock, and lifecycle field. Legacy floats are preserved as evidence with their algorithm/version; they do not silently become current fixed-point findings. A missing source kind, audience context, metric denominator, route meaning, policy, or owner is not inferred. The adapter either emits new immutable V2.1 artifacts plus a migration receipt or preserves the old bytes and returns a typed blocker.

## 5. Proposed architecture and workflows

### Components and responsibilities

| Component | Owns | Must not do |
|---|---|---|
| `CampaignInputResolver` | Resolve exact source, audience/context, F02/F03/F05, Final Script, derivative, profile, policy, authority, and evaluation refs. | Guess source kind, audience, Edge, role, policy, owner, or approval. |
| `CampaignSemanticCompiler` | Create AIR-owned sequence entries and program from eligible derivative opportunities. | Compile Pipeline jobs, execute, publish, or alter upstream semantics. |
| `CampaignDiversityValidator` | Evaluate non-compensable role/direction/tension/Edge/coalition/archetype/structure/format/relief constraints against pinned policy. | Substitute a local aggregate score or historical default. |
| `FreshnessProjector` | Build immutable, context-scoped exposure profile and deterministic findings from exact history. | Declare global novelty, infer missing exposure, or use current clock implicitly. |
| `PublishingObservationAdmissionPort` | Verify signatures/schema/asset/context/window/metric definitions and admit raw observation refs. | Interpret source truth, campaign meaning, or causal effectiveness. |
| `AudienceReactionInterpreter` | Compile an AIR receipt with separate observed facts, inferred role/counteractivation findings, limitations, and delta to intent. | Create Interview Expression Reaction Receipts or mutate source/Final Script. |
| `CampaignFatigueDetector` | Emit typed, profile-pinned fatigue/counteractivation signals and evidence. | Treat absence of engagement as fatigue or use ungoverned thresholds. |
| `CampaignRevisionCompiler` | Create bounded additive revision candidates and impact sets. | Rewrite published history or repair another product's object. |
| `F13IndependentEvaluationPort` | Obtain externally owned evaluation receipts for program/profile/reaction/signal/revision. | Share producer identity or issue publication authority. |
| `CampaignLifecycleService` | Authorization, commands, idempotency, concurrency, transactions, handoff, invalidation, cancellation, replay. | Own Pipeline execution or Studio state. |
| `CampaignRepository` | Immutable artifacts, observation refs, edges, commands, events, receipts, outbox, projections, historical bytes. | Accept orphan artifacts/receipts or in-place updates. |
| `PipelineCampaignHandoffAdapter` | Export exact evaluated AIR program and ingest Pipeline acknowledgement/observation refs. | Flatten semantic fields or accept unsupported features. |
| `StudioCampaignProjectionAdapter` | Reconstruct inspectable views and translate attributable commands/HumanResolution refs. | Become canonical state or auto-promote local corrections. |

### Workflow A - compile a coordinated Campaign Activation Program

1. `CompileCampaignActivationProgramCommand` supplies caller-generated command/idempotency/program IDs and event time, expected aggregate version, authority/actor refs, exact canonical source package and source-kind/provenance, audience/context refs, eligible derivative opportunity refs, F02/F03/F05 semantic refs, approved archetype-coalition Final Script refs, Voice/Visual DNA refs, transfer/derivative program refs, format/category/profile refs, wrong-reading locks, campaign objective, relationship movement, diversity/freshness policies, evaluation contract, and publication-function constraints.
2. The resolver validates ID/version/hash/owner/lifecycle for every ref. It denies stale, cross-brand, unsupported, unevaluated, unapproved, or source-scope-incompatible opportunities before proposal/ranking. No missing route is manufactured.
3. The compiler creates candidate asset plans preserving per-item source spans/grants, audience segment, psychological role inside a tension, activation direction, Edge Product, Primitive Coalition/Signature, archetype coalition, Final Script, stance, pressure/relief function, relationship movement, format/profile, sequence function, source reuse, dependencies, locks, and exclusions.
4. `CampaignDiversityValidator` applies the exact policy to the whole sequence. It evaluates all governed axes and adjacency/window constraints. Any fatal repetition, relief deficit, role overload, unsupported irony/share use, or policy violation blocks regardless of local asset scores.
5. The compiler creates an ordered sequence with explicit affinity resets, escalation/relief, holds, and dependency edges. It does not choose publication time or provider execution details unless supplied as immutable external constraints.
6. Deterministic gates precede independent evaluation. On success, program/asset-plan bytes, candidate decisions/exclusions, edges, command record, event, outbox item, and compilation receipt commit atomically. State becomes `COMPILED_PENDING_EVALUATION`.
7. Independent Evaluation checks campaign-level role/tension coherence, policy compliance, anti-centroid preservation, source/final-script fidelity, Primitive applicability, counteractivation, and wrong readings. Passing creates an eligibility projection; it does not publish.

### Workflow B - compile and update the Activation Freshness Profile

1. `CompileActivationFreshnessProfileCommand` pins audience segment/context, platform/profile, observation cutoff supplied by caller, exposure-window policy, pattern taxonomy, exact historical campaign/program/asset/publication refs, raw observation refs, exclusions, and prior profile ref when incrementally projecting.
2. The projector enumerates each exposure by exact pattern dimensions: linguistic structure, inversion pattern, role, tension, direction, Edge, Primitive coalition/signature, archetype coalition, visual operator, format, stance, relationship move, pressure/relief, affinity reset, and source reuse. Unknown dimensions remain typed unknown.
3. The projector records counts, recency relative to the caller-supplied cutoff, audience reach/denominator when measurable, evidence completeness, and qualitative signals with attributable refs. It does not collapse all dimensions into one universal score.
4. A pinned `FreshnessEvaluationProfile` may derive fixed-point per-dimension availability/fatigue findings, repetition budget use, prediction-error decay hypotheses, and policy violations. Thresholds and weights live in the profile and are included in the hash.
5. The profile remains specific to audience/context/platform/window. A profile for one segment cannot reject another without an exact compatibility/transfer decision.
6. A new observation or corrected publication record creates a successor profile version; old profile bytes remain replayable.

### Workflow C - capture audience reaction as a separate evidence stream

1. Pipeline or an authorized publishing adapter emits `PublishingObservationEnvelope` for an exact published asset version and publication/execution receipt. The envelope includes platform/profile, audience-context ref, exposure and observation windows, metric definitions/units, values and denominators, sampling/filtering/distribution flags, raw evidence refs, adapter identity/version, limits, and signature.
2. `AdmitPublishingObservationCommand` validates provenance, signature, schema/profile compatibility, source authority for the data, asset/campaign binding, time-window legality, duplication, correction/supersession, and PII/security constraints. It does not interpret the payload.
3. `CompileAudienceReactionReceiptCommand` pins admitted envelope(s), exact campaign intent/asset plan, evaluator profile, and prior receipt where applicable. Observed metrics remain separate from inferred role/counteractivation/meaning findings.
4. The interpreter may propose `role_evidence`, `wrong_role_evidence`, `counteractivation_hypotheses`, `fatigue_hypotheses`, and `planned_observed_delta`, each with evidence, confidence form defined by the profile, counterevidence, alternative explanations, and measurement limitations. It cannot create a source Reaction Receipt.
5. Deterministic validation rejects missing asset version, context, window, definition, denominator when required by the metric, or contradictory corrections. Independent evaluation assesses judgment dimensions. The AIR receipt stays evidence, not automatic revision or publication success.
6. Late/corrected observations append new envelopes and receipt versions. Previously used evidence remains historically reachable; affected fatigue/revision projections are selectively invalidated.

### Workflow D - detect counteractivation and campaign fatigue

1. `DetectCampaignFatigueCommand` pins current campaign/program sequence, freshness profile, audience reaction receipts, evaluation profile, comparison/baseline refs when available, and requested detection window.
2. Deterministic detectors identify policy-defined repetition, exposure, relief deficit, and sequence violations. Bounded judgment may assess formula visibility, habituation, defensive repetition, role overload, Edge overuse, misrecognition, performative agreement, reactance, or loss of self-authorship.
3. Every `FatigueSignal` states type, scope, epistemic state, exact affected entries/dimensions, evidence/counterevidence, alternative hypotheses, limits, severity under a governed profile, and responsible repair layer. Missing evidence cannot yield a low-risk assertion.
4. A signal is not a global audience truth and does not automatically retire an archetype/Primitive. It is current only for the pinned context/window and may be rejected or superseded.
5. Independent Evaluation must distinguish fatigue from topic mismatch, distribution change, source mismatch, seasonality, audience composition, measurement change, platform anomaly, or low-quality realization before a revision becomes eligible.

### Workflow E - revise the campaign additively

1. `ProposeCampaignRevisionCommand` pins current program/profile/receipts/signals, exact failure attribution, affected dependency graph, allowed revision policy, and operator/evaluator context. A model may propose candidates only inside the typed envelope.
2. `CampaignRevisionCompiler` emits one or more immutable candidates using closed operations: `RESEQUENCE`, `REPLACE_ASSET_PLAN_REF`, `INSERT_AFFINITY_RESET`, `ADJUST_ROLE_DIRECTION_MIX`, `LOWER_PRESSURE`, `ADD_RELIEF`, `HOLD_PUBLICATION`, `SPLIT_AUDIENCE_CONTEXT`, `RETIRE_PATTERN_FOR_SCOPE`, or `REQUEST_UPSTREAM_REPAIR`.
3. Each operation names affected sequence entries, preserved properties, evidence, expected effect, limits, invalidated descendants, required reruns, and rollback. It cannot edit source, coalition, Final Script, derivative program, or published output.
4. Upstream semantic defects produce `REQUEST_UPSTREAM_REPAIR` to the owning AIR feature or source product. F13 waits for a new immutable upstream version before recompiling affected plans.
5. A separate authorized command, with independent evaluation and any required human resolution, promotes exactly one bounded revision into a successor Campaign Activation Program. Unaffected entries retain their exact refs; published history and observations remain unchanged.

### Workflow F - Pipeline handoff, cancellation, invalidation, and replay

1. `HandoffCampaignProgramCommand` exports only an evaluated current program plus exact schemas/features/profile requirements and limitations. Pipeline responds with a separate consumption acknowledgement; it does not duplicate AIR evaluation.
2. Pipeline compiles operational batch/jobs under its own spec. The AIR semantic asset plan and Pipeline job contract retain distinct IDs, owners, versions, and receipts linked by exact refs.
3. Cancellation before commit stores no partial semantic state. Cancellation after commit appends a cancellation receipt and prevents new handoff; it does not delete history. Late external observations may be admitted as historical evidence if tied to an already valid publication, but cannot reopen a cancelled current campaign automatically.
4. Superseding/revoking source, authority, Context/Matrix, hypothesis, coalition/signature/Edge, Final Script, transfer/derivative program, policy, profile, observation, or evaluation version traverses typed edges and invalidates only current dependent projections. Revoked source authority blocks new use immediately.
5. Replay resolves stored canonical bytes/registry/profile snapshots, replays command/event order, and reproduces artifact/receipt hashes independently of current registries, current clock, random state, environment, filesystem order, or machine path.

## 6. Data models, contracts, schemas, and APIs

### Shared scalar, reference, and canonicalization rules

All schemas are closed (`additionalProperties: false`). IDs are caller-supplied nonempty opaque strings. `ImmutableRef` contains `{object_type, object_id, version, sha256, authoritative_owner, lifecycle_state_at_use}`. Text is Unicode NFC, trimmed, and nonempty where required. Semantic ratios/scores that affect identity use integer micros `0..1_000_000`; raw platform integers remain integers and decimal measurements use canonical base-10 scaled values with declared scale/unit. Binary floats never contribute to canonical identity.

Ordered campaign sequences preserve order. Semantically unordered sets/maps serialize as sorted arrays of closed key/value records by canonical key. Canonical JSON uses UTF-8 without BOM, LF for semantic text, lexicographic object keys, no insignificant whitespace, normalized numbers, and no absolute filesystem paths. Each root object includes `schema_id`, `schema_version`, `artifact_id`, `artifact_version`, `aggregate_id`, `aggregate_version`, `owner_product`, `authority_ref`, `created_by_actor_ref`, caller-supplied `effective_at`, `canonicalization_profile`, `dependency_refs`, `artifact_sha256`, and `lifecycle_state`.

### `CampaignActivationProgram`

Schema ID: `ca.air.campaign-activation-program/2.1.0-candidate`.

| Field | Type | Owner / invariant |
|---|---|---|
| `campaign_program_ref` | `ImmutableRef` | AIR immutable version. |
| `epistemic_class` | literal `planned` | Program intent is planned, never observed audience truth. |
| `source_package_refs` | tuple of refs, 1..n | Exact source owner/kind/provenance/route scope; no copied source text. |
| `identity_brand_context_refs` | `IdentityBrandContextSet` | Exact human-owned Identity DNA plus Brand Context/Voice/Visual DNA refs. |
| `context_premise_refs`, `matrix_refs`, `broad_signal_refs` | tuple of refs | Exact F02 context per audience/segment. |
| `selected_hypothesis_and_portfolio_refs` | tuple of refs | Exact F03 selection/history for each semantic program. |
| `primitive_coalition_refs`, `coalition_signature_refs`, `edge_product_refs` | tuple of refs | Exact F05 geometry/fatality/transfer invariants. |
| `archetype_coalition_refs`, `approved_final_script_refs` | tuple of refs | Operator-approved semantic authority; required per content-bearing item. |
| `activation_transfer_and_derivative_program_refs` | tuple of refs | Exact eligible AIR programs; campaign cannot alter them. |
| `audience_contexts` | tuple of `CampaignAudienceContext`, 1..n | IDs, context evidence, relationship stage, platform/profile, source authority scope. |
| `campaign_objective` | `EpistemicAssertion<CampaignObjective>` | Intended role/tension/relationship movement and evidence limits. |
| `asset_plans` | ordered tuple of `CampaignAssetPlan`, 1..n | Unique contiguous sequence positions under policy. |
| `role_direction_portfolio` | `CampaignAxisPortfolio` | Exact per-axis counts/coverage/distance decisions and exclusions. |
| `sequence_program` | `CampaignSequenceProgram` | Escalation, relief, affinity resets, dependencies, publication functions, hold conditions. |
| `diversity_policy_ref`, `freshness_policy_ref`, `evaluation_profile_ref` | exact refs | Required; thresholds/rules never local defaults. |
| `freshness_profile_refs` | tuple of refs | Exact context profiles used at compilation. |
| `wrong_reading_locks` | tuple of locks, 1..n | Inherited union; cannot be weakened. |
| `candidate_exclusion_receipt_refs`, `evaluation_receipt_refs` | tuple of refs | Alternatives and denials remain inspectable. |
| `pipeline_compatibility_requirements` | closed tuple | Required schemas/features/profiles for handoff. |

### `CampaignAssetPlan`

Schema ID: `ca.air.campaign-asset-plan/2.1.0-candidate`. This is AIR semantic intent, not a Pipeline job.

Required fields are:

`asset_plan_ref`; `campaign_program_ref`; `sequence_index`; `audience_context_refs`; `source_package_and_span_refs`; `derivative_activation_program_ref`; `activation_transfer_contract_ref`; `psychological_role_ref`; `tension_ref`; `activation_direction`; `edge_product_ref`; `primitive_coalition_ref`; `coalition_signature_ref`; `archetype_coalition_ref`; `approved_final_script_ref`; `brand_context_ref`; `guest_voice_dna_ref`; `visual_dna_ref`; `format_category_profile_refs`; `stance`; `relationship_movement`; `pressure_and_relief_function`; `attention_sequence_function`; `participation_path`; `source_reuse_policy_ref`; `sequence_dependency_refs`; `affinity_reset_role`; `publication_function`; `routeability_and_eligibility_receipt_refs`; `wrong_reading_locks`; `limitations`; and `canonical_hash`.

`activation_direction` is a governed closed value from the active policy/contract, not an implementation-created free string. `publication_function` describes semantic sequence purpose such as entry, recognition, pressure, contradiction, relief, reset, invitation, proof, or close; it does not schedule or publish. `affinity_reset_role` is `NONE` or a typed reset program with evidence; `NONE` is not a missing value.

### `CampaignDiversityPolicy` and axis evidence

Schema ID: `ca.air.campaign-diversity-policy/2.1.0-candidate`; managed in a governed profile registry, not created by the campaign compiler.

It contains `{policy_ref, applicability_envelope, required_axes, minimum_distinct_values_by_axis, maximum_repetitions_by_axis_and_window, adjacency_constraints, combination_distance_rules, pressure_relief_rules, affinity_reset_rules, source_reuse_rules, exception_rules, fatal_rules, evaluator_profile_ref, canonical_hash}`. Every threshold is an integer/fixed-point value tied to a named window and applicability envelope. Exceptions require authority/evidence and cannot waive source, owner, lock, Final Script, or reaction-separation law.

`CampaignAxisPortfolio` contains one `AxisCoverageEvidence` for each required axis: role, tension, direction, Edge, Primitive coalition/signature, archetype coalition, linguistic structure, visual operator, format/profile, stance, pressure/relief, relationship movement, and source reuse where applicable. Each evidence record lists exact entry refs, canonical axis values, counts/window, distinctness proof, repetition findings, exclusions, and policy result. A wording-only difference cannot prove semantic diversity.

### `ActivationFreshnessProfile`

Schema ID: `ca.air.activation-freshness-profile/2.1.0-candidate`.

| Field | Type | Rule |
|---|---|---|
| `profile_ref` | `ImmutableRef` | AIR; immutable context snapshot. |
| `audience_context_ref`, `platform_profile_ref` | exact refs | Required scope; no global reuse without compatibility proof. |
| `window` | `ObservationWindow` | Caller-supplied cutoff/start/end and policy/timezone basis. |
| `taxonomy_ref`, `freshness_policy_ref` | exact refs | Defines patterns, windows, thresholds, scoring/decision rules. |
| `exposure_records` | tuple of `PatternExposureRecord` | Exact asset/publication/sequence/evidence refs and observed/unknown reach. |
| `dimension_findings` | tuple of `FreshnessDimensionFinding` | Structure, inversion, visual, role, tension, Edge, coalition, archetype, format, direction, relationship, pressure/relief, source reuse. |
| `qualitative_signal_refs` | tuple of refs | Attributable human/evaluator/platform evidence; not bare strings. |
| `available_patterns`, `limited_patterns`, `exhausted_patterns` | tuples of typed decisions | Each decision is context/window/profile specific and evidence-linked. |
| `unknown_dimensions` | tuple of `UnknownFinding` | Missing/ambiguous evidence with next admissible action. |
| `profile_evaluation_receipt_refs` | tuple of refs | Independent findings; no single scalar is required. |

`PatternExposureRecord` contains `{pattern_key, dimension, canonical_value_ref, asset_ref, campaign_ref, publication_receipt_ref, audience_context_ref, platform_profile_ref, exposure_window, observed_reach, denominator, distribution_mode, evidence_refs, measurement_limits}`. `observed_reach` may be `UNKNOWN_WITH_REASON`; it is never silently zero.

`FreshnessDimensionFinding` contains `{dimension, value_ref, finding, budget_used, policy_limit, exposure_count, evidence_completeness, recency_basis, audience_scope, evidence_refs, counterevidence_refs, limitations}` where `finding` is `AVAILABLE`, `LIMITED`, `EXHAUSTED`, `CONFLICTED`, or `UNKNOWN`. Any optional aggregate is profile-defined and cannot compensate for a fatal dimension.

### `PublishingObservationEnvelope` and `AudienceReactionReceipt`

`PublishingObservationEnvelope` schema ID: `ca.pipeline.publishing-observation-envelope/2.1.0-candidate`. Its authoritative payload producer is Pipeline or a declared publishing adapter; AIR stores the exact ref and signature result.

Required fields: `envelope_ref`; `producer_product_or_adapter_ref`; `adapter_version`; `publication_execution_receipt_ref`; `asset_ref`; `campaign_program_ref`; `campaign_asset_plan_ref`; `audience_context_ref`; `platform_profile_ref`; `exposure_window`; `observation_window`; `distribution_mode`; `metric_definition_set_ref`; `metric_observations`; `sampling_and_filtering`; `missing_data`; `measurement_limits`; `raw_evidence_refs`; `correction_or_supersedes_ref`; `signature`; `canonical_hash`.

`MetricObservation` is a closed union:

- `COUNT`: nonnegative integer plus population/denominator semantics;
- `RATE`: canonical integer numerator/denominator plus definition ref;
- `DURATION`: integer duration in declared unit plus censoring rules;
- `CATEGORICAL_COUNT`: closed category ref plus integer count;
- `UNKNOWN`: reason code and attempted evidence refs.

Open metric dictionaries and unversioned platform labels are forbidden.

`AudienceReactionReceipt` schema ID: `ca.air.audience-reaction-receipt/2.1.0-candidate`.

Required fields: `receipt_ref`; exact `observation_envelope_refs`; `asset_ref`; `campaign_program_ref`; `campaign_asset_plan_ref`; `audience_context_ref`; `platform_profile_ref`; `exposure_and_observation_windows`; `observed_metric_facts`; `intended_role_tension_direction_and_relationship_refs`; `inferred_role_evidence`; `wrong_role_evidence`; `counteractivation_hypotheses`; `fatigue_hypotheses`; `planned_observed_delta`; `alternative_explanations`; `measurement_limits`; `epistemic_assertions`; `interpreter_ref`; `evaluation_profile_ref`; `independent_evaluation_receipt_refs`; `operator_resolution_ref`; `supersedes_ref`; `canonical_hash`.

The schema explicitly forbids source-domain `reaction_observation_refs`, `reaction_receipt_id`, or `expression_moment_ref` fields as substitutes for audience evidence. It may reference source lineage only to identify the asset's origin, never to claim that audience behavior changed the source reaction.

### `FatigueSignal` and counteractivation assessment

Schema ID: `ca.air.campaign-fatigue-signal/2.1.0-candidate`.

Fields: `signal_ref`; `campaign_program_ref`; `audience_context_ref`; `window`; `signal_type`; `epistemic_state`; `affected_asset_plan_refs`; `affected_axis_values`; `freshness_profile_ref`; `audience_reaction_receipt_refs`; `deterministic_policy_findings`; `judgment_findings`; `evidence_refs`; `counterevidence_refs`; `alternative_hypotheses`; `severity_under_profile`; `fatal_under_profile`; `responsible_layer`; `recommended_revision_operations`; `limitations`; `evaluation_receipt_refs`; `supersedes_ref`; `canonical_hash`.

`signal_type` is one of `DEFENSIVE_REPETITION`, `HABITUATION`, `FORMULA_VISIBILITY`, `ROLE_OVERLOAD`, `EDGE_OVERUSE`, `COALITION_OVERUSE`, `ARCHETYPE_OVERUSE`, `INVERSION_FATIGUE`, `RELIEF_DEFICIT`, `FORMAT_REPETITION`, `MISRECOGNITION`, `PERFORMATIVE_AGREEMENT`, `REACTANCE`, or a registry-governed extension. No signal is inferred solely from a low local engagement value.

### `CampaignRevision`

Schema ID: `ca.air.campaign-revision/2.1.0-candidate`.

Fields: `revision_ref`; `prior_campaign_program_ref`; `trigger_refs`; `failure_attribution_ref`; `revision_scope`; ordered `operations`; `affected_asset_plan_refs`; `preserved_asset_plan_refs`; `frozen_upstream_refs`; `preserved_property_refs`; `invalidated_descendant_refs`; `required_pipeline_reruns`; `expected_effect_assertions`; `limitations`; `rollback_program`; `authority_ref`; `operator_or_human_resolution_ref`; `evaluation_receipt_refs`; `promotion_state`; `successor_campaign_program_ref`; `canonical_hash`.

Allowed operation union:

- `RESEQUENCE {entry_ref, from_index, to_index, reason_refs}`;
- `REPLACE_ASSET_PLAN_REF {old_ref, eligible_successor_ref, reason_refs}`;
- `INSERT_AFFINITY_RESET {after_entry_ref, reset_program, reason_refs}`;
- `ADJUST_ROLE_DIRECTION_MIX {affected_refs, target_policy_findings, reason_refs}`;
- `LOWER_PRESSURE {affected_refs, maximum_new_dose_ref, reason_refs}`;
- `ADD_RELIEF {after_entry_ref, relief_program_ref, reason_refs}`;
- `HOLD_PUBLICATION {affected_refs, hold_condition, release_requirements}`;
- `SPLIT_AUDIENCE_CONTEXT {affected_refs, new_context_refs, evidence_refs}`;
- `RETIRE_PATTERN_FOR_SCOPE {pattern_key, audience_context_ref, window, policy_ref}`;
- `REQUEST_UPSTREAM_REPAIR {responsible_owner, object_ref, failure_code, required_evidence}`.

No operation contains free-form patches. Promotion creates a new program version and never changes a published asset or upstream semantic artifact.

### Primitive applicability, `NOT_APPLICABLE`, and locks

Each active Primitive binding includes exact ID/version/hash, plane/family, local campaign job, trigger/activation evidence, suppression decision, conflicts, misuse modes, affected sequence entries, evaluation result, and source provenance.

- `PRM-PRS-002` local job: verify campaign tension/relief rhythm and prevent unresolved or exhausting repetition.
- `PRM-HUM-021` local job: verify an irony pattern is grounded, legible, resolved, and not fatigued; suppression is required for low literacy or genuine-harm contexts.
- `EXP-TRS-003` local job: verify an eligible status/share function serves the person represented and is voluntary/specific; suppression is required for private/poor-performance/inapplicable contexts.

`NOT_APPLICABLE` is allowed only with a reason code, evidence/authority refs, and applicability-profile rule. It cannot waive required source/owner/Final Script/lock/reaction-separation/diversity-policy fields. An inapplicable Primitive remains visible as a decision, not omitted.

Each asset plan and revision inherits all upstream wrong-reading locks by exact ref/hash. A campaign may add stricter sequence-level locks, such as preventing repeated accusation or forced sharing, but cannot remove/weaken an inherited lock. Relaxation requires a new authorized upstream semantic version.

### Lifecycle, commands, events, receipts, and repository API

Program lifecycle projections: `DRAFT -> COMPILED_PENDING_EVALUATION -> EVALUATED_BLOCKED | EVALUATED_ELIGIBLE -> HANDED_OFF -> ACTIVE_BY_PIPELINE_ACKNOWLEDGEMENT -> SUPERSEDED | INVALIDATED | CANCELLED`. `ACTIVE` describes acknowledged execution context, not production certification or publication success.

Observation/receipt/profile/signal/revision objects have independent immutable lifecycles. Raw observation corrections never mutate prior receipts; they trigger successor interpretations and selective invalidation.

Commands:

- `CompileCampaignActivationProgramCommand`;
- `EvaluateCampaignActivationProgramCommand`;
- `HandoffCampaignProgramCommand`;
- `AcknowledgeCampaignProgramConsumptionCommand`;
- `CompileActivationFreshnessProfileCommand`;
- `AdmitPublishingObservationCommand`;
- `CompileAudienceReactionReceiptCommand`;
- `DetectCampaignFatigueCommand`;
- `ProposeCampaignRevisionCommand`;
- `PromoteCampaignRevisionCommand`;
- `CancelCampaignProgramCommand`;
- `InvalidateCampaignProgramCommand`;
- `ReplayCampaignProgramCommand`.

Every command envelope contains `{command_id, idempotency_key, command_type, aggregate_id, expected_aggregate_version, actor_ref, authority_ref, issued_at, input_refs, canonical_payload_sha256}`. The command records authorization result before semantic execution.

Events include `CampaignProgramCompiled`, `CampaignProgramEvaluated`, `CampaignProgramHandedOff`, `CampaignConsumptionAcknowledged`, `FreshnessProfileCompiled`, `PublishingObservationAdmitted`, `AudienceReactionReceiptCompiled`, `CampaignFatigueDetected`, `CampaignRevisionProposed`, `CampaignRevisionPromoted`, `CampaignProgramCancelled`, `CampaignProgramInvalidated`, and `CampaignProgramSuperseded`.

Receipts name exact inputs/outputs/hashes, command and aggregate versions, producer/evaluator identities, authority, policy/profile refs, gate results, limitations, dependency/invalidation edges, transaction/outbox refs, and decision code. Pipeline consumption acknowledgement is not AIR evaluation or publication authorization.

Repository port methods are transactional `execute(command, expected_version)`, immutable `get(ref)`, `get_by_hash`, `resolve_dependencies`, `current_projection`, `admit_external_observation`, `append_invalidation`, `replay(aggregate_id, through_event)`, and `verify_artifact_receipt_parity`. The in-memory test implementation must satisfy identical atomic/idempotent/concurrency/replay behavior.

### Compatibility and examples

Compatibility negotiation pins exact schema IDs/versions, campaign policy, source kind/profile support, category/format profile set, audience-observation metric definitions, Primitive features, lock inheritance, reaction separation, lifecycle, invalidation, and evaluation capability. Unknown required features fail before handoff. An adapter cannot flatten Edge to prose, map audience receipt to source Reaction Receipt, convert unknown measurement to zero, drop policy rules, weaken locks, or declare local parse success as semantic compatibility.

Positive example: three eligible asset plans use distinct evidence-backed roles/directions and different coalition/Edge geometries, an affinity reset follows two pressure entries, all three Final Scripts are approved, and a profile proves no context-scoped repetition violation. A later platform envelope records exact metrics/limits; AIR infers a limited role finding with alternatives, not a source truth.

Negative example: three paraphrases use different formats and hooks but all assign the audience as accused witness under the same tension, Edge, coalition, and irony inversion. Their local scores are high. The campaign fails the non-compensable role/coalition/inversion repetition gates; format diversity cannot rescue it.

## 7. Implementation stages and exact target paths

These are future implementation targets only. Work requires ratified/current authority and a separately issued Development Capsule with exact paths.

| Stage | Exact future target paths | FR/Story and completion boundary |
|---|---|---|
| 0 - capsule/source lock | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/development-capsules/TS-AIR-013/DEVELOPMENT_CAPSULE.md`; `.../SOURCE_LOCK.yaml`; `.../ALLOWED_PATHS.yaml` | All FRs; required authority/source/upstream/Primitive/policy/profile bytes and owner decisions pinned. |
| 1 - domain models | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/campaign_activation.py`; `.../domain/campaign_freshness.py`; `.../domain/audience_reaction.py`; `.../domain/campaign_revision.py` | FR-073..078; immutable closed objects and invariants. |
| 2 - canonical schemas | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f13.campaign-activation-program.schema.json`; `.../air.f13.activation-freshness-profile.schema.json`; `.../air.f13.audience-reaction-receipt.schema.json`; `.../air.f13.campaign-fatigue-and-revision.schema.json` | All FRs; generated schema/type parity and positive/negative fixtures; no shared release bytes at this stage. |
| 3 - canonicalization/repository | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/serialization/canonical.py`; `.../repositories/campaign_repository.py` | All Stories; deterministic identity, immutable versions, atomicity, idempotency, concurrency, replay. |
| 4 - campaign compilation/diversity | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/campaign_semantic_compiler.py`; `.../validation/campaign_diversity_validator.py` | AIR-FR-073/074, AIR-ST-13.01; exact sequence and non-compensable gates. |
| 5 - freshness | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/freshness_projector.py`; `.../validation/freshness_policy.py` | AIR-FR-075, AIR-ST-13.02; scoped exposure evidence and profile-pinned findings. |
| 6 - observation/reaction | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/publishing_observation_admission.py`; `.../services/audience_reaction_interpreter.py` | AIR-FR-076, AIR-ST-13.02; raw evidence ownership, metric/limit validation, source-reaction separation. |
| 7 - fatigue/revision/evaluation | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/f13_evaluation_port.py`; `.../services/campaign_fatigue_detector.py`; `.../services/campaign_revision_compiler.py` | AIR-FR-077/078, AIR-ST-13.03; independent findings and additive bounded revisions. |
| 8 - lifecycle and adapters | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/campaign_lifecycle_service.py`; `.../invalidation/f13_invalidation_projector.py`; `.../adapters/pipeline_campaign_handoff.py`; `.../projections/studio_campaign_projection.py` | All Stories; owner-safe handoff, acknowledgement, cancellation, invalidation, replay. |
| 9 - migrations | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/migrations/ai_v2_campaign.py`; `.../migrations/ai_v2_freshness.py` | AIR-FR-073/075/076; new immutable artifacts or typed block, never guessed meaning. |
| 10 - evidence | Exact test paths in section 10 | Full behavior, boundary, fault, replay, portability, conformance, and reference-slice evidence. |

No stage may edit Builder behavior, Pipeline/VAE/Delegation product state, current authority, historical receipts, source packages, Final Scripts, canonical schemas outside a separately authorized capsule, or shared contract release bytes. Format 02 remains deferred and VAE Stage 5 remains unauthorized.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Condition | Required behavior |
|---|---|---|
| `AIR_F13_UPSTREAM_DRAFT_DRIFT` | AIR-002/003/005 path, state, bytes, or SHA differs from Wave 3 lock. | Stop affected component; reopen sections 3, 5, 6, 8, 9, 10. |
| `AIR_F13_BUILD_AUTHORITY_ABSENT` | Build/capsule requested while candidate remains unratified. | Deny and preserve specification-only state. |
| `AIR_F13_REQUIRED_LINEAGE_MISSING` | Source/context/Matrix/hypothesis/coalition/Edge/archetype/Final Script/derivative/policy/profile ref absent or stale. | Reject before ranking and name responsible owner/ref. |
| `AIR_F13_UNSUPPORTED_DERIVATIVE_ROUTE` | Opportunity lacks source/category/profile/Harness eligibility. | Exclude with receipt; unrelated eligible entries continue. |
| `AIR_F13_ROLE_TENSION_MISSING` | Asset communicates topic but no approved psychological role inside tension. | Reject asset plan/campaign eligibility. |
| `AIR_F13_DIVERSITY_POLICY_FAILED` | Required role/direction/tension/Edge/coalition/archetype/structure/format/relief rule fails. | Hard block; local score cannot compensate. |
| `AIR_F13_CENTROID_VARIATION` | Wording/format differs but semantic axes remain the same. | Count as repetition, not diversity. |
| `AIR_F13_UNRESOLVED_TENSION` | Sequence raises pressure without commensurate relief/reset/stop. | Reject under PRM-PRS-002. |
| `AIR_F13_MICRO_TENSION_EXHAUSTION` | Sequence oscillates too rapidly under pinned policy. | Reject/revise under PRM-PRS-002. |
| `AIR_F13_IRONY_INAPPLICABLE_OR_FATIGUED` | Irony lacks subtext/conviction, is harmful/illegible, or repeats beyond policy. | Suppress/reject under PRM-HUM-021. |
| `AIR_F13_FORCED_OR_GENERIC_STATUS_SHARE` | Share is transactional, generic, humiliating, private-loop, or required for progress. | Reject under EXP-TRS-003. |
| `AIR_F13_FRESHNESS_SCOPE_MISMATCH` | Profile audience/platform/window is applied outside compatibility envelope. | Reject; compile a new scoped profile. |
| `AIR_F13_FRESHNESS_EVIDENCE_UNKNOWN` | Required exposure/denominator/history is missing or ambiguous. | Record unknown/limited; never zero or fresh. |
| `AIR_F13_OBSERVATION_PROVENANCE_INVALID` | Envelope signature/producer/asset/publication/context/window/metric definition invalid. | Reject raw admission without semantic receipt. |
| `AIR_F13_AUDIENCE_SOURCE_REACTION_CONFUSION` | Audience evidence is mapped to Interview Expression Reaction Receipt/Expression Moment or vice versa. | Reject with authority/epistemic boundary receipt. |
| `AIR_F13_MEASUREMENT_LIMITS_MISSING` | Audience receipt omits required denominator/distribution/filter/window/definition/limits. | Reject interpretation or constrain it to typed unknown. |
| `AIR_F13_CAUSAL_OVERCLAIM` | Correlational audience metrics represented as causal semantic truth. | Reject evaluation; preserve observed facts and alternatives. |
| `AIR_F13_FATIGUE_UNATTRIBUTED` | Signal has no affected axes/evidence/counterevidence/alternatives/responsible layer. | Reject signal. |
| `AIR_F13_REVISION_SCOPE_OVERREACH` | Revision patches source/Final Script/derivative/published output or unrelated entries. | Reject; issue upstream repair request or narrower revision. |
| `AIR_F13_PARENT_LOCK_WEAKENED` | Campaign/adapter/revision drops or weakens inherited lock. | Reject; require authorized upstream successor to relax. |
| `AIR_F13_EVALUATOR_NOT_INDEPENDENT` | Producer and evaluator identity/authority collapse. | Reject receipt; no eligibility/revision promotion. |
| `AIR_F13_PIPELINE_SEMANTIC_MUTATION` | Pipeline handoff/ack changes AIR semantic fields. | Reject acknowledgement and identify changed hashes. |
| `AIR_F13_COMPATIBILITY_UNSUPPORTED` | Consumer cannot enforce a required semantic feature/profile/lifecycle/lock/observation rule. | Reject before handoff; parser success is insufficient. |
| `AIR_F13_IDEMPOTENCY_CONFLICT` | Same key, different canonical payload. | Return conflict; commit nothing. |
| `AIR_F13_CONCURRENT_MODIFICATION` | Expected aggregate version differs from current. | Reject atomically and require reload/new command. |
| `AIR_F13_ATOMIC_COMMIT_FAILED` | Any staged artifact/edge/command/event/receipt/outbox write fails. | Roll back entire transaction; no orphan state. |
| `AIR_F13_CANCELLED_OR_STALE` | New handoff/revision targets cancelled, superseded, revoked, or invalidated version. | Deny current action; historical replay remains. |
| `AIR_F13_MIGRATION_MEANING_MISSING` | Legacy record cannot prove mandatory owner/lineage/policy/measurement semantics. | Preserve legacy bytes and block; never infer. |
| `AIR_F13_ABSOLUTE_PATH_CONTAMINATION` | Canonical bytes contain local machine path. | Reject serialization and name field. |

### Retries, quality repair, cancellation, and late results

Infrastructure retry uses the original command/idempotency key and frozen inputs. Quality repair uses a new command and immutable candidate version tied to failed receipt/failure attribution. A worker crash after commit returns the original receipt through idempotency lookup. A cancellation racing with compilation is ordered by aggregate stream version: the first committed command wins; the loser receives a typed current-state conflict. Cancellation never deletes previously published history.

Late observations for an actually published historical asset may be admitted with their true observation window and campaign version even after current supersession/cancellation. They update only a successor evidence/profile projection and cannot reactivate the old campaign, alter source truth, or rewrite the earlier evaluation.

### Migration and compatibility

The V2 campaign adapter preserves legacy campaign/asset order, source refs, roles, directions, Edge text as legacy evidence, format, numeric policy values, reset indices, evaluation ref, original example bytes, and predecessor algorithm/version. It emits a V2.1 object only if exact owners, source kind/provenance, audience context, role/tension refs, coalition/signature/Edge refs, archetype/Final Script refs, derivative/transfer refs, policy/profile semantics, locks, and lifecycle evidence can be supplied attributably.

The V2 freshness adapter preserves each hard-coded input and computed float as a legacy algorithm result. It does not translate `0.35` or the 30-day formula into current policy truth. Current profile findings are recomputed only from exact admitted evidence under a pinned current profile. Deprecated schemas remain readable for historical replay but cannot become current through parsing alone.

### Rollback, recovery, invalidation, and replay

Fault injection after each stage of the atomic bundle must prove zero partial artifacts/receipts/edges/outbox records. A failed service/model/profile/registry deployment rolls back the runtime binding while retaining every incident and output produced under the failed version. Rollback does not rewrite semantic history.

Invalidation begins at the exact changed parent and traverses dependency edges. A corrected metric envelope invalidates dependent audience receipts, fatigue signals, and revision candidates but not source/Final Script bytes. A corrected source/Final Script invalidates campaign entries and Pipeline descendants that use it but not unrelated campaign entries. Revocation blocks new use immediately while historical hashes remain resolvable.

Replay loads the exact command inputs, policies, profiles, registries, adapter versions, external observation bytes, and event sequence stored for that historical run. It reproduces artifact and receipt hashes in a clean process. Current platform values, current time, live APIs, random state, local environment, and absolute paths are never required.

### Observability and degraded behavior

Structured telemetry records command/trace IDs, aggregate/version, actor/authority IDs, input/output hashes, policy/profile/schema versions, source/audience/platform logical refs, axis coverage and hard-gate codes, Primitive applicability/misuse, freshness scope/evidence completeness, observation admission/correction, metric definition IDs (not sensitive payload), inference/evaluation codes, fatigue signal types, revision operation types, idempotency/concurrency/transaction outcome, handoff/ack status, invalidation count/cause, and replay result.

Logs redact source contents, audience/user identifiers beyond governed pseudonymous refs, raw comments/messages, secrets, prompts, and platform tokens. They exclude absolute machine paths and unbounded model output. Metrics may aggregate lifecycle/failure codes and latency but cannot become canonical evidence or a certification claim.

When an evaluator, platform adapter, or evidence source is unavailable, compilation may stop at the last truthful non-eligible state. The system may preserve a candidate program/profile/receipt request with a typed blocker; it may not substitute a hidden provider, assume no reaction, mark the campaign fresh, or publish.

## 9. Behavior-specific acceptance criteria

| AC | Governing FR / Story | Given / When / Then pass condition | Concrete failure example | Evidence / test layer |
|---|---|---|---|---|
| AC-01 | AIR-FR-073 / AIR-ST-13.01 | Given exact current source, audience, F02/F03/F05, approved Final Script, derivative and policy refs, when compile runs, then every ordered asset plan preserves audience, role, tension, direction, Edge, coalition/signature, archetype, format, relationship movement and source lineage. | Campaign uses copied slogans and an Edge text with no refs; `AIR_F13_REQUIRED_LINEAGE_MISSING`. | program + compilation receipt; integration/contract |
| AC-02 | AIR-FR-073 / AIR-ST-13.01 | Given several eligible routes, when one route lacks current category/profile or source support, then it is excluded with reason while unrelated routes remain candidates. | Compiler manufactures a fit because the topic resembles an archetype; `AIR_F13_UNSUPPORTED_DERIVATIVE_ROUTE`. | exclusion receipt; unit/integration |
| AC-03 | AIR-FR-074 / AIR-ST-13.01 | Given policy requiring role/direction/Edge/coalition diversity, when whole-sequence validation runs, then each axis has evidence and all fatal repetition constraints pass before local ranking. | Three high-score assets repeat accused-witness/regret/same coalition; hard fail despite high average. | axis portfolio/policy receipt; property/integration |
| AC-04 | AIR-FR-074 / AIR-ST-13.01 | Given different wording and formats over identical semantic geometry, when distinctness is computed, then they count as repetition, not diversity. | Hook paraphrases are counted as three fresh roles; `AIR_F13_CENTROID_VARIATION`. | canonical axis vectors; property |
| AC-05 | AIR-FR-075 / AIR-ST-13.02 | Given exact publication/exposure history for one audience/platform/window, when profile compiles, then every pattern finding names asset/evidence/policy/scope and unknowns remain explicit. | Missing denominator is converted to zero reach and pattern marked fresh; `AIR_F13_FRESHNESS_EVIDENCE_UNKNOWN`. | profile + evidence-completeness receipt; unit/contract |
| AC-06 | AIR-FR-075 / AIR-ST-13.02 | Given the same pattern under a different audience context, when prior profile is proposed, then compatibility is required or a new profile is compiled. | One segment's irony fatigue globally retires Irony Inversion; `AIR_F13_FRESHNESS_SCOPE_MISMATCH`. | compatibility denial; contract |
| AC-07 | AIR-FR-076 / AIR-ST-13.02 | Given a signed platform envelope tied to exact published asset/context/windows/metric definitions/limits, when admitted and interpreted, then observed facts and inferred audience-role findings remain separate. | Free-form metrics with no denominator or adapter version become a pass receipt; reject. | observation/admission and reaction receipts; integration |
| AC-08 | AIR-FR-076 / AIR-ST-13.02 | Given audience observations for an interview-derived asset, when receipt compiles, then it cannot use/overwrite the source Reaction Receipt or Expression Moment schema/owner. | Audience likes are represented as guest Reaction Receipt evidence; `AIR_F13_AUDIENCE_SOURCE_REACTION_CONFUSION`. | authority denial; architecture/contract |
| AC-09 | AIR-FR-076 / AIR-ST-13.02 | Given mixed paid/organic exposure, missing cohort data, or platform definition drift, when interpretation runs, then limitations/unknowns/alternative explanations constrain claims. | Engagement difference is asserted causal semantic truth; `AIR_F13_CAUSAL_OVERCLAIM`. | evaluation receipt; adversarial evaluator |
| AC-10 | AIR-FR-077 / AIR-ST-13.03 | Given profile, receipts and policy, when fatigue detection runs, then defensive repetition, habituation, formula visibility, role overload, Edge/coalition/archetype overuse and relief deficit are distinct evidence-linked signals. | Low views alone create `HABITUATION`; `AIR_F13_FATIGUE_UNATTRIBUTED`. | fatigue signals; unit/evaluator |
| AC-11 | AIR-FR-077 / AIR-ST-13.03 | Given repeated tension without relief, when sequence evaluates, then PRM-PRS-002 hard gates block unresolved/micro-tension exhaustion. | Every asset escalates pressure and no reset/relief exists; campaign remains ineligible. | Primitive applicability/evaluation; CBAR |
| AC-12 | AIR-FR-075/077 / AIR-ST-13.02/03 | Given Irony Inversion entries, when applicability/freshness checks run, then subtext, conviction, literacy/harm context, resolution and sustained-fatigue constraints are enforced. | Emoji-marked sarcasm or repeated irony is treated fresh; `AIR_F13_IRONY_INAPPLICABLE_OR_FATIGUED`. | Primitive fixture; CBAR/evaluator |
| AC-13 | AIR-FR-077/078 / AIR-ST-13.03 | Given a status-share route, when EXP-TRS-003 checks run, then it requires a supported win/identity signal, specific asset, voluntariness, and applicable context. | Sharing unlocks next step or uses generic stock/status marketing; reject. | experience-Primitive receipt; contract/evaluator |
| AC-14 | AIR-FR-078 / AIR-ST-13.03 | Given one evidence-backed fatigue signal affecting two entries, when revision compiles/promotes, then only those sequence/plan decisions receive new versions and all other/published history remains exact. | Service rewrites source/Final Script or every campaign entry; `AIR_F13_REVISION_SCOPE_OVERREACH`. | revision/impact/invalidation receipts; integration/recovery |
| AC-15 | AIR-FR-078 / AIR-ST-13.03 | Given a defect belongs to source, coalition, Final Script, derivative program or Pipeline execution, when revision is requested, then F13 emits `REQUEST_UPSTREAM_REPAIR` to the exact owner. | F13 silently repairs another owner's object; authority denial. | failure-attribution receipt; architecture |
| AC-16 | all / all Stories | Given producer and evaluator identities, when evaluation is recorded, then they are distinct and the exact profile/hash is present. | Compiler self-passes campaign based on local score; `AIR_F13_EVALUATOR_NOT_INDEPENDENT`. | evaluation boundary receipt; architecture |
| AC-17 | all / all Stories | Given a current evaluated program, when handed to Pipeline, then Pipeline acknowledges exact hashes/features and compiles a distinct operational batch object. | Pipeline changes AIR role/Edge or reuses AIR ID as execution job; `AIR_F13_PIPELINE_SEMANTIC_MUTATION`. | producer/consumer conformance; cross-product |
| AC-18 | all / recovery | Given identical input in two clean processes with shuffled set/map/traversal order and different roots/env/time/random, then canonical artifacts/receipts match byte-for-byte. | A current timestamp, float, dict order, or absolute path changes hash. | golden vectors; property/clean-room |
| AC-19 | all / recovery | Given retry/concurrent/fault scenarios, then identical retry returns original receipt, conflicting retry/version is typed, and every injected commit failure leaves no partial state. | Artifact stored without command/receipt or receipt without artifact. | transaction parity/fault traces; repository |
| AC-20 | AIR-FR-078 / recovery | Given upstream or observation correction, when invalidation runs, then only dependent current projections are stale and historical program/profile/receipt/revision bytes replay. | Unrelated campaign invalidated or prior evidence deleted. | dependency graph/replay hashes; recovery |
| AC-21 | migration | Given complete V2 evidence, when migration runs, then a new immutable V2.1 object preserves original bytes/algorithm and supplies current meaning; otherwise it blocks. | Legacy 0.35 fatigue score becomes current truth or missing audience/source kind is guessed. | migration receipt/blocker; migration |
| AC-22 | governance | Given this writer result, when factory validation runs, then state is `WRITTEN_PENDING_AUDIT`, authority candidate, build false, no capsule/code/schema/release. | Any production/certification/Format 02/VAE Stage 5 claim fails. | writer receipts; governance |

## 10. Testing and completion evidence

### Required future test suites

| Exact future path | Named coverage |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_campaign_activation_program.py` | Complete AIR semantic program/asset plans, exact refs/owners, role/tension, contiguous sequence, locks, source scope, no Pipeline object collapse. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_campaign_diversity.py` | Every axis, adjacency/window, minima/maxima, non-compensability, paraphrase/format centroid denial, policy versioning. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_campaign_freshness.py` | Scoped profiles, exposure records, unknowns, policy windows, fixed-point findings, context compatibility, no universal score. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_audience_reaction_receipt.py` | Raw/derived separation, metric union, denominators, windows, limits, corrections, causal denial, source-reaction schema prohibition. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_campaign_fatigue_signal.py` | All signal types, attribution, evidence/counterevidence/alternatives, profile severity, low-view-only denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_campaign_revision.py` | Closed operations, exact affected/preserved sets, upstream repair request, rollback, no free patch, additive successor. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_f13_primitive_applicability.py` | Exact PRM-PRS-002, PRM-HUM-021, EXP-TRS-003 hashes, triggers/suppressions/misuse/conflicts and typed N/A. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_f13_lock_inheritance.py` | Exact parent union, stricter sequence locks, weaken/remove denial, upstream-only relaxation. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/property/test_f13_canonical_serialization.py` | Unicode/key/set/order, fixed point, clock/random/env/locale/path independence and stable hashes. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/repository/test_campaign_repository.py` | Immutable versions, command/artifact/receipt/outbox parity, idempotency, optimistic concurrency, replay. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/fault_injection/test_f13_atomic_commit.py` | Failure after each artifact/edge/command/event/receipt/outbox stage leaves no residue. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_campaign_compilation_and_evaluation.py` | AIR-FR-073/074 and AIR-ST-13.01 end-to-end, exclusions, non-compensable gates, evaluator separation. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_freshness_and_audience_reaction.py` | AIR-FR-075/076 and AIR-ST-13.02, scoped histories, platform envelopes, corrections, measurement limits, reaction separation. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_campaign_fatigue_and_revision.py` | AIR-FR-077/078 and AIR-ST-13.03, signal alternatives, bounded revision, upstream repair, promotion, history. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_campaign_invalidation_and_replay.py` | Parent-specific invalidation, cancellation/late observations, preserved published evidence, historical byte reproduction. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_pipeline_campaign_handoff.py` | Exact semantic features, profile/lock/lifecycle support, distinct Pipeline batch/job identity, acknowledgement, stale rejection. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_publishing_observation_admission.py` | Signatures, producer/version, metric definitions, denominator, paid/organic/unknown, windows, correction/supersession. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_f13_evaluation_boundary.py` | Distinct producer/evaluator, profile pin, no self-pass, unavailable/disagreement state, no certification inference. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_f13_product_boundaries.py` | AIR campaign meaning, Pipeline execution/observations, Interview source reaction, evaluator, Studio, Builder, VAE, Delegation, publishing adapter. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_ai_v2_campaign.py` | Complete fixture migration and all missing owner/lineage/policy cases blocked without invention. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_ai_v2_freshness.py` | Legacy formula/float retained only as evidence; no current-profile promotion without exact data/policy. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_interview_source_to_campaign.py` | Exact Interview Expression source lineage into AIR campaign without confusing source Reaction Receipt and audience receipt. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/clean_room/test_f13_portability.py` | Fresh-process and different-root reproduction, no absolute paths/hidden files/environment/network dependency. |

### Required adversarial and recovery matrix

Future fixtures cover: stale source/context/Matrix/hypothesis/coalition/Edge/Final Script/derivative/profile; unsupported route; topic-only archetype; copied Edge text; role/tension missing; high local scores with repeated role/direction/Edge/coalition/archetype; wording-only and format-only variation; unresolved tension; micro-tension exhaustion; irony without subtext/conviction; low-literacy/harmful irony; sustained irony fatigue; generic/overt/forced/private/poor-performance status share; missing exposure; ambiguous audience; cross-context profile reuse; unknown denominator; metric definition drift; mixed paid/organic exposure; invalid signature; observation correction; audience/source reaction collision; correlation-as-causation; low-views-only fatigue; fatigue without alternatives; upstream defect misrepaired locally; over-broad revision; producer self-evaluation; unsupported Pipeline feature; semantic mutation on handoff; parent-lock removal; invalid N/A; duplicate command conflict; concurrent revision; cancellation race; late result; partial failure at every commit boundary; orphan artifact/receipt; invalidation overreach/underreach; replay after registry/policy/platform changes; guessed migration; float/order/time/random/environment/path contamination; unauthorized capsule/build/production/Format 02/VAE Stage 5 claim.

### Completion evidence contract

An eventual implementation may be declared technically complete for independent review only with:

1. ratified/current authority and a separately authorized TS-AIR-013 Development Capsule;
2. exact source/upstream/Primitive/policy/profile hash locks and generated schema/type parity manifests;
3. all unit, property, contract, integration, architecture, migration, fault-injection, replay, clean-room, and affected regression suites tied to exact code/artifact hashes;
4. full suite twice in fresh processes, Python compilation/type checks, and canonical golden vectors reproduced under a different workspace root;
5. command/event/artifact/receipt/outbox parity and rollback evidence for every injected boundary;
6. Independent Evaluation receipts proving distinct identities and profile versions without production/certification overclaim;
7. Pipeline producer/consumer and publishing-observation conformance receipts, including source/audience reaction separation and semantic non-mutation;
8. selective invalidation and historical replay evidence across source, Final Script, policy, observation correction, fatigue, and revision cases;
9. migration receipts/blockers proving no guessed owner/source/audience/policy/measurement/lineage semantics;
10. an implementation completion receipt whose claim ceiling remains separate from publication, audience effectiveness, production, provider, release, and certification authority.

The writer evidence for this document is limited to the V3.3 spec-writing receipt, files-read receipt, source traceability, draft-dependency receipt, and writer file manifest. The next lifecycle step is independent audit by a different agent. No audit, revision, acceptance, implementation, schema generation, capsule, build, shared release, publication, production, or certification work is performed here.
