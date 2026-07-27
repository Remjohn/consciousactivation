---
title: Decision Register
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
decision_count: 28
---

# Decision Register

These decisions were locked through the 28-question Grill-me session. Changes require an explicit product decision delta.

## D001 — Complete visual asset-resolution system

**Status:** locked  
**Decision:** The product transforms authorized Visual Asset Demand Contracts into production-ready assets through governed reuse, retrieval, extraction, transformation, compositing, deterministic construction, generation, animation, or capture requests without changing authorized meaning.

**Features:** F01, F22  
**FR coverage:** FR-001–FR-176

## D002 — Autonomous production with exception-only human intervention

**Status:** locked  
**Decision:** Routine production is fully autonomous. Human intervention occurs only after three failed quality-repair rounds, unauthorized cost, unresolved capability gaps, blocking constraint conflicts, unresolved evaluator contradiction, or explicit degraded acceptance.

**Features:** F01, F07, F15, F16, F18, F20  
**FR coverage:** FR-001–FR-160

## D003 — Typed Visual Asset Demand is authoritative

**Status:** locked  
**Decision:** Every run requires a versioned typed demand contract. Natural-language notes may enrich but never override its semantic, Activative, composition, continuity, delivery, or budget authority.

**Features:** F02, F09, F19, F20, F22  
**FR coverage:** FR-009–FR-176

## D004 — Layered asset effectiveness

**Status:** locked  
**Decision:** Acceptance requires production validity, demand fidelity, and effectiveness in the intended composition; both asset-level and composition-level evaluation are mandatory.

**Features:** F01, F05, F14, F21  
**FR coverage:** FR-001–FR-168

## D005 — Governed multi-method resolution

**Status:** locked  
**Decision:** The editor selects the least complex reliable route and may compose approved routes rather than default to generation.

**Features:** F03, F06, F09  
**FR coverage:** FR-017–FR-072

## D006 — Canonical asset-family ontology

**Status:** locked  
**Decision:** Shared versioned asset families govern production capabilities while harness-specific roles and Activative functions preserve precise meaning.

**Features:** F03, F06, F11  
**FR coverage:** FR-017–FR-088

## D007 — Reference Evidence and Production Assets remain distinct

**Status:** locked  
**Decision:** Reference material cannot enter final composition silently; promotion requires lineage, production transformation or approval, and evaluation.

**Features:** F03, F04  
**FR coverage:** FR-017–FR-032

## D008 — Immutable versioned asset lineage

**Status:** locked  
**Decision:** Candidates, repairs, accepted masters, delivery variants, supersession, and consumption are explicit immutable versions and lifecycle events.

**Features:** F04, F11, F19  
**FR coverage:** FR-025–FR-152

## D009 — Typed Composition Intent and image-conditioned geometry

**Status:** locked  
**Decision:** The Content Harness owns composition intent; the editor returns feasible geometry, masks, safe zones, gaze, crop variants, collision analysis, and nonbinding recommendations.

**Features:** F02, F05, F09, F11, F19, F20  
**FR coverage:** FR-009–FR-160

## D010 — Dynamic specialist workcell

**Status:** locked  
**Decision:** The runtime compiles the smallest sufficient set of specialist authorities and uses an independent VLM evaluator; no standalone Rights Analyst or routine manual rights-review layer is required.

**Features:** F01, F06, F07, F14  
**FR coverage:** FR-001–FR-112

## D011 — Versioned Visual Capability Registry

**Status:** locked  
**Decision:** ComfyUI workflows, models, VAEs, LoRAs, controls, custom nodes, runtime profiles, compatibility, performance, and failure patterns are governed and versioned.

**Features:** F06, F08, F09, F12  
**FR coverage:** FR-041–FR-096

## D012 — Provider-neutral Visual Production Plan IR

**Status:** locked  
**Decision:** Every demand compiles into a typed provider-neutral plan; ComfyUI JSON and other provider payloads are deterministic compiled artifacts, not the source of meaning.

**Features:** F05, F06, F07, F09  
**FR coverage:** FR-033–FR-072

## D013 — Event-sourced resumable production graph

**Status:** locked  
**Decision:** Plans execute as typed dependency graphs with isolated nodes, checkpoints, event history, infrastructure recovery, targeted invalidation, and bounded parallelism.

**Features:** F04, F07, F09, F10, F12, F15  
**FR coverage:** FR-025–FR-120

## D014 — Syntax-aware Visual Asset Memory

**Status:** locked  
**Decision:** Memory tracks rendered usage context, Visual Syntax role, Activative function, transformations, neighboring elements, continuity, and VLM recurrence verdict; repetition is judged by contextual function, not frequency.

**Features:** F04, F11, F17, F18  
**FR coverage:** FR-025–FR-144

## D015 — Hybrid containerized Visual Compute Fabric

