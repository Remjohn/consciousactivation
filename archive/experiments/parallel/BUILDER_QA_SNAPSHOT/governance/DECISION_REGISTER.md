---
title: Builder Product Decision Register
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: locked_product_constitution
created: '2026-07-13'
updated: '2026-07-13'
decision_count: 33
---

# Builder Product Decision Register

These decisions were resolved through the 33-question Grill-me session and form the product constitution for this PRD version. Changes require an explicit decision delta and downstream impact analysis.

## D001 — Product boundary

**Decision:** The product is a harness-development compiler: it produces a typed Harness IR, specifications, phase-local JIT Skills and recipes, module and runtime contracts, evaluation and repair systems, implementation artifacts, and a readiness receipt; it does not implement the final production harness.

**Rationale:** This reaches far enough downstream to remove architectural invention without turning the Builder into an uncontrolled implementation factory.

**Mapped FRs:** FR-008, FR-153, FR-210

## D002 — Authority model

**Decision:** The Builder is a human-governed agentic compiler. Deterministic tooling owns evidence processing and validation; agents investigate and recommend; humans own constitutional, creative-policy, risk, and irreversible architectural decisions.

**Rationale:** High automation is preserved without delegating irreversible policy to a stochastic system.

**Mapped FRs:** FR-005, FR-036, FR-044, FR-045, FR-048, FR-125, FR-132, FR-182, FR-186, FR-201, FR-208

## D003 — Definition of success

**Decision:** Builder success has three gates: structural validity, implementation readiness, and downstream harness effectiveness.

**Rationale:** A valid-looking specification is not sufficient if the resulting harness performs poorly.

**Mapped FRs:** FR-014, FR-016, FR-039, FR-059, FR-062, FR-116, FR-133, FR-159, FR-167, FR-187, FR-190, FR-198, FR-199, FR-204, FR-206, FR-209

## D004 — Compilation targets

**Decision:** The Builder supports three explicit compilation targets: Atomic Content Harness, Visual Asset Editor, and Content↔Asset Delegation Contract. Atomic Content Harness is the primary reference path.

**Rationale:** The targets share infrastructure but own materially different constitutions and authorization criteria.

**Mapped FRs:** FR-001, FR-004, FR-168, FR-170, FR-171, FR-172, FR-173, FR-179, FR-180

## D005 — Canonical input boundary

**Decision:** Each run starts from a configured evidence workspace with an exact target candidate and target-specific source profile.

**Rationale:** The Builder must ground itself in the actual CMF corpus, registries, doctrine, prior implementations, and specimens.

**Mapped FRs:** FR-002, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-017, FR-174

## D006 — Lifecycle

**Decision:** All runs share a governed top-level lifecycle while each compilation target supplies a typed target-specific phase profile.

**Rationale:** This preserves predictable orchestration without flattening materially different product types.

**Mapped FRs:** FR-001, FR-003, FR-004, FR-005, FR-009, FR-170, FR-176, FR-181, FR-183, FR-184, FR-185, FR-186, FR-193, FR-194, FR-201, FR-202

## D007 — Visual Syntax First

**Decision:** Atomic Content Harness runs must complete Visual Syntactic Parsing, composition-variable classification, BBOX evidence mapping, visual-function hypotheses, cross-specimen syntax induction, sequence-grammar drafting, and draft Activative hypotheses before saturation can pass.

**Rationale:** Visual observation and compositional understanding must precede semantic compression and constitutional design.

**Mapped FRs:** FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-023, FR-024, FR-025, FR-026, FR-028, FR-029, FR-030, FR-031, FR-052, FR-063, FR-119, FR-145

## D008 — Atomicity

**Decision:** Atomicity is classified through an evidence-based typed test and receives human ratification.

**Rationale:** Folder names and topics are unreliable boundaries; production promise, visual instrument, state machine, contracts, runtime, evaluation, and repair behavior are decisive.

**Mapped FRs:** FR-026, FR-029, FR-032, FR-033, FR-034, FR-035, FR-036, FR-040, FR-149

## D009 — Genesis entry state

**Decision:** Genesis begins from a compiled but explicitly unratified Draft Harness Model.

