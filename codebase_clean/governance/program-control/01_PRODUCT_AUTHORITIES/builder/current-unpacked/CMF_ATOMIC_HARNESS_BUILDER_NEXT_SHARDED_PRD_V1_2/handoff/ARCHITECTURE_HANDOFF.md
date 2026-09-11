---
title: Architecture Handoff — CMF Atomic Harness Builder Next
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: ready_for_architecture
created: '2026-07-13'
updated: '2026-07-13'
---

# Architecture Handoff

The Architecture phase must turn this PRD into a coherent technical system without changing the product promise, authority model, category taxonomy, or requirement semantics.

## Required inputs

- complete sharded PRD and combined reading view;
- Decision Register and Product Constitution;
- FR/NFR registries and traceability maps;
- source register and V2.1 brownfield addendum;
- existing Builder, Activative, Visual Syntax, CCSB, prior PRD, and Era 3 source material;
- selected Release 1 reference harness when `OQ-001` is resolved.

## Architecture workstreams

1. **Canonical data and state** — Harness IR, schema evolution, decisions, events, artifacts, receipts, snapshots, migrations.
2. **Evidence and visual understanding** — source adapters, indexing, media normalization, multimodal parsing, deterministic validation, cross-specimen induction.
3. **Builder workflow runtime** — Workflow IR, actor matrix, profile registry, router, scheduler, deterministic and agent node executors, sandboxes, node validation, bounded feedback, CI promotion, rollback, and incidents.
4. **Compiler control plane** — target profiles, lifecycle, phase graph, dependency engine, contract system, context compiler, authorization.
5. **Skill system** — capability registry, skill IR, package compiler, adaptation model, composition recipes, behavioral evals, JIT capsule compiler.
6. **Category and sequencing** — category constitutions, format profiles, registries, Activative Sequencing Intelligence, atomic overlays.
7. **Quality and learning** — evaluators, benchmark stores, protected cases, maturity, hard gates, downstream feedback.
8. **Observability** — event model, Run Ledger, read models, Control Tower command surface, cost and performance telemetry.
9. **Migration and handoff** — V2.1 compatibility, dual-run, Development Capsule, export, implementation deltas, certification.

## Architecture decision requirements

Every major technical decision must include:

- mapped FR/NFR IDs;
- considered alternatives and rejected rationale;
- ownership and public interface;
- data, event, and error contracts;
- determinism versus stochasticity boundary;
- security and authority boundary;
- observability and repair behavior;
- performance and context budgets;
- compatibility and migration implications;
- required tests and benchmark evidence.

## Architecture completion gate

Architecture is complete only when every FR and NFR has a technical owner or an explicit product-level disposition; every cross-feature graph is coherent; all Release 1 work has a testable vertical path; unresolved product questions are returned to the Decision Register rather than silently decided in implementation.


## Constitutional alignment requirements

Architecture and technical specifications must cite `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`, distinguish harness-development Visual Syntax First from runtime Activation First, support the Conversational Activation / Human Expression category, preserve Activative Intelligence and Expression Moment lineage, and prove that generated visual demands carry Visual Semantic, Visual Narrative, Feature Contract, somatic-route, and wrong-reading context.
