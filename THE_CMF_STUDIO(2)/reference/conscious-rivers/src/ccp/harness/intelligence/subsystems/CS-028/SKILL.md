# CS-028 Skill

## Purpose

Apply the Element Counter so the frame does not exceed mobile working-memory capacity with too many simultaneous meaningful elements.

## Use This Skill When

- auditing overlays in dense teaching scenes
- stacking face, text, icons, and product cues
- deciding whether information should be serialized instead of layered

## Required Inputs

- per-frame meaningful element count
- semantic weights
- redundancy map

## Decision Procedure

1. Count how many meaningful items are active in the frame.
2. Remove or sequence lower-priority elements when the cap is exceeded.
3. Preserve one dominant look target, one read target, and optional support.

## Runtime Guidance

- Helpful overlays can still overload the frame.
- Sequence information across cuts when needed.
- Three meaningful elements is usually the hard edge on mobile.