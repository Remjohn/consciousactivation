"""
CA-M008 / FR-008 / FR-PORT-001 executable evidence.

Coverage (positive paths):
- Valid draft creation with correct content digest
- All required fields are captured in snapshot
- Deliverable identity, quantity, aspect ratio, format requirement fields
- DRAFT → SEALED lifecycle transition
- Sealed snapshot digest is stable and unchanged by lifecycle transition
- Active revision pointer in registry is updated after registration
- Multiple sequential revisions can be registered without error
- ``require_admitted_portfolio`` passes for a valid SEALED snapshot
- ``to_dict`` exposes the complete contract and schema version
- Notes are excluded from the content digest
- Registry retrieves by exact revision_id

Coverage (negative / fail-closed paths):
- Empty deliverables list raises InvalidDeliverableError
- Duplicate deliverable_ids within a portfolio raises InvalidDeliverableError
- Zero or negative quantity raises InvalidDeliverableError
- Invalid aspect ratio fields raise InvalidDeliverableError
- Invalid format_id raises InvalidDeliverableError
- Admitting a DRAFT (not SEALED) raises PortfolioAdmissionError
- Admitting a None raises PortfolioAdmissionError
- Cross-workspace portfolio admission raises PortfolioAdmissionError
- Cross-campaign portfolio admission raises PortfolioAdmissionError
- Re-sealing a SEALED snapshot raises PortfolioMutationError
- Registering the same revision_id twice raises DuplicatePortfolioRevisionError
- Registering a DRAFT (not sealed) raises PortfolioAdmissionError
- Digest mismatch on tampered snapshot raises PortfolioDigestMismatchError
- Digest mismatch detected inside require_admitted_portfolio
- Notes change does NOT change the revision digest (notes are non-canonical)
- Deliverable field change DOES change the revision digest
"""

from __future__ import annotations

import dataclasses

import pytest

from ca_runtime.frozen_portfolio import (
    AspectRatioSpec,
    DeliverableEntry,
    DuplicatePortfolioRevisionError,
    FormatRequirement,
    FrozenPortfolioRegistry,
    FrozenPortfolioSnapshot,
    InvalidDeliverableError,
    INVARIANT_ID,
    PORTFOLIO_SCHEMA_VERSION,
    PortfolioAdmissionError,
    PortfolioDigestMismatchError,
    PortfolioLifecycleState,
    PortfolioMutationError,
    require_admitted_portfolio,
)


# ---------------------------------------------------------------------------
# Test constants
# ---------------------------------------------------------------------------

WS = "ws-ca-m008"
CAM = "campaign-ca-m008"
PORT = "portfolio-ca-m008"
REV1 = "rev-001"
REV2 = "rev-002"


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def make_aspect(label: str = "16:9", w: int = 1920, h: int = 1080) -> AspectRatioSpec:
    return AspectRatioSpec(ratio_label=label, width_px=w, height_px=h)


def make_format(fmt_id: str = "short-form-video") -> FormatRequirement:
    return FormatRequirement(format_id=fmt_id, codec_or_mime="video/mp4")


def make_deliverable(
    did: str = "d-001",
    label: str = "Hero Video",
    qty: int = 3,
) -> DeliverableEntry:
    return DeliverableEntry(
        deliverable_id=did,
        label=label,
        quantity=qty,
        aspect_ratio=make_aspect(),
        format_requirement=make_format(),
    )


def make_draft(
    workspace_id: str = WS,
    campaign_id: str = CAM,
    portfolio_id: str = PORT,
    revision_id: str = REV1,
    deliverables: list[DeliverableEntry] | None = None,
    notes: str | None = None,
) -> FrozenPortfolioSnapshot:
    if deliverables is None:
        deliverables = [make_deliverable()]
    return FrozenPortfolioSnapshot.create_draft(
        portfolio_id=portfolio_id,
        revision_id=revision_id,
        workspace_id=workspace_id,
        campaign_id=campaign_id,
        narrative_context="Q4 launch — guest: Jane Doe — tension: autonomy vs accountability",
        deliverables=deliverables,
        notes=notes,
    )


def make_sealed(
    workspace_id: str = WS,
    campaign_id: str = CAM,
    portfolio_id: str = PORT,
    revision_id: str = REV1,
    deliverables: list[DeliverableEntry] | None = None,
) -> FrozenPortfolioSnapshot:
    return make_draft(
        workspace_id=workspace_id,
        campaign_id=campaign_id,
        portfolio_id=portfolio_id,
        revision_id=revision_id,
        deliverables=deliverables,
    ).seal()


