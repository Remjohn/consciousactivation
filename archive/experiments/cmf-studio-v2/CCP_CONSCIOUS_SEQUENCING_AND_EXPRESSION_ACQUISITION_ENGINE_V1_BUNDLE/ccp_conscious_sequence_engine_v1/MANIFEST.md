# CCP Conscious Sequencing & Expression Acquisition Engine V1

## Reading order

1. `00_AGENT_START_HERE.md`
2. `01_MASTER_SPEC.md`
3. `02_DOMAIN_CONTRACTS_AND_STATE_MACHINES.md`
4. `03_RUNTIME_WORKFLOWS.md`
5. `04_REGISTRIES_AND_FORMAT_ADAPTERS.md`
6. `05_EVALUATION_GOVERNANCE_AND_LEARNING.md`
7. `06_IMPLEMENTATION_SEQUENCE.md`

## Executable artifacts

- `models/sequence_engine_models.py` — canonical Pydantic contracts.
- `schemas/*.schema.json` — generated JSON Schemas.
- `registries/*.json` — sequence, ingredient, acquisition, adapter, and eval registries.
- `examples/*.json` — validated end-to-end examples.
- `generated/sequence_contracts.ts` — TypeScript consumer contracts; Python remains authoritative.
- `tests/test_examples.py` — contract-validation smoke tests.

## Binding doctrine

The Interview Brief shops for ingredients. The live interview harvests them. The Expression Ingredient Inventory stores them. The Conscious Sequencing Engine cooks them. Composition engines plate them. CMF renders them. Evaluations taste and approve them.

This bundle adds an explicit sequencing and acquisition layer without replacing the existing CCP registries, Complete Expression Session, Complete Editing Session, Brand Context, Voice DNA, Visual DNA, Matrix of Edging, or primitive system.
