from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from hashlib import sha256
import json
from typing import Iterable, Mapping

from cmf_builder.domain.harness_ir import HarnessIR


ARTIFACT_MANIFEST_SCHEMA_ID = "cmf-builder-artifact-manifest/v1"
ARTIFACT_MANIFEST_SCHEMA_VERSION = "1.0.0"
ARTIFACT_COMPILER_ID = "cmf-builder/deterministic-artifact-compiler"
ARTIFACT_COMPILER_VERSION = "1.0.0"
ARTIFACT_AUTHORITY_CLASS = (
    "GENERATED_AUTHORITATIVE_VIEW_SUBORDINATE_TO_HARNESS_IR"
)

HUMAN_ARTIFACT_PATHS = (
    "human/product.md",
    "human/syntax.md",
    "human/activative-program.md",
    "human/runtime-architecture.md",
    "human/skill-system.md",
    "human/evaluation.md",
    "human/repair.md",
    "human/handoff.md",
)
OPENSPEC_ARTIFACT_PATHS = (
    "openspec/change.json",
    "openspec/harness-ir-view.schema.json",
    "openspec/implementation-governance.json",
)
MACHINE_ARTIFACT_PATHS = (
    "machine/registry-view.json",
    "machine/contract-view.json",
    "machine/graph-view.json",
    "machine/skill-manifest-view.json",
    "machine/evaluation-manifest-view.json",
    "machine/repair-policy-view.json",
    "machine/dashboard-config-view.json",
    "machine/fixture-view.json",
    "machine/traceability-map.json",
    "machine/implementation-ticket-view.json",
)
ARTIFACT_PATHS = tuple(
    sorted((*HUMAN_ARTIFACT_PATHS, *OPENSPEC_ARTIFACT_PATHS, *MACHINE_ARTIFACT_PATHS))
)


class GeneratedArtifactError(Exception):
    code = "GeneratedArtifactError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class ReproducibleBuildConfigInvalid(GeneratedArtifactError):
    code = "ReproducibleBuildConfigInvalid"


class ArtifactInventoryInvalid(GeneratedArtifactError):
    code = "ArtifactInventoryInvalid"


class ArtifactDependencyInvalid(GeneratedArtifactError):
    code = "ArtifactDependencyInvalid"


class ArtifactIntegrityInvalid(GeneratedArtifactError):
    code = "ArtifactIntegrityInvalid"


class ArtifactSetInvalidatedError(GeneratedArtifactError):
    code = "ArtifactSetInvalidatedError"


@dataclass(frozen=True, slots=True)
class ReproducibleBuildConfig:
    compiler_id: str
    compiler_version: str
    config_version: str
    generation_timestamp: str

    def validate(self) -> None:
        if (
            self.compiler_id != ARTIFACT_COMPILER_ID
            or self.compiler_version != ARTIFACT_COMPILER_VERSION
            or self.config_version != "1.0.0"
        ):
            raise ReproducibleBuildConfigInvalid(
                "The deterministic artifact compiler configuration is unsupported."
            )
        try:
            parsed = datetime.fromisoformat(self.generation_timestamp.replace("Z", "+00:00"))
        except ValueError as error:
            raise ReproducibleBuildConfigInvalid(
                "Generation timestamp must be RFC3339."
            ) from error
        if parsed.tzinfo is None or not self.generation_timestamp.endswith("Z"):
            raise ReproducibleBuildConfigInvalid(
                "Generation timestamp must be an explicit UTC RFC3339 value."
            )

    def canonical_dict(self) -> dict[str, str]:
        return {
            "compiler_id": self.compiler_id,
            "compiler_version": self.compiler_version,
            "config_version": self.config_version,
            "generation_timestamp": self.generation_timestamp,
        }

    def canonical_bytes(self) -> bytes:
        self.validate()
        return _canonical_json(self.canonical_dict())

    @property
    def config_hash(self) -> str:
        return f"sha256:{sha256(self.canonical_bytes()).hexdigest()}"


