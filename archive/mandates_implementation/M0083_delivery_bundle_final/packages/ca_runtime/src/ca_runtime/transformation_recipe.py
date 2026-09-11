"""M0083 deterministic TransformationIntent -> TransformationRecipe compiler.

This module is intentionally narrow.  It does not own semantic meaning,
retrieval, asset identity, geometry, runtime execution, or operator promotion.
It resolves a typed TransformationIntent to a small, immutable-in-code registry
of approved primitive sequences and motion/keyframe templates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence

from ca_contracts import canonical_sha256
from ca_runtime.storyboard_session import (
    TRANSFORMATION_INTENTS,
    TRANSFORMATION_MOTIONS,
    TRANSFORMATION_MODES,
    TRANSFORMATION_SOURCE_QUALITIES,
    TRANSFORMATION_SOURCE_ROLES,
    TransformationIntent,
    TransformationRecipe,
)


TRANSFORMATION_RECIPE_REGISTRY_VERSION = "M0083-1"


class TransformationCompilationError(ValueError):
    """Base fail-closed error for transformation recipe compilation."""


class TransformationRecipeNotFoundError(TransformationCompilationError):
    """Raised when an intent has no governed recipe registration."""


class TransformationAuthorizationError(TransformationCompilationError):
    """Raised when an otherwise-valid recipe is not authorized for the caller."""


class StaleTransformationRecipeRegistryError(TransformationCompilationError):
    """Raised when compilation targets a registry version other than the current one."""


class TransformationModeMismatchError(TransformationCompilationError):
    """Raised when a plausible mode is not approved for the declared intent."""


class TransformationConstraintError(TransformationCompilationError):
    """Raised when a declared constraint is malformed or outside bounded policy."""


class SourceQualityRequiredError(TransformationCompilationError):
    """Raised before motion/scale can be applied without source-quality evidence."""


@dataclass(frozen=True)
class TransformationRecipeTemplate:
    """Small registry entry describing one approved recipe shape."""

    template_id: str
    intents: frozenset[str]
    allowed_modes: frozenset[str]
    primitive_ops: tuple[str, ...]
    default_motion: str
    keyframe_template: str
    scale_delta_bps_high: int = 0
    scale_delta_bps_medium: int = 0


_APPROVED_PRIMITIVES = frozenset(
    {
        "EXTRACT_REGION",
        "REFRAME",
        "HIGHLIGHT",
        "SIDE_BY_SIDE",
        "ANNOTATE",
        "INSET",
        "CONNECTOR",
        "MASK_REGION",
        "CUT",
        "RETURN",
        "HOLD",
    }
)

_TEMPLATES: tuple[TransformationRecipeTemplate, ...] = (
    TransformationRecipeTemplate(
        template_id="REVEAL_TARGET_V1",
        intents=frozenset({"REVEAL", "PROVE"}),
        allowed_modes=frozenset({"AUTO", "EXTRACT_REGION"}),
        primitive_ops=("EXTRACT_REGION", "HIGHLIGHT"),
        default_motion="SUBTLE_ZOOM",
        keyframe_template="SUBTLE_ZOOM_IN",
        scale_delta_bps_high=800,
        scale_delta_bps_medium=500,
    ),
    TransformationRecipeTemplate(
        template_id="FOCUS_TARGET_V1",
        intents=frozenset({"FOCUS", "ESCALATE"}),
        allowed_modes=frozenset({"AUTO", "REFRAME"}),
        primitive_ops=("REFRAME", "HIGHLIGHT"),
        default_motion="SUBTLE_ZOOM",
        keyframe_template="SUBTLE_ZOOM_IN",
        scale_delta_bps_high=700,
        scale_delta_bps_medium=400,
    ),
    TransformationRecipeTemplate(
        template_id="CONTRAST_SOURCES_V1",
        intents=frozenset({"CONTRAST"}),
        allowed_modes=frozenset({"AUTO", "COMPARE"}),
        primitive_ops=("SIDE_BY_SIDE", "HIGHLIGHT"),
        default_motion="STATIC",
        keyframe_template="STATIC_HOLD",
    ),
    TransformationRecipeTemplate(
        template_id="EXPLAIN_TARGET_V1",
        intents=frozenset({"EXPLAIN"}),
        allowed_modes=frozenset({"AUTO", "ANNOTATE"}),
        primitive_ops=("EXTRACT_REGION", "ANNOTATE"),
        default_motion="STATIC",
        keyframe_template="STATIC_HOLD",
    ),
    TransformationRecipeTemplate(
        template_id="CONNECT_CONTEXT_V1",
        intents=frozenset({"CONNECT"}),
        allowed_modes=frozenset({"AUTO", "INSET"}),
        primitive_ops=("INSET", "CONNECTOR"),
        default_motion="STATIC",
        keyframe_template="STATIC_HOLD",
    ),
    TransformationRecipeTemplate(
        template_id="WITHHOLD_REGION_V1",
        intents=frozenset({"WITHHOLD"}),
        allowed_modes=frozenset({"AUTO", "PROTECT"}),
        primitive_ops=("MASK_REGION",),
        default_motion="STATIC",
        keyframe_template="STATIC_HOLD",
    ),
    TransformationRecipeTemplate(
        template_id="INTERRUPT_CUT_V1",
        intents=frozenset({"INTERRUPT"}),
        allowed_modes=frozenset({"AUTO", "CUT"}),
        primitive_ops=("CUT", "HOLD"),
        default_motion="STATIC",
        keyframe_template="STATIC_HOLD",
    ),
    TransformationRecipeTemplate(
        template_id="RESOLVE_RETURN_V1",
        intents=frozenset({"RESOLVE"}),
        allowed_modes=frozenset({"AUTO", "RETURN"}),
        primitive_ops=("RETURN", "HOLD"),
        default_motion="RETURN",
        keyframe_template="RETURN_TO_SOURCE",
    ),
)

_TEMPLATE_BY_INTENT: dict[str, TransformationRecipeTemplate] = {
    intent: template
    for template in _TEMPLATES
    for intent in template.intents
}


def _validate_constraints(constraints: Mapping[str, Any]) -> dict[str, Any]:
    allowed = {
        "source_quality",
        "source_role",
        "allow_motion",
        "max_scale_change_bps",
        "max_motion_amplitude_bps",
    }
    unknown = sorted(set(constraints) - allowed)
    if unknown:
        raise TransformationConstraintError(
            f"unsupported transformation constraints: {', '.join(unknown)}"
        )

    normalized = dict(constraints)
    if "source_quality" in normalized:
        quality = str(normalized["source_quality"]).upper()
        if quality not in TRANSFORMATION_SOURCE_QUALITIES:
            raise TransformationConstraintError(
                f"unsupported source_quality: {normalized['source_quality']}"
            )
        normalized["source_quality"] = quality
    if "source_role" in normalized:
        role = str(normalized["source_role"]).upper()
        if role not in TRANSFORMATION_SOURCE_ROLES:
            raise TransformationConstraintError(
                f"unsupported source_role: {normalized['source_role']}"
            )
        normalized["source_role"] = role
    if "allow_motion" in normalized and not isinstance(normalized["allow_motion"], bool):
        raise TransformationConstraintError("allow_motion must be boolean")
    for key in ("max_scale_change_bps", "max_motion_amplitude_bps"):
        if key in normalized:
            value = normalized[key]
            if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > 2000:
                raise TransformationConstraintError(
                    f"{key} must be an integer in [0, 2000]"
                )
    return normalized


def _keyframes(*, template: str, scale_delta_bps: int = 0) -> list[dict[str, Any]]:
    if template == "STATIC_HOLD":
        return [
            {"at_bps": 0, "template": "HOLD"},
            {"at_bps": 10000, "template": "HOLD"},
        ]
    if template == "SUBTLE_ZOOM_IN":
        return [
            {"at_bps": 0, "template": "SCALE", "scale_bps": 10000},
            {
                "at_bps": 10000,
                "template": "SCALE",
                "scale_bps": 10000 + scale_delta_bps,
            },
        ]
    if template == "RETURN_TO_SOURCE":
        return [
            {"at_bps": 0, "template": "RETURN", "progress_bps": 0},
            {"at_bps": 10000, "template": "RETURN", "progress_bps": 10000},
        ]
    raise TransformationCompilationError(f"unknown keyframe template: {template}")


class TransformationRecipeRegistry:
    """Immutable-in-code registry of M0083 approved recipe templates."""

    def __init__(self, version: str = TRANSFORMATION_RECIPE_REGISTRY_VERSION) -> None:
        self.version = version
        self._templates = dict(_TEMPLATE_BY_INTENT)
        if set(self._templates) != set(TRANSFORMATION_INTENTS):
            missing = sorted(set(TRANSFORMATION_INTENTS) - set(self._templates))
            raise RuntimeError(f"recipe registry missing intents: {missing}")
        for template in self._templates.values():
            if not template.primitive_ops or not set(template.primitive_ops).issubset(_APPROVED_PRIMITIVES):
                raise RuntimeError(f"recipe template contains unapproved primitive: {template.template_id}")
            if not set(template.allowed_modes).issubset(TRANSFORMATION_MODES):
                raise RuntimeError(f"recipe template contains unapproved mode: {template.template_id}")
            if template.default_motion not in TRANSFORMATION_MOTIONS:
                raise RuntimeError(f"recipe template contains unapproved motion: {template.template_id}")

    def resolve(self, intent: str) -> TransformationRecipeTemplate:
        try:
            return self._templates[intent]
        except KeyError as exc:
            raise TransformationRecipeNotFoundError(
                f"no governed transformation recipe registered for intent '{intent}'"
            ) from exc


class TransformationRecipeCompiler:
    """Compile TransformationIntent into deterministic, bounded recipe data."""

    def __init__(self, registry: Optional[TransformationRecipeRegistry] = None) -> None:
        self.registry = registry or TransformationRecipeRegistry()

    def compile(
        self,
        intent: TransformationIntent,
        *,
        authorized_recipe_ids: Optional[Sequence[str]] = None,
        expected_registry_version: Optional[str] = None,
    ) -> TransformationRecipe:
        if expected_registry_version is not None and expected_registry_version != self.registry.version:
            raise StaleTransformationRecipeRegistryError(
                f"stale transformation recipe registry: expected {expected_registry_version}, current {self.registry.version}"
            )

        template = self.registry.resolve(intent.intent)
        if intent.mode not in template.allowed_modes:
            raise TransformationModeMismatchError(
                f"mode '{intent.mode}' is not approved for intent '{intent.intent}'"
            )
        if authorized_recipe_ids is not None and template.template_id not in set(authorized_recipe_ids):
            raise TransformationAuthorizationError(
                f"recipe template '{template.template_id}' is not authorized"
            )

        normalized_constraints = _validate_constraints(intent.constraints)
        source_quality = normalized_constraints.get("source_quality")
        allow_motion = normalized_constraints.get("allow_motion", True)
        requested_motion = intent.motion if intent.motion != "STATIC" else template.default_motion
        if not allow_motion:
            requested_motion = "STATIC"

        if requested_motion != "STATIC" and source_quality in {None, "UNKNOWN"}:
            raise SourceQualityRequiredError(
                "source_quality must be explicit before non-static transformation motion is compiled"
            )

        if requested_motion not in TRANSFORMATION_MOTIONS:
            raise TransformationCompilationError(
                f"motion '{requested_motion}' is not registered"
            )

        scale_delta_bps = 0
        keyframe_template = "STATIC_HOLD"
        if requested_motion == "SUBTLE_ZOOM":
            if source_quality == "HIGH":
                scale_delta_bps = template.scale_delta_bps_high
            elif source_quality == "MEDIUM":
                scale_delta_bps = template.scale_delta_bps_medium
            else:
                # LOW/DEGRADED material keeps source quality from becoming the
                # dominant perceptual event: suppress zoom deterministically.
                scale_delta_bps = 0
            keyframe_template = "SUBTLE_ZOOM_IN" if scale_delta_bps else "STATIC_HOLD"
        elif requested_motion == "RETURN":
            keyframe_template = "RETURN_TO_SOURCE"
        elif requested_motion == "SUBTLE_PAN":
            # No geometry is invented here; M0083 exposes the primitive/motion
            # boundary only and leaves exact position solving downstream.
            keyframe_template = "STATIC_HOLD"
        else:
            keyframe_template = template.keyframe_template

        if "max_scale_change_bps" in normalized_constraints:
            scale_delta_bps = min(scale_delta_bps, normalized_constraints["max_scale_change_bps"])
            if scale_delta_bps == 0 and requested_motion == "SUBTLE_ZOOM":
                keyframe_template = "STATIC_HOLD"

        primitive_payload = [
            {"op": op, "target": "intent_target"}
            for op in template.primitive_ops
        ]
        keyframe_payload = _keyframes(
            template=keyframe_template,
            scale_delta_bps=scale_delta_bps,
        )
        effective_constraints = {
            **normalized_constraints,
            "effective_motion": "STATIC" if keyframe_template == "STATIC_HOLD" else requested_motion,
        }

        identity_payload = {
            "registry_version": self.registry.version,
            "template_id": template.template_id,
            "intent_id": intent.intent_id,
            "intent": intent.intent,
            "source": intent.source,
            "semantic_target": intent.semantic_target,
            "mode": intent.mode,
            "emphasis": intent.emphasis,
            "motion": requested_motion,
            "constraints": effective_constraints,
            "primitives": primitive_payload,
            "keyframes": keyframe_payload,
        }
        digest = canonical_sha256(identity_payload)
        recipe_id = f"recipe_{digest[:20]}"
        return TransformationRecipe(
            recipe_id=recipe_id,
            intent_id=intent.intent_id,
            primitives=primitive_payload,
            keyframes=keyframe_payload,
            constraints=effective_constraints,
            template_id=template.template_id,
            registry_version=self.registry.version,
            motion_template=keyframe_template,
            governed=True,
            recipe_sha256=digest,
        )


def compile_transformation_intent(
    intent: TransformationIntent,
    *,
    authorized_recipe_ids: Optional[Sequence[str]] = None,
    expected_registry_version: Optional[str] = None,
) -> TransformationRecipe:
    """Convenience entrypoint for deterministic M0083 compilation."""
    return TransformationRecipeCompiler().compile(
        intent,
        authorized_recipe_ids=authorized_recipe_ids,
        expected_registry_version=expected_registry_version,
    )


__all__ = [
    "TRANSFORMATION_RECIPE_REGISTRY_VERSION",
    "TransformationCompilationError",
    "TransformationRecipeNotFoundError",
    "TransformationAuthorizationError",
    "StaleTransformationRecipeRegistryError",
    "TransformationModeMismatchError",
    "TransformationConstraintError",
    "SourceQualityRequiredError",
    "TransformationRecipeTemplate",
    "TransformationRecipeRegistry",
    "TransformationRecipeCompiler",
    "compile_transformation_intent",
]
