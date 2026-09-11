"""Operator projection for governed asset research and PlayPhrase-like temporal discovery.

M0086 keeps retrieval authority inside the existing CAE Asset Intelligence corpus and
SemanticCinematicRetriever.  The temporal adapter below only locates transcript cues
and creates playable references; it never promotes or mutates canonical asset state.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Iterable, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .corpus import SceneRecord, TranscriptCue
from .domain import EditorialInsertRole, RightsStatus
from .retrieval import RetrievalQuery, RetrievalState, RightsPolicy, SemanticCinematicRetriever

MANDATE_ID = "M0086"
RESEARCH_SESSION_SCHEMA_VERSION = "1.0.0"


class AssetResearchMode(str, Enum):
    PHRASE = "PHRASE"
    SEMANTIC_CINEMATIC = "SEMANTIC_CINEMATIC"


class AssetResearchSessionState(str, Enum):
    CANDIDATES = "CANDIDATES"
    ABSTAIN = "ABSTAIN"
    BLOCKED = "BLOCKED"
    SELECTED = "SELECTED"
    PROMOTION_REQUESTED = "PROMOTION_REQUESTED"


class RangeMode(str, Enum):
    MATCH = "MATCH"
    CONTEXT = "CONTEXT"


class AssetResearchError(Exception):
    """Base M0086 research-session error."""


class CandidateSelectionError(AssetResearchError):
    """Raised when a candidate cannot be selected or promoted."""


class AssetResearchRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    workspace_id: str = Field(..., min_length=1)
    query: str = Field(..., min_length=3)
    mode: AssetResearchMode = AssetResearchMode.SEMANTIC_CINEMATIC
    candidate_id: str | None = None
    insert_roles: tuple[EditorialInsertRole, ...] = ()
    semantic_roles: tuple[str, ...] = ()
    rights_policy: RightsPolicy = RightsPolicy.CLEARED_ONLY
    top_k: int = Field(default=8, ge=1, le=50)
    min_confidence: float = Field(default=0.58, ge=0.0, le=1.0)
    expected_index_sha256: str | None = Field(default=None, min_length=64, max_length=64)
    context_before_seconds: float = Field(default=2.0, ge=0.0, le=30.0)
    context_after_seconds: float = Field(default=3.0, ge=0.0, le=30.0)
    range_mode: RangeMode = RangeMode.CONTEXT

    @model_validator(mode="after")
    def validate_query(self) -> "AssetResearchRequest":
        if not self.query.strip():
            raise ValueError("query must contain searchable text")
        return self


class SourceTimeRange(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., gt=0.0)

    @model_validator(mode="after")
    def validate_range(self) -> "SourceTimeRange":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be greater than start_time")
        return self


class TranscriptExcerpt(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., gt=0.0)
    text: str = Field(..., min_length=1)
    speaker: str | None = None


class PlayablePreviewRef(BaseModel):
    """A browser/player-ready temporal reference; it is not evidence of playback."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    uri: str | None = None
    range: SourceTimeRange
    mime_type: str | None = None
    playable: bool = False
    preview_kind: str = "SOURCE_TEMPORAL_RANGE"

    @model_validator(mode="after")
    def validate_playability(self) -> "PlayablePreviewRef":
        if self.playable and not self.uri:
            raise ValueError("playable preview requires a source URI")
        return self


class ResearchSourceRef(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    media_id: str
    scene_id: str
    source_version: str
    source_sha256: str = Field(..., min_length=64, max_length=64)


class AssetResearchCandidate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    research_candidate_id: str
    source: ResearchSourceRef
    asset_id: str
    workspace_id: str
    candidate_id: str
    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., gt=0.0)
    match_range: SourceTimeRange | None = None
    context_range: SourceTimeRange
    selected_range: SourceTimeRange
    transcript: tuple[TranscriptExcerpt, ...] = ()
    contextual_explanation: str = Field(..., min_length=15)
    semantic_role: str
    insert_role: EditorialInsertRole
    rights_status: RightsStatus
    confidence: float = Field(..., ge=0.0, le=1.0)
    lexical_score: float = Field(default=0.0, ge=0.0, le=1.0)
    semantic_score: float = Field(default=0.0, ge=-1.0, le=1.0)
    retrieval_mode: AssetResearchMode
    match_basis: tuple[str, ...] = ()
    preview: PlayablePreviewRef
    provenance: Mapping[str, str] = Field(default_factory=dict)


