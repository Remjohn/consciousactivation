from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane

from ..domain.errors import PipelineNotFound
from ..workflow.infrastructure.repository import PipelineRepository
from .models import (
    ResearchBrief,
    ResearchBriefAuthorityError,
    ResearchBriefBlockedError,
    ResearchBriefDraft,
    ResearchBriefInspection,
    ResearchBriefNotFoundError,
    ResearchBriefReceipt,
    ResearchBriefStaleError,
    ResearchCitation,
    ResearchClaim,
)


class ResearchSourceRecordLike(Protocol):
    source_id: str
    workspace_id: str
    version: int
    content_sha256: str
    origin_url: str
    status: str


class ResearchSourceResolver(Protocol):
    def get_source_record(
        self,
        source_id: str,
        workspace_id: str | None = None,
    ) -> ResearchSourceRecordLike | None:
        ...


@dataclass(frozen=True, slots=True)
class _ValidationOutcome:
    reason_codes: tuple[str, ...]
    source_pins: tuple[dict[str, object], ...]


class ResearchBriefService:
    """Canonical Pipeline boundary for admission, inspection, and consumption of research briefs."""

    OBJECT_TYPE = "research_brief"
    RECEIPT_OBJECT_TYPE = "research_brief_admission_receipt"
    SEMANTIC_VERSION = "1.0.0"
    REQUIRED_LANE = AuthorityLane.COMPOSER

    def __init__(
        self,
        repository: PipelineRepository,
        *,
        source_resolver: ResearchSourceResolver | None = None,
    ) -> None:
        self.repository = repository
        self.source_resolver = source_resolver

    def admit(
        self,
        draft: ResearchBriefDraft | Mapping[str, Any],
        *,
        actor_id: str,
        idempotency_key: str,
        expected_revision: int,
        authority_lane: AuthorityLane = REQUIRED_LANE,
    ) -> dict[str, Any]:
        """Validate and seal one immutable brief revision through PipelineRepository."""
        self._require_lane(authority_lane)
        if expected_revision < 0:
            raise ResearchBriefStaleError("expected_revision must be >= 0")
        if not actor_id.strip():
            raise ValueError("actor_id is required")

        draft_model = draft if isinstance(draft, ResearchBriefDraft) else ResearchBriefDraft.model_validate(draft)
        current_revision = self._current_revision(draft_model.brief_id)
        if current_revision != expected_revision:
            raise ResearchBriefStaleError(
                f"stale Research Brief admission for {draft_model.brief_id}: "
                f"expected repository revision {expected_revision}, observed {current_revision}"
            )

        target_revision = expected_revision + 1
        draft_reasons = self._validate_draft_shape(draft_model)
        if draft_reasons:
            raise ResearchBriefBlockedError(
                "Research Brief admission blocked: " + ", ".join(draft_reasons),
                reason_codes=draft_reasons,
            )
        try:
            brief = self._bind_revision(draft_model, target_revision)
        except Exception as exc:
            raise ResearchBriefBlockedError(
                "Research Brief admission blocked by schema validation",
                reason_codes=(f"SCHEMA_ERROR:{type(exc).__name__}",),
            ) from exc
        validation = self._validate_brief(brief)
        if validation.reason_codes:
            raise ResearchBriefBlockedError(
                "Research Brief admission blocked: " + ", ".join(validation.reason_codes),
                reason_codes=validation.reason_codes,
            )

        timestamp = utc_now_rfc3339()
        stored = self.repository.store_object(
            self.OBJECT_TYPE,
            brief.model_dump(mode="json"),
            idempotency_key=idempotency_key,
            object_id=brief.brief_id,
            semantic_version=self.SEMANTIC_VERSION,
            lifecycle_state="SEALED",
            authority_state="candidate_not_current",
            expected_revision=expected_revision,
            now=timestamp,
        )
        stored_brief = ResearchBrief.model_validate(stored["object"]["payload"])
        receipt = self._build_receipt(
            brief=stored_brief,
            actor_id=actor_id,
            input_payload=draft_model.model_dump(mode="json"),
            output_payload=stored["object"],
            idempotent_replay=bool(stored.get("idempotent_replay", False)),
        )
        receipt_stored = self.repository.store_object(
            self.RECEIPT_OBJECT_TYPE,
            receipt.model_dump(mode="json"),
            idempotency_key=f"{idempotency_key}:receipt",
            object_id=f"{brief.brief_id}:receipt:{stored_brief.revision}",
            semantic_version=self.SEMANTIC_VERSION,
            lifecycle_state="EMITTED",
            authority_state="candidate_not_current",
            expected_revision=0,
            now=timestamp,
        )
        self.repository.add_edge(
            f"{brief.brief_id}:receipt:{stored_brief.revision}",
            brief.brief_id,
            "receipt_for",
            evidence={
                "brief_revision": stored_brief.revision,
                "brief_canonical_sha256": stored["object"]["canonical_sha256"],
                "receipt_sha256": receipt.receipt_sha256,
            },
            now=timestamp,
        )
        return {
            "brief": stored_brief,
            "stored_object": stored["object"],
            "receipt": ResearchBriefReceipt.model_validate(receipt_stored["object"]["payload"]),
            "source_pins": validation.source_pins,
            "idempotent_replay": bool(stored.get("idempotent_replay", False)),
        }

    def consume(
        self,
        *,
        brief_id: str,
        revision: int,
    ) -> ResearchBrief:
        """Read and revalidate a current sealed brief as typed structured input, never as prose."""
        if revision < 1:
            raise ResearchBriefStaleError("revision must be >= 1")
        try:
            stored = self.repository.get_object(brief_id, revision=revision)
            current = self.repository.get_object(brief_id)
        except PipelineNotFound as exc:
            raise ResearchBriefNotFoundError(str(exc)) from exc

        if not current["current"] or int(current["revision"]) != revision:
            raise ResearchBriefStaleError(
                f"Research Brief {brief_id} revision {revision} is stale; "
                f"current revision is {current['revision']}"
            )
        if stored["object_type"] != self.OBJECT_TYPE or stored["lifecycle_state"] != "SEALED":
            raise ResearchBriefBlockedError(
                f"Research Brief {brief_id} revision {revision} is not a sealed research_brief object",
                reason_codes=("LIFECYCLE_ERROR",),
            )
        recalculated = canonical_sha256(stored["payload"])
        if recalculated != stored["canonical_sha256"]:
            raise ResearchBriefBlockedError(
                f"Research Brief {brief_id} revision {revision} failed canonical digest verification",
                reason_codes=("PROVENANCE_ERROR",),
            )

        brief = ResearchBrief.model_validate(stored["payload"])
        validation = self._validate_brief(brief)
        if validation.reason_codes:
            raise ResearchBriefBlockedError(
                "Research Brief consumption blocked: " + ", ".join(validation.reason_codes),
                reason_codes=validation.reason_codes,
            )
        return brief

    def inspect(self, *, brief_id: str, revision: int | None = None) -> ResearchBriefInspection:
        """Expose operator-facing provenance and fail-closed block reasons without mutating state."""
        try:
            current = self.repository.get_object(brief_id)
        except PipelineNotFound:
            return ResearchBriefInspection(
                brief_id=brief_id,
                current_revision=None,
                inspected_revision=revision,
                admission_state="NOT_FOUND",
                block_reasons=("BRIEF_NOT_FOUND",),
                claim_count=0,
                source_pins=(),
            )

        inspected_revision = revision or int(current["revision"])
        try:
            inspected = self.repository.get_object(brief_id, revision=inspected_revision)
        except PipelineNotFound:
            return ResearchBriefInspection(
                brief_id=brief_id,
                current_revision=int(current["revision"]),
                inspected_revision=inspected_revision,
                admission_state="BLOCKED",
                block_reasons=("REVISION_NOT_FOUND",),
                claim_count=0,
                source_pins=(),
            )

        try:
            brief = ResearchBrief.model_validate(inspected["payload"])
            outcome = self._validate_brief(brief)
            reasons = list(outcome.reason_codes)
            if inspected_revision != int(current["revision"]):
                reasons.append("STALE_BRIEF")
            state = "READY" if not reasons else "BLOCKED"
            return ResearchBriefInspection(
                brief_id=brief_id,
                current_revision=int(current["revision"]),
                inspected_revision=inspected_revision,
                admission_state=state,
                block_reasons=tuple(dict.fromkeys(reasons)),
                claim_count=len(brief.claims),
                source_pins=outcome.source_pins,
            )
        except Exception as exc:
            return ResearchBriefInspection(
                brief_id=brief_id,
                current_revision=int(current["revision"]),
                inspected_revision=inspected_revision,
                admission_state="BLOCKED",
                block_reasons=(f"SCHEMA_ERROR:{type(exc).__name__}",),
                claim_count=0,
                source_pins=(),
            )

    @staticmethod
    def _validate_draft_shape(draft: ResearchBriefDraft) -> tuple[str, ...]:
        reasons: list[str] = []
        if not draft.claims:
            reasons.append("MISSING_CLAIMS")
        for claim in draft.claims:
            if not isinstance(claim.claim_id, str) or not claim.claim_id.strip():
                reasons.append("MALFORMED_CLAIM_ID")
            if not isinstance(getattr(claim, "claim_text", None), str) or len(claim.claim_text.strip()) < 10:
                reasons.append(f"MALFORMED_CLAIM_TEXT:{getattr(claim, 'claim_id', '<unknown>')}")
            tier = getattr(claim, "authority_tier", None)
            if not isinstance(tier, int) or isinstance(tier, bool) or not 1 <= tier <= 4:
                reasons.append(f"INVALID_AUTHORITY_TIER:{getattr(claim, 'claim_id', '<unknown>')}")
            citations = getattr(claim, "citations", ())
            if not citations:
                reasons.append(f"MISSING_CITATION:{getattr(claim, 'claim_id', '<unknown>')}")
            for citation in citations:
                if not getattr(citation, "source_content_sha256", None) and not getattr(citation, "immutable_locator", None):
                    reasons.append(f"MISSING_SOURCE_ANCHOR:{getattr(citation, 'citation_id', '<unknown>')}")
            falsification = getattr(claim, "falsification_condition", None)
            if falsification is None or not str(getattr(falsification, "condition", "")).strip() or not str(getattr(falsification, "evidence_to_check", "")).strip():
                reasons.append(f"MISSING_FALSIFICATION_CONDITION:{getattr(claim, 'claim_id', '<unknown>')}")
        return tuple(dict.fromkeys(reasons))

    def _bind_revision(self, draft: ResearchBriefDraft, revision: int) -> ResearchBrief:
        return ResearchBrief(
            brief_id=draft.brief_id,
            workspace_id=draft.workspace_id,
            question_id=draft.question_id,
            owner_id=draft.owner_id,
            revision=revision,
            claims=tuple(
                ResearchClaim(**claim.model_dump(mode="json"), brief_revision=revision)
                for claim in draft.claims
            ),
        )

    def _validate_brief(self, brief: ResearchBrief) -> _ValidationOutcome:
        reasons: list[str] = []
        source_pins: list[dict[str, object]] = []
        if not brief.claims:
            reasons.append("MISSING_CLAIMS")
        if self.source_resolver is None:
            reasons.append("PROVENANCE_RESOLVER_UNAVAILABLE")
            return _ValidationOutcome(tuple(dict.fromkeys(reasons)), tuple())

        for claim in brief.claims:
            if not claim.citations:
                reasons.append(f"MISSING_CITATION:{claim.claim_id}")
                continue
            if not claim.falsification_condition.condition.strip() or not claim.falsification_condition.evidence_to_check.strip():
                reasons.append(f"MISSING_FALSIFICATION_CONDITION:{claim.claim_id}")
            for citation in claim.citations:
                if not citation.source_content_sha256 and not citation.immutable_locator:
                    reasons.append(f"MISSING_SOURCE_ANCHOR:{citation.citation_id}")
                    continue
                try:
                    source = self.source_resolver.get_source_record(
                        citation.source_id,
                        brief.workspace_id,
                    )
                except Exception as exc:
                    reasons.append(f"SOURCE_RESOLUTION_ERROR:{citation.source_id}:{type(exc).__name__}")
                    continue
                if source is None:
                    reasons.append(f"SOURCE_NOT_FOUND:{citation.source_id}")
                    continue
                if str(source.workspace_id) != brief.workspace_id:
                    reasons.append(f"CROSS_WORKSPACE_SOURCE:{citation.source_id}")
                if int(source.version) != citation.source_revision:
                    reasons.append(
                        f"SOURCE_REVISION_MISMATCH:{citation.source_id}:expected={citation.source_revision}:observed={source.version}"
                    )
                if str(getattr(source, "status", "")).upper() in {"QUARANTINED", "REJECTED", "DELETED"}:
                    reasons.append(f"SOURCE_NOT_ADMISSIBLE:{citation.source_id}:{source.status}")
                if citation.source_content_sha256 and source.content_sha256.lower() != citation.source_content_sha256:
                    reasons.append(f"SOURCE_DIGEST_MISMATCH:{citation.source_id}")
                if citation.immutable_locator and source.origin_url != citation.immutable_locator:
                    reasons.append(f"SOURCE_LOCATOR_MISMATCH:{citation.source_id}")
                source_pins.append(
                    {
                        "citation_id": citation.citation_id,
                        "source_id": citation.source_id,
                        "source_revision": citation.source_revision,
                        "source_content_sha256": citation.source_content_sha256,
                        "immutable_locator": citation.immutable_locator,
                    }
                )
        return _ValidationOutcome(tuple(dict.fromkeys(reasons)), tuple(source_pins))

    def _current_revision(self, brief_id: str) -> int:
        try:
            return int(self.repository.get_object(brief_id)["revision"])
        except PipelineNotFound:
            return 0

    @classmethod
    def _require_lane(cls, lane: AuthorityLane) -> None:
        if lane != cls.REQUIRED_LANE:
            raise ResearchBriefAuthorityError(
                f"Research Brief admission requires {cls.REQUIRED_LANE.value} authority lane; observed {lane.value}"
            )

    @staticmethod
    def _build_receipt(
        *,
        brief: ResearchBrief,
        actor_id: str,
        input_payload: Mapping[str, Any],
        output_payload: Mapping[str, Any],
        idempotent_replay: bool,
    ) -> ResearchBriefReceipt:
        output_digest = canonical_sha256(output_payload)
        input_digest = canonical_sha256(input_payload)
        receipt_core = {
            "receipt_type": "cae_execution_receipt",
            "receipt_id": f"rcpt:research-brief:{brief.brief_id}:{brief.revision}",
            "operation_id": "cae.research_brief.admit@1.0.0",
            "actor_id": actor_id,
            "authority_lane": AuthorityLane.COMPOSER.value,
            "workspace_id": brief.workspace_id,
            "aggregate_id": brief.brief_id,
            "brief_revision": brief.revision,
            "brief_canonical_sha256": canonical_sha256(brief.model_dump(mode="json")),
            "input_snapshot_sha256": input_digest,
            "output_snapshot_sha256": output_digest,
            "idempotent_replay": idempotent_replay,
        }
        return ResearchBriefReceipt(
            **receipt_core,
            receipt_sha256=canonical_sha256(receipt_core),
        )


__all__ = ["ResearchBriefService", "ResearchSourceResolver", "ResearchSourceRecordLike"]
