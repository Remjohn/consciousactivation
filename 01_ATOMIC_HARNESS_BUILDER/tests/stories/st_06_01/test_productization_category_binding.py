from __future__ import annotations

import json
from pathlib import Path

import pytest

from cmf_builder.application.export_service import PortableAtomicHarnessCompiler
from cmf_builder.application.manifest_parser import OperatorManifestParser
from cmf_builder.application.productization_contracts import (
    OperatorManifestRequest,
    ProductizationError,
)
from cmf_builder.domain.portable_export import PortableAtomicHarnessDefinition


ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "tests/fixtures/productization/manifests"


def _parse(name: str):
    path = FIXTURES / name
    return OperatorManifestParser().parse(
        OperatorManifestRequest(path.read_bytes(), path.name)
    )


def test_activative_manifest_and_portable_definition_preserve_category_binding() -> None:
    manifest = _parse("activative_expression.json")
    assert manifest.category_id == "conversational_activation_expression"
    record = PortableAtomicHarnessCompiler().compile(manifest)
    definition = PortableAtomicHarnessDefinition.from_payload_bytes(record.payload)
    binding = definition.content["category_binding"]
    assert binding["applicability"] == "REQUIRED"
    assert binding["category_id"] == "conversational_activation_expression"
    assert binding["runtime_law"] == "Activation First"
    assert binding["harness_development_law"] == "Visual Syntax First"
    assert binding["production_ready"] is False
    assert binding["certified"] is False


def test_activative_manifest_without_category_is_rejected() -> None:
    source = json.loads((FIXTURES / "activative_expression.json").read_text(encoding="utf-8"))
    del source["category_id"]
    with pytest.raises(ProductizationError):
        OperatorManifestParser().parse(
            OperatorManifestRequest(json.dumps(source).encode(), "missing-category.json")
        )


def test_generic_definition_declares_governed_not_applicable_category() -> None:
    record = PortableAtomicHarnessCompiler().compile(_parse("generic_text_summary.json"))
    definition = PortableAtomicHarnessDefinition.from_payload_bytes(record.payload)
    assert definition.content["category_binding"] == {
        "applicability": "NOT_APPLICABLE",
        "basis": "GENERIC_NON_ACTIVATIVE_TASK",
        "category_id": None,
    }
    assert "category_neutral" in definition.content["classification"]


def test_generic_manifest_cannot_smuggle_category_metadata() -> None:
    source = json.loads((FIXTURES / "generic_text_summary.json").read_text(encoding="utf-8"))
    source["category_id"] = "short_form_edited_video"
    with pytest.raises(ProductizationError):
        OperatorManifestParser().parse(
            OperatorManifestRequest(json.dumps(source).encode(), "generic-category.json")
        )