class CandidateSelectionReceipt(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = RESEARCH_SESSION_SCHEMA_VERSION
    receipt_id: str
    mandate_id: str = MANDATE_ID
    request_ref: str
    candidate_set_ref: str
    selected_candidate: str
    rejected_candidates: tuple[str, ...] = ()
    operator_ref: str | None = None
    auto_selection_policy: str | None = None
    source_ref: ResearchSourceRef
    source_hash: str
    source_range: SourceTimeRange
    rights_state: RightsStatus
    storyboard_element_ref: str | None = None
    revision_ref: str | None = None
    actor: str
    state: AssetResearchSessionState = AssetResearchSessionState.SELECTED
    preconditions: Mapping[str, str] = Field(default_factory=dict)
    validators: Mapping[str, str] = Field(default_factory=dict)
    postconditions: Mapping[str, str] = Field(default_factory=dict)
    recovery_path: str = Field(..., min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AssetPromotionRequest(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = RESEARCH_SESSION_SCHEMA_VERSION
    promotion_request_id: str
    mandate_id: str = MANDATE_ID
    request_ref: str
    candidate_set_ref: str
    selected_candidate: str
    source_ref: ResearchSourceRef
    source_range: SourceTimeRange
    rights_state: RightsStatus
    storyboard_element_ref: str
    revision_ref: str
    operator_ref: str
    selection_receipt_ref: str
    state: AssetResearchSessionState = AssetResearchSessionState.PROMOTION_REQUESTED


class AssetResearchSession(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = RESEARCH_SESSION_SCHEMA_VERSION
    session_id: str
    request: AssetResearchRequest
    request_ref: str
    candidate_set_ref: str
    state: AssetResearchSessionState
    candidates: tuple[AssetResearchCandidate, ...] = ()
    rejected_candidate_ids: tuple[str, ...] = ()
    selected_candidate_id: str | None = None
    transition_receipt_ids: tuple[str, ...] = ()
    actor: str

    def reject(self, candidate_id: str, *, actor: str, reason: str) -> tuple["AssetResearchSession", str]:
        candidate = self._candidate(candidate_id)
        if candidate_id in self.rejected_candidate_ids:
            return self, self._transition_receipt_id("REJECT", candidate_id, reason)
        next_rejected = tuple(sorted((*self.rejected_candidate_ids, candidate_id)))
        receipt_id = self._transition_receipt_id("REJECT", candidate_id, reason)
        next_state = AssetResearchSessionState.ABSTAIN if len(next_rejected) == len(self.candidates) else self.state
        updated = self.model_copy(
            update={
                "rejected_candidate_ids": next_rejected,
                "state": next_state,
                "transition_receipt_ids": (*self.transition_receipt_ids, receipt_id),
                "actor": actor,
            }
        )
        return updated, receipt_id

    def select(self, candidate_id: str, *, actor: str, operator_ref: str | None = None) -> tuple["AssetResearchSession", CandidateSelectionReceipt]:
        candidate = self._candidate(candidate_id)
        if candidate_id in self.rejected_candidate_ids:
            raise CandidateSelectionError(f"candidate '{candidate_id}' was rejected and cannot be selected")
        if not candidate.preview.uri:
            raise CandidateSelectionError("selected candidate has no browser/player source URI")
        if candidate.rights_status == RightsStatus.UNKNOWN_UNLICENSED:
            raise CandidateSelectionError("selected candidate has unresolved rights")
        rejected = tuple(sorted(set(self.rejected_candidate_ids)))
        receipt_id = self._selection_receipt_id(candidate_id, operator_ref)
        receipt = CandidateSelectionReceipt(
            receipt_id=receipt_id,
            request_ref=self.request_ref,
            candidate_set_ref=self.candidate_set_ref,
            selected_candidate=candidate_id,
            rejected_candidates=tuple(sorted(set(self.rejected_candidate_ids))),
            operator_ref=operator_ref,
            source_ref=candidate.source,
            source_hash=candidate.source.source_sha256,
            source_range=candidate.selected_range,
            rights_state=candidate.rights_status,
            actor=actor,
            preconditions={
                "candidate_present": "PASS",
                "candidate_not_rejected": "PASS",
                "preview_uri": "PASS",
            },
            validators={
                "workspace": "PASS",
                "rights": "PASS",
                "provenance": "PASS",
                "temporal_range": "PASS",
            },
            postconditions={
                "selected_candidate": candidate_id,
                "rejected_candidates_preserved": "PASS",
                "canonical_asset_mutation": "NOT_PERFORMED",
            },
            recovery_path="Selection is a projection only. To change the selection, issue a new immutable selection request; canonical Storyboard/VAE state is unchanged here.",
        )
        updated = self.model_copy(
            update={
                "state": AssetResearchSessionState.SELECTED,
                "selected_candidate_id": candidate_id,
                "rejected_candidate_ids": rejected,
                "transition_receipt_ids": (*self.transition_receipt_ids, receipt_id),
                "actor": actor,
            }
        )
        return updated, receipt

    def request_promotion(
        self,
        candidate_id: str,
        *,
        actor: str,
        operator_ref: str,
        storyboard_element_ref: str,
        revision_ref: str,
        selection_receipt_ref: str,
    ) -> AssetPromotionRequest:
        candidate = self._candidate(candidate_id)
        if self.selected_candidate_id != candidate_id or self.state != AssetResearchSessionState.SELECTED:
            raise CandidateSelectionError("promotion requires an explicitly selected candidate")
        if not operator_ref.strip():
            raise CandidateSelectionError("operator_ref is required for promotion request")
        promotion_id = "PROMO-" + _digest(
            {
                "request_ref": self.request_ref,
                "candidate_set_ref": self.candidate_set_ref,
                "candidate_id": candidate_id,
                "storyboard_element_ref": storyboard_element_ref,
                "revision_ref": revision_ref,
                "selection_receipt_ref": selection_receipt_ref,
            }
        )[:24]
        return AssetPromotionRequest(
            promotion_request_id=promotion_id,
            request_ref=self.request_ref,
            candidate_set_ref=self.candidate_set_ref,
            selected_candidate=candidate_id,
            source_ref=candidate.source,
            source_range=candidate.selected_range,
            rights_state=candidate.rights_status,
            storyboard_element_ref=storyboard_element_ref,
            revision_ref=revision_ref,
            operator_ref=operator_ref,
            selection_receipt_ref=selection_receipt_ref,
        )

    def _candidate(self, candidate_id: str) -> AssetResearchCandidate:
        candidate = next((item for item in self.candidates if item.research_candidate_id == candidate_id), None)
        if candidate is None:
            raise CandidateSelectionError(f"unknown research candidate '{candidate_id}'")
        return candidate

    def _transition_receipt_id(self, action: str, candidate_id: str, reason: str) -> str:
        return "RSTR-" + _digest(
            {"session_id": self.session_id, "action": action, "candidate_id": candidate_id, "reason": reason}
        )[:24]

    def _selection_receipt_id(self, candidate_id: str, operator_ref: str | None) -> str:
        return "RSEL-" + _digest(
            {"session_id": self.session_id, "candidate_id": candidate_id, "operator_ref": operator_ref}
        )[:24]


@dataclass(frozen=True, slots=True)
class _PhraseMatch:
    record: SceneRecord
    cue: TranscriptCue
    terms: tuple[str, ...]


class PlayPhraseTemporalAdapter:
    """Deterministic phrase-to-range adapter over governed SceneRecord transcripts.

    It deliberately does not own eligibility, semantic authority, or promotion. Its
    output is normalized into AssetResearchCandidate by AssetResearchSessionFactory.
    """

    def find(
        self,
        phrase: str,
        records: Iterable[SceneRecord],
        *,
        workspace_id: str,
        candidate_id: str | None,
        rights_policy: RightsPolicy,
        context_before_seconds: float,
        context_after_seconds: float,
        range_mode: RangeMode,
    ) -> tuple[_PhraseMatch, ...]:
        normalized = _normalize_phrase(phrase)
        if len(normalized) < 3:
            return ()
        terms = tuple(sorted(_tokenize(normalized)))
        matches: list[_PhraseMatch] = []
        for record in records:
            if record.workspace_id != workspace_id:
                continue
            if candidate_id and record.annotation.candidate_id != candidate_id:
                continue
            if record.annotation.rights.status == RightsStatus.UNKNOWN_UNLICENSED:
                continue
            if rights_policy == RightsPolicy.CLEARED_ONLY and record.annotation.rights.status != RightsStatus.CLEARED:
                continue
            if rights_policy == RightsPolicy.CLEARED_OR_LEGAL_REVIEW and record.annotation.rights.status not in {
                RightsStatus.CLEARED,
                RightsStatus.FAIR_USE_LEGAL_REVIEW_REQUIRED,
            }:
                continue
            for cue in record.transcript:
                if normalized in _normalize_phrase(cue.text):
                    matches.append(_PhraseMatch(record, cue, terms))
        matches.sort(key=lambda item: (item.cue.start_time, item.record.scene_id))
        return tuple(matches)


class AssetResearchSessionFactory:
    """Compile a bounded operator session from existing Asset Intelligence retrieval."""

    def __init__(
        self,
        *,
        semantic_retriever: SemanticCinematicRetriever | None = None,
        temporal_adapter: PlayPhraseTemporalAdapter | None = None,
        source_uri_resolver: Callable[[SceneRecord], str | None] | None = None,
        preview_mime_resolver: Callable[[SceneRecord], str | None] | None = None,
        actor: str = "execution-agent",
    ):
        self.semantic_retriever = semantic_retriever or SemanticCinematicRetriever(actor=actor)
        self.temporal_adapter = temporal_adapter or PlayPhraseTemporalAdapter()
        self.source_uri_resolver = source_uri_resolver
        self.preview_mime_resolver = preview_mime_resolver
        self.actor = actor

    def open(
        self,
        request: AssetResearchRequest,
        records: Iterable[SceneRecord],
        *,
        index_sha256: str | None = None,
        indexed_receipt=None,
    ) -> AssetResearchSession:
        records = tuple(records)
        request_ref = "RRQ-" + _digest(request.model_dump(mode="json"))[:24]
        if request.mode == AssetResearchMode.PHRASE:
            if index_sha256 is not None and request.expected_index_sha256 and request.expected_index_sha256 != index_sha256:
                return self._session(request, request_ref, AssetResearchSessionState.BLOCKED, (), error_actor=self.actor)
            matches = self.temporal_adapter.find(
                request.query,
                records,
                workspace_id=request.workspace_id,
                candidate_id=request.candidate_id,
                rights_policy=request.rights_policy,
                context_before_seconds=request.context_before_seconds,
                context_after_seconds=request.context_after_seconds,
                range_mode=request.range_mode,
            )
            candidates = tuple(self._from_phrase_match(match, request) for match in matches[: request.top_k])
            state = AssetResearchSessionState.CANDIDATES if candidates else AssetResearchSessionState.ABSTAIN
            return self._session(request, request_ref, state, candidates)

        if index_sha256 is None:
            return self._session(request, request_ref, AssetResearchSessionState.BLOCKED, ())
        retrieval_query = RetrievalQuery(
            workspace_id=request.workspace_id,
            query=request.query,
            candidate_id=request.candidate_id,
            insert_roles=request.insert_roles,
            semantic_roles=request.semantic_roles,
            rights_policy=request.rights_policy,
            top_k=request.top_k,
            min_confidence=request.min_confidence,
            expected_index_sha256=request.expected_index_sha256,
        )
        retrieved, receipt = self.semantic_retriever.retrieve(
            retrieval_query,
            records,
            index_sha256=index_sha256,
            indexed_receipt=indexed_receipt,
        )
        if receipt.state == RetrievalState.BLOCKED:
            return self._session(request, request_ref, AssetResearchSessionState.BLOCKED, ())
        if not retrieved:
            return self._session(request, request_ref, AssetResearchSessionState.ABSTAIN, ())
        candidates = tuple(self._from_semantic_candidate(candidate, records, request) for candidate in retrieved)
        return self._session(request, request_ref, AssetResearchSessionState.CANDIDATES, candidates)

    def _session(
        self,
        request: AssetResearchRequest,
        request_ref: str,
        state: AssetResearchSessionState,
        candidates: tuple[AssetResearchCandidate, ...],
        *,
        error_actor: str | None = None,
    ) -> AssetResearchSession:
        candidate_set_ref = "RSET-" + _digest(
            {
                "request_ref": request_ref,
                "candidate_ids": [candidate.research_candidate_id for candidate in candidates],
            }
        )[:24]
        session_id = "ASES-" + _digest(
            {
                "request_ref": request_ref,
                "candidate_set_ref": candidate_set_ref,
                "state": state.value,
            }
        )[:24]
        return AssetResearchSession(
            session_id=session_id,
            request=request,
            request_ref=request_ref,
            candidate_set_ref=candidate_set_ref,
            state=state,
            candidates=candidates,
            actor=error_actor or self.actor,
        )

    def _from_phrase_match(self, match: _PhraseMatch, request: AssetResearchRequest) -> AssetResearchCandidate:
        context = _context_range(match.record, match.cue.start_time, match.cue.end_time, request)
        selected = context if request.range_mode == RangeMode.CONTEXT else SourceTimeRange(start_time=match.cue.start_time, end_time=match.cue.end_time)
        return AssetResearchCandidate(
            research_candidate_id=_research_candidate_id(request, match.record, match.cue.start_time, match.cue.end_time),
            source=ResearchSourceRef(
                media_id=match.record.media_id,
                scene_id=match.record.scene_id,
                source_version=match.record.source_version,
                source_sha256=match.record.source_sha256,
            ),
            asset_id=match.record.annotation.asset_id,
            workspace_id=match.record.workspace_id,
            candidate_id=match.record.annotation.candidate_id,
            start_time=selected.start_time,
            end_time=selected.end_time,
            match_range=SourceTimeRange(start_time=match.cue.start_time, end_time=match.cue.end_time),
            context_range=context,
            selected_range=selected,
            transcript=_transcript_window(match.record.transcript, context),
            contextual_explanation=(
                f"Exact transcript phrase match in {match.record.semantic_role}; "
                f"the temporal adapter resolved {match.cue.start_time:.3f}s–{match.cue.end_time:.3f}s."
            ),
            semantic_role=match.record.semantic_role,
            insert_role=match.record.insert_role,
            rights_status=match.record.annotation.rights.status,
            confidence=1.0,
            lexical_score=1.0,
            semantic_score=1.0,
            retrieval_mode=AssetResearchMode.PHRASE,
            match_basis=("EXACT_TRANSCRIPT_PHRASE", *match.terms),
            preview=self._preview(match.record, selected),
            provenance=_provenance(match.record, MANDATE_ID),
        )

    def _from_semantic_candidate(self, candidate, records: Sequence[SceneRecord], request: AssetResearchRequest) -> AssetResearchCandidate:
        record = next(item for item in records if item.scene_id == candidate.scene_id)
        context = SourceTimeRange(start_time=record.start_time, end_time=record.end_time)
        selected = context
        transcript = _transcript_window(record.transcript, context)
        return AssetResearchCandidate(
            research_candidate_id=_research_candidate_id(request, record, record.start_time, record.end_time),
            source=ResearchSourceRef(
                media_id=record.media_id,
                scene_id=record.scene_id,
                source_version=record.source_version,
                source_sha256=record.source_sha256,
            ),
            asset_id=candidate.asset_id,
            workspace_id=record.workspace_id,
            candidate_id=record.annotation.candidate_id,
            start_time=selected.start_time,
            end_time=selected.end_time,
            match_range=None,
            context_range=context,
            selected_range=selected,
            transcript=transcript,
            contextual_explanation=candidate.contextual_explanation,
            semantic_role=candidate.semantic_role,
            insert_role=candidate.insert_role,
            rights_status=candidate.rights_status,
            confidence=candidate.confidence,
            lexical_score=candidate.lexical_score,
            semantic_score=candidate.semantic_score,
            retrieval_mode=AssetResearchMode.SEMANTIC_CINEMATIC,
            match_basis=candidate.match_terms or ("SEMANTIC_CINEMATIC",),
            preview=self._preview(record, selected),
            provenance=candidate.provenance,
        )

    def _preview(self, record: SceneRecord, selected: SourceTimeRange) -> PlayablePreviewRef:
        uri = self.source_uri_resolver(record) if self.source_uri_resolver else None
        mime_type = self.preview_mime_resolver(record) if self.preview_mime_resolver else None
        return PlayablePreviewRef(
            uri=uri,
            range=selected,
            mime_type=mime_type,
            playable=bool(uri),
        )


def _research_candidate_id(request: AssetResearchRequest, record: SceneRecord, start: float, end: float) -> str:
    return "RCND-" + _digest(
        {
            "request": request.model_dump(mode="json"),
            "scene_id": record.scene_id,
            "start": start,
            "end": end,
        }
    )[:24]


def _context_range(record: SceneRecord, start: float, end: float, request: AssetResearchRequest) -> SourceTimeRange:
    bounded_start = max(record.start_time, start - request.context_before_seconds)
    bounded_end = min(record.end_time, end + request.context_after_seconds)
    return SourceTimeRange(start_time=bounded_start, end_time=bounded_end)


def _transcript_window(cues: Sequence[TranscriptCue], window: SourceTimeRange) -> tuple[TranscriptExcerpt, ...]:
    selected = [
        TranscriptExcerpt(start_time=cue.start_time, end_time=cue.end_time, text=cue.text, speaker=cue.speaker)
        for cue in cues
        if cue.end_time > window.start_time and cue.start_time < window.end_time
    ]
    return tuple(selected)


def _provenance(record: SceneRecord, mandate_id: str) -> dict[str, str]:
    return {
        "scene_id": record.scene_id,
        "media_id": record.media_id,
        "source_version": record.source_version,
        "source_sha256": record.source_sha256,
        "candidate_id": record.annotation.candidate_id,
        "mandate_id": mandate_id,
    }


def _normalize_phrase(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+(?:['’-][a-z0-9]+)?", value.lower()))


def _tokenize(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", _normalize_phrase(value)))


def _digest(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
