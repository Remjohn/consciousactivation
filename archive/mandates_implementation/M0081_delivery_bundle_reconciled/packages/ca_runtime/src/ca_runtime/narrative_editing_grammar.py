"""CAE-native Narrative Editing Grammar (M0081).

The grammar is a constrained narrative vocabulary. It describes relationships
and sequence conditions that translate upstream editorial / activative meaning
into a scene-level perceptual role. It intentionally contains no effect,
provider, geometry, or keyframe recipes.

Semantic meaning remains upstream. Harness identity is carried as an execution
binding. The validator is deterministic and fail-closed.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ca_contracts import CanonicalizationError, canonical_sha256


class NarrativeGrammarError(ValueError):
    """Base error for fail-closed narrative grammar validation."""


class NarrativeGrammarUnknownModeError(NarrativeGrammarError):
    """A binding references a mode not present in the canonical registry."""


class NarrativeGrammarBindingError(NarrativeGrammarError):
    """A scene/archetype/harness binding violates the grammar contract."""


class NarrativeGrammarSequenceError(NarrativeGrammarError):
    """A set of bindings cannot form a valid narrative sequence."""


class NarrativeGrammarMode(str):
    WITHHOLD = "WITHHOLD"
    REVEAL = "REVEAL"
    FOCUS = "FOCUS"
    CONTRAST = "CONTRAST"
    PROVE = "PROVE"
    EXPLAIN = "EXPLAIN"
    CONNECT = "CONNECT"
    ESCALATE = "ESCALATE"
    INTERRUPT = "INTERRUPT"
    RESOLVE = "RESOLVE"


_NARRATIVE_MODES = {
    NarrativeGrammarMode.WITHHOLD, NarrativeGrammarMode.REVEAL,
    NarrativeGrammarMode.FOCUS, NarrativeGrammarMode.CONTRAST,
    NarrativeGrammarMode.PROVE, NarrativeGrammarMode.EXPLAIN,
    NarrativeGrammarMode.CONNECT, NarrativeGrammarMode.ESCALATE,
    NarrativeGrammarMode.INTERRUPT, NarrativeGrammarMode.RESOLVE,
}


class NarrativeSceneContext(str):
    OPENING = "OPENING"
    ORIENTATION = "ORIENTATION"
    SETUP = "SETUP"
    TENSION = "TENSION"
    EVIDENCE = "EVIDENCE"
    CONTRAST = "CONTRAST"
    TURN = "TURN"
    INTERRUPT = "INTERRUPT"
    RESOLUTION = "RESOLUTION"
    BRIDGE = "BRIDGE"
    AFTERMATH = "AFTERMATH"


class NarrativeEditingGrammarEntry(BaseModel):
    """One executable grammar rule; never an effect recipe."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    grammar_id: str
    version: str
    mode: str
    purpose: str
    relational_pattern: str
    allowed_scene_contexts: Tuple[str, ...]
    required_meaning_fields: Tuple[str, ...]
    requires_prior_modes: Tuple[str, ...] = ()
    requires_later_modes: Tuple[str, ...] = ()
    min_relation_targets: int = 0
    min_evidence_refs: int = 0
    false_proof_conditions: Tuple[str, ...] = ()

    @field_validator("mode")
    @classmethod
    def mode_is_known(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in _NARRATIVE_MODES:
            raise ValueError(f"unsupported narrative grammar mode: {value}")
        return normalized

    @field_validator("min_relation_targets", "min_evidence_refs")
    @classmethod
    def counts_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("grammar minimum counts must be non-negative")
        return value


class NarrativeGrammarBinding(BaseModel):
    """Scene-local binding of narrative grammar to upstream meaning and harness."""

    model_config = ConfigDict(extra="forbid")

    binding_id: str
    scene_id: str
    grammar_mode: str
    grammar_version: str
    archetype_id: str
    harness_id: str
    activative_meaning: str
    editorial_intent: str
    scene_context: str
    sequence_index: int
    evidence_refs: List[str] = Field(default_factory=list)
    relation_scene_ids: List[str] = Field(default_factory=list)
    wrong_reading_locks: List[str] = Field(default_factory=list)

    @field_validator(
        "binding_id",
        "scene_id",
        "archetype_id",
        "harness_id",
        "activative_meaning",
        "editorial_intent",
        "scene_context",
    )
    @classmethod
    def non_empty_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("narrative grammar identity/context text cannot be empty")
        return value

    @field_validator("grammar_mode")
    @classmethod
    def normalize_mode(cls, value: str) -> str:
        return value.upper()

    @field_validator("scene_context")
    @classmethod
    def normalize_context(cls, value: str) -> str:
        return value.upper()

    @field_validator("sequence_index")
    @classmethod
    def non_negative_sequence(cls, value: int) -> int:
        if value < 0:
            raise ValueError("sequence_index must be non-negative")
        return value


class NarrativeGrammarValidationReport(BaseModel):
    """Deterministic proof that a grammar binding set satisfied all rules."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    grammar_id: str
    grammar_version: str
    passed: bool
    checks: Dict[str, str] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    report_sha256: str


class NarrativeEditingGrammarRegistry:
    """Canonical in-process registry for Narrative Editing Grammar V1."""

    GRAMMAR_ID = "CAE_NARRATIVE_EDITING_GRAMMAR"
    VERSION = "1.0.0"

    _ENTRIES: Tuple[NarrativeEditingGrammarEntry, ...] = (
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.WITHHOLD,
            purpose="Delay a decisive relation so a later beat can reorganize the viewer's expectation.",
            relational_pattern="establish_context_without_decisive_resolution -> later_reframe",
            allowed_scene_contexts=(
                NarrativeSceneContext.OPENING,
                NarrativeSceneContext.ORIENTATION,
                NarrativeSceneContext.SETUP,
                NarrativeSceneContext.TENSION,
                NarrativeSceneContext.BRIDGE,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            requires_later_modes=(NarrativeGrammarMode.REVEAL, NarrativeGrammarMode.RESOLVE),
            false_proof_conditions=(
                "A scene that simply omits information but has no later reframe is not a valid WITHHOLD.",
            ),
        ),
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.REVEAL,
            purpose="Expose a previously constrained or incomplete relation so meaning changes through recognition.",
            relational_pattern="prior_withheld_state -> explicit_recognition",
            allowed_scene_contexts=(
                NarrativeSceneContext.TURN,
                NarrativeSceneContext.EVIDENCE,
                NarrativeSceneContext.RESOLUTION,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            requires_prior_modes=(NarrativeGrammarMode.WITHHOLD,),
            min_evidence_refs=1,
            false_proof_conditions=(
                "A visually striking reveal with no prior withheld question is not a valid REVEAL.",
            ),
        ),
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.FOCUS,
            purpose="Narrow attention from a broader state to one meaning-bearing detail.",
            relational_pattern="broad_context -> discriminating_detail",
            allowed_scene_contexts=(
                NarrativeSceneContext.OPENING,
                NarrativeSceneContext.ORIENTATION,
                NarrativeSceneContext.SETUP,
                NarrativeSceneContext.EVIDENCE,
                NarrativeSceneContext.TURN,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            min_evidence_refs=1,
            false_proof_conditions=(
                "A tighter crop or stronger emphasis without a changed meaning target is not a valid FOCUS.",
            ),
        ),
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.CONTRAST,
            purpose="Place materially different evidence states in relation so the difference itself carries meaning.",
            relational_pattern="state_A <> state_B -> recognition_of_difference",
            allowed_scene_contexts=(
                NarrativeSceneContext.TENSION,
                NarrativeSceneContext.CONTRAST,
                NarrativeSceneContext.TURN,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            min_relation_targets=1,
            min_evidence_refs=1,
            false_proof_conditions=(
                "Two adjacent but semantically equivalent shots are not a valid CONTRAST.",
            ),
        ),
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.PROVE,
            purpose="Connect a claim or proposition to source-grounded evidence that can bear the claim.",
            relational_pattern="claim -> evidence_bearing_instance",
            allowed_scene_contexts=(
                NarrativeSceneContext.EVIDENCE,
                NarrativeSceneContext.TURN,
                NarrativeSceneContext.RESOLUTION,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            min_evidence_refs=1,
            false_proof_conditions=(
                "An impressive-looking illustrative asset without source evidence is not a valid PROVE.",
            ),
        ),
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.EXPLAIN,
            purpose="Make a causal or mechanistic relation legible without inventing upstream meaning.",
            relational_pattern="observed_state -> causal_mechanism",
            allowed_scene_contexts=(
                NarrativeSceneContext.ORIENTATION,
                NarrativeSceneContext.SETUP,
                NarrativeSceneContext.EVIDENCE,
                NarrativeSceneContext.TURN,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            min_evidence_refs=1,
            false_proof_conditions=(
                "A sequence that adds plausible narration but has no evidence for the claimed mechanism is not a valid EXPLAIN.",
            ),
        ),
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.CONNECT,
            purpose="Link separated evidence or scenes through an explicit shared meaning relation.",
            relational_pattern="current_state <-> related_state",
            allowed_scene_contexts=(
                NarrativeSceneContext.BRIDGE,
                NarrativeSceneContext.TENSION,
                NarrativeSceneContext.TURN,
                NarrativeSceneContext.AFTERMATH,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            min_relation_targets=1,
            false_proof_conditions=(
                "A repeated motif with no declared semantic relation is not a valid CONNECT.",
            ),
        ),
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.ESCALATE,
            purpose="Increase the consequence, tension, or irreversibility carried by the active narrative relation.",
            relational_pattern="current_stakes < next_stakes",
            allowed_scene_contexts=(
                NarrativeSceneContext.TENSION,
                NarrativeSceneContext.TURN,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            requires_prior_modes=(
                NarrativeGrammarMode.WITHHOLD,
                NarrativeGrammarMode.CONTRAST,
                NarrativeGrammarMode.EXPLAIN,
                NarrativeGrammarMode.PROVE,
            ),
            false_proof_conditions=(
                "More motion, scale, or density without higher narrative stakes is not a valid ESCALATE.",
            ),
        ),
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.INTERRUPT,
            purpose="Break the established attention path with a meaningful alternate carrier or perspective.",
            relational_pattern="established_pattern -> meaningful_break -> return_or_reframe",
            allowed_scene_contexts=(
                NarrativeSceneContext.INTERRUPT,
                NarrativeSceneContext.TURN,
                NarrativeSceneContext.BRIDGE,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            min_relation_targets=1,
            false_proof_conditions=(
                "A pattern break that creates attention but no narrative reorientation is not a valid INTERRUPT.",
            ),
        ),
        NarrativeEditingGrammarEntry(
            grammar_id=GRAMMAR_ID,
            version=VERSION,
            mode=NarrativeGrammarMode.RESOLVE,
            purpose="Close an active uncertainty, tension, or prediction gap with a meaningful outcome.",
            relational_pattern="open_relation -> clarified_or_closed_relation",
            allowed_scene_contexts=(
                NarrativeSceneContext.TURN,
                NarrativeSceneContext.RESOLUTION,
                NarrativeSceneContext.AFTERMATH,
            ),
            required_meaning_fields=("activative_meaning", "editorial_intent"),
            requires_prior_modes=(
                NarrativeGrammarMode.WITHHOLD,
                NarrativeGrammarMode.REVEAL,
                NarrativeGrammarMode.CONTRAST,
                NarrativeGrammarMode.PROVE,
                NarrativeGrammarMode.EXPLAIN,
                NarrativeGrammarMode.ESCALATE,
                NarrativeGrammarMode.INTERRUPT,
                NarrativeGrammarMode.CONNECT,
            ),
            min_evidence_refs=1,
            false_proof_conditions=(
                "Ending a sequence with a visual stop or title card without closing the active meaning is not a valid RESOLVE.",
            ),
        ),
    )

    @classmethod
    def modes(cls) -> Tuple[str, ...]:
        return tuple(entry.mode for entry in cls._ENTRIES)

    @classmethod
    def all_entries(cls) -> Tuple[NarrativeEditingGrammarEntry, ...]:
        return cls._ENTRIES

    @classmethod
    def get(cls, mode: str) -> NarrativeEditingGrammarEntry:
        normalized = mode.upper()
        for entry in cls._ENTRIES:
            if entry.mode == normalized:
                return entry
        raise NarrativeGrammarUnknownModeError(
            f"narrative grammar mode '{mode}' is not registered"
        )

    @classmethod
    def validate_binding(
        cls,
        binding: NarrativeGrammarBinding,
        *,
        expected_harness_id: str | None = None,
    ) -> None:
        entry = cls.get(binding.grammar_mode)
        if binding.grammar_version != entry.version:
            raise NarrativeGrammarBindingError(
                f"scene '{binding.scene_id}' uses grammar version '{binding.grammar_version}', "
                f"expected '{entry.version}'"
            )
        if binding.scene_context not in entry.allowed_scene_contexts:
            raise NarrativeGrammarBindingError(
                f"scene '{binding.scene_id}' context '{binding.scene_context}' is not allowed "
                f"for {entry.mode}"
            )
        if expected_harness_id is not None and binding.harness_id != expected_harness_id:
            raise NarrativeGrammarBindingError(
                f"scene '{binding.scene_id}' binds harness '{binding.harness_id}' "
                f"but revision harness is '{expected_harness_id}'"
            )
        for field_name in entry.required_meaning_fields:
            value = getattr(binding, field_name, None)
            if not isinstance(value, str) or not value.strip():
                raise NarrativeGrammarBindingError(
                    f"scene '{binding.scene_id}' is missing required meaning input '{field_name}'"
                )
        if len(binding.evidence_refs) < entry.min_evidence_refs:
            raise NarrativeGrammarBindingError(
                f"scene '{binding.scene_id}' requires at least {entry.min_evidence_refs} "
                f"evidence reference(s) for {entry.mode}"
            )
        if len(set(binding.evidence_refs)) != len(binding.evidence_refs):
            raise NarrativeGrammarBindingError(
                f"scene '{binding.scene_id}' evidence_refs must be unique"
            )
        if len(binding.relation_scene_ids) < entry.min_relation_targets:
            raise NarrativeGrammarBindingError(
                f"scene '{binding.scene_id}' requires at least {entry.min_relation_targets} "
                f"relation target(s) for {entry.mode}"
            )
        if binding.scene_id in binding.relation_scene_ids:
            raise NarrativeGrammarBindingError(
                f"scene '{binding.scene_id}' cannot relate to itself"
            )

    @classmethod
    def validate_sequence(
        cls,
        bindings: Sequence[NarrativeGrammarBinding],
        *,
        expected_harness_id: str | None = None,
        expected_scene_ids: Iterable[str] | None = None,
    ) -> NarrativeGrammarValidationReport:
        errors: List[str] = []
        checks: Dict[str, str] = {
            "registry_identity": "PASS",
            "binding_contracts": "PASS",
            "sequence_order": "PASS",
            "relational_requirements": "PASS",
            "harness_binding": "PASS",
        }

        if not bindings:
            checks["binding_contracts"] = "SKIP"
            payload = {
                "grammar_id": cls.GRAMMAR_ID,
                "grammar_version": cls.VERSION,
                "passed": True,
                "checks": checks,
                "errors": errors,
            }
            return NarrativeGrammarValidationReport(
                **payload, report_sha256=canonical_sha256(payload)
            )

        try:
            for binding in bindings:
                cls.validate_binding(
                    binding, expected_harness_id=expected_harness_id
                )
        except NarrativeGrammarError as exc:
            errors.append(str(exc))
            checks["binding_contracts"] = "FAIL"

        scene_ids = [binding.scene_id for binding in bindings]
        if len(scene_ids) != len(set(scene_ids)):
            errors.append("narrative grammar scene_id values must be unique")
            checks["binding_contracts"] = "FAIL"

        sequence_indexes = [binding.sequence_index for binding in bindings]
        if sorted(sequence_indexes) != list(range(len(bindings))):
            errors.append("narrative grammar sequence_index values must be contiguous from zero")
            checks["sequence_order"] = "FAIL"

        if expected_scene_ids is not None:
            expected = set(expected_scene_ids)
            actual = set(scene_ids)
            if actual != expected:
                missing = sorted(expected - actual)
                extra = sorted(actual - expected)
                errors.append(
                    f"narrative grammar scene binding mismatch: missing={missing}, extra={extra}"
                )
                checks["binding_contracts"] = "FAIL"

        ordered = sorted(bindings, key=lambda item: item.sequence_index)
        for position, binding in enumerate(ordered):
            try:
                entry = cls.get(binding.grammar_mode)
            except NarrativeGrammarUnknownModeError as exc:
                errors.append(str(exc))
                checks["binding_contracts"] = "FAIL"
                continue
            prior_modes = {item.grammar_mode for item in ordered[:position]}
            later_modes = {item.grammar_mode for item in ordered[position + 1 :]}
            has_required_prior = not entry.requires_prior_modes or bool(
                prior_modes.intersection(entry.requires_prior_modes)
            )
            has_required_later = not entry.requires_later_modes or bool(
                later_modes.intersection(entry.requires_later_modes)
            )
            if not has_required_prior:
                errors.append(
                    f"scene '{binding.scene_id}' {entry.mode} requires a prior mode in "
                    f"{list(entry.requires_prior_modes)}"
                )
            if not has_required_later:
                errors.append(
                    f"scene '{binding.scene_id}' {entry.mode} requires a later mode in "
                    f"{list(entry.requires_later_modes)}"
                )

            missing_targets = [
                target for target in binding.relation_scene_ids if target not in scene_ids
            ]
            if missing_targets:
                errors.append(
                    f"scene '{binding.scene_id}' references unknown relation target(s): "
                    f"{sorted(missing_targets)}"
                )

        if any("requires a prior mode" in error for error in errors) or any(
            "requires a later mode" in error for error in errors
        ):
            checks["relational_requirements"] = "FAIL"

        if expected_harness_id is not None and any(
            binding.harness_id != expected_harness_id for binding in bindings
        ):
            checks["harness_binding"] = "FAIL"

        passed = not errors
        payload = {
            "grammar_id": cls.GRAMMAR_ID,
            "grammar_version": cls.VERSION,
            "passed": passed,
            "checks": checks,
            "errors": errors,
        }
        try:
            digest = canonical_sha256(payload)
        except CanonicalizationError as exc:
            raise NarrativeGrammarSequenceError(
                f"narrative grammar report is not canonicalizable: {exc}"
            ) from exc
        return NarrativeGrammarValidationReport(report_sha256=digest, **payload)


def narrative_grammar_registry_payload() -> Dict[str, Any]:
    """Return a canonical, documentation-friendly registry payload."""
    return {
        "grammar_id": NarrativeEditingGrammarRegistry.GRAMMAR_ID,
        "version": NarrativeEditingGrammarRegistry.VERSION,
        "authority_boundary": (
            "Narrative Editing Grammar constrains sequence and relational meaning. "
            "It does not contain effect recipes, geometry, provider parameters, "
            "generation commands, or semantic-authority replacement."
        ),
        "entries": [
            {
                **entry.model_dump(),
            }
            for entry in NarrativeEditingGrammarRegistry.all_entries()
        ],
    }


__all__ = [
    "NarrativeEditingGrammarEntry",
    "NarrativeEditingGrammarRegistry",
    "NarrativeGrammarBinding",
    "NarrativeGrammarBindingError",
    "NarrativeGrammarError",
    "NarrativeGrammarMode",
    "NarrativeGrammarSequenceError",
    "NarrativeGrammarUnknownModeError",
    "NarrativeGrammarValidationReport",
    "NarrativeSceneContext",
    "narrative_grammar_registry_payload",
]
