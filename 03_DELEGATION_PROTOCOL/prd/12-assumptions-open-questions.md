---
title: Assumptions and Open Questions
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---


# 12. Assumptions and Open Questions

- **A-01** `accepted` — The validated Builder and Visual Asset Editor PRDs remain authoritative upstream architecture sources. Owner: `product governance`.

- **A-02** `accepted` — The first production cross-product reference slice is Format 02 Minimal Coach Theatre. Owner: `Release 1`.

- **A-03** `architecture_required` — The Content Harness and VAE will have independently authenticated product identities. Owner: `security architecture`.

- **A-04** `architecture_required` — Large assets and canonical contracts will reside in governed storage reachable through stable references and hashes. Owner: `data architecture`.

- **A-05** `accepted` — The shared protocol may use HTTP, queues, event streams, or local fixtures without changing semantics. Owner: `protocol architecture`.

- **A-06** `accepted` — Final public schemas from the VAE PRD remain provisional until this protocol package validates them. Owner: `delegation product`.

- **A-07** `open_non_blocking` — Exact SLO thresholds will be tuned in Architecture and benchmark phases. Owner: `operations`.

- **A-08** `accepted` — Cryptographic algorithms and key-management implementation remain Architecture decisions, while identity/integrity behavior is a product requirement. Owner: `security architecture`.

- **A-09** `accepted` — Published media cannot be silently rewritten by protocol invalidation or replacement. Owner: `Content Harness`.

- **A-10** `implementation_gate` — A complete shared conformance suite will be executable by both reference product implementations before authorization. Owner: `cross-product engineering`.

## Architecture-phase open questions

1. Which transport combination is canonical for Release 1: direct HTTP plus event bus, or queue-first?
2. Which signature algorithm, trust root, credential store and rotation interval will be used?
3. Which durable audit/event store guarantees append order and recovery?
4. How are stable resource URIs authorized and resolved across local and cloud environments?
5. What exact p95/p99 SLOs are realistic after the Format 02 compute proof?
6. Which fields are mandatory in protocol `1.0` versus reserved for `1.1`?
7. Which composition runtime principal owns automatic result acknowledgement in Release 1?
