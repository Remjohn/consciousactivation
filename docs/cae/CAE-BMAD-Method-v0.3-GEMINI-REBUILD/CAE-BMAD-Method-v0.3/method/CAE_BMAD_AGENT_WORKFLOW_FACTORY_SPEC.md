# CAE-BMAD Agent, Workflow, and Factory Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M06  
**Scope:** Architecture, agent boundaries, workflow orchestration DAGs, Agentic Development Workflows (ADWs), JIT context capsule management, and software factory pipelines across Operating Levels 04 and 05.

---

## 1. Constitutional Distinction: Agent vs Factory vs Runtime

A critical failure mode in AI engineering is conflating:
1. **Agent Level (`Level 04: AGENT`):** Persona definitions, role contracts, tool permissions, boundary rules, and prompt engineering.
2. **Workflow / Factory Level (`Level 05: AI WORKFLOW / FACTORY`):** Multi-agent DAG execution, state transition graphs, JIT context assembly, Single-Step Software Factory (SSSF) pipelines, and handoff validation.
3. **Product Runtime (`Level 07: APPLICATION` / `Level 10: MODULE`):** Concrete operational services (`packages/ca_runtime`, `services/pipeline`) executing deterministic data models and persistent storage.

```text
Level 04: AGENT                    [Who acts, what they know, what tools they may call]
         ↕
Level 05: AI WORKFLOW / FACTORY    [How agents coordinate, sequence steps, recover from errors]
         ↕
Level 06: REPOSITORY               [Files, manifests, workspace boundaries]
         ↕
Level 07: APPLICATION / RUNTIME    [Running Python services, deterministic state machines, CAS]
```

---

## 2. Agent Level Architecture (`Level 04`)

Each of the 19 governed CAE-BMAD agents operates under a strict constitutional profile:
- **Explicit Role & Persona:** Non-overlapping domain authority.
- **Bounded Tool Access:** Strictly typed tool permissions preventing rogue filesystem or network execution.
- **Boundary Statement:** Hard negative constraints (e.g. "Must NOT assume operator-level constitutional authority").
- **Typed Input/Output Contracts:** Pre- and post-conditions defined by JSON schemas.

---

## 3. Workflow & Factory Architecture (`Level 05`)

### 3.1 Factory Primitives
1. **JIT Context Capsule Assembler:** Dynamic assembly of minimal token-efficient context packets containing only relevant sources, schemas, and upstream artifacts.
2. **Deterministic Step Scheduler:** Orchestration runtime that advances workflow state machines only upon schema-verified artifact emission.
3. **Compare-And-Swap (CAS) State Transitions:** State aggregate transitions guarded by optimistic locking and constitutional invariants (`CA-CAN-04_WORKFLOW_PRIMITIVES.yaml`).

### 3.2 Agentic Development Workflows (ADWs)
- **SSSF (Single-Step Software Factory):** Deterministic micro-pipelines where a single prompt/agent pair consumes a typed input artifact and produces an audited output artifact.
- **Bi-Directional Review Loop:** Generation agents paired with adversarial reviewer agents (`cae-adversarial-reviewer`) before artifact promotion.

### 3.3 Error Recovery & Rollback Matrix
No workflow may execute without an explicit rollback and quarantine strategy:
- **Schema Failure:** Abort step, emit validation error report, quarantine intermediate output.
- **Timeout / Loop Detection:** Circuit-breaker abort, log `WORKFLOW_UNDER_SPECIFIED`, alert operator.
- **Constitutional Contradiction:** Escalate to Operator Gate with exact decision packet.
