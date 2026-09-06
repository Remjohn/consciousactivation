# Agent System Architecture Map

**Artifact ID:** CAE-ART-AAM-001  
**Status:** APPROVED  
**Total Governed Agents:** 19  
**Generated Date:** 2026-09-03T09:01:40.258525  

---

## 1. Governed Agent Inventory

| # | Agent ID | Role Name | Primary Level | Assigned Skills | Boundaries |
|---|---|---|---|---|---|
| 01 | `cae-adversarial-reviewer` | Adversarial Reviewer | `PRODUCT / INTENT` | `caebmad-operating-level`, `caebmad-review` | Must NOT ignore unreferenced files or broken traceability li... |
| 02 | `cae-agent-systems-analyst` | Agent Systems Analyst | `Level 04: AGENT` | `caebmad-operating-level` | Must NOT permit autonomous agents to assume operator-level c... |
| 03 | `cae-application-analyst` | Application Analyst | `Level 07: APPLICATION` | `caebmad-operating-level`, `caebmad-brownfield` | Must NOT alter production ports or live service bindings wit... |
| 04 | `cae-architecture-agent` | Architecture Agent | `Level 02: DOCUMENTATION` & `Level 07: APPLICATION` | `caebmad-operating-level`, `caebmad-architecture` | Must NOT specify unbounded or untyped API contracts.... |
| 05 | `cae-brownfield-auditor` | Brownfield Auditor | `Level 06: REPOSITORY` down through `Level 13: LINE / BLOCK` | `caebmad-operating-level`, `caebmad-brownfield` | Must NOT exceed delegated authority or assume operator const... |
| 06 | `cae-cli-script-analyst` | Script/CLI Analyst | `Level 08: SCRIPT / CLI` | `caebmad-operating-level`, `caebmad-brownfield` | Must NOT assume a script works without checking syntax and d... |
| 07 | `cae-code-forensics-analyst` | Code Forensics Analyst | `Level 11: FILE / TYPE / CLASS`, `Level 12: FUNCTION`, and `Level 13: LINE / BLOCK` | `caebmad-operating-level`, `caebmad-brownfield` | Must NOT exceed delegated authority or assume operator const... |
| 08 | `cae-data-analyst` | Data Analyst | `Level 09: DATABASE / TABLE` | `caebmad-operating-level`, `caebmad-brownfield` | Must NOT claim schema compatibility without verifying column... |
| 09 | `cae-delivery-agent` | Epic/Story Agent | `Level 03: PLAN` | `caebmad-operating-level`, `caebmad-epics-stories` | Must NOT create monolithic epics that span multiple unrelate... |
| 10 | `cae-documentation-analyst` | Documentation Analyst | `Level 02: DOCUMENTATION` | `caebmad-operating-level`, `caebmad-prd` | Must NOT delete conflicting documentation without recording ... |
| 11 | `cae-method-orchestrator` | Method Orchestrator | `Level 01: PRODUCT / INTENT` (descends to all levels for gating and coordination)` | `caebmad-operating-level`, `caebmad-help`, `caebmad-grill`, `caebmad-handoff` | Must NOT present multi-question compound prompts to the oper... |
| 12 | `cae-module-analyst` | Module Analyst | `Level 10: MODULE / DIRECTORY` | `caebmad-operating-level`, `caebmad-brownfield` | Must NOT bypass module public API exports.... |
| 13 | `cae-plan-analyst` | Plan Analyst | `Level 03: PLAN` | `caebmad-operating-level`, `caebmad-epics-stories` | Must NOT alter delivery sequencing without an explicit depen... |
| 14 | `cae-prd-agent` | Modular PRD Agent | `Level 02: DOCUMENTATION` | `caebmad-operating-level`, `caebmad-prd`, `caebmad-fr` | Must NOT conflate product requirements with specific impleme... |
| 15 | `cae-product-brief-agent` | Product Brief Agent | `Level 01: PRODUCT / INTENT` | `caebmad-operating-level`, `caebmad-product-brief` | Must NOT proceed without an approved Product Reconstruction ... |
| 16 | `cae-product-reconstructor` | Product Reconstructor | `Level 01: PRODUCT / INTENT` | `caebmad-operating-level`, `caebmad-product-reconstruction` | Must NOT score unread or unindexed documents.... |
| 17 | `cae-repository-analyst` | Repository Analyst | `Level 06: REPOSITORY` | `caebmad-operating-level`, `caebmad-brownfield` | Must NOT assume repository structure matches documentation w... |
| 18 | `cae-ux-agent` | UI/UX Agent | `Level 01: PRODUCT / INTENT` & `Level 07: APPLICATION` | `caebmad-operating-level`, `caebmad-ui` | Must NOT produce purely aesthetic designs without specifying... |
| 19 | `cae-workflow-factory-analyst` | Workflow/Factory Analyst | `Level 05: AI WORKFLOW / FACTORY` | `caebmad-operating-level` | Must NOT allow unvalidated handoffs between agents.... |

---

## 2. Global Boundary Rules

- No autonomous agent may promote an artifact to PROMOTED status without explicit Operator Gate ratification.
- Every agent must execute within its assigned operating level and record descent/ascent steps when crossing boundaries.
- Tool permissions are strictly bounded; destructive operations require human-in-the-loop authorization.

---

## 3. Communication & Delegation Topology

| Source Agent | Target Agent | Protocol | Validation Contract |
|---|---|---|---|
| `cae-method-orchestrator` | `cae-product-reconstructor` | `WORKFLOW_INVOCATION` | `schemas/product_reconstruction.schema.json` |
| `cae-product-reconstructor` | `cae-prd-agent` | `ARTIFACT_HANDOFF` | `schemas/prd_module.schema.json` |
| `cae-prd-agent` | `cae-delivery-agent` | `ARTIFACT_HANDOFF` | `schemas/epic_story.schema.json` |
| `cae-method-orchestrator` | `cae-adversarial-reviewer` | `REVIEW_REQUEST` | `schemas/constitution.schema.json` |