**Rationale:** Genesis should challenge a grounded provisional model rather than start from an empty page or merely confirm an opaque conclusion.

**Mapped FRs:** FR-037, FR-038, FR-039

## D010 — Genesis decision protocol

**Decision:** Genesis uses a dependency-driven decision graph, asks one dependency-ready question at a time, records recommendations and human decisions, and reopens affected nodes when contradictions appear.

**Rationale:** This makes Grill-me auditable, resumable, and internally consistent.

**Mapped FRs:** FR-007, FR-040, FR-041, FR-042, FR-043, FR-044, FR-045, FR-046, FR-047, FR-048, FR-049, FR-050, FR-120, FR-158, FR-176, FR-201

## D011 — Canonical source of truth

**Decision:** A typed Harness IR is the canonical source of truth; every document, skill, graph, contract, evaluation, ticket, and receipt is compiled from it.

**Rationale:** Dozens of independently authored artifacts would otherwise drift and contradict one another.

**Mapped FRs:** FR-028, FR-037, FR-038, FR-041, FR-046, FR-051, FR-052, FR-053, FR-054, FR-055, FR-056, FR-057, FR-058, FR-059, FR-126, FR-152, FR-175, FR-181, FR-184, FR-194, FR-207

## D012 — Capability ownership

**Decision:** Every required capability receives an explicit ownership assignment such as deterministic module, typed model program, JIT Skill, reference, human decision, independent evaluator, provider adapter, or hybrid pipeline.

**Rationale:** The Builder must act as an architecture compiler rather than turn every hard problem into a prompt.

**Mapped FRs:** FR-021, FR-023, FR-060, FR-061, FR-062, FR-063, FR-071, FR-082, FR-084, FR-102, FR-182, FR-184, FR-186, FR-188, FR-195, FR-196, FR-199, FR-210

## D013 — Phase and context architecture

**Decision:** Every generated harness receives a harness-specific typed Phase Graph and Context Graph.

**Rationale:** Different atomic production promises require different workflows and minimum complete contexts.

**Mapped FRs:** FR-066, FR-067, FR-068, FR-071, FR-118, FR-181, FR-183, FR-184, FR-189, FR-197, FR-210

## D014 — Phase handoffs

**Decision:** All authoritative phase-to-phase communication uses versioned typed contracts; downstream phases cannot silently rewrite upstream outputs.

**Rationale:** Sparse, validated handoffs reduce context pollution and make failures traceable.

**Mapped FRs:** FR-024, FR-069, FR-070, FR-071, FR-122, FR-154, FR-180, FR-181, FR-183, FR-184, FR-188, FR-190, FR-191, FR-196, FR-197, FR-200, FR-210

## D015 — Module architecture

**Decision:** The Builder compiles responsibility-centered deep modules with explicit contracts, invariants, exclusions, dependencies, failure ownership, and test seams.

**Rationale:** Technology-layer modules scatter cohesive responsibilities and hide semantic authority.

**Mapped FRs:** FR-064, FR-065, FR-122, FR-153, FR-182, FR-188, FR-195

## D016 — Reference loading

**Decision:** The Builder compiles a versioned Reference and Loading Graph governing exactly which doctrine, registries, examples, ontologies, and SPR resources each phase may load.

**Rationale:** Progressive disclosure and phase-local loading protect relevance, reproducibility, and context budgets.

**Mapped FRs:** FR-072, FR-073, FR-074, FR-075, FR-076, FR-088, FR-196

## D017 — Layered skill compilation

**Decision:** The skill system has four layers: Canonical Skill, Harness-local Skill Adaptation, Skill Composition Recipe, and ephemeral phase-local JIT Execution Capsule. New canonical skills require a formal capability-gap test.

**Rationale:** This preserves the original runtime-compiled prompt insight while separating durable procedural capability from temporary execution context.

**Mapped FRs:** FR-075, FR-076, FR-081, FR-082, FR-084, FR-085, FR-086, FR-087, FR-088, FR-090, FR-091, FR-092, FR-101, FR-121, FR-189, FR-210

## D018 — JIT compilation

