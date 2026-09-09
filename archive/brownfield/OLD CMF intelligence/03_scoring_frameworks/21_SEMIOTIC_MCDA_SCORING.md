# Semiotic MCDA Scoring

## Purpose

The visual harness must battle-test visual ideas before generation.

The question is not:

> Is this image beautiful?

The question is:

> Does this visual force a mental action from this audience?

## Scoring dimensions

```txt
Zero-Second Hook
Audience Visual World Fit
Mirror Activation Power
Target Activation Power
Viewer Role Clarity
Recognition Carrier Strength
Emotional Load Fit
Edge Pressure Fit
Identity Tension Fit
Pattern Match Strength
Pattern Interrupt Strength
Prediction Gap
Payoff Potential
Affinity Texture
Anticipation Gap
Anti-Cliché Score
Composition Potential
T/V Route Fit
Real-Life Reference Strength
Wrong-Reading Resistance
```

## Example scoring summary

For “the safer sentence”:

| Candidate | Mirror | Target | Role | Anti-cliché | Result |
|---|---:|---:|---:|---:|---|
| generic confident leader portrait | low | low | low | low | reject |
| Slack message softened to “all good” | high | high | high | medium-high | strong |
| meeting note with real issue circled | medium-high | high | high | high | strong |

## Required output

```json
{
  "semiotic_mcda": {
    "candidates": [],
    "selected_candidate": "...",
    "selection_reason": "...",
    "rejected_candidates": []
  }
}
```
