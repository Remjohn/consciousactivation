"""M0082 deterministic Editorial Expression Calculus.

This is a pure, bounded projection from editorial grammar to fixed-point
expression values. It owns neither semantic meaning nor rendering execution.
"""

from __future__ import annotations

from typing import ClassVar, Dict, Iterable, Mapping, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ca_contracts import canonical_sha256


class EditorialExpressionProfileError(ValueError):
    """Raised when a format/scene profile is not governed."""


class EditorialExpressionBounds(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    minimum: int
    maximum: int

    @field_validator("minimum", "maximum")
    @classmethod
    def non_negative(cls, value: int) -> int:
        if isinstance(value, bool) or value < 0:
            raise ValueError("bounds must be non-negative integers")
        return value

    @field_validator("maximum")
    @classmethod
    def ordered(cls, value: int, info) -> int:
        minimum = info.data.get("minimum")
        if minimum is not None and value < minimum:
            raise ValueError("maximum must be at least minimum")
        return value


class NarrativeEditingGrammar(BaseModel):
    """Bounded structural grammar consumed by the calculus."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    format_id: str
    scene_kind: str
    rhythm: str = "STEADY"
    attention: str = "FOCUS"
    information: str = "PROVE"
    texture: str = "CLEAN"
    captioning: str = "SUPPORTIVE"
    source_evidence_refs: Tuple[str, ...]
    source_quality: str

    _FORMATS: ClassVar[frozenset[str]] = frozenset(
        {"VIDEO", "CAROUSEL", "SUPERVISUAL", "PRESENTATION"}
    )
    _SCENES: ClassVar[frozenset[str]] = frozenset(
        {"OPENING", "EXPOSITION", "EVIDENCE", "PIVOT", "CLIMAX", "RESOLUTION"}
    )
    _RHYTHMS: ClassVar[frozenset[str]] = frozenset(
        {"HOLD", "STEADY", "PUNCTUATED", "ACCELERATE"}
    )
    _ATTENTION: ClassVar[frozenset[str]] = frozenset(
        {"QUIET", "FOCUS", "EMPHATIC", "INTERRUPT"}
    )
    _INFORMATION: ClassVar[frozenset[str]] = frozenset(
        {"WITHHOLD", "REVEAL", "PROVE", "CONNECT", "RESOLVE"}
    )
    _TEXTURES: ClassVar[frozenset[str]] = frozenset({"CLEAN", "LAYERED", "DENSE"})
    _CAPTIONING: ClassVar[frozenset[str]] = frozenset(
        {"NONE", "SPARSE", "SUPPORTIVE", "EXPLANATORY"}
    )
    _QUALITY: ClassVar[frozenset[str]] = frozenset({"AUDITED", "HIGH", "VERIFIED"})

    @field_validator("format_id", "scene_kind", "rhythm", "attention", "information", "texture", "captioning", "source_quality")
    @classmethod
    def normalize_vocab(cls, value: str, info) -> str:
        normalized = value.upper()
        allowed = {
            "format_id": cls._FORMATS,
            "scene_kind": cls._SCENES,
            "rhythm": cls._RHYTHMS,
            "attention": cls._ATTENTION,
            "information": cls._INFORMATION,
            "texture": cls._TEXTURES,
            "captioning": cls._CAPTIONING,
            "source_quality": cls._QUALITY,
        }[info.field_name]
        if normalized not in allowed:
            if info.field_name == "source_quality":
                raise ValueError("source_quality must be one of AUDITED, HIGH, VERIFIED")
            raise ValueError(f"{info.field_name} must be one of {sorted(allowed)}")
        return normalized

    @field_validator("source_evidence_refs")
    @classmethod
    def validate_evidence_refs(cls, value: Tuple[str, ...]) -> Tuple[str, ...]:
        refs = tuple(str(item).strip() for item in value)
        if not refs or any(not item for item in refs):
            raise ValueError("source_evidence_refs must contain at least one non-empty reference")
        if len(refs) != len(set(refs)):
            raise ValueError("source_evidence_refs must be unique")
        return refs


class EditorialExpression(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    profile_id: str
    source_evidence_refs: Tuple[str, ...]
    source_quality: str
    pace_bps: int
    shot_duration_ms: int
    hold_duration_ms: int
    cut_interval_ms: int
    occupancy_bps: int
    scale_bps: int
    motion_amplitude_bps: int
    motion_velocity_bps_per_second: int
    visual_density_bps: int
    caption_density_bps: int
    contrast_bps: int
    salience_bps: int
    intervention_frequency_per_minute: int
    canonical_sha256: str


class EditorialExpressionProfile(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    profile_id: str
    shot_duration_ms: EditorialExpressionBounds
    hold_duration_ms: EditorialExpressionBounds
    occupancy_bps: EditorialExpressionBounds
    scale_bps: EditorialExpressionBounds
    motion_amplitude_bps: EditorialExpressionBounds
    motion_velocity_bps_per_second: EditorialExpressionBounds
    visual_density_bps: EditorialExpressionBounds
    caption_density_bps: EditorialExpressionBounds
    contrast_bps: EditorialExpressionBounds
    salience_bps: EditorialExpressionBounds
    intervention_frequency_per_minute: EditorialExpressionBounds


_FORMAT_BASE: Mapping[str, Mapping[str, int]] = {
    "VIDEO": {"pace": 5600, "occupancy": 7000, "scale": 10000, "motion": 700, "density": 5700, "caption": 4200, "contrast": 5200, "salience": 6000, "intervention": 5},
    "CAROUSEL": {"pace": 4200, "occupancy": 6200, "scale": 9800, "motion": 350, "density": 6100, "caption": 5000, "contrast": 5600, "salience": 5900, "intervention": 4},
    "SUPERVISUAL": {"pace": 5000, "occupancy": 7800, "scale": 10200, "motion": 850, "density": 7000, "caption": 3000, "contrast": 6200, "salience": 6600, "intervention": 5},
    "PRESENTATION": {"pace": 3300, "occupancy": 5600, "scale": 9600, "motion": 220, "density": 4300, "caption": 6200, "contrast": 4800, "salience": 5400, "intervention": 3},
}
_SCENE_BIAS: Mapping[str, Mapping[str, int]] = {
    "OPENING": {"pace": -300, "salience": 100, "contrast": 0},
    "EXPOSITION": {"pace": -100, "salience": 0, "contrast": 0},
    "EVIDENCE": {"pace": 0, "salience": 450, "contrast": 250},
    "PIVOT": {"pace": 550, "salience": 700, "contrast": 500},
    "CLIMAX": {"pace": 900, "salience": 950, "contrast": 700},
    "RESOLUTION": {"pace": -650, "salience": 250, "contrast": -150},
}
_PROFILE_FIELDS = (
    "shot_duration_ms", "hold_duration_ms", "occupancy_bps", "scale_bps",
    "motion_amplitude_bps", "motion_velocity_bps_per_second",
    "visual_density_bps", "caption_density_bps", "contrast_bps", "salience_bps",
    "intervention_frequency_per_minute",
)


def _bounds_for(format_id: str, scene_kind: str) -> EditorialExpressionProfile:
    profile_id = f"M0082:{format_id}:{scene_kind}"
    pace = _FORMAT_BASE[format_id]["pace"] + _SCENE_BIAS[scene_kind]["pace"]
    duration = max(500, 6200 - pace // 2)
    hold = max(250, duration * 3 // 4)
    return EditorialExpressionProfile(
        profile_id=profile_id,
        shot_duration_ms=EditorialExpressionBounds(minimum=max(300, duration - 2200), maximum=duration + 2200),
        hold_duration_ms=EditorialExpressionBounds(minimum=max(150, hold - 1800), maximum=hold + 1800),
        occupancy_bps=EditorialExpressionBounds(minimum=3500, maximum=9800),
        scale_bps=EditorialExpressionBounds(minimum=7000, maximum=12000),
        motion_amplitude_bps=EditorialExpressionBounds(minimum=0, maximum=2200),
        motion_velocity_bps_per_second=EditorialExpressionBounds(minimum=0, maximum=20000),
        visual_density_bps=EditorialExpressionBounds(minimum=1800, maximum=9800),
        caption_density_bps=EditorialExpressionBounds(minimum=0, maximum=9800),
        contrast_bps=EditorialExpressionBounds(minimum=1000, maximum=9800),
        salience_bps=EditorialExpressionBounds(minimum=1000, maximum=9800),
        intervention_frequency_per_minute=EditorialExpressionBounds(minimum=0, maximum=12),
    )


_PROFILES = {
    (format_id, scene_kind): _bounds_for(format_id, scene_kind)
    for format_id in _FORMAT_BASE
    for scene_kind in NarrativeEditingGrammar._SCENES
}


def get_editorial_expression_profile(format_id: str, scene_kind: str) -> EditorialExpressionProfile:
    key = (str(format_id).upper(), str(scene_kind).upper())
    try:
        return _PROFILES[key]
    except KeyError as exc:
        raise EditorialExpressionProfileError(
            f"no editorial expression profile for format '{format_id}' and scene '{scene_kind}'"
        ) from exc


def _clamp(value: int, bounds: EditorialExpressionBounds) -> int:
    return max(bounds.minimum, min(bounds.maximum, int(value)))


def _interpolate_inverse(pace: int, minimum: int, maximum: int) -> int:
    # 0..10000 pace range maps to max..min duration without floats.
    return maximum - ((maximum - minimum) * pace // 10000)


def compile_editorial_expression(grammar: NarrativeEditingGrammar) -> EditorialExpression:
    profile = get_editorial_expression_profile(grammar.format_id, grammar.scene_kind)
    base = dict(_FORMAT_BASE[grammar.format_id])
    base.update({key: base.get(key, 0) + value for key, value in _SCENE_BIAS[grammar.scene_kind].items()})

    rhythm = {"HOLD": -1400, "STEADY": 0, "PUNCTUATED": 650, "ACCELERATE": 1900}[grammar.rhythm]
    attention = {"QUIET": -500, "FOCUS": 250, "EMPHATIC": 700, "INTERRUPT": 1100}[grammar.attention]
    information = {"WITHHOLD": -350, "REVEAL": 200, "PROVE": 400, "CONNECT": 0, "RESOLVE": -150}[grammar.information]
    texture = {"CLEAN": -300, "LAYERED": 350, "DENSE": 700}[grammar.texture]
    captions = {"NONE": -700, "SPARSE": -150, "SUPPORTIVE": 350, "EXPLANATORY": 700}[grammar.captioning]
    pace = _clamp(base["pace"] + rhythm + attention // 2 + information // 3, EditorialExpressionBounds(minimum=0, maximum=10000))

    duration_bounds = profile.shot_duration_ms
    shot_duration = _clamp(_interpolate_inverse(pace, duration_bounds.minimum, duration_bounds.maximum), duration_bounds)
    hold_base = shot_duration * 3 // 4
    hold_duration = _clamp(hold_base + (500 if grammar.rhythm == "HOLD" else 0) - pace // 30, profile.hold_duration_ms)
    scale = _clamp(base["scale"] + attention // 2 + (150 if grammar.information in {"PROVE", "REVEAL"} else 0), profile.scale_bps)
    occupancy = _clamp(base["occupancy"] + attention + texture, profile.occupancy_bps)
    motion = _clamp(base["motion"] + rhythm // 2 + attention // 2, profile.motion_amplitude_bps)
    velocity = _clamp(motion * 6 + pace // 2, profile.motion_velocity_bps_per_second)
    visual_density = _clamp(base["density"] + texture + attention // 2, profile.visual_density_bps)
    caption_density = _clamp(base["caption"] + captions, profile.caption_density_bps)
    contrast = _clamp(base["contrast"] + _SCENE_BIAS[grammar.scene_kind]["contrast"] + attention // 2, profile.contrast_bps)
    salience = _clamp(base["salience"] + _SCENE_BIAS[grammar.scene_kind]["salience"] + attention + information, profile.salience_bps)
    intervention = _clamp(base["intervention"] + (rhythm // 450) + (attention // 500), profile.intervention_frequency_per_minute)

    payload = {
        "profile_id": profile.profile_id,
        "source_evidence_refs": grammar.source_evidence_refs,
        "source_quality": grammar.source_quality,
        "pace_bps": pace,
        "shot_duration_ms": shot_duration,
        "hold_duration_ms": hold_duration,
        "cut_interval_ms": shot_duration,
        "occupancy_bps": occupancy,
        "scale_bps": scale,
        "motion_amplitude_bps": motion,
        "motion_velocity_bps_per_second": velocity,
        "visual_density_bps": visual_density,
        "caption_density_bps": caption_density,
        "contrast_bps": contrast,
        "salience_bps": salience,
        "intervention_frequency_per_minute": intervention,
    }
    digest = canonical_sha256(payload)
    return EditorialExpression(**payload, canonical_sha256=digest)


__all__ = [
    "EditorialExpression",
    "EditorialExpressionBounds",
    "EditorialExpressionProfile",
    "EditorialExpressionProfileError",
    "NarrativeEditingGrammar",
    "compile_editorial_expression",
    "get_editorial_expression_profile",
]