**Status:** locked  
**Decision:** Approved workloads may run across local, self-hosted, cloud, autoscaled, or approved external compute through immutable runtime profiles.

**Features:** F08, F10, F12  
**FR coverage:** FR-057–FR-096

## D016 — Governed visual capability development

**Status:** locked  
**Decision:** Reusable capability gaps may trigger a separate LoRA/model/control/workflow adaptation pipeline with evidence sufficiency, sandboxed training, benchmarks, shadow use, promotion, and rollback.

**Features:** F08, F13  
**FR coverage:** FR-057–FR-104

## D017 — Versioned Visual Evaluation Profiles

**Status:** locked  
**Decision:** Asset-family-aware profiles combine deterministic validation, independent VLM asset and composition evaluation, syntax-aware recurrence analysis, and temporal evaluation where relevant.

**Features:** F04, F05, F07, F08, F10, F11, F14, F15, F21  
**FR coverage:** FR-025–FR-168

## D018 — Typed causal repair and invalidation

**Status:** locked  
**Decision:** Repairs preserve what is already correct, modify only permitted causal bindings, rerun only invalidated nodes, and stop after three VLM-directed quality rounds.

**Features:** F04, F05, F06, F07, F09, F10, F14, F15, F20, F21  
**FR coverage:** FR-025–FR-168

## D019 — Budgeted candidate portfolios and Budget Programs

**Status:** locked  
**Decision:** Lean, Standard, Premium, Exploration, Capability Learning, and Custom programs govern candidate counts, parallelism, evaluator depth, production learning, time, and cost.

**Features:** F02, F06, F08, F09, F10, F12, F13, F16, F17, F18, F21  
**FR coverage:** FR-009–FR-168

## D020 — Governed Visual Steering Intelligence with CMF-OKF projection

**Status:** locked  
**Decision:** Cross-run evidence may become versioned Steering Recipes after controlled validation. Smart retrieval uses authority filters, typed graph traversal, hybrid search, visual/syntax matching, VLM reranking, contradiction coverage, and Minimum Complete Context. CMF-OKF is a readable knowledge projection, not operational truth.

**Features:** F06, F11, F13, F14, F15, F16, F17, F18, F21  
**FR coverage:** FR-041–FR-168

## D021 — Visual Asset Editor Control Tower specialization

**Status:** locked  
**Decision:** The existing event-sourced Harness Control Tower architecture is preserved and receives Visual Asset Editor views and event projections.

**Features:** F10, F11, F12, F16, F17, F18, F22  
**FR coverage:** FR-073–FR-176

## D022 — Inspectable supervisory console

**Status:** locked  
**Decision:** The operator controls policies, budgets, experimental scope, costs, and exceptions while ordinary production remains autonomous and inspectable.

**Features:** F07, F16, F18  
**FR coverage:** FR-049–FR-144

## D023 — Asynchronous contract-driven service

**Status:** locked  
**Decision:** Registered callers submit immutable demand versions through an idempotent asynchronous API and receive events, typed exceptions, and provenance-complete Asset Result Contracts.

**Features:** F02, F04, F10, F12, F18, F19, F22  
**FR coverage:** FR-009–FR-176

## D024 — Typed constraint conflict and amendment proposal

**Status:** locked  
**Decision:** The editor may diagnose infeasibility and propose nonbinding amendments but cannot silently relax the authorized demand.

**Features:** F02, F05, F09, F15, F18, F19, F20  
**FR coverage:** FR-009–FR-160

## D025 — Layered benchmark portfolio and staged certification

**Status:** locked  
**Decision:** Production promotion requires family-aware, syntax-context-aware, evaluator, repair, recovery, compatibility, shadow, limited-production, and rollback evidence with hard gates.

**Features:** F03, F08, F12, F13, F14, F16, F21, F22  
**FR coverage:** FR-017–FR-176

## D026 — Release 1 Format 02 reference vertical slice

**Status:** locked  
**Decision:** Release 1 proves a complete autonomous 2D Character Animation / Minimal Coach Theatre character-and-scene path; other asset families remain structurally represented and uncertified.

**Features:** F03, F13, F21, F22  
**FR coverage:** FR-017–FR-176

## D027 — Independent versioning with governed compatibility

**Status:** locked  
**Decision:** The editor, contracts, registries, evaluation profiles, and compute runtimes evolve independently through explicit compatibility manifests, pinned versions, migration rules, and rollback.

**Features:** F02, F03, F04, F08, F10, F12, F13, F14, F17, F19, F20, F21, F22  
**FR coverage:** FR-009–FR-176

## D028 — Formal implementation authorization gate

**Status:** locked  
**Decision:** PRD approval authorizes Architecture only. Implementation requires preserved upstream architecture, representative contracts, Format 02 fixtures, compute proof, evaluator readiness, benchmark plan, and a Development Capsule.

**Features:** F01, F02, F13, F19, F21, F22  
**FR coverage:** FR-001–FR-176
