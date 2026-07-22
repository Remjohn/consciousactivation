# TS-EVAL-001 - Deterministic and Independent Evaluation Profiles

```yaml
spec_id: TS-EVAL-001
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product: Atomic Harness Pipeline
primary_owner: Independent Evaluation
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: INDEPENDENT_AUDIT_REQUIRED
writing_wave: 12
controlling_story: ST-09.01
controlling_frs: [FR-091, FR-092]
```

This candidate specification is authorized for specification work only. It does not make V2.1 candidate authority current, certify an evaluator, authorize implementation or production, grant VAE Stage 5, issue a Development Capsule, or permit `ACCEPTED_FOR_BUILD` before attributable authority ratification.

## 1. Files and authorities read

The writer consumed two exact Wave 12 upstream drafts under the mandatory label `DRAFT_DEPENDENCY_NOT_ACCEPTED`:

| Upstream draft | State | SHA-256 | Interface used and downstream revision impact |
|---|---|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-002.md` | `WRITTEN_PENDING_AUDIT` | `3e76ee7e4ec8f3b288a58bb8b8eb886195d9ad17097c67ded613c22fbb3dccd4` | Supplies the draft `AtomicHarnessDefinition` intake, `HarnessExecutionBindingManifest`, typed evaluation-requirement projection, category/profile binding, ownership, lineage, and hard-gate interface. If its audited bytes change, revisit sections 3, 5, 6, 8, 9, and 10. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-017.md` | `WRITTEN_PENDING_AUDIT` | `0e87466a326eac865a66609d2609a1fc8006f5b32a5a847bd01e36e488363a81` | Supplies draft AIR-to-Pipeline visual handoff, Visual Asset Demand, visual result, Visual Semantic Pack, Visual Narrative Program, Composition Intent, Feature Contract, T/V route, wrong-reading-lock, and reparse evidence interfaces. If its audited bytes change, revisit sections 3, 5, 6, 8, 9, and 10. |

Neither upstream draft is accepted authority. They are hash-pinned WRITE interfaces admitted by the Prompt 02C recovery authorization. Current Constitution V1.1 and current product PRDs remain controlling where candidate drafts conflict.

