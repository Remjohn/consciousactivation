# Repository Reality Map

**Artifact ID:** CAE-ART-RRM-001  
**Status:** APPROVED  
**Root Path:** `d:\Work\consciousactivation`  
**Hygiene Verdict:** `GOVERNED`  
**Generated Date:** 2026-09-03T11:07:50.402896  

---

## 1. Managed Workspace Directories

| Path | Purpose | Managed By | File Count Estimate |
|---|---|---|---|
| `services/` | Deployable microservices and runtime pipelines | `cae-application-analyst` | 50+ files across 5 services |
| `packages/` | Shared Python runtime libraries and primitives (ca_runtime) | `cae-module-analyst` | 20+ core library files |
| `programs/` | AI workflow programs and multi-agent factory specs | `cae-workflow-factory-analyst` | 15+ workflow definitions |
| `docs/` | Specifications, PRDs, constitutions, and CAE-BMAD rebuild assets | `cae-documentation-analyst` | 100+ documents |
| `governance/` | Program status exports and cross-repo contract fixtures | `cae-plan-analyst` | 25+ governance files |
| `scripts/` | Platform utility scripts, migration tools, and validators | `cae-cli-script-analyst` | 30+ executable scripts |
| `tests/` | Automated pytest suites and contract verification harnesses | `cae-adversarial-reviewer` | 50+ test files |

---

## 2. Cross-Repository Contracts

| Contract Name | Schema Path | Verified Valid |
|---|---|---|
| Evidence Source Contract | `docs/cae/constitutions/CA-CAN-01B_EVIDENCE_SOURCE.yaml` | YES |
| State Aggregate Contract | `docs/cae/constitutions/CA-CAN-02_STATE_AGGREGATE.yaml` | YES |
| Workflow Primitives Contract | `docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml` | YES |

---

## 3. Orphaned or Legacy Paths

- Conscious Activation Engine Brownfield/intelligence archive files/ (Historical Archive)
- .tmp/ (Transient build caches)
