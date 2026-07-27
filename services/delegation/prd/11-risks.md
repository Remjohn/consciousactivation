---
title: Risk Register
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---


# 11. Risks and Mitigations

| Risk | Failure mode | Primary mitigation |
|---|---|---|

| Authority leakage | A boundary service gradually starts making semantic or production choices. | Executable Authority Matrix, prohibited-action tests, preservation gate. |

| Contract sprawl | Many message variants become difficult to understand or maintain. | Single-purpose registry, version discipline, deprecation and conformance. |

| Lifecycle divergence | Projection, product state and audit history disagree. | Event-sourced reconstruction tests and projection freshness SLO. |

| False compatibility | Consumers parse messages but fail to enforce required behavior. | Semantic negotiation and feature-level conformance. |

| Stale result consumption | Late results enter a newer sequence or composition. | Version/hash acknowledgement, supersession and invalidation gates. |

| Duplicate production | Retry or replay starts multiple expensive VAE runs. | Idempotency, nonce/replay controls and durable submission receipts. |

| Cancellation corruption | Hard stops damage artifacts or permit stale promotion. | Nearest-safe-checkpoint policy and disposition receipt. |

| Audit gaps | State changes occur while audit storage is unavailable. | Fail-safe acceptance gate and chained receipts. |

| Excessive protocol coupling | Internal VAE nodes leak into the public lifecycle. | Stable projection layer and privacy boundary. |

| Migration drift | Adapters or migrations drop authority-bearing information. | Lossless transformation rules, equivalence fixtures and owner review. |

| Operational overload | Too many events or controls make the boundary expensive. | Minimum Complete Contract, references for large payloads, SLO tuning. |

| Premature certification | A happy-path demo is mistaken for production readiness. | Format 02 scenario portfolio, resilience and authority suites. |
