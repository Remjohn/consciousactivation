from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from cmf_builder.skills.portable_package import (
    MATURITY,
    MATURITY_CEILING,
    REQUIRED_MEMBER_PATHS,
    PortablePackageError,
    PortablePackageErrorCode,
    PortableSkillPackage,
    validate_portable_member,
)


PACKAGE_ROOT = Path(
    "skill-packages/activative_intelligence_pack_compiler/1.0.0"
)


def _load() -> PortableSkillPackage:
    return PortableSkillPackage.load(PACKAGE_ROOT)


def _copy_package(tmp_path: Path) -> Path:
    target = tmp_path / "package"
    shutil.copytree(PACKAGE_ROOT, target)
    return target


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def test_package_identity_manifest_and_receipt_are_immutable() -> None:
    package = _load()

    assert package.skill_id == "activative_intelligence_pack_compiler"
    assert package.version == "1.0.0"
    assert package.authority_lane == "Analyst"
    assert package.maturity == MATURITY == "development_uncertified"
    assert package.maturity_ceiling == MATURITY_CEILING == "development_validated"
    assert package.manifest_hash == (
        "sha256:abb88f0ab6c3797be650de420f7e5b19a66ee3417fba87b557193f87105ea982"
    )
    assert package.package_hash == (
        "sha256:6e9fbf9925a3ccaedf2bc053f4a349e69e3bff80500443c2d22b52ca40c789c6"
    )
    assert package.receipt.receipt_hash == (
        "sha256:5593591c9e8c90fccdc139cd8129a7d072b63e48361bf576404a9df740c1b0a5"
    )
    assert package.receipt.outcome == "PASS"
    assert package.receipt.production_eligible is False
    assert package.receipt.certified is False


def test_manifest_and_receipt_bytes_are_canonical() -> None:
    for relative in ("manifest.json", "PACKAGE_RECEIPT.json"):
        content = (PACKAGE_ROOT / relative).read_bytes()
        assert content == _canonical_json(json.loads(content))
        assert content.endswith(b"\n")


def test_member_set_is_exact_complete_and_canonically_ordered() -> None:
    package = _load()

    assert tuple(item.path for item in package.members) == REQUIRED_MEMBER_PATHS
    assert len(package.members) == 12
    assert package.member_set_hash == (
        "sha256:0e258972cd3b368a5c2a38c148542cb39992f5cc54457ecc559c176d4aff5c65"
    )
    for member in package.members:
        content = package.member(member.path)
        assert member.sha256 == f"sha256:{sha256(content).hexdigest()}"
        assert member.size_bytes == len(content)


def test_package_contains_active_procedure_and_required_governance() -> None:
    package = _load()
    skill = package.member("SKILL.md").decode("utf-8")
    authority = package.member("references/authority-boundaries.md").decode("utf-8")
    locks = package.member("references/wrong-reading-locks.md").decode("utf-8")
    failures = package.member("references/failure-taxonomy.md").decode("utf-8")
    observability = package.member("references/observability.md").decode("utf-8")

    assert "## Active procedure" in skill
    assert "## Completion criteria" in skill
    assert "Human identity authority owns Identity DNA" in authority
    assert "At least one non-empty wrong-reading lock is mandatory" in locks
    assert "HUMAN_TRUTH_INVENTION" in failures
    assert "package skill ID, version, manifest hash, and package hash" in observability


def test_input_contract_has_exact_frozen_semantic_fields() -> None:
    schema = json.loads(_load().member("contracts/input.schema.json"))
    assert set(schema["required"]) == {
        "source_refs",
        "authority_refs",
        "identity_dna_ref",
        "audience_context_premise_ref",
        "live_premise_evidence_refs",
        "resonance_map_ref",
        "matrix_of_edging_ref",
        "edge_pressure",
        "format_goal",
        "desired_roles",
        "activative_call_constraints",
        "desired_reaction",
        "micro_commitment",
        "wrong_reading_locks",
        "downstream_applicability",
    }
    assert schema["additionalProperties"] is False
    assert schema["properties"]["wrong_reading_locks"]["$ref"].endswith(
        "nonEmptyStringList"
    )


def test_output_contract_preserves_lineage_externality_and_readiness_ceiling() -> None:
    schema = json.loads(_load().member("contracts/output.schema.json"))
    properties = schema["properties"]

    assert schema["title"] == "ActivativeIntelligencePack"
    assert properties["human_truth_external"] == {"const": True}
    assert properties["human_reaction_external"] == {"const": True}
    assert properties["production_eligible"] == {"const": False}
    assert properties["certified"] == {"const": False}
    assert properties["maturity"]["enum"] == [
        "development_uncertified",
        "development_validated",
    ]
    assert properties["field_lineage"]["minProperties"] == 7
    assert set(properties["downstream_applicability"]["required"]) == {
        "conversational",
        "visual",
    }


