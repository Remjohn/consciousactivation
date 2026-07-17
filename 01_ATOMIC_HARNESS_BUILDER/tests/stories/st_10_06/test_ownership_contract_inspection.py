import pytest

from cmf_builder.application.ownership_contract_inspection import (
    OwnershipInspectionError,
    OwnershipObjectClass,
    OwnershipRecord,
    inspect_ownership,
    validate_ownership_records,
)


def record(identity="module:application", object_class=OwnershipObjectClass.MODULE, **overrides):
    values = {
        "identity": identity,
        "object_class": object_class,
        "owning_product": "Atomic Harness Builder",
        "owning_module": "application",
        "responsibility": "projection",
        "allowed_dependencies": ("domain",),
        "prohibited_dependencies": ("vae_runtime", "delegation_runtime"),
        "inbound_ports": ("query",),
        "outbound_ports": ("repository",),
        "adapters": (),
        "contract_version": "v1",
        "compatibility": "compatible",
        "implementation_paths": ("src/cmf_builder/application/run_index_projection.py",),
        "story_ownership": "ST-10.06",
        "obligation_ownership": "OBLIGATION-1",
        "external_ownership": "NONE",
        "authority_basis": "OD-AM-004",
        "source_evidence": ("receipt:st-10.01",),
        "validity": "ACTIVE",
        "supersession": "NONE",
        "limitations": ("offline development",),
    }
    values.update(overrides)
    return OwnershipRecord(**values)


def test_ownership_records_validate_against_registry_and_query_surfaces():
    records = (
        record(),
        record("contract:app", OwnershipObjectClass.APPLICATION_CONTRACT, owning_module="application", implementation_paths=("src/cmf_builder/application/run_index_projection.py",)),
    )
    validate_ownership_records(records, {"src/cmf_builder/application/run_index_projection.py"})

    assert inspect_ownership(records, module="application")
    assert inspect_ownership(records, source_path="src/cmf_builder/application/run_index_projection.py")
    assert inspect_ownership(records, story="ST-10.06")


def test_duplicate_ownership_unregistered_source_and_unowned_module_fail():
    with pytest.raises(OwnershipInspectionError) as source:
        validate_ownership_records((record(),), set())
    assert source.value.code == "SOURCE_OUTSIDE_GOVERNED_REGISTRY"

    records = (record("module:a", primary_obligation_owner=True), record("module:b", primary_obligation_owner=True))
    with pytest.raises(OwnershipInspectionError) as duplicate:
        validate_ownership_records(records, {"src/cmf_builder/application/run_index_projection.py"})
    assert duplicate.value.code == "DUPLICATE_PRIMARY_OBLIGATION_OWNER"

    with pytest.raises(OwnershipInspectionError) as unowned:
        validate_ownership_records((record("contract:x", OwnershipObjectClass.APPLICATION_CONTRACT, owning_module="missing"),), {"src/cmf_builder/application/run_index_projection.py"})
    assert unowned.value.code == "UNOWNED_MODULE"


def test_external_product_claims_adapter_authority_and_prohibited_dependencies_fail():
    with pytest.raises(OwnershipInspectionError) as external:
        record(external_ownership="VAE")
    assert external.value.code == "EXTERNAL_PRODUCT_OWNERSHIP_CLAIMED_BY_BUILDER"

    with pytest.raises(OwnershipInspectionError) as adapter:
        record("adapter:bad", OwnershipObjectClass.ADAPTER, claims_human_authority=True)
    assert adapter.value.code == "ADAPTER_PRESENTED_AS_AUTHORITY"

    with pytest.raises(OwnershipInspectionError) as dep:
        validate_ownership_records((record(allowed_dependencies=("vae_runtime",)),), {"src/cmf_builder/application/run_index_projection.py"})
    assert dep.value.code == "PROHIBITED_DEPENDENCY_ALLOWED"
