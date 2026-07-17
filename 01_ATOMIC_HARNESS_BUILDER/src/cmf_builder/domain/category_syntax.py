from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Mapping


ACTIVATION_FIRST = "Activation First"
VISUAL_SYNTAX_FIRST = "Visual Syntax First"
CATEGORY_CONSTITUTION_VERSION = "1.1"
MATURITY_STATUS = "OFFLINE_STRUCTURAL_IMPLEMENTED_EVIDENCE_PENDING"
NOT_APPLICABLE = "NOT_APPLICABLE"

EDITED_VIDEO_PROFILES = (
    "format01_story_video",
    "format03_living_commentary",
    "format04_conscious_reaction",
    "format05_silent_dialogue_theatre",
    "format06_data_scale_race",
    "format07_direct_coaching_a_roll",
    "format08_poetic_quote_theatre",
)
CONVERSATIONAL_PROFILES = (
    "public_comment",
    "reply_dm",
    "reelcast_expression",
    "interview_expression",
)
CATEGORY_PROFILE_CONTRACTS: Mapping[str, tuple[str, ...]] = {
    "short_form_edited_video": EDITED_VIDEO_PROFILES,
    "2d_character_animation": ("format02_minimal_coach_theatre",),
    "carousels": (),
    "supervisuals": (),
    "conversational_activation_expression": CONVERSATIONAL_PROFILES,
}
GRAMMAR_FAMILIES: Mapping[str, str] = {
    "short_form_edited_video": "SHORT_FORM_EDITED_VIDEO_TIMELINE",
    "2d_character_animation": "TWO_D_CHARACTER_PERFORMANCE_CONTINUITY",
    "carousels": "CAROUSEL_SWIPE_PROGRESSION",
    "supervisuals": "SUPERVISUAL_STATIC_HIERARCHY",
    "conversational_activation_expression": "CONVERSATIONAL_TURN_RELATIONSHIP",
}
REQUIRED_RICH_LINEAGE_ROLES = frozenset(
    {
        "source_premise",
        "identity_dna",
        "context_premise",
        "resonance_map",
        "matrix_of_edging",
        "activative_intelligence_pack",
        "evaluation_contract",
    }
)
_SHA256 = re.compile(r"^[a-f0-9]{64}$")


