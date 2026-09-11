---
name: caebmad-architecture
description: Authors technical architecture specifications, subsystem boundaries, typed interface schemas, and brownfield integration strategies.
version: 0.3.0-rebuild
agent: cae-architecture-agent
---

# Skill: caebmad-architecture

## 1. Purpose & Invocation
The `caebmad-architecture` skill enables the `cae-architecture-agent` to author, validate, and maintain technical architecture specifications at `Level 02: DOCUMENTATION` and `Level 07: APPLICATION`.

## 2. Invocation Preconditions
1. Functional Requirements matrix available.
2. Brownfield application and data maps accessible.
3. Schema `schemas/architecture_spec.schema.json` loaded.

## 3. Execution Logic
1. **Subsystem Decomposition:** Define service responsibilities, storage models, and message queues.
2. **Interface Contract Definition:** Specify typed schemas for inter-service communication.
3. **Brownfield Reconciliation:** Map greenfield components directly onto existing Python packages.
4. **Deliverable Emission:** Assemble `docs/cae-bmad/04_architecture/ARCHITECTURE.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/04_architecture/ARCHITECTURE.json`
- `docs/cae-bmad/04_architecture/ARCHITECTURE.md`
