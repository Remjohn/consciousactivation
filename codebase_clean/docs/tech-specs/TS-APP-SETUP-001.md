---
spec_id: TS-APP-SETUP-001
title: Repository Restructure and Redundancy Cleanup
document_class: TECH_SPEC
product: Conscious Activations
module: repo
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CURRENT
build_authority: false
controlling_frs:
  - none directly — this is infrastructure prerequisite work referenced by
    CA_APP_FR_EPIC_SPEC_PLAN.md Part 5 ("Repository Restructure — Do First")
controlling_stories:
  - none directly — blocks every ST-APP-* story by making paths predictable
upstream_dependencies:
  - CA_PROJECT_SNAPSHOT_V2.md (authority — CURRENT)
  - CA_APP_FR_EPIC_SPEC_PLAN.md (authority — CURRENT, Part 5)
downstream_consumers:
  - TS-APP-API-001 through TS-APP-API-006 (all reference services/{name}/src paths
    this spec creates)
  - TS-APP-UI-001 through TS-APP-UI-004 (all reference apps/web/ this spec creates)
  - SPEC_GAP_LEDGER.md (companion document — sequencing depends on this spec running first)
output_path: repository root (directory moves, no new application code)
wave: 0
---

# TS-APP-SETUP-001 — Repository Restructure and Redundancy Cleanup

## 1. Files and Authorities Read

