# Workflow and Factory Map

**Artifact ID:** CAE-ART-WFM-001  
**Status:** APPROVED  
**Generated Date:** 2026-09-03T09:01:40.261944  

---

## 1. AI Factory Primitives

| Primitive ID | Name | Description | Runtime Binding |
|---|---|---|---|
| `PRIM-01` | JIT Context Capsule Assembler | Assembles minimal token-efficient context packets containing only active schemas, lineage cards, and upstream inputs. | `packages/ca_runtime/src/ca_runtime/agent_invocation.py` |
| `PRIM-02` | Deterministic Step Scheduler | Advances workflow state machines sequentially only upon schema verification of output artifacts. | `services/pipeline/src/cmf_pipeline/workflow/application/compiler.py` |
| `PRIM-03` | Compare-And-Swap State CAS Runtime | Guarantees atomic, optimistic locking state mutations preventing race conditions across multi-agent execution. | `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` |

---

## 2. Multi-Agent Workflow Pipelines

### PIPE-M01: Constitution and Method Contract Rebuild
- **Trigger:** `Gemini Activation Prompt M01`
- **Terminal Condition:** All 10 M01 tests pass and operator approves gate.
- **Rollback Strategy:** Quarantine generated schemas and revert to baseline constitution stubs.

| Step # | Agent | Action | Output Artifact |
|---|---|---|---|
| 1 | `cae-method-orchestrator` | Author Constitution & Governance | `CAE_BMAD_CONSTITUTION.md` |
| 2 | `cae-adversarial-reviewer` | Run Countertests & Boundary Checks | `OPERATOR_GATE_M01.md` |

### PIPE-M02: 216-Source Research Library Intake
- **Trigger:** `Gemini Activation Prompt M02`
- **Terminal Condition:** Exact 216 sources validated against schema with zero unclassified sources.
- **Rollback Strategy:** Purge .caebmad/research/ output and reload 144-source baseline catalog.

| Step # | Agent | Action | Output Artifact |
|---|---|---|---|
| 1 | `cae-product-reconstructor` | Ingest 216 Sources and Score Relevance | `CAE_RESEARCH_LIBRARY.yaml` |
| 2 | `cae-adversarial-reviewer` | Verify Anti-Flattening Invariants | `OPERATOR_GATE_M02.md` |

### PIPE-M03: Multi-Level Engineering Investigation
- **Trigger:** `Gemini Activation Prompt M03`
- **Terminal Condition:** All 13 levels evaluated with concrete filesystem evidence paths.
- **Rollback Strategy:** Revert assessment deliverables to DRAFT status and log investigation errors.

| Step # | Agent | Action | Output Artifact |
|---|---|---|---|
| 1 | `cae-documentation-analyst` | Scan 13 Operating Levels | `OPERATING_LEVEL_ASSESSMENT.json` |
| 2 | `cae-brownfield-auditor` | Identify Code Drift and Broken References | `OPERATOR_GATE_M03.md` |

### PIPE-M04: Product Intent and Lineage Reconstruction
- **Trigger:** `Gemini Activation Prompt M04`
- **Terminal Condition:** All 5 Capability Pillars defined with verified code paths and 216 sources analyzed.
- **Rollback Strategy:** Revert reconstruction record and re-evaluate capability pillar extraction.

| Step # | Agent | Action | Output Artifact |
|---|---|---|---|
| 1 | `cae-product-reconstructor` | Synthesize 5 Capability Pillars | `PRODUCT_RECONSTRUCTION.json` |
| 2 | `cae-brownfield-auditor` | Map Brownfield Code Crosswalks | `OPERATOR_GATE_M04.md` |

---

## 3. Agentic Development Workflow (ADW) Patterns

### ADW-SSSF: Single-Step Software Factory (SSSF)
Deterministic step execution pattern where an agent receives a strictly typed context capsule and produces an audited artifact.

- **JIT Capsule Strategy:** Inject only target schema, input artifact, and specific operating level boundaries.

### ADW-ADV-LOOP: Adversarial Review Loop
Two-agent pattern where a generator agent's output is subjected to countertests and false-proof defenses by cae-adversarial-reviewer.

- **JIT Capsule Strategy:** Inject generated artifact, countertest rules, and constitutional boundary checks.

---

## 4. Error Recovery & Rollback Matrix

| Error Type | Detection Agent | Recovery Action | Operator Escalation |
|---|---|---|---|
| `SCHEMA_VALIDATION_ERROR` | `cae-method-orchestrator` | Reject artifact, emit error diagnostics, retry with corrected parameters. | NO |
| `CONTRADICTION_UNRESOLVED` | `cae-adversarial-reviewer` | Log in Decision Ledger, halt pipeline, generate Operator Gate packet. | YES |
| `INFINITE_DESCENT_LOOP` | `cae-brownfield-auditor` | Circuit-breaker abort, log WORKFLOW_UNDER_SPECIFIED, return to parent level. | NO |
