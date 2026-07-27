# CMF Visual Asset Editor Stage 2 Specification Index

Date: 2026-07-14  
Status: draft for architecture validation  
Production implementation authorized: no

## Normative authority order

1. Locked VAE decisions D001-D028 and VAE FR/NFR registries.
2. Frozen Atomic Harness Builder preservation contract.
3. Delegation Protocol PRD, governance, lifecycle, and schema package for the shared boundary.
4. These Stage 2 specifications and their ADR resolutions.
5. Future epics, stories, implementation, and deployment manifests.

The Delegation package at `../CMF_CONTENT_HARNESS_VISUAL_ASSET_EDITOR_DELEGATION_SHARDED_PRD_V1` is a validated `0.1.0-draft` design dependency, not a published production package. Stage 3 must pin its released package identity. Until then, generated bindings and fixtures are provisional and all shared messages pass through `DelegationContractPort`.

## Product boundary

- The Content Harness owns meaning, Activative function, sequence role, composition intent, identity/continuity requirements, wrong-reading locks, demand versions, and downstream consumption acknowledgement.
- The Delegation Protocol owns public schemas, field-authority validation, compatibility negotiation, public lifecycle, message integrity, routing, idempotency/replay policy, and audit receipts.
- The Visual Asset Editor owns Visual Production Plan IR, workcell selection, capabilities, provider compilation, compute, candidates, evaluation, repair, production acceptance, assets, and production memory.
- The downstream Format 02/Remotion runtime owns final timing, deterministic text, sequence grammar, and composition consumption.

## Reference implementation shape

Stage 5 should begin as a modular VAE control plane plus replaceable adapters, not a fleet of premature services:

| Deployable/module | Responsibility | Canonical state |
|---|---|---|
| `vae-control-plane` | Intake, planning, routing, runtime coordination, budgets, lifecycle, evaluation coordination, repair, asset promotion, service API, projections | PostgreSQL-compatible transactional store through repository ports |
| `vae-gpu-worker` | Execute one compiled provider artifact inside a pinned OCI runtime and return content-addressed outputs/receipts | No independent canonical state; checkpoint/output references only |
| `vae-evaluator-adapter` | Invoke an independent VLM/evaluator and return typed evidence | No production authority beyond signed evaluation facts |
| `DelegationContractPort` | Validate and map Delegation-owned messages to immutable internal commands/facts | Delegation package and audit receipts remain externally authoritative |
| `WorkflowRuntimePort` | Register VAE node types with the frozen Builder Workflow Runtime and expose append-only events/checkpoints | Upstream runtime plus editor-local event records; no duplicate Builder runtime |
| `ObjectStorePort` | Store immutable media, masks, geometry, compiled graphs, logs, and receipts by digest | Object bytes and immutable metadata |
| `ControlTowerProjectionPort` | Publish VAE and Delegation read models into the existing Control Tower | Projection only, never authority state |

Release 1 reference persistence is PostgreSQL-compatible metadata/event storage plus S3-compatible content-addressed object storage. Queue, event bus, and workflow-engine products are bindings behind ports until the pinned Builder runtime is available. A compatibility manifest must name every selected binding and version before implementation authorization.

## Canonical data and state

| Entity | Authority | Mutability rule |
|---|---|---|
| `DemandSnapshot` | Content Harness through Delegation | Immutable; identity is request ID + version + payload hash + canonical reference. |
| `ProductionPlan` | VAE | Append-only versions; amendments never mutate the demand. |
| `Execution` and `ExecutionEvent` | VAE internal | Event-sourced; public lifecycle is a Delegation projection, not internal node state. |
| `CompiledWorkflowArtifact` | VAE compiler | Immutable derivative of plan + capability/runtime bindings; ComfyUI JSON is one payload. |
| `CandidateAsset` | VAE | Immutable by digest; eligibility and evaluation facts are append-only. |
| `QualityEvaluation` and `RepairContract` | Independent evaluator/VAE repair controller | Immutable versions linked to candidate and plan. |
| `AcceptedAssetVersion` and `DeliveryVariant` | VAE | Immutable; supersession/revocation creates new records and notices. |
| `VisualAssetMemoryRecord` | VAE | Append-only evidence and current projection; OKF/embeddings are non-authoritative projections. |
| Shared Delegation messages | Producing principal named by protocol | Immutable and validated by the Delegation package. |

## Cross-spec invariants