# ---------------------------------------------------------------------------
# Positive tests — draft creation
# ---------------------------------------------------------------------------


def test_ca_m008_draft_creates_with_correct_lifecycle_state() -> None:
    draft = make_draft()
    assert draft.lifecycle_state == PortfolioLifecycleState.DRAFT


def test_ca_m008_draft_captures_all_required_fields() -> None:
    deliverable = make_deliverable(did="d-001", label="Hero Video", qty=3)
    draft = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV1,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context="Test narrative context",
        deliverables=[deliverable],
    )
    assert draft.portfolio_id == PORT
    assert draft.revision_id == REV1
    assert draft.workspace_id == WS
    assert draft.campaign_id == CAM
    assert draft.narrative_context == "Test narrative context"
    assert len(draft.deliverables) == 1
    assert draft.deliverables[0].deliverable_id == "d-001"
    assert draft.deliverables[0].label == "Hero Video"
    assert draft.deliverables[0].quantity == 3


def test_ca_m008_draft_computes_revision_digest_on_creation() -> None:
    draft = make_draft()
    assert isinstance(draft.revision_digest, str)
    assert len(draft.revision_digest) == 64  # SHA-256 hex


def test_ca_m008_draft_digest_is_stable_across_identical_calls() -> None:
    """The digest is deterministic given identical inputs and timestamps."""
    ts = "2026-09-08T12:00:00Z"
    draft_a = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV1,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context="stable",
        deliverables=[make_deliverable()],
        created_at=ts,
    )
    draft_b = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV1,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context="stable",
        deliverables=[make_deliverable()],
        created_at=ts,
    )
    assert draft_a.revision_digest == draft_b.revision_digest


def test_ca_m008_draft_verify_digest_passes_for_intact_snapshot() -> None:
    draft = make_draft()
    draft.verify_digest()  # must not raise


def test_ca_m008_deliverable_aspect_ratio_fields_are_captured() -> None:
    spec = AspectRatioSpec(ratio_label="9:16", width_px=1080, height_px=1920)
    entry = DeliverableEntry(
        deliverable_id="d-vertical",
        label="Vertical Clip",
        quantity=2,
        aspect_ratio=spec,
        format_requirement=make_format(),
    )
    draft = make_draft(deliverables=[entry])
    captured = draft.deliverables[0].aspect_ratio
    assert captured.ratio_label == "9:16"
    assert captured.width_px == 1080
    assert captured.height_px == 1920


def test_ca_m008_deliverable_format_requirement_fields_are_captured() -> None:
    fmt = FormatRequirement(format_id="image-still", codec_or_mime="image/jpeg", notes="JPEG only")
    entry = DeliverableEntry(
        deliverable_id="d-image",
        label="Still Image",
        quantity=5,
        aspect_ratio=make_aspect("1:1", 1080, 1080),
        format_requirement=fmt,
    )
    draft = make_draft(deliverables=[entry])
    captured = draft.deliverables[0].format_requirement
    assert captured.format_id == "image-still"
    assert captured.codec_or_mime == "image/jpeg"
    assert captured.notes == "JPEG only"


# ---------------------------------------------------------------------------
# Positive tests — sealing lifecycle transition
# ---------------------------------------------------------------------------


def test_ca_m008_seal_transitions_state_to_sealed() -> None:
    draft = make_draft()
    sealed = draft.seal()
    assert sealed.lifecycle_state == PortfolioLifecycleState.SEALED


def test_ca_m008_seal_preserves_revision_digest() -> None:
    """The lifecycle state is excluded from the digest, so sealing must not change it."""
    draft = make_draft()
    sealed = draft.seal()
    assert sealed.revision_digest == draft.revision_digest


def test_ca_m008_sealed_snapshot_verify_digest_passes() -> None:
    sealed = make_sealed()
    sealed.verify_digest()  # must not raise


def test_ca_m008_sealed_snapshot_all_fields_intact() -> None:
    draft = make_draft()
    sealed = draft.seal()
    assert sealed.portfolio_id == draft.portfolio_id
    assert sealed.revision_id == draft.revision_id
    assert sealed.workspace_id == draft.workspace_id
    assert sealed.campaign_id == draft.campaign_id
    assert sealed.narrative_context == draft.narrative_context
    assert sealed.deliverables == draft.deliverables
    assert sealed.created_at == draft.created_at