@dataclass(frozen=True, slots=True)
class ArtifactDependencySelector:
    artifact_path: str
    source_node_paths: tuple[str, ...]

    def validate(self, ir: HarnessIR) -> None:
        if self.artifact_path not in ARTIFACT_PATHS:
            raise ArtifactDependencyInvalid(
                "Artifact path is outside the closed inventory.", path=self.artifact_path
            )
        expected = tuple(sorted(set(self.source_node_paths)))
        if not expected or expected != self.source_node_paths:
            raise ArtifactDependencyInvalid(
                "Source-node selectors must be non-empty, unique and canonical.",
                path=self.artifact_path,
            )
        available = {item.path for item in ir.material_values}
        missing = tuple(path for path in expected if path not in available)
        if missing:
            raise ArtifactDependencyInvalid(
                "Artifact selector references an undeclared Harness IR node.",
                path=self.artifact_path,
                missing=missing,
            )


@dataclass(frozen=True, slots=True)
class GeneratedArtifact:
    path: str
    media_type: str
    authority_class: str
    source_ir_id: str
    source_ir_hash: str
    source_node_paths: tuple[str, ...]
    compiler_id: str
    compiler_version: str
    config_hash: str
    generation_timestamp: str
    content: bytes
    content_hash: str

    @classmethod
    def create(
        cls,
        *,
        path: str,
        media_type: str,
        ir: HarnessIR,
        selector: ArtifactDependencySelector,
        config: ReproducibleBuildConfig,
        content: bytes,
    ) -> "GeneratedArtifact":
        selector.validate(ir)
        config.validate()
        candidate = cls(
            path=path,
            media_type=media_type,
            authority_class=ARTIFACT_AUTHORITY_CLASS,
            source_ir_id=ir.ir_id,
            source_ir_hash=ir.ir_hash,
            source_node_paths=selector.source_node_paths,
            compiler_id=config.compiler_id,
            compiler_version=config.compiler_version,
            config_hash=config.config_hash,
            generation_timestamp=config.generation_timestamp,
            content=content,
            content_hash=f"sha256:{sha256(content).hexdigest()}",
        )
        candidate.validate(ir)
        return candidate

    def validate(self, ir: HarnessIR) -> None:
        ArtifactDependencySelector(self.path, self.source_node_paths).validate(ir)
        expected_media = "text/markdown" if self.path.endswith(".md") else "application/json"
        if self.media_type != expected_media:
            raise ArtifactIntegrityInvalid("Artifact media type is invalid.", path=self.path)
        if (
            self.authority_class != ARTIFACT_AUTHORITY_CLASS
            or self.source_ir_id != ir.ir_id
            or self.source_ir_hash != ir.ir_hash
            or self.compiler_id != ARTIFACT_COMPILER_ID
            or self.compiler_version != ARTIFACT_COMPILER_VERSION
            or not self.config_hash.startswith("sha256:")
            or not self.generation_timestamp.endswith("Z")
        ):
            raise ArtifactIntegrityInvalid(
                "Artifact identity or authority metadata is inconsistent.", path=self.path
            )
        expected_hash = f"sha256:{sha256(self.content).hexdigest()}"
        if self.content_hash != expected_hash:
            raise ArtifactIntegrityInvalid("Artifact content hash drifted.", path=self.path)

    def descriptor(self) -> dict[str, object]:
        return {
            "path": self.path,
            "media_type": self.media_type,
            "authority_class": self.authority_class,
            "source_ir_id": self.source_ir_id,
            "source_ir_hash": self.source_ir_hash,
            "source_node_paths": list(self.source_node_paths),
            "compiler_id": self.compiler_id,
            "compiler_version": self.compiler_version,
            "config_hash": self.config_hash,
            "generation_timestamp": self.generation_timestamp,
            "content_hash": self.content_hash,
            "byte_count": len(self.content),
        }


