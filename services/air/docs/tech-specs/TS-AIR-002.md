---
type: technical_specification
spec_id: TS-AIR-002
title: Identity, Context, Resonance, and Matrix of Edging
product: Activative Intelligence Runtime
version: 2.1.0-candidate
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
document_class: CANDIDATE_CANONICAL_TECH_SPEC
output_path_class: DIRECT_PRODUCT_SPEC_PATH
gate: GATE_B_SEMANTIC_IDENTITY_AND_CONTEXT
writing_wave: 1
controlling_frs:
  - AIR-FR-007
  - AIR-FR-008
  - AIR-FR-009
  - AIR-FR-010
  - AIR-FR-011
  - AIR-FR-012
controlling_stories:
  - AIR-ST-02.01
  - AIR-ST-02.02
  - AIR-ST-02.03
upstream_draft_dependency:
  spec_id: TS-AIR-001
  quality_state: WRITTEN_PENDING_AUDIT
  sha256: 622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc
  label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-002 — Identity, Context, Resonance, and Matrix of Edging

This candidate specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`; this document neither adopts the candidate as current authority nor authorizes implementation, build, production, certification, or a Development Capsule.

`TS-AIR-001` is consumed only as a hash-pinned `WRITTEN_PENDING_AUDIT` interface draft and is therefore labeled `DRAFT_DEPENDENCY_NOT_ACCEPTED`. It is not represented as ratified or accepted authority. A change to its pinned bytes reopens the downstream revision-impact sections named in section 1.

## 1. Files and authorities read

| Authority class | Exact path | Version/state | SHA-256 | Use |
|---|---|---|---|---|
| Candidate constitutional authority | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `2.1.0-draft`, pending ratification | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Product sovereignty, evidence ceilings, identity continuity, semantic lineage, immutable history, and lifecycle law. |
| Candidate authority pointer | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CURRENT_AUTHORITY.md` | `DRAFT_FOR_HUMAN_RATIFICATION` | `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Confirms that the candidate is not current authority and that implementation authorization is separate. |
| Controlling PRD feature | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/prd/features/F02-identity-context-resonance-and-matrix-of-edging.md` | `2.1.0-draft` | `7f12a98c877def64cac4b6ff6d5c7bd255674e249c0c8d79dd2cfc15af4f8318` | AIR-FR-007 through AIR-FR-012 and F02 failure expectations. |
| Controlling Stories | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | `2.1.0-draft` | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-02.01 through AIR-ST-02.03, acceptance, adversarial, recovery, and evidence expectations. |
| Source draft/assignment | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-002-identity-context-resonance-and-matrix-of-edging.md` | `DRAFT_AFTER_PRD_PENDING_RATIFICATION` | `c3522186cd471fc820e39efbf38e39ab4f7d0ea8ea28166c81e54af76133fd01` | Candidate design input reconciled to current Program Control ownership. |
| Upstream interface draft | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-001.md` | `WRITTEN_PENDING_AUDIT`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | `622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc` | Typed immutable references, epistemic assertions, semantic object versions, commands, receipts, blockers, hashing, and lifecycle semantics. |
| Dispatch lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_01_DISPATCH_LOCK.yaml` | Wave 1 dispatched | `2fa4102de472196fb05320e675ad6095316689e7c585bcba42f432f59ed98692` | Pins the upstream F01 draft and authorizes this one-spec execution. |
| Cross-product authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | AIR owns semantic lifecycle and production-program meaning; Interview Expression owns live evidence. |
| Semantic ownership | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | Resolves local-source ownership conflicts without transferring human or product sovereignty. |
| Source disposition | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | validated | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Admits required unique evidence and excludes unavailable optional references from factual support. |
| Specification-work authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active, specification only | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes writing and technical review, not build. |
| Authority-stage decision | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | ratification pending | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Sets `CANDIDATE_NOT_CURRENT` and the pre-ratification acceptance ceiling. |
| Required unique evidence | `.../sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | `SRC-INT-001` | `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | Human-truth, interviewer-resonance, source-package, and Expression Moment lineage. |
| Required unique evidence | `.../sources/doctrine/CCP_V9_1_EXPRESSION_CAPTURE_ARCHETYPE_ROUTING.md` | `SRC-INT-002` | `58e92fee3f9486ab524d1229c4759566f760b6cc91472aff279e457b0b52482b` | Evidence-preserving source capture and archetype-routing doctrine. |
| Required unique evidence | `.../sources/doctrine/MATRIX_OF_EDGING.md` | `SRC-MOE-001` | `7ba1858cd9238a63f32d28e9cc8e7bbe306ba82ac5fa5af4a0346128aa3b6ebb` | Broad-first matrix construction, survival, coalition, routeability, and anti-centroid laws. |
| Required unique evidence | `.../sources/doctrine/CCP_CMF_BRAND_GENESIS_AND_MICRO_SEMIOTIC_PIPELINE_V3.md` | `SRC-BRAND-001` | `61710fe56484b569ce28ddefadbb4c8047e9ae48cadf25291423cf4f200e3dcb` | Versioned brand context, identity evidence, source traceability, and operator confirmation. |
| Required unique evidence | `.../sources/doctrine/RSCS_RECURSIVE_SIGNAL_COMPRESSION_SYSTEMS.md` | `SRC-RSCS-001` | `bb8ebfcd5c519649b4363731cf11434ce600c71fb5e1d020abb59cbb51b8a330` | Saturation, collision, compression, evaluation, and recursive improvement without premature compression. |
| Required unique evidence | `.../sources/doctrine/CCV_COMBINATORIAL_CONTROLLED_VARIATION.md` | `SRC-CCV-001` | `0869ff50e4bdaba3dc1854183100826d0de9568b9ed5558bf68b4590834a62c4` | Axis-labelled controlled variation bounded by evidence and semantic invariants. |
| Primitive | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-001.yaml` | `PRM-PSY-001` | `77c09b403aca66e77b2c71b1faa4dbeacd410d9d6c69685f9c2222dc65bf8ca7` | Matching the practical, emotional, and social layer without performative matching. |
| Primitive | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-008.yaml` | `PRM-PSY-008` | `1f63263ab6e0178e3c62feda7bfc5951ea02f1dd8bdafa96b15efd0a0381cfeb` | Attack the problem, not the person; avoid passive aggression and toxic positivity. |
| Primitive | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/persuasion_reasoning/PRM-PRS-015.yaml` | `PRM-PRS-015` | `b05b6aabef1d48f0a3bf07f5b4a43febe2fb53445df5e1a8524a6ba0f78f48d5` | Balance what is with what could be without exaggerating either. |
| Studio predecessor | `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/brand_genesis.py` | predecessor | `c5a46f4c3009ca576e3d62542461d07f998c408e5f308dd5fb81d73488710238` | Existing Brand Genesis objects and portability gaps. |
| Studio predecessor | `THE_CMF_STUDIO(2)/src/ccp_studio/services/brand_genesis_service.py` | predecessor | `276e6b1648383a185dff2c1955ecab36e134118c33bcdf11f083f684e6d7e89c` | Existing session workflow and non-atomic behavior. |
| Studio predecessor | `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/matrix.py` | predecessor | `a7adb287f51c63ba787b941a887ae0952009557fd355119531c9b84a06e22222` | Existing matrix fields and untyped/open structures. |
| Studio predecessor | `THE_CMF_STUDIO(2)/src/ccp_studio/services/matrix_service.py` | predecessor | `c4f1e1f6781d8e8fdd41bb05ba4209b6a04743a6cec43e3dbcd138aab888a914` | Compile/evaluate/approve coupling and missing independence. |
| Studio predecessor | `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/matrix.py` | predecessor | `9bee1a5788531f3c2f283a2c6f7ae2e2111d21818c217f4432331d3bdc1fc959` | In-memory overwrite behavior and receipt gaps. |
| Studio test evidence | `THE_CMF_STUDIO(2)/tests/test_brand_genesis_service.py` | predecessor | `f8eea24891d428fa5230f1bc11130f0797a20b1c61a33f7edcc7e9e220af9cde` | Existing identity/source workflow expectations. |
| Studio test evidence | `THE_CMF_STUDIO(2)/tests/test_matrix_service.py` | predecessor | `076fd8fd4d87d0527ba261f38ea6da06a2fd39ac94cddc82bed958601c912df1` | Existing primitive, unsupported-tension, and downstream-packet behavior. |

