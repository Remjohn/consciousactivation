# Codebase Inventory

## Audit Scope

- Primary PRD package: `D:\Work\Conscious Activations\CMF_ATOMIC_HARNESS_BUILDER_NEXT_SHARDED_PRD_V1_1\CMF_ATOMIC_HARNESS_BUILDER_NEXT_SHARDED_PRD_V1_1`
- Extracted brownfield implementation: `D:\Work\CCP_CMF_ATOMIC_HARNESS_SPEC_BUILDER_V2_1`
- PRD status: `0.2.0-draft`; 70 manifest-listed package files plus `MANIFEST.json` itself; package validator PASS. All 71 files are recorded in `PRD_PACKAGE_FILE_INVENTORY.csv`.
- Brownfield source baseline: 401 files, 1,575,769 bytes, aggregate audit SHA-256 `f6b1bca3ec1072913b3e63c983a77aa56a3bc651e0bcb3b3d9911ace1c26c571`.
- Observed working copy: 406 files. The additional five are pre-existing `.pytest_cache` tooling residue, marked `generated_test_cache` in the CSV and excluded from the registered 401-file source baseline.
- Neither directory is a Git working tree, so commit identity, branch state, and change provenance cannot be verified locally.

Every file in the brownfield tree was read or parsed by type. Python files were AST-parsed, JSON and YAML were parsed structurally, UTF-8 text was decoded, and remaining assets were byte-read. There were zero inspection errors. See `REPOSITORY_FILE_INVENTORY.csv`.

## Repository Landscape

| Area | Files | Verified role |
|---|---:|---|
| `src/cmf_harness_spec_builder` | 16 Python files | CLI, file-backed run state, source indexing, decision graph, question protocol, OpenSpec compiler, readiness checks, legacy donor guard, and target pointer scaffold |
| `tests` | 3 | One 632-line Python suite plus two pre-existing bytecode files; 28 live tests |
| `schemas` | 40 | JSON Schemas for run, decisions, plans, constitutions, VAE/delegation contracts, and artifact manifest |
| `openspec` | 157 | Deprecated v1, content v2/v2.1, VAE, and delegation OpenSpec schemas/templates |
| `.pi` | 28 | Operator skill, system prompt, wrappers, and 15 Markdown workflow steps |
| `templates` | 69 | Run and module document templates |
| `configs` | 7 | Module and reference-run configuration |
| `docs` and `references` | 53 | Architecture notes, migration notes, walkthroughs, and embedded reference material |
| `scripts` | 2 | Reference-run plan creation and target installation helper |
| Deployment/IaC/CI | 0 | No GitHub Actions, container, Compose, Kubernetes, Helm, Terraform, service, or release deployment asset found |

The brownfield package contains 3,754 lines across 19 readable Python files: 16 package modules, two scripts, and one test module.

## Runtime And Packaging

- Python `>=3.11`; setuptools build; dependencies are Pydantic, PyYAML, and Pillow.
- Console entry point: `cmf-harness-spec = cmf_harness_spec_builder.cli:main`.
- `pyproject.toml` declares `2.1.0`, while `src/cmf_harness_spec_builder/__init__.py:1` declares `2.0.0`.
- The first uninstalled test invocation failed import collection. The live suite passed only after adding `src` to `sys.path`, exposing an unverified installation/package-data path.
- Schemas, OpenSpec assets, templates, and configs live outside the Python package; no explicit package-data declaration was found.

## Executable Components

