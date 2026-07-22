# CS-022 Skill

## Purpose

Apply the AV Sync Enforcer so audio and visual events stay inside the allowed synchrony band and are perceived as one event instead of two competing signals.

## Use This Skill When

- timing proof cards, impact cuts, captions, and gesture accents
- reviewing regenerated visuals against existing audio timing
- validating cut rhythm against sound events before commit

## Required Inputs

- audio onset timestamps
- visual onset timestamps
- event type
- timing offsets

## Decision Procedure

1. Measure the offset between the audio and visual event.
2. Compare it against the allowed synchrony band.
3. Return `PASS`, `REVISE`, or `BLOCK` plus the correction amount.

## Runtime Guidance

- Treat sync drift as a memory and polish issue, not only as a post detail.
- Use tighter correction on speech-linked events than decorative motion.
- If timing broke after regeneration, do not commit until it is re-aligned.