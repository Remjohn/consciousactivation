from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.domain.evidence_index import EvidenceIndex, SpecimenStatus
from cmf_builder.domain.evidence_workspace import SourceLock


SATURATION_VERSION = "1.0.0"


class SaturationError(Exception):
    code = "SaturationError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class SaturationContractInvalid(SaturationError):
    code = "SaturationContractInvalid"


class SaturationInputInvalid(SaturationError):
    code = "SaturationInputInvalid"


class SaturationEvaluationInvalid(SaturationError):
    code = "SaturationEvaluationInvalid"


class SaturationEvaluationInvalidated(SaturationError):
    code = "SaturationEvaluationInvalidated"


class SaturationOutcome(str, Enum):
    PASS = "PASS"
    PASS_WITH_LIMITATIONS = "PASS_WITH_LIMITATIONS"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    BLOCKED_CONTRADICTORY_AUTHORITY = "BLOCKED_CONTRADICTORY_AUTHORITY"
    INSUFFICIENT_TARGET_EVIDENCE = "INSUFFICIENT_TARGET_EVIDENCE"


class DownstreamConsequence(str, Enum):
    PROCEED = "PROCEED"
    PROCEED_PROVISIONALLY = "PROCEED_PROVISIONALLY"
    BLOCK = "BLOCK"


class GapKind(str, Enum):
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    UNREADABLE_EVIDENCE = "UNREADABLE_EVIDENCE"
    SPARSE_TARGET_EVIDENCE = "SPARSE_TARGET_EVIDENCE"
    CONTRADICTORY_SOURCES = "CONTRADICTORY_SOURCES"
    UNRESOLVED_PROVENANCE = "UNRESOLVED_PROVENANCE"
    CRITICAL_CLAIM_WITHOUT_EVIDENCE = "CRITICAL_CLAIM_WITHOUT_EVIDENCE"
    NONCRITICAL_LIMITATION = "NONCRITICAL_LIMITATION"


class ConcernKind(str, Enum):
    CONTRADICTORY_SOURCES = "CONTRADICTORY_SOURCES"
    CONTRADICTORY_AUTHORITY = "CONTRADICTORY_AUTHORITY"
    UNRESOLVED_PROVENANCE = "UNRESOLVED_PROVENANCE"
    CRITICAL_CLAIM_WITHOUT_EVIDENCE = "CRITICAL_CLAIM_WITHOUT_EVIDENCE"
    NONCRITICAL_LIMITATION = "NONCRITICAL_LIMITATION"


