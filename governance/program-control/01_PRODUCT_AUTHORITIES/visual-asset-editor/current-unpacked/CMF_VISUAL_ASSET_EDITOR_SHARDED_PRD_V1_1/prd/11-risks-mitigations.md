---
title: Risks and Mitigations
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
risk_count: 14
---

# Risks and Mitigations

### R-01 — Semantic drift during production

**Risk:** A model or workflow changes meaning while producing a visually attractive asset.

**Mitigation:** Typed demand authority, protected bindings, independent VLM hard gates, amendment flow.

### R-02 — Evaluator overconfidence or bias

**Risk:** The VLM approves wrong actions or rejects valid recurrence.

**Mitigation:** Labeled evaluator benchmarks, calibration, secondary evaluation on uncertainty, shadow promotion.

### R-03 — ComfyUI/custom-node drift

**Risk:** Mutable dependencies break reproducibility or production consistency.

**Mitigation:** Digest-pinned containers, node lockfiles, capability registry, local/cloud parity tests.

### R-04 — GPU cost explosion

**Risk:** High candidate counts, video models, or repairs exceed value.

**Mitigation:** Budget Programs, estimates, hard ceilings, adaptive early stop, cost-per-accepted-asset analytics.

### R-05 — False memory relevance

**Risk:** Semantic search retrieves attractive but incompatible knowledge.

**Mitigation:** Authority filters, typed graph, compatibility, syntax fingerprints, VLM reranking, contradiction coverage.

### R-06 — Skill/memory sediment

**Risk:** Steering knowledge grows noisy and contradictory.

**Mitigation:** CMF-OKF lifecycle, supersession, indexes, maturity, validity windows, retrieval evaluation.

### R-07 — Capability sprawl

**Risk:** Too many LoRAs, models, workflows, and adapters fragment routing.

**Mitigation:** Capability-gap threshold, control comparison, expected reuse, registry deduplication, deprecation.

### R-08 — Reference-slice overfitting

**Risk:** The product works only for Format 02.

**Mitigation:** Provider-neutral IR, structurally represented families, transfer benchmarks, later family certification.

### R-09 — Architecture collision

**Risk:** Editor design rewrites the validated Builder or Content Harness authority.

**Mitigation:** Architecture Preservation Contract, upstream amendment route, readiness prohibition tests.

### R-10 — Manual-operation creep

**Risk:** Operators become permanent ComfyUI technicians.

**Mitigation:** Autonomous workflow, policy-first console, exception-only human states, no-routine-manual-work metric.

### R-11 — Visual repetition misclassification

**Risk:** Continuity is rejected or repeated visual arguments are missed.

**Mitigation:** Rendered syntax usage receipts, VLM recurrence labels, protected recurrence benchmarks.

### R-12 — Repair-induced drift

**Risk:** A local repair changes identity, geometry, or semantic properties that were already correct.

**Mitigation:** Typed preserve lists, causal binding changes, before/after evaluation, selective invalidation.

### R-13 — Public contract instability

**Risk:** Independent releases break Content Harness callers.

**Mitigation:** Semantic versions, compatibility manifest, representative fixtures, separate Delegation PRD, rollback.

### R-14 — OKF authority confusion

**Risk:** Readable knowledge files become treated as transactional truth.

**Mitigation:** Explicit projection-only doctrine, canonical resource URIs, hashes, typed store precedence, validator checks.
