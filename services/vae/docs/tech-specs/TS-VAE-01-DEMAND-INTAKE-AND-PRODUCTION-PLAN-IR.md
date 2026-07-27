# TS-VAE-01 Demand Intake and Visual Production Plan IR

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Features: F02, F05, F09, F20
- Owned FRs: FR-009 through FR-016; FR-033 through FR-040; FR-065 through FR-072; FR-153 through FR-160
- Owned NFRs: NFR-SEM-001 through NFR-SEM-005
- Decisions: D003, D009, D012, D024
- Journeys: UJ-01, UJ-03, UJ-04, UJ-07, UJ-12, UJ-14
- Components: `DelegationContractPort`, `DemandIntake`, `DemandRepository`, `CompositionFeasibilityService`, `ProductionPlanCompiler`, `ProductionPlanRepository`, `ConflictCoordinator`

## 2. Files and evidence read

- VAE feature shards F02, F05, F09, F20 and `governance/REQUIREMENTS_REGISTRY.yaml`
- VAE demand, plan, geometry, conflict schemas and all Format 02 examples
- VAE preservation contract, product constitution, workcell and budget registries
- Delegation Protocol constitution, authority matrix, lifecycle machine, failure taxonomy, compatibility policy, contract ownership register, and conformance cases
- Delegation schemas for demand, submission, receipt, conflict, amendment, supersession, invalidation, event, and result
- Format 02 negotiated profile and VAE compatibility manifest

## 3. Problem, solution, and scope

### Problem

The VAE must turn an immutable, externally authorized demand into an executable provider-neutral plan without assuming authority over meaning or leaking provider JSON into canonical state. It must diagnose infeasibility, preserve exact demand identity, and propose amendments without modifying the accepted demand.

### Approved solution

`DelegationContractPort` validates a Delegation-owned envelope and payload, then creates an immutable `DemandSnapshot`. Deterministic authority and compatibility validation precede bounded visual interpretation. `ProductionPlanCompiler` emits a versioned `ProductionPlan` whose bindings explicitly separate preserved demand fields from mutable production choices. Conflicts create typed Delegation conflict/amendment messages; accepted changes arrive only as a new demand version.

### In scope

- demand identity, validation, authority, admission fact, and immutable storage;
- composition feasibility and image-conditioned geometry requirements;
- canonical Visual Production Plan IR and plan versioning;
- plan-stage dependency graph, preservation/mutable bindings, capabilities, budgets, evaluation, repair hooks, and provider-binding slots;
- conflicts, internal plan amendments, upstream amendment proposals, supersession impact, and selective invalidation inputs.

### Explicitly out of scope

- changing Content Harness fields or selecting final sequence/timing;
- public schema ownership or lifecycle enforcement, which belong to Delegation;
- provider graph generation, compute execution, candidate evaluation, or asset promotion;
- manual prompt/ComfyUI editing as an accepted planning path.

## 4. Brownfield and contract alignment

The current VAE schemas and fixtures are architecture seeds. The Delegation demand schema matches the VAE demand at the top level and is authoritative. Submission uses Delegation `demand_hash`; protocol version comes from the envelope/negotiated profile. VAE-local result and conflict snapshots are not public ABI.

Retain the V2.1/frozen model of Harness-owned meaning, typed contracts, dependency resolution, event-sourced workflow, and smallest-responsible invalidation. Adapt it through ports. Remove no upstream behavior. Prohibit `authorized_for_composition` in VAE output; production acceptance and downstream acknowledgement remain separate.

## 5. Component responsibilities