@dataclass(frozen=True, slots=True)
class ArtifactManifest:
    manifest_id: str
    manifest_hash: str
    artifact_set_id: str
    schema_id: str
    schema_version: str
    run_id: str
    ir_id: str
    ir_hash: str
    target_profile_ref: str
    source_lock_ref: str
    upstream_refs: tuple[str, ...]
    compiler_id: str
    compiler_version: str
    config_version: str
    config_hash: str
    generation_timestamp: str
    authority_class: str
    nondeterminism_exceptions: tuple[str, ...]
    artifacts: tuple[GeneratedArtifact, ...]

    @classmethod
    def create(
        cls,
        *,
        ir: HarnessIR,
        config: ReproducibleBuildConfig,
        artifacts: Iterable[GeneratedArtifact],
    ) -> "ArtifactManifest":
        ordered = tuple(sorted(artifacts, key=lambda item: item.path))
        candidate = cls(
            manifest_id="pending",
            manifest_hash="pending",
            artifact_set_id="pending",
            schema_id=ARTIFACT_MANIFEST_SCHEMA_ID,
            schema_version=ARTIFACT_MANIFEST_SCHEMA_VERSION,
            run_id=ir.run_id,
            ir_id=ir.ir_id,
            ir_hash=ir.ir_hash,
            target_profile_ref=ir.target_profile_ref,
            source_lock_ref=ir.source_lock_ref,
            upstream_refs=ir.upstream_refs,
            compiler_id=config.compiler_id,
            compiler_version=config.compiler_version,
            config_version=config.config_version,
            config_hash=config.config_hash,
            generation_timestamp=config.generation_timestamp,
            authority_class=ARTIFACT_AUTHORITY_CLASS,
            nondeterminism_exceptions=(),
            artifacts=ordered,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            manifest_id=f"artifact-manifest_{digest}",
            manifest_hash=f"sha256:{digest}",
            artifact_set_id=f"artifact-set_{digest}",
        )
        result.validate(ir, config)
        return result

    @property
    def artifact_count(self) -> int:
        return len(self.artifacts)

    @property
    def total_bytes(self) -> int:
        return sum(len(item.content) for item in self.artifacts)

    @property
    def compilation_key(self) -> tuple[str, str, str, str]:
        return (self.ir_hash, self.compiler_id, self.compiler_version, self.config_hash)

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "ir_id": self.ir_id,
            "ir_hash": self.ir_hash,
            "target_profile_ref": self.target_profile_ref,
            "source_lock_ref": self.source_lock_ref,
            "upstream_refs": list(self.upstream_refs),
            "compiler_id": self.compiler_id,
            "compiler_version": self.compiler_version,
            "config_version": self.config_version,
            "config_hash": self.config_hash,
            "generation_timestamp": self.generation_timestamp,
            "authority_class": self.authority_class,
            "nondeterminism_exceptions": list(self.nondeterminism_exceptions),
            "artifacts": [item.descriptor() for item in self.artifacts],
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())

    def validate(self, ir: HarnessIR, config: ReproducibleBuildConfig) -> None:
        config.validate()
        paths = tuple(item.path for item in self.artifacts)
        if paths != ARTIFACT_PATHS or len(set(paths)) != len(paths):
            raise ArtifactInventoryInvalid(
                "Artifact manifest must contain the exact canonical 21-item inventory.",
                observed=paths,
            )
        if (
            self.schema_id != ARTIFACT_MANIFEST_SCHEMA_ID
            or self.schema_version != ARTIFACT_MANIFEST_SCHEMA_VERSION
            or self.run_id != ir.run_id
            or self.ir_id != ir.ir_id
            or self.ir_hash != ir.ir_hash
            or self.target_profile_ref != ir.target_profile_ref
            or self.source_lock_ref != ir.source_lock_ref
            or self.upstream_refs != ir.upstream_refs
            or self.compiler_id != config.compiler_id
            or self.compiler_version != config.compiler_version
            or self.config_version != config.config_version
            or self.config_hash != config.config_hash
            or self.generation_timestamp != config.generation_timestamp
            or self.authority_class != ARTIFACT_AUTHORITY_CLASS
            or self.nondeterminism_exceptions
        ):
            raise ArtifactIntegrityInvalid("Artifact manifest identity or lineage is invalid.")
        for artifact in self.artifacts:
            artifact.validate(ir)
            if artifact.config_hash != self.config_hash:
                raise ArtifactIntegrityInvalid(
                    "Artifact uses a different reproducible build configuration.",
                    path=artifact.path,
                )
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.manifest_hash != f"sha256:{digest}"
            or self.manifest_id != f"artifact-manifest_{digest}"
            or self.artifact_set_id != f"artifact-set_{digest}"
        ):
            raise ArtifactIntegrityInvalid("Artifact manifest identity does not match its content.")