# ---------------------------------------------------------------------------
# Positive tests — require_admitted_portfolio
# ---------------------------------------------------------------------------


def test_ca_m008_require_admitted_portfolio_passes_for_sealed_snapshot() -> None:
    sealed = make_sealed()
    result = require_admitted_portfolio(sealed, workspace_id=WS, campaign_id=CAM)
    assert result is sealed


def test_ca_m008_admitted_portfolio_returns_same_object() -> None:
    sealed = make_sealed()
    admitted = require_admitted_portfolio(sealed, workspace_id=WS, campaign_id=CAM)
    assert admitted.revision_digest == sealed.revision_digest


# ---------------------------------------------------------------------------
# Positive tests — to_dict serialization
# ---------------------------------------------------------------------------


def test_ca_m008_to_dict_includes_schema_version_and_invariant() -> None:
    sealed = make_sealed()
    d = sealed.to_dict()
    assert d["schema"] == PORTFOLIO_SCHEMA_VERSION
    assert d["invariant_id"] == INVARIANT_ID


def test_ca_m008_to_dict_exposes_complete_contract() -> None:
    sealed = make_sealed()
    d = sealed.to_dict()
    assert "portfolio_id" in d
    assert "revision_id" in d
    assert "workspace_id" in d
    assert "campaign_id" in d
    assert "narrative_context" in d
    assert "deliverables" in d
    assert "lifecycle_state" in d
    assert "revision_digest" in d
    assert "created_at" in d


def test_ca_m008_to_dict_deliverables_includes_aspect_and_format() -> None:
    sealed = make_sealed()
    deliverable_dicts = sealed.to_dict()["deliverables"]
    assert len(deliverable_dicts) == 1
    dv = deliverable_dicts[0]
    assert "deliverable_id" in dv
    assert "quantity" in dv
    assert "aspect_ratio" in dv
    assert "format_requirement" in dv
    assert dv["aspect_ratio"]["ratio_label"] == "16:9"
    assert dv["format_requirement"]["format_id"] == "short-form-video"


def test_ca_m008_to_dict_lifecycle_state_is_serialized_as_string() -> None:
    sealed = make_sealed()
    d = sealed.to_dict()
    assert d["lifecycle_state"] == "SEALED"


# ---------------------------------------------------------------------------
# Positive tests — notes excluded from digest
# ---------------------------------------------------------------------------


def test_ca_m008_notes_do_not_affect_revision_digest() -> None:
    """Notes are operator annotations; they must not change the contract identity."""
    ts = "2026-09-08T12:00:00Z"
    without_notes = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV1,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context="Same",
        deliverables=[make_deliverable()],
        created_at=ts,
    )
    with_notes = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV1,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context="Same",
        deliverables=[make_deliverable()],
        notes="This annotation must not change the digest",
        created_at=ts,
    )
    assert without_notes.revision_digest == with_notes.revision_digest


# ---------------------------------------------------------------------------
# Positive tests — multiple deliverables and revisions
# ---------------------------------------------------------------------------


def test_ca_m008_multiple_deliverables_captured_in_order() -> None:
    d1 = make_deliverable(did="d-001", label="Hero Video", qty=3)
    d2 = DeliverableEntry(
        deliverable_id="d-002",
        label="Carousel Card",
        quantity=5,
        aspect_ratio=AspectRatioSpec("1:1", 1080, 1080),
        format_requirement=FormatRequirement("image-still", codec_or_mime="image/jpeg"),
    )
    draft = make_draft(deliverables=[d1, d2])
    assert len(draft.deliverables) == 2
    assert draft.deliverables[0].deliverable_id == "d-001"
    assert draft.deliverables[1].deliverable_id == "d-002"


def test_ca_m008_second_revision_has_different_digest() -> None:
    """A new revision with different content must produce a different digest."""
    ts = "2026-09-08T12:00:00Z"
    rev1 = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV1,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context="V1 context",
        deliverables=[make_deliverable(qty=3)],
        created_at=ts,
    )
    rev2 = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV2,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context="V2 context — updated quantity",
        deliverables=[make_deliverable(qty=5)],
        created_at=ts,
    )
    assert rev1.revision_digest != rev2.revision_digest


# ---------------------------------------------------------------------------
# Positive tests — registry
# ---------------------------------------------------------------------------


def test_ca_m008_registry_registers_and_retrieves_sealed_snapshot() -> None:
    registry = FrozenPortfolioRegistry()
    sealed = make_sealed()
    registry.register(sealed)
    retrieved = registry.get_revision(WS, PORT, REV1)
    assert retrieved is sealed


