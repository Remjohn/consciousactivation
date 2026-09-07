from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Dict, Tuple

import pytest

from ca_runtime.pi_adapter import AuthorityLane
from cmf_pipeline.briefs import (
    ClaimType,
    FalsificationCondition,
    ResearchBriefAuthorityError,
    ResearchBriefBlockedError,
    ResearchBriefDraft,
    ResearchBriefService,
    ResearchBriefSourceSubstitutionError,
    ResearchBriefStaleError,
    ResearchClaimDraft,
    ResearchCitation,
)
from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository


@dataclass(frozen=True)
class Source:
    source_id: str
    workspace_id: str
    version: int
    content_sha256: str
    origin_url: str
    status: str = "ACTIVE"


class SourceCatalog:
    def __init__(self, sources: Tuple[Source, ...]) -> None:
        self.sources: Dict[str, Source] = {source.source_id: source for source in sources}

    def get_source_record(self, source_id: str, workspace_id: str | None = None) -> Source | None:
        source = self.sources.get(source_id)
        if source is None:
            return None
        if workspace_id is not None and source.workspace_id != workspace_id:
            return None
        return source


def _source(text: str, *, source_id: str = "cae:source:1", revision: int = 1) -> Source:
    return Source(
        source_id=source_id,
        workspace_id="ws-1",
        version=revision,
        content_sha256=hashlib.sha256(text.strip().encode("utf-8")).hexdigest(),
        origin_url="https://example.test/source/1",
    )


def _draft(source: Source, *, brief_id: str = "rb:q10", authority_tier: int = 2) -> ResearchBriefDraft:
    citation = ResearchCitation(
        citation_id="cit-1",
        source_id=source.source_id,
        source_revision=source.version,
        source_content_sha256=source.content_sha256,
        immutable_locator=source.origin_url,
    )
    claim = ResearchClaimDraft(
        claim_id="claim-1",
        claim_type=ClaimType.FACT,
        authority_tier=authority_tier,
        claim_text="A stable source-backed research claim is admissible.",
        citations=(citation,),
        falsification_condition=FalsificationCondition(
            condition="The claim is disconfirmed by the exact cited source revision.",
            evidence_to_check="Compare the cited source revision content and its pinned SHA-256 digest.",
        ),
    )
    second_citation = citation.model_copy(update={"citation_id": "cit-2"})
    second_claim = claim.model_copy(
        update={
            "claim_id": "claim-2",
            "claim_type": ClaimType.INFERENCE,
            "authority_tier": authority_tier,
            "claim_text": f"The cited evidence supports an authority tier {authority_tier} interpretation.",
            "citations": (second_citation,),
        }
    )
    return ResearchBriefDraft(
        brief_id=brief_id,
        workspace_id="ws-1",
        question_id="Q10",
        owner_id="research-owner",
        claims=(claim, second_claim),
    )


def _service(tmp_path: Path) -> tuple[ResearchBriefService, SourceCatalog, Source]:
    repository = PipelineRepository(tmp_path / "pipeline.sqlite3")
    repository.initialize()
    source = _source("Stable exact source revision content for Q10.")
    catalog = SourceCatalog((source,))
    return ResearchBriefService(repository, source_resolver=catalog), catalog, source