The `...` paths in source, Primitive, and AIR rows expand beneath `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE`. The F02 PRD is subordinate where its local ownership table conflicts with the current Program Control candidate ownership matrices: authorized humans own canonical Identity DNA values; AIR owns compiled Context Premise, Resonance/Matrix, and Edge Product meaning; Interview Expression owns live Reaction Observation, Reaction Receipt, Expression Moment, and Canonical Source Package evidence.

The upstream F01 draft controls the interface assumptions used in sections 3, 5, 6, 8, 9, and 10. Any upstream byte change invalidates that pin and requires revision-impact review of all six sections before this draft can advance.

## 2. Problem, user outcome, solution, and scope

### Problem and outcome

Without a governed F02 boundary, identity may be inferred from a single expression, audience context may become generic demographic copy, interviewer resonance may be detached from evidence, and a Matrix of Edging may collapse into topic similarity or aesthetic mood. The operator instead needs a reproducible semantic compilation that binds the exact human-authorized identity and brand context to evidence-backed audience, relationship, interviewer-resonance, Primitive, and objective inputs, then produces a broad signal and an Edge Product whose lineage can be inspected and invalidated.

### Bounded solution

Implement an immutable F02 semantic compiler that:

1. resolves exact, versioned Identity DNA, Brand Genesis, Brand Context Version, Voice DNA, and Visual DNA references without mutating human-owned canonical values;
2. compiles a versioned Audience Context Premise containing situation, self-perception, pressure, desired movement, probable defenses, and relationship stage;
3. incorporates interviewer lived stake, curiosity, recognition, and current relationship context only when attributable and material;
4. constructs a broad Matrix signal before ranking any edge;
5. binds exact Primitive versions, hashes, compatibility, misuse constraints, coalition signatures, and independent evaluation evidence;
6. emits only Edge Product candidates that survive source-evidence, identity-fit, counteractivation, planned-versus-observed, and routeability checks; and
7. proposes evidence-linked Identity DNA candidate observations without changing canonical Identity DNA.

### In scope

- typed immutable references and F02 semantic objects;
- identity and brand-context resolution;
- audience, interviewer-resonance, and relationship compilation;
- broad-signal, tension-site, Primitive-binding, candidate-survival, coalition, and Edge Product compilation;
- independent semantic evaluation and deterministic receipts;
- canonical serialization, SHA-256 identities, optimistic concurrency, idempotency, atomic commit, invalidation, replay, and historical reproduction;
- migration/adaptation of named Studio predecessor records without granting them AIR authority;
- typed F02 handoff to later AIR features.

### Out of scope and non-goals

- human ratification, build authority, implementation, production, or certification;
- editing Identity DNA, Brand Context, Voice DNA, or Visual DNA canonical values;
- live interview capture or ownership of Reaction Observations, Reaction Receipts, Expression Moments, or source packages;
- rebuilding Primitive definitions, archetypes, Final Scripts, Visual Asset Demands, Composition Intent, or visual-production decisions;
- Pipeline execution, VAE realization, Studio canonical ownership, or Delegation transport;
- creating generic creative-safety or content-rights approval authority; operator-supplied source authority, provenance, lineage, approvals, and product sovereignty remain intact;
- treating a confidence score as permission to invent absent source classification or human evidence;
- activating Format 02 or VAE Stage 5.

## 3. Governing decisions and constraints