def test_ca_m008_registry_get_active_revision_returns_latest() -> None:
    registry = FrozenPortfolioRegistry()
    sealed1 = make_sealed(revision_id=REV1)
    sealed2 = make_sealed(revision_id=REV2)
    registry.register(sealed1)
    registry.register(sealed2)
    active = registry.get_active_revision(WS, PORT)
    assert active is sealed2


def test_ca_m008_registry_list_revision_ids_returns_all() -> None:
    registry = FrozenPortfolioRegistry()
    sealed1 = make_sealed(revision_id=REV1)
    sealed2 = make_sealed(revision_id=REV2)
    registry.register(sealed1)
    registry.register(sealed2)
    ids = registry.list_revision_ids(WS, PORT)
    assert REV1 in ids
    assert REV2 in ids


def test_ca_m008_registry_returns_none_for_unknown_revision() -> None:
    registry = FrozenPortfolioRegistry()
    result = registry.get_revision(WS, PORT, "nonexistent-rev")
    assert result is None


def test_ca_m008_registry_returns_none_for_unknown_portfolio() -> None:
    registry = FrozenPortfolioRegistry()
    result = registry.get_active_revision(WS, "portfolio-unknown")
    assert result is None


# ---------------------------------------------------------------------------
# Negative tests — invalid deliverable construction
# ---------------------------------------------------------------------------


def test_ca_m008_empty_deliverables_raises_invalid_deliverable_error() -> None:
    with pytest.raises(InvalidDeliverableError, match="at least one deliverable"):
        FrozenPortfolioSnapshot.create_draft(
            portfolio_id=PORT,
            revision_id=REV1,
            workspace_id=WS,
            campaign_id=CAM,
            narrative_context="Test",
            deliverables=[],
        )


def test_ca_m008_duplicate_deliverable_ids_raises_invalid_deliverable_error() -> None:
    d1 = make_deliverable(did="d-001")
    d2 = make_deliverable(did="d-001")  # same id
    with pytest.raises(InvalidDeliverableError, match="unique"):
        make_draft(deliverables=[d1, d2])


def test_ca_m008_zero_quantity_raises_invalid_deliverable_error() -> None:
    with pytest.raises(InvalidDeliverableError, match="quantity"):
        DeliverableEntry(
            deliverable_id="d-bad",
            label="Bad",
            quantity=0,
            aspect_ratio=make_aspect(),
            format_requirement=make_format(),
        )


def test_ca_m008_negative_quantity_raises_invalid_deliverable_error() -> None:
    with pytest.raises(InvalidDeliverableError, match="quantity"):
        DeliverableEntry(
            deliverable_id="d-neg",
            label="Negative",
            quantity=-1,
            aspect_ratio=make_aspect(),
            format_requirement=make_format(),
        )


def test_ca_m008_blank_deliverable_id_raises_invalid_deliverable_error() -> None:
    with pytest.raises(InvalidDeliverableError, match="deliverable_id"):
        DeliverableEntry(
            deliverable_id="  ",
            label="Label",
            quantity=1,
            aspect_ratio=make_aspect(),
            format_requirement=make_format(),
        )


def test_ca_m008_blank_deliverable_label_raises_invalid_deliverable_error() -> None:
    with pytest.raises(InvalidDeliverableError, match="label"):
        DeliverableEntry(
            deliverable_id="d-ok",
            label="",
            quantity=1,
            aspect_ratio=make_aspect(),
            format_requirement=make_format(),
        )


def test_ca_m008_zero_width_px_raises_invalid_deliverable_error() -> None:
    with pytest.raises(InvalidDeliverableError, match="width_px"):
        AspectRatioSpec(ratio_label="16:9", width_px=0, height_px=1080)


def test_ca_m008_blank_format_id_raises_invalid_deliverable_error() -> None:
    with pytest.raises(InvalidDeliverableError, match="format_id"):
        FormatRequirement(format_id="")


# ---------------------------------------------------------------------------
# Negative tests — lifecycle mutation prohibition
# ---------------------------------------------------------------------------


def test_ca_m008_sealing_already_sealed_snapshot_raises_mutation_error() -> None:
    sealed = make_sealed()
    with pytest.raises(PortfolioMutationError, match="already SEALED"):
        sealed.seal()


def test_ca_m008_draft_cannot_be_admitted_for_evidence_acquisition() -> None:
    draft = make_draft()
    with pytest.raises(PortfolioAdmissionError, match="SEALED"):
        require_admitted_portfolio(draft, workspace_id=WS, campaign_id=CAM)


