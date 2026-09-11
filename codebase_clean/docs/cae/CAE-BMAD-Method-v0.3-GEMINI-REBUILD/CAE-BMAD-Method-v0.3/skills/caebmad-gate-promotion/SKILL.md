---
name: caebmad-gate-promotion
description: Manages the operator gate evaluation lifecycle, gate packet generation, decision recording, and rollback procedures.
version: 0.3.0-rebuild
agent: cae-method-orchestrator
---

# Skill: caebmad-gate-promotion

## 1. Purpose & Invocation
The `caebmad-gate-promotion` skill enables the `cae-method-orchestrator` to compile Operator Gate packets and enforce human sign-off before state promotion.

## 2. Invocation Preconditions
1. Adversarial Review Record completed and clearance granted.
2. Full test suite execution logs available.
3. Schema `schemas/operator_gate_decision.schema.json` loaded.

## 3. Execution Logic
1. **Gate Packet Assembly:** Synthesize evidence, test reports, and missing registers into `OPERATOR_GATE_Mxx.md`.
2. **Decision Recording:** Maintain `docs/cae-bmad/00_governance/OPERATOR_GATE_DECISIONS.json` and `.md`.
3. **Rollback Enforcement:** Trigger rollback procedures if an operator rejects a gate or tests regress.
4. **State Promotion:** Transition mandate status to RATIFIED upon explicit operator command.

## 4. Output Contract
- `docs/cae-bmad/00_governance/OPERATOR_GATE_DECISIONS.json`
- `docs/cae-bmad/00_governance/OPERATOR_GATE_DECISIONS.md`
