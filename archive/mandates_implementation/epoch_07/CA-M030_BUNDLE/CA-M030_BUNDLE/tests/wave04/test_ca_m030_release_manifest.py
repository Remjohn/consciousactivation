from __future__ import annotations

import json
from pathlib import Path

import pytest

import importlib.util
import sys

from ca_contracts import canonical_sha256


def _load_release_manifest_module():
    module_path = Path(__file__).parents[2] / "packages" / "ca_runtime" / "src" / "ca_runtime" / "release_manifest.py"
    spec = importlib.util.spec_from_file_location("ca_runtime.release_manifest", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_release_manifest = _load_release_manifest_module()
ReleaseManifestBuilder = _release_manifest.ReleaseManifestBuilder
ReleaseManifestIntegrityError = _release_manifest.ReleaseManifestIntegrityError
ReleaseManifestValidationError = _release_manifest.ReleaseManifestValidationError
ReleaseManifestError = _release_manifest.ReleaseManifestError


SECRET = b"ca-m030-test-secret"


def _ref(object_id: str, revision: str, payload: object) -> dict[str, str]:
    return {"object_id": object_id, "revision": revision, "sha256": canonical_sha256(payload)}


def _fixture(tmp_path: Path):
    artifact_a = tmp_path / "campaign-script.txt"
    artifact_b = tmp_path / "storyboard.json"
    artifact_a.write_bytes(b"release-approved campaign script\n")
    artifact_b.write_bytes(b'{"scene":"01","duration_ms":1200}\n')
    composition_ref = _ref("composition:campaign-7", "rev-12", {"composition": 12})
    policy_ref = _ref("policy:release", "policy-4", {"policy": 4})
    authorization = {
        **_ref("authorization:campaign-7", "auth-9", {"decision": "GRANT"}),
        "decision": "GRANT",
        "resource_id": "release:campaign-7",
        "resource_revision": "rev-12",
    }
    provenance = {
        "node_id": "campaign-7",
        "node_type": "campaign",
        "revision": "rev-12",
        "sha256": canonical_sha256({"campaign": 7}),
        "children": [
            {
                "node_id": "brief-3",
                "node_type": "brief",
                "revision": "rev-3",
                "sha256": canonical_sha256({"brief": 3}),
                "children": [],
            }
        ],
    }
    builder = ReleaseManifestBuilder(SECRET)
    manifest = builder.build(
        release_id="release:campaign-7",
        release_version="1.0.0",
        release_metadata={"campaign_id": "campaign-7", "created_by": "release-pipeline"},
        artifact_paths=[
            {
                "path": artifact_a,
                "logical_uri": "campaign/script.txt",
                "kind": "text",
                "license_metadata": {"license": "CC-BY-4.0", "attribution": "CAE Test Author"},
                "provenance_refs": [_ref("source:interview-1", "rev-2", {"quote": "hello"})],
            },
            {
                "path": artifact_b,
                "logical_uri": "campaign/storyboard.json",
                "kind": "json",
                "license_metadata": {"license": "Proprietary", "attribution": "CAE"},
                "provenance_refs": [_ref("source:interview-1", "rev-2", {"quote": "hello"})],
            },
        ],
        source_refs=[_ref("source:interview-1", "rev-2", {"quote": "hello"})],
        semantic_refs=[_ref("semantic:story-1", "rev-6", {"story": 1})],
        composition_ref=composition_ref,
        authorization_refs=[authorization],
        policy_ref=policy_ref,
        provenance_tree=provenance,
        license_metadata={"license": "mixed", "attribution": "Campaign contributors"},
    )
    return builder, manifest, artifact_a, artifact_b, composition_ref


def test_seal_contains_digests_license_and_provenance_and_verifies_real_files(tmp_path: Path):
    builder, manifest, artifact_a, artifact_b, composition_ref = _fixture(tmp_path)

    assert manifest.release_state == "RELEASE_SEALED"
    assert len(manifest.artifacts) == 2
    assert manifest.artifacts[0].sha256
    assert manifest.license_metadata["license"] == "mixed"
    assert manifest.provenance_tree["children"][0]["node_id"] == "brief-3"
    manifest.verify(
        SECRET,
        expected_artifact_paths={
            "campaign/script.txt": artifact_a,
            "campaign/storyboard.json": artifact_b,
        },
        expected_composition_ref=composition_ref,
        expected_policy_revision="policy-4",
    )


def test_deterministic_build_produces_identical_identity(tmp_path: Path):
    _, first, *_ = _fixture(tmp_path)
    _, second, *_ = _fixture(tmp_path)
    assert first.to_dict() == second.to_dict()
    assert first.merkle_root_sha256 == second.merkle_root_sha256
    assert first.manifest_sha256 == second.manifest_sha256
    assert first.signature == second.signature


def test_artifact_byte_mutation_fails_closed(tmp_path: Path):
    builder, manifest, artifact_a, artifact_b, _ = _fixture(tmp_path)
    artifact_a.write_bytes(b"tampered bytes\n")
    with pytest.raises(ReleaseManifestIntegrityError, match="artifact digest mismatch"):
        manifest.verify(
            SECRET,
            expected_artifact_paths={
                "campaign/script.txt": artifact_a,
                "campaign/storyboard.json": artifact_b,
            },
        )


def test_manifest_mutation_fails_closed(tmp_path: Path):
    _, manifest, artifact_a, artifact_b, _ = _fixture(tmp_path)
    payload = manifest.to_dict()
    payload["release_metadata"]["campaign_id"] = "attacker-campaign"
    mutated = manifest.from_dict(payload)
    with pytest.raises(ReleaseManifestIntegrityError, match="manifest digest mismatch"):
        mutated.verify(
            SECRET,
            expected_artifact_paths={
                "campaign/script.txt": artifact_a,
                "campaign/storyboard.json": artifact_b,
            },
        )


def test_persistence_reload_preserves_immutable_identity(tmp_path: Path):
    _, manifest, artifact_a, artifact_b, _ = _fixture(tmp_path)
    path = manifest.write(tmp_path / "RELEASE_MANIFEST.json")
    reloaded = manifest.read(path)
    assert reloaded.to_dict() == manifest.to_dict()
    reloaded.verify(
        SECRET,
        expected_artifact_paths={
            "campaign/script.txt": artifact_a,
            "campaign/storyboard.json": artifact_b,
        },
    )


def test_missing_lineage_is_rejected(tmp_path: Path):
    artifact = tmp_path / "output.txt"
    artifact.write_text("payload", encoding="utf-8")
    builder = ReleaseManifestBuilder(SECRET)
    with pytest.raises(ReleaseManifestValidationError, match="composition_ref.object_id"):
        builder.build(
            release_id="release:x",
            release_version="1",
            release_metadata={},
            artifact_paths=[
                {
                    "path": artifact,
                    "logical_uri": "output.txt",
                    "kind": "text",
                    "license_metadata": {"license": "MIT", "attribution": "CAE"},
                    "provenance_refs": [],
                }
            ],
            source_refs=[_ref("source:x", "1", {"x": 1})],
            semantic_refs=[_ref("semantic:x", "1", {"x": 1})],
            composition_ref={},
            authorization_refs=[{
                "object_id": "auth:x",
                "revision": "1",
                "sha256": canonical_sha256({"x": 1}),
                "decision": "GRANT",
                "resource_id": "release:x",
                "resource_revision": "1",
            }],
            policy_ref=_ref("policy:x", "1", {"x": 1}),
            provenance_tree={
                "node_id": "root",
                "node_type": "release",
                "revision": "1",
                "sha256": canonical_sha256({"x": 1}),
                "children": [],
            },
            license_metadata={"license": "MIT", "attribution": "CAE"},
        )


def test_mismatched_policy_revision_fails_closed(tmp_path: Path):
    _, manifest, artifact_a, artifact_b, _ = _fixture(tmp_path)
    with pytest.raises(ReleaseManifestIntegrityError, match="policy revision"):
        manifest.verify(
            SECRET,
            expected_artifact_paths={
                "campaign/script.txt": artifact_a,
                "campaign/storyboard.json": artifact_b,
            },
            expected_policy_revision="policy-999",
        )


def test_mismatched_authorization_binding_fails_closed(tmp_path: Path):
    _, manifest, artifact_a, artifact_b, _ = _fixture(tmp_path)
    payload = manifest.to_dict()
    payload["authorization_refs"][0]["resource_revision"] = "rev-999"
    tampered = manifest.from_dict(payload)
    with pytest.raises(ReleaseManifestIntegrityError, match="manifest digest mismatch"):
        tampered.verify(
            SECRET,
            expected_artifact_paths={
                "campaign/script.txt": artifact_a,
                "campaign/storyboard.json": artifact_b,
            },
        )


def test_wrong_signing_secret_fails_closed(tmp_path: Path):
    _, manifest, artifact_a, artifact_b, _ = _fixture(tmp_path)
    with pytest.raises(ReleaseManifestIntegrityError, match="signature mismatch"):
        manifest.verify(
            b"wrong-secret",
            expected_artifact_paths={
                "campaign/script.txt": artifact_a,
                "campaign/storyboard.json": artifact_b,
            },
        )


def test_verifier_requires_every_declared_artifact(tmp_path: Path):
    _, manifest, artifact_a, _, _ = _fixture(tmp_path)
    with pytest.raises(ReleaseManifestIntegrityError, match="no filesystem path supplied"):
        manifest.verify(
            SECRET,
            expected_artifact_paths={"campaign/script.txt": artifact_a},
        )


def test_merkle_root_changes_when_artifact_identity_changes(tmp_path: Path):
    _, first, artifact_a, artifact_b, _ = _fixture(tmp_path)
    builder = ReleaseManifestBuilder(SECRET)
    artifact_a.write_bytes(b"different but valid output\n")
    with pytest.raises(ReleaseManifestIntegrityError):
        first.verify(
            SECRET,
            expected_artifact_paths={
                "campaign/script.txt": artifact_a,
                "campaign/storyboard.json": artifact_b,
            },
        )
    # Rebuilding after the byte change yields a distinct release identity.
    specs = [
        {
            "path": artifact_a,
            "logical_uri": "campaign/script.txt",
            "kind": "text",
            "license_metadata": {"license": "CC-BY-4.0", "attribution": "CAE Test Author"},
            "provenance_refs": [_ref("source:interview-1", "rev-2", {"quote": "hello"})],
        },
        {
            "path": artifact_b,
            "logical_uri": "campaign/storyboard.json",
            "kind": "json",
            "license_metadata": {"license": "Proprietary", "attribution": "CAE"},
            "provenance_refs": [_ref("source:interview-1", "rev-2", {"quote": "hello"})],
        },
    ]
    rebuilt = builder.build(
        release_id="release:campaign-7-v2",
        release_version="1.0.0",
        release_metadata={"campaign_id": "campaign-7", "created_by": "release-pipeline"},
        artifact_paths=specs,
        source_refs=[_ref("source:interview-1", "rev-2", {"quote": "hello"})],
        semantic_refs=[_ref("semantic:story-1", "rev-6", {"story": 1})],
        composition_ref=_ref("composition:campaign-7", "rev-12", {"composition": 12}),
        authorization_refs=[{
            **_ref("authorization:campaign-7", "auth-9", {"decision": "GRANT"}),
            "decision": "GRANT",
            "resource_id": "release:campaign-7-v2",
            "resource_revision": "rev-12",
        }],
        policy_ref=_ref("policy:release", "policy-4", {"policy": 4}),
        provenance_tree={
            "node_id": "campaign-7",
            "node_type": "campaign",
            "revision": "rev-12",
            "sha256": canonical_sha256({"campaign": 7}),
            "children": [],
        },
        license_metadata={"license": "mixed", "attribution": "Campaign contributors"},
    )
    assert rebuilt.merkle_root_sha256 != first.merkle_root_sha256
    assert rebuilt.manifest_sha256 != first.manifest_sha256


def test_false_proof_top_level_manifest_hash_without_real_artifact_verification_fails(tmp_path: Path):
    _, manifest, artifact_a, artifact_b, _ = _fixture(tmp_path)
    payload = manifest.to_dict()
    assert payload["manifest_sha256"] == manifest.manifest_sha256
    artifact_a.write_bytes(b"post-seal semantic mutation")
    # A verifier that only checks the stored manifest hash would falsely pass.
    expected_manifest_sha = canonical_sha256(manifest.unsigned_payload())
    assert expected_manifest_sha == manifest.manifest_sha256
    with pytest.raises(ReleaseManifestIntegrityError, match="artifact digest mismatch"):
        manifest.verify(
            SECRET,
            expected_artifact_paths={
                "campaign/script.txt": artifact_a,
                "campaign/storyboard.json": artifact_b,
            },
        )


def test_sealed_manifest_cannot_be_overwritten_with_different_bytes(tmp_path: Path):
    _, manifest, _, _, _ = _fixture(tmp_path)
    path = manifest.write(tmp_path / "release.json")
    mutated = manifest.to_dict()
    mutated["release_metadata"]["note"] = "attempted repair"
    with pytest.raises(ReleaseManifestError, match="immutable and cannot be overwritten"):
        # A sealed release is historical; changing semantic bytes requires a new release.
        manifest.from_dict(mutated).write(path)


def test_real_json_round_trip_is_canonical_and_signed(tmp_path: Path):
    _, manifest, artifact_a, artifact_b, _ = _fixture(tmp_path)
    path = manifest.write(tmp_path / "release.json")
    raw = path.read_bytes()
    parsed = json.loads(raw)
    assert raw == (manifest.to_json_bytes() + b"\n")
    assert parsed["seal_algorithm"] == "HMAC-SHA256"
    manifest.read(path).verify(
        SECRET,
        expected_artifact_paths={
            "campaign/script.txt": artifact_a,
            "campaign/storyboard.json": artifact_b,
        },
    )
