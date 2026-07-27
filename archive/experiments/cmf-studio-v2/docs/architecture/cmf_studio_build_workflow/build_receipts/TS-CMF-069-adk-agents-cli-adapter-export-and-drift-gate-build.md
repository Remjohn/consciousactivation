# Build Receipt: TS-CMF-069 ADK and Agents CLI Adapter Export and Drift Gate

**Status:** Built  
**Built At:** 2026-06-22  
**Spec:** `docs/tech-specs/TS-CMF-069-adk-agents-cli-adapter-export-and-drift-gate.md`

## Implementation

- Added adapter export target, generated adapter file, adapter export, drift finding, and export receipt contracts.
- Added generated-only adapter export from active `AgentRoleSpec` plus accepted readiness eval.
- Added drift checker comparing current adapter contents to generated hashes.
- Added API endpoint for adapter export.

## Acceptance Evidence

- Export is blocked unless the agent role is active and readiness is accepted.
- Generated adapter files cite source spec refs.
- Hand-edited adapter content creates `regenerate_required` drift findings.
- Drifted exports are marked `drift_detected`.

## Tests

- Covered by `test_hooks_extensions_skills_tools_and_adapters_enforce_runtime_boundaries`.
- Full CMF Studio suite -> 437 passed, 2 skipped.

