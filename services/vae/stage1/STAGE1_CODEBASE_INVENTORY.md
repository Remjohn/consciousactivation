# Stage 1 Codebase Inventory

Generated: 2026-07-14
Scope: D:\Work\Conscious Activations\CMF_VISUAL_ASSET_EDITOR_SHARDED_PRD_V1\CMF_VISUAL_ASSET_EDITOR_SHARDED_PRD_V1

## Governing instruction discovery

- `AGENTS.md`: NOT FOUND in repository root, either configured workspace root, or parent package directory search.
- Consequence: the AGENTS-defined per-requirement verdict taxonomy is unavailable. This audit uses the visible final triad `PASS`, `CONCERNS`, `FAIL` only for coverage and final go/no-go signaling, and records this as a blocker.

## Repository shape verified

- Git repository: NOT FOUND (`git status` failed with `not a git repository`).
- Total files inspected before Stage 1 artifacts: 123.
- File extensions: .csv=2, .json=11, .md=64, .py=2, .yaml=44.
- Production source code files: 0.
- Verification/utility scripts: 2 (`scripts/rebuild_combined_prd.py`, `scripts/validate_prd_package.py`).
- Contract schemas: 13.
- Test/spec filename matches: 2 documentation/template artifacts; no executable tests or test suites were found.
- CI/workflow assets: 0.
- Deployment/infra assets: 0.
- Package-manager/build manifests: none found for npm, Python, Rust, Go, Java, .NET, Docker, Compose, Make, or Just.

## Primary PRD package inventory

- PRD shards: 14 spine files plus 22 feature shards and combined view.
- Governance: decision register, requirements registry, traceability matrix, source register, preservation contract, hard gates, prohibitions, constitution, asset/budget/workcell/profile registries.
- Contracts: 13 JSON Schema 2020-12 YAML schemas and 6 Format 02 example contracts.
- Reference slice: Format 02 Minimal Coach Theatre README, syntax summary, benchmark manifest, seed registries, and reference contracts.
- Handoff/templates: architecture handoff, delegation handoff, epics/stories handoff, feature tech spec template, requirement/story/demand templates.
- Validation: saved reports plus rerun embedded validator output.

## Verification results

- Saved `LOCAL_VERIFICATION.json`: status `PASS`, artifact status `draft_for_review`, implementation_authorized `False`.
- Saved `validation/PRD_VALIDATION_REPORT.md`: PASS as of 2026-07-13.
- Current rerun of `python scripts/validate_prd_package.py`: `FAIL`.
- Current blocker from rerun: ["Source integrity errors: ['missing SRC-001: \\\\mnt\\\\data\\\\CMF_ATOMIC_HARNESS_BUILDER_NEXT_SHARDED_PRD_V1_1.zip', 'missing SRC-002: \\\\mnt\\\\data\\\\CCP_CMF_ATOMIC_HARNESS_SPEC_BUILDER_V2_1 (2)(3).zip', 'missing SRC-003: \\\\mnt\\\\data\\\\CCP_ACTIVATIVE_INTELLIGENCE_VISUAL_NARRATIVE_V1_BUNDLE(2).zip', 'missing SRC-004: \\\\mnt\\\\data\\\\VISUAL SYNTAX BUILDER (2)(2).zip', 'missing SRC-005: \\\\mnt\\\\data\\\\architecture.zip', 'missing SRC-006: \\\\mnt\\\\data\\\\modules.zip', 'missing SRC-007: \\\\mnt\\\\data\\\\ccsb_paper(1).md', 'missing SRC-008: \\\\mnt\\\\data\\\\achievement-story-design-brief-v1.2.yaml', 'missing SRC-009: \\\\mnt\\\\data\\\\Pasted text(12).txt', 'missing SRC-010: \\\\mnt\\\\data\\\\Conscious Architect University.zip']"].

## Coverage rule applied

Documentation, filenames, registries, examples, and validation reports are treated as specification evidence only. They are not counted as production implementation or executable test coverage.
