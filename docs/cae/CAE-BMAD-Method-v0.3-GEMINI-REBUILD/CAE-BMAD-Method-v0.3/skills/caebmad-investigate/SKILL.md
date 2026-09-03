---
name: caebmad-investigate
description: Executes multi-level engineering investigations across the 13 operating levels, enforcing descent stop conditions and evidence-backed ascent.
version: 0.3.0-rebuild
agent: cae-documentation-analyst
---

# Skill: caebmad-investigate

## 1. Purpose & Invocation
The `caebmad-investigate` skill performs deep technical investigations across the 13 operating levels. It traces high-level documentation claims down to function and line code reality and surfaces doc-to-code drift.

## 2. Invocation Preconditions
1. Stated claim, PRD requirement, or contradiction identified.
2. Workspace mounted and Python / repository file trees accessible.
3. Operating levels framework (`method/CAE_BMAD_OPERATING_LEVELS.md`) loaded.

## 3. Execution Logic
1. **Starting Level Assessment:** Determine the abstraction level of the claim (e.g. Level 02: DOCUMENTATION).
2. **Descent Execution:** Systematically descend to inspect lower levels:
   - Level 06: Check repository file existence.
   - Level 07/08: Check application entrypoint and CLI contracts.
   - Level 09: Check database models and table schemas.
   - Level 10/11: Check module imports and class definitions.
   - Level 12/13: Check exact function logic, AST nodes, and test assertions.
3. **Stop Condition Evaluation:** Terminate descent as soon as conclusive evidence is discovered or missing code is proven.
4. **Drift Classification:** Categorize finding as `CONFIRMED`, `DRIFT_DETECTED`, `CONTRADICTED`, or `MISSING_IMPLEMENTATION`.
5. **Trace Generation:** Record the complete trajectory using `templates/level_investigation_trace.md`.

## 4. Output Contract
- Level Investigation Trace record
- Updated Operating Level Assessment (`docs/cae-bmad/02_investigation/OPERATING_LEVEL_ASSESSMENT.md`)
- Drift items logged in Contradiction Register if conflicting.
