---
name: interview_question_hunter
version: 1.0.0
description: "Passive, flat Canonical Skill for extracting high-recall JIT question candidates and semantic activation targets from approved Collision Hypotheses and Guest Research Packages."
authority_lane: HUNTER
---

# Interview Question Hunter Skill

## 1. Purpose & Authority Lane
This skill operates strictly within the **HUNTER** lane of `interview_semantic_program`.
Its mandate is high-recall extraction of semantic targets, 12-D coordinate grounding, and candidate questions across the 4-stage progression grammar.

## 2. Input Requirements
- `workspace_id`: Tenant workspace identifier.
- `approved_collision_hypothesis`: An approved `CollisionHypothesisRecord` from M32 with 12-D coordinate vectors.
- `guest_research_package`: Authoritative guest lived proof citations and source records.

## 3. Progression Grammar & Evidence Mapping
Derived candidate questions MUST follow the four sequential inquiry stages:
1. **ORIENTATION (`ORIENTATION`)**: Establishes initial psychological context and lived ground truth.
   - Target Resolution: `EPISODIC`
   - Desired Evidence: `EVIDENCE_OF_LIVED_EXPERIENCE`
2. **TENSION_PROBE (`TENSION_PROBE`)**: Probes the friction point between status quo paradigms and guest reality.
   - Target Resolution: `MECHANISTIC`
   - Desired Evidence: `CONTRARIAN_DECISION`
3. **CRUCIBLE_EXPOSURE (`CRUCIBLE_EXPOSURE`)**: Evokes the specific point of failure, irreversible commitment, and cost paid.
   - Target Resolution: `EVIDENTIAL`
   - Desired Evidence: `CRUCIBLE_MOMENT`
4. **RESOLUTION_SYNTHESIS (`RESOLUTION_SYNTHESIS`)**: Elicits counter-intuitive operating principles and transferable proof.
   - Target Resolution: `MECHANISTIC`
   - Desired Evidence: `COST_PAID_RECEIPT`

## 4. Invariant Constraints
- **Passive Execution**: Does not call external APIs, database connections, or other skills directly.
- **Non-Leading Formulation**: All questions must be open-ended, non-scripted prompts that never presume the answer.
- **Lineage Integrity**: Every generated candidate question must cite its upstream hypothesis and source refs.
