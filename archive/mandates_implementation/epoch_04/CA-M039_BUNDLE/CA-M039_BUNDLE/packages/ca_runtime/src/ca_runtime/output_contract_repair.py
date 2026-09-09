"""Deterministic Output Contract & Bounded Self-Repair (CA-M039 / INV-OUT-001).

Enforce strict JSON / Pydantic schema validation on all program outputs.
Apply bounded, deterministic AST-style self-repair to malformed LLM responses,
and fail closed if repair cannot achieve 100% schema compliance.

Governing authority:
- Mandate CA-M039 (Deterministic Output Contract & Self-Repair)
- Invariant INV-OUT-001
- Canon Q39: greedy JSON extraction + 1-turn bounded schema self-repair + fail-closed

Design invariants:
1. Greedy extraction tolerates markdown fences and prose wrapping.
2. Local deterministic repair is pure and bounded (no unbounded loops).
3. At most one model-assisted repair turn is permitted.
4. After the single repair attempt, validation failure raises fail-closed.
5. No silent acceptance of non-compliant payloads.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

try:
    from pydantic import BaseModel, ValidationError
except ImportError:  # pragma: no cover - project always has pydantic
    BaseModel = object  # type: ignore
    ValidationError = Exception  # type: ignore

T = TypeVar("T", bound="BaseModel")

# ---------------------------------------------------------------------------
# Public error taxonomy (fail-closed surface)
# ---------------------------------------------------------------------------


class OutputContractError(RuntimeError):
    """Base for all output-contract / repair failures."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "OUTPUT_CONTRACT_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class JSONExtractionError(OutputContractError):
    """No extractable JSON object/array found in model response."""

    def __init__(self, message: str, *, raw_text: str = "") -> None:
        super().__init__(
            message,
            reason_code="JSON_EXTRACTION_FAILED",
            details={"raw_text_preview": (raw_text or "")[:512]},
        )


class SchemaComplianceError(OutputContractError):
    """Payload failed Pydantic (or equivalent) schema validation after repair."""

    def __init__(
        self,
        message: str,
        *,
        validation_errors: Optional[List[Dict[str, Any]]] = None,
        raw_text: str = "",
        repair_attempted: bool = False,
    ) -> None:
        super().__init__(
            message,
            reason_code="SCHEMA_COMPLIANCE_FAILED",
            details={
                "validation_errors": validation_errors or [],
                "raw_text_preview": (raw_text or "")[:512],
                "repair_attempted": repair_attempted,
            },
        )
        self.validation_errors = validation_errors or []
        self.repair_attempted = repair_attempted


class RepairBudgetExhaustedError(OutputContractError):
    """More than one model-assisted repair turn was requested (forbidden)."""

    def __init__(self, message: str = "Model-assisted repair budget exhausted (max 1 turn)") -> None:
        super().__init__(message, reason_code="REPAIR_BUDGET_EXHAUSTED")


# ---------------------------------------------------------------------------
# Result / telemetry types
# ---------------------------------------------------------------------------


class RepairStage(str, Enum):
    EXTRACT = "EXTRACT"
    LOCAL_DETERMINISTIC = "LOCAL_DETERMINISTIC"
    MODEL_ASSISTED = "MODEL_ASSISTED"
    VALIDATE = "VALIDATE"


@dataclass(frozen=True)
class RepairAttemptRecord:
    """Immutable record of a single repair stage for audit lineage."""

    stage: RepairStage
    success: bool
    input_preview: str
    output_preview: str
    notes: str = ""
    validation_errors: Tuple[Dict[str, Any], ...] = field(default_factory=tuple)


@dataclass
class OutputContractResult:
    """Successful validated output plus full repair lineage."""

    payload: Any  # validated Pydantic model instance or plain dict
    raw_extracted_json: str
    lineage: List[RepairAttemptRecord] = field(default_factory=list)
    repair_turns_used: int = 0  # model-assisted turns only (0 or 1)
    local_repairs_applied: int = 0

    @property
    def is_compliant(self) -> bool:
        return True


