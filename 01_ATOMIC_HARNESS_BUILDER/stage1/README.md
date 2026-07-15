# Stage 1 Audit Package

This directory is the evidence-backed Stage 1 output for CMF Atomic Harness Builder Next. It contains no production implementation changes.

| Artifact | Purpose |
|---|---|
| `CODEBASE_INVENTORY.md` | Human-readable code, schema, test, workflow, documentation, and deployment inventory |
| `PRD_PACKAGE_FILE_INVENTORY.csv` | Per-file path, size, SHA-256, and inspection result for the complete primary PRD package |
| `REPOSITORY_FILE_INVENTORY.csv` | Per-file path, size, SHA-256, asset class, and inspection result for the brownfield bundle |
| `REQUIREMENT_COVERAGE_MATRIX.csv` | One row for every FR, NFR, locked decision, anti-goal, and hard gate |
| `ARCHITECTURE_BASELINE_MANIFEST.yaml` | Machine-readable observed architecture baseline |
| `DELTA_ADR_REGISTER.md` | Proposed architecture-decision work required by the PRD delta |
| `TECHNICAL_SPECIFICATION_PLAN.md` | Ordered plan for specification authoring after blockers are resolved |
| `STAGE_1_READINESS_REPORT.md` | Stage conclusion, blockers, and proceed verdict |
| `STAGE1_EVIDENCE_SUMMARY.json` | Generated counts, hashes, parse results, and matrix completeness |
| `generate_stage1_evidence.py` | Reproducible audit generator; reads but does not modify the source bundle |

## Reproduction

From the PRD package root:

```powershell
python -B stage1\generate_stage1_evidence.py
python -B scripts\validate_prd_package.py
```

The brownfield live test command used by the audit was:

```powershell
Set-Location D:\Work\CCP_CMF_ATOMIC_HARNESS_SPEC_BUILDER_V2_1
python -B -c "import sys; sys.path.insert(0, 'src'); import pytest; raise SystemExit(pytest.main(['-q', '-p', 'no:cacheprovider']))"
```
