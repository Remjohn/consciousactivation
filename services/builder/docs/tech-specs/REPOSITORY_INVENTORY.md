# Repository Inventory

## Scope And Authority

Repository inspected:

`D:\Work\CONSCIOUS_ACTIVATIONS\01_ATOMIC_HARNESS_BUILDER`

The authoritative product definition is Builder PRD V1.2 under the Activative Intelligence Constitution V1.1 and `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`. The inspection covers the aligned PRD, governance and contract registries, documentation schemas/examples, 33 locked decisions, 15 Readiness Hard Gates, accepted architecture, TS-00 through TS-15, approved Control Tower UX, planning inventory, validation tools, and the pre-existing `stage1/` audit artifacts.

The package validator reports `PASS` with no errors. The important authority digests at inspection time are:

| Artifact | SHA-256 |
|---|---|
| `prd/PRD_COMBINED.md` | `bb561740d5e912a4653973ff14e345a717a540917e7687a6b0cc9f2e55b60dcd` |
| `governance/REQUIREMENTS_REGISTRY.json` | `52ad039406ad1cdacd7c3310e536b922c647b88ab2651410c5f35355adf0fb69` |
| `governance/DECISION_REGISTER.json` | `3680548974a675e6db88ecf05e348da8edb61d6e9a0905212a1553519f2006e8` |
| `governance/PRODUCT_CONSTITUTION.yaml` | `33188e686da73f2f7c1716f5ea8d4845b8ab0e1cb8765d0663fa5f40cbe8d8e5` |
| `governance/READINESS_HARD_GATES.yaml` | `f1d431738086484978df71243f9bbddd049aadf31341d2e5cea354772c292800` |
| `handoff/ARCHITECTURE_HANDOFF.md` | `91788a980350edafe6f356bed9deb51854d580940cce9957ab7d97b412fb749c` |
| `docs/planning/PLANNING_REQUIREMENTS_INVENTORY.csv` | `d3db32a78f4acce25e5448ff7c6ecb765ba814c0bdbf1bb44d6b49de00c55923` |

## Initial V1.1 Physical Inventory

Before the technical-specification and V1.2 alignment packages were added, the workspace contained 82 files. This table is retained as historical inspection evidence rather than a current file-count claim:

| Area | Files | Role |
|---|---:|---|
| `prd/` | 34 | Combined PRD, sharded sections, and 18 feature definitions |
| `governance/` | 17 | Requirements, decisions, constitution, gates, registries, traceability, metrics, and source register |
| `addendum/` | 5 | Architecture-rich, JIT, legacy-method, BMAD, and V2.1 context |
| `handoff/` | 3 | Architecture, epics/stories, and feature-spec handoff |
| `validation/` | 5 | PRD integrity, source integrity, ID coverage, and link reports |
| `templates/` | 2 | Feature-requirement and epic/story templates |
| `scripts/` | 2 | PRD rebuild and validation utilities |
| `stage1/` | 11 | Prior audit evidence and generated inventory; not product implementation |
| Root metadata | 5 | README, manifest, local verification, plus empty `.git/` and `.agents/` directories |

File extensions were 54 Markdown, 11 JSON, 9 YAML, 5 CSV, and 3 Python files. The empty `.git/` directory is not a valid Git repository; Git commands fail because it contains no repository metadata.

## Implementation Search

No Builder Next or Builder V2.1 production implementation exists in this repository.

Evidence:

- No `src/`, production `tests/`, production product-schema package, `packages/`, `apps/`, `lib/`, service manifest, migration, deployment, or CI directory exists. `docs/contracts/schemas/` contains documentation-time V1.2 JSON Schemas and fixtures only.
- `scripts/rebuild_combined_prd.py` rebuilds the combined PRD from documentation.
- `scripts/validate_prd_package.py` validates PRD package structure and traceability.
- `stage1/generate_stage1_evidence.py` generates audit CSV/JSON artifacts and is not runtime code.
- No product API, CLI, event store, workflow engine, target compiler, Harness IR model, Workflow IR model, benchmark runner, Control Tower, or production test was found.
- The source register points to an external SRC-001 V2.1 archive, but that archive and its extracted implementation are not inside this repository.

Documentation claims are not credited as implementation coverage. Accordingly, no requirement is classified as `IMPLEMENTED_AND_KEEP`, `IMPLEMENTED_BUT_ALIGN`, `PARTIALLY_IMPLEMENTED`, or `REPLACE_EXISTING_BEHAVIOR`.

## V2.1 Determination

V2.1 is historical and architectural context only for this repository.

- `governance/SOURCE_REGISTER.json` records SRC-001 and its archive hash.
- `addendum/V2_1_BROWNFIELD_DELTA.md` describes intended retain/extend behavior.
- Neither source is executable evidence because the referenced archive, schemas, package, and tests are absent from the repository boundary.
- FR-160 through FR-166 and NFR-COMPAT-001 are therefore `NOT_APPLICABLE` for the current implementation baseline.
- FR-167, FR-168, and FR-169 remain applicable because Release 1 proof, bounded certification, and future general certification are Builder Next product obligations independent of local V2.1 migration.
- If an authoritative V2.1 package is later imported, this disposition must be invalidated and the coverage matrix regenerated before implementation continues.

## Architecture-Preservation Authority

`docs/tech-specs/ARCHITECTURE_PRESERVATION_CONTRACT.md` is the ratified TS-00 derived contract. It remains subordinate to the pinned Activative Intelligence Constitution V1.1, Builder PRD V1.2 amendment, and `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`. HG-015 operationalizes missing semantic stack, fifth-category, rich-lineage, and dual-order failures.

## Frozen Cross-Product Boundaries

- Builder may compile a Visual Asset Editor target profile, schemas, contracts, and Development Capsule. It must not implement editor production behavior.
- Builder may compile a Content-to-Asset Delegation target profile. Shared delegation contracts remain owned by the Delegation repository.
- ComfyUI, model execution, LoRA training, GPU scheduling, and generated harness execution are external adapters or downstream responsibilities.
- Atomic Content Harness semantic authority is preserved; target compilers may not flatten content, asset, and delegation ownership into one universal runtime.