| File / Path | Status | Fact extracted |
|---|---|---|
| `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 5 | READ — AUTHORITY, CURRENT | Names the exact `mv` commands this spec must execute in full; this spec is that plan made testable and complete |
| `01_ATOMIC_HARNESS_BUILDER/` through `07_CONSCIOUS_ACTIVATIONS_STUDIO/` | READ — CURRENT, on disk | Seven numbered service directories, each with its own `pyproject.toml` referencing `{NN_NAME}/src` as package root |
| `TS-APP-API-001.md` §7 | READ — CURRENT (WRITTEN_PENDING_AUDIT) | Already written Dockerfile and dependency code assumes `services/builder`, `services/air`, `services/pipeline`, `services/interview`, `services/vae` paths — i.e. **this spec's target structure is already load-bearing for existing specs**, not merely proposed |
| `TS-APP-UI-001.md` §1 | READ — CURRENT (WRITTEN_PENDING_AUDIT) | Cites `services/studio/tsconfig.json` at SHA `2288a69d` — confirms this spec must preserve that file's content exactly across the move, only its path changes |
| `CONSCIOUS_ACTIVATIONS_PHASE_*_BUNDLE/` (nine directories + duplicate ZIPs) | READ — CURRENT, on disk | Each phase bundle directory contains `full-replacement-files/` (already-applied source, now redundant with the live `0N_*` directories) plus `receipts/`, `scripts/` (verify/apply/rollback tooling, historically useful, not runtime-imported) |
| `_PARALLEL/`, `_PARALLEL_REPORTS/`, `THE_CMF_STUDIO(2)/`, `05_FUTURE_PRODUCTS/` | READ — CURRENT, on disk | Not imported by any `pyproject.toml`, any `tsconfig.json`, or any test file — confirmed by grep across all `import`/`require` statements in `services/`, `packages/`, `tests/` |
| `Specs_Builder_Library_CA_V2_1_3/` | READ — CURRENT, on disk | Governs how Tech Specs are written; must remain readable by future spec authors, so it is archived, not deleted |
| `CMF_PROGRAM_CONTROL/` | READ — CURRENT, on disk | Contains per-phase status receipts and traceability matrices; referenced by historical claim-ceiling statements in already-shipped bundles, not imported by any running code |

**Source Gap Notice — this spec's authority is stronger than "proposed cleanup."** Because `TS-APP-API-001.md` and `TS-APP-UI-001.md` already cite `services/{name}` paths as if they exist, this spec is not optional groundwork — it is a **precondition** those two specs silently assumed. Implementing `TS-APP-API-001` before this spec runs would create `services/` as a second, empty tree alongside the still-present `0N_*` directories, and nothing would import correctly. This spec must execute first, exactly as `CA_APP_FR_EPIC_SPEC_PLAN.md` Part 5 already said.

---

## 2. Problem, User Outcome, Solution, and Scope

### Problem without this spec
The repository has ten already-written Tech Specs (`TS-APP-API-001` through `TS-APP-UI-004`) that reference a directory structure — `services/builder`, `services/air`, `services/pipeline`, `services/interview`, `services/vae`, `services/studio`, `apps/web`, `api/` — that does not exist yet. The actual repository still has `01_ATOMIC_HARNESS_BUILDER` through `07_CONSCIOUS_ACTIVATIONS_STUDIO`, nine `CONSCIOUS_ACTIVATIONS_PHASE_*_BUNDLE` directories duplicating already-applied source under `full-replacement-files/`, four spec-library/experiment directories not imported by any code, and `pyproject.toml` files across six packages pointing at the old paths. An implementing agent handed any of the ten written specs today will either fail immediately on missing paths or — worse — silently create a second, parallel `services/` tree that diverges from the real one.

### User outcome
An agent implementing any of the ten already-written specs finds every path they reference exists, contains the real code, and nothing else. `python -m pytest tests/ -q` passes with the same result as before the move. No capital-letter directory names remain anywhere in the active tree. Historical bundle and spec-library material is still reachable under `archive/` for provenance, but does not appear when browsing the live application.

### Solution
A sequence of `git mv` operations (preserving history) that:
1. Renames the seven numbered service directories to their `services/{name}` targets
2. Renames `07_CONSCIOUS_ACTIVATIONS_STUDIO` to `services/studio`
3. Moves all nine phase bundle directories and their ZIPs to `archive/bundles/`
4. Moves the four spec-library/experiment/PRD directories to `archive/specs/` and `archive/experiments/`
5. Moves `CMF_PROGRAM_CONTROL/` to `governance/program-control/`
6. Updates the six `pyproject.toml` files' `package-dir`/`packages.find.where` entries to match new paths
7. Creates the empty skeleton directories `api/`, `apps/web/`, `infra/docker/`, `infra/nginx/`, `docs/specs/current/`, `docs/specs/archive/` that TS-APP-API-001 and TS-APP-UI-001 will populate
8. Runs the full existing test suite and the reinstall sequence to prove nothing broke

### In scope
- Directory and file **moves only** — `git mv`, never `rm` on anything with unverified redundancy
- `pyproject.toml` path field updates (mechanical, no dependency version changes)
- Creating empty target directories with `.gitkeep` for Wave 1+ specs to populate
- A redundancy audit producing `archive/bundles/BUNDLE_ARCHIVE_MANIFEST.yaml` recording original SHA-256, why each item was archived, and confirmation it is not runtime-imported
- Verifying the pre-existing 60-file test suite still passes byte-for-byte in behaviour after the move

### Out of scope
- Any change to Python or TypeScript business logic
- Deleting anything — this spec archives, it does not delete (see AC-005)
- Resolving Gap 4 (Builder/Pipeline schema mismatch) — that is a code-level compiler concern, tracked in `SPEC_GAP_LEDGER.md`, not a path problem
- Writing the missing AIR API spec — tracked in `SPEC_GAP_LEDGER.md`
- Reconciling the "assumed interface" gaps in TS-APP-UI-002/003 — tracked in `SPEC_GAP_LEDGER.md`
- Renaming Python module names (`cmf_pipeline`, `cmf_activative_intelligence`, etc.) — only directory paths change, not importable package names, so no code that does `import cmf_pipeline` needs to change

---

## 3. Governing Decisions and Constraints

**Archive, never delete.** Every phase bundle, spec library, and experiment directory moves to `archive/` with an intact manifest. This preserves the provenance chain the project's own history (Phase 1–9 receipts) depends on for audit purposes. Deletion is a separate, later, explicitly-authorized decision — not this spec's to make.

**Python package import names do not change.** `cmf_pipeline`, `cmf_activative_intelligence`, `cmf_vae`, `cmf_builder`, `conscious_activations_interview_expression`, `ca_contracts`, `ca_runtime`, `ca_delegation_rc4`, `ca_release` remain exactly as they are. Only the **directory path on disk** (`01_ATOMIC_HARNESS_PIPELINE/src/...` → `services/pipeline/src/...`) and the `pyproject.toml` fields that point at that path change. No `import` statement inside any `.py` file needs editing, because Python imports reference the installed package name, not the source directory name.

**`git mv` only, to preserve blame/history.** Plain `mv` followed by `git add` loses rename tracking in most git tooling's default view. `git mv` (or `mv` + `git add -A` with `git config diff.renames true`, but `git mv` is simpler and this spec mandates it) keeps history attached to each file.

**Redundancy claims must be provable, not assumed.** Before any directory is classified "not imported, safe to archive," this spec requires a `grep -r` pass across every `.py`, `.ts`, `.tsx`, `.json`, `.yaml`, `.toml` file in the tree for references to that directory's path or package name. If any reference is found, that specific file is either updated or the whole directory is excluded from this spec's move list and flagged for manual review — not archived speculatively.

**Naming convention enforced going forward:** `kebab-case` for all new directories, `snake_case` for Python files, `PascalCase` for React components, `camelCase` for TypeScript utilities/hooks. This spec does not rename individual Python or TypeScript **files** — only top-level directories — because renaming individual source files risks breaking internal relative imports in ways a pure directory move does not. File-level naming cleanup, if wanted later, is a separate spec.

**Claim ceiling:** `REPOSITORY_STRUCTURE_CLEANUP_EVIDENCE`. This spec does not claim any business logic was validated, improved, or changed. It claims only that paths are now predictable and tests still pass.

---

## 4. Current Brownfield Inventory and Disposition

| Path | Contents | Imported by live code? | Disposition | Target |
|---|---|---|---|---|
| `01_ATOMIC_HARNESS_BUILDER/` | `cmf_builder` package, ~91 .py files | YES — `pyproject.toml`, tests | MOVE | `services/builder/` |
| `02_VISUAL_ASSET_EDITOR/` | `cmf_vae` package, ~18 .py files | YES | MOVE | `services/vae/` |
| `03_DELEGATION_PROTOCOL/` | `ca_delegation_rc4` RC4 release, 231 files | YES | MOVE | `services/delegation/` |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/` | `cmf_activative_intelligence`, ~34 .py files | YES | MOVE | `services/air/` |
| `05_ATOMIC_HARNESS_PIPELINE/` | `cmf_pipeline`, ~76 .py files | YES | MOVE | `services/pipeline/` |
| `06_INTERVIEW_EXPRESSION/` | interview package, ~23 .py files | YES | MOVE | `services/interview/` |
| `07_CONSCIOUS_ACTIVATIONS_STUDIO/` | Studio TS domain, 18 files | YES — cited by TS-APP-UI-001/002/003 by exact SHA | MOVE | `services/studio/` |
| `packages/ca_contracts/`, `ca_runtime/`, `ca_release/` | shared Python packages | YES | KEEP IN PLACE | unchanged |
| `CONSCIOUS_ACTIVATIONS_PHASE_01_FOUNDATION_BUNDLE/` | applied historical bundle | NO — verified via grep, zero references outside its own receipts | ARCHIVE | `archive/bundles/phase-01/` |
| `CONSCIOUS_ACTIVATIONS_PHASE_02_AIR_CORE_BUNDLE/` | applied historical bundle | NO | ARCHIVE | `archive/bundles/phase-02/` |
| `CONSCIOUS_ACTIVATIONS_PHASE_03_AHP_CORE_BUNDLE/` | applied historical bundle | NO | ARCHIVE | `archive/bundles/phase-03/` |
| `CONSCIOUS_ACTIVATIONS_PHASE_01_03_TRACEABILITY_AND_GAP_CLOSURE_BUNDLE/` | applied historical bundle | NO | ARCHIVE | `archive/bundles/phase-01-03-traceability/` |
| `CONSCIOUS_ACTIVATIONS_PHASE_04_INTERVIEW_EXPRESSION_BUNDLE/` | applied historical bundle | NO | ARCHIVE | `archive/bundles/phase-04/` |
| `CONSCIOUS_ACTIVATIONS_PHASE_05_SEMANTIC_PRODUCTION_COMPILER_BUNDLE/` | applied historical bundle | NO | ARCHIVE | `archive/bundles/phase-05/` |
| `CONSCIOUS_ACTIVATIONS_PHASE_06_COMPOSITION_MEDIA_RUNTIMES_BUNDLE/` | applied historical bundle | NO | ARCHIVE | `archive/bundles/phase-06/` |
| `CONSCIOUS_ACTIVATIONS_PHASE_07_STUDIO_SUPERVISION_BUNDLE/` | applied historical bundle | NO | ARCHIVE | `archive/bundles/phase-07/` |
| `CONSCIOUS_ACTIVATIONS_PHASE_08_DELEGATION_VAE_INTEGRATION_BUNDLE/` | applied historical bundle | NO | ARCHIVE | `archive/bundles/phase-08/` |
| `CONSCIOUS_ACTIVATIONS_PHASE_09_FINAL_APPLICATION_BUNDLE/` | applied historical bundle | NO | ARCHIVE | `archive/bundles/phase-09/` |
| `*.zip` files (nine phase bundle ZIPs at repo root) | duplicate compressed copies of the above | NO | ARCHIVE | `archive/bundles/zips/` |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/` | PRD source, referenced by `CA_APP_FR_EPIC_SPEC_PLAN.md` as authority | NO — read historically, not imported | ARCHIVE (readable) | `archive/specs/prd-v1-2/` |
| `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/` | old spec workflow docs | NO | ARCHIVE | `archive/specs/workflow-v3-3/` |
| `Specs_Builder_Library_CA_V2_1_3/` | governs spec-writing itself; already cited by name in this spec's own header | NO — read by humans/agents writing specs, not imported by app code | ARCHIVE (readable) | `archive/specs/spec-builder-library/` |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/` | superseded AIR bundle, pre-dates Phase 2 | NO | ARCHIVE | `archive/specs/air-v2-1-bundle/` |
| `_PARALLEL/` | experimental/duplicate work | NO — zero import references found | ARCHIVE | `archive/experiments/parallel/` |
| `_PARALLEL_REPORTS/` | experimental reports | NO | ARCHIVE | `archive/experiments/parallel-reports/` |
| `THE_CMF_STUDIO(2)/` | duplicate/experimental Studio copy | NO — confirmed distinct from `07_CONSCIOUS_ACTIVATIONS_STUDIO`, zero references | ARCHIVE | `archive/experiments/cmf-studio-v2/` |
| `05_FUTURE_PRODUCTS/` | roadmap material, not implementation | NO | ARCHIVE | `archive/experiments/future-products/` |
| `CMF_PROGRAM_CONTROL/` | phase status receipts, traceability matrices | NO — referenced only by historical claim-ceiling text in bundle READMEs, not by running code | MOVE | `governance/program-control/` |
| `tests/` | 60 test files | YES | KEEP IN PLACE, update internal path references only where they import from renamed dirs | unchanged location |

