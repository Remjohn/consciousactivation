# M04 — Interview Brief Compilation

**Status:** PROPOSED
**Depends on:** M03
**Primary requirement:** FR-IP-009

## Objective

Compile Operator-approved hypothesis/question material into the existing `activative_interview_brief` contract. Do not create a second Brief representation.

## Brownfield rule

`TS-APP-COMPOSER-001` remains authoritative for the existing Brief structure. Before editing, inspect the current live `domain.py`, canonical validators, repository storage, API schema, and tests.

## Required compilation

The compiler must preserve or produce, as the live contract permits:

- research package reference;
- Brand Context / Voice DNA references where already supported;
- tension hypothesis;
- Matrix of Edging seed/reference in the existing supported form;
- planned question sequence;
- expression targets;
- planning/provenance lineage;
- Operator authority state.

## Adaptive planning representation

The Brief may carry a deterministic coverage spine plus bounded candidate alternatives only if the existing schema can represent them. Do not force the full runtime frontier into the Brief if it belongs to a runtime/derived structure.

## Required tests

- real Brief can be created and read back;
- invalid planned-question references are rejected;
- AIR ownership is not duplicated;
- compilation is idempotent under the repository's existing conventions;
- selected/rejected candidate states are reflected correctly.

## Stop conditions

Stop if the current Brief contract cannot represent required semantics without canonical schema change. Escalate that change instead of overloading free text or creating a parallel Brief.