1. Every run pins demand hash, plan version/hash, compatibility profile, workflow, image digest, custom nodes, model, VAE, LoRA, controls, evaluator, budget program, and schema versions.
2. ComfyUI API JSON is generated from `ProductionPlan`; manual graph edits cannot become accepted run state.
3. No producer model evaluates its own output. Evaluator identity and producer identity must differ, and the evaluation invocation has independent credentials and receipts.
4. Deterministic checks execute before VLM evaluation. Failed technical integrity cannot be overruled by an average score.
5. Candidate ranking occurs only after all applicable hard gates pass.
6. Quality repair changes only permitted causal bindings, preserves declared valid properties, reruns invalidated nodes, and stops after at most three autonomous quality rounds.
7. Infrastructure retries do not consume quality rounds and cannot alter pinned creative bindings.
8. Budget pressure never weakens demand meaning, hard gates, required evaluator depth, or certified capability rules.
9. Accepted demand and accepted assets are never mutated. Supersession, replacement, invalidation, and revocation retain history.
10. Internal VAE node states never become Delegation lifecycle states. Public messages contain stable event facts only.
11. Secrets never enter plans, compiled artifacts, events, logs, receipts, prompts, or object metadata.
12. An unresolved cross-product conflict blocks the affected transition and emits a typed conflict/failure; it is never silently resolved by the VAE.

## Primary requirement ownership

Each VAE FR has exactly one primary Stage 2 owner. Other specs may consume it as a dependency.

| Specification | Primary features and FRs | Primary NFRs | Primary decisions |
|---|---|---|---|
| TS-VAE-01 | F02 FR-009..016; F05 FR-033..040; F09 FR-065..072; F20 FR-153..160 | NFR-SEM-001..005 | D003, D009, D012, D024 |
| TS-VAE-02 | F06 FR-041..048; F07 FR-049..056 | NFR-WORKFLOW-001..005 | D002, D005, D010 |
| TS-VAE-03 | F08 FR-057..064 | NFR-COMPAT-001..005 | D011, D027 |
| TS-VAE-04 | F12 FR-089..096 | NFR-COMPUTE-001..005 | D015 |
| TS-VAE-05 | F16 FR-121..128 | NFR-PERF-001..005; NFR-COST-001..005 | D019 |
| TS-VAE-06 | F14 FR-105..112 | NFR-EVAL-001..005 | D004, D017 |
| TS-VAE-07 | F15 FR-113..120 | NFR-REL-001..005 | D018 |
| TS-VAE-08 | F03 FR-017..024; F04 FR-025..032; F11 FR-081..088; F17 FR-129..136 | NFR-MEM-001..005 | D006, D007, D008, D014, D020 |
| TS-VAE-09 | F10 FR-073..080; F18 FR-137..144; F19 FR-145..152 | NFR-OBS-001..005; NFR-SEC-001..005; NFR-UX-001..005 | D013, D021, D022, D023 |
| TS-VAE-10 | F01 FR-001..008; F21 FR-161..168; F22 FR-169..176 | NFR-TRACE-001..005; NFR-GOV-001, 002, 004, 005 | D001, D025, D026, D028 |
| TS-VAE-11 | F13 FR-097..104 | NFR-GOV-003 | D016 |

## Shared interfaces

| Interface | Key methods/messages | Owner spec |
|---|---|---|
| `DelegationContractPort` | validate envelope/payload, negotiate profile, map demand, emit admission fact/event/result/conflict/budget/cancellation/failure | TS-VAE-01 and TS-VAE-09 |
| `ProductionPlanRepository` | create version, append amendment, load exact version/hash, mark superseded | TS-VAE-01 |
| `CapabilityRegistryPort` | resolve compatible capabilities, pin bundle, inspect maturity/evidence, impact analysis | TS-VAE-03 |
| `WorkflowCompilerPort` | compile plan stage to provider artifact, validate graph, emit manifest and input/output map | TS-VAE-03 |
| `WorkflowRuntimePort` | schedule node, checkpoint, resume, cancel, invalidate, replay events | TS-VAE-09 |
| `ComputeFabricPort` | quote, reserve, execute, heartbeat, cancel, recover, return receipts | TS-VAE-04 |
| `BudgetControllerPort` | authorize, reserve, debit, forecast, stop, request escalation, close receipt | TS-VAE-05 |
| `EvaluationPort` | deterministic validation, VLM evaluation, arbitration, certification lookup | TS-VAE-06 |
| `RepairControllerPort` | create repair contract, compute invalidation, apply binding delta, enforce round limit | TS-VAE-07 |
| `AssetRepository` and `MemoryPort` | promote immutable asset, derive variant, supersede, record usage, retrieve evidence, publish OKF | TS-VAE-08 |
| `CapabilityLabPort` | create plan, snapshot dataset, run benchmark, compare control, promote/deprecate/rollback | TS-VAE-11 |

## Shared contract reconciliation decisions

The Delegation-owned schemas replace VAE-local public snapshots at the adapter boundary:

- Demand top-level fields currently match; the Delegation package remains authoritative.
- Submission uses Delegation `demand_hash`; VAE-local `delegation_contract_version` is represented by the negotiated envelope/profile instead.
- VAE event identity, timestamp, and sequence remain signed envelope/audit metadata; arbitrary internal `state` is not exposed.
- The VAE result emits production acceptance only. VAE-local `authorized_for_composition` is prohibited; downstream authorization exists only in Delegation `result-acknowledgement`.
- Conflict execution references remain VAE evidence; amendments use Delegation `amendment-proposal` rather than a VAE-owned open `proposed_amendments` field.