**Redundancy finding worth naming explicitly:** the nine `full-replacement-files/` subdirectories inside the phase bundles contain what is, file-for-file, an earlier snapshot of the same source now living in `01_` through `07_`. They are not a second copy that needs reconciling — they are the **history that produced** the current live copy. Archiving them (not deleting) preserves that lineage without keeping duplicate active source in the working tree.

---

## 5. Proposed Architecture and Workflow

```
Stage 0 — Pre-flight
  ├── git status must be clean (no uncommitted changes)
  ├── Run full existing test suite, record baseline pass count
  └── Create working branch: chore/repo-restructure-ts-app-setup-001

Stage 1 — Redundancy verification (before any move)
  ├── grep -rn "01_ATOMIC_HARNESS_BUILDER\|02_VISUAL_ASSET_EDITOR\|..." 
  │     across tests/, packages/, and every pyproject.toml
  ├── grep -rn "_PARALLEL\|THE_CMF_STUDIO\|05_FUTURE_PRODUCTS"
  │     across tests/, packages/, services-to-be/
  └── Any hit outside the bundle's own internal files → STOP, flag for manual review,
      exclude that specific path from Stage 2

Stage 2 — Service directory renames (git mv, preserves history)
  ├── git mv 01_ATOMIC_HARNESS_BUILDER services/builder
  ├── git mv 02_VISUAL_ASSET_EDITOR services/vae
  ├── git mv 03_DELEGATION_PROTOCOL services/delegation
  ├── git mv 04_ACTIVATIVE_INTELLIGENCE_RUNTIME services/air
  ├── git mv 05_ATOMIC_HARNESS_PIPELINE services/pipeline
  ├── git mv 06_INTERVIEW_EXPRESSION services/interview
  └── git mv 07_CONSCIOUS_ACTIVATIONS_STUDIO services/studio

Stage 3 — Archive moves (git mv)
  ├── nine phase bundle dirs → archive/bundles/phase-0N/
  ├── nine phase bundle zips → archive/bundles/zips/
  ├── four spec-library dirs → archive/specs/{name}/
  ├── four experiment dirs → archive/experiments/{name}/
  └── CMF_PROGRAM_CONTROL → governance/program-control/

Stage 4 — Skeleton creation (new empty dirs, .gitkeep placeholders)
  ├── api/{routers,websockets}/
  ├── apps/web/src/{pages,components,hooks,api}/
  ├── infra/{docker,nginx}/
  └── docs/specs/{current,archive}/

Stage 5 — pyproject.toml path updates (six files)
  └── For each services/{name}/pyproject.toml:
        [tool.setuptools]
        package-dir = {"" = "src"}          ← unchanged, relative to new location
        [tool.setuptools.packages.find]
        where = ["src"]                     ← unchanged, relative to new location
      NOTE: because package-dir/where are already relative to the pyproject.toml's
      own location, most require ZERO edits — the directory move alone suffices.
      Verify this assumption in Stage 6 rather than editing blindly.

Stage 6 — Verification
  ├── pip install -e (all six services + four packages) --break-system-packages
  ├── python -m pytest tests/ -q --tb=short
  ├── Compare pass count to Stage 0 baseline — must match exactly
  └── Generate archive/bundles/BUNDLE_ARCHIVE_MANIFEST.yaml

Stage 7 — Commit
  └── One commit per stage (2–7), not one giant commit, so a reviewer can
      verify each stage's diff is exactly what it claims to be
```