1. **Ownership is field-specific.** Authorized humans own canonical Coach/Guest Identity DNA values and operator-supplied source authority. AIR may resolve, bind, compare, and propose evidence-linked candidate observations; it may not mutate canonical identity. Interview Expression owns live reaction evidence. AIR owns compiled Context Premise, Resonance/Matrix, and Edge Product meaning.
2. **F01 is a draft interface, not accepted authority.** All F01-shaped references and assertions in this document are contingent on the exact pinned bytes. Their use must retain `DRAFT_DEPENDENCY_NOT_ACCEPTED` in receipts and downstream metadata until F01 reaches a later accepted state.
3. **Meaning precedes scoring.** The Matrix starts with broad source, identity, audience, relationship, and objective signals. Ranking may order surviving candidates; it may not manufacture candidates that were absent from the broad signal.
4. **Evidence ceilings are non-compensable.** High model confidence, Primitive fit, or operator urgency cannot compensate for missing source evidence, stale identity refs, unsupported relationship claims, or a missing planned/observed epistemic distinction.
5. **Identity continuity is exact.** Every compilation binds the profile identifier, object version, content hash, authority ref, Brand Context Version, and Voice/Visual DNA references that were valid for that command. `latest` and mutable aliases are forbidden in stored compilations.
6. **Context is an attributable premise, not a fact claim.** Each audience, interviewer, and relationship assertion carries its epistemic state, evidence refs, confidence in integer micros, validity window, and consequence if wrong. Unknown values remain unknown; they are not guessed.
7. **Interview resonance is conditional.** Interviewer resonance is included only when evidence shows it is material to the audience relationship, source meaning, or activation objective. Live reaction evidence is referenced, never re-owned or reconstructed by AIR.
8. **Primitive use is exact and governed.** Each binding records Primitive ID, version, hash, local job, activation/suppression conditions, misuse, conflicts, and evaluation receipt. Name-only or registry-latest bindings are invalid.
9. **Coalitions must preserve tensions.** A Coalition Signature records ordered members, explicit interaction, bounded ratios, conflicts, and the emergent semantic job. It may not average contradictory signals into a comfortable centroid.
10. **Counteractivation is a first-class rejection test.** An edge that would intensify shame, status threat, disbelief, manipulation, identity distortion, or false relational intimacy beyond the authorized objective is blocked or weakened with an explicit receipt.
11. **Controlled variation is axis-labelled.** Variants may alter only declared axes and must preserve invariant identity, evidence, objective, and wrong-reading constraints. Random variation is not an F02 semantic operation.
12. **Producer and evaluator are independent roles.** The actor or process that compiles a Matrix cannot issue the independent evaluation receipt used for downstream eligibility in the same authority context.
13. **History is additive and reproducible.** Corrections, supersession, and invalidation create new immutable artifacts and edges. Historical versions and their exact dependency graph remain replayable after a current version is revoked.
14. **No generic approval expansion.** Technical security may validate signatures, integrity, access, and path safety, but it does not create a new content-rights or creative-safety authority outside attributable source and product governance.
15. **Compiler boundaries remain explicit.** F02 is an AIR semantic lifecycle component. It is not the Activative Contract Compiler, Pipeline, VAE, Studio, or Delegation Protocol.

## 4. Current brownfield architecture

### Reusable evidence

The Studio Brand Genesis predecessor already models discovery sessions, source references, profile proposals, quality checks, and operator confirmation. Its tests demonstrate useful behaviors around required source input and explicit approval. The Studio Matrix predecessor already exposes tension, Primitive reference, evaluation, approval, and downstream-packet concepts; its tests demonstrate that unsupported speculative tension cannot anchor a Matrix, a generic RSCS-style output can fail, unresolved Primitive references block, and downstream packets preserve identifiers.

These artifacts are evidence and migration inputs, not current AIR authority. Their useful names and fixtures may be adapted only when they satisfy the contracts in section 6.

### Gaps and unsafe assumptions

| Brownfield surface | Observation | Required disposition |
|---|---|---|
| Brand Genesis contracts | Mutable models, generated UUID/time values, storage-oriented paths, and generic string references prevent deterministic identity and clean historical reconstruction. | `ADAPT`: map explicit legacy values into immutable typed AIR refs; never generate missing classification during migration. |
| Brand Genesis service | Session state is written before the full workflow has completed; subsequent blocking can leave partial state. | `REPLACE_TRANSACTION_BOUNDARY`: commit artifacts, edges, command record, and receipt atomically. |
| Matrix contracts | Open dictionaries, floats, generated UUID/time, and Studio-local ownership flatten field meaning and make hashes non-portable. | `ADAPT`: use closed tagged unions, integer micros, caller-supplied IDs/times, normalized UTF-8 serialization, and Program Control ownership. |
| Matrix service | Compile, evaluate, approve, and persist responsibilities can share one service/actor. | `SPLIT`: compiler and evaluator have separate actor roles and receipts; approval remains attributable governance, not self-evaluation. |
| Matrix repository | In-memory overwrite by identifier lacks immutable versions, idempotency, concurrency control, invalidation edges, and receipt/artifact parity. | `REPLACE_FOR_PRODUCTION`; predecessor remains a fixture source only. |
| Matrix tests | Eight predecessor cases cover local happy/adversarial behavior but not canonical hashing, atomic rollback, replay, descendant invalidation, or product-boundary enforcement. | `ACTIVATE_AS_REGRESSION_INPUT` and add the evidence suite in section 10. |

No predecessor record is silently promoted. Missing identity version, source kind, epistemic state, relationship evidence, Primitive hash, or owner causes typed migration blocking rather than inference.

## 5. Proposed architecture and workflows

### Component boundaries

The future implementation consists of six bounded responsibilities:

