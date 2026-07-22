---
type: prd-module
project: CMF STUDIO
module_id: PRD-CMF-09
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_sections:
  - Non-Functional Requirements
last_updated: 2026-06-22
---

# PRD-CMF-09 - Non-Functional Requirements

## Module Purpose

This module consolidates the non-functional requirements from the current PRD so architecture, stories, specs, evals, and implementation can test the same operational standard.

## Performance and Operator Responsiveness

- NFR1: Non-render PWA actions for active brand workspaces complete within 2 seconds at p95 when no external provider call is required.
- NFR2: Operator dashboards show current queue, approval, consent, render, and publishing state within 4 seconds at p95 for an active brand workspace.
- NFR3: Telegram approval, rejection, preview, and status commands acknowledge within 3 seconds at p95 when accepted for async execution.
- NFR4: Transcription, provider generation, rendering, evaluation, and publishing run asynchronously.
- NFR5: Render previews are available in compressed review form before final publishable exports when supported.
- NFR6: Transcript, source playback, timestamp, Expression Moment, route, and evaluation context remain usable without forcing full media reprocessing.

## Reliability and Workflow Recovery

- NFR7: Every state-changing command is idempotent and produces a domain event or recorded failure.
- NFR8: Complete Expression Session, Complete Editing Session, Brand Genesis, provider job, render, approval, publishing, and memory workflows survive restarts.
- NFR9: Source artifacts, locked Brand Context Versions, approved Expression Moments, provider receipts, evaluation receipts, approval events, and publishing results are immutable after completion.
- NFR10: Provider failures support retry, fallback, terminal failure, or manual review.
- NFR11: Batch GPU jobs checkpoint per asset.
- NFR12: Recovery from provider outage, renderer failure, queue interruption, and object-storage retry does not require direct database edits.

## Security, Privacy, and Consent

- NFR13: Brand data is isolated by organization and brand scope across storage, commands, events, provider jobs, receipts, memory, and projections.
- NFR14: Source recordings, transcripts, likeness assets, voice assets, provider tokens, and publishing credentials are encrypted at rest and in transit.
- NFR15: Asset access uses scoped, short-lived access and does not expose private assets publicly by default.
- NFR16: Consent policy is evaluated before recording use, provider processing, likeness generation, Voice-DNA Boost, memory admission, publishing intent, and Publer scheduling.
- NFR17: High-impact commands require permission and confirmation according to role, object state, consent, cost, and publishing policy.
- NFR18: Pi, DSPy, Telegram, and UI surfaces cannot bypass Command Bus, consent checks, approval checks, or audit logging.

## Scalability and Resource Governance

- NFR19: The system scales by brand, queue, worker profile, provider capability, and resource budget.
- NFR20: Capacity constraints degrade by concurrency, queue priority, render tier, or brand throughput, not by bypassing workflow obligations.
- NFR21: GPU workers operate batch-first: start for queued work, process typed jobs, checkpoint outputs, write receipts, report cost, upload artifacts, and shut down.
- NFR22: Provider and render jobs carry cost policy, retry policy, timeout policy, and idempotency keys.
- NFR23: Operators can inspect queue depth, blockers, active workers, failed jobs, estimated cost, and render tier.
- NFR24: Object storage and projections support rebuild from contracts, events, receipts, and immutable artifacts.

## Integration and Provider Interoperability

- NFR25: External integrations use capability contracts, not direct domain-level SDK calls.
- NFR26: Provider receipts include provider identity, model or workflow version, parameters, source hashes, output hashes, cost, status, and failure details.
- NFR27: Ideogram 4 preserves `CompositionJob` JSON, prompt hash, composition plate URI, composition analysis, and downstream usage state.
- NFR28: GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, self-hosted ComfyUI Docker workers, LavaSR, MOSS-TTS, Remotion, Motion Canvas, Telegram, transcript providers, and Publer remain replaceable behind contracts.
- NFR29: Publer never owns canonical approval, caption truth, publishing authority, or asset lineage.
- NFR30: Integration failure returns actionable status and avoids duplicate publishing, duplicate provider jobs, or orphaned outputs.

## Observability, Auditability, and Reproducibility

- NFR31: Every production output traces from source recording and transcript through Interview Asset Contract, Expression Moment, route, Asset Package Spec, Complete Editing Session, SceneSpec, provider jobs, render output, evaluation receipt, approval event, and Publishing Intent.
- NFR32: Every command, workflow transition, provider job, approval action, publishing action, migration action, and memory admission creates audit records.
- NFR33: Render reproducibility preserves Brand Context Version, registry bundle version, source hashes, SceneSpec, composition lineage, provider metadata, selected assets, text plan, renderer route, and evaluation receipts.
- NFR34: Legacy migration decisions retain source path, semantic changes, fixture targets, evaluation targets, reviewer, status, and content hash.
- NFR35: Neo4j rebuilds from canonical events and state, and projection failure does not mutate canonical business truth.
- NFR36: Observability exposes correlation IDs across PWA, Telegram, Agent Gateway, workflows, provider jobs, renderers, storage, Publer, and memory.

## Accessibility and Operator Usability

- NFR37: PWA review surfaces support keyboard-accessible review, approval, rejection, revision, and publishing confirmation.
- NFR38: Evaluation receipts are readable human review artifacts.
- NFR39: Media review includes captions or transcript context when audio/video is evaluated.
- NFR40: Telegram previews link to exact PWA object state for deeper review.
- NFR41: Operator screens distinguish source truth, generated proposal, approved state, failed state, and publish-ready state.
- NFR42: Operators do not need raw infrastructure logs for normal queue, provider, render, consent, or approval decisions.

## Maintainability and Contract Governance

- NFR43: Pydantic models are semantic contract authority for domain objects, commands, events, workflows, provider jobs, render contracts, and receipts.
- NFR44: TypeScript consumers are generated from authoritative contracts and do not define shadow domain semantics.
- NFR45: Registry entries validate at boot, reject missing cross-references, and require evaluation rubrics before becoming active.
- NFR46: Direct imports from legacy runtime into production packages are blocked unless an explicit exception ADR is approved.
- NFR47: Changes to DSPy signatures, optimizer artifacts, thresholds, output models, or registry schemas create versioned artifacts.
- NFR48: Pull requests affecting production behavior include requirement linkage, contract impact, tests, migration notes, observability, security/brand-scope review, and rollback notes.
