"""M0089 acceptance tests for immutable operator visual feedback + evaluation projection."""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import pytest
from jsonschema import validate as jsonschema_validate

REPO_ROOT = Path(__file__).resolve().parents[2]
CA_RUNTIME_SRC = REPO_ROOT / "packages" / "ca_runtime" / "src"
PIPELINE_SRC = REPO_ROOT / "services" / "pipeline" / "src"
CA_CONTRACTS_SRC = REPO_ROOT / "packages" / "ca_contracts" / "src"

# The supplied archive omits optional PostgreSQL dependencies and the legacy
# Builder package. These namespace shims keep this unit/integration test on the
# real SQLite PipelineRepository path without mocking the feedback implementation.
if "ca_runtime" not in sys.modules:
    pkg = types.ModuleType("ca_runtime")
    pkg.__path__ = [str(CA_RUNTIME_SRC)]
    sys.modules["ca_runtime"] = pkg
if "ca_runtime.paths" not in sys.modules:
    paths_mod = types.ModuleType("ca_runtime.paths")
    def _default_database_path(product_id: str):
        return Path(".conscious-activations") / "dev" / product_id.replace("/", "-").replace("\\", "-") / "product.sqlite3"
    paths_mod.default_database_path = _default_database_path
    sys.modules["ca_runtime.paths"] = paths_mod
if "ca_runtime.migrations" not in sys.modules:
    import importlib.util
    migrations_init = CA_RUNTIME_SRC / "ca_runtime" / "migrations" / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        "ca_runtime.migrations", migrations_init, submodule_search_locations=[str(migrations_init.parent)]
    )
    pkg = types.ModuleType("ca_runtime.migrations")
    pkg.__path__ = [str(migrations_init.parent)]
    pkg.__spec__ = spec
    sys.modules["ca_runtime.migrations"] = pkg
if "cmf_pipeline.migrations" not in sys.modules:
    import importlib.util
    migrations_init = PIPELINE_SRC / "cmf_pipeline" / "migrations" / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        "cmf_pipeline.migrations", migrations_init, submodule_search_locations=[str(migrations_init.parent)]
    )
    pkg = types.ModuleType("cmf_pipeline.migrations")
    pkg.__path__ = [str(migrations_init.parent)]
    pkg.__spec__ = spec
    sys.modules["cmf_pipeline.migrations"] = pkg
if "cmf_pipeline" not in sys.modules:
    pkg = types.ModuleType("cmf_pipeline")
    pkg.__path__ = [str(PIPELINE_SRC)]
    pkg.PRODUCT_ID = "atomic-harness-pipeline"
    pkg.PRODUCT_VERSION = "0.9.0-dev.1"
    sys.modules["cmf_pipeline"] = pkg

# Pytest/plugin discovery may have preloaded a non-package cmf_pipeline module.
# Bind only the subpackages needed by this acceptance test so imports do not
# execute unrelated application aggregators.
if "cmf_pipeline.evaluation" not in sys.modules:
    pkg = types.ModuleType("cmf_pipeline.evaluation")
    pkg.__path__ = [str(PIPELINE_SRC / "cmf_pipeline" / "evaluation")]
    sys.modules["cmf_pipeline.evaluation"] = pkg
if "cmf_pipeline.workflow" not in sys.modules:
    pkg = types.ModuleType("cmf_pipeline.workflow")
    pkg.__path__ = [str(PIPELINE_SRC / "cmf_pipeline" / "workflow")]
    sys.modules["cmf_pipeline.workflow"] = pkg
if "cmf_pipeline.workflow.infrastructure" not in sys.modules:
    pkg = types.ModuleType("cmf_pipeline.workflow.infrastructure")
    pkg.__path__ = [str(PIPELINE_SRC / "cmf_pipeline" / "workflow" / "infrastructure")]
    sys.modules["cmf_pipeline.workflow.infrastructure"] = pkg
if "cmf_pipeline.domain" not in sys.modules:
    pkg = types.ModuleType("cmf_pipeline.domain")
    pkg.__path__ = [str(PIPELINE_SRC / "cmf_pipeline" / "domain")]
    sys.modules["cmf_pipeline.domain"] = pkg
if str(CA_CONTRACTS_SRC) not in sys.path:
    sys.path.insert(0, str(CA_CONTRACTS_SRC))

from cmf_pipeline.evaluation.visual_feedback import (  # noqa: E402
    CONTRASTIVE_EXAMPLES,
    VisualFeedbackRecord,
    VisualFeedbackService,
    build_visual_feedback_evaluation_dataset,
)
from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository  # noqa: E402


