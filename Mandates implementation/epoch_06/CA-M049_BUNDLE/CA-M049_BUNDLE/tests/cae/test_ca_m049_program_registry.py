"""CA-M049 / INV-REG-001 — Program Registry Immutability Requirement."""
from __future__ import annotations
from pathlib import Path
from types import MappingProxyType
import pytest
import yaml
from ca_runtime.program_registry import (
    IMMUTABLE_STATUSES,
    ProgramConflictError,
    ProgramDigestMismatchError,
    ProgramImmutabilityError,
    ProgramManifest,
    ProgramNotFoundError,
    ProgramPackage,
    ProgramRegistry,
    ProgramStatus,
)

def _write_minimal_package(
    root: Path,
    *,
    program_id: str = "imm_test_program",
    version: str = "1.0.0",
    status: str = "DRAFT",
    purpose: str = "CA-M049 immutability test package",
    extra_file_content: str = "payload-v1",
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "id": program_id, "version": version, "status": status, "purpose": purpose,
        "lanes": ["HUNTER"], "skills": [], "operations": [], "inputs": [],
        "outputs": [], "preconditions": [], "artifacts": [],
    }
    (root / "program_manifest.yaml").write_text(yaml.dump(manifest), encoding="utf-8")
    (root / "payload.txt").write_text(extra_file_content, encoding="utf-8")
    return root

@pytest.fixture
def registry() -> ProgramRegistry:
    return ProgramRegistry()

@pytest.fixture
def pkg_dir(tmp_path: Path) -> Path:
    return _write_minimal_package(tmp_path / "imm_test_program")

