# Behavioral Anchors — Primitive Alignment Editor

## Core Principles

1. **Primitive-Grounded Prose:** Every psychological pressure and participant stance statement must cite specific primitive IDs (`PRM-HUM-009`, `PRM-BUS-001`, etc.) and align with the primitive's governed `core_move`.

2. **Noun-Stripping Discipline:** Reference specimens are source material, not harness invariants. Proper nouns, named individuals, brand names, and episode-specific details must be replaced with generic descriptions ("the reference specimen").

3. **Pairwise Conflict Resolution:** When multiple candidate primitives match a harness's prose, their YAML snapshots must be checked for `conflicts_with` entries. If candidate A conflicts with candidate B, drop the lower-fit candidate. Never cite conflicting primitives together.

4. **Option B Lock Partitioning:** Spatial layout rules (`text_block`, `hero_zone`, `z_index`, `non_overlap`) belong in `wrong_reading_locks` (handled by `visual_syntax_composition_compiler`). Psychological traps and identity boundaries belong in `wrong_reading_locks_meaning` (handled by this Skill).

5. **Audit Receipt Integrity:** Every alignment run produces a deterministic alignment receipt recording SHA256 checksum verifications, dropped conflict pairs, and prose diffs.
