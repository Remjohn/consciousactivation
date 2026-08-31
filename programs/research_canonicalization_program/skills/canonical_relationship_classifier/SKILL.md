---
name: canonical_relationship_classifier
description: Passive flat skill for classifying semantic relationships, resolving aliases, and guarding against false merges.
version: 1.0.0
lane: ANALYST
---

# Canonical Relationship Classifier Skill

## Role & Invariants
- Operates strictly under the **ANALYST** lane.
- Classifies candidate relationships into `SAME`, `RELATED`, `SUBTYPE`, `SUPERTYPE`, `CONTRADICTORY`, and `DISTINCT`.
- Resolves aliases into unified canonical clusters while strictly preventing false merges of distinct homonyms.
- Flags contradiction edges for operator adjudication.
- Computes deterministic SHA-256 lineage back-pointers to immutable source evidence.
- Passive and flat: invokes no sub-skills or downstream services.
