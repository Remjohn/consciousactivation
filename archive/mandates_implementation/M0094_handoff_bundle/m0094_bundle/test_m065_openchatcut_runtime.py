from __future__ import annotations

import hashlib
import json
import sys
import types
from fractions import Fraction
from pathlib import Path

# Keep this mandate-focused integration test runnable in the minimal sandbox even when
# the repository's optional PostgreSQL runtime dependency is not installed.
_cmf_package = types.ModuleType("cmf_pipeline")
_cmf_package.__path__ = [str(Path(__file__).resolve().parents[2] / "services/pipeline/src/cmf_pipeline")]
_cmf_package.PRODUCT_ID = "atomic-harness-pipeline"
_cmf_package.PRODUCT_VERSION = "0.9.0-dev.1"
_cmf_package.PACKAGE_VERSION = "0.9.0.dev1"
sys.modules.setdefault("cmf_pipeline", _cmf_package)
_carm_package = types.ModuleType("ca_runtime")
_carm_package.__path__ = [str(Path(__file__).resolve().parents[2] / "packages/ca_runtime/src/ca_runtime")]
sys.modules.setdefault("ca_runtime", _carm_package)

import pytest
from ca_contracts import canonical_sha256

import cmf_pipeline.media.openchatcut as openchatcut
from cmf_pipeline.media.openchatcut import (
    OPENCHATCUT_STATE_EXECUTED,
    OPENCHATCUT_STATE_BLOCKED,
    OpenChatCutRuntimeAdapter,
    OpenChatCutRuntimeConfig,
    OpenChatCutTimelineVerificationError,
    _McpStreamableHttpClient,
    _frame_count_from_ms,
)
from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository


SOURCE_REF = {"object_id": "source-registration:unit", "version": "1.0.0", "sha256": "a" * 64}


def _program_payload(source_sha256: str = "4" * 64) -> dict:
    return {
        "program_id": "video-edit-program:test",
        "program_version": "1.0.0",
        "derivative_job_ref": {"object_id": "job:test", "version": "1.0.0", "sha256": "b" * 64},
        "source_registration_ref": SOURCE_REF,
        "semantic_production_package_ref": {"object_id": "package:test", "version": "1.0.0", "sha256": "c" * 64},
        "final_script_ref": {"object_id": "script:test", "version": "1.0.0", "sha256": "d" * 64},
        "activation_transfer_contract_ref": {"object_id": "transfer:test", "version": "1.0.0", "sha256": "e" * 64},
        "harness_binding_ref": {"object_id": "binding:test", "version": "1.0.0", "sha256": "f" * 64},
        "evaluation_profile_ref": {"object_id": "evaluation:test", "version": "1.0.0", "sha256": "1" * 64},
        "source_media_ref": {"object_id": "source-media:" + "2" * 64, "version": "1.0.0", "sha256": "3" * 64},
        "source_media_sha256": source_sha256,
        "source_authority": "SOVEREIGN_SOURCE_MEDIA_BYTES",
        "source_integrity": {"status": "VERIFIED"},
        "canvas": {"width": 1080, "height": 1920, "fps_numerator": 30, "fps_denominator": 1, "duration_ms": 2000},
        "timebase": {"numerator": 30, "denominator": 1},
        "tracks": [
            {
                "track_id": "video-main",
                "track_type": "VIDEO",
                "role": "PRIMARY_A_ROLL_SPINE",
                "z_index": 0,
                "elements": [
                    {
                        "element_id": "clip-1",
                        "kind": "SOURCE_SEGMENT",
                        "output_start_ms": 0,
                        "output_end_ms": 1000,
                        "semantic_role": "hook",
                        "sequence_role": "open",
                        "source_registration_ref": SOURCE_REF,
                        "source_start_ms": 1000,
                        "source_end_ms": 2000,
                        "artifact_ref": "NOT_APPLICABLE",
                        "generated_slot_state": "UNMATERIALIZED",
                        "bbox_intent_ref": "NOT_APPLICABLE",
                        "text": "NOT_APPLICABLE",
                    }
                ],
            },
            {
                "track_id": "audio-main",
                "track_type": "AUDIO",
                "role": "BED",
                "z_index": 1,
                "elements": [
                    {
                        "element_id": "audio-1",
                        "kind": "AUDIO",
                        "output_start_ms": 0,
                        "output_end_ms": 1000,
                        "semantic_role": "underscore",
                        "sequence_role": "bed",
                        "source_registration_ref": "NOT_APPLICABLE",
                        "source_start_ms": "NOT_APPLICABLE",
                        "source_end_ms": "NOT_APPLICABLE",
                        "artifact_ref": {"object_id": "audio-artifact:test", "version": "1.0.0", "sha256": "5" * 64},
                        "generated_slot_state": "MATERIALIZED",
                        "bbox_intent_ref": "NOT_APPLICABLE",
                        "text": "NOT_APPLICABLE",
                    }
                ],
            },
        ],
        "wrong_reading_locks": ["Do not remove source spine."],
        "timeline_authority": "CANONICAL_VIDEO_EDIT_PROGRAM",
        "source_a_roll_required": True,
        "production_authorized": False,
    }


