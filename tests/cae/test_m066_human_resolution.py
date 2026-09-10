"""CAE-M0066 unit/integration-style tests for native editing and immutable resolution evidence."""
from __future__ import annotations

import json
import sqlite3
import sys
import types
from pathlib import Path

import pytest

# The uploaded brownfield bundle omits the separate Studio source package and
# the sandbox lacks its optional runtime dependencies. Stub only the imports
# needed by the M0066 service so these tests remain self-contained.
errors_mod = types.ModuleType("cmf_pipeline.domain.errors")
class PipelineConflict(RuntimeError):
    pass
errors_mod.PipelineConflict = PipelineConflict
validation_mod = types.ModuleType("cmf_pipeline.domain.validation")
def reject_noncanonical(value):
    json.dumps(value, allow_nan=False)
validation_mod.reject_noncanonical = reject_noncanonical
campaign_projection_mod = types.ModuleType("api.services.campaign_projection")
campaign_projection_mod.CAMPAIGN_STATE_TYPE = "studio_campaign_state"
campaign_projection_mod.state_object_id = lambda campaign_id: f"studio-campaign-state:{campaign_id}"
cmf_pipeline_mod = types.ModuleType("cmf_pipeline")
cmf_pipeline_domain = types.ModuleType("cmf_pipeline.domain")
cmf_pipeline_workflow = types.ModuleType("cmf_pipeline.workflow")
cmf_pipeline_workflow_infra = types.ModuleType("cmf_pipeline.workflow.infrastructure")
sys.modules.setdefault("cmf_pipeline", cmf_pipeline_mod)
sys.modules.setdefault("cmf_pipeline.domain", cmf_pipeline_domain)
sys.modules["cmf_pipeline.domain.errors"] = errors_mod
sys.modules["cmf_pipeline.domain.validation"] = validation_mod
sys.modules.setdefault("cmf_pipeline.workflow", cmf_pipeline_workflow)
sys.modules.setdefault("cmf_pipeline.workflow.infrastructure", cmf_pipeline_workflow_infra)
sys.modules["api.services.campaign_projection"] = campaign_projection_mod

from ca_contracts import canonical_sha256
from api.services.human_resolution import (
    _canonical_timeline,
    HumanResolutionStaleError,
    HumanResolutionValidationError,
    apply_native_edit,
    commit_native_edit,
    compile_native_edit_program,
)


ACTOR = {
    "actor_id": "operator:test",
    "actor_type": "human",
    "product_id": "conscious-activations-studio",
    "workflow_role": "operator",
}


def timeline() -> dict:
    return {
        "width": 1920,
        "height": 1080,
        "fps_numerator": 30,
        "fps_denominator": 1,
        "duration_frames": 900,
        "tracks": [{
            "track_id": "track:primary",
            "track_type": "VIDEO",
            "role": "PRIMARY",
            "z_index": 0,
            "items": [{
                "item_id": "clip:001",
                "track_id": "track:primary",
                "kind": "VIDEO_CLIP",
                "role": "PRIMARY",
                "start_frame": 0,
                "end_frame": 300,
                "source_start_ms": 0,
                "source_end_ms": 10000,
                "source_ref": {"object_id": "asset:old", "version": "1.0.0", "sha256": "a" * 64},
                "editable_operations": ["ADJUST_TIMING", "SUBSTITUTE_ASSET"],
            }],
        }],
        "items": [],
    }


def state() -> dict:
    return {
        "campaign_id": "m066",
        "lifecycle_state": "RUNNING",
        "autonomy_mode": "AUTOPILOT",
        "version": 1,
        "video_edit_program": timeline(),
        "human_resolution_refs": [],
    }


def test_compile_timing_program_captures_cas_and_before_digest() -> None:
    current = state()
    program = compile_native_edit_program(
        campaign_id="m066",
        state=current,
        state_revision=7,
        target_ref=current["video_edit_program"]["tracks"][0]["items"][0]["source_ref"],
        target_node_id="clip:001",
        manipulation_type="ADJUST_TIMING",
        arguments={"delta_frames": 30, "source_start_delta_ms": 0, "source_end_delta_ms": 1000},
        operator_actor=ACTOR,
    )
    assert program.expected_state_version == 1
    assert program.expected_state_revision == 7
    assert program.before_timeline_sha256 == canonical_sha256(_canonical_timeline(current["video_edit_program"]))
    assert len(program.program_sha256) == 64


