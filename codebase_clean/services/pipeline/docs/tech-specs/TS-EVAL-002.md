# TS-EVAL-002 - Rendered Visual Syntax Reparse and Responsible-Layer Diagnosis

```yaml
spec_id: TS-EVAL-002
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product: Atomic Harness Pipeline
primary_owner: Independent Evaluation
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: INDEPENDENT_AUDIT_REQUIRED
writing_wave: 13
controlling_frs: [FR-093, FR-094]
controlling_story: ST-09.02
upstream_dependency_label: DRAFT_DEPENDENCY_NOT_ACCEPTED
```

This is a candidate specification written under the Prompt 02C specification-work authorization. It does not make candidate authority current, authorize implementation, issue a Development Capsule, certify an evaluator, authorize VAE production, or permit `ACCEPTED_FOR_BUILD`.

## 1. Files and authorities read

The following exact inputs were read. Candidate and upstream drafts are explicitly non-accepted interfaces.

| Source | State / classification | Use |
|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current constitutional authority | Preserves semantic lineage, human reaction, visual narrative, wrong-reading locks, and product sovereignty. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate, `CANDIDATE_NOT_CURRENT` | AIR owns meaning; Pipeline evaluates and orchestrates; VAE realizes; Delegation transports. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate, `CANDIDATE_NOT_CURRENT` | Prevents evaluator-side reconstruction or mutation of semantic objects. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | recovery packet | Pins FR-093/FR-094, ST-09.02, Wave 13, target path, claim ceiling, and source list. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_13_DISPATCH_LOCK.yaml` | frozen dispatch | Pins `TS-EVAL-001` at `0c3a47dc3cfb331630df794bec4869c71d5fc70894b6f0fd77b08068ff74024f` as a non-accepted draft. |
| `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-EVAL-001.md` | `WRITTEN_PENDING_AUDIT`, non-accepted | Supplies profile, deterministic-first, independent-judgment, hard-gate, and receipt interfaces. |
| `02_VISUAL_ASSET_EDITOR/prd/05-features/F14-visual-evaluation-profiles.md` | current VAE requirement | Profile applicability, deterministic checks, and hard-gate precedence. |
| `02_VISUAL_ASSET_EDITOR/prd/05-features/F15-repair-invalidation-reruns.md` | current VAE requirement | Causal repair, selective invalidation, and no threshold lowering. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/prd/features/F16-independent-evaluation-visual-syntax-reparse-diagnosis-and-selective-repair.md` | candidate FR source | Normative FR-093 and FR-094 behavior. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | candidate Story source | ST-09.02 journey, denial, replay, CBAR, and selective recovery criteria. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/render_qa.py` | legacy evidence | Reusable historical categories only; mutable/time/random identity is not current authority. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/render_qa_service.py` | legacy evidence | Reusable orchestration boundary; does not define independent evaluation authority. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/ffprobe_validation_service.py` | legacy evidence | Deterministic media evidence adapter boundary. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/frame_sampling_service.py` | legacy evidence | Deterministic frame evidence adapter boundary. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/audio_level_analysis_service.py` | legacy evidence | Deterministic audio evidence adapter boundary. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SOURCE_DISPOSITION_LEDGER.yaml` | current source policy | Optional/deferred sources cannot be reconstructed or treated as authority. |
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3 required method | One-spec writing, ten sections, no self-audit or acceptance. |

No unavailable `REQUIRED_AUTHORITY`, `REQUIRED_CURRENT_IMPLEMENTATION`, or `REQUIRED_UNIQUE_EVIDENCE` source was used to make a factual claim. Any deferred profile or calibration evidence remains a typed blocker.

## 2. Problem, solution, scope, and non-goals

### Problem and outcome

The pipeline needs to compare an intended visual contract with what was actually rendered and identify the responsible layer without allowing the producer to approve itself. Legacy QA wraps supplied measurements but cannot prove exact reparse identity, semantic context, evaluator independence, or safe selective recovery. A plausible visual result can therefore hide a hierarchy, reading-order, timing, or responsible-layer failure.

### Bounded solution

Define a deterministic reparse boundary and a diagnosis record that consumes an immutable evaluation run, exact artifact bytes, and hash-pinned intended contracts. The boundary emits observed static and temporal syntax, compares it with the intended contract, records typed discrepancies, and attributes each discrepancy to a governed layer. It provides evidence for a repair controller; it does not perform repair or change semantic authority.

### In scope

- FR-093 observed BBOX, hierarchy, reading order, temporal timing, and contract comparison.
- FR-094 distinction among knowledge, retrieval, context, Programmed Model, tool, runtime, VAE, and evaluator defects.
- Separate deterministic reparse and independent judgment receipts.
- Immutable identity, replay, invalidation, cancellation, selective rerun, and downstream handoff.
- Exact AIR/VAD/Visual Semantic Pack/Visual Narrative Program/Composition Intent/Feature Contract/T/V/wrong-reading-lock references.
- Evidence adapters for media probing, frame sampling, audio analysis, and eligible independent judgment.

