---
title: PRD 06 — Cross-Cutting Non-Functional Requirements
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
section: '06'
nfr_count: 53
---

# 6. Cross-Cutting Non-Functional Requirements

## Reliability and execution integrity

### NFR-REL-001 — Deterministic replay

Given identical locked sources, ratified decisions, compiler versions, and configuration, deterministic Builder stages must reproduce byte-identical authoritative artifacts or record an explicit nondeterminism exception.

### NFR-REL-002 — Resumability

Every run must resume after interruption from the last committed authoritative event without replaying completed human decisions.

### NFR-REL-003 — Idempotent compilation

Recompiling an unchanged Harness IR must not create semantically different artifacts or duplicate ledger events.

### NFR-REL-004 — Failure isolation

A phase failure must not corrupt locked evidence, ratified decisions, or unaffected artifacts.

## Performance, cost, and context budgets

### NFR-PERF-001 — Interactive Control Tower

Common Control Tower status and detail queries should render within 2 seconds at the reference-corpus scale, excluding intentional long-running model operations.

### NFR-PERF-002 — Compilation budget visibility

Every stochastic phase and JIT capsule must declare expected token, latency, and cost budgets and emit actual usage.

### NFR-PERF-003 — No hidden budget overflow

A phase that exceeds its hard context or cost budget must block, degrade through an approved policy, or request authorization; it may not continue silently.

### NFR-PERF-004 — Parallel-safe work

Independent deterministic scans, benchmark repetitions, and evaluator tasks should support bounded parallel execution without shared-state conflicts.

## Corpus and workload scale

### NFR-SCALE-001 — Corpus-scale evidence processing

The Builder must inventory and index the reference-corpus scale without losing source coverage, stable identities, or bounded parallelism; exact thresholds are calibrated in Architecture and benchmarks.

## Traceability and provenance

### NFR-TRACE-001 — End-to-end provenance

Every material requirement, IR value, generated artifact, decision, benchmark result, and authorization state must be traceable to its source evidence or governing decision.

### NFR-TRACE-002 — Append-only operational history

Run and human-action history must be append-only or cryptographically superseded; destructive history editing is prohibited.

### NFR-TRACE-003 — Evaluated artifact identity

Production eligibility must bind exact source-IR, skill, recipe, capsule, compiler, and evaluation-receipt hashes.

### NFR-TRACE-004 — Knowledge-status integrity

No system component may promote generated or hypothesized content into observed or ratified status without the required authority transition.

## Observability

### NFR-OBS-001 — Event completeness

Every lifecycle transition, blocker, decision, waiver, invalidation, repair, benchmark verdict, and authorization change must emit a typed event.

### NFR-OBS-002 — Evidence-backed status

Every displayed status must link to the criteria, events, artifacts, or receipts that justify it.

### NFR-OBS-003 — No second source of truth

The Control Tower may mutate state only through governed commands that update the Harness IR or run ledger and emit receipts.

### NFR-OBS-004 — Exportability

Operators must be able to export machine-readable run state, scorecards, decision history, artifacts, and receipts without scraping the UI.

## Builder workflow runtime and execution factory

### NFR-WORKFLOW-001 — Reproducible workflow routing

Given the same request classification, target profile, risk state, and workflow registry version, the router must select the same workflow profile or emit an explicit nondeterminism receipt.

### NFR-WORKFLOW-002 — Explicit actor ownership

Every workflow node must identify whether its primary actor is deterministic code, a bounded agent program, a human gate, or a governed hybrid; undocumented general-agent ownership is prohibited.

### NFR-WORKFLOW-003 — Typed node handoffs

Every node-to-node handoff must use a versioned contract with validated producer, consumer, authority, error, and completion semantics.

### NFR-WORKFLOW-004 — Bounded control flow

Retries, loops, timeouts, fan-out, arbitration, and fallback routes must have declared limits and terminal conditions; unbounded autonomous looping is prohibited.

### NFR-WORKFLOW-005 — Idempotent workflow resume

A workflow must resume from committed node state without duplicating successful side effects, replaying ratified human actions, or silently changing the selected profile.

### NFR-WORKFLOW-006 — Failure containment

A failed node, agent, tool, sandbox, or workflow profile must not corrupt locked sources, ratified decisions, protected benchmarks, or unaffected workflow branches.

### NFR-WORKFLOW-007 — Sandbox least privilege

Node sandboxes must receive only approved tools, sources, secrets, network access, storage, compute, and lifetime required by the node contract.

### NFR-WORKFLOW-008 — Bounded parallelism

Parallel execution is allowed only for dependency-independent work with explicit concurrency, budget, merge, cancellation, and conflict policies.

### NFR-WORKFLOW-009 — Risk-aware model and compute routing

Model tier, repetition count, candidate fan-out, evaluator strength, and compute budget must be selected by explicit task-complexity, risk, and expected-value policy and recorded in the run.

### NFR-WORKFLOW-010 — Workflow observability