# ---------------------------------------------------------------------------
# Greedy JSON extraction (INV-OUT-001)
# ---------------------------------------------------------------------------

# Matches the outermost balanced JSON object or array, including content that
# may be wrapped in markdown fences or prose. Greedy by design (non-reluctant).
_JSON_OBJECT_RE = re.compile(
    r"(\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})",
    re.DOTALL,
)
_JSON_ARRAY_RE = re.compile(
    r"(\[(?:[^\[\]]|(?:\[(?:[^\[\]]|(?:\[[^\[\]]*\]))*\]))*\])",
    re.DOTALL,
)
_FENCE_RE = re.compile(
    r"```(?:json|JSON)?\s*([\s\S]*?)\s*```",
    re.MULTILINE,
)


def _strip_markdown_fences(text: str) -> str:
    """Remove common markdown code fences while preserving inner content."""
    if not text:
        return text
    m = _FENCE_RE.search(text)
    if m:
        return m.group(1).strip()
    # Fallback: simple line-oriented fence strip
    lines = text.strip().splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def greedy_extract_json(raw_text: str) -> str:
    """Extract the outermost JSON object or array from model text.

    Tolerates:
    - Markdown ```json ... ``` fences
    - Leading / trailing prose
    - Nested objects/arrays (balanced-brace approximation)

    Raises JSONExtractionError if nothing extractable is found.
    """
    if raw_text is None:
        raise JSONExtractionError("raw_text is None", raw_text="")

    text = str(raw_text).strip()
    if not text:
        raise JSONExtractionError("Empty model response", raw_text=text)

    # Prefer fenced content when present
    fenced = _strip_markdown_fences(text)
    candidates = [fenced, text] if fenced != text else [text]

    for candidate in candidates:
        # Direct parse first (fast path for clean JSON)
        try:
            json.loads(candidate)
            return candidate
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

        # Greedy object then array
        for pattern in (_JSON_OBJECT_RE, _JSON_ARRAY_RE):
            match = pattern.search(candidate)
            if match:
                snippet = match.group(1).strip()
                try:
                    json.loads(snippet)
                    return snippet
                except (json.JSONDecodeError, TypeError, ValueError):
                    # Continue searching for a later match that does parse
                    continue

    raise JSONExtractionError(
        "No valid JSON object or array could be extracted from model response",
        raw_text=text,
    )


# ---------------------------------------------------------------------------
# Deterministic local AST-style repair (bounded, pure)
# ---------------------------------------------------------------------------

_TRAILING_COMMA_RE = re.compile(r",(\s*[}\]])")
_SINGLE_QUOTE_KEY_RE = re.compile(r"(?P<prefix>[{,\s])'(?P<key>[^']+)'(\s*):")
_TRUE_FALSE_NULL_RE = re.compile(r"\b(True|False|None)\b")


def _repair_python_literals(text: str) -> str:
    """Convert common Python literals that appear in LLM JSON to JSON literals."""
    return _TRUE_FALSE_NULL_RE.sub(
        lambda m: {"True": "true", "False": "false", "None": "null"}[m.group(1)],
        text,
    )


def _repair_trailing_commas(text: str) -> str:
    """Remove trailing commas before } or ] (common LLM artefact)."""
    prev = None
    cur = text
    # Bounded iterations to avoid pathological cases
    for _ in range(32):
        if cur == prev:
            break
        prev = cur
        cur = _TRAILING_COMMA_RE.sub(r"\1", cur)
    return cur


def _repair_single_quoted_keys(text: str) -> str:
    """Replace single-quoted object keys with double-quoted keys."""
    return _SINGLE_QUOTE_KEY_RE.sub(r'\g<prefix>"\g<key>":', text)


def _try_ast_literal_eval(text: str) -> Optional[Any]:
    """Attempt to interpret as a Python literal (handles single quotes etc.)."""
    try:
        value = ast.literal_eval(text)
        if isinstance(value, (dict, list)):
            return value
    except (SyntaxError, ValueError, MemoryError, TypeError):
        pass
    return None


