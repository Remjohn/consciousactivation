# Source Path Rebase Evidence

**Recorded:** 2026-07-14  
**Scope:** `SRC-001` through `SRC-010` local artifacts  
**Method:** Recursive local candidate discovery followed by byte-level SHA-256 comparison against `governance/SOURCE_REGISTER.json`.

The original `/mnt/data` mount is not available in this workspace. Paths were rebased only where a local artifact matched the registered SHA-256 exactly. No expected hash or size was changed.

| Source | Result | Evidence |
|---|---|---|
| `SRC-001` | `PASS` | Exact hash match at `D:/Work/Conscious Activations/CMF_ATOMIC_HARNESS_BUILDER_NEXT_SHARDED_PRD_V1_1.zip` |
| `SRC-002` | `PASS` | Exact hash match at `D:/Work/Conscious_Rivers/THE CMF STUDIO/CCP_CMF_ATOMIC_HARNESS_SPEC_BUILDER_V2_1 (2).zip` |
| `SRC-003` | `PASS` | Exact hash match at `D:/Work/Conscious_Rivers/THE CMF STUDIO/CCP_ACTIVATIVE_INTELLIGENCE_VISUAL_NARRATIVE_V1_BUNDLE.zip` |
| `SRC-004` | `PASS` | Exact hash match at `D:/Work/Conscious_Rivers/THE CMF STUDIO/VISUAL SYNTAX BUILDER (2).zip` |
| `SRC-005` | `PASS` | Exact hash match at `D:/Work/Conscious_Rivers/docs/architecture.zip` |
| `SRC-006` | `PASS` | Exact hash match at `D:/Work/The Conscious Coaching Factory/docs/prd/modules.zip` |
| `SRC-007` | `PASS` | Exact hash match at `D:/Work/CCP_CMF_ATOMIC_HARNESS_SPEC_BUILDER_V2_1/references/skills/ccsb_paper.md` |
| `SRC-008` | `PASS` | Exact hash match at `D:/Work/CCP_CMF_ATOMIC_HARNESS_SPEC_BUILDER_V2_1/references/skills/achievement-story-design-brief-v1.2.yaml` |
| `SRC-009` | `FAIL` | No exact hash match after scanning 2,618 text files under `D:/Work`, the active attachment store, and the Codex artifact directory. Registered path remains unchanged. |
| `SRC-010` | `PASS` | Exact hash match at `D:/Work/The Conscious Coaching Factory/Conscious Architect University.zip` |

## Disposition

Nine source-integrity failures are closed by exact-content path rebasing. `SRC-009` remains a hard source-integrity blocker; the registered artifact or another byte-identical copy must be supplied. The package validator must continue to fail closed until that artifact is restored.
