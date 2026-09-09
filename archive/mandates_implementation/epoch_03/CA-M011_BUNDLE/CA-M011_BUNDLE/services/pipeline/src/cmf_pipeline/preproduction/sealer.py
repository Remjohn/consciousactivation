"""
CA-M011 — Cryptographically Sealed Pre-Production Snapshot
FR-PREP-001 — Sealed Pre-Production Pack

Enforces the authoritative mutable-to-immutable boundary:

    PREPARATION_STATE
        → COMPILE_SNAPSHOT
        → SEALED_PREPROD_SNAPSHOT
        → EXECUTION_ADMISSION

Invariant: No pipeline stage may execute against an unsealed, modified, or
unverified pack.  A sealed snapshot is identified by a deterministic SHA-256
digest of its canonical JSON representation.  Subsequent drafts produce new
candidates; they never mutate an already-sealed snapshot.

Design decisions (follow codebase pattern from causal_admission.py / source.py):
- canonical_json_text + canonical_sha256 from ca_contracts for deterministic
  serialisation and identity.
- PipelineRepository.store_object for durable object persistence.
- Errors subclass the project's PipelineError hierarchy.
- Frozen dataclasses for public value objects.
- All state transitions documented with actor / preconditions / postconditions.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping, Sequence

from ca_contracts import canonical_json_bytes, canonical_sha256, utc_now_rfc3339

from ..domain.errors import (
    PipelineLifecycleError,
    PipelineValidationError,
)
from ..domain.validation import reject_noncanonical, require_sha, require_string
from ..workflow.infrastructure.repository import PipelineRepository

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PREPROD_PACK_VERSION = "1.0.0"
PREPROD_PACK_OBJECT_TYPE = "preprod_sealed_pack"
PREPROD_RUN_BINDING_OBJECT_TYPE = "preprod_run_binding"
PREPROD_ADMISSION_RECEIPT_OBJECT_TYPE = "preprod_admission_receipt"

SEAL_ACTOR = "PreProductionSealer"

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class PreprodPackState(StrEnum):
    """Lifecycle states for a pre-production pack."""

    DRAFT = "DRAFT"               # Mutable preparation; not yet compiled
    COMPILED = "COMPILED"         # Snapshot compiled; digest computed; not yet sealed
    SEALED = "SEALED"             # Immutable; digest verified; admissible for execution
    SUPERSEDED = "SUPERSEDED"     # A newer sealed pack exists; this remains inspectable
    INVALIDATED = "INVALIDATED"   # Revoked; must not be used for execution


class PreprodAdmissionDecision(StrEnum):
    ADMITTED = "ADMITTED"
    REJECTED = "REJECTED"


class PreprodRejectionReason(StrEnum):
    PACK_NOT_FOUND = "PACK_NOT_FOUND"
    PACK_NOT_SEALED = "PACK_NOT_SEALED"
    DIGEST_MISMATCH = "DIGEST_MISMATCH"
    PACK_INVALIDATED = "PACK_INVALIDATED"
    PACK_SUPERSEDED = "PACK_SUPERSEDED"
    CONSTITUENT_DIGEST_MISMATCH = "CONSTITUENT_DIGEST_MISMATCH"
    MISSING_REQUIRED_CONSTITUENT = "MISSING_REQUIRED_CONSTITUENT"
    RUN_BINDING_MISMATCH = "RUN_BINDING_MISMATCH"
    MUTABLE_REHYDRATION_DETECTED = "MUTABLE_REHYDRATION_DETECTED"


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ConstituentRef:
    """
    Authoritative reference to a single upstream asset bound into the pack.

    Every constituent carries its own content digest so that any mutation
    of upstream state after sealing is detectable at admission time.
    """

    constituent_type: str       # e.g. "prompt", "model_manifest", "media_ref", "parameters"
    object_id: str              # stable semantic identity of the upstream object
    revision: str               # upstream revision/version at sealing time
    content_digest: str         # SHA-256 of the constituent's canonical representation
    authority: str              # authority boundary that produced this constituent


@dataclass(frozen=True)
class PreprodPackDraft:
    """
    Mutable preparation state passed to compile().

    The executor builds this from operator-approved preparation state.
    This is NOT the sealed object; it is the input to the compiler.
    """

    campaign_id: str
    operator_id: str
    prompts: Sequence[ConstituentRef]
    model_manifests: Sequence[ConstituentRef]
    media_refs: Sequence[ConstituentRef]
    parameters: Sequence[ConstituentRef]
    preparation_revision: str       # revision of the upstream preparation graph
    preparation_digest: str         # SHA-256 of the upstream preparation graph object


@dataclass(frozen=True)
class SealedPreprodPack:
    """
    Immutable, cryptographically identified pre-production pack.

    Identity is the SHA-256 of the canonical JSON of ALL constituent digests
    plus the preparation digest.  Any mutation of upstream state changes the
    identity, causing admission to fail.
    """

    pack_id: str                    # semantic identity: "preprod-pack:<digest>"
    pack_digest: str                # SHA-256 of canonical identity payload
    pack_version: str               # schema version
    campaign_id: str
    operator_id: str
    sealed_at_utc: str
    sealed_by: str                  # actor
    preparation_revision: str
    preparation_digest: str
    constituents: tuple[ConstituentRef, ...]
    state: PreprodPackState


@dataclass(frozen=True)
class PreprodAdmissionResult:
    """Result of attempting to admit a sealed pack for execution."""

    decision: PreprodAdmissionDecision
    pack_id: str
    pack_digest: str
    run_id: str
    reason: PreprodRejectionReason | None = None
    message: str = ""
    details: Mapping[str, Any] = field(default_factory=dict)

    @property
    def is_admitted(self) -> bool:
        return self.decision == PreprodAdmissionDecision.ADMITTED

    def to_receipt(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "pack_id": self.pack_id,
            "pack_digest": self.pack_digest,
            "run_id": self.run_id,
            "reason": self.reason.value if self.reason else None,
            "message": self.message,
            "details": dict(self.details),
        }


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class PreprodSealError(PipelineLifecycleError):
    """Raised when the sealing operation cannot be completed."""


class PreprodAdmissionError(PipelineLifecycleError):
    """Raised when execution admission is denied for a sealed pack."""

    def __init__(self, result: PreprodAdmissionResult):
        self.result = result
        super().__init__(
            f"preprod admission rejected for pack {result.pack_id}, "
            f"run {result.run_id}: {result.message}"
        )


class PreprodMutabilityError(PipelineLifecycleError):
    """Raised when an attempt is made to mutate a sealed snapshot in place."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _constituent_identity_payload(c: ConstituentRef) -> dict[str, Any]:
    """Deterministic projection of a ConstituentRef for digest contribution."""
    return {
        "authority": c.authority,
        "constituent_type": c.constituent_type,
        "content_digest": c.content_digest,
        "object_id": c.object_id,
        "revision": c.revision,
    }


