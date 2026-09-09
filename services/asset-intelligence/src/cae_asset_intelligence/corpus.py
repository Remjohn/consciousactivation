"""
CAE-M0062 cinematic corpus ingestion and scene organization.

The corpus layer is a derived projection over the canonical AssetAnnotation
contract. It accepts only explicitly authorized source bytes, produces stable
millisecond-aligned scene identities, and emits immutable ingest receipts.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Iterable, Mapping, Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .annotator import AssetAnnotator
from .domain import AssetAnnotation, EditorialInsertRole, MediaType, RightsMetadata, SourceType
from .errors import AssetByteHashMismatchError, AssetIntelligenceError, MissingRightsEvidenceError


MANDATE_ID = "CAE-M0062"
SCHEMA_VERSION = "1.0.0"


class CorpusState(str, Enum):
    SOURCE_ACCEPTED = "SOURCE_ACCEPTED"
    INGESTED = "INGESTED"
    INDEXED = "INDEXED"
    QUARANTINED = "QUARANTINED"


class CorpusIngestionError(AssetIntelligenceError):
    """Base error for governed cinematic corpus ingestion."""


class AuthorizationError(CorpusIngestionError):
    """The source is not explicitly approved for this workspace and bytes."""


class SceneBoundaryError(CorpusIngestionError):
    """Scene boundaries are unstable, overlapping, or outside source duration."""


class CorpusIntegrityError(CorpusIngestionError):
    """A derived scene/index record fails source or time-range verification."""


class IngestStateError(CorpusIngestionError):
    """A requested state transition is not valid for the current receipt."""


class MediaAuthorization(BaseModel):
    """Operator/legal authorization record; it never upgrades rights status."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    authorization_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    source_sha256: str = Field(..., min_length=64, max_length=64)
    source_version: str = Field(..., min_length=1)
    approved: bool = False
    authority_ref: str = Field(..., min_length=1)


