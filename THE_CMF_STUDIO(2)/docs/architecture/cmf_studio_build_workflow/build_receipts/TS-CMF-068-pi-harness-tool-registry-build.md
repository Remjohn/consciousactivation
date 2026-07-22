# Build Receipt: TS-CMF-068 Pi Harness Tool Registry

**Status:** Built  
**Built At:** 2026-06-22  
**Spec:** `docs/tech-specs/TS-CMF-068-pi-harness-tool-registry.md`

## Implementation

- Added `ToolCapabilitySpec`, `ToolInvocationRequest`, `ToolInvocationReceipt`, and `DepartmentRuntimeRegistry`.
- Added tool registration and invocation gates for agent scope, stage scope, idempotency, mutation boundary, and missing-tool handoff.
- Added API endpoint for tool registration and invocation.

## Acceptance Evidence

- Pi cannot use missing tools; missing capabilities emit handoff receipts.
- Mutating tools must declare Command Bus or workflow command boundary.
- Mis-scoped agents/stages are blocked.
- Idempotent invocations reuse the registered idempotency receipt path.

## Tests

- Covered by `test_hooks_extensions_skills_tools_and_adapters_enforce_runtime_boundaries`.
- Full CMF Studio suite -> 437 passed, 2 skipped.