class _FakeMcp:
    def __init__(self):
        self.server_info = {"name": "openchatcut", "version": "test-native"}
        self.session_id = "mcp-test-session"
        self.tools = [
            {"name": name}
            for name in (
                "create_project", "target_project", "begin_edit_session", "review_edit_session",
                "read_timeline", "edit_track", "edit_item", "import_asset", "discard_edit_session",
            )
        ]
        self.project_id = "project:test"
        self.edit_session_id = "edit:test"
        self.tracks = []
        self.items = []
        self.assets = {}
        self.applied = False
        self.discarded = False

    def initialize(self):
        return {"protocolVersion": "2025-06-18", "serverInfo": self.server_info}

    def list_tools(self):
        return self.tools

    def call_tool(self, name, arguments=None):
        args = dict(arguments or {})
        if name == "create_project":
            return {"id": self.project_id}
        if name == "target_project":
            return {"ok": True, "projectId": args["projectId"]}
        if name == "openchatcut_status":
            return {"bindingMode": "browser", "projectId": self.project_id}
        if name == "begin_edit_session":
            return {"editSessionId": self.edit_session_id, "status": "draft"}
        if name == "read_timeline":
            return {
                "fps": 30,
                "tracks": list(self.tracks),
                "items": list(self.items),
            }
        if name == "edit_track":
            data = json.loads(args["json"])
            idx = len(self.tracks)
            track = {"id": f"track-{idx}", "alias": f"V{idx + 1}" if data["trackType"] == "video" else f"A{idx + 1}", **data}
            self.tracks.append(track)
            return {"created": [track]}
        if name == "import_asset":
            path = str(args["path"])
            asset_id = f"asset:{len(self.assets) + 1}"
            self.assets[path] = asset_id
            return {"asset": {"id": asset_id}}
        if name == "edit_item":
            for add in args["adds"]:
                asset_id = add.get("assetId")
                item = {
                    "id": f"item:{len(self.items) + 1}",
                    "track": add["track"],
                    "startFrame": add["fromFrame"],
                    "durationInFrames": add["durationInFrames"],
                    "srcInFrame": add.get("sourceStartFrame", 0),
                    "sourceAssetId": add.get("assetId"),
                }
                self.items.append(item)
            return {"ok": True, "count": len(self.items)}
        if name == "review_edit_session":
            self.applied = True
            return {"status": "applied"}
        if name == "discard_edit_session":
            self.discarded = True
            return {"status": "discarded"}
        raise AssertionError(f"unexpected tool {name}")


@pytest.fixture
def repository(tmp_path: Path):
    return PipelineRepository(tmp_path / "pipeline.sqlite3")


def _store_program(repository: PipelineRepository, source_sha256: str = "4" * 64) -> str:
    payload = _program_payload(source_sha256)
    return repository.store_object(
        "video_edit_program",
        payload,
        idempotency_key="test:program",
        object_id=payload["program_id"],
        lifecycle_state="COMPILED",
    )["object"]["object_id"]


