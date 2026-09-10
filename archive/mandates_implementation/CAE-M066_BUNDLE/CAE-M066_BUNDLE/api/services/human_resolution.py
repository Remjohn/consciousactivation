from __future__ import annotations

"""CAE-M0066 native editing and immutable human-resolution persistence.

The module owns the narrow campaign/video-edit mutation boundary required by
M0066. It deliberately reuses PipelineRepository's SQLite command transaction
so the canonical campaign revision and the immutable HumanResolutionEpisode
land in one compare-and-swap commit.
"""

from dataclasses import dataclass
from typing import Any, Mapping
from uuid import uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from cmf_pipeline.domain.validation import reject_noncanonical
from cmf_pipeline.domain.errors import PipelineConflict

from api.services.campaign_projection import CAMPAIGN_STATE_TYPE, state_object_id


MAX_TIMING_DELTA_FRAMES = 300
MAX_SOURCE_SHIFT_MS = 5_000
ALLOWED_MANIPULATIONS = {"SUBSTITUTE_ASSET", "ADJUST_TIMING"}
EDITABLE_OPERATIONS_BY_MANIPULATION = {
    "SUBSTITUTE_ASSET": "SUBSTITUTE_ASSET",
    "ADJUST_TIMING": "ADJUST_TIMING",
}


class HumanResolutionValidationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class HumanResolutionStaleError(RuntimeError):
    code = "STALE_STATE_VERSION"


@dataclass(frozen=True)
class NativeEditProgram:
    program_id: str
    campaign_id: str
    expected_state_version: int
    expected_state_revision: int
    operator_actor: dict[str, Any]
    target_ref: dict[str, Any]
    target_node_id: str
    manipulation_type: str
    arguments: dict[str, Any]
    before_timeline_sha256: str
    program_sha256: str
    created_at: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "program_id": self.program_id,
            "campaign_id": self.campaign_id,
            "expected_state_version": self.expected_state_version,
            "expected_state_revision": self.expected_state_revision,
            "operator_actor": dict(self.operator_actor),
            "target_ref": dict(self.target_ref),
            "target_node_id": self.target_node_id,
            "manipulation_type": self.manipulation_type,
            "arguments": dict(self.arguments),
            "before_timeline_sha256": self.before_timeline_sha256,
            "program_sha256": self.program_sha256,
            "created_at": self.created_at,
        }


def _ref(object_id: str, version: str, payload: Mapping[str, Any]) -> dict[str, str]:
    return {"object_id": object_id, "version": version, "sha256": canonical_sha256(payload)}


def _timeline_from_state(state: Mapping[str, Any]) -> dict[str, Any]:
    timeline = state.get("video_edit_program")
    if timeline is None:
        return {
            "width": 1920,
            "height": 1080,
            "fps_numerator": 30,
            "fps_denominator": 1,
            "duration_frames": 0,
            "tracks": [],
            "items": [],
        }
    if not isinstance(timeline, Mapping):
        raise HumanResolutionValidationError("INVALID_TIMELINE", "video_edit_program must be an object")
    return _canonical_timeline(timeline)


def _canonical_timeline(timeline: Mapping[str, Any]) -> dict[str, Any]:
    tracks = []
    items_by_id: dict[str, dict[str, Any]] = {}
    for raw_track in timeline.get("tracks", []):
        track = dict(raw_track)
        raw_items = list(track.get("items", []))
        normalized_items = []
        for raw_item in raw_items:
            item = dict(raw_item)
            item.setdefault("editable_operations", [])
            normalized_items.append(item)
            items_by_id[str(item["item_id"])] = item
        track["items"] = normalized_items
        track["item_ids"] = [str(item["item_id"]) for item in normalized_items]
        tracks.append(track)
    top_level_items = [dict(item) for item in timeline.get("items", [])]
    if not top_level_items:
        top_level_items = [dict(item) for item in items_by_id.values()]
    return {
        "width": int(timeline.get("width", 1920)),
        "height": int(timeline.get("height", 1080)),
        "fps_numerator": int(timeline.get("fps_numerator", 30)),
        "fps_denominator": int(timeline.get("fps_denominator", 1)),
        "duration_frames": int(timeline.get("duration_frames", 0)),
        "tracks": tracks,
        "items": top_level_items,
    }


