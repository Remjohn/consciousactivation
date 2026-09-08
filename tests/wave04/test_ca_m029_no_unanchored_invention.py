"""CA-M029 / FR-029 — no-unanchored-invention acceptance suite.

The tests exercise the real interview evidence persistence/admission boundary for
positive/negative cases and also cover the semantic-unit false-proof countercase.
"""

from __future__ import annotations

import hashlib
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# The archive does not include third-party runtime wheels.  Keep collection
# self-contained with a minimal psycopg stub, and load only the ca_runtime modules
# needed by this mandate rather than executing the package's broad public __init__.
if "psycopg" not in sys.modules:
    psycopg_stub = types.ModuleType("psycopg")
    psycopg_stub.__path__ = []
    psycopg_stub.Connection = object
    psycopg_stub.Cursor = object
    types_pkg = types.ModuleType("psycopg.types")
    json_pkg = types.ModuleType("psycopg.types.json")
    json_pkg.Jsonb = lambda value: value
    types_pkg.json = json_pkg
    sys.modules["psycopg"] = psycopg_stub
    sys.modules["psycopg.types"] = types_pkg
    sys.modules["psycopg.types.json"] = json_pkg

ca_runtime_pkg = types.ModuleType("ca_runtime")
ca_runtime_pkg.__path__ = [str(ROOT / "packages/ca_runtime/src/ca_runtime")]
sys.modules.setdefault("ca_runtime", ca_runtime_pkg)

import pytest

for p in reversed(
    [
        ROOT / "packages/ca_contracts/src",
        ROOT / "packages/ca_runtime/src",
        ROOT / "services/interview/src",
    ]
):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)

from ca_runtime.no_unanchored_invention import (
    CA_M029,
    FR_029,
    ConnectivePolicy,
    EvidenceRef,
    GroundingClass,
    NoUnanchoredInventionError,
    SentenceClaim,
    UnanchoredClaimError,
    VerbatimAnchor,
    VerbatimMismatchError,
    audit_sentences,
    extract_sentences,
    flag_unanchored_sentences,
    purge_unanchored_sentences,
    require_admitted_composition,
    verify_evidence_reference,
)
from conscious_activations_interview_expression.repository import InterviewRepository


def _stored_verbatim(repo: InterviewRepository, *, evidence_id: str = "ev-1", quote: str = "Our database crashed at 3 AM.") -> dict:
    payload = {
        "evidence_id": evidence_id,
        "version": "1.0.0",
        "quote_text": quote,
        "quote_sha256": hashlib.sha256(quote.encode("utf-8")).hexdigest(),
        "validation": {"status": "PASS", "exact_character_slice": True},
        "admission_receipt": {"validation_status": "PASS", "command": "admit_verbatim_evidence"},
        "lifecycle_state": "VALIDATED",
        "epistemic_state": "OBSERVED",
        "source_package_ref": {"object_id": "source-1", "version": "1.0.0", "sha256": "1" * 64},
    }
    return repo.store_object(
        "verbatim_evidence",
        payload,
        object_id=evidence_id,
        idempotency_key=f"store:{evidence_id}",
        lifecycle_state="VALIDATED",
    )["object"]


def _anchor(stored: dict, quote: str | None = None) -> VerbatimAnchor:
    obj_ref = EvidenceRef(
        object_id=stored["object_id"],
        version=stored["version"],
        sha256=stored["sha256"],
    )
    return VerbatimAnchor(obj_ref, quote or stored["payload"]["quote_text"])


def test_extracts_every_narrative_sentence_independently():
    assert extract_sentences('First fact. Second fact! Is this supported?') == (
        "First fact.",
        "Second fact!",
        "Is this supported?",
    )


def test_positive_path_requires_exact_verbatim_anchor_and_admitted_evidence(tmp_path):
    repo = InterviewRepository(tmp_path / "m029.sqlite3")
    stored = _stored_verbatim(repo)
    anchor = _anchor(stored)
    claim = SentenceClaim(
        sentence='The guest said, "Our database crashed at 3 AM."',
        grounding=GroundingClass.EVIDENCE_BACKED,
        evidence_refs=(anchor.evidence_ref,),
        verbatim_anchors=(anchor,),
        claim_id="claim-1",
    )

    report = audit_sentences([claim], repo)
    assert report.admitted is True
    assert report.mandate_id == CA_M029
    assert report.invariant_id == "INV-NO-INVENT-001"
    assert report.sentences[0].evidence_verifications[0].quote_sha256 == stored["payload"]["quote_sha256"]

    admission = require_admitted_composition([claim], repo)
    assert admission.text == claim.sentence
    assert admission.audit.validation_digest


def test_real_content_addressed_lookup_rejects_stale_revision(tmp_path):
    repo = InterviewRepository(tmp_path / "m029-stale.sqlite3")
    stored = _stored_verbatim(repo)
    stale_ref = EvidenceRef(stored["object_id"], stored["version"], "2" * 64)
    with pytest.raises(Exception) as exc_info:
        verify_evidence_reference(stale_ref, repo)
    assert "could not be resolved" in str(exc_info.value) or "revision/digest" in str(exc_info.value)


def test_mutated_quote_fails_even_when_object_metadata_is_present(tmp_path):
    repo = InterviewRepository(tmp_path / "m029-quote.sqlite3")
    stored = _stored_verbatim(repo, quote="The database crashed at 3 AM.")
    anchor = _anchor(stored, quote="The database crashed at 4 AM.")
    claim = SentenceClaim(
        sentence='The guest said, "The database crashed at 4 AM."',
        evidence_refs=(anchor.evidence_ref,),
        verbatim_anchors=(anchor,),
    )
    report = audit_sentences([claim], repo)
    assert report.admitted is False
    assert report.sentences[0].reasons[0] == "CA_M029_VERBATIM_MISMATCH"


