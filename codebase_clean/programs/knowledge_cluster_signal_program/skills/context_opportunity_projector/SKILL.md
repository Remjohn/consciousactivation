---
name: context_opportunity_projector
description: Projects research signals and knowledge clusters onto guest emotional DNA and audience cognitive tensions to synthesize typed ContextProjections.
version: 1.0.0
authority_lane: COMPOSER
invocable_by:
  - knowledge_cluster_signal_program
passive: true
---

# Context Opportunity Projector Skill

## 1. Constitutional Role & Authority Lane
The `context_opportunity_projector` skill operates strictly in the **COMPOSER** authority lane. It projects temporal research signals onto guest identity dimensions (`identity_dna`, `EXP-TRG-*` trigger vectors) and audience cognitive tensions (`TNS-*`), synthesizing typed `ContextProjection` records.

## 2. Invariants & Constraints
1. **Passive Execution:** This skill is strictly passive and flat.
2. **Episodic vs Semantic Register:** Prioritizes signals that intersect with lived episodic trigger vectors over high-level topical interests.
3. **Triple-Gated Composite Scoring:**
   $$\text{CompositeOpportunityScore} = \frac{\text{ActivationPotential} \times \text{DistributionPotential} \times \text{EvidenceConfidence}}{10^{12}}$$
   All intermediate and final scores are computed in integer micros ($0 \dots 1000000$).
4. **Hard Non-Compensable Gates:** If any core factor (activation, distribution, or evidence confidence) is zero, composite opportunity score is zero fail-closed.

## 3. Output Schema
```json
{
  "projection_id": "cprj_uuid7",
  "signal_id": "sig_uuid7",
  "cluster_id": "kcl_uuid7",
  "guest_id": "gst_uuid7",
  "audience_state_id": "aud_uuid7",
  "activation_potential_micros": 880000,
  "distribution_potential_micros": 750000,
  "evidence_confidence_micros": 920000,
  "composite_opportunity_score_micros": 607200,
  "trigger_vector_refs": ["EXP-TRG-001", "EXP-TRG-004"],
  "audience_tension_refs": ["TNS-002"],
  "hypothesis_readiness": true
}
```
