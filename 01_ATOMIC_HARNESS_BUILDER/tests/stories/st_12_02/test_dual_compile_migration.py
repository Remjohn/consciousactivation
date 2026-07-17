import pytest

from cmf_builder.application.dual_compile_migration import CompatibilityResult, DualCompileMigration, MigrationError, MigrationLedger


def migration(**overrides):
    values = {
        "source_artifact": "legacy:1",
        "source_version": "v2.1",
        "source_hash": "hash:source",
        "destination_schema": "builder:v1.2",
        "source_compilation_hash": "hash:legacy-compile",
        "destination_compilation_hash": "hash:builder-compile",
        "semantic_differences": (),
        "structural_differences": ("field_order",),
        "authority_differences": (),
        "evidence_differences": (),
        "accepted_differences": ("field_order",),
        "prohibited_differences": ("semantic_flattening",),
        "compatibility_result": CompatibilityResult.COMPATIBLE_WITH_ACCEPTED_DIFFERENCES,
        "rollback_identity": "rollback:1",
        "regression_receipt": "receipt:regression",
    }
    values.update(overrides)
    return DualCompileMigration(**values)


def test_migration_is_idempotent_and_rollback_preserves_prior_state():
    ledger = MigrationLedger()
    committed = ledger.commit(migration())
    repeated = ledger.commit(migration())

    assert committed.migration_identity == repeated.migration_identity
    assert ledger.rollback(committed.migration_identity) == "rollback:1"
    assert committed.as_dict()["production_cutover"] is False


def test_migration_rejects_missing_evidence_flattening_authority_and_cutover():
    with pytest.raises(MigrationError) as missing:
        migration(source_hash="MISSING", compatibility_result=CompatibilityResult.COMPATIBLE)
    assert missing.value.code == "MISSING_SOURCE_EVIDENCE_MUST_REMAIN_MISSING"

    with pytest.raises(MigrationError) as flattening:
        migration(semantic_differences=("semantic_flattening",), accepted_differences=("semantic_flattening",))
    assert flattening.value.code == "PROHIBITED_DIFFERENCE_ACCEPTED"

    with pytest.raises(MigrationError) as authority:
        migration(authority_differences=("external_owner_changed",), compatibility_result=CompatibilityResult.COMPATIBLE)
    assert authority.value.code == "AUTHORITY_DIFFERENCE_NOT_COMPATIBLE"

    with pytest.raises(MigrationError) as cutover:
        migration(production_cutover=True)
    assert cutover.value.code == "PRODUCTION_CUTOVER_PROHIBITED"
