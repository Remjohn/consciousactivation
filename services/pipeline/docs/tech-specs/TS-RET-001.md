# TS-RET-001 — Authority-First Hybrid Retrieval and JIT Execution Capsule Compiler

| Field | Value |
|---|---|
| Spec ID | `TS-RET-001` |
| Product | Atomic Harness Pipeline (AHP) |
| Primary owner | Atomic Harness Pipeline |
| Lifecycle state | `WRITTEN_PENDING_AUDIT` |
| Authority state | `CANDIDATE_NOT_CURRENT` |
| Specification work authorized | `true` |
| Build authority | `false` |
| Later acceptance ceiling before ratification | `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION` |
| Writing packet | `CA-P03-WRITE-TS-RET-001-RECOVERY` |
| Writing wave | `13` |
| Output path class | `DIRECT_PRODUCT_SPEC_PATH` |
| Controlled requirements | `AIR-FR-113`, `FR-019` through `FR-024` |
| Controlled stories | `AIR-ST-19.03`, `ST-07.01` |

This document is an implementation-grade candidate specification. It does not make the V2.1 candidate authority current, authorize implementation, certify a model or retrieval system, create contract-release bytes, or issue a Development Capsule.

## 1. Governing inputs and source basis

### 1.1 Authority and workflow inputs

The writer admitted the following governance inputs:

| Input | Role | Disposition |
|---|---|---|
| `CA_TECH_SPEC_WRITE_SKILL.md` V3.3 workflow copy | Ten-section writing law and claim ceiling | Governing writing method |
| `ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml`, packet `CA-P03-WRITE-TS-RET-001-RECOVERY` | Exact identity, requirements, Stories, path, dependencies, and scope | Governing packet |
| `WAVE_13_DISPATCH_LOCK.yaml` | Wave admission and disjoint-path lock | Governing dispatch |
| Prompt 02C specification-work authorization | Candidate-authority writing permission | Authorizes WRITE only |
| AIR Constitution/PRD candidate package V2.1 | Semantic lifecycle and semantic-object ownership | `CANDIDATE_NOT_CURRENT` |
| AHP PRD candidate package V1.3 integration state | Pipeline behavior and product boundary | `CANDIDATE_NOT_CURRENT` |

No statement in this spec promotes a candidate authority, Story, upstream draft, or source implementation to accepted authority. Where current and candidate authority differ, implementation remains blocked until the required ratification and adoption receipts exist.

### 1.2 Hash-pinned upstream writing inputs

Both upstream specifications are admitted as drafts under `DRAFT_DEPENDENCY_NOT_ACCEPTED`:

