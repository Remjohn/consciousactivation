---
name: semantic_attribution
description: Interprets EvidenceSegment entities into typed SemanticAnnotation records while strictly enforcing anti-inflation, anti-story-labeling, and partition constraints.
version: 1.0.0
lane: ANALYST
inputs:
  - evidence_segment
  - semantic_role
  - epistemic_status
outputs:
  - semantic_annotation
maturity: PRODUCTION_READY
---

# Semantic Attribution Canonical Skill

## 1. Operational Scope
Governed by CAE Mandate M35 and CAE-M06.
Executed exclusively in the **ANALYST** lane.
Partitions the interpretation into:
1. `ObservableEvidence`: Verbatim speech text and immutable timestamps.
2. `SemanticInference`: Semantic role (`STAKES`, `MECHANISM`, `TURN`, `RESULT`, `IMPLICATION`, etc.), epistemic status (`OBSERVED_DIRECT`, `INFERRED`, etc.), confidence score (in integer basis points `_bps`), tension references, and invariant references.

## 2. Invariants
- **Anti-Status-Inflation**: Pure inferences cannot be upgraded to `OBSERVED_DIRECT` evidence.
- **Anti-Story-Labeling**: Content without causal transformation cannot be labeled as a narrative climax or complete story.
- **Strict Non-Publishability**: Semantic annotations are analytical artifacts; `is_publishable` remains `False`.
