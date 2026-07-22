# CMF Component Spec Convention

Component specs define the interchangeable cinematic vehicles that may fill a valid container.

Each package follows this contract:

- `spec.json`
- `rules.yaml`

## Spec File

- file: `spec.json`
- schema file: `intelligence/schemas/component-spec.schema.json`
- required schema id: `cmf.component.spec/v1`

Required top-level keys:

- `$schema`
- `schema_id`
- `component_id`
- `scene_number`
- `name`
- `version`
- `function`
- `compatible_containers`
- `cls_footprint`
- `required_asset_types`
- `template_variants`
- `effect_dependencies`
- `selection_signals`
- `audio_profile`
- `fallback_behavior`

## Rules File

- file: `rules.yaml`
- schema file: `intelligence/schemas/component-rules.schema.json`
- required schema id: `cmf.component.rules/v1`

Required top-level keys:

- `schema`
- `schema_id`
- `component_id`
- `enabled`
- `selection_priority`
- `enforcement`
- `applies_to`

Components are creative choices, not structural laws. The container governs whether a component is allowed; the subsystem layer governs whether its output stays legitimate.