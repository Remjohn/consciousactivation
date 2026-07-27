from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.domain.evidence_workspace import SourceDescriptor, SourceLock


INDEX_VERSION = "1.0.0"
ADAPTER_VERSION = "evidence-indexer/1.0.0"


class EvidenceIndexError(Exception):
    code = "EvidenceIndexError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class EvidenceIndexIncomplete(EvidenceIndexError):
    code = "EvidenceIndexIncomplete"


class EvidenceIdentityCollision(EvidenceIndexError):
    code = "EvidenceIdentityCollision"


class EvidenceProvenanceInvalid(EvidenceIndexError):
    code = "EvidenceProvenanceInvalid"


class EvidenceIndexInvalid(EvidenceIndexError):
    code = "EvidenceIndexInvalid"


class EvidenceIndexInvalidated(EvidenceIndexError):
    code = "EvidenceIndexInvalidated"


class SpecimenStatus(str, Enum):
    ACTIVE = "ACTIVE"
    QUARANTINED = "QUARANTINED"
    INVALIDATED = "INVALIDATED"


class KnowledgeStatus(str, Enum):
    OBSERVED = "OBSERVED"
    REPORTED = "REPORTED"
    INFERRED = "INFERRED"
    PROPOSED = "PROPOSED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True, slots=True)
class SpecimenObservation:
    observed_media_type: str
    observed_size_bytes: int
    observed_content_hash: str
    observation_kind: str = "SOURCE_DESCRIPTOR_METADATA"

    def validate(self) -> None:
        if (
            not self.observed_media_type.strip()
            or self.observed_size_bytes < 0
            or not _valid_prefixed_hash(self.observed_content_hash)
            or self.observation_kind != "SOURCE_DESCRIPTOR_METADATA"
        ):
            raise ValueError("Specimen observation metadata is invalid.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "observation_kind": self.observation_kind,
            "observed_content_hash": self.observed_content_hash,
            "observed_media_type": self.observed_media_type,
            "observed_size_bytes": self.observed_size_bytes,
        }


@dataclass(frozen=True, slots=True)
class EvidenceProvenance:
    run_id: str
    source_lock_ref: str
    source_lock_hash: str
    source_profile_ref: str
    source_id: str
    source_content_hash: str
    canonical_uri: str
    discovered_from: str
    authority: str
    license: str
    privacy_class: str

    def validate(self) -> None:
        required = (
            self.run_id,
            self.source_lock_ref,
            self.source_profile_ref,
            self.source_id,
            self.canonical_uri,
            self.discovered_from,
            self.authority,
            self.license,
            self.privacy_class,
        )
        if not all(value.strip() for value in required):
            raise EvidenceProvenanceInvalid("Evidence provenance is incomplete.")
        if not _valid_prefixed_hash(self.source_lock_hash) or not _valid_prefixed_hash(
            self.source_content_hash
        ):
            raise EvidenceProvenanceInvalid("Evidence provenance hashes are invalid.")
        normalized = self.canonical_uri.replace("\\", "/")
        if normalized.startswith(("/", "file://")) or (
            len(normalized) > 2 and normalized[1:3] == ":/"
        ):
            raise EvidenceProvenanceInvalid(
                "Portable evidence provenance cannot contain an absolute machine path."
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "authority": self.authority,
            "canonical_uri": self.canonical_uri,
            "discovered_from": self.discovered_from,
            "license": self.license,
            "privacy_class": self.privacy_class,
            "run_id": self.run_id,
            "source_content_hash": self.source_content_hash,
            "source_id": self.source_id,
            "source_lock_hash": self.source_lock_hash,
            "source_lock_ref": self.source_lock_ref,
            "source_profile_ref": self.source_profile_ref,
        }


@dataclass(frozen=True, slots=True)
class EvidenceRelationship:
    relationship_type: str
    subject_ref: str
    object_ref: str

    def validate(self) -> None:
        if self.relationship_type not in {
            "DERIVED_FROM_SOURCE",
            "MEMBER_OF_SOURCE_LOCK",
        } or not self.subject_ref.strip() or not self.object_ref.strip():
            raise ValueError("Evidence relationship is invalid.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "object_ref": self.object_ref,
            "relationship_type": self.relationship_type,
            "subject_ref": self.subject_ref,
        }


