from __future__ import annotations

import ast
from pathlib import Path

from tests.stories.st_01_04 import build_context, evaluation_command


ROOT = Path(__file__).resolve().parents[3]


def test_observability_contains_required_public_seam_fields() -> None:
    service, repository, observations, run_id, _, _, contract = build_context()
    receipt = service.evaluate(evaluation_command(run_id, contract))
    delivered = repository.delivered_observations(receipt.command_id)
    assert {item.event_name for item in delivered} == {
        "ST-01.04:SaturationEvaluated",
        "ST-01.04:OutcomeVerified",
    }
    assert observations.observations == delivered
    for item in delivered:
        assert item.run_id == run_id
        assert item.story_id == "ST-01.04"
        assert item.artifact_identity == receipt.evaluation_id
        assert item.authority_identity == "code-1"
        assert item.version == "1.0.0"
        assert item.provenance.startswith("evidence-index_")
        assert item.outcome == "PASS"
        assert item.source_lock_id.startswith("source-lock_")


def test_new_source_modules_are_layered_standard_library_only() -> None:
    prohibited = {"requests", "sqlalchemy", "fastapi", "temporalio", "boto3", "delegation", "visual_asset_editor"}
    for relative in (
        "src/cmf_builder/domain/evidence_saturation.py",
        "src/cmf_builder/application/evidence_saturation_commands.py",
    ):
        path = ROOT / relative
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
        assert not ({item.split(".", 1)[0] for item in imports} & prohibited)
        if "/domain/" in relative:
            assert not any(item.startswith(("cmf_builder.application", "cmf_builder.adapters")) for item in imports)


def test_no_external_product_or_production_surface_is_added() -> None:
    joined = "\n".join(
        (ROOT / relative).read_text(encoding="utf-8").lower()
        for relative in (
            "src/cmf_builder/domain/evidence_saturation.py",
            "src/cmf_builder/application/evidence_saturation_commands.py",
        )
    )
    for prohibited in (
        "format02", "comfyui", "image_generation", "delegation runtime",
        "production_ready = true", "certified = true"
    ):
        assert prohibited not in joined


def test_capsule_contract_is_explicit_non_production_and_non_certified() -> None:
    text = (ROOT / "development-capsules/ST-01.04/SATURATION_CONTRACT.yaml").read_text(encoding="utf-8")
    assert "production_eligible: false" in text
    assert "certified: false" in text
    assert "human_reaction: NOT_APPLICABLE" in text
    assert "visual_syntax: NOT_APPLICABLE" in text