1. `IdentityContextResolver` validates exact human-authorized identity and brand references and emits a resolved input set without changing them.
2. `ContextPremiseCompiler` compiles audience, interviewer-resonance, and relationship assertions from admitted evidence.
3. `MatrixOfEdgingCompiler` constructs broad signals, tension sites, candidate-survival decisions, Primitive bindings, coalition signatures, and Edge Product candidates.
4. `F02IndependentEvaluator` checks evidence fitness, identity fit, counteractivation, anti-centroid behavior, routeability, and Primitive constraints from an independent actor context.
5. `IdentityCandidateObserver` emits pending evidence-linked candidate observations for later authorized human resolution; it has no identity update command.
6. `IdentityContextRepository` atomically stores immutable artifacts, lineage edges, command records, evaluation receipts, invalidation records, and replay indexes.

### Workflow A — resolve identity and compile Context Premise

1. Receive `CompileContextPremiseCommand` with caller-supplied command ID, idempotency key, expected aggregate version, event time, F01 interface version, exact identity/brand refs, evidence refs, and objective ref.
2. Resolve every immutable ref by ID, version, and hash; reject mutable aliases, stale hashes, mixed Brand Context Versions, or missing human authority attribution.
3. Validate evidence ownership. Interview Expression refs may support live reaction facts but remain owned by Interview Expression; AIR records only immutable refs and permitted-use scope.
4. Normalize assertions into typed audience, interviewer, and relationship structures. Preserve observed/planned/inferred/unknown states field by field.
5. Reject ungrounded required fields. Optional unknowns remain explicit `UNKNOWN` assertions with no fabricated value.
6. Canonically serialize and hash the Context Premise. Stage artifact, lineage edges, command record, and compilation receipt in one transaction.
7. Commit only if expected version still matches and every staged hash re-verifies.

### Workflow B — compile the Matrix of Edging

1. Receive `CompileMatrixOfEdgingCommand` pinned to an eligible Context Premise and exact source, objective, Primitive-registry snapshot, and F01 refs.
2. Saturate the admitted evidence into broad signals without ranking or compression. Record which source/evidence/identity/context assertions support each signal.
3. Detect collisions and tension sites across guest or coach truth, audience reality, interviewer/relationship resonance, and objective.
4. Propose candidate edges from those tension sites. A candidate not traceable to a broad signal is rejected as a topic-similarity shortcut.
5. Resolve exact Primitive bindings and run source-evidence, identity-fit, counteractivation, planned/observed, compatibility, misuse, and routeability survival tests.
6. Form one or more explicit Coalition Signatures from surviving candidates. Preserve productive contradictions; do not average them away.
7. Emit bounded Edge Product candidates with confidence in integer micros and a typed reason for every inclusion, weakening, or rejection.
8. Atomically store the Matrix version, dependency edges, candidate decisions, command record, and compile receipt. It is not yet downstream eligible.

### Workflow C — independent evaluation and eligibility

1. An evaluator with a distinct actor and authority context loads the exact compiled Matrix and all pinned dependencies.
2. The evaluator deterministically executes the checks in the profile identified by `evaluation_profile_ref`.
3. Any missing dependency, identity mismatch, unsupported inference, self-evaluation, Primitive violation, or counteractivation breach produces a typed blocker receipt.
4. A passing receipt creates an additive `evaluated_by` edge and a new eligibility projection; it does not rewrite the Matrix artifact.
5. The F02 handoff exposes the exact Matrix, Edge Product, identity/context refs, evaluation receipt, and unresolved caveats to dependent AIR features.

### Workflow D — Identity DNA candidate observation

1. A recurrence detector may receive multiple evidence-linked observations under `ProposeIdentityDNACandidateCommand`.
2. It emits `IdentityDNACandidateObservation` only when every observation is attributable, contradictions are preserved, applicability is bounded, and the candidate remains `PENDING_HUMAN_RESOLUTION`.
3. The command cannot update an Identity DNA profile. The separate human authority process may later accept, reject, split, or defer it and must issue its own receipt.

### Workflow E — supersession, invalidation, and replay

1. A new identity, brand, source, Context Premise, objective, Primitive, or evaluation version never overwrites the old dependency.
2. Authorized supersession creates a new object and explicit `supersedes` edge.
3. The invalidation engine traverses typed descendant edges and marks only materially dependent current projections stale. Historical artifacts remain readable.
4. Active downstream consumption is denied when any pinned dependency or evaluation receipt is stale, revoked, or invalidated.
5. Replay resolves exact stored bytes and command inputs, not current registry aliases, and must reproduce every artifact hash and receipt decision or emit a divergence receipt.

## 6. Data models, contracts, schemas, and APIs

All objects are immutable, reject unknown fields, use normalized UTF-8 and lexicographically sorted keys, encode decimal-like scores as integers in `[0, 1_000_000]`, and contain no implicit current time, random identifier, environment variable, filesystem path, or traversal-order dependency. `ImmutableRef`, `AuthorityRef`, `ActorRef`, `EvidenceRef`, `EpistemicAssertion`, and `SemanticObjectVersion` follow the pinned F01 draft and remain subject to its revision-impact rule.

### Core input and context models

```text
IdentityContextInputSet
  schema_id: Literal["air.f02.identity_context_input_set"]
  schema_version: Literal["2.1.0-candidate"]
  identity_dna_ref: ImmutableRef
  identity_authority_ref: AuthorityRef
  brand_genesis_session_ref: ImmutableRef
  brand_context_version_ref: ImmutableRef
  voice_dna_ref: ImmutableRef
  visual_dna_ref: ImmutableRef
  canonical_source_package_refs: tuple[ImmutableRef, ...]
  audience_evidence_refs: tuple[EvidenceRef, ...]
  interviewer_evidence_refs: tuple[EvidenceRef, ...]
  relationship_evidence_refs: tuple[EvidenceRef, ...]
  activation_objective_ref: ImmutableRef
  primitive_registry_snapshot_ref: ImmutableRef
  f01_contract_ref: ImmutableRef
```

All tuples that affect meaning are non-empty where required, deduplicated, and canonically ordered by `(object_type, object_id, version, sha256)`. The resolved set must prove that its Identity DNA and Voice/Visual DNA refs belong to the same Brand Context Version or fail `AIR_F02_BRAND_CONTEXT_MISMATCH`.