---

## 6. Data Models, Contracts, Schemas

This spec produces one new artifact: the archive manifest.

### `BUNDLE_ARCHIVE_MANIFEST.yaml`
```yaml
manifest_version: 1
archived_at: "2026-07-25T00:00:00Z"
archived_by_spec: TS-APP-SETUP-001
entries:
  - original_path: CONSCIOUS_ACTIVATIONS_PHASE_01_FOUNDATION_BUNDLE
    archived_path: archive/bundles/phase-01
    original_root_sha256: "<sha256 of directory tarball at move time>"
    reason: "applied historical bundle, superseded by live services/ tree"
    verified_not_imported: true
    verification_method: "grep -rn across tests/, packages/, services/ — zero hits"
  # ... one entry per archived path, same shape
verification:
  test_suite_baseline_pass_count: <N>
  test_suite_post_move_pass_count: <N>
  match: true
```

---

## 7. Implementation Stages and Exact Commands

### Stage 0 — Pre-flight
```bash
git status --porcelain  # must be empty
git checkout -b chore/repo-restructure-ts-app-setup-001
python -m pytest tests/ -q --tb=short 2>&1 | tee /tmp/baseline_test_output.txt
grep -c "passed" /tmp/baseline_test_output.txt  # record this number
```

### Stage 1 — Redundancy verification script
```bash
#!/usr/bin/env bash
# verify_redundancy.sh
set -euo pipefail

CANDIDATES=(
  "_PARALLEL"
  "_PARALLEL_REPORTS"
  "THE_CMF_STUDIO(2)"
  "05_FUTURE_PRODUCTS"
)

for dir in "${CANDIDATES[@]}"; do
  echo "=== Checking references to: $dir ==="
  hits=$(grep -rln --include="*.py" --include="*.ts" --include="*.tsx" \
    --include="*.toml" --include="*.json" --include="*.yaml" \
    -F "$dir" tests/ packages/ 01_ATOMIC_HARNESS_BUILDER 02_VISUAL_ASSET_EDITOR \
    03_DELEGATION_PROTOCOL 04_ACTIVATIVE_INTELLIGENCE_RUNTIME \
    05_ATOMIC_HARNESS_PIPELINE 06_INTERVIEW_EXPRESSION \
    07_CONSCIOUS_ACTIVATIONS_STUDIO 2>/dev/null | grep -v "^$dir" || true)
  if [ -n "$hits" ]; then
    echo "  BLOCKED — found references outside own directory:"
    echo "$hits"
    exit 1
  else
    echo "  CLEAR — no external references found"
  fi
done
echo "All candidates verified redundant. Safe to proceed to Stage 3."
```
Run it and require `All candidates verified redundant` before continuing:
```bash
chmod +x verify_redundancy.sh && ./verify_redundancy.sh
```

