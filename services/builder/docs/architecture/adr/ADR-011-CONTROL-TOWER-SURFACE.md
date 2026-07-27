# ADR-011: Control Tower Surface

Status: `ACCEPTED`

Owners: UX, architecture, and operations. Trace: D002, D011, D025, D027; TS-12. Blocker: BD-009.

## Context

Operators need live evidence, graphs, decisions, workflows, costs, repairs, and authorization. A UI-owned database or optimistic local state would contradict event-sourced authority. Pi is the authoring environment but core contracts must remain adapter-bounded.

## Decision

Expose a FastAPI command/query API and a React/TypeScript Control Tower launched or linked from Pi. Read models are idempotent event projections. UI actions submit typed commands with expected versions and render authoritative receipts. The UI stores presentation preferences only.

## Alternatives

- CLI only: rejected for graph/evidence inspection and operational use.
- Pi skill responses only: rejected because status and actions need durable public seams.
- Desktop-native UI first: rejected provisionally due portability and delivery cost.
- Direct database admin UI: rejected because it bypasses domain authority.

## Interfaces, Data, And Errors

Versioned REST/stream APIs for runs, graphs, evidence, decisions, skills, evaluation, workflow, events, exports, and commands. Errors include stale version, unauthorized action, projection lag, redacted data, command rejection, and service unavailable.

## Authority, Security, And Determinism

API command handlers enforce authority. Projections exclude protected labels, secrets, raw chain-of-thought, and unrelated sources. Exports are redacted, hashed, and audited.

## Consequences

Positive: accessible operational surface, testable API, and Pi integration without core coupling. Cost: two frontend/backend codebases and projection operations.

## Observability, Performance, Migration

Target WCAG 2.2 AA, keyboard completeness, p95 query under 500 ms, command acknowledgement under one second, event-to-view lag under two seconds, pending calibration. Projection versions rebuild side-by-side and switch atomically.

## V1.2 Constitutional Alignment Amendment

The accepted FastAPI/React and event-derived authority decision is unchanged; approved routes receive additive constitutional projections only.

| Implementation owner | Component boundary | Data / contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- |
| control_tower_projection_owner | Projection is read-only and event-derived; UI stores no constitutional truth | category/profile, rich semantic lineage, Activative Calls, Reaction Receipts, Expression Moments, wrong-reading locks, HG-015, and external handoff refs | Stale/unavailable projection is explicit; protected reaction data is redacted; missing truth is never synthesized | event replay, redaction, stale version, accessibility, and command-authority fixtures | Existing routes show additive V1.2 evidence with unchanged command authorization | Additive projection/API version; original UX approval and ratification receipt remain valid |

## Verification

Contract, replay, stale-command, authorization, redaction, accessibility, performance, disconnection, and projection-rebuild tests are mandatory before acceptance.
