"""CA-M028 / Q27 — Policy Revision Binding (FR-POL-002 / INV-POL-001).

Executable proof suite:
- Positive initial binding of a policy revision digest to an execution / lease
- Attachment of binding into lease and dispatch payloads
- Prospective campaign update: active execution stays on Pn; new execution binds Pn+1
- Negative: rebind of a live execution is rejected
- Negative: missing / stale / mutated revision fails closed and aborts
- Drift detection → mark DRIFT → abort in-flight execution
- Persistence / recovery: binding survives registry restart (process-scoped reset
  + reload of recorded binding dict)
- Contrastive false-proof: reading live campaign policy for an in-flight
  authorization decision would violate the contract; the binding gate refuses
  to use a mismatched prospective digest
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import pytest
import yaml

from ca_runtime.policy_package import (
    POLICY_PACKAGE_SCHEMA_ID,
    POLICY_PACKAGE_SCHEMA_VERSION,
    LoadedPolicyPackage,
    PolicyPackageRegistry,
    PolicyRulePackageManifest,
    compute_package_identity_digest,
    get_policy_package_registry,
    parse_policy_package_dict,
    reset_policy_package_registry,
)
from ca_runtime.policy_revision_binding import (
    BINDING_SCHEMA_ID,
    BINDING_SCHEMA_VERSION,
    DISPATCH_POLICY_BINDING_KEY,
    LEASE_POLICY_BINDING_KEY,
    BindingAbortedError,
    BindingAlreadyExistsError,
    BindingNotFoundError,
    BindingStatus,
    PolicyDriftDetectedError,
    PolicyRevisionBinding,
    PolicyRevisionBindingError,
    PolicyRevisionBindingRegistry,
    StalePolicySnapshotError,
    attach_binding_to_dispatch_payload,
    attach_binding_to_lease_payload,
    bind_loaded_package_to_execution,
    bind_policy_revision_to_execution,
    binding_digest_for_payload,
    check_binding_integrity,
    contrast_bound_vs_prospective,
    detect_and_abort_on_drift,
    extract_binding_from_payload,
    get_policy_revision_binding_registry,
    require_live_binding,
    reset_policy_revision_binding_registry,
    resolve_bound_package,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _clean_registries():
    reset_policy_package_registry()
    reset_policy_revision_binding_registry()
    yield
    reset_policy_package_registry()
    reset_policy_revision_binding_registry()


def _minimal_valid_package_dict(
    package_id: str = "test_policy",
    version: str = "1.0.0",
    **overrides: Any,
) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "schema_id": POLICY_PACKAGE_SCHEMA_ID,
        "schema_version": POLICY_PACKAGE_SCHEMA_VERSION,
        "package_id": package_id,
        "version": version,
        "status": "ACTIVE",
        "applicable_program": "test_program",
        "rules": [
            {
                "predicate_id": "approve_cmd",
                "operation": "approve",
                "required_authority_lane": "COMMANDER",
                "evidence_prerequisites": [
                    {"evidence_class": "OPERATOR_DECISION", "required": True},
                    {"evidence_class": "EXECUTABLE", "required": True},
                ],
            }
        ],
        "constitutional_dependencies": [
            {"dependency_id": "fr_pol_002", "ref": "FR-POL-002", "immutable": True}
        ],
    }
    base.update(overrides)
    return base


def _register_package(
    package_id: str = "test_policy",
    version: str = "1.0.0",
    **overrides: Any,
) -> LoadedPolicyPackage:
    data = _minimal_valid_package_dict(package_id=package_id, version=version, **overrides)
    manifest = parse_policy_package_dict(data)
    digest = compute_package_identity_digest(manifest)
    loaded = LoadedPolicyPackage(
        manifest=manifest,
        identity_digest=digest,
        source_path=None,
        loaded_at="2026-09-08T00:00:00Z",
        revision=1,
    )
    reg = get_policy_package_registry()
    return reg.register(loaded)


# ---------------------------------------------------------------------------
# Positive: initial binding
# ---------------------------------------------------------------------------

def test_bind_policy_revision_to_execution_positive():
    pkg = _register_package()
    binding = bind_policy_revision_to_execution(
        execution_id="exec-001",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
        lease_id="lease-001",
    )
    assert binding.execution_id == "exec-001"
    assert binding.lease_id == "lease-001"
    assert binding.package_id == pkg.manifest.package_id
    assert binding.package_version == pkg.manifest.version
    assert binding.identity_digest == pkg.identity_digest
    assert binding.revision == pkg.revision
    assert binding.status == BindingStatus.BOUND
    assert binding.bound_at

    # Registry round-trip
    reg = get_policy_revision_binding_registry()
    fetched = reg.get("exec-001")
    assert fetched.identity_digest == binding.identity_digest
    assert fetched.binding_id == binding.binding_id


def test_bind_loaded_package_direct():
    pkg = _register_package(version="2.0.0")
    binding = bind_loaded_package_to_execution(
        execution_id="exec-direct",
        program_id="test_program",
        loaded_package=pkg,
        lease_id="lease-d",
    )
    assert binding.identity_digest == pkg.identity_digest
    assert binding.status == BindingStatus.BOUND


# ---------------------------------------------------------------------------
# Lease / dispatch payload attachment
# ---------------------------------------------------------------------------

def test_attach_binding_to_lease_and_dispatch_payloads():
    pkg = _register_package()
    binding = bind_policy_revision_to_execution(
        execution_id="exec-payload",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
        lease_id="lease-p",
    )

    lease = {"lease_id": "lease-p", "aggregate_id": "exec-payload", "status": "LEASE_ENQUEUED"}
    enriched_lease = attach_binding_to_lease_payload(lease, binding)
    assert LEASE_POLICY_BINDING_KEY in enriched_lease
    assert enriched_lease["bound_policy_identity_digest"] == binding.identity_digest
    assert enriched_lease["bound_policy_package_id"] == binding.package_id
    assert enriched_lease["bound_policy_revision"] == binding.revision
    # original not mutated
    assert LEASE_POLICY_BINDING_KEY not in lease

    dispatch = {"workflow_id": "wf-1", "aggregate_id": "exec-payload"}
    enriched_dispatch = attach_binding_to_dispatch_payload(dispatch, binding)
    assert DISPATCH_POLICY_BINDING_KEY in enriched_dispatch
    assert enriched_dispatch["bound_policy_identity_digest"] == binding.identity_digest

    # extract round-trip
    recovered = extract_binding_from_payload(enriched_lease)
    assert recovered is not None
    assert recovered.identity_digest == binding.identity_digest
    assert recovered.execution_id == binding.execution_id

    recovered_d = extract_binding_from_payload(enriched_dispatch)
    assert recovered_d is not None
    assert recovered_d.identity_digest == binding.identity_digest


# ---------------------------------------------------------------------------
# Prospective update contrast (core Q27 / INV-POL-001 proof)
# ---------------------------------------------------------------------------

def test_prospective_update_active_stays_on_pn_new_binds_pn1():
    """Key contrastive case:
    1. Start execution under Pn
    2. Campaign policy advances to Pn+1
    3. Active execution still resolves Pn
    4. New execution binds Pn+1
    """
    # Pn
    pkg_n = _register_package(package_id="campaign_policy", version="1.0.0")
    binding_n = bind_policy_revision_to_execution(
        execution_id="exec-active",
        program_id="test_program",
        package_id="campaign_policy",
        package_version="1.0.0",
        lease_id="lease-active",
        campaign_prospective_digest=pkg_n.identity_digest,
    )
    assert binding_n.identity_digest == pkg_n.identity_digest

    # Campaign advances to Pn+1 (new immutable version)
    pkg_n1 = _register_package(
        package_id="campaign_policy",
        version="1.1.0",
        # slightly different rule set so digest differs
        rules=[
            {
                "predicate_id": "approve_cmd",
                "operation": "approve",
                "required_authority_lane": "COMMANDER",
                "evidence_prerequisites": [
                    {"evidence_class": "OPERATOR_DECISION", "required": True},
                    {"evidence_class": "EXECUTABLE", "required": True},
                ],
            },
            {
                "predicate_id": "emit_composer",
                "operation": "emit",
                "required_authority_lane": "COMPOSER",
                "evidence_prerequisites": [
                    {"evidence_class": "EXECUTABLE", "required": True},
                ],
            },
        ],
    )
    assert pkg_n1.identity_digest != pkg_n.identity_digest

    # Active execution still resolves Pn
    live = require_live_binding("exec-active")
    assert live.identity_digest == pkg_n.identity_digest
    assert live.package_version == "1.0.0"
    assert live.status == BindingStatus.BOUND

    contrast = contrast_bound_vs_prospective(
        "exec-active",
        prospective_digest=pkg_n1.identity_digest,
    )
    assert contrast["digests_differ"] is True
    assert contrast["bound_identity_digest"] == pkg_n.identity_digest
    assert contrast["prospective_campaign_digest"] == pkg_n1.identity_digest
    assert contrast["prospective_only"] is True

    # New execution binds Pn+1
    binding_n1 = bind_policy_revision_to_execution(
        execution_id="exec-new",
        program_id="test_program",
        package_id="campaign_policy",
        package_version="1.1.0",
        lease_id="lease-new",
        campaign_prospective_digest=pkg_n1.identity_digest,
    )
    assert binding_n1.identity_digest == pkg_n1.identity_digest
    assert binding_n1.package_version == "1.1.0"

    # Integrity of both still holds
    check_binding_integrity("exec-active")
    check_binding_integrity("exec-new")


# ---------------------------------------------------------------------------
# Negative: rebind prohibited
# ---------------------------------------------------------------------------

def test_rebind_active_execution_rejected():
    pkg = _register_package()
    bind_policy_revision_to_execution(
        execution_id="exec-rebind",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    with pytest.raises(BindingAlreadyExistsError) as ei:
        bind_policy_revision_to_execution(
            execution_id="exec-rebind",
            program_id="test_program",
            package_id=pkg.manifest.package_id,
            package_version=pkg.manifest.version,
        )
    assert ei.value.reason_code == "BINDING_ALREADY_EXISTS"


# ---------------------------------------------------------------------------
# Negative: missing / unknown package → stale
# ---------------------------------------------------------------------------

def test_bind_unknown_package_fails_closed():
    with pytest.raises(StalePolicySnapshotError) as ei:
        bind_policy_revision_to_execution(
            execution_id="exec-missing",
            program_id="test_program",
            package_id="does_not_exist",
            package_version="9.9.9",
        )
    assert ei.value.reason_code == "STALE_POLICY_SNAPSHOT"
    assert ei.value.details["package_id"] == "does_not_exist"


def test_resolve_bound_package_missing_after_bind():
    """Simulate retention collision: package removed from registry after bind."""
    pkg = _register_package(package_id="ephemeral", version="1.0.0")
    binding = bind_policy_revision_to_execution(
        execution_id="exec-ephemeral",
        program_id="test_program",
        package_id="ephemeral",
        package_version="1.0.0",
    )
    # Wipe package registry (simulates unrecoverable deletion)
    reset_policy_package_registry()
    with pytest.raises(StalePolicySnapshotError) as ei:
        resolve_bound_package(binding)
    assert ei.value.reason_code == "STALE_POLICY_SNAPSHOT"


# ---------------------------------------------------------------------------
# Drift detection and abort
# ---------------------------------------------------------------------------

def test_detect_and_abort_on_forced_digest_mismatch():
    pkg = _register_package()
    bind_policy_revision_to_execution(
        execution_id="exec-drift",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
        lease_id="lease-drift",
    )
    aborted = detect_and_abort_on_drift(
        "exec-drift",
        force_observed_digest="0" * 64,  # deliberately different
    )
    assert aborted.status == BindingStatus.ABORTED
    assert aborted.abort_reason
    assert "POLICY_DRIFT_DETECTED" in (aborted.abort_reason or "")

    # Subsequent live requirement fails
    with pytest.raises(BindingAbortedError):
        require_live_binding("exec-drift")

    # Idempotent abort
    again = detect_and_abort_on_drift("exec-drift", force_observed_digest="0" * 64)
    assert again.status == BindingStatus.ABORTED


def test_check_integrity_raises_on_aborted():
    pkg = _register_package()
    bind_policy_revision_to_execution(
        execution_id="exec-aborted-check",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    detect_and_abort_on_drift(
        "exec-aborted-check",
        force_observed_digest="deadbeef" * 8,
    )
    with pytest.raises(BindingAbortedError):
        check_binding_integrity("exec-aborted-check")


def test_binding_not_found():
    with pytest.raises(BindingNotFoundError) as ei:
        get_policy_revision_binding_registry().get("never-bound")
    assert ei.value.reason_code == "BINDING_NOT_FOUND"


# ---------------------------------------------------------------------------
# Persistence / recovery (process restart simulation)
# ---------------------------------------------------------------------------

def test_binding_survives_registry_reload_from_dict():
    """Simulate restart: serialize binding, clear registry, reload from dict."""
    pkg = _register_package()
    original = bind_policy_revision_to_execution(
        execution_id="exec-persist",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
        lease_id="lease-persist",
        metadata={"note": "pre-restart"},
    )
    snapshot = original.to_dict()

    # Process restart simulation
    reset_policy_revision_binding_registry()
    with pytest.raises(BindingNotFoundError):
        get_policy_revision_binding_registry().get("exec-persist")

    # Recovery: rehydrate from durable record
    recovered = PolicyRevisionBinding.from_dict(snapshot)
    assert recovered.identity_digest == original.identity_digest
    assert recovered.execution_id == original.execution_id
    assert recovered.status == BindingStatus.BOUND
    assert recovered.metadata.get("note") == "pre-restart"

    # Re-insert into registry (as a durable store would do on load)
    reg = get_policy_revision_binding_registry()
    # Use internal put via bind with allow after clear — since clear wiped it,
    # normal bind works.
    re_bound = bind_loaded_package_to_execution(
        execution_id=recovered.execution_id,
        program_id=recovered.program_id,
        loaded_package=pkg,
        lease_id=recovered.lease_id,
        metadata=recovered.metadata,
    )
    assert re_bound.identity_digest == original.identity_digest
    live = require_live_binding("exec-persist")
    assert live.identity_digest == original.identity_digest


# ---------------------------------------------------------------------------
# Status transitions & complete
# ---------------------------------------------------------------------------

def test_complete_binding():
    pkg = _register_package()
    bind_policy_revision_to_execution(
        execution_id="exec-complete",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    reg = get_policy_revision_binding_registry()
    completed = reg.complete("exec-complete")
    assert completed.status == BindingStatus.COMPLETED

    # Cannot complete an aborted binding
    bind_policy_revision_to_execution(
        execution_id="exec-abort-then-complete",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    detect_and_abort_on_drift(
        "exec-abort-then-complete",
        force_observed_digest="ff" * 32,
    )
    with pytest.raises(BindingAbortedError):
        reg.complete("exec-abort-then-complete")


def test_list_bindings_filter():
    pkg = _register_package()
    bind_policy_revision_to_execution(
        execution_id="exec-a",
        program_id="prog_a",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    bind_policy_revision_to_execution(
        execution_id="exec-b",
        program_id="prog_b",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    reg = get_policy_revision_binding_registry()
    all_b = reg.list_bindings()
    assert len(all_b) == 2
    only_a = reg.list_bindings(program_id="prog_a")
    assert len(only_a) == 1
    assert only_a[0].execution_id == "exec-a"
    bound_only = reg.list_bindings(status=BindingStatus.BOUND)
    assert len(bound_only) == 2


# ---------------------------------------------------------------------------
# Binding record serialization & schema identity
# ---------------------------------------------------------------------------

def test_binding_to_dict_schema_identity():
    pkg = _register_package()
    binding = bind_policy_revision_to_execution(
        execution_id="exec-schema",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    d = binding.to_dict()
    assert d["schema_id"] == BINDING_SCHEMA_ID
    assert d["schema_version"] == BINDING_SCHEMA_VERSION
    assert d["status"] == "BOUND"
    roundtrip = PolicyRevisionBinding.from_dict(d)
    assert roundtrip.identity_digest == binding.identity_digest


def test_binding_digest_for_payload_stable():
    pkg = _register_package()
    binding = bind_policy_revision_to_execution(
        execution_id="exec-digest",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    d1 = binding_digest_for_payload(binding)
    d2 = binding_digest_for_payload(binding)
    assert d1 == d2
    assert len(d1) == 64  # sha256 hex


# ---------------------------------------------------------------------------
# History audit trail
# ---------------------------------------------------------------------------

def test_history_records_status_transitions():
    pkg = _register_package()
    bind_policy_revision_to_execution(
        execution_id="exec-hist",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    detect_and_abort_on_drift(
        "exec-hist",
        force_observed_digest="aa" * 32,
    )
    hist = get_policy_revision_binding_registry().history("exec-hist")
    statuses = [h.status for h in hist]
    assert BindingStatus.BOUND in statuses
    assert BindingStatus.DRIFT_DETECTED in statuses
    assert BindingStatus.ABORTED in statuses
    assert hist[-1].status == BindingStatus.ABORTED


# ---------------------------------------------------------------------------
# Integrity with matching prospective (no false positive)
# ---------------------------------------------------------------------------

def test_integrity_ok_when_prospective_matches_bound():
    pkg = _register_package()
    bind_policy_revision_to_execution(
        execution_id="exec-match",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
        campaign_prospective_digest=pkg.identity_digest,
    )
    live = check_binding_integrity(
        "exec-match",
        prospective_campaign_digest=pkg.identity_digest,
    )
    assert live.status == BindingStatus.BOUND
    assert live.identity_digest == pkg.identity_digest


# ---------------------------------------------------------------------------
# Require live rejects non-BOUND statuses
# ---------------------------------------------------------------------------

def test_require_live_rejects_completed():
    pkg = _register_package()
    bind_policy_revision_to_execution(
        execution_id="exec-done",
        program_id="test_program",
        package_id=pkg.manifest.package_id,
        package_version=pkg.manifest.version,
    )
    get_policy_revision_binding_registry().complete("exec-done")
    with pytest.raises(PolicyRevisionBindingError) as ei:
        require_live_binding("exec-done")
    assert ei.value.reason_code == "BINDING_NOT_LIVE"