| Source | State and SHA-256 | Classification | Specific fact used |
|---|---|---|---|
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | required method | One writer writes one spec and may not self-audit, revise, accept, build, or issue a capsule. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | recovery packet; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | required packet | Fixes packet identity, FR-091/FR-092, ST-09.01, exact path, Wave 12, dependency labels, and claim ceiling. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_12_DISPATCH_LOCK.yaml` | Wave 12 lock; `96f655bbf67a40a38a5cf233cfa9ad3f954466a8dae80ff68dfa87a2a5c9e5a7` | required dispatch lock | Pins the exact upstream draft paths, states, and hashes used here. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | current V1.1; `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | highest current authority | Evaluation must preserve Activative meaning, human reaction, semantic lineage, visual narrative, wrong-reading locks, and product sovereignty. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending ratification; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | candidate ownership | AIR owns semantic lifecycle/production-program meaning; Pipeline executes and coordinates; VAE realizes visual demands; Delegation transports; Studio projects/corrects. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending ratification; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | candidate object ownership | Pipeline may reference and orchestrate evaluation of externally owned semantic objects but may not redefine them. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | frozen Prompt 02; `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | required queue | TS-EVAL-001 is the queued canonical evaluation-profile specification. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` | frozen Prompt 02; `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | required traceability | FR-091 and FR-092 have one primary Story/spec/owner chain and a bounded claim ceiling. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | frozen Prompt 02; `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | required traceability | ST-09.01 requires separate mechanical and judgment evaluation, hard-gate precedence, evidence, replay, and selective recovery. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | current source disposition; `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | required source policy | The current VAE feature sources and five predecessor implementation sources are required and available. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | Prompt 02C; `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | required dependency policy | Both upstream edges are WRITE-interface dependencies, not build-acceptance gates. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification-only authorization; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | write authorization | Candidate-authority specification work may proceed; build, production, and certification remain false. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/spec_assignments/TS-EVAL-001.md` | assignment brief; `5ce2bbd694e2c204359370bfcc95bb45a99511896141493f9f522cfde2cd269e` | required assignment | Defines deterministic validation, independent judgment, evidence, replay, hard-gate, and source-review duties. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/prd/features/F16-independent-evaluation-visual-syntax-reparse-diagnosis-and-selective-repair.md` | candidate requirement; `0a247a2025ef803df09e8bfc97b9456d73a64cf2f867598135b3c8ba03a668e2` | required candidate authority | FR-091 lists deterministic domains; FR-092 lists independent semantic/judgment dimensions and forbids hidden invalidity. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | candidate Story inventory; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | required Story | ST-09.01 separates producer and evaluator, prevents averaged-score bypass, and requires selective recovery and replay. |
| `02_VISUAL_ASSET_EDITOR/prd/05-features/F14-visual-evaluation-profiles.md` | current VAE requirement; `03bd9c1c918a4602e396095a5dd60e2b5221af0eca03bd213a588839f4db6dd8` | `SRC-CUR-018`; required authority | VAE production evaluation profiles are typed by family/subtype/route/context, deterministic checks run first, and hard gates outrank aggregates. |
| `02_VISUAL_ASSET_EDITOR/prd/05-features/F15-repair-invalidation-reruns.md` | current VAE requirement; `79b40d744ea93a35716224a4df6849ed33f58ecb2c63e86cc329b05def05effc` | `SRC-CUR-019`; required authority | VAE owns targeted production repair, preserves accepted properties, uses causal evidence, and may not lower a threshold merely to pass. |
| `02_VISUAL_ASSET_EDITOR/governance/VISUAL_EVALUATION_PROFILE_REGISTRY.yaml` | `specified_not_certified`; `7d3d8c75fbd02dc93567cd7261f28bd79af82ca8e9ecad0856a29fee72f46131` | current readiness evidence | Evaluation thresholds, calibration sets, model/program pins, arbitration, and rollback evidence remain pending; capability presence is not certification. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/render_qa.py` | predecessor code; `b3e4aa987d23113438ac1ee023c0f447738dbc4909bd37416834c9485d8380f0` | `SRC-LEG-019`; required unique evidence | Existing QA objects expose useful categories but use mutable/open structures, time/random identity, generic thresholds, and incomplete composite hard-gate logic. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/render_qa_service.py` | predecessor code; `01ec1c91c05672610794efb97d188dbcef5cf6ef5e5f22c1565f36f19e390dd8` | `SRC-LEG-020`; required unique evidence | Current orchestration wraps supplied measurements and maps blockers but does not prove independent evaluation identity or semantic-profile authority. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/ffprobe_validation_service.py` | predecessor code; `9e345420ef3b55e0676b10e1cf994a7dc8602cc6cac6d8f6f0fd2cdadeaf3f61` | `SRC-LEG-021`; required unique evidence | FFprobe evidence is a reusable deterministic adapter boundary, not an evaluation authority. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/frame_sampling_service.py` | predecessor code; `41b55520aa1bb1e6cea76002fa7e6acb73047ce239f682108f7fa69b1e4ef98c` | `SRC-LEG-022`; required unique evidence | Frame sampling is reusable evidence acquisition but must be deterministic and profile-pinned. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/audio_level_analysis_service.py` | predecessor code; `e39a1a88d9c631714c6dedcdfd47abda1db98e2e55f20de6dd5876f2d20484c4` | `SRC-LEG-023`; required unique evidence | Audio measurement is reusable evidence acquisition but cannot define thresholds or certification. |

The exact output is authorized as `DIRECT_PRODUCT_SPEC_PATH`. No target or ancestor `AGENTS.md` exists. The assignment's older `04_ATOMIC_HARNESS_PIPELINE` target is superseded by the canonical Prompt 02 path under `05_ATOMIC_HARNESS_PIPELINE`.

## 2. Problem, user outcome, solution, and scope

### Problem

Pipeline needs to decide whether a produced artifact satisfies mechanical constraints and governed semantic intent without becoming the authority that invents either. Existing predecessor QA code can wrap measurements and emit blockers, but it permits generic defaults, random/time-derived identity, open strings, unpinned evaluator context, a boolean operator downgrade, and a composite result that can omit judgment status. A plausible aggregate can therefore hide a failed applicable hard gate, a producer can appear to validate its own output, and replay cannot prove that the same profile, semantic inputs, tools, models, or thresholds were used.

### User and system outcome

An operator can request one evaluation against an exact execution binding, artifact, AIR/VAD/Feature Contract context, and versioned evaluation profile. Pipeline deterministically plans and coordinates the run. Mechanical validators and independent judgment evaluators emit separate, typed, immutable receipts. Every applicable hard gate is visible; one failed hard gate makes the run ineligible regardless of averages. `NOT_APPLICABLE` is governed and evidenced. Repeating the same request yields the same logical identities and result, while every external observation is content-addressed. The result is auditable without being confused with VAE production acceptance, downstream consumption, evaluator certification, or product authorization.

### Bounded solution

Define:

1. a profile-reference and requirement-projection boundary that consumes externally owned evaluation meaning without copying editable semantics;
2. a Pipeline-owned evaluation plan, run state machine, dispatch protocol, evidence ledger, and orchestration receipt;
3. independent-evaluator-owned deterministic and judgment receipts with attributable implementation identity;
4. fail-closed applicability, hard-gate, independence, eligibility, replay, invalidation, and cancellation rules;
5. exact future module paths, API surfaces, persistence contracts, migrations, tests, and completion evidence.

### In scope

- FR-091 deterministic validation of contract, schema, geometry, text fit, timing, source lineage, tool use, export, and execution-envelope facts.
- FR-092 independent evaluation of source/semantic fidelity, psychological role, Edge Product, Activative function, Primitive coalition and misuse, archetype, Voice/Visual DNA, category grammar, Negative Space, Edge Integrity, composition, temporal effect, Feature Contracts, T/V routing, and wrong-reading risk when applicable.
- ST-09.01 separation of producer and evaluator, hard-gate precedence, replay, CBAR hardening, evidence retention, and selective recovery.
- Category/profile-specific evaluation requirement projection from TS-AHP-002.
- Exact AIR visual semantics, VAD/result, Composition Intent, Feature Contract, lock, and reparse references from TS-AIR-017.
- Structural support for deterministic validators, independent VLM evaluators, other eligible judgment evaluators, and human arbitration as declared by governed profiles.

### Out of scope and non-goals

- Defining or changing AIR semantic meaning, Primitive/archetype doctrine, approved Final Script, Visual Semantic Pack, Visual Narrative Program, Composition Intent, Feature Contract intent, T/V somatic meaning, or wrong-reading locks.
- Creating or certifying VAE evaluation thresholds, benchmarks, evaluator models, programs, calibration sets, or production-readiness evidence.
- Selecting VAE production workflows, models, LoRAs, conditioning, candidates, repair implementation, or production acceptance.
- Root-cause diagnosis and repair-plan semantics owned by TS-EVAL-002 and TS-EVAL-003, except emitting typed failure evidence needed by them.
- Treating a capability declaration, passing synthetic fixture, average score, or Pipeline orchestration receipt as evaluator certification.
- Implementing source code, schemas, tests, migrations, contract bytes, production services, or Development Capsules during this writing task.

## 3. Governing decisions and constraints

### 3.1 Authority and product sovereignty

- Constitution V1.1 remains current. V2.1 ownership artifacts, TS-AHP-002, and TS-AIR-017 are `CANDIDATE_NOT_CURRENT`.
- Independent Evaluation owns the semantic definition of evaluation dimensions, applicability, hard-gate classification, evidence sufficiency, evaluator eligibility, calibration, benchmark, and certification requirements. Pipeline must not reinterpret those rules.
- Pipeline owns evaluation orchestration: resolving exact pinned inputs, constructing a run plan, scheduling eligible evaluators, collecting evidence, enforcing ordering and hard-gate outcomes, persisting immutable receipts, replaying, and projecting status.
- AIR owns the meaning and authoritative bytes of Activative Intelligence, source/semantic lineage, psychological role, Matrix of Edging, Edge Product, Primitive/archetype and misuse constraints, approved Final Script, Activation Contract, Visual Semantic Pack, Visual Narrative Program, T/V routes, Composition Intent, Feature Contracts, and wrong-reading locks.
- Builder owns `AtomicHarnessDefinition`. Pipeline consumes its immutable evaluation requirements through TS-AHP-002 and may not change their source values.
- Content Harness/AIR-controlled targets own `VisualAssetDemand` semantic intent and amendment authority. VAE owns Visual Production Plan, visual realization, production evaluation, repair, production acceptance, asset lineage, and delivery.
- Delegation transports immutable messages and enforces shared contract compatibility; it does not decide whether a creative artifact is semantically successful.
- Studio projects state and submits governed commands/corrections; it does not silently replace evaluator evidence.
- A producer, renderer, generator, VAE workflow, or Pipeline executor must not approve its own output. An independent evaluator implementation must have a different actor/implementation identity and satisfy the profile's independence policy.
- `Activative Contract Compiler != Activative Intelligence Runtime`, and neither equals Independent Evaluation or Pipeline orchestration.

### 3.2 Evaluation profile authority and certification

An `EvaluationProfileRef` is an exact external reference, not a Pipeline-owned policy blob. It identifies owner, profile ID, semantic version, content hash, category/profile applicability, dimension set, hard-gate rules, evidence requirements, eligibility rules, and certification state. Pipeline may cache immutable bytes but must validate the owner and hash.

The current VAE Visual Evaluation Profile Registry is `specified_not_certified`. Its pending threshold references must not be replaced with guessed numbers. For a production-eligible run, each required profile component must be governed, hash-pinned, supported, and certified to the level required by the binding. Structural and synthetic tests may use explicitly non-production fixture profiles with `certification_state: TEST_FIXTURE_NOT_CERTIFIED`; their receipts must remain ineligible for production and certification claims.

Capability presence and contract compatibility are distinct from certification:

```text
capability_declared
  != capability_contract_compatible
  != evaluator_implemented
  != evaluator_calibrated
  != limited_production_certified
  != production_certified
