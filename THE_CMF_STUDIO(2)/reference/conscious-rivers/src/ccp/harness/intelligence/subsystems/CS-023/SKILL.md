# CS-023 Skill

## Purpose

Apply the Rhythm Generator so default shot timing feels organic and 1/f-like instead of robotic or random.

## Use This Skill When

- generating default beat timing maps
- setting ASL patterns for Scene Builder
- balancing burst clusters with reset spaces

## Required Inputs

- runtime
- target ASL
- BPM range
- scene sequence
- pacing constraints

## Decision Procedure

1. Generate a duration pattern with local bursts and longer-range variation.
2. Keep the distribution natural instead of metronomic.
3. Hand the rhythm field to downstream pacing and duration gates for refinement.

## Runtime Guidance

- Rhythm should feel alive, not mechanical.
- Use it as a baseline field, not as an isolated law.
- Let arousal and duration constraints modulate the generated pattern.