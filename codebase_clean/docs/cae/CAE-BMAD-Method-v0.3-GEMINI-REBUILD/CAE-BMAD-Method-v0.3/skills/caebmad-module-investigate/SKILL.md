---
name: caebmad-module-investigate
description: Audits module hierarchies, Python namespaces, package cohesion, and circular import dependencies at Level 10.
version: 0.3.0-rebuild
agent: cae-module-analyst
---

# Skill: caebmad-module-investigate

## 1. Purpose & Invocation
The `caebmad-module-investigate` skill enables the `cae-module-analyst` to audit Python package hierarchies, import trees, and module encapsulation at `Level 10: MODULE / DIRECTORY`.

## 2. Invocation Preconditions
1. Package source trees (`packages/`, `services/*/src/`) accessible.
2. `__init__.py` files readable.
3. Schema `schemas/module_map.schema.json` loaded.

## 3. Execution Logic
1. **Namespace Mapping:** Scan package trees and record Python module namespaces.
2. **Public API Extraction:** Extract `__all__` or imported public symbols from `__init__.py`.
3. **Import Graph Analysis:** Trace inter-module dependencies and detect circular imports.
4. **Map Assembly:** Emit `docs/cae-bmad/07_brownfield/MODULE_MAP.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/07_brownfield/MODULE_MAP.json`
- `docs/cae-bmad/07_brownfield/MODULE_MAP.md`
