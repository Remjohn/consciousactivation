from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
import json


CAPABILITY_OWNERSHIP_SCHEMA_ID = "cmf-builder-capability-ownership/v1"
CAPABILITY_OWNERSHIP_SCHEMA_VERSION = "1.0.0"
CAPABILITY_OWNERSHIP_RECEIPT_SCHEMA_ID = (
    "cmf-builder-capability-ownership-receipt/v1"
)
CAPABILITY_OWNERSHIP_INPUT_PATH = (
    "development-capsules/ST-04.01/CAPABILITY_OWNERSHIP_INPUT.json"
)
CAPABILITY_OWNERSHIP_INPUT_SHA256 = (
    "c6c8429f7eabeea6b11a62c1a2698becaeec747797264ab187e0cb05227afc18"
)
CAPABILITY_OWNERSHIP_INPUT_SCHEMA = (
    "cmf-builder-synthetic-capability-ownership-input/v1"
)
CAPABILITY_OWNERSHIP_SCOPE = "ST-04.01_SYNTHETIC_CORE_ONLY"
SYNTHETIC_TARGET_PROFILE_REF = "synthetic_text_normalization_v1@1.0.0"
SOURCE_CAPABILITY_PATH = "skills.capabilities"
EXPECTED_CAPABILITIES = (
    "atomic_boundary_declaration",
    "deterministic_validation_and_receipt_generation",
    "target_and_output_contract_definition",
)
EMPTY_SKILL_REGISTRY_POLICY_PATH = "governance/EMPTY_SKILL_REGISTRY_POLICY.yaml"
EMPTY_SKILL_REGISTRY_POLICY_SHA256 = (
    "260df1cb40655fe4f42d264bb73f3e6bda012b9fe6bd015a1b6ae153615f985c"
)
EMPTY_SKILL_REGISTRY_FIXTURE_PATH = (
    "governance/fixtures/synthetic-core/empty-skill-registry.yaml"
)
EMPTY_SKILL_REGISTRY_FIXTURE_SHA256 = (
    "a4a9e5afaf91f60b22529ec01f1bc8e22a0d895444ad9a9e9a96e7a3e7b28114"
)
EMPTY_SKILL_REGISTRY_VALIDATION_PATH = (
    "governance/EMPTY_SKILL_REGISTRY_VALIDATION_RECEIPT.json"
)
EMPTY_SKILL_REGISTRY_VALIDATION_SHA256 = (
    "79164fa7418d3750ffefee116264b1ca44533c8073afb5485b84089ebd945ee1"
)
EMPTY_SKILL_REGISTRY_REF = "builder-core-synthetic-empty-skill-registry@1.0.0"


class CapabilityOwnershipError(Exception):
    code = "CapabilityOwnershipError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class CapabilityOwnershipInputInvalid(CapabilityOwnershipError):
    code = "CapabilityOwnershipInputInvalid"


class CapabilityCoverageInvalid(CapabilityOwnershipError):
    code = "CapabilityCoverageInvalid"


class CapabilityAuthorityInvalid(CapabilityOwnershipError):
    code = "CapabilityAuthorityInvalid"


class CapabilityOwnershipInvalidatedError(CapabilityOwnershipError):
    code = "CapabilityOwnershipInvalidated"


class CapabilityOwnerKind(str, Enum):
    CODE = "CODE"
    AGENT = "AGENT"
    HUMAN = "HUMAN"
    EXTERNAL = "EXTERNAL"
    HYBRID = "HYBRID"


