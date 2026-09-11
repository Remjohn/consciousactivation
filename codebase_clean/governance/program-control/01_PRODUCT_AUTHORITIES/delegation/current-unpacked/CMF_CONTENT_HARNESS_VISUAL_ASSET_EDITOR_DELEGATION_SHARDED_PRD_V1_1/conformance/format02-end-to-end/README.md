---
title: Format 02 End-to-End Conformance
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# Format 02 End-to-End Conformance

The suite executes the ten scenarios in `../../reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/SCENARIO_MANIFEST.yaml`.

A certified run must prove:

- contract and envelope conformance;
- signed principal authority;
- pinned compatibility negotiation;
- correct shared-state projection;
- complete audit chain;
- exact demand and asset versions;
- safe supersession, amendment, budget and cancellation behavior;
- production acceptance followed by current consumption acknowledgement;
- immutable post-completion invalidation and replacement;
- no duplicate VAE production under replay or transport retry;
- downstream composition reference to the exact acknowledged asset version.