### Out of scope and non-goals

- Changing AIR semantic meaning, source classification, lineage, Visual Asset Demand, Feature Contract, composition intent, or locks.
- Selecting VAE production models, LoRAs, conditioning, candidates, repair parameters, or production acceptance.
- Defining evaluator thresholds, benchmarks, calibration, or certification; current VAE evaluation remains `specified_not_certified`.
- Mutating legacy records, writing code, schemas, migrations, releases, or Development Capsules during this writing task.

## 3. Architecture traceability, product ownership, and governing decisions

### Authority boundary

AIR and Content Harness remain authoritative for semantic intent and lineage. Builder owns the immutable `AtomicHarnessDefinition`; Pipeline consumes its evaluation requirements. VAE owns visual realization, production evaluation, targeted repair, acceptance, and asset delivery. Delegation transports immutable requests/results and enforces compatibility; it is not a creative evaluator. Studio may project a diagnosis and request a governed repair but may not replace evidence. `Activative Contract Compiler != Activative Intelligence Runtime` and neither is this evaluator.

### Reparse stages

1. **Preflight:** resolve exact demand/result/semantic/profile hashes, category/profile/source kind, artifact digest, and evaluator eligibility. Reject stale, unknown, missing, or ambiguous inputs before side effects.
2. **Deterministic acquisition:** probe media, sample frames, inspect static geometry and hierarchy, derive reading order, and measure temporal timing using pinned tool/program versions and bounded parameters.
3. **Independent comparison:** compare observed syntax with typed intended contract and applicable Feature Contract/T/V/lock requirements. Judgment evaluators remain distinct from producers and renderers.
4. **Diagnosis synthesis:** emit typed discrepancies and responsible-layer candidates with evidence links, confidence classification, and permitted repair scope. Never invent a cause when evidence is insufficient; emit `UNRESOLVED_ESCALATE`.
5. **Handoff:** publish an immutable diagnosis receipt to the repair controller and downstream owner. A pass does not mean production acceptance, consumption authorization, certification, or build readiness.

### Brownfield disposition

`render_qa.py` is `ADAPT` for closed immutable receipts and typed identifiers; its random/time identity and open dictionaries are rejected. `render_qa_service.py` is `ADAPT` as an orchestration seam only. FFprobe, frame-sampling, and audio services are `ACTIVATE` behind ports with exact tool/program/config hashes. Legacy records are `ARCHIVE` or losslessly migrated with source hashes and unmapped-field receipts; they never gain current authority by parsing alone.

## 4. Staged implementation plan, paths, and migration dispositions

### Stage 1 — Domain and canonical identities

Create `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/reparse/domain/models.py`, `errors.py`, `identity.py`, and `state_machine.py`. Use closed enums for `SyntaxDimension`, `ResponsibleLayer`, `DiscrepancyKind`, `Applicability`, and `DiagnosisOutcome`; canonical JSON uses sorted keys, explicit units, and no clock/random/environment values.

### Stage 2 — Reparse and comparison application

Create `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/reparse.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/comparison.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/diagnosis.py`, and `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/preflight.py`. Require hash-pinned intended contract references and exact artifact bytes. Produce observed geometry/hierarchy/order/timing, discrepancy records, and typed blocks for missing or stale lineage.

### Stage 3 — Ports and evidence adapters

Create `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/reparser.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/diagnoser.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/media_probe.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/frame_sampler.py`, and `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/audio_analyzer.py`; adapt legacy implementations under `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/adapters/`. Adapters provide evidence only and cannot define threshold, semantic ownership, or certification.

### Stage 4 — Persistence and lifecycle

Create `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/infrastructure/reparse_repository.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/infrastructure/outbox.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/replay.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/invalidation.py`, and `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/cancellation.py`. Persist command, plan, evidence, diagnosis, and downstream receipt atomically. Invalidation follows the exact dependency closure; late results are quarantined.

### Stage 5 — Delivery and tests

Create `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/api/reparse_contracts.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/api/handlers.py`, and tests under `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/reparse/`. No implementation is authorized by this candidate document; later lifecycle stages require independent audit and ratification/adoption.

## 5. Schemas, APIs, state transitions, commands, events, and receipts

### Core typed objects

`ReparseRequest` contains `request_id`, `execution_binding_id/hash`, `artifact_id/hash`, `intended_contract_id/hash`, `profile_id/version/hash`, `purpose`, `category/profile`, source-kind and provenance references, semantic lineage references, and expected aggregate revision. All IDs and hashes are non-empty canonical strings; source kind is closed and unknown values reject.

