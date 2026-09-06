# Command and Control Map

**Artifact ID:** CAE-ART-CCM-001  
**Status:** APPROVED  
**Total Command Suites:** 5  
**Generated Date:** 2026-09-03T11:07:50.422032  

---

## 1. Automation Script Suites

| Suite ID | Name | Script Path | Engine | Description | Verified Executable |
|---|---|---|---|---|---|
| `SUITE-REBUILD-VALIDATORS` | CAE-BMAD Rebuild Validation Suite | `docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/scripts/validate_rebuild.py` | `PYTHON` | Orchestrates multi-mandate schema checks, state machine vali... | YES |
| `SUITE-RESEARCH-INTAKE` | 216-Source Corpus Intake and Lineage Engine | `docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/scripts/intake_research_corpus.py` | `PYTHON` | Ingests baseline and extended research sources, performs sco... | YES |
| `SUITE-LEVEL-INVESTIGATOR` | 13-Level Engineering Investigation Tool | `docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/scripts/investigate_operating_levels.py` | `PYTHON` | Traverses 13 operating levels, audits doc-to-code drift, and... | YES |
| `SUITE-DOC-PLANNING-GEN` | Documentation & Planning System Generator | `docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/scripts/generate_doc_planning.py` | `PYTHON` | Compiles 5 PRD modules, Functional Requirements matrix, and ... | YES |
| `SUITE-AGENT-FACTORY-GEN` | Agent & Workflow Map Generator | `docs/cae/CAE-BMAD-Method-v0.3-GEMINI-REBUILD/CAE-BMAD-Method-v0.3/scripts/generate_agent_workflow_factory_maps.py` | `PYTHON` | Compiles the 19-agent architecture map and multi-agent facto... | YES |

---

## 2. CLI Entrypoints

| Command Name | Target Function | Package |
|---|---|---|
| `cae-validate` | `validate_rebuild:main` | `cae-bmad-method` |
| `cae-investigate` | `investigate_operating_levels:main` | `cae-bmad-method` |

---

## 3. Execution Test Summary

All 5 command suites verified executable in Python 3.12 environment with 100% successful exit codes.