| Component | Responsibility | Must not do |
|---|---|---|
| `DelegationContractPort` | Validate schema/profile/authority/integrity result supplied by protocol; map public messages to internal commands and facts. | Fork public schemas or reinterpret lifecycle. |
| `DemandIntake` | Check exact demand identity, immutable references, notes isolation, required profile and admission preconditions. | Amend demand fields. |
| `DemandRepository` | Store content-addressed immutable snapshots and supersession links. | Overwrite a version. |
| `CompositionFeasibilityService` | Check geometry, reserved regions, tolerance, control availability, and return evidence. | Decide final composition or weaken intent. |
| `ProductionPlanCompiler` | Compile one deterministic plan version from demand + registry snapshots + policy inputs. | Emit provider JSON as canonical plan. |
| `ProductionPlanRepository` | Append plan versions, hashes, amendments, bindings, and lineage. | Change a plan used by an active run. |
| `ConflictCoordinator` | Classify conflicts and create non-binding Delegation conflict/amendment facts. | Accept its own proposal. |

## 6. Canonical data models

### `DemandIdentity`

Required fields: `request_id`, integer `version`, canonical `payload_ref`, `payload_sha256`, `content_harness_principal`, `category_profile`, `format_profile`, and negotiated Delegation profile ID. Equality requires all identity fields; a string alias alone is invalid.

### `DemandSnapshot`

Contains exact normalized demand payload, identity, received envelope/audit refs, notes in a non-authoritative namespace, admission status, and immutable source/reference hashes. Normalization may reorder maps and resolve references but may not change values or semantics.

### `ProductionPlan`

Required fields:

- `plan_id`, `version`, `plan_sha256`, `created_at`, `compiler_version`;
- exact `demand_identity` and optional `supersedes_plan`;
- `objective` containing asset family/role and Activative function references;
- `preserved_bindings` as demand JSON Pointers plus expected hashes;
- `mutable_bindings` with owner, allowed range/set, and reason;
- ordered typed `stages` with node ID/type, actor authority, inputs, outputs, dependencies, checkpoint policy, retry policy, timeout, invalidation tags, and cost class;
- provider-neutral `capability_requirements` and compatibility constraints;
- `composition_constraints`, coordinate profile, tolerance, reserved regions, geometry outputs;
- `budget_authorization_ref`, portfolio policy, evaluation profile refs, repair policy;
- `fallback_routes` with typed triggers;
- unresolved `provider_bindings` slots or a pinned `CapabilityBundleRef` after resolution;
- versioned `compatibility`, security classification, retention, and trace references.

Plan JSON Schema must close all mandatory objects. Extensions use a versioned owner namespace and cannot replace mandatory fields.

### `FeasibilityAssessment`

Records deterministic constraint results, optional VLM observations, control/capability evidence, geometry simulation refs, conflict codes, confidence, and recommended non-binding options. Observation and inference are labeled separately.

## 7. State machine and flows

Internal intake states are `RECEIVED`, `CONTRACT_VALIDATED`, `AUTHORITY_VALIDATED`, `ADMITTED`, `FEASIBILITY_CHECKED`, `PLANNED`, `BLOCKED_CONFLICT`, `SUPERSEDED`, and `REJECTED`. They are private and map only to stable Delegation facts.

Transitions are append-only and compare-and-swap on `(demand_identity, state_version)`. Duplicate intake with the same idempotency scope returns the existing admission fact. Same key with a different hash is `SCHEMA_INVALID`/integrity failure and creates no state change.

Successful flow: validate envelope and demand -> persist snapshot -> run deterministic feasibility -> bounded visual analysis -> compile plan -> hash/persist -> emit `plan_ready` internal event -> runtime accepts exact plan version.

Conflict flow: freeze valid assessment -> persist evidence -> emit `constraint_conflict` and optional `amendment_proposal` through Delegation -> wait. An accepted option is never applied directly; a Content Harness demand supersession creates a new snapshot and impact analysis.

## 8. APIs, queues, events, and adapters

Internal command interface:

```text
admit(envelope_ref, payload_ref, idempotency_key) -> VaeAdmissionFact
assess_feasibility(demand_identity) -> FeasibilityAssessmentRef
compile_plan(demand_identity, registry_snapshot, budget_authorization) -> ProductionPlanRef
analyze_supersession(old_identity, new_identity) -> InvalidationInput
```