```

### 3.3 Deterministic facts and independent judgment remain separate

Deterministic validators establish reproducible facts from exact bytes and tool evidence. Independent evaluators render governed judgments from exact semantic and artifact context. They produce separate receipts and failure types. A judgment may not override a failed deterministic hard gate. A deterministic pass may not substitute for missing semantic judgment. The final orchestration decision is a conjunction over all required applicable hard gates, not an average.

Optional diagnostic evaluations may run after a hard-gate failure only when the profile explicitly allows them, they are labeled `DIAGNOSTIC_ONLY_AFTER_INELIGIBILITY`, and they cannot restore eligibility.

### 3.4 No semantic reconstruction or flattening

Pipeline passes typed, hash-pinned references. It must not flatten required lineage into notes, reconstruct missing Reaction Receipt/Expression Moment/source provenance, infer a source kind, synthesize a missing Feature Contract, restate Composition Intent as a free-form prompt, weaken a wrong-reading lock, or map an unknown dimension to a generic quality score. Missing required semantic material yields a typed preflight failure before evaluator dispatch.

### 3.5 Hard-gate and `NOT_APPLICABLE` law

- Every requirement has `applicability: REQUIRED | OPTIONAL_IF_PROFILE_RULE | NOT_APPLICABLE_BY_RULE`.
- `NOT_APPLICABLE_BY_RULE` requires a profile-owned rule ID, rule version/hash, evaluated input facts, deterministic rationale, and decision receipt.
- A required hard gate cannot be marked `NOT_APPLICABLE`.
- An unavailable evaluator, missing evidence, unknown dimension, unsupported profile, pending threshold, or execution error is not `NOT_APPLICABLE`; it is a blocker/error.
- A non-interview source may make interview-only provenance checks inapplicable if and only if the governed profile rule establishes that fact. Supplied interview provenance remains validated.
- Applicability decisions are immutable inputs to synthesis. Later changes create a new evaluation run version.

### 3.6 Identity, determinism, and portability

Logical IDs are derived from canonical bytes, never random UUIDs, current time, filesystem order, environment variables, absolute paths, locale, or dictionary insertion order. Operational timestamps may be appended as non-identity metadata by an injected clock and excluded from hashes. Canonical serialization uses UTF-8, normalized line endings, sorted object keys, order-preserving arrays where order is semantic, explicit decimals/units, and no `NaN`/infinity.

Provider/model nondeterminism is contained by recording request bytes, response bytes, model/program/provider identity, parameters, seed when supported, evidence set, and attempt. A replay in verification mode proves historical results from stored evidence; it does not falsely promise that a remote model will emit identical bytes on a fresh call.

### 3.7 Acceptance boundaries

- An independent evaluation receipt is evidence for a decision; it is not a VAE production-acceptance receipt.
- VAE production acceptance is not downstream consumption authorization.
- Pipeline consumption acknowledgement does not duplicate visual evaluation and cannot consume stale, superseded, invalidated, or revoked demand/result versions.
- `PASS` means all required applicable gates passed under the exact profile. It does not mean evaluator certified, artifact production-approved, product implementation authorized, or release trusted.

## 4. Current brownfield architecture

### 4.1 Reusable evidence adapters

The predecessor Studio code contains useful bounded seams:

- `ffprobe_validation_service.py` can execute a deterministic media-inspection tool and capture structured facts;
- `frame_sampling_service.py` can select frames for evidence acquisition;
- `audio_level_analysis_service.py` can produce audio measurements;
- `render_qa_service.py` demonstrates orchestration of measurement inputs into a composite report;
- `render_qa.py` names deterministic categories such as codec, duration, dimensions, frame rate, safe zones, text fit, audio, frame integrity, visual semantics, motion/camera, content, and feature-contract checks.

These are migration evidence, not current authority. Adapters may be wrapped behind new ports only after their inputs, outputs, tool identity, failure modes, timeouts, portability, and evidence hashes meet this spec.

### 4.2 Correctness and trust gaps

1. Model defaults derive identifiers from random UUIDs and times from the process clock, so equivalent inputs cannot prove stable identity.
2. Mutable/open mappings and `Any` values admit untyped dimensions and machine-specific data.
3. Generic hard-coded thresholds are not pinned to a governed evaluation profile.
4. Free-form references, statuses, and blocker codes do not prove owner, version, or compatibility.
5. A boolean operator-downgrade flag can weaken a blocking motion defect without an attributable amendment or authority reference.
6. Supplied measurements are wrapped without always proving the tool invocation, raw bytes, parameters, or chain of custody.
7. Producer/evaluator implementation identity is not structurally separated.
8. Evaluator model/program, prompt, calibration set, benchmark, and certification state are not pinned.
9. `RenderQACompositeReport` aggregation omits `rendered_asset_evaluation`; a failing judgment receipt can be absent from the composite gate.
10. There is no exact AIR/VAD/Feature Contract/lock semantic context digest, profile applicability proof, atomic commit protocol, optimistic concurrency rule, or historical replay contract.

### 4.3 Migration posture

No predecessor object is accepted as the new canonical contract. Existing facts may be adapted losslessly into typed evidence records. Unknown legacy fields are retained in a content-addressed `LegacyEvidenceEnvelope` for audit but do not become active requirements. A legacy report lacking exact profile, semantic context, evaluator independence, and all required gates is `HISTORICAL_UNVERIFIED_EVIDENCE`; it cannot be promoted to current PASS through default insertion.

## 5. Proposed architecture and workflows

### 5.1 Components and ownership

```text
HarnessExecutionBindingManifest (Builder meaning, Pipeline binding)
        + VisualActivationHandoff / VAD / VisualResult (AIR/content/VAE authority)
        + EvaluationProfileRef (Independent Evaluation or VAE profile authority)
                              |
                              v
EvaluationRequestIntake -> EvaluationPreflight -> EvaluationRunPlanner
      (Pipeline)             (Pipeline)             (Pipeline)
                              |
               +--------------+--------------+
               |                             |
               v                             v
DeterministicValidatorPorts       IndependentJudgmentEvaluatorPorts
(eligible tool adapters)          (eligible independent evaluator actors)
               |                             |
               +--------------+--------------+
                              v
                   Evidence/Receipt Collector
                            (Pipeline)
                              |
                              v
                    HardGateSynthesisEngine
           (mechanical enforcement of profile-owned rules)
                              |
                              v
                  EvaluationOrchestrationReceipt
                            (Pipeline)