```text
AudienceContextPremise
  semantic_object: SemanticObjectVersion
  audience_segment_ref: ImmutableRef
  situation: EpistemicAssertion[NonEmptyText]
  self_perceptions: tuple[EpistemicAssertion[NonEmptyText], ...]
  pressures: tuple[EpistemicAssertion[NonEmptyText], ...]
  desired_movements: tuple[EpistemicAssertion[NonEmptyText], ...]
  probable_defenses: tuple[EpistemicAssertion[NonEmptyText], ...]
  relationship_stage: EpistemicAssertion[RelationshipStage]
  smallest_useful_commitment: EpistemicAssertion[NonEmptyText]
  valid_from: CanonicalTimestamp
  valid_until: CanonicalTimestamp | null
  friction_if_wrong: tuple[NonEmptyText, ...]
  evidence_refs: tuple[EvidenceRef, ...]
  compilation_receipt_ref: ImmutableRef
```

`RelationshipStage` is a closed enum: `UNOBSERVED`, `PUBLICLY_AWARE`, `PUBLICLY_ENGAGED`, `DIRECT_REPLY_ESTABLISHED`, `INTERVIEW_ESTABLISHED`, `RECURRING_RELATIONSHIP`, or `UNKNOWN`. Stage transition requires evidence; absence of evidence maps to `UNKNOWN`, never a guessed higher stage.

```text
InterviewerResonanceContext
  context_ref: ImmutableRef
  interviewer_identity_ref: ImmutableRef
  entries: tuple[ResonanceEntry, ...]
  materiality: EpistemicAssertion[MaterialityDecision]
  operator_confirmation_ref: ImmutableRef | null

ResonanceEntry
  entry_id: StableId
  kind: LIVED_OVERLAP | CURIOSITY | RECOGNITION | DISBELIEF |
        PERSONAL_STAKE | CREDIBILITY_LIMIT | DISTORTION_RISK
  assertion: EpistemicAssertion[NonEmptyText]
  permitted_semantic_use: tuple[SemanticUse, ...]
  prohibited_inferences: tuple[NonEmptyText, ...]
```

An interviewer entry may refer to a Reaction Receipt or Expression Moment, but AIR stores only the immutable evidence ref. It cannot edit, reinterpret as observed when merely planned, or synthesize a missing live-evidence object.

### Matrix models

```text
MatrixOfEdgingProgram
  semantic_object: SemanticObjectVersion
  input_set_ref: ImmutableRef
  context_premise_ref: ImmutableRef
  objective_ref: ImmutableRef
  broad_signals: tuple[BroadSignal, ...]
  tension_sites: tuple[TensionSite, ...]
  primitive_bindings: tuple[PrimitiveBinding, ...]
  survival_decisions: tuple[CandidateSurvivalDecision, ...]
  coalition_signatures: tuple[CoalitionSignature, ...]
  edge_product_candidates: tuple[EdgeProductCandidate, ...]
  route_implications: tuple[RouteImplication, ...]
  fatality_risks: tuple[FatalityRisk, ...]
  compile_receipt_ref: ImmutableRef
  evaluation_receipt_ref: ImmutableRef | null
```

```text
BroadSignal
  signal_id: StableId
  layer: PRACTICAL | EMOTIONAL | SOCIAL | IDENTITY | RELATIONSHIP | SYSTEMIC
  statement: NonEmptyText
  epistemic_state: EpistemicState
  evidence_refs: tuple[EvidenceRef, ...]
  source_scope: tuple[ImmutableRef, ...]
  magnitude_micros: Integer[0..1_000_000]
  uncertainty_micros: Integer[0..1_000_000]

TensionSite
  tension_id: StableId
  pole_a: SignalRef
  pole_b: SignalRef
  relationship: CONTRADICTION | GAP | PRESSURE | UNEXPRESSED_DESIRE |
                STATUS_RISK | BELONGING_RISK | IDENTITY_FRICTION
  evidence_refs: tuple[EvidenceRef, ...]
  forbidden_shortcuts: tuple[NonEmptyText, ...]
```

```text
PrimitiveBinding
  binding_id: StableId
  primitive_id: NonEmptyText
  primitive_version: SemanticVersion
  primitive_sha256: Sha256
  registry_snapshot_ref: ImmutableRef
  local_job: NonEmptyText
  activation_conditions: tuple[NonEmptyText, ...]
  suppression_conditions: tuple[NonEmptyText, ...]
  misuse_constraints: tuple[NonEmptyText, ...]
  compatible_primitive_refs: tuple[PrimitiveExactRef, ...]
  conflicting_primitive_refs: tuple[PrimitiveExactRef, ...]
  evidence_refs: tuple[EvidenceRef, ...]
  primitive_evaluation_receipt_ref: ImmutableRef

CoalitionSignature
  coalition_id: StableId
  ordered_binding_refs: tuple[ImmutableRef, ...]
  bounded_ratios: tuple[PrimitiveRatio, ...]
  interaction_rationale: NonEmptyText
  preserved_tensions: tuple[ImmutableRef, ...]
  prohibited_centroid_moves: tuple[NonEmptyText, ...]
  emergent_semantic_job: NonEmptyText
```

`PrimitiveRatio.value_micros` is an integer and all ratios sum to exactly `1_000_000`. A ratio does not waive evidence, misuse, or compatibility constraints.