Commands are queued through `WorkflowRuntimePort` using immutable references, expected hashes, deadline, priority, and correlation/causation IDs. Events are `DemandAdmitted`, `DemandRejected`, `FeasibilityCompleted`, `PlanCompiled`, `PlanSuperseded`, `ConflictDetected`, and `AmendmentProposed`. External messages are emitted only through `DelegationContractPort`.

The admission split follows Delegation ADR-DLG-004: VAE produces a signed `VaeAdmissionFact`; the protocol owns validation/audit and public receipt composition.

## 9. Cross-cutting production contract

| Concern | Requirement in this spec |
|---|---|
| Provider adapters | Planning uses provider-neutral capability IDs; adapters cannot mutate plan/demand. |
| ComfyUI compilation | TS-VAE-03 compiles pinned stages. ComfyUI JSON is absent from canonical plan fields. |
| Docker/model/VAE/LoRA locks | Plan records capability requirements; resolved lock bundle is attached immutably before execution. |
| GPU/storage | Plan stages declare resource classes and object refs, never local paths. |
| Deterministic vs VLM | Schema, authority, identity, geometry arithmetic, hashes, locks, and conflicts are deterministic. VLM may classify visual feasibility/ambiguity with evidence but cannot alter authority. |
| Budget/candidates | Plan pins authorization and portfolio ceilings from TS-VAE-05. |
| Evaluation | Plan references certified profiles from TS-VAE-06; demand may request profile/gates, not evaluator strategy. |
| Repair/invalidation | Plan exposes preserved/mutable bindings and node invalidation tags consumed by TS-VAE-07. |
| Idempotency/checkpoints | Intake and compile are idempotent by input hashes; persisted snapshots and plan versions are checkpoints. |
| Observability/cost | Every compile emits duration, selected route, estimated cost range, input/output hashes, and conflict evidence. |
| Security/isolation | Notes and references are untrusted; prompts cannot grant authority; URIs are allowlisted and hash-verified. |
| Migration/rollback | Migrations create new snapshots/plan versions with equivalence receipts. Active runs keep original versions. Rollback selects an earlier compiler/plan schema via compatibility manifest. |

## 10. Behavioral rules

1. Demand validation fails closed on missing identity, hash, authority, required feature, category certification, or reference integrity.
2. Notes may influence a bounded interpretation only when consistent with authoritative fields; conflicts ignore notes.
3. Preserved bindings must include semantic intent, Activative function, wrong-reading locks, sequence/asset/composition role, identity requirements, and delivery hard constraints.
4. Every mutable binding names the VAE owner and allowed domain; undeclared mutation is forbidden.
5. Feasibility runs before expensive generation and returns evidence, not a silent relaxation.
6. Image-conditioned geometry uses normalized coordinates plus explicit canvas/profile version; transforms preserve source and target coordinates.
7. An internal production amendment may alter only declared VAE-owned bindings and creates a new plan version.
8. A demand-level amendment requires Content Harness authority and a new demand version.
9. A provider binding cannot be accepted unless all compatibility edges and maturity/certification gates pass.
10. Recompiling identical normalized inputs and registry snapshots must yield the same plan hash.

## 11. Failure, degradation, and recovery

- Contract/authority/integrity/compatibility failures route to Delegation and create no plan.
- Feasibility failures use `COMPOSITION_CONSTRAINT_CONFLICT`, `CONTRADICTORY_DEMAND_CONSTRAINTS`, `INSUFFICIENT_REFERENCE_EVIDENCE`, or `CAPABILITY_GAP`.
- Registry/storage outage is an infrastructure failure and may retry with identical inputs; it does not consume a quality round.
- Compiler crash resumes from the last committed snapshot. An incomplete plan is never visible.
- Optional capability degradation requires an explicit Delegation compatibility verdict and owner authorization; mandatory semantics never degrade.
- Supersession freezes the old plan, blocks stale promotion, and preserves completed outputs for impact analysis.

