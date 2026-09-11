"""Comprehensive Test Suite for CAE Mandate CA-M039: Deterministic Output Contract & Self-Repair.

Governed by:
- Mandate CA-M039 (Deterministic Output Contract & Self-Repair)
- Invariant INV-OUT-001
- Canon Q39: greedy JSON extraction + 1-turn bounded schema self-repair + fail-closed

Verifies:
- Gate 1: Greedy extraction recovers JSON wrapped in markdown fences / prose.
- Gate 2: Deterministic local AST-style repair fixes trailing commas, Python literals, single-quoted keys.
- Gate 3: Pydantic schema validation is enforced; invalid payloads fail closed.
- Gate 4: At most one model-assisted repair turn is permitted.
- Gate 5: After the single repair turn, remaining non-compliance raises SchemaComplianceError.
- False-Proof Defense 1: Empty / non-JSON text raises JSONExtractionError (no silent success).
- False-Proof Defense 2: Requesting >1 model repair turn is clamped / rejected.
- False-Proof Defense 3: Model repair that still yields invalid schema fails closed.
- False-Proof Defense 4: Clean valid JSON passes without any repair turns.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Type

import pytest

try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:  # pragma: no cover
    pytest.skip("pydantic not available", allow_module_level=True)

from ca_runtime.output_contract_repair import (
    JSONExtractionError,
    ModelRepairFn,
    OutputContractError,
    OutputContractResult,
    RepairBudgetExhaustedError,
    RepairStage,
    SchemaComplianceError,
    deterministic_local_repair,
    enforce_output_contract,
    greedy_extract_json,
    parse_and_validate,
    validate_against_schema,
)


# ---------------------------------------------------------------------------
# Test schemas
# ---------------------------------------------------------------------------


class SimpleAgentOutput(BaseModel):
    status: str
    agent_id: str
    summary: str = ""
    score: Optional[float] = None


class NestedOutput(BaseModel):
    items: List[str]
    meta: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Gate 1 — Greedy extraction
# ---------------------------------------------------------------------------


class TestGreedyExtraction:
    def test_clean_json_object(self) -> None:
        raw = '{"status": "SUCCESS", "agent_id": "A1", "summary": "ok"}'
        extracted = greedy_extract_json(raw)
        assert json.loads(extracted)["status"] == "SUCCESS"

    def test_clean_json_array(self) -> None:
        raw = '[1, 2, 3]'
        extracted = greedy_extract_json(raw)
        assert json.loads(extracted) == [1, 2, 3]

    def test_markdown_json_fence(self) -> None:
        raw = """Here is the result:

```json
{"status": "SUCCESS", "agent_id": "A1", "summary": "fenced"}
```

