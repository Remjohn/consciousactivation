# CS-007 Skill

## Purpose

Apply the Theta Reset Validator so each cut earns the encoding reset it triggers.

## Use This Skill When

- evaluating dense cut sequences
- reviewing punch-ins or reframes
- deciding whether an edit adds new information or only fake activity

## Required Inputs

- cut map
- information delta per cut
- semantic novelty
- motion change
- shot purpose

## Decision Procedure

1. Check what new meaning the incoming shot provides.
2. Penalize cuts that spend a reset without adding semantic value.
3. Flag sequences that look active but move the narrative nowhere.

## Runtime Guidance

- Cuts are encoding events, not decoration.
- More cuts are not automatically more engaging.
- If a cut adds nothing, remove it.