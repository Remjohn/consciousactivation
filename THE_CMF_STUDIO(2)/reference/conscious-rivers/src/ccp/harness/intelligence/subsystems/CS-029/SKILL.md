# CS-029 Skill

## Purpose

Apply the ISC Quality Scorer to estimate whether the full composition is likely to synchronize audience attention strongly enough to justify publish or commit.

## Use This Skill When

- reviewing a composed scene set before render
- deciding whether a regeneration improved the whole piece or only a local detail
- ranking residual risks after all local subsystem checks have run

## Required Inputs

- outputs from active subsystems
- arc metadata
- focal continuity and structural compliance scores
- retention and pacing signals

## Decision Procedure

1. Aggregate the outputs of the currently active subsystems.
2. Convert them into a composite synchrony-quality score.
3. Identify the weakest contributing dimensions.
4. Return a final score and publish or revise recommendation.

## Runtime Guidance

- Treat this as the global quality north star, not a replacement for local checks.
- A good local color or timing decision does not guarantee strong whole-sequence synchrony.
- Use CS-029 late in the pipeline when enough subsystem outputs exist to score the whole composition.