| Edge | Input | Quality state | SHA-256 | Use |
|---|---|---|---|---|
| `SDE-066` | `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-002.md` | `WRITTEN_PENDING_AUDIT` | `3e76ee7e4ec8f3b288a58bb8b8eb886195d9ad17097c67ded613c22fbb3dccd4` | Harness-to-runtime binding boundary and workflow-node execution contract |
| `SDE-067` | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-019.md` | `WRITTEN_PENDING_AUDIT` | `515e42a7e015c212f9f972b4e78e1e7aa0558816448f10ff18db9b9a7f7ecd5e` | Failure attribution, bounded repair, role context, and replay boundary |

Their downstream revision impact is mandatory. A changed upstream hash or accepted semantic change reopens at least sections 3, 5, 6, 8, 9, and 10 of this spec: governing decisions; proposed architecture and workflows; data models, contracts, schemas, and APIs; failure/migration/rollback/recovery/observability; acceptance criteria; and testing/completion evidence.

### 1.3 Requirement and Story inputs

This spec operationalizes:

- `FR-019`: typed context slots declare authority, freshness, contradiction, and budget rules.
- `FR-020`: authority, lifecycle, category/profile, identity, embodiment, and evidence eligibility precede semantic ranking.
- `FR-021`: exact, lexical, dense, graph, visual, syntax, and evidence signals are selected according to the task contract.
- `FR-022`: required contradictory, failed, and superseding evidence is included when the node contract demands it.
- `FR-023`: Minimum Complete Context produces a current JIT Capsule with exact source identities, inclusion reasons, and a context budget.
- `FR-024`: retrieval receipts expose filters, candidates, exclusions, ranking, compression, unavailable context, and downstream outcome.
- `AIR-FR-113`: role-specific Minimum Complete Context capsules distinguish Hunters, Analysts, Composers, and Commanders.
- `ST-07.01`: a learned or agentic node receives the smallest eligible context, including governed contradictions and exclusions, rather than scanning an unrestricted corpus.
- `AIR-ST-19.03`: failure is attributed to a responsible layer; only affected descendants are invalidated; repair remains bounded; replay avoids unrelated regeneration.

### 1.4 Current implementation and unique evidence inputs

| Source | Disposition | SHA-256 | Admitted use |
|---|---|---|---|
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/skills/jit_capsule.py` | `REQUIRED_CURRENT_IMPLEMENTATION` | `6546b1e879961be6336b7e519590f380afe2a16f30768587c1686b8d3c47ee4e` | Brownfield capsule taxonomy, canonical JSON, relative-reference and non-production defaults |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/jit_capsule_commands.py` | Current implementation context | `71ed6302239b08b3b9e1dd1adcbc4d6ef3c932f293df0e5f8fe96364cb5036cb` | Existing command/idempotency behavior and gaps |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/skills/capsule_lifecycle.py` | Current implementation context | `900e0bdad6ccce61c7df56e8225c2b19a061be96108c404e210e59e41edaeaa3` | Existing pinned/verified/active/disposed/invalidated lifecycle |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/capsule_lifecycle_commands.py` | Current implementation context | `8bc3a14e5cd97840ae38c316c190b2a9393ae5545e96c66ed58e07e430dccb3e` | Current lifecycle command surface |
| `02_VISUAL_ASSET_EDITOR/prd/05-features/F17-steering-intelligence-cmf-okf-retrieval.md` | `REQUIRED_AUTHORITY` | `9acefd1eaa224cd9de3dd5d39fec7443dfd6edcbac32a1dfe97355e1b8230aa7` | VAE ownership of visual production knowledge and projection boundary |
| `sources/ai_v2_predecessor/contracts/11_FAILURE_ATTRIBUTION_AND_REPAIR_PROGRAM.md` | `REQUIRED_UNIQUE_EVIDENCE` | `b25670847d79678eb0d269656afe38cd45d0a9244b47d5051dea931379ec2ae7` | Failure-attribution and repair-program lineage |
| `sources/doctrine/AHP_F16_EVALUATION_REPAIR.md` | `REQUIRED_UNIQUE_EVIDENCE` | `0a247a2025ef803df09e8bfc97b9456d73a64cf2f867598135b3c8ba03a668e2` | Independent evaluation and bounded repair behavior |
| `sources/doctrine/AHP_F03_BOUNDED_ROLE_TAXONOMY.md` | `REQUIRED_UNIQUE_EVIDENCE` | `1d50940d7313b89331e872b63393276267e698cb5908254479e216a234f3ec77` | Bounded role taxonomy and non-conflation rules |

`SRC-EXT-005`, the named external Nemotron reference, is a `DEFERRED_REFERENCE`; exact bytes are unavailable and no active requirement depends uniquely on it. This spec makes no factual claim attributed to that source.

## 2. Problem, outcomes, and scope

### 2.1 Problem statement

An execution node cannot safely ask “what is most similar?” before establishing “what is eligible, current, authorized, compatible, and necessary?” Similarity-first retrieval can return a persuasive but wrong recipe, identity, source version, format profile, tool claim, evaluator result, or production precedent. An unrestricted long-context dump is not a remedy: it hides contradiction, raises cost, leaks data across authority boundaries, weakens replay, and makes downstream outcomes impossible to attribute to exact evidence.

The Pipeline therefore needs an authority-first retrieval system and JIT compiler that transforms a governed node-context declaration plus immutable source projections into the smallest complete execution capsule. It must preserve source identity, epistemic state, contradiction, supersession, exclusions, and budget decisions; bind a Programmed Model only after those decisions; record the downstream outcome; and support selective invalidation and exact replay.

### 2.2 Required outcomes

The implementation described here shall:

1. Reject ineligible context before any learned similarity or reranking step.
2. Query only authorized projections, never another product's private canonical store.
3. Select task-appropriate exact, lexical, dense, graph, visual, syntax, and evidence signals under a versioned retrieval profile.
4. Prove coverage of mandatory contradiction, failure, and supersession obligations.
5. Compile a deterministic, content-addressed Minimum Complete Context capsule per role and node attempt.
6. Separate semantic role, runtime actor, authority owner, capability owner, tool grant, and Programmed Model identity.
7. Bind every item to an immutable source/version/hash and explicit inclusion reason.
8. Preserve visible exclusions and unavailable required context instead of guessing.
9. Emit sufficient receipts to reproduce eligibility, candidate discovery, ranking, compression, capsule construction, activation, downstream result, and invalidation.
10. Keep production eligibility and certification false until later governed gates establish otherwise.

### 2.3 In scope

- Pipeline-side retrieval query planning and projection admission.
- Deterministic eligibility and authority filters.
- Hybrid candidate discovery and post-eligibility ranking.
- Contradiction, failure, and supersession coverage.
- Budgeted Minimum Complete Context selection.
- Hunter, Analyst, Composer, and Commander capsule profiles.
- Programmed Model binding under an explicit claim envelope.
- Capsule lifecycle, idempotency, replay, selective invalidation, and historical reproduction.
- Retrieval and execution receipts, outcome observations, and evaluation hooks.
- Brownfield adaptation of the Builder JIT taxonomy without moving Builder or VAE authority into Pipeline.

### 2.4 Out of scope

- Creating or editing semantic meaning owned by AIR, Builder-generated targets, Interview Expression, VAE, Studio, or Delegation.
- Reconstructing missing source classification, human authority, Reaction Receipts, Expression Moments, Identity DNA, Final Script approval, or Visual Asset Demand meaning.
- VAE Steering Recipe creation, visual-production knowledge governance, model/LoRA/conditioning choice, candidate generation, or production acceptance.
- Training or certifying an embedding, reranker, VLM, evaluator, or Programmed Model.
- Changing a Harness definition, Feature Contract, semantic program, approved source package, or lifecycle policy.
- A shared contract release, production deployment, Stage 5 work, or a Development Capsule.
- Generic content-rights or creative-safety approval authority. Provenance and operator-supplied source authority remain with their owning products; technical security remains operational.

### 2.5 Claim ceiling

Successful conformance to this draft proves only technical compliance with a candidate specification. It does not prove retrieval quality in production, semantic correctness, evaluator certification, source authority, product adoption, or build authorization.

## 3. Governing decisions and ownership boundaries

### 3.1 Decisions

**D1 — Eligibility precedes ranking.** The eligibility engine shall produce an immutable eligible-candidate snapshot before dense similarity, learned fusion, or learned reranking executes. A ranker cannot restore an excluded candidate.

**D2 — Similarity is never authority.** Scores order already eligible candidates. Scores may not grant lifecycle validity, category/profile support, identity continuity, embodiment compatibility, evidence sufficiency, source authority, or permission to use an object.

**D3 — Canonical products publish projections.** Retrieval adapters read immutable, versioned, purpose-scoped projections from owning products. The Pipeline neither crawls private repositories nor treats its index as a canonical source.

**D4 — The node contract defines completeness.** Minimum Complete Context is evaluated against typed slots and coverage obligations. “Minimum” means no selected item can be removed without breaking an explicit slot, contradiction, provenance, dependency, or stopping-law obligation.

**D5 — Required absence is a blocker.** If required context is missing, stale, ambiguous, contradictory without a resolution rule, unverifiable, or outside the budget, the compiler returns a typed blocker. It does not invent, summarize away, or silently omit the requirement.

**D6 — Optional context is not opportunistic padding.** An item marked optional is excluded from a minimum capsule unless a governed conditional rule promotes it to `CONDITIONAL_REQUIRED` for this attempt. Promotion and its evidence are receipted.

**D7 — Contradiction is first-class.** A context requirement may demand active contradictions, failed alternatives, rejected candidates, or superseding evidence. Required contradiction cannot be removed by compression or low similarity.

**D8 — Capsules are role-specific.** Hunter, Analyst, Composer, and Commander profiles have distinct admissible slots. The system does not give every role the same unrestricted context.

**D9 — Role is not authority.** A role label never hides the executing actor, authority owner, capability owner, product boundary, tool grants, output contract, evaluator, or stopping law.

**D10 — Programmed Models are bounded candidates.** A Programmed Model may retrieve, rank, compress, or propose only inside its declared capability, training/data claim, epistemic, and output envelopes. It cannot decide authority eligibility or mutate canonical meaning.

**D11 — Compression preserves verification.** A summary is a derived context item with its own hash, compiler identity, input item set, loss declaration, and verification links. Required exact clauses, locks, identifiers, approvals, contradictions, and executable contracts may be marked non-compressible.

**D12 — Capsule identity is content-derived.** Given identical admitted projections, requirements, profiles, tokenizer, eligibility rules, ranking configuration, and compiler version, byte output and digest shall be identical across process, machine, traversal order, clock, and environment.

**D13 — History is append-only.** Invalidation changes consumability; it never deletes the capsule, artifact, command, candidate snapshot, or receipt needed for historical reproduction.

**D14 — Repair is selective.** A source or rule change invalidates the capsule and only descendants whose dependency proofs include the changed object. Repair may not broaden scope or regenerate unrelated outputs.

**D15 — Outcomes close the evidence loop.** The retrieval receipt links to downstream execution and evaluation observations. Outcome data may inform later evaluation or profile governance but never retroactively changes the historical selection.

### 3.2 Semantic-object and behavior ownership

| Object or behavior | Canonical owner | Pipeline permission | Prohibited Pipeline behavior |
|---|---|---|---|
| AIR semantic lifecycle, Primitive/archetype/role-tension/Matrix/transfer meaning | AIR | Consume exact approved projections; execute/invalidate | Recompile or reinterpret meaning |
| Reaction Receipt and Expression Moment evidence | Interview Expression/source product | Validate refs and include required evidence | Synthesize human reaction or authority |
| Harness node/context declaration | Builder or Builder-generated target | Validate and bind at runtime | Rewrite semantic intent or node authority |
| Context requirement for an AIR-owned semantic operation | AIR | Execute requirement | Weaken or broaden it |
| Retrieval execution, eligibility, query plan, ranking, Minimum Complete Context | Pipeline | Own | Delegate authority decisions to a learned model |
| Programmed Model semantic responsibility and claim envelope | Owning product/AIR governance | Bind an eligible implementation candidate | Treat a model card or score as semantic authority |
| Visual Steering Recipe and production knowledge | VAE | Consume typed authorized projection | Fork VAE knowledge or choose production semantics |
| Studio correction decision/HumanResolution | Studio/human authority | Route and replay authorized result | Manufacture approval |
| Message transport and shared failure envelope | Delegation | Use immutable message contract | Let transport become creative authority |
| Retrieval/evaluation profile governance | Owning product and evaluator governance | Execute pinned profile | Self-certify profile or evaluator |

### 3.3 Authority hierarchy during a request

For every context item the eligibility engine evaluates, in order:

1. constitutional and ratified product authority;
2. exact governing contract and authorized amendments;
3. source-product ownership and operator-supplied authority;
4. lifecycle state, version, supersession, revocation, and selective invalidation;
5. node-declared authority and provenance requirements;
6. category, profile, identity, embodiment, audience, and sequence compatibility;
7. evidence and freshness policy;
8. retrieval-profile signal and ranking policy.

If two higher-order authorities conflict, the request is blocked with `RET-AUTHORITY-CONFLICT`; a ranker or Programmed Model never chooses the winner.

### 3.4 Role-context contracts

- **Hunter:** discovery question, admissible source classes, known gaps, search boundaries, exclusion policy, and stopping law. It does not receive unbounded production or approval context.
- **Analyst:** exact evidence, provenance, epistemic states, required contradictions, failed/superseded alternatives, evaluation rubric, and attribution contract.
- **Composer:** approved ingredients, semantic and feature contracts, identity/continuity locks, composition constraints, forbidden readings, and output schema. Discovery-only speculation is excluded.
- **Commander:** candidate outputs, receipts, gates, dependency graph, stopping/cancellation laws, evaluator decisions, and authorized escalation routes. It does not gain authority to alter meaning.

## 4. Brownfield assessment and disposition

### 4.1 Existing Builder JIT capsule

The Builder `PhaseLocalJITCapsule` establishes useful invariants: immutable data classes; relative, non-machine-specific references; canonical sorted JSON; source hashes; phase and owner metadata; the classifications `REQUIRED`, `CONDITIONAL_REQUIRED`, `OPTIONAL`, `FORBIDDEN`, and `NOT_APPLICABLE`; and explicit non-production/non-certification defaults. Those invariants shall be **adapted**, not copied into an independent Pipeline fork.

The current implementation is insufficient as the runtime retrieval compiler because it contains string-oriented references, no governed eligibility or ranking snapshot, no typed freshness or lifecycle evidence, no contradiction/supersession coverage proof, no task-specific signal plan, no budget-unit contract, no compression provenance, and no downstream outcome link. Its application repository deletes an invalidated capsule from active storage and does not retain the complete retrieval decision graph. It is therefore not the final Pipeline implementation.

### 4.2 Existing capsule lifecycle

The current lifecycle states `PINNED`, `VERIFIED`, `ACTIVE`, `DISPOSED`, and `INVALIDATED`, plus command idempotency and history, are useful brownfield concepts. The Pipeline implementation shall adapt the append-only transition pattern while separating:

- capsule build lifecycle;
- verification lifecycle;
- consumption lifecycle;
- invalidation/revocation lifecycle;
- downstream attempt lifecycle.

An active lookup may hide an invalid capsule, but the historical repository shall retain its immutable bytes, receipt, transitions, and descendants.

### 4.3 VAE retrieval boundary

VAE F17 remains authoritative for VAE Steering Recipes, product knowledge, and its projection lifecycle. Pipeline may query a purpose-scoped VAE projection after compatibility and authority checks. A Pipeline index is a rebuildable projection, not the VAE canonical store, and a Pipeline retrieval score cannot approve a visual-production method.

### 4.4 Dispositions

| Brownfield element | Disposition | Required change |
|---|---|---|
| Builder classification vocabulary | `ADAPT` | Add governed promotion, reason codes, evidence, and typed N/A rule |
| Builder canonical serialization/relative references | `ADAPT` | Generalize to all retrieval/capsule records and pinned canonicalization version |
| Builder JIT domain object | `SUPERSEDE_AT_RUNTIME` | Preserve declaration compatibility; implement Pipeline-owned runtime models |
| Builder JIT command repository | `REPLACE_FOR_PIPELINE` | Transactional append-only artifact/receipt/command store |
| Builder capsule lifecycle | `ADAPT` | Preserve states where compatible; add build, verification, consumption, and selective invalidation evidence |
| VAE F17 knowledge retrieval | `CONSUME_PROJECTION` | No copied knowledge authority or VAE-local writes |
| AIR repair context | `CONSUME_EXACT_CONTRACT` | Pipeline executes bounded repair; AIR retains semantic repair meaning |
| Existing tests | `RETAIN_AS_COMPATIBILITY_TESTS` | Add eligibility, hybrid retrieval, contradiction, determinism, replay, and failure suites |

### 4.5 Migration constraint

Legacy Builder capsules may be imported only as `legacy_migrated` declaration evidence. Migration must preserve their original bytes/hash, mark missing runtime evidence explicitly, and create a new immutable Pipeline capsule or a typed `RET-LEGACY-EVIDENCE-INCOMPLETE` blocker. Migration never invents source kind, lifecycle validity, authority, contradiction coverage, or selection reasons.

## 5. Proposed architecture and workflows

### 5.1 Component model

1. **Context Requirement Intake** validates a hash-pinned Harness node declaration or AIR semantic-operation requirement.
2. **Projection Registry** records source-product projection descriptors, owners, lifecycle endpoints, schemas, compatibility profiles, and rebuild cursors.
3. **Authority and Eligibility Engine** evaluates deterministic authority, lifecycle, compatibility, identity, embodiment, provenance, evidence, and freshness rules.
4. **Retrieval Query Planner** maps typed slots to the permitted signal families and per-signal budgets.
5. **Signal Adapters** execute exact, lexical, dense, graph, visual, syntax, and evidence retrieval against the eligible snapshot.
6. **Candidate Snapshot Store** freezes admitted and excluded candidates with reason codes before ranking.
7. **Fusion and Ranking Engine** ranks only eligible candidates with a pinned deterministic profile and stable tie-breaks.
8. **Contradiction/Supersession Resolver** proves required opposition, failure, supersession, and resolution coverage without choosing authority through similarity.
9. **Minimum Complete Context Solver** satisfies required slots and obligations under a deterministic budget, then removes redundant items while preserving completeness.
10. **Capsule Compiler** emits role-specific canonical bytes, exact references, inclusion/exclusion summaries, tool/output/evaluator contracts, and stopping law.
11. **Programmed Model Binder** chooses only an eligible implementation whose capability and claim envelopes satisfy the node binding.
12. **Capsule Lifecycle Repository** atomically stores artifact, retrieval receipt, command record, transitions, and dependency edges.
13. **Outcome and Evaluation Linker** records downstream execution/result/evaluation without mutating historical retrieval evidence.
14. **Invalidation Planner** computes affected descendants from immutable dependency proofs and emits a bounded replay plan.

Components communicate through typed domain ports. Signal adapters never call the capsule repository directly; models never call canonical product stores; rankers never call authority mutation ports; and projections never own source-product truth.

### 5.2 End-to-end compile workflow

1. Receive `CompileJITCapsuleCommand` with request ID, idempotency key, tenant/program scope, node binding hash, attempt ID, role profile, projection-set ID, retrieval-profile ID, compiler version, and expected repository revision.
2. Resolve the exact node/context requirement. Reject mutable or unversioned input.
3. Verify authority state and candidate-specification/build gates. A runtime implementation cannot run under this draft until separately authorized.
4. Resolve every projection descriptor and immutable snapshot cursor. Reject unpinned or unauthorized projections.
5. Enumerate candidates for each slot using deterministic metadata predicates. Record every admission/exclusion decision.
6. Freeze the eligible-candidate snapshot and its digest. Learned retrieval receives only that snapshot.
7. Plan permitted signal adapters for each slot. Exact identifiers and graph dependencies execute before approximate signals.
8. Execute signals with pinned implementation/model/version, normalization, and budget. Record raw scores using canonical decimal encoding.
9. Fuse features and rank using stable ordering: governed tier, normalized score vector, source/version identity, and content digest. No runtime clock or container order is a tie-breaker.
10. Expand mandatory dependency, contradiction, failed-alternative, and superseding-evidence closures.
11. Solve slot minimums and maximums. If mandatory coverage exceeds budget, emit a blocker with an operator/owner escalation route; do not truncate mandatory content.
12. Apply allowed lossless extraction or governed derived summaries. Preserve exact non-compressible fragments.
13. Run a deletion proof: removing each selected item must violate at least one recorded coverage obligation. Items without a necessity proof are removed.
14. Bind an eligible Programmed Model and tool grant, if the node requires one. Binding is separate from semantic role and authority.
15. Canonicalize, hash, and atomically commit capsule bytes, retrieval receipt, command record, candidate snapshot, dependency graph, and lifecycle transition.
16. Return a portable reference plus summary metadata. The response does not embed secrets or machine paths.

### 5.3 Projection registration and refresh workflow

Projection registration requires source product, authority owner, schema ID/version, compatibility profile, source-set digest, lifecycle watermark, tenant/program partition, allowed purposes, data classification, and verification signature or local trust state. Refresh creates a new projection snapshot; it never mutates a snapshot used by an accepted attempt. If source items are revoked or superseded, the registry records the event and triggers dependency-based invalidation.

A projection adapter must expose deterministic enumeration or a stable cursor. Filesystem traversal order, database default ordering, locale, process environment, and wall time shall not influence its exported canonical snapshot.

### 5.4 Eligibility workflow

Each candidate passes all applicable gates:

1. tenant/program/source-product boundary;
2. authority owner and permitted-purpose match;
3. exact source-kind and provenance requirement;
4. lifecycle state, revocation, supersession, and invalidation state;
5. category, format/profile, sequence, asset, and feature applicability;
6. identity and continuity binding;
7. embodiment and T/V route compatibility;
8. evidence class and epistemic-state admissibility;
9. freshness and effective-time policy using command-pinned instants, never “now” during replay;
10. wrong-reading-lock and constraint compatibility;
11. data classification, security, and tool-use boundary;
12. schema and compatibility-profile support.

Every failure creates an `EligibilityDecision` with a governed code. The system records excluded metadata and digest, but may redact content according to the caller’s rights.

### 5.5 Hybrid discovery and ranking workflow

Signal families have distinct jobs:

- **exact:** immutable IDs, contract keys, version refs, source hashes, feature refs;
- **lexical:** governed terms, phrases, aliases, labels, and requirement vocabulary;
- **dense:** semantic proximity after eligibility, with a pinned embedding implementation;
- **graph:** lineage, dependency, contradiction, supersession, identity, audience, sequence, and descendant edges;
- **visual:** visual-semantic descriptors or embeddings from an authorized projection, never raw VAE authority mutation;
- **syntax:** AST/schema/query/path structure for code, configuration, contracts, or formal artifacts;
- **evidence:** provenance strength, evaluator status, receipt linkage, reproduction, and epistemic state.

The profile declares which signals are required, optional, or forbidden per slot. Fusion shall use pinned weights or a pinned deterministic reranker. If a model is nondeterministic, it can propose features but a deterministic policy must normalize, constrain, and freeze the result; exact replay requires the recorded proposal bytes and model execution receipt.

### 5.6 Role-specific compilation workflow

The compiler starts from common authority, identity, attempt, and output-envelope items. It then applies one role profile:

- Hunter: include query space, source catalog, known gaps, discovery evidence, exclusions, and stopping law.
- Analyst: include exact claims/evidence, contradictions, supersession, failed alternatives, uncertainty, and evaluation contract.
- Composer: include only approved semantic ingredients/contracts, identity and continuity facts, locks, source-bound expression evidence, and output schema.
- Commander: include candidate/result refs, receipts, gates, descendant graph, cancellation/invalidation powers, recovery bounds, and human escalation.

When one actor performs multiple roles, it receives separate role capsules or an explicit composed capsule whose section boundaries, authorities, and permitted actions remain distinguishable.

### 5.7 Activation and downstream outcome workflow

A capsule may transition to active only after digest verification, dependency-current verification, Programmed Model/tool compatibility, and expected attempt revision. Activation stores the exact capsule digest on the execution attempt. Downstream output stores input capsule digest, model/tool receipts, output artifact digest, evaluation-profile ref, evaluation result ref, and descendant edges.

Production acceptance, downstream consumption acknowledgement, certification, and human approval remain distinct events. A good downstream outcome does not retroactively authorize an ineligible source; a poor outcome does not mutate the historical capsule.

### 5.8 Invalidation, repair, and replay workflow

An invalidation event names an exact source, projection, policy, model, capsule, or result version and a reason. The planner traverses stored dependency edges and classifies descendants as directly affected, transitively affected, or unaffected. It writes a proposed invalidation set and proof before applying state transitions atomically.

Repair uses the AIR-owned semantic repair requirement and Pipeline-owned runtime plan. If the responsible layer is unknown, the audience role/tension is unapproved, human authority is missing, or a repair proposal broadens scope, compilation stops with a typed escalation. Replay pins the original command, projection snapshots, rules, signals, model execution receipts, and effective instants. A current-state rerun is a new attempt, not historical replay.

### 5.9 Atomicity and concurrency

Each command uses optimistic concurrency on the aggregate revision. The atomic commit contains:

- immutable capsule bytes;
- retrieval and compiler receipt;
- candidate snapshot;
- command/idempotency record;
- lifecycle event;
- artifact and descendant edges;
- audit-envelope metadata.

If any write fails, none becomes visible. Repeating an idempotency key with identical canonical command bytes returns the prior outcome; reusing it with different bytes returns `RET-IDEMPOTENCY-CONFLICT`. Repository reads distinguish active/current from historical without deleting either.

## 6. Data models, contracts, schemas, and APIs

### 6.1 Common conventions

All persisted records are immutable, versioned, and content-addressed. Identifiers use bounded UTF-8 strings and normalized Unicode NFC. Timestamps in historical records are input facts and are encoded as UTC RFC 3339 with microseconds; the compiler does not call the wall clock while deriving deterministic identity. Hashes use lowercase SHA-256. Decimal scores use canonical strings, never platform floating-point serialization. Collections with no semantic order are sorted by their governed key before serialization.

References are repository-relative logical URIs or contract IDs. Drive letters, absolute paths, hostnames, temporary directories, and user names are forbidden in portable artifacts.

### 6.2 Core references

```text
ArtifactRef {
  artifact_id: NonEmptyId
  artifact_type: GovernedArtifactType
  owner_product: ProductId
  authority_owner: AuthorityOwnerId
  version: ImmutableVersion
  sha256: Sha256
  schema_id: SchemaId
  schema_version: SemVer
  lifecycle_state: GovernedLifecycleState
  epistemic_state: EpistemicState
  logical_uri: RelativeLogicalUri
}

