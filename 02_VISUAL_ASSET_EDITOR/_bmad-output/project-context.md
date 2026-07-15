---
project: CMF Visual Asset Editor
release_target: Format 02 Minimal Coach Theatre
stage: 4
readiness_verdict: FAIL
implementation_authorized: false
updated: 2026-07-14
---

# Project Context for Implementation Agents

## Stop Gate

Do not write production implementation until `docs/implementation/IMPLEMENTATION_READINESS.md` is PASS and explicitly grants implementation authorization. The current repository is a validated PRD/specification package, not an application scaffold. Creating boilerplate, choosing providers, or inventing upstream interfaces would bypass the binding authorization gate.

## Authority Order

1. Locked VAE decisions D001-D028 and FR/NFR registries.
2. Frozen Atomic Harness Builder architecture and its real extension points.
3. Published Delegation package for all shared schemas, public lifecycle, compatibility, authority, integrity, idempotency/replay, and audit.
4. Stage 2 VAE technical specifications.
5. Stage 3 contract dependency, compatibility matrix, and adapter test plan.
6. Stage 4 Epics, dependency graph, release plan, and readiness receipt.

Content Harness owns meaning, Activative purpose, sequence role, composition intent, demand versions, and downstream acknowledgement. VAE owns production planning and production acceptance. Delegation owns shared contracts. Remotion owns final composition/timing/text. Builder owns Harness IR, workflow/runtime primitives, JIT Skills/Capsules, repair/invalidation primitives, Development Capsule conventions, and Control Tower.

## Current Repository Reality

- No production source tree, executable product tests, Docker/OCI profile, ComfyUI graph/lock, model/VAE/LoRA lock, local/cloud GPU binding, evaluator dataset/profile, CI pipeline, or deployment assets exist.
- The package remains `0.1.0-draft`, `draft_for_review`; architecture and implementation approval receipts are absent.
- All 176 FRs, 70 NFRs, and 28 decisions have Stage 2 specification owners.
- The five local shared-boundary schemas are provisional comparison fixtures. Never compile them as public protocol bindings.
- The Delegation sibling contains a coherent unsigned local RC2 package with 26 messages, generated bindings, package validator PASS and 42 tests PASS. The VAE matrix matches all 26 schema and producer/consumer entries, but one path is incompatible (`amendment-response` omits VAE as consumer), result migration remains required, and the package is unpublished.
- Exact frozen Builder PRD and Spec Builder V2.1 sources are restored, and the Spec Builder suite passes 28 tests. The target Atomic Harness Builder runtime checkout/extensions and Format 02 Content Harness/Remotion consumer remain absent.
- Nine of ten local source artifacts pass exact registered hashes; `SRC-009` remains missing.

## Intended First Deployable Shape

Keep Release 1 modular until operational evidence justifies decomposition:

- `vae-control-plane`: intake mapping, immutable demand facts, planning, routing, event/checkpoint coordination, budget, evaluation/repair coordination, asset promotion, API, and projections.
- `vae-gpu-worker`: executes one validated compiled artifact in a pinned OCI profile; owns no canonical plan or acceptance state.
- independent evaluator adapter: returns typed signed evaluation facts under an identity distinct from the producer.
- adapter ports: `DelegationContractPort`, `WorkflowRuntimePort`, `ComputeFabricPort`, `ObjectStorePort`, `EvaluationPort`, and `ControlTowerProjectionPort`.

Canonical metadata/event state is PostgreSQL-compatible through repository ports. Immutable large artifacts are S3-compatible/content-addressed through `ObjectStorePort`. Queue, event bus, database, object store, cloud provider, and evaluator products remain unselected and must be pinned by an approved release bundle.

## Canonical State Rules

- `DemandSnapshot` is immutable and identified by request ID, demand version, payload hash, and canonical reference.
- `ProductionPlan` is VAE-owned, provider-neutral, append-only, versioned, and hash-addressed.
- ComfyUI API JSON is a compiled provider artifact, never canonical product state.
- Internal execution state is private; Delegation public lifecycle is an externally governed projection.
- Candidates, evaluations, repairs, accepted assets, variants, geometry, usage, and receipts are immutable facts/versions.
- Amendments never mutate accepted demand; owner-approved changes create linked superseding versions.
- VAE result contains production acceptance only. Downstream composition authorization requires a separate acknowledgement.

## Cross-Cutting Invariants