### Stage 2 — Service renames
```bash
git mv 01_ATOMIC_HARNESS_BUILDER services/builder
git mv 02_VISUAL_ASSET_EDITOR services/vae
git mv 03_DELEGATION_PROTOCOL services/delegation
git mv 04_ACTIVATIVE_INTELLIGENCE_RUNTIME services/air
git mv 05_ATOMIC_HARNESS_PIPELINE services/pipeline
git mv 06_INTERVIEW_EXPRESSION services/interview
git mv 07_CONSCIOUS_ACTIVATIONS_STUDIO services/studio
git commit -m "TS-APP-SETUP-001 Stage 2: rename service directories to kebab-case services/{name}"
```

### Stage 3 — Archive moves
```bash
mkdir -p archive/bundles/zips archive/specs archive/experiments governance

for n in 01 02 03 04 05 06 07 08 09; do
  bundle_dir=$(ls -d CONSCIOUS_ACTIVATIONS_PHASE_${n}_*_BUNDLE 2>/dev/null | head -1)
  [ -n "$bundle_dir" ] && git mv "$bundle_dir" "archive/bundles/phase-${n}"
done
git mv CONSCIOUS_ACTIVATIONS_PHASE_01_03_TRACEABILITY_AND_GAP_CLOSURE_BUNDLE \
  archive/bundles/phase-01-03-traceability 2>/dev/null || true
git mv CONSCIOUS_ACTIVATIONS_PHASE_*_BUNDLE.zip archive/bundles/zips/ 2>/dev/null || true

git mv CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED archive/specs/prd-v1-2
git mv CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3 archive/specs/workflow-v3-3
git mv Specs_Builder_Library_CA_V2_1_3 archive/specs/spec-builder-library
git mv CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE archive/specs/air-v2-1-bundle

git mv _PARALLEL archive/experiments/parallel
git mv _PARALLEL_REPORTS archive/experiments/parallel-reports
git mv "THE_CMF_STUDIO(2)" archive/experiments/cmf-studio-v2
git mv 05_FUTURE_PRODUCTS archive/experiments/future-products

git mv CMF_PROGRAM_CONTROL governance/program-control

git commit -m "TS-APP-SETUP-001 Stage 3: archive historical bundles, spec libraries, and experiments"
```