@dataclass(frozen=True, slots=True)
class Specimen:
    specimen_id: str
    source_id: str
    source_content_hash: str
    role: str
    source_kind: str
    media_type: str
    precedence: int
    observation: SpecimenObservation
    governed_status: SpecimenStatus
    knowledge_status: KnowledgeStatus
    provenance: EvidenceProvenance
    relationships: tuple[EvidenceRelationship, ...]

    @classmethod
    def from_descriptor(
        cls, *, run_id: str, source_lock: SourceLock, descriptor: SourceDescriptor
    ) -> "Specimen":
        specimen_id = stable_specimen_id(descriptor)
        source_hash = f"sha256:{descriptor.sha256}"
        specimen = cls(
            specimen_id=specimen_id,
            source_id=descriptor.source_id,
            source_content_hash=source_hash,
            role=descriptor.role,
            source_kind=descriptor.source_kind,
            media_type=descriptor.media_type,
            precedence=descriptor.precedence,
            observation=SpecimenObservation(
                observed_media_type=descriptor.media_type,
                observed_size_bytes=descriptor.size_bytes,
                observed_content_hash=source_hash,
            ),
            governed_status=SpecimenStatus.ACTIVE,
            knowledge_status=KnowledgeStatus.OBSERVED,
            provenance=EvidenceProvenance(
                run_id=run_id,
                source_lock_ref=source_lock.lock_id,
                source_lock_hash=source_lock.aggregate_hash,
                source_profile_ref=source_lock.source_profile_ref,
                source_id=descriptor.source_id,
                source_content_hash=source_hash,
                canonical_uri=descriptor.canonical_uri,
                discovered_from=descriptor.discovered_from,
                authority=descriptor.authority,
                license=descriptor.license,
                privacy_class=descriptor.privacy_class,
            ),
            relationships=(
                EvidenceRelationship(
                    relationship_type="DERIVED_FROM_SOURCE",
                    subject_ref=specimen_id,
                    object_ref=descriptor.source_id,
                ),
                EvidenceRelationship(
                    relationship_type="MEMBER_OF_SOURCE_LOCK",
                    subject_ref=specimen_id,
                    object_ref=source_lock.lock_id,
                ),
            ),
        )
        specimen.validate()
        return specimen

    def validate(self) -> None:
        if not isinstance(self.governed_status, SpecimenStatus) or not isinstance(
            self.knowledge_status, KnowledgeStatus
        ):
            raise ValueError("Specimen status and knowledge status must be typed.")
        if (
            not all(
                value.strip()
                for value in (
                    self.specimen_id,
                    self.source_id,
                    self.role,
                    self.source_kind,
                    self.media_type,
                )
            )
            or not _valid_prefixed_hash(self.source_content_hash)
            or self.precedence <= 0
        ):
            raise ValueError("Specimen identity or classification is invalid.")
        self.observation.validate()
        self.provenance.validate()
        if (
            self.source_id != self.provenance.source_id
            or self.source_content_hash != self.provenance.source_content_hash
        ):
            raise EvidenceProvenanceInvalid(
                "Specimen identity differs from its provenance."
            )
        if {item.relationship_type for item in self.relationships} != {
            "DERIVED_FROM_SOURCE",
            "MEMBER_OF_SOURCE_LOCK",
        }:
            raise EvidenceIndexIncomplete(
                "Every specimen requires both governed provenance relationships."
            )
        for relationship in self.relationships:
            relationship.validate()
            if relationship.subject_ref != self.specimen_id:
                raise EvidenceProvenanceInvalid(
                    "Relationship subject differs from specimen identity."
                )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "governed_status": self.governed_status.value,
            "knowledge_status": self.knowledge_status.value,
            "media_type": self.media_type,
            "observation": self.observation.canonical_dict(),
            "precedence": self.precedence,
            "provenance": self.provenance.canonical_dict(),
            "relationships": [item.canonical_dict() for item in self.relationships],
            "role": self.role,
            "source_content_hash": self.source_content_hash,
            "source_id": self.source_id,
            "source_kind": self.source_kind,
            "specimen_id": self.specimen_id,
        }