@dataclass(frozen=True, slots=True)
class CapabilityOwnershipDecision:
    capability_id: str
    owner_kind: CapabilityOwnerKind
    owner_id: str
    reliability_evidence: tuple[str, ...]
    cost_evidence: tuple[str, ...]
    authority_boundary: str
    handoff_responsibility: str | None
    ordered_participants: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if (
            not self.capability_id.strip()
            or not self.owner_id.strip()
            or not self.authority_boundary.strip()
            or not self.reliability_evidence
            or not self.cost_evidence
            or any(
                not item.strip()
                for item in (
                    *self.reliability_evidence,
                    *self.cost_evidence,
                    *self.ordered_participants,
                )
            )
            or len(set(self.reliability_evidence)) != len(self.reliability_evidence)
            or len(set(self.cost_evidence)) != len(self.cost_evidence)
            or len(set(self.ordered_participants)) != len(self.ordered_participants)
        ):
            raise CapabilityOwnershipInputInvalid(
                "Capability ownership evidence or identity is incomplete.",
                capability_id=self.capability_id,
            )
        if self.owner_kind is CapabilityOwnerKind.CODE:
            if self.handoff_responsibility is not None or self.ordered_participants:
                raise CapabilityAuthorityInvalid(
                    "Code ownership cannot invent a handoff or participant chain.",
                    capability_id=self.capability_id,
                )
            return
        if (
            self.handoff_responsibility is None
            or not self.handoff_responsibility.strip()
            or not self.ordered_participants
            or self.owner_id not in self.ordered_participants
            or (
                self.owner_kind is CapabilityOwnerKind.HYBRID
                and len(self.ordered_participants) < 2
            )
        ):
            raise CapabilityAuthorityInvalid(
                "Non-code ownership requires attributable ordered participants and an explicit handoff.",
                capability_id=self.capability_id,
                owner_kind=self.owner_kind.value,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "capability_id": self.capability_id,
            "owner_kind": self.owner_kind.value,
            "owner_id": self.owner_id,
            "reliability_evidence": list(self.reliability_evidence),
            "cost_evidence": list(self.cost_evidence),
            "authority_boundary": self.authority_boundary,
            "handoff_responsibility": self.handoff_responsibility,
            "ordered_participants": list(self.ordered_participants),
        }