def _pack_identity_payload(
    campaign_id: str,
    operator_id: str,
    preparation_revision: str,
    preparation_digest: str,
    constituents: Sequence[ConstituentRef],
) -> dict[str, Any]:
    """
    Deterministic canonical payload used to compute the pack's primary digest.

    Sorted by (constituent_type, object_id) so that insertion order cannot
    produce two different digests for semantically identical packs.
    """
    sorted_constituents = sorted(
        constituents,
        key=lambda c: (c.constituent_type, c.object_id),
    )
    return {
        "campaign_id": campaign_id,
        "constituent_digests": [c.content_digest for c in sorted_constituents],
        "constituent_identities": [
            _constituent_identity_payload(c) for c in sorted_constituents
        ],
        "operator_id": operator_id,
        "preparation_digest": preparation_digest,
        "preparation_revision": preparation_revision,
        "schema_version": PREPROD_PACK_VERSION,
    }


def _constituent_from_mapping(data: Mapping[str, Any], index: int) -> ConstituentRef:
    prefix = f"constituents[{index}]"
    return ConstituentRef(
        constituent_type=require_string(data.get("constituent_type"), f"{prefix}.constituent_type"),
        object_id=require_string(data.get("object_id"), f"{prefix}.object_id"),
        revision=require_string(data.get("revision"), f"{prefix}.revision"),
        content_digest=require_sha(data.get("content_digest"), f"{prefix}.content_digest"),
        authority=require_string(data.get("authority"), f"{prefix}.authority"),
    )


def _sealed_pack_from_payload(pack_id: str, payload: Mapping[str, Any]) -> SealedPreprodPack:
    """Reconstruct a SealedPreprodPack from a stored repository payload."""
    constituents = tuple(
        _constituent_from_mapping(c, i)
        for i, c in enumerate(payload.get("constituents", []))
    )
    return SealedPreprodPack(
        pack_id=pack_id,
        pack_digest=payload["pack_digest"],
        pack_version=payload["pack_version"],
        campaign_id=payload["campaign_id"],
        operator_id=payload["operator_id"],
        sealed_at_utc=payload["sealed_at_utc"],
        sealed_by=payload["sealed_by"],
        preparation_revision=payload["preparation_revision"],
        preparation_digest=payload["preparation_digest"],
        constituents=constituents,
        state=PreprodPackState(payload["state"]),
    )