## 12. Observability, security, performance, and budgets

Metrics: intake latency, rejection family, feasibility latency, compile latency, deterministic plan-hash stability, conflict rate, stale-reference rejection, and estimate error. Trace spans carry correlation, demand, plan, compiler, and registry snapshot IDs without prompt/secrets.

Admission should fit Delegation SLO-01 once protocol overhead is included. Planning latency is Budget Program aware but never bypasses validation. Cost estimates include compute, evaluator, storage, and candidate ceilings. Large inputs remain content-addressed object references.

Least privilege grants intake read-only access to Delegation payloads, plan compiler read-only access to registries, and repository write access only to its own entities. Reference fetchers run sandboxed with URI schemes, size limits, MIME checks, malware scanning, and digest verification.

## 13. Compatibility and migration

Stage 3 imports the published Delegation package. Until publication, fixtures are tagged `provisional-delegation/0.1.0-draft`. The adapter must prove compatibility for demand identity, submission hash, receipt/admission split, event projection, result authority, and amendment exchange.

Plan schema patch changes cannot alter behavior; minor changes add optional fields with deterministic defaults; major changes require migration. Migration never rewrites historical plans. A release manifest declares readable and writable plan versions and compiler rollback support.

## 14. Implementation plan

1. Define closed internal schemas for `DemandIdentity`, `DemandSnapshot`, `ProductionPlan`, `FeasibilityAssessment`, and `VaeAdmissionFact`.
2. Implement Delegation adapter tests against the 25-schema package without copying schema ownership.
3. Implement immutable repositories and hash/canonicalization utilities.
4. Implement deterministic authority, reference, geometry, and compatibility validation.
5. Implement plan compilation for the Format 02 fixture using registry ports and no provider JSON.
6. Implement conflict/amendment/supersession mapping and selective-invalidation inputs.
7. Add metrics, audit references, security tests, migration fixtures, and rollback tests.

## 15. Given/When/Then acceptance criteria

1. Given a valid signed Format 02 demand, when admitted twice with the same key/hash, then one immutable snapshot and one execution admission fact exist.
2. Given the same idempotency key with a different demand hash, when admitted, then it is rejected and no plan state changes.
3. Given hostile instructions in `notes`, when planning, then authoritative fields remain unchanged and the injection is recorded as untrusted evidence.
4. Given the canonical Format 02 demand, when compiled against the same registry snapshot, then repeated runs produce the same plan hash and stage graph.
5. Given impossible BBOX, protected-hand, and text-reservation constraints, when assessed, then a typed conflict is emitted and the accepted demand is unchanged.
6. Given an accepted amendment option, when no new demand version exists, then planning remains blocked.
7. Given a new superseding demand, when impact is computed, then reusable outputs and invalidated nodes are evidence-backed and stale promotion is blocked.
8. Given a ComfyUI graph payload offered as a plan, when validated, then it is rejected as a provider artifact rather than canonical IR.
9. Given an old supported plan version, when read after a minor release, then it remains reproducible; when rollback occurs, the original compiler binding is selected.

## 16. Testing strategy

- Unit: canonicalization, identity equality, authority paths, geometry transforms, deterministic plan hashes.
- Contract: Delegation demand/submission/receipt/conflict/amendment/supersession fixtures and negative mutations.
- Integration: repositories, registry snapshot, plan compiler, outbox, duplicate admission, restart recovery.
- Behavioral: VLM feasibility observations versus expert labels; no authority mutation.
- Adversarial: prompt injection in notes/references, hash mismatch, oversized object, unsupported profile, stale demand.
- Compatibility: published package versions, lossless adapter, migration and rollback.
- Reference slice: compile VAD-F02-0001 into a provider-neutral plan matching required stage/capability invariants.