```text
CandidateSurvivalDecision
  candidate_id: StableId
  broad_signal_refs: tuple[ImmutableRef, ...]
  source_evidence: PASS | FAIL
  identity_fit: PASS | FAIL
  counteractivation: PASS | FAIL
  planned_observed_separation: PASS | FAIL
  primitive_compatibility: PASS | FAIL
  routeability: PASS | FAIL
  decision: SURVIVES | WEAKENED | REJECTED
  reason_codes: tuple[F02ReasonCode, ...]

EdgeProductCandidate
  edge_id: StableId
  pressure: NonEmptyText
  role_or_identity_at_stake: NonEmptyText
  stance: NonEmptyText
  consequence: NonEmptyText
  broad_signal_refs: tuple[ImmutableRef, ...]
  tension_site_refs: tuple[ImmutableRef, ...]
  source_evidence_refs: tuple[EvidenceRef, ...]
  survival_decision_ref: ImmutableRef
  coalition_signature_ref: ImmutableRef
  planned_assertion_refs: tuple[ImmutableRef, ...]
  observed_assertion_refs: tuple[ImmutableRef, ...]
  counteractivation_notes: tuple[NonEmptyText, ...]
  routeability: tuple[RouteImplication, ...]
  confidence_micros: Integer[0..1_000_000]
```

An `EdgeProductCandidate` cannot exist unless all required survival dimensions pass; `WEAKENED` candidates may be retained as evidence but are not downstream eligible. At least one broad signal and one source evidence ref are mandatory.

### Identity candidate model

```text
IdentityDNACandidateObservation
  candidate_id: StableId
  identity_dna_ref: ImmutableRef
  proposed_dimension: VOICE_PATTERN | VALUE_SIGNAL | RHYTHM | METAPHOR |
                      BOUNDARY | RELATIONAL_STANCE | VISUAL_TENDENCY
  proposed_value: NonEmptyText
  evidence_refs: tuple[EvidenceRef, ...]
  recurrence_count: PositiveInteger
  contradiction_refs: tuple[EvidenceRef, ...]
  fit_micros: Integer[0..1_000_000]
  applicability_scope: NonEmptyText
  authority_state: PENDING_HUMAN_RESOLUTION
  resolution_ref: ImmutableRef | null
```

No `UpdateIdentityDNACommand` exists in this boundary. A non-null resolution ref points to an externally authorized human resolution artifact and creates a new versioned identity dependency; it never mutates the observation.

### Commands, events, receipts, and repository API

Commands are closed tagged unions:

- `CompileContextPremiseCommand`;
- `CompileMatrixOfEdgingCommand`;
- `EvaluateMatrixOfEdgingCommand`;
- `ProposeIdentityDNACandidateCommand`;
- `SupersedeF02ObjectCommand`;
- `InvalidateF02DescendantsCommand`; and
- `ReplayF02CompilationCommand`.

Every command contains `command_id`, `idempotency_key`, `aggregate_id`, `expected_aggregate_version`, `actor_ref`, `authority_ref`, `issued_at`, exact input refs, and `command_payload_sha256`. Caller-supplied timestamps are canonical UTC with microseconds removed; wall-clock reads are prohibited in domain logic.

Every successful command emits one typed event and one immutable receipt. Each receipt records input hashes, output hashes, actor/authority refs, evaluation-profile ref when applicable, reason codes, committed lineage-edge IDs, repository transaction ID, and command-record hash. A blocked command emits a blocker receipt and no semantic artifact.

The repository interface is:

```text
load_exact(ref: ImmutableRef) -> ImmutableArtifact
load_current_projection(object_type, aggregate_id) -> VersionedProjection | null
begin(command_id, idempotency_key, expected_version) -> F02Transaction
stage_artifact(transaction, artifact_bytes, artifact_sha256)
stage_edge(transaction, typed_lineage_edge)
stage_receipt(transaction, receipt_bytes, receipt_sha256)
stage_command_record(transaction, command_record)
commit(transaction) -> AtomicCommitReceipt
rollback(transaction, reason_code) -> RollbackReceipt
list_descendants(root_ref, edge_types) -> tuple[ImmutableRef, ...]
replay(command_record_ref, dependency_snapshot) -> ReplayReceipt
```

Commit succeeds only when artifacts, receipts, edges, and the command record are complete and mutually referential. Receipt-only or artifact-only state is invalid.

### Canonical hashing and portability

Canonical bytes use UTF-8 without BOM, Unicode NFC, LF newlines, sorted object keys, declared tuple order, lowercase hexadecimal SHA-256, and no absolute path. Maps with semantic order are forbidden; use ordered tuples with stable identifiers. Canonical bytes exclude derived storage locations and include schema ID/version. Repeated execution with identical command bytes and dependency snapshot must return the exact prior receipt and artifact hashes.

## 7. Implementation stages and exact target paths

Implementation is not authorized by this specification. If later ratified, accepted, and issued a Development Capsule, work is staged as follows:

| Stage | Future exact target paths | Deliverable and gate |
|---|---|---|
| 1 — domain kernel | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/identity_context.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/matrix_of_edging.py` | Frozen closed models, invariants, canonical encoding, and typed blockers. No repository effects. |
| 2 — schemas | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f02.identity-context.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f02.matrix-of-edging.schema.json`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.f02.receipt.schema.json` | Schema/model round-trip and additional-property rejection. No shared release bytes. |
| 3 — repository | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/repositories/identity_context_repository.py` | Atomic artifact/edge/receipt/command commit, optimistic concurrency, idempotency, invalidation, and exact replay. |
| 4 — compiler service | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/identity_context_matrix_service.py` | Workflows A, B, D, and E with no evaluation authority. |
| 5 — independent evaluation | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/f02_evaluator.py` | Independent evidence, identity, counteractivation, anti-centroid, Primitive, and routeability checks. |
| 6 — adapters and migration | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/studio_brand_genesis_adapter.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/interview_expression_context_adapter.py`; `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/migrations/studio_matrix_v1_to_air_f02.py` | Lossless translation or typed block; no source-kind or identity invention. |
| 7 — downstream handoff | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/f02_handoff.py` | Exact eligible F02 package for F03 and later features, including caveats and dependency hashes. |