class CategorySyntaxError(ValueError):
    def __init__(self, message: str, *, code: str = "CATEGORY_SYNTAX_REJECTED") -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class GovernedRef:
    object_id: str
    version: str
    sha256: str
    authority: str
    lineage_role: str
    status: str = "ACTIVE"

    def validate(self) -> None:
        _require_text(self.object_id, "ref.object_id")
        _require_text(self.version, "ref.version")
        _require_text(self.authority, "ref.authority")
        _require_text(self.lineage_role, "ref.lineage_role")
        if not _SHA256.fullmatch(self.sha256):
            raise CategorySyntaxError("A governed reference has an invalid SHA-256.")
        if self.status != "ACTIVE":
            raise CategorySyntaxError(
                "Stale, superseded, or invalidated lineage cannot compile active syntax."
            )

    def canonical_dict(self) -> dict[str, str]:
        return {
            "object_id": self.object_id,
            "version": self.version,
            "sha256": self.sha256,
            "authority": self.authority,
            "lineage_role": self.lineage_role,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class GrammarDimension:
    applicability: str
    rules: tuple[str, ...]
    basis: str

    @classmethod
    def required(cls, *rules: str) -> "GrammarDimension":
        validated = tuple(_require_text(rule, "grammar rule") for rule in rules)
        if not validated:
            raise CategorySyntaxError("Applicable grammar requires at least one rule.")
        return cls("REQUIRED", validated, "CATEGORY_NATIVE")

    @classmethod
    def not_applicable(cls, basis: str) -> "GrammarDimension":
        return cls(NOT_APPLICABLE, (), _require_text(basis, "not applicable basis"))

    def canonical_dict(self) -> dict[str, object]:
        return {
            "applicability": self.applicability,
            "rules": list(self.rules),
            "basis": self.basis,
        }


@dataclass(frozen=True, slots=True)
class CategorySyntaxInput:
    harness_id: str
    harness_version: str
    mode: str
    category_id: str | None
    profile_id: str | None
    category_constitution_version: str | None
    requested_grammar_family: str | None
    category_binding_ref: GovernedRef | None
    structural_profile_ref: GovernedRef | None
    shared_activative_core_ref: GovernedRef | None
    evidence_refs: tuple[GovernedRef, ...]
    rich_source_object_refs: tuple[GovernedRef, ...]
    authority_refs: tuple[GovernedRef, ...]
    wrong_reading_locks: tuple[str, ...]
    activation_direction: str | None
    participant_role: str | None
    states: tuple[str, ...]
    transitions: tuple[str, ...]
    pacing: str | None
    sonic_or_silence_function: str | None
    payoff: str | None
    intended_reaction: str | None
    micro_commitment: str | None
    production_ready: bool = False
    certified: bool = False

    def canonical_dict(self) -> dict[str, object]:
        return {
            "harness_id": self.harness_id,
            "harness_version": self.harness_version,
            "mode": self.mode,
            "category_id": self.category_id,
            "profile_id": self.profile_id,
            "category_constitution_version": self.category_constitution_version,
            "requested_grammar_family": self.requested_grammar_family,
            "category_binding_ref": _optional_ref(self.category_binding_ref),
            "structural_profile_ref": _optional_ref(self.structural_profile_ref),
            "shared_activative_core_ref": _optional_ref(
                self.shared_activative_core_ref
            ),
            "evidence_refs": _canonical_refs(self.evidence_refs),
            "rich_source_object_refs": _canonical_refs(
                self.rich_source_object_refs
            ),
            "authority_refs": _canonical_refs(self.authority_refs),
            "wrong_reading_locks": list(self.wrong_reading_locks),
            "activation_direction": self.activation_direction,
            "participant_role": self.participant_role,
            "states": list(self.states),
            "transitions": list(self.transitions),
            "pacing": self.pacing,
            "sonic_or_silence_function": self.sonic_or_silence_function,
            "payoff": self.payoff,
            "intended_reaction": self.intended_reaction,
            "micro_commitment": self.micro_commitment,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }


@dataclass(frozen=True, slots=True)
class CategoryNativeSyntax:
    syntax_id: str
    version: str
    harness_id: str
    harness_version: str
    applicability: str
    category_id: str | None
    profile_id: str | None
    category_constitution_version: str | None
    grammar_family: str | None
    spatial_grammar: GrammarDimension
    temporal_grammar: GrammarDimension
    reading_order: GrammarDimension
    character_performance_grammar: GrammarDimension
    conversational_turn_structure: GrammarDimension
    wrong_reading_locks: tuple[str, ...]
    semantic_lineage: tuple[GovernedRef, ...]
    runtime_law: str
    development_law: str
    maturity_status: str
    evidence_gate: str
    production_ready: bool
    certified: bool
    syntax_hash: str
    canonical_bytes: bytes

    def canonical_dict(self) -> dict[str, object]:
        content = json.loads(self.canonical_bytes.decode("utf-8"))
        content["syntax_hash"] = self.syntax_hash
        return content


@dataclass(frozen=True, slots=True)
class ActivativeSequenceProgram:
    sequence_id: str
    version: str
    harness_id: str
    harness_version: str
    applicability: str
    shared_core_ref: GovernedRef | None
    category_syntax_ref: str
    activation_direction: str | None
    participant_role: str | None
    states: tuple[str, ...]
    transitions: tuple[str, ...]
    pacing: str | None
    sonic_or_silence_function: str | None
    payoff: str | None
    intended_reaction: str | None
    micro_commitment: str | None
    wrong_reading_locks: tuple[str, ...]
    semantic_lineage: tuple[GovernedRef, ...]
    runtime_law: str
    development_law: str
    maturity_status: str
    evidence_gate: str
    production_ready: bool
    certified: bool
    sequence_hash: str
    canonical_bytes: bytes

    def canonical_dict(self) -> dict[str, object]:
        content = json.loads(self.canonical_bytes.decode("utf-8"))
        content["sequence_hash"] = self.sequence_hash
        return content


def compile_category_native_syntax(
    source: CategorySyntaxInput,
) -> tuple[CategoryNativeSyntax, ActivativeSequenceProgram]:
    _require_text(source.harness_id, "harness_id")
    _require_text(source.harness_version, "harness_version")
    if source.production_ready or source.certified:
        raise CategorySyntaxError(
            "The offline structural branch cannot claim production or certification."
        )
    if source.mode == "generic":
        _validate_generic(source)
        return _compile_generic(source)
    if source.mode != "activative":
        raise CategorySyntaxError("Only generic and activative modes are governed.")
    _validate_activative(source)
    dimensions = _category_dimensions(source.category_id, source.profile_id)
    lineage = _complete_lineage(source)
    locks = tuple(sorted(source.wrong_reading_locks))
    syntax = _build_syntax(source, dimensions, lineage, locks)
    sequence = _build_sequence(source, syntax, lineage, locks)
    return syntax, sequence


def _validate_generic(source: CategorySyntaxInput) -> None:
    forbidden = (
        source.category_id,
        source.profile_id,
        source.category_constitution_version,
        source.requested_grammar_family,
        source.category_binding_ref,
        source.structural_profile_ref,
        source.shared_activative_core_ref,
        source.activation_direction,
        source.participant_role,
        source.pacing,
        source.sonic_or_silence_function,
        source.payoff,
        source.intended_reaction,
        source.micro_commitment,
    )
    if any(item is not None for item in forbidden):
        raise CategorySyntaxError(
            "A generic task cannot acquire Activative category semantics."
        )
    if (
        source.evidence_refs
        or source.rich_source_object_refs
        or source.authority_refs
        or source.wrong_reading_locks
        or source.states
        or source.transitions
    ):
        raise CategorySyntaxError(
            "A generic task cannot carry Activative syntax or lineage."
        )


def _validate_activative(source: CategorySyntaxInput) -> None:
    category_id = _require_text(source.category_id, "category_id")
    if category_id not in CATEGORY_PROFILE_CONTRACTS:
        raise CategorySyntaxError(f"Category '{category_id}' is unsupported.")
    if source.category_constitution_version != CATEGORY_CONSTITUTION_VERSION:
        raise CategorySyntaxError("The category constitution version is not current.")
    expected_family = GRAMMAR_FAMILIES[category_id]
    if source.requested_grammar_family != expected_family:
        raise CategorySyntaxError(
            "Category flattening or cross-category grammar substitution is prohibited."
        )
    governed_profiles = CATEGORY_PROFILE_CONTRACTS[category_id]
    if governed_profiles:
        if source.profile_id not in governed_profiles:
            raise CategorySyntaxError(
                "The structural profile is not owned by the selected category."
            )
    elif source.profile_id is not None:
        raise CategorySyntaxError(
            "This category has no governed category-local profile in the active registry."
        )
    for field, ref in (
        ("category_binding_ref", source.category_binding_ref),
        ("structural_profile_ref", source.structural_profile_ref),
        ("shared_activative_core_ref", source.shared_activative_core_ref),
    ):
        if ref is None:
            raise CategorySyntaxError(f"{field} is required.")
        ref.validate()
    if not source.evidence_refs:
        raise CategorySyntaxError("At least one governed evidence reference is required.")
    if not source.authority_refs:
        raise CategorySyntaxError("At least one authority reference is required.")
    if not source.rich_source_object_refs:
        raise CategorySyntaxError("Frozen rich-object lineage is required.", code="HG-015")
    for ref in (
        source.evidence_refs
        + source.rich_source_object_refs
        + source.authority_refs
    ):
        ref.validate()
    roles = {ref.lineage_role for ref in source.rich_source_object_refs}
    missing_roles = sorted(REQUIRED_RICH_LINEAGE_ROLES - roles)
    if missing_roles:
        raise CategorySyntaxError(
            "Frozen rich-object lineage is incomplete: " + ",".join(missing_roles),
            code="HG-015",
        )
    _require_unique_texts(source.wrong_reading_locks, "wrong_reading_locks")
    _require_text(source.activation_direction, "activation_direction")
    _require_text(source.participant_role, "participant_role")
    _require_unique_texts(source.states, "states")
    _require_unique_texts(source.transitions, "transitions")
    _require_text(source.pacing, "pacing")
    _require_text(source.sonic_or_silence_function, "sonic_or_silence_function")
    _require_text(source.payoff, "payoff")
    _require_text(source.intended_reaction, "intended_reaction")
    _require_text(source.micro_commitment, "micro_commitment")


def _category_dimensions(
    category_id: str | None, profile_id: str | None
) -> tuple[GrammarDimension, ...]:
    if category_id == "short_form_edited_video":
        return (
            GrammarDimension.required("frame_hierarchy", "subject_caption_separation"),
            GrammarDimension.required("time_state_order", "edited_transition_continuity"),
            GrammarDimension.required("hook_to_evidence_to_payoff"),
            GrammarDimension.not_applicable("NO_CHARACTER_PERFORMANCE_SUBSTRATE"),
            GrammarDimension.not_applicable("NO_CONVERSATIONAL_TURN_SUBSTRATE"),
        )
    if category_id == "2d_character_animation":
        return (
            GrammarDimension.required("stage_relationships", "camera_and_framing"),
            GrammarDimension.required("performance_beats", "character_state_continuity"),
            GrammarDimension.required("character_to_evidence_to_activative_call"),
            GrammarDimension.required(
                "identity_pose_expression_gesture_gaze",
                "prop_attachment_and_animation_primitives",
            ),
            GrammarDimension.not_applicable("NO_CONVERSATIONAL_TURN_SUBSTRATE"),
        )
    if category_id == "carousels":
        return (
            GrammarDimension.required("slide_role_layout", "cross_slide_anchor_continuity"),
            GrammarDimension.not_applicable("STATIC_SLIDES_HAVE_NO_FRAME_TIME_MOTION"),
            GrammarDimension.required("swipe_progression", "final_commitment_slide"),
            GrammarDimension.not_applicable("NO_CHARACTER_PERFORMANCE_SUBSTRATE"),
            GrammarDimension.not_applicable("NO_CONVERSATIONAL_TURN_SUBSTRATE"),
        )
    if category_id == "supervisuals":
        return (
            GrammarDimension.required(
                "single_frame_attention_hierarchy",
                "feed_size_legibility",
                "static_composition",
            ),
            GrammarDimension.not_applicable("SINGLE_FRAME_HAS_NO_TEMPORAL_GRAMMAR"),
            GrammarDimension.required("recognition_to_pressure_to_activative_call"),
            GrammarDimension.not_applicable("NO_CHARACTER_PERFORMANCE_SUBSTRATE"),
            GrammarDimension.not_applicable("NO_CONVERSATIONAL_TURN_SUBSTRATE"),
        )
    if category_id == "conversational_activation_expression":
        return (
            GrammarDimension.not_applicable("CONVERSATIONAL_SURFACE_IS_NOT_A_FRAME_LAYOUT"),
            GrammarDimension.not_applicable("CONVERSATIONAL_SURFACE_IS_NOT_A_TIMELINE"),
            GrammarDimension.required("turn_sequence_reading_order"),
            GrammarDimension.not_applicable("NO_CHARACTER_PERFORMANCE_SUBSTRATE"),
            GrammarDimension.required(*_conversation_rules(profile_id)),
        )
    raise CategorySyntaxError("No category-native grammar exists for the category.")


def _conversation_rules(profile_id: str | None) -> tuple[str, ...]:
    common = (
        "turn_relationship",
        "activative_call",
        "reaction_receipt_reference_only",
        "expression_moment_reference_only",
        "human_landing_reference_only",
        "micro_commitment",
    )
    local: Mapping[str, tuple[str, ...]] = {
        "public_comment": ("public_call_and_open_response_boundary",),
        "reply_dm": ("prior_call_reaction_reference_and_adaptive_reply",),
        "reelcast_expression": ("message_elevation_and_reelcast_close_reference",),
        "interview_expression": ("adaptive_guest_call_and_human_ratified_landing_reference",),
    }
    if profile_id not in local:
        raise CategorySyntaxError("A governed conversational profile is required.")
    return common + local[profile_id]


def _compile_generic(
    source: CategorySyntaxInput,
) -> tuple[CategoryNativeSyntax, ActivativeSequenceProgram]:
    not_applicable = GrammarDimension.not_applicable("GENERIC_NON_ACTIVATIVE_TASK")
    dimensions = (
        not_applicable,
        not_applicable,
        not_applicable,
        not_applicable,
        not_applicable,
    )
    syntax = _build_syntax(source, dimensions, (), ())
    return syntax, _build_sequence(source, syntax, (), ())


def _build_syntax(
    source: CategorySyntaxInput,
    dimensions: tuple[GrammarDimension, ...],
    lineage: tuple[GovernedRef, ...],
    locks: tuple[str, ...],
) -> CategoryNativeSyntax:
    applicability = "REQUIRED" if source.mode == "activative" else NOT_APPLICABLE
    content: dict[str, object] = {
        "schema_version": "cmf-builder-category-native-syntax/v1",
        "version": "1.0.0",
        "harness_id": source.harness_id,
        "harness_version": source.harness_version,
        "applicability": applicability,
        "category_id": source.category_id,
        "profile_id": source.profile_id,
        "category_constitution_version": source.category_constitution_version,
        "grammar_family": source.requested_grammar_family,
        "spatial_grammar": dimensions[0].canonical_dict(),
        "temporal_grammar": dimensions[1].canonical_dict(),
        "reading_order": dimensions[2].canonical_dict(),
        "character_performance_grammar": dimensions[3].canonical_dict(),
        "conversational_turn_structure": dimensions[4].canonical_dict(),
        "wrong_reading_locks": list(locks),
        "semantic_lineage": [ref.canonical_dict() for ref in lineage],
        "runtime_law": ACTIVATION_FIRST,
        "development_law": VISUAL_SYNTAX_FIRST,
        "maturity_status": MATURITY_STATUS,
        "evidence_gate": "BD-007:EVIDENCE_PENDING",
        "production_ready": False,
        "certified": False,
    }
    canonical_bytes = _canonical_json(content)
    digest = sha256(canonical_bytes).hexdigest()
    return CategoryNativeSyntax(
        syntax_id=f"category-native-syntax_{digest}",
        version="1.0.0",
        harness_id=source.harness_id,
        harness_version=source.harness_version,
        applicability=applicability,
        category_id=source.category_id,
        profile_id=source.profile_id,
        category_constitution_version=source.category_constitution_version,
        grammar_family=source.requested_grammar_family,
        spatial_grammar=dimensions[0],
        temporal_grammar=dimensions[1],
        reading_order=dimensions[2],
        character_performance_grammar=dimensions[3],
        conversational_turn_structure=dimensions[4],
        wrong_reading_locks=locks,
        semantic_lineage=lineage,
        runtime_law=ACTIVATION_FIRST,
        development_law=VISUAL_SYNTAX_FIRST,
        maturity_status=MATURITY_STATUS,
        evidence_gate="BD-007:EVIDENCE_PENDING",
        production_ready=False,
        certified=False,
        syntax_hash=f"sha256:{digest}",
        canonical_bytes=canonical_bytes,
    )


def _build_sequence(
    source: CategorySyntaxInput,
    syntax: CategoryNativeSyntax,
    lineage: tuple[GovernedRef, ...],
    locks: tuple[str, ...],
) -> ActivativeSequenceProgram:
    applicability = "REQUIRED" if source.mode == "activative" else NOT_APPLICABLE
    content: dict[str, object] = {
        "schema_version": "cmf-builder-activative-sequence-program/v1",
        "version": "1.0.0",
        "harness_id": source.harness_id,
        "harness_version": source.harness_version,
        "applicability": applicability,
        "shared_core_ref": _optional_ref(source.shared_activative_core_ref),
        "category_syntax_ref": syntax.syntax_hash,
        "activation_direction": source.activation_direction,
        "participant_role": source.participant_role,
        "states": list(source.states),
        "transitions": list(source.transitions),
        "pacing": source.pacing,
        "sonic_or_silence_function": source.sonic_or_silence_function,
        "payoff": source.payoff,
        "intended_reaction": source.intended_reaction,
        "micro_commitment": source.micro_commitment,
        "wrong_reading_locks": list(locks),
        "semantic_lineage": [ref.canonical_dict() for ref in lineage],
        "runtime_law": ACTIVATION_FIRST,
        "development_law": VISUAL_SYNTAX_FIRST,
        "maturity_status": MATURITY_STATUS,
        "evidence_gate": "BD-007:EVIDENCE_PENDING",
        "production_ready": False,
        "certified": False,
    }
    canonical_bytes = _canonical_json(content)
    digest = sha256(canonical_bytes).hexdigest()
    return ActivativeSequenceProgram(
        sequence_id=f"activative-sequence-program_{digest}",
        version="1.0.0",
        harness_id=source.harness_id,
        harness_version=source.harness_version,
        applicability=applicability,
        shared_core_ref=source.shared_activative_core_ref,
        category_syntax_ref=syntax.syntax_hash,
        activation_direction=source.activation_direction,
        participant_role=source.participant_role,
        states=source.states,
        transitions=source.transitions,
        pacing=source.pacing,
        sonic_or_silence_function=source.sonic_or_silence_function,
        payoff=source.payoff,
        intended_reaction=source.intended_reaction,
        micro_commitment=source.micro_commitment,
        wrong_reading_locks=locks,
        semantic_lineage=lineage,
        runtime_law=ACTIVATION_FIRST,
        development_law=VISUAL_SYNTAX_FIRST,
        maturity_status=MATURITY_STATUS,
        evidence_gate="BD-007:EVIDENCE_PENDING",
        production_ready=False,
        certified=False,
        sequence_hash=f"sha256:{digest}",
        canonical_bytes=canonical_bytes,
    )


def _complete_lineage(source: CategorySyntaxInput) -> tuple[GovernedRef, ...]:
    refs = (
        (source.category_binding_ref,)
        + (source.structural_profile_ref,)
        + (source.shared_activative_core_ref,)
        + source.evidence_refs
        + source.rich_source_object_refs
        + source.authority_refs
    )
    complete = tuple(ref for ref in refs if ref is not None)
    keys = [
        (ref.lineage_role, ref.object_id, ref.version, ref.sha256, ref.authority)
        for ref in complete
    ]
    if len(set(keys)) != len(keys):
        raise CategorySyntaxError("Semantic lineage contains duplicate references.")
    return tuple(sorted(complete, key=lambda ref: (
        ref.lineage_role,
        ref.object_id,
        ref.version,
        ref.sha256,
        ref.authority,
    )))


def _canonical_refs(refs: tuple[GovernedRef, ...]) -> list[dict[str, str]]:
    return [
        ref.canonical_dict()
        for ref in sorted(
            refs,
            key=lambda item: (
                item.lineage_role,
                item.object_id,
                item.version,
                item.sha256,
                item.authority,
            ),
        )
    ]


def _optional_ref(ref: GovernedRef | None) -> dict[str, str] | None:
    return None if ref is None else ref.canonical_dict()


def _require_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CategorySyntaxError(f"{field} must be a non-empty string.")
    return value.strip()


def _require_unique_texts(value: tuple[str, ...], field: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or not value:
        raise CategorySyntaxError(f"{field} must be a non-empty tuple.")
    normalized = tuple(_require_text(item, field) for item in value)
    if len(set(normalized)) != len(normalized):
        raise CategorySyntaxError(f"{field} contains duplicates.")
    return normalized


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