@dataclass(frozen=True, slots=True)
class ArtifactSetCompilationReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    run_id: str
    artifact_set_id: str
    manifest_id: str
    manifest_hash: str
    ir_id: str
    ir_hash: str
    compiler_id: str
    compiler_version: str
    config_hash: str
    generation_timestamp: str
    authority_identity: str
    artifact_count: int
    total_bytes: int
    event_ids: tuple[str, ...]
    stream_version: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        run_id: str,
        manifest: ArtifactManifest,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "ArtifactSetCompilationReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            command_id=command_id,
            run_id=run_id,
            artifact_set_id=manifest.artifact_set_id,
            manifest_id=manifest.manifest_id,
            manifest_hash=manifest.manifest_hash,
            ir_id=manifest.ir_id,
            ir_hash=manifest.ir_hash,
            compiler_id=manifest.compiler_id,
            compiler_version=manifest.compiler_version,
            config_hash=manifest.config_hash,
            generation_timestamp=manifest.generation_timestamp,
            authority_identity=authority_identity,
            artifact_count=manifest.artifact_count,
            total_bytes=manifest.total_bytes,
            event_ids=event_ids,
            stream_version=stream_version,
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(
            candidate,
            receipt_id=f"artifact-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "command_id": self.command_id,
                "run_id": self.run_id,
                "artifact_set_id": self.artifact_set_id,
                "manifest_id": self.manifest_id,
                "manifest_hash": self.manifest_hash,
                "ir_id": self.ir_id,
                "ir_hash": self.ir_hash,
                "compiler_id": self.compiler_id,
                "compiler_version": self.compiler_version,
                "config_hash": self.config_hash,
                "generation_timestamp": self.generation_timestamp,
                "authority_identity": self.authority_identity,
                "artifact_count": self.artifact_count,
                "total_bytes": self.total_bytes,
                "event_ids": list(self.event_ids),
                "stream_version": self.stream_version,
                "outcome": self.outcome,
            }
        )

    def validate(self, manifest: ArtifactManifest) -> None:
        if (
            self.artifact_set_id != manifest.artifact_set_id
            or self.manifest_id != manifest.manifest_id
            or self.manifest_hash != manifest.manifest_hash
            or self.ir_id != manifest.ir_id
            or self.ir_hash != manifest.ir_hash
            or self.compiler_id != manifest.compiler_id
            or self.compiler_version != manifest.compiler_version
            or self.config_hash != manifest.config_hash
            or self.generation_timestamp != manifest.generation_timestamp
            or self.artifact_count != manifest.artifact_count
            or self.total_bytes != manifest.total_bytes
            or self.outcome != "PASS"
        ):
            raise ArtifactIntegrityInvalid("Artifact compilation receipt does not match manifest.")
        digest = sha256(self.canonical_bytes()).hexdigest()
        if self.receipt_id != f"artifact-receipt_{digest}" or self.receipt_hash != f"sha256:{digest}":
            raise ArtifactIntegrityInvalid("Artifact receipt identity does not match its content.")


@dataclass(frozen=True, slots=True)
class ArtifactDrift:
    path: str
    expected_hash: str
    observed_hash: str
    reason: str


