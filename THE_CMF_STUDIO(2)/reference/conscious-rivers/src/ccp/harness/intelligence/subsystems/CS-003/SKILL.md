# CS-003 Skill

## Purpose

Apply Gaze Direction Transfer so the face either bonds with the viewer or routes the viewer into the overlay, instead of competing with it.

## Use This Skill When

- placing captions beside a face
- aligning proof graphics with a coach shot
- deciding whether a moment needs direct gaze or averted gaze

## Required Inputs

- eye-line vector
- overlay coordinates
- scene intent
- text density
- graphic entry timing

## Decision Procedure

1. Identify whether the scene is bonding or instructional.
2. Compare gaze direction to overlay placement.
3. Reject layouts where the face and graphic ask for attention at the same time.

## Runtime Guidance

- Use direct gaze for vulnerability and connection.
- Use averted gaze when the face should hand attention to a graphic.
- Dense instructional text should not fight a full-intensity talking head.