## 17. Constitutional alignment V1.1 addendum

This addendum strengthens FR-009 without replacing the completed intake and plan architecture. The public Visual Asset Demand remains Delegation-owned. VAE stores the validated canonical payload and creates only an internal, immutable projection of authoritative references; it does not copy the public type or reconstruct missing meaning.

### Constitution-complete intake

Before feasibility or plan compilation, DemandIntake must prove that the negotiated canonical demand carries enforceable references for:

- the Activative Intelligence Pack, Identity DNA, Context Premise, Resonance, Matrix of Edging, and source evidence;
- authoritative source-kind or applicability evidence for Reaction Receipt and Expression Moment provenance;
- the Activation Contract;
- the Visual Semantic Pack and Semiotic MCDA decision receipt;
- the Visual Narrative Program;
- applicable Feature Contracts;
- the requested T/V somatic route;
- Composition Intent;
- an evaluation policy and applicable constitutional hard gates;
- non-empty wrong-reading locks for every semantic production or transformation route.

The internal ConstitutionalDemandContext records canonical JSON Pointers or generated-binding accessors, owner/version/hash evidence, and applicability results. It contains no locally invented shared fields. Missing, open, semantically unenforceable, or lossy mandatory context yields CONSTITUTIONAL_CONTEXT_UNENFORCEABLE before admission.

If the canonical source-kind declares interview-derived material, Reaction Receipt and Expression Moment references are mandatory and non-empty. If source-kind or applicability is absent, VAE must not infer it from notes, generic semantic intent, filenames, or visual resemblance; admission blocks.

Wrong-reading locks are inline and non-empty for generation, compositing, restyling, inpainting, outpainting, and other semantic transformations. A deterministic resize or encoding-only route may use canonical inherited-lock evidence only when it identifies the accepted master and immutable lock set. If the pinned Delegation version cannot represent that evidence, the route is incompatible rather than silently defaulted.

### Composition Asset Pack and plan bindings

ProductionPlanCompiler preserves a Composition Asset Pack binding composed of authoritative references to the Activation Contract, Visual Semantic Pack, Visual Narrative Program, Feature Contracts, T/V request, Composition Intent/BBOX intent, wrong-reading locks, format constraints, and evaluation contract. Composition Intent remains upstream intent; VAE-owned exact geometry and runtime decisions remain explicit mutable production bindings. Neither the planner nor a model actor may choose a recognition carrier, viewer role, narrative beat, feature meaning, or somatic route from free-form semantic intent.

Preserved bindings must cover the full ConstitutionalDemandContext, not only semantic_intent, activative_function, and wrong_reading_locks. A plan hash includes the canonical demand hash, every preserved constitutional reference/hash, applicability evidence, and the evaluation-profile version.

### Additional acceptance criteria

1. Given a demand missing any mandatory constitutional layer, when intake validates it, then admission fails before feasibility and no default object is synthesized.
2. Given an interview-derived demand without Reaction Receipt or Expression Moment provenance, when intake validates it, then admission fails closed.
3. Given free-form intent but no selected recognition carrier or viewer role, when planning runs, then the materializer is not invoked and the demand is rejected as constitutionally unenforceable.
4. Given a semantic production route with an empty lock set, when intake validates it, then the demand is rejected.
5. Given an encoding-only derivative with canonical accepted-master lock inheritance, when planning runs, then the master, lock set, and hashes are preserved without reinterpreting the locks.
6. Given a valid constitution-complete demand, when plan compilation repeats, then the Composition Asset Pack bindings and plan hash are deterministic.

## 18. Non-goals

- Owning or editing Harness IR, category constitutions, sequence grammar, or final Remotion composition.
- Publishing shared Delegation schemas from this repository.
- Choosing a specific generation model, VLM, cloud vendor, or ComfyUI node implementation here.
- Treating plan completeness, aesthetic quality, or PRD approval as implementation authorization.