Each stage requires unit evidence before the next begins. Stage 6 must preserve source authority and live-evidence ownership; Stage 7 must reject stale or unevaluated F02 artifacts. No stage may create an Activative Contract Compiler or assume Pipeline/VAE execution authority.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Trigger | Required behavior |
|---|---|---|
| `AIR_F02_UPSTREAM_F01_DRAFT_DRIFT` | F01 path, state, or SHA differs from the dispatch lock. | Stop F02 advancement; reopen sections 3, 5, 6, 8, 9, and 10 for revision impact. |
| `AIR_F02_IDENTITY_REF_STALE` | Identity ID/version/hash or human authority ref cannot be resolved exactly. | Block with no compiled artifact. |
| `AIR_F02_BRAND_CONTEXT_MISMATCH` | Identity, Brand Genesis, Voice DNA, and Visual DNA do not bind the same governed Brand Context Version. | Block and list mismatched refs. |
| `AIR_F02_CONTEXT_PREMISE_UNGROUNDED` | A required premise field lacks admissible evidence or explicit unknown state. | Block; never fill from model inference alone. |
| `AIR_F02_INTERVIEWER_RESONANCE_UNATTRIBUTED` | Personal stake/resonance lacks evidence, operator confirmation when required, or permitted-use scope. | Exclude the entry or block when material to the objective. |
| `AIR_F02_RELATIONSHIP_STAGE_UNSUPPORTED` | Relationship stage exceeds its evidence. | Set no higher stage; issue blocker with evidence gap. |
| `AIR_F02_MATRIX_BROAD_SIGNAL_MISSING` | Candidate generation begins without evidence-linked broad signals. | Reject the Matrix command. |
| `AIR_F02_MATRIX_TOPIC_SIMILARITY_SHORTCUT` | An edge is derived from topic/embedding proximity without a supported tension site. | Reject candidate and record the shortcut. |
| `AIR_F02_PRIMITIVE_REF_UNRESOLVED` | Primitive ID/version/hash or registry snapshot cannot be resolved. | Block downstream eligibility. |
| `AIR_F02_PRIMITIVE_CONFLICT_UNRESOLVED` | Coalition contains incompatible bindings without a governed resolution. | Reject the coalition. |
| `AIR_F02_EDGE_SURVIVAL_FAILED` | Any non-compensable survival dimension fails. | Retain rejected evidence; emit no eligible Edge Product. |
| `AIR_F02_IDENTITY_MUTATION_FORBIDDEN` | An AIR command attempts to change canonical Identity DNA. | Deny and emit an authority-boundary receipt. |
| `AIR_F02_SELF_EVALUATION` | Compiler and independent evaluator resolve to the same actor/authority context. | Deny eligibility. |
| `AIR_F02_STALE_EXPECTED_VERSION` | Current aggregate version differs from command expectation. | Roll back all staged writes and return current ref. |
| `AIR_F02_IDEMPOTENCY_CONFLICT` | Same idempotency key has different command bytes or dependency snapshot. | Reject both mutation and receipt reuse. |
| `AIR_F02_NON_ATOMIC_STATE` | Staged artifacts, receipts, edges, or command record are incomplete or inconsistent. | Roll back and quarantine transaction evidence. |

### Migration

Migration consumes named Studio predecessor records as untrusted historical inputs. It must:

1. preserve original bytes and SHA-256;
2. map only explicit values into typed F02 fields;
3. retain the original identifier as a historical alias while assigning a stable immutable AIR ref;
4. replace generated current time with the recorded legacy time or block if time is required and absent;
5. preserve open/unmapped fields in a separate immutable migration-evidence attachment, never a canonical model field;
6. refuse to guess identity version, source kind, relationship stage, epistemic state, Primitive hash, owner, or approval authority; and
7. produce a new immutable migration artifact and receipt without overwriting the predecessor.

Migration result is `MIGRATED`, `MIGRATED_WITH_NONAUTHORITATIVE_ATTACHMENT`, or `BLOCKED_REQUIRED_MEANING_MISSING`. Only `MIGRATED` artifacts may become current candidates after independent evaluation.

### Rollback and recovery

Transaction rollback deletes only uncommitted staging objects. It never deletes committed history. If a process stops after staging but before commit, recovery compares the transaction journal, content-addressed objects, edges, command record, and receipt set; it either completes the same atomic commit when every hash and precondition still matches, or writes a rollback receipt. It may not synthesize a missing receipt.

Supersession or revocation marks current projections and material descendants stale through typed edges such as `compiled_from`, `constrained_by`, `evaluated_by`, and `supersedes`. Non-material reference-only descendants remain valid. Historical resolution by exact hash continues after invalidation.

### Observability

Structured events include `command_id`, `transaction_id`, `aggregate_id`, `aggregate_version`, `artifact_ref`, `input_hashes`, `output_hashes`, `actor_ref`, `authority_ref`, `reason_codes`, `dependency_state`, `duration_micros`, and `correlation_id`. Logs contain refs and hashes, not unrestricted interview content or identity payloads. Metrics include blocked commands by reason, idempotent replays, conflicts, rollback/recovery outcomes, unsupported relationship assertions, rejected topic shortcuts, Primitive conflicts, self-evaluation attempts, invalidation fan-out, and replay divergence. Operational telemetry is not semantic authority.

## 9. Behavior-specific acceptance criteria

