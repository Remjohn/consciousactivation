---
name: derivative_source_extractor
description: Extracts multi-modal source spans and verbatim evidence anchors for visual derivatives.
version: 1.0.0
lane: HUNTER
---

# Derivative Source Extractor Skill

## Role
Passive, flat skill executed within the `HUNTER` authority lane.
Extracts verbatim audio/text snippets, speaker metadata, and timing boundaries from authentic evidence recordings.

## Invariants
- Operates strictly on authentic evidence segments.
- Computes canonical SHA-256 digests of all extracted quotes.
- No sub-skill execution.
