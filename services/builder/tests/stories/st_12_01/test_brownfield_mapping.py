import pytest

from cmf_builder.application.brownfield_mapping import BrownfieldArtifactRecord, BrownfieldMappingError, ProvenBehaviorStatus, build_brownfield_inventory


def record(identity="artifact:1", status=ProvenBehaviorStatus.OBSERVED_NOT_PROVEN, **overrides):
    values = {
        "reference_artifact_identity": identity,
        "source_location": "repository_fixture",
        "artifact_type": "reference_profile",
        "version": "v2.1",
        "source_hash": "hash:1",
        "observed_behavior": ("compile",),
        "proven_behavior_status": status,
        "evidence_class": "REPOSITORY_OWNED_FIXTURE",
        "builder_capability": "capability:compile",
        "mapped_story": "ST-12.01",
        "mapped_obligation": "OBLIGATION-1",
        "compatibility": "development_only",
        "gap": "external_reference_pending",
        "conflict": "NONE",
        "provenance": "fixture",
        "limitations": ("not production evidence",),
    }
    values.update(overrides)
    return BrownfieldArtifactRecord(**values)


def test_inventory_maps_observed_and_missing_artifacts_without_fabricating_evidence():
    observed = record(status=ProvenBehaviorStatus.OBSERVED_NOT_PROVEN)
    missing = record("artifact:missing", ProvenBehaviorStatus.MISSING, source_hash="MISSING", observed_behavior=(), gap="reference unavailable")

    inventory = build_brownfield_inventory((missing, observed))
    assert inventory["mode"] == "BROWNFIELD_MAPPING_DEVELOPMENT"
    assert inventory["reference_evidence"] == "PENDING_OR_PARTIAL"
    assert inventory["production_migration_authority"] is False


def test_inventory_rejects_duplicate_and_misrepresented_evidence():
    with pytest.raises(BrownfieldMappingError) as duplicate:
        build_brownfield_inventory((record("same"), record("same")))
    assert duplicate.value.code == "DUPLICATE_REFERENCE_ARTIFACT"

    with pytest.raises(BrownfieldMappingError) as proven:
        record(status=ProvenBehaviorStatus.OBSERVED_AND_PROVEN, observed_behavior=())
    assert proven.value.code == "PROVEN_BEHAVIOR_REQUIRES_OBSERVATION"

    with pytest.raises(BrownfieldMappingError) as missing:
        record(status=ProvenBehaviorStatus.MISSING, source_hash="hash:fake")
    assert missing.value.code == "MISSING_ARTIFACT_CANNOT_HAVE_HASH"