def test_multi_claim_admission_persists_structured_brief_and_receipt(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    result = service.admit(
        _draft(source),
        actor_id="operator-1",
        idempotency_key="rb:q10:r1",
        expected_revision=0,
    )

    assert result["brief"].revision == 1
    assert all(claim.brief_revision == 1 for claim in result["brief"].claims)
    assert result["receipt"].brief_revision == 1
    assert result["receipt"].receipt_sha256
    assert len(result["source_pins"]) == 2

    consumed = service.consume(brief_id="rb:q10", revision=1)
    assert consumed.brief_id == "rb:q10"
    assert consumed.claims[0].citations[0].source_id == source.source_id
    assert consumed.claims[0].citations[0].source_content_sha256 == source.content_sha256


def test_revision_preserves_prior_immutable_revision_and_rejects_stale_consumer(tmp_path: Path) -> None:
    service, catalog, source = _service(tmp_path)
    first = service.admit(
        _draft(source),
        actor_id="operator-1",
        idempotency_key="rb:q10:r1",
        expected_revision=0,
    )
    second_source = _source("Stable exact source revision content for Q10 v2.", revision=2)
    catalog.sources[second_source.source_id] = second_source
    second_draft = _draft(second_source)
    second_draft = second_draft.model_copy(update={"brief_id": "rb:q10"})
    service.admit(
        second_draft,
        actor_id="operator-1",
        idempotency_key="rb:q10:r2",
        expected_revision=1,
    )

    old = service.repository.get_object("rb:q10", revision=1)
    current = service.repository.get_object("rb:q10")
    assert old["revision"] == 1
    assert old["current"] is False
    assert current["revision"] == 2
    assert current["current"] is True
    assert old["payload"]["claims"][0]["brief_revision"] == 1
    assert current["payload"]["claims"][0]["brief_revision"] == 2

    with pytest.raises(ResearchBriefStaleError):
        service.consume(brief_id="rb:q10", revision=1)

    assert first["brief"].revision == 1


def test_missing_citation_is_blocked_before_persistence(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    draft = _draft(source)
    broken_claim = draft.claims[0].model_copy(update={"citations": ()})
    broken = draft.model_copy(update={"claims": (broken_claim, draft.claims[1])})

    # Pydantic catches the malformed claim before it can cross the runtime boundary.
    with pytest.raises(ValueError):
        service.admit(broken, actor_id="operator-1", idempotency_key="broken-cit", expected_revision=0)
    assert not service.repository.has_object("rb:q10")


def test_false_proof_clickable_citation_without_digest_or_immutable_locator_fails_closed(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    citation = ResearchCitation.model_construct(
        citation_id="cit-false-proof",
        source_id=source.source_id,
        source_revision=source.version,
        source_content_sha256=None,
        immutable_locator=None,
    )
    claim = ResearchClaimDraft.model_construct(
        claim_id="claim-false-proof",
        claim_type=ClaimType.FACT,
        authority_tier=2,
        claim_text="This polished claim is missing a verifiable source anchor.",
        citations=(citation,),
        falsification_condition=FalsificationCondition(
            condition="The claim is disconfirmed by the exact cited source revision.",
            evidence_to_check="Compare the cited source revision content and its pinned SHA-256 digest.",
        ),
    )
    draft = _draft(source).model_copy(update={"claims": (claim,)})

    with pytest.raises(ResearchBriefBlockedError) as exc:
        service.admit(draft, actor_id="operator-1", idempotency_key="false-proof", expected_revision=0)
    assert "MISSING_SOURCE_ANCHOR:cit-false-proof" in exc.value.reason_codes
    assert not service.repository.has_object("rb:q10")


def test_bad_source_digest_is_rejected_and_operator_inspection_exposes_block_reason(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    citation = ResearchCitation(
        citation_id="cit-bad-digest",
        source_id=source.source_id,
        source_revision=source.version,
        source_content_sha256="0" * 64,
        immutable_locator=source.origin_url,
    )
    claim = _draft(source).claims[0].model_copy(update={"citations": (citation,)})
    draft = _draft(source).model_copy(update={"claims": (claim,)})

    with pytest.raises(ResearchBriefBlockedError) as exc:
        service.admit(draft, actor_id="operator-1", idempotency_key="bad-digest", expected_revision=0)
    assert "SOURCE_DIGEST_MISMATCH:cae:source:1" in exc.value.reason_codes

    # Persisted operator inspection of the blocked reason is available without mutating the artifact.
    inspection = service.inspect(brief_id="rb:q10")
    assert inspection.admission_state == "NOT_FOUND"
    assert "BRIEF_NOT_FOUND" in inspection.block_reasons


def test_source_substitution_is_fail_closed_at_consumption_boundary(tmp_path: Path) -> None:
    service, catalog, source = _service(tmp_path)
    service.admit(
        _draft(source),
        actor_id="operator-1",
        idempotency_key="rb:q10:r1",
        expected_revision=0,
    )
    catalog.sources[source.source_id] = Source(
        source_id=source.source_id,
        workspace_id=source.workspace_id,
        version=source.version,
        content_sha256=hashlib.sha256(b"A substituted source body with a different digest.").hexdigest(),
        origin_url=source.origin_url,
    )

    with pytest.raises(ResearchBriefBlockedError) as exc:
        service.consume(brief_id="rb:q10", revision=1)
    assert "SOURCE_DIGEST_MISMATCH:cae:source:1" in exc.value.reason_codes
    assert not any(reason.startswith("SOURCE_NOT_FOUND") for reason in exc.value.reason_codes)


def test_invalid_authority_lane_is_rejected_without_state_change(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    with pytest.raises(ResearchBriefAuthorityError):
        service.admit(
            _draft(source),
            actor_id="analyst-1",
            idempotency_key="wrong-lane",
            expected_revision=0,
            authority_lane=AuthorityLane.ANALYST,
        )
    assert not service.repository.has_object("rb:q10")


def test_stale_expected_revision_is_rejected_before_new_revision_is_created(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    service.admit(_draft(source), actor_id="operator-1", idempotency_key="r1", expected_revision=0)
    with pytest.raises(ResearchBriefStaleError):
        service.admit(_draft(source), actor_id="operator-1", idempotency_key="stale-r2", expected_revision=0)
    current = service.repository.get_object("rb:q10")
    assert current["revision"] == 1


def test_malformed_claim_and_invalid_authority_tier_fail_at_schema_boundary(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    with pytest.raises(ValueError):
        ResearchCitation(
            citation_id="bad",
            source_id=source.source_id,
            source_revision=source.version,
            source_content_sha256="not-a-sha",
        )
    with pytest.raises(ValueError):
        _draft(source, authority_tier=5)


def test_inspection_of_current_revision_is_ready_and_contains_source_lineage(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    service.admit(_draft(source), actor_id="operator-1", idempotency_key="inspect-r1", expected_revision=0)
    inspection = service.inspect(brief_id="rb:q10")

    assert inspection.admission_state == "READY"
    assert inspection.current_revision == 1
    assert inspection.inspected_revision == 1
    assert inspection.block_reasons == ()
    assert inspection.claim_count == 2
    assert all(pin["source_id"] == source.source_id for pin in inspection.source_pins)


def test_locator_only_citation_is_admissible_when_source_identity_and_revision_are_resolved(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    citation = ResearchCitation(
        citation_id="cit-locator-only",
        source_id=source.source_id,
        source_revision=source.version,
        immutable_locator=source.origin_url,
    )
    claim = _draft(source).claims[0].model_copy(update={"citations": (citation,)})
    draft = _draft(source).model_copy(update={"claims": (claim,)})

    result = service.admit(draft, actor_id="operator-1", idempotency_key="locator-only", expected_revision=0)
    assert result["brief"].claims[0].citations[0].immutable_locator == source.origin_url
    assert result["brief"].claims[0].citations[0].source_content_sha256 is None


def test_missing_falsification_condition_is_blocked_fail_closed(tmp_path: Path) -> None:
    service, _, source = _service(tmp_path)
    claim = _draft(source).claims[0].model_copy(
        update={
            "falsification_condition": FalsificationCondition.model_construct(
                condition="",
                evidence_to_check="",
            )
        }
    )
    draft = _draft(source).model_copy(update={"claims": (claim,)})

    with pytest.raises(ResearchBriefBlockedError) as exc:
        service.admit(draft, actor_id="operator-1", idempotency_key="missing-falsification", expected_revision=0)
    assert "MISSING_FALSIFICATION_CONDITION:claim-1" in exc.value.reason_codes
    assert not service.repository.has_object("rb:q10")
