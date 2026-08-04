# Context Requirements — Visual Syntax Composition Compiler

## Context Classification Matrix

| Context Element               | Requirement Status    | Description                                            |
|-------------------------------|-----------------------|--------------------------------------------------------|
| `harness_definition_id`       | REQUIRED              | Source harness identifier                             |
| `category_id`                 | REQUIRED              | Must be `carousels` or `supervisuals`                  |
| `wrong_reading_locks`         | REQUIRED              | Non-empty list of format locks                         |
| `slide_evidence`              | REQUIRED              | Analyzed primitives from visual specimens              |
| `canvas_dimensions`           | REQUIRED              | Target width/height in pixels                          |
| `activative_input_refs`       | REQUIRED              | Lineage refs (`identity_dna`, `source_premise`, etc.)  |
| `runtime_copy`                | FORBIDDEN             | Per-campaign copy is injected later at composition time |
| `raw_image_bytes`             | FORBIDDEN             | Skill handles layout geometry specs, not raw media     |
| `provider_credentials`        | FORBIDDEN             | Skill is provider-neutral                              |
