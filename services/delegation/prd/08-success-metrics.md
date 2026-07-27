---
title: Success Metrics and Counter-Metrics
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---


# 8. Success Metrics and Counter-Metrics

## SM-01 — Valid submission acceptance

**Definition:** Share of valid, compatible, authorized submissions accepted without manual intervention.

**Target:** >= 99.5%

**Validates:** `FR-001`, `FR-017`, `FR-113`

## SM-02 — Unauthorized mutation rejection

**Definition:** Recall for attempts to change fields outside the sender's authority.

**Target:** 100% in conformance suite

**Validates:** `FR-009`, `FR-014`, `FR-106`

## SM-03 — Duplicate production prevention

**Definition:** Rate at which duplicate or replayed submissions avoid starting duplicate VAE executions.

**Target:** 100%

**Validates:** `FR-022`, `FR-109`, `FR-124`

## SM-04 — Lifecycle transition validity

**Definition:** Accepted shared transitions conforming to the lifecycle machine.

**Target:** 100%

**Validates:** `FR-027`, `FR-030`, `FR-119`

## SM-05 — Automatic result acknowledgement

**Definition:** Eligible RESULT_READY messages acknowledged automatically within the SLO.

**Target:** >= 99%

**Validates:** `FR-043`, `FR-046`, `FR-120`

## SM-06 — Selective reuse precision

**Definition:** Preserved artifacts later confirmed valid after supersession or repair.

**Target:** >= 98%

**Validates:** `FR-036`, `FR-038`

## SM-07 — Stale result prevention

**Definition:** Superseded, cancelled, invalidated, or incompatible results entering current composition.

**Target:** 0

**Validates:** `FR-037`, `FR-062`, `FR-045`

## SM-08 — Compatibility truthfulness

**Definition:** Declared compatibility paths that pass semantic conformance fixtures.

**Target:** 100%

**Validates:** `FR-081`, `FR-088`, `FR-121`

## SM-09 — Audit completeness

**Definition:** State-changing messages with complete chained audit receipts.

**Target:** 100%

**Validates:** `FR-006`, `FR-110`, `FR-118`

## SM-10 — Cancellation response

**Definition:** Time from accepted cancellation to blocking new work and producing disposition receipt.

**Target:** p99 <= 10 seconds for boundary actions

**Validates:** `FR-058`, `FR-064`

## SM-11 — Critical notice propagation

**Definition:** Time to project critical revocation/invalidation to affected active consumers.

**Target:** p99 <= 10 seconds

**Validates:** `FR-099`, `FR-103`, `FR-116`

## SM-12 — Format 02 conformance

**Definition:** Mandatory reference scenarios passing for the pinned product/protocol versions.

**Target:** 100% before production certification

**Validates:** `FR-120`, `FR-126`

## SM-C1 — Message count *(counter-metric)*

Do not optimize for generating more messages; prefer the minimum complete auditable exchange.

**Counterbalances:** SM-01, SM-04

## SM-C2 — Adapter usage *(counter-metric)*

Do not optimize for high adapter use; direct compatible contracts are preferable.

**Counterbalances:** SM-08

## SM-C3 — Protocol-owned decisions *(counter-metric)*

Do not optimize for more decisions inside the protocol; creative and production authority must remain in products.

**Counterbalances:** SM-02
