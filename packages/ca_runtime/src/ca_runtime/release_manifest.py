"""Immutable, digest-backed release manifests for CA-M030 / FR-REL-001.

The manifest is a release boundary: it freezes artifact bytes, license metadata,
provenance lineage, authorization/policy references, a deterministic SHA-256
Merkle root, and an HMAC-SHA256 cryptographic seal.  Verification always
re-reads referenced artifacts from the filesystem; it never trusts stored
artifact digests alone.

This module is deliberately self-contained and uses the repository's canonical
JSON/hash primitives.  It does not implement downstream distribution.
"""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from ca_contracts import canonical_json_bytes, canonical_json_text, canonical_sha256

SCHEMA_VERSION = "ca-release-manifest/v1"
SEAL_ALGORITHM = "HMAC-SHA256"
SHA256_HEX_LENGTH = 64


class ReleaseManifestError(RuntimeError):
    """Base class for release manifest errors."""


class ReleaseManifestValidationError(ReleaseManifestError, ValueError):
    """Raised when a manifest input is structurally or semantically invalid."""


class ReleaseManifestIntegrityError(ReleaseManifestError):
    """Raised when a sealed manifest or referenced artifact fails verification."""


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReleaseManifestValidationError(f"{field} must be a non-empty string")
    return value


def _require_sha256(value: Any, field: str) -> str:
    value = _require_text(value, field).lower()
    if len(value) != SHA256_HEX_LENGTH or any(ch not in "0123456789abcdef" for ch in value):
        raise ReleaseManifestValidationError(f"{field} must be a lowercase SHA-256 hex digest")
    return value


def _normalize_secret(secret: bytes | str) -> bytes:
    if isinstance(secret, str):
        secret = secret.encode("utf-8")
    if not isinstance(secret, bytes) or not secret:
        raise ReleaseManifestValidationError("signing_secret must be non-empty bytes")
    return secret


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ReleaseManifestIntegrityError(f"Unable to read release artifact: {path}") from exc
    return digest.hexdigest()


def _leaf_digest(label: str, payload: Any) -> str:
    return hashlib.sha256(b"\x00" + label.encode("utf-8") + b"\x00" + canonical_json_bytes(payload)).hexdigest()


def _merkle_root(leaves: Sequence[tuple[str, Any]]) -> str:
    if not leaves:
        raise ReleaseManifestValidationError("release manifest must contain at least one integrity leaf")
    layer = [_leaf_digest(label, payload) for label, payload in sorted(leaves, key=lambda item: item[0])]
    while len(layer) > 1:
        next_layer: list[str] = []
        for index in range(0, len(layer), 2):
            left = layer[index]
            right = layer[index + 1] if index + 1 < len(layer) else left
            next_layer.append(hashlib.sha256(b"\x01" + bytes.fromhex(left) + bytes.fromhex(right)).hexdigest())
        layer = next_layer
    return layer[0]


def _sorted_refs(refs: Iterable[Mapping[str, Any]], field: str) -> tuple[dict[str, Any], ...]:
    normalized: list[dict[str, Any]] = []
    for ref in refs:
        if not isinstance(ref, Mapping):
            raise ReleaseManifestValidationError(f"{field} entries must be mappings")
        item = dict(ref)
        _require_text(item.get("object_id"), f"{field}.object_id")
        _require_text(item.get("revision"), f"{field}.revision")
        _require_sha256(item.get("sha256"), f"{field}.sha256")
        normalized.append(item)
    normalized.sort(key=lambda item: (item["object_id"], item["revision"], item["sha256"]))
    return tuple(normalized)


def _normalize_provenance_tree(node: Mapping[str, Any], path: str = "root") -> dict[str, Any]:
    if not isinstance(node, Mapping):
        raise ReleaseManifestValidationError(f"provenance tree node {path} must be a mapping")
    result = dict(node)
    _require_text(result.get("node_id"), f"provenance[{path}].node_id")
    _require_text(result.get("node_type"), f"provenance[{path}].node_type")
    _require_text(result.get("revision"), f"provenance[{path}].revision")
    _require_sha256(result.get("sha256"), f"provenance[{path}].sha256")
    children = result.get("children", [])
    if not isinstance(children, Sequence) or isinstance(children, (str, bytes, bytearray)):
        raise ReleaseManifestValidationError(f"provenance[{path}].children must be a sequence")
    normalized_children = [
        _normalize_provenance_tree(child, f"{path}.{index}")
        for index, child in enumerate(children)
    ]
    normalized_children.sort(key=lambda item: (item["node_id"], item["revision"], item["sha256"]))
    result["children"] = normalized_children
    return result