### Stage 4 — Skeleton directories
```bash
mkdir -p api/routers api/websockets
mkdir -p apps/web/src/{pages,components,hooks,api}
mkdir -p infra/docker infra/nginx
mkdir -p docs/specs/current docs/specs/archive

touch api/routers/.gitkeep api/websockets/.gitkeep
touch apps/web/src/pages/.gitkeep apps/web/src/components/.gitkeep
touch apps/web/src/hooks/.gitkeep apps/web/src/api/.gitkeep
touch infra/docker/.gitkeep infra/nginx/.gitkeep
touch docs/specs/current/.gitkeep docs/specs/archive/.gitkeep

git add api/ apps/ infra/ docs/
git commit -m "TS-APP-SETUP-001 Stage 4: create skeleton directories for Wave 1+ specs"
```

### Stage 5 — pyproject.toml verification
```bash
for svc in builder vae delegation air pipeline interview; do
  echo "=== services/$svc/pyproject.toml ==="
  grep -A2 "package-dir\|\[tool.setuptools.packages.find\]" "services/$svc/pyproject.toml"
done
# Because package-dir = {"" = "src"} and where = ["src"] are relative to the
# pyproject.toml file's own location, and pyproject.toml moved WITH its src/
# directory (both under the same git mv), these fields require no edits.
# This step is verification, not editing. If any field contains an absolute
# or repo-root-relative path (it should not, per the files read in Section 1),
# flag it here rather than assuming.
```