| Component | Concrete evidence | Live test evidence | Verified baseline and material limit |
|---|---|---|---|
| Module registry | `module_registry.py:12-108`, `cli.py:35-49` | `test_spec_builder_v2.py:452-478` | Three modules are listed. `cli.py:302` defaults omitted selection to content, so explicit-selection governance is not enforced. |
| Run state | `state.py:12-27`, `models.py:334-364` | Exercised by guided-flow tests | JSON load/save exists. No event ledger, checkpoint graph, concurrency control, invalidation, or lifecycle transition guard exists. |
| Source index | `source_index.py:47-257` | `test_spec_builder_v2.py:115-132` | Files/ZIPs are hashed; images receive dimensions. No directory identity hash, media extraction, stable specimen identity, duplicate detection, role/status authority, or archive resource bounds. |
| Saturation | `saturation.py:72-148` | Density assertion at `test_spec_builder_v2.py:124-132` | Text keywords produce reports. No target-specific saturation contract, contradiction model, confidence threshold, visual/temporal evidence, or typed outcome. |
| Genesis graph | `decision_tree.py:188-316` | `test_spec_builder_v2.py:144-209` | Static graphs, dependencies, provisional/resolved states, and one active question exist. Reopen does not invalidate descendants and no transaction commits canonical IR. |
| Question protocol | `grill_me.py:81-313`, `models.py:204-330` | `test_spec_builder_v2.py:165-209,332-377` | Word-count and recommendation-record validators exist; recommendation content remains a manual file-mediated interaction. |
| Spec compiler | `spec_compiler.py:72-188` | `test_spec_builder_v2.py:319-330,604-622` | Templates compile to OpenSpec artifacts. There is no canonical Harness IR, compiler-version identity, migration, integrity manifest, or multi-target compilation boundary. |
| Readiness | `readiness.py:14-143` | `test_spec_builder_v2.py:319-330,604-622` | Structural checks can issue PASS. Empty `SOURCE_LOCK`, `SPECIMEN_INDEX`, and `EVIDENCE_INDEX` fixtures at lines 108-111 and 445-448 still pass; semantic evidence, benchmark, anti-goal, repair, and authorization gates are absent. |
| Legacy guard | `legacy_format01.py:44-103` | `test_spec_builder_v2.py:379-397` | Detects a likely donor and blocks an unconfirmed Format 01 reuse. It is not a general migration/equivalence system. |
| Target scaffold | `target_scaffold.py:10-54` | No dedicated target installation test | Writes additive README and pointer files. It does not produce or validate a Development Capsule. |
| Workflow | `.pi/skills/.../SKILL.md` and steps 00-14 | No workflow runtime tests | A human-operated Markdown sequence exists. It is not typed Workflow IR and has no scheduler, router, sandbox, retry policy, telemetry, promotion, or rollback runtime. |

## Schemas And Contracts

- All 40 JSON Schema files parse successfully.
- Thirty-nine schema titles correspond to Pydantic model names. Thirty-eight generated model schemas compare exactly with checked-in JSON; `question_packet` differs in metadata/detail while retaining the same top-level properties and required keys.
- `harness_spec_artifact_manifest.schema.json` has no corresponding Pydantic model.
- OpenSpec templates have no missing declared template files. The tests validate artifact DAG ordering for content v2 and all three current targets.
- No canonical Harness IR, Builder Workflow IR, event envelope, benchmark receipt, category constitution runtime model, or deployment contract schema was found.

## Tests

Latest live command result: `28 passed in 13.35s` with `src` inserted into the import path and pytest cache disabled. Pytest also reported that `asyncio_default_fixture_loop_scope` is unset and its future default will change.

The suite verifies ZIP snapshots, graph dependencies, one-active-question behavior, provisional/YOLO/ratification paths, selected model validators, OpenSpec DAG ordering, three-module menu exposure, and structural readiness happy paths.

It does not verify lifecycle command ordering, state replay, directory hashes, visual syntax, atomicity inference, canonical IR, schema migration, benchmarks, event history, Control Tower, repair graphs, Development Capsules, dual-run migration, workflow execution, fault isolation, sandboxing, CI, deployment, or installed-package operation.

## Workflows, Documentation, And Deployment

- The operator workflow is described across 15 `.pi` Markdown steps. CLI commands do not enforce that sequence.
- Documentation is extensive, but it was treated as claimed intent only. Coverage was credited only when executable code and tests supported it.
- `scripts/install_into_visual_syntax_builder.py` references `openspec/schemas/cmf-atomic-harness-genesis`, a path present only under `_deprecated_v1`, so that helper is stale against the active layout.
- No service topology, persistence adapter, UI project, API, authentication, secrets management, observability backend, CI pipeline, artifact registry, or deployment target is present.

## External Source Availability

The PRD source register lists 12 sources. Only the extracted equivalent of SRC-001 and the in-package SRC-012 decision record are locally inspectable. The registered `/mnt/data` files for SRC-002 through SRC-010 are not present under the inspected `D:\Work` or user Documents trees, and the SRC-011 BMAD repository/commit is not locally available. The three target repositories and the required reference harness are also absent.
