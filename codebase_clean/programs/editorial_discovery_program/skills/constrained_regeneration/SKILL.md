---
name: constrained_regeneration
description: Executes constrained candidate regeneration guided by operator steering rationale, creating versioned candidates with unbroken lineage without mutating authentic source evidence.
version: 1.0.0
lane: COMPOSER
inputs:
  - predecessor_candidate_id
  - regeneration_spec
  - operator_guidance
outputs:
  - versioned_content_candidate
  - decision_receipt
maturity: PRODUCTION_READY
---

# Constrained Regeneration Canonical Skill

## 1. Operational Scope
Governed by CAE Mandate M38 and Phase 4 Asset Lineage Graph (Doc 31).
Executed in the **COMPOSER** lane under **COMMANDER** operator steering.
Derives new candidate versions from existing candidates based on operator guidance and constraints.

## 2. Invariants
- **Unbroken Predecessor Lineage**: Every regenerated candidate explicitly links `predecessor_candidate_id` and increments `version` ($v_{n+1} = v_n + 1$).
- **Evidence Immutability**: Underlying evidence links, verbatim text segments, and SHA-256 hashes are strictly verified and preserved unchanged.
- **Supercession Accounting**: Predecessor candidates are marked as `SUPERSEDED_BY_REGENERATION` in the authoritative store.
- **Operator Steering Rationale**: Regeneration constraints (hook emphasis, tone refinement, duration targets, preserved segments, forbidden angles) are formally captured in a signed `EditorialDecisionReceiptRecord`.
- **Draft Isolation**: Regenerated candidates enter the lifecycle in `DRAFT_CANDIDATE` status and require explicit operator selection before downstream production eligibility.
