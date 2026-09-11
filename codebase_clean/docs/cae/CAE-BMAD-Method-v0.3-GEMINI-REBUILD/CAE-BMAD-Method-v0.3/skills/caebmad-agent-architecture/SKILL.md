---
name: caebmad-agent-architecture
description: Analyzes and validates agent definitions, boundary rules, tool permissions, and multi-agent communication contracts at Level 04.
version: 0.3.0-rebuild
agent: cae-agent-systems-analyst
---

# Skill: caebmad-agent-architecture

## 1. Purpose & Invocation
The `caebmad-agent-architecture` skill enables the `cae-agent-systems-analyst` to audit, construct, and validate agent systems at `Level 04: AGENT`.

## 2. Invocation Preconditions
1. Agent definitions loaded in `gemini_execution/agents/`.
2. Agent Routing configuration (`config/CAE_BMAD_AGENT_ROUTING.yaml`) available.
3. Agent System Architecture schema (`schemas/agent_system_architecture.schema.json`) available.

## 3. Execution Logic
1. **Agent Inventory Audit:** Scan all 19 agent specification files.
2. **Contract & Skill Verification:** Validate that every agent has explicit input/output contracts and loadable skills.
3. **Boundary Verification:** Verify that hard negative boundaries are stated for every agent.
4. **Communication Matrix Compilation:** Map valid invocation edges and delegation rules.
5. **Schema Validation:** Ensure the generated map passes `schemas/agent_system_architecture.schema.json`.

## 4. Output Contract
- `docs/cae-bmad/02_investigation/AGENT_ARCHITECTURE_MAP.json`
- `docs/cae-bmad/02_investigation/AGENT_ARCHITECTURE_MAP.md`
