---
title: "TS-CMF-074 Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 1"
spec: "THE CMF STUDIO/docs/tech-specs/TS-CMF-074-reaction-clip-renderer-and-background-removal-compositing.md"
---

# TS-CMF-074 Build Receipt

Implemented deterministic reaction renderer props through `SubjectCutoutLayer`, `ReactionClipRendererProps`, `ReactionClipRenderManifest`, and `CompositionRuntimeService.compile_reaction_renderer_manifest`. The default manifest uses an upper reaction UI zone and lower background-removed human cutout zone with beat cue refs and caption/audio policy.

Verification: `test_batch1_reaction_renderer_uses_upper_reaction_ui_lower_human_cutouts_and_transcript_timing`.

