"""Guest Genesis and Protected/Derived Semantic Territory Program for Conscious Activation Engine (CAE).

Governed by Phase 3 Mandate M27 (TS-AIR-007, F30, §1.3a).
Orchestrates the lifecycle of Guest Genesis, Voice/Visual DNA synthesis, 5-layer RSCS distillation,
and protected vs centroid semantic territory ratification with strict cryptographic lineage and anti-centroid integrity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339

logger = logging.getLogger("ca_runtime.guest_genesis_program")

CANONICAL_AUTHORITY_LANES: Set[str] = {"HUNTER", "ANALYST", "COMPOSER", "COMMANDER"}


# ============================================================================
# 1. Error Taxonomy
# ============================================================================

class GuestGenesisProgramError(RuntimeError):
    """Base exception for all Guest Genesis and Semantic Territory program operations."""

    def __init__(self, message: str, *, reason_code: str = "GUEST_GENESIS_PROGRAM_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class InvalidStateTransitionError(GuestGenesisProgramError):
    """Raised when an illegal lifecycle transition is attempted."""

    def __init__(self, current_state: str, target_state: str, allowed_transitions: Sequence[str]):
        super().__init__(
            f"Illegal state transition from '{current_state}' to '{target_state}'. Allowed targets: {list(allowed_transitions)}",
            reason_code="INVALID_STATE_TRANSITION",
            details={"current_state": current_state, "target_state": target_state, "allowed_transitions": list(allowed_transitions)},
        )


class AuthorityLaneViolationError(GuestGenesisProgramError):
    """Raised when an operation is executed outside its permitted Authority Lane."""

    def __init__(self, required_lane: str, actual_lane: str, operation_name: str):
        super().__init__(
            f"Operation '{operation_name}' requires Authority Lane '{required_lane}', but was invoked by '{actual_lane}'",
            reason_code="AUTHORITY_LANE_VIOLATION",
            details={"required_lane": required_lane, "actual_lane": actual_lane, "operation_name": operation_name},
        )


class ProtectedSourceMutationError(GuestGenesisProgramError):
    """Raised when an attempt is made to silently mutate or overwrite protected guest evidence."""

    def __init__(self, message: str, *, evidence_id: str):
        super().__init__(
            message,
            reason_code="PROTECTED_SOURCE_MUTATION_ERROR",
            details={"evidence_id": evidence_id},
        )


class LineageIntegrityError(GuestGenesisProgramError):
    """Raised when derived artifacts lack valid cryptographic SHA-256 evidence lineage."""

    def __init__(self, message: str, *, missing_or_invalid_hashes: Sequence[str]):
        super().__init__(
            message,
            reason_code="LINEAGE_INTEGRITY_ERROR",
            details={"missing_or_invalid_hashes": list(missing_or_invalid_hashes)},
        )


class AntiCentroidViolationError(GuestGenesisProgramError):
    """Raised when candidate material contains prohibited generic centroid patterns."""

    def __init__(self, message: str, *, violations: Sequence[str]):
        super().__init__(
            message,
            reason_code="ANTI_CENTROID_VIOLATION",
            details={"violations": list(violations)},
        )


# ============================================================================
# 2. State Enum & Data Models
# ============================================================================

class GuestGenesisState(str, Enum):
    INITIAL = "INITIAL"
    EVIDENCE_INDEXED = "EVIDENCE_INDEXED"
    BRAND_CONTEXT_DERIVED = "BRAND_CONTEXT_DERIVED"
    VOICE_VISUAL_SYNTHESIZED = "VOICE_VISUAL_SYNTHESIZED"
    DISTILLATION_VERIFIED = "DISTILLATION_VERIFIED"
    TERRITORY_RATIFIED = "TERRITORY_RATIFIED"
    REPAIRING = "REPAIRING"


@dataclass(frozen=True, slots=True)
class ProtectedGuestEvidence:
    """Authenticated, immutable source evidence for a Guest participant."""
    evidence_id: str
    source_url: str
    content_type: str
    sha256_digest: str
    transcript_spans: Tuple[str, ...]
    captured_at: str = field(default_factory=utc_now_rfc3339)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.evidence_id or not self.evidence_id.strip():
            raise GuestGenesisProgramError("evidence_id cannot be empty")
        if not self.sha256_digest or len(self.sha256_digest) != 64:
            raise GuestGenesisProgramError(
                f"Invalid sha256_digest for evidence '{self.evidence_id}': must be 64-char hex string"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "source_url": self.source_url,
            "content_type": self.content_type,
            "sha256_digest": self.sha256_digest,
            "transcript_spans": list(self.transcript_spans),
            "captured_at": self.captured_at,
            "metadata": self.metadata,
        }


@dataclass(frozen=True, slots=True)
class DerivedVoiceVisualDNA:
    """Subordinate Voice & Visual DNA expressions with cryptographic evidence lineage."""
    voice_dna_id: str
    visual_dna_id: str
    brand_context_ref: Dict[str, str]
    vocabulary_patterns: Tuple[str, ...]
    rhythm_patterns: Tuple[str, ...]
    stance_patterns: Tuple[str, ...]
    prohibited_centroid_patterns: Tuple[str, ...]
    prohibited_centroid_defaults: Tuple[str, ...]
    source_evidence_hashes: Tuple[str, ...]
    lineage_sha256: str
    derived_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "voice_dna_id": self.voice_dna_id,
            "visual_dna_id": self.visual_dna_id,
            "brand_context_ref": self.brand_context_ref,
            "vocabulary_patterns": list(self.vocabulary_patterns),
            "rhythm_patterns": list(self.rhythm_patterns),
            "stance_patterns": list(self.stance_patterns),
            "prohibited_centroid_patterns": list(self.prohibited_centroid_patterns),
            "prohibited_centroid_defaults": list(self.prohibited_centroid_defaults),
            "source_evidence_hashes": list(self.source_evidence_hashes),
            "lineage_sha256": self.lineage_sha256,
            "derived_at": self.derived_at,
        }


@dataclass(frozen=True, slots=True)
class SemanticTerritoryDescriptor:
    """Ratified Protected vs Centroid Semantic Territory."""
    territory_id: str
    protected_territory: Dict[str, List[str]]
    centroid_territory: Dict[str, List[str]]
    wrong_reading_locks: Tuple[str, ...]
    lineage_sha256: str
    ratified_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "territory_id": self.territory_id,
            "protected_territory": self.protected_territory,
            "centroid_territory": self.centroid_territory,
            "wrong_reading_locks": list(self.wrong_reading_locks),
            "lineage_sha256": self.lineage_sha256,
            "ratified_at": self.ratified_at,
        }


# ============================================================================
# 3. Guest Genesis Program Coordinator
# ============================================================================

class GuestGenesisProgramCoordinator:
    """Coordinator for Guest Genesis and Protected/Derived Semantic Territory Program.

    Governs the lifecycle:
      INITIAL -> EVIDENCE_INDEXED -> BRAND_CONTEXT_DERIVED -> VOICE_VISUAL_SYNTHESIZED
      -> DISTILLATION_VERIFIED -> TERRITORY_RATIFIED (with REPAIRING recovery route).

    Enforces:
    - Protected Guest evidence source immutability.
    - Cryptographic SHA-256 lineage chaining on all derived expressions.
    - Anti-centroid and wrong-reading locks validation.
    - Four Authority Lanes separation (HUNTER, ANALYST, COMPOSER, COMMANDER).
    - Deterministic CAE transition receipts on every state mutation.
    """

    ALLOWED_TRANSITIONS: Dict[GuestGenesisState, Set[GuestGenesisState]] = {
        GuestGenesisState.INITIAL: {GuestGenesisState.EVIDENCE_INDEXED, GuestGenesisState.REPAIRING},
        GuestGenesisState.EVIDENCE_INDEXED: {GuestGenesisState.BRAND_CONTEXT_DERIVED, GuestGenesisState.REPAIRING},
        GuestGenesisState.BRAND_CONTEXT_DERIVED: {GuestGenesisState.VOICE_VISUAL_SYNTHESIZED, GuestGenesisState.REPAIRING},
        GuestGenesisState.VOICE_VISUAL_SYNTHESIZED: {GuestGenesisState.DISTILLATION_VERIFIED, GuestGenesisState.REPAIRING},
        GuestGenesisState.DISTILLATION_VERIFIED: {GuestGenesisState.TERRITORY_RATIFIED, GuestGenesisState.REPAIRING},
        GuestGenesisState.TERRITORY_RATIFIED: {GuestGenesisState.REPAIRING},
        GuestGenesisState.REPAIRING: {
            GuestGenesisState.INITIAL,
            GuestGenesisState.EVIDENCE_INDEXED,
            GuestGenesisState.BRAND_CONTEXT_DERIVED,
            GuestGenesisState.VOICE_VISUAL_SYNTHESIZED,
            GuestGenesisState.DISTILLATION_VERIFIED,
            GuestGenesisState.TERRITORY_RATIFIED,
        },
    }

    def __init__(self, *, program_id: str, workspace_id: str, guest_id: str):
        self._program_id = program_id
        self._workspace_id = workspace_id
        self._guest_id = guest_id
        self._state = GuestGenesisState.INITIAL
        self._version = 1

        self._protected_evidence: Dict[str, ProtectedGuestEvidence] = {}
        self._brand_context: Optional[Dict[str, Any]] = None
        self._voice_visual_dna: Optional[DerivedVoiceVisualDNA] = None
        self._distillation_receipts: List[Dict[str, Any]] = []
        self._semantic_territory: Optional[SemanticTerritoryDescriptor] = None

        self._receipt_history: List[Dict[str, Any]] = []
        self._state_hash = self._compute_state_hash()

    @property
    def program_id(self) -> str:
        return self._program_id

    @property
    def workspace_id(self) -> str:
        return self._workspace_id

    @property
    def guest_id(self) -> str:
        return self._guest_id

    @property
    def current_state(self) -> GuestGenesisState:
        return self._state

    @property
    def version(self) -> int:
        return self._version

    @property
    def state_hash(self) -> str:
        return self._state_hash

    @property
    def protected_evidence_count(self) -> int:
        return len(self._protected_evidence)

    @property
    def brand_context(self) -> Optional[Dict[str, Any]]:
        return self._brand_context

    @property
    def voice_visual_dna(self) -> Optional[DerivedVoiceVisualDNA]:
        return self._voice_visual_dna

    @property
    def distillation_receipts(self) -> List[Dict[str, Any]]:
        return list(self._distillation_receipts)

    @property
    def semantic_territory(self) -> Optional[SemanticTerritoryDescriptor]:
        return self._semantic_territory

    @property
    def receipt_history(self) -> List[Dict[str, Any]]:
        return list(self._receipt_history)

    def _verify_lane(self, actual_lane: str, required_lane: str, operation_name: str) -> None:
        if actual_lane not in CANONICAL_AUTHORITY_LANES:
            raise AuthorityLaneViolationError(required_lane, actual_lane, operation_name)
        if actual_lane != required_lane:
            raise AuthorityLaneViolationError(required_lane, actual_lane, operation_name)

    def _compute_state_hash(self) -> str:
        snapshot = {
            "program_id": self._program_id,
            "workspace_id": self._workspace_id,
            "guest_id": self._guest_id,
            "state": self._state.value,
            "version": self._version,
            "evidence_hashes": sorted(e.sha256_digest for e in self._protected_evidence.values()),
            "brand_context_id": self._brand_context.get("brand_context_id") if self._brand_context else None,
            "voice_dna_id": self._voice_visual_dna.voice_dna_id if self._voice_visual_dna else None,
            "territory_id": self._semantic_territory.territory_id if self._semantic_territory else None,
        }
        return canonical_sha256(snapshot)

    def _transition(self, target_state: GuestGenesisState, *, operation_name: str, actor_lane: str, payload_summary: Dict[str, Any]) -> Dict[str, Any]:
        allowed = self.ALLOWED_TRANSITIONS.get(self._state, set())
        if target_state not in allowed:
            raise InvalidStateTransitionError(self._state.value, target_state.value, sorted(s.value for s in allowed))

        prior_state = self._state
        prior_hash = self._state_hash
        self._state = target_state
        self._version += 1
        self._state_hash = self._compute_state_hash()

        receipt = {
            "receipt_id": f"rcpt:gg:{self._program_id}:{self._version}",
            "program_id": self._program_id,
            "workspace_id": self._workspace_id,
            "guest_id": self._guest_id,
            "operation": operation_name,
            "actor_lane": actor_lane,
            "prior_state": prior_state.value,
            "target_state": target_state.value,
            "prior_hash": prior_hash,
            "target_hash": self._state_hash,
            "version": self._version,
            "payload_summary": payload_summary,
            "timestamp": utc_now_rfc3339(),
        }
        self._receipt_history.append(receipt)
        logger.info("Transitioned to %s (version: %d, op: %s)", target_state.value, self._version, operation_name)
        return receipt

    # ------------------------------------------------------------------------
    # State Operations
    # ------------------------------------------------------------------------

    def index_protected_evidence(
        self,
        *,
        evidence_items: Sequence[ProtectedGuestEvidence],
        actor_lane: str = "HUNTER",
    ) -> Dict[str, Any]:
        """Indexes authenticated Guest source evidence under HUNTER lane authority."""
        self._verify_lane(actor_lane, "HUNTER", "cae.guest_genesis.index_evidence@1.0.0")
        if not evidence_items:
            raise GuestGenesisProgramError("Must provide at least one evidence item to index")

        for item in evidence_items:
            # Check for silent mutation of already indexed evidence with different content
            if item.evidence_id in self._protected_evidence:
                existing = self._protected_evidence[item.evidence_id]
                if existing.sha256_digest != item.sha256_digest:
                    raise ProtectedSourceMutationError(
                        f"Cannot overwrite protected evidence '{item.evidence_id}' with modified SHA-256 digest",
                        evidence_id=item.evidence_id,
                    )
            self._protected_evidence[item.evidence_id] = item

        return self._transition(
            GuestGenesisState.EVIDENCE_INDEXED,
            operation_name="cae.guest_genesis.index_evidence@1.0.0",
            actor_lane=actor_lane,
            payload_summary={"evidence_count": len(self._protected_evidence)},
        )

    def derive_brand_context(
        self,
        *,
        brand_context_id: str,
        identity_truths: Sequence[str],
        audience_relationship: str,
        positioning_tension: str,
        source_evidence_ids: Sequence[str],
        actor_lane: str = "ANALYST",
    ) -> Dict[str, Any]:
        """Derives subordinate Brand Context from protected evidence under ANALYST authority."""
        self._verify_lane(actor_lane, "ANALYST", "cae.guest_genesis.derive_brand_context@1.0.0")

        # Verify evidence references
        missing_ids = [eid for eid in source_evidence_ids if eid not in self._protected_evidence]
        if missing_ids:
            raise LineageIntegrityError(
                f"Cannot derive Brand Context: source evidence IDs not found in protected evidence: {missing_ids}",
                missing_or_invalid_hashes=missing_ids,
            )

        evidence_hashes = [self._protected_evidence[eid].sha256_digest for eid in source_evidence_ids]
        lineage_hash = canonical_sha256({"evidence_hashes": sorted(evidence_hashes)})

        self._brand_context = {
            "brand_context_id": brand_context_id,
            "guest_id": self._guest_id,
            "workspace_id": self._workspace_id,
            "identity_truths": list(identity_truths),
            "audience_relationship": audience_relationship,
            "positioning_tension": positioning_tension,
            "source_evidence_ids": list(source_evidence_ids),
            "source_evidence_hashes": evidence_hashes,
            "lineage_sha256": lineage_hash,
            "derived_at": utc_now_rfc3339(),
        }

        return self._transition(
            GuestGenesisState.BRAND_CONTEXT_DERIVED,
            operation_name="cae.guest_genesis.derive_brand_context@1.0.0",
            actor_lane=actor_lane,
            payload_summary={"brand_context_id": brand_context_id, "lineage_sha256": lineage_hash},
        )

    def synthesize_voice_visual_dna(
        self,
        *,
        voice_dna_id: str,
        visual_dna_id: str,
        vocabulary_patterns: Sequence[str],
        rhythm_patterns: Sequence[str],
        stance_patterns: Sequence[str],
        prohibited_centroid_patterns: Sequence[str],
        prohibited_centroid_defaults: Sequence[str],
        source_evidence_ids: Sequence[str],
        actor_lane: str = "COMPOSER",
    ) -> Dict[str, Any]:
        """Synthesizes Voice and Visual DNA with anti-centroid enforcement under COMPOSER authority."""
        self._verify_lane(actor_lane, "COMPOSER", "cae.guest_genesis.synthesize_dna@1.0.0")
        if self._brand_context is None:
            raise GuestGenesisProgramError("Cannot synthesize DNA without derived brand context")

        # Verify anti-centroid integrity
        lowered_prohibited = [p.lower().strip() for p in prohibited_centroid_patterns if p.strip()]
        violations: List[str] = []
        for word in vocabulary_patterns:
            for pat in lowered_prohibited:
                if pat in word.lower():
                    violations.append(f"Vocabulary '{word}' contains prohibited centroid pattern '{pat}'")

        if violations:
            raise AntiCentroidViolationError(
                f"Candidate Voice DNA collapsed into generic centroid platitudes: {violations}",
                violations=violations,
            )

        # Verify evidence lineage
        missing_ids = [eid for eid in source_evidence_ids if eid not in self._protected_evidence]
        if missing_ids:
            raise LineageIntegrityError(
                f"DNA synthesis references missing protected evidence: {missing_ids}",
                missing_or_invalid_hashes=missing_ids,
            )

        evidence_hashes = tuple(self._protected_evidence[eid].sha256_digest for eid in source_evidence_ids)
        combined_lineage = canonical_sha256(
            {"brand_lineage": self._brand_context["lineage_sha256"], "evidence_hashes": sorted(evidence_hashes)}
        )

        self._voice_visual_dna = DerivedVoiceVisualDNA(
            voice_dna_id=voice_dna_id,
            visual_dna_id=visual_dna_id,
            brand_context_ref={"object_id": self._brand_context["brand_context_id"], "version": "1.0.0", "sha256": self._brand_context["lineage_sha256"]},
            vocabulary_patterns=tuple(vocabulary_patterns),
            rhythm_patterns=tuple(rhythm_patterns),
            stance_patterns=tuple(stance_patterns),
            prohibited_centroid_patterns=tuple(prohibited_centroid_patterns),
            prohibited_centroid_defaults=tuple(prohibited_centroid_defaults),
            source_evidence_hashes=evidence_hashes,
            lineage_sha256=combined_lineage,
            derived_at=utc_now_rfc3339(),
        )

        return self._transition(
            GuestGenesisState.VOICE_VISUAL_SYNTHESIZED,
            operation_name="cae.guest_genesis.synthesize_dna@1.0.0",
            actor_lane=actor_lane,
            payload_summary={"voice_dna_id": voice_dna_id, "visual_dna_id": visual_dna_id, "lineage_sha256": combined_lineage},
        )

    def verify_distillation_layers(
        self,
        *,
        receipts: Sequence[Dict[str, Any]],
        actor_lane: str = "ANALYST",
    ) -> Dict[str, Any]:
        """Verifies 5-layer RSCS distillation receipts under ANALYST authority."""
        self._verify_lane(actor_lane, "ANALYST", "cae.guest_genesis.verify_distillation@1.0.0")

        expected_layers = {"saturation", "collision", "compression", "evaluation", "recursion"}
        observed_layers = {r.get("layer") for r in receipts}

        if not expected_layers.issubset(observed_layers):
            missing = expected_layers - observed_layers
            raise GuestGenesisProgramError(f"Distillation verification incomplete: missing RSCS layers: {missing}")

        for r in receipts:
            layer = r.get("layer")
            if layer in {"compression", "evaluation", "recursion"}:
                if not r.get("edge_product_preserved"):
                    raise GuestGenesisProgramError(f"RSCS layer '{layer}' failed: edge_product_preserved must be true")
                if not r.get("role_tension_preserved"):
                    raise GuestGenesisProgramError(f"RSCS layer '{layer}' failed: role_tension_preserved must be true")

        self._distillation_receipts = list(receipts)

        return self._transition(
            GuestGenesisState.DISTILLATION_VERIFIED,
            operation_name="cae.guest_genesis.verify_distillation@1.0.0",
            actor_lane=actor_lane,
            payload_summary={"receipt_count": len(receipts), "layers_verified": sorted(list(observed_layers))},
        )

    def ratify_semantic_territory(
        self,
        *,
        territory_id: str,
        wrong_reading_locks: Sequence[str],
        actor_lane: str = "COMMANDER",
    ) -> Dict[str, Any]:
        """Ratifies protected vs centroid semantic territory under COMMANDER authority."""
        self._verify_lane(actor_lane, "COMMANDER", "cae.guest_genesis.ratify_territory@1.0.0")
        if self._voice_visual_dna is None or self._brand_context is None:
            raise GuestGenesisProgramError("Cannot ratify territory without synthesized DNA and brand context")

        protected_territory = {
            "core_identity_truths": self._brand_context.get("identity_truths", []),
            "voice_stance": list(self._voice_visual_dna.stance_patterns),
            "vocabulary_boundaries": list(self._voice_visual_dna.vocabulary_patterns),
        }
        centroid_territory = {
            "prohibited_centroid_patterns": list(self._voice_visual_dna.prohibited_centroid_patterns),
            "prohibited_centroid_defaults": list(self._voice_visual_dna.prohibited_centroid_defaults),
        }

        territory_lineage = canonical_sha256(
            {"voice_lineage": self._voice_visual_dna.lineage_sha256, "wrong_reading_locks": sorted(wrong_reading_locks)}
        )

        self._semantic_territory = SemanticTerritoryDescriptor(
            territory_id=territory_id,
            protected_territory=protected_territory,
            centroid_territory=centroid_territory,
            wrong_reading_locks=tuple(wrong_reading_locks),
            lineage_sha256=territory_lineage,
            ratified_at=utc_now_rfc3339(),
        )

        return self._transition(
            GuestGenesisState.TERRITORY_RATIFIED,
            operation_name="cae.guest_genesis.ratify_territory@1.0.0",
            actor_lane=actor_lane,
            payload_summary={"territory_id": territory_id, "lineage_sha256": territory_lineage},
        )

    def fault_to_repairing(self, *, reason: str, actor_lane: str = "COMMANDER") -> Dict[str, Any]:
        """Routes program into REPAIRING state under COMMANDER authority upon detecting anomalies."""
        self._verify_lane(actor_lane, "COMMANDER", "cae.guest_genesis.fault_to_repair@1.0.0")
        return self._transition(
            GuestGenesisState.REPAIRING,
            operation_name="cae.guest_genesis.fault_to_repair@1.0.0",
            actor_lane=actor_lane,
            payload_summary={"reason": reason},
        )

    def resume_from_repair(self, *, target_state: GuestGenesisState, reason: str, actor_lane: str = "COMMANDER") -> Dict[str, Any]:
        """Recovers and resumes program from REPAIRING state to a valid target state."""
        self._verify_lane(actor_lane, "COMMANDER", "cae.guest_genesis.resume_from_repair@1.0.0")
        if self._state != GuestGenesisState.REPAIRING:
            raise GuestGenesisProgramError(f"Cannot resume from repair: current state is '{self._state.value}', not 'REPAIRING'")

        return self._transition(
            target_state,
            operation_name="cae.guest_genesis.resume_from_repair@1.0.0",
            actor_lane=actor_lane,
            payload_summary={"reason": reason, "resumed_state": target_state.value},
        )
