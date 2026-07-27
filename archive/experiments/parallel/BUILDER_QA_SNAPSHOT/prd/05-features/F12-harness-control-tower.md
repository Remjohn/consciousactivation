---
title: F12 — Event-Sourced Harness Control Tower and Observability
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F12
governing_decisions:
- D024
- D025
- D026
- D027
- D029
user_journeys:
- UJ-01
- UJ-02
- UJ-04
- UJ-08
- UJ-09
- UJ-10
- UJ-11
functional_requirement_count: 10
---

# F12 — Event-Sourced Harness Control Tower and Observability

**User outcome:** Operators can see what is happening, why, what evidence supports it, who owns the next action, what changed, what was invalidated, and what remains before authorization.

## Description

The Pi Control Tower is the human-facing control plane for the Builder. It renders authoritative state from the Harness IR, Run Ledger, Decision Register, Artifact Registry, and receipts and provides only governed, receipted actions.

## Brownfield baseline

V2.1 exposes CLI status and filesystem artifacts. Parallel workspaces include runbooks and verification, but there is no unified live visual interface for specimen overlays, phase graphs, decisions, skills, contracts, evaluation, repair, cost, and readiness.

## Required product delta

Define event schemas, read models, dashboard manifests, evidence viewers, graph views, cost telemetry, human command surfaces, and integrity rules preventing the UI from becoming a second source of truth.

## Traceability

- **Decisions:** D024, D025, D026, D027, D029
- **User journeys:** UJ-01, UJ-02, UJ-04, UJ-08, UJ-09, UJ-10, UJ-11
- **Cross-cutting NFRs:** NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-UX-001, NFR-UX-002

## Functional Requirements

### FR-117 — Show a run overview

**Requirement:** The Control Tower must display target, category and format profile, lifecycle stage, overall status, active blockers, pending human decisions, authorization trajectory, elapsed time, and actual versus budgeted cost and tokens.

**Consequences (testable):**

- Every status links to its authoritative event or receipt.
- Unknown or stale data is shown explicitly rather than inferred.

**Traceability:** Decisions D025; journeys UJ-01, UJ-09.

### FR-118 — Render the Phase and Context Graphs

**Requirement:** Operators must be able to inspect each phase's state, dependencies, executor, active capsule, inputs, outputs, completion criteria, context manifest, failure owner, and timestamps.

**Consequences (testable):**

- Blocked phases display missing prerequisites and next actions.
- Parallel and invalidated paths are visually distinguishable.

**Traceability:** Decisions D013, D025; journeys UJ-09.

### FR-119 — Expose evidence and visual understanding

**Requirement:** The Control Tower must provide source coverage, specimen inventory, contact sheets, frame or slide navigation, parse overlays, BBOX maps, relationship graphs, composition variables, confidence, knowledge status, gaps, and contradictions.

**Consequences (testable):**

- Clicking a component reveals supporting specimens and function hypotheses.
- Human corrections produce governed events and do not edit source evidence.

**Traceability:** Decisions D007, D025; journeys UJ-02, UJ-09.

### FR-120 — Expose Genesis decisions and authority

**Requirement:** The UI must show decision dependencies, recommendations, evidence, human answers, final decisions, authority status, reopened nodes, waivers, and downstream effects.

**Consequences (testable):**

- The operator can distinguish provisional, ratified, superseded, and invalidated decisions.
- Decision actions invoke the same governed command path as CLI or API actions.

**Traceability:** Decisions D010, D025; journeys UJ-04, UJ-09.

### FR-121 — Expose skills, recipes, and capsules

**Requirement:** The UI must show selected canonical skills, harness adaptations, composition recipes, maturity, behavioral results, loaded references, context inclusion and exclusion, capsule hashes, budgets, and model policy.

**Consequences (testable):**

- An ineligible skill is visibly linked to the blocker it creates.
- The exact evaluated and compiled identities can be compared.

**Traceability:** Decisions D017, D018, D021, D025; journeys UJ-08, UJ-09.

### FR-122 — Expose contracts and module ownership

**Requirement:** Operators must be able to inspect producer and consumer graphs, contract versions and authority, module ownership, test seams, compatibility, and invalidation edges.

**Consequences (testable):**

- Orphan contracts and ownership conflicts are highlighted.
- The view traces from a requirement to its module and contract.

**Traceability:** Decisions D014, D015, D025; journeys UJ-05, UJ-09.

### FR-123 — Expose evaluations and repair history

**Requirement:** The UI must show score dimensions, hard gates, failed cases, repetition distributions, dominant failure patterns, root-cause owner, repair attempts, invalidated artifacts, and before/after results.

**Consequences (testable):**

- A reviewer can move from a score failure to the exact evidence and repair route.
- Repair history remains append-only.

**Traceability:** Decisions D024, D025, D026; journeys UJ-09, UJ-10.

### FR-124 — Track cost, latency, and context usage

**Requirement:** Every deterministic and stochastic operation must report timing, tokens where applicable, model or provider, retries, cache behavior, and budget status to the observability system.

**Consequences (testable):**

- The UI can aggregate per phase, run, target, skill, and accepted Development Capsule.
- Cost data does not replace quality dimensions.

**Traceability:** Decisions D020, D024, D025; journeys UJ-07, UJ-12.

### FR-125 — Provide governed human actions

**Requirement:** The Control Tower may support approve, reject, request evidence, correct a parse, ratify, waive, trigger targeted repair, compare releases, freeze, and export actions only through typed commands that validate authority and append receipts.

**Consequences (testable):**

- Unauthorized actions are rejected without state mutation.
- Every successful action shows its event and affected state.

**Traceability:** Decisions D002, D025, D027; journeys UJ-09.

### FR-126 — Prevent the UI from becoming a second source of truth

**Requirement:** All Control Tower read models must derive from authoritative IR, ledger, registries, and receipts; UI caches and local component state may not define product truth.

**Consequences (testable):**

- A rebuild from authoritative stores reproduces the displayed run state.
- Conflicting cache data is discarded or marked stale.

**Traceability:** Decisions D011, D025, D033; journeys UJ-09.

## Known failure and edge conditions

- A phase is shown as passed without a receipt.
- The UI corrects an IR value directly without a command event.
- A visual overlay hides low confidence or missing specimens.
- Cost is tracked only after final completion.
- A stale dashboard continues to display authorization.

## Explicitly out of scope

- A general analytics platform unrelated to Builder operations.
- Replacing canonical Markdown/JSON exports.
- Selecting a specific frontend framework in the PRD.
