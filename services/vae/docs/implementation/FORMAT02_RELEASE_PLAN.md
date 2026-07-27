# Format 02 Release 1 Plan

**Canonical profile:** `format02_minimal_coach_theatre` (historical alias: `minimal_coach_theatre`; governed by the shared Program Control alias registry)  
**Target:** Minimal Coach Theatre, `2d_character_animation`, AF-02 character/scene path  
**Reference demand:** `VAD-F02-0001` skeptical-listener reaction  
**Current readiness:** FAIL - plan approved for Stage 4 review only  
**Production implementation:** blocked

**Current profile state:** `reference_profile=true`, `structurally_supported=true`, `contract_compatible=true`, `benchmarked=false`, `limited_production_certified=false`, `production_certified=false`.

## Release Promise

Release 1 is intended to prove one autonomous, governed path from an immutable Format 02 demand to a production-accepted character asset, composition geometry, downstream Remotion validation, acknowledgement, usage evidence, and recoverable operations. The present plan does not certify that path or any production scope.

The target reaction is restrained skepticism rather than contempt, with leftward gaze/gesture, foreground-right geometry, face/hand protection, reserved text/caption regions, transparent character output, Standard budget, independent evaluation, and one demonstrated gesture repair.

```text
Delegation submission
-> immutable demand snapshot
-> composition feasibility
-> provider-neutral production plan
-> certified route/workcell/capability bundle
-> compiled provider artifact
-> Standard candidate portfolio
-> isolated local or cloud compute
-> deterministic validation
-> independent visual evaluation
-> one causal repair when needed
-> immutable accepted asset and variants
-> composition geometry receipt
-> Delegation result
-> Content Harness/Remotion acknowledgement
-> usage and Control Tower projections
```

## Authority Boundary

- Content Harness owns meaning, Activative purpose, sequence role, composition intent, demand versions, and downstream acknowledgement.
- Delegation owns public schemas, versions, compatibility, public lifecycle, authority validation, message integrity, idempotency/replay, and audit.
- VAE owns production planning, capability/compute routing, candidates, independent evaluation coordination, repair, immutable assets, geometry, and production acceptance.
- Remotion owns final deterministic text, timing, sequence grammar, composition, and asset consumption.
- Builder owns Harness IR, Workflow Runtime, JIT Skills/Capsules, repair/invalidation primitives, Development Capsule conventions, and Control Tower.

No accepted demand is mutated. ComfyUI JSON is compiled output, not canonical product state. A production model never approves its own output. VAE never grants downstream composition authorization.

## Certified Scope

In scope:

- one recurring character identity, pose, expression, gesture, gaze, simple prop/environment dependency, and transparent cutout;
- image-conditioned BBOX, gaze vector, negative space, safe-crop, protected-region, mask/depth, and collision geometry;
- reuse, deterministic transforms, generation, background removal, bounded inpaint/outpaint, simple composite, and variants when certified;
- Standard Budget Program: four initial candidates, ten maximum, two parallel jobs, three maximum autonomous quality repairs;
- one local/self-hosted and one cloud Docker GPU proof through the same port;
- independent asset, composition, syntax/recurrence, identity/continuity, and applicable technical evaluation;
- one gesture-focused repair preserving identity, expression, gaze, palette, alpha, and valid geometry;
- asynchronous service, immutable result, downstream acknowledgement, usage receipt, and Control Tower projection;
- one governed capability-development cycle after the production path is stable.

Not certified: broad documentary sourcing, advanced long-form video, full UI reproduction, advanced diagrams, complex multi-character temporal continuity, lip sync, arbitrary LoRA training, all providers, all asset families, universal editing, or final composition ownership.

## Release Bundle

An implementation-authorized `Format02ReleaseBundle` must pin immutable identities for:

1. VAE product build, internal schemas, compiler, runtime adapter, database migrations, and source revision.
2. Atomic Harness Builder profile, contracts, symbols, extension points, and source digest.
3. Delegation package coordinate, protocol/message/schema versions, generated bindings, adapter versions, profile, and conformance evidence.
4. Format/category profile, syntax doctrine, demand, scene, composition, acknowledgement, and usage fixtures.
5. Character, pose, expression, gesture, animation, scene, route, capability, budget, evaluator, and steering registry snapshots.
6. Production plan, workflow template/compiler, model, VAE, LoRA/control, runtime, and provider bindings.
7. Local/cloud OCI image digests, ComfyUI commit, custom-node lock, Python dependency lock, CUDA/driver matrix, mounted-resource hashes, and network policy.
8. Labeled evaluator/calibration/protected benchmark versions, thresholds, repair fixtures, compatibility fixtures, and rollback bundle.

No value may be `latest`, mutable, inferred at runtime, or architecture-pending.

## Release Work Packages