`ObservedVisualSyntax` contains artifact hash, media metadata, static `bbox[]` with explicit coordinate units, `hierarchy[]` with parent IDs, `reading_order[]`, `timing[]` with explicit time units, frame-sampling evidence, tool/program identity, and canonical evidence hash. Traversal order is sorted by stable IDs, never filesystem order.

`DiscrepancyRecord` contains dimension, expected reference, observed reference, typed delta, severity, applicability, evidence IDs, and responsible-layer candidates. `DiagnosisReceipt` contains request/run/plan IDs, complete input hashes, discrepancy IDs, selected layer or `UNRESOLVED_ESCALATE`, rationale evidence, permitted repair units, evaluator identity, state revision, receipt hash, and immutable supersession/invalidation links.

### Responsible layers

Allowed values are `KNOWLEDGE`, `RETRIEVAL`, `CONTEXT`, `PROGRAMMED_MODEL`, `TOOL`, `RUNTIME`, `VAE`, `EVALUATOR`, and `UNRESOLVED_ESCALATE`. Assignment requires evidence sufficient under the profile. A producer, VAE workflow, or renderer cannot select `EVALUATOR` for its own output; evaluator identity must be independent and attributable.

### Commands and events

Commands: `RequestReparse`, `CancelReparse`, `InvalidateReparse`, `ReplayDiagnosis`, `AcknowledgeDiagnosis`. Events: `ReparseRequested`, `PreflightBlocked`, `EvidenceCaptured`, `SyntaxObserved`, `DiscrepancyRecorded`, `DiagnosisIssued`, `ReparseCancelled`, `ReparseInvalidated`, `LateEvidenceQuarantined`, and `DiagnosisSuperseded`. Commands are idempotent by canonical request identity; conflicting reuse of a key fails without partial state.

### State machine

`REQUESTED -> PREFLIGHTED -> ACQUIRING_EVIDENCE -> COMPARED -> DIAGNOSED -> HANDED_OFF` or typed terminal `BLOCKED`, `CANCELLED`, `INVALIDATED`, `QUARANTINED`. Terminal states cannot be mutated. `NOT_APPLICABLE` is valid only with profile rule ID/hash, evaluated facts, and rationale; evaluator unavailability or missing evidence is never N/A.

### Compatibility and immutability

Schema identity/version, profile hash, intended contract hash, artifact hash, and evaluator/tool/program pins are required. New versions emit new immutable artifacts. Adapters preserve all mandatory lineage and lock fields or block migration; they do not flatten them into notes.

## 6. Backward compatibility, fallback, rollback, invalidation, and historical replay

- Legacy QA bytes remain immutable. Migration emits a new `DiagnosisReceipt` with `legacy_source_hash`, adapter identity/version/hash, mapped and unmapped fields, and eligibility state.
- Random/time IDs, generic thresholds, open blockers, or missing evaluator/profile evidence become `HISTORICAL_UNVERIFIED_EVIDENCE`, never current PASS.
- A changed artifact, intended contract, Visual Semantic Pack, Narrative Program, Feature Contract, T/V route, source/provenance ref, lock set, profile, tool, or evaluator invalidates the minimum dependency closure and final diagnosis.
- A derivative may inherit all wrong-reading locks and add stricter locks; it may not weaken or remove a parent lock without a new authorized upstream demand version.
- Failed transactions roll back command, evidence, diagnosis, and outbox writes together. Historical receipts remain queryable and reproducible after cancellation, replacement, revocation, or invalidation.
- Replay recomputes canonical identities and verifies each stored hash. Any mismatch produces a typed replay error; it never silently repairs history.
- Late results after cancellation or invalidation remain quarantined evidence and cannot reopen or alter a terminal run.

## 7. Implementation tasks and path ownership

