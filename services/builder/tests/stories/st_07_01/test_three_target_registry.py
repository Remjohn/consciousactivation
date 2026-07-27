from __future__ import annotations

from dataclasses import replace
from hashlib import sha256

from cmf_builder.domain.category_syntax import GovernedRef
from cmf_builder.domain.compilation_targets import (
    DELEGATION_TRUST,
    DELEGATION_VERSION,
    EXTERNAL_VALIDATION_PENDING,
    TARGET_IDS,
    CompilationTargetProfile,
    compile_target_registry,
)


def ref(role: str, suffix: str, *, version: str = "1.0.0", authority: str = "target-code") -> GovernedRef:
    return GovernedRef(
        object_id=f"{role}-{suffix}",
        version=version,
        sha256=sha256(f"{role}:{suffix}:{version}".encode()).hexdigest(),
        authority=authority,
        lineage_role=role,
    )


def profile(target_id: str, *, version: str = "1.0.0") -> CompilationTargetProfile:
    boundaries = {
        "atomic_content_harness": (
            "Atomic Harness Builder",
            "compiled_harness_owner_not_ST_07_01",
            "BUILDER_LOCAL_STRUCTURAL",
            None,
            ("category_profile_extension", "activative_intelligence_extension"),
            ("no_external_runtime", "no_external_authority_borrowing"),
        ),
        "visual_asset_editor": (
            "Visual Asset Editor product authority",
            "external_visual_asset_editor",
            EXTERNAL_VALIDATION_PENDING,
            ref("vae_interface_snapshot", "v1", authority="Visual Asset Editor product authority"),
            ("visual_semantic_mapping", "visual_narrative_mapping"),
            ("no_image_generation", "no_external_runtime", "no_semantic_mutation"),
        ),
        "content_asset_delegation_contract": (
            "Delegation Protocol product authority",
            "external_delegation_protocol",
            EXTERNAL_VALIDATION_PENDING,
            ref("delegation_interface_snapshot", "rc4", version=DELEGATION_VERSION, authority="Delegation Protocol product authority"),
            (DELEGATION_TRUST, "delegation_rc4_mapping"),
            ("no_shared_schema_ownership", "no_transport", "no_runtime"),
        ),
    }
    owner, execution, compatibility, snapshot, extensions, prohibitions = boundaries[target_id]
    authority = ref("target_authority", "v1")
    return CompilationTargetProfile(
        target_id=target_id,
        target_version=version,
        product_owner=owner,
        execution_owner=execution,
        source_profile_ref=ref("source_profile", target_id),
        ir_projection_ref=ref("ir_projection", target_id),
        genesis_graph_ref=ref("genesis_graph", target_id),
        compiler_ref=ref("compiler", target_id),
        artifact_set_ref=ref("artifact_set", target_id),
        evaluation_gate_ref=ref("evaluation_gate", target_id),
        compatibility_state=compatibility,
        certification_scope="UNCERTIFIED_DEVELOPMENT_ONLY",
        required_extensions=extensions,
        explicit_prohibitions=prohibitions,
        interface_snapshot_ref=snapshot,
        authority_ref=authority,
        provenance=(ref("source_provenance", target_id),),
    )


def registry(*, version: str = "1.0.0", profiles=None):
    values = tuple(profile(target_id) for target_id in TARGET_IDS) if profiles is None else profiles
    return compile_target_registry(
        registry_id="compilation-target-registry",
        registry_version=version,
        profiles=values,
        authority_ref=ref("target_authority", "v1"),
    )


def test_registry_contains_exactly_three_distinct_targets() -> None:
    result = registry()
    assert tuple(item.target_id for item in result.profiles) == tuple(sorted(TARGET_IDS))
    assert len(result.profiles) == 3
    assert result.production_ready is False
    assert result.certified is False
    assert result.canonical_dict()["universal_target_supported"] is False


def test_each_target_preserves_distinct_ownership_evidence_and_compatibility() -> None:
    profiles = {item.target_id: item for item in registry().profiles}
    assert len({item.product_owner for item in profiles.values()}) == 3
    assert profiles["atomic_content_harness"].interface_snapshot_ref is None
    assert profiles["atomic_content_harness"].compatibility_state == "BUILDER_LOCAL_STRUCTURAL"
    assert profiles["visual_asset_editor"].compatibility_state == EXTERNAL_VALIDATION_PENDING
    delegation = profiles["content_asset_delegation_contract"]
    assert delegation.interface_snapshot_ref.version == DELEGATION_VERSION
    assert DELEGATION_TRUST in delegation.required_extensions


def test_category_identity_is_not_a_target_alias() -> None:
    assert "conversational_activation_expression" not in TARGET_IDS
    assert "2d_character_animation" not in TARGET_IDS


def test_registry_identity_is_order_independent_and_byte_deterministic() -> None:
    values = tuple(profile(target_id) for target_id in TARGET_IDS)
    first = registry(profiles=values)
    second = registry(profiles=tuple(reversed(values)))
    assert first.registry_hash == second.registry_hash
    assert first.canonical_bytes == second.canonical_bytes


def test_changed_profile_creates_changed_registry_identity() -> None:
    values = tuple(profile(target_id) for target_id in TARGET_IDS)
    changed = tuple(
        replace(item, target_version="1.1.0") if item.target_id == "atomic_content_harness" else item
        for item in values
    )
    assert registry(profiles=values).registry_hash != registry(version="1.1.0", profiles=changed).registry_hash