1. **AIR-FR-007 / AIR-ST-02.01 — exact identity set:** given aligned Identity DNA, Brand Genesis, Brand Context, Voice DNA, and Visual DNA refs, compilation stores every exact ID/version/hash and human authority ref; changing any hash changes the artifact hash. A mixed Brand Context Version blocks with `AIR_F02_BRAND_CONTEXT_MISMATCH`.
2. **AIR-FR-008 / AIR-ST-02.01 — Context Premise:** the result contains situation, self-perceptions, pressures, desired movements, probable defenses, and relationship stage as field-level epistemic assertions with evidence and validity. Missing required evidence blocks; optional unknowns remain explicit.
3. **AIR-FR-009 / AIR-ST-02.02 — resonance:** material interviewer lived overlap, curiosity, recognition, and current relationship context are preserved with attributable evidence and permitted use. An ungrounded personal claim cannot influence the Matrix.
4. **AIR-FR-010 / AIR-ST-02.02 — broad-first Matrix:** every tension and candidate traces to the intersection of source truth, audience reality, interviewer/relationship resonance where material, and objective. Candidate ranking cannot run before at least one admissible broad signal exists.
5. **AIR-FR-011 / AIR-ST-02.03 — Edge Product survival:** an eligible Edge Product has passing source-evidence, identity-fit, counteractivation, planned/observed separation, Primitive compatibility, and routeability decisions plus exact Primitive hashes, Coalition Signature, misuse constraints, and independent evaluation receipt.
6. **AIR-FR-012 / AIR-ST-02.03 — identity observation ceiling:** AIR can emit an evidence-linked recurrent identity candidate in `PENDING_HUMAN_RESOLUTION`; it cannot alter the canonical Identity DNA object or represent the candidate as accepted.
7. **Determinism:** two fresh processes given identical command bytes and dependency snapshots produce byte-identical artifacts, edges, and receipts. Current time, random state, dictionary insertion, traversal order, absolute paths, locale, and environment do not change results.
8. **Idempotency:** an exact replay returns the original committed refs and hashes without another version. The same idempotency key with changed bytes returns `AIR_F02_IDEMPOTENCY_CONFLICT` and changes no state.
9. **Optimistic concurrency:** two commands against the same expected version cannot both commit; the loser receives `AIR_F02_STALE_EXPECTED_VERSION`, and no artifact or orphan receipt remains.
10. **Atomicity:** injected failure at every stage between artifact, edge, receipt, and command-record staging leaves either the complete prior state or the complete new commit, never partial state.
11. **Invalidation:** superseding an identity/context/Primitive/evaluation dependency invalidates only material descendants and denies stale handoff; historical artifacts remain resolvable and replayable by exact hash.
12. **Independent evaluation:** compiler identity and evaluator identity must differ in actor and authority context. Presence of a score alone does not confer eligibility.
13. **Ownership:** contract and architecture tests prove AIR cannot write Interview Expression live evidence, canonical Identity DNA, Pipeline execution state, VAE production state, Studio canonical state, or Delegation routing state.
14. **Migration:** complete legacy records migrate losslessly to new immutable artifacts; incomplete classification blocks with the exact missing fields. Migration never guesses source kind, epistemic state, relationship stage, or identity ownership.
15. **Primitive laws:** PRM-PSY-001 layer matching, PRM-PSY-008 dignity-preserving correction, and PRM-PRS-015 current/future balance are present as exact bindings when invoked, with their misuse constraints enforced rather than paraphrased away.
16. **Pending authority:** metadata and all receipts retain `CANDIDATE_NOT_CURRENT`, `specification_work_authorized: true`, `build_authority: false`, and the pre-ratification ceiling. No result claims `ACCEPTED_FOR_BUILD`.
17. **Draft dependency:** every F02 writing/validation receipt pins F01 SHA `622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc` and labels it `DRAFT_DEPENDENCY_NOT_ACCEPTED` until its state advances.

## 10. Testing and completion evidence

### Required future test suites

| Test path | Evidence required |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_identity_context.py` | Identity/brand alignment, Context Premise required fields, unknown preservation, and mutation denial. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_matrix_of_edging.py` | Broad-first construction, tension sites, survival, coalitions, anti-centroid behavior, and identity candidate ceiling. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/serialization/test_f02_canonical_hash.py` | Fresh-process determinism across insertion order, traversal order, environment, locale, and machine paths. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_air_f02_schemas.py` | Closed schemas, tagged unions, integer micros, ref/hash validation, and generated-model equivalence. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_identity_context_resonance_and_matrix_of_edging.py` | AIR-FR-007 through AIR-FR-012 end-to-end with exact lineage and independent evaluation. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_f02_atomic_commit_and_idempotency.py` | Failure injection, no partial state, exact replay, conflict denial, and receipt/artifact parity. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/architecture/test_f02_product_boundaries.py` | No cross-product mutation or generic approval authority; compiler/runtime distinction preserved. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_studio_matrix_v1_to_air_f02.py` | Lossless mapping, historical aliases, immutable source bytes, and typed blocks for absent meaning. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/recovery/test_f02_replay_and_invalidation.py` | Descendant-only invalidation, stale-consumption denial, recovery, and historical reproduction. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/clean_environment/test_f02_portability.py` | Clean extracted-layout behavior and absence of absolute path/environment dependencies. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/reference_slice/test_f02_to_f03_handoff.py` | Exact F02 identity/context/Matrix/Edge Product handoff and rejection of stale or unevaluated inputs. |

The predecessor Studio tests at `THE_CMF_STUDIO(2)/tests/test_brand_genesis_service.py` and `THE_CMF_STUDIO(2)/tests/test_matrix_service.py` become regression inputs, not proof of F02 completion.

### Required adversarial matrix

The future evidence run must include stale Identity DNA, cross-brand Voice DNA, absent audience pressure, fabricated interviewer stake, overclaimed relationship stage, topic-only edge creation, centroid-smoothed coalition, unresolved Primitive hash, conflicting Primitive bindings, observed/planned flattening, self-evaluation, confidence compensation, random ordering, current-time injection, absolute-path contamination, mid-commit failure, conflicting idempotency reuse, concurrent update, invalidated dependency, incomplete legacy migration, and attempted AIR mutation of human-owned Identity DNA.

### Completion evidence contract

F02 implementation could be considered technically complete only when all named suites pass twice in fresh processes; all source files compile; schema/generated-type parity passes; canonical fixtures match; mutation, branch, and failure-injection coverage reaches the later governed thresholds; every requirement maps to a test and receipt; an independent evaluator signs the F02 result; clean-room replay reproduces exact hashes; and a separately authorized independent audit accepts the evidence.

This writing receipt is not that evidence. The current document ends at `WRITTEN_PENDING_AUDIT`, remains governed by an unratified candidate, and may advance no higher than `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` until attributable ratification. It issues no build authority, implementation authorization, Development Capsule, product adoption, production eligibility, or certification.
