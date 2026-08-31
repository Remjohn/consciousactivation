---
name: knowledge_candidate_extractor
description: Passive flat skill for extracting structured knowledge candidates from immutable research sources with source SHA-256 provenance.
version: 1.0.0
lane: HUNTER
---

# Knowledge Candidate Extractor Skill

## Role & Invariants
- Operates strictly under the **HUNTER** lane.
- Ingests verified research sources (`ResearchSourceRecord`, `RawObservation`).
- Extracts entities, concepts, and claims without modifying source content.
- Ensures all candidates retain `source_id` and exact `source_sha256` back-pointers.
- Passive and flat: invokes no sub-skills or downstream services.
