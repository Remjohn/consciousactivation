from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from cmf_builder.domain.category_binding import (
    ACTIVATION_FIRST,
    CANONICAL_CATEGORY_IDS,
    VISUAL_SYNTAX_FIRST,
    CanonicalCategoryRegistry,
    CategoryBinding,
    CategoryBindingError,
)


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "governance/CANONICAL_CATEGORY_REGISTRY.yaml"
ACTIVATIVE = ROOT / "tests/fixtures/productization/manifests/activative_expression.json"


def _activative() -> dict[str, object]:
    return json.loads(ACTIVATIVE.read_text(encoding="utf-8"))["activative_input"]


def _bind(category_id: str) -> CategoryBinding:
    return CategoryBinding.create(
        harness_id="activative-harness",
        harness_version="1.0.0",
        mode="activative",
        category_ids=(category_id,),
        activative_input=_activative(),
        registry_bytes=REGISTRY.read_bytes(),
    )


def test_registry_preserves_exact_five_constitutional_identities() -> None:
    registry = CanonicalCategoryRegistry.from_bytes(REGISTRY.read_bytes())
    assert registry.category_ids == CANONICAL_CATEGORY_IDS
    assert len(registry.categories) == 5
    assert registry.version == "1.2.0-aligned"
    assert registry.categories[-1].category_id == "conversational_activation_expression"
    assert registry.categories[-1].canonical_name == "Conversational Activation / Human Expression"
    assert all(item.governance_owner for item in registry.categories)


@pytest.mark.parametrize("category_id", CANONICAL_CATEGORY_IDS)
def test_every_category_produces_one_deterministic_uncertified_binding(category_id: str) -> None:
    first = _bind(category_id)
    second = _bind(category_id)
    assert first == second
    assert first.category_id == category_id
    assert first.applicability == "REQUIRED"
    assert first.runtime_law == ACTIVATION_FIRST
    assert first.harness_development_law == VISUAL_SYNTAX_FIRST
    assert first.production_ready is False
    assert first.certified is False
    assert first.certification_state == "STRUCTURAL_UNCERTIFIED"
    assert len(first.semantic_lineage_refs) >= 8
    assert first.wrong_reading_locks
    assert first.binding_hash.startswith("sha256:")


def test_generic_non_activative_branch_is_explicitly_not_applicable() -> None:
    binding = CategoryBinding.create(
        harness_id="generic-task",
        harness_version="1.0.0",
        mode="generic",
        category_ids=(),
        activative_input=None,
        registry_bytes=REGISTRY.read_bytes(),
    )
    assert binding.applicability == "NOT_APPLICABLE"
    assert binding.category_id is None
    assert binding.not_applicable_basis == "GENERIC_NON_ACTIVATIVE_TASK"
    assert binding.production_ready is False
    assert binding.certified is False


@pytest.mark.parametrize(
    ("category_ids", "match"),
    [
        ((), "exactly one"),
        (("carousels", "supervisuals"), "exactly one"),
        (("universal_creative",), "unsupported"),
    ],
)
def test_categoryless_multiple_and_unsupported_activative_bindings_fail_closed(
    category_ids: tuple[str, ...], match: str
) -> None:
    with pytest.raises(CategoryBindingError, match=match):
        CategoryBinding.create(
            harness_id="activative-harness",
            harness_version="1.0.0",
            mode="activative",
            category_ids=category_ids,
            activative_input=_activative(),
            registry_bytes=REGISTRY.read_bytes(),
        )


@pytest.mark.parametrize(
    "field",
    [
        "identity_dna_ref",
        "context_premise_ref",
        "resonance_map_ref",
        "matrix_of_edging_ref",
        "activative_intelligence_pack_ref",
        "evaluation_contract_ref",
        "wrong_reading_locks",
    ],
)
def test_missing_semantic_stack_or_wrong_reading_locks_fails_hg015(field: str) -> None:
    activative = deepcopy(_activative())
    activative[field] = [] if field == "wrong_reading_locks" else ""
    with pytest.raises(CategoryBindingError) as raised:
        CategoryBinding.create(
            harness_id="activative-harness",
            harness_version="1.0.0",
            mode="activative",
            category_ids=("short_form_edited_video",),
            activative_input=activative,
            registry_bytes=REGISTRY.read_bytes(),
        )
    assert raised.value.code == "HG-015"


def test_registry_drift_and_missing_fifth_category_fail_closed() -> None:
    mutated = REGISTRY.read_bytes().replace(
        b"conversational_activation_expression", b"flattened_expression_category"
    )
    with pytest.raises(CategoryBindingError, match="registry"):
        CanonicalCategoryRegistry.from_bytes(mutated)


def test_category_change_requires_a_new_immutable_harness_version() -> None:
    current = _bind("carousels")
    with pytest.raises(CategoryBindingError, match="new immutable Harness version"):
        current.validate_rebinding(
            candidate_harness_version="1.0.0",
            candidate_category_id="supervisuals",
        )
    current.validate_rebinding(
        candidate_harness_version="2.0.0",
        candidate_category_id="supervisuals",
    )

