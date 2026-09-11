from __future__ import annotations

from typing import Any, Mapping

from cmf_builder.domain.portable_export import PortableAtomicHarnessDefinition

from ..domain.errors import PipelineValidationError
from ..domain.validation import require_semver
from .compiler_profile_registry import HarnessDefinitionProfileRegistry
from .harness_compiler_contracts import (
    BLOCKER_1_TEXT,
    BLOCKER_2_TEXT,
    BLOCKER_3_TEXT,
    BLOCKER_4_TEXT,
    BLOCKER_5_TEXT,
    BLOCKER_6_EVAL_TEXT,
    BLOCKER_6_REPAIR_TEXT,
    HarnessCompilationBlocked,
)

_profile_registry = HarnessDefinitionProfileRegistry()


def compile_portable_to_intake(
    definition: PortableAtomicHarnessDefinition,
    *,
    semantic_dependencies: list[dict[str, str]] | None = None,
    capability_metadata: dict[str, dict[str, object]] | None = None,
    workflow: dict[str, object] | None = None,
    evaluation_requirements: list[str] | None = None,
    repair_laws: list[str] | None = None,
) -> dict[str, Any]:
    content = definition.content

    # Blocker 3 — mode gate
    if content["mode"] != "activative":
        raise HarnessCompilationBlocked(
            field="category_id",
            reason=BLOCKER_3_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-3",
        )
    category_binding = content["category_binding"]
    category_id = category_binding["category_id"]

    # Blocker 4 — semver gate (reuses Pipeline's own validator, not reimplemented)
    manifest_version = content["manifest_version"]
    try:
        definition_version = require_semver(manifest_version, "manifest_version")
    except PipelineValidationError as exc:
        raise HarnessCompilationBlocked(
            field="definition_version",
            reason=BLOCKER_4_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-4",
        ) from exc

    # profile_id — clean, deterministic derivation via existing Pipeline registry
    profile = _profile_registry.resolve(f"portable_{content['mode']}_v1")

    # Blocker 1 — semantic_dependencies must be caller-supplied
    if semantic_dependencies is None:
        raise HarnessCompilationBlocked(
            field="semantic_dependencies",
            reason=BLOCKER_1_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-1",
        )

    # Blocker 2 — capability_metadata must cover every required capability_id
    capability_ids: list[str] = list(content["capability_requirements"])
    if capability_metadata is None:
        raise HarnessCompilationBlocked(
            field="capabilities",
            reason=BLOCKER_2_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-2",
        )
    missing = sorted(set(capability_ids) - set(capability_metadata))
    if missing:
        raise HarnessCompilationBlocked(
            field="capabilities",
            reason=f"{BLOCKER_2_TEXT}; missing metadata for: {missing}",
            blocker_ref="TS-APP-BRIDGE-001#blocker-2",
        )
    capabilities = [
        {
            "capability_id": cap_id,
            "owner_kind": capability_metadata[cap_id]["owner_kind"],
            "required_features": capability_metadata[cap_id]["required_features"],
            "authority_boundary": capability_metadata[cap_id]["authority_boundary"],
        }
        for cap_id in capability_ids
    ]

    # Blocker 5 — workflow must be caller-supplied; this compiler never derives it
    if workflow is None:
        raise HarnessCompilationBlocked(
            field="workflow",
            reason=BLOCKER_5_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-5",
        )

    # Blocker 6 — evaluation_requirements / repair_laws must be caller-supplied
    if evaluation_requirements is None:
        raise HarnessCompilationBlocked(
            field="evaluation_requirements",
            reason=BLOCKER_6_EVAL_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-6",
        )
    if repair_laws is None:
        raise HarnessCompilationBlocked(
            field="repair_laws",
            reason=BLOCKER_6_REPAIR_TEXT,
            blocker_ref="TS-APP-BRIDGE-001#blocker-6",
        )

    # wrong_reading_locks — clean derivation from category_binding (activative mode only,
    # always present here)
    wrong_reading_locks = list(category_binding["wrong_reading_locks"])

    # Blocker 7 — invalidation_state defaults to NOT_INVALIDATED for fresh compilation
    invalidation_state = "NOT_INVALIDATED"

    return {
        "definition_id": definition.definition_id,
        "definition_version": definition_version,
        "category_id": category_id,
        "profile_id": profile.profile_id,
        "purpose": content["goal"],
        "semantic_dependencies": semantic_dependencies,
        "capabilities": capabilities,
        "workflow": workflow,
        "evaluation_requirements": evaluation_requirements,
        "repair_laws": repair_laws,
        "wrong_reading_locks": wrong_reading_locks,
        "production_ready": content["production_eligible"],
        "certified": content["certified"],
        "invalidation_state": invalidation_state,
    }
