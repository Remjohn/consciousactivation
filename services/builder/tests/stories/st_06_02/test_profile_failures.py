from __future__ import annotations

from pathlib import Path

import pytest

from cmf_builder.domain.format_profiles import (
    ProfileCompilationError,
    compile_structural_profile_registry,
)


ROOT = Path(__file__).resolve().parents[3]
CATEGORIES = ROOT / "governance/CANONICAL_CATEGORY_REGISTRY.yaml"
CONVERSATIONAL = ROOT / "governance/CONVERSATIONAL_PROFILE_REGISTRY.yaml"
COMPATIBILITY = ROOT / "contracts/integration/CATEGORY_PROFILE_COMPATIBILITY.yaml"


def _compile(**overrides):
    values = {
        "category_registry_bytes": CATEGORIES.read_bytes(),
        "compatibility_bytes": COMPATIBILITY.read_bytes(),
        "conversational_registry_bytes": CONVERSATIONAL.read_bytes(),
    }
    values.update(overrides)
    return compile_structural_profile_registry(**values)


@pytest.mark.parametrize(
    "field",
    ["category_registry_bytes", "compatibility_bytes", "conversational_registry_bytes"],
)
def test_altered_governing_registry_fails_closed(field: str) -> None:
    original = {
        "category_registry_bytes": CATEGORIES.read_bytes(),
        "compatibility_bytes": COMPATIBILITY.read_bytes(),
        "conversational_registry_bytes": CONVERSATIONAL.read_bytes(),
    }[field]
    with pytest.raises(ProfileCompilationError, match="hash"):
        _compile(**{field: original + b"\n# drift"})


def test_cross_category_binding_and_unknown_profile_fail_closed() -> None:
    registry = _compile()
    with pytest.raises(ProfileCompilationError, match="cross-category"):
        registry.require_profile_category(
            "format02_minimal_coach_theatre", "short_form_edited_video"
        )
    with pytest.raises(ProfileCompilationError, match="unknown"):
        registry.profile("format99_unknown")


def test_historical_format02_alias_resolves_to_canonical_output_only() -> None:
    registry = _compile()
    assert registry.resolve_profile_id("minimal_coach_theatre") == "format02_minimal_coach_theatre"
    assert registry.profile("minimal_coach_theatre").profile_id == "format02_minimal_coach_theatre"


def test_missing_character_performance_state_rejects_when_state_is_bound() -> None:
    registry = _compile()
    with pytest.raises(ProfileCompilationError, match="missing character-performance"):
        registry.validate_format02_registry_state({})


def test_false_certification_projection_is_rejected() -> None:
    registry = _compile()
    profile = registry.profile("format02_minimal_coach_theatre")
    with pytest.raises(ProfileCompilationError, match="certification"):
        profile.validate_claim(production_certified=True, benchmarked=False)