def test_frame_mapping_rejects_non_frame_exact_ranges():
    assert _frame_count_from_ms(0, 1000, 30, 1, field="source") == (0, 30)
    with pytest.raises(Exception, match="frame-exact"):
        _frame_count_from_ms(1, 1000, 30, 1, field="source")


def test_sse_parser_accepts_streamable_http_event():
    body = b'data: {"jsonrpc":"2.0","id":7,"result":{"ok":true}}\n\n'
    class Headers:
        def get_content_type(self):
            return "text/event-stream"
    class Response:
        headers = Headers()
    parsed = _McpStreamableHttpClient._parse_response(Response(), body)
    assert parsed["id"] == 7
    assert parsed["result"]["ok"] is True


def test_full_handoff_preserves_native_tracks_media_cuts_and_roles(repository, monkeypatch, tmp_path):
    source = tmp_path / "source.mp4"
    source.write_bytes(b"source bytes")
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"audio bytes")
    program_id = _store_program(repository, hashlib.sha256(source.read_bytes()).hexdigest())
    fake = _FakeMcp()
    monkeypatch.setattr(openchatcut, "_McpStreamableHttpClient", lambda config: fake)
    adapter = OpenChatCutRuntimeAdapter(
        repository,
        OpenChatCutRuntimeConfig(endpoint_url="http://localhost:5199/api/external-mcp/mcp"),
    )
    receipt = adapter.handoff(
        program_id,
        media_paths={
            SOURCE_REF["object_id"]: source,
            "audio-artifact:test": audio,
        },
        idempotency_key="test:handoff",
    )
    assert receipt["payload"]["state"] == OPENCHATCUT_STATE_EXECUTED
    assert receipt["payload"]["runtime_identity"]["server_name"] == "openchatcut"
    assert receipt["payload"]["verification"]["native_item_count"] == 2
    source_native_id = receipt["payload"]["verification"]["verified_elements"][0]["native_source_asset_id"]
    assert source_native_id == receipt["payload"]["asset_map"][SOURCE_REF["object_id"]]
    assert receipt["payload"]["verification"]["verified_elements"][0]["source_start_frame"] == 30
    assert receipt["payload"]["verification"]["verified_elements"][0]["semantic_role"] == "hook"
    assert receipt["payload"]["timeline_authority"] == "CANONICAL_VIDEO_EDIT_PROGRAM"
    assert receipt["payload"]["imported_media_sha256"][SOURCE_REF["object_id"]] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert fake.applied is True






def test_runtime_inspection_reads_native_state_and_discards_session(repository, monkeypatch):
    program_id = _store_program(repository)
    fake = _FakeMcp()
    fake.tracks = [
        {"id": "track-0", "alias": "V1", "trackType": "video"},
        {"id": "track-1", "alias": "A1", "trackType": "audio"},
    ]
    fake.items = [
        {"id": "item:1", "track": "track-0", "startFrame": 0, "durationInFrames": 30, "srcInFrame": 30, "sourceDurationInFrames": 30, "sourceAssetId": "asset:1"},
        {"id": "item:2", "track": "track-1", "startFrame": 0, "durationInFrames": 30, "sourceAssetId": "asset:2"},
    ]
    monkeypatch.setattr(openchatcut, "_McpStreamableHttpClient", lambda config: fake)
    adapter = OpenChatCutRuntimeAdapter(repository, OpenChatCutRuntimeConfig())
    report = adapter.inspect_runtime(
        program_id,
        project_id="project:test",
        track_map={"video-main": "track-0", "audio-main": "track-1"},
        asset_map={SOURCE_REF["object_id"]: "asset:1", "audio-artifact:test": "asset:2"},
    )
    assert report["status"] == "IN_SYNC"
    assert report["edit_session_disposition"] == "DISCARDED_AFTER_READ"
    assert fake.discarded is True


