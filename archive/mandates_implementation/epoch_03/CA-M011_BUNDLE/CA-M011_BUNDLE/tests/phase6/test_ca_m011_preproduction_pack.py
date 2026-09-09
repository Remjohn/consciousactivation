"""
CA-M011 — Test suite for Cryptographically Sealed Pre-Production Snapshot
FR-PREP-001 — Sealed Pre-Production Pack

Invariant proven by this test file:
    No pipeline stage may execute against an unsealed, modified, or unverified
    pre-production pack.  A sealed snapshot is identified by a deterministic
    SHA-256 digest.  Any mutation of upstream constituent state after sealing
    is detected at execution admission and causes a fail-closed rejection.

Test categories:
    POSITIVE — intended path: compile, seal, persist, retrieve, admit.
    NEGATIVE — fail-closed boundary: tampered inputs, digest mismatch,
               stale snapshot, UI-only-seal bypass, mutable-rehydration,
               duplicate / conflicting seals, and latest-state substitution.

Mandate evidence record (per Section 9 of the mandate):
    Command:     pytest tests/phase6/test_ca_m011_preproduction_pack.py -v
    Environment: tmp_path (pytest fixture) — isolated SQLite database per test
    Fixtures:    _app(), _constituent(), _draft(), _seal()
    Limitation:  Tests use an in-process SQLite repository; they do not cover
                 multi-process concurrency or network-remote state stores.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

# Ensure the project packages are importable in this test environment.
import sys
_ROOT = Path(__file__).resolve().parents[2]
for _p in [
    _ROOT / "packages/ca_contracts/src",
    _ROOT / "packages/ca_runtime/src",
    _ROOT / "services/pipeline/src",
]:
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from ca_contracts import canonical_sha256

from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import PipelineValidationError
from cmf_pipeline.preproduction import (
    ConstituentRef,
    PreprodAdmissionDecision,
    PreprodAdmissionError,
    PreprodPackDraft,
    PreprodPackState,
    PreprodRejectionReason,
    PreprodSealError,
    PreProductionSealer,
    SealedPreprodPack,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_db(tmp_path: Path) -> Path:
    return tmp_path / "test_ca_m011.sqlite3"


@pytest.fixture
def app(tmp_db: Path) -> PipelineApplication:
    a = PipelineApplication(tmp_db)
    a.initialize()
    return a


@pytest.fixture
def sealer(app: PipelineApplication) -> PreProductionSealer:
    return PreProductionSealer(app.repository)


def _make_constituent(
    *,
    constituent_type: str = "prompt",
    object_id: str = "prompt:001",
    revision: str = "1",
    seed: str = "seed-001",
    authority: str = "EDITORIAL_AUTHORITY",
) -> ConstituentRef:
    """Build a ConstituentRef with a deterministic content_digest from seed."""
    content_digest = canonical_sha256({"seed": seed, "type": constituent_type})
    return ConstituentRef(
        constituent_type=constituent_type,
        object_id=object_id,
        revision=revision,
        content_digest=content_digest,
        authority=authority,
    )


def _prep_digest(seed: str = "prep-graph-v1") -> str:
    return canonical_sha256({"preparation_seed": seed})


def _make_draft(
    *,
    campaign_id: str = "campaign:alpha",
    operator_id: str = "operator:alice",
    prompts: list[ConstituentRef] | None = None,
    model_manifests: list[ConstituentRef] | None = None,
    media_refs: list[ConstituentRef] | None = None,
    parameters: list[ConstituentRef] | None = None,
    prep_seed: str = "prep-graph-v1",
) -> PreprodPackDraft:
    if prompts is None:
        prompts = [_make_constituent(constituent_type="prompt", object_id="prompt:001", seed="p1")]
    if model_manifests is None:
        model_manifests = [_make_constituent(constituent_type="model_manifest", object_id="model:gpt4o", seed="m1")]
    if media_refs is None:
        media_refs = [_make_constituent(constituent_type="media_ref", object_id="media:hero.mp4", seed="mr1")]
    if parameters is None:
        parameters = [_make_constituent(constituent_type="parameters", object_id="params:v1", seed="par1")]
    return PreprodPackDraft(
        campaign_id=campaign_id,
        operator_id=operator_id,
        prompts=prompts,
        model_manifests=model_manifests,
        media_refs=media_refs,
        parameters=parameters,
        preparation_revision="rev-001",
        preparation_digest=_prep_digest(prep_seed),
    )


# ---------------------------------------------------------------------------
# POSITIVE TESTS — intended path
# ---------------------------------------------------------------------------


class TestPositive:
    """Tests that verify the intended compile → seal → persist → retrieve → admit path."""

    def test_compile_and_seal_returns_sealed_pack(self, sealer: PreProductionSealer):
        """
        Property proved: compile_and_seal() returns a SealedPreprodPack with
        state=SEALED and a non-empty pack_digest.
        """
        draft = _make_draft()
        pack = sealer.compile_and_seal(draft, idempotency_key="test:seal:001")

        assert isinstance(pack, SealedPreprodPack)
        assert pack.state == PreprodPackState.SEALED
        assert pack.pack_digest, "pack_digest must be non-empty"
        assert len(pack.pack_digest) == 64, "pack_digest must be a 64-char SHA-256 hex"
        assert pack.pack_id == f"preprod-pack:{pack.pack_digest}"

    def test_pack_digest_is_deterministic(self, sealer: PreProductionSealer, tmp_db: Path):
        """
        Property proved: identical drafts produce identical pack_digests across
        independent sealer instances (no timestamp or random contribution to digest).
        """
        draft = _make_draft()
        pack1 = sealer.compile_and_seal(draft, idempotency_key="test:det:a")

        # New sealer instance, same database — idempotency key differs
        app2 = PipelineApplication(tmp_db)
        app2.initialize()
        sealer2 = PreProductionSealer(app2.repository)
        draft2 = _make_draft()  # structurally identical draft
        pack2 = sealer2.compile_and_seal(draft2, idempotency_key="test:det:b")

        assert pack1.pack_digest == pack2.pack_digest, (
            "identical drafts must produce identical digests (determinism invariant)"
        )

    def test_sealed_pack_is_retrievable_by_id(self, sealer: PreProductionSealer):
        """
        Property proved: a sealed pack can be retrieved from the repository by its
        pack_id and the retrieved object has the same digest.
        """
        draft = _make_draft()
        pack = sealer.compile_and_seal(draft, idempotency_key="test:retrieve:001")

        retrieved = sealer.get_pack(pack.pack_id)
        assert retrieved.pack_id == pack.pack_id
        assert retrieved.pack_digest == pack.pack_digest
        assert retrieved.state == PreprodPackState.SEALED

    def test_admitted_run_binding_is_persisted(self, sealer: PreProductionSealer):
        """
        Property proved: after successful execution admission, a run binding
        receipt is persisted in the repository.
        """
        draft = _make_draft()
        pack = sealer.compile_and_seal(draft, idempotency_key="test:bind:seal:001")

        result = sealer.admit_for_execution(
            pack.pack_id,
            pack.pack_digest,
            run_id="run:beta-001",
            idempotency_key="test:bind:admit:001",
        )
        assert result.is_admitted
        assert result.decision == PreprodAdmissionDecision.ADMITTED

        binding = sealer.get_run_binding("run:beta-001", pack.pack_id)
        assert binding["payload"]["pack_id"] == pack.pack_id
        assert binding["payload"]["pack_digest"] == pack.pack_digest
        assert binding["payload"]["run_id"] == "run:beta-001"
        assert binding["payload"]["decision"] == "ADMITTED"

    def test_constituent_cross_check_passes_for_exact_match(self, sealer: PreProductionSealer):
        """
        Property proved: admission with explicit expected_constituents succeeds
        when all constituent digests match the sealed pack exactly.
        """
        prompt = _make_constituent(constituent_type="prompt", object_id="prompt:c01", seed="cp1")
        draft = _make_draft(prompts=[prompt])
        pack = sealer.compile_and_seal(draft, idempotency_key="test:constcheck:seal")

        result = sealer.admit_for_execution(
            pack.pack_id,
            pack.pack_digest,
            run_id="run:constcheck-001",
            expected_constituents=[prompt],
            idempotency_key="test:constcheck:admit",
        )
        assert result.is_admitted

    def test_supersede_marks_old_pack_and_allows_new_seal(self, sealer: PreProductionSealer):
        """
        Property proved: a SEALED pack can be superseded; the historical identity
        is preserved; a new draft can be sealed as a new candidate.
        """
        draft_v1 = _make_draft(prep_seed="v1")
        pack_v1 = sealer.compile_and_seal(draft_v1, idempotency_key="test:super:seal:v1")
        assert pack_v1.state == PreprodPackState.SEALED

        superseded = sealer.supersede_pack(pack_v1.pack_id, idempotency_key="test:super:supersede:v1")
        assert superseded.state == PreprodPackState.SUPERSEDED
        # digest unchanged
        assert superseded.pack_digest == pack_v1.pack_digest

        # New draft produces a different pack
        draft_v2 = _make_draft(prep_seed="v2")
        pack_v2 = sealer.compile_and_seal(draft_v2, idempotency_key="test:super:seal:v2")
        assert pack_v2.state == PreprodPackState.SEALED
        assert pack_v2.pack_id != pack_v1.pack_id

    def test_list_packs_returns_current_sealed_packs(self, sealer: PreProductionSealer):
        """
        Property proved: list_packs() returns all current sealed packs for a campaign.
        """
        draft = _make_draft(campaign_id="campaign:list-test", prep_seed="list-v1")
        sealer.compile_and_seal(draft, idempotency_key="test:list:001")

        packs = sealer.list_packs(campaign_id="campaign:list-test")
        assert len(packs) >= 1
        assert all(p.campaign_id == "campaign:list-test" for p in packs)

    def test_idempotent_seal_replay_returns_same_pack(self, sealer: PreProductionSealer):
        """
        Property proved: calling compile_and_seal() twice with the same
        idempotency_key returns the same pack (repository idempotency).
        """
        draft = _make_draft(prep_seed="idempotent-v1")
        pack1 = sealer.compile_and_seal(draft, idempotency_key="test:idempotent:001")
        pack2 = sealer.compile_and_seal(draft, idempotency_key="test:idempotent:001")
        assert pack1.pack_id == pack2.pack_id
        assert pack1.pack_digest == pack2.pack_digest

    def test_constituents_are_bound_and_retrievable_from_sealed_pack(self, sealer: PreProductionSealer):
        """
        Property proved: all constituent types (prompt, model_manifest, media_ref,
        parameters) are bound into the sealed pack and survives a round-trip
        through the repository.
        """
        prompt = _make_constituent(constituent_type="prompt", object_id="pr:01", seed="p-seed")
        model = _make_constituent(constituent_type="model_manifest", object_id="mo:01", seed="m-seed")
        media = _make_constituent(constituent_type="media_ref", object_id="me:01", seed="mr-seed")
        params = _make_constituent(constituent_type="parameters", object_id="pa:01", seed="pa-seed")
        draft = _make_draft(
            prompts=[prompt],
            model_manifests=[model],
            media_refs=[media],
            parameters=[params],
        )
        pack = sealer.compile_and_seal(draft, idempotency_key="test:constituents:001")
        retrieved = sealer.get_pack(pack.pack_id)

        retrieved_ids = {c.object_id for c in retrieved.constituents}
        assert {"pr:01", "mo:01", "me:01", "pa:01"} == retrieved_ids

        retrieved_types = {c.constituent_type for c in retrieved.constituents}
        assert {"prompt", "model_manifest", "media_ref", "parameters"} == retrieved_types


# ---------------------------------------------------------------------------
# NEGATIVE TESTS — fail-closed boundary
# ---------------------------------------------------------------------------


class TestNegative:
    """
    Tests that prove the fail-closed boundary.

    Each test verifies that a specific tampering or bypass attempt is REJECTED
    with the correct reason before any downstream pipeline stage can proceed.
    """

    # --- Digest mismatch ---------------------------------------------------

    def test_stale_digest_is_rejected_at_admission(self, sealer: PreProductionSealer):
        """
        Property proved: supplying a stale / wrong pack_digest is rejected with
        DIGEST_MISMATCH even when the pack_id is valid.

        False-proof case: caller holds an old digest from a superseded pack.
        """
        draft = _make_draft()
        pack = sealer.compile_and_seal(draft, idempotency_key="test:stale:seal")
        stale_digest = canonical_sha256({"stale": "yes"})  # not the real digest

        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                pack.pack_id,
                stale_digest,
                run_id="run:stale-001",
                idempotency_key="test:stale:admit",
            )
        result = exc_info.value.result
        assert result.decision == PreprodAdmissionDecision.REJECTED
        assert result.reason == PreprodRejectionReason.DIGEST_MISMATCH
        assert "stale" not in result.details.get("stored_digest", "")

    def test_forged_pack_id_that_does_not_exist_is_rejected(self, sealer: PreProductionSealer):
        """
        Property proved: a pack_id not in the repository causes PACK_NOT_FOUND.
        """
        forged_digest = canonical_sha256({"forged": True})
        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                f"preprod-pack:{forged_digest}",
                forged_digest,
                run_id="run:forged-001",
                idempotency_key="test:forged:admit",
            )
        assert exc_info.value.result.reason == PreprodRejectionReason.PACK_NOT_FOUND

    # --- Mutable rehydration detection (false-proof case) ------------------

    def test_mutable_rehydration_after_sealing_is_detected(
        self, sealer: PreProductionSealer, app: PipelineApplication
    ):
        """
        Property proved: the false-proof case from CA-M011 mandate Section 9.

        "A system that reports a seal but silently rehydrates latest mutable
        data at execution time — that must fail."

        Mechanism: We manually overwrite the stored payload's constituent
        digest in the raw repository object, simulating an attacker who
        modifies the database after sealing.  Admission must detect this
        via the anti-rehydration digest recomputation step.
        """
        draft = _make_draft()
        pack = sealer.compile_and_seal(draft, idempotency_key="test:rehydrate:seal")

        # Retrieve the raw stored object and tamper with a constituent digest
        raw_obj = app.repository.get_object(pack.pack_id)
        payload = copy.deepcopy(raw_obj["payload"])
        if payload["constituents"]:
            # Replace the first constituent's content_digest with a different hash
            payload["constituents"][0]["content_digest"] = canonical_sha256({"mutated": True})

        # Write the tampered payload back using a new idempotency key
        app.repository.store_object(
            "preprod_sealed_pack",
            payload,
            idempotency_key="test:rehydrate:tamper",
            object_id=pack.pack_id,
            lifecycle_state="SEALED",
        )

        # Admission must reject because recomputed digest != stored pack_digest
        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                pack.pack_id,
                pack.pack_digest,
                run_id="run:rehydrate-001",
                idempotency_key="test:rehydrate:admit",
            )
        result = exc_info.value.result
        assert result.reason in (
            PreprodRejectionReason.MUTABLE_REHYDRATION_DETECTED,
            PreprodRejectionReason.DIGEST_MISMATCH,
        ), f"expected rehydration or digest mismatch, got: {result.reason}"

    # --- Tampered / changed upstream constituent --------------------------

    def test_constituent_digest_mismatch_is_rejected(self, sealer: PreProductionSealer):
        """
        Property proved: if a constituent's digest changes after sealing,
        the caller-supplied expected_constituents check fails with
        CONSTITUENT_DIGEST_MISMATCH.
        """
        original_prompt = _make_constituent(constituent_type="prompt", object_id="pr:tamper", seed="orig")
        draft = _make_draft(prompts=[original_prompt])
        pack = sealer.compile_and_seal(draft, idempotency_key="test:tamper:seal")

        # Caller holds a reference to the original constituent but its content changed
        mutated_prompt = ConstituentRef(
            constituent_type=original_prompt.constituent_type,
            object_id=original_prompt.object_id,
            revision=original_prompt.revision,
            content_digest=canonical_sha256({"mutated": "yes"}),
            authority=original_prompt.authority,
        )

        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                pack.pack_id,
                pack.pack_digest,
                run_id="run:tamper-001",
                expected_constituents=[mutated_prompt],
                idempotency_key="test:tamper:admit",
            )
        result = exc_info.value.result
        assert result.reason == PreprodRejectionReason.CONSTITUENT_DIGEST_MISMATCH

    def test_missing_required_constituent_is_rejected(self, sealer: PreProductionSealer):
        """
        Property proved: if the caller expects a constituent object_id that is not
        in the sealed pack, admission fails with MISSING_REQUIRED_CONSTITUENT.
        """
        draft = _make_draft()
        pack = sealer.compile_and_seal(draft, idempotency_key="test:missing:seal")

        phantom = _make_constituent(constituent_type="prompt", object_id="prompt:does-not-exist", seed="ghost")

        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                pack.pack_id,
                pack.pack_digest,
                run_id="run:missing-001",
                expected_constituents=[phantom],
                idempotency_key="test:missing:admit",
            )
        result = exc_info.value.result
        assert result.reason == PreprodRejectionReason.MISSING_REQUIRED_CONSTITUENT

    # --- Unsealed pack ---------------------------------------------------

    def test_invalidated_pack_is_rejected_at_admission(self, sealer: PreProductionSealer):
        """
        Property proved: an invalidated pack cannot be admitted even if the
        caller supplies the correct digest.

        State: SEALED → INVALIDATED → admission REJECTED
        """
        draft = _make_draft()
        pack = sealer.compile_and_seal(draft, idempotency_key="test:invalid:seal")
        sealer.invalidate_pack(pack.pack_id, idempotency_key="test:invalid:inv", reason="operator revoked")

        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                pack.pack_id,
                pack.pack_digest,
                run_id="run:invalid-001",
                idempotency_key="test:invalid:admit",
            )
        result = exc_info.value.result
        # PACK_NOT_SEALED covers the invalidated state check path because the stored
        # state is no longer SEALED; or PACK_INVALIDATED depending on state check order.
        assert result.reason in (
            PreprodRejectionReason.PACK_NOT_SEALED,
            PreprodRejectionReason.PACK_INVALIDATED,
        )

    # --- Draft-only (UI-only seal bypass) ---------------------------------

    def test_no_admission_without_prior_seal(self, sealer: PreProductionSealer):
        """
        Property proved: fabricating a pack_id that looks valid but was never
        sealed results in PACK_NOT_FOUND.  A UI or caller cannot bypass the
        sealing step by constructing a plausible pack_id.
        """
        fabricated_digest = canonical_sha256({"ui_only": True, "bypass": True})
        fabricated_id = f"preprod-pack:{fabricated_digest}"

        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                fabricated_id,
                fabricated_digest,
                run_id="run:ui-bypass",
                idempotency_key="test:uibypass:admit",
            )
        assert exc_info.value.result.reason == PreprodRejectionReason.PACK_NOT_FOUND

    # --- Latest-state substitution ----------------------------------------

    def test_latest_state_substitution_is_blocked(self, sealer: PreProductionSealer):
        """
        Property proved: if the upstream preparation state mutates after the
        pack was sealed, and the caller tries to re-admit using the NEW
        preparation_digest (i.e. latest-state substitution), admission fails
        because the pack_digest no longer matches.

        This test simulates the scenario where an attacker derives a new digest
        from the mutated preparation state and tries to pass it as pack_digest.
        """
        original_prep_seed = "original-prep"
        draft_v1 = _make_draft(prep_seed=original_prep_seed)
        pack_v1 = sealer.compile_and_seal(draft_v1, idempotency_key="test:latest:seal:v1")

        # Simulate upstream preparation state mutation → derive a new draft
        mutated_prep_seed = "mutated-prep"
        draft_mutated = _make_draft(prep_seed=mutated_prep_seed)

        # The attacker derives a NEW digest from mutated state and passes it
        from cmf_pipeline.preproduction.sealer import _pack_identity_payload
        from cmf_pipeline.preproduction.sealer import _prep_digest as _pd

        all_c = (
            list(draft_mutated.prompts)
            + list(draft_mutated.model_manifests)
            + list(draft_mutated.media_refs)
            + list(draft_mutated.parameters)
        )
        mutated_identity = _pack_identity_payload(
            campaign_id=draft_mutated.campaign_id,
            operator_id=draft_mutated.operator_id,
            preparation_revision=draft_mutated.preparation_revision,
            preparation_digest=draft_mutated.preparation_digest,
            constituents=all_c,
        )
        mutated_digest = canonical_sha256(mutated_identity)

        # Admission with the original pack_id but mutated digest must fail
        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                pack_v1.pack_id,
                mutated_digest,                 # ← latest-state substitution
                run_id="run:latest-sub-001",
                idempotency_key="test:latest:admit",
            )
        result = exc_info.value.result
        assert result.reason == PreprodRejectionReason.DIGEST_MISMATCH

    # --- Draft validation --------------------------------------------------

    def test_empty_constituent_list_is_rejected(self, sealer: PreProductionSealer):
        """
        Property proved: a draft with zero constituents raises PipelineValidationError.
        """
        draft = PreprodPackDraft(
            campaign_id="campaign:empty",
            operator_id="operator:alice",
            prompts=[],
            model_manifests=[],
            media_refs=[],
            parameters=[],
            preparation_revision="rev-001",
            preparation_digest=_prep_digest(),
        )
        with pytest.raises(PipelineValidationError, match="at least one constituent"):
            sealer.compile_and_seal(draft, idempotency_key="test:empty:seal")

    def test_duplicate_constituent_object_ids_are_rejected(self, sealer: PreProductionSealer):
        """
        Property proved: two constituents with the same object_id are rejected.
        """
        dup_a = _make_constituent(constituent_type="prompt", object_id="dup:001", seed="a")
        dup_b = _make_constituent(constituent_type="model_manifest", object_id="dup:001", seed="b")
        draft = PreprodPackDraft(
            campaign_id="campaign:dup",
            operator_id="operator:alice",
            prompts=[dup_a],
            model_manifests=[dup_b],
            media_refs=[],
            parameters=[_make_constituent(constituent_type="parameters", object_id="p:1", seed="p")],
            preparation_revision="rev-001",
            preparation_digest=_prep_digest(),
        )
        with pytest.raises(PipelineValidationError, match="duplicate"):
            sealer.compile_and_seal(draft, idempotency_key="test:dup:seal")

    def test_invalid_preparation_digest_format_is_rejected(self, sealer: PreProductionSealer):
        """
        Property proved: a malformed preparation_digest (not 64-char hex) is rejected.
        """
        draft = PreprodPackDraft(
            campaign_id="campaign:baddigest",
            operator_id="operator:alice",
            prompts=[_make_constituent(object_id="pr:01", seed="p")],
            model_manifests=[],
            media_refs=[],
            parameters=[],
            preparation_revision="rev-001",
            preparation_digest="not-a-sha256",
        )
        with pytest.raises(PipelineValidationError):
            sealer.compile_and_seal(draft, idempotency_key="test:baddig:seal")

    # --- Immutability — later draft is a new candidate --------------------

    def test_later_draft_does_not_mutate_original_sealed_pack(self, sealer: PreProductionSealer):
        """
        Property proved: sealing a new draft from updated preparation state
        creates a NEW pack object with a different pack_id; the original sealed
        pack retains its digest and state.
        """
        draft_v1 = _make_draft(prep_seed="original")
        pack_v1 = sealer.compile_and_seal(draft_v1, idempotency_key="test:immut:v1:seal")

        draft_v2 = _make_draft(prep_seed="updated")
        pack_v2 = sealer.compile_and_seal(draft_v2, idempotency_key="test:immut:v2:seal")

        assert pack_v1.pack_id != pack_v2.pack_id
        assert pack_v1.pack_digest != pack_v2.pack_digest

        # Original still SEALED with its original digest
        retrieved_v1 = sealer.get_pack(pack_v1.pack_id)
        assert retrieved_v1.state == PreprodPackState.SEALED
        assert retrieved_v1.pack_digest == pack_v1.pack_digest

    # --- Superseded pack cannot be admitted --------------------------------

    def test_superseded_pack_is_rejected_at_admission(self, sealer: PreProductionSealer):
        """
        Property proved: a SUPERSEDED pack cannot be admitted for execution.
        """
        draft = _make_draft(prep_seed="super-adm")
        pack = sealer.compile_and_seal(draft, idempotency_key="test:superadm:seal")
        sealer.supersede_pack(pack.pack_id, idempotency_key="test:superadm:super")

        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                pack.pack_id,
                pack.pack_digest,
                run_id="run:superadm-001",
                idempotency_key="test:superadm:admit",
            )
        assert exc_info.value.result.reason in (
            PreprodRejectionReason.PACK_NOT_SEALED,
            PreprodRejectionReason.PACK_SUPERSEDED,
        )

    # --- Constituent digest format validation ------------------------------

    def test_constituent_with_invalid_digest_format_is_rejected(self, sealer: PreProductionSealer):
        """
        Property proved: a constituent whose content_digest is not a valid
        64-char lowercase SHA-256 is rejected during draft validation.
        """
        bad_constituent = ConstituentRef(
            constituent_type="prompt",
            object_id="pr:bad",
            revision="1",
            content_digest="ZZZZ-not-hex",
            authority="EDITORIAL_AUTHORITY",
        )
        draft = PreprodPackDraft(
            campaign_id="campaign:badconst",
            operator_id="operator:alice",
            prompts=[bad_constituent],
            model_manifests=[],
            media_refs=[],
            parameters=[],
            preparation_revision="rev-001",
            preparation_digest=_prep_digest(),
        )
        with pytest.raises(PipelineValidationError):
            sealer.compile_and_seal(draft, idempotency_key="test:badconst:seal")


# ---------------------------------------------------------------------------
# ANTI-CENTROID / FALSE-PROOF TESTS
# ---------------------------------------------------------------------------


class TestAntiCentroid:
    """
    The mandate requires at least one anti-centroid (false-proof) case.

    A result can look polished and pass a shallow check while violating the
    actual invariant.  The tests below confirm that green-looking but
    structurally wrong inputs are reliably rejected.
    """

    def test_correct_pack_id_with_wrong_digest_does_not_leak_pack_data(
        self, sealer: PreProductionSealer
    ):
        """
        Anti-centroid: the pack exists, the pack_id is correct, BUT the digest
        is wrong (e.g. attacker constructed the wrong hash).
        Prove the system does NOT leak pack contents in the error; it only
        returns reason=DIGEST_MISMATCH.
        """
        draft = _make_draft()
        pack = sealer.compile_and_seal(draft, idempotency_key="test:anti:seal")
        wrong_digest = "a" * 64  # valid format, wrong value

        with pytest.raises(PreprodAdmissionError) as exc_info:
            sealer.admit_for_execution(
                pack.pack_id,
                wrong_digest,
                run_id="run:anti-001",
                idempotency_key="test:anti:admit",
            )
        result = exc_info.value.result
        assert result.reason == PreprodRejectionReason.DIGEST_MISMATCH
        # The error should contain diagnostics but not raw payload data
        assert "constituents" not in str(exc_info.value)

    def test_two_different_drafts_never_collide_on_digest(self, sealer: PreProductionSealer):
        """
        Anti-centroid: two structurally distinct drafts must never share a digest.
        Verifies that digest space is used correctly (no trivial collision source).
        """
        draft_a = _make_draft(prep_seed="anti-a")
        draft_b = _make_draft(prep_seed="anti-b")
        pack_a = sealer.compile_and_seal(draft_a, idempotency_key="test:nocollide:a")
        pack_b = sealer.compile_and_seal(draft_b, idempotency_key="test:nocollide:b")
        assert pack_a.pack_digest != pack_b.pack_digest

    def test_run_binding_not_persisted_on_rejected_admission(self, sealer: PreProductionSealer, app: PipelineApplication):
        """
        Anti-centroid: a rejected admission must NOT persist a run binding.
        If binding were persisted on rejection it would look like a successful
        binding but the run would operate against an unverified pack.
        """
        from cmf_pipeline.domain.errors import PipelineNotFound

        draft = _make_draft()
        pack = sealer.compile_and_seal(draft, idempotency_key="test:norbind:seal")
        bad_digest = "b" * 64

        with pytest.raises(PreprodAdmissionError):
            sealer.admit_for_execution(
                pack.pack_id,
                bad_digest,
                run_id="run:norbind-001",
                idempotency_key="test:norbind:admit",
            )

        # Attempt to retrieve the binding — it must NOT exist
        binding_id = f"preprod-run-binding:run:norbind-001:{pack.pack_id}"
        with pytest.raises(PipelineNotFound):
            app.repository.get_object(binding_id)

    def test_digest_is_over_actual_bytes_not_metadata_field(self, sealer: PreProductionSealer):
        """
        Anti-centroid: the digest must be computed from the actual constituent
        content bytes (modelled as canonical_sha256 of their identity payload),
        NOT merely from the presence of a metadata field named 'content_digest'.

        Proof: two constituents with the same object_id/type/revision but
        different content yield different pack_digests.
        """
        prompt_v1 = _make_constituent(constituent_type="prompt", object_id="pr:bytes", seed="v1-content")
        prompt_v2 = _make_constituent(constituent_type="prompt", object_id="pr:bytes", seed="v2-content")
        assert prompt_v1.content_digest != prompt_v2.content_digest

        draft_v1 = _make_draft(prompts=[prompt_v1])
        draft_v2 = PreprodPackDraft(
            campaign_id=draft_v1.campaign_id,
            operator_id=draft_v1.operator_id,
            prompts=[prompt_v2],
            model_manifests=list(draft_v1.model_manifests),
            media_refs=list(draft_v1.media_refs),
            parameters=list(draft_v1.parameters),
            preparation_revision=draft_v1.preparation_revision,
            preparation_digest=draft_v1.preparation_digest,
        )

        # They cannot share a pack_id because the constituent digests differ
        pack_v1 = sealer.compile_and_seal(draft_v1, idempotency_key="test:bytes:v1")
        pack_v2 = sealer.compile_and_seal(draft_v2, idempotency_key="test:bytes:v2")
        assert pack_v1.pack_digest != pack_v2.pack_digest
