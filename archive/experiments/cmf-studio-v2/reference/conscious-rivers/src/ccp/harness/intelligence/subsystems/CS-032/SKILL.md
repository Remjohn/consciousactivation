# CS-032 Skill

## Purpose

Apply the Silence Container subsystem to guarantee a real low-noise receiving beat after major peaks so residual arousal has somewhere to land.

## Use This Skill When

- a timeline contains a CLS 4 beat
- a post-peak section still feels noisy or over-explained
- CS-008 reports no valid receiving vessel

## Required Inputs

- preceding beat CLS
- time since the peak beat
- soundtrack density
- dialogue density
- visual CLS of the candidate pause

## Decision Procedure

1. Detect whether a major peak has just occurred.
2. Check whether a low-CLS pause or silence container follows.
3. Confirm the receiving beat is quiet enough to function as a vessel.
4. Return a pause mandate, suggested placement, and duration guidance.

## Runtime Guidance

- Silence is a functional container, not empty runtime.
- If the composition keeps talking through the peak aftermath, the transfer mechanism breaks.
- Prefer a true pause over decorative low-volume noise.

## Escalate Or Block When

- no low-CLS container follows a peak that needs transfer
- the supposed pause still contains dense dialogue or visual clutter
- downstream edits remove the only receiving vessel