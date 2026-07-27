---
type: prd-module
project: CMF STUDIO
module_id: PRD-CMF-08
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_sections:
  - FR-CMF-09
  - FR-CMF-10
last_updated: 2026-06-22
---

# PRD-CMF-08 - Evaluation, Review, Publishing, Memory, and Operations

## Module Purpose

This module covers the final quality, review, release, learning, and operational health layer. CMF STUDIO releases assets only after evidence-backed evaluation, human approval, consent compatibility, publishing intent, and lineage preservation. It learns through memory only when claims are evidence-backed, reversible, and consent-compatible. Neo4j is a rebuildable relationship projection, not canonical business state.

## Product Requirements

### PR-CMF-08.01 Evaluation Receipts

The system can generate evaluation receipts for source truth, archetype fit, expression depth, identity consistency, likeness, composition, style, motion restraint, platform fit, negative space, micro-semiotic anchors, routeability, Voice DNA, Emotional DNA, and publishing readiness.

Primitives are the quality standard for evals. Evaluation registries must connect target selection, run commands, scoring rubrics, blockers, receipt output, and review read models.

### PR-CMF-08.02 Review Workbench

Operators can inspect source quote, transcript segment, route, Brand Context Version, selected assets, render output, evaluation receipt, consent state, revision history, provider receipts, and lineage graph before approving, rejecting, revising, or escalating.

### PR-CMF-08.03 Human Approval

Models and agents can recommend, but humans approve. Final approval is blocked when lineage, consent, source truth, identity, evaluation, format, platform, or content-format requirements fail.

Telegram quick approvals must show enough evidence to avoid blind rubber-stamping and deep-link to the exact PWA object for complex review.

### PR-CMF-08.04 Publishing Intent and Publer

Publishing Intent can be created only after approval, consent, lineage, platform variants, captions, and scheduling metadata are valid. Publer is an adapter for scheduling and status tracking. It is never the system of record for approval, caption truth, source state, or publishing authority.

### PR-CMF-08.05 Memory Admission

Brand Memory, Interviewer Memory, Route Memory, anchor memory, archetype survival memory, rejected-pattern memory, and publishing-performance memory can be admitted only with evidence, source references, provenance, consent compatibility, confidence, and admission receipts.

Operators can inspect, correct, reverse, expire, or quarantine memory admissions.

### PR-CMF-08.06 Neo4j Projection

Neo4j is allowed as a relationship projection over brand, guest, session, expression, archetype, asset, approval, publishing, provider, and memory relationships. It must rebuild from canonical events and cannot become the only source of truth for production decisions.

### PR-CMF-08.07 Operations and Recovery

Operators can inspect queue depth, active workers, render tier, provider status, failed jobs, retry state, workflow checkpoints, cost receipts, consent blockers, approval blockers, publish readiness, memory blockers, and recommended recovery actions.

The system can retry, resume, cancel, compensate, or quarantine provider jobs and workflows idempotently.

## Functional Requirements Covered

- FR-CMF-09.01 through FR-CMF-09.07.
- FR-CMF-10.01 through FR-CMF-10.07.

## Acceptance Gates

- Public publishing requires explicit human approval.
- Evaluation failure creates revision, blocker, quarantine, or rejection state rather than silent release.
- Publer failure updates Publishing Intent without duplicating schedules.
- Memory remains evidence-backed, reversible, and consent-aware.
- Neo4j outage cannot stop canonical workflows from using primary state.
