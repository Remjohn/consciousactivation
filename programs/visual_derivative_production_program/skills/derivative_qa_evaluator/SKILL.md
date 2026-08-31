---
name: derivative_qa_evaluator
description: Performs independent dual-axis Semantic QA and Render QA on visual derivatives.
version: 1.0.0
lane: ANALYST
---

# Derivative QA Evaluator Skill

## Role
Passive, flat skill executed within the `ANALYST` authority lane.
Evaluates both Semantic QA (source fidelity, verbatim quotes, wrong-reading locks) and Render QA (file validity, byte sizes, dimensions, frame integrity).

## Invariants
- Enforces strict dual-axis independence.
- Verifies that rendering success does not bypass semantic validation.
- Verifies that semantic validity does not bypass render verification.