# ---------------------------------------------------------------------------
# Negative tests — admission gate failures
# ---------------------------------------------------------------------------


def test_ca_m008_none_portfolio_is_refused_at_admission_gate() -> None:
    with pytest.raises(PortfolioAdmissionError):
        require_admitted_portfolio(None, workspace_id=WS, campaign_id=CAM)  # type: ignore[arg-type]


def test_ca_m008_wrong_type_is_refused_at_admission_gate() -> None:
    with pytest.raises(PortfolioAdmissionError):
        require_admitted_portfolio("not-a-snapshot", workspace_id=WS, campaign_id=CAM)  # type: ignore[arg-type]


def test_ca_m008_cross_workspace_admission_is_refused() -> None:
    sealed = make_sealed(workspace_id="ws-other")
    with pytest.raises(PortfolioAdmissionError, match="workspace_id"):
        require_admitted_portfolio(sealed, workspace_id=WS, campaign_id=CAM)


def test_ca_m008_cross_campaign_admission_is_refused() -> None:
    sealed = make_sealed(campaign_id="campaign-other")
    with pytest.raises(PortfolioAdmissionError, match="campaign_id"):
        require_admitted_portfolio(sealed, workspace_id=WS, campaign_id=CAM)


# ---------------------------------------------------------------------------
# Negative tests — digest integrity
# ---------------------------------------------------------------------------


def test_ca_m008_tampered_deliverable_quantity_changes_digest() -> None:
    """A deliverable field change must yield a different digest, catching mutation."""
    ts = "2026-09-08T12:00:00Z"
    original = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV1,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context="Context",
        deliverables=[make_deliverable(qty=3)],
        created_at=ts,
    )
    # Build a tampered snapshot with the same frozen digest but different quantity
    tampered_entry = DeliverableEntry(
        deliverable_id="d-001",
        label="Hero Video",
        quantity=99,  # mutated from 3
        aspect_ratio=make_aspect(),
        format_requirement=make_format(),
    )
    tampered = dataclasses.replace(original, deliverables=(tampered_entry,))
    # The stored digest no longer matches the actual content
    with pytest.raises(PortfolioDigestMismatchError):
        tampered.verify_digest()


def test_ca_m008_tampered_narrative_context_changes_digest() -> None:
    ts = "2026-09-08T12:00:00Z"
    original = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV1,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context="original narrative",
        deliverables=[make_deliverable()],
        created_at=ts,
    )
    tampered = dataclasses.replace(original, narrative_context="mutated narrative")
    with pytest.raises(PortfolioDigestMismatchError):
        tampered.verify_digest()


def test_ca_m008_tampered_snapshot_is_rejected_at_admission_gate() -> None:
    """require_admitted_portfolio must detect a tampered sealed snapshot."""
    sealed = make_sealed()
    tampered_entry = DeliverableEntry(
        deliverable_id="d-001",
        label="Hero Video",
        quantity=999,  # silently mutated
        aspect_ratio=make_aspect(),
        format_requirement=make_format(),
    )
    tampered = dataclasses.replace(sealed, deliverables=(tampered_entry,))
    with pytest.raises(PortfolioDigestMismatchError):
        require_admitted_portfolio(tampered, workspace_id=WS, campaign_id=CAM)


# ---------------------------------------------------------------------------
# Negative tests — registry admission
# ---------------------------------------------------------------------------


def test_ca_m008_registry_refuses_draft_registration() -> None:
    registry = FrozenPortfolioRegistry()
    draft = make_draft()
    with pytest.raises(PortfolioAdmissionError, match="SEALED"):
        registry.register(draft)


def test_ca_m008_registry_refuses_duplicate_revision_id() -> None:
    registry = FrozenPortfolioRegistry()
    sealed = make_sealed(revision_id=REV1)
    registry.register(sealed)
    with pytest.raises(DuplicatePortfolioRevisionError, match=REV1):
        registry.register(sealed)


def test_ca_m008_registry_refuses_tampered_snapshot_on_registration() -> None:
    registry = FrozenPortfolioRegistry()
    sealed = make_sealed()
    tampered = dataclasses.replace(sealed, narrative_context="injected narrative")
    with pytest.raises(PortfolioDigestMismatchError):
        registry.register(tampered)


# ---------------------------------------------------------------------------
# Integration evidence — full campaign → seal → admit path
# ---------------------------------------------------------------------------