| Task | Exact path | Owner | FR/Story | Claim ceiling |
|---|---|---|---|---|
| Closed models and identity | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/reparse/domain/` | Pipeline | FR-093/094, ST-09.02 | candidate draft only |
| Deterministic reparse | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/reparse.py` | Pipeline | FR-093 | no production claim |
| Comparison and diagnosis | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/comparison.py`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/diagnosis.py` | Independent Evaluation | FR-093/094 | no evaluator certification |
| Evidence ports/adapters | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/adapters/` | Pipeline | FR-093/094 | no threshold ownership |
| Persistence, replay, invalidation | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/infrastructure/`, `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/` | Pipeline | ST-09.02 | no lifecycle authorization |
| API and downstream receipt | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/api/` | Pipeline | ST-09.02 | no VAE acceptance |
| Tests and fixtures | `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/reparse/` | Independent test owner | FR-093/094 | independent audit required |

The target path is `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-EVAL-002.md`; no other product path is modified by this writer.

## 8. Behavior-specific acceptance criteria

1. **FR-093 primary journey:** Given valid current authority, an eligible binding, exact artifact bytes, and a hash-pinned intended contract, when reparse runs, then BBOX, hierarchy, reading-order, and timing observations are emitted with deterministic evidence and compared to the intended contract. Failure example: missing timing evidence yields `BLOCKED_MISSING_REQUIRED_EVIDENCE`, not PASS. Evidence: `reparse_receipt` and tool evidence hashes.
2. **FR-094 diagnosis:** Given a typed discrepancy and independent evaluator evidence, diagnosis identifies one governed responsible layer or `UNRESOLVED_ESCALATE`; it distinguishes knowledge, retrieval, context, Programmed Model, tool, runtime, VAE, and evaluator causes. Failure example: ambiguous evidence cannot be collapsed into a generic quality score. Evidence: `DiagnosisReceipt` with rationale and layer evidence.
3. **ST-09.02 invalid input:** Given stale, superseded, unknown, ambiguous, or unverifiable inputs, the command creates no downstream side effect and returns owner, failure code, expected/observed hashes, and next action. Failure example: stale VAD hash blocks before adapter dispatch.
4. **Producer/evaluator separation:** A producer, renderer, VAE workflow, or selecting actor bound as evaluator is rejected with `EVAL_EVALUATOR_NOT_INDEPENDENT`; aliases do not bypass actor/implementation comparison.
5. **Semantic sovereignty:** Missing source kind, interview provenance, Visual Semantic Pack, Narrative Program, Feature Contract, T/V route, Composition Intent, or wrong-reading-lock evidence blocks rather than being reconstructed or flattened.
6. **Selective recovery:** Changing one evidence dependency invalidates only its dimension and descendants; unrelated accepted evidence and historical receipts remain unchanged. A lock relaxation requires a new authorized upstream demand version.
7. **Replay and cancellation:** Duplicate identical requests return the same run; conflicting replay fails. Cancellation is idempotent, and late evidence is quarantined.
8. **N/A governance:** N/A requires profile rule/hash and evaluated facts. Required checks, unsupported evaluators, and missing evidence cannot be marked N/A.
9. **Certification truth:** Structural tests may use `TEST_FIXTURE_NOT_CERTIFIED` profiles. VAE `specified_not_certified` remains contract-compatible but production-ineligible; no capability or PASS receipt becomes certification.
10. **Evidence closure:** Every terminal result references one command, complete artifact/evidence receipts, profile and semantic hashes, state revision, and downstream handoff. Missing receipt is a typed trust failure.

## 9. Dependencies, source authority, providers, and external products

The sole Wave 13 write dependency is `TS-EVAL-001` at SHA-256 `0c3a47dc3cfb331630df794bec4869c71d5fc70894b6f0fd77b08068ff74024f`, state `WRITTEN_PENDING_AUDIT`, labeled `DRAFT_DEPENDENCY_NOT_ACCEPTED`. Its profile and synthesis interfaces are draft context, not ratified law. Any audited hash change reopens sections 3, 5, 6, 8, and 10.

VAE profile registries, AIR semantic objects, Builder definitions, Delegation envelopes, and Studio correction commands remain externally owned. Provider/model/program identity is pinned in evidence; providers cannot alter thresholds, applicability, ownership, certification, or lineage. Deferred calibration or external paper sources are not reconstructed and cannot block this draft unless promoted as required unique evidence by authority.

## 10. Testing, observability, security, performance, recovery, evidence, and release

Required future evidence includes unit/property tests for canonical identity and deterministic ordering; integration tests for static/temporal reparse, full lineage, interview/non-interview provenance, independent evaluator separation, hard-gate handling, N/A rules, selective invalidation, cancellation, replay, and legacy migration; architecture tests for inward ports and no VAE/AIR compiler/provider imports; and security tests for unsafe paths, archive traversal, malformed media, oversized payloads, secrets, and redaction.

Performance tests must bound frame sampling, media probing, queue concurrency, retries, and evidence size without changing logical identity. Observability records request/run/plan/task IDs, profile and semantic hashes, dimension, stage, layer outcome, failure code, retry, and evidence hashes while excluding private reaction/expression content, credentials, raw provider payloads, and machine-local paths.

The later Build Receipt must prove exact source/test manifests, FR/Story coverage, fresh-process deterministic reproduction, profile/certification truth, producer/evaluator independence, atomicity, optimistic concurrency, cancellation, replay, invalidation, rollback, historical reproduction, and security. It must explicitly claim zero production authorization, VAE acceptance, consumption authorization, evaluator certification, and Development Capsule unless separately ratified and adopted.

This writer stops at `WRITTEN_PENDING_AUDIT`. Independent Audit → Revision → Re-Audit → Acceptance remains required, and the candidate authority remains `CANDIDATE_NOT_CURRENT`.
