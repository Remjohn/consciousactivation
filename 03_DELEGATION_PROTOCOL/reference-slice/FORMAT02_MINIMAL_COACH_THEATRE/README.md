---
title: Format 02 Delegation Reference Slice
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# Format 02 — Minimal Coach Theatre Delegation Reference Slice

This reference slice is the first mandatory cross-product conformance target for the Delegation Protocol.

The aligned slice pins envelope protocol `1.0`, Visual Asset Demand message
`1.1`, and package candidate `1.1.0-rc.1`. Its compatibility proof requires
behavioral preservation/enforcement and evaluator evidence; parsing the new
fields is not sufficient.

## Why Format 02

Minimal Coach Theatre exercises the complete shared boundary:

- a Content Harness owns Activative meaning, scene role and composition intent;
- the VAE owns 2D character identity, pose, expression, gesture, gaze and scene production;
- multiple assets may share character, environment, palette, lighting and interaction geometry;
- assets must remain compatible with a 9:16 Remotion composition and deterministic text;
- character recurrence is often beneficial continuity rather than fatigue;
- asset results may need amendments, supersession, repair, acknowledgement, invalidation and replacement.

## Required scenario portfolio

| Scenario | Product proof |
|---|---|
| SCN-01 | Single-asset happy path |
| SCN-02 | Atomic multi-asset Delegation Set |
| SCN-03 | Supersession and selective invalidation |
| SCN-04 | Budget escalation |
| SCN-05 | Constraint conflict and amendment |
| SCN-06 | Safe cancellation |
| SCN-07 | Post-completion invalidation and replacement |
| SCN-08 | Authority violation |
| SCN-09 | Compatibility migration |
| SCN-10 | Replay and out-of-order resilience |

SCN-08 proves Content Harness semantic authority. SCN-09 proves the immutable,
owner-evidenced V1-to-V1.1 demand migration. SCN-10 proves Activative
Intelligence Pack, Reaction Receipt, and Expression Moment lineage remains
unchanged across retry and replay handling.

## Release rule

These fixtures are PRD-level examples. Architecture must bind them to executable producers, consumers, signing, event transport, audit storage and Control Tower projections before implementation authorization.
