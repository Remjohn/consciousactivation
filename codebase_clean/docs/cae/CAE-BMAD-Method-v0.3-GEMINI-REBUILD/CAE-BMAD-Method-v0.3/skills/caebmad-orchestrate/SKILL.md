---
name: caebmad-orchestrate
description: Governs method state transitions, milestone dependency evaluation, and gate verification.
version: 0.3.0-rebuild
agent: cae-method-orchestrator
---

# Skill: caebmad-orchestrate

## 1. Purpose & Invocation
The `caebmad-orchestrate` skill evaluates milestone completion, validates state transition invariants, and prepares operator gate packets for formal review.

## 2. Invocation Preconditions
1. Active mandate or milestone execution has generated its declared deliverables.
2. The relevant analyst agent has produced its artifact report.
3. Test logs and evidence records are available.

## 3. Execution Logic
1. **Artifact Verification:** Check that all required artifacts for the state transition exist on disk and are non-empty.
2. **Schema Validation:** Run JSON Schema / YAML validation on all structured deliverables.
3. **Traceability Check:** Ensure requirement-to-code traceability links are bidirectional.
4. **False-Proof Audit:** Verify that tests include negative/countertests and touch real execution surfaces.
5. **Gate Packet Assembly:** If all checks pass, generate the formal `OPERATOR_GATE_*.md` packet.

## 4. Output Contract
- Updated `MANDATE_EXECUTION_LEDGER.md`
- Gate verification report with PASS / FAIL / OPERATOR_DECISION_REQUIRED status.