def test_ca_m008_integration_full_path_from_draft_to_admitted_evidence() -> None:
    """
    Integration proof: DRAFT → SEALED → admitted for evidence acquisition.

    This test exercises the complete campaign content portfolio lifecycle
    mandated by FR-PORT-001:

    1. A draft portfolio is constructed for a campaign with deliverable
       specifications (identity, quantity, aspect ratio, format requirement).
    2. The draft is sealed, creating an immutable snapshot.
    3. The sealed snapshot is registered in the registry.
    4. Evidence acquisition admission is called; the portfolio passes all
       validation gates (workspace, campaign, state, digest).
    5. The admitted snapshot is the exact same object registered.
    6. A second revision cannot overwrite the first in the registry.
    """
    # Step 1 — create draft with two deliverables
    deliverables = [
        DeliverableEntry(
            deliverable_id="d-hero",
            label="Hero Short Video",
            quantity=3,
            aspect_ratio=AspectRatioSpec("16:9", 1920, 1080),
            format_requirement=FormatRequirement("short-form-video", "video/mp4"),
        ),
        DeliverableEntry(
            deliverable_id="d-vertical",
            label="Vertical Cut",
            quantity=2,
            aspect_ratio=AspectRatioSpec("9:16", 1080, 1920),
            format_requirement=FormatRequirement("short-form-video", "video/mp4"),
        ),
    ]
    draft = FrozenPortfolioSnapshot.create_draft(
        portfolio_id=PORT,
        revision_id=REV1,
        workspace_id=WS,
        campaign_id=CAM,
        narrative_context=(
            "Q4 launch campaign — guest: Jane Doe — "
            "tension: autonomy vs accountability"
        ),
        deliverables=deliverables,
        notes="Operator-drafted notes are excluded from the contract digest.",
    )
    assert draft.lifecycle_state == PortfolioLifecycleState.DRAFT

    # Step 2 — seal the portfolio
    sealed = draft.seal()
    assert sealed.lifecycle_state == PortfolioLifecycleState.SEALED
    assert sealed.revision_digest == draft.revision_digest  # digest unchanged by sealing

    # Step 3 — register in the registry
    registry = FrozenPortfolioRegistry()
    registry.register(sealed)

    # Step 4 — evidence acquisition admission
    active = registry.get_active_revision(WS, PORT)
    assert active is sealed
    admitted = require_admitted_portfolio(active, workspace_id=WS, campaign_id=CAM)
    assert admitted is sealed

    # Step 5 — admitted snapshot has exact deliverable contract
    assert len(admitted.deliverables) == 2
    hero = admitted.deliverables[0]
    assert hero.deliverable_id == "d-hero"
    assert hero.quantity == 3
    assert hero.aspect_ratio.ratio_label == "16:9"
    assert hero.format_requirement.format_id == "short-form-video"

    # Step 6 — second revision cannot overwrite rev-001
    sealed2 = make_sealed(revision_id=REV2)
    registry.register(sealed2)
    with pytest.raises(DuplicatePortfolioRevisionError):
        registry.register(sealed)  # attempt to overwrite rev-001 is blocked

    # Original revision is still retrievable unchanged
    retrieved_rev1 = registry.get_revision(WS, PORT, REV1)
    assert retrieved_rev1 is sealed
    retrieved_rev1.verify_digest()  # digest integrity is intact after registry operations


def test_ca_m008_regression_seal_does_not_mutate_original_draft() -> None:
    """Regression: sealing must produce a new object; the original draft is unmodified."""
    draft = make_draft()
    sealed = draft.seal()
    assert draft.lifecycle_state == PortfolioLifecycleState.DRAFT  # draft unchanged
    assert sealed.lifecycle_state == PortfolioLifecycleState.SEALED


def test_ca_m008_regression_draft_portfolio_is_refused_before_interview_starts() -> None:
    """
    Regression: evidence acquisition cannot begin with a DRAFT portfolio.

    This is the core invariant of FR-PORT-001: the portfolio must be frozen
    (SEALED) before physical evidence acquisition proceeds.
    """
    registry = FrozenPortfolioRegistry()
    draft = make_draft()
    # A draft cannot be registered
    with pytest.raises(PortfolioAdmissionError):
        registry.register(draft)

    # Even if we bypass the registry, direct admission must also fail
    with pytest.raises(PortfolioAdmissionError, match="SEALED"):
        require_admitted_portfolio(draft, workspace_id=WS, campaign_id=CAM)