```

The synthesis engine does not invent weights or decide what should matter. It applies the exact profile-owned applicability and gate algebra to immutable evaluator receipts.

### 5.2 Primary workflow

1. **Admit request.** Validate request schema, canonical bytes, idempotency key, caller authority, target artifact hash, binding ID/hash, semantic handoff ID/hash, VAD/result versions, profile reference, and requested purpose.
2. **Load exact upstream state.** Resolve immutable `HarnessExecutionBindingManifest`, `VisualActivationHandoff`, `VisualAssetDemand`, `VisualResult`, source/provenance references, Feature Contracts, Composition Intent, T/V routes, wrong-reading locks, category/profile, and invalidation/supersession state.
3. **Project requirements.** Read `EvaluationRequirementProjection` entries from the binding. Verify each `source_pointer` and `source_value_hash` against the imported Harness; do not accept caller overrides.
4. **Resolve profile.** Load exact owner/version/hash. Verify category, format/profile, asset family/subtype, route, source kind, feature set, result version, and purpose compatibility. Reject uncertified components when production eligibility requires certification.
5. **Determine applicability.** For every profile dimension, emit an `ApplicabilityDecision`. Fail if required dimensions are missing, duplicated, unknown, owner-mismatched, or marked N/A without a governed rule.
6. **Freeze plan.** Canonically order stages and dependencies, select eligible validators/evaluators, bind all tool/model/program/calibration identities, compute `evaluation_input_digest` and `evaluation_plan_id`, and atomically persist the plan plus command record before dispatch.
7. **Run deterministic gates first.** Dispatch only pinned deterministic validator adapters. Capture raw and normalized evidence. Any required hard-gate failure makes the run ineligible. The profile decides whether diagnostic judgment stages may continue.
8. **Run independent judgment.** For each applicable dimension, dispatch an eligible evaluator that is independent of producer and production-plan actors. Supply exact artifact evidence and semantic context refs. Require a typed receipt with conclusion, confidence/evidence sufficiency if governed, citations to exact inputs, and failure taxonomy.
9. **Synthesize mechanically.** Validate receipt signatures/hashes, independence, evidence completeness, profile version, and applicability. Compute the conjunction of applicable hard gates. Aggregates may inform diagnostics only; they cannot hide a hard failure or missing receipt.
10. **Commit atomically.** Persist evidence, individual receipts, synthesis, orchestration receipt, event sequence, and immutable state transition in one transaction. Only then publish the terminal event/outbox message.
11. **Project outcome.** Expose `PASS`, `FAIL`, `BLOCKED`, `CANCELLED`, `INVALIDATED`, or `ERROR` with typed reasons. Keep production acceptance, consumption acknowledgement, certification, and build authority separate.

### 5.3 Idempotency and optimistic concurrency

- `evaluation_request_id = sha256(canonical EvaluationRequestCore)`.
- Same request ID and same canonical bytes returns the same run/receipt or current nonterminal state without re-dispatch.
- Same request ID with different bytes returns `EVAL_IDEMPOTENCY_KEY_REUSED`.
- Every state mutation supplies expected `run_revision`; mismatch returns `EVAL_CONCURRENCY_CONFLICT` without partial writes.
- Dispatch uses deterministic `evaluation_task_id = sha256(plan_id + stage_id + evaluator_binding_hash + attempt_ordinal)`.
- Duplicate/late evaluator receipts are accepted only if byte-identical to the stored receipt for that task. Conflicting bytes are quarantined and never synthesized.
- Event/outbox publication is transactionally coupled to state via an outbox record. Delivery may repeat; consumer idempotency is mandatory.

### 5.4 Deterministic validation workflow

Deterministic checks include only profile-declared applicable domains. Typical domains are:

- contract/schema/version/hash and immutable reference validity;
- source-kind and source-lineage/provenance requirements;
- required Reaction Receipt/Expression Moment references for `interview_expression`;
- geometry, aspect ratio, dimensions, safe zones, crop bounds, text fit and legibility facts;
- duration, frame rate, timebase, timing windows, sequence order, audio presence/levels and export facts;
- artifact readability, codec/container, frame integrity and package/member hashes;
- allowed tool/model/worker identity, capability and execution-envelope compliance;
- VAD/result version alignment, Feature Contract reference integrity, derivative parent-lock evidence, and lock inheritance equality/strengthening;
- absence of absolute paths or ungoverned environment data in portable artifacts.

Each validator receipt records facts and comparison results. It does not turn mechanical evidence into semantic approval.

### 5.5 Independent judgment workflow

Judgment dimensions are explicitly profile-owned and may include:

- source fidelity and semantic fidelity;
- psychological-role and role-tension preservation;
- Edge Product and Activative function;
- Primitive coalition, coalition signature, Primitive misuse risk, archetype, Voice DNA and Visual DNA fidelity;
- category grammar, sequence role, asset role, Negative Space, Edge Integrity, composition and temporal effect;
- Visual Semantic Pack, Visual Narrative Program, T/V somatic route, Composition Intent, Feature Contract realization and wrong-reading-lock conformance.

The evaluator receives typed refs and content-addressed evidence, not a free-form summary. Every receipt cites the exact fields/evidence used. A dimension owner may require multiple independent evaluators or human arbitration; Pipeline applies that declared topology. An evaluator cannot alter the source object, threshold, applicability rule, or gate type.

### 5.6 Failure and selective recovery workflow

Failure receipts identify failed requirement/dimension IDs and evidence. They do not prescribe creative repairs beyond governed structured observations. TS-EVAL-002 may attribute failure; TS-EVAL-003 may compile/selectively schedule repair. A new attempt reuses unchanged accepted evidence only when the profile declares it reusable and its full dependency closure is byte-identical. Changed artifact bytes, semantic context, VAD/result version, profile, threshold, evaluator binding, or applicable dimension set invalidates affected evidence and every dependent synthesis while preserving historical records.

### 5.7 Cancellation and late evidence

Cancellation moves a run to `CANCELLING`, stops undispatched work, requests cooperative cancellation, and closes as `CANCELLED`. Already observed external work remains receipted. Late results are stored as historical orphan evidence with task linkage but cannot reopen or pass the cancelled run. A new authorized request creates a new run identity when the canonical input set differs.

## 6. Data models, contracts, schemas, and APIs

All models are immutable, closed, versioned, and canonically serializable. Unknown fields/enum values fail at the boundary unless a negotiated forward-compatible envelope explicitly preserves them without activating behavior.

### 6.1 Core references

```text
EvaluationRequirementProjection
  requirement_id: EvaluationRequirementId
  source_pointer: JsonPointer
  source_value_hash: Sha256
  requirement_owner: ProductAuthorityRef
  evaluator_owner: ProductAuthorityRef
  applicability_mode: REQUIRED | OPTIONAL_IF_PROFILE_RULE
  hard_gate: bool
  required_evidence_kinds: ordered[EvidenceKind]

EvaluationProfileRef
  profile_id: EvaluationProfileId
  profile_version: SemVer
  profile_hash: Sha256
  profile_owner: ProductAuthorityRef
  compatibility_profile_id: CompatibilityProfileId
  certification_state: SPECIFIED_NOT_CERTIFIED | TEST_FIXTURE_NOT_CERTIFIED |
                       BENCHMARKED | LIMITED_PRODUCTION_CERTIFIED |
                       PRODUCTION_CERTIFIED
  certification_evidence_refs: ordered[ArtifactRef]