ProjectionSnapshotRef {
  projection_id: ProjectionId
  source_product: ProductId
  purpose: PurposeId
  snapshot_version: ImmutableVersion
  source_set_sha256: Sha256
  projection_sha256: Sha256
  schema_id: SchemaId
  schema_version: SemVer
  compatibility_profile_id: CompatibilityProfileId
  lifecycle_watermark: ImmutableCursor
  trust_state: TrustState
}
```

`ArtifactRef` never implies that the Pipeline owns the referenced artifact. The pair `(owner_product, authority_owner)` is required and validated.

### 6.3 Context requirement model

```text
NodeContextRequirement {
  requirement_id: RequirementId
  version: ImmutableVersion
  sha256: Sha256
  declaring_product: ProductId
  authority_owner: AuthorityOwnerId
  node_binding_ref: ArtifactRef
  role_profile: HUNTER | ANALYST | COMPOSER | COMMANDER
  slots: ordered ContextSlotRequirement[1..N]
  common_obligations: CoverageObligation[*]
  allowed_projection_purposes: PurposeId[1..N]
  budget: ContextBudget
  retrieval_profile_ref: VersionedProfileRef
  compiler_profile_ref: VersionedProfileRef
  output_contract_ref: ArtifactRef
  evaluation_profile_ref: ArtifactRef
  stopping_law_ref: ArtifactRef
  effective_instant: PinnedInstant
}