@dataclass(frozen=True, slots=True)
class SaturationContract:
    contract_id: str
    contract_hash: str
    version: str
    source_profile_ref: str
    required_roles: tuple[str, ...]
    minimum_distinct_source_ids: int
    minimum_distinct_content_hashes: int
    specimens_per_required_role: int
    required_evidence_categories: tuple[str, ...]
    visual_syntax_applicability: str
    human_reaction_applicability: str
    prior_art_applicability: str
    allowed_outcomes: tuple[SaturationOutcome, ...]
    amendment_rule: str
    production_eligible: bool = False
    certified: bool = False

    @classmethod
    def create(
        cls,
        *,
        contract_id: str,
        source_profile_ref: str,
        required_roles: tuple[str, ...],
        minimum_distinct_source_ids: int = 1,
        minimum_distinct_content_hashes: int = 1,
        specimens_per_required_role: int = 1,
        required_evidence_categories: tuple[str, ...] = (
            "descriptor_metadata",
            "authority",
            "license",
            "privacy",
            "provenance",
            "traceability",
        ),
        visual_syntax_applicability: str = "NOT_APPLICABLE",
        human_reaction_applicability: str = "NOT_APPLICABLE",
        prior_art_applicability: str = "NOT_APPLICABLE_SYNTHETIC_TASK_DEFINITION",
        amendment_rule: str = "any_change_requires_a_new_immutable_contract_version",
        version: str = SATURATION_VERSION,
    ) -> "SaturationContract":
        allowed = tuple(SaturationOutcome)
        base = {
            "amendment_rule": amendment_rule,
            "allowed_outcomes": [item.value for item in allowed],
            "certified": False,
            "contract_id": contract_id,
            "human_reaction_applicability": human_reaction_applicability,
            "minimum_distinct_content_hashes": minimum_distinct_content_hashes,
            "minimum_distinct_source_ids": minimum_distinct_source_ids,
            "prior_art_applicability": prior_art_applicability,
            "production_eligible": False,
            "required_evidence_categories": sorted(required_evidence_categories),
            "required_roles": sorted(required_roles),
            "source_profile_ref": source_profile_ref,
            "specimens_per_required_role": specimens_per_required_role,
            "version": version,
            "visual_syntax_applicability": visual_syntax_applicability,
        }
        contract = cls(
            contract_id=contract_id,
            contract_hash=f"sha256:{sha256(_canonical_json(base)).hexdigest()}",
            version=version,
            source_profile_ref=source_profile_ref,
            required_roles=tuple(sorted(required_roles)),
            minimum_distinct_source_ids=minimum_distinct_source_ids,
            minimum_distinct_content_hashes=minimum_distinct_content_hashes,
            specimens_per_required_role=specimens_per_required_role,
            required_evidence_categories=tuple(sorted(required_evidence_categories)),
            visual_syntax_applicability=visual_syntax_applicability,
            human_reaction_applicability=human_reaction_applicability,
            prior_art_applicability=prior_art_applicability,
            allowed_outcomes=allowed,
            amendment_rule=amendment_rule,
        )
        contract.validate()
        return contract

    def validate(self) -> None:
        if (
            not all(
                value.strip()
                for value in (
                    self.contract_id,
                    self.version,
                    self.source_profile_ref,
                    self.visual_syntax_applicability,
                    self.human_reaction_applicability,
                    self.prior_art_applicability,
                    self.amendment_rule,
                )
            )
            or self.version != SATURATION_VERSION
            or not self.required_roles
            or len(set(self.required_roles)) != len(self.required_roles)
            or self.minimum_distinct_source_ids <= 0
            or self.minimum_distinct_content_hashes <= 0
            or self.specimens_per_required_role <= 0
            or not self.required_evidence_categories
            or set(self.required_evidence_categories)
            != {
                "descriptor_metadata",
                "authority",
                "license",
                "privacy",
                "provenance",
                "traceability",
            }
            or tuple(self.allowed_outcomes) != tuple(SaturationOutcome)
            or self.production_eligible
            or self.certified
        ):
            raise SaturationContractInvalid("Saturation Contract fields are invalid.")
        for applicability in (
            self.visual_syntax_applicability,
            self.human_reaction_applicability,
            self.prior_art_applicability,
        ):
            if applicability.startswith("NOT_APPLICABLE") is False:
                raise SaturationContractInvalid(
                    "The synthetic contract cannot activate category or prior-art evidence."
                )
        expected = sha256(_canonical_json(self._identity_payload())).hexdigest()
        if self.contract_hash != f"sha256:{expected}":
            raise SaturationContractInvalid(
                "Saturation Contract identity differs from its canonical bytes."
            )

    def _identity_payload(self) -> dict[str, object]:
        return {
            "amendment_rule": self.amendment_rule,
            "allowed_outcomes": [item.value for item in self.allowed_outcomes],
            "certified": self.certified,
            "contract_id": self.contract_id,
            "human_reaction_applicability": self.human_reaction_applicability,
            "minimum_distinct_content_hashes": self.minimum_distinct_content_hashes,
            "minimum_distinct_source_ids": self.minimum_distinct_source_ids,
            "prior_art_applicability": self.prior_art_applicability,
            "production_eligible": self.production_eligible,
            "required_evidence_categories": list(self.required_evidence_categories),
            "required_roles": list(self.required_roles),
            "source_profile_ref": self.source_profile_ref,
            "specimens_per_required_role": self.specimens_per_required_role,
            "version": self.version,
            "visual_syntax_applicability": self.visual_syntax_applicability,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json({**self._identity_payload(), "contract_hash": self.contract_hash})


@dataclass(frozen=True, slots=True)
class SaturationConcern:
    concern_id: str
    kind: ConcernKind
    evidence_refs: tuple[str, ...]
    detail_code: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        kind: ConcernKind,
        evidence_refs: tuple[str, ...],
        detail_code: str,
        authority_identity: str,
    ) -> "SaturationConcern":
        base = {
            "authority_identity": authority_identity,
            "detail_code": detail_code,
            "evidence_refs": sorted(evidence_refs),
            "kind": kind.value,
        }
        concern = cls(
            concern_id=f"saturation-concern_{sha256(_canonical_json(base)).hexdigest()}",
            kind=kind,
            evidence_refs=tuple(sorted(evidence_refs)),
            detail_code=detail_code,
            authority_identity=authority_identity,
        )
        concern.validate()
        return concern

    def validate(self) -> None:
        if not self.detail_code.strip() or not self.authority_identity.strip():
            raise SaturationInputInvalid("A saturation concern requires governed detail and authority.")
        if self.kind not in {
            ConcernKind.CRITICAL_CLAIM_WITHOUT_EVIDENCE,
            ConcernKind.NONCRITICAL_LIMITATION,
        } and not self.evidence_refs:
            raise SaturationInputInvalid("This concern requires exact evidence references.")
        if (
            self.kind is ConcernKind.CRITICAL_CLAIM_WITHOUT_EVIDENCE
            and self.evidence_refs
        ):
            raise SaturationInputInvalid(
                "A critical-claim-without-evidence record cannot cite supporting evidence."
            )
        base = {
            "authority_identity": self.authority_identity,
            "detail_code": self.detail_code,
            "evidence_refs": list(self.evidence_refs),
            "kind": self.kind.value,
        }
        if self.concern_id != f"saturation-concern_{sha256(_canonical_json(base)).hexdigest()}":
            raise SaturationInputInvalid("Saturation concern identity is invalid.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "authority_identity": self.authority_identity,
            "concern_id": self.concern_id,
            "detail_code": self.detail_code,
            "evidence_refs": list(self.evidence_refs),
            "kind": self.kind.value,
        }


