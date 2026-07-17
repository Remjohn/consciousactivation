from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Mapping


CATEGORY_REGISTRY_SHA256 = "9a836e5cc80371719cce688884ca3f071ee500862d54e6533982266d15b553b1"
COMPATIBILITY_SHA256 = "781a438ef1298c1bc71da6ab54298774f09c0be97becf513510913f98fc97a71"
CONVERSATIONAL_REGISTRY_SHA256 = "e849f4217e488c7bf4685c167c69264d2e51e0880a403be01d242b6d5ab4b651"

EDITED_VIDEO_PROFILE_IDS = (
    "format01_story_video",
    "format03_living_commentary",
    "format04_conscious_reaction",
    "format05_silent_dialogue_theatre",
    "format06_data_scale_race",
    "format07_direct_coaching_a_roll",
    "format08_poetic_quote_theatre",
)
CONVERSATIONAL_PROFILE_IDS = (
    "public_comment",
    "reply_dm",
    "reelcast_expression",
    "interview_expression",
)
CHARACTER_PERFORMANCE_REGISTRIES = (
    "character_identity",
    "pose",
    "expression",
    "gesture",
    "gaze",
    "prop_and_attachment",
    "animation_primitive",
    "character_state",
    "scene_relationship",
    "camera_and_framing",
    "transition",
    "sonic_cue",
    "compatibility",
)
CANONICAL_CATEGORY_IDS = (
    "short_form_edited_video",
    "2d_character_animation",
    "carousels",
    "supervisuals",
    "conversational_activation_expression",
)


class ProfileCompilationError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class FormatProfile:
    profile_id: str
    category_id: str
    canonical_path: str
    substrate_grammar: str
    strongest_current_state: str
    required_registry_kinds: tuple[str, ...]
    reference_profile: bool
    structurally_supported: bool
    contract_compatible: bool
    benchmarked: bool
    limited_production_certified: bool
    production_certified: bool
    runtime_behavior_included: bool

    def canonical_dict(self) -> dict[str, object]:
        return {
            "profile_id": self.profile_id,
            "category_id": self.category_id,
            "canonical_path": self.canonical_path,
            "substrate_grammar": self.substrate_grammar,
            "strongest_current_state": self.strongest_current_state,
            "required_registry_kinds": list(self.required_registry_kinds),
            "reference_profile": self.reference_profile,
            "structurally_supported": self.structurally_supported,
            "contract_compatible": self.contract_compatible,
            "benchmarked": self.benchmarked,
            "limited_production_certified": self.limited_production_certified,
            "production_certified": self.production_certified,
            "runtime_behavior_included": self.runtime_behavior_included,
        }

    def validate_claim(self, *, production_certified: bool, benchmarked: bool) -> None:
        if production_certified or benchmarked:
            raise ProfileCompilationError(
                "Profile certification or benchmark claims are not supported by this structural branch."
            )


@dataclass(frozen=True, slots=True)
class CompiledProfileRegistry:
    registry_id: str
    registry_version: str
    runtime_law: str
    development_law: str
    source_hashes: tuple[tuple[str, str], ...]
    categories: tuple[tuple[str, tuple[str, ...]], ...]
    profiles: tuple[FormatProfile, ...]
    production_ready: bool
    certified: bool
    registry_hash: str
    canonical_bytes: bytes

    def category_profile_ids(self, category_id: str) -> tuple[str, ...]:
        for observed, profile_ids in self.categories:
            if observed == category_id:
                return profile_ids
        raise ProfileCompilationError(f"Category '{category_id}' is unknown.")

    def resolve_profile_id(self, profile_id: str) -> str:
        if profile_id == "minimal_coach_theatre":
            return "format02_minimal_coach_theatre"
        if any(item.profile_id == profile_id for item in self.profiles):
            return profile_id
        raise ProfileCompilationError(f"Profile '{profile_id}' is unknown.")

    def profile(self, profile_id: str) -> FormatProfile:
        canonical = self.resolve_profile_id(profile_id)
        for item in self.profiles:
            if item.profile_id == canonical:
                return item
        raise ProfileCompilationError(f"Profile '{profile_id}' is unknown.")

    def require_profile_category(self, profile_id: str, category_id: str) -> None:
        profile = self.profile(profile_id)
        if profile.category_id != category_id:
            raise ProfileCompilationError(
                "Profile cross-category reuse is prohibited."
            )

    def validate_format02_registry_state(self, state: Mapping[str, object]) -> None:
        missing = tuple(
            item for item in CHARACTER_PERFORMANCE_REGISTRIES if item not in state
        )
        if missing:
            raise ProfileCompilationError(
                "Format 02 is missing character-performance registry state: "
                + ",".join(missing)
            )
        unexpected = tuple(sorted(set(state) - set(CHARACTER_PERFORMANCE_REGISTRIES)))
        if unexpected:
            raise ProfileCompilationError(
                "Format 02 registry state contains unsupported entries: "
                + ",".join(unexpected)
            )
        if any(not isinstance(value, str) or not value.strip() for value in state.values()):
            raise ProfileCompilationError(
                "Every Format 02 registry state reference must be non-empty."
            )


