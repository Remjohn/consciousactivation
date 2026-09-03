---
name: caebmad-operating-level
description: Traverses the 13 engineering operating levels, enforcing top-down descent and bottom-up ascent heuristics.
version: 0.3.0-rebuild
agent: cae-method-orchestrator
---

# Skill: caebmad-operating-level

## 1. Purpose & Invocation
The `caebmad-operating-level` skill governs how agents move up and down the 13-level engineering stack. It prevents unsupported high-level assertions by enforcing top-down descent to code/runtime ground truth and controls bottom-up abstraction creation.

## 2. Operating Levels Reference
- Level 01: `PRODUCT / INTENT`
- Level 02: `DOCUMENTATION`
- Level 03: `PLAN`
- Level 04: `AGENT`
- Level 05: `AI WORKFLOW / FACTORY`
- Level 06: `REPOSITORY`
- Level 07: `APPLICATION`
- Level 08: `SCRIPT / CLI`
- Level 09: `DATABASE / TABLE`
- Level 10: `MODULE / DIRECTORY`
- Level 11: `FILE / TYPE / CLASS`
- Level 12: `FUNCTION`
- Level 13: `LINE / BLOCK`

## 3. Execution Logic
1. **Identify Starting Level:** Determine the initial operating level of the inquiry or requirement.
2. **Evaluate Descent Need:** If the claim lacks code citations or conflicts with documentation, calculate the minimum required descent depth (e.g. descend from Level 02 down to Level 12).
3. **Execute Ground-Truth Inspection:** Call code search, AST parsing, or test execution at the target lower level.
4. **Ascent Formulation:** Aggregate verified low-level facts into high-level findings.
5. **Record Level Trace:** Document the descent trajectory: `Starting Level → Target Level → Evidence Found → Ascended Conclusion`.