@dataclass(frozen=True, slots=True)
class EvidenceIndex:
    index_id: str
    index_hash: str
    index_version: str
    adapter_version: str
    run_id: str
    source_lock_ref: str
    source_lock_hash: str
    source_profile_ref: str
    authority_identity: str
    descriptor_count: int
    specimens: tuple[Specimen, ...]
    production_eligible: bool = False
    certified: bool = False

    @property
    def specimen_count(self) -> int:
        return len(self.specimens)

    @classmethod
    def create(
        cls,
        *,
        run_id: str,
        source_lock: SourceLock,
        authority_identity: str,
        adapter_version: str = ADAPTER_VERSION,
    ) -> "EvidenceIndex":
        if source_lock.run_id != run_id:
            raise EvidenceProvenanceInvalid(
                "Source Lock and evidence-index run identities differ."
            )
        expected_source_lock_hash = source_lock_identity_hash(source_lock)
        if source_lock.aggregate_hash != expected_source_lock_hash:
            raise EvidenceProvenanceInvalid(
                "Source Lock bytes and aggregate identity differ.",
                expected_source_lock_hash=expected_source_lock_hash,
                observed_source_lock_hash=source_lock.aggregate_hash,
            )
        ordered_descriptors = tuple(
            sorted(
                source_lock.ordered_descriptors,
                key=lambda item: (
                    item.precedence,
                    item.canonical_uri,
                    item.sha256,
                    item.source_id,
                ),
            )
        )
        specimens: list[Specimen] = []
        specimen_ids: set[str] = set()
        source_ids: set[str] = set()
        for descriptor in ordered_descriptors:
            specimen = Specimen.from_descriptor(
                run_id=run_id, source_lock=source_lock, descriptor=descriptor
            )
            if (
                specimen.specimen_id in specimen_ids
                or specimen.source_id in source_ids
            ):
                raise EvidenceIdentityCollision(
                    "A Source Lock contains a duplicate or colliding specimen identity.",
                    specimen_id=specimen.specimen_id,
                    source_id=specimen.source_id,
                )
            specimen_ids.add(specimen.specimen_id)
            source_ids.add(specimen.source_id)
            specimens.append(specimen)
        base = {
            "adapter_version": adapter_version,
            "authority_identity": authority_identity,
            "certified": False,
            "descriptor_count": len(ordered_descriptors),
            "index_version": INDEX_VERSION,
            "production_eligible": False,
            "run_id": run_id,
            "source_lock_hash": source_lock.aggregate_hash,
            "source_lock_ref": source_lock.lock_id,
            "source_profile_ref": source_lock.source_profile_ref,
            "specimens": [item.canonical_dict() for item in specimens],
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        index = cls(
            index_id=f"evidence-index_{digest}",
            index_hash=f"sha256:{digest}",
            index_version=INDEX_VERSION,
            adapter_version=adapter_version,
            run_id=run_id,
            source_lock_ref=source_lock.lock_id,
            source_lock_hash=source_lock.aggregate_hash,
            source_profile_ref=source_lock.source_profile_ref,
            authority_identity=authority_identity,
            descriptor_count=len(ordered_descriptors),
            specimens=tuple(specimens),
        )
        index.validate(source_lock)
        return index

    def validate(self, source_lock: SourceLock) -> None:
        if (
            self.index_version != INDEX_VERSION
            or self.adapter_version != ADAPTER_VERSION
            or self.run_id != source_lock.run_id
            or self.source_lock_ref != source_lock.lock_id
            or self.source_lock_hash != source_lock.aggregate_hash
            or self.source_profile_ref != source_lock.source_profile_ref
            or not self.authority_identity.strip()
            or self.production_eligible
            or self.certified
        ):
            raise EvidenceIndexInvalid(
                "Evidence index identity, lineage or non-production boundary is invalid."
            )
        if self.descriptor_count != len(source_lock.ordered_descriptors) or (
            self.specimen_count != self.descriptor_count
        ):
            raise EvidenceIndexIncomplete(
                "Evidence index does not account for every Source Lock descriptor.",
                descriptor_count=len(source_lock.ordered_descriptors),
                specimen_count=self.specimen_count,
            )
        expected_ids = {item.source_id for item in source_lock.ordered_descriptors}
        actual_ids = {item.source_id for item in self.specimens}
        if len(expected_ids) != self.descriptor_count or actual_ids != expected_ids:
            raise EvidenceIndexIncomplete(
                "Source descriptor and specimen coverage differ."
            )
        for specimen in self.specimens:
            specimen.validate()
            if (
                specimen.provenance.run_id != self.run_id
                or specimen.provenance.source_lock_ref != self.source_lock_ref
                or specimen.provenance.source_lock_hash != self.source_lock_hash
                or specimen.provenance.source_profile_ref != self.source_profile_ref
            ):
                raise EvidenceProvenanceInvalid(
                    "Specimen provenance differs from evidence-index lineage."
                )
        digest = sha256(_canonical_json(self._identity_payload())).hexdigest()
        if self.index_id != f"evidence-index_{digest}" or self.index_hash != f"sha256:{digest}":
            raise EvidenceIndexInvalid("Evidence index identity does not match canonical bytes.")

    def _identity_payload(self) -> dict[str, object]:
        return {
            "adapter_version": self.adapter_version,
            "authority_identity": self.authority_identity,
            "certified": self.certified,
            "descriptor_count": self.descriptor_count,
            "index_version": self.index_version,
            "production_eligible": self.production_eligible,
            "run_id": self.run_id,
            "source_lock_hash": self.source_lock_hash,
            "source_lock_ref": self.source_lock_ref,
            "source_profile_ref": self.source_profile_ref,
            "specimens": [item.canonical_dict() for item in self.specimens],
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                **self._identity_payload(),
                "index_hash": self.index_hash,
                "index_id": self.index_id,
            }
        )

    def query(
        self,
        *,
        specimen_id: str | None = None,
        source_id: str | None = None,
        role: str | None = None,
        governed_status: str | None = None,
        knowledge_status: str | None = None,
    ) -> tuple[Specimen, ...]:
        result = self.specimens
        if specimen_id is not None:
            result = tuple(item for item in result if item.specimen_id == specimen_id)
        if source_id is not None:
            result = tuple(item for item in result if item.source_id == source_id)
        if role is not None:
            result = tuple(item for item in result if item.role == role)
        if governed_status is not None:
            result = tuple(
                item for item in result if item.governed_status.value == governed_status
            )
        if knowledge_status is not None:
            result = tuple(
                item for item in result if item.knowledge_status.value == knowledge_status
            )
        return result