def deterministic_local_repair(json_text: str) -> Tuple[str, int]:
    """Apply a fixed sequence of pure, deterministic repairs.

    Returns (repaired_text, number_of_transforms_applied).
    Never loops unboundedly; each transform is applied at most a fixed number
    of times.
    """
    if not json_text:
        return json_text, 0

    original = json_text
    current = json_text
    transforms = 0

    # 1. Python literal normalisation
    repaired = _repair_python_literals(current)
    if repaired != current:
        transforms += 1
        current = repaired

    # 2. Trailing commas
    repaired = _repair_trailing_commas(current)
    if repaired != current:
        transforms += 1
        current = repaired

    # 3. Single-quoted keys
    repaired = _repair_single_quoted_keys(current)
    if repaired != current:
        transforms += 1
        current = repaired

    # 4. AST literal_eval fallback (handles remaining single-quoted values etc.)
    try:
        json.loads(current)
        return current, transforms
    except (json.JSONDecodeError, TypeError, ValueError):
        pass

    ast_value = _try_ast_literal_eval(current)
    if ast_value is not None:
        current = json.dumps(ast_value, ensure_ascii=False)
        transforms += 1
        return current, transforms

    # 5. Last resort: strip non-printable control chars except whitespace
    cleaned = "".join(
        ch for ch in current if ch in ("\n", "\r", "\t") or (ord(ch) >= 32)
    )
    if cleaned != current:
        transforms += 1
        current = cleaned

    return current, transforms


# ---------------------------------------------------------------------------
# Schema validation helpers
# ---------------------------------------------------------------------------


def _validation_error_list(exc: Exception) -> List[Dict[str, Any]]:
    """Normalise Pydantic ValidationError (or generic) into a list of dicts."""
    errors: List[Dict[str, Any]] = []
    if hasattr(exc, "errors") and callable(getattr(exc, "errors")):
        try:
            for item in exc.errors():  # type: ignore[attr-defined]
                errors.append(
                    {
                        "loc": list(item.get("loc", [])),
                        "msg": str(item.get("msg", "")),
                        "type": str(item.get("type", "")),
                    }
                )
            return errors
        except Exception:
            pass
    errors.append({"loc": [], "msg": str(exc), "type": type(exc).__name__})
    return errors


def validate_against_schema(
    data: Any,
    schema: Optional[Type[BaseModel]] = None,
    *,
    allow_dict: bool = True,
) -> Any:
    """Validate data against an optional Pydantic model.

    If schema is None and allow_dict is True, requires data to be a dict or list
    (already parsed JSON). Returns the validated model instance or the dict/list.
    Raises SchemaComplianceError on failure.
    """
    if schema is None:
        if allow_dict and isinstance(data, (dict, list)):
            return data
        raise SchemaComplianceError(
            "No schema provided and payload is not a plain dict/list",
            validation_errors=[{"loc": [], "msg": "schema required", "type": "missing_schema"}],
        )

    try:
        if isinstance(data, schema):
            return data
        if hasattr(schema, "model_validate"):
            return schema.model_validate(data)  # pydantic v2
        if hasattr(schema, "parse_obj"):
            return schema.parse_obj(data)  # pydantic v1
        # Fallback constructor
        return schema(**data) if isinstance(data, dict) else schema(data)
    except ValidationError as exc:
        raise SchemaComplianceError(
            f"Schema validation failed: {exc}",
            validation_errors=_validation_error_list(exc),
        ) from exc
    except Exception as exc:
        raise SchemaComplianceError(
            f"Schema validation failed: {exc}",
            validation_errors=_validation_error_list(exc),
        ) from exc


# ---------------------------------------------------------------------------
# Core contract enforcer
# ---------------------------------------------------------------------------

# Type of an optional model-assisted repair callback.
# Signature: (raw_text, validation_errors, attempt_number) -> repaired_raw_text
ModelRepairFn = Callable[[str, List[Dict[str, Any]], int], str]


