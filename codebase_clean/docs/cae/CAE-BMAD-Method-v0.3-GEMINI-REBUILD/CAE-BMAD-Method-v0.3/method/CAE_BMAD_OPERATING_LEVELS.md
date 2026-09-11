# CAE-BMAD Operating Level Framework

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL FRAMEWORK  
**Authority:** CAE Rebuild Program / Operator Mandate M01  
**Scope:** Engineering operating levels, traversal heuristics, agent mappings, and stop/ascent rules.

---

## 1. The 13 Engineering Operating Levels

The method structures all investigation, authoring, and verification across 13 discrete levels:

```text
Level 01: PRODUCT / INTENT
  - Mission, business model, problem statement, user value, operator outcomes.
Level 02: DOCUMENTATION
  - PRDs, technical specs, RFCs, operator manuals, markdown architecture guides.
Level 03: PLAN
  - Epics, user stories, milestones, delivery roadmaps, cutover plans.
Level 04: AGENT
  - AI personas, system prompts, role boundaries, tool definitions, agentic schemas.
Level 05: AI WORKFLOW / FACTORY
  - Multi-agent graphs, state pipelines, task handoffs, orchestration rules, retry policies.
Level 06: REPOSITORY
  - Git roots, directory trees, repo-level configurations, cross-repo dependency links.
Level 07: APPLICATION
  - Deployable services, web apps, API gateways, daemon runners, runtime processes.
Level 08: SCRIPT / CLI
  - Automation scripts, build tools, migration runners, CLI command entrypoints.
Level 09: DATABASE / TABLE
  - Database schemas, tables, indices, migrations, event stores, data dictionaries.
Level 10: MODULE / DIRECTORY
  - Packages, namespaces, subpackages, internal domain boundaries.
Level 11: FILE / TYPE / CLASS
  - Source code files, data classes, Pydantic schemas, TypeScript interfaces, domain models.
Level 12: FUNCTION
  - Concrete callable methods, endpoints, handlers, pure functions, algorithms.
Level 13: LINE / BLOCK
  - Exact lines of code, conditional statements, variable assignments, loops, assertions.
```

---

## 2. Agent Specialization Matrix

Each operating level is assigned a primary analytical agent:

| Level | Level Name | Primary Specialized Agent | Core Analytical Responsibility |
|---|---|---|---|
| 01 | PRODUCT / INTENT | `cae-method-orchestrator` / `cae-product-reconstructor` | Product mission, intent synthesis, phase governance |
| 02 | DOCUMENTATION | `cae-documentation-analyst` / `cae-prd-agent` | Specification auditing, PRD authoring, document drift |
| 03 | PLAN | `cae-plan-analyst` / `cae-delivery-agent` | Milestone genealogy, epic/story sizing, dependency order |
| 04 | AGENT | `cae-agent-systems-analyst` | Agent prompt auditing, tool boundary enforcement, role drift |
| 05 | AI WORKFLOW / FACTORY | `cae-workflow-factory-analyst` | Multi-agent pipelines, handoff contracts, orchestration failure |
| 06 | REPOSITORY | `cae-repository-analyst` | Workspace mapping, cross-repo contracts, directory hygiene |
| 07 | APPLICATION | `cae-application-analyst` | Service entrypoints, API contracts, deployment configurations |
| 08 | SCRIPT / CLI | `cae-cli-script-analyst` | CLI parsers, automation scripts, operational tooling |
| 09 | DATABASE / TABLE | `cae-data-analyst` | Schemas, table definitions, migration drift, event logs |
| 10 | MODULE / DIRECTORY | `cae-module-analyst` | Domain boundaries, import graphs, circular dependencies |
| 11 | FILE / TYPE / CLASS | `cae-code-forensics-analyst` | Class hierarchies, typed interfaces, data structures |
| 12 | FUNCTION | `cae-code-forensics-analyst` | Function signatures, return contracts, error handling |
| 13 | LINE / BLOCK | `cae-code-forensics-analyst` / `cae-brownfield-auditor` | Exact code execution, AST analysis, mutation reality |

Cross-cutting review: `cae-adversarial-reviewer` inspects all levels for false-proof, lineage loss, and unsupported claims.

---

## 3. Stack Traversal Rules

### 3.1 Descent Trigger Heuristics (Top-Down)
An agent must descend down the stack when:
1. **Ambiguity:** High-level documentation does not clearly define operational behavior.
2. **Contradiction:** Stated documentation or user requirements disagree with existing codebase logic.
3. **Missing Implementation:** An abstract claim has no identifiable runtime counterpart.
4. **Failure Investigation:** A test or workflow execution fails, requiring root-cause tracing down to functions and lines.
5. **High-Risk Change:** Modifying a core protocol or shared schema demands inspecting all downstream call sites.

**Descent Stop Condition:** Descent terminates as soon as concrete, verifiable ground truth is reached (e.g. the exact line, schema, or test that proves or disproves the assertion).

### 3.2 Ascent Trigger Heuristics (Bottom-Up)
An agent ascends up the stack when:
1. **Empirical Generalization:** Repeated low-level code patterns justify creating a shared module, script, or workflow abstraction.
2. **Reality Verification:** Lower-level code and passing tests validate that a technical specification or PRD requirement is satisfied.
3. **Artifact Promotion:** Implementation and verification evidence is aggregated into high-level milestone and release reports for operator gate approval.

**Ascent Condition:** Ascent is permitted only when backed by empirical evidence gathered from the lower levels.