@dataclass(frozen=True, slots=True)
class EvidenceIndexReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    run_id: str
    index_id: str
    index_hash: str
    source_lock_ref: str
    source_lock_hash: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    specimen_count: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        index: EvidenceIndex,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "EvidenceIndexReceipt":
        base = {
            "authority_identity": index.authority_identity,
            "command_id": command_id,
            "event_ids": event_ids,
            "index_hash": index.index_hash,
            "index_id": index.index_id,
            "outcome": "PASS",
            "run_id": index.run_id,
            "source_lock_hash": index.source_lock_hash,
            "source_lock_ref": index.source_lock_ref,
            "specimen_count": index.specimen_count,
            "stream_version": stream_version,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        return cls(
            receipt_id=f"evidence-index-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
            command_id=command_id,
            run_id=index.run_id,
            index_id=index.index_id,
            index_hash=index.index_hash,
            source_lock_ref=index.source_lock_ref,
            source_lock_hash=index.source_lock_hash,
            authority_identity=index.authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            specimen_count=index.specimen_count,
            outcome="PASS",
        )

    def validate(self, index: EvidenceIndex) -> None:
        if (
            self.run_id != index.run_id
            or self.index_id != index.index_id
            or self.index_hash != index.index_hash
            or self.source_lock_ref != index.source_lock_ref
            or self.source_lock_hash != index.source_lock_hash
            or self.authority_identity != index.authority_identity
            or self.specimen_count != index.specimen_count
            or self.outcome != "PASS"
            or not self.command_id.strip()
            or not self.event_ids
            or self.stream_version <= 0
        ):
            raise EvidenceIndexInvalid("Evidence-index receipt does not match its index.")
        digest = sha256(_canonical_json(self._identity_payload())).hexdigest()
        if self.receipt_id != f"evidence-index-receipt_{digest}" or self.receipt_hash != f"sha256:{digest}":
            raise EvidenceIndexInvalid("Evidence-index receipt identity is invalid.")

    def _identity_payload(self) -> dict[str, object]:
        return {
            "authority_identity": self.authority_identity,
            "command_id": self.command_id,
            "event_ids": self.event_ids,
            "index_hash": self.index_hash,
            "index_id": self.index_id,
            "outcome": self.outcome,
            "run_id": self.run_id,
            "source_lock_hash": self.source_lock_hash,
            "source_lock_ref": self.source_lock_ref,
            "specimen_count": self.specimen_count,
            "stream_version": self.stream_version,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                **self._identity_payload(),
                "receipt_hash": self.receipt_hash,
                "receipt_id": self.receipt_id,
            }
        )


