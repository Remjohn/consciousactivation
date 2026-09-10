"""Governed natural-language retrieval over the CAE cinematic scene corpus."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Iterable, Mapping, Protocol, Sequence

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .corpus import CorpusState, IngestReceipt, SceneRecord
from .domain import EditorialInsertRole, RightsStatus

MANDATE_ID = "CAE-M0063"
RETRIEVAL_SCHEMA_VERSION = "1.0.0"


class RetrievalError(Exception):
    """Base retrieval error."""


class RetrievalState(str, Enum):
    RETRIEVAL_REQUESTED = "RETRIEVAL_REQUESTED"
    CANDIDATES = "CANDIDATES"
    RANKED = "RANKED"
    ABSTAIN = "ABSTAIN"
    BLOCKED = "BLOCKED"


class RightsPolicy(str, Enum):
    CLEARED_ONLY = "CLEARED_ONLY"
    CLEARED_OR_LEGAL_REVIEW = "CLEARED_OR_LEGAL_REVIEW"


class EmbeddingModel(Protocol):
    model_id: str
    dimension: int

    def embed(self, text: str) -> Sequence[float]: ...


class DeterministicSemanticEncoder:
    """Provider-neutral local encoder used only when no external model is bound.

    It is deterministic, explainable, and deliberately not presented as a trained
    model. Semantic neighborhood expansion uses governed editorial paraphrases and
    hashing to create vectors; a promoted external model must be injected explicitly.
    """

    model_id = "cae-deterministic-semantic-v1"
    dimension = 256

    _GROUPS = (
        ("dawn", "sunrise", "early morning", "before sunrise"),
        ("pressure", "tension", "stress", "high stakes", "under pressure"),
        ("decision", "choice", "decisive", "operational choice", "turning point"),
        ("control room", "operations room", "command center", "control-room"),
        ("failure", "breakdown", "mistake", "operational failure", "failed"),
        ("response", "reaction", "aftermath", "responding"),
        ("setting", "location", "place", "environment", "world"),
        ("team", "crew", "staff", "operators"),
        ("contrast", "opposition", "difference", "counterpoint"),
        ("emotion", "emotional", "feeling", "human reaction"),
    )

    def __init__(self, *, model_id: str | None = None):
        self.model_id = model_id or self.model_id
        self._aliases: dict[str, str] = {}
        for group in self._GROUPS:
            anchor = group[0]
            for term in group:
                self._aliases[term] = anchor

    def embed(self, text: str) -> Sequence[float]:
        vector = [0.0] * self.dimension
        tokens = self._semantic_tokens(text)
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = int.from_bytes(digest[:4], "big") % self.dimension
            sign = 1.0 if digest[4] & 1 else -1.0
            vector[idx] += sign
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return tuple(vector)
        return tuple(value / norm for value in vector)

    def _semantic_tokens(self, text: str) -> tuple[str, ...]:
        lowered = text.lower()
        phrases = sorted(self._aliases, key=len, reverse=True)
        for phrase in phrases:
            if phrase in lowered:
                lowered += " " + self._aliases[phrase]
        words = re.findall(r"[a-z0-9]+", lowered)
        return tuple(sorted(set(word for word in words if len(word) > 2)))


class RetrievalQuery(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    workspace_id: str = Field(..., min_length=1)
    query: str = Field(..., min_length=3)
    candidate_id: str | None = None
    insert_roles: tuple[EditorialInsertRole, ...] = ()
    semantic_roles: tuple[str, ...] = ()
    rights_policy: RightsPolicy = RightsPolicy.CLEARED_ONLY
    top_k: int = Field(default=5, ge=1, le=50)
    min_confidence: float = Field(default=0.58, ge=0.0, le=1.0)
    expected_index_sha256: str | None = Field(default=None, min_length=64, max_length=64)

    @model_validator(mode="after")
    def validate_query(self) -> "RetrievalQuery":
        if not self.query.strip():
            raise ValueError("query must contain searchable text")
        return self


class RetrievalCandidate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    scene_id: str
    asset_id: str
    workspace_id: str
    source_version: str
    source_sha256: str
    start_time: float
    end_time: float
    duration: float
    contextual_explanation: str = Field(..., min_length=15)
    semantic_role: str
    insert_role: EditorialInsertRole
    rights_status: RightsStatus
    lexical_score: float = Field(..., ge=0.0, le=1.0)
    semantic_score: float = Field(..., ge=-1.0, le=1.0)
    hybrid_score: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    match_terms: tuple[str, ...] = ()
    provenance: Mapping[str, str] = Field(default_factory=dict)


class RetrievalReceipt(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = RETRIEVAL_SCHEMA_VERSION
    receipt_id: str
    mandate_id: str = MANDATE_ID
    request_digest: str
    workspace_id: str
    actor: str
    state: RetrievalState
    model_id: str
    candidates: tuple[str, ...] = ()
    selected_scene_ids: tuple[str, ...] = ()
    query: str
    confidence_threshold: float
    validator_results: Mapping[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error_code: str | None = None
    error_detail: str | None = None
    recovery_path: str = Field(..., min_length=1)


@dataclass(frozen=True)
class _ScoredScene:
    record: SceneRecord
    lexical: float
    semantic: float
    hybrid: float
    terms: tuple[str, ...]


class SemanticCinematicRetriever:
    """Fail-closed hybrid retriever over already-governed scene records."""

    def __init__(self, model: EmbeddingModel | None = None, *, actor: str = "execution-agent"):
        self.model = model or DeterministicSemanticEncoder()
        self.actor = actor

    def retrieve(
        self,
        query: RetrievalQuery,
        records: Iterable[SceneRecord],
        *,
        index_sha256: str,
        index_state: CorpusState = CorpusState.INDEXED,
        indexed_receipt: IngestReceipt | None = None,
    ) -> tuple[tuple[RetrievalCandidate, ...], RetrievalReceipt]:
        request_digest = _digest(query.model_dump(mode="json"))
        try:
            self._validate_index(query, index_sha256, index_state, indexed_receipt)
            eligible = [record for record in records if self._eligible(record, query)]
            scored = self._score(query.query, eligible)
            if not scored or scored[0].hybrid < query.min_confidence:
                receipt = self._receipt(
                    request_digest=request_digest,
                    query=query,
                    state=RetrievalState.ABSTAIN,
                    candidates=tuple(s.record.scene_id for s in scored[: query.top_k]),
                    selected_scene_ids=(),
                    validator_results={"workspace": "PASS", "rights": "PASS", "index": "PASS", "confidence": "FAIL"},
                    error_code="LOW_CONFIDENCE",
                    error_detail="No candidate exceeded the governed retrieval confidence threshold.",
                    recovery_path="Refine the query or lower the threshold only through governed operator configuration; preserve this receipt.",
                )
                return (), receipt

            chosen = scored[: query.top_k]
            candidates = tuple(self._candidate(item, query) for item in chosen)
            receipt = self._receipt(
                request_digest=request_digest,
                query=query,
                state=RetrievalState.RANKED,
                candidates=tuple(item.record.scene_id for item in scored),
                selected_scene_ids=tuple(candidate.scene_id for candidate in candidates),
                validator_results={"workspace": "PASS", "rights": "PASS", "index": "PASS", "confidence": "PASS"},
                recovery_path="Preserve receipt and rerun as a new request when governed corpus/model/index inputs change.",
            )
            return candidates, receipt
        except RetrievalError as exc:
            receipt = self._receipt(
                request_digest=request_digest,
                query=query,
                state=RetrievalState.BLOCKED,
                validator_results={"workspace": "UNKNOWN", "rights": "UNKNOWN", "index": "FAIL"},
                error_code=type(exc).__name__.replace("Error", "").upper(),
                error_detail=str(exc),
                recovery_path="Do not return candidates. Repair the governed index or request constraints, then issue a new retrieval request.",
            )
            return (), receipt

    def _validate_index(self, query: RetrievalQuery, index_sha256: str, index_state: CorpusState, receipt: IngestReceipt | None) -> None:
        if index_state != CorpusState.INDEXED:
            raise RetrievalError("Retrieval requires an INDEXED corpus")
        if query.expected_index_sha256 and query.expected_index_sha256 != index_sha256:
            raise RetrievalError("Provided index hash does not match the expected governed index")
        if receipt is not None and receipt.state != CorpusState.INDEXED:
            raise RetrievalError("Indexed receipt is not in INDEXED state")
        if receipt is not None and receipt.workspace_id != query.workspace_id:
            raise RetrievalError("Indexed receipt workspace does not match query workspace")

    @staticmethod
    def _eligible(record: SceneRecord, query: RetrievalQuery) -> bool:
        if record.workspace_id != query.workspace_id:
            return False
        if query.candidate_id and record.annotation.candidate_id != query.candidate_id:
            return False
        if query.insert_roles and record.insert_role not in query.insert_roles:
            return False
        if query.semantic_roles and record.semantic_role not in query.semantic_roles:
            return False
        if query.rights_policy == RightsPolicy.CLEARED_ONLY and record.annotation.rights.status != RightsStatus.CLEARED:
            return False
        if query.rights_policy == RightsPolicy.CLEARED_OR_LEGAL_REVIEW and record.annotation.rights.status not in {
            RightsStatus.CLEARED,
            RightsStatus.FAIR_USE_LEGAL_REVIEW_REQUIRED,
        }:
            return False
        return True

    def _score(self, query_text: str, records: Sequence[SceneRecord]) -> list[_ScoredScene]:
        query_tokens = self._tokens(query_text)
        query_vector = self.model.embed(query_text)
        scored: list[_ScoredScene] = []
        for record in records:
            haystack = " ".join((record.contextual_caption, record.semantic_role, record.insert_role.value, *(cue.text for cue in record.transcript)))
            doc_tokens = self._tokens(haystack)
            overlap = query_tokens & doc_tokens
            lexical = len(overlap) / max(len(query_tokens), 1)
            semantic = self._cosine(query_vector, self.model.embed(haystack))
            # Semantic score is clipped to a bounded positive contribution. Lexical
            # precision gets a small boost so exact terminology remains strong.
            semantic_norm = max(0.0, semantic)
            hybrid = min(1.0, 0.58 * semantic_norm + 0.42 * lexical)
            scored.append(_ScoredScene(record, lexical, semantic, hybrid, tuple(sorted(overlap))))
        return sorted(scored, key=lambda item: (-item.hybrid, -item.lexical, item.record.scene_id))

    @staticmethod
    def _candidate(item: _ScoredScene, query: RetrievalQuery) -> RetrievalCandidate:
        confidence = round(min(1.0, item.hybrid), 6)
        explanation = (
            f"Matches '{query.query}' through {', '.join(item.terms) or 'semantic context'}; "
            f"the scene is annotated as {item.record.semantic_role} and serves as {item.record.insert_role.value.lower().replace('_', ' ')}."
        )
        return RetrievalCandidate(
            scene_id=item.record.scene_id,
            asset_id=item.record.annotation.asset_id,
            workspace_id=item.record.workspace_id,
            source_version=item.record.source_version,
            source_sha256=item.record.source_sha256,
            start_time=item.record.start_time,
            end_time=item.record.end_time,
            duration=item.record.annotation.duration,
            contextual_explanation=explanation,
            semantic_role=item.record.semantic_role,
            insert_role=item.record.insert_role,
            rights_status=item.record.annotation.rights.status,
            lexical_score=round(item.lexical, 6),
            semantic_score=round(item.semantic, 6),
            hybrid_score=confidence,
            confidence=confidence,
            match_terms=item.terms,
            provenance={
                "scene_id": item.record.scene_id,
                "media_id": item.record.media_id,
                "source_version": item.record.source_version,
                "source_sha256": item.record.source_sha256,
                "candidate_id": item.record.annotation.candidate_id,
                "mandate_id": MANDATE_ID,
            },
        )

    def _receipt(self, *, request_digest: str, query: RetrievalQuery, state: RetrievalState, candidates: tuple[str, ...] = (), selected_scene_ids: tuple[str, ...] = (), validator_results: Mapping[str, str], recovery_path: str, error_code: str | None = None, error_detail: str | None = None) -> RetrievalReceipt:
        payload = {
            "request_digest": request_digest,
            "workspace_id": query.workspace_id,
            "state": state.value,
            "model_id": self.model.model_id,
            "candidates": candidates,
            "selected_scene_ids": selected_scene_ids,
            "error_code": error_code,
        }
        return RetrievalReceipt(
            receipt_id="RRET-" + _digest(payload)[:24],
            request_digest=request_digest,
            workspace_id=query.workspace_id,
            actor=self.actor,
            state=state,
            model_id=self.model.model_id,
            candidates=candidates,
            selected_scene_ids=selected_scene_ids,
            query=query.query,
            confidence_threshold=query.min_confidence,
            validator_results=validator_results,
            error_code=error_code,
            error_detail=error_detail,
            recovery_path=recovery_path,
        )

    @staticmethod
    def _tokens(text: str) -> set[str]:
        lowered = text.lower().replace("control-room", "control room")
        return {token for token in re.findall(r"[a-z0-9]+", lowered) if len(token) > 2}

    @staticmethod
    def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
        if len(left) != len(right):
            raise RetrievalError("Embedding dimension mismatch")
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return sum(a * b for a, b in zip(left, right)) / (left_norm * right_norm)


def _digest(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
