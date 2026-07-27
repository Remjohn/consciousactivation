from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from cmf_builder.application.manifest_parser import (
    OperatorManifestParser,
    parse_operator_manifest,
)
from cmf_builder.application.productization_contracts import (
    OperatorManifestRequest,
    ProductizationError,
    ProductizationErrorCode,
)


FIXTURES = Path("tests/fixtures/productization/manifests")


def _fixture(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


def _request(content: bytes, name: str = "operator-task.json") -> OperatorManifestRequest:
    return OperatorManifestRequest(manifest_bytes=content, source_name=name)


def _mapping(name: str) -> dict[str, object]:
    return json.loads(_fixture(name))


def _encoded(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False).encode("utf-8")


def test_generic_manifest_is_canonical_and_hash_pinned() -> None:
    result = parse_operator_manifest(_request(_fixture("generic_text_summary.json")))

    assert result.manifest_id == "operator-manifest-generic-summary"
    assert result.manifest_version == "1.0.0"
    assert result.task_id == "generic_text_summary_v1"
    assert result.mode == "generic"
    assert result.activative_input is None
    assert result.canonical_bytes.endswith(b"\n")
    assert result.manifest_hash == f"sha256:{sha256(result.canonical_bytes).hexdigest()}"
    assert json.loads(result.canonical_bytes) == result.normalized


def test_key_order_and_incidental_whitespace_do_not_change_identity() -> None:
    source = _mapping("generic_text_summary.json")
    reordered = {key: source[key] for key in reversed(source)}
    reordered["task"] = {
        key: source["task"][key] for key in reversed(source["task"])
    }
    reordered["manifest_id"] = "  operator-manifest-generic-summary  "

    first = parse_operator_manifest(_request(_fixture("generic_text_summary.json")))
    second = parse_operator_manifest(_request(_encoded(reordered)))

    assert first.canonical_bytes == second.canonical_bytes
    assert first.manifest_hash == second.manifest_hash


def test_activative_manifest_preserves_complete_rich_contract() -> None:
    result = OperatorManifestParser().parse(
        _request(_fixture("activative_expression.json"))
    )

    contract = result.activative_input
    assert result.mode == "activative"
    assert contract is not None
    assert contract.identity_dna_ref.startswith("identity-dna@4.2.0#sha256:")
    assert contract.activation_directions == ("recognize", "reframe", "choose")
    assert contract.roles == ("coach", "participant")
    assert contract.smallest_useful_commitment == "Name the next reversible action."
    assert contract.wrong_reading_locks == (
        "Do not frame hesitation as incapacity.",
    )
    assert contract.reaction_receipt_refs == ()
    assert contract.expression_moment_refs == ()
    normalized = result.normalized["activative_input"]
    assert isinstance(normalized, dict)
    assert normalized["identity_dna_ref"] == contract.identity_dna_ref
    assert "notes" not in normalized


@pytest.mark.parametrize(
    "field",
    [
        "source_premise_ref",
        "identity_dna_ref",
        "context_premise_ref",
        "resonance_map_ref",
        "matrix_of_edging_ref",
        "activative_intelligence_pack_ref",
        "hidden_pressure",
        "activation_directions",
        "roles",
        "stance",
        "stakes",
        "identity_urges",
        "participation_design",
        "intended_reaction",
        "smallest_useful_commitment",
        "evidence_provenance_refs",
        "evaluation_contract_ref",
        "wrong_reading_locks",
    ],
)
def test_every_rich_activative_field_is_mandatory(field: str) -> None:
    source = _mapping("activative_expression.json")
    del source["activative_input"][field]

    with pytest.raises(ProductizationError) as raised:
        parse_operator_manifest(_request(_encoded(source)))

    assert raised.value.code is ProductizationErrorCode.INVALID_ACTIVATIVE_INPUT
    assert raised.value.field_path == "activative_input"


def test_generic_mode_rejects_activative_input() -> None:
    generic = _mapping("generic_text_summary.json")
    generic["activative_input"] = _mapping("activative_expression.json")[
        "activative_input"
    ]

    with pytest.raises(ProductizationError) as raised:
        parse_operator_manifest(_request(_encoded(generic)))

    assert raised.value.code is ProductizationErrorCode.INVALID_MANIFEST
    assert raised.value.field_path == "manifest"


def test_activative_mode_rejects_flattened_notes_instead_of_rich_fields() -> None:
    source = _mapping("activative_expression.json")
    source["activative_input"] = {"notes": "all Activative meaning was here"}

    with pytest.raises(ProductizationError) as raised:
        parse_operator_manifest(_request(_encoded(source)))

    assert raised.value.code is ProductizationErrorCode.INVALID_ACTIVATIVE_INPUT
    assert raised.value.field_path == "activative_input"


def test_identity_dna_mutation_is_rejected_even_inside_input_contract() -> None:
    source = _mapping("activative_expression.json")
    source["task"]["input_contract"]["identity_dna_patch"] = {
        "type": "object"
    }

    with pytest.raises(ProductizationError) as raised:
        parse_operator_manifest(_request(_encoded(source)))

    assert raised.value.code is ProductizationErrorCode.INVALID_MANIFEST
    assert raised.value.field_path.endswith("identity_dna_patch")


def test_identity_dna_reference_is_never_rewritten() -> None:
    source = _mapping("activative_expression.json")
    expected = source["activative_input"]["identity_dna_ref"]
    original = deepcopy(source)

    result = parse_operator_manifest(_request(_encoded(source)))

    assert result.activative_input is not None
    assert result.activative_input.identity_dna_ref == expected
    assert result.normalized["activative_input"]["identity_dna_ref"] == expected
    assert source == original


def test_mutable_or_unhashed_rich_reference_fails_closed() -> None:
    source = _mapping("activative_expression.json")
    source["activative_input"]["identity_dna_ref"] = "identity-dna-latest"

    with pytest.raises(ProductizationError) as raised:
        parse_operator_manifest(_request(_encoded(source)))

    assert raised.value.code is ProductizationErrorCode.INVALID_ACTIVATIVE_INPUT
    assert raised.value.field_path == "activative_input.identity_dna_ref"


@pytest.mark.parametrize("claim", ["production_ready", "certified"])
def test_operator_cannot_claim_production_or_certification(claim: str) -> None:
    source = _mapping("generic_text_summary.json")
    source["task"]["output_contract"][claim] = False

    with pytest.raises(ProductizationError) as raised:
        parse_operator_manifest(_request(_encoded(source)))

    assert raised.value.code is ProductizationErrorCode.INVALID_MANIFEST
    assert claim in (raised.value.field_path or "")


def test_duplicate_json_keys_fail_closed() -> None:
    duplicate = b'{"manifest_id":"one","manifest_id":"two"}'

    with pytest.raises(ProductizationError) as raised:
        parse_operator_manifest(_request(duplicate))

    assert raised.value.code is ProductizationErrorCode.INVALID_MANIFEST
    assert raised.value.field_path == "manifest_id"


@pytest.mark.parametrize(
    "content",
    [b"", b"not-json", b"\xef\xbb\xbf{}", b'{"value":NaN}'],
)
def test_unreadable_or_noncanonical_json_fails_closed(content: bytes) -> None:
    with pytest.raises(ProductizationError) as raised:
        parse_operator_manifest(_request(content))

    assert raised.value.code is ProductizationErrorCode.INVALID_MANIFEST


def test_duplicate_governed_list_entries_fail_closed() -> None:
    source = _mapping("generic_text_summary.json")
    source["task"]["required_context"].append(
        source["task"]["required_context"][0]
    )

    with pytest.raises(ProductizationError) as raised:
        parse_operator_manifest(_request(_encoded(source)))

    assert raised.value.code is ProductizationErrorCode.INVALID_MANIFEST
    assert raised.value.field_path == "task.required_context"