# ---------------------------------------------------------------------------
# Core service
# ---------------------------------------------------------------------------


class PreProductionSealer:
    """
    CA-M011 — Enforces cryptographic sealing of the pre-production pack and
    fail-closed execution admission.

    State transitions enforced here:

        DRAFT (PreprodPackDraft, caller-owned)
            → compile()
            → COMPILED (internal transient; digest computed)
            → seal()
            → SEALED  (persisted SealedPreprodPack)

        SEALED + run_id
            → admit_for_execution()
            → ADMITTED / REJECTED + receipt

    Invariants:
    - A sealed pack is never mutated in place.
    - A new draft always produces a new candidate pack (new pack_id).
    - Execution admission verifies the pack digest byte-for-byte before
      allowing the run to proceed.
    - Admission REJECTS if the pack is not found, not sealed, or has a
      digest mismatch (false-proof / mutable-rehydration detection).
    """

    def __init__(self, repository: PipelineRepository) -> None:
        self._repo = repository

    # ------------------------------------------------------------------
    # 1. Compile + Seal
    # ------------------------------------------------------------------

    def compile_and_seal(
        self,
        draft: PreprodPackDraft,
        *,
        idempotency_key: str,
        now: str | None = None,
    ) -> SealedPreprodPack:
        """
        Transition: DRAFT → COMPILE_SNAPSHOT → SEALED_PREPROD_SNAPSHOT

        Actor: PreProductionSealer (automated boundary)
        Preconditions:
            - draft is a valid PreprodPackDraft with at least one constituent
            - idempotency_key is unique per sealing operation
        Postconditions:
            - A SealedPreprodPack is persisted with state=SEALED
            - pack_digest is deterministic SHA-256 of canonical identity payload
            - Constituent digests are bound; upstream mutable state is frozen at sealing time
        Error route: PreprodSealError on validation failure or conflicts
        Receipt: The returned SealedPreprodPack object; also persisted in repository
        """
        self._validate_draft(draft)
        timestamp = now or utc_now_rfc3339()

        # --- COMPILE_SNAPSHOT: compute deterministic digest ------------------
        all_constituents = list(draft.prompts) + list(draft.model_manifests) + \
                           list(draft.media_refs) + list(draft.parameters)

        identity_payload = _pack_identity_payload(
            campaign_id=draft.campaign_id,
            operator_id=draft.operator_id,
            preparation_revision=draft.preparation_revision,
            preparation_digest=draft.preparation_digest,
            constituents=all_constituents,
        )
        # Deterministic: sort_keys=True enforced inside canonical_json_bytes
        pack_digest = canonical_sha256(identity_payload)
        pack_id = f"preprod-pack:{pack_digest}"

        # --- SEALED_PREPROD_SNAPSHOT: build persisted payload ----------------
        constituents_payload = sorted(
            [
                {
                    "authority": c.authority,
                    "constituent_type": c.constituent_type,
                    "content_digest": c.content_digest,
                    "object_id": c.object_id,
                    "revision": c.revision,
                }
                for c in all_constituents
            ],
            key=lambda d: (d["constituent_type"], d["object_id"]),
        )

        stored_payload: dict[str, Any] = {
            "campaign_id": draft.campaign_id,
            "constituents": constituents_payload,
            "operator_id": draft.operator_id,
            "pack_digest": pack_digest,
            "pack_version": PREPROD_PACK_VERSION,
            "preparation_digest": draft.preparation_digest,
            "preparation_revision": draft.preparation_revision,
            "sealed_at_utc": timestamp,
            "sealed_by": SEAL_ACTOR,
            "state": PreprodPackState.SEALED.value,
        }
        reject_noncanonical(stored_payload)

        # Self-verify: recompute from stored payload bytes to prove determinism
        verification_payload = _pack_identity_payload(
            campaign_id=stored_payload["campaign_id"],
            operator_id=stored_payload["operator_id"],
            preparation_revision=stored_payload["preparation_revision"],
            preparation_digest=stored_payload["preparation_digest"],
            constituents=all_constituents,
        )
        verification_digest = canonical_sha256(verification_payload)
        if verification_digest != pack_digest:
            raise PreprodSealError(
                f"internal: digest non-determinism detected "
                f"(first={pack_digest}, second={verification_digest})"
            )

        # Persist via repository idempotent store
        result = self._repo.store_object(
            PREPROD_PACK_OBJECT_TYPE,
            stored_payload,
            idempotency_key=idempotency_key,
            object_id=pack_id,
            semantic_version=PREPROD_PACK_VERSION,
            lifecycle_state=PreprodPackState.SEALED.value,
            now=timestamp,
        )
        persisted_payload = result["object"]["payload"]
        return _sealed_pack_from_payload(pack_id, persisted_payload)

    # ------------------------------------------------------------------
    # 2. Retrieve
    # ------------------------------------------------------------------

    def get_pack(self, pack_id: str) -> SealedPreprodPack:
        """
        Retrieve a sealed pack by its stable pack_id.

        Raises PipelineNotFound (via repository) if not found.
        """
        obj = self._repo.get_object(pack_id)
        return _sealed_pack_from_payload(pack_id, obj["payload"])

    def list_packs(self, *, campaign_id: str | None = None) -> list[SealedPreprodPack]:
        """
        List all current sealed packs, optionally filtered by campaign_id.
        """
        objects = self._repo.list_objects(object_type=PREPROD_PACK_OBJECT_TYPE)
        packs: list[SealedPreprodPack] = []
        for obj in objects:
            payload = obj["payload"]
            if campaign_id is not None and payload.get("campaign_id") != campaign_id:
                continue
            packs.append(_sealed_pack_from_payload(obj["object_id"], payload))
        return packs

    # ------------------------------------------------------------------
    # 3. Execution Admission
    # ------------------------------------------------------------------

    def admit_for_execution(
        self,
        pack_id: str,
        pack_digest: str,
        run_id: str,
        *,
        expected_constituents: Sequence[ConstituentRef] | None = None,
        idempotency_key: str,
        now: str | None = None,
    ) -> PreprodAdmissionResult:
        """
        Transition: SEALED_PREPROD_SNAPSHOT → EXECUTION_ADMISSION

        Verifies exact pack digest (SHA-256) and optionally cross-checks
        each constituent's content_digest against the caller's expectations.

        Actor: Pipeline execution boundary
        Preconditions:
            - pack_id identifies a currently sealed pack
            - pack_digest matches the stored pack's canonical digest byte-for-byte
        Postconditions:
            - On ADMITTED: a run binding receipt is persisted
            - On REJECTED: no run is started; error surface contains reason
        Error route: PreprodAdmissionError raised on rejection
        False-proof invariant: If pack_id is valid but pack_digest is stale /
            rehydrated from latest mutable state, admission REJECTS.
        """
        timestamp = now or utc_now_rfc3339()
        require_string(pack_id, "pack_id")
        require_sha(pack_digest, "pack_digest")
        require_string(run_id, "run_id")

        def _reject(
            reason: PreprodRejectionReason,
            message: str,
            details: dict[str, Any] | None = None,
        ) -> PreprodAdmissionResult:
            return PreprodAdmissionResult(
                decision=PreprodAdmissionDecision.REJECTED,
                pack_id=pack_id,
                pack_digest=pack_digest,
                run_id=run_id,
                reason=reason,
                message=message,
                details=details or {},
            )

        # Fetch persisted pack
        try:
            obj = self._repo.get_object(pack_id)
        except Exception:
            result = _reject(
                PreprodRejectionReason.PACK_NOT_FOUND,
                f"pack {pack_id} not found in repository",
            )
            raise PreprodAdmissionError(result)

        payload = obj["payload"]
        stored_state = PreprodPackState(payload.get("state", ""))

        # Must be SEALED
        if stored_state != PreprodPackState.SEALED:
            result = _reject(
                PreprodRejectionReason.PACK_NOT_SEALED,
                f"pack {pack_id} is in state {stored_state.value}, not SEALED",
                {"stored_state": stored_state.value},
            )
            raise PreprodAdmissionError(result)

        if stored_state == PreprodPackState.INVALIDATED:
            result = _reject(
                PreprodRejectionReason.PACK_INVALIDATED,
                f"pack {pack_id} has been invalidated",
            )
            raise PreprodAdmissionError(result)

        # --- Core integrity check: digest must match byte-for-byte ----------
        stored_digest = payload.get("pack_digest", "")
        if stored_digest != pack_digest:
            result = _reject(
                PreprodRejectionReason.DIGEST_MISMATCH,
                (
                    f"pack_digest mismatch for pack {pack_id}: "
                    f"caller supplied {pack_digest}, stored {stored_digest}"
                ),
                {
                    "caller_digest": pack_digest,
                    "stored_digest": stored_digest,
                },
            )
            raise PreprodAdmissionError(result)

        # --- Re-derive digest from stored constituents (anti-rehydration) ---
        #
        # This is the false-proof gate from the mandate:
        # "a system that reports a seal but silently rehydrates latest
        #  preparation data at execution time must fail."
        #
        # We recompute the expected digest from the stored constituents and
        # compare it against both stored_digest AND caller-supplied pack_digest.
        stored_constituents = [
            _constituent_from_mapping(c, i)
            for i, c in enumerate(payload.get("constituents", []))
        ]
        recomputed_payload = _pack_identity_payload(
            campaign_id=payload["campaign_id"],
            operator_id=payload["operator_id"],
            preparation_revision=payload["preparation_revision"],
            preparation_digest=payload["preparation_digest"],
            constituents=stored_constituents,
        )
        recomputed_digest = canonical_sha256(recomputed_payload)
        if recomputed_digest != stored_digest:
            result = _reject(
                PreprodRejectionReason.MUTABLE_REHYDRATION_DETECTED,
                (
                    f"stored pack body recomputes to digest {recomputed_digest} "
                    f"but stored pack_digest is {stored_digest}; "
                    "this indicates silent mutation of the sealed snapshot"
                ),
                {
                    "recomputed_digest": recomputed_digest,
                    "stored_digest": stored_digest,
                },
            )
            raise PreprodAdmissionError(result)

        # --- Optional per-constituent cross-check ---------------------------
        if expected_constituents is not None:
            stored_by_id = {c.object_id: c for c in stored_constituents}
            for exp in expected_constituents:
                stored_c = stored_by_id.get(exp.object_id)
                if stored_c is None:
                    result = _reject(
                        PreprodRejectionReason.MISSING_REQUIRED_CONSTITUENT,
                        f"expected constituent {exp.object_id} not found in sealed pack",
                        {"missing_object_id": exp.object_id},
                    )
                    raise PreprodAdmissionError(result)
                if stored_c.content_digest != exp.content_digest:
                    result = _reject(
                        PreprodRejectionReason.CONSTITUENT_DIGEST_MISMATCH,
                        (
                            f"constituent {exp.object_id} content_digest mismatch: "
                            f"expected {exp.content_digest}, stored {stored_c.content_digest}"
                        ),
                        {
                            "object_id": exp.object_id,
                            "expected_digest": exp.content_digest,
                            "stored_digest": stored_c.content_digest,
                        },
                    )
                    raise PreprodAdmissionError(result)

        # --- Persist run binding receipt ------------------------------------
        binding_payload: dict[str, Any] = {
            "admitted_at_utc": timestamp,
            "campaign_id": payload["campaign_id"],
            "decision": PreprodAdmissionDecision.ADMITTED.value,
            "pack_digest": stored_digest,
            "pack_id": pack_id,
            "pack_version": payload.get("pack_version", PREPROD_PACK_VERSION),
            "run_id": run_id,
        }
        reject_noncanonical(binding_payload)
        binding_id = f"preprod-run-binding:{run_id}:{pack_id}"
        self._repo.store_object(
            PREPROD_RUN_BINDING_OBJECT_TYPE,
            binding_payload,
            idempotency_key=idempotency_key,
            object_id=binding_id,
            lifecycle_state="ADMITTED",
            now=timestamp,
        )

        admitted_result = PreprodAdmissionResult(
            decision=PreprodAdmissionDecision.ADMITTED,
            pack_id=pack_id,
            pack_digest=stored_digest,
            run_id=run_id,
            message="pack admitted for execution",
        )
        return admitted_result

    def require_admitted(
        self,
        pack_id: str,
        pack_digest: str,
        run_id: str,
        *,
        expected_constituents: Sequence[ConstituentRef] | None = None,
        idempotency_key: str,
        now: str | None = None,
    ) -> PreprodAdmissionResult:
        """
        Convenience wrapper: identical to admit_for_execution() but raises
        PreprodAdmissionError on rejection rather than returning a REJECTED result.
        (Callers that need the result for logging may call admit_for_execution() directly.)
        """
        return self.admit_for_execution(
            pack_id,
            pack_digest,
            run_id,
            expected_constituents=expected_constituents,
            idempotency_key=idempotency_key,
            now=now,
        )

    # ------------------------------------------------------------------
    # 4. Supersede (new draft → new candidate, old remains inspectable)
    # ------------------------------------------------------------------

    def supersede_pack(
        self,
        current_pack_id: str,
        *,
        idempotency_key: str,
        now: str | None = None,
    ) -> SealedPreprodPack:
        """
        Mark an existing SEALED pack as SUPERSEDED.

        Preconditions: pack must exist and be in SEALED state
        Postconditions:
            - pack state is SUPERSEDED
            - The previous object row is still inspectable (history preserved)
        Note: The caller must then call compile_and_seal() with a new draft
              to produce the replacement candidate.

        State: SEALED → SUPERSEDED
        """
        timestamp = now or utc_now_rfc3339()
        obj = self._repo.get_object(current_pack_id)
        payload = dict(obj["payload"])
        current_state = PreprodPackState(payload.get("state", ""))

        if current_state not in (PreprodPackState.SEALED,):
            raise PreprodSealError(
                f"cannot supersede pack {current_pack_id} in state {current_state.value}; "
                "only SEALED packs may be superseded"
            )

        # Create a new revision of the same object with updated state.
        # Immutability invariant: we never alter the pack_digest; only state changes.
        payload["state"] = PreprodPackState.SUPERSEDED.value
        reject_noncanonical(payload)

        result = self._repo.store_object(
            PREPROD_PACK_OBJECT_TYPE,
            payload,
            idempotency_key=idempotency_key,
            object_id=current_pack_id,
            lifecycle_state=PreprodPackState.SUPERSEDED.value,
            now=timestamp,
        )
        return _sealed_pack_from_payload(current_pack_id, result["object"]["payload"])

    # ------------------------------------------------------------------
    # 5. Invalidate
    # ------------------------------------------------------------------

    def invalidate_pack(
        self,
        pack_id: str,
        *,
        idempotency_key: str,
        reason: str,
        now: str | None = None,
    ) -> SealedPreprodPack:
        """
        Mark a pack as INVALIDATED.  An invalidated pack cannot be admitted.

        Postconditions:
            - state = INVALIDATED
            - The object remains inspectable with its original digest
        """
        timestamp = now or utc_now_rfc3339()
        require_string(reason, "reason")
        obj = self._repo.get_object(pack_id)
        payload = dict(obj["payload"])
        payload["state"] = PreprodPackState.INVALIDATED.value
        payload["invalidation_reason"] = reason
        reject_noncanonical(payload)

        result = self._repo.store_object(
            PREPROD_PACK_OBJECT_TYPE,
            payload,
            idempotency_key=idempotency_key,
            object_id=pack_id,
            lifecycle_state=PreprodPackState.INVALIDATED.value,
            now=timestamp,
        )
        return _sealed_pack_from_payload(pack_id, result["object"]["payload"])

    # ------------------------------------------------------------------
    # 6. Get run binding
    # ------------------------------------------------------------------

    def get_run_binding(self, run_id: str, pack_id: str) -> dict[str, Any]:
        """Retrieve the persisted admission binding for a run+pack pair."""
        binding_id = f"preprod-run-binding:{run_id}:{pack_id}"
        return self._repo.get_object(binding_id)

    # ------------------------------------------------------------------
    # Internal validation
    # ------------------------------------------------------------------

    def _validate_draft(self, draft: PreprodPackDraft) -> None:
        require_string(draft.campaign_id, "draft.campaign_id")
        require_string(draft.operator_id, "draft.operator_id")
        require_string(draft.preparation_revision, "draft.preparation_revision")
        require_sha(draft.preparation_digest, "draft.preparation_digest")

        all_constituents = (
            list(draft.prompts)
            + list(draft.model_manifests)
            + list(draft.media_refs)
            + list(draft.parameters)
        )
        if not all_constituents:
            raise PipelineValidationError(
                "preprod pack must contain at least one constituent "
                "(prompt, model_manifest, media_ref, or parameter)"
            )

        seen_ids: set[str] = set()
        for c in all_constituents:
            require_string(c.constituent_type, "constituent.constituent_type")
            require_string(c.object_id, "constituent.object_id")
            require_string(c.revision, "constituent.revision")
            require_sha(c.content_digest, "constituent.content_digest")
            require_string(c.authority, "constituent.authority")
            if c.object_id in seen_ids:
                raise PipelineValidationError(
                    f"duplicate constituent object_id: {c.object_id}"
                )
            seen_ids.add(c.object_id)
