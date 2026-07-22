# CS-015 Skill

## Purpose

Apply the Shot Duration Enforcer so shots remain on screen long enough to support inference instead of only being seen.

## Use This Skill When

- auditing rapid montage sequences
- validating reaction inserts
- deciding whether a beat can carry meaning at its current duration

## Required Inputs

- shot length
- prior context duration
- shot role
- semantic complexity
- shot scale

## Decision Procedure

1. Determine whether the shot must introduce meaning or only energize tempo.
2. Compare duration against the inference floor for the given context.
3. Extend or serialize shots that are too brief for their semantic load.

## Runtime Guidance

- Ultra-short cuts are tools, not defaults.
- Faster is not automatically more modern.
- If the viewer cannot infer the beat, hold longer.