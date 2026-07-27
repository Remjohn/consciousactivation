# CMF Container Contract Convention

Container contracts define what must be true at a fixed arc position before any specific cinematic vehicle is chosen.

Each package follows this contract:

- `contract.json`
- `rules.yaml`

## Contract File

- file: `contract.json`
- schema file: `intelligence/schemas/container-contract.schema.json`
- required schema id: `cmf.container.contract/v1`

Required top-level keys:

- `$schema`
- `schema_id`
- `container_id`
- `name`
- `version`
- `arc_order`
- `narrative_role`
- `neural_targets`
- `transportation_state`
- `cls_budget`
- `asl_seconds`
- `color_temperature_kelvin`
- `pad_target`
- `motion_palette`
- `duration_share_of_video`
- `detection_mode`
- `prediction_error_budget`
- `compatible_components`
- `hard_requirements`
- `default_component`

## Rules File

- file: `rules.yaml`
- schema file: `intelligence/schemas/container-rules.schema.json`
- required schema id: `cmf.container.rules/v1`

Required top-level keys:

- `schema`
- `schema_id`
- `container_id`
- `enabled`
- `priority`
- `enforcement`
- `applies_to`
- `required_sequence`

Containers define the biological search space. Components may vary, but they must not violate the active container contract.