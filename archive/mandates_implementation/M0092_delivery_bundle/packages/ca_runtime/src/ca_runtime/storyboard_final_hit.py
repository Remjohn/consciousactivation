"""M0092 final-hit storyboard validation and MotionPlan compilation.

The module is deliberately a projection layer. It validates an existing
StoryboardRevision and deterministically compiles MotionPlan/Keyframe data; it
does not become a semantic, retrieval, Design System, VAE, or runtime authority.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from pydantic import BaseModel, Field, validator

from ca_contracts import canonical_sha256
from ca_runtime.narrative_editing_grammar import NarrativeEditingGrammarRegistry
from ca_runtime.storyboard_programs import (
    StoryboardProgramAuthorityError,
    StoryboardProgramValidationError,
    get_storyboard_program,
)
from ca_runtime.storyboard_session import (
    Keyframe,
    MotionPlan,
    SourceQualityProfile,
    StoryboardElement,
    StoryboardRevision,
    StoryboardScene,
    StoryboardShot,
    TRANSFORMATION_MOTIONS,
    TransformationIntent,
    TransformationRecipe,
    validate_transformation_for_source_quality,
)


class FinalHitValidationError(ValueError):
    """Base fail-closed final-hit validation error."""


class FinalHitMotionCompilationError(FinalHitValidationError):
    """Motion/keyframe source cannot be compiled deterministically."""


class DesignSystemValidationError(FinalHitValidationError):
    """A Design System reference or binding is malformed or inconsistent."""


class HarnessConstraintValidationError(FinalHitValidationError):
    """Harness constraints are missing, unknown, or out of bounds."""


class MotionPlanCompilation(BaseModel):
    """One deterministic final-hit MotionPlan plus its compilation digest."""

    element_id: str
    motion_plan: MotionPlan
    compilation_sha256: str


class FinalHitValidationResult(BaseModel):
    """Deterministic validation result; perceptual acceptance remains operator-owned."""

    passed: bool
    strict: bool
    format_id: Optional[str] = None
    checks: Dict[str, str] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    motion_plan_compilations: List[MotionPlanCompilation] = Field(default_factory=list)
    validation_sha256: str
    operator_judgment_required: bool = True


_VALID_INTENSITY_MAX_BPS = 2000
_ALLOWED_HARNESS_KEYS = frozenset(
    {
        "max_motion_intensity_bps",
        "max_attention_cost_bps",
        "max_keyframes",
        "min_legibility_bps",
        "safe_area",
        "require_design_system",
        "require_wrong_reading_locks",
    }
)
_ALLOWED_TEMPLATES = frozenset({"HOLD", "SCALE", "RETURN"})
_HEADING_WORDS = re.compile(r"[^a-z0-9]+")


def _tokens(value: str) -> set[str]:
    return {token for token in _HEADING_WORDS.split(value.lower()) if len(token) >= 4}


def _canonical_ref(value: Mapping[str, Any], field: str) -> Dict[str, str]:
    required = {"object_id", "version", "sha256"}
    if set(value) != required:
        raise DesignSystemValidationError(
            f"{field} must contain exactly object_id, version, sha256"
        )
    object_id = str(value["object_id"]).strip()
    version = str(value["version"]).strip()
    digest = str(value["sha256"]).strip()
    if not object_id or not version or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise DesignSystemValidationError(f"{field} is not a valid canonical reference")
    return {"object_id": object_id, "version": version, "sha256": digest}


def _safe_area_from_constraints(constraints: Mapping[str, Any]) -> Optional[Mapping[str, int]]:
    value = constraints.get("safe_area")
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise HarnessConstraintValidationError("safe_area must be a mapping")
    required = {"x_bps", "y_bps", "width_bps", "height_bps"}
    if set(value) != required:
        raise HarnessConstraintValidationError(
            "safe_area must contain x_bps, y_bps, width_bps, height_bps"
        )
    clean: Dict[str, int] = {}
    for key in required:
        raw = value[key]
        if isinstance(raw, bool) or not isinstance(raw, int):
            raise HarnessConstraintValidationError(f"safe_area.{key} must be an integer")
        if raw < 0 or raw > 10000:
            raise HarnessConstraintValidationError(f"safe_area.{key} must be in [0, 10000]")
        clean[key] = raw
    if clean["width_bps"] <= 0 or clean["height_bps"] <= 0:
        raise HarnessConstraintValidationError("safe_area must be visible")
    if clean["x_bps"] + clean["width_bps"] > 10000 or clean["y_bps"] + clean["height_bps"] > 10000:
        raise HarnessConstraintValidationError("safe_area exceeds normalized canvas")
    return clean


def _validate_harness_constraints(constraints: Mapping[str, Any], *, strict: bool) -> Dict[str, Any]:
    unknown = sorted(set(constraints) - _ALLOWED_HARNESS_KEYS)
    if unknown:
        raise HarnessConstraintValidationError(
            "unsupported storyboard harness constraints: " + ", ".join(unknown)
        )
    normalized = dict(constraints)
    for key in ("max_motion_intensity_bps", "max_attention_cost_bps", "min_legibility_bps"):
        if key in normalized:
            value = normalized[key]
            maximum = 10000 if key != "max_motion_intensity_bps" else _VALID_INTENSITY_MAX_BPS
            if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > maximum:
                raise HarnessConstraintValidationError(
                    f"{key} must be an integer in [0, {maximum}]"
                )
    if "max_keyframes" in normalized:
        value = normalized["max_keyframes"]
        if isinstance(value, bool) or not isinstance(value, int) or value < 2 or value > 32:
            raise HarnessConstraintValidationError("max_keyframes must be an integer in [2, 32]")
    if "require_design_system" in normalized and not isinstance(normalized["require_design_system"], bool):
        raise HarnessConstraintValidationError("require_design_system must be boolean")
    if "require_wrong_reading_locks" in normalized and not isinstance(normalized["require_wrong_reading_locks"], bool):
        raise HarnessConstraintValidationError("require_wrong_reading_locks must be boolean")
    _safe_area_from_constraints(normalized)
    if strict:
        for required in ("max_motion_intensity_bps", "max_attention_cost_bps", "safe_area"):
            if required not in normalized:
                raise HarnessConstraintValidationError(
                    f"strict final-hit validation requires harness constraint '{required}'"
                )
    return normalized


def _geometry_within_safe_area(geometry: Mapping[str, Any], safe_area: Mapping[str, int], field: str) -> None:
    required = {"x_bps", "y_bps", "width_bps", "height_bps"}
    if set(geometry) != required:
        raise FinalHitValidationError(f"{field} must contain x_bps, y_bps, width_bps, height_bps")
    values = {key: geometry[key] for key in required}
    if any(isinstance(value, bool) or not isinstance(value, int) for value in values.values()):
        raise FinalHitValidationError(f"{field} must use integer basis points")
    if any(value < 0 or value > 10000 for value in values.values()):
        raise FinalHitValidationError(f"{field} is outside normalized bounds")
    if values["width_bps"] <= 0 or values["height_bps"] <= 0:
        raise FinalHitValidationError(f"{field} must be visible")
    if values["x_bps"] + values["width_bps"] > 10000 or values["y_bps"] + values["height_bps"] > 10000:
        raise FinalHitValidationError(f"{field} exceeds canvas bounds")
    if (
        values["x_bps"] < safe_area["x_bps"]
        or values["y_bps"] < safe_area["y_bps"]
        or values["x_bps"] + values["width_bps"] > safe_area["x_bps"] + safe_area["width_bps"]
        or values["y_bps"] + values["height_bps"] > safe_area["y_bps"] + safe_area["height_bps"]
    ):
        raise FinalHitValidationError(f"{field} exceeds harness safe area")


def _element_source_quality(element: StoryboardElement) -> Optional[SourceQualityProfile]:
    profiles = [
        asset.source_quality_profile
        for asset in element.asset_references
        if asset.source_quality_profile is not None
    ]
    if not profiles:
        return None
    first = profiles[0]
    if any(profile.profile_id != first.profile_id for profile in profiles[1:]):
        raise FinalHitValidationError(
            f"element '{element.element_id}' binds multiple source-quality profiles"
        )
    return first


def _recipe_for_element(element: StoryboardElement) -> Optional[TransformationRecipe]:
    intent = element.transformation_intent
    recipe = element.transformation_recipe
    if intent is None:
        if recipe is not None:
            raise FinalHitMotionCompilationError(
                f"element '{element.element_id}' has a recipe without TransformationIntent"
            )
        return None
    if recipe is None:
        recipe = intent.compile()
    elif recipe.intent_id != intent.intent_id:
        raise FinalHitMotionCompilationError(
            f"element '{element.element_id}' recipe is detached from its TransformationIntent"
        )
    if not recipe.governed:
        recipe = intent.compile()
    return recipe


def _recipe_keyframe_to_model(raw: Mapping[str, Any], *, duration_ms: int, purpose: str) -> Keyframe:
    template = str(raw.get("template", "HOLD")).upper()
    if template not in _ALLOWED_TEMPLATES:
        raise FinalHitMotionCompilationError(f"unsupported keyframe template '{template}'")
    if "at_bps" in raw:
        at_bps = raw["at_bps"]
        if isinstance(at_bps, bool) or not isinstance(at_bps, int) or at_bps < 0 or at_bps > 10000:
            raise FinalHitMotionCompilationError("keyframe at_bps must be an integer in [0, 10000]")
        at_ms = (duration_ms * at_bps) // 10000
    elif "at_ms" in raw:
        at_ms = raw["at_ms"]
    else:
        raise FinalHitMotionCompilationError("keyframe requires at_bps or at_ms")
    payload: Dict[str, Any] = {
        "at_ms": at_ms,
        "template": template,
        "purpose": str(raw.get("purpose", purpose)).upper(),
    }
    if "scale_bps" in raw:
        payload["scale_bps"] = raw["scale_bps"]
    if "x_bps" in raw:
        payload["x_bps"] = raw["x_bps"]
    if "y_bps" in raw:
        payload["y_bps"] = raw["y_bps"]
    return Keyframe(**payload)


def _compile_motion_plan(
    element: StoryboardElement,
    *,
    shot_duration_ms: int,
    harness_constraints: Mapping[str, Any],
) -> Optional[MotionPlanCompilation]:
    recipe = _recipe_for_element(element)
    if recipe is None and element.motion_plan is None:
        return None

    if element.motion_plan is not None and recipe is None:
        plan = element.motion_plan
        _validate_motion_plan(plan, element_id=element.element_id, shot_duration_ms=shot_duration_ms, constraints=harness_constraints)
        payload = {"element_id": element.element_id, "motion_plan": plan.model_dump(mode="json")}
        return MotionPlanCompilation(
            element_id=element.element_id,
            motion_plan=plan,
            compilation_sha256=canonical_sha256(payload),
        )

    assert recipe is not None
    intent = element.transformation_intent
    assert intent is not None
    profile = _element_source_quality(element)
    effective_motion = str(recipe.constraints.get("effective_motion", intent.motion)).upper()
    if effective_motion not in TRANSFORMATION_MOTIONS:
        raise FinalHitMotionCompilationError(
            f"element '{element.element_id}' has unsupported effective motion '{effective_motion}'"
        )
    if effective_motion != "STATIC" and profile is None:
        raise FinalHitMotionCompilationError(
            f"element '{element.element_id}' requires source-quality evidence before non-static motion"
        )
    if profile is not None:
        quality_result = validate_transformation_for_source_quality(profile, recipe)
        if not quality_result.allowed:
            raise FinalHitMotionCompilationError(
                f"element '{element.element_id}' transformation exceeds source-quality limits: "
                + "; ".join(quality_result.violations)
            )

    purpose = {
        "WITHHOLD": "WITHHOLD",
        "REVEAL": "REVEAL_TARGET",
        "FOCUS": "FOCUS_TARGET",
        "CONTRAST": "CONTRAST",
        "PROVE": "PROVE_EVIDENCE",
        "EXPLAIN": "EXPLAIN_TARGET",
        "CONNECT": "CONNECT_CONTEXT",
        "ESCALATE": "ESCALATE",
        "INTERRUPT": "INTERRUPT",
        "RESOLVE": "RETURN_TO_SOURCE",
    }[intent.intent]
    raw_keyframes = recipe.keyframes
    if not raw_keyframes:
        raw_keyframes = [{"at_bps": 0, "template": "HOLD"}, {"at_bps": 10000, "template": "HOLD"}]
    keyframes = [
        _recipe_keyframe_to_model(raw, duration_ms=shot_duration_ms, purpose=purpose)
        for raw in raw_keyframes
    ]
    motion_identity = {
        "element_id": element.element_id,
        "recipe_id": recipe.recipe_id,
        "duration_ms": shot_duration_ms,
        "keyframes": [kf.model_dump(mode="json") for kf in keyframes],
    }
    plan = MotionPlan(
        motion_plan_id=f"motion:{canonical_sha256(motion_identity)[:24]}",
        duration_ms=shot_duration_ms,
        keyframes=keyframes,
        intensity_bps=_motion_intensity_bps(recipe, keyframes),
        attention_cost_bps=_attention_cost_bps(recipe, keyframes),
        compiled_from_recipe_id=recipe.recipe_id,
        source_quality_level=profile.quality_level if profile is not None else None,
    )
    _validate_motion_plan(
        plan,
        element_id=element.element_id,
        shot_duration_ms=shot_duration_ms,
        constraints=harness_constraints,
    )
    if plan.motion_plan_id.startswith("motion:"):
        digest = canonical_sha256(
            {
                "element_id": element.element_id,
                "intent_id": intent.intent_id,
                "recipe_id": recipe.recipe_id,
                "motion_plan": plan.model_dump(mode="json"),
            }
        )
    else:  # pragma: no cover - content-addressed identity is always prefixed above.
        digest = canonical_sha256(plan.model_dump(mode="json"))
    return MotionPlanCompilation(
        element_id=element.element_id,
        motion_plan=plan,
        compilation_sha256=digest,
    )


def _motion_intensity_bps(recipe: TransformationRecipe, keyframes: Sequence[Keyframe]) -> int:
    scale_deltas = [abs((keyframe.scale_bps or 10000) - 10000) for keyframe in keyframes]
    declared = 0
    for primitive in recipe.primitives:
        if "motion_amplitude_bps" in primitive:
            declared = max(declared, abs(int(primitive["motion_amplitude_bps"])))
    return min(10000, max(max(scale_deltas, default=0), declared))


def _attention_cost_bps(recipe: TransformationRecipe, keyframes: Sequence[Keyframe]) -> int:
    intensity = _motion_intensity_bps(recipe, keyframes)
    extra_interventions = max(0, len(keyframes) - 2)
    # This is a deterministic benchmark/decision rule, not a universal claim
    # about human attention. It charges for magnitude plus extra interventions.
    return min(10000, intensity + extra_interventions * 250)


def _validate_motion_plan(
    plan: MotionPlan,
    *,
    element_id: str,
    shot_duration_ms: int,
    constraints: Mapping[str, Any],
) -> None:
    if plan.duration_ms != shot_duration_ms:
        raise FinalHitMotionCompilationError(
            f"element '{element_id}' motion duration {plan.duration_ms} does not match shot duration {shot_duration_ms}"
        )
    if len(plan.keyframes) < 2:
        raise FinalHitMotionCompilationError(f"element '{element_id}' motion requires at least two keyframes")
    if plan.keyframes[0].at_ms != 0 or plan.keyframes[-1].at_ms != plan.duration_ms:
        raise FinalHitMotionCompilationError(
            f"element '{element_id}' motion keyframes must span the complete shot"
        )
    previous = -1
    for keyframe in plan.keyframes:
        if keyframe.at_ms <= previous:
            raise FinalHitMotionCompilationError(
                f"element '{element_id}' motion keyframes must be strictly increasing"
            )
        if keyframe.at_ms < 0 or keyframe.at_ms > plan.duration_ms:
            raise FinalHitMotionCompilationError(
                f"element '{element_id}' motion keyframe is outside shot timing"
            )
        previous = keyframe.at_ms
    max_intensity = int(constraints.get("max_motion_intensity_bps", _VALID_INTENSITY_MAX_BPS))
    max_attention = int(constraints.get("max_attention_cost_bps", 10000))
    if plan.intensity_bps > max_intensity:
        raise FinalHitMotionCompilationError(
            f"element '{element_id}' motion intensity {plan.intensity_bps} exceeds harness maximum {max_intensity}"
        )
    if plan.attention_cost_bps > max_attention:
        raise FinalHitMotionCompilationError(
            f"element '{element_id}' attention cost {plan.attention_cost_bps} exceeds harness budget {max_attention}"
        )
    max_keyframes = int(constraints.get("max_keyframes", 32))
    if len(plan.keyframes) > max_keyframes:
        raise FinalHitMotionCompilationError(
            f"element '{element_id}' uses {len(plan.keyframes)} keyframes; harness maximum is {max_keyframes}"
        )
    if plan.intensity_bps > _VALID_INTENSITY_MAX_BPS:
        raise FinalHitMotionCompilationError(
            f"element '{element_id}' motion intensity exceeds deterministic maximum {_VALID_INTENSITY_MAX_BPS}"
        )


def _iter_elements(revision: StoryboardRevision) -> Iterable[Tuple[StoryboardScene, StoryboardShot, StoryboardElement]]:
    for scene in revision.scenes:
        for shot in scene.shots:
            for element in shot.elements:
                yield scene, shot, element


def _validate_asset_and_evidence(element: StoryboardElement, revision_evidence: set[str], errors: List[str]) -> None:
    if not element.source_evidence_refs or not set(element.source_evidence_refs).issubset(revision_evidence):
        errors.append(f"element '{element.element_id}' has invalid source evidence lineage")
    for asset in element.asset_references:
        if not asset.approved:
            errors.append(f"asset '{asset.asset_id}' is not operator-approved")
        if asset.rights_status.upper() not in {"CLEARED", "NOT_REQUIRED"}:
            errors.append(f"asset '{asset.asset_id}' has unresolved rights status '{asset.rights_status}'")
        if not asset.evidence_refs or not set(asset.evidence_refs).issubset(revision_evidence):
            errors.append(f"asset '{asset.asset_id}' has invalid evidence lineage")
        if asset.source_quality_profile is not None:
            if asset.source_quality_profile.source_ref != asset.asset_id:
                errors.append(f"asset '{asset.asset_id}' source-quality profile is bound to another source")
            if not set(asset.source_quality_profile.evidence_refs).issubset(revision_evidence):
                errors.append(f"asset '{asset.asset_id}' source-quality evidence is outside revision lineage")


def _validate_design_system(
    revision: StoryboardRevision,
    *,
    design_system_ref: Optional[Mapping[str, Any]],
    constraints: Mapping[str, Any],
    strict: bool,
    warnings: List[str],
    errors: List[str],
) -> None:
    required = bool(constraints.get("require_design_system", strict))
    try:
        normalized_ref = _canonical_ref(design_system_ref, "design_system_ref") if design_system_ref is not None else None
    except DesignSystemValidationError as exc:
        errors.append(str(exc))
        return
    if normalized_ref is None:
        if required:
            errors.append(
                "strict final-hit validation requires an explicit Design System canonical reference"
            )
        else:
            warnings.append("Design System reference not supplied; downstream composition authority must bind it")
        return
    for _, _, element in _iter_elements(revision):
        local = element.properties.get("design_system_ref")
        if local is None:
            continue
        try:
            local_ref = _canonical_ref(local, f"element '{element.element_id}' design_system_ref")
        except DesignSystemValidationError as exc:
            errors.append(str(exc))
            continue
        if local_ref != normalized_ref:
            errors.append(
                f"element '{element.element_id}' design_system_ref does not match storyboard Design System reference"
            )


def _validate_legibility(element: StoryboardElement, *, constraints: Mapping[str, Any], strict: bool, errors: List[str], warnings: List[str]) -> None:
    raw = element.properties.get("evidence_legibility_bps")
    if raw is None:
        if strict and str(element.kind).upper() in {"DOCUMENT", "SCREENSHOT", "TEXT", "SOURCE_FRAME"}:
            errors.append(
                f"element '{element.element_id}' has no evidence_legibility_bps observation; pixel-level legibility is unproven"
            )
        elif not strict:
            warnings.append(
                f"element '{element.element_id}' has no evidence_legibility_bps observation; pixel-level legibility remains unproven"
            )
        return
    if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0 or raw > 10000:
        errors.append(f"element '{element.element_id}' evidence_legibility_bps is invalid")
        return
    minimum = int(constraints.get("min_legibility_bps", 0))
    if raw < minimum:
        errors.append(
            f"element '{element.element_id}' evidence legibility {raw} is below harness minimum {minimum}"
        )


def validate_final_hit(
    revision: StoryboardRevision,
    *,
    format_id: str,
    design_system_ref: Optional[Mapping[str, Any]] = None,
    harness_constraints: Optional[Mapping[str, Any]] = None,
    wrong_reading_locks: Optional[Sequence[str]] = None,
    strict: bool = True,
) -> FinalHitValidationResult:
    constraints = _validate_harness_constraints(harness_constraints or {}, strict=strict)
    checks: Dict[str, str] = {}
    errors: List[str] = []
    warnings: List[str] = []
    compilations: List[MotionPlanCompilation] = []

    try:
        program = get_storyboard_program(format_id)
        program.validate(revision)
        checks["format_grammar"] = "PASS"
    except (StoryboardProgramAuthorityError, StoryboardProgramValidationError, ValueError) as exc:
        checks["format_grammar"] = "FAIL"
        errors.append(str(exc))

    revision_evidence = set(revision.source_evidence_refs)
    if not revision_evidence:
        checks["source_evidence"] = "FAIL"
        errors.append("final-hit validation requires source_evidence_refs")
    elif len(revision_evidence) != len(revision.source_evidence_refs):
        checks["source_evidence"] = "FAIL"
        errors.append("source_evidence_refs must be deterministic and unique")
    else:
        checks["source_evidence"] = "PASS"

    if strict and not revision.harness_id:
        checks["harness_constraints"] = "FAIL"
        errors.append("strict final-hit validation requires StoryboardRevision.harness_id")
    else:
        checks["harness_constraints"] = "PASS" if revision.harness_id else "WARN"
        if not revision.harness_id:
            warnings.append("StoryboardRevision has no harness_id; legacy validation does not establish a harness binding")

    _validate_design_system(
        revision,
        design_system_ref=design_system_ref,
        constraints=constraints,
        strict=strict,
        warnings=warnings,
        errors=errors,
    )
    checks["design_system"] = "PASS" if not any("Design System" in error for error in errors) else "FAIL"

    if wrong_reading_locks is None:
        wrong_reading_locks = []
    clean_locks = [str(lock).strip() for lock in wrong_reading_locks if str(lock).strip()]
    if constraints.get("require_wrong_reading_locks", strict) and not clean_locks:
        checks["wrong_reading_locks"] = "FAIL"
        errors.append("final-hit validation requires non-empty wrong-reading locks")
    else:
        checks["wrong_reading_locks"] = "PASS" if clean_locks else "WARN"
        if not clean_locks:
            warnings.append("wrong-reading locks were not supplied; downstream semantic lock preservation is unproven")

    motion_failure_count = 0
    for scene, shot, element in _iter_elements(revision):
        if shot.start_ms < 0 or shot.end_ms <= shot.start_ms:
            errors.append(f"shot '{shot.shot_id}' has invalid non-negative timing")
        if not scene.semantic_purpose.strip():
            errors.append(f"scene '{scene.scene_id}' semantic purpose is empty")
        if not shot.semantic_purpose.strip():
            errors.append(f"shot '{shot.shot_id}' semantic purpose is empty")
        if not element.semantic_purpose.strip():
            errors.append(f"element '{element.element_id}' semantic purpose is empty")
        _validate_asset_and_evidence(element, revision_evidence, errors)
        _validate_legibility(element, constraints=constraints, strict=strict, errors=errors, warnings=warnings)

        intent = element.transformation_intent
        if intent is not None:
            overlap = _tokens(element.semantic_purpose) & _tokens(intent.semantic_target)
            if not overlap:
                errors.append(
                    f"element '{element.element_id}' semantic purpose does not share a material target token with transformation semantic_target"
                )
            if scene.narrative_grammar is not None and scene.narrative_grammar.grammar_mode != intent.intent:
                errors.append(
                    f"element '{element.element_id}' transformation intent '{intent.intent}' does not match scene grammar '{scene.narrative_grammar.grammar_mode}'"
                )
            profile = _element_source_quality(element)
            if intent.motion != "STATIC" and profile is None:
                errors.append(
                    f"element '{element.element_id}' requires a source-quality profile before non-static motion"
                )
        geometry = element.properties.get("geometry")
        if geometry is not None:
            try:
                safe_area = _safe_area_from_constraints(constraints)
                if safe_area is not None:
                    _geometry_within_safe_area(geometry, safe_area, f"element '{element.element_id}' geometry")
                else:
                    # Canvas-bound geometry is still validated when a safe area is not supplied.
                    _geometry_within_safe_area(
                        geometry,
                        {"x_bps": 0, "y_bps": 0, "width_bps": 10000, "height_bps": 10000},
                        f"element '{element.element_id}' geometry",
                    )
            except FinalHitValidationError as exc:
                errors.append(str(exc))
        elif format_id.upper() == "SUPERVISUAL":
            errors.append(f"supervisual element '{element.element_id}' requires geometry")

        try:
            compilation = _compile_motion_plan(
                element,
                shot_duration_ms=shot.end_ms - shot.start_ms,
                harness_constraints=constraints,
            )
            if compilation is not None:
                compilations.append(compilation)
        except FinalHitValidationError as exc:
            motion_failure_count += 1
            errors.append(str(exc))

    if motion_failure_count == 0:
        checks["motion_plan_keyframes"] = "PASS"
    else:
        checks["motion_plan_keyframes"] = "FAIL"

    checks["semantic_purpose"] = "FAIL" if any("semantic purpose" in error for error in errors) else "PASS"
    checks["evidence_legibility"] = "FAIL" if any("legibility" in error for error in errors) else "PASS"
    checks["geometry_safe_area"] = "FAIL" if any("geometry" in error or "safe area" in error for error in errors) else "PASS"
    checks["source_quality"] = "FAIL" if any("source-quality" in error or "source-quality profile" in error for error in errors) else "PASS"
    checks["attention_cost"] = "FAIL" if any("attention cost" in error for error in errors) else "PASS"
    checks["motion_intensity"] = "FAIL" if any("motion intensity" in error for error in errors) else "PASS"
    checks["continuity"] = "FAIL" if any("keyframes" in error or "shot duration" in error for error in errors) else "PASS"

    missing_grammar = scene_count_without_grammar(revision)
    grammar_bindings = [scene.narrative_grammar for scene in revision.scenes if scene.narrative_grammar is not None]
    if grammar_bindings:
        grammar_report = NarrativeEditingGrammarRegistry.validate_sequence(
            grammar_bindings,
            expected_harness_id=revision.harness_id,
            expected_scene_ids=(scene.scene_id for scene in revision.scenes),
        )
        if not grammar_report.passed:
            errors.extend(grammar_report.errors)
    if strict and missing_grammar:
        errors.append("strict final-hit validation requires a NarrativeEditingGrammar binding for every scene")
    if missing_grammar:
        checks["visual_grammar"] = "FAIL" if strict else "WARN"
        if not strict:
            warnings.append("not every scene has a NarrativeEditingGrammar binding; semantic-to-expression grammar is incomplete")
    else:
        checks["visual_grammar"] = (
            "PASS" if not any("narrative grammar" in error.lower() for error in errors) else "FAIL"
        )

    passed = not errors
    payload = {
        "passed": passed,
        "strict": strict,
        "format_id": format_id.upper(),
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "motion_plan_compilations": [item.model_dump(mode="json") for item in compilations],
        "operator_judgment_required": True,
    }
    return FinalHitValidationResult(
        **payload,
        validation_sha256=canonical_sha256(payload),
    )


class FinalHitCompilation(BaseModel):
    """Pure final-hit compilation artifact; no canonical state is mutated."""

    format_id: str
    revision_id: str
    validation_sha256: str
    motion_plan_compilations: List[MotionPlanCompilation] = Field(default_factory=list)
    compilation_sha256: str


def compile_final_hit(
    revision: StoryboardRevision,
    *,
    format_id: str,
    design_system_ref: Optional[Mapping[str, Any]] = None,
    harness_constraints: Optional[Mapping[str, Any]] = None,
    wrong_reading_locks: Optional[Sequence[str]] = None,
    strict: bool = True,
) -> FinalHitCompilation:
    """Validate and project final-hit motion plans without changing persisted state."""
    result = validate_final_hit(
        revision,
        format_id=format_id,
        design_system_ref=design_system_ref,
        harness_constraints=harness_constraints,
        wrong_reading_locks=wrong_reading_locks,
        strict=strict,
    )
    if not result.passed:
        raise FinalHitValidationError(
            "final-hit compilation blocked by validation: " + "; ".join(result.errors)
        )
    payload = {
        "format_id": format_id.upper(),
        "revision_id": revision.revision_id,
        "validation_sha256": result.validation_sha256,
        "motion_plan_compilations": [item.model_dump(mode="json") for item in result.motion_plan_compilations],
    }
    return FinalHitCompilation(
        **payload,
        compilation_sha256=canonical_sha256(payload),
    )


def scene_count_without_grammar(revision: StoryboardRevision) -> int:
    return sum(1 for scene in revision.scenes if scene.narrative_grammar is None)


__all__ = [
    "DesignSystemValidationError",
    "FinalHitMotionCompilationError",
    "FinalHitValidationError",
    "FinalHitValidationResult",
    "FinalHitCompilation",
    "HarnessConstraintValidationError",
    "MotionPlanCompilation",
    "scene_count_without_grammar",
    "compile_final_hit",
    "validate_final_hit",
]
