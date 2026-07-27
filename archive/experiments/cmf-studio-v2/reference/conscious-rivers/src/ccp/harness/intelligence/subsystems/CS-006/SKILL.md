# CS-006 Skill

## Purpose

Apply the Gaze Continuity Checker so cuts preserve attentional momentum instead of forcing the viewer to reorient from scratch.

## Use This Skill When

- cutting between A-roll and B-roll
- evaluating reframes across adjacent shots
- checking whether an incoming shot lands near the outgoing focal point

## Required Inputs

- outgoing focal coordinates
- incoming focal coordinates
- cut type
- motion direction
- shot scale delta

## Decision Procedure

1. Measure focal shift across the cut.
2. Decide whether the jump is justified by a strong reorientation cue.
3. Revise layouts that make the cut itself more salient than the message.

## Runtime Guidance

- Good continuity reduces search after the cut.
- Allow large jumps only when a reorientation cue is explicit.
- A-roll to B-roll swaps should preserve attention, not reset it.