1. Pin demand, plan, profile, workflow, image, custom nodes, model, VAE, LoRA/control, runtime, evaluator, budget, schema, and adapter versions per run.
2. Deterministic validation runs before independent VLM evaluation; applicable hard gates cannot be averaged away.
3. Producer and evaluator identities/credentials/invocations must differ.
4. Selection considers only hard-gate-pass candidates and ranks quality first within authorized budget.
5. Repair changes only causal permitted bindings, preserves declared valid properties, reruns invalidated descendants, and stops after at most three autonomous rounds.
6. Infrastructure retry does not consume a quality-repair round or change creative bindings.
7. Budget pressure cannot weaken meaning, hard gates, evaluator depth, or certified-capability rules.
8. Cancellation, supersession, revocation, and lease fencing block stale output promotion while preserving evidence.
9. Secrets cannot enter plans, provider artifacts, prompts, events, logs, receipts, or object metadata.
10. Unknown required semantics, authority, compatibility, migration, integrity, or lifecycle fail closed.

## Stage 5 Slice After PASS

Implement only this exact interface-preserving path:

```text
typed Visual Asset Demand fixture
-> Visual Production Plan IR
-> registered fixture or real ComfyUI adapter
-> one character candidate portfolio
-> deterministic validation
-> independent VLM evaluation adapter
-> one targeted gesture repair
-> immutable accepted Asset Result
-> composition geometry receipt
```

Mocks are allowed only as `fixture_only` implementations of exact production ports. They cannot change contract shapes or support certification claims. Do not implement every asset family.

## Implementation Conventions Once Authorized

- Attach to verified Builder owners; never implement a replacement workflow runtime, Harness IR, Control Tower, JIT Skill system, or repair graph.
- Generate Delegation bindings from the published package into build artifacts. Do not hand-maintain copied public DTOs.
- Keep domain/application code independent of ComfyUI, cloud, database, queue, object store, and evaluator SDKs; isolate them behind the named ports.
- Prefer immutable typed values and explicit state transitions. Reject raw unvalidated maps at application boundaries.
- Make idempotency keys, content hashes, version references, principal/authority evidence, and receipts explicit.
- Use structured parsers/serializers and canonical encodings. Never derive protocol behavior through string manipulation or model inference.
- Keep provider IDs and provider state inside adapters/receipts, outside plan IR and shared contracts.
- Add abstractions only at verified ownership/integration boundaries or where they remove meaningful duplication.
- Keep changes scoped to the current Story; each Story must pass independently before dependent Stories start.

No programming language/framework is selected by current evidence. Select one only after Builder/runtime integration constraints and approved ADRs establish the target, then record the exact versions and migration/rollback consequences.

## Required Test Layers

- schema, binding, canonical serialization, hash, signature, authority, lifecycle, idempotency/replay, and compatibility tests;
- domain/unit tests for plans, routing, budgets, hard gates, selection, repair, invalidation, lineage, and geometry;
- adapter contract tests for Builder runtime, ComfyUI, local/cloud workers, storage, evaluator, Delegation, and Control Tower;
- checkpoint/restart, duplicate, out-of-order, worker loss, event/audit outage, cancellation, supersession, backup/restore, migration, and rollback fault tests;
- evaluator labeled/golden/adversarial/protected calibration and repair-preservation tests;
- all Delegation conformance and Format 02 scenarios plus VAE benchmark families;
- security tests for least privilege, secret leakage, hostile notes/media, parser limits, artifact integrity, and sandbox escape boundaries.

Tests must prove behavior. Loading declarative case YAML or checking fixture presence is not conformance.

## Mandatory Pre-Implementation Reads

- `docs/implementation/IMPLEMENTATION_READINESS.md`
- `docs/implementation/DEPENDENCY_GRAPH.yaml`
- `docs/implementation/EPICS_AND_VERTICAL_STORIES.md`
- `docs/implementation/FORMAT02_RELEASE_PLAN.md`
- `docs/tech-specs/STAGE2_SPECIFICATION_INDEX.md`
- the Story's owning TS-VAE specification and dependencies
- all three files under `docs/contracts/`
- `governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`
- `governance/READINESS_HARD_GATES.yaml`
- `CROSS_REPO_ISSUES.md`

## Prohibited Shortcuts

- production implementation before PASS;
- VAE-owned changes to shared schemas or lifecycle meanings;
- accepted-demand mutation or silent demand relaxation;
- production-model self-approval;
- hand-edited production ComfyUI graphs;
- unpinned/mutable images, nodes, weights, evaluators, or profiles;
- routine manual approval or ComfyUI operation;
- hidden optional degradation;
- stale result/asset promotion;
- uncertified family/provider/feature claims;
- document completeness presented as executable readiness.