SemanticEvaluationContextRef
  activative_handoff_ref: ArtifactRef
  visual_asset_demand_ref: ArtifactRef
  visual_result_ref: ArtifactRef
  source_package_ref: ArtifactRef | null
  visual_semantic_pack_ref: ArtifactRef | null
  visual_narrative_program_ref: ArtifactRef | null
  composition_intent_ref: ArtifactRef | null
  feature_contract_refs: ordered[ArtifactRef]
  tv_route_refs: ordered[ArtifactRef]
  wrong_reading_lock_set_ref: ArtifactRef | null
  lineage_digest: Sha256
```

Null is allowed only where the profile proves a field not required. Required content must never be moved into generic notes.

### 6.2 Request, input bundle, and plan

```text
EvaluationRequestCore
  contract_version: SemVer
  harness_execution_binding_ref: ArtifactRef
  target_artifact_ref: ArtifactRef
  semantic_context_ref: ArtifactRef
  evaluation_profile_ref: EvaluationProfileRef
  evaluation_purpose: STRUCTURAL_TEST | PRE_PRODUCTION_EVIDENCE |
                      PRODUCTION_ELIGIBILITY | POST_COMPLETION_REVALIDATION
  requested_by: ActorAuthorityRef
  request_authority_ref: ArtifactRef
  idempotency_key: NonEmptyString

EvaluationInputBundle
  request_id: EvaluationRequestId
  binding_hash: Sha256
  target_artifact_hash: Sha256
  semantic_context_hash: Sha256
  profile_hash: Sha256
  requirement_projection_hash: Sha256
  category_id: CategoryId
  format_profile_id: FormatProfileId
  source_kind: SourceKind
  execution_evidence_refs: ordered[ArtifactRef]
  invalidation_snapshot_hash: Sha256

EvaluationRunPlan
  plan_id: EvaluationPlanId
  plan_schema_version: SemVer
  input_bundle_hash: Sha256
  applicability_decisions: ordered[ApplicabilityDecision]
  stages: ordered[EvaluationStagePlan]
  evaluator_bindings: ordered[EvaluatorBinding]
  hard_gate_rule_set_ref: ArtifactRef
  evidence_retention_policy_ref: ArtifactRef
  production_eligibility_requested: bool
  production_eligibility_possible: bool
  ineligibility_reasons: ordered[FailureCode]
```

`production_eligibility_possible` is false when any required certification/threshold/profile evidence is pending. The run may still produce non-production structural evidence if the purpose permits it.

### 6.3 Applicability and evaluator binding

```text
ApplicabilityDecision
  dimension_id: EvaluationDimensionId
  decision: APPLICABLE_REQUIRED | APPLICABLE_OPTIONAL | NOT_APPLICABLE_BY_RULE
  profile_rule_id: RuleId
  profile_rule_version: SemVer
  profile_rule_hash: Sha256
  evaluated_fact_refs: ordered[EvidenceRef]
  rationale_code: ApplicabilityRationaleCode
  decision_hash: Sha256

EvaluatorBinding
  evaluator_binding_id: Sha256
  dimension_ids: ordered[EvaluationDimensionId]
  evaluator_owner: ProductAuthorityRef
  evaluator_actor_ref: ActorRef
  implementation_id: ImplementationId
  implementation_version: SemVer
  implementation_hash: Sha256
  capability_contract_ref: ArtifactRef
  evaluation_program_ref: ArtifactRef
  model_provider_ref: ArtifactRef | null
  model_id: NonEmptyString | null
  model_version: NonEmptyString | null
  parameter_hash: Sha256
  calibration_evidence_ref: ArtifactRef | null
  certification_state: EvaluatorCertificationState
  independence_proof: EvaluatorIndependenceProof
```

`EvaluatorIndependenceProof` identifies all producer, workflow, repair, and approval actors and proves the evaluator actor/implementation is eligible under the profile. A simple inequality of display names is insufficient.

### 6.4 Evidence and receipts

```text
EvidenceRecord
  evidence_id: Sha256
  evidence_kind: EvidenceKind
  subject_ref: ArtifactRef
  acquisition_adapter_id: ImplementationId
  adapter_version: SemVer
  adapter_hash: Sha256
  tool_or_model_ref: ArtifactRef | null
  invocation_request_hash: Sha256
  raw_result_hash: Sha256
  normalized_result_hash: Sha256
  ordered_dependency_refs: ordered[ArtifactRef]
  portability_class: PORTABLE_CONTENT_ADDRESSED | EXTERNAL_RETRIEVABLE
  observed_at: Timestamp | null  # metadata, excluded from logical identity

DeterministicValidationReceipt
  receipt_id: Sha256
  evaluation_task_id: Sha256
  dimension_id: EvaluationDimensionId
  validator_binding_ref: ArtifactRef
  profile_rule_ref: ArtifactRef
  evidence_refs: ordered[EvidenceRef]
  facts: ordered[TypedFact]
  outcome: PASS | FAIL | BLOCKED | ERROR
  hard_gate: bool
  failure_codes: ordered[FailureCode]
  receipt_hash: Sha256

JudgmentDimensionReceipt
  receipt_id: Sha256
  evaluation_task_id: Sha256
  dimension_id: EvaluationDimensionId
  evaluator_binding_ref: ArtifactRef
  semantic_context_hash: Sha256
  artifact_evidence_refs: ordered[EvidenceRef]
  cited_source_pointers: ordered[JsonPointer]
  conclusion: PASS | FAIL | BLOCKED | ERROR
  governed_measurements: ordered[TypedMeasurement]
  evidence_sufficiency: SUFFICIENT | INSUFFICIENT | NOT_DEFINED_BY_PROFILE
  failure_codes: ordered[FailureCode]
  receipt_hash: Sha256

IndependentEvaluationReceipt
  receipt_id: Sha256
  evaluator_binding_ref: ArtifactRef
  dimension_receipt_refs: ordered[ArtifactRef]
  independence_proof_hash: Sha256
  evaluator_certification_state: EvaluatorCertificationState
  outcome: PASS | FAIL | BLOCKED | ERROR
  receipt_hash: Sha256

EvaluationOrchestrationReceipt
  receipt_id: Sha256
  request_id: EvaluationRequestId
  run_id: EvaluationRunId
  plan_ref: ArtifactRef
  deterministic_receipt_refs: ordered[ArtifactRef]
  independent_receipt_refs: ordered[ArtifactRef]
  applicability_decision_refs: ordered[ArtifactRef]
  all_required_applicable_receipts_present: bool
  all_required_applicable_hard_gates_passed: bool
  outcome: PASS | FAIL | BLOCKED | CANCELLED | INVALIDATED | ERROR
  production_eligibility: bool
  production_ineligibility_reasons: ordered[FailureCode]
  certification_claim: NONE
  production_acceptance_claim: NONE
  consumption_authorization_claim: NONE
  receipt_hash: Sha256
