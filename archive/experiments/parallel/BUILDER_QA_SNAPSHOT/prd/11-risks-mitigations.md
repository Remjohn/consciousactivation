---
title: PRD 11 — Risks and Mitigations
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
section: '11'
risk_count: 16
---

# 11. Risks and Mitigations

| ID | Risk | Failure mode | Mitigation |
| --- | --- | --- | --- |
| R-001 | Meta-framework overbuilding | The project may perfect abstractions without producing a real harness. | Keep one reference harness as a continuous integration target and require a working vertical slice in Release 1. |
| R-002 | Benchmark overfitting | The Builder may learn visible labels instead of general rules. | Use protected release cases, controlled mutations, transfer targets, and independent expert review. |
| R-003 | Visual parser unreliability | Multimodal parsing may omit or misclassify important components and states. | Use typed outputs, multiple views, deterministic geometry checks, independent evaluators, and selective human ratification. |
| R-004 | Skill sprawl | Every new capability may be expressed as another large skill. | Enforce canonical reuse, capability-gap analysis, no-op controls, progressive disclosure, and maturity gates. |
| R-005 | Category flattening | Shared infrastructure may absorb category or atomic creative policy. | Use explicit ownership tests, category constitutions, dependency impact analysis, and benchmark transfer gates. |
| R-006 | IR and document divergence | Readable documents may drift from machine state. | Compile documents from IR, hash artifacts, prohibit manual authoritative edits, and validate round-trip traceability. |
| R-007 | Control Tower becomes a second source of truth | UI state may diverge from the run ledger. | Use command/event architecture, authoritative reads from IR and ledger, and receipted mutations only. |
| R-008 | V2.1 migration damage | A rewrite may lose working Genesis, ratification, OpenSpec, or readiness behavior. | Inventory retained capabilities, run dual compilation, preserve compatibility, and deprecate only with regression evidence. |
| R-009 | Excessive phase fragmentation | Too many model calls may increase latency and lose useful coupling. | Compile phases from responsibility and risk, use deterministic code for mechanical work, and benchmark merged versus isolated calls. |
| R-010 | Human-review overload | The architecture may require too many approvals and visual corrections. | Limit human gates to constitutional or high-impact ambiguity and use confidence, batching, and progressive disclosure. |
| R-011 | Provider coupling | The system may assume one model or tool behavior. | Keep typed program and adapter boundaries, record model policy, and test critical capabilities across supported runtimes. |
| R-012 | Downstream feedback arrives too late | Builder defects may only become visible after expensive implementation. | Use prototype-only authorization, early vertical slices, implementation-question logging, and online benchmark refinement. |
| R-013 | Workflow runtime becomes a second meta-framework | The team may build a broad orchestration platform before proving the reference Builder path. | Implement only the nodes and profiles exercised by the reference harness, then extract reusable workflow mechanisms from evidence. |
| R-014 | Router misclassification | A normal compilation, migration, repair, or hotfix may be sent through the wrong workflow profile. | Use typed request classification, protected route cases, human escalation for uncertain high-risk classes, and recorded router confidence. |
| R-015 | Sandbox and parallel-compute sprawl | Isolation and candidate fan-out may multiply cost, stale environments, and merge complexity. | Set workflow-level concurrency and compute budgets, automatic cleanup, quality-gated races, and per-profile cost telemetry. |
| R-016 | Automation hides operational ignorance | The workflow may appear autonomous while no one understands node behavior or failure propagation. | Require a shadow workflow, node-level contracts, fault injection, run reconstruction, and operator drill procedures before production promotion. |
