---
name: caebmad-help
description: Context-aware CAE-BMAD routing, phase state guidance, and next-action recommendation.
version: 0.3.0-rebuild
agent: cae-method-orchestrator
---

# Skill: caebmad-help

## 1. Purpose & Invocation
The `caebmad-help` skill provides context-aware status analysis and workflow guidance for the CAE-BMAD product development method. Use this skill when the operator asks what to do next, what milestone state is active, or which agent/workflow to invoke.

## 2. Invocation Preconditions
Before providing guidance:
1. Load `config/caebmad-config.yaml` and `.caebmad/state/project-state.yaml`.
2. Inspect `config/CAE_BMAD_METHOD_STATES.yaml` to identify the current phase.
3. Check `config/CAE_BMAD_ARTIFACT_GRAPH.yaml` to determine which artifacts are completed, in review, or pending.
4. Verify if any active contradictions or pending operator grill questions exist.

## 3. Execution Logic
1. **State Evaluation:** Determine current state against the 12 method states (e.g. `NOT_STARTED`, `RESEARCHING`, `DEFINING_PRODUCT`, etc.).
2. **Missing Prerequisite Check:** If an upstream artifact is missing or unverified, block downstream execution and report the exact error code (`MANDATE_INPUT_MISSING`, `WORKFLOW_UNDER_SPECIFIED`).
3. **Next Agent Routing:** Route to the primary executing agent mapped in `config/CAE_BMAD_AGENT_ROUTING.yaml`.
4. **Command Recommendation:** Provide the exact CLI command or prompt needed to advance.

## 4. Output Contract
The skill returns a structured status packet:
- **Current State:** Active state ID and phase description.
- **Completed Artifacts:** List of validated artifacts.
- **Pending Deliverables:** Next required artifacts.
- **Recommended Action:** Specific agent invocation prompt or script command.
- **Unresolved Operator Decisions:** Any open items in the Decision Ledger.
