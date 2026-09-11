# Workflow and Factory Map

**Artifact ID:** CAE-ART-WFM-001  
**Status:** DRAFT  
**Generated Date:** {{GENERATED_DATE}}

---

## 1. AI Factory Primitives
| Primitive ID | Name | Description | Runtime Binding |
|---|---|---|---|
| `{{PRIM_ID}}` | {{PRIM_NAME}} | {{PRIM_DESC}} | `{{RUNTIME_BINDING}}` |

---

## 2. Multi-Agent Workflow Pipelines
### {{PIPELINE_ID}}: {{PIPELINE_NAME}}
- **Trigger:** `{{TRIGGER}}`
- **Terminal Condition:** `{{TERMINAL_COND}}`
- **Rollback Strategy:** {{ROLLBACK_STRAT}}

**Pipeline Steps:**
| Step # | Agent | Action | Output Artifact |
|---|---|---|---|
| {{STEP_NUM}} | `{{STEP_AGENT}}` | {{STEP_ACTION}} | `{{STEP_ARTIFACT}}` |

---

## 3. Agentic Development Workflow (ADW) Patterns
- **Pattern:** {{PATTERN_NAME}}
- **Description:** {{PATTERN_DESC}}
- **JIT Context Strategy:** {{JIT_STRAT}}

---

## 4. Error Recovery & Rollback Matrix
| Error Type | Detection Agent | Recovery Action | Escalation Required |
|---|---|---|---|
| `{{ERROR_TYPE}}` | `{{DETECT_AGENT}}` | {{RECOVERY_ACTION}} | {{ESCALATE}} |
