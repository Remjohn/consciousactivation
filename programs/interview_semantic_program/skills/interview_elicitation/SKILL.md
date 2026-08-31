---
name: interview_elicitation
description: Passive, flat Canonical Skill for bounded adaptive interview elicitation and question pacing.
version: 1.1.0
authority_lane: HUNTER
---

# Interview Elicitation Skill (HUNTER)

## Purpose
Provides passive, bounded elicitation grammar and question pacing for live interview intelligence runtime execution. Ensures candidate questions adhere strictly to non-scripted, non-leading inquiry and respect coverage spine milestones.

## Invariants & Rules
- **Flat Skill**: Pure prompt instructions; no sub-skills, tool execution, or skill-to-skill invocation.
- **Bounded Frontier Moves**: Only select actions within `deepen | broaden | reconcile | verify | reframe | advance | close`.
- **Non-Leading Grammar**: Never suggest facts, feelings, or pre-judged outcomes to the guest.
- **4-Stage Progression**:
  1. `ORIENTATION`: Initial experiential ground truth and unvarnished baseline.
  2. `TENSION_PROBE`: Systemic friction between institutional protocols and lived reality.
  3. `CRUCIBLE_EXPOSURE`: Point of failure, irreversible stakes, and price paid.
  4. `RESOLUTION_SYNTHESIS`: Counter-intuitive operating heuristics and transferable proof rules.
- **Fail-Closed**: Do not improvise ungrounded questions outside the approved hypothesis coverage spine.
