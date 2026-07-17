from __future__ import annotations

from pathlib import Path

from cmf_builder.domain.format_profiles import (
    CHARACTER_PERFORMANCE_REGISTRIES,
    CONVERSATIONAL_PROFILE_IDS,
    EDITED_VIDEO_PROFILE_IDS,
    compile_structural_profile_registry,
)


ROOT = Path(__file__).resolve().parents[3]
CATEGORIES = ROOT / "governance/CANONICAL_CATEGORY_REGISTRY.yaml"
CONVERSATIONAL = ROOT / "governance/CONVERSATIONAL_PROFILE_REGISTRY.yaml"
COMPATIBILITY = ROOT / "contracts/integration/CATEGORY_PROFILE_COMPATIBILITY.yaml"


def _compile():
    return compile_structural_profile_registry(
        category_registry_bytes=CATEGORIES.read_bytes(),
        compatibility_bytes=COMPATIBILITY.read_bytes(),
        conversational_registry_bytes=CONVERSATIONAL.read_bytes(),
    )


def test_exact_edited_video_mapping_excludes_format02() -> None:
    registry = _compile()
    assert registry.category_profile_ids("short_form_edited_video") == EDITED_VIDEO_PROFILE_IDS
    assert "format02_minimal_coach_theatre" not in EDITED_VIDEO_PROFILE_IDS
    for profile_id in EDITED_VIDEO_PROFILE_IDS:
        profile = registry.profile(profile_id)
        assert profile.category_id == "short_form_edited_video"
        assert profile.substrate_grammar == "SHORT_FORM_EDITED_VIDEO_TIMELINE"
        assert profile.strongest_current_state == "structurally_supported"


def test_format02_is_character_performance_reference_without_certification() -> None:
    profile = _compile().profile("format02_minimal_coach_theatre")
    assert profile.category_id == "2d_character_animation"
    assert profile.canonical_path == "2d_character_animation/format02_minimal_coach_theatre"
    assert profile.substrate_grammar == "TWO_D_CHARACTER_PERFORMANCE_CONTINUITY"
    assert profile.required_registry_kinds == CHARACTER_PERFORMANCE_REGISTRIES
    assert profile.reference_profile is True
    assert profile.strongest_current_state == "contract_compatible"
    assert profile.benchmarked is False
    assert profile.production_certified is False
    assert profile.limited_production_certified is False


def test_conversational_profiles_remain_structural_uncertified_under_fifth_category() -> None:
    registry = _compile()
    assert registry.category_profile_ids("conversational_activation_expression") == CONVERSATIONAL_PROFILE_IDS
    for profile_id in CONVERSATIONAL_PROFILE_IDS:
        profile = registry.profile(profile_id)
        assert profile.category_id == "conversational_activation_expression"
        assert profile.substrate_grammar == "CONVERSATIONAL_ACTIVATION_EXPRESSION"
        assert profile.production_certified is False
        assert profile.runtime_behavior_included is False


def test_categories_without_current_profiles_are_explicit() -> None:
    registry = _compile()
    assert registry.category_profile_ids("carousels") == ()
    assert registry.category_profile_ids("supervisuals") == ()


def test_compilation_is_byte_deterministic_and_preserves_both_laws() -> None:
    first = _compile()
    second = _compile()
    assert first == second
    assert first.canonical_bytes == second.canonical_bytes
    assert first.registry_hash == second.registry_hash
    assert first.runtime_law == "Activation First"
    assert first.development_law == "Visual Syntax First"
    assert first.production_ready is False
    assert first.certified is False

