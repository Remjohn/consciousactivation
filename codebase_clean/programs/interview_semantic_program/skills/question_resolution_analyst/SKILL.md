---
name: question_resolution_analyst
version: 1.0.0
description: "Passive, flat Canonical Skill for adversarially evaluating candidate questions, validating Matrix of Edging pressure paths, and assessing downstream archetype compatibility."
authority_lane: ANALYST
---

# Question Resolution Analyst Skill

## 1. Purpose & Authority Lane
This skill operates strictly within the **ANALYST** lane of `interview_semantic_program`.
Its mandate is adversarial quality filtering, non-scripted invariant enforcement, Matrix of Edging verification, and downstream archetype compatibility assessment.

## 2. Invariant Checks & Gate Taxonomy
The analyst evaluates candidate question sequences against 3 strict gates:

1. **Non-Scripted / Anti-Leading Assertion (`assert_non_scripted_prompt`)**:
   - Rejects leading rhetorical patterns (e.g., *"Don't you agree"*, *"Isn't it true"*, *"Wouldn't you say"*, *"Can you confirm that"*).
   - Enforces open-ended experiential inquiry focusing on *what*, *where*, *when*, *take me to the moment*, *how*.

2. **Matrix of Edging Pressure Path Verification**:
   - Verifies the 7 mandatory seed parameters:
     - `psychological_role`
     - `tension`
     - `activation_direction_set`
     - `pressure_path` (must be `progressive_escalation_to_crucible` or validated variant)
     - `stance`
     - `counteractivation_strategy`
     - `smallest_commitment`
   - Validates that escalation preserves psychological safety while probing authentic tension.

3. **Downstream Content Archetype Fit**:
   - Assesses compatibility against format targets:
     - Format 01: `F01_CINEMATIC_STORY` (high episodic crucible depth)
     - Format 02: `F02_MINIMAL_COACH` (mechanistic clarity and small useful movements)
     - Format 03: `F03_PROOF_COMMENTARY` (evidential receipts and contrarian decisions)

## 3. Invariant Constraints
- **Passive Execution**: Computes evaluation verdicts strictly in-memory without side-effects.
- **Fail-Closed Filtering**: Any violation of non-scripting invariants immediately fails the evaluation gate.