def _find_item(timeline: Mapping[str, Any], item_id: str) -> tuple[dict[str, Any], dict[str, Any] | None]:
    for item in timeline.get("items", []):
        if str(item.get("item_id")) == item_id:
            return item, None
    for track in timeline.get("tracks", []):
        for item in track.get("items", []):
            if str(item.get("item_id")) == item_id:
                return item, track
    raise HumanResolutionValidationError("TARGET_ITEM_NOT_FOUND", f"timeline item not found: {item_id}")


def _validate_actor(actor: Mapping[str, Any]) -> None:
    if not str(actor.get("actor_id", "")).strip():
        raise HumanResolutionValidationError("INVALID_OPERATOR", "operator_actor.actor_id is required")
    if actor.get("actor_type") != "human":
        raise HumanResolutionValidationError("INVALID_OPERATOR", "operator_actor.actor_type must be human")
    if actor.get("workflow_role") != "operator":
        raise HumanResolutionValidationError("INVALID_OPERATOR", "operator_actor.workflow_role must be operator")


def _validate_edit_request(
    *,
    timeline: Mapping[str, Any],
    target_node_id: str,
    manipulation_type: str,
    arguments: Mapping[str, Any],
) -> dict[str, Any]:
    if manipulation_type not in ALLOWED_MANIPULATIONS:
        raise HumanResolutionValidationError(
            "UNSUPPORTED_MANIPULATION",
            f"manual manipulation must be one of {sorted(ALLOWED_MANIPULATIONS)}",
        )
    item, _track = _find_item(timeline, target_node_id)
    editable = set(str(value) for value in item.get("editable_operations", []))
    required = EDITABLE_OPERATIONS_BY_MANIPULATION[manipulation_type]
    if required not in editable:
        raise HumanResolutionValidationError(
            "EDIT_NOT_PERMITTED",
            f"timeline item {target_node_id} does not permit {manipulation_type}",
        )

    normalized = dict(arguments)
    if manipulation_type == "SUBSTITUTE_ASSET":
        source_ref = normalized.get("source_ref")
        if not isinstance(source_ref, Mapping):
            raise HumanResolutionValidationError("INVALID_ASSET_REF", "source_ref must be an object reference")
        for field in ("object_id", "version", "sha256"):
            if not str(source_ref.get(field, "")).strip():
                raise HumanResolutionValidationError("INVALID_ASSET_REF", f"source_ref.{field} is required")
        normalized["source_ref"] = dict(source_ref)
    else:
        delta_frames = normalized.get("delta_frames")
        if isinstance(delta_frames, bool) or not isinstance(delta_frames, int):
            raise HumanResolutionValidationError("INVALID_TIMING_DELTA", "delta_frames must be an integer")
        if abs(delta_frames) > MAX_TIMING_DELTA_FRAMES:
            raise HumanResolutionValidationError(
                "TIMING_BOUND_EXCEEDED",
                f"delta_frames must be between {-MAX_TIMING_DELTA_FRAMES} and {MAX_TIMING_DELTA_FRAMES}",
            )
        delta_start_ms = normalized.get("source_start_delta_ms", 0)
        delta_end_ms = normalized.get("source_end_delta_ms", 0)
        for field, value in (("source_start_delta_ms", delta_start_ms), ("source_end_delta_ms", delta_end_ms)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise HumanResolutionValidationError("INVALID_SOURCE_DELTA", f"{field} must be an integer")
            if abs(value) > MAX_SOURCE_SHIFT_MS:
                raise HumanResolutionValidationError(
                    "SOURCE_SHIFT_BOUND_EXCEEDED",
                    f"{field} exceeds {MAX_SOURCE_SHIFT_MS} ms bound",
                )
        start = int(item.get("start_frame", 0))
        end = int(item.get("end_frame", 0))
        new_end = end + delta_frames
        if new_end <= start:
            raise HumanResolutionValidationError("INVALID_TIMELINE_RANGE", "adjustment would produce a non-positive item duration")
        if new_end > int(timeline.get("duration_frames", 0)) and int(timeline.get("duration_frames", 0)) > 0:
            raise HumanResolutionValidationError("TIMING_BOUND_EXCEEDED", "adjustment would exceed timeline duration")
    return normalized


def compile_native_edit_program(
    *,
    campaign_id: str,
    state: Mapping[str, Any],
    state_revision: int,
    target_ref: Mapping[str, Any],
    target_node_id: str,
    manipulation_type: str,
    arguments: Mapping[str, Any],
    operator_actor: Mapping[str, Any],
) -> NativeEditProgram:
    _validate_actor(operator_actor)
    timeline = _timeline_from_state(state)
    normalized_arguments = _validate_edit_request(
        timeline=timeline,
        target_node_id=target_node_id,
        manipulation_type=manipulation_type,
        arguments=arguments,
    )
    before_digest = canonical_sha256(timeline)
    now = utc_now_rfc3339()
    body = {
        "campaign_id": campaign_id,
        "expected_state_version": int(state["version"]),
        "expected_state_revision": int(state_revision),
        "target_ref": dict(target_ref),
        "target_node_id": target_node_id,
        "manipulation_type": manipulation_type,
        "arguments": normalized_arguments,
        "operator_actor": dict(operator_actor),
        "before_timeline_sha256": before_digest,
    }
    return NativeEditProgram(
        program_id=f"revision:{uuid4().hex}",
        campaign_id=campaign_id,
        expected_state_version=int(state["version"]),
        expected_state_revision=int(state_revision),
        operator_actor=dict(operator_actor),
        target_ref=dict(target_ref),
        target_node_id=target_node_id,
        manipulation_type=manipulation_type,
        arguments=normalized_arguments,
        before_timeline_sha256=before_digest,
        program_sha256=canonical_sha256(body),
        created_at=now,
    )


def apply_native_edit(timeline: Mapping[str, Any], program: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    before = _canonical_timeline(timeline)
    after = _canonical_timeline(timeline)
    target_node_id = str(program["target_node_id"])
    item, _track = _find_item(after, target_node_id)
    manipulation_type = str(program["manipulation_type"])
    args = dict(program["arguments"])
    changes: list[dict[str, Any]] = []

    if manipulation_type == "SUBSTITUTE_ASSET":
        old = item.get("source_ref")
        new = dict(args["source_ref"])
        item["source_ref"] = new
        changes.append({"path": f"items[{target_node_id}].source_ref", "before": old, "after": new})
        for track in after.get("tracks", []):
            for track_item in track.get("items", []):
                if str(track_item.get("item_id")) == target_node_id:
                    track_item["source_ref"] = dict(new)
    else:
        delta_frames = int(args["delta_frames"])
        old_start = int(item.get("start_frame", 0))
        old_end = int(item.get("end_frame", 0))
        old_source_start = item.get("source_start_ms")
        old_source_end = item.get("source_end_ms")
        item["start_frame"] = old_start
        item["end_frame"] = old_end + delta_frames
        if old_source_start is not None:
            item["source_start_ms"] = int(old_source_start) + int(args.get("source_start_delta_ms", 0))
        if old_source_end is not None:
            item["source_end_ms"] = int(old_source_end) + int(args.get("source_end_delta_ms", 0))
        changes.extend(
            [
                {"path": f"items[{target_node_id}].start_frame", "before": old_start, "after": old_start},
                {"path": f"items[{target_node_id}].end_frame", "before": old_end, "after": old_end + delta_frames},
            ]
        )
        if old_source_start is not None:
            changes.append({"path": f"items[{target_node_id}].source_start_ms", "before": old_source_start, "after": item["source_start_ms"]})
        if old_source_end is not None:
            changes.append({"path": f"items[{target_node_id}].source_end_ms", "before": old_source_end, "after": item["source_end_ms"]})
        for track in after.get("tracks", []):
            for track_item in track.get("items", []):
                if str(track_item.get("item_id")) == target_node_id:
                    track_item.update({k: v for k, v in item.items() if k in {"start_frame", "end_frame", "source_start_ms", "source_end_ms"}})

    before_hash = canonical_sha256(before)
    after_hash = canonical_sha256(after)
    return after, [
        {"path": "timeline", "before_sha256": before_hash, "after_sha256": after_hash, "changes": changes}
    ]


def _store_object_row(connection, *, object_id: str, object_type: str, payload: Mapping[str, Any], idempotency_key: str, timestamp: str, expected_revision: int | None = None) -> dict[str, Any]:
    normalized = dict(payload)
    reject_noncanonical(normalized)
    object_sha = canonical_sha256(normalized)
    current = connection.execute(
        "SELECT * FROM pipeline_objects WHERE object_id = ? AND is_current = 1",
        (object_id,),
    ).fetchone()
    current_revision = int(current["revision"]) if current else 0
    if expected_revision is not None and expected_revision != current_revision:
        raise PipelineConflict(f"expected revision {expected_revision}, current revision {current_revision}")
    if object_type == "human_resolution_episode" and current is not None:
        raise PipelineConflict("HumanResolutionEpisode records are immutable")
    if current and current["canonical_sha256"] == object_sha:
        return {
            "object_id": str(current["object_id"]),
            "revision": current_revision,
            "canonical_sha256": str(current["canonical_sha256"]),
            "payload": dict(normalized),
            "created": False,
        }
    revision = current_revision + 1
    if current:
        connection.execute(
            "UPDATE pipeline_objects SET is_current = 0 WHERE object_id = ? AND revision = ?",
            (object_id, current_revision),
        )
    connection.execute(
        """
        INSERT INTO pipeline_objects(
            object_id, revision, object_type, semantic_version,
            canonical_sha256, payload_json, lifecycle_state, authority_state,
            is_current, idempotency_key, created_at_utc, supersedes_revision
        ) VALUES(?, ?, ?, '1.0.0', ?, ?, 'ACTIVE', 'candidate_not_current', 1, ?, ?, ?)
        """,
        (
            object_id,
            revision,
            object_type,
            object_sha,
            canonical_json_text(normalized),
            idempotency_key,
            timestamp,
            current_revision or None,
        ),
    )
    return {
        "object_id": object_id,
        "revision": revision,
        "canonical_sha256": object_sha,
        "payload": normalized,
        "created": True,
    }


def commit_native_edit(
    *,
    pipeline: Any,
    campaign_id: str,
    program: Mapping[str, Any],
    idempotency_key: str,
    expected_state_version: int,
) -> dict[str, Any]:
    reject_noncanonical(program)
    reject_noncanonical({"expected_state_version": expected_state_version})
    state_object = state_object_id(campaign_id)
    episode_id = f"human-resolution:{campaign_id}:{uuid4().hex}"

    def callback(connection, timestamp: str) -> dict[str, Any]:
        row = connection.execute(
            "SELECT * FROM pipeline_objects WHERE object_id = ? AND is_current = 1",
            (state_object,),
        ).fetchone()
        if row is None:
            raise HumanResolutionValidationError("CAMPAIGN_NOT_FOUND", campaign_id)
        current_state = __import__("json").loads(row["payload_json"])
        current_revision = int(row["revision"])
        if int(current_state["version"]) != expected_state_version:
            raise HumanResolutionStaleError(
                f"expected state version {expected_state_version}, current {current_state['version']}"
            )
        if int(program["expected_state_version"]) != expected_state_version:
            raise HumanResolutionStaleError("compiled revision expected state version does not match request")
        if int(program["expected_state_revision"]) != current_revision:
            raise HumanResolutionStaleError(
                f"expected repository revision {program['expected_state_revision']}, current {current_revision}"
            )
        current_timeline = _timeline_from_state(current_state)
        if canonical_sha256(current_timeline) != str(program["before_timeline_sha256"]):
            raise HumanResolutionStaleError("timeline changed since compile; refresh and recompile")

        after_timeline, diff = apply_native_edit(current_timeline, program)
        after_state = dict(current_state)
        after_state["video_edit_program"] = after_timeline
        after_state["version"] = int(current_state["version"]) + 1
        after_state["human_resolution_state"] = "QA_REQUIRED"
        after_state["human_resolution_refs"] = list(current_state.get("human_resolution_refs", []))
        after_state["human_resolution_refs"].append({"object_id": episode_id, "version": "1.0.0"})
        after_state_sha = canonical_sha256(after_state)
        receipt_id = f"receipt:{canonical_sha256({'episode_id': episode_id, 'after_state_sha256': after_state_sha})[:24]}"
        after_ref = {
            "object_id": state_object,
            "version": f"{after_state['version']}.0.0",
            "sha256": after_state_sha,
        }
        episode_payload = {
            "episode_id": episode_id,
            "version": "1.0.0",
            "authority": {"authority_id": "ca-program-control-v2.1-candidate", "authority_state": "candidate_not_current"},
            "lifecycle_state": "approved",
            "epistemic_state": "observed",
            "before_state_refs": [{"object_id": state_object, "version": f"{current_state['version']}.0.0", "sha256": str(row["canonical_sha256"])}],
            "after_state_refs": [after_ref],
            "operator_request": f"{program['manipulation_type']} on {program['target_node_id']}",
            "interpreted_target": f"Native edit of timeline item {program['target_node_id']}",
            "exact_changes": [{"operation": program["manipulation_type"], "target_ref": dict(program["target_ref"]), "parameter_changes": dict(program["arguments"])}],
            "tools_invoked": [f"studio.native_edit.{program['manipulation_type'].lower()}"] ,
            "models_or_runtimes": ["cae-native-editing-surface"],
            "context_refs": [dict(program["target_ref"])],
            "invariants": ["INV-HUMAN-RESOLUTION-001", "upstream_semantic_authority_preserved", "source_lineage_preserved", "release_authority_preserved"],
            "required_transformations": ["persist canonical timeline revision", "persist immutable before/after evidence"],
            "creative_freedom": [],
            "wrong_reading_locks": ["manual edits remain bounded to the selected timeline item"],
            "result_refs": [after_ref],
            "evaluation_refs": [],
            "operator_verdict": "approved",
            "applicability_scope": {"campaign_id": campaign_id, "target_node_id": program["target_node_id"], "manipulation_type": program["manipulation_type"]},
            "programming_material_dispositions": ["archive_for_manual_curation"],
            "promotion_status": "captured_not_promoted",
            "revision_receipt": {
                "receipt_id": receipt_id,
                "actor_id": program["operator_actor"]["actor_id"],
                "operation": program["manipulation_type"],
                "version_before": current_state["version"],
                "version_after": after_state["version"],
                "repository_revision_before": current_revision,
                "repository_revision_after": current_revision + 1,
                "source_state_sha256": str(row["canonical_sha256"]),
                "output_state_sha256": after_state_sha,
                "validator_results": {"cas": "PASS", "bounds": "PASS", "before_after_diff": "PASS", "release_bypass": "PASS"},
                "timestamp": timestamp,
            },
            "before_after_diff": diff,
        }
        episode_sha = canonical_sha256(episode_payload)
        episode_payload["revision_receipt"]["episode_sha256"] = episode_sha

        _store_object_row(
            connection,
            object_id=state_object,
            object_type=CAMPAIGN_STATE_TYPE,
            payload=after_state,
            idempotency_key=f"{idempotency_key}:state",
            timestamp=timestamp,
            expected_revision=current_revision,
        )
        _store_object_row(
            connection,
            object_id=episode_id,
            object_type="human_resolution_episode",
            payload=episode_payload,
            idempotency_key=f"{idempotency_key}:episode",
            timestamp=timestamp,
            expected_revision=0,
        )
        return {
            "campaign": after_state,
            "episode": episode_payload,
            "receipt": episode_payload["revision_receipt"],
            "before_state_sha256": str(row["canonical_sha256"]),
            "after_state_sha256": after_state_sha,
        }

    try:
        return pipeline.repository.execute_idempotent(
            command_type="human_resolution_native_edit",
            idempotency_key=idempotency_key,
            payload={"campaign_id": campaign_id, "program_id": program["program_id"], "expected_state_version": expected_state_version},
            callback=callback,
        )
    except PipelineConflict as exc:
        raise HumanResolutionStaleError(str(exc)) from exc