These are adapter rules, not unilateral edits to the Delegation schemas. Stage 3 must consume the published package and execute its conformance suite.

## Stage 2 outputs

- `TS-VAE-01-DEMAND-INTAKE-AND-PRODUCTION-PLAN-IR.md`
- `TS-VAE-02-DYNAMIC-WORKCELL-AND-CAPABILITY-ROUTING.md`
- `TS-VAE-03-COMFYUI-WORKFLOW-COMPILER-AND-REGISTRIES.md`
- `TS-VAE-04-CONTAINERIZED-VISUAL-COMPUTE-FABRIC.md`
- `TS-VAE-05-BUDGET-PROGRAMS-AND-CANDIDATE-PORTFOLIOS.md`
- `TS-VAE-06-INDEPENDENT-VLM-EVALUATION.md`
- `TS-VAE-07-REPAIR-INVALIDATION-AND-BOUNDED-RERUNS.md`
- `TS-VAE-08-ASSET-LIFECYCLE-MEMORY-OKF-AND-STEERING.md`
- `TS-VAE-09-ASYNCHRONOUS-SERVICE-AND-CONTROL-TOWER.md`
- `TS-VAE-10-FORMAT02-RELEASE1-VERTICAL-SLICE.md`
- `TS-VAE-11-LORA-AND-CAPABILITY-DEVELOPMENT.md`

## Stage 2 exit rules

Stage 2 is complete when all 176 FRs, 70 NFRs, and 28 decisions have primary ownership; each specification defines state, interfaces, failure behavior, security, observability, migration/rollback, tests, Given/When/Then acceptance, implementation tasks, and non-goals; links and IDs validate; and unresolved empirical or cross-repository dependencies are explicit gates rather than hidden assumptions.

Stage 2 completion does not authorize Stage 5. Contract publication, executable conformance, compute proof, evaluator calibration, Format 02 fixtures, recovery, rollback, epics/stories, and the Development Capsule remain later hard gates.

## V1.1 constitutional alignment overlay

This overlay preserves the completed Stage 2 baseline and adds only the VAE-owned obligations introduced or clarified by the Visual Asset Editor PRD V1.1 and Activative Intelligence Constitution V1.1. For those obligations, the current constitutional and PRD authority supersedes conflicting V1 wording. Delegation remains the sole owner of the public Visual Asset Demand and shared message shapes.

| Specification | V1.1 alignment responsibility |
|---|---|
| TS-VAE-01 | Fail-closed Visual Asset Demand admission; complete Activative lineage; Reaction Receipt and Expression Moment applicability; Activation Contract; Visual Semantic Pack; Semiotic MCDA receipt; Visual Narrative Program; Feature Contracts; T/V; Composition Intent and Composition Asset Pack bindings; non-empty wrong-reading locks; no semantic inference |
| TS-VAE-02 | Route enforceability and preservation of constitutional bindings; rejection of syntactically parseable but behaviorally unenforceable routes |
| TS-VAE-03 | Deterministic materialization of every Composition Asset Pack obligation without model-default semantics |
| TS-VAE-05 | Candidate eligibility and budget non-degradation across all mandatory constitutional and evaluation gates |
| TS-VAE-06 | V1.1 Visual Evaluation Profile dimensions, wrong-reading and conditional delete-caption/no-text gates, responsible-layer evidence, and repair authority |
| TS-VAE-07 | Bounded repair at the responsible VAE-owned layer while preserving upstream contracts and rerunning invalidated constitutional gates |
| TS-VAE-08 | Immutable selected-asset lineage through Activative Intelligence Pack and applicable Reaction Receipt/Expression Moment provenance |
| TS-VAE-09 | Service and Control Tower evidence for constitutional completeness, gate outcomes, provenance, and owner/version/hash references |
| TS-VAE-10 | Format 02 acceptance and benchmark coverage for the complete constitutional path |
| TS-VAE-11 | Capability-development promotion against the same constitutional profile and authoritative lineage |
| TS-VAE-04 | No internal constitutional delta identified; existing compute-fabric invariants remain unchanged |

The shared boundary remains wire-shape agnostic until Delegation `1.1.0-rc.1` is an immutable validated release. Internal specifications use opaque authoritative references and fail closed; they do not declare new public fields, copy Delegation types, or infer missing Activative meaning.

The VAE-owned evaluation schema, profile registry, example receipt, Format 02 reference receipt, and benchmark manifest now cover zero-second hook, pattern-match strength, pattern-interrupt strength, viewer-role clarity, activation direction, prediction gap, payoff, affinity, anticipation residue, anti-cliche strength, wrong-reading risk, Feature Contract compliance, and delete-caption/no-text survival when applicable. The profile remains `specified_not_certified` until the evaluation authority supplies thresholds, evaluator pins, labeled calibration and protected sets, arbitration evidence, and rollback proof.