ContextSlotRequirement {
  slot_id: SlotId
  semantic_purpose: GovernedPurpose
  classification: REQUIRED | CONDITIONAL_REQUIRED | OPTIONAL | FORBIDDEN | NOT_APPLICABLE
  conditional_rule_ref: Optional<ArtifactRef>
  not_applicable_rule_ref: Optional<ArtifactRef>
  authority_constraints: AuthorityConstraint[1..N]
  source_kind_constraints: SourceKindConstraint[*]
  lifecycle_constraints: LifecycleConstraint[1..N]
  compatibility_constraints: CompatibilityConstraint[*]
  identity_constraints: IdentityConstraint[*]
  evidence_constraints: EvidenceConstraint[*]
  freshness_policy: FreshnessPolicy
  contradiction_policy: ContradictionPolicy
  min_items: UInt
  max_items: UInt
  non_compressible: Boolean
  signal_policy: SignalPolicy
}
```

`NOT_APPLICABLE` is valid only with an evaluated governed rule reference and evidence. It is not a free-text shortcut. `FORBIDDEN` candidates are never passed to ranking. A conditional slot records its rule inputs and decision.

### 6.4 Budget contract

```text
ContextBudget {
  tokenizer_id: TokenizerId
  tokenizer_version: ImmutableVersion
  tokenizer_sha256: Sha256
  max_canonical_bytes: UInt
  max_input_tokens: UInt
  reserved_output_tokens: UInt
  per_slot_min_tokens: Map<SlotId, UInt>
  per_slot_max_tokens: Map<SlotId, UInt>
  metadata_overhead_policy: VersionedProfileRef
  overflow_behavior: BLOCK | GOVERNED_EXTRACT
}
```

Token counts are computed with the pinned tokenizer bytes. Canonical-byte limits remain authoritative for portability even when a model tokenizer changes. Required metadata, source references, locks, and receipt links count toward the capsule budget.

### 6.5 Candidate and eligibility models

```text
CandidateProjection {
  candidate_id: CandidateId
  artifact_ref: ArtifactRef
  projection_snapshot_ref: ProjectionSnapshotRef
  source_kind: GovernedSourceKind
  provenance_refs: ArtifactRef[*]
  category_profile_refs: ArtifactRef[*]
  identity_refs: ArtifactRef[*]
  embodiment_refs: ArtifactRef[*]
  feature_contract_refs: ArtifactRef[*]
  wrong_reading_lock_refs: ArtifactRef[*]
  lineage_edges: LineageEdge[*]
  valid_from: Optional<PinnedInstant>
  valid_until: Optional<PinnedInstant>
  content_descriptor_sha256: Sha256
  retrievable_payload_ref: RelativeLogicalUri
}

EligibilityDecision {
  candidate_id: CandidateId
  slot_id: SlotId
  eligible: Boolean
  evaluated_rules: RuleEvaluation[1..N]
  exclusion_codes: EligibilityCode[*]
  redaction_state: RedactionState
  decision_sha256: Sha256
}