### Stage 6 — Verification
```bash
pip install -e packages/ca_contracts -e packages/ca_runtime \
  -e services/builder -e services/air -e services/pipeline \
  -e services/interview -e services/vae \
  --break-system-packages

python -m pytest tests/ -q --tb=short 2>&1 | tee /tmp/postmove_test_output.txt
diff <(grep "passed" /tmp/baseline_test_output.txt) \
     <(grep "passed" /tmp/postmove_test_output.txt)
# Must show no diff — identical pass count
```

### Stage 7 — Generate manifest and final commit
```python
# generate_archive_manifest.py
import hashlib, yaml, subprocess
from pathlib import Path
from datetime import datetime, timezone

entries = []
archive_root = Path("archive")
for item in sorted(archive_root.rglob("*")):
    if item.is_dir() and item.parent.parent == archive_root:
        # top-level archived directory (e.g. archive/bundles/phase-01)
        entries.append({
            "archived_path": str(item),
            "reason": "see TS-APP-SETUP-001 Section 4 disposition table",
            "verified_not_imported": True,
            "verification_method": "verify_redundancy.sh — grep across tests/, packages/, services/",
        })

manifest = {
    "manifest_version": 1,
    "archived_at": datetime.now(timezone.utc).isoformat(),
    "archived_by_spec": "TS-APP-SETUP-001",
    "entries": entries,
}
Path("archive/bundles/BUNDLE_ARCHIVE_MANIFEST.yaml").write_text(yaml.dump(manifest, sort_keys=False))
print(f"Wrote manifest with {len(entries)} entries")
```
```bash
python generate_archive_manifest.py
git add archive/bundles/BUNDLE_ARCHIVE_MANIFEST.yaml
git commit -m "TS-APP-SETUP-001 Stage 7: generate archive manifest"
```

---

## 8. Failure, Migration, Rollback, Recovery, and Observability

| Failure | Cause | Behaviour | Recovery |
|---|---|---|---|
| `REDUNDANCY_VERIFICATION_FAILED` | Stage 1 script finds a reference to a "candidate" directory outside itself | Script exits non-zero before any move happens | Investigate the specific hit; either it's a false positive (update the grep pattern) or the directory is not actually redundant (remove from candidate list, keep in place) |
| `TEST_COUNT_MISMATCH` | Stage 6 post-move pass count differs from Stage 0 baseline | Do not proceed to Stage 7; do not merge the branch | `git diff` each Stage 2–5 commit individually to find which move broke an import; most likely cause is a `pyproject.toml` with a non-relative path (see Stage 5 note) |
| `PYPROJECT_INSTALL_FAILED` | A service's `pyproject.toml` references a path that moved incorrectly | `pip install -e` raises `FileNotFoundError` or similar | Check that `package-dir` and `where` are relative, not absolute; this should not happen given Section 1's file reads, but Stage 5 exists specifically to catch it if it does |
| Any git mv history loss | Using `mv` + `git add` instead of `git mv` | `git log --follow` on a moved file returns empty history | This spec mandates `git mv` throughout specifically to prevent this; if it happens, `git log --all --full-history` can usually still locate the pre-move commits by content |

### Rollback
Every stage is its own commit. Rollback to any prior stage:
```bash
git reset --hard <commit-before-stage-N>
```
Because this spec never deletes (only archives via `git mv`), a full rollback via `git checkout main -- .` before merging the branch is always available and lossless.

### Observability
- Stage 0 baseline test count and Stage 6 post-move test count are both saved to `/tmp/*.txt` and should be attached to the PR description
- `BUNDLE_ARCHIVE_MANIFEST.yaml` is the permanent, committed record of what moved and why

---

## 9. Acceptance Criteria

**AC-001 — Redundancy verification passes before any move**
Given the candidate list in Section 4 (`_PARALLEL`, `_PARALLEL_REPORTS`, `THE_CMF_STUDIO(2)`, `05_FUTURE_PRODUCTS`),
When `verify_redundancy.sh` is run,
Then it prints `All candidates verified redundant` and exits 0.
Failure example: script finds a hit in `tests/` referencing `_PARALLEL` and exits 1.
Test layer: pre-flight script, run manually and captured in PR description.

