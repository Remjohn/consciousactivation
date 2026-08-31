---
name: asset_annotation_curator
description: Passive flat skill for cataloging media assets, classifying editorial insert roles, and validating rights clearance with SHA-256 integrity.
version: 1.0.0
lane: ANALYST
---

# Asset Annotation Curator Skill

## Role & Invariants
- Operates strictly under the **ANALYST** lane.
- Catalogs primary evidence visual assets and E/D-roll editorial inserts.
- Classifies semantic insert roles (`SEMANTIC_SIMILE`, `PATTERN_MATCH`, `PATTERN_INTERRUPT`, etc.).
- Enforces strict rights verification (`CLEARED_COMMERCIAL`, `PUBLIC_DOMAIN`, etc.) and SHA-256 checksum checks.
- Passive and flat: invokes no sub-skills or downstream services.