@dataclass(frozen=True, slots=True)
class RoleCoverage:
    role: str
    specimen_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    content_hashes: tuple[str, ...]
    required_count: int
    observed_count: int
    status: str

    def validate(self, *, index: EvidenceIndex, contract: SaturationContract) -> None:
        selected = tuple(
            item
            for item in index.specimens
            if item.role == self.role and item.governed_status is SpecimenStatus.ACTIVE
        )
        expected_specimens = tuple(sorted(item.specimen_id for item in selected))
        expected_sources = tuple(sorted({item.source_id for item in selected}))
        expected_hashes = tuple(sorted({item.source_content_hash for item in selected}))
        if not selected:
            expected_status = "MISSING"
        elif len(selected) < contract.specimens_per_required_role:
            expected_status = "SPARSE"
        else:
            expected_status = "COMPLETE"
        all_for_role = tuple(item for item in index.specimens if item.role == self.role)
        if all_for_role and len(selected) != len(all_for_role):
            expected_status = "UNREADABLE"
        if (
            self.role not in contract.required_roles
            or self.specimen_ids != expected_specimens
            or self.source_ids != expected_sources
            or self.content_hashes != expected_hashes
            or self.required_count != contract.specimens_per_required_role
            or self.observed_count != len(selected)
            or self.status != expected_status
        ):
            raise SaturationEvaluationInvalid("Role coverage differs from active evidence.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "content_hashes": list(self.content_hashes),
            "observed_count": self.observed_count,
            "required_count": self.required_count,
            "role": self.role,
            "source_ids": list(self.source_ids),
            "specimen_ids": list(self.specimen_ids),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class EvidenceGap:
    gap_id: str
    kind: GapKind
    required_role: str | None
    evidence_refs: tuple[str, ...]
    detail_code: str
    blocks: bool

    def validate(self, *, specimen_ids: set[str]) -> None:
        if (
            not self.detail_code.strip()
            or set(self.evidence_refs) - specimen_ids
            or self.kind is GapKind.MISSING_EVIDENCE and self.required_role is None
            or self.kind is GapKind.CRITICAL_CLAIM_WITHOUT_EVIDENCE and self.evidence_refs
        ):
            raise SaturationEvaluationInvalid("Evidence-gap content is invalid.")
        base = {
            "blocks": self.blocks,
            "detail_code": self.detail_code,
            "evidence_refs": list(self.evidence_refs),
            "kind": self.kind.value,
            "required_role": self.required_role,
        }
        if self.gap_id != f"evidence-gap_{sha256(_canonical_json(base)).hexdigest()}":
            raise SaturationEvaluationInvalid("Evidence-gap identity is invalid.")

    @classmethod
    def create(
        cls,
        *,
        kind: GapKind,
        required_role: str | None,
        evidence_refs: tuple[str, ...],
        detail_code: str,
        blocks: bool = True,
    ) -> "EvidenceGap":
        base = {
            "blocks": blocks,
            "detail_code": detail_code,
            "evidence_refs": sorted(evidence_refs),
            "kind": kind.value,
            "required_role": required_role,
        }
        return cls(
            gap_id=f"evidence-gap_{sha256(_canonical_json(base)).hexdigest()}",
            kind=kind,
            required_role=required_role,
            evidence_refs=tuple(sorted(evidence_refs)),
            detail_code=detail_code,
            blocks=blocks,
        )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "blocks": self.blocks,
            "detail_code": self.detail_code,
            "evidence_refs": list(self.evidence_refs),
            "gap_id": self.gap_id,
            "kind": self.kind.value,
            "required_role": self.required_role,
        }