def test_timing_bound_is_enforced() -> None:
    with pytest.raises(HumanResolutionValidationError, match="delta_frames must be"):
        compile_native_edit_program(
            campaign_id="m066", state=state(), state_revision=1,
            target_ref=state()["video_edit_program"]["tracks"][0]["items"][0]["source_ref"],
            target_node_id="clip:001", manipulation_type="ADJUST_TIMING",
            arguments={"delta_frames": 301}, operator_actor=ACTOR,
        )


def test_non_editable_item_is_rejected() -> None:
    current = state()
    current["video_edit_program"]["tracks"][0]["items"][0]["editable_operations"] = []
    with pytest.raises(HumanResolutionValidationError, match="does not permit"):
        compile_native_edit_program(
            campaign_id="m066", state=current, state_revision=1,
            target_ref=current["video_edit_program"]["tracks"][0]["items"][0]["source_ref"],
            target_node_id="clip:001", manipulation_type="SUBSTITUTE_ASSET",
            arguments={"source_ref": {"object_id": "asset:new", "version": "1.0.0", "sha256": "b" * 64}},
            operator_actor=ACTOR,
        )


def test_asset_substitution_changes_canonical_target_and_emits_diff() -> None:
    before = timeline()
    after, diff = apply_native_edit(before, {
        "target_node_id": "clip:001",
        "manipulation_type": "SUBSTITUTE_ASSET",
        "arguments": {"source_ref": {"object_id": "asset:new", "version": "2.0.0", "sha256": "b" * 64}},
    })
    assert after["tracks"][0]["items"][0]["source_ref"]["object_id"] == "asset:new"
    assert diff[0]["before_sha256"] != diff[0]["after_sha256"]
    assert diff[0]["changes"][0]["before"]["object_id"] == "asset:old"


