---
name: caebmad-adversarial-review
description: Executes skeptical audits, countertests, and false-proof detection across all 13 operating levels.
version: 0.3.0-rebuild
agent: cae-adversarial-reviewer
---

# Skill: caebmad-adversarial-review

## 1. Purpose & Invocation
The `caebmad-adversarial-review` skill enables the `cae-adversarial-reviewer` to audit deliverables against false proofs, ungrounded claims, and broken countertests.

## 2. Invocation Preconditions
1. Deliverable artifacts emitted in `docs/cae-bmad/`.
2. Test suites and schemas accessible.
3. Schema `schemas/review_proof_record.schema.json` loaded.

## 3. Execution Logic
1. **False-Proof Screening:** Verify that positive tests touch physical files and fail when inputs are perturbed.
2. **Countertest Verification:** Execute negative test suites to prove robust error rejection.
3. **Lineage & Dependency Integrity:** Check that crosswalks, source hashes, and parent links resolve.
4. **Deliverable Emission:** Assemble `docs/cae-bmad/09_review/REVIEW_AND_GATE_RECORD.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/09_review/REVIEW_AND_GATE_RECORD.json`
- `docs/cae-bmad/09_review/REVIEW_AND_GATE_RECORD.md`