class TestGate1_FirstRegistrationPinsDigests:
    def test_register_new_identity_succeeds_and_pins(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        assert len(pkg.manifest_sha256) == 64
        assert len(pkg.package_sha256) == 64
        registry.register(pkg)
        stored = registry.get_program("imm_test_program", "1.0.0")
        assert stored.manifest_sha256 == pkg.manifest_sha256
        pins = registry.get_pinned_digests("imm_test_program", "1.0.0")
        assert isinstance(pins, MappingProxyType)
        assert pins["package_sha256"] == pkg.package_sha256

    def test_duplicate_register_without_overwrite_raises_conflict(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        draft = pkg.with_status(ProgramStatus.DRAFT)
        registry.register(draft)
        with pytest.raises(ProgramConflictError) as exc:
            registry.register(draft, allow_overwrite=False)
        assert exc.value.reason_code == "PROGRAM_CONFLICT"

class TestGate2_ReleasePreservesPins:
    def test_release_promotes_status_and_keeps_digests(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        draft = pkg.with_status(ProgramStatus.DRAFT)
        registry.register(draft)
        m_sha, p_sha = draft.manifest_sha256, draft.package_sha256
        released = registry.release("imm_test_program", "1.0.0")
        assert released.manifest.status == ProgramStatus.RELEASED
        assert released.manifest_sha256 == m_sha
        assert released.package_sha256 == p_sha
        assert released.is_immutable() is True
        again = registry.release("imm_test_program", "1.0.0")
        assert again.manifest_sha256 == m_sha

class TestGate3_SameVersionOverwriteRejected:
    def test_overwrite_released_rejected_even_with_allow_overwrite(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.register(pkg.with_status(ProgramStatus.DRAFT))
        registry.release("imm_test_program", "1.0.0")
        (pkg_dir / "payload.txt").write_text("payload-TAMPERED", encoding="utf-8")
        tampered = registry.inspect_and_validate_package(pkg_dir)
        assert tampered.package_sha256 != pkg.package_sha256
        with pytest.raises(ProgramImmutabilityError) as exc:
            registry.register(tampered, allow_overwrite=True)
        assert exc.value.reason_code == "PROGRAM_IMMUTABILITY_VIOLATION"
        assert exc.value.details["existing_package_sha256"] == pkg.package_sha256

    def test_overwrite_active_status_also_rejected(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        active_pkg = pkg.with_status(ProgramStatus.ACTIVE)
        registry.register(active_pkg)
        assert active_pkg.is_immutable()
        (pkg_dir / "payload.txt").write_text("changed", encoding="utf-8")
        other = registry.inspect_and_validate_package(pkg_dir)
        with pytest.raises(ProgramImmutabilityError):
            registry.register(other, allow_overwrite=True)

    def test_immutable_statuses_set(self):
        assert "RELEASED" in IMMUTABLE_STATUSES
        assert "ACTIVE" in IMMUTABLE_STATUSES
        assert "DRAFT" not in IMMUTABLE_STATUSES

class TestGate4_NewVersionAcceptedWithoutAlteringOld:
    def test_new_version_registers_independently(self, registry, tmp_path):
        v1_dir = _write_minimal_package(tmp_path / "v1", version="1.0.0", status="DRAFT")
        v2_dir = _write_minimal_package(tmp_path / "v2", version="2.0.0", status="DRAFT", extra_file_content="payload-v2")
        v1 = registry.inspect_and_validate_package(v1_dir)
        registry.register(v1)
        registry.release("imm_test_program", "1.0.0")
        pin_v1 = registry.get_pinned_digests("imm_test_program", "1.0.0")
        v2 = registry.inspect_and_validate_package(v2_dir)
        registry.register(v2)
        registry.release("imm_test_program", "2.0.0")
        still_v1 = registry.get_program("imm_test_program", "1.0.0")
        assert still_v1.manifest.status == ProgramStatus.RELEASED
        assert still_v1.package_sha256 == pin_v1["package_sha256"]
        got_v2 = registry.get_program("imm_test_program", "2.0.0")
        assert got_v2.package_sha256 != still_v1.package_sha256

class TestGate5_DigestMismatchDetection:
    def test_verify_integrity_passes_on_unchanged(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.register(pkg)
        result = registry.verify_package_integrity("imm_test_program", "1.0.0")
        assert result.package_sha256 == pkg.package_sha256

    def test_verify_integrity_fails_after_mutation(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.register(pkg)
        (pkg_dir / "payload.txt").write_text("MUTATED-BYTES", encoding="utf-8")
        with pytest.raises(ProgramDigestMismatchError) as exc:
            registry.verify_package_integrity("imm_test_program", "1.0.0")
        assert exc.value.reason_code == "PROGRAM_DIGEST_MISMATCH"
        assert exc.value.details["field"] == "package_sha256"

class TestGate6_PreflightPinningAndIntegrity:
    def test_preflight_returns_pinned_digests(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.register(pkg)
        result = registry.preflight("imm_test_program", workspace_id="ws-test")
        assert result.pinned_manifest_sha256 == pkg.manifest_sha256
        assert result.pinned_package_sha256 == pkg.package_sha256
        assert result.eligible is True

    def test_preflight_require_integrity_fails_on_mismatch(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.register(pkg)
        (pkg_dir / "payload.txt").write_text("broken", encoding="utf-8")
        result = registry.preflight("imm_test_program", workspace_id="ws-test", require_integrity=True)
        assert result.eligible is False
        assert any("Digest mismatch" in i or "digest" in i.lower() for i in result.issues)

class TestGate7_FrozenModels:
    def test_program_package_is_frozen(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        with pytest.raises(Exception):
            pkg.package_sha256 = "0" * 64  # type: ignore

    def test_program_manifest_is_frozen(self):
        m = ProgramManifest(id="freeze_test", version="0.1.0", purpose="frozen model check", lanes=["HUNTER"])
        with pytest.raises(Exception):
            m.status = ProgramStatus.RELEASED  # type: ignore

    def test_with_status_returns_new_instance(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        released = pkg.with_status(ProgramStatus.RELEASED)
        assert released is not pkg
        assert released.manifest.status == ProgramStatus.RELEASED

class TestGate8_RegistryFreeze:
    def test_freeze_blocks_register(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.freeze()
        assert registry.is_frozen is True
        with pytest.raises(ProgramImmutabilityError):
            registry.register(pkg)

class TestGate9_DiscoveryRespectsImmutability:
    def test_discover_skips_overwrite_of_released_with_different_bytes(self, registry, tmp_path):
        root = tmp_path / "programs"
        pkg_path = _write_minimal_package(root / "imm_test_program", status="DRAFT")
        pkg = registry.inspect_and_validate_package(pkg_path)
        registry.register(pkg)
        registry.release("imm_test_program", "1.0.0")
        original_sha = pkg.package_sha256
        (pkg_path / "payload.txt").write_text("DISCOVERY-TAMPER", encoding="utf-8")
        registry.discover(search_paths=[root])
        still = registry.get_program("imm_test_program", "1.0.0")
        assert still.package_sha256 == original_sha
        assert still.manifest.status == ProgramStatus.RELEASED

class TestFalseProof_RegisterPathEnforcesInvariant:
    def test_register_path_rejects_released_overwrite(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.register(pkg.with_status(ProgramStatus.DRAFT))
        registry.release("imm_test_program", "1.0.0")
        same = registry.inspect_and_validate_package(pkg_dir)
        with pytest.raises(ProgramImmutabilityError) as exc:
            registry.register(same, allow_overwrite=True)
        assert exc.value.reason_code == "PROGRAM_IMMUTABILITY_VIOLATION"

    def test_direct_dict_tamper_is_not_the_proof(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.register(pkg.with_status(ProgramStatus.DRAFT))
        registry.release("imm_test_program", "1.0.0")
        with pytest.raises(ProgramImmutabilityError):
            registry.register(pkg.with_status(ProgramStatus.RELEASED), allow_overwrite=True)

class TestEdgeCases:
    def test_not_found(self, registry):
        with pytest.raises(ProgramNotFoundError):
            registry.get_program("does_not_exist")

    def test_quarantined_cannot_release(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.register(pkg.with_status(ProgramStatus.QUARANTINED))
        with pytest.raises(ProgramImmutabilityError):
            registry.release("imm_test_program", "1.0.0")

    def test_inspect_reports_immutable_flag(self, registry, pkg_dir):
        pkg = registry.inspect_and_validate_package(pkg_dir)
        registry.register(pkg.with_status(ProgramStatus.DRAFT))
        registry.release("imm_test_program", "1.0.0")
        meta = registry.inspect_program("imm_test_program", "1.0.0")
        assert meta["immutable"] is True
        assert meta["status"] == "RELEASED"
        assert meta["manifest_sha256"] == pkg.manifest_sha256