def compile_structural_profile_registry(
    *,
    category_registry_bytes: bytes,
    compatibility_bytes: bytes,
    conversational_registry_bytes: bytes,
) -> CompiledProfileRegistry:
    source_hashes = (
        ("canonical_category_registry", _verify_hash(category_registry_bytes, CATEGORY_REGISTRY_SHA256)),
        ("category_profile_compatibility", _verify_hash(compatibility_bytes, COMPATIBILITY_SHA256)),
        ("conversational_profile_registry", _verify_hash(conversational_registry_bytes, CONVERSATIONAL_REGISTRY_SHA256)),
    )
    profiles: list[FormatProfile] = []
    for profile_id in EDITED_VIDEO_PROFILE_IDS:
        profiles.append(
            _profile(
                profile_id,
                "short_form_edited_video",
                "SHORT_FORM_EDITED_VIDEO_TIMELINE",
                "structurally_supported",
                contract_compatible=False,
            )
        )
    profiles.append(
        _profile(
            "format02_minimal_coach_theatre",
            "2d_character_animation",
            "TWO_D_CHARACTER_PERFORMANCE_CONTINUITY",
            "contract_compatible",
            required_registry_kinds=CHARACTER_PERFORMANCE_REGISTRIES,
            reference_profile=True,
            contract_compatible=True,
        )
    )
    for profile_id in CONVERSATIONAL_PROFILE_IDS:
        profiles.append(
            _profile(
                profile_id,
                "conversational_activation_expression",
                "CONVERSATIONAL_ACTIVATION_EXPRESSION",
                "contract_compatible",
                contract_compatible=True,
            )
        )
    categories = (
        ("short_form_edited_video", EDITED_VIDEO_PROFILE_IDS),
        ("2d_character_animation", ("format02_minimal_coach_theatre",)),
        ("carousels", ()),
        ("supervisuals", ()),
        ("conversational_activation_expression", CONVERSATIONAL_PROFILE_IDS),
    )
    content = {
        "schema_version": "cmf-builder-structural-profile-registry/v1",
        "registry_id": "category-local-format-profiles",
        "registry_version": "1.0.0",
        "runtime_law": "Activation First",
        "development_law": "Visual Syntax First",
        "source_hashes": [list(item) for item in source_hashes],
        "categories": [
            {"category_id": category_id, "profile_ids": list(profile_ids)}
            for category_id, profile_ids in categories
        ],
        "profiles": [item.canonical_dict() for item in profiles],
        "production_ready": False,
        "certified": False,
    }
    canonical_bytes = _canonical_json(content)
    digest = sha256(canonical_bytes).hexdigest()
    return CompiledProfileRegistry(
        registry_id="category-local-format-profiles",
        registry_version="1.0.0",
        runtime_law="Activation First",
        development_law="Visual Syntax First",
        source_hashes=source_hashes,
        categories=categories,
        profiles=tuple(profiles),
        production_ready=False,
        certified=False,
        registry_hash=f"sha256:{digest}",
        canonical_bytes=canonical_bytes,
    )


def _profile(
    profile_id: str,
    category_id: str,
    substrate_grammar: str,
    strongest_current_state: str,
    *,
    required_registry_kinds: tuple[str, ...] = (),
    reference_profile: bool = False,
    contract_compatible: bool,
) -> FormatProfile:
    return FormatProfile(
        profile_id=profile_id,
        category_id=category_id,
        canonical_path=f"{category_id}/{profile_id}",
        substrate_grammar=substrate_grammar,
        strongest_current_state=strongest_current_state,
        required_registry_kinds=required_registry_kinds,
        reference_profile=reference_profile,
        structurally_supported=True,
        contract_compatible=contract_compatible,
        benchmarked=False,
        limited_production_certified=False,
        production_certified=False,
        runtime_behavior_included=False,
    )


def _verify_hash(value: bytes, expected: str) -> str:
    if not isinstance(value, bytes) or not value:
        raise ProfileCompilationError("Governing registry bytes are required.")
    digest = sha256(value).hexdigest()
    if digest != expected:
        raise ProfileCompilationError("Governing registry hash mismatch.")
    return f"sha256:{digest}"


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
