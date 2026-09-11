---
name: caebmad-method-certification
description: Orchestrates the comprehensive end-to-end integration run, verifies cross-mandate consistency (M01-M12), and compiles the Master Method Certification package.
version: 0.3.0-rebuild
agent: cae-method-orchestrator
---

# Skill: caebmad-method-certification

## 1. Purpose & Invocation
The `caebmad-method-certification` skill enables the `cae-method-orchestrator` to certify the complete CAE-BMAD method rebuild across all 13 operating levels and all 12 mandates.

## 2. Invocation Preconditions
1. Mandates M01 through M11 successfully executed.
2. Full regression test suite passing in `tests/`.
3. Schemas `schemas/method_certification_package.schema.json` and `schemas/end_to_end_integration_run.schema.json` loaded.

## 3. Execution Logic
1. **Vertical Slice Execution:** Run the end-to-end integration trace from Level 01 (Product Intent) to Level 13 (Line/Block) on a real physical code area.
2. **Cross-Mandate Matrix Verification:** Validate that every mandate has passing unit tests and schema-compliant deliverables.
3. **Residual Gap Audit:** Ensure that all known partial/missing layers are registered in the Missing Implementation Register.
4. **Deliverable Emission:** Assemble `docs/cae-bmad/10_certification/CAE_BMAD_METHOD_CERTIFICATION.json` and `END_TO_END_INTEGRATION_RUN.json` with accompanying markdown documents.

## 4. Output Contract
- `docs/cae-bmad/10_certification/CAE_BMAD_METHOD_CERTIFICATION.json` & `.md`
- `docs/cae-bmad/10_certification/END_TO_END_INTEGRATION_RUN.json` & `.md`