def _walk_provenance(node: Mapping[str, Any]) -> Iterable[dict[str, Any]]:
    yield dict(node)
    for child in node.get("children", []):
        yield from _walk_provenance(child)


@dataclass(frozen=True)
class ReleaseArtifact:
    """One immutable artifact declaration in a sealed release."""

    artifact_id: str
    logical_uri: str
    kind: str
    sha256: str
    byte_length: int
    license_metadata: Mapping[str, Any]
    provenance_refs: tuple[dict[str, Any], ...]
    filesystem_path: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.artifact_id, "artifact_id")
        _require_text(self.logical_uri, "logical_uri")
        _require_text(self.kind, "kind")
        _require_sha256(self.sha256, "sha256")
        if not isinstance(self.byte_length, int) or self.byte_length < 0:
            raise ReleaseManifestValidationError("byte_length must be a non-negative integer")
        if not isinstance(self.license_metadata, Mapping):
            raise ReleaseManifestValidationError("license_metadata must be a mapping")
        for required in ("license", "attribution"):
            if required not in self.license_metadata:
                raise ReleaseManifestValidationError(f"license_metadata must include {required}")
        for index, ref in enumerate(self.provenance_refs):
            _require_text(ref.get("object_id"), f"artifact.provenance_refs[{index}].object_id")
            _require_text(ref.get("revision"), f"artifact.provenance_refs[{index}].revision")
            _require_sha256(ref.get("sha256"), f"artifact.provenance_refs[{index}].sha256")

    def to_dict(self) -> dict[str, Any]:
        result = {
            "artifact_id": self.artifact_id,
            "logical_uri": self.logical_uri,
            "kind": self.kind,
            "sha256": self.sha256,
            "byte_length": self.byte_length,
            "license_metadata": dict(self.license_metadata),
            "provenance_refs": [dict(ref) for ref in self.provenance_refs],
        }
        if self.filesystem_path is not None:
            result["filesystem_path"] = self.filesystem_path
        return result

    @classmethod
    def from_path(
        cls,
        path: str | Path,
        *,
        logical_uri: str,
        kind: str,
        license_metadata: Mapping[str, Any],
        provenance_refs: Sequence[Mapping[str, Any]],
    ) -> "ReleaseArtifact":
        artifact_path = Path(path)
        try:
            size = artifact_path.stat().st_size
        except OSError as exc:
            raise ReleaseManifestValidationError(f"artifact path is not readable: {artifact_path}") from exc
        digest = _file_sha256(artifact_path)
        return cls(
            artifact_id=f"artifact:{digest}",
            logical_uri=_require_text(logical_uri, "logical_uri"),
            kind=_require_text(kind, "kind"),
            sha256=digest,
            byte_length=size,
            license_metadata=dict(license_metadata),
            provenance_refs=_sorted_refs(provenance_refs, "provenance_refs"),
            filesystem_path=str(artifact_path),
        )


