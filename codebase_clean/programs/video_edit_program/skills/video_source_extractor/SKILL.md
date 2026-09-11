---
name: video_source_extractor
description: Registers source media and extracts verbatim word boundaries and evidence spans for video editing.
version: 1.0.0
lane: HUNTER
---

# Video Source Extractor Skill

## Role
Passive, flat skill executed within the `HUNTER` authority lane.
Registers physical source media, extracts verbatim audio and word boundary timings, and verifies evidence hashes.

## Invariants
- Operates strictly on authentic evidence segments.
- Validates cryptographic SHA-256 digests of all spoken quotes.
- No sub-skill execution.
