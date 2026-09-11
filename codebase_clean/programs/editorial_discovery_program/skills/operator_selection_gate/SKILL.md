---
name: operator_selection_gate
description: Governs human operator editorial decision-making including candidate selection, rejection, locking, and comparative evaluation without changing authenticated evidence or bypassing state/receipt rules.
version: 1.0.0
lane: COMMANDER
inputs:
  - content_candidate
  - operator_action
  - rationale
  - taste_delta
outputs:
  - editorial_storyboard
  - candidate_lock_record
  - decision_receipt
maturity: PRODUCTION_READY
---

# Operator Selection Gate Canonical Skill

## 1. Operational Scope
Governed by CAE Mandate M38 and CAE-M09.
Executed exclusively in the **COMMANDER** lane.
Acts as the authoritative gateway for operator editorial choices over candidates.

## 2. Invariants
- **Backend-Authoritative Decisions**: Operator decisions (`SELECT`, `REJECT`, `LOCK`, `COMPARE`, `REGENERATE`) are canonical and cannot be bypassed or overridden by agent text.
- **Fail-Closed Synthetic Block**: Unapproved, rejected, or synthetic candidates are strictly blocked from downstream execution.
- **Evidence Immutability Defense**: No operator action or candidate transformation may mutate underlying verbatim evidence text or SHA-256 hashes.
- **Mandatory Explanatory Rationale**: All operator actions require non-empty rationale ($\ge 5$ characters) stored in a cryptographically hashed `EditorialDecisionReceiptRecord`.
- **Lock Protection**: Locked candidates are protected against automated re-ranking, pruning, or modification.
- **Taste Delta Capture**: Operator taste feedback and boundary notes are preserved on rejections and selections for downstream calibration.