class TranscriptCue(BaseModel):
    """Optional dialogue/transcript evidence attached to a scene range."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., gt=0.0)
    text: str = Field(..., min_length=1)
    speaker: Optional[str] = None

    @model_validator(mode="after")
    def validate_range(self) -> "TranscriptCue":
        if self.end_time <= self.start_time:
            raise ValueError("Transcript cue end_time must be greater than start_time")
        return self


class SceneProposal(BaseModel):
    """Deterministic scene-segmentation output supplied by the upstream analyzer."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., gt=0.0)
    contextual_caption: str = Field(..., min_length=15)
    semantic_role: str = Field(..., min_length=3)
    insert_role: EditorialInsertRole = EditorialInsertRole.WORLD_BUILDING
    media_type: MediaType = MediaType.VIDEO_CLIP
    source_type: SourceType = SourceType.ARCHIVAL
    transcript: tuple[TranscriptCue, ...] = ()
    metadata: Mapping[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_range(self) -> "SceneProposal":
        if self.end_time <= self.start_time:
            raise ValueError("SceneProposal end_time must be greater than start_time")
        return self


class SceneRecord(BaseModel):
    """Governed scene corpus record backed by one canonical AssetAnnotation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = SCHEMA_VERSION
    scene_id: str = Field(..., min_length=1)
    media_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    source_version: str = Field(..., min_length=1)
    source_sha256: str = Field(..., min_length=64, max_length=64)
    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., gt=0.0)
    contextual_caption: str = Field(..., min_length=15)
    semantic_role: str = Field(..., min_length=3)
    insert_role: EditorialInsertRole
    transcript: tuple[TranscriptCue, ...] = ()
    annotation: AssetAnnotation
    metadata: Mapping[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_annotation_lineage(self) -> "SceneRecord":
        if self.end_time <= self.start_time:
            raise ValueError("SceneRecord end_time must be greater than start_time")
        if self.annotation.workspace_id != self.workspace_id:
            raise CorpusIntegrityError("Scene annotation workspace does not match corpus workspace")
        if self.annotation.source_sha256 != self.source_sha256:
            raise CorpusIntegrityError("Scene annotation hash does not match corpus source hash")
        if self.annotation.start_time != self.start_time or self.annotation.end_time != self.end_time:
            raise CorpusIntegrityError("Scene annotation time range does not match scene record")
        if self.annotation.contextual_caption != self.contextual_caption:
            raise CorpusIntegrityError("Scene annotation caption does not match scene record")
        return self


class IngestReceipt(BaseModel):
    """Immutable receipt for one source verification and corpus projection attempt."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = SCHEMA_VERSION
    receipt_id: str = Field(..., min_length=1)
    ingest_key: str = Field(..., min_length=1)
    mandate_id: str = MANDATE_ID
    workspace_id: str = Field(..., min_length=1)
    authorization_id: str = Field(..., min_length=1)
    source_version: str = Field(..., min_length=1)
    source_sha256: str = Field(..., min_length=64, max_length=64)
    state: CorpusState
    scene_ids: tuple[str, ...] = ()
    actor: str = Field(..., min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    validator_results: Mapping[str, str] = Field(default_factory=dict)
    error_code: Optional[str] = None
    error_detail: Optional[str] = None
    recovery_path: str = Field(..., min_length=1)

    @field_validator("source_sha256")
    @classmethod
    def validate_hex(cls, value: str) -> str:
        try:
            int(value, 16)
        except ValueError as exc:
            raise ValueError("source_sha256 must be hexadecimal") from exc
        return value.lower()


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def stable_media_id(workspace_id: str, source_sha256: str, source_version: str) -> str:
    """Stable identity derived only from governed source identity, never random UUIDs."""
    return "MED-" + _canonical_hash({"workspace_id": workspace_id, "source_sha256": source_sha256, "source_version": source_version})[:24]


def stable_scene_id(media_id: str, start_time: float, end_time: float) -> str:
    """Stable scene identity using exact millisecond boundaries."""
    start_ms = round(start_time * 1000)
    end_ms = round(end_time * 1000)
    return f"SCN-{_canonical_hash({'media_id': media_id, 'start_ms': start_ms, 'end_ms': end_ms})[:24]}"


def _normalize_seconds(value: float) -> float:
    return round(value, 3)


class CinematicCorpusEngine:
    """Bounded, deterministic source-to-scene corpus projection."""

    def __init__(self, *, actor: str = "execution-agent", captioner: Optional[Callable[[SceneProposal], str]] = None):
        self.actor = actor
        self.captioner = captioner

    def ingest(
        self,
        *,
        workspace_id: str,
        candidate_id: str,
        source_version: str,
        source_bytes: bytes,
        media_duration: float,
        authorization: MediaAuthorization,
        rights: RightsMetadata,
        scenes: Sequence[SceneProposal],
    ) -> tuple[tuple[SceneRecord, ...], IngestReceipt]:
        """Verify authorized bytes/time ranges, annotate scenes, and return an immutable receipt.

        The engine does not fetch remote media, infer legal clearance, or mutate canonical assets.
        """
        actual_hash = hashlib.sha256(source_bytes).hexdigest()
        ingest_key = _canonical_hash({"workspace_id": workspace_id, "source_sha256": actual_hash, "source_version": source_version})
        try:
            self._validate_authorization(workspace_id, actual_hash, source_version, authorization)
            if media_duration <= 0:
                raise SceneBoundaryError("media_duration must be positive")
            normalized = self._validate_scene_boundaries(scenes, media_duration)
            if rights.status.value == "CLEARED" and not rights.license_id and not rights.proof_url:
                raise MissingRightsEvidenceError("Assets marked CLEARED must provide a valid license_id or proof_url documentation.")

            media_id = stable_media_id(workspace_id, actual_hash, source_version)
            records: list[SceneRecord] = []
            for proposal in normalized:
                caption = self.captioner(proposal) if self.captioner else proposal.contextual_caption
                caption = caption.strip()
                annotation = AssetAnnotator.annotate_insert(
                    candidate_id=candidate_id,
                    workspace_id=workspace_id,
                    source_type=proposal.source_type,
                    media_type=proposal.media_type,
                    start_time=proposal.start_time,
                    end_time=proposal.end_time,
                    contextual_caption=caption,
                    semantic_role=proposal.semantic_role,
                    insert_role=proposal.insert_role,
                    source_sha256=actual_hash,
                    rights=rights,
                )
                records.append(
                    SceneRecord(
                        scene_id=stable_scene_id(media_id, proposal.start_time, proposal.end_time),
                        media_id=media_id,
                        workspace_id=workspace_id,
                        source_version=source_version,
                        source_sha256=actual_hash,
                        start_time=proposal.start_time,
                        end_time=proposal.end_time,
                        contextual_caption=caption,
                        semantic_role=proposal.semantic_role,
                        insert_role=proposal.insert_role,
                        transcript=proposal.transcript,
                        annotation=annotation,
                        metadata=proposal.metadata,
                    )
                )
            receipt = self._receipt(
                ingest_key=ingest_key,
                workspace_id=workspace_id,
                authorization_id=authorization.authorization_id,
                source_version=source_version,
                source_sha256=actual_hash,
                state=CorpusState.INGESTED,
                scene_ids=tuple(r.scene_id for r in records),
                validator_results={"authorization": "PASS", "sha256": "PASS", "time_ranges": "PASS", "rights": "PASS"},
                recovery_path="Index derived records; if indexing fails preserve this receipt and quarantine derived records only.",
            )
            return tuple(records), receipt
        except (AuthorizationError, SceneBoundaryError, MissingRightsEvidenceError, AssetByteHashMismatchError, CorpusIntegrityError, ValueError) as exc:
            code = exc.__class__.__name__.replace("Error", "").upper()
            receipt = self._receipt(
                ingest_key=ingest_key,
                workspace_id=workspace_id,
                authorization_id=authorization.authorization_id,
                source_version=source_version,
                source_sha256=actual_hash,
                state=CorpusState.QUARANTINED,
                validator_results={"authorization": "FAIL" if isinstance(exc, AuthorizationError) else "PASS", "sha256": "PASS", "time_ranges": "NOT_RUN", "rights": "NOT_RUN"},
                error_code=code,
                error_detail=str(exc),
                recovery_path="Preserve receipt; repair authorization or source/scene input; re-run as a new immutable attempt.",
            )
            return (), receipt

    def index_receipt(self, receipt: IngestReceipt, scene_ids: Sequence[str], index_sha256: str) -> IngestReceipt:
        """Create a new immutable INDEXED receipt after derived index persistence succeeds."""
        if receipt.state != CorpusState.INGESTED:
            raise IngestStateError("Only INGESTED receipts may transition to INDEXED")
        payload = {
            "ingest_receipt_id": receipt.receipt_id,
            "scene_ids": tuple(scene_ids),
            "index_sha256": index_sha256,
            "workspace_id": receipt.workspace_id,
            "source_sha256": receipt.source_sha256,
        }
        indexed_id = "RCPT-" + _canonical_hash(payload)[:24]
        return IngestReceipt(
            receipt_id=indexed_id,
            ingest_key=receipt.ingest_key,
            authorization_id=receipt.authorization_id,
            workspace_id=receipt.workspace_id,
            source_version=receipt.source_version,
            source_sha256=receipt.source_sha256,
            state=CorpusState.INDEXED,
            scene_ids=tuple(scene_ids),
            actor=self.actor,
            validator_results={**receipt.validator_results, "index": "PASS"},
            recovery_path="Remove only derived index records; preserve source, scenes, and both immutable receipts.",
        )

    @staticmethod
    def _validate_authorization(workspace_id: str, actual_hash: str, source_version: str, authorization: MediaAuthorization) -> None:
        if not authorization.approved:
            raise AuthorizationError("Media authorization is not approved")
        if authorization.workspace_id != workspace_id:
            raise AuthorizationError("Authorization workspace does not match ingest workspace")
        if authorization.source_sha256.lower() != actual_hash:
            raise AssetByteHashMismatchError("Authorized source hash does not match provided media bytes")
        if authorization.source_version != source_version:
            raise AuthorizationError("Authorization source_version does not match ingest source_version")

    @staticmethod
    def _validate_scene_boundaries(scenes: Sequence[SceneProposal], media_duration: float) -> tuple[SceneProposal, ...]:
        if not scenes:
            raise SceneBoundaryError("At least one scene proposal is required")
        ordered = tuple(sorted(scenes, key=lambda s: (s.start_time, s.end_time)))
        previous_end = 0.0
        for idx, scene in enumerate(ordered, start=1):
            start = _normalize_seconds(scene.start_time)
            end = _normalize_seconds(scene.end_time)
            if start != scene.start_time or end != scene.end_time:
                scene = scene.model_copy(update={"start_time": start, "end_time": end})
                ordered = tuple(scene if i == idx - 1 else old for i, old in enumerate(ordered))
            if end > media_duration:
                raise SceneBoundaryError(f"Scene {idx} ends at {end}s beyond media duration {media_duration}s")
            if start < previous_end:
                raise SceneBoundaryError(f"Scene {idx} overlaps the prior scene")
            previous_end = end
        return ordered

    def _receipt(self, **kwargs: object) -> IngestReceipt:
        payload = {k: (v.value if isinstance(v, Enum) else v) for k, v in kwargs.items()}
        receipt_id = "RCPT-" + _canonical_hash(payload)[:24]
        return IngestReceipt(receipt_id=receipt_id, actor=self.actor, **kwargs)


class SceneIndex:
    """Deterministic in-memory search projection over governed scene records."""

    @staticmethod
    def build(records: Iterable[SceneRecord]) -> dict[str, tuple[str, ...]]:
        index: dict[str, set[str]] = {}
        for scene in sorted(records, key=lambda r: r.scene_id):
            tokens = SceneIndex._tokens(scene.contextual_caption, scene.semantic_role, scene.insert_role.value, scene.transcript)
            for token in tokens:
                index.setdefault(token, set()).add(scene.scene_id)
        return {token: tuple(sorted(ids)) for token, ids in sorted(index.items())}

    @staticmethod
    def search(index: Mapping[str, Sequence[str]], query: str) -> tuple[str, ...]:
        tokens = SceneIndex._tokens(query)
        if not tokens:
            return ()
        sets = [set(index.get(token, ())) for token in tokens]
        if not sets:
            return ()
        return tuple(sorted(set.intersection(*sets)))

    @staticmethod
    def _tokens(*values: object) -> set[str]:
        raw: list[str] = []
        for value in values:
            if isinstance(value, tuple):
                for cue in value:
                    raw.append(cue.text)
            else:
                raw.append(str(value))
        return {token for text in raw for token in __import__("re").findall(r"[a-z0-9]+", text.lower()) if len(token) > 2}
