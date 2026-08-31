---
name: search_index_builder
description: Passive flat skill for compiling lexical search tokens, exact match terms, and dense embedding adapter candidate payloads.
version: 1.0.0
lane: ANALYST
---

# Search Index Builder Skill

## Role & Invariants
- Operates strictly under the **ANALYST** lane.
- Extracts token sets, exact matching terms, categories, and tags from canonical knowledge nodes.
- Normalizes token distributions and computes integer basis points representations (`_micros`).
- Formats candidate payloads for optional advisory dense embedding adapters while strictly preserving authority-first filtering.
- Passive and flat: invokes no sub-skills or downstream services.
