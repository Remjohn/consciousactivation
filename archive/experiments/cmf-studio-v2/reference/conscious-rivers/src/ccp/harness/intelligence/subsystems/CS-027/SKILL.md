# CS-027 Skill

## Purpose

Apply Temporal Binding to make spoken keywords and their supporting graphics arrive inside the memory-binding window rather than as two separate events.

## Use This Skill When

- placing C-roll against spoken teaching points
- timing proof cards, diagrams, and keyword overlays
- reviewing editor regenerations that moved graphics but not audio

## Required Inputs

- phonetic onset or keyword timestamp
- waveform peak data
- graphic first-frame timestamp
- event type and salience

## Decision Procedure

1. Identify the target spoken keyword or phrase.
2. Measure the offset between phonetic onset and first visual frame.
3. Score the offset against the allowed binding window.
4. Return a binding score and adjustment amount if needed.

## Runtime Guidance

- Visual-leading is slightly safer than late graphics.
- Treat late graphics as recall failures, not just timing polish issues.
- Use this skill on educational, proof, and coaching overlays first.

## Escalate Or Block When

- the visual arrives after the binding window
- the word and graphic are technically present but cognitively split
- a regeneration patch broke synchronization around a key teaching moment