---
title: "TS-CMF-084 Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 1"
spec: "THE CMF STUDIO/docs/tech-specs/TS-CMF-084-transcript-beat-map-and-timeline-cue-compiler.md"
---

# TS-CMF-084 Build Receipt

Implemented transcript beat-map compilation through `SourceTimestampRange`, `CompositionBeat`, `TimelineCue`, `CompositionBeatMap`, `BeatMapCompilationReceipt`, and `compile_beat_map`. Timing validation blocks reversed cue ranges and emits cue refs for renderer manifests.

Verification: `test_batch1_reaction_renderer_uses_upper_reaction_ui_lower_human_cutouts_and_transcript_timing`.