@dataclass(frozen=True, slots=True)
class AuthorityConflict:
    conflict_id: str
    evidence_refs: tuple[str, ...]
    detail_code: str
    source_authorities: tuple[str, ...]

    def validate(self, *, index: EvidenceIndex) -> None:
        specimen_ids = {item.specimen_id for item in index.specimens}
        expected_authorities = tuple(
            sorted(
                {
                    item.provenance.authority
                    for item in index.specimens
                    if item.specimen_id in self.evidence_refs
                }
            )
        )
        if (
            not self.detail_code.strip()
            or not self.evidence_refs
            or set(self.evidence_refs) - specimen_ids
            or self.source_authorities != expected_authorities
        ):
            raise SaturationEvaluationInvalid("Authority-conflict evidence is invalid.")
        base = {
            "detail_code": self.detail_code,
            "evidence_refs": list(self.evidence_refs),
            "source_authorities": list(self.source_authorities),
        }
        if self.conflict_id != f"authority-conflict_{sha256(_canonical_json(base)).hexdigest()}":
            raise SaturationEvaluationInvalid("Authority-conflict identity is invalid.")

    @classmethod
    def create(
        cls,
        *,
        evidence_refs: tuple[str, ...],
        detail_code: str,
        source_authorities: tuple[str, ...],
    ) -> "AuthorityConflict":
        base = {
            "detail_code": detail_code,
            "evidence_refs": sorted(evidence_refs),
            "source_authorities": sorted(source_authorities),
        }
        return cls(
            conflict_id=f"authority-conflict_{sha256(_canonical_json(base)).hexdigest()}",
            evidence_refs=tuple(sorted(evidence_refs)),
            detail_code=detail_code,
            source_authorities=tuple(sorted(source_authorities)),
        )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "conflict_id": self.conflict_id,
            "detail_code": self.detail_code,
            "evidence_refs": list(self.evidence_refs),
            "source_authorities": list(self.source_authorities),
        }