@dataclass(frozen=True, slots=True)
class EvidenceIndexInvalidation:
    invalidation_id: str
    invalidation_hash: str
    command_id: str
    run_id: str
    index_id: str
    index_hash: str
    source_lock_ref: str
    authority_identity: str
    reason: str
    event_ids: tuple[str, ...]
    stream_version: int

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        index: EvidenceIndex,
        authority_identity: str,
        reason: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "EvidenceIndexInvalidation":
        base = {
            "authority_identity": authority_identity,
            "command_id": command_id,
            "event_ids": event_ids,
            "index_hash": index.index_hash,
            "index_id": index.index_id,
            "reason": reason,
            "run_id": index.run_id,
            "source_lock_ref": index.source_lock_ref,
            "stream_version": stream_version,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        return cls(
            invalidation_id=f"evidence-index-invalidation_{digest}",
            invalidation_hash=f"sha256:{digest}",
            command_id=command_id,
            run_id=index.run_id,
            index_id=index.index_id,
            index_hash=index.index_hash,
            source_lock_ref=index.source_lock_ref,
            authority_identity=authority_identity,
            reason=reason,
            event_ids=event_ids,
            stream_version=stream_version,
        )

    def validate(self, index: EvidenceIndex) -> None:
        if (
            self.run_id != index.run_id
            or self.index_id != index.index_id
            or self.index_hash != index.index_hash
            or self.source_lock_ref != index.source_lock_ref
            or not self.authority_identity.strip()
            or not self.command_id.strip()
            or not self.reason.strip()
            or not self.event_ids
            or self.stream_version <= 0
        ):
            raise EvidenceIndexInvalid(
                "Evidence-index invalidation does not match its historical index."
            )
        digest = sha256(_canonical_json(self._identity_payload())).hexdigest()
        if (
            self.invalidation_id != f"evidence-index-invalidation_{digest}"
            or self.invalidation_hash != f"sha256:{digest}"
        ):
            raise EvidenceIndexInvalid("Evidence-index invalidation identity is invalid.")

    def _identity_payload(self) -> dict[str, object]:
        return {
            "authority_identity": self.authority_identity,
            "command_id": self.command_id,
            "event_ids": self.event_ids,
            "index_hash": self.index_hash,
            "index_id": self.index_id,
            "reason": self.reason,
            "run_id": self.run_id,
            "source_lock_ref": self.source_lock_ref,
            "stream_version": self.stream_version,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                **self._identity_payload(),
                "invalidation_hash": self.invalidation_hash,
                "invalidation_id": self.invalidation_id,
            }
        )


def stable_specimen_id(descriptor: SourceDescriptor) -> str:
    payload = {
        "role": descriptor.role,
        "source_content_hash": f"sha256:{descriptor.sha256}",
        "source_id": descriptor.source_id,
    }
    return f"specimen_{sha256(_canonical_json(payload)).hexdigest()}"


def source_lock_identity_hash(source_lock: SourceLock) -> str:
    ordered = tuple(
        sorted(
            source_lock.ordered_descriptors,
            key=lambda item: (item.precedence, item.canonical_uri, item.sha256),
        )
    )
    payload = {
        "run_id": source_lock.run_id,
        "source_profile_ref": source_lock.source_profile_ref,
        "source_profile_hash": source_lock.source_profile_hash,
        "target_profile_ref": source_lock.target_profile_ref,
        "target_candidate_ref": source_lock.target_candidate_ref,
        "ordered_descriptors": [item.identity_payload() for item in ordered],
        "invalidates_lock_ref": source_lock.invalidates_lock_ref,
    }
    return f"sha256:{sha256(_canonical_json(payload)).hexdigest()}"


def _valid_prefixed_hash(value: str) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        return False
    raw = value[7:]
    return len(raw) == 64 and all(character in "0123456789abcdef" for character in raw)


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
