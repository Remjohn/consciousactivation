# Gemini Activation Prompt — M60

You are executing CAE Mandate M60: **Workflow Step Contracts**.

This is a governed brownfield implementation mandate. Before changing anything, read `docs/PRD/CURRENT.md`, the CAE Mandate Authoring Protocol, the Gemini Mandate Execution Skill, the relevant constitutions, `governance/program-control/`, the mandate-specific files listed in the mandate, and the exact CAE source symbols/callers that currently implement the requested behavior. Also inspect the SSSF reference files named by the mandate. Report what you actually read.

Also read `00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md` and satisfy its state-boundary, transition, recovery, shared-control-surface and procedural-practice obligations where they apply.
Do not assume an architecture statement is implemented. Reconcile each requested behavior against the current repository. Reuse existing CAE objects, registries, Program/Harness/State/Receipt authorities and runtime components. Do not create a second workflow engine or alternate source of truth.

Execute ONLY M60. Produce the artifacts specified by the mandate. For every material behavior, provide exact code paths, test commands, fixtures, runtime evidence and limitations. Include at least one deliberate false-proof/reward-hacking attempt. Where an Agent is involved, demonstrate the concrete Agent → compiled context → model/tool policy → typed output → gate path. Where a workflow is involved, demonstrate the deterministic control-flow path and state transition.

Update the relevant section of `docs/PRD/CURRENT.md` in the same session. Update any affected local `CURRENT.md` / `CURRENT_PROJECT_STATUS.md` file in the same session. Record the exact commit SHA and operator decision.

STOP after M60 at the operator gate. Do not begin M61. A green unit test is not sufficient; distinguish authored, code-existing, test-verified, runtime-verified and operator-accepted claims.
