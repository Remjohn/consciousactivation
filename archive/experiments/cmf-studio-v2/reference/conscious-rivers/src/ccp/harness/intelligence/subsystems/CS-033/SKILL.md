# CS-033 Skill

## Purpose

Apply the Prediction Error Gate subsystem to keep surprise strong enough to capture attention without letting novelty destroy legibility.

## Use This Skill When

- a hook, contrast beat, or turning point feels flat or too expected
- a regeneration patch improved polish but removed the surprise event
- a sequence is visually novel yet harder to understand

## Required Inputs

- container prediction error budget
- component prediction error profile
- schema familiarity score
- reveal timing in milliseconds
- legibility loss introduced by the surprise move

## Decision Procedure

1. Read the active container's target and max prediction error budget.
2. Estimate how strongly the selected component violates or refreshes viewer expectation.
3. Check whether the surprise lands in the right window and remains legible.
4. Return a verdict plus amplification or softening guidance.

## Runtime Guidance

- Prediction error is only useful when the viewer can still resolve meaning.
- Hooks and turning points can spend more surprise budget than setup or resolution beats.
- If surprise forces explanation delay beyond comprehension, reduce it.

## Escalate Or Block When

- the beat uses no meaningful novelty where the container expects it
- surprise exceeds the container budget and breaks comprehension
- explanatory cleanup removes the only schema-breaking moment