def test_unanchored_factual_sentence_is_fatal_even_when_other_sentences_are_grounded(tmp_path):
    repo = InterviewRepository(tmp_path / "m029-centroid.sqlite3")
    stored = _stored_verbatim(repo)
    anchored = SentenceClaim(
        sentence='The guest said, "Our database crashed at 3 AM."',
        evidence_refs=(EvidenceRef(stored["object_id"], stored["version"], stored["sha256"]),),
        verbatim_anchors=(_anchor(stored),),
        claim_id="grounded",
    )
    invented = SentenceClaim(
        sentence="The outage permanently changed the company's architecture.",
        grounding=GroundingClass.EVIDENCE_BACKED,
        claim_id="invented",
    )

    report = audit_sentences([anchored, invented], repo)
    assert report.admitted is False
    assert report.sentences[0].admitted is True
    assert report.sentences[1].admitted is False
    assert report.rejected_sentences == (invented.sentence,)

    with pytest.raises(NoUnanchoredInventionError):
        require_admitted_composition([anchored, invented], repo)


def test_evidence_reference_alone_cannot_borrow_a_whole_paragraph(tmp_path):
    repo = InterviewRepository(tmp_path / "m029-whole-paragraph.sqlite3")
    stored = _stored_verbatim(repo)
    claim = SentenceClaim(
        sentence='The database crashed at 3 AM, and the team rebuilt the architecture the next day.',
        evidence_refs=(EvidenceRef(stored["object_id"], stored["version"], stored["sha256"]),),
        # No exact sentence-level anchor: intentionally a false proof.
        verbatim_anchors=(),
    )
    report = audit_sentences([claim], repo)
    assert report.admitted is False
    assert "sentence-level exact verbatim anchor" in report.sentences[0].reasons[1]


def test_connective_transformation_requires_explicit_versioned_policy(tmp_path):
    repo = InterviewRepository(tmp_path / "m029-connective.sqlite3")
    claim = SentenceClaim(
        sentence="Then the scene moves into the next beat.",
        grounding=GroundingClass.CONNECTIVE,
        connective_operation="SCENE_TRANSITION",
    )

    denied = audit_sentences([claim], repo)
    assert denied.admitted is False

    policy = ConnectivePolicy.strict_allowlist(
        {"SCENE_TRANSITION"}, policy_id="script-program-connectives", version="2.1.0"
    )
    allowed = audit_sentences([claim], repo, connective_policy=policy)
    assert allowed.admitted is True
    assert allowed.sentences[0].reasons == ("AUTHORIZED_CONNECTIVE_TRANSFORMATION",)


def test_purge_mode_removes_only_failed_sentences_and_keeps_audit(tmp_path):
    repo = InterviewRepository(tmp_path / "m029-purge.sqlite3")
    stored = _stored_verbatim(repo)
    good = SentenceClaim(
        sentence='The guest said, "Our database crashed at 3 AM."',
        evidence_refs=(EvidenceRef(stored["object_id"], stored["version"], stored["sha256"]),),
        verbatim_anchors=(_anchor(stored),),
    )
    bad = SentenceClaim(sentence="The outage was caused by an unrecorded vendor failure.")

    result = purge_unanchored_sentences([good, bad], repo)
    assert result.text == good.sentence
    assert result.audit.admitted is False
    assert result.audit.purged_sentences == (bad.sentence,)


def test_flag_mode_preserves_all_candidate_sentences_for_review(tmp_path):
    repo = InterviewRepository(tmp_path / "m029-flag.sqlite3")
    bad = SentenceClaim(sentence="A new product launch doubled revenue.")
    report = flag_unanchored_sentences([bad], repo)
    assert report.admitted is False
    assert report.rejected_sentences == (bad.sentence,)
    assert report.sentences[0].action.value == "FLAG"


def test_forged_anchored_boolean_is_not_a_grounding_authority(tmp_path):
    repo = InterviewRepository(tmp_path / "m029-boolean.sqlite3")
    claim = {
        "sentence": "The system was redesigned after the outage.",
        "grounding": "EVIDENCE_BACKED",
        "metadata": {"anchored": True, "confidence": 1.0},
    }
    report = audit_sentences([claim], repo)
    assert report.admitted is False
    assert "CA_M029_UNANCHORED_CLAIM" in report.sentences[0].reasons


def test_mapping_input_accepts_real_repository_object_ref_and_top_level_quote(tmp_path):
    repo = InterviewRepository(tmp_path / "m029-mapping.sqlite3")
    stored = _stored_verbatim(repo)
    claim = {
        "claim_id": "claim-mapping",
        "sentence": 'Witness: "Our database crashed at 3 AM."',
        "grounding": "EVIDENCE_BACKED",
        "evidence_refs": [
            {"object_id": stored["object_id"], "version": stored["version"], "sha256": stored["sha256"]}
        ],
        "verbatim_quote": stored["payload"]["quote_text"],
    }
    report = audit_sentences([claim], repo)
    assert report.admitted is True
    assert report.to_dict()["sentences"][0]["claim"]["claim_id"] == "claim-mapping"


def test_constants_match_mandate_contract():
    assert CA_M029 == "CA-M029"
    assert FR_029 == "FR-029"