**Decision:** Generated harnesses use a deterministic, reproducible JIT compiler to assemble the smallest complete phase-local Execution Capsule.

**Rationale:** Deterministic assembly removes hidden prompt selection while bounded stochastic execution retains semantic and creative judgment.

**Mapped FRs:** FR-080, FR-094, FR-099, FR-100, FR-102, FR-121, FR-188, FR-189

## D019 — Bindings and precedence

**Decision:** All runtime variables use a typed dependency, authority, precedence, conflict, invalidation, and degradation system and must resolve before capsule compilation.

**Rationale:** Architectural conflicts and missing values must never be silently delegated to the execution model.

**Mapped FRs:** FR-042, FR-072, FR-086, FR-093, FR-095, FR-096, FR-097, FR-184, FR-186, FR-189, FR-193, FR-194, FR-197

## D020 — Context budget

**Decision:** Every phase uses a Minimum Complete Context policy; required context is never silently truncated.

**Rationale:** A smaller but complete context is preferable to both indiscriminate loading and blind token-limit truncation.

**Mapped FRs:** FR-068, FR-075, FR-077, FR-078, FR-079, FR-080, FR-098, FR-099, FR-101, FR-124, FR-189, FR-191, FR-196, FR-199, FR-200, FR-209

## D021 — Skill maturity

**Decision:** Canonical skills, adaptations, recipes, capsules, and end-to-end phase behavior require layered behavioral evaluation and maturity promotion before production use.

**Rationale:** Structural validity and persuasive prose do not prove behavioral improvement.

**Mapped FRs:** FR-058, FR-074, FR-081, FR-083, FR-087, FR-089, FR-090, FR-100, FR-103, FR-104, FR-105, FR-106, FR-107, FR-108, FR-121, FR-131, FR-136, FR-155, FR-164, FR-178, FR-185, FR-189, FR-190, FR-198, FR-200, FR-206

## D022 — Builder benchmark strategy

**Decision:** Builder quality is proven through a staged benchmark portfolio anchored by one mandatory primary reference harness and expanded through transfer targets.

**Rationale:** A reference slice prevents abstract framework development while transfer targets prevent overfitting.

**Mapped FRs:** FR-109, FR-116, FR-157, FR-159, FR-162, FR-167, FR-169, FR-185, FR-187, FR-204, FR-205, FR-206

## D023 — Benchmark corpus

**Decision:** The benchmark corpus combines real specimens, expert goldens, known failures, adversarial near-misses, incomplete or contradictory evidence, controlled mutations, transfer cases, and protected release cases.

**Rationale:** Successful examples alone cannot demonstrate boundary understanding, uncertainty handling, or robustness.

**Mapped FRs:** FR-015, FR-020, FR-106, FR-110, FR-111, FR-112, FR-155, FR-204, FR-205

## D024 — Performance scorecard

**Decision:** Builder performance uses multidimensional scores, hard release gates, repeated fresh-context runs, and target-specific thresholds.

**Rationale:** No average score may compensate for an evidentiary, constitutional, atomicity, contract, or readiness failure.

**Mapped FRs:** FR-105, FR-112, FR-113, FR-114, FR-115, FR-123, FR-124, FR-178, FR-190, FR-192, FR-193, FR-197, FR-198, FR-199, FR-200, FR-201, FR-203, FR-204, FR-205, FR-206, FR-208, FR-209

## D025 — Observability

**Decision:** The Builder generates an event-sourced Pi Harness Control Tower backed by the Harness IR, Run Ledger, Decision Register, Artifact Registry, and receipts.

**Rationale:** No status should exist without evidence, no state change without an event, and no human action without a receipt.

**Mapped FRs:** FR-002, FR-006, FR-007, FR-013, FR-050, FR-067, FR-080, FR-117, FR-118, FR-119, FR-120, FR-121, FR-122, FR-123, FR-124, FR-125, FR-126, FR-166, FR-186, FR-194, FR-195, FR-202, FR-203, FR-207, FR-208, FR-209

## D026 — Repair

**Decision:** The Builder compiles a typed Repair and Invalidation Graph with root-cause analysis, smallest-responsible-layer repair, targeted regression, escalation, and receipts.

