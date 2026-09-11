"""Research Source Ingestion + Identity Program Coordinator.

Governed by:
- Phase 3 Mandate M28 (03_PHASE_3_INTELLIGENCE_AND_PROGRAMS/M28_research_source_ingestion_identity.md)
- 00_CONTROL/20_PHASE3_CANONICALIZATION_MODEL.md
- 00_CONTROL/21_PHASE3_KNOWLEDGE_RUNTIME_CONTRACT.md
- 00_CONTROL/22_PHASE3_RESEARCH_RETRIEVAL_MATRIX.md
- 00_CONTROL/24_PHASE3_PROGRAM_STATE_HOOKS_MATRIX.md
- Object Constitution CA-CAN-01B_EVIDENCE_SOURCE.yaml
- Live PostgreSQL/RLS Tenancy Authority (TS-CAE-TEN-001)

Operating Model:
- Immutable Research Sources: Protected source-bearing records cannot be silently rewritten.
- Stable Canonical Identity: Stable deterministic identity derived from workspace and source origin.
- Idempotency & De-duplication: Re-ingesting identical content yields an idempotent replay receipt
  without creating duplicate canonical identities.
- Versioned Re-ingestion: Re-ingesting modified content produces an incremented version (v2, v3...)
  with cryptographic lineage (supersedes_source_id and ancestor_version_hashes) leaving the prior
  version record untouched.
- Four Authority Lanes:
  - HUNTER: Source discovery and raw observation ingestion.
  - ANALYST: Source verification, anti-inflation gating, and provenance validation.
  - COMPOSER: Immutable ResearchSourceRecord packaging.
  - COMMANDER: Operator gating, source activation, quarantine, and repair.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateAggregateNotFoundError,
    ProgramStateLifecycle,
    ProgramStateMachineDefinition,
    ProgramStateRuntimeError,
    ProgramStateVersionConflictError,
    ProgramTransitionContract,
    ProgramTransitionResult,
    SideEffectClass,
    UniversalProgramStateRuntime,
    _compute_state_hash,
)
from ca_runtime.state_lifecycle import (
    CausalTraceLedger,
    StateLifecycleCoordinator,
)
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    TenantContext,
    TenancyError,
    TenancyViolationError,
    require_current_tenant_context,
)
from cae_world_intelligence.domain import (
    ProvenanceRecord,
    RawObservation,
    ResearchSignal,
    SourceMultiplicity,
)
from cae_world_intelligence.errors import (
    DuplicateSourceInflationError,
    EvidenceError,
    ProvenanceError,
    StaleObservationError,
)
from cae_world_intelligence.normalization import SignalNormalizer
from cae_world_intelligence.verifier import ResearchSignalVerifier

logger = logging.getLogger("ca_runtime.research_source_program")

PROGRAM_ID = "research_source_ingestion_program"
PROGRAM_VERSION = "1.0.0"


# ============================================================================
# 1. Typed Error Hierarchy
# ============================================================================

class ResearchSourceProgramError(ProgramStateRuntimeError):
    """Base exception for Research Source Program execution."""
    pass


class SourceProvenanceIntegrityError(ResearchSourceProgramError):
    """Raised when source provenance fails validation or cryptographic verification."""

    def __init__(self, message: str, *, source_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            reason_code="PROVENANCE_INTEGRITY_ERROR",
            details={"source_id": source_id, **(details or {})},
        )
        self.source_id = source_id


class SourceHashMismatchError(ResearchSourceProgramError):
    """Raised when raw content excerpt does not match declared SHA-256 hash."""

    def __init__(self, message: str, *, expected_hash: str, actual_hash: str):
        super().__init__(
            message,
            reason_code="SOURCE_HASH_MISMATCH",
            details={"expected_hash": expected_hash, "actual_hash": actual_hash},
        )
        self.expected_hash = expected_hash
        self.actual_hash = actual_hash


class DuplicateSourceInflationViolationError(ResearchSourceProgramError):
    """Raised when syndicated duplicates artificially inflate independent source counts."""

    def __init__(self, message: str, *, multiplicity: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            reason_code="DUPLICATE_SOURCE_INFLATION",
            details={"multiplicity": multiplicity or {}},
        )
        self.multiplicity = multiplicity


class SourceImmutabilityViolationError(ResearchSourceProgramError):
    """Raised when an attempt is made to silently mutate a protected source record in-place."""

    def __init__(self, message: str, *, source_id: str):
        super().__init__(
            message,
            reason_code="SOURCE_IMMUTABILITY_VIOLATION",
            details={"source_id": source_id},
        )
        self.source_id = source_id


class InvalidSourceReingestionError(ResearchSourceProgramError):
    """Raised when re-ingestion parameters violate lineage or version constraints."""

    def __init__(self, message: str, *, source_id: str, reason: str):
        super().__init__(
            message,
            reason_code="INVALID_SOURCE_REINGESTION",
            details={"source_id": source_id, "reason": reason},
        )
        self.source_id = source_id


# ============================================================================
# 2. Immutable Domain Models
# ============================================================================

@dataclass(frozen=True, slots=True)
class ResearchSourceRecord:
    """Immutable, versioned research source record with stable identity and provenance."""
    source_id: str
    workspace_id: str
    source_type: str
    origin_url: str
    root_domain: str
    platform: str
    content_sha256: str
    raw_content_excerpt: str
    author_outlet: Optional[str]
    rights_metadata: Dict[str, Any]
    version: int
    supersedes_source_id: Optional[str]
    ancestor_version_hashes: Tuple[str, ...]
    provenance_record: Dict[str, Any]
    source_multiplicity: Dict[str, Any]
    admitted_at: str
    verified_at: Optional[str]
    status: str
    receipt_sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "workspace_id": self.workspace_id,
            "source_type": self.source_type,
            "origin_url": self.origin_url,
            "root_domain": self.root_domain,
            "platform": self.platform,
            "content_sha256": self.content_sha256,
            "raw_content_excerpt": self.raw_content_excerpt,
            "author_outlet": self.author_outlet,
            "rights_metadata": self.rights_metadata,
            "version": self.version,
            "supersedes_source_id": self.supersedes_source_id,
            "ancestor_version_hashes": list(self.ancestor_version_hashes),
            "provenance_record": self.provenance_record,
            "source_multiplicity": self.source_multiplicity,
            "admitted_at": self.admitted_at,
            "verified_at": self.verified_at,
            "status": self.status,
            "receipt_sha256": self.receipt_sha256,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ResearchSourceRecord:
        return cls(
            source_id=data["source_id"],
            workspace_id=data["workspace_id"],
            source_type=data["source_type"],
            origin_url=data["origin_url"],
            root_domain=data["root_domain"],
            platform=data["platform"],
            content_sha256=data["content_sha256"],
            raw_content_excerpt=data["raw_content_excerpt"],
            author_outlet=data.get("author_outlet"),
            rights_metadata=dict(data.get("rights_metadata", {})),
            version=int(data.get("version", 1)),
            supersedes_source_id=data.get("supersedes_source_id"),
            ancestor_version_hashes=tuple(data.get("ancestor_version_hashes", ())),
            provenance_record=dict(data.get("provenance_record", {})),
            source_multiplicity=dict(data.get("source_multiplicity", {})),
            admitted_at=data["admitted_at"],
            verified_at=data.get("verified_at"),
            status=data.get("status", "ADMITTED"),
            receipt_sha256=data.get("receipt_sha256", ""),
        )


@dataclass(frozen=True, slots=True)
class ResearchSourceSnapshot:
    """Operator-facing snapshot of active Research Source Ingestion Program."""
    aggregate_id: str
    workspace_id: str
    current_state: str
    active_source_id: Optional[str]
    active_source_version: int
    origin_url: Optional[str]
    content_sha256: Optional[str]
    root_domain: Optional[str]
    status: str
    total_versions: int
    version: int
    state_hash: str
    last_receipt_id: Optional[str]


# ============================================================================
# 3. Canonical State Machine Definition
# ============================================================================

def get_canonical_research_source_state_machine() -> ProgramStateMachineDefinition:
    """State machine for research_source_ingestion_program (Mandate M28)."""
    transitions = {
        "admit_source": ProgramTransitionContract(
            from_state="INITIAL",
            to_state="SOURCE_ADMITTED",
            transition_name="admit_source",
            trigger_operation="cae.research_source.admit@1.0.0",
            required_lane=AuthorityLane.HUNTER,
            preconditions=("workspace_active", "source_origin_valid"),
            side_effect_class=SideEffectClass.LOCAL_STATE_WRITE,
        ),
        "verify_source": ProgramTransitionContract(
            from_state="SOURCE_ADMITTED",
            to_state="SOURCE_VERIFIED",
            transition_name="verify_source",
            trigger_operation="cae.research_source.verify@1.0.0",
            required_lane=AuthorityLane.ANALYST,
            preconditions=("workspace_active", "provenance_hash_verified", "multiplicity_checked"),
            side_effect_class=SideEffectClass.LOCAL_STATE_WRITE,
        ),
        "register_source": ProgramTransitionContract(
            from_state="SOURCE_VERIFIED",
            to_state="SOURCE_REGISTERED",
            transition_name="register_source",
            trigger_operation="cae.research_source.register@1.0.0",
            required_lane=AuthorityLane.COMPOSER,
            preconditions=("workspace_active", "immutable_record_formed"),
            side_effect_class=SideEffectClass.TRANSACTIONAL_COMMIT,
        ),
        "approve_source": ProgramTransitionContract(
            from_state="SOURCE_REGISTERED",
            to_state="SOURCE_ACTIVE",
            transition_name="approve_source",
            trigger_operation="cae.research_source.approve@1.0.0",
            required_lane=AuthorityLane.COMMANDER,
            preconditions=("workspace_active", "operator_authorized"),
            side_effect_class=SideEffectClass.TRANSACTIONAL_COMMIT,
        ),
        "reingest_source": ProgramTransitionContract(
            from_state="SOURCE_ACTIVE",
            to_state="SOURCE_VERSIONED",
            transition_name="reingest_source",
            trigger_operation="cae.research_source.reingest@1.0.0",
            required_lane=AuthorityLane.HUNTER,
            preconditions=("workspace_active", "version_lineage_preserved"),
            side_effect_class=SideEffectClass.TRANSACTIONAL_COMMIT,
        ),
        "quarantine_source": ProgramTransitionContract(
            from_state="SOURCE_ADMITTED",
            to_state="SOURCE_QUARANTINED",
            transition_name="quarantine_source",
            trigger_operation="cae.research_source.quarantine@1.0.0",
            required_lane=AuthorityLane.COMMANDER,
            preconditions=("workspace_active", "quarantine_reason_provided"),
            side_effect_class=SideEffectClass.TRANSACTIONAL_COMMIT,
        ),
    }
    repair_transitions = {
        "repair_source": ProgramTransitionContract(
            from_state="REPAIRING",
            to_state="SOURCE_ADMITTED",
            transition_name="repair_source",
            trigger_operation="cae.research_source.repair@1.0.0",
            required_lane=AuthorityLane.COMMANDER,
            preconditions=("workspace_active", "operator_authorized"),
            side_effect_class=SideEffectClass.TRANSACTIONAL_COMMIT,
        ),
    }
    return ProgramStateMachineDefinition(
        machine_id="RESEARCH_SOURCE_STATE_MACHINE_V1",
        program_id="research_source_ingestion_program",
        initial_state="INITIAL",
        terminal_states={"SOURCE_ACTIVE", "SOURCE_VERSIONED", "SOURCE_QUARANTINED"},
        transitions=transitions,
        repair_transitions=repair_transitions,
    )


# ============================================================================
# 4. Program Coordinator
# ============================================================================

class ResearchSourceProgramCoordinator:
    """Governed Coordinator for Research Source Ingestion + Identity Program.

    Orchestrates:
      INITIAL -> SOURCE_ADMITTED (Hunter)
              -> SOURCE_VERIFIED (Analyst)
              -> SOURCE_REGISTERED (Composer)
              -> SOURCE_ACTIVE (Commander)
              -> SOURCE_VERSIONED (Re-ingestion with modified content)
              -> SOURCE_QUARANTINED (Commander/Analyst gate failure)
              -> REPAIRING -> SOURCE_ADMITTED (Commander repair route)

    Enforces:
    - Root tenant boundary at Workspace level.
    - Protected source immutability (no in-place mutation of existing source records).
    - Idempotency (identical content yields replay receipt without duplicate canonical IDs).
    - Multi-version lineage (modified re-ingestion increments version, preserves ancestry).
    - Anti-inflation and syndication detection.
    - Four Authority Lanes (HUNTER, ANALYST, COMPOSER, COMMANDER).
    - Deterministic cryptographic execution receipts.
    """

    def __init__(
        self,
        runtime: UniversalProgramStateRuntime,
        ledger: Optional[CausalTraceLedger] = None,
    ):
        self.runtime = runtime
        self.ledger = ledger or CausalTraceLedger()
        self._source_records: Dict[str, ResearchSourceRecord] = {}
        self._source_versions_by_origin: Dict[str, List[str]] = {}

    def _ensure_tenant(self, workspace_id: str) -> TenantContext:
        ctx = require_current_tenant_context()
        if str(ctx.workspace_id) != str(workspace_id):
            raise CrossWorkspaceLeakError(
                f"Active tenant workspace '{ctx.workspace_id}' does not match target workspace '{workspace_id}'"
            )
        return ctx

    def _build_receipt(
        self,
        *,
        operation_id: str,
        lane: AuthorityLane,
        actor_id: str,
        workspace_id: str,
        aggregate_id: str,
        input_payload: Mapping[str, Any],
        output_payload: Mapping[str, Any],
        idempotent_replay: bool = False,
    ) -> Dict[str, Any]:
        receipt_id = f"rcpt:rs:{uuid4().hex[:16]}"
        recorded_at = utc_now_rfc3339()
        receipt_payload = {
            "receipt_type": "cae_execution_receipt",
            "receipt_id": receipt_id,
            "claim_id": f"CAE-M28.{operation_id}",
            "component_id": "ca_runtime.research_source_program",
            "operation_id": operation_id,
            "authority_lane": lane.value,
            "actor_id": actor_id,
            "workspace_id": workspace_id,
            "aggregate_id": aggregate_id,
            "input_snapshot_sha256": canonical_sha256(dict(input_payload)),
            "output_snapshot_sha256": canonical_sha256(dict(output_payload)),
            "idempotent_replay": idempotent_replay,
            "recorded_at": recorded_at,
            "environment_identity": {
                "state_authority": "postgresql_supabase",
                "runtime_component": "ca_runtime.ResearchSourceProgramCoordinator",
            },
        }
        receipt_payload["receipt_sha256"] = canonical_sha256(receipt_payload)
        return receipt_payload

    # ------------------------------------------------------------------------
    # 1. Admit Source (Hunter)
    # ------------------------------------------------------------------------
    def admit_source(
        self,
        *,
        workspace_id: str,
        aggregate_id: str,
        actor_id: str,
        origin_url: str,
        raw_text_snippet: str,
        source_platform: str = "web",
        source_type: str = "EXTERNAL_WEB",
        author_outlet: Optional[str] = None,
        rights_metadata: Optional[Dict[str, Any]] = None,
        raw_payload: Optional[Dict[str, Any]] = None,
        expected_version: Optional[int] = None,
    ) -> Tuple[ResearchSourceRecord, Dict[str, Any]]:
        """Admit an external research observation into the workspace pipeline.

        Lane: HUNTER.
        """
        self._ensure_tenant(workspace_id)

        if not origin_url or not origin_url.startswith(("http://", "https://", "feed://", "file://", "cae://")):
            raise SourceProvenanceIntegrityError(f"Invalid origin URL format: '{origin_url}'")

        clean_text = raw_text_snippet.strip()
        if len(clean_text) < 10:
            raise SourceProvenanceIntegrityError(
                "Raw text snippet is too short to constitute verifiable source evidence (minimum 10 characters required)"
            )

        content_sha256 = hashlib.sha256(clean_text.encode("utf-8")).hexdigest()
        root_domain = SignalNormalizer.extract_root_domain(origin_url)

        # Check for exact duplicate in this workspace
        origin_key = f"{workspace_id}:{origin_url}"
        existing_version_ids = self._source_versions_by_origin.get(origin_key, [])
        for sid in existing_version_ids:
            rec = self._source_records.get(sid)
            if rec and rec.content_sha256 == content_sha256:
                # Idempotent replay: return existing record and replay receipt
                receipt = self._build_receipt(
                    operation_id="cae.research_source.admit@1.0.0",
                    lane=AuthorityLane.HUNTER,
                    actor_id=actor_id,
                    workspace_id=workspace_id,
                    aggregate_id=aggregate_id,
                    input_payload={"origin_url": origin_url, "content_sha256": content_sha256},
                    output_payload=rec.to_dict(),
                    idempotent_replay=True,
                )
                return rec, receipt

        # Derive stable canonical ID
        source_id = f"cae:source:rs:{canonical_sha256({'workspace_id': workspace_id, 'origin_url': origin_url, 'content_sha256': content_sha256})[:32]}"

        now_utc = utc_now_rfc3339()
        provenance = {
            "origin_url": origin_url,
            "root_domain": root_domain,
            "platform": source_platform,
            "observed_at": now_utc,
            "content_hash_sha256": content_sha256,
            "author_outlet": author_outlet,
            "is_syndicated_copy": SignalNormalizer.is_syndicated_text(clean_text),
        }

        multiplicity = {
            "raw_mention_count": 1,
            "unique_root_domain_count": 1,
            "independent_source_count": 1,
            "syndication_ratio_bps": 10000 if provenance["is_syndicated_copy"] else 0,
        }

        # Transition Aggregate
        aggregate = self.runtime.get_aggregate(aggregate_id)
        if aggregate.current_state == "INITIAL":
            self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="admit_source",
                actor_lane=AuthorityLane.HUNTER,
                actor_id=actor_id,
                context_claims=["workspace_active", "source_origin_valid"],
                state_updates={
                    "active_source_id": source_id,
                    "origin_url": origin_url,
                    "root_domain": root_domain,
                    "content_sha256": content_sha256,
                    "platform": source_platform,
                    "source_type": source_type,
                    "author_outlet": author_outlet,
                    "rights_metadata": rights_metadata or {},
                    "version": 1,
                },
                expected_version=expected_version,
            )

        receipt = self._build_receipt(
            operation_id="cae.research_source.admit@1.0.0",
            lane=AuthorityLane.HUNTER,
            actor_id=actor_id,
            workspace_id=workspace_id,
            aggregate_id=aggregate_id,
            input_payload={"origin_url": origin_url, "content_sha256": content_sha256},
            output_payload={"source_id": source_id, "status": "ADMITTED"},
            idempotent_replay=False,
        )

        record = ResearchSourceRecord(
            source_id=source_id,
            workspace_id=workspace_id,
            source_type=source_type,
            origin_url=origin_url,
            root_domain=root_domain,
            platform=source_platform,
            content_sha256=content_sha256,
            raw_content_excerpt=clean_text,
            author_outlet=author_outlet,
            rights_metadata=rights_metadata or {},
            version=1,
            supersedes_source_id=None,
            ancestor_version_hashes=(),
            provenance_record=provenance,
            source_multiplicity=multiplicity,
            admitted_at=now_utc,
            verified_at=None,
            status="ADMITTED",
            receipt_sha256=receipt["receipt_sha256"],
        )

        self._source_records[source_id] = record
        if origin_key not in self._source_versions_by_origin:
            self._source_versions_by_origin[origin_key] = []
        self._source_versions_by_origin[origin_key].append(source_id)

        return record, receipt

    # ------------------------------------------------------------------------
    # 2. Verify Source (Analyst)
    # ------------------------------------------------------------------------
    def verify_source(
        self,
        *,
        workspace_id: str,
        aggregate_id: str,
        actor_id: str,
        source_id: str,
        corroborating_observations: Optional[List[RawObservation]] = None,
        expected_version: Optional[int] = None,
    ) -> Tuple[ResearchSourceRecord, Dict[str, Any]]:
        """Verify provenance integrity, content hashes, and anti-inflation constraints.

        Lane: ANALYST.
        """
        self._ensure_tenant(workspace_id)

        record = self._source_records.get(source_id)
        if not record:
            raise SourceProvenanceIntegrityError(f"Research source '{source_id}' not found", source_id=source_id)

        if str(record.workspace_id) != str(workspace_id):
            raise CrossWorkspaceLeakError(
                f"Source '{source_id}' belongs to workspace '{record.workspace_id}', not '{workspace_id}'"
            )

        # 1. Verify content hash
        computed_hash = hashlib.sha256(record.raw_content_excerpt.encode("utf-8")).hexdigest()
        if computed_hash != record.content_sha256:
            raise SourceHashMismatchError(
                f"Content excerpt hash '{computed_hash}' does not match declared hash '{record.content_sha256}'",
                expected_hash=record.content_sha256,
                actual_hash=computed_hash,
            )

        # 2. Multiplicity & Anti-Inflation Analysis
        observations: List[RawObservation] = [
            RawObservation(
                source_platform=record.platform,
                query_context=record.origin_url,
                raw_payload={},
                retrieved_at=datetime.fromisoformat(record.admitted_at),
                raw_text_snippet=record.raw_content_excerpt,
                source_url=record.origin_url,
                author_outlet=record.author_outlet,
            )
        ]
        if corroborating_observations:
            observations.extend(corroborating_observations)

        multiplicity_obj, provenance_list = SignalNormalizer.calculate_multiplicity(observations)

        multiplicity_data = {
            "raw_mention_count": multiplicity_obj.raw_mention_count,
            "unique_root_domain_count": multiplicity_obj.unique_root_domain_count,
            "independent_source_count": multiplicity_obj.independent_source_count,
            "syndication_ratio_bps": int(round(multiplicity_obj.syndication_ratio * 10000)),
        }

        # Anti-inflation check: independent count cannot exceed unique domains
        if multiplicity_obj.independent_source_count > multiplicity_obj.unique_root_domain_count:
            raise DuplicateSourceInflationViolationError(
                f"Independent source count ({multiplicity_obj.independent_source_count}) cannot exceed unique root domains ({multiplicity_obj.unique_root_domain_count})",
                multiplicity=multiplicity_data,
            )

        now_utc = utc_now_rfc3339()

        # Transition Aggregate
        aggregate = self.runtime.get_aggregate(aggregate_id)
        if aggregate.current_state == "SOURCE_ADMITTED":
            self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="verify_source",
                actor_lane=AuthorityLane.ANALYST,
                actor_id=actor_id,
                context_claims=["workspace_active", "provenance_hash_verified", "multiplicity_checked"],
                state_updates={
                    "verified_at": now_utc,
                    "multiplicity": multiplicity_data,
                    "status": "VERIFIED",
                },
                expected_version=expected_version,
            )

        receipt = self._build_receipt(
            operation_id="cae.research_source.verify@1.0.0",
            lane=AuthorityLane.ANALYST,
            actor_id=actor_id,
            workspace_id=workspace_id,
            aggregate_id=aggregate_id,
            input_payload={"source_id": source_id, "content_sha256": record.content_sha256},
            output_payload={"source_id": source_id, "status": "VERIFIED", "multiplicity": multiplicity_data},
        )

        verified_record = ResearchSourceRecord(
            source_id=record.source_id,
            workspace_id=record.workspace_id,
            source_type=record.source_type,
            origin_url=record.origin_url,
            root_domain=record.root_domain,
            platform=record.platform,
            content_sha256=record.content_sha256,
            raw_content_excerpt=record.raw_content_excerpt,
            author_outlet=record.author_outlet,
            rights_metadata=record.rights_metadata,
            version=record.version,
            supersedes_source_id=record.supersedes_source_id,
            ancestor_version_hashes=record.ancestor_version_hashes,
            provenance_record=record.provenance_record,
            source_multiplicity=multiplicity_data,
            admitted_at=record.admitted_at,
            verified_at=now_utc,
            status="VERIFIED",
            receipt_sha256=receipt["receipt_sha256"],
        )

        self._source_records[source_id] = verified_record
        return verified_record, receipt

    # ------------------------------------------------------------------------
    # 3. Register Source (Composer)
    # ------------------------------------------------------------------------
    def register_source(
        self,
        *,
        workspace_id: str,
        aggregate_id: str,
        actor_id: str,
        source_id: str,
        expected_version: Optional[int] = None,
    ) -> Tuple[ResearchSourceRecord, Dict[str, Any]]:
        """Package verified source into an immutable registered record.

        Lane: COMPOSER.
        """
        self._ensure_tenant(workspace_id)

        record = self._source_records.get(source_id)
        if not record or record.status not in ("VERIFIED", "ADMITTED"):
            raise SourceProvenanceIntegrityError(
                f"Source '{source_id}' must be in VERIFIED state before registration (current status: '{record.status if record else 'NONE'}')",
                source_id=source_id,
            )

        aggregate = self.runtime.get_aggregate(aggregate_id)
        if aggregate.current_state == "SOURCE_VERIFIED":
            self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="register_source",
                actor_lane=AuthorityLane.COMPOSER,
                actor_id=actor_id,
                context_claims=["workspace_active", "immutable_record_formed"],
                state_updates={
                    "registered_at": utc_now_rfc3339(),
                    "status": "REGISTERED",
                },
                expected_version=expected_version,
            )

        receipt = self._build_receipt(
            operation_id="cae.research_source.register@1.0.0",
            lane=AuthorityLane.COMPOSER,
            actor_id=actor_id,
            workspace_id=workspace_id,
            aggregate_id=aggregate_id,
            input_payload={"source_id": source_id},
            output_payload={"source_id": source_id, "status": "REGISTERED"},
        )

        registered_record = ResearchSourceRecord(
            source_id=record.source_id,
            workspace_id=record.workspace_id,
            source_type=record.source_type,
            origin_url=record.origin_url,
            root_domain=record.root_domain,
            platform=record.platform,
            content_sha256=record.content_sha256,
            raw_content_excerpt=record.raw_content_excerpt,
            author_outlet=record.author_outlet,
            rights_metadata=record.rights_metadata,
            version=record.version,
            supersedes_source_id=record.supersedes_source_id,
            ancestor_version_hashes=record.ancestor_version_hashes,
            provenance_record=record.provenance_record,
            source_multiplicity=record.source_multiplicity,
            admitted_at=record.admitted_at,
            verified_at=record.verified_at,
            status="REGISTERED",
            receipt_sha256=receipt["receipt_sha256"],
        )

        self._source_records[source_id] = registered_record
        return registered_record, receipt

    # ------------------------------------------------------------------------
    # 4. Approve Source (Commander)
    # ------------------------------------------------------------------------
    def approve_source(
        self,
        *,
        workspace_id: str,
        aggregate_id: str,
        actor_id: str,
        source_id: str,
        expected_version: Optional[int] = None,
    ) -> Tuple[ResearchSourceRecord, Dict[str, Any]]:
        """Authorize and activate the registered source for downstream intelligence consumption.

        Lane: COMMANDER.
        """
        self._ensure_tenant(workspace_id)

        record = self._source_records.get(source_id)
        if not record or record.status != "REGISTERED":
            raise SourceProvenanceIntegrityError(
                f"Source '{source_id}' must be in REGISTERED state before approval (current: '{record.status if record else 'NONE'}')",
                source_id=source_id,
            )

        aggregate = self.runtime.get_aggregate(aggregate_id)
        if aggregate.current_state == "SOURCE_REGISTERED":
            self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="approve_source",
                actor_lane=AuthorityLane.COMMANDER,
                actor_id=actor_id,
                context_claims=["workspace_active", "operator_authorized"],
                state_updates={
                    "approved_at": utc_now_rfc3339(),
                    "approved_by": actor_id,
                    "status": "ACTIVE",
                },
                expected_version=expected_version,
            )

        receipt = self._build_receipt(
            operation_id="cae.research_source.approve@1.0.0",
            lane=AuthorityLane.COMMANDER,
            actor_id=actor_id,
            workspace_id=workspace_id,
            aggregate_id=aggregate_id,
            input_payload={"source_id": source_id, "approver_id": actor_id},
            output_payload={"source_id": source_id, "status": "ACTIVE"},
        )

        active_record = ResearchSourceRecord(
            source_id=record.source_id,
            workspace_id=record.workspace_id,
            source_type=record.source_type,
            origin_url=record.origin_url,
            root_domain=record.root_domain,
            platform=record.platform,
            content_sha256=record.content_sha256,
            raw_content_excerpt=record.raw_content_excerpt,
            author_outlet=record.author_outlet,
            rights_metadata=record.rights_metadata,
            version=record.version,
            supersedes_source_id=record.supersedes_source_id,
            ancestor_version_hashes=record.ancestor_version_hashes,
            provenance_record=record.provenance_record,
            source_multiplicity=record.source_multiplicity,
            admitted_at=record.admitted_at,
            verified_at=record.verified_at,
            status="ACTIVE",
            receipt_sha256=receipt["receipt_sha256"],
        )

        self._source_records[source_id] = active_record
        return active_record, receipt

    # ------------------------------------------------------------------------
    # 5. Re-ingest Source with Versioning (Hunter/Commander)
    # ------------------------------------------------------------------------
    def reingest_source(
        self,
        *,
        workspace_id: str,
        aggregate_id: str,
        actor_id: str,
        prior_source_id: str,
        new_raw_text_snippet: str,
        rights_metadata: Optional[Dict[str, Any]] = None,
        author_outlet: Optional[str] = None,
        expected_version: Optional[int] = None,
    ) -> Tuple[ResearchSourceRecord, Dict[str, Any]]:
        """Re-ingest a source at an existing origin URL.

        If new content hash matches prior version -> idempotent replay.
        If new content hash differs -> creates new immutable version (v+1) with cryptographic
        ancestry lineage linking back to prior_source_id, leaving prior record untouched.
        """
        self._ensure_tenant(workspace_id)

        prior_record = self._source_records.get(prior_source_id)
        if not prior_record:
            raise InvalidSourceReingestionError(
                f"Prior source '{prior_source_id}' not found for re-ingestion",
                source_id=prior_source_id,
                reason="PRIOR_SOURCE_NOT_FOUND",
            )

        clean_text = new_raw_text_snippet.strip()
        new_content_sha256 = hashlib.sha256(clean_text.encode("utf-8")).hexdigest()

        # Check for identical content
        if new_content_sha256 == prior_record.content_sha256:
            # Idempotent replay: content unchanged, version unchanged
            receipt = self._build_receipt(
                operation_id="cae.research_source.reingest@1.0.0",
                lane=AuthorityLane.HUNTER,
                actor_id=actor_id,
                workspace_id=workspace_id,
                aggregate_id=aggregate_id,
                input_payload={"prior_source_id": prior_source_id, "content_sha256": new_content_sha256},
                output_payload=prior_record.to_dict(),
                idempotent_replay=True,
            )
            return prior_record, receipt

        # Content has changed: create new immutable version
        new_version_num = prior_record.version + 1
        new_source_id = f"cae:source:rs:{canonical_sha256({'workspace_id': workspace_id, 'origin_url': prior_record.origin_url, 'content_sha256': new_content_sha256, 'version': new_version_num})[:32]}"

        new_ancestors = prior_record.ancestor_version_hashes + (prior_record.content_sha256,)
        now_utc = utc_now_rfc3339()

        provenance = {
            "origin_url": prior_record.origin_url,
            "root_domain": prior_record.root_domain,
            "platform": prior_record.platform,
            "observed_at": now_utc,
            "content_hash_sha256": new_content_sha256,
            "author_outlet": author_outlet or prior_record.author_outlet,
            "is_syndicated_copy": SignalNormalizer.is_syndicated_text(clean_text),
        }

        multiplicity = {
            "raw_mention_count": 1,
            "unique_root_domain_count": 1,
            "independent_source_count": 1,
            "syndication_ratio_bps": 10000 if provenance["is_syndicated_copy"] else 0,
        }

        # Transition Aggregate
        aggregate = self.runtime.get_aggregate(aggregate_id)
        if aggregate.current_state in ("SOURCE_ACTIVE", "SOURCE_REGISTERED"):
            self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="reingest_source",
                actor_lane=AuthorityLane.HUNTER,
                actor_id=actor_id,
                context_claims=["workspace_active", "version_lineage_preserved"],
                state_updates={
                    "active_source_id": new_source_id,
                    "active_source_version": new_version_num,
                    "supersedes_source_id": prior_source_id,
                    "content_sha256": new_content_sha256,
                    "version": new_version_num,
                    "status": "VERSIONED",
                },
                expected_version=expected_version,
            )

        receipt = self._build_receipt(
            operation_id="cae.research_source.reingest@1.0.0",
            lane=AuthorityLane.HUNTER,
            actor_id=actor_id,
            workspace_id=workspace_id,
            aggregate_id=aggregate_id,
            input_payload={"prior_source_id": prior_source_id, "new_content_sha256": new_content_sha256, "version": new_version_num},
            output_payload={"new_source_id": new_source_id, "version": new_version_num, "status": "VERSIONED"},
            idempotent_replay=False,
        )

        new_record = ResearchSourceRecord(
            source_id=new_source_id,
            workspace_id=workspace_id,
            source_type=prior_record.source_type,
            origin_url=prior_record.origin_url,
            root_domain=prior_record.root_domain,
            platform=prior_record.platform,
            content_sha256=new_content_sha256,
            raw_content_excerpt=clean_text,
            author_outlet=author_outlet or prior_record.author_outlet,
            rights_metadata=rights_metadata or prior_record.rights_metadata,
            version=new_version_num,
            supersedes_source_id=prior_source_id,
            ancestor_version_hashes=new_ancestors,
            provenance_record=provenance,
            source_multiplicity=multiplicity,
            admitted_at=now_utc,
            verified_at=now_utc,
            status="VERSIONED",
            receipt_sha256=receipt["receipt_sha256"],
        )

        self._source_records[new_source_id] = new_record
        origin_key = f"{workspace_id}:{prior_record.origin_url}"
        self._source_versions_by_origin[origin_key].append(new_source_id)

        return new_record, receipt

    # ------------------------------------------------------------------------
    # 6. Quarantine Source (Commander / Analyst)
    # ------------------------------------------------------------------------
    def quarantine_source(
        self,
        *,
        workspace_id: str,
        aggregate_id: str,
        actor_id: str,
        source_id: str,
        quarantine_reason: str,
        expected_version: Optional[int] = None,
    ) -> Tuple[ResearchSourceRecord, Dict[str, Any]]:
        """Quarantine a source due to evidence failure or invalid provenance.

        Lane: COMMANDER.
        """
        self._ensure_tenant(workspace_id)

        record = self._source_records.get(source_id)
        if not record:
            raise SourceProvenanceIntegrityError(f"Source '{source_id}' not found", source_id=source_id)

        aggregate = self.runtime.get_aggregate(aggregate_id)
        if aggregate.current_state in ("SOURCE_ADMITTED", "SOURCE_VERIFIED"):
            self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="quarantine_source",
                actor_lane=AuthorityLane.COMMANDER,
                actor_id=actor_id,
                context_claims=["workspace_active", "quarantine_reason_provided"],
                state_updates={
                    "quarantined_at": utc_now_rfc3339(),
                    "quarantine_reason": quarantine_reason,
                    "status": "QUARANTINED",
                },
                expected_version=expected_version,
            )

        receipt = self._build_receipt(
            operation_id="cae.research_source.quarantine@1.0.0",
            lane=AuthorityLane.COMMANDER,
            actor_id=actor_id,
            workspace_id=workspace_id,
            aggregate_id=aggregate_id,
            input_payload={"source_id": source_id, "reason": quarantine_reason},
            output_payload={"source_id": source_id, "status": "QUARANTINED"},
        )

        quarantined_record = ResearchSourceRecord(
            source_id=record.source_id,
            workspace_id=record.workspace_id,
            source_type=record.source_type,
            origin_url=record.origin_url,
            root_domain=record.root_domain,
            platform=record.platform,
            content_sha256=record.content_sha256,
            raw_content_excerpt=record.raw_content_excerpt,
            author_outlet=record.author_outlet,
            rights_metadata=record.rights_metadata,
            version=record.version,
            supersedes_source_id=record.supersedes_source_id,
            ancestor_version_hashes=record.ancestor_version_hashes,
            provenance_record=record.provenance_record,
            source_multiplicity=record.source_multiplicity,
            admitted_at=record.admitted_at,
            verified_at=record.verified_at,
            status="QUARANTINED",
            receipt_sha256=receipt["receipt_sha256"],
        )

        self._source_records[source_id] = quarantined_record
        return quarantined_record, receipt

    def recover_to_repairing(
        self,
        *,
        aggregate_id: str,
        failure_reason: str,
        context: TenantContext,
        actor_id: str = "usr_commander_lead",
    ) -> ProgramStateAggregate:
        """Transitions aggregate to REPAIRING lifecycle on invariant violation or fault."""
        aggregate = self.runtime.get_aggregate(aggregate_id)
        if not aggregate:
            raise ProgramStateAggregateNotFoundError(aggregate_id)
        if str(aggregate.workspace_id) != str(context.workspace_id):
            raise CrossWorkspaceLeakError("Tenant workspace mismatch")

        current_data = dict(aggregate.state_data)
        current_data["repair_reason"] = failure_reason
        current_data["entered_repair_at"] = utc_now_rfc3339()

        new_version_num = aggregate.version + 1
        now = utc_now_rfc3339()
        new_state_hash = _compute_state_hash(
            aggregate_id=aggregate.aggregate_id,
            program_id=aggregate.program_id,
            program_version=aggregate.program_version,
            current_state="REPAIRING",
            version=new_version_num,
            state_data=current_data,
        )

        repairing_aggregate = ProgramStateAggregate(
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            cae_run_id=aggregate.cae_run_id,
            program_id=aggregate.program_id,
            program_version=aggregate.program_version,
            current_state="REPAIRING",
            state_data=current_data,
            version=new_version_num,
            state_hash=new_state_hash,
            lifecycle=ProgramStateLifecycle.REPAIRING,
            last_receipt_id=aggregate.last_receipt_id,
            created_at=aggregate.created_at,
            updated_at=now,
        )

        self.runtime.store.save_aggregate(repairing_aggregate, expected_version=aggregate.version)
        return repairing_aggregate

    # ------------------------------------------------------------------------
    # 7. Repair Route (Commander)
    # ------------------------------------------------------------------------
    def repair_source_state(
        self,
        *,
        workspace_id: str,
        aggregate_id: str,
        actor_id: str,
        repair_reason: str,
        expected_version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Bounded repair route recovering aggregate from REPAIRING back to SOURCE_ADMITTED.

        Lane: COMMANDER.
        """
        self._ensure_tenant(workspace_id)

        aggregate = self.runtime.get_aggregate(aggregate_id)
        if aggregate.current_state != "REPAIRING":
            raise ResearchSourceProgramError(
                f"Cannot execute repair on aggregate in state '{aggregate.current_state}': must be in 'REPAIRING'",
                reason_code="INVALID_REPAIR_STATE",
            )

        self.runtime.execute_transition(
            aggregate_id=aggregate_id,
            transition_name="repair_source",
            actor_lane=AuthorityLane.COMMANDER,
            actor_id=actor_id,
            context_claims=["workspace_active", "operator_authorized"],
            state_updates={
                "repaired_at": utc_now_rfc3339(),
                "repair_reason": repair_reason,
            },
            expected_version=expected_version,
        )

        receipt = self._build_receipt(
            operation_id="cae.research_source.repair@1.0.0",
            lane=AuthorityLane.COMMANDER,
            actor_id=actor_id,
            workspace_id=workspace_id,
            aggregate_id=aggregate_id,
            input_payload={"repair_reason": repair_reason},
            output_payload={"target_state": "SOURCE_ADMITTED"},
        )
        return receipt

    # ------------------------------------------------------------------------
    # Inspection & Getters
    # ------------------------------------------------------------------------
    def get_source_record(
        self,
        source_id: str,
        workspace_id: Optional[str] = None,
    ) -> Optional[ResearchSourceRecord]:
        if workspace_id:
            self._ensure_tenant(workspace_id)
        rec = self._source_records.get(source_id)
        if rec and workspace_id and str(rec.workspace_id) != str(workspace_id):
            raise CrossWorkspaceLeakError(f"Cross-workspace leak detected: record {source_id} belongs to {rec.workspace_id}")
        return rec

    def get_versions_for_origin(self, workspace_id: str, origin_url: str) -> List[ResearchSourceRecord]:
        self._ensure_tenant(workspace_id)
        origin_key = f"{workspace_id}:{origin_url}"
        ids = self._source_versions_by_origin.get(origin_key, [])
        return [self._source_records[sid] for sid in ids if sid in self._source_records]

    def get_snapshot(self, aggregate_id: str) -> ResearchSourceSnapshot:
        aggregate = self.runtime.get_aggregate(aggregate_id)
        state_data = aggregate.state_data
        active_source_id = state_data.get("active_source_id")
        origin_key = f"{aggregate.workspace_id}:{state_data.get('origin_url', '')}"
        total_versions = len(self._source_versions_by_origin.get(origin_key, []))

        return ResearchSourceSnapshot(
            aggregate_id=aggregate.aggregate_id,
            workspace_id=aggregate.workspace_id,
            current_state=aggregate.current_state,
            active_source_id=active_source_id,
            active_source_version=int(state_data.get("active_source_version", state_data.get("version", 1))),
            origin_url=state_data.get("origin_url"),
            content_sha256=state_data.get("content_sha256"),
            root_domain=state_data.get("root_domain"),
            status=state_data.get("status", aggregate.current_state),
            total_versions=total_versions,
            version=aggregate.version,
            state_hash=aggregate.state_hash,
            last_receipt_id=aggregate.last_receipt_id,
        )
