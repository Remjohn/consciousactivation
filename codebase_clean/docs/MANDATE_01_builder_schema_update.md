# Mandate: Add `activative_input.aligned_primitive_ids` to cmf_builder

## Problem statement

`services/builder` (the Harness/manifest ingest pipeline) has **no code path that
references the AIR primitive registry at all** — confirmed by grepping
`services/builder/src` for `primitive_id`, `PrimitiveCoalition`, and
`primitive_coalition`: zero matches. Primitive binding today only happens
upstream, in AIR's own Matrix-of-Edging → Primitive Coalition Contract stage,
per-campaign, after a Harness has already been selected.

This means a Harness manifest's `activative_input.hidden_pressure`,
`activative_input.stance`, and `activative_input.wrong_reading_locks` can cite
psychological/archetypal mechanics in free-text prose, but nothing at ingest
time verifies those citations against the real registry
(`services/air/src/cmf_activative_intelligence/data/governance/PRIMITIVE_INVENTORY.csv`,
243 rows) — not existence, not `conflicts_with`. This mandate adds a
**format-only** field and validator to close the gap at the Builder layer. The
semantic work (does this ID exist, does it conflict with another cited ID,
does the prose actually reflect it) is explicitly **out of scope** for this
mandate — that's `MANDATE_02` (the new Skill).

## Verified current state (read directly off these files — not summarized)

### `services/builder/src/cmf_builder/application/manifest_parser.py`
This is the actual enforcement point for `activative_input`'s field set — **not**
`category_binding.py`. Lines ~29-48 (as of this read):

```python
GENERIC_ROOT_FIELDS = frozenset(
    {"manifest_id", "manifest_version", "task_id", "mode", "task"}
)
ACTIVATIVE_ROOT_FIELDS = GENERIC_ROOT_FIELDS | {"category_id", "activative_input"}
ACTIVATIVE_REQUIRED_FIELDS = frozenset(
    {
        "source_premise_ref", "identity_dna_ref", "context_premise_ref",
        "resonance_map_ref", "matrix_of_edging_ref",
        "activative_intelligence_pack_ref", "hidden_pressure",
        "activation_directions", "roles", "stance", "stakes",
        "identity_urges", "participation_design", "intended_reaction",
        "smallest_useful_commitment", "evidence_provenance_refs",
        "evaluation_contract_ref", "wrong_reading_locks",
    }
)
ACTIVATIVE_OPTIONAL_FIELDS = frozenset(
    {"reaction_receipt_refs", "expression_moment_refs"}
)
ACTIVATIVE_FIELDS = ACTIVATIVE_REQUIRED_FIELDS | ACTIVATIVE_OPTIONAL_FIELDS
```

Inside `_parse_activative()`, the check is:
```python
observed = frozenset(fields)
missing = sorted(ACTIVATIVE_REQUIRED_FIELDS - observed)
unexpected = sorted(observed - ACTIVATIVE_FIELDS)
if missing or unexpected:
    raise OperatorManifestInvalid(...)
```
**This is exact-set enforcement.** Any key not in `ACTIVATIVE_FIELDS` (20 keys
total today) fails ingest with `unexpected=...`. Adding a new key to
`activative_input` without first adding it here breaks nothing existing, but
adding it to a manifest before this code change breaks that manifest's ingest.
Sequence matters: ship the schema change first.

`reaction_receipt_refs` and `expression_moment_refs` are the existing
precedent for "optional, defaults to empty" fields — parsed as:
```python
reaction_receipt_refs = require_ref_tuple(
    fields.get("reaction_receipt_refs", []),
    "activative_input.reaction_receipt_refs",
    allow_empty=True,
)
```
Model the new field on this exact pattern, not on the 18 required fields.

### `services/builder/src/cmf_builder/domain/operator_manifest.py`
Defines the low-level validators `manifest_parser.py` imports. Relevant
existing functions to mirror:
- `require_immutable_ref()` (~line 222) — validates one string against
  `IMMUTABLE_REF_PATTERN` (~line 9): `^[A-Za-z0-9][A-Za-z0-9._:/-]*@[A-Za-z0-9][A-Za-z0-9._-]*#sha256:[a-f0-9]{64}$`.
- `require_ref_tuple()` (~line 202) — list version, with `allow_empty: bool = False` param, dedupe check via `len(set(normalized)) != len(normalized)`.
- `require_text_tuple()` (~line 186) — **no `allow_empty` param exists**; always requires non-empty. Do not reuse this for the new field without adding an `allow_empty` parameter, since the field must be legal when absent/empty.

Primitive IDs (`PRM-HUM-009`, `PRM-HUM-023`, `PRM-PSY-018`, `EXP-FBK-004` — all
four confirmed live in the CSV) do not match `IMMUTABLE_REF_PATTERN` (no
`@version#sha256:` suffix), so they need their own pattern and validator, not
reuse of `require_immutable_ref`.

### `services/builder/src/cmf_builder/application/productization_contracts.py`
`ActivativeInputContract` (~line 37-57), a frozen dataclass, 18 positional
required fields followed by exactly two defaulted fields:
```python
    reaction_receipt_refs: tuple[str, ...] = ()
    expression_moment_refs: tuple[str, ...] = ()
```
The new field is a third defaulted field, appended after these two (dataclass
field-ordering rules require defaulted fields last).

