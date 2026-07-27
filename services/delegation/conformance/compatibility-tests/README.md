---
title: Compatibility Conformance
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# Compatibility Conformance

Compatibility cases assert preservation of required meaning, authority, lifecycle, category profile, evaluation and failure behavior. Parsing success alone is not a passing condition.

Every adapter or migration case must compare source and target authority-bearing fields.

For Visual Asset Demand `1.1`, compatibility requires explicit per-domain
preservation and enforcement plus evaluator-profile evidence wherever
evaluation is mandatory. Parse-only claims, missing evaluator evidence, and
any adapter that drops Expression Moment lineage or weakens wrong-reading
locks are `INCOMPATIBLE`.