def enforce_output_contract(
    raw_model_text: str,
    *,
    schema: Optional[Type[BaseModel]] = None,
    model_repair_fn: Optional[ModelRepairFn] = None,
    max_model_repair_turns: int = 1,
) -> OutputContractResult:
    """Enforce INV-OUT-001 on a single model response.

    Pipeline:
    1. Greedy JSON extraction (markdown / prose tolerant).
    2. Deterministic local AST-style repair.
    3. Pydantic (or dict) validation.
    4. If validation fails and a model_repair_fn is supplied, perform at most
       ``max_model_repair_turns`` (default 1) assisted repair turns, then
       re-extract / re-validate.
    5. Fail closed (raise SchemaComplianceError or JSONExtractionError) if
       still non-compliant.

    Parameters
    ----------
    raw_model_text:
        The full text returned by the model (may contain prose or fences).
    schema:
        Optional Pydantic BaseModel subclass. When omitted, any valid JSON
        object/array is accepted.
    model_repair_fn:
        Optional callback used for the single model-assisted repair turn.
        Must be pure with respect to side-effects other than producing a new
        text response. If omitted, only local deterministic repair is applied.
    max_model_repair_turns:
        Hard upper bound; values > 1 are clamped to 1 per INV-OUT-001.
    """
    if max_model_repair_turns < 0:
        max_model_repair_turns = 0
    if max_model_repair_turns > 1:
        # Hard invariant: never more than one model-assisted turn
        max_model_repair_turns = 1

    lineage: List[RepairAttemptRecord] = []
    local_repairs = 0
    model_turns = 0
    current_raw = raw_model_text

    def _attempt_pipeline(text: str, stage_prefix: str) -> Tuple[Any, str]:
        nonlocal local_repairs
        # Extract
        try:
            extracted = greedy_extract_json(text)
            lineage.append(
                RepairAttemptRecord(
                    stage=RepairStage.EXTRACT,
                    success=True,
                    input_preview=text[:256],
                    output_preview=extracted[:256],
                    notes=f"{stage_prefix}: greedy extraction succeeded",
                )
            )
        except JSONExtractionError as exc:
            lineage.append(
                RepairAttemptRecord(
                    stage=RepairStage.EXTRACT,
                    success=False,
                    input_preview=text[:256],
                    output_preview="",
                    notes=str(exc),
                )
            )
            raise

        # Local deterministic repair
        repaired, n_transforms = deterministic_local_repair(extracted)
        local_repairs += n_transforms
        lineage.append(
            RepairAttemptRecord(
                stage=RepairStage.LOCAL_DETERMINISTIC,
                success=True,
                input_preview=extracted[:256],
                output_preview=repaired[:256],
                notes=f"{stage_prefix}: applied {n_transforms} local transform(s)",
            )
        )

        # Parse JSON
        try:
            data = json.loads(repaired)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            lineage.append(
                RepairAttemptRecord(
                    stage=RepairStage.VALIDATE,
                    success=False,
                    input_preview=repaired[:256],
                    output_preview="",
                    notes=f"json.loads failed after local repair: {exc}",
                )
            )
            raise SchemaComplianceError(
                f"JSON parse failed after deterministic repair: {exc}",
                validation_errors=[{"loc": [], "msg": str(exc), "type": "json_decode"}],
                raw_text=text,
                repair_attempted=model_turns > 0,
            ) from exc

        # Schema validation
        try:
            validated = validate_against_schema(data, schema)
            lineage.append(
                RepairAttemptRecord(
                    stage=RepairStage.VALIDATE,
                    success=True,
                    input_preview=repaired[:256],
                    output_preview=str(type(validated).__name__),
                    notes=f"{stage_prefix}: schema compliance achieved",
                )
            )
            return validated, repaired
        except SchemaComplianceError as exc:
            lineage.append(
                RepairAttemptRecord(
                    stage=RepairStage.VALIDATE,
                    success=False,
                    input_preview=repaired[:256],
                    output_preview="",
                    notes=str(exc),
                    validation_errors=tuple(exc.validation_errors),
                )
            )
            raise

    # --- First pass (extract + local + validate) ---
    try:
        payload, extracted_json = _attempt_pipeline(current_raw, "initial")
        return OutputContractResult(
            payload=payload,
            raw_extracted_json=extracted_json,
            lineage=lineage,
            repair_turns_used=model_turns,
            local_repairs_applied=local_repairs,
        )
    except (JSONExtractionError, SchemaComplianceError) as first_exc:
        first_errors = (
            first_exc.validation_errors
            if isinstance(first_exc, SchemaComplianceError)
            else [{"loc": [], "msg": str(first_exc), "type": first_exc.reason_code}]
        )

    # --- Optional single model-assisted repair turn ---
    if model_repair_fn is None or max_model_repair_turns < 1:
        # Fail closed immediately
        if isinstance(first_exc, JSONExtractionError):
            raise first_exc
        raise SchemaComplianceError(
            f"Schema compliance failed and no model repair available: {first_exc}",
            validation_errors=first_errors,
            raw_text=current_raw,
            repair_attempted=False,
        ) from first_exc

    # Budget check (defensive)
    if model_turns >= max_model_repair_turns:
        raise RepairBudgetExhaustedError()

    model_turns += 1
    try:
        repaired_raw = model_repair_fn(current_raw, first_errors, model_turns)
    except Exception as cb_exc:
        lineage.append(
            RepairAttemptRecord(
                stage=RepairStage.MODEL_ASSISTED,
                success=False,
                input_preview=current_raw[:256],
                output_preview="",
                notes=f"model_repair_fn raised: {cb_exc}",
            )
        )
        raise SchemaComplianceError(
            f"Model-assisted repair callback failed: {cb_exc}",
            validation_errors=first_errors,
            raw_text=current_raw,
            repair_attempted=True,
        ) from cb_exc

    lineage.append(
        RepairAttemptRecord(
            stage=RepairStage.MODEL_ASSISTED,
            success=True,
            input_preview=current_raw[:256],
            output_preview=(repaired_raw or "")[:256],
            notes=f"model-assisted turn {model_turns} completed",
        )
    )
    current_raw = repaired_raw or ""

    # Re-run pipeline after the single repair turn; any failure is final
    try:
        payload, extracted_json = _attempt_pipeline(current_raw, "post-repair")
        return OutputContractResult(
            payload=payload,
            raw_extracted_json=extracted_json,
            lineage=lineage,
            repair_turns_used=model_turns,
            local_repairs_applied=local_repairs,
        )
    except (JSONExtractionError, SchemaComplianceError) as final_exc:
        errors = (
            final_exc.validation_errors
            if isinstance(final_exc, SchemaComplianceError)
            else [{"loc": [], "msg": str(final_exc), "type": final_exc.reason_code}]
        )
        raise SchemaComplianceError(
            f"Fail-closed: schema compliance not achieved after 1 model-assisted repair turn: {final_exc}",
            validation_errors=errors,
            raw_text=current_raw,
            repair_attempted=True,
        ) from final_exc


# ---------------------------------------------------------------------------
# Convenience: parse-or-raise for call sites that already have a schema
# ---------------------------------------------------------------------------


def parse_and_validate(
    raw_model_text: str,
    schema: Type[BaseModel],
    *,
    model_repair_fn: Optional[ModelRepairFn] = None,
) -> Any:
    """Thin wrapper returning only the validated payload (raises on failure)."""
    result = enforce_output_contract(
        raw_model_text,
        schema=schema,
        model_repair_fn=model_repair_fn,
        max_model_repair_turns=1,
    )
    return result.payload


__all__ = [
    "OutputContractError",
    "JSONExtractionError",
    "SchemaComplianceError",
    "RepairBudgetExhaustedError",
    "RepairStage",
    "RepairAttemptRecord",
    "OutputContractResult",
    "greedy_extract_json",
    "deterministic_local_repair",
    "validate_against_schema",
    "enforce_output_contract",
    "parse_and_validate",
    "ModelRepairFn",
]