```

Every list with semantic meaning has a declared order; sets are canonicalized by stable IDs before hashing. No receipt permits arbitrary `metadata` to affect behavior.

### 6.5 State machine and persistence

```text
PLANNED -> PREFLIGHT_VALIDATED -> DETERMINISTIC_RUNNING
DETERMINISTIC_RUNNING -> JUDGMENT_RUNNING | SYNTHESIS_READY | BLOCKED | FAILED | ERROR
JUDGMENT_RUNNING -> SYNTHESIS_READY | BLOCKED | FAILED | ERROR
SYNTHESIS_READY -> PASSED | FAILED | BLOCKED | ERROR
nonterminal -> CANCELLING -> CANCELLED
terminal/nonterminal -> INVALIDATED (authorized upstream invalidation)
```

`FAILED` is a valid evaluated outcome. `ERROR` is an execution/infrastructure failure. `BLOCKED` means required evidence/profile/evaluator/authority is unavailable or unresolved. A terminal state is immutable; retry or changed input creates a new run/attempt linked by `predecessor_run_ref`.

Required repositories:

```text
EvaluationPlanRepository
EvaluationRunRepository
EvaluationEvidenceRepository
EvaluationReceiptRepository
EvaluationCommandRepository
EvaluationEventOutboxRepository
EvaluationIdempotencyRepository
```

`commit_transition(expected_revision, command_record, state, artifacts, receipts, events, outbox)` is atomic. State without its command/receipt, or receipt without referenced evidence/artifact, is invalid and rejected during repository integrity validation.

### 6.6 Ports and application APIs

```text
EvaluationProfileResolver.resolve(profile_ref, context) -> ResolvedEvaluationProfile
EvaluationPreflightService.validate(request) -> EvaluationInputBundle
EvaluationRunPlanner.compile(input_bundle) -> EvaluationRunPlan
DeterministicValidatorPort.evaluate(task, evidence_context) -> DeterministicValidationReceipt
IndependentEvaluatorPort.evaluate(task, semantic_context) -> IndependentEvaluationReceipt
EvaluationReceiptVerifier.verify(receipt, plan) -> VerifiedReceipt
HardGateSynthesisService.synthesize(plan, verified_receipts) -> EvaluationOrchestrationReceipt
EvaluationApplicationService.submit(request) -> EvaluationRunView
EvaluationApplicationService.cancel(command) -> EvaluationRunView
EvaluationApplicationService.get(run_id) -> EvaluationRunView
EvaluationReplayService.verify(run_id) -> EvaluationReplayReceipt
EvaluationInvalidationService.apply(event) -> EvaluationInvalidationReceipt
```

Ports return typed results/errors; they do not raise generic exceptions across application boundaries. Provider credentials, absolute paths, and environment state never enter portable domain objects.

### 6.7 Failure codes

At minimum:

```text
EVAL_REQUEST_SCHEMA_INVALID
EVAL_AUTHORITY_DENIED
EVAL_INPUT_HASH_MISMATCH
EVAL_INPUT_STALE_OR_INVALIDATED
EVAL_BINDING_REQUIREMENT_MISMATCH
EVAL_SEMANTIC_CONTEXT_INCOMPLETE
EVAL_SOURCE_PROVENANCE_INCOMPLETE
EVAL_PROFILE_UNKNOWN
EVAL_PROFILE_HASH_MISMATCH
EVAL_PROFILE_INCOMPATIBLE
EVAL_PROFILE_NOT_CERTIFIED_FOR_PURPOSE
EVAL_THRESHOLD_AUTHORITY_PENDING
EVAL_DIMENSION_UNKNOWN
EVAL_REQUIRED_DIMENSION_MISSING
EVAL_NOT_APPLICABLE_UNGOVERNED
EVAL_REQUIRED_GATE_MARKED_NOT_APPLICABLE
EVAL_EVALUATOR_UNAVAILABLE
EVAL_EVALUATOR_NOT_INDEPENDENT
EVAL_EVALUATOR_NOT_ELIGIBLE
EVAL_EVIDENCE_INSUFFICIENT
EVAL_EVIDENCE_HASH_MISMATCH
EVAL_RECEIPT_PROFILE_MISMATCH
EVAL_RECEIPT_CONFLICT
EVAL_HARD_GATE_FAILED
EVAL_REQUIRED_RECEIPT_MISSING
EVAL_AGGREGATE_BYPASS_ATTEMPT
EVAL_IDEMPOTENCY_KEY_REUSED
EVAL_CONCURRENCY_CONFLICT
EVAL_CANCELLED
EVAL_LATE_RESULT_QUARANTINED
EVAL_REPLAY_MISMATCH
EVAL_INVALIDATED
EVAL_PERSISTENCE_ATOMICITY_FAILURE
```

## 7. Implementation stages and exact target paths

These are future implementation targets only. Creating this spec does not authorize them.

### Stage 1 - Closed domain contracts and canonicalization

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/domain/models.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/domain/enums.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/domain/identifiers.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/domain/errors.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/domain/canonicalization.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/domain/state_machine.py`

Completion: frozen/closed models, canonical hashes, explicit units/order, typed errors, no clock/random/environment identity, and round-trip property tests.

### Stage 2 - Profile and semantic-input boundaries

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/profile_resolver.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/preflight.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/requirement_projection.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/profile_registry.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/semantic_artifact_store.py`

Completion: exact owner/version/hash resolution; category/profile/source-kind compatibility; full lineage/Feature Contract/lock validation; governed N/A; uncertified production runs blocked; no threshold invention.

### Stage 3 - Planner, independence, and dispatch

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/planner.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/evaluator_eligibility.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/dispatch.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/deterministic_validator.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/ports/independent_evaluator.py`

Completion: stable plans/tasks, producer/evaluator separation, deterministic-stage precedence, bounded diagnostic continuation, and no dispatch before atomic command/plan persistence.

### Stage 4 - Evidence adapters

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/adapters/media_probe.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/adapters/frame_sampler.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/adapters/audio_analyzer.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/adapters/vlm_evaluator.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/adapters/legacy_render_qa.py`

Completion: tool/model/program/version/parameters pinned; raw/normalized evidence hashed; unsafe paths rejected; predecessor reports admitted only as historical evidence unless fully mapped; no adapter defines thresholds.

### Stage 5 - Synthesis, persistence, replay, and invalidation

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/synthesis.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/service.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/replay.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/application/invalidation.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/infrastructure/repositories.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/infrastructure/sqlite_repositories.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/infrastructure/outbox.py`

Completion: hard-gate conjunction includes every required applicable receipt; atomic commit; optimistic concurrency; idempotent replay; cancellation/late-result quarantine; selective invalidation with historical reproduction.

### Stage 6 - Delivery boundary and documentation

Create:

- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/api/contracts.py`
- `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/evaluation/api/handlers.py`
- `05_ATOMIC_HARNESS_PIPELINE/docs/evaluation/EVALUATION_PROFILE_INTEGRATION.md`
- `05_ATOMIC_HARNESS_PIPELINE/docs/evaluation/EVALUATION_AUTHORITY_BOUNDARY.md`
- `05_ATOMIC_HARNESS_PIPELINE/docs/evaluation/LEGACY_QA_MIGRATION.md`

Completion: authenticated commands/queries; no secret or absolute-path leakage; typed projection separates evidence PASS from production/certification/consumption claims.

### Stage 7 - Tests and governed evidence

Create:

- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/unit/test_canonical_identity.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/unit/test_applicability.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/unit/test_hard_gate_synthesis.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/unit/test_evaluator_independence.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/integration/test_deterministic_then_judgment.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/integration/test_atomic_commit_and_replay.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/integration/test_invalidation_and_cancellation.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/integration/test_air_vad_feature_contract_context.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/integration/test_legacy_qa_migration.py`
- `05_ATOMIC_HARNESS_PIPELINE/tests/evaluation/architecture/test_evaluation_boundaries.py`

Completion requires the evidence in section 10 and an independently issued lifecycle decision. No stage is authorized by this document.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Fail-closed matrix

| Condition | Required behavior | No permitted fallback |
|---|---|---|
| Input/binding/profile hash mismatch | reject before dispatch; record expected/observed refs | guessed latest or silent rehash |
| Stale/superseded/invalidated VAD, result, semantic context, or binding | block and link invalidation evidence | evaluate as current |
| Missing source provenance or interview Reaction Receipt/Expression Moment | block required provenance gate | infer from notes/text |
| Unknown profile/dimension/category/profile/source kind | block incompatibility | map to generic score |
| Pending threshold/certification for production purpose | `BLOCKED`, production eligibility false | invented threshold or capability-as-certification |
| Ungoverned `NOT_APPLICABLE` | reject plan | omit dimension |
| Producer and evaluator not independent | reject evaluator binding | self-approval |
| Deterministic hard gate fails | outcome ineligible; optional diagnostics only if governed | average/override/downgrade |
| Required independent receipt missing | `BLOCKED` | treat absent as pass |
| Receipt conflicts with task/profile/context | quarantine and `ERROR`/`BLOCKED` | accept newest |
| Persistence transaction fails | rollback all new run state/receipts/outbox | partial commit |
| Late result after cancellation/invalidation | preserve as orphan historical evidence | reopen terminal run |

### 8.2 Legacy migration

Migration reads predecessor QA records, canonicalizes stable facts where exact units and source evidence exist, and emits new immutable artifacts. It never mutates legacy bytes. Every migrated record contains `legacy_source_hash`, adapter ID/version/hash, mapped fields, unmapped fields, omissions, and eligibility result.

Records using random IDs/current-time defaults get new content-derived IDs while preserving original identifiers as non-authoritative aliases. Generic thresholds, boolean operator downgrades, and free-form blockers are retained as historical facts only. Missing profile/semantic/evaluator evidence results in `HISTORICAL_UNVERIFIED_EVIDENCE`, not synthetic current fields. Migration never guesses source kind, profile, evaluator, threshold, Feature Contract, lock, or applicability.

### 8.3 Rollback and recovery

- Deployment rollback changes runtime implementation routing, not immutable run/receipt bytes.
- The last compatible reader remains available for historical versions; unsupported active versions block new work without corrupting history.
- A failed transaction leaves no visible state change. Recovery reconciles transaction journal and outbox, verifies every artifact/receipt reference, and quarantines impossible partial histories.
- A failed evaluator attempt can be retried only through the plan's bounded attempt policy. Attempts remain separately receipted.
- Selective recovery reuses only evidence whose full dependency closure is unchanged and whose profile explicitly permits reuse. Otherwise the affected dimension and dependent synthesis rerun.
- Historical runs remain reproducible from stored request, plan, semantic refs, artifact/evidence bytes, evaluator outputs, profile, and code/tool/model/program identities.

### 8.4 Invalidation and supersession

An upstream invalidation maps changed object IDs/hashes to affected evidence and receipts. It invalidates the minimum dependency closure plus the final synthesis. Derivative visual results inherit parent wrong-reading locks and must carry parent-lock evidence; removing/weakening a lock requires a new authorized upstream VAD version. A replacement result or demand does not rewrite the old evaluation. Active delegations/runs remain pinned to accepted versions unless a governed revocation/invalidation explicitly blocks consumption.

### 8.5 Observability

Structured events include request/run/plan/task IDs, revision, profile ID/version/hash, purpose, category/profile, dimension ID, stage, evaluator binding ID, outcome, failure code, retry attempt, duration, and artifact/evidence hashes. Logs must exclude source content, private Reaction/Expression content, credentials, raw prompts/responses unless stored in controlled evidence, and machine-local paths.

Metrics include preflight denials by code, stage latency, evaluator availability, deterministic/judgment failure counts, missing-receipt incidents, hard-gate bypass attempts, independence denials, N/A decisions by governed rule, retry/late-result counts, invalidation fan-out, replay mismatches, and atomicity recovery events. Metrics never create a new approval score.

Every terminal orchestration receipt can be traced to one command record and complete artifacts; every artifact/receipt has a run and plan; every event has a committed state revision. Integrity scans surface gaps as P0 trust failures.

## 9. Behavior-specific acceptance criteria

### 9.1 Deterministic profile application - FR-091

Given an exact binding, artifact, semantic context, and governed profile, two fresh processes compile byte-identical logical input bundle and plan bytes despite different dictionary insertion order, filesystem traversal order, locale, clock, random state, and environment. The same deterministic tool evidence yields byte-identical receipts. Operational timestamps do not change logical IDs.

### 9.2 Complete deterministic domain coverage - FR-091

For a fixture profile requiring contract, geometry, text fit, timing, source lineage, tool use, export, execution-envelope, VAD/result, Feature Contract, and lock-inheritance checks, the plan contains each requirement exactly once and every terminal outcome includes a receipt or typed blocker for each. Unknown or omitted required checks fail before PASS.

### 9.3 Interview provenance

For `interview_expression`, absence of at least one non-empty Reaction Receipt reference or at least one non-empty Expression Moment reference blocks evaluation before semantic judgment. For non-interview source kinds those refs are optional unless required by the profile, but if supplied they are validated. Unknown or ambiguous source kind is rejected, never guessed.

### 9.4 Independent judgment coverage - FR-092

The independent-evaluation fixture exercises all profile-applicable dimensions: source/semantic fidelity, psychological role, Edge Product, Activative function, Primitive coalition/misuse, archetype, Voice/Visual DNA, category grammar, Negative Space, Edge Integrity, composition, temporal effect, Feature Contracts, T/V route, and wrong-reading risk. Receipts cite exact semantic context and evidence; no required lineage is flattened into notes.

### 9.5 Producer/evaluator separation - ST-09.01

Binding an evaluator actor or implementation that produced, selected, repaired, or approved the candidate is rejected with `EVAL_EVALUATOR_NOT_INDEPENDENT`. Display-name changes or provider aliases do not bypass actor/implementation lineage comparison. A governed human-arbitration role remains distinct and attributable.

