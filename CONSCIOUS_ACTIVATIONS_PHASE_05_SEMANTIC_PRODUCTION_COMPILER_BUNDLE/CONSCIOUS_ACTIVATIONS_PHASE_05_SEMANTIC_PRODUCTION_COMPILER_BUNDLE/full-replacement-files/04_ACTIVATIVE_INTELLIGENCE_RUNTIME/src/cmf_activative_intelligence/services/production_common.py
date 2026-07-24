from __future__ import annotations

from typing import Any, Iterable, Mapping

from ca_contracts import canonical_sha256

from ..repositories.air_repository import AirRepository, ObjectNotFound, StoredAirObject


def immutable_ref(value: Mapping[str, Any]) -> dict[str, str]:
    return {
        "object_id": str(value["object_id"]),
        "version": str(value["semantic_version"]),
        "sha256": str(value["canonical_sha256"]),
    }


def require_air_ref(
    repository: AirRepository,
    ref: Mapping[str, Any],
    *,
    object_types: str | Iterable[str] | None = None,
) -> StoredAirObject:
    stored = repository.get_object(str(ref["object_id"]))
    allowed = {object_types} if isinstance(object_types, str) else set(object_types or ())
    if allowed and stored.object_type not in allowed:
        raise ValueError(
            f"{ref['object_id']} identifies {stored.object_type}, expected one of {sorted(allowed)}"
        )
    if stored.semantic_version != str(ref["version"]):
        raise ValueError(f"{ref['object_id']} semantic version mismatch")
    if stored.canonical_sha256 != str(ref["sha256"]):
        raise ValueError(f"{ref['object_id']} hash mismatch")
    return stored


def optional_external_or_air_ref(
    repository: AirRepository,
    ref: Mapping[str, Any],
    *,
    object_types: str | Iterable[str] | None = None,
) -> StoredAirObject | None:
    try:
        return require_air_ref(repository, ref, object_types=object_types)
    except ObjectNotFound:
        return None


def signature_for(payload: Mapping[str, Any], *, exclude: Iterable[str]) -> str:
    excluded = set(exclude)
    return canonical_sha256({key: value for key, value in payload.items() if key not in excluded})


def stored_result_ref(result: Mapping[str, Any]) -> dict[str, str]:
    obj = result["object"]
    return {
        "object_id": str(obj["object_id"]),
        "version": str(obj["semantic_version"]),
        "sha256": str(obj["canonical_sha256"]),
    }


def add_lineage_edges(
    repository: AirRepository,
    *,
    source_result: Mapping[str, Any],
    relation_type: str,
    target_refs: Iterable[Mapping[str, Any]],
    evidence: Mapping[str, Any],
) -> list[dict[str, Any]]:
    source_ref = stored_result_ref(source_result)
    return [
        repository.add_object_edge(
            source_ref=source_ref,
            relation_type=relation_type,
            target_ref=dict(target_ref),
            evidence=dict(evidence),
        )
        for target_ref in target_refs
    ]
