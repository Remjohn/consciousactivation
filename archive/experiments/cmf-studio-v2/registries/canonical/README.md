# Canonical Registry Namespace

This folder is the first implementation pass for Registry Consolidation.

## Namespaces

Canonical registry entries now use a normalized namespace model:

- `registry.primitive.meaning`
- `registry.primitive.experience`
- `registry.methodology`
- `registry.content.*`
- `registry.sequence.pattern`
- `registry.composition.*`
- `registry.visual.*`
- `registry.asset.*`
- `registry.provider.capability`
- `registry.eval.rubric`
- `registry.agent.role`
- `registry.skill.binding`

## Current contents

- `ontology/` — ontology layers, term types, master glossary copy.
- `composition/frame_profiles.v1.json` — delivery/source frame profiles.
- `visual_styles/style_routes.v1.json` — CAC/GMG/Paper-Cut/Documentary/UI style routes.
- `registry/consolidation_manifest.v1.json` — canonical entry manifest and crosswalk.
- `registry/crosswalk.v1.csv` — current registry root to canonical namespace map.

## Rule

New registries should be added here first, then consumed through services. Old registry folders stay as legacy sources until the crosswalk is complete.
