---
name: "demand_admission_verifier"
version: "1.0.0"
description: "Verifies visual asset demand integrity, upstream evidence lineage, non-synthetic assertions, and wrong-reading locks before VAE admission."
lanes:
  - "COMMANDER"
  - "HUNTER"
---

# Demand Admission Verifier Skill

## Role & Purpose
Verifies incoming visual asset demands to guarantee they meet all constitutional CAE and Phase 4 standards before delegation to VAE workcells.

## Verification Protocol
1. **Non-Synthetic Integrity**: Ensure `is_synthetic` is false. Reject mock or synthetic test fixtures from production promotion.
2. **Upstream Evidence Lineage**: Verify reaction receipts and expression moments are non-empty and cryptographically addressable.
3. **Evidence Hash Matching**: Check evidence segment spoken text against `text_sha256` digest.
4. **Wrong-Reading Locks**: Ensure wrong-reading lock constraints are present and non-empty.
5. **No Flat Float State**: Ensure coordinates, confidence scores, and aspect ratios conform to integer/basis-points serialization.