EligibleCandidateSnapshot {
  snapshot_id: SnapshotId
  request_sha256: Sha256
  admitted: CandidateId[*]
  excluded: EligibilityDecision[*]
  authority_rule_set_ref: VersionedProfileRef
  eligibility_engine_version: ImmutableVersion
  sha256: Sha256
}
```

Unknown source kind, lifecycle state, profile, owner, schema, or compatibility value is rejected. Ambiguous source kind is never guessed. Interview-expression projections remain subject to their upstream provenance contract; the Pipeline validates required Reaction Receipt and Expression Moment references but does not create them.

### 6.6 Query and signal models

```text
RetrievalRequest {
  request_id: RequestId
  idempotency_key: IdempotencyKey
  tenant_id: TenantId
  program_id: ProgramId
  execution_attempt_id: AttemptId
  requirement_ref: ArtifactRef
  projection_snapshots: ProjectionSnapshotRef[1..N]
  retrieval_profile_ref: VersionedProfileRef
  query_facts: QueryFact[*]
  expected_repository_revision: UInt
}

SignalExecution {
  signal_id: SignalId
  family: EXACT | LEXICAL | DENSE | GRAPH | VISUAL | SYNTAX | EVIDENCE
  implementation_id: ImplementationId
  implementation_version: ImmutableVersion
  implementation_sha256: Sha256
  model_ref: Optional<ProgrammedModelBinding>
  normalized_query_sha256: Sha256
  candidate_snapshot_sha256: Sha256
  budget: SignalBudget
  ordered_hits: SignalHit[*]
  execution_receipt_sha256: Sha256
}

SignalHit {
  candidate_id: CandidateId
  raw_score: CanonicalDecimal
  normalized_score: CanonicalDecimal
  matched_feature_refs: FeatureRef[*]
  rank: UInt
}
```

An adapter returns only candidate IDs present in the eligible snapshot. Unexpected IDs are a hard contract failure.

### 6.7 Fusion, contradiction, and selection models

```text
RankedCandidate {
  candidate_id: CandidateId
  slot_id: SlotId
  authority_tier: UInt
  feature_vector: ordered RankingFeature[1..N]
  fused_score: CanonicalDecimal
  stable_tie_break_key: CanonicalString
  rank: UInt
}

CoverageObligation {
  obligation_id: ObligationId
  kind: SLOT_MINIMUM | EXACT_DEPENDENCY | PROVENANCE | CONTRADICTION | FAILED_ALTERNATIVE |
        SUPERSESSION | WRONG_READING_LOCK | IDENTITY_CONTINUITY | STOPPING_LAW | EVALUATOR_INPUT
  subject_refs: ArtifactRef[*]
  minimum_coverage: UInt
  resolution_rule_ref: Optional<ArtifactRef>
  non_compressible: Boolean
}

ContextSelection {
  selection_id: SelectionId
  ranked_snapshot_sha256: Sha256
  selected: SelectedItem[1..N]
  excluded_after_ranking: SelectionExclusion[*]
  coverage_proofs: CoverageProof[1..N]
  deletion_proofs: DeletionProof[1..N]
  budget_accounting: BudgetAccounting
  unavailable_obligations: UnavailableObligation[*]
  selection_sha256: Sha256
}
```

A selection with any unavailable required obligation is non-compilable. The unavailable facts remain in the receipt and blocker.

### 6.8 Capsule item and derived-summary models

```text
CapsuleItem {
  item_id: ItemId
  slot_id: SlotId
  classification: REQUIRED | CONDITIONAL_REQUIRED
  source_ref: ArtifactRef
  source_fragment_ref: Optional<CanonicalFragmentRef>
  exact_content_sha256: Sha256
  inclusion_reason_codes: InclusionReason[1..N]
  satisfied_obligation_ids: ObligationId[1..N]
  provenance_refs: ArtifactRef[*]
  lineage_edges: LineageEdge[*]
  compression: Optional<CompressionRecord>
  portable_payload: CanonicalValue
}