def test_atomic_commit_persists_state_and_immutable_episode(tmp_path: Path) -> None:
    class FakeRepo:
        def __init__(self, db: Path):
            self.db = db
            self.replays = {}
        def execute_idempotent(self, *, command_type, idempotency_key, payload, callback):
            if idempotency_key in self.replays:
                return self.replays[idempotency_key]
            con = sqlite3.connect(self.db, isolation_level=None)
            con.row_factory = sqlite3.Row
            con.execute("BEGIN IMMEDIATE")
            try:
                result = callback(con, "2026-09-09T21:00:00Z")
                con.execute("INSERT INTO pipeline_command_results VALUES (?, ?)", (idempotency_key, json.dumps(result)))
                con.execute("COMMIT")
            except Exception:
                con.execute("ROLLBACK")
                con.close()
                raise
            con.close()
            self.replays[idempotency_key] = result
            return result

    db = tmp_path / "m066_human_resolution.sqlite3"
    con = sqlite3.connect(db)
    con.executescript("""
        CREATE TABLE pipeline_command_results(idempotency_key TEXT PRIMARY KEY, result_json TEXT NOT NULL);
        CREATE TABLE pipeline_objects(
          object_id TEXT NOT NULL, revision INTEGER NOT NULL, object_type TEXT NOT NULL,
          semantic_version TEXT NOT NULL, canonical_sha256 TEXT NOT NULL, payload_json TEXT NOT NULL,
          lifecycle_state TEXT NOT NULL, authority_state TEXT NOT NULL, is_current INTEGER NOT NULL,
          idempotency_key TEXT NOT NULL, created_at_utc TEXT NOT NULL, supersedes_revision INTEGER
        );
    """)
    campaign_id = "m066"
    state_payload = state()
    con.execute("INSERT INTO pipeline_objects VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
        f"studio-campaign-state:{campaign_id}", 0, "studio_campaign_state", "1.0.0",
        canonical_sha256(state_payload), json.dumps(state_payload, separators=(",", ":")),
        "ACTIVE", "candidate_not_current", 1, "seed", "2026-09-09T20:00:00Z", None,
    ))
    con.commit(); con.close()

    repo = FakeRepo(db)
    program = compile_native_edit_program(
        campaign_id=campaign_id, state=state_payload, state_revision=0,
        target_ref=state_payload["video_edit_program"]["tracks"][0]["items"][0]["source_ref"],
        target_node_id="clip:001", manipulation_type="ADJUST_TIMING",
        arguments={"delta_frames": 30, "source_start_delta_ms": 0, "source_end_delta_ms": 500}, operator_actor=ACTOR,
    ).as_dict()
    result = commit_native_edit(pipeline=types.SimpleNamespace(repository=repo), campaign_id=campaign_id,
        program=program, idempotency_key="execute:m066:1", expected_state_version=1)

    assert result["campaign"]["version"] == 2
    assert result["episode"]["before_after_diff"][0]["before_sha256"] != result["episode"]["before_after_diff"][0]["after_sha256"]
    assert result["receipt"]["validator_results"]["cas"] == "PASS"
    assert result["episode"]["promotion_status"] == "captured_not_promoted"

    con = sqlite3.connect(db); con.row_factory = sqlite3.Row
    state_rows = con.execute("SELECT revision, is_current, payload_json FROM pipeline_objects WHERE object_id=? ORDER BY revision", (f"studio-campaign-state:{campaign_id}",)).fetchall()
    episode_rows = con.execute("SELECT object_id, object_type, is_current FROM pipeline_objects WHERE object_type='human_resolution_episode'").fetchall()
    con.close()
    assert [row["revision"] for row in state_rows] == [0, 1]
    assert state_rows[-1]["is_current"] == 1
    persisted_state = json.loads(state_rows[-1]["payload_json"])
    persisted_item = persisted_state["video_edit_program"]["tracks"][0]["items"][0]
    assert persisted_item["end_frame"] == 330
    assert persisted_item["source_end_ms"] == 10500
    assert persisted_state["human_resolution_refs"] == [{"object_id": result["episode"]["episode_id"], "version": "1.0.0"}]
    assert persisted_state["human_resolution_state"] == "QA_REQUIRED"
    assert len(episode_rows) == 1
    assert episode_rows[0]["object_type"] == "human_resolution_episode"

    replay = commit_native_edit(
        pipeline=types.SimpleNamespace(repository=repo),
        campaign_id=campaign_id,
        program=program,
        idempotency_key="execute:m066:1",
        expected_state_version=1,
    )
    assert replay == result
    con = sqlite3.connect(db)
    assert con.execute("SELECT COUNT(*) FROM pipeline_objects WHERE object_type='human_resolution_episode'").fetchone()[0] == 1
    con.close()


def test_stale_concurrent_revision_is_rejected_without_new_episode(tmp_path: Path) -> None:
    class FakeRepo:
        def execute_idempotent(self, **kwargs):
            class Conn:
                def execute(self, *args):
                    return type("R", (), {"fetchone": lambda self: None})()
            return kwargs["callback"](Conn(), "2026-09-09T21:00:00Z")

    # Exercise the precondition directly: the commit transaction observes a
    # current state version different from the compiled one and aborts before
    # any evidence object can be inserted.
    with pytest.raises(Exception):
        commit_native_edit(
            pipeline=types.SimpleNamespace(repository=FakeRepo()), campaign_id="m066",
            program={"program_id": "revision:stale", "expected_state_version": 1, "expected_state_revision": 0,
                     "target_node_id": "clip:001", "manipulation_type": "ADJUST_TIMING",
                     "arguments": {"delta_frames": 1}, "target_ref": {"object_id": "x", "version": "1", "sha256": "a" * 64},
                     "before_timeline_sha256": canonical_sha256(timeline()), "operator_actor": ACTOR},
            idempotency_key="execute:stale", expected_state_version=1,
        )