def test_runtime_inspection_requires_discard_capability(repository, monkeypatch):
    program_id = _store_program(repository)
    class NoDiscard(_FakeMcp):
        def list_tools(self):
            return [tool for tool in self.tools if tool["name"] != "discard_edit_session"]
    monkeypatch.setattr(openchatcut, "_McpStreamableHttpClient", lambda config: NoDiscard())
    adapter = OpenChatCutRuntimeAdapter(repository, OpenChatCutRuntimeConfig())
    with pytest.raises(openchatcut.OpenChatCutRuntimeError, match="discard_edit_session"):
        adapter.inspect_runtime(
            program_id, project_id="project:test",
            track_map={"video-main": "track-0", "audio-main": "track-1"},
            asset_map={SOURCE_REF["object_id"]: "asset:1", "audio-artifact:test": "asset:2"},
        )

def test_native_inspection_reports_in_sync_and_is_deterministically_replayable(repository):
    program = _program_payload()
    timeline = {
        "fps": 30,
        "tracks": [
            {"id": "track-0", "alias": "V1", "trackType": "video"},
            {"id": "track-1", "alias": "A1", "trackType": "audio"},
        ],
        "items": [
            {"id": "item:1", "track": "track-0", "startFrame": 0, "durationInFrames": 30, "srcInFrame": 30, "sourceDurationInFrames": 30, "sourceAssetId": "asset:1"},
            {"id": "item:2", "track": "track-1", "startFrame": 0, "durationInFrames": 30, "sourceAssetId": "asset:2"},
        ],
    }
    adapter = OpenChatCutRuntimeAdapter(repository)
    maps = ({"video-main": "track-0", "audio-main": "track-1"}, {SOURCE_REF["object_id"]: "asset:1", "audio-artifact:test": "asset:2"})
    first = adapter.inspect_native_timeline(timeline, program, *maps)
    second = adapter.inspect_native_timeline(timeline, program, *maps)
    assert first["status"] == "IN_SYNC"
    assert first["source_media_sha256"] == program["source_media_sha256"]
    assert first == second


def test_native_inspection_catches_good_looking_wrong_asset_even_when_timing_matches(repository):
    program = _program_payload()
    timeline = {
        "fps": 30,
        "tracks": [{"id": "track-0", "alias": "V1", "trackType": "video"}, {"id": "track-1", "alias": "A1", "trackType": "audio"}],
        "items": [
            {"id": "item:1", "track": "track-0", "startFrame": 0, "durationInFrames": 30, "srcInFrame": 30, "sourceDurationInFrames": 30, "sourceAssetId": "asset:wrong-but-plausible"},
            {"id": "item:2", "track": "track-1", "startFrame": 0, "durationInFrames": 30, "sourceAssetId": "asset:2"},
        ],
    }
    inspection = OpenChatCutRuntimeAdapter.inspect_native_timeline(
        timeline, program,
        {"video-main": "track-0", "audio-main": "track-1"},
        {SOURCE_REF["object_id"]: "asset:1", "audio-artifact:test": "asset:2"},
    )
    assert inspection["status"] == "DIVERGED"
    assert any(d["type"] == "ASSET_DIVERGENCE" for d in inspection["differences"])
    assert inspection["reconciliation_candidates"] == []


def test_native_inspection_exposes_only_operator_gated_timing_update(repository):
    program = _program_payload()
    timeline = {
        "fps": 30,
        "tracks": [{"id": "track-0", "alias": "V1", "trackType": "video"}, {"id": "track-1", "alias": "A1", "trackType": "audio"}],
        "items": [
            {"id": "item:1", "track": "track-0", "startFrame": 0, "durationInFrames": 45, "srcInFrame": 30, "sourceDurationInFrames": 30, "sourceAssetId": "asset:1"},
            {"id": "item:2", "track": "track-1", "startFrame": 0, "durationInFrames": 30, "sourceAssetId": "asset:2"},
        ],
    }
    inspection = OpenChatCutRuntimeAdapter.inspect_native_timeline(
        timeline, program,
        {"video-main": "track-0", "audio-main": "track-1"},
        {SOURCE_REF["object_id"]: "asset:1", "audio-artifact:test": "asset:2"},
    )
    request = OpenChatCutRuntimeAdapter.build_human_resolution_request(inspection)
    assert request["manipulation_type"] == "ADJUST_TIMING"
    assert request["arguments"]["delta_frames"] == 15
    assert request["operator_required"] is True
    assert request["direct_runtime_write"] is False