### `services/builder/src/cmf_builder/domain/category_binding.py`
`CategoryBinding.create()` reads exactly 9 named keys off the already-parsed
`activative_input` mapping via `.get(field)` — the 7-entry `_SEMANTIC_REF_FIELDS`
tuple, plus `evidence_provenance_refs`, plus `wrong_reading_locks`. It does
**not** enumerate or reject unknown keys. **No change needed here** for this
mandate — confirmed by reading the full file; it will silently ignore
`aligned_primitive_ids` whether or not it's present, which is correct for a
format-only addition.

Called from exactly two places (both application-layer, verified by grep):
`services/builder/src/cmf_builder/application/export_service.py:34` and
`services/builder/src/cmf_builder/application/category_commands.py:151`.
Neither needs to change for this mandate. Note them for `MANDATE_02` — they're
the natural place a *future* semantic check (does the harness's bound category
make sense given its aligned primitives) would eventually be wired in, if that
is ever wanted at Builder-ingest time rather than only in the new Skill.

## Required changes

### 1. `services/builder/src/cmf_builder/domain/operator_manifest.py`
Add near `IMMUTABLE_REF_PATTERN` (~line 9):
```python
PRIMITIVE_ID_PATTERN = re.compile(r"^(PRM|EXP)-[A-Z]{3}-\d{3}$")
```
**Caveat, stated plainly:** this regex is derived from 4 verified rows
(`PRM-HUM-009`, `PRM-HUM-023`, `PRM-PSY-018`, `EXP-FBK-004`) out of 243 total
rows in `PRIMITIVE_INVENTORY.csv`. Before merging, run it against the full
`primitive_id` column and confirm 243/243 matches — do not assume it from 4
samples the way the wrong_reading_locks sampling error happened earlier in
this project.

Add two new functions mirroring `require_immutable_ref` / `require_ref_tuple`:
```python
def require_primitive_id(value: object, field_path: str) -> str:
    text = require_text(value, field_path)
    if PRIMITIVE_ID_PATTERN.fullmatch(text) is None:
        raise OperatorManifestInvalid(
            "Primitive id must match the governed PRM-/EXP- id pattern.",
            field_path=field_path,
        )
    return text


def require_primitive_id_tuple(
    value: object, field_path: str, *, allow_empty: bool = True
) -> tuple[str, ...]:
    if not isinstance(value, list) or (not value and not allow_empty):
        qualifier = "a JSON list" if allow_empty else "a non-empty JSON list"
        raise OperatorManifestInvalid(
            f"{qualifier} of primitive ids is required.", field_path=field_path
        )
    normalized = tuple(
        require_primitive_id(item, f"{field_path}[{index}]")
        for index, item in enumerate(value)
    )
    if len(set(normalized)) != len(normalized):
        raise OperatorManifestInvalid(
            "Duplicate primitive ids are not canonical.", field_path=field_path
        )
    return normalized
```
This deliberately does **not** check the ID against `PRIMITIVE_INVENTORY.csv`
— `services/builder` has no existing dependency on `services/air`'s data
directory, and adding one here would be a real cross-service coupling
decision, not a mechanical addition. That check belongs in the new Skill
(`MANDATE_02`), which already needs to read that CSV for `conflicts_with`
resolution.

### 2. `services/builder/src/cmf_builder/application/productization_contracts.py`
In `ActivativeInputContract`, after `expression_moment_refs: tuple[str, ...] = ()`:
```python
    aligned_primitive_ids: tuple[str, ...] = ()
```

### 3. `services/builder/src/cmf_builder/application/manifest_parser.py`
- Add `require_primitive_id_tuple` to the import block from
  `cmf_builder.domain.operator_manifest` (alongside the existing
  `require_ref_tuple`, `require_text_tuple`, etc. imports).
- Add `"aligned_primitive_ids"` to `ACTIVATIVE_OPTIONAL_FIELDS`.
- In `_parse_activative()`, alongside the `reaction_receipt_refs` /
  `expression_moment_refs` parsing:
  ```python
  aligned_primitive_ids = require_primitive_id_tuple(
      fields.get("aligned_primitive_ids", []),
      "activative_input.aligned_primitive_ids",
      allow_empty=True,
  )
  ```
- Add `aligned_primitive_ids=aligned_primitive_ids` to both the
  `ActivativeInputContract(...)` construction and the `normalized = {...}`
  dict later in the same function.

## Explicit non-goals for this mandate
- No change to `category_binding.py`, `export_service.py`, or
  `category_commands.py`.
- No read of `services/air`'s CSV or YAML snapshots from `services/builder`.
- No enforcement that the field is *used* correctly (conflict-free, actually
  reflected in the prose fields) — format only.
- No change to `TASK_FIELDS` in `operator_manifest.py` — that governs `task`,
  a completely separate object from `activative_input`, and is not implicated
  by this change at all.

## Test coverage a reviewing agent should look for
- Existing manifests with no `aligned_primitive_ids` key still ingest
  unchanged (this is the whole point of using `ACTIVATIVE_OPTIONAL_FIELDS`,
  not `ACTIVATIVE_REQUIRED_FIELDS` — no migration, no version bump needed).
- A manifest with `"aligned_primitive_ids": ["PRM-HUM-009", "PRM-HUM-009"]`
  (duplicate) is rejected.
- A manifest with `"aligned_primitive_ids": ["not-a-real-id"]` is rejected at
  format level (pattern mismatch), independent of whether the ID exists in
  the registry.
- A manifest with `"aligned_primitive_ids": []` ingests successfully (empty
  list is legal, per `allow_empty=True`).
