# CS-008 Skill

## Purpose

Apply the Excitation Transfer Timer to validate whether a high-intensity beat is followed by the right low-intensity beat soon enough for residual arousal to become feeling instead of noise.

## Use This Skill When

- sequencing beats after a TURNING_POINT or any CLS 4 event
- deciding whether to insert a pause or vulnerability container
- validating regeneration patches that alter post-peak timing

## Required Inputs

- ordered CLS timeline
- beat timestamps and durations
- scene sequence metadata
- arousal tags for adjacent beats

## Decision Procedure

1. Detect whether a peak beat reached CLS 4.
2. Measure time to the next low-intensity beat.
3. Confirm the follow-up beat drops to CLS 1 or 2.
4. Reject immediate CLS 4 to CLS 4 transitions.
5. Return `PASS`, `FAIL`, or `BLOCK` with the measured transfer window.

## Runtime Guidance

- The quiet beat after the storm is functional, not decorative.
- If no low-intensity vessel exists, route toward CS-032.
- Use this subsystem before polishing transitions or adding more intensity.

## Escalate Or Block When

- no low-CLS beat appears inside the 2 to 5 second window
- a CLS 4 is followed by another CLS 4
- the follow-up beat is too delayed and the charge has already decayed