def test_identical_package_reproduces_identity_in_fresh_process() -> None:
    command = (
        "from pathlib import Path; "
        "from cmf_builder.skills.portable_package import PortableSkillPackage; "
        "p=PortableSkillPackage.load(Path('skill-packages/activative_intelligence_pack_compiler/1.0.0')); "
        "print(p.package_hash, p.receipt.receipt_hash)"
    )
    environment = dict(os.environ)
    environment["PYTHONPATH"] = "src;."

    first = subprocess.run(
        [sys.executable, "-c", command],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    ).stdout
    second = subprocess.run(
        [sys.executable, "-c", command],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    ).stdout

    assert first == second
    assert "6e9fbf9925a3ccaedf2bc053f4a349e69e3bff80500443c2d22b52ca40c789c6" in first


def test_missing_member_fails_closed(tmp_path: Path) -> None:
    package = _copy_package(tmp_path)
    (package / "references/behavioral-anchors.md").unlink()

    with pytest.raises(PortablePackageError) as raised:
        PortableSkillPackage.load(package)

    assert raised.value.code is PortablePackageErrorCode.MISSING_MEMBER


def test_altered_member_fails_closed(tmp_path: Path) -> None:
    package = _copy_package(tmp_path)
    member = package / "execution/system-instructions.md"
    member.write_bytes(member.read_bytes() + b"\naltered\n")

    with pytest.raises(PortablePackageError) as raised:
        PortableSkillPackage.load(package)

    assert raised.value.code is PortablePackageErrorCode.ALTERED_MEMBER
    assert raised.value.member_path == "execution/system-instructions.md"


def test_unmanifested_member_fails_closed(tmp_path: Path) -> None:
    package = _copy_package(tmp_path)
    (package / "hidden-prompt.md").write_text("hidden", encoding="utf-8")

    with pytest.raises(PortablePackageError) as raised:
        PortableSkillPackage.load(package)

    assert raised.value.code is PortablePackageErrorCode.MISSING_MEMBER
    assert raised.value.context["unexpected"] == ["hidden-prompt.md"]


@pytest.mark.parametrize(
    "content",
    [
        b"workspace: C:\\Users\\operator\\secret.json",
        b"source: /home/operator/secret.json",
        b"source: file://local/private.json",
    ],
)
def test_absolute_or_machine_local_paths_are_rejected(content: bytes) -> None:
    with pytest.raises(PortablePackageError) as raised:
        validate_portable_member("references/candidate.md", content)

    assert raised.value.code is PortablePackageErrorCode.UNSAFE_PATH


@pytest.mark.parametrize(
    "content",
    [
        b"production_ready: true",
        b"certified = yes",
        b"maturity: shadow_ready",
    ],
)
def test_unsupported_readiness_claims_are_rejected(content: bytes) -> None:
    with pytest.raises(PortablePackageError) as raised:
        validate_portable_member("references/candidate.md", content)

    assert raised.value.code is PortablePackageErrorCode.UNSUPPORTED_CLAIM


def test_provider_coupling_is_rejected() -> None:
    with pytest.raises(PortablePackageError) as raised:
        validate_portable_member(
            "execution/candidate.md", b"provider: Anthropic"
        )

    assert raised.value.code is PortablePackageErrorCode.PROVIDER_COUPLING


@pytest.mark.parametrize(
    "relative_path",
    ["/absolute.md", "../escape.md", "nested\\windows.md", "C:/drive.md"],
)
def test_member_paths_must_be_canonical_relative_posix(relative_path: str) -> None:
    with pytest.raises(PortablePackageError) as raised:
        validate_portable_member(relative_path, b"safe content")

    assert raised.value.code is PortablePackageErrorCode.UNSAFE_PATH


def test_noncanonical_manifest_bytes_are_rejected(tmp_path: Path) -> None:
    package = _copy_package(tmp_path)
    manifest_path = package / "manifest.json"
    value = json.loads(manifest_path.read_bytes())
    manifest_path.write_text(json.dumps(value, indent=2), encoding="utf-8")

    with pytest.raises(PortablePackageError) as raised:
        PortableSkillPackage.load(package)

    assert raised.value.code is PortablePackageErrorCode.NON_CANONICAL


def test_receipt_drift_is_rejected(tmp_path: Path) -> None:
    package = _copy_package(tmp_path)
    receipt_path = package / "PACKAGE_RECEIPT.json"
    receipt = json.loads(receipt_path.read_bytes())
    receipt["member_count"] = 13
    receipt_path.write_bytes(_canonical_json(receipt))

    with pytest.raises(PortablePackageError) as raised:
        PortableSkillPackage.load(package)

    assert raised.value.code is PortablePackageErrorCode.RECEIPT_MISMATCH
