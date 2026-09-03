# Operating Level Assessment

**Artifact ID:** CAE-ART-OLA-001  
**Status:** DRAFT  
**Governing Method:** CAE-BMAD v0.3.0  
**Evaluating Agent:** `cae-documentation-analyst`  
**Assessment Date:** {{ASSESSMENT_DATE}}

---

## 1. 13-Level Fidelity Evaluation Summary

| Level # | Level Name | Analyst Agent | Fidelity Status | Primary Evidence Path |
|---|---|---|---|---|
| 01 | PRODUCT / INTENT | `cae-method-orchestrator` | {{L01_STATUS}} | `docs/cae-bmad/03_product/PRODUCT_BRIEF.md` |
| 02 | DOCUMENTATION | `cae-documentation-analyst` | {{L02_STATUS}} | `docs/PRD/CURRENT.md` |
| 03 | PLAN | `cae-plan-analyst` | {{L03_STATUS}} | `docs/cae-bmad/05_planning/EPICS.md` |
| 04 | AGENT | `cae-agent-systems-analyst` | {{L04_STATUS}} | `gemini_execution/agents/` |
| 05 | AI WORKFLOW / FACTORY | `cae-workflow-factory-analyst` | {{L05_STATUS}} | `programs/` |
| 06 | REPOSITORY | `cae-repository-analyst` | {{L06_STATUS}} | `WORKSPACE_MANIFEST.json` |
| 07 | APPLICATION | `cae-application-analyst` | {{L07_STATUS}} | `services/` |
| 08 | SCRIPT / CLI | `cae-cli-script-analyst` | {{L08_STATUS}} | `scripts/` |
| 09 | DATABASE / TABLE | `cae-data-analyst` | {{L09_STATUS}} | `storage/` |
| 10 | MODULE / DIRECTORY | `cae-module-analyst` | {{L10_STATUS}} | `packages/` |
| 11 | FILE / TYPE / CLASS | `cae-code-forensics-analyst` | {{L11_STATUS}} | `services/*/models/` |
| 12 | FUNCTION | `cae-code-forensics-analyst` | {{L12_STATUS}} | `services/*/application/` |
| 13 | LINE / BLOCK | `cae-brownfield-auditor` | {{L13_STATUS}} | `services/*/verifier.py` |

---

## 2. Multi-Level Investigation Findings
- **Finding 1:** {{FINDING_1}}
- **Finding 2:** {{FINDING_2}}

---

## 3. Documentation-to-Code Drift Matrix
| Component | Documented State | Codebase State | Drift Class | Recommended Remediation |
|---|---|---|---|---|
| {{COMPONENT}} | {{DOC_STATE}} | {{CODE_STATE}} | {{DRIFT_CLASS}} | {{REMEDIATION}} |

---

## 4. Remediation & Gate Recommendations
- {{RECOMMENDATIONS}}
