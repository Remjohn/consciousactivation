from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from .canonical import (
    exact_keys,
    immutable_ref,
    require_enum,
    require_int,
    require_portable_uri,
    require_ref,
    require_sha,
    require_source_span,
    require_string,
    semantic_id,
)
from .errors import ValidationError

ADMISSION_MODES = {"IMPORTED", "BRIEF_LED"}
SOURCE_KINDS = {"INTERVIEW_EXPRESSION", "NON_INTERVIEW"}
SLOT_STATES = {"PENDING_REQUIRED_COMPONENT", "BOUND", "NOT_APPLICABLE", "INVALIDATED"}
EPISTEMIC_STATES = {"PLANNED", "OBSERVED", "INFERRED", "OPERATOR_CONFIRMED", "REJECTED", "SUPERSEDED"}
SPEAKER_STATES = {"RESOLVED", "UNKNOWN", "OVERLAP"}
TAG_STATES = EPISTEMIC_STATES
REACTION_OUTCOMES = {
    "ANCHOR_HIT", "PARTIAL_HIT", "UNEXPECTED_EDGE", "STATE_TRANSITION", "FLAT_ANSWER",
    "DEFENSIVE_REACTION", "TOPIC_ESCAPE", "SILENCE", "CONTRADICTION", "LANDING_REACHED",
    "ACTIVATION_NULL",
}
MODALITY_STATES = {"PRESENT", "ABSENT_NOT_CAPTURED", "NOT_APPLICABLE"}
SESSION_STATES = {"ACTIVE", "PAUSED", "LANDED", "STOPPED", "CANCELLED"}
CALL_ORIGINS = {"AIR_OPTION_EXACT", "AIR_OPTION_ADAPTED", "SPONTANEOUS_HUMAN", "NONVERBAL_ACTION"}


def make_media_asset(*, logical_uri: str, sha256: str, bytes_count: int, media_type: str, technical: Mapping[str, Any]) -> dict[str, Any]:
    core = {
        "logical_uri": require_portable_uri(logical_uri),
        "sha256": require_sha(sha256, "media.sha256"),
        "bytes": require_int(bytes_count, "media.bytes", minimum=1),
        "media_type": require_string(media_type, "media.media_type"),
        "technical": dict(technical),
    }
    core["asset_id"] = semantic_id("ie:media", core)
    return core


def component_slot(*, state: str, ref: Mapping[str, Any] | None = None, reason: str | None = None) -> dict[str, Any]:
    state = require_enum(state, SLOT_STATES, "component.state")
    if state == "BOUND":
        if ref is None:
            raise ValidationError("BOUND component requires ref")
        return {"state": state, "ref": require_ref(ref), "reason": "NOT_APPLICABLE"}
    if ref is not None:
        raise ValidationError(f"{state} component cannot carry ref")
    if state == "NOT_APPLICABLE":
        return {"state": state, "ref": "NOT_APPLICABLE", "reason": require_string(reason, "component.reason")}
    return {"state": state, "ref": "NOT_APPLICABLE", "reason": require_string(reason or state, "component.reason")}


def make_source_span(*, source_ref: Mapping[str, str], start_ms: int, end_ms: int, speaker_id: str) -> dict[str, Any]:
    return require_source_span({
        "source_id": source_ref["object_id"],
        "source_version": source_ref["version"],
        "source_sha256": source_ref["sha256"],
        "start_ms": start_ms,
        "end_ms": end_ms,
        "speaker_id": speaker_id,
    })


def make_tag_assertion(*, tag: str, epistemic_state: str, source_spans: list[Mapping[str, Any]], actor_id: str, evidence_refs: list[Mapping[str, Any]], rationale: str) -> dict[str, Any]:
    state = require_enum(epistemic_state, TAG_STATES, "tag.epistemic_state")
    spans = [require_source_span(item, f"source_spans[{i}]") for i, item in enumerate(source_spans)]
    evidence = [require_ref(item, f"evidence_refs[{i}]") for i, item in enumerate(evidence_refs)]
    core = {
        "tag": require_string(tag, "tag"),
        "epistemic_state": state,
        "source_spans": sorted(spans, key=lambda x: (x["start_ms"], x["end_ms"], x["speaker_id"])),
        "actor_id": require_string(actor_id, "actor_id"),
        "evidence_refs": sorted(evidence, key=lambda x: x["object_id"]),
        "rationale": require_string(rationale, "rationale"),
    }
    core["tag_assertion_id"] = semantic_id("ie:tag", core)
    return core


def validate_planning_lineage(mode: str, lineage: Mapping[str, Any]) -> dict[str, Any]:
    if mode == "IMPORTED":
        exact_keys(lineage, {"state"}, "planning_lineage")
        if lineage["state"] != "ABSENT_NOT_CREATED":
            raise ValidationError("imported admission must preserve ABSENT_NOT_CREATED planning lineage")
        return {"state": "ABSENT_NOT_CREATED"}
    required = {"state", "brief_ref", "planned_aip_ref", "iac_ref", "arm_receipt_ref", "planned_object_digests"}
    exact_keys(lineage, required, "planning_lineage")
    if lineage["state"] != "PRESENT_VERIFIED":
        raise ValidationError("Brief-led planning lineage must be PRESENT_VERIFIED")
    refs = {name: require_ref(lineage[name], f"planning_lineage.{name}") for name in ["brief_ref", "planned_aip_ref", "iac_ref", "arm_receipt_ref"]}
    digests = lineage["planned_object_digests"]
    if not isinstance(digests, Mapping) or set(digests) != {"brief", "planned_aip", "iac"}:
        raise ValidationError("planned_object_digests has invalid shape")
    normalized = {name: require_sha(value, f"planned_object_digests.{name}") for name, value in digests.items()}
    if normalized["brief"] != refs["brief_ref"]["sha256"] or normalized["planned_aip"] != refs["planned_aip_ref"]["sha256"] or normalized["iac"] != refs["iac_ref"]["sha256"]:
        raise ValidationError("INT_ARMED_PLAN_HASH_MISMATCH")
    return {"state": "PRESENT_VERIFIED", **refs, "planned_object_digests": normalized}
