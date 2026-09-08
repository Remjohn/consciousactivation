# CA-M027 AGENT HANDOFF — Declarative Policy Rule Packages (Q26 / FR-AUTH-002)

## 1. Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/policy_package.py` | **NEW** — Policy rule package models, schema/semantic validation, canonical identity digest, immutable revision registry, runtime `authorize()` consumption, discovery under `programs/*/policy/` | Packages are machine-readable, versioned, digest-identified; constitutional minimums cannot be weakened; historical revisions retained; runtime effect is deterministic |
| `packages/ca_runtime/schemas/policy_rule_package.schema.json` | **NEW** — JSON Schema (draft 2020-12) for the package format; `additionalProperties: false` | Schema-level rejection of unknown fields; explicit typed predicates |
| `programs/editorial_storyboard_program/policy/policy_package.yaml` | **NEW** — Declarative policy package for editorial storyboard (COMPOSER emit + COMMANDER approve) | Compatibility with existing program layout; Stage-12 approve remains COMMANDER + OPERATOR_DECISION + EXECUTABLE |
| `programs/script_program/policy/policy_package.yaml` | **NEW** — Declarative policy package for script_program authority lanes | Existing program CAE invariants expressed as typed rules without prose authority |
| `tests/wave04/test_ca_m027_declarative_policy_packages.py` | **NEW** — Positive load/auth, malformed rejection, constitutional-weakening rejection, independent dual-revision proof, program-layout compatibility | Executable + TEST evidence; contrastive false-proof (schema-valid weakening rejected at semantic gate) |

No existing shared registry, migration, or program_manifest schema was mutated (ProgramManifest uses `extra="forbid"`; policy packages live in a sibling `policy/` directory and a dedicated module).

## 2. Exact paste instructions

Copy/replace into the repository root as follows (paths relative to repo root):

```
packages/ca_runtime/src/ca_runtime/policy_package.py
  ← CA-M027_BUNDLE/packages/ca_runtime/src/ca_runtime/policy_package.py

packages/ca_runtime/schemas/policy_rule_package.schema.json
  ← CA-M027_BUNDLE/packages/ca_runtime/schemas/policy_rule_package.schema.json
  (create parent dir `packages/ca_runtime/schemas/` if absent)

programs/editorial_storyboard_program/policy/policy_package.yaml
  ← CA-M027_BUNDLE/programs/editorial_storyboard_program/policy/policy_package.yaml
  (create `policy/` directory)

programs/script_program/policy/policy_package.yaml
  ← CA-M027_BUNDLE/programs/script_program/policy/policy_package.yaml
  (create `policy/` directory)

tests/wave04/test_ca_m027_declarative_policy_packages.py
  ← CA-M027_BUNDLE/tests/wave04/test_ca_m027_declarative_policy_packages.py
  (create `tests/wave04/` if absent)
```

Do **not** modify:
- `programs/editorial_storyboard_program/program_manifest.yaml`
- `programs/script_program/CAE.md`
- `packages/ca_runtime/src/ca_runtime/program_registry.py`
- Any shared migration or receipt schema

## 3. Manual post-apply commands

```bash
# From repository root, with package install / PYTHONPATH including packages/ca_runtime/src and packages/ca_contracts/src

# Focused mandate tests
pytest tests/wave04/test_ca_m027_declarative_policy_packages.py -v

# Optional: confirm discovery against live programs tree
python -c "
from pathlib import Path
from ca_runtime.policy_package import load_and_register_from_program_root, get_policy_package_registry
pkgs = load_and_register_from_program_root(Path('programs'))
print([(p.manifest.package_id, p.manifest.version, p.identity_digest[:12]) for p in pkgs])
"
```

No database migrations are required. No npm scripts. No control-state record update is mandated beyond the Operator decision request below.

## 4. Names of new automated tests included in the bundle

- `tests/wave04/test_ca_m027_declarative_policy_packages.py`
  - `test_parse_valid_package_dict`
  - `test_load_from_yaml_path`
  - `test_identity_digest_stable`
  - `test_identity_digest_changes_on_rule_change`
  - `test_reject_missing_required_fields`
  - `test_reject_invalid_semver`
  - `test_reject_invalid_authority_lane`
  - `test_reject_unknown_fields_extra_forbid`
  - `test_reject_active_with_empty_rules`
  - `test_reject_duplicate_predicate_ids`
  - `test_reject_constitutional_lane_weakening`  ← contrastive false-proof
  - `test_reject_missing_constitutional_evidence`
  - `test_reject_prohibited_operation_delegation`
  - `test_raising_requirements_is_allowed`
  - `test_registry_register_and_get`
  - `test_registry_rejects_conflicting_digest_same_version`
  - `test_two_revisions_behave_independently`  ← decisive dual-revision proof
  - `test_authorize_positive`
  - `test_authorize_deny_insufficient_lane`
  - `test_authorize_deny_missing_evidence`
  - `test_authorize_deny_unknown_operation`
  - `test_discover_editorial_storyboard_policy_if_present`
  - `test_load_real_editorial_storyboard_package_from_bundle`
  - `test_load_real_script_program_package_from_bundle`
  - `test_default_registry_roundtrip`
  - `test_evidence_classes_documented`

## 5. Evidence classes & locators

| Claim | Evidence class | Locator |
|---|---|---|
| Package schema + typed predicates | SCHEMA | `packages/ca_runtime/schemas/policy_rule_package.schema.json`; Pydantic models in `policy_package.py` |
| Load + canonical digest | EXECUTABLE | `load_policy_package_from_path`, `compute_package_identity_digest` |
| Constitutional non-weakening | EXECUTABLE | `validate_constitutional_non_weakening`; tests `test_reject_constitutional_*` |
| Runtime authorization effect | EXECUTABLE | `authorize`, `authorize_via_registry` |
| Immutable revisions independent | EXECUTABLE | `PolicyPackageRegistry` + `test_two_revisions_behave_independently` |
| Program layout compatibility | TEST / REGISTRY_SOURCE | `programs/*/policy/policy_package.yaml`; discovery helpers |
| False-proof countercase | TEST | Schema-valid package lowering `approve` to COMPOSER is rejected with `CONSTITUTIONAL_WEAKENING_REJECTED` |

## 6. Residual limitations

- Policy packages are process-scoped in the default registry (in-memory). Durable persistence of package revisions into the CAE PostgreSQL state plane is intentionally out of scope for CA-M027 (no new migration authorized).
- `ProgramManifest` was not extended; programs reference policy packages by filesystem convention (`policy/policy_package.yaml`), not by a new manifest field.
- Q27 prospective binding, release/distribution, and any second policy engine are explicitly out of scope.
- Precedence among multiple concurrently applicable packages for the same operation is fail-closed (caller must pin `package_id`/`version`); undefined multi-package merge is not implemented.

## 7. Control-state impact

None required beyond this handoff. No historical policy/authorization objects were mutated in place.

## 8. Operator decision request

**Approve or reject `CA-M027`** based on whether the executable evidence above proves the ratified Q26 / FR-AUTH-002 contract at the canonical authority boundary (versioned declarative packages, typed predicates, validation, identity/digest, runtime consumption, non-weakening of constitutional Stage-12 gates, independent dual-revision behavior).

Do not infer approval solely from a green test suite; inspect the dual-revision test and the constitutional-weakening rejection as the decisive proofs.

## 9. Commit SHA

Not applicable in this isolated bundle construction environment. After paste, record the implementing commit SHA in the Operator completion report.
