---
title: Authority Conformance
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# Authority Conformance

These cases prove field and action sovereignty. Each rejected case must:

1. return an `authority_failure`;
2. preserve lifecycle state;
3. create a rejection audit receipt;
4. start no downstream production.

`AUTH-CONSTITUTION-001` applies those rules to recognition intent, viewer role,
stance, and the Visual Narrative Program. A VAE-authored mutation must return
`AUTHORITY_DENIED`, preserve the current state, and name the attempted paths in
the rejection audit evidence.
