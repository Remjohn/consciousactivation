---
name: caebmad-repository-investigate
description: Audits physical filesystem structures, workspace manifests, cross-repo contracts, and repository hygiene at Level 06.
version: 0.3.0-rebuild
agent: cae-repository-analyst
---

# Skill: caebmad-repository-investigate

## 1. Purpose & Invocation
The `caebmad-repository-investigate` skill enables the `cae-repository-analyst` to audit physical filesystem layouts, detect directory drift, and verify cross-repository contracts at `Level 06: REPOSITORY`.

## 2. Invocation Preconditions
1. Workspace root directory accessible.
2. `WORKSPACE_MANIFEST.json` or `FOLDER_MAP.md` present.
3. Schema `schemas/repository_reality_map.schema.json` loaded.

## 3. Execution Logic
1. **Directory Tree Scan:** Inspect top-level folders and match against workspace documentation.
2. **Cross-Repo Contract Check:** Verify existence and schema validity of contracts under `governance/program-control/02_CROSS_REPO_CONTRACTS/`.
3. **Orphan Detection:** Identify directories without active maintenance ownership or manifest registration.
4. **Hygiene Verdict:** Assign one of `CLEAN`, `NEEDS_CLEANUP`, `CRITICAL_DRIFT`, or `GOVERNED`.
5. **Map Assembly:** Emit `docs/cae-bmad/07_brownfield/REPOSITORY_REALITY_MAP.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/07_brownfield/REPOSITORY_REALITY_MAP.json`
- `docs/cae-bmad/07_brownfield/REPOSITORY_REALITY_MAP.md`
