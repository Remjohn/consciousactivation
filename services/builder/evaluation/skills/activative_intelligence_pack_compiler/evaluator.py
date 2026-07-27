from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Mapping


ALLOWED_STATUSES = (
    "development_validated",
    "insufficient_evidence",
    "shadow_ready",
    "certified",
)
CAMPAIGN_CEILING = "development_validated"
EVALUATOR_ID = "activative_intelligence_pack_compiler_development_evaluator"
EVALUATOR_VERSION = "1.0.0"


@dataclass(frozen=True, slots=True)
class EvaluationReceipt:
    case_id: str
    case_hash: str
    rubric_hash: str
    evaluation_subject_ref: str
    evaluation_subject_hash: str
    status: str
    dimension_verdicts: tuple[tuple[str, str], ...]
    hard_gate_failures: tuple[str, ...]
    evaluator_id: str
    evaluator_version: str
    receipt_hash: str


def canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def sha256_id(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def load_case(base_path: Path, case_path: Path) -> dict[str, object]:
    base = read_json(base_path)
    overlay = read_json(case_path)
    if overlay.get("extends") != base_path.name:
        raise ValueError(f"Case does not pin its governed base fixture: {case_path}")
    merged = _deep_merge(base, {key: value for key, value in overlay.items() if key != "extends"})
    return merged


def evaluate_case(
    case: Mapping[str, object],
    rubric: Mapping[str, object],
    *,
    requested_status: str = CAMPAIGN_CEILING,
) -> EvaluationReceipt:
    if requested_status not in ALLOWED_STATUSES:
        raise ValueError(f"Unsupported maturity status: {requested_status}")

    dimensions = tuple(str(item) for item in rubric["dimensions"])
    allowed_verdicts = set(str(item) for item in rubric["allowed_dimension_verdicts"])
    labels = _mapping(case, "independent_labels")
    if set(labels) != set(dimensions):
        raise ValueError("Every governed dimension requires exactly one independent label.")
    if any(str(value) not in allowed_verdicts for value in labels.values()):
        raise ValueError("A dimension label uses an ungoverned verdict.")

    failures = set(_hard_gate_failures(case, labels))
    if requested_status in {"shadow_ready", "certified"}:
        failures.add("MATURITY_CEILING_EXCEEDED")

    status = (
        CAMPAIGN_CEILING
        if not failures
        and all(str(labels[item]) in {"pass", "weak_acceptable"} for item in dimensions)
        else "insufficient_evidence"
    )
    case_hash = sha256_id(canonical_bytes(case))
    rubric_hash = sha256_id(canonical_bytes(rubric))
    subject = _mapping(case, "evaluation_subject")
    dimension_verdicts = tuple((item, str(labels[item])) for item in dimensions)
    hard_gate_failures = tuple(sorted(failures))
    unsigned = {
        "case_id": str(case["case_id"]),
        "case_hash": case_hash,
        "rubric_hash": rubric_hash,
        "evaluation_subject_ref": str(subject["ref"]),
        "evaluation_subject_hash": str(subject["hash"]),
        "status": status,
        "dimension_verdicts": dimension_verdicts,
        "hard_gate_failures": hard_gate_failures,
        "evaluator_id": EVALUATOR_ID,
        "evaluator_version": EVALUATOR_VERSION,
    }
    return EvaluationReceipt(**unsigned, receipt_hash=sha256_id(canonical_bytes(unsigned)))


def _hard_gate_failures(
    case: Mapping[str, object], labels: Mapping[str, object]
) -> tuple[str, ...]:
    inputs = _mapping(case, "input")
    candidate = _mapping(case, "candidate")
    call = _mapping(candidate, "activative_call")
    failures: set[str] = set()

    evidence_refs = _strings(inputs.get("source_evidence_refs"))
    provenance_refs = _strings(candidate.get("evidence_provenance_refs"))
    if not evidence_refs or not set(evidence_refs).issubset(provenance_refs):
        failures.add("MISSING_EVIDENCE")
    if candidate.get("authority_override_attempt") is True:
        failures.add("AUTHORITY_CONTRADICTION")
    if candidate.get("semantic_fields_flattened") is True:
        failures.add("SEMANTIC_FLATTENING")
    if candidate.get("identity_dna_ref") != inputs.get("identity_dna_ref"):
        failures.add("IDENTITY_DRIFT")
    if candidate.get("audience_context_ref") != inputs.get("audience_context_ref"):
        failures.add("AUDIENCE_CONTEXT_DRIFT")
    if candidate.get("identity_role") not in _strings(inputs.get("allowed_identity_roles")):
        failures.add("INVENTED_HUMAN_TRUTH")
    if candidate.get("audience_reality") not in _strings(inputs.get("audience_reality_claims")):
        failures.add("INVENTED_HUMAN_TRUTH")
    if (
        candidate.get("observed_reaction") is not None
        or candidate.get("reaction_receipt") is not None
        or call.get("claimed_human_reaction") is True
    ):
        failures.add("INVENTED_HUMAN_REACTION")
    required_locks = set(_strings(inputs.get("wrong_reading_locks")))
    observed_locks = set(_strings(candidate.get("wrong_reading_locks")))
    if not required_locks or not required_locks.issubset(observed_locks):
        failures.add("WRONG_READING_LOCK_WEAKENED")
    if not _lineage_complete(inputs, candidate):
        failures.add("LINEAGE_INCOMPLETE")
    if labels.get("non_generic_pressure") == "fail":
        failures.add("GENERIC_MOTIVATIONAL_LANGUAGE")
    if (
        labels.get("correct_human_role") == "fail"
        or labels.get("desired_reaction") == "fail"
        or labels.get("micro_commitment_integrity") == "fail"
        or not call.get("assigned_role")
        or call.get("asks_micro_commitment") is not True
    ):
        failures.add("FALSE_ACTIVATIVE_CALL")
    if labels.get("non_invention_of_human_truth") in {"fail", "insufficient_evidence"}:
        failures.add("INVENTED_HUMAN_TRUTH")
    return tuple(sorted(failures))


def _lineage_complete(
    inputs: Mapping[str, object], candidate: Mapping[str, object]
) -> bool:
    lineage = candidate.get("field_lineage")
    if not isinstance(lineage, dict):
        return False
    required_fields = (
        "identity_role",
        "audience_reality",
        "edge_pressure",
        "correct_human_role",
        "desired_reaction",
        "micro_commitment",
        "wrong_reading_locks",
    )
    evidence_refs = set(_strings(inputs.get("source_evidence_refs")))
    for field in required_fields:
        refs = _strings(lineage.get(field))
        if not refs or not set(refs).issubset(evidence_refs):
            return False
    return True


def _mapping(value: Mapping[str, object], key: str) -> Mapping[str, object]:
    result = value.get(key)
    if not isinstance(result, dict):
        raise ValueError(f"{key} must be a mapping.")
    return result


def _strings(value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        return ()
    return tuple(value)


def _deep_merge(base: object, overlay: object) -> object:
    if isinstance(base, dict) and isinstance(overlay, dict):
        result = dict(base)
        for key, value in overlay.items():
            result[key] = _deep_merge(result[key], value) if key in result else value
        return result
    return overlay