def test_native_inspection_rejects_topology_divergence(repository):
    program = _program_payload()
    timeline = {
        "fps": 30,
        "tracks": [{"id": "track-0", "alias": "V1", "trackType": "video"}, {"id": "track-1", "alias": "A1", "trackType": "audio"}],
        "items": [{"id": "item:1", "track": "track-0", "startFrame": 0, "durationInFrames": 30, "srcInFrame": 30, "sourceDurationInFrames": 30, "sourceAssetId": "asset:1"}],
    }
    inspection = OpenChatCutRuntimeAdapter.inspect_native_timeline(
        timeline, program,
        {"video-main": "track-0", "audio-main": "track-1"},
        {SOURCE_REF["object_id"]: "asset:1", "audio-artifact:test": "asset:2"},
    )
    assert inspection["status"] == "DIVERGED"
    assert any(d["type"] == "TOPOLOGY_DIVERGENCE" for d in inspection["differences"])
    assert all(d.get("reconciliation") != "ADJUST_TIMING_VIA_CAE_HUMAN_RESOLUTION" for d in inspection["differences"])


def test_handoff_blocks_when_runtime_is_unreachable(repository, monkeypatch):
    program_id = _store_program(repository)
    class Unavailable:
        def __init__(self, config):
            pass
        def initialize(self):
            raise openchatcut.OpenChatCutUnavailableError("unreachable")
    monkeypatch.setattr(openchatcut, "_McpStreamableHttpClient", Unavailable)
    adapter = OpenChatCutRuntimeAdapter(repository, OpenChatCutRuntimeConfig(endpoint_url="http://127.0.0.1:1/mcp"))
    receipt = adapter.handoff(
        program_id,
        media_paths={SOURCE_REF["object_id"]: "/does/not/exist"},
        idempotency_key="test:blocked",
    )
    assert receipt["payload"]["state"] == OPENCHATCUT_STATE_BLOCKED
    assert "unreachable" in receipt["payload"]["blocking_reason"]


def test_native_verifier_rejects_wrong_source_in(repository):
    program = _program_payload()
    timeline = {
        "items": [{
            "id": "item:1",
            "track": "track-0",
            "startFrame": 0,
            "durationInFrames": 30,
            "srcInFrame": 31,
            "sourceAssetId": "asset:1",
        }, {
            "id": "item:2",
            "track": "track-1",
            "startFrame": 0,
            "durationInFrames": 30,
            "sourceAssetId": "asset:2",
        }]
    }
    with pytest.raises(OpenChatCutTimelineVerificationError, match="source in"):
        OpenChatCutRuntimeAdapter._verify_native_timeline(
            timeline, program, {"video-main": "track-0", "audio-main": "track-1"},
            {SOURCE_REF["object_id"]: "asset:1", "audio-artifact:test": "asset:2"},
        )


def test_handoff_rejects_source_bytes_that_do_not_match_cae_identity(repository, monkeypatch, tmp_path):
    source = tmp_path / "source.mp4"
    source.write_bytes(b"wrong bytes")
    audio = tmp_path / "audio.wav"
    audio.write_bytes(b"audio bytes")
    program_id = _store_program(repository, "0" * 64)
    fake = _FakeMcp()
    monkeypatch.setattr(openchatcut, "_McpStreamableHttpClient", lambda config: fake)
    adapter = OpenChatCutRuntimeAdapter(repository, OpenChatCutRuntimeConfig())
    with pytest.raises(Exception, match="source bytes do not match CAE source_media_sha256"):
        adapter.handoff(
            program_id,
            media_paths={SOURCE_REF["object_id"]: source, "audio-artifact:test": audio},
            idempotency_key="test:digest-mismatch",
        )
    assert fake.assets == {}
