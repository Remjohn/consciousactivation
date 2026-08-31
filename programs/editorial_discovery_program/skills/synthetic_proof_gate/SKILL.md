---
name: synthetic_proof_gate
description: Enforces the fail-closed Synthetic-Proof Block and manages human Operator selection gates, ensuring no synthetic or ungrounded artifacts reach production.
version: 1.0.0
lane: COMMANDER
inputs:
  - content_candidate
  - operator_action
  - rationale
outputs:
  - editorial_storyboard
  - decision_receipt
maturity: PRODUCTION_READY
---

# Synthetic-Proof Gate Canonical Skill

## 1. Operational Scope
Governed by CAE Mandate M35 and CAE-M09.
Executed exclusively in the **COMMANDER** lane.
Acts as the final constitutional gate before content promotion.

## 2. Invariants
- **Fail-Closed Synthetic Block**: Any candidate originating from a synthetic producer (`is_synthetic=True`, `production_authorized=False`, synthetic adapters) is strictly rejected from production search and selection gates, generating a signed `SYNTHETIC_BLOCKED` receipt.
- **Lineage Verification**: Cryptographic validation of all evidence links against stored authentic interview turns.
- **Evidence Immutability**: Operator modifications to titles/hooks cannot alter underlying evidence text or hashes.
- **Mandatory Operator Rationale**: Operator selections, rejections, and modifications require explanatory rationale ($\ge 5$ characters).
- **Anti-Self-Approval**: Automated agents cannot self-approve production candidates.
