---
name: caebmad-workflow-factory
description: Maps and validates multi-agent workflows, factory execution pipelines, JIT context assembly, and rollback strategies at Level 05.
version: 0.3.0-rebuild
agent: cae-workflow-factory-analyst
---

# Skill: caebmad-workflow-factory

## 1. Purpose & Invocation
The `caebmad-workflow-factory` skill enables the `cae-workflow-factory-analyst` to map, validate, and troubleshoot orchestration DAGs, factory primitives, and error recovery policies at `Level 05: AI WORKFLOW / FACTORY`.

## 2. Invocation Preconditions
1. Active workflows available in `workflows/`.
2. Workflow primitive constitutions (`docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml`) accessible.
3. Workflow Factory Map schema (`schemas/workflow_factory_map.schema.json`) available.

## 3. Execution Logic
1. **Workflow DAG Mapping:** Ingest workflow YAML manifests and extract steps, triggers, and handoffs.
2. **Factory Primitive Verification:** Map runtime bindings to `ca_runtime` and `cmf_pipeline`.
3. **Rollback Strategy Audit:** Verify that all pipelines have non-empty rollback policies and error transitions.
4. **ADW Pattern Cataloging:** Document SSSF, JIT Context Capsule, and adversarial review patterns.
5. **Schema Validation:** Ensure the generated map passes `schemas/workflow_factory_map.schema.json`.

## 4. Output Contract
- `docs/cae-bmad/02_investigation/WORKFLOW_FACTORY_MAP.json`
- `docs/cae-bmad/02_investigation/WORKFLOW_FACTORY_MAP.md`
