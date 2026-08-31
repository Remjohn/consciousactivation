---
name: visual_requirement_extractor
description: Passive flat skill for extracting structured visual obligations, somatic effects, and recognition targets from verified spoken evidence.
version: 1.0.0
lane: HUNTER
---

# Visual Requirement Extractor Skill

## Role & Invariants
- Operates strictly under the **HUNTER** lane.
- Ingests verified `SemanticProgram` scenes and spoken evidence turns.
- Extracts visual subjects, recognition targets, viewer state transitions, and somatic obligations.
- Ensures all requirements retain exact segment and turn SHA-256 back-pointers.
- Passive and flat: invokes no sub-skills or downstream services.
