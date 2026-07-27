"""Portable wrong-reading-lock inheritance validation for derivative artifacts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .canonical import canonical_hash


DETERMINISTIC_DERIVATIONS = {
    "DETERMINISTIC_CROP",
    "DETERMINISTIC_RESIZE",
    "DETERMINISTIC_FORMAT_CONVERSION",
    "DETERMINISTIC_COMPOSITE",
}
SEMANTIC_DERIVATIONS = {
    "SEMANTIC_TRANSFORMATION",
    "TRANSFORMATIVE_RECOMPOSITION",
}

LOCK_INHERITANCE_VALID = "LOCK_INHERITANCE_VALID"
PARENT_LOCK_EVIDENCE_REQUIRED = "PARENT_LOCK_EVIDENCE_REQUIRED"
PARENT_LOCK_REMOVED = "PARENT_LOCK_REMOVED"
PARENT_LOCK_WEAKENED = "PARENT_LOCK_WEAKENED"
UNAUTHORIZED_LOCK_RELAXATION = "UNAUTHORIZED_LOCK_RELAXATION"
DERIVATION_CLASSIFICATION_REQUIRED = "DERIVATION_CLASSIFICATION_REQUIRED"


def _outcome(status: str, *, valid: bool = False, **details: Any) -> dict[str, Any]:
    return {"status": status, "valid": valid, **details}


def _lock_map(locks: Any) -> dict[str, dict[str, Any]] | None:
    if not isinstance(locks, list) or not locks:
        return None
    result: dict[str, dict[str, Any]] = {}
    for lock in locks:
        if not isinstance(lock, dict) or set(lock) != {
            "lock_id",
            "statement",
            "meaning_hash",
            "scope_paths",
            "enforcement_level",
        }:
            return None
        lock_id = lock.get("lock_id")
        statement = lock.get("statement")
        scope_paths = lock.get("scope_paths")
        level = lock.get("enforcement_level")
        if (
            not isinstance(lock_id, str)
            or not lock_id
            or lock_id in result
            or not isinstance(statement, str)
            or not statement
            or lock.get("meaning_hash") != canonical_hash(statement)
            or not isinstance(scope_paths, list)
            or not scope_paths
            or any(not isinstance(path, str) for path in scope_paths)
            or len(set(scope_paths)) != len(scope_paths)
            or not isinstance(level, int)
            or isinstance(level, bool)
            or not 1 <= level <= 100
        ):
            return None
        result[lock_id] = lock
    return result


def _resolve_parent_locks(
    claim: dict[str, Any], resolved_parent_evidence: dict[str, Any] | list[dict[str, Any]] | None
) -> list[dict[str, Any]] | None:
    evidence = claim.get("parent_lock_evidence")
    if not isinstance(evidence, dict):
        return None
    locks = evidence.get("parent_wrong_reading_locks")
    if locks is None:
        if evidence.get("parent_lock_set_ref") is None or resolved_parent_evidence is None:
            return None
        if isinstance(resolved_parent_evidence, list):
            locks = resolved_parent_evidence
        elif isinstance(resolved_parent_evidence, dict):
            if (
                resolved_parent_evidence.get("parent_lock_set_ref") is not None
                and resolved_parent_evidence.get("parent_lock_set_ref")
                != evidence.get("parent_lock_set_ref")
            ):
                return None
            locks = resolved_parent_evidence.get("parent_wrong_reading_locks")
        else:
            return None
    if _lock_map(locks) is None:
        return None
    if evidence.get("parent_lock_set_hash") != canonical_hash(locks):
        return None
    return deepcopy(locks)


def _relaxation(
    parent: dict[str, dict[str, Any]], derivative: dict[str, dict[str, Any]]
) -> tuple[str | None, list[str]]:
    removed = sorted(set(parent) - set(derivative))
    if removed:
        return PARENT_LOCK_REMOVED, removed
    weakened: list[str] = []
    for lock_id, parent_lock in parent.items():
        derivative_lock = derivative[lock_id]
        if (
            derivative_lock["statement"] != parent_lock["statement"]
            or derivative_lock["meaning_hash"] != parent_lock["meaning_hash"]
            or not set(parent_lock["scope_paths"]).issubset(derivative_lock["scope_paths"])
            or derivative_lock["enforcement_level"] < parent_lock["enforcement_level"]
        ):
            weakened.append(lock_id)
    return (PARENT_LOCK_WEAKENED, weakened) if weakened else (None, [])


def _is_new_authoritative_demand(
    governing: Any, authorization: dict[str, Any]
) -> bool:
    if not isinstance(governing, dict):
        return False
    successor = authorization.get("authoritative_demand_ref")
    supersedes = authorization.get("supersedes_demand_ref")
    return bool(
        isinstance(successor, dict)
        and successor.get("request_id") == governing.get("request_id")
        and isinstance(successor.get("version"), int)
        and isinstance(governing.get("version"), int)
        and successor["version"] > governing["version"]
        and successor.get("payload_hash") != governing.get("payload_hash")
        and successor.get("canonical_ref") != governing.get("canonical_ref")
        and supersedes == governing
    )


def validate_derivative_lock_inheritance(
    claim: dict[str, Any],
    resolved_parent_evidence: dict[str, Any] | list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate a portable parent/derivative lock claim without repository state."""

    derivation_type = claim.get("derivation_type")
    semantics = claim.get("derivative_semantics")
    is_deterministic = derivation_type in DETERMINISTIC_DERIVATIONS
    is_semantic = derivation_type in SEMANTIC_DERIVATIONS
    if not (
        (is_deterministic and semantics == "NON_SEMANTIC")
        or (is_semantic and semantics == "SEMANTIC_TRANSFORMATIVE")
    ):
        return _outcome(
            DERIVATION_CLASSIFICATION_REQUIRED,
            reason="Derivation type and semantic classification must be explicit and consistent.",
        )

    from .contracts import validate_payload

    try:
        validate_payload("derivative-lock-inheritance", claim)
    except Exception as exc:
        return _outcome("DERIVATIVE_LOCK_CONTRACT_INVALID", reason=str(exc))

    parent_locks = _resolve_parent_locks(claim, resolved_parent_evidence)
    if parent_locks is None:
        return _outcome(
            PARENT_LOCK_EVIDENCE_REQUIRED,
            reason="Inline or resolved immutable parent lock evidence is required and must match its hash.",
        )
    parent = _lock_map(parent_locks)
    derivative = _lock_map(claim.get("derivative_wrong_reading_locks"))
    if parent is None:
        return _outcome(PARENT_LOCK_EVIDENCE_REQUIRED)
    if derivative is None:
        return _outcome("DERIVATIVE_LOCK_EVIDENCE_INVALID")

    relaxation_code, affected_locks = _relaxation(parent, derivative)
    if is_deterministic:
        if relaxation_code:
            return _outcome(
                relaxation_code,
                affected_lock_ids=affected_locks,
                requires_new_authoritative_demand=True,
            )
        return _outcome(
            LOCK_INHERITANCE_VALID,
            valid=True,
            inherited_lock_ids=sorted(parent),
            added_lock_ids=sorted(set(derivative) - set(parent)),
            authorized_relaxation=False,
        )

    authorization = claim.get("authoritative_lock_authorization")
    if not isinstance(authorization, dict):
        return _outcome(
            UNAUTHORIZED_LOCK_RELAXATION,
            reason="Semantic derivatives require an explicit authoritative applicable lock set.",
            requires_new_authoritative_demand=bool(relaxation_code),
        )
    authorized = _lock_map(authorization.get("applicable_wrong_reading_locks"))
    if authorized is None or authorization.get("applicable_wrong_reading_locks") != claim.get(
        "derivative_wrong_reading_locks"
    ):
        return _outcome(
            UNAUTHORIZED_LOCK_RELAXATION,
            reason="The derivative lock set must exactly match the authoritative applicable lock set.",
            requires_new_authoritative_demand=bool(relaxation_code),
        )
    if relaxation_code and not _is_new_authoritative_demand(
        claim.get("governing_authoritative_demand_ref"), authorization
    ):
        return _outcome(
            UNAUTHORIZED_LOCK_RELAXATION,
            affected_lock_ids=affected_locks,
            requires_new_authoritative_demand=True,
        )
    if not relaxation_code and authorization.get("authoritative_demand_ref") != claim.get(
        "governing_authoritative_demand_ref"
    ) and not _is_new_authoritative_demand(
        claim.get("governing_authoritative_demand_ref"), authorization
    ):
        return _outcome(
            UNAUTHORIZED_LOCK_RELAXATION,
            reason="Applicable locks must be authorized by the governing or a successor demand.",
        )
    return _outcome(
        LOCK_INHERITANCE_VALID,
        valid=True,
        inherited_lock_ids=sorted(set(parent) & set(derivative)),
        added_lock_ids=sorted(set(derivative) - set(parent)),
        authorized_relaxation=bool(relaxation_code),
    )


def migrate_legacy_derivative_lock_claim(
    source: dict[str, Any], authoritative_evidence: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Refuse to infer classification or parent locks for legacy derivative records."""

    if source.get("derivation_type") is None or source.get("derivative_semantics") is None:
        return _outcome(
            DERIVATION_CLASSIFICATION_REQUIRED,
            migration="NOT_PERFORMED",
            authoritative_classification_required=True,
        )
    if authoritative_evidence is None:
        return _outcome(
            PARENT_LOCK_EVIDENCE_REQUIRED,
            migration="NOT_PERFORMED",
            authoritative_parent_evidence_required=True,
        )
    target = deepcopy(source)
    target["parent_lock_evidence"] = deepcopy(authoritative_evidence)
    outcome = validate_derivative_lock_inheritance(target)
    if not outcome["valid"]:
        return {**outcome, "migration": "NOT_PERFORMED"}
    return {"status": "MIGRATED", "valid": True, "migration": "PERFORMED", "target": target}