### 9.6 Hard-gate precedence - FR-091, FR-092, ST-09.01

A fixture with nine high scores and one failed applicable hard gate ends `FAIL`, production eligibility false. A missing required judgment receipt ends `BLOCKED`. A deterministic failure cannot be overridden by an aggregate, operator boolean, VLM judgment, or threshold change. The current predecessor bug in which rendered-asset judgment is omitted from composite aggregation has a regression test.

### 9.7 Governed `NOT_APPLICABLE`

Every N/A includes a pinned rule and evaluated facts. Attempts to mark a required gate N/A, use evaluator unavailability as N/A, or omit a dimension without a rule fail. Adding a new category/profile/source kind without an applicable rule fails closed.

### 9.8 Evaluation authority and certification truth

Pipeline resolves profile owner/version/hash and applies its rules without changing them. A current VAE profile with `specified_not_certified` may support structural contract tests but cannot yield production eligibility or evaluator certification. Capability declaration does not elevate certification. No numeric threshold appears unless sourced from exact governed profile bytes.

### 9.9 AIR/VAD/Feature Contract sovereignty

Changing any AIR handoff, VAD, Visual Result, Visual Semantic Pack, Visual Narrative Program, Composition Intent, Feature Contract, T/V route, source-lineage, or wrong-reading-lock hash changes input/run identity or invalidates the affected run. Pipeline never writes back an altered semantic object. Missing meaning is blocked, not reconstructed.

### 9.10 VAE and lifecycle boundaries

An evaluation PASS does not create a VAE production-acceptance receipt, consumption acknowledgement, evaluator certification, Stage 5 authorization, or product/build authority. A stale/superseded result cannot be consumed. Historical result/evidence remains reproducible after invalidation, revocation, replacement, or cancellation.

### 9.11 Idempotency, concurrency, atomicity, and replay

Duplicate identical submit returns the same run. Reused key with different bytes fails. Conflicting expected revisions produce no partial state. Injected failures at each repository/outbox boundary prove atomic rollback. Historical verification recomputes all canonical identities and gate synthesis from stored bytes; mismatch is typed and never repaired silently.

### 9.12 Cancellation and late results

Cancellation stops undispatched tasks, receipts already incurred work, and closes once. Late or conflicting results are quarantined and cannot alter the terminal outcome. Repeated cancel is idempotent.

### 9.13 Portability and source safety

Absolute Windows/POSIX paths, credentials, environment-specific values, unstable traversal ordering, unsafe archive members, symlink escapes, and unbounded payloads are rejected or isolated outside portable objects. Fresh-context reproduction on a different workspace root yields identical logical identities.

### 9.14 Brownfield migration

Every predecessor object either maps losslessly with exact evidence or becomes `HISTORICAL_UNVERIFIED_EVIDENCE`. Random/time identities, generic thresholds, open blockers, and operator downgrade booleans do not gain current authority. Migration creates new immutable artifacts and preserves original bytes/hashes.

### 9.15 Selective recovery

Changing only one evidence dependency invalidates its dimension receipt and all dependent synthesis, not unrelated evidence. Changing profile applicability, artifact bytes, semantic context, lock set, or evaluator binding invalidates the exact dependency closure. Reuse decisions are receipted and profile-authorized.

## 10. Testing and completion evidence

### 10.1 Unit and property tests

- Canonical serialization and IDs are stable across processes, orderings, roots, clocks, random seeds, locales, and environments.
- Closed enums/objects reject unknown values, `NaN`, infinity, ambiguous units, duplicate IDs, mutable defaults, and behavior-bearing free-form metadata.
- Profile resolution validates owner/version/hash/certification/category/profile/route/source-kind compatibility.
- Applicability tests cover every allowed mode and adversarial N/A attempts.
- Hard-gate synthesis is a conjunction over all required applicable gates and includes deterministic plus judgment receipts.
- Independence proofs reject shared producer/evaluator actor, implementation, workflow, or ungoverned alias.
- Receipt verification detects altered evidence, profile, semantic context, evaluator, outcome, order, or signature/hash.
- State-machine/property tests reject illegal transitions and terminal mutation.

### 10.2 Integration tests

- End-to-end deterministic-first then independent-judgment evaluation with exact AHP-002 and AIR-017-compatible fixtures.
- Interview and non-interview provenance cases.
- Full AIR/VAD/Feature Contract/T/V/Composition Intent/wrong-reading-lock context propagation.
- Uncertified VAE profile remains contract-compatible but production-ineligible.
- Unsupported profile/dimension/evaluation requirement fails before side effects.
- Media probe, frame sample, audio, and VLM adapters capture exact evidence/tool/model/program pins.
- Missing judgment receipt and predecessor omitted-judgment aggregation regression fail.
- Atomic commit fault injection, duplicate delivery, conflicting late result, cancellation, retry, outbox replay, and optimistic concurrency.
- Selective invalidation and historical reproduction after semantic/profile/artifact changes.
- Legacy QA migration preserves aliases/raw evidence and refuses synthetic PASS.

### 10.3 Architecture and authority tests

- Evaluation domain/application code cannot import VAE implementations, Studio UI/application services, AIR compiler internals, Builder compiler internals, provider SDKs, clocks, random generators, or filesystem/network adapters.
- Adapters depend inward through ports; independent evaluator contracts are separate from producer/renderer ports.
- No Pipeline model owns editable AIR/VAD/Feature Contract/profile semantic values.
- No code path emits VAE production acceptance, downstream consumption authorization, evaluator certification, build authority, or Development Capsule.
- Exact-source tests protect small boundary symbols/contracts; broader behavior uses contract/property tests so harmless formatting does not create repetitive maintenance stops.

### 10.4 Security and operational tests

- Archive/path traversal, symlink, absolute-path, oversized evidence, malformed media, injection, untrusted content, credential leakage, timeout, provider failure, and resource exhaustion tests.
- Authorization tests for submit/cancel/invalidate/replay/evidence access.
- Redaction tests for private source/reaction/expression content and provider payloads.
- Bounded concurrency/backpressure and deterministic retry tests.

### 10.5 Required completion artifacts for a later lifecycle stage

A future implementation claim requires, at minimum:

1. source and test manifests with exact hashes;
2. FR-091/FR-092/ST-09.01 traceability;
3. two fresh-process full regression results;
4. source compilation/type/static-analysis results;
5. deterministic reproduction and portability results;
6. profile/threshold/certification truth evidence;
7. producer/evaluator independence evidence;
8. hard-gate regression and complete-receipt evidence;
9. atomicity, concurrency, idempotency, cancellation, replay, invalidation, rollback, and historical reproduction evidence;
10. security/path/archive/adversarial results;
11. explicit zero claims for production acceptance, consumption authorization, certification, and build authority unless separately authorized;
12. an independent audit by a different agent under Prompt 04.

This writing task ends at `WRITTEN_PENDING_AUDIT`. No audit, revision, re-audit, acceptance, implementation, release creation, Development Capsule, VAE adoption, Stage 5, or production authorization is performed here.
