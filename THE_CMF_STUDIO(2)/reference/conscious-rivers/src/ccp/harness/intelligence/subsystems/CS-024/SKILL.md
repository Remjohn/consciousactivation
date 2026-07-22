# CS-024 Skill

## Purpose

Apply the Arousal-Pacing Gate so emotionally hot content is not cut so aggressively that it collapses into overload.

## Use This Skill When

- setting shot durations for high-stakes scenes
- regenerating a timeline after pace changes
- evaluating whether a peak beat should be slowed rather than accelerated

## Required Inputs

- scene arousal score or tag
- scene CLS
- shot-duration vector
- per-cut information density
- semantic burden of the beat

## Decision Procedure

1. Classify the beat as high-arousal or low-arousal.
2. Compare pacing against the allowed duration band for that arousal level.
3. Check whether cut density and informational density are multiplying overload.
4. Return `PASS`, `REVISE`, or `BLOCK` and specify whether the scene should slow down.

## Runtime Guidance

- Do not assume emotional intensity needs faster cutting.
- High-arousal beats usually need longer, cleaner holds.
- Low-arousal explanation can tolerate faster pacing if information density per cut stays low.

## Escalate Or Block When

- a high-arousal beat is cut inside a low-arousal duration band
- cut density is raised to create intensity instead of comprehension
- the pacing decision conflicts with CS-008 or CS-027