class SQLitePipelineRepository(PipelineRepository):
    """Use the real repository storage code with local migration files in the archive."""

    def initialize(self, *, now: str | None = None):
        import sqlite3

        timestamp = now or "2026-09-10T22:00:00Z"
        foundation = (CA_RUNTIME_SRC / "ca_runtime" / "migrations" / "0001_foundation.sql").read_text(encoding="utf-8")
        pipeline = (PIPELINE_SRC / "cmf_pipeline" / "migrations" / "0001_pipeline_core.sql").read_text(encoding="utf-8")
        with sqlite3.connect(self.path) as connection:
            connection.executescript(foundation)
            connection.execute(
                "INSERT INTO schema_migrations(version, name, applied_at_utc) VALUES(1, '0001_foundation', ?) ON CONFLICT(version) DO NOTHING",
                (timestamp,),
            )
            connection.execute(
                """INSERT INTO product_metadata(
                    product_id, product_version, authority_state,
                    development_authorized, production_authorized, certified,
                    initialized_at_utc
                ) VALUES(?, '0.9.0-dev.1', 'candidate_not_current', 1, 0, 0, ?)
                ON CONFLICT(product_id) DO UPDATE SET
                    product_version=excluded.product_version,
                    authority_state='candidate_not_current',
                    development_authorized=1, production_authorized=0, certified=0""",
                ("atomic-harness-pipeline", timestamp),
            )
            connection.executescript(pipeline)
            connection.execute(
                "INSERT INTO pipeline_migrations(version, name, applied_at_utc) VALUES(1, '0001_pipeline_core', ?) ON CONFLICT(version) DO NOTHING",
                (timestamp,),
            )
        return self.health()


ACTOR = {
    "actor_id": "operator-m0089",
    "actor_type": "human",
    "product_id": "conscious-activations",
    "workflow_role": "operator",
}


def ref(name: str, seed: str) -> dict[str, str]:
    from ca_contracts import canonical_sha256

    return {"object_id": name, "version": "1.0.0", "sha256": canonical_sha256({"seed": seed})}


def build_record(*, decision: str = "GOOD", created_at: str = "2026-09-10T22:00:00Z") -> VisualFeedbackRecord:
    return VisualFeedbackRecord.build(
        workspace_id="ws-m0089",
        session_id="session-m0089",
        campaign_ref=ref("campaign:m0089", "campaign"),
        storyboard_revision_ref=ref("storyboard-revision:m0089:r1", "revision-r1"),
        harness_ref=ref("harness:supervisual", "harness"),
        design_system_ref=ref("design-system:cae-v1", "design-system"),
        element_revision_ref=ref("element:m0089:1", "element-revision"),
        affected_scene_ref=ref("scene:m0089:1", "scene"),
        affected_element_ref=ref("element:m0089", "element"),
        asset_source_ref=ref("asset:source-1", "asset"),
        decision=decision,  # type: ignore[arg-type]
        reason={"code": "WRONG_READING", "detail": "Source remains semantically wrong despite polished composition."}
        if decision != "GOOD"
        else None,
        note="Operator judged the visual against source evidence.",
        region={
            "coordinate_space": "NORMALIZED_BPS",
            "x_bps": 1200,
            "y_bps": 800,
            "width_bps": 4200,
            "height_bps": 3600,
        },
        operator_actor=ACTOR,
        created_at=created_at,
    )


def test_persists_distinct_feedback_records_immutably_and_replays_deterministically(tmp_path: Path) -> None:
    repository = SQLitePipelineRepository(tmp_path / "pipeline.sqlite3")
    service = VisualFeedbackService(repository)

    good = build_record(decision="GOOD")
    first = service.record(good)
    replay = service.record(good)
    needs_edit = build_record(decision="NEEDS_EDIT", created_at="2026-09-10T22:01:00Z")
    second = service.record(needs_edit)

    assert first["object"]["object_id"] == good.feedback_id
    assert replay["object"]["object_id"] == good.feedback_id
    assert replay["idempotent_replay"] is True
    assert second["object"]["object_id"] == needs_edit.feedback_id
    assert second["object"]["object_id"] != first["object"]["object_id"]

    objects = repository.list_objects(object_type="studio_visual_feedback")
    assert len(objects) == 2
    assert {item["payload"]["decision"] for item in objects} == {"GOOD", "NEEDS_EDIT"}


def test_structured_reason_region_and_revision_lineage_project_to_evaluation_without_mutating_rules(tmp_path: Path) -> None:
    repository = SQLitePipelineRepository(tmp_path / "pipeline.sqlite3")
    service = VisualFeedbackService(repository)
    service.record(build_record(decision="NEEDS_EDIT"))

    dataset = service.project_evaluation_dataset()
    assert dataset["dataset_id"] == "visual-operator-feedback"
    assert dataset["record_count"] == 1
    assert dataset["production_rules_mutated"] is False
    record = dataset["records"][0]
    assert record["decision"] == "NEEDS_EDIT"
    assert record["evaluation_rank_score_bps"] == 5000
    assert record["reason"]["code"] == "WRONG_READING"
    assert record["region"]["coordinate_space"] == "NORMALIZED_BPS"
    assert record["storyboard_revision_ref"]["object_id"] == "storyboard-revision:m0089:r1"
    assert record["affected_scene_ref"]["object_id"] == "scene:m0089:1"
    assert record["affected_element_ref"]["object_id"] == "element:m0089"

    assert len(repository.list_objects(object_type="studio_visual_feedback")) == 1


