# CA-M039 Agent Handoff — Deterministic Output Contract & Self-Repair

**Mandate ID:** CA-M039  
**Invariant:** INV-OUT-001  
**Status:** Implementation complete — awaiting Operator approve/reject

## 1. Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/output_contract_repair.py` | **NEW** module implementing greedy JSON extraction, deterministic AST-style local repair, optional 1-turn model-assisted repair, and fail-closed Pydantic schema validation. | INV-OUT-001: all program outputs are schema-validated; malformed LLM responses receive bounded repair; non-compliance after one repair turn aborts. |
| `tests/cae/test_ca_m039_output_repair.py` | **NEW** comprehensive unit/integration tests covering extraction, local repair, schema enforcement, single model-repair turn, and all fail-closed / false-proof paths. | Positive (prose-wrapped success, local repair success, one model-turn success) and negative (empty, prose-only, post-repair still invalid, >1 turn clamped) executable evidence. |

No other repository files were modified (file-boundary compliance with mandate target list).

## 2. Exact paste instructions

Replace / add the following paths in the repository root (paths are relative to repo root):

1. **Add new module**  
   Source in bundle:  
   `CA-M039_BUNDLE/packages/ca_runtime/src/ca_runtime/output_contract_repair.py`  
   → Destination:  
   `packages/ca_runtime/src/ca_runtime/output_contract_repair.py`

2. **Add new test suite**  
   Source in bundle:  
   `CA-M039_BUNDLE/tests/cae/test_ca_m039_output_repair.py`  
   → Destination:  
   `tests/cae/test_ca_m039_output_repair.py`

Optional (not required by this mandate): wire `enforce_output_contract` / `parse_and_validate` into the output-contract validation block of `packages/ca_runtime/src/ca_runtime/agent_invocation.py` (currently uses a simple fence-strip + `json.loads`). That integration is intentionally left out of this bounded mandate so the Operator can approve the pure contract module first.

## 3. Manual post-apply commands

None required (no migrations, no package rebuild, no npm scripts).

After paste, the module is importable as:

```python
from ca_runtime.output_contract_repair import (
    enforce_output_contract,
    parse_and_validate,
    greedy_extract_json,
    deterministic_local_repair,
)
```

If the package uses an explicit `__init__.py` re-export list, you may optionally add the public symbols; this is not required for the mandate.

## 4. New automated tests included in the bundle

- `tests/cae/test_ca_m039_output_repair.py`

  Test classes:
  - `TestGreedyExtraction` — markdown fences, prose wrapping, empty/None/no-JSON failures
  - `TestDeterministicLocalRepair` — trailing commas, Python literals, single-quoted keys via AST, clean no-op
  - `TestSchemaValidation` — valid payload, missing fields, wrong types, no-schema dict path, fenced+schema success
  - `TestBoundedModelRepair` — one successful model turn, post-repair still-invalid fail-closed, no repair_fn, max_turns clamped to 1, local repair avoids model turn
  - `TestFalseProofDefenses` — empty/prose-only never succeed, wrapper helpers, lineage, nested schema, callback exception
  - `TestEndToEndPipeline` — full prose+fence+trailing-comma local success; prose+invalid then model repair success

Suggested invocation (Operator / CI only; agent was instructed not to run tests):

```bash
pytest tests/cae/test_ca_m039_output_repair.py -v
```

## 5. Residual limitations

- Model-assisted repair is supplied via an injectable `model_repair_fn` callback; this mandate does not itself call a live LLM. Call sites that want the 1-turn model loop must pass a callback that performs the provider call and returns the repaired text.
- Greedy extraction uses a balanced-brace regular expression (plus fence stripping). Extremely pathological nesting beyond the regex depth may fall back to extraction failure (fail-closed).
- When `schema=None`, any valid JSON object/array is accepted; callers that require a specific contract must pass a Pydantic model.
- Integration into `agent_invocation.py` is out of scope for this mandate (see paste instructions).

## 6. Evidence locators

- Implementation: `packages/ca_runtime/src/ca_runtime/output_contract_repair.py`
  - `greedy_extract_json` — INV-OUT-001 greedy extraction
  - `deterministic_local_repair` — bounded AST-style local repair
  - `enforce_output_contract` — full pipeline with max 1 model turn + fail-closed
  - Error taxonomy: `JSONExtractionError`, `SchemaComplianceError`, `RepairBudgetExhaustedError`
- Tests: `tests/cae/test_ca_m039_output_repair.py` (all classes listed above)

## 7. Operator decision request

Does the evidence prove that model output parsing enforces greedy JSON extraction and 1-turn bounded schema self-repair at the canonical runtime boundary, and that non-compliance after repair fails closed?

**Approve or reject CA-M039.**
