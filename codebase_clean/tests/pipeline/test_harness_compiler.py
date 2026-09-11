"""Tests for TS-APP-BRIDGE-001 — Harness Definition Compiler.

Implements AC-001 through AC-011 from TS-APP-BRIDGE-001.md §9.
Test naming mirrors the spec's ``§10. Test files to create`` list exactly.

Why we don't use ``PortableAtomicHarnessDefinition.create()``
--------------------------------------------------------------
``create()`` chains through an operator-manifest parser whose governed
task-contract validators require a full, parseable manifest file.
That path is not the subject of this spec — the compiler under test
never calls ``create()`` or ``validate()`` on the Builder side.

Instead we build a thin test double whose ``.content`` attribute is the
exact 32-key dict shape that ``create()`` would emit (see
``portable_export.py`` §3 of TS-APP-BRIDGE-001).  The compiler reads
``definition.definition_id`` and ``definition.content[...]`` only —
both are present.  ``definition.content_bytes`` and
``definition.payload_bytes`` are not touched by the compiler, so they
are filled with a plausible SHA-256 placeholder for realism.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

import pytest

from cmf_pipeline.intake.harness_compiler import (
    compile_portable_to_intake,
)
from cmf_pipeline.intake.harness_compiler_contracts import (
    BLOCKER_1_TEXT,
    BLOCKER_2_TEXT,
    BLOCKER_3_TEXT,
    BLOCKER_4_TEXT,
    BLOCKER_5_TEXT,
    BLOCKER_6_REPAIR_TEXT,
    BLOCKER_6_EVAL_TEXT,
    HarnessCompilationBlocked,
)


# ---------------------------------------------------------------------------
# Minimal test-double: mirrors the dataclass shape the compiler touches
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class _TestDefinition:
    definition_id: str
    definition_hash: str
    content: Mapping[str, Any]  # the 32-key dict Porter creates from a task
    content_bytes: bytes = hashlib.sha256(b"").digest()
    payload_bytes: bytes = hashlib.sha256(b"").digest()


# ---------------------------------------------------------------------------
# Fixture: a realistic, minimal activative-mode PortableAtomicHarnessDefinition
# .content with all 32 keys populated exactly as PortableAtomicHarnessDefinition
# .create() would emit for a valid activative manifest.
# ---------------------------------------------------------------------------

def _make_definition(
    *,
    mode: str = "activative",
    manifest_version: str = "1.0.0",
) -> _TestDefinition:
    """Return a _TestDefinition whose .content matches the real Builder schema."""
    manifest_hash = "c" * 64
    digest = hashlib.sha256(
        json.dumps(
            {
                "schema_id": "cmf-builder-atomic-harness-definition/v1",
                "mode": mode,
                "manifest_version": manifest_version,
                "manifest_hash": manifest_hash,
                "task_id": "test-task",
                "category_id": "short_video",
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()
    definition_id = f"atomic-harness-definition_{digest}"

    if mode == "activative":
        category_binding: dict[str, Any] = {
            "harness_id": "test-harness-v1",
            "harness_version": "1.0.0",
            "applicability": "REQUIRED",
            "category_id": "short_video",
            "category_name": "Short Video",
            "category_registry_version": "1.0.0",
            "category_registry_hash": "a" * 64,
            "constitutional_authority_ref": "constitution:short_video:v1",
            "runtime_law": "Visual Syntax First",
            "harness_development_law": "Visual Syntax First",
            "semantic_lineage_refs": [f"lineage:{i}" for i in range(1, 11)],
            "wrong_reading_locks": ["lock_a", "lock_b"],
            "not_applicable_basis": "NONE",
            "certification_state": "STRUCTURAL_UNCERTIFIED",
            "production_ready": False,
            "certified": False,
            "binding_hash": "b" * 64,
        }
        classification = [
            "canonical_category_bound",
            "short_video",
            "activative_operator_manifest",
            "non_certified",
            "non_production",
        ]
    else:
        # generic mode — used only in blocker-3 tests
        category_binding = {
            "applicability": "NOT_APPLICABLE",
            "basis": "GENERIC_NON_ACTIVATIVE_TASK",
            "category_id": None,
        }
        classification = [
            "category_neutral",
            "generic_operator_manifest",
            "non_certified",
            "non_production",
        ]

    authority_ref = "cfg:test-operator-manifest:v1"
    provenance_refs = ["prv:source:abc123"]

    content: dict[str, Any] = {
        "schema_id": "cmf-builder-atomic-harness-definition/v1",
        "schema_version": "1.0.0",
        "compiler_id": "cmf-builder/productized-manifest-compiler",
        "compiler_version": "1.0.0",
        "amendment": "PX-AM-001",
        "manifest_id": "test-manifest",
        "manifest_version": manifest_version,
        "manifest_hash": manifest_hash,
        "task_id": "test-task",
        "mode": mode,
        "classification": classification,
        "category_binding": category_binding,
        "atomic_boundary": "scope boundary text",
        "goal": "Create a 30-second short video",
        "success_condition": "A renderable video file is produced.",
        "input_contract": {"type": "operator_manifest"},
        "output_contract": {"artifact_type": "AtomicHarnessDefinition"},
        "minimum_complete_context": ["interview_transcript", "brand_guidelines"],
        "capability_requirements": ["video_editing"],
        "acceptance_tests": ["output_hashes_match_expected"],
        "execution_plan": [
            "accept_governed_operator_manifest",
            "validate_atomic_boundary_and_contracts",
            "compile_atomic_harness_definition",
            "validate_acceptance_contracts",
            "package_portable_artifacts",
        ],
        "authority_chain": [
            "activative_intelligence_constitution_v1_1",
            "builder_prd_v1_2",
            "PX-AM-001",
            authority_ref,
        ],
        "provenance_refs": provenance_refs,
        "activative_intelligence": (
            {"intelligence_profile": "activative-v1", "runtime_config": {}}
            if mode == "activative"
            else None
        ),
        "external_skills_required": 0,
        "external_runtime_dependencies": [],
        "workflow_execution_performed": False,
        "production_eligible": False,
        "certified": False,
        "certification_state": "uncertified_nonproduction",
        "compatibility_status": "builder_contract_compatible_nonproduction",
        "lineage": [manifest_hash, authority_ref, *provenance_refs],
    }
    # Add binding_hash to lineage for activative mode (matches create() logic)
    if mode == "activative":
        content["lineage"].append(category_binding["binding_hash"])  # type: ignore[index]

    return _TestDefinition(
        definition_id=definition_id,
        definition_hash=f"sha256:{digest}",
        content=content,
        content_bytes=hashlib.sha256(json.dumps(content, sort_keys=True).encode()).digest(),
        payload_bytes=hashlib.sha256(
            json.dumps(
                {
                    "artifact_type": "AtomicHarnessDefinition",
                    "definition_id": definition_id,
                    "definition_hash": f"sha256:{digest}",
                    "definition": content,
                },
                sort_keys=True,
            ).encode()
        ).digest(),
    )


# ---------------------------------------------------------------------------
#Happy-path kwargs used by nearly every positive-path test
# ---------------------------------------------------------------------------

def _valid_kwargs() -> dict[str, Any]:
    return {
        "semantic_dependencies": [
            {
                "object_id": "final-script_abc123",
                "version": "1.0.0",
                "sha256": "a" * 64,
            }
        ],
        "capability_metadata": {
            "video_editing": {
                "owner_kind": "tool",
                "required_features": ["ffmpeg"],
                "authority_boundary": "pipeline_owned_execution",
            },
        },
        "workflow": {
            "nodes": [
                {
                    "node_id": "root",
                    "capability_id": "video_editing",
                    "phase_order": 0,
                    "purpose": "Edit the video",
                    "actor_kind": "tool",
                    "role": "composer",
                    "product_boundary": "pipeline",
                    "input_contracts": ["src_pkg_v1"],
                    "output_contracts": ["video_edit_prog_v1"],
                    "side_effect_class": "produces_artifact",
                }
            ],
            "edges": [],
        },
        "evaluation_requirements": ["source_fidelity_check"],
        "repair_laws": ["bounded_local_repair_only"],
    }


# ===========================================================================
# AC-001 — happy path: all blockers satisfied, activative mode, valid semver
# ===========================================================================

class TestFullRoundTrip:
    def test_full_round_trip_validates(self) -> None:
        """AC-001: valid definition + all six optional params -> 14-key output."""
        definition = _make_definition()
        result = compile_portable_to_intake(definition, **_valid_kwargs())

        from cmf_pipeline.intake.definition_intake import (
            AtomicHarnessDefinitionIntake,
        )
        expected = set(AtomicHarnessDefinitionIntake.REQUIRED_KEYS)
        assert set(result) == expected, (
            f"unexpected keys: {set(result) ^ expected}"
        )
        assert result["definition_id"] == definition.definition_id
        assert result["definition_version"] == "1.0.0"
        assert result["category_id"] == "short_video"
        assert result["profile_id"] == "portable-activative-v1"
        assert result["purpose"] == "Create a 30-second short video"
        assert result["wrong_reading_locks"] == ["lock_a", "lock_b"]
        assert result["production_ready"] is False
        assert result["certified"] is False
        assert result["invalidation_state"] == "NOT_INVALIDATED"

    def test_profile_id_matches_existing_registry(self) -> None:
        """AC-009: profile_id derives from the unmodified Pipeline registry."""
        definition = _make_definition()
        result = compile_portable_to_intake(definition, **_valid_kwargs())
        assert result["profile_id"] == "portable-activative-v1"

    def test_wrong_reading_locks_passthrough(self) -> None:
        """AC-010: wrong_reading_locks pass through untransformed."""
        definition = _make_definition()
        result = compile_portable_to_intake(definition, **_valid_kwargs())
        assert result["wrong_reading_locks"] == ["lock_a", "lock_b"]

    def test_blocker_7_default_always_not_invalidated(self) -> None:
        """AC-008: invalidation_state always defaults to NOT_INVALIDATED."""
        definition = _make_definition()
        result = compile_portable_to_intake(definition, **_valid_kwargs())
        assert result["invalidation_state"] == "NOT_INVALIDATED"


# ===========================================================================
# AC-002 — Blocker 1: semantic_dependencies must be caller-supplied
# ===========================================================================

class TestBlocker1SemanticDependencies:
    def test_blocker_1_semantic_dependencies_required(self) -> None:
        definition = _make_definition()
        kwargs = dict(_valid_kwargs())
        del kwargs["semantic_dependencies"]

        with pytest.raises(HarnessCompilationBlocked) as exc_info:
            compile_portable_to_intake(definition, **kwargs)

        exc = exc_info.value
        assert exc.field == "semantic_dependencies"
        assert BLOCKER_1_TEXT in exc.reason
        assert exc.blocker_ref == "TS-APP-BRIDGE-001#blocker-1"


# ===========================================================================
# AC-003 — Blocker 2: capability_metadata must cover every declared capability
# ===========================================================================

class TestBlocker2CapabilityMetadata:
    def test_blocker_2_partial_capability_metadata(self) -> None:
        definition = _make_definition()
        # supply empty metadata so video_editing is missing
        kwargs = dict(_valid_kwargs())
        kwargs["capability_metadata"] = {}

        with pytest.raises(HarnessCompilationBlocked) as exc_info:
            compile_portable_to_intake(definition, **kwargs)

        exc = exc_info.value
        assert exc.field == "capabilities"
        assert BLOCKER_2_TEXT in exc.reason
        assert "video_editing" in exc.reason
        assert exc.blocker_ref == "TS-APP-BRIDGE-001#blocker-2"

    def test_blocker_2_full_capability_metadata_succeeds(self) -> None:
        definition = _make_definition()
        kwargs = dict(_valid_kwargs())
        kwargs["capability_metadata"] = {
            "video_editing": {
                "owner_kind": "tool",
                "required_features": ["ffmpeg"],
                "authority_boundary": "pipeline_owned_execution",
            },
        }
        result = compile_portable_to_intake(definition, **kwargs)
        assert result["capabilities"] == [
            {
                "capability_id": "video_editing",
                "owner_kind": "tool",
                "required_features": ["ffmpeg"],
                "authority_boundary": "pipeline_owned_execution",
            }
        ]


# ===========================================================================
# AC-004 — Blocker 3: generic-mode Harnesses are rejected
# ===========================================================================

class TestBlocker3GenericMode:
    def test_blocker_3_generic_mode_rejected(self) -> None:
        definition = _make_definition(mode="generic")
        kwargs = _valid_kwargs()

        with pytest.raises(HarnessCompilationBlocked) as exc_info:
            compile_portable_to_intake(definition, **kwargs)

        exc = exc_info.value
        assert exc.field == "category_id"
        assert BLOCKER_3_TEXT in exc.reason
        assert exc.blocker_ref == "TS-APP-BRIDGE-001#blocker-3"

    def test_blocker_3_activative_mode_proceeds(self) -> None:
        definition = _make_definition(mode="activative")
        result = compile_portable_to_intake(definition, **_valid_kwargs())
        assert result["category_id"] == "short_video"


# ===========================================================================
# AC-005 — Blocker 4: manifest_version must be valid semver
# ===========================================================================

class TestBlocker4Semver:
    @pytest.mark.parametrize(
        "manifest_version, should_raise",
        [
            ("1.0.0", False),
            ("v1-draft", True),
            ("1.0", True),
            ("1.0.0-beta.1", False),
        ],
        ids=["1.0.0-passes", "v1-draft-fails", "1.0-fails", "1.0.0-beta.1-passes"],
    )
    def test_blocker_4_semver_validation(
        self, manifest_version: str, should_raise: bool
    ) -> None:
        definition = _make_definition(manifest_version=manifest_version)

        if should_raise:
            with pytest.raises(HarnessCompilationBlocked) as exc_info:
                compile_portable_to_intake(definition, **_valid_kwargs())
            exc = exc_info.value
            assert exc.field == "definition_version"
            assert BLOCKER_4_TEXT in exc.reason
            assert exc.blocker_ref == "TS-APP-BRIDGE-001#blocker-4"
        else:
            result = compile_portable_to_intake(definition, **_valid_kwargs())
            assert result["definition_version"] == manifest_version


# ===========================================================================
# AC-006 — Blocker 5: workflow must be caller-supplied (always required)
# ===========================================================================

class TestBlocker5Workflow:
    def test_blocker_5_workflow_always_required(self) -> None:
        definition = _make_definition()
        kwargs = dict(_valid_kwargs())
        del kwargs["workflow"]

        with pytest.raises(HarnessCompilationBlocked) as exc_info:
            compile_portable_to_intake(definition, **kwargs)

        exc = exc_info.value
        assert exc.field == "workflow"
        assert BLOCKER_5_TEXT in exc.reason
        assert exc.blocker_ref == "TS-APP-BRIDGE-001#blocker-5"

    def test_blocker_5_workflow_supplied_succeeds(self) -> None:
        definition = _make_definition()
        result = compile_portable_to_intake(definition, **_valid_kwargs())
        assert result["workflow"] == _valid_kwargs()["workflow"]


# ===========================================================================
# AC-007 — Blocker 6: evaluation_requirements and repair_laws independently req
# ===========================================================================

class TestBlocker6EvalRepair:
    @pytest.mark.parametrize(
        "missing_key, expected_field, expected_text",
        [
            ("evaluation_requirements", "evaluation_requirements", BLOCKER_6_EVAL_TEXT),
            ("repair_laws", "repair_laws", BLOCKER_6_REPAIR_TEXT),
        ],
        ids=["eval-omitted", "repair-omitted"],
    )
    def test_blocker_6_independent_checks(
        self, missing_key: str, expected_field: str, expected_text: str
    ) -> None:
        definition = _make_definition()
        kwargs = dict(_valid_kwargs())
        kwargs[missing_key] = None  # type: ignore[assignment]

        with pytest.raises(HarnessCompilationBlocked) as exc_info:
            compile_portable_to_intake(definition, **kwargs)

        exc = exc_info.value
        assert exc.field == expected_field
        assert expected_text in exc.reason
        assert exc.blocker_ref == "TS-APP-BRIDGE-001#blocker-6"
