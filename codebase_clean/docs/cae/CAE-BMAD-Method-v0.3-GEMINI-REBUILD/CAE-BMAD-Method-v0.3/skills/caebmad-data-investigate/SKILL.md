---
name: caebmad-data-investigate
description: Audits database schemas, data entities, storage models, and canonical state aggregate alignment at Level 09.
version: 0.3.0-rebuild
agent: cae-data-analyst
---

# Skill: caebmad-data-investigate

## 1. Purpose & Invocation
The `caebmad-data-investigate` skill enables the `cae-data-analyst` to audit data models, entity fields, and canonical state aggregate schemas at `Level 09: DATABASE / TABLE`.

## 2. Invocation Preconditions
1. Database and domain models accessible in `services/*/src/` or `packages/`.
2. State constitutions in `docs/cae/constitutions/` accessible.
3. Schema `schemas/data_reality_map.schema.json` loaded.

## 3. Execution Logic
1. **Model Discovery:** Inspect Pydantic, dataclass, and database models across services.
2. **Field & Key Extraction:** Extract required fields, primary keys, and storage bindings.
3. **Constitution Cross-Check:** Verify alignment against `CA-CAN-02_STATE_AGGREGATE.yaml`.
4. **Map Assembly:** Emit `docs/cae-bmad/07_brownfield/DATA_REALITY_MAP.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/07_brownfield/DATA_REALITY_MAP.json`
- `docs/cae-bmad/07_brownfield/DATA_REALITY_MAP.md`