| Package | Entry | Deliverable and proof | Exit | Current state |
|---|---|---|---|---|
| RP-00 Close authorization blockers | Stage 4 artifacts complete | Published Delegation pin; Builder checkout/extension map; approvals; source restoration; local/cloud/evaluator/storage selections | All six Stage 4 conditions and applicable GATE-IA items PASS | BLOCKED |
| RP-01 Contract and binding proof | RP-00 | Reconciled generated Delegation bindings, 26 message paths, authority/lifecycle/compatibility tests, exact demand identity, signed package pin | Contract consumer/producer/adapter suites pass; no VAE schema fork | BLOCKED |
| RP-02 Exact-interface fixture slice | RP-01 plus Stage 5 authorization | Demand -> plan -> fixture ComfyUI -> four fixture candidates -> deterministic checks -> independent fixture evaluation -> one repair -> result/geometry | All interfaces exact; fixture-only labels present; no production claim | BLOCKED |
| RP-03 Local GPU proof | RP-02 plus local release profile | Real compiled ComfyUI artifact through rootless local worker, checkpoint/restart, immutable outputs and receipts | Reproducible local run and fault tests pass without manual graph operation | BLOCKED |
| RP-04 Cloud equivalence and recovery | RP-03 plus cloud profile | Same artifact/bindings through cloud adapter; local-to-cloud failover; quote/cost/isolation evidence | Equivalence, fencing, failover, cancellation and cost receipts pass | BLOCKED |
| RP-05 Evaluator and repair certification | RP-03/RP-04 plus approved labeled sets | Independent evaluator calibration, protected cases, hard-failure thresholds, one causal repair and preservation proof | Calibration/recall/false-rejection, repair precision and producer separation pass | BLOCKED |
| RP-06 Real Format 02 integration | RP-01..RP-05 plus producer/consumer | Real submission/events/result/acknowledgement/usage; Remotion composition validation; Control Tower evidence | All 10 Delegation scenarios and VAE end-to-end reference cases pass | BLOCKED |
| RP-07 Benchmark, rollback and limited-production review | RP-06 | Full benchmark corpus, recovery/load/security/migration/backup/restore/rollback, compatibility manifest and Development Capsule | Independent review grants `LIMITED_PRODUCTION_CERTIFIED` for declared scope | BLOCKED |

RP-02 is the first implementation slice named by Stage 5. It cannot start while RP-00/RP-01 or the readiness receipt fail.

## Runtime Strategies

### Local/self-hosted

The local adapter implements `ComputeFabricPort` against a rootless OCI/Docker GPU worker. The release profile pins image, ComfyUI, custom nodes, Python/CUDA/driver compatibility, model/VAE/LoRA/control mounts, GPU/VRAM class, CPU/RAM/scratch limits, read-only resource policy, network deny-by-default policy, health probes, and output contract. No startup package installation or mutable model download is allowed.

Jobs receive scoped input/output object access, a lease/fencing epoch, cancellation token, budget reservation, and exact compiled artifact. Checkpoints and outputs are content-addressed. Only the current lease may commit.

### Cloud

The cloud adapter implements the identical port and job/receipt contracts. Provider/region/instance identifiers remain adapter details and appear only in compute/cost receipts. Routing requires capability, quote, budget, data policy, image availability, health, checkpoint portability, and expected-value evidence. The preferred proof uses the same OCI digest and resource bundle as local; any unavoidable platform delta is declared and equivalence-tested.

### Current runtime disposition

Both strategies are specified. Neither has a selected image, ComfyUI/custom-node lock, driver matrix, provider binding, model bundle, or execution evidence. This satisfies strategy design, not executable compute readiness.

## Evaluator Test Program

Evaluation order is deterministic integrity/geometry/policy validation, then independent VLM programs, then hard-gate synthesis, then quality-first ranking. Producer and evaluator have different registered identities, credentials, invocations, prompts, and receipts.

Required tests:

1. Schema/profile tests for asset, composition, syntax/recurrence, identity/continuity, and optional temporal evaluators.
2. At least 30 expert-labeled calibration cases spanning accepted, rejected, borderline, false-positive traps, and false-negative traps.
3. Protected release cases unavailable to training/optimization prompts.
4. Semantic and Activative wrong-reading cases, including skepticism versus contempt.
5. Geometry, crop, negative-space, gaze, face/hand protection, alpha, attachment, and text-collision cases.
6. Identity drift, pose, expression, gesture, hand artifact, recurrence/fatigue, and contradictory reuse cases.
7. Producer/evaluator identity collision, missing receipt, stale profile, prompt injection, unavailable evaluator, disagreement, and arbitration cases.
8. No-average-compensation tests: any applicable hard gate blocks regardless of aggregate score.
9. Repair oracle tests labeling responsible layer and frozen properties; successful precision target is at least 90%.
10. Evaluator version rollback and old-result replay against the exact historical profile.

Thresholds for hard-failure recall and false rejection must be approved from labeled evidence. They are not invented by this plan.