@dataclass(frozen=True, slots=True)
class CapabilityOwnershipGraph:
    graph_id: str
    graph_hash: str
    schema_id: str
    schema_version: str
    scope: str
    run_id: str
    target_profile_ref: str
    ir_id: str
    ir_hash: str
    source_lock_ref: str
    boundary_ref: str
    ratification_ref: str
    model_ref: str
    artifact_set_id: str
    constitutional_report_id: str
    constitutional_report_hash: str
    constitutional_receipt_id: str
    constitutional_receipt_hash: str
    authority_identity: str
    source_capability_path: str
    ownership_input_path: str
    ownership_input_hash: str
    empty_registry_policy_hash: str
    empty_registry_fixture_hash: str
    empty_registry_validation_hash: str
    decisions: tuple[CapabilityOwnershipDecision, ...]
    external_skills_required: bool
    dynamic_skill_discovery_allowed: bool
    production_eligible: bool
    certified: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        run_id: str,
        ir_id: str,
        ir_hash: str,
        source_lock_ref: str,
        boundary_ref: str,
        ratification_ref: str,
        model_ref: str,
        artifact_set_id: str,
        constitutional_report_id: str,
        constitutional_report_hash: str,
        constitutional_receipt_id: str,
        constitutional_receipt_hash: str,
        authority_identity: str,
        decisions: tuple[CapabilityOwnershipDecision, ...],
    ) -> "CapabilityOwnershipGraph":
        candidate = cls(
            graph_id="pending",
            graph_hash="pending",
            schema_id=CAPABILITY_OWNERSHIP_SCHEMA_ID,
            schema_version=CAPABILITY_OWNERSHIP_SCHEMA_VERSION,
            scope=CAPABILITY_OWNERSHIP_SCOPE,
            run_id=run_id,
            target_profile_ref=SYNTHETIC_TARGET_PROFILE_REF,
            ir_id=ir_id,
            ir_hash=ir_hash,
            source_lock_ref=source_lock_ref,
            boundary_ref=boundary_ref,
            ratification_ref=ratification_ref,
            model_ref=model_ref,
            artifact_set_id=artifact_set_id,
            constitutional_report_id=constitutional_report_id,
            constitutional_report_hash=constitutional_report_hash,
            constitutional_receipt_id=constitutional_receipt_id,
            constitutional_receipt_hash=constitutional_receipt_hash,
            authority_identity=authority_identity,
            source_capability_path=SOURCE_CAPABILITY_PATH,
            ownership_input_path=CAPABILITY_OWNERSHIP_INPUT_PATH,
            ownership_input_hash=f"sha256:{CAPABILITY_OWNERSHIP_INPUT_SHA256}",
            empty_registry_policy_hash=f"sha256:{EMPTY_SKILL_REGISTRY_POLICY_SHA256}",
            empty_registry_fixture_hash=f"sha256:{EMPTY_SKILL_REGISTRY_FIXTURE_SHA256}",
            empty_registry_validation_hash=f"sha256:{EMPTY_SKILL_REGISTRY_VALIDATION_SHA256}",
            decisions=tuple(sorted(decisions, key=lambda item: item.capability_id)),
            external_skills_required=False,
            dynamic_skill_discovery_allowed=False,
            production_eligible=False,
            certified=False,
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            graph_id=f"capability-ownership-graph_{digest}",
            graph_hash=f"sha256:{digest}",
        )
        result.validate()
        return result

    @property
    def capability_ids(self) -> tuple[str, ...]:
        return tuple(item.capability_id for item in self.decisions)

    @property
    def owner_kind_counts(self) -> tuple[tuple[str, int], ...]:
        return tuple(
            (kind.value, sum(item.owner_kind is kind for item in self.decisions))
            for kind in CapabilityOwnerKind
            if any(item.owner_kind is kind for item in self.decisions)
        )

    def validate(self) -> None:
        for item in self.decisions:
            item.validate()
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != CAPABILITY_OWNERSHIP_SCHEMA_ID
            or self.schema_version != CAPABILITY_OWNERSHIP_SCHEMA_VERSION
            or self.scope != CAPABILITY_OWNERSHIP_SCOPE
            or self.target_profile_ref != SYNTHETIC_TARGET_PROFILE_REF
            or self.source_capability_path != SOURCE_CAPABILITY_PATH
            or self.ownership_input_path != CAPABILITY_OWNERSHIP_INPUT_PATH
            or self.ownership_input_hash
            != f"sha256:{CAPABILITY_OWNERSHIP_INPUT_SHA256}"
            or self.empty_registry_policy_hash
            != f"sha256:{EMPTY_SKILL_REGISTRY_POLICY_SHA256}"
            or self.empty_registry_fixture_hash
            != f"sha256:{EMPTY_SKILL_REGISTRY_FIXTURE_SHA256}"
            or self.empty_registry_validation_hash
            != f"sha256:{EMPTY_SKILL_REGISTRY_VALIDATION_SHA256}"
            or self.capability_ids != EXPECTED_CAPABILITIES
            or len(set(self.capability_ids)) != len(self.capability_ids)
            or any(
                item.owner_kind is not CapabilityOwnerKind.CODE
                for item in self.decisions
            )
            or not all(
                value.strip()
                for value in (
                    self.run_id,
                    self.ir_id,
                    self.ir_hash,
                    self.source_lock_ref,
                    self.boundary_ref,
                    self.ratification_ref,
                    self.model_ref,
                    self.artifact_set_id,
                    self.constitutional_report_id,
                    self.constitutional_report_hash,
                    self.constitutional_receipt_id,
                    self.constitutional_receipt_hash,
                    self.authority_identity,
                )
            )
            or self.external_skills_required
            or self.dynamic_skill_discovery_allowed
            or self.production_eligible
            or self.certified
            or self.outcome != "PASS"
            or self.graph_id != f"capability-ownership-graph_{digest}"
            or self.graph_hash != f"sha256:{digest}"
        ):
            raise CapabilityCoverageInvalid(
                "Capability ownership graph is incomplete, broadened, or hash-invalid."
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "scope": self.scope,
            "run_id": self.run_id,
            "target_profile_ref": self.target_profile_ref,
            "ir_id": self.ir_id,
            "ir_hash": self.ir_hash,
            "source_lock_ref": self.source_lock_ref,
            "boundary_ref": self.boundary_ref,
            "ratification_ref": self.ratification_ref,
            "model_ref": self.model_ref,
            "artifact_set_id": self.artifact_set_id,
            "constitutional_report_id": self.constitutional_report_id,
            "constitutional_report_hash": self.constitutional_report_hash,
            "constitutional_receipt_id": self.constitutional_receipt_id,
            "constitutional_receipt_hash": self.constitutional_receipt_hash,
            "authority_identity": self.authority_identity,
            "source_capability_path": self.source_capability_path,
            "ownership_input_path": self.ownership_input_path,
            "ownership_input_hash": self.ownership_input_hash,
            "empty_registry_policy_hash": self.empty_registry_policy_hash,
            "empty_registry_fixture_hash": self.empty_registry_fixture_hash,
            "empty_registry_validation_hash": self.empty_registry_validation_hash,
            "decisions": [item.canonical_dict() for item in self.decisions],
            "external_skills_required": self.external_skills_required,
            "dynamic_skill_discovery_allowed": self.dynamic_skill_discovery_allowed,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class CapabilityOwnershipReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    graph_id: str
    graph_hash: str
    ir_id: str
    constitutional_report_id: str
    constitutional_receipt_id: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    capability_count: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        graph: CapabilityOwnershipGraph,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "CapabilityOwnershipReceipt":
        graph.validate()
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=CAPABILITY_OWNERSHIP_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=graph.run_id,
            graph_id=graph.graph_id,
            graph_hash=graph.graph_hash,
            ir_id=graph.ir_id,
            constitutional_report_id=graph.constitutional_report_id,
            constitutional_receipt_id=graph.constitutional_receipt_id,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            capability_count=len(graph.decisions),
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            receipt_id=f"capability-ownership-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )
        result.validate(graph)
        return result

    def validate(self, graph: CapabilityOwnershipGraph) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != CAPABILITY_OWNERSHIP_RECEIPT_SCHEMA_ID
            or self.run_id != graph.run_id
            or self.graph_id != graph.graph_id
            or self.graph_hash != graph.graph_hash
            or self.ir_id != graph.ir_id
            or self.constitutional_report_id != graph.constitutional_report_id
            or self.constitutional_receipt_id != graph.constitutional_receipt_id
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.capability_count != len(graph.decisions)
            or self.outcome != "PASS"
            or self.receipt_id != f"capability-ownership-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise CapabilityOwnershipError(
                "Capability ownership receipt does not match its graph."
            )

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "graph_id": self.graph_id,
                "graph_hash": self.graph_hash,
                "ir_id": self.ir_id,
                "constitutional_report_id": self.constitutional_report_id,
                "constitutional_receipt_id": self.constitutional_receipt_id,
                "authority_identity": self.authority_identity,
                "event_ids": list(self.event_ids),
                "stream_version": self.stream_version,
                "capability_count": self.capability_count,
                "outcome": self.outcome,
            }
        )


@dataclass(frozen=True, slots=True)
class CapabilityOwnershipInvalidation:
    invalidation_id: str
    invalidation_hash: str
    graph_ref: str
    constitutional_report_ref: str
    upstream_invalidation_ref: str
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        graph_ref: str,
        constitutional_report_ref: str,
        upstream_invalidation_ref: str,
        reason: str,
        authority_identity: str,
    ) -> "CapabilityOwnershipInvalidation":
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            graph_ref=graph_ref,
            constitutional_report_ref=constitutional_report_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            reason=reason,
            authority_identity=authority_identity,
        )
        if not all(
            value.strip()
            for value in (
                invalidation_id,
                graph_ref,
                constitutional_report_ref,
                upstream_invalidation_ref,
                reason,
                authority_identity,
            )
        ):
            raise CapabilityOwnershipError(
                "Capability ownership invalidation identity is incomplete."
            )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "invalidation_id": self.invalidation_id,
                "graph_ref": self.graph_ref,
                "constitutional_report_ref": self.constitutional_report_ref,
                "upstream_invalidation_ref": self.upstream_invalidation_ref,
                "reason": self.reason,
                "authority_identity": self.authority_identity,
            }
        )


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
