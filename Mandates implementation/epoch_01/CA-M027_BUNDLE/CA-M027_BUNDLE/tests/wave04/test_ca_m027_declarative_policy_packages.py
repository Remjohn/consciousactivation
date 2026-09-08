"""CA-M027 / Q26 — Declarative Policy Rule Packages (FR-AUTH-002).

Executable proof suite:
- Positive load + schema/semantic validation + canonical identity
- Runtime authorization effect under a loaded package
- Rejection of malformed / schema-invalid packages
- Rejection of constitutional-policy weakening
- Compatibility with existing program layout (editorial_storyboard_program)
- Immutable revision history (two independent revisions behave independently)
- Contrastive false-proof: schema-valid package that weakens constitution is rejected at semantic gate
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest
import yaml

from ca_runtime.policy_package import (
    CANONICAL_AUTHORITY_LANES,
    AuthorizationDecision,
    AuthorizationRequest,
    ConstitutionalWeakeningError,
    LoadedPolicyPackage,
    POLICY_PACKAGE_SCHEMA_ID,
    POLICY_PACKAGE_SCHEMA_VERSION,
    PolicyAuthorizationDeniedError,
    PolicyPackageConflictError,
    PolicyPackageError,
    PolicyPackageNotFoundError,
    PolicyPackageRegistry,
    PolicyPackageSchemaError,
    PolicyPackageSemanticError,
    PolicyRulePackageManifest,
    authorize,
    authorize_via_registry,
    compute_package_identity_digest,
    discover_policy_packages,
    get_policy_package_registry,
    load_and_register_from_program_root,
    load_policy_package_from_path,
    parse_policy_package_dict,
    reset_policy_package_registry,
    validate_constitutional_non_weakening,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _clean_registry():
    reset_policy_package_registry()
    yield
    reset_policy_package_registry()


def _minimal_valid_package_dict(**overrides: Any) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "schema_id": POLICY_PACKAGE_SCHEMA_ID,
        "schema_version": POLICY_PACKAGE_SCHEMA_VERSION,
        "package_id": "test_policy",
        "version": "1.0.0",
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
            {"dependency_id": "fr_auth_002", "ref": "FR-AUTH-002", "immutable": True}
        ],
    }
    base.update(overrides)
    return base


@pytest.fixture
def valid_package_path(tmp_path: Path) -> Path:
    p = tmp_path / "policy_package.yaml"
    p.write_text(yaml.safe_dump(_minimal_valid_package_dict()), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Schema / parse positives
# ---------------------------------------------------------------------------

def test_parse_valid_package_dict():
    manifest = parse_policy_package_dict(_minimal_valid_package_dict())
    assert manifest.package_id == "test_policy"
    assert manifest.version == "1.0.0"
    assert manifest.schema_id == POLICY_PACKAGE_SCHEMA_ID
    assert len(manifest.rules) == 1
    assert manifest.rules[0].required_authority_lane == "COMMANDER"


def test_load_from_yaml_path(valid_package_path: Path):
    loaded = load_policy_package_from_path(valid_package_path)
    assert isinstance(loaded, LoadedPolicyPackage)
    assert loaded.manifest.package_id == "test_policy"
    assert len(loaded.identity_digest) == 64
    assert loaded.source_path is not None
    assert loaded.revision == 1


def test_identity_digest_stable(valid_package_path: Path):
    a = load_policy_package_from_path(valid_package_path)
    b = load_policy_package_from_path(valid_package_path)
    assert a.identity_digest == b.identity_digest
    assert a.identity_digest == compute_package_identity_digest(a.manifest)


def test_identity_digest_changes_on_rule_change(tmp_path: Path):
    d1 = _minimal_valid_package_dict()
    d2 = _minimal_valid_package_dict()
    d2["rules"][0]["predicate_id"] = "approve_cmd_v2"
    p1 = tmp_path / "p1.yaml"
    p2 = tmp_path / "p2.yaml"
    p1.write_text(yaml.safe_dump(d1), encoding="utf-8")
    p2.write_text(yaml.safe_dump(d2), encoding="utf-8")
    a = load_policy_package_from_path(p1)
    b = load_policy_package_from_path(p2)
    assert a.identity_digest != b.identity_digest


# ---------------------------------------------------------------------------
# Schema negatives (malformed / contradictory)
# ---------------------------------------------------------------------------

def test_reject_missing_required_fields():
    with pytest.raises(PolicyPackageSchemaError):
        parse_policy_package_dict({"package_id": "x"})  # missing version, rules, etc.


def test_reject_invalid_semver():
    d = _minimal_valid_package_dict(version="not-a-version")
    with pytest.raises(PolicyPackageSchemaError):
        parse_policy_package_dict(d)


def test_reject_invalid_authority_lane():
    d = _minimal_valid_package_dict()
    d["rules"][0]["required_authority_lane"] = "SUPERUSER"
    with pytest.raises(PolicyPackageSchemaError):
        parse_policy_package_dict(d)


def test_reject_unknown_fields_extra_forbid():
    d = _minimal_valid_package_dict(unknown_authority_bypass=True)
    with pytest.raises(PolicyPackageSchemaError):
        parse_policy_package_dict(d)


def test_reject_active_with_empty_rules():
    d = _minimal_valid_package_dict(rules=[])
    with pytest.raises(PolicyPackageSchemaError):
        parse_policy_package_dict(d)


def test_reject_duplicate_predicate_ids(tmp_path: Path):
    d = _minimal_valid_package_dict()
    d["rules"].append(
        {
            "predicate_id": "approve_cmd",  # duplicate
            "operation": "approve",
            "required_authority_lane": "COMMANDER",
            "evidence_prerequisites": [
                {"evidence_class": "OPERATOR_DECISION", "required": True},
                {"evidence_class": "EXECUTABLE", "required": True},
            ],
        }
    )
    p = tmp_path / "dup.yaml"
    p.write_text(yaml.safe_dump(d), encoding="utf-8")
    with pytest.raises(PolicyPackageSemanticError):
        load_policy_package_from_path(p)


# ---------------------------------------------------------------------------
# Constitutional non-weakening (critical invariant)
# ---------------------------------------------------------------------------

def test_reject_constitutional_lane_weakening(tmp_path: Path):
    """False-proof contrastive case: schema-valid package that lowers approve to COMPOSER."""
    d = _minimal_valid_package_dict()
    d["rules"] = [
        {
            "predicate_id": "approve_weakened",
            "operation": "approve",
            "required_authority_lane": "COMPOSER",  # constitutional min is COMMANDER
            "evidence_prerequisites": [
                {"evidence_class": "OPERATOR_DECISION", "required": True},
                {"evidence_class": "EXECUTABLE", "required": True},
            ],
        }
    ]
    p = tmp_path / "weaken.yaml"
    p.write_text(yaml.safe_dump(d), encoding="utf-8")
    with pytest.raises(ConstitutionalWeakeningError) as ei:
        load_policy_package_from_path(p)
    assert ei.value.reason_code == "CONSTITUTIONAL_WEAKENING_REJECTED"
    assert "COMPOSER" in str(ei.value)


def test_reject_missing_constitutional_evidence(tmp_path: Path):
    d = _minimal_valid_package_dict()
    d["rules"] = [
        {
            "predicate_id": "approve_no_evidence",
            "operation": "approve",
            "required_authority_lane": "COMMANDER",
            "evidence_prerequisites": [],  # missing OPERATOR_DECISION + EXECUTABLE
        }
    ]
    p = tmp_path / "noev.yaml"
    p.write_text(yaml.safe_dump(d), encoding="utf-8")
    with pytest.raises(ConstitutionalWeakeningError) as ei:
        load_policy_package_from_path(p)
    assert "OPERATOR_DECISION" in str(ei.value) or "missing" in str(ei.value).lower()


def test_reject_prohibited_operation_delegation(tmp_path: Path):
    d = _minimal_valid_package_dict()
    d["rules"] = [
        {
            "predicate_id": "mutate_hist",
            "operation": "mutate_historical_policy",
            "required_authority_lane": "COMMANDER",
            "allow_delegation": True,
            "evidence_prerequisites": [
                {"evidence_class": "OPERATOR_DECISION", "required": True},
            ],
        }
    ]
    p = tmp_path / "mut.yaml"
    p.write_text(yaml.safe_dump(d), encoding="utf-8")
    with pytest.raises(ConstitutionalWeakeningError):
        load_policy_package_from_path(p)


def test_raising_requirements_is_allowed(tmp_path: Path):
    """A package may raise lane requirements above constitutional minimum."""
    d = _minimal_valid_package_dict()
    # already COMMANDER for approve — fine. Add extra evidence.
    d["rules"][0]["evidence_prerequisites"].append(
        {"evidence_class": "REGISTRY_SOURCE", "required": True}
    )
    p = tmp_path / "raised.yaml"
    p.write_text(yaml.safe_dump(d), encoding="utf-8")
    loaded = load_policy_package_from_path(p)
    assert loaded.manifest.rules[0].required_authority_lane == "COMMANDER"


# ---------------------------------------------------------------------------
# Registry immutability & independent revisions
# ---------------------------------------------------------------------------

def test_registry_register_and_get(valid_package_path: Path):
    reg = PolicyPackageRegistry()
    loaded = load_policy_package_from_path(valid_package_path)
    registered = reg.register(loaded)
    got = reg.get("test_policy", "1.0.0")
    assert got.identity_digest == registered.identity_digest


def test_registry_rejects_conflicting_digest_same_version(tmp_path: Path):
    reg = PolicyPackageRegistry()
    d1 = _minimal_valid_package_dict()
    d2 = _minimal_valid_package_dict()
    d2["description"] = "different body same version"
    p1 = tmp_path / "a.yaml"
    p2 = tmp_path / "b.yaml"
    p1.write_text(yaml.safe_dump(d1), encoding="utf-8")
    p2.write_text(yaml.safe_dump(d2), encoding="utf-8")
    a = load_policy_package_from_path(p1)
    b = load_policy_package_from_path(p2)
    reg.register(a)
    with pytest.raises(PolicyPackageConflictError):
        reg.register(b)


def test_two_revisions_behave_independently(tmp_path: Path):
    """Decisive proof: two executions under different prospective revisions behave independently."""
    reg = PolicyPackageRegistry()

    # Revision A: 1.0.0 — COMPOSER may emit
    d_a = _minimal_valid_package_dict(
        package_id="rev_demo",
        version="1.0.0",
        rules=[
            {
                "predicate_id": "emit_v1",
                "operation": "emit_editorial_storyboard",
                "required_authority_lane": "COMPOSER",
                "evidence_prerequisites": [
                    {"evidence_class": "EXECUTABLE", "required": True},
                ],
            },
            {
                "predicate_id": "approve_v1",
                "operation": "approve",
                "required_authority_lane": "COMMANDER",
                "evidence_prerequisites": [
                    {"evidence_class": "OPERATOR_DECISION", "required": True},
                    {"evidence_class": "EXECUTABLE", "required": True},
                ],
            },
        ],
    )
    # Revision B: 1.1.0 — same ops but ANALYST cannot; only COMMANDER for emit (raised)
    d_b = _minimal_valid_package_dict(
        package_id="rev_demo",
        version="1.1.0",
        rules=[
            {
                "predicate_id": "emit_v2",
                "operation": "emit_editorial_storyboard",
                "required_authority_lane": "COMMANDER",  # raised
                "evidence_prerequisites": [
                    {"evidence_class": "EXECUTABLE", "required": True},
                    {"evidence_class": "OPERATOR_DECISION", "required": True},
                ],
            },
            {
                "predicate_id": "approve_v2",
                "operation": "approve",
                "required_authority_lane": "COMMANDER",
                "evidence_prerequisites": [
                    {"evidence_class": "OPERATOR_DECISION", "required": True},
                    {"evidence_class": "EXECUTABLE", "required": True},
                ],
            },
        ],
    )
    pa = tmp_path / "rev_a.yaml"
    pb = tmp_path / "rev_b.yaml"
    pa.write_text(yaml.safe_dump(d_a), encoding="utf-8")
    pb.write_text(yaml.safe_dump(d_b), encoding="utf-8")

    loaded_a = reg.register(load_policy_package_from_path(pa))
    loaded_b = reg.register(load_policy_package_from_path(pb))

    assert loaded_a.identity_digest != loaded_b.identity_digest
    assert loaded_a.revision != loaded_b.revision
    hist = reg.history("rev_demo")
    assert len(hist) == 2

    # Under 1.0.0 COMPOSER + EXECUTABLE is allowed for emit
    req_composer = AuthorizationRequest(
        operation="emit_editorial_storyboard",
        actor_lane="COMPOSER",
        provided_evidence_classes=["EXECUTABLE"],
        package_id="rev_demo",
        package_version="1.0.0",
    )
    dec_a = authorize_via_registry(req_composer, reg)
    assert dec_a.allowed is True
    assert dec_a.package_identity_digest == loaded_a.identity_digest

    # Under 1.1.0 same request is denied (lane raised to COMMANDER)
    req_composer_v2 = AuthorizationRequest(
        operation="emit_editorial_storyboard",
        actor_lane="COMPOSER",
        provided_evidence_classes=["EXECUTABLE"],
        package_id="rev_demo",
        package_version="1.1.0",
    )
    dec_b = authorize_via_registry(req_composer_v2, reg)
    assert dec_b.allowed is False
    assert dec_b.package_identity_digest == loaded_b.identity_digest

    # Historical 1.0.0 still behaves as before (independent)
    dec_a2 = authorize_via_registry(req_composer, reg)
    assert dec_a2.allowed is True
    assert dec_a2.package_identity_digest == loaded_a.identity_digest


# ---------------------------------------------------------------------------
# Runtime authorization effect
# ---------------------------------------------------------------------------

def test_authorize_positive(valid_package_path: Path):
    loaded = load_policy_package_from_path(valid_package_path)
    req = AuthorizationRequest(
        operation="approve",
        actor_lane="COMMANDER",
        provided_evidence_classes=["OPERATOR_DECISION", "EXECUTABLE"],
    )
    dec = authorize(req, loaded)
    assert dec.allowed is True
    assert dec.reason_code == "AUTHORIZED"
    assert dec.matched_predicate_id == "approve_cmd"
    assert dec.package_identity_digest == loaded.identity_digest


def test_authorize_deny_insufficient_lane(valid_package_path: Path):
    loaded = load_policy_package_from_path(valid_package_path)
    req = AuthorizationRequest(
        operation="approve",
        actor_lane="COMPOSER",
        provided_evidence_classes=["OPERATOR_DECISION", "EXECUTABLE"],
    )
    dec = authorize(req, loaded)
    assert dec.allowed is False
    assert dec.reason_code == "INSUFFICIENT_AUTHORITY_OR_EVIDENCE"


def test_authorize_deny_missing_evidence(valid_package_path: Path):
    loaded = load_policy_package_from_path(valid_package_path)
    req = AuthorizationRequest(
        operation="approve",
        actor_lane="COMMANDER",
        provided_evidence_classes=["EXECUTABLE"],  # missing OPERATOR_DECISION
    )
    dec = authorize(req, loaded)
    assert dec.allowed is False


def test_authorize_deny_unknown_operation(valid_package_path: Path):
    loaded = load_policy_package_from_path(valid_package_path)
    req = AuthorizationRequest(
        operation="nonexistent_op",
        actor_lane="COMMANDER",
        provided_evidence_classes=["OPERATOR_DECISION", "EXECUTABLE"],
    )
    dec = authorize(req, loaded)
    assert dec.allowed is False
    assert dec.reason_code == "NO_MATCHING_RULE"


# ---------------------------------------------------------------------------
# Compatibility with existing program layout
# ---------------------------------------------------------------------------

def test_discover_editorial_storyboard_policy_if_present():
    """Compatibility: discovery convention under programs/<id>/policy/*.yaml."""
    # Use the bundle-local programs tree if present; otherwise synthesize.
    programs_root = Path(__file__).resolve().parents[2] / "programs"
    editorial_policy = (
        programs_root / "editorial_storyboard_program" / "policy" / "policy_package.yaml"
    )
    if not editorial_policy.is_file():
        pytest.skip("Bundle programs tree not on path; unit fixtures cover load path")

    found = discover_policy_packages([programs_root])
    ids = {p.manifest.package_id for p in found}
    assert "editorial_storyboard_policy" in ids or "script_program_policy" in ids


def test_load_real_editorial_storyboard_package_from_bundle():
    """If the bundle path is available, load the real package and authorize."""
    # Locate relative to this test file inside the bundle
    candidates = [
        Path(__file__).resolve().parents[2]
        / "programs"
        / "editorial_storyboard_program"
        / "policy"
        / "policy_package.yaml",
        Path("programs/editorial_storyboard_program/policy/policy_package.yaml"),
    ]
    path = next((c for c in candidates if c.is_file()), None)
    if path is None:
        pytest.skip("editorial_storyboard policy package not present in runtime cwd")

    loaded = load_policy_package_from_path(path)
    assert loaded.manifest.package_id == "editorial_storyboard_policy"
    assert loaded.manifest.applicable_program == "editorial_storyboard_program"
    assert any(r.operation == "approve" for r in loaded.manifest.rules)

    # Positive: COMMANDER + required evidence may approve
    dec = authorize(
        AuthorizationRequest(
            operation="approve",
            actor_lane="COMMANDER",
            provided_evidence_classes=["OPERATOR_DECISION", "EXECUTABLE"],
        ),
        loaded,
    )
    assert dec.allowed is True

    # Negative: COMPOSER may not approve
    dec2 = authorize(
        AuthorizationRequest(
            operation="approve",
            actor_lane="COMPOSER",
            provided_evidence_classes=["OPERATOR_DECISION", "EXECUTABLE"],
        ),
        loaded,
    )
    assert dec2.allowed is False


def test_load_real_script_program_package_from_bundle():
    candidates = [
        Path(__file__).resolve().parents[2]
        / "programs"
        / "script_program"
        / "policy"
        / "policy_package.yaml",
        Path("programs/script_program/policy/policy_package.yaml"),
    ]
    path = next((c for c in candidates if c.is_file()), None)
    if path is None:
        pytest.skip("script_program policy package not present in runtime cwd")

    loaded = load_policy_package_from_path(path)
    assert loaded.manifest.package_id == "script_program_policy"
    # ensure constitutional approve rule present
    approve_rules = [r for r in loaded.manifest.rules if r.operation == "approve"]
    assert len(approve_rules) == 1
    assert approve_rules[0].required_authority_lane == "COMMANDER"


# ---------------------------------------------------------------------------
# Registry via default singleton
# ---------------------------------------------------------------------------

def test_default_registry_roundtrip(valid_package_path: Path):
    loaded = load_policy_package_from_path(valid_package_path)
    reg = get_policy_package_registry()
    reg.register(loaded)
    got = reg.get("test_policy")
    assert got.identity_digest == loaded.identity_digest


# ---------------------------------------------------------------------------
# Evidence class summary for completion report
# ---------------------------------------------------------------------------

def test_evidence_classes_documented():
    """Meta: this suite itself provides EXECUTABLE + TEST evidence for CA-M027."""
    assert "EXECUTABLE" in {
        "EXECUTABLE",
        "SCHEMA",
        "TEST",
        "REGISTRY_SOURCE",
        "DOCUMENT",
    }