@dataclass(frozen=True, slots=True)
class SaturationEvaluation:
    evaluation_id: str
    evaluation_hash: str
    version: str
    run_id: str
    source_lock_ref: str
    source_lock_hash: str
    evidence_index_ref: str
    evidence_index_hash: str
    contract_id: str
    contract_hash: str
    authority_identity: str
    role_coverage: tuple[RoleCoverage, ...]
    gaps: tuple[EvidenceGap, ...]
    authority_conflicts: tuple[AuthorityConflict, ...]
    outcome: SaturationOutcome
    downstream_consequence: DownstreamConsequence
    human_waiver_ref: str | None
    production_eligible: bool = False
    certified: bool = False

    @classmethod
    def evaluate(
        cls,
        *,
        run_id: str,
        source_lock: SourceLock,
        index: EvidenceIndex,
        contract: SaturationContract,
        authority_identity: str,
        concerns: tuple[SaturationConcern, ...] = (),
        human_waiver_ref: str | None = None,
        waiver_authority_kind: str | None = None,
    ) -> "SaturationEvaluation":
        contract.validate()
        index.validate(source_lock)
        if (
            source_lock.run_id != run_id
            or index.run_id != run_id
            or contract.source_profile_ref != source_lock.source_profile_ref
            or index.source_profile_ref != contract.source_profile_ref
            or not authority_identity.strip()
        ):
            raise SaturationInputInvalid("Saturation lineage or authority is inconsistent.")
        specimen_ids = {item.specimen_id for item in index.specimens}
        for concern in concerns:
            concern.validate()
            if concern.authority_identity != authority_identity:
                raise SaturationInputInvalid(
                    "Concern authority differs from the authorized evaluator."
                )
            unknown = set(concern.evidence_refs) - specimen_ids
            if unknown:
                raise SaturationInputInvalid(
                    "A concern cites evidence outside the active index.",
                    unknown_evidence_refs=tuple(sorted(unknown)),
                )

        coverage: list[RoleCoverage] = []
        gaps: list[EvidenceGap] = []
        for role in contract.required_roles:
            selected = tuple(item for item in index.specimens if item.role == role)
            active = tuple(item for item in selected if item.governed_status is SpecimenStatus.ACTIVE)
            status = "COMPLETE"
            if not selected:
                status = "MISSING"
                gaps.append(
                    EvidenceGap.create(
                        kind=GapKind.MISSING_EVIDENCE,
                        required_role=role,
                        evidence_refs=(),
                        detail_code="required_role_absent",
                    )
                )
            elif len(active) != len(selected):
                status = "UNREADABLE"
                gaps.append(
                    EvidenceGap.create(
                        kind=GapKind.UNREADABLE_EVIDENCE,
                        required_role=role,
                        evidence_refs=tuple(item.specimen_id for item in selected if item not in active),
                        detail_code="required_role_contains_non_active_specimen",
                    )
                )
            elif len(active) < contract.specimens_per_required_role:
                status = "SPARSE"
                gaps.append(
                    EvidenceGap.create(
                        kind=GapKind.SPARSE_TARGET_EVIDENCE,
                        required_role=role,
                        evidence_refs=tuple(item.specimen_id for item in active),
                        detail_code="minimum_specimens_per_role_not_met",
                    )
                )
            coverage.append(
                RoleCoverage(
                    role=role,
                    specimen_ids=tuple(sorted(item.specimen_id for item in active)),
                    source_ids=tuple(sorted({item.source_id for item in active})),
                    content_hashes=tuple(sorted({item.source_content_hash for item in active})),
                    required_count=contract.specimens_per_required_role,
                    observed_count=len(active),
                    status=status,
                )
            )

        all_source_ids = {item.source_id for item in index.specimens}
        all_content_hashes = {item.source_content_hash for item in index.specimens}
        if (
            len(all_source_ids) < contract.minimum_distinct_source_ids
            or len(all_content_hashes) < contract.minimum_distinct_content_hashes
        ):
            gaps.append(
                EvidenceGap.create(
                    kind=GapKind.SPARSE_TARGET_EVIDENCE,
                    required_role=None,
                    evidence_refs=tuple(sorted(specimen_ids)),
                    detail_code="minimum_global_diversity_not_met",
                )
            )

        conflicts: list[AuthorityConflict] = []
        for concern in sorted(concerns, key=lambda item: item.concern_id):
            if concern.kind is ConcernKind.CONTRADICTORY_AUTHORITY:
                authorities = tuple(
                    sorted(
                        {
                            item.provenance.authority
                            for item in index.specimens
                            if item.specimen_id in concern.evidence_refs
                        }
                    )
                )
                conflicts.append(
                    AuthorityConflict.create(
                        evidence_refs=concern.evidence_refs,
                        detail_code=concern.detail_code,
                        source_authorities=authorities,
                    )
                )
            elif concern.kind is ConcernKind.CONTRADICTORY_SOURCES:
                gaps.append(
                    EvidenceGap.create(
                        kind=GapKind.CONTRADICTORY_SOURCES,
                        required_role=None,
                        evidence_refs=concern.evidence_refs,
                        detail_code=concern.detail_code,
                    )
                )
            elif concern.kind is ConcernKind.UNRESOLVED_PROVENANCE:
                gaps.append(
                    EvidenceGap.create(
                        kind=GapKind.UNRESOLVED_PROVENANCE,
                        required_role=None,
                        evidence_refs=concern.evidence_refs,
                        detail_code=concern.detail_code,
                    )
                )
            elif concern.kind is ConcernKind.CRITICAL_CLAIM_WITHOUT_EVIDENCE:
                gaps.append(
                    EvidenceGap.create(
                        kind=GapKind.CRITICAL_CLAIM_WITHOUT_EVIDENCE,
                        required_role=None,
                        evidence_refs=(),
                        detail_code=concern.detail_code,
                    )
                )
            elif concern.kind is ConcernKind.NONCRITICAL_LIMITATION:
                gaps.append(
                    EvidenceGap.create(
                        kind=GapKind.NONCRITICAL_LIMITATION,
                        required_role=None,
                        evidence_refs=concern.evidence_refs,
                        detail_code=concern.detail_code,
                        blocks=human_waiver_ref is None,
                    )
                )

        kinds = {item.kind for item in gaps}
        if conflicts:
            outcome = SaturationOutcome.BLOCKED_CONTRADICTORY_AUTHORITY
        elif kinds & {
            GapKind.MISSING_EVIDENCE,
            GapKind.UNREADABLE_EVIDENCE,
            GapKind.UNRESOLVED_PROVENANCE,
            GapKind.CRITICAL_CLAIM_WITHOUT_EVIDENCE,
        }:
            outcome = SaturationOutcome.BLOCKED_MISSING_EVIDENCE
        elif kinds & {
            GapKind.SPARSE_TARGET_EVIDENCE,
            GapKind.CONTRADICTORY_SOURCES,
        }:
            outcome = SaturationOutcome.INSUFFICIENT_TARGET_EVIDENCE
        elif GapKind.NONCRITICAL_LIMITATION in kinds:
            if human_waiver_ref is None or waiver_authority_kind != "HUMAN":
                outcome = SaturationOutcome.INSUFFICIENT_TARGET_EVIDENCE
            else:
                outcome = SaturationOutcome.PASS_WITH_LIMITATIONS
        else:
            outcome = SaturationOutcome.PASS
        consequence = {
            SaturationOutcome.PASS: DownstreamConsequence.PROCEED,
            SaturationOutcome.PASS_WITH_LIMITATIONS: DownstreamConsequence.PROCEED_PROVISIONALLY,
            SaturationOutcome.BLOCKED_MISSING_EVIDENCE: DownstreamConsequence.BLOCK,
            SaturationOutcome.BLOCKED_CONTRADICTORY_AUTHORITY: DownstreamConsequence.BLOCK,
            SaturationOutcome.INSUFFICIENT_TARGET_EVIDENCE: DownstreamConsequence.BLOCK,
        }[outcome]
        base = {
            "authority_conflicts": [item.canonical_dict() for item in sorted(conflicts, key=lambda item: item.conflict_id)],
            "authority_identity": authority_identity,
            "certified": False,
            "contract_hash": contract.contract_hash,
            "contract_id": contract.contract_id,
            "downstream_consequence": consequence.value,
            "evidence_index_hash": index.index_hash,
            "evidence_index_ref": index.index_id,
            "gaps": [item.canonical_dict() for item in sorted(gaps, key=lambda item: item.gap_id)],
            "human_waiver_ref": human_waiver_ref,
            "outcome": outcome.value,
            "production_eligible": False,
            "role_coverage": [item.canonical_dict() for item in sorted(coverage, key=lambda item: item.role)],
            "run_id": run_id,
            "source_lock_hash": source_lock.aggregate_hash,
            "source_lock_ref": source_lock.lock_id,
            "version": SATURATION_VERSION,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        evaluation = cls(
            evaluation_id=f"saturation-evaluation_{digest}",
            evaluation_hash=f"sha256:{digest}",
            version=SATURATION_VERSION,
            run_id=run_id,
            source_lock_ref=source_lock.lock_id,
            source_lock_hash=source_lock.aggregate_hash,
            evidence_index_ref=index.index_id,
            evidence_index_hash=index.index_hash,
            contract_id=contract.contract_id,
            contract_hash=contract.contract_hash,
            authority_identity=authority_identity,
            role_coverage=tuple(sorted(coverage, key=lambda item: item.role)),
            gaps=tuple(sorted(gaps, key=lambda item: item.gap_id)),
            authority_conflicts=tuple(sorted(conflicts, key=lambda item: item.conflict_id)),
            outcome=outcome,
            downstream_consequence=consequence,
            human_waiver_ref=human_waiver_ref,
        )
        evaluation.validate(source_lock=source_lock, index=index, contract=contract)
        return evaluation

    def validate(
        self, *, source_lock: SourceLock, index: EvidenceIndex, contract: SaturationContract
    ) -> None:
        contract.validate()
        index.validate(source_lock)
        if (
            self.version != SATURATION_VERSION
            or self.run_id != source_lock.run_id
            or self.run_id != index.run_id
            or self.source_lock_ref != source_lock.lock_id
            or self.source_lock_hash != source_lock.aggregate_hash
            or self.evidence_index_ref != index.index_id
            or self.evidence_index_hash != index.index_hash
            or self.contract_id != contract.contract_id
            or self.contract_hash != contract.contract_hash
            or not self.authority_identity.strip()
            or self.outcome not in contract.allowed_outcomes
            or self.production_eligible
            or self.certified
        ):
            raise SaturationEvaluationInvalid("Saturation evaluation lineage or classification is invalid.")
        if (
            tuple(item.role for item in self.role_coverage) != contract.required_roles
            or len({item.role for item in self.role_coverage}) != len(self.role_coverage)
            or len({item.gap_id for item in self.gaps}) != len(self.gaps)
            or len({item.conflict_id for item in self.authority_conflicts})
            != len(self.authority_conflicts)
        ):
            raise SaturationEvaluationInvalid("Saturation coverage, gap or conflict cardinality is invalid.")
        for coverage in self.role_coverage:
            coverage.validate(index=index, contract=contract)
        specimen_ids = {item.specimen_id for item in index.specimens}
        for gap in self.gaps:
            gap.validate(specimen_ids=specimen_ids)
        for conflict in self.authority_conflicts:
            conflict.validate(index=index)
        kinds = {item.kind for item in self.gaps}
        if self.authority_conflicts:
            expected_outcome = SaturationOutcome.BLOCKED_CONTRADICTORY_AUTHORITY
        elif kinds & {
            GapKind.MISSING_EVIDENCE,
            GapKind.UNREADABLE_EVIDENCE,
            GapKind.UNRESOLVED_PROVENANCE,
            GapKind.CRITICAL_CLAIM_WITHOUT_EVIDENCE,
        }:
            expected_outcome = SaturationOutcome.BLOCKED_MISSING_EVIDENCE
        elif kinds & {GapKind.SPARSE_TARGET_EVIDENCE, GapKind.CONTRADICTORY_SOURCES}:
            expected_outcome = SaturationOutcome.INSUFFICIENT_TARGET_EVIDENCE
        elif GapKind.NONCRITICAL_LIMITATION in kinds:
            expected_outcome = (
                SaturationOutcome.PASS_WITH_LIMITATIONS
                if self.human_waiver_ref
                else SaturationOutcome.INSUFFICIENT_TARGET_EVIDENCE
            )
        else:
            expected_outcome = SaturationOutcome.PASS
        expected_consequence = {
            SaturationOutcome.PASS: DownstreamConsequence.PROCEED,
            SaturationOutcome.PASS_WITH_LIMITATIONS: DownstreamConsequence.PROCEED_PROVISIONALLY,
            SaturationOutcome.BLOCKED_MISSING_EVIDENCE: DownstreamConsequence.BLOCK,
            SaturationOutcome.BLOCKED_CONTRADICTORY_AUTHORITY: DownstreamConsequence.BLOCK,
            SaturationOutcome.INSUFFICIENT_TARGET_EVIDENCE: DownstreamConsequence.BLOCK,
        }[expected_outcome]
        if self.outcome is not expected_outcome or self.downstream_consequence is not expected_consequence:
            raise SaturationEvaluationInvalid("Typed saturation outcome differs from governed evidence.")
        if self.human_waiver_ref is not None and self.outcome is not SaturationOutcome.PASS_WITH_LIMITATIONS:
            raise SaturationEvaluationInvalid("A human waiver may apply only to a limitations outcome.")
        digest = sha256(_canonical_json(self._identity_payload())).hexdigest()
        if self.evaluation_id != f"saturation-evaluation_{digest}" or self.evaluation_hash != f"sha256:{digest}":
            raise SaturationEvaluationInvalid("Saturation evaluation identity differs from canonical bytes.")

    def _identity_payload(self) -> dict[str, object]:
        return {
            "authority_conflicts": [item.canonical_dict() for item in self.authority_conflicts],
            "authority_identity": self.authority_identity,
            "certified": self.certified,
            "contract_hash": self.contract_hash,
            "contract_id": self.contract_id,
            "downstream_consequence": self.downstream_consequence.value,
            "evidence_index_hash": self.evidence_index_hash,
            "evidence_index_ref": self.evidence_index_ref,
            "gaps": [item.canonical_dict() for item in self.gaps],
            "human_waiver_ref": self.human_waiver_ref,
            "outcome": self.outcome.value,
            "production_eligible": self.production_eligible,
            "role_coverage": [item.canonical_dict() for item in self.role_coverage],
            "run_id": self.run_id,
            "source_lock_hash": self.source_lock_hash,
            "source_lock_ref": self.source_lock_ref,
            "version": self.version,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {**self._identity_payload(), "evaluation_hash": self.evaluation_hash, "evaluation_id": self.evaluation_id}
        )


@dataclass(frozen=True, slots=True)
class SaturationReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    run_id: str
    evaluation_id: str
    evaluation_hash: str
    contract_id: str
    contract_hash: str
    outcome: SaturationOutcome
    downstream_consequence: DownstreamConsequence
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        evaluation: SaturationEvaluation,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "SaturationReceipt":
        base = {
            "authority_identity": evaluation.authority_identity,
            "command_id": command_id,
            "contract_hash": evaluation.contract_hash,
            "contract_id": evaluation.contract_id,
            "downstream_consequence": evaluation.downstream_consequence.value,
            "evaluation_hash": evaluation.evaluation_hash,
            "evaluation_id": evaluation.evaluation_id,
            "event_ids": list(event_ids),
            "outcome": evaluation.outcome.value,
            "run_id": evaluation.run_id,
            "stream_version": stream_version,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        return cls(
            receipt_id=f"saturation-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
            command_id=command_id,
            run_id=evaluation.run_id,
            evaluation_id=evaluation.evaluation_id,
            evaluation_hash=evaluation.evaluation_hash,
            contract_id=evaluation.contract_id,
            contract_hash=evaluation.contract_hash,
            outcome=evaluation.outcome,
            downstream_consequence=evaluation.downstream_consequence,
            authority_identity=evaluation.authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
        )

    def validate(self, evaluation: SaturationEvaluation) -> None:
        base = {
            "authority_identity": self.authority_identity,
            "command_id": self.command_id,
            "contract_hash": self.contract_hash,
            "contract_id": self.contract_id,
            "downstream_consequence": self.downstream_consequence.value,
            "evaluation_hash": self.evaluation_hash,
            "evaluation_id": self.evaluation_id,
            "event_ids": list(self.event_ids),
            "outcome": self.outcome.value,
            "run_id": self.run_id,
            "stream_version": self.stream_version,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        if (
            self.run_id != evaluation.run_id
            or self.evaluation_id != evaluation.evaluation_id
            or self.evaluation_hash != evaluation.evaluation_hash
            or self.contract_id != evaluation.contract_id
            or self.contract_hash != evaluation.contract_hash
            or self.outcome is not evaluation.outcome
            or self.downstream_consequence is not evaluation.downstream_consequence
            or self.authority_identity != evaluation.authority_identity
            or self.receipt_id != f"saturation-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise SaturationEvaluationInvalid("Saturation receipt differs from its evaluation.")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "authority_identity": self.authority_identity,
                "command_id": self.command_id,
                "contract_hash": self.contract_hash,
                "contract_id": self.contract_id,
                "downstream_consequence": self.downstream_consequence.value,
                "evaluation_hash": self.evaluation_hash,
                "evaluation_id": self.evaluation_id,
                "event_ids": list(self.event_ids),
                "outcome": self.outcome.value,
                "receipt_hash": self.receipt_hash,
                "receipt_id": self.receipt_id,
                "run_id": self.run_id,
                "stream_version": self.stream_version,
            }
        )


@dataclass(frozen=True, slots=True)
class SaturationInvalidation:
    invalidation_id: str
    invalidation_hash: str
    command_id: str
    run_id: str
    evaluation_id: str
    evaluation_hash: str
    authority_identity: str
    reason: str
    event_ids: tuple[str, ...]
    stream_version: int

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        evaluation: SaturationEvaluation,
        authority_identity: str,
        reason: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "SaturationInvalidation":
        if not reason.strip():
            raise SaturationInputInvalid("Invalidation requires a governed reason.")
        base = {
            "authority_identity": authority_identity,
            "command_id": command_id,
            "evaluation_hash": evaluation.evaluation_hash,
            "evaluation_id": evaluation.evaluation_id,
            "event_ids": list(event_ids),
            "reason": reason,
            "run_id": evaluation.run_id,
            "stream_version": stream_version,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        return cls(
            invalidation_id=f"saturation-invalidation_{digest}",
            invalidation_hash=f"sha256:{digest}",
            command_id=command_id,
            run_id=evaluation.run_id,
            evaluation_id=evaluation.evaluation_id,
            evaluation_hash=evaluation.evaluation_hash,
            authority_identity=authority_identity,
            reason=reason,
            event_ids=event_ids,
            stream_version=stream_version,
        )

    def validate(self, evaluation: SaturationEvaluation) -> None:
        base = {
            "authority_identity": self.authority_identity,
            "command_id": self.command_id,
            "evaluation_hash": self.evaluation_hash,
            "evaluation_id": self.evaluation_id,
            "event_ids": list(self.event_ids),
            "reason": self.reason,
            "run_id": self.run_id,
            "stream_version": self.stream_version,
        }
        digest = sha256(_canonical_json(base)).hexdigest()
        if (
            self.run_id != evaluation.run_id
            or self.evaluation_id != evaluation.evaluation_id
            or self.evaluation_hash != evaluation.evaluation_hash
            or self.invalidation_id != f"saturation-invalidation_{digest}"
            or self.invalidation_hash != f"sha256:{digest}"
        ):
            raise SaturationEvaluationInvalid("Saturation invalidation identity is invalid.")


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