**Rationale:** Whole-run regeneration is wasteful and dangerous; local failures must invalidate exactly their dependent descendants.

**Mapped FRs:** FR-047, FR-070, FR-071, FR-103, FR-123, FR-127, FR-128, FR-129, FR-130, FR-131, FR-132, FR-158, FR-180, FR-183, FR-184, FR-191, FR-192, FR-193, FR-194, FR-205, FR-208

## D027 — Implementation authorization

**Decision:** Implementation begins only after an evidence-backed Authorization Gate; a restricted prototype-only state is available for empirical uncertainties.

**Rationale:** Readiness is an authorization decision, not a count of documents or schemas.

**Mapped FRs:** FR-003, FR-005, FR-018, FR-035, FR-048, FR-049, FR-059, FR-097, FR-107, FR-125, FR-133, FR-134, FR-135, FR-136, FR-178, FR-184, FR-190, FR-201, FR-203, FR-208, FR-210

## D028 — V2.1 migration

**Decision:** V2.1 evolves through controlled, benchmarked increments with compatibility, deprecation, mapping, and regression tracking.

**Rationale:** The existing source saturation, decision graph, ratification, OpenSpec, and readiness capabilities are valuable and must not be discarded without evidence.

**Mapped FRs:** FR-011, FR-053, FR-055, FR-116, FR-159, FR-160, FR-161, FR-162, FR-163, FR-164, FR-165, FR-166, FR-185, FR-187, FR-206, FR-207, FR-208

## D029 — Implementation handoff

**Decision:** The Builder delivers a traceable Development Capsule containing authoritative specifications and only the executable scaffolding justified by the Harness IR.

**Rationale:** The handoff must remove architectural invention without generating speculative boilerplate or unapproved business logic.

**Mapped FRs:** FR-008, FR-054, FR-056, FR-058, FR-136, FR-151, FR-152, FR-153, FR-154, FR-155, FR-156, FR-158, FR-159, FR-177, FR-195

## D030 — Category architecture and sequencing

**Decision:** The content-harness architecture is Shared Activative Core → Canonical Format Category → Category Format Profile → Atomic Harness. Every short-form video and 2D character-animation harness includes format-adapted Activative Sequencing Intelligence informed by visual and temporal syntax.

**Rationale:** Sequencing is a primary Activative intelligence layer, not an output-format afterthought.

**Mapped FRs:** FR-022, FR-027, FR-030, FR-031, FR-076, FR-137, FR-138, FR-141, FR-142, FR-143, FR-144, FR-145, FR-146, FR-147, FR-149, FR-171

## D031 — Canonical category constitutions

**Decision:** The four categories—Short-Form Edited Video, 2D Character Animation, Carousels, and Supervisuals—are governed through versioned category constitutions.

**Rationale:** Each category owns different parsing, sequencing, registries, runtime constraints, evaluation, repair, and migration rules.

**Mapped FRs:** FR-022, FR-027, FR-030, FR-138, FR-139, FR-140, FR-141, FR-142, FR-143, FR-144, FR-145, FR-146, FR-148, FR-150, FR-171

## D032 — Release strategy

**Decision:** Release 1 establishes the complete architectural spine and proves it through one fully implemented and certified Atomic Content Harness vertical slice; other targets remain structurally supported but uncertified.

**Rationale:** One real path must prove the architecture before the Builder claims generality.

**Mapped FRs:** FR-109, FR-135, FR-156, FR-157, FR-167, FR-168, FR-169, FR-185, FR-187, FR-204

## D033 — Binding anti-goals

**Decision:** The product constitution includes machine-testable boundaries preventing implementation creep, universal creative engines, category flattening, unsupported evidence promotion, skill sprawl, orchestration leakage, silent context truncation, broad repairs, hidden operational state, and premature general certification.

**Rationale:** Positive requirements alone do not prevent gradual architectural drift.

**Mapped FRs:** FR-008, FR-034, FR-040, FR-057, FR-064, FR-079, FR-084, FR-090, FR-102, FR-114, FR-126, FR-130, FR-149, FR-153, FR-168, FR-169, FR-179, FR-188, FR-192, FR-193, FR-196, FR-198, FR-210