## Fixture Inventory and Gaps

Available representative VAE inputs:

- six Format 02 contract fixtures: demand, plan, quality evaluation, repair, conflict, and result;
- six seed registries: character identity, pose, expression, gesture, animation primitive, and scene configuration;
- benchmark seed defining 10 case families and release hard gates;
- internal schemas for plan, evaluation, repair, geometry, budget, memory, steering, and compatibility.

Available provisional Delegation inputs:

- observed unsigned local RC4 release with exact receipt/manifest hashes, schemas, examples, generated Python/TypeScript bindings, validators, migrations, and portable derivative-lock inheritance;
- current VAE matrix PASS against all 26 exact registry paths and hashes: 20 compatible, 4 adapter, 1 migration-required, 1 incompatible;
- package validator PASS and all 42 current validator tests PASS;
- 56 declarative authority/lifecycle/compatibility/resilience cases;
- 10 Format 02 scenario definitions.

Missing executable cross-product inputs:

- coherent published signed Delegation release, corrected VAE consumer on `amendment-response`, repeated 26-message reconciliation, result migration, and executable VAE conformance;
- real Content Harness submission producer and exact Format 02 profile;
- Remotion scene/composition consumer, geometry validation, acknowledgement, and usage receipt;
- executable conformance cases rather than declarative YAML only;
- completed benchmark instances and approved labels/protected set.

## Benchmark and Release Evidence

Minimum benchmark families are 12 representative demands, 8 behavior goldens, 12 known failures, 8 adversarial demands, 12 mutations, 10 repairs, 12 recurrence contexts, 8 infrastructure recovery cases, 30 evaluator calibration cases, and 8 compatibility/rollback cases. Overlap is allowed only with explicit labels and evidence for each family.

Primary release targets:

- at least 90% autonomous completion after limited-production learning;
- at least 98% expert-labeled semantic/Activative correctness for accepted assets, with no known constitutional failure;
- at least 92% composition-context/downstream pass without asset regeneration;
- at least 99% recoverable-failure success;
- 100% accepted-asset reproducibility;
- at least 90% repair precision;
- maximum three autonomous quality repairs;
- evaluator hard-failure thresholds approved from protected evidence.

No metric can be improved by lowering hard gates, hiding exceptions, producing more candidates, or expanding uncertified scope.

## Recovery and Rollback Proof

| Failure/release action | Required assertion |
|---|---|
| Duplicate submission after timeout | Existing receipt returns; no duplicate execution |
| Boundary/control-plane restart | Idempotency and lifecycle projection rebuild from durable evidence |
| Local worker/GPU loss | Same plan/artifact/bindings resume locally or in cloud from verified checkpoint |
| Late output after lease loss/cancellation/supersession | Output is quarantined as evidence and cannot promote |
| Event bus outage/out-of-order event | Ordered at-least-once recovery does not create illegal public transition |
| Audit store unavailable | State-changing admission/acceptance fails safe |
| Cache/resource corruption | Digest check rejects resource; healthy registered source is restored |
| Missing custom node/model | Preflight rejects before GPU reservation/execution |
| Evaluator unavailable/disagrees | Acceptance blocks or registered arbitration runs; producer cannot substitute |
| Database/object-store restore | Metadata, events, object hashes, lineage, and audit chain reconcile without mutable history |
| Runtime/workflow/model/evaluator rollback | Prior certified bundle restores and historical in-flight pins remain supported |
| Contract migration rollback | Immutable old/new representations and equivalence evidence remain addressable |

Recovery/rollback is specified but not currently testable: runtime/storage products, executable fault harness, backup/restore environment, and rollback bundle do not exist.

## Security and Operations Evidence

- registered principals, signatures, hashes, expiry, authority, lifecycle, idempotency, and replay validate before work;
- prompt injection in notes/reference media cannot change demand, tools, evaluator policy, or secrets;
- untrusted media is decoded/scanned in bounded sandboxes;
- workers/evaluator use least-privilege scoped credentials and cannot list unrelated objects;
- secrets never enter plans, compiled graphs, prompts, events, logs, receipts, or metadata;
- every state-changing action has trace, audit, principal, version, hash, budget, and cost evidence;
- Control Tower is a projection through the existing owner, never a second authority store;
- SLO/load/cost evidence is dimensioned by release, profile, provider, capability, budget, and failure family.

## Promotion Decision

Promotion states are `represented`, `experimental`, `benchmarked`, `shadow`, `limited_production`, and `production_certified`. A fixture-only slice is at most `represented`. Local/cloud/evaluator proof may reach `benchmarked` or `shadow` only after all applicable evidence passes. Limited production requires real cross-product integration, rollback, incident/operations evidence, and an independent authorization receipt.

Current decision: **FAIL for implementation authorization**. RP-00 blockers prevent Stage 5 and every later work package.
