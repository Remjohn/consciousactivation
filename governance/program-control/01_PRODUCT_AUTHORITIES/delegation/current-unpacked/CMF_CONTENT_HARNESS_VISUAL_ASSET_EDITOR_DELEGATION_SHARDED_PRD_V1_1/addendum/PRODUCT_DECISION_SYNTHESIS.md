---
title: Product Decision Synthesis
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: reference
created: '2026-07-13'
updated: '2026-07-13'
---

# Product Decision Synthesis

The 16 decisions form one coherent boundary architecture:

```text
Immutable Content Harness-owned Visual Asset Demand
→ signed Delegation Envelope
→ deterministic boundary validation
→ semantic compatibility negotiation
→ VAE production acceptance
→ Content Harness consumption acknowledgement
```

Cross-cutting exchanges handle supersession, amendment, budgets, cancellation, multi-asset sets, failures, migration and post-completion governance. Every exchange remains immutable, authority-scoped and auditable.

## Why this is not a third orchestrator

The protocol routes and validates product-authored messages. It does not choose visual concepts, production methods, candidates, composition layouts or sequence behavior.

## Why a contract package alone is insufficient

Production correctness requires lifecycle enforcement, authority validation, idempotency, compatibility, audit, cancellation, supersession and post-completion impact—not merely matching JSON shapes.