def test_contrastive_example_is_good_looking_but_wrong_and_remains_evaluation_only() -> None:
    assert CONTRASTIVE_EXAMPLES
    wrong = CONTRASTIVE_EXAMPLES[0]
    assert wrong["decision"] == "REJECT"
    assert wrong["reason"]["code"] == "WRONG_READING"
    assert "source lineage" in wrong["why_good_looking_is_wrong"]
    assert wrong["invariant_violated"] == "source_truth_and_wrong_reading_locks"


def test_malformed_region_and_non_operator_fail_closed() -> None:
    with pytest.raises(Exception, match=r"x_bps \+ width_bps"):
        VisualFeedbackRecord.build(
            workspace_id="ws-m0089",
            session_id="session-m0089",
            campaign_ref=ref("campaign:m0089", "campaign"),
            storyboard_revision_ref=ref("storyboard-revision:m0089:r1", "revision-r1"),
            harness_ref=ref("harness:supervisual", "harness"),
            design_system_ref=ref("design-system:cae-v1", "design-system"),
            decision="GOOD",
            region={"coordinate_space": "NORMALIZED_BPS", "x_bps": 9000, "y_bps": 0, "width_bps": 2000, "height_bps": 1000},
            operator_actor=ACTOR,
        )

    bad_actor = dict(ACTOR, actor_type="model_program")
    with pytest.raises(Exception, match="human operator actor"):
        VisualFeedbackRecord.build(
            workspace_id="ws-m0089",
            session_id="session-m0089",
            campaign_ref=ref("campaign:m0089", "campaign"),
            storyboard_revision_ref=ref("storyboard-revision:m0089:r1", "revision-r1"),
            harness_ref=ref("harness:supervisual", "harness"),
            design_system_ref=ref("design-system:cae-v1", "design-system"),
            decision="GOOD",
            operator_actor=bad_actor,
        )


def test_contrastive_reference_artifact_matches_runtime_constants() -> None:
    reference_path = REPO_ROOT / "services" / "pipeline" / "evaluation" / "M0089_CONTRASTIVE_EXAMPLES.json"
    on_disk = json.loads(reference_path.read_text(encoding="utf-8"))
    assert on_disk == list(CONTRASTIVE_EXAMPLES)


def test_dataset_projection_is_deterministic_for_same_feedback_objects() -> None:
    objects = [
        {
            "object_id": "visual-feedback:1",
            "semantic_version": "1.0.0",
            "canonical_sha256": "a" * 64,
            "payload": {
                "decision": "GOOD",
                "revision_ref": ref("revision:1", "revision"),
                "created_at": "2026-09-10T22:00:00Z",
            },
        }
    ]
    first = build_visual_feedback_evaluation_dataset(objects)
    second = build_visual_feedback_evaluation_dataset(objects)
    assert first == second
    assert first["dataset_sha256"]



def test_emitted_contracts_validate_and_identity_tampering_fails(tmp_path: Path) -> None:
    record = build_record(decision="REJECT")
    feedback_schema = json.loads(
        (
            REPO_ROOT
            / "services"
            / "pipeline"
            / "contracts"
            / "schemas"
            / "visual_operator_feedback.schema.json"
        ).read_text(encoding="utf-8")
    )
    evaluation_schema = json.loads(
        (
            REPO_ROOT
            / "services"
            / "pipeline"
            / "contracts"
            / "schemas"
            / "visual_feedback_evaluation_dataset.schema.json"
        ).read_text(encoding="utf-8")
    )

    jsonschema_validate(record.model_dump(mode="json"), feedback_schema)
    with pytest.raises(Exception, match="feedback_sha256 does not match"):
        VisualFeedbackRecord.model_validate(
            {**record.model_dump(mode="json"), "feedback_sha256": "0" * 64}
        )

    repository = SQLitePipelineRepository(tmp_path / "pipeline.sqlite3")
    service = VisualFeedbackService(repository)
    service.record(record)
    dataset = service.project_evaluation_dataset()
    jsonschema_validate(dataset, evaluation_schema)


def test_legacy_feedback_payload_projects_without_rewriting_or_dropping_lineage() -> None:
    legacy = {
        "object_id": "visual-feedback:legacy-1",
        "semantic_version": "1.0.0",
        "canonical_sha256": "b" * 64,
        "payload": {
            "decision": "REJECT",
            "revision_ref": ref("revision:legacy", "revision-legacy"),
            "target_ref": ref("asset:legacy", "asset-legacy"),
            "reason": "WRONG_READING",
            "reason_category": "WRONG_READING",
            "note": "Legacy operator payload should remain evaluable.",
            "created_at": "2026-09-10T22:02:00Z",
        },
    }
    dataset = build_visual_feedback_evaluation_dataset([legacy])
    projected = dataset["records"][0]
    assert projected["decision"] == "REJECT"
    assert projected["evaluation_label"] == "NEGATIVE"
    assert projected["storyboard_revision_ref"] == legacy["payload"]["revision_ref"]
    assert projected["asset_source_ref"] == legacy["payload"]["target_ref"]
    assert projected["reason_code"] == "WRONG_READING"
    assert projected["production_rule_effect"] == "NONE"