Hope that helps.
"""
        extracted = greedy_extract_json(raw)
        data = json.loads(extracted)
        assert data["summary"] == "fenced"
        assert data["agent_id"] == "A1"

    def test_generic_fence_without_language(self) -> None:
        raw = """```
{"status": "OK", "agent_id": "X", "summary": "generic"}
```"""
        extracted = greedy_extract_json(raw)
        assert json.loads(extracted)["status"] == "OK"

    def test_prose_wrapped_object(self) -> None:
        raw = (
            "Sure, I can help. The structured answer is "
            '{"status": "SUCCESS", "agent_id": "prose", "summary": "wrapped"} '
            "and that should be all you need."
        )
        extracted = greedy_extract_json(raw)
        assert json.loads(extracted)["agent_id"] == "prose"

    def test_empty_raises(self) -> None:
        with pytest.raises(JSONExtractionError) as ei:
            greedy_extract_json("")
        assert ei.value.reason_code == "JSON_EXTRACTION_FAILED"

    def test_none_raises(self) -> None:
        with pytest.raises(JSONExtractionError):
            greedy_extract_json(None)  # type: ignore[arg-type]

    def test_no_json_at_all_raises(self) -> None:
        with pytest.raises(JSONExtractionError):
            greedy_extract_json("This is pure prose with no braces or brackets.")


# ---------------------------------------------------------------------------
# Gate 2 — Deterministic local repair
# ---------------------------------------------------------------------------


class TestDeterministicLocalRepair:
    def test_trailing_comma_object(self) -> None:
        broken = '{"status": "SUCCESS", "agent_id": "A1",}'
        repaired, n = deterministic_local_repair(broken)
        assert n >= 1
        data = json.loads(repaired)
        assert data["status"] == "SUCCESS"

    def test_trailing_comma_array(self) -> None:
        broken = '["a", "b",]'
        repaired, n = deterministic_local_repair(broken)
        assert n >= 1
        assert json.loads(repaired) == ["a", "b"]

    def test_python_true_false_none(self) -> None:
        broken = '{"ok": True, "missing": None, "flag": False}'
        repaired, n = deterministic_local_repair(broken)
        assert n >= 1
        data = json.loads(repaired)
        assert data["ok"] is True
        assert data["missing"] is None
        assert data["flag"] is False

    def test_single_quoted_keys_via_ast(self) -> None:
        # Python-literal style that AST can recover
        broken = "{'status': 'SUCCESS', 'agent_id': 'A1', 'summary': 'sq'}"
        repaired, n = deterministic_local_repair(broken)
        assert n >= 1
        data = json.loads(repaired)
        assert data["agent_id"] == "A1"
        assert data["summary"] == "sq"

    def test_already_valid_no_transform(self) -> None:
        clean = '{"status": "SUCCESS", "agent_id": "A1"}'
        repaired, n = deterministic_local_repair(clean)
        assert n == 0
        assert repaired == clean


# ---------------------------------------------------------------------------
# Gate 3 — Schema validation & fail-closed
# ---------------------------------------------------------------------------


class TestSchemaValidation:
    def test_valid_payload_passes(self) -> None:
        raw = '{"status": "SUCCESS", "agent_id": "A1", "summary": "ok", "score": 0.9}'
        result = enforce_output_contract(raw, schema=SimpleAgentOutput)
        assert isinstance(result, OutputContractResult)
        assert result.is_compliant
        assert result.repair_turns_used == 0
        assert result.payload.status == "SUCCESS"
        assert result.payload.score == 0.9

    def test_missing_required_field_fails_closed(self) -> None:
        raw = '{"status": "SUCCESS"}'  # missing agent_id
        with pytest.raises(SchemaComplianceError) as ei:
            enforce_output_contract(raw, schema=SimpleAgentOutput)
        assert ei.value.reason_code == "SCHEMA_COMPLIANCE_FAILED"
        assert ei.value.repair_attempted is False
        assert len(ei.value.validation_errors) >= 1

    def test_wrong_type_fails_closed(self) -> None:
        raw = '{"status": "SUCCESS", "agent_id": "A1", "score": "not-a-number"}'
        with pytest.raises(SchemaComplianceError):
            enforce_output_contract(raw, schema=SimpleAgentOutput)

    def test_no_schema_accepts_any_json_object(self) -> None:
        raw = '{"arbitrary": true, "nested": {"x": 1}}'
        result = enforce_output_contract(raw, schema=None)
        assert result.payload["arbitrary"] is True

    def test_markdown_plus_schema_success(self) -> None:
        raw = """```json
{"status": "SUCCESS", "agent_id": "fence-agent", "summary": "via fence"}
```"""
        result = enforce_output_contract(raw, schema=SimpleAgentOutput)
        assert result.payload.agent_id == "fence-agent"
        assert result.repair_turns_used == 0


# ---------------------------------------------------------------------------
# Gate 4 & 5 — Bounded 1-turn model-assisted repair + fail-closed
# ---------------------------------------------------------------------------


class TestBoundedModelRepair:
    def test_one_repair_turn_succeeds(self) -> None:
        """First response is invalid; model_repair_fn returns a valid payload."""
        broken = '{"status": "SUCCESS"}'  # missing agent_id

        def repair_fn(
            raw: str, errors: List[Dict[str, Any]], attempt: int
        ) -> str:
            assert attempt == 1
            assert len(errors) >= 1
            return json.dumps(
                {
                    "status": "SUCCESS",
                    "agent_id": "repaired-agent",
                    "summary": "fixed by model turn",
                }
            )

        result = enforce_output_contract(
            broken,
            schema=SimpleAgentOutput,
            model_repair_fn=repair_fn,
            max_model_repair_turns=1,
        )
        assert result.repair_turns_used == 1
        assert result.payload.agent_id == "repaired-agent"
        stages = [r.stage for r in result.lineage]
        assert RepairStage.MODEL_ASSISTED in stages
        assert RepairStage.VALIDATE in stages

    def test_repair_still_invalid_fails_closed(self) -> None:
        """Model repair returns another invalid payload → fail closed."""
        broken = '{"status": "SUCCESS"}'

        def bad_repair(
            raw: str, errors: List[Dict[str, Any]], attempt: int
        ) -> str:
            return '{"status": "STILL_BROKEN"}'  # still missing agent_id

        with pytest.raises(SchemaComplianceError) as ei:
            enforce_output_contract(
                broken,
                schema=SimpleAgentOutput,
                model_repair_fn=bad_repair,
                max_model_repair_turns=1,
            )
        assert ei.value.repair_attempted is True
        assert "Fail-closed" in str(ei.value) or ei.value.reason_code == "SCHEMA_COMPLIANCE_FAILED"

    def test_no_repair_fn_fails_immediately(self) -> None:
        broken = '{"status": "SUCCESS"}'
        with pytest.raises(SchemaComplianceError) as ei:
            enforce_output_contract(broken, schema=SimpleAgentOutput, model_repair_fn=None)
        assert ei.value.repair_attempted is False

    def test_max_turns_clamped_to_one(self) -> None:
        """Even if caller passes max_model_repair_turns=5, only one turn runs."""
        call_count = {"n": 0}

        def counting_repair(
            raw: str, errors: List[Dict[str, Any]], attempt: int
        ) -> str:
            call_count["n"] += 1
            # Always return invalid so a second turn would be tempting
            return '{"status": "STILL_BROKEN"}'

        with pytest.raises(SchemaComplianceError):
            enforce_output_contract(
                '{"status": "SUCCESS"}',
                schema=SimpleAgentOutput,
                model_repair_fn=counting_repair,
                max_model_repair_turns=5,  # clamped internally to 1
            )
        assert call_count["n"] == 1

    def test_local_repair_avoids_model_turn(self) -> None:
        """Trailing-comma payload is fixed locally; model_repair_fn never called."""
        broken = '{"status": "SUCCESS", "agent_id": "local", "summary": "ok",}'
        called = {"n": 0}

        def should_not_run(
            raw: str, errors: List[Dict[str, Any]], attempt: int
        ) -> str:
            called["n"] += 1
            return raw

        result = enforce_output_contract(
            broken,
            schema=SimpleAgentOutput,
            model_repair_fn=should_not_run,
        )
        assert called["n"] == 0
        assert result.repair_turns_used == 0
        assert result.local_repairs_applied >= 1
        assert result.payload.agent_id == "local"


# ---------------------------------------------------------------------------
# False-proof defenses & helpers
# ---------------------------------------------------------------------------


class TestFalseProofDefenses:
    def test_empty_response_never_succeeds(self) -> None:
        with pytest.raises(JSONExtractionError):
            enforce_output_contract("", schema=SimpleAgentOutput)

    def test_prose_only_never_succeeds(self) -> None:
        with pytest.raises(JSONExtractionError):
            enforce_output_contract(
                "I am unable to produce structured output at this time.",
                schema=SimpleAgentOutput,
            )

    def test_parse_and_validate_wrapper(self) -> None:
        raw = '{"status": "SUCCESS", "agent_id": "wrap", "summary": "ok"}'
        payload = parse_and_validate(raw, SimpleAgentOutput)
        assert payload.agent_id == "wrap"

    def test_parse_and_validate_raises_on_invalid(self) -> None:
        with pytest.raises(SchemaComplianceError):
            parse_and_validate('{"status": "SUCCESS"}', SimpleAgentOutput)

    def test_lineage_records_present_on_success(self) -> None:
        raw = '{"status": "SUCCESS", "agent_id": "lin", "summary": "ok"}'
        result = enforce_output_contract(raw, schema=SimpleAgentOutput)
        assert len(result.lineage) >= 2
        assert any(r.stage == RepairStage.EXTRACT for r in result.lineage)
        assert any(r.stage == RepairStage.VALIDATE and r.success for r in result.lineage)

    def test_nested_schema(self) -> None:
        raw = '{"items": ["a", "b"], "meta": {"k": 1}}'
        result = enforce_output_contract(raw, schema=NestedOutput)
        assert result.payload.items == ["a", "b"]
        assert result.payload.meta["k"] == 1

    def test_model_repair_fn_exception_fails_closed(self) -> None:
        def exploding(
            raw: str, errors: List[Dict[str, Any]], attempt: int
        ) -> str:
            raise RuntimeError("model blew up")

        with pytest.raises(SchemaComplianceError) as ei:
            enforce_output_contract(
                '{"status": "SUCCESS"}',
                schema=SimpleAgentOutput,
                model_repair_fn=exploding,
            )
        assert ei.value.repair_attempted is True
        assert "model blew up" in str(ei.value) or "callback failed" in str(ei.value).lower()


# ---------------------------------------------------------------------------
# Integration-style: full pipeline with prose + local repair + schema
# ---------------------------------------------------------------------------


class TestEndToEndPipeline:
    def test_prose_fence_trailing_comma_local_success(self) -> None:
        raw = """
I analysed the request and here is the structured result:

```json
{
  "status": "SUCCESS",
  "agent_id": "e2e-agent",
  "summary": "end-to-end",
  "score": 0.95,
}
```

Let me know if you need more.
"""
        result = enforce_output_contract(raw, schema=SimpleAgentOutput)
        assert result.payload.agent_id == "e2e-agent"
        assert result.payload.score == 0.95
        assert result.repair_turns_used == 0
        assert result.local_repairs_applied >= 1

    def test_prose_invalid_then_model_repair(self) -> None:
        raw = """
The answer is:

```json
{"status": "SUCCESS"}
```
"""

        def repair(
            text: str, errors: List[Dict[str, Any]], attempt: int
        ) -> str:
            return json.dumps(
                {
                    "status": "SUCCESS",
                    "agent_id": "model-fixed",
                    "summary": "recovered",
                    "score": 1.0,
                }
            )

        result = enforce_output_contract(
            raw,
            schema=SimpleAgentOutput,
            model_repair_fn=repair,
        )
        assert result.payload.agent_id == "model-fixed"
        assert result.repair_turns_used == 1
