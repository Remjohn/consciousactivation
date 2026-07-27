# CMF Subsystem Package Convention

All subsystem packages must follow the same four-file contract:

- `SKILL.md`
- `intelligence.md`
- `config.json`
- `rules.yaml`

The machine-readable files are now versioned by shared schema identifiers.

## Config Contract

- file: `config.json`
- schema file: `intelligence/schemas/subsystem-config.schema.json`
- required schema id: `cmf.subsystem.config/v1`

Required top-level keys:

- `$schema`
- `schema_id`
- `subsystem_id`
- `name`
- `version`
- `priority_tier`
- `research_basis`
- `inputs`
- `outputs`
- `thresholds`
- `default_action_on_fail`

## Rules Contract

- file: `rules.yaml`
- schema file: `intelligence/schemas/subsystem-rules.schema.json`
- required schema id: `cmf.subsystem.rules/v1`

Required top-level keys:

- `schema`
- `schema_id`
- `subsystem_id`
- `enabled`
- `priority`
- `enforcement`
- `applies_to`

## Runtime Validation

The assembler validates subsystem packages through `apps/cmf-assembler/subsystem_loader.py` before attaching them to Scene Builder or regeneration legitimacy checks.

## Explicit Compiler Command

From the workspace root:

```powershell
.\.venv\Scripts\python.exe .\apps\cmf-assembler\compile_subsystem_runtime_assets.py --stage all
```

This compiles the dedicated runtime JSON assets under `intelligence/subsystems/runtime/` without needing to run tests or wait for implicit runtime compilation.

If a package fails validation, runtime loading should fail fast rather than silently fall back to prose interpretation.