---
name: video_edl_compiler
description: Compiles word boundary EDLs and VideoEditPrograms with primary A-roll spines.
version: 1.0.0
lane: COMPOSER
---

# Video EDL Compiler Skill

## Role
Passive, flat skill executed within the `COMPOSER` authority lane.
Compiles `WordBoundaryEdl`, constructs `VideoEditProgram` tracks, binds export specifications (Remotion, HyperFrames), and triggers physical FFmpeg source-led rendering passes.

## Invariants
- Enforces strict word boundary alignments and tail protections.
- Preserves mandatory `PRIMARY_A_ROLL_SPINE` track structure.
- No sub-skill execution.