Every workflow node and route must emit start, completion, validation, failure, retry, cancellation, cost, latency, and artifact events sufficient to reconstruct execution.

### NFR-WORKFLOW-011 — Workflow-level testability

Every production workflow profile must support contract tests, end-to-end integration tests, fault injection, resume tests, route tests, and rollback tests at stable public seams.

### NFR-WORKFLOW-012 — Versioned promotion and rollback

Workflow definitions, routers, node contracts, and execution policies must be versioned, maturity-gated, promotable through CI, and rollback-safe with migration receipts.

## Security, authority, and source safety

### NFR-SEC-001 — Source immutability

Configured source repositories, archives, and specimens are read-only evidence unless an explicit import or migration action creates a new governed copy.

### NFR-SEC-002 — Path and archive safety

The Builder must prevent archive traversal, unsafe extraction, executable surprise, and unbounded recursive ingestion.

### NFR-SEC-003 — Authority enforcement

Only authorized actors may ratify constitutional decisions, approve waivers, freeze category constitutions, or issue implementation authorization.

### NFR-SEC-004 — Secret isolation

Credentials and provider secrets must never be written into Harness IR, generated skills, execution capsules, logs, or exported Development Capsules.

## Architecture integrity

### NFR-ARCH-001 — Explicit ownership integrity

Every capability, phase, module, contract, skill, evaluator, repair, and human gate must have the ownership cardinality permitted by its schema; undocumented general-agent ownership is prohibited.

### NFR-ARCH-002 — Executable graph integrity

Phase, context, contract, dependency, loading, and repair graphs must be acyclic where execution requires a DAG, explicitly model approved loops, and fail validation on unresolved cycles or orphan nodes.

## Testability

### NFR-TEST-001 — Public-seam testability

Every implementation module and behaviorally significant skill must expose stable public seams and fixtures sufficient for contract, behavioral, integration, benchmark, and adversarial testing without coupling tests to hidden internals.

## Category and atomic ownership

### NFR-CAT-001 — Category isolation

Category and format-profile ontologies, registries, parsing fields, runtime rules, and evaluators must not leak into unrelated categories unless a shared abstraction is explicitly proven and versioned.

### NFR-CAT-002 — Atomic creative ownership

Creative production promise, semantic workcell, visual or temporal grammar, legal variables, and format-native evaluation remain atomic-harness-owned unless implemented transfer evidence authorizes extraction.

### NFR-CAT-003 — Sequence fidelity

For sequence-bearing products, the compiled architecture must preserve required viewer-state progression, scene or slide roles, timing or swipe logic, continuity, payoff, and intended reaction through typed contracts and category-appropriate evaluation.

## Evaluation and benchmark integrity

### NFR-EVAL-001 — Protected benchmark integrity

Protected release cases and expected labels must be access-controlled and excluded from training or prompt construction paths.

### NFR-EVAL-002 — Repeated-run measurement

Critical stochastic benchmark cases must run in fresh contexts with recorded repetition count, variance, minimum, mean, and failure frequency.

### NFR-EVAL-003 — Independent evaluation

A generator or reasoning phase may not be the sole authority approving its own output.

### NFR-EVAL-004 — Category-appropriate evaluation

Evaluation dimensions, thresholds, fixtures, and repair routes must reflect the selected category and format profile; metrics from one production substrate may not substitute for another without an explicit equivalence test.

## Compatibility and migration

### NFR-COMPAT-001 — V2.1 compatibility

Existing V2.1 runs and compiled packages must remain readable or receive an explicit migration path with loss and incompatibility receipts.

### NFR-COMPAT-002 — Schema evolution

IR, contract, event, category, and skill schemas must be versioned and support documented compatibility and migration rules.

### NFR-COMPAT-003 — Artifact deprecation

Deprecated outputs must include replacement guidance, affected consumers, removal gates, and regression evidence.

## Portability and adapter boundaries

### NFR-PORT-001 — Portable source profiles

Source profiles must use resolvable URIs or paths and support local directories and archives without requiring one machine-specific layout.

### NFR-PORT-002 — Runtime adapter boundary

Core IR and compilation logic must not be coupled irreversibly to one model provider or one agent harness.

## Operator experience and accessibility

### NFR-UX-001 — Accessible Control Tower

The Pi UI must support keyboard navigation, readable status semantics, non-color-only indicators, and accessible evidence inspection.

### NFR-UX-002 — Progressive disclosure

The UI and generated documents must lead with decisions, blockers, and evidence and disclose lower-level technical detail on demand.

## Maintainability and evolution

### NFR-MAINT-001 — Single-source generation

Readable documents and executable artifacts must be compiled from canonical IR or registries rather than independently maintained duplicates.

### NFR-MAINT-002 — Skill ecology maintainability

Canonical skill duplication, relation cycles, unsupported dependencies, and maturity violations must be detectable automatically.

### NFR-MAINT-003 — Category migration safety

A category-constitution change must identify dependent harnesses, run the required benchmark portfolio, and issue a migration receipt before release.
