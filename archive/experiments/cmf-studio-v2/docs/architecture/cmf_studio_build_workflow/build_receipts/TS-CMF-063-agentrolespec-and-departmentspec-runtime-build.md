# Build Receipt: TS-CMF-063 AgentRoleSpec and DepartmentSpec Runtime

**Status:** Built  
**Built At:** 2026-06-22  
**Spec:** `docs/tech-specs/TS-CMF-063-agentrolespec-and-departmentspec-runtime.md`

## Implementation

- Added `DepartmentSpec`, `MemoryAccessPolicy`, `AgentRoleSpec`, activation state, and role receipts.
- Added agent role registration, mutation-boundary validation, readiness activation gate, and department runtime read model.
- Added Agent Factory API endpoints for role registration, readiness eval, and activation.

## Acceptance Evidence

- Agent roles require registered persona codes.
- Agent roles must declare goal, active objects, tools, memory policy, evals, blocked actions, and receipts.
- Active roles require accepted `AgentReadinessEval`.
- Direct canonical write bypasses are blocked at role-spec validation.

## Tests

- `python -m pytest tests/cmf_studio/test_agent_factory_runtime.py` -> 5 passed.
- Full CMF Studio suite -> 437 passed, 2 skipped.