@dataclass(frozen=True)
class ReleaseManifest:
    """Sealed, immutable representation of a release manifest."""

    release_id: str
    release_version: str
    release_state: str
    release_metadata: Mapping[str, Any]
    source_refs: tuple[dict[str, Any], ...]
    semantic_refs: tuple[dict[str, Any], ...]
    composition_ref: Mapping[str, Any]
    authorization_refs: tuple[dict[str, Any], ...]
    policy_ref: Mapping[str, Any]
    artifacts: tuple[ReleaseArtifact, ...]
    provenance_tree: Mapping[str, Any]
    license_metadata: Mapping[str, Any]
    merkle_root_sha256: str
    manifest_sha256: str
    seal_algorithm: str
    signature: str
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        _require_text(self.release_id, "release_id")
        _require_text(self.release_version, "release_version")
        if self.release_state != "RELEASE_SEALED":
            raise ReleaseManifestValidationError("sealed manifests must have release_state=RELEASE_SEALED")
        if not isinstance(self.release_metadata, Mapping):
            raise ReleaseManifestValidationError("release_metadata must be a mapping")
        if not self.artifacts:
            raise ReleaseManifestValidationError("release manifest must contain at least one artifact")
        if self.seal_algorithm != SEAL_ALGORITHM:
            raise ReleaseManifestValidationError(f"unsupported seal algorithm: {self.seal_algorithm}")
        _require_sha256(self.merkle_root_sha256, "merkle_root_sha256")
        _require_sha256(self.manifest_sha256, "manifest_sha256")
        _require_text(self.signature, "signature")
        if not isinstance(self.license_metadata, Mapping):
            raise ReleaseManifestValidationError("license_metadata must be a mapping")

    def unsigned_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "release_id": self.release_id,
            "release_version": self.release_version,
            "release_state": self.release_state,
            "release_metadata": dict(self.release_metadata),
            "source_refs": [dict(ref) for ref in self.source_refs],
            "semantic_refs": [dict(ref) for ref in self.semantic_refs],
            "composition_ref": dict(self.composition_ref),
            "authorization_refs": [dict(ref) for ref in self.authorization_refs],
            "policy_ref": dict(self.policy_ref),
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "provenance_tree": dict(self.provenance_tree),
            "license_metadata": dict(self.license_metadata),
            "merkle_root_sha256": self.merkle_root_sha256,
        }

    def signing_payload(self) -> dict[str, Any]:
        return {**self.unsigned_payload(), "manifest_sha256": self.manifest_sha256}

    def to_dict(self) -> dict[str, Any]:
        return {**self.signing_payload(), "seal_algorithm": self.seal_algorithm, "signature": self.signature}

    def to_json_bytes(self) -> bytes:
        return canonical_json_bytes(self.to_dict())

    def write(self, path: str | Path) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        serialized = self.to_json_bytes() + b"\n"
        if destination.exists():
            try:
                existing = destination.read_bytes()
            except OSError as exc:
                raise ReleaseManifestError(f"unable to inspect sealed release manifest: {destination}") from exc
            if existing != serialized:
                raise ReleaseManifestError(
                    f"sealed release manifest is immutable and cannot be overwritten: {destination}"
                )
            return destination
        try:
            destination.write_bytes(serialized)
        except OSError as exc:
            raise ReleaseManifestError(f"unable to persist sealed release manifest: {destination}") from exc
        return destination

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ReleaseManifest":
        if not isinstance(data, Mapping):
            raise ReleaseManifestValidationError("release manifest JSON root must be an object")
        artifacts: list[ReleaseArtifact] = []
        for item in data.get("artifacts", []):
            artifacts.append(
                ReleaseArtifact(
                    artifact_id=_require_text(item.get("artifact_id"), "artifact_id"),
                    logical_uri=_require_text(item.get("logical_uri"), "logical_uri"),
                    kind=_require_text(item.get("kind"), "kind"),
                    sha256=_require_sha256(item.get("sha256"), "sha256"),
                    byte_length=int(item.get("byte_length")),
                    license_metadata=dict(item.get("license_metadata", {})),
                    provenance_refs=_sorted_refs(item.get("provenance_refs", []), "provenance_refs"),
                    filesystem_path=item.get("filesystem_path"),
                )
            )
        return cls(
            release_id=_require_text(data.get("release_id"), "release_id"),
            release_version=_require_text(data.get("release_version"), "release_version"),
            release_state=_require_text(data.get("release_state"), "release_state"),
            release_metadata=dict(data.get("release_metadata", {})),
            source_refs=_sorted_refs(data.get("source_refs", []), "source_refs"),
            semantic_refs=_sorted_refs(data.get("semantic_refs", []), "semantic_refs"),
            composition_ref=dict(data.get("composition_ref", {})),
            authorization_refs=_sorted_refs(data.get("authorization_refs", []), "authorization_refs"),
            policy_ref=dict(data.get("policy_ref", {})),
            artifacts=tuple(sorted(artifacts, key=lambda artifact: artifact.logical_uri)),
            provenance_tree=_normalize_provenance_tree(data.get("provenance_tree", {})),
            license_metadata=dict(data.get("license_metadata", {})),
            merkle_root_sha256=_require_sha256(data.get("merkle_root_sha256"), "merkle_root_sha256"),
            manifest_sha256=_require_sha256(data.get("manifest_sha256"), "manifest_sha256"),
            seal_algorithm=_require_text(data.get("seal_algorithm"), "seal_algorithm"),
            signature=_require_text(data.get("signature"), "signature"),
            schema_version=_require_text(data.get("schema_version"), "schema_version"),
        )

    @classmethod
    def read(cls, path: str | Path) -> "ReleaseManifest":
        source = Path(path)
        try:
            data = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ReleaseManifestValidationError(f"unable to read release manifest: {source}") from exc
        return cls.from_dict(data)

    def verify(
        self,
        signing_secret: bytes | str,
        *,
        expected_artifact_paths: Mapping[str, str | Path] | None = None,
        expected_composition_ref: Mapping[str, Any] | None = None,
        expected_policy_revision: str | None = None,
    ) -> None:
        secret = _normalize_secret(signing_secret)
        expected_manifest_sha = canonical_sha256(self.unsigned_payload())
        if not hmac.compare_digest(self.manifest_sha256, expected_manifest_sha):
            raise ReleaseManifestIntegrityError("release manifest digest mismatch")

        expected_signature = hmac.new(
            secret,
            canonical_json_bytes(self.signing_payload()),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(self.signature, expected_signature):
            raise ReleaseManifestIntegrityError("release manifest signature mismatch")

        if expected_composition_ref is not None and dict(self.composition_ref) != dict(expected_composition_ref):
            raise ReleaseManifestIntegrityError("composition lineage does not match the expected revision")
        if expected_policy_revision is not None and self.policy_ref.get("revision") != expected_policy_revision:
            raise ReleaseManifestIntegrityError("policy revision does not match the expected release policy")

        actual_root = self._calculate_merkle_root()
        if not hmac.compare_digest(self.merkle_root_sha256, actual_root):
            raise ReleaseManifestIntegrityError("release Merkle root mismatch")

        paths = expected_artifact_paths or {
            artifact.logical_uri: artifact.filesystem_path
            for artifact in self.artifacts
            if artifact.filesystem_path is not None
        }
        for artifact in self.artifacts:
            raw_path = paths.get(artifact.logical_uri)
            if raw_path is None:
                raise ReleaseManifestIntegrityError(
                    f"no filesystem path supplied for artifact {artifact.logical_uri}"
                )
            path = Path(raw_path)
            actual_digest = _file_sha256(path)
            if not hmac.compare_digest(actual_digest, artifact.sha256):
                raise ReleaseManifestIntegrityError(
                    f"artifact digest mismatch for {artifact.logical_uri}"
                )
            actual_size = path.stat().st_size
            if actual_size != artifact.byte_length:
                raise ReleaseManifestIntegrityError(
                    f"artifact byte length mismatch for {artifact.logical_uri}"
                )

    def _calculate_merkle_root(self) -> str:
        leaves: list[tuple[str, Any]] = []
        for artifact in self.artifacts:
            leaves.append(
                (
                    f"artifact:{artifact.logical_uri}",
                    {
                        "artifact_id": artifact.artifact_id,
                        "logical_uri": artifact.logical_uri,
                        "kind": artifact.kind,
                        "sha256": artifact.sha256,
                        "byte_length": artifact.byte_length,
                        "license_metadata": dict(artifact.license_metadata),
                        "provenance_refs": [dict(ref) for ref in artifact.provenance_refs],
                    },
                )
            )
        for ref_type, refs in (
            ("source", self.source_refs),
            ("semantic", self.semantic_refs),
            ("authorization", self.authorization_refs),
        ):
            for ref in refs:
                leaves.append((f"{ref_type}:{ref['object_id']}:{ref['revision']}", dict(ref)))
        leaves.append(("composition", dict(self.composition_ref)))
        leaves.append(("policy", dict(self.policy_ref)))
        leaves.append(("license", dict(self.license_metadata)))
        leaves.extend(
            (
                f"provenance:{node['node_id']}:{node['revision']}",
                {
                    "node_id": node["node_id"],
                    "node_type": node["node_type"],
                    "revision": node["revision"],
                    "sha256": node["sha256"],
                },
            )
            for node in _walk_provenance(self.provenance_tree)
        )
        return _merkle_root(leaves)


class ReleaseManifestBuilder:
    """Build and seal a deterministic release manifest from real artifacts."""

    def __init__(self, signing_secret: bytes | str):
        self._signing_secret = _normalize_secret(signing_secret)

    def build(
        self,
        *,
        release_id: str,
        release_version: str,
        release_metadata: Mapping[str, Any],
        artifact_paths: Sequence[Mapping[str, Any]],
        source_refs: Sequence[Mapping[str, Any]],
        semantic_refs: Sequence[Mapping[str, Any]],
        composition_ref: Mapping[str, Any],
        authorization_refs: Sequence[Mapping[str, Any]],
        policy_ref: Mapping[str, Any],
        provenance_tree: Mapping[str, Any],
        license_metadata: Mapping[str, Any],
    ) -> ReleaseManifest:
        _require_text(release_id, "release_id")
        _require_text(release_version, "release_version")
        if not isinstance(artifact_paths, Sequence) or not artifact_paths:
            raise ReleaseManifestValidationError("artifact_paths must contain at least one artifact")
        if not isinstance(composition_ref, Mapping):
            raise ReleaseManifestValidationError("composition_ref must be a mapping")
        if not isinstance(policy_ref, Mapping):
            raise ReleaseManifestValidationError("policy_ref must be a mapping")
        _validate_lineage_ref(composition_ref, "composition_ref")
        _validate_lineage_ref(policy_ref, "policy_ref")
        if not authorization_refs:
            raise ReleaseManifestValidationError("at least one authorization decision reference is required")

        artifacts: list[ReleaseArtifact] = []
        for index, spec in enumerate(artifact_paths):
            if not isinstance(spec, Mapping):
                raise ReleaseManifestValidationError(f"artifact_paths[{index}] must be a mapping")
            artifacts.append(
                ReleaseArtifact.from_path(
                    spec.get("path"),
                    logical_uri=_require_text(spec.get("logical_uri"), f"artifact_paths[{index}].logical_uri"),
                    kind=_require_text(spec.get("kind"), f"artifact_paths[{index}].kind"),
                    license_metadata=dict(spec.get("license_metadata", license_metadata)),
                    provenance_refs=_sorted_refs(spec.get("provenance_refs", []), f"artifact_paths[{index}].provenance_refs"),
                )
            )
        artifacts.sort(key=lambda artifact: artifact.logical_uri)

        normalized_provenance = _normalize_provenance_tree(provenance_tree)
        normalized_authorizations = _sorted_refs(authorization_refs, "authorization_refs")
        for index, ref in enumerate(normalized_authorizations):
            if ref.get("decision") not in {"GRANT", "OPERATOR_OVERRIDE"}:
                raise ReleaseManifestValidationError(
                    f"authorization_refs[{index}].decision must grant release authority"
                )
            _require_text(ref.get("resource_id"), f"authorization_refs[{index}].resource_id")
            _require_text(ref.get("resource_revision"), f"authorization_refs[{index}].resource_revision")

        unsigned = {
            "schema_version": SCHEMA_VERSION,
            "release_id": release_id,
            "release_version": release_version,
            "release_state": "RELEASE_SEALED",
            "release_metadata": dict(release_metadata),
            "source_refs": list(_sorted_refs(source_refs, "source_refs")),
            "semantic_refs": list(_sorted_refs(semantic_refs, "semantic_refs")),
            "composition_ref": dict(composition_ref),
            "authorization_refs": list(normalized_authorizations),
            "policy_ref": dict(policy_ref),
            "artifacts": tuple(artifacts),
            "provenance_tree": normalized_provenance,
            "license_metadata": dict(license_metadata),
        }

        provisional = ReleaseManifest(
            **unsigned,
            merkle_root_sha256="0" * SHA256_HEX_LENGTH,
            manifest_sha256="0" * SHA256_HEX_LENGTH,
            seal_algorithm=SEAL_ALGORITHM,
            signature="pending",
        )
        merkle_root = provisional._calculate_merkle_root()
        unsigned["merkle_root_sha256"] = merkle_root
        manifest_sha = canonical_sha256(unsigned)
        signing_payload = {**unsigned, "manifest_sha256": manifest_sha}
        signature = hmac.new(self._signing_secret, canonical_json_bytes(signing_payload), hashlib.sha256).hexdigest()
        manifest = ReleaseManifest(
            **unsigned,
            manifest_sha256=manifest_sha,
            seal_algorithm=SEAL_ALGORITHM,
            signature=signature,
        )
        manifest.verify(self._signing_secret)
        return manifest


def _validate_lineage_ref(value: Mapping[str, Any], field: str) -> None:
    _require_text(value.get("object_id"), f"{field}.object_id")
    _require_text(value.get("revision"), f"{field}.revision")
    _require_sha256(value.get("sha256"), f"{field}.sha256")