@dataclass(frozen=True, slots=True)
class ArtifactDriftReport:
    report_id: str
    report_hash: str
    manifest_id: str
    artifact_set_id: str
    ir_id: str
    checked_paths: tuple[str, ...]
    mismatches: tuple[ArtifactDrift, ...]
    quarantined: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        manifest: ArtifactManifest,
        observed: Mapping[str, bytes],
    ) -> "ArtifactDriftReport":
        expected = {item.path: item for item in manifest.artifacts}
        mismatches: list[ArtifactDrift] = []
        for path in sorted(set(expected) | set(observed)):
            expected_item = expected.get(path)
            observed_bytes = observed.get(path)
            if expected_item is None:
                mismatches.append(
                    ArtifactDrift(path, "absent", _hash_bytes(observed_bytes or b""), "UNDECLARED_EXTRA")
                )
            elif observed_bytes is None:
                mismatches.append(
                    ArtifactDrift(path, expected_item.content_hash, "absent", "MISSING")
                )
            else:
                observed_hash = _hash_bytes(observed_bytes)
                if observed_hash != expected_item.content_hash:
                    mismatches.append(
                        ArtifactDrift(path, expected_item.content_hash, observed_hash, "CONTENT_HASH_MISMATCH")
                    )
        candidate = cls(
            report_id="pending",
            report_hash="pending",
            manifest_id=manifest.manifest_id,
            artifact_set_id=manifest.artifact_set_id,
            ir_id=manifest.ir_id,
            checked_paths=tuple(sorted(observed)),
            mismatches=tuple(mismatches),
            quarantined=bool(mismatches),
            outcome="DRIFT" if mismatches else "PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(
            candidate,
            report_id=f"artifact-drift_{digest}",
            report_hash=f"sha256:{digest}",
        )

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "manifest_id": self.manifest_id,
                "artifact_set_id": self.artifact_set_id,
                "ir_id": self.ir_id,
                "checked_paths": list(self.checked_paths),
                "mismatches": [
                    {
                        "path": item.path,
                        "expected_hash": item.expected_hash,
                        "observed_hash": item.observed_hash,
                        "reason": item.reason,
                    }
                    for item in self.mismatches
                ],
                "quarantined": self.quarantined,
                "outcome": self.outcome,
            }
        )


@dataclass(frozen=True, slots=True)
class ArtifactSetInvalidation:
    invalidation_id: str
    invalidation_hash: str
    artifact_set_ref: str
    manifest_ref: str
    ir_ref: str
    upstream_invalidation_ref: str
    reason: str
    authority_identity: str
    new_version_required: bool

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        artifact_set_ref: str,
        manifest_ref: str,
        ir_ref: str,
        upstream_invalidation_ref: str,
        reason: str,
        authority_identity: str,
    ) -> "ArtifactSetInvalidation":
        if not all(
            value.strip()
            for value in (
                invalidation_id,
                artifact_set_ref,
                manifest_ref,
                ir_ref,
                upstream_invalidation_ref,
                reason,
                authority_identity,
            )
        ):
            raise ArtifactIntegrityInvalid("Artifact-set invalidation is incomplete.")
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            artifact_set_ref=artifact_set_ref,
            manifest_ref=manifest_ref,
            ir_ref=ir_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            reason=reason,
            authority_identity=authority_identity,
            new_version_required=True,
        )
        return replace(candidate, invalidation_hash=_hash_bytes(candidate.canonical_bytes()))

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "invalidation_id": self.invalidation_id,
                "artifact_set_ref": self.artifact_set_ref,
                "manifest_ref": self.manifest_ref,
                "ir_ref": self.ir_ref,
                "upstream_invalidation_ref": self.upstream_invalidation_ref,
                "reason": self.reason,
                "authority_identity": self.authority_identity,
                "new_version_required": self.new_version_required,
            }
        )


def _hash_bytes(value: bytes) -> str:
    return f"sha256:{sha256(value).hexdigest()}"


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