CompressionRecord {
  compiler_id: ImplementationId
  compiler_version: ImmutableVersion
  compiler_sha256: Sha256
  input_item_refs: ArtifactRef[1..N]
  input_content_sha256s: Sha256[1..N]
  output_sha256: Sha256
  loss_declaration: LossDeclaration
  preserved_exact_fragments: CanonicalFragmentRef[*]
  verification_receipt_ref: ArtifactRef
}
```

Generic “notes” cannot replace a required semantic object. If the downstream contract requires an Activative Call, Reaction Receipt, Expression Moment, Activation Contract, Visual Semantic Pack, Visual Narrative Program, Feature Contract, T/V route, Composition Intent, identity object, or wrong-reading lock, the capsule carries a typed exact reference and the required projection fields.

### 6.9 JIT Execution Capsule

```text
JITExecutionCapsule {
  capsule_id: CapsuleId
  capsule_schema_version: SemVer
  compiler_id: ImplementationId
  compiler_version: ImmutableVersion
  compiler_sha256: Sha256
  request_ref: ArtifactRef
  execution_attempt_id: AttemptId
  node_binding_ref: ArtifactRef
  role_profile: RoleProfile
  actor_binding: ActorBinding
  authority_binding: AuthorityBinding
  capability_binding: CapabilityBinding
  programmed_model_binding: Optional<ProgrammedModelBinding>
  tool_grants: ToolGrant[*]
  items: ordered CapsuleItem[1..N]
  exclusions_summary: ExclusionSummary
  budget_accounting: BudgetAccounting
  output_contract_ref: ArtifactRef
  evaluation_profile_ref: ArtifactRef
  stopping_law_ref: ArtifactRef
  retrieval_receipt_ref: ArtifactRef
  production_eligible: false
  certified: false
  sha256: Sha256
}
```

The capsule ID derives from canonical capsule bytes excluding the self-hash field; the stored self-hash is then placed in the envelope. The envelope and payload canonicalization algorithms are versioned.

### 6.10 Programmed Model binding

```text
ProgrammedModelBinding {
  programmed_model_id: ProgrammedModelId
  implementation_id: ImplementationId
  implementation_version: ImmutableVersion
  artifact_sha256: Sha256
  capability_profile_ref: ArtifactRef
  claim_envelope_ref: ArtifactRef
  permitted_roles: RoleProfile[1..N]
  permitted_signal_families: SignalFamily[*]
  supported_input_contracts: ContractRef[1..N]
  supported_output_contracts: ContractRef[1..N]
  data_boundary_ref: ArtifactRef
  deterministic_mode: DeterminismMode
  certification_state: CertificationState
}
```

`certification_state` is evidence, not authority. An uncertified but separately permitted candidate may be used only where the node’s gate permits it; this specification does not grant that permission. A model cannot be selected if its claim envelope omits a required capability or if its data boundary conflicts with a projection.

### 6.11 Receipt model

```text
RetrievalAndCapsuleReceipt {
  receipt_id: ReceiptId
  command_sha256: Sha256
  requirement_sha256: Sha256
  projection_snapshot_refs: ProjectionSnapshotRef[1..N]
  eligibility_snapshot_ref: ArtifactRef
  query_plan_ref: ArtifactRef
  signal_execution_refs: ArtifactRef[*]
  ranking_profile_ref: ArtifactRef
  ranked_snapshot_ref: ArtifactRef
  coverage_and_selection_ref: ArtifactRef
  compression_refs: ArtifactRef[*]
  excluded_candidate_counts_by_code: Map<EligibilityCode, UInt>
  unavailable_context: UnavailableObligation[*]
  capsule_ref: ArtifactRef
  downstream_attempt_ref: Optional<ArtifactRef>
  downstream_outcome_ref: Optional<ArtifactRef>
  evaluation_result_ref: Optional<ArtifactRef>
  repository_revision: UInt
  receipt_sha256: Sha256
}
```

The receipt can prove why an item was included, why a candidate was excluded, which model/signals affected rank, which compression occurred, which required context was unavailable, and what downstream result consumed the capsule.

### 6.12 Commands and events

Commands:

- `RegisterProjectionSnapshotCommand`
- `CompileJITCapsuleCommand`
- `VerifyJITCapsuleCommand`
- `ActivateJITCapsuleCommand`
- `RecordCapsuleOutcomeCommand`
- `InvalidateRetrievalDependencyCommand`
- `PlanSelectiveCapsuleReplayCommand`
- `DisposeActiveCapsuleCommand`

Events:

- `ProjectionSnapshotRegistered`
- `EligibleCandidateSnapshotFrozen`
- `RetrievalSignalsExecuted`
- `MinimumCompleteContextSelected`
- `JITCapsuleCompiled`
- `JITCapsuleVerified`
- `JITCapsuleActivated`
- `CapsuleOutcomeRecorded`
- `RetrievalDependencyInvalidated`
- `CapsuleInvalidated`
- `SelectiveReplayPlanned`
- `JITCapsuleDisposed`

Every command stores canonical input bytes, idempotency key, expected revision, actor/tool authority, decision or error, and emitted event IDs.

### 6.13 Service ports

```text
ProjectionRegistryPort.register(snapshot) -> RegistrationReceipt
ProjectionReaderPort.enumerate(snapshot_ref, predicates, cursor) -> CandidatePage
EligibilityPort.freeze(request, candidates, rules) -> EligibleCandidateSnapshot
SignalAdapterPort.execute(plan, eligible_snapshot) -> SignalExecution
RankingPort.rank(executions, profile) -> RankedCandidateSnapshot
ContextSolverPort.solve(requirement, ranked_snapshot) -> ContextSelection | TypedBlocker
CapsuleCompilerPort.compile(selection, binding) -> CapsuleArtifact
CapsuleRepositoryPort.commit_atomic(commit_bundle, expected_revision) -> CommitReceipt
DependencyGraphPort.plan_invalidation(trigger) -> InvalidationPlan
OutcomePort.record(attempt, capsule_ref, result_ref, evaluation_ref) -> OutcomeReceipt
```

Ports accept and return domain records, not untyped dictionaries. Adapters validate at the boundary and never pass unknown enum values inward.

### 6.14 Lifecycle states

The capsule lifecycle is:

`COMPILED -> VERIFIED -> ACTIVE -> DISPOSED`

with `COMPILED`, `VERIFIED`, or `ACTIVE` able to transition to `INVALIDATED`; any state may receive a non-consuming `REVOKED` authority overlay from an owning product. A failed verification creates a failure receipt but does not mutate artifact bytes. Only one capsule digest may be active for a `(execution_attempt_id, node_binding_version, role_profile)` tuple. Historical attempts keep their active-at-time relationship after later invalidation.

### 6.15 Compatibility and migration

Compatibility is semantic and feature-based. The consumer declares required features such as `AUTHORITY_FIRST_ELIGIBILITY`, `CONTRADICTION_COVERAGE`, `ROLE_SPECIFIC_MCC`, `PORTABLE_REFERENCES`, `SELECTIVE_INVALIDATION`, and the needed signal families. Missing required features fail negotiation. An adapter may add evidence or transform encoding without removing authority, provenance, lineage, locks, obligations, exclusions, or lifecycle meaning.

Migration creates new immutable projection/capsule artifacts and a migration receipt linking old and new hashes. Active historical attempts remain pinned to their negotiated versions. Deprecating a version blocks new negotiation when governed but does not invalidate reproducible history.

## 7. Intended implementation surfaces and import boundaries

No files in this section are created by this writing prompt. They define the later build boundary only.

### 7.1 Proposed Pipeline paths

```text
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/domain/models.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/domain/eligibility.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/domain/context_solver.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/domain/lifecycle.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/application/commands.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/application/services.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/application/invalidation.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/ports/projections.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/ports/signals.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/ports/repository.py
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/adapters/persistence/
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/adapters/signals/
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/adapters/projections/
05_ATOMIC_HARNESS_PIPELINE/src/atomic_harness_pipeline/retrieval/api/
```

### 7.2 Import rules

- `domain` imports only standard-library/value-object utilities and cannot import adapters, frameworks, model SDKs, Builder, AIR, VAE, Studio, or Delegation.
- `application` imports domain and ports, never concrete adapters.
- `ports` expose Protocol/ABC contracts over domain types.
- `adapters` import their port and external client only; adapter-specific payloads do not leak into domain models.
- `api` translates transport envelopes to application commands and has no authority logic.
- Product integrations exchange published contracts/projections. They do not import another product’s source tree.
- Evaluation adapters remain independent of candidate-model adapters where the profile requires independent evaluation.

### 7.3 Persistence boundary

The durable repository shall support atomic multi-object commit, optimistic revision, unique idempotency key, immutable content blobs, append-only events, active indexes, dependency-edge indexes, and historical queries. An in-memory adapter is permitted for unit tests only and must pass the same repository contract tests. It may not use shared mutable defaults or return live internal collections.

### 7.4 Configuration boundary

Retrieval, eligibility, ranking, tokenizer, compiler, and evaluation profiles are immutable governed artifacts, not process environment switches. Environment variables may locate infrastructure or credentials but cannot change semantic behavior, candidate ordering, eligibility, or canonical output without changing a pinned profile identity.

## 8. Failure behavior, recovery, security, and observability

### 8.1 Typed failures

| Code | Meaning | Retry | Owner/escalation |
|---|---|---|---|
| `RET-REQUIREMENT-INVALID` | Context requirement is malformed, mutable, or unversioned | No | Declaring product |
| `RET-AUTHORITY-CONFLICT` | Applicable authorities conflict or owner is ambiguous | No automatic retry | Program authority owner |
| `RET-PROJECTION-UNAUTHORIZED` | Purpose/scope does not permit projection use | No | Source product/security operator |
| `RET-PROJECTION-STALE` | Snapshot fails governed freshness/lifecycle rule | Retry only with new pinned snapshot | Source product |
| `RET-COMPATIBILITY-UNSUPPORTED` | Schema/profile/required feature is unsupported | No | Integration owner |
| `RET-SOURCE-KIND-UNKNOWN` | Source-kind enum is unknown or ambiguous | No guessing | Source owner |
| `RET-PROVENANCE-INCOMPLETE` | Required provenance refs are absent/empty | No | Source owner |
| `RET-ELIGIBILITY-ENGINE-FAILURE` | Deterministic eligibility could not complete | Safe retry on same inputs | Pipeline |
| `RET-SIGNAL-CONTRACT-VIOLATION` | Signal adapter returned an ineligible/unknown candidate | Quarantine adapter | Pipeline adapter owner |
| `RET-MODEL-CLAIM-UNSUPPORTED` | Programmed Model claim envelope lacks capability | No | Capability owner |
| `RET-CONTRADICTION-MISSING` | Required contradictory/failed/superseding evidence absent | No silent omission | Requirement/source owner |
| `RET-MANDATORY-CONTEXT-UNAVAILABLE` | Required slot has insufficient eligible context | Retry only with governed new evidence | Declaring/source owner |
| `RET-BUDGET-UNSATISFIABLE` | Mandatory complete context exceeds budget | No truncation; escalate | Declaring product/operator |
| `RET-COMPRESSION-UNVERIFIED` | Derived summary lacks preservation proof | Retry without compression if budget permits | Pipeline |
| `RET-NONDETERMINISTIC-OUTPUT` | Same inputs produce different canonical bytes | No activation; incident | Pipeline |
| `RET-IDEMPOTENCY-CONFLICT` | Key reused with different command bytes | No | Caller |
| `RET-REVISION-CONFLICT` | Expected aggregate revision is stale | Retry after reread | Caller/Pipeline |
| `RET-ATOMIC-COMMIT-FAILED` | Commit bundle was not wholly persisted | Safe retry if no commit receipt | Persistence owner |
| `RET-CAPSULE-STALE` | Dependency changed after compile | Recompile as new capsule | Pipeline/source owner |
| `RET-REPLAY-EVIDENCE-MISSING` | Historical signal/model/projection evidence unavailable | No fabricated replay | Evidence owner |
| `RET-REPAIR-SCOPE-BROADENED` | Proposed repair affects unrelated scope | No | AIR/Commander/human escalation |
| `RET-LEGACY-EVIDENCE-INCOMPLETE` | Legacy capsule cannot prove required current invariants | No migration guess | Migration owner |

Failures are domain results with stable codes, safe operator messages, precise context refs, responsible layer when known, retry classification, and evidence links. Raw stack traces, prompts, credentials, or restricted payloads do not cross external boundaries.

### 8.2 Retry and compensation

Reads and pure deterministic compilation may retry against the same pinned inputs. External model/signal calls require an idempotent execution key and stored response digest. A timed-out call with unknown completion state is reconciled before retry. There is no “best effort” partial capsule: a failed compile commits a command/failure receipt but no active capsule.

If the artifact blob is durably written but the transaction aborts before visibility, the blob remains unreachable and is garbage-collected only after a safe retention interval. Compensation never deletes a referenced historical artifact.

### 8.3 Invalidation and historical reproduction

Dependency edges include source artifact, projection snapshot, policy/rule set, tokenizer, signal implementation/model, ranking profile, compiler, Programmed Model binding, tool contract, and evaluation profile. Invalidation evaluates exact edges and stored rule outcomes. Broad “invalidate all” is prohibited unless a governed incident explicitly authorizes that scope.

Historical reproduction has two modes:

- **exact replay:** use stored immutable inputs and execution responses to reproduce the same capsule bytes and digest;
- **current-state rerun:** issue a new command against current projections/profiles and link it as a successor.

The API and receipt must not confuse those modes.

### 8.4 Security and privacy

- Enforce tenant/program/purpose partitioning before candidate content is read.
- Apply least-privilege credentials per projection and signal adapter.
- Redact excluded-candidate content from callers without content permission while retaining an auditable protected record.
- Encrypt persisted restricted payloads and transport; store secrets only in a secret manager.
- Reject path traversal, archive traversal, drive-qualified paths, UNC paths, device paths, symlink escapes, and unsafe URI schemes.
- Limit query size, candidate count, graph depth, contradiction expansion, model calls, output bytes, and execution duration under pinned profiles.
- Treat retrieved text and metadata as untrusted data, not executable instructions. Tools are granted only by the capsule's explicit tool contract.
- Preserve provenance, operator-supplied source authority, and product sovereignty. Technical security does not become creative approval authority.

### 8.5 Observability

Metrics include compile attempts by terminal code, eligibility counts by reason, per-signal latency/error counts, candidate and selected counts, context bytes/tokens, contradiction coverage, compression ratio, cache hit, deterministic replay mismatch, invalidation breadth, selective-replay breadth, and downstream evaluation linkage rate.

Traces carry request/attempt/capsule/receipt correlation IDs and component spans, not raw restricted content. Logs expose artifact IDs, versions, hashes, reason codes, and counts under access policy. High-cardinality IDs use trace storage rather than unrestricted metric labels.

Alerts cover nondeterministic output, ineligible-candidate leakage to a ranker, missing command/receipt/artifact linkage, atomicity invariant failure, unexplained broad invalidation, replay-evidence loss, cross-tenant access, and activation of a stale capsule.

### 8.6 Operational invariants

At all observable revisions:

- every active capsule has immutable bytes, a receipt, a command record, and dependency edges;
- every receipt that names a capsule resolves to those exact bytes;
- every completed idempotency key resolves to exactly one canonical command and terminal result;
- no rank snapshot contains an ineligible candidate;
- no consumed capsule is missing its activation and execution-attempt link;
- invalidation never destroys reproducibility;
- production eligibility and certification remain false absent separate governed evidence.

## 9. Acceptance criteria

The following criteria are for later independent audit and acceptance. Satisfying them in a future implementation does not itself grant build or production authority.

### AC-01 — Packet and ownership traceability

**Given** this spec is evaluated, **when** its traceability is inspected, **then** all seven FRs, both Stories, exact packet identity, candidate-authority label, Pipeline ownership, and upstream draft labels are present. Failure: `RET-SPEC-TRACEABILITY-GAP`. Evidence: spec index and traceability report. Layer: specification governance. Trace: `FR-019..024`, `AIR-FR-113`, `ST-07.01`, `AIR-ST-19.03`.

### AC-02 — Authority before similarity

**Given** an unauthorized candidate has the best dense score, **when** retrieval runs, **then** the candidate is excluded before the dense adapter and absent from every rank snapshot. Failure: `RET-INELIGIBLE-RANKED`. Evidence: candidate snapshot, adapter request, exclusion receipt. Layer: Pipeline eligibility. Trace: `FR-020`.

### AC-03 — Unknown source kind

**Given** a projection with an unknown or ambiguous source kind, **when** eligibility runs, **then** it returns `RET-SOURCE-KIND-UNKNOWN` and does not infer a value. Evidence: negative test and receipt. Layer: projection boundary. Trace: `FR-019`, `FR-020`.

### AC-04 — Interview provenance

**Given** `interview_expression` context missing a non-empty Reaction Receipt or Expression Moment reference, **when** eligibility runs, **then** it returns `RET-PROVENANCE-INCOMPLETE`; non-interview context validates supplied interview refs but does not require them. Evidence: parameterized provenance tests. Layer: source projection. Trace: `FR-019`, `FR-020`.

### AC-05 — Typed slots and N/A

**Given** required, conditional, optional, forbidden, and not-applicable slots, **when** the requirement is evaluated, **then** only governed conditional and N/A decisions are accepted; free-text N/A and forbidden inclusion fail. Evidence: rule-evaluation receipt. Layer: requirement intake. Trace: `FR-019`.

### AC-06 — Hybrid signals

**Given** a profile requiring exact, lexical, graph, dense, and evidence signals, **when** retrieval runs, **then** all required pinned adapters execute within budget and return only eligible candidate IDs. Evidence: query plan and signal receipts. Layer: retrieval. Trace: `FR-021`.

### AC-07 — Stable ordering

**Given** equal fused scores and different enumeration orders across processes, **when** candidates are ranked, **then** canonical ordering and final capsule bytes are identical. Evidence: shuffled-order repeated test. Layer: ranking/determinism. Trace: `FR-021`, `FR-023`.

### AC-08 — Contradiction coverage

**Given** a node contract requiring contradictory and superseding evidence, **when** minimum context is selected, **then** each obligation has a selected proof or compilation blocks with `RET-CONTRADICTION-MISSING`. Evidence: coverage proof and hard-negative fixture. Layer: context solver. Trace: `FR-022`.

### AC-09 — Failed alternatives

**Given** an AIR repair request requiring failed alternatives, **when** the Analyst capsule is compiled, **then** failed alternative refs, rejection reasons, and epistemic states remain explicit and typed. Evidence: capsule inspection. Layer: compiler. Trace: `AIR-FR-113`, `AIR-ST-19.03`.

### AC-10 — Minimum completeness

**Given** redundant eligible items, **when** the solver completes, **then** every selected item has a deletion proof and removing any one breaks a coverage obligation; optional padding is absent. Evidence: solver proof and minimality property test. Layer: context solver. Trace: `FR-023`, `ST-07.01`.

### AC-11 — Unsatisfiable budget

**Given** mandatory exact context exceeds the pinned budget, **when** compilation runs, **then** it returns `RET-BUDGET-UNSATISFIABLE`, identifies the obligations and required size, and emits no active capsule. Evidence: failure receipt and repository query. Layer: compiler/repository. Trace: `FR-019`, `FR-023`.

### AC-12 — Compression provenance

**Given** governed extraction is allowed, **when** compressed context is selected, **then** source hashes, compiler identity, loss declaration, exact preserved fragments, and verification receipt are present; required exact locks and approvals are unchanged. Evidence: compression conformance test. Layer: compiler. Trace: `FR-023`.

### AC-13 — Semantic lineage preservation

**Given** a capsule requires typed Activative lineage objects, **when** it is serialized, **then** exact typed refs and lineage edges exist and none is flattened to generic notes. Evidence: schema/round-trip and field-presence tests. Layer: compiler. Trace: `AIR-FR-113`.

### AC-14 — Role separation

**Given** the same attempt requires Hunter, Analyst, Composer, and Commander work, **when** capsules are compiled, **then** each has its bounded slot profile and distinct actor, authority, capability, tool, evaluator, and stopping-law bindings. Evidence: role matrix test. Layer: compiler/binder. Trace: `AIR-FR-113`, `ST-07.01`.

### AC-15 — Programmed Model claim envelope

**Given** a model with high evaluation scores but a missing required capability, **when** binding occurs, **then** it is rejected with `RET-MODEL-CLAIM-UNSUPPORTED`. Evidence: binding negative test. Layer: model binder. Trace: `FR-020`, `FR-021`.

### AC-16 — Source-product sovereignty

**Given** AIR, VAE, Builder, or Interview Expression data, **when** retrieved, **then** Pipeline reads only an authorized immutable projection and never changes the source canonical object. Evidence: architecture/import and mock-port tests. Layer: integration boundary. Trace: all controlled requirements.

### AC-17 — Portable deterministic bytes

**Given** identical inputs across machines, temporary roots, locales, environment variables, process clocks, and randomized map/traversal order, **when** compilation runs twice, **then** canonical bytes and SHA-256 match and contain no absolute machine path. Evidence: fresh-process portability suite. Layer: serialization. Trace: `FR-023`, `FR-024`.

### AC-18 — Complete receipt

**Given** a successful compile, **when** the receipt is queried, **then** it exposes filters, admitted/excluded candidates, signal/model versions, rankings, selection/deletion proofs, compression, unavailable context, capsule digest, and later downstream outcome links. Evidence: receipt conformance. Layer: receipt repository. Trace: `FR-024`.

### AC-19 — Atomic commit

**Given** injected failure at each persistence step, **when** commit runs, **then** no partial visible artifact/receipt/command/event relation exists; a successful retry creates one result. Evidence: transactional fault-injection tests. Layer: repository. Trace: `FR-024`, `ST-07.01`.

### AC-20 — Idempotency conflict

**Given** the same idempotency key, **when** identical bytes are replayed, **then** the prior result returns; when different bytes are supplied, `RET-IDEMPOTENCY-CONFLICT` returns without mutation. Evidence: repository contract tests. Layer: application/repository. Trace: `FR-024`.

### AC-21 — Optimistic concurrency

**Given** two commands at one expected revision, **when** both attempt activation, **then** exactly one commits and the other receives `RET-REVISION-CONFLICT`; at most one capsule is active for the tuple. Evidence: concurrency test. Layer: repository. Trace: `FR-024`.

### AC-22 — Selective invalidation

**Given** one source artifact is superseded, **when** invalidation is planned, **then** only capsules/results with proven dependency edges and their affected descendants are invalidated; unrelated attempts remain consumable. Evidence: branching graph test. Layer: invalidation planner. Trace: `AIR-ST-19.03`.

### AC-23 — Historical reproduction

**Given** a capsule is later invalidated or revoked, **when** exact historical replay is requested, **then** immutable inputs and stored execution responses reproduce the original bytes and digest without making it currently consumable. Evidence: historical replay test. Layer: lifecycle/repository. Trace: `AIR-ST-19.03`, `FR-024`.

### AC-24 — Bounded repair

**Given** a failure attributed to one layer, **when** replay planning occurs, **then** the plan does not broaden semantic scope or regenerate unrelated descendants; unknown responsibility returns escalation. Evidence: repair-scope property test. Layer: invalidation/replay. Trace: `AIR-ST-19.03`.

### AC-25 — Architecture boundaries

**Given** the implementation tree, **when** import tests run, **then** domain imports no framework/product/adapters, products exchange projections/contracts rather than source imports, and learned adapters cannot call authority mutation ports. Evidence: AST import test plus behavioral port tests. Layer: architecture. Trace: ownership decisions.

### AC-26 — Security boundary

**Given** cross-tenant candidates, unsafe logical paths, prompt-like retrieved text, or oversized graph expansion, **when** processing occurs, **then** access is denied or bounded, paths are rejected, text is inert data, and no unauthorized tool executes. Evidence: security-negative suite. Layer: projection/compiler/tool boundary. Trace: `FR-020`, `FR-023`.

### AC-27 — Downstream decision evidence

**Given** a retrieval benchmark case, **when** the capsule is consumed and evaluated, **then** the outcome links to the exact capsule and can compare context size, hard-negative rejection, and decision quality without altering the retrieval receipt. Evidence: benchmark receipt. Layer: outcome/evaluation. Trace: `FR-024`, `ST-07.01`.

### AC-28 — Claim ceiling

**Given** all technical tests pass, **when** status is emitted under pending ratification, **then** quality is at most `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`, build/production/certification remain false, and no capsule is called accepted-for-build. Evidence: status-policy test. Layer: governance. Trace: packet authority rule.

## 10. Testing, evidence, rollout constraints, and completion

### 10.1 Unit tests

- classification, governed conditional, and governed N/A evaluation;
- authority/lifecycle/category/profile/identity/embodiment/provenance/freshness filters;
- unknown enum and ambiguous source-kind rejection;
- interview provenance rules;
- exact/lexical/dense/graph/visual/syntax/evidence adapter contracts;
- score normalization and stable tie-breaks;
- contradiction/supersession/failure obligation expansion;
- minimum-context solver and deletion-proof properties;
- tokenizer/budget accounting and mandatory overflow;
- compression non-loss and exact-fragment preservation;
- role-profile slot allowlists;
- Programmed Model claim-envelope binding;
- canonical serialization, content identity, relative path enforcement;
- lifecycle transition, idempotency, and optimistic concurrency rules.

### 10.2 Contract and integration tests

- projection adapters for AIR, Builder/Harness, Interview Expression, VAE, Studio, and Delegation-facing envelopes;
- repository atomic commit under stepwise fault injection;
- immutable projection refresh and source supersession;
- retrieval-to-capsule-to-execution-to-evaluation receipt chain;
- compatibility negotiation with required feature flags;
- legacy Builder capsule migration with explicit incomplete-evidence blocking;
- independent evaluator separation from candidate model;
- adapter rejection when it emits an ID outside the eligible snapshot;
- no product source-tree imports or canonical-store mutations.

### 10.3 Determinism and portability tests

Run the same governed fixture at least twice in fresh processes while varying:

- input dictionary insertion order;
- projection enumeration and filesystem traversal order;
- wall clock and timezone;
- locale;
- random seeds;
- temporary/workspace root;
- environment-variable ordering and unrelated values;
- process ID and host name.

Assert byte-identical request normalization, eligible snapshot, rank snapshot, context selection, capsule, and receipts. Scan all generated artifacts for drive letters, UNC paths, user profile paths, temporary roots, and hostnames.

### 10.4 Retrieval benchmark evidence

The completion evidence for `ST-07.01` requires a governed benchmark with:

- positive eligible context;
- semantically attractive but authority-ineligible hard negatives;
- stale and superseded versions;
- category/profile and identity mismatches;
- source-provenance failures;
- required contradictions and failed alternatives;
- missing-context and over-budget cases;
- role-specific tasks for Hunter, Analyst, Composer, and Commander;
- exact baseline corpus scan and bounded-capsule comparison.

Report eligibility precision/recall against governed labels, hard-negative leakage, required-obligation coverage, capsule byte/token reduction, deterministic replay rate, latency/cost, and downstream decision lift. No universal evaluator threshold is invented here; a later ratified benchmark/evaluation profile must define claim-specific thresholds and confidence intervals.

### 10.5 Failure, invalidation, and replay tests

Build a branching dependency fixture containing shared and unrelated ancestors/descendants. Inject projection revocation, source supersession, ranking-profile defect, Programmed Model withdrawal, evaluator correction, and post-completion invalidation. Prove exact affected-set calculation, retention of historical bytes, distinct exact-replay/current-rerun semantics, no broad repair, and typed escalation when attribution is unknown.

### 10.6 Required completion evidence

Before any later build acceptance, evidence must include:

1. requirements-to-tests traceability for all controlled FRs and Stories;
2. repository contract-test results for durable and in-memory adapters;
3. deterministic fresh-process reproduction matrix;
4. security and unsafe-path test report;
5. hybrid retrieval benchmark and hard-negative corpus manifest;
6. Minimum Complete Context minimality and coverage proofs;
7. selective invalidation/historical replay proof;
8. source-product projection ownership conformance;
9. independent architecture/import-boundary audit;
10. failure and observability catalog verification;
11. migration evidence for any legacy capsule;
12. current ratification, product adoption, and Build authorization receipts.

### 10.7 Rollout constraints

A future implementation shall begin behind a non-production feature gate and operate on synthetic/hash-locked fixtures. Shadow evaluation may compare proposed capsules with existing behavior without authorizing their consumption. Canary or production use is prohibited until authority ratification, product adoption, independent audit/revision/re-audit, required benchmark evidence, operational readiness, and an authorized Development Capsule are complete.

Rollback disables new capsule activation and returns callers to the last governed compatible path; it does not delete projections, capsules, receipts, outcomes, or invalidation history. Active attempts remain pinned to their accepted capsule and negotiated versions unless a governed revocation or invalidation blocks consumption.

### 10.8 Draft-dependency revision impacts

This spec consumed `TS-AHP-002` and `TS-AIR-019` as `DRAFT_DEPENDENCY_NOT_ACCEPTED`. A new upstream digest or accepted change triggers a downstream-impact review of:

- section 3, if authority, role, node, Programmed Model, or repair ownership changes;
- section 5, if the binding, execution, repair, replay, or lifecycle workflow changes;
- section 6, if any referenced contract, state, field, enum, error, or compatibility rule changes;
- section 8, if failure attribution, recovery, invalidation, security, or observability changes;
- section 9, if acceptance evidence or responsible layers change;
- section 10, if tests, benchmarks, rollout gates, or completion evidence change.

Until that review is receipted, the affected draft is stale for later acceptance, though its historical bytes remain reproducible.

### 10.9 Writing completion declaration

This document completes only the WRITE stage for packet `CA-P03-WRITE-TS-RET-001-RECOVERY`. Its quality state is `WRITTEN_PENDING_AUDIT`. It has not been self-audited, revised, re-audited, accepted, adopted for build, implemented, certified, or released. Candidate authority remains `CANDIDATE_NOT_CURRENT`; specification work is authorized; build authority is false; and the pre-ratification acceptance ceiling remains `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
