from __future__ import annotations

import ast
from pathlib import Path

from tests.stories.st_01_03 import build_context, index_command


ROOT = Path(__file__).resolve().parents[3]


def test_observability_contains_required_public_seam_fields() -> None:
    service, repository, observations, run_id, _ = build_context()
    receipt = service.index(index_command(run_id))
    delivered = repository.delivered_observations(receipt.command_id)
    names = {item.event_name for item in delivered}
    assert {
        "ST-01.03:EvidenceIndexStarted",
        "ST-01.03:SpecimenInventoryCompleted",
        "ST-01.03:EvidenceIndexCommitted",
        "ST-01.03:OutcomeVerified",
    } <= names
    assert observations.observations == delivered
    for item in delivered:
        assert item.run_id == run_id
        assert item.story_id == "ST-01.03"
        assert item.artifact_identity == receipt.index_id
        assert item.authority_identity == "code-1"
        assert item.version == "1.0.0"
        assert item.provenance.startswith("source-lock_")
        assert item.outcome == "PASS"


def test_new_source_modules_are_layered_standard_library_only() -> None:
    prohibited = {"requests", "sqlalchemy", "fastapi", "temporalio", "boto3", "delegation", "visual_asset_editor"}
    for relative in (
        "src/cmf_builder/domain/evidence_index.py",
        "src/cmf_builder/domain/evidence_saturation.py",
        "src/cmf_builder/application/evidence_index_commands.py",
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
            "src/cmf_builder/domain/evidence_index.py",
            "src/cmf_builder/domain/evidence_saturation.py",
            "src/cmf_builder/application/evidence_index_commands.py",
            "src/cmf_builder/application/evidence_saturation_commands.py",
        )
    )
    for prohibited in ("format02", "comfyui", "gpu", "image_generation", "delegation runtime", "production_ready = true"):
        assert prohibited not in joined