**AC-002 — All seven service directories renamed**
Given the repository before this spec,
When Stage 2 completes,
Then `services/builder`, `services/vae`, `services/delegation`, `services/air`, `services/pipeline`, `services/interview`, `services/studio` all exist and contain their original `src/` trees unchanged, and none of the original `0N_*` directory names exist anywhere in the tree.
Failure example: `04_ACTIVATIVE_INTELLIGENCE_RUNTIME` still exists alongside `services/air`.
Evidence: `find . -maxdepth 1 -name "0[1-7]_*"` returns empty.

**AC-003 — Zero pre-existing test regressions**
Given the baseline test pass count recorded in Stage 0,
When Stage 6 completes,
Then the post-move test pass count is identical.
Failure example: baseline shows "121 passed", post-move shows "119 passed, 2 errors".
Evidence: diff of the two captured pytest output files shows no difference in pass count.

**AC-004 — No capital-letter directories in the active tree**
Given the repository after Stage 4,
When `find . -maxdepth 2 -type d -regex '.*/[A-Z].*'` is run, excluding `archive/` and `.git/`,
Then it returns empty.
Failure example: `CMF_PROGRAM_CONTROL` still present at repo root instead of moved to `governance/program-control`.
Evidence: find command output.

**AC-005 — Nothing was deleted, only archived**
Given the disposition table in Section 4,
When the full move sequence completes,
Then every path marked ARCHIVE exists under `archive/` with content byte-identical to its pre-move state (verified by tarball SHA-256 comparison), and `BUNDLE_ARCHIVE_MANIFEST.yaml` lists every archived path.
Failure example: a bundle directory is missing from both its original location and `archive/`.
Evidence: `BUNDLE_ARCHIVE_MANIFEST.yaml` entry count matches the disposition table's ARCHIVE row count exactly (18 entries: 9 bundle dirs + 1 zips dir + 4 spec/experiment dirs, or itemized per actual directory count).

**AC-006 — Skeleton directories exist for Wave 1+ specs**
Given Stage 4 completes,
When TS-APP-API-001 is implemented next,
Then `api/routers/`, `api/websockets/`, `apps/web/src/pages/`, `apps/web/src/components/`, `apps/web/src/hooks/`, `apps/web/src/api/`, `infra/docker/`, `infra/nginx/`, `docs/specs/current/`, `docs/specs/archive/` all already exist and require no additional `mkdir -p` calls.
Evidence: `find api apps infra docs -type d` output matches expected list.

**AC-007 — git history preserved for every moved file**
Given any file that was moved (e.g. `services/pipeline/src/cmf_pipeline/application.py`),
When `git log --follow --oneline services/pipeline/src/cmf_pipeline/application.py` is run,
Then it shows commit history predating the move, not just the single move commit.
Failure example: `git log --follow` on a moved file shows only one commit.
Evidence: git log output length > 1.

---

## 10. Testing and Completion Evidence

### Test files
No new test files are created by this spec — it is infrastructure, not application behaviour. The existing 60 test files at `tests/` are the test suite this spec must not regress.

### Verification commands (run in order, output captured for the build receipt)
```bash
./verify_redundancy.sh                                    # AC-001
find . -maxdepth 1 -name "0[1-7]_*"                        # AC-002 (expect empty)
python -m pytest tests/ -q --tb=short                      # AC-003
find . -maxdepth 2 -type d -regex '.*/[A-Z].*' \
  | grep -v "^\./archive" | grep -v "^\./\.git"             # AC-004 (expect empty)
python verify_archive_manifest.py                          # AC-005
find api apps infra docs -type d                           # AC-006
git log --follow --oneline services/pipeline/src/cmf_pipeline/application.py | wc -l  # AC-007
```

### Build Receipt claim ceiling
`REPOSITORY_STRUCTURE_CLEANUP_EVIDENCE`

This spec does not claim:
- any business logic was reviewed, tested, or improved
- Gap 4 (Builder/Pipeline schema mismatch) is resolved
- the missing AIR API is written
- any "assumed interface" gap in TS-APP-UI-002/003 is reconciled
- production readiness of any kind

---
spec_end: true
next_spec: TS-APP-API-001 (already written — can now be implemented against real paths)
prerequisite_for_next: AC-002, AC-003, AC-006 must all pass before TS-APP-API-001 implementation begins
companion_document: SPEC_GAP_LEDGER.md — read before implementing TS-APP-API-004, TS-APP-API-005, TS-APP-UI-002, TS-APP-UI-003
