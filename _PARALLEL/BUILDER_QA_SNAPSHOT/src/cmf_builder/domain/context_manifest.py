from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.domain.handoff import (
    InternalHandoff,
    InternalHandoffDecision,
    InternalHandoffDecisionAction,
    PhaseHandoffGraph,
)
from cmf_builder.domain.phase_graph import PhaseGraph


MINIMUM_CONTEXT_INPUT_PATH = "development-capsules/ST-04.05/MINIMUM_CONTEXT_INPUT.json"
MINIMUM_CONTEXT_INPUT_SHA256 = (
    "bf44fa7595ab064ac47654addf73a6a930687ce1f04e6ef05fa0c2c14c6d30ab"
)
MINIMUM_CONTEXT_INPUT_SCHEMA = "cmf-builder-synthetic-minimum-context-input/v1"
MINIMUM_CONTEXT_SCOPE = "ST-04.05_SYNTHETIC_MINIMUM_COMPLETE_CONTEXT_ONLY"
PHASE_HANDOFF_CONTRACT = "cmf-builder-phase-handoff-graph/v1@1.0.0"
MINIMUM_CONTEXT_GRAPH_SCHEMA_ID = "cmf-builder-minimum-complete-context-graph/v1"
MINIMUM_CONTEXT_GRAPH_SCHEMA_VERSION = "1.0.0"
PHASE_CONTEXT_MANIFEST_SCHEMA_ID = "cmf-builder-phase-context-manifest/v1"
CONTEXT_COMPILATION_RECEIPT_SCHEMA_ID = "cmf-builder-context-compilation-receipt/v1"

GOVERNED_PRIORITY_ORDER = (
    "phase_responsibility",
    "output_contract",
    "ratified_decision",
    "binding",
    "canonical_procedure",
    "harness_adaptation",
    "direct_evidence",
    "constraint",
    "conditional_reference",
    "example",
    "enrichment",
)
MANIFEST_CATEGORIES = ("included", "excluded", "summarized", "retrieved", "compressed")
OVERFLOW_REMEDIATION_CHOICES = (
    "ISSUE_NEW_GOVERNED_BUDGET_POLICY_VERSION",
    "ISSUE_NEW_CONTEXT_INPUT_VERSION_WITH_NON_REQUIRED_CONTEXT_REMOVED",
    "ISSUE_NEW_PHASE_GRAPH_VERSION_WITH_NARROWER_RESPONSIBILITY",
)


class ContextError(Exception):
    code = "ContextError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class ContextInputInvalid(ContextError):
    code = "ContextInputInvalid"


class ContextContractInvalid(ContextError):
    code = "ContextContractInvalid"


class ContextAuthorityInvalid(ContextError):
    code = "ContextAuthorityInvalid"


class ContextLineageInvalid(ContextError):
    code = "ContextLineageInvalid"


class ContextStateInvalid(ContextError):
    code = "ContextStateInvalid"


class ContextInvalidatedError(ContextError):
    code = "ContextInvalidated"


class ContextBudgetOverflow(ContextError):
    code = "ContextBudgetOverflow"


class ContextDisposition(str, Enum):
    REQUIRED = "REQUIRED"
    CONDITIONAL = "CONDITIONALLY_REQUIRED"
    OPTIONAL = "OPTIONAL"
    FORBIDDEN = "FORBIDDEN"
    UNAVAILABLE_NON_REQUIRED = "UNAVAILABLE_NON_REQUIRED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


def _unique(values: tuple[str, ...], label: str, *, allow_empty: bool = False) -> None:
    if (
        (not values and not allow_empty)
        or any(not value.strip() for value in values)
        or len(values) != len(set(values))
    ):
        raise ContextContractInvalid(f"{label} must contain unique non-empty values.")


def _sha256(value: str, label: str) -> None:
    if not value.startswith("sha256:") or len(value) != 71:
        raise ContextContractInvalid(f"{label} must be a lowercase SHA-256 identity.")
    try:
        int(value[7:], 16)
    except ValueError as error:
        raise ContextContractInvalid(f"{label} must be a lowercase SHA-256 identity.") from error
    if value[7:] != value[7:].lower():
        raise ContextContractInvalid(f"{label} must be a lowercase SHA-256 identity.")


@dataclass(frozen=True, slots=True)
class BudgetLimit:
    tokens: int
    latency_ms: int
    cost_microunits: int

    def __post_init__(self) -> None:
        if self.tokens < 0 or self.latency_ms < 0 or self.cost_microunits < 0:
            raise ContextContractInvalid("Context budgets cannot be negative.")

    def canonical_dict(self) -> dict[str, int]:
        return {
            "tokens": self.tokens,
            "latency_ms": self.latency_ms,
            "cost_microunits": self.cost_microunits,
        }


@dataclass(frozen=True, slots=True)
class ReferenceDeclaration:
    reference_id: str
    version: str
    integrity_source: str
    owner: str
    authority: str
    content_role: str
    loading_mode: str
    allowed_phases: tuple[str, ...]
    may_influence: tuple[str, ...]
    must_not_influence: tuple[str, ...]
    progressive_disclosure_pointer: str | None = None
    semantic_status: str = "APPLICABLE"

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.reference_id,
                self.version,
                self.integrity_source,
                self.owner,
                self.authority,
                self.content_role,
                self.loading_mode,
            )
        ):
            raise ContextContractInvalid("Reference identity, ownership, authority, and loading are required.")
        _unique(self.allowed_phases, "Allowed phases", allow_empty=True)
        _unique(self.may_influence, "May-influence boundaries", allow_empty=True)
        _unique(self.must_not_influence, "Must-not-influence boundaries", allow_empty=True)
        if set(self.may_influence) & set(self.must_not_influence):
            raise ContextContractInvalid("Reference influence boundaries cannot conflict.")
        if self.loading_mode not in {"phase_local", "retrieval_only", "forbidden_at_runtime"}:
            raise ContextContractInvalid("Reference loading mode is not governed.")
        if self.semantic_status not in {"APPLICABLE", "NOT_APPLICABLE"}:
            raise ContextContractInvalid("Reference semantic status is not governed.")
        if self.semantic_status == "NOT_APPLICABLE" and (
            self.allowed_phases or self.loading_mode != "forbidden_at_runtime"
        ):
            raise ContextContractInvalid("NOT_APPLICABLE context must be explicitly forbidden at runtime.")
        if self.loading_mode == "retrieval_only" and not (
            self.progressive_disclosure_pointer and self.progressive_disclosure_pointer.strip()
        ):
            raise ContextContractInvalid("Retrieval-only context requires an immutable typed pointer.")
        if self.loading_mode != "retrieval_only" and self.progressive_disclosure_pointer is not None:
            raise ContextContractInvalid("Only retrieval-only references may declare progressive disclosure pointers.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "reference_id": self.reference_id,
            "version": self.version,
            "integrity_source": self.integrity_source,
            "owner": self.owner,
            "authority": self.authority,
            "content_role": self.content_role,
            "loading_mode": self.loading_mode,
            "allowed_phases": list(self.allowed_phases),
            "may_influence": list(self.may_influence),
            "must_not_influence": list(self.must_not_influence),
            "progressive_disclosure_pointer": self.progressive_disclosure_pointer,
            "semantic_status": self.semantic_status,
        }


@dataclass(frozen=True, slots=True)
class ContextBudgetPolicy:
    phase_ref: str
    required_references: tuple[str, ...]
    optional_references: tuple[str, ...]
    excluded_references: tuple[str, ...]
    hard_budget: BudgetLimit
    soft_budget: BudgetLimit
    governed_token_contributions: tuple[tuple[str, int], ...]
    compression_permissions: tuple[str, ...]
    retrieval_policy: str
    overflow_behavior: str

    def __post_init__(self) -> None:
        if not self.phase_ref.strip():
            raise ContextContractInvalid("Context budget policy requires a phase identity.")
        _unique(self.required_references, "Required references")
        _unique(self.optional_references, "Optional references", allow_empty=True)
        _unique(self.excluded_references, "Excluded references", allow_empty=True)
        _unique(self.compression_permissions, "Compression permissions", allow_empty=True)
        groups = (
            set(self.required_references),
            set(self.optional_references),
            set(self.excluded_references),
        )
        if (groups[0] & groups[1]) or (groups[0] & groups[2]) or (groups[1] & groups[2]):
            raise ContextContractInvalid("Required, optional, and excluded context must remain distinct.")
        names = tuple(name for name, _ in self.governed_token_contributions)
        _unique(names, "Governed token contributions", allow_empty=True)
        if any(tokens < 0 for _, tokens in self.governed_token_contributions):
            raise ContextContractInvalid("Governed token contributions cannot be negative.")
        if set(names) != set((*self.required_references, *self.optional_references)):
            raise ContextContractInvalid("Every selectable context reference requires one governed token contribution.")
        if self.soft_budget.tokens > self.hard_budget.tokens:
            raise ContextContractInvalid("Soft token budget cannot exceed the hard budget.")
        if self.soft_budget.latency_ms > self.hard_budget.latency_ms:
            raise ContextContractInvalid("Soft latency budget cannot exceed the hard budget.")
        if self.soft_budget.cost_microunits > self.hard_budget.cost_microunits:
            raise ContextContractInvalid("Soft cost budget cannot exceed the hard budget.")
        if self.retrieval_policy not in {"PROHIBITED", "POINTER_ONLY_NO_RUNTIME_FETCH"}:
            raise ContextContractInvalid("Runtime retrieval is outside the synthetic proof.")
        if self.overflow_behavior != "BLOCK_WITH_TYPED_REMEDIATION":
            raise ContextContractInvalid("Required context overflow must fail closed without truncation.")
        if self.compression_permissions:
            raise ContextContractInvalid("The synthetic proof does not authorize context compression.")

    @property
    def token_contributions(self) -> dict[str, int]:
        return dict(self.governed_token_contributions)

    @property
    def declared_references(self) -> tuple[str, ...]:
        return (*self.required_references, *self.optional_references, *self.excluded_references)

    def canonical_dict(self) -> dict[str, object]:
        return {
            "phase_ref": self.phase_ref,
            "required_references": list(self.required_references),
            "optional_references": list(self.optional_references),
            "excluded_references": list(self.excluded_references),
            "hard_budget": self.hard_budget.canonical_dict(),
            "soft_budget": self.soft_budget.canonical_dict(),
            "governed_token_contributions": {
                name: tokens for name, tokens in self.governed_token_contributions
            },
            "compression_permissions": list(self.compression_permissions),
            "retrieval_policy": self.retrieval_policy,
            "overflow_behavior": self.overflow_behavior,
        }


@dataclass(frozen=True, slots=True)
class ResolvedContextItem:
    reference_id: str
    version: str
    artifact_id: str
    artifact_hash: str
    integrity_source: str
    authoritative_source: str
    provenance: tuple[str, ...]
    owning_responsibility: str
    consuming_module: str
    consuming_phase: str
    inclusion_reason: str
    authority_boundary: str
    content_role: str
    loading_mode: str
    may_influence: tuple[str, ...]
    must_not_influence: tuple[str, ...]
    disposition: ContextDisposition
    governed_tokens: int
    pointer_target: str | None = None

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.reference_id,
                self.version,
                self.artifact_id,
                self.integrity_source,
                self.authoritative_source,
                self.owning_responsibility,
                self.consuming_module,
                self.consuming_phase,
                self.inclusion_reason,
                self.authority_boundary,
                self.content_role,
                self.loading_mode,
            )
        ):
            raise ContextContractInvalid("Resolved context identity, provenance, purpose, and authority are required.")
        _sha256(self.artifact_hash, "Resolved context hash")
        _unique(self.provenance, "Resolved context provenance")
        _unique(self.may_influence, "Resolved may-influence boundaries", allow_empty=True)
        _unique(self.must_not_influence, "Resolved must-not-influence boundaries", allow_empty=True)
        if self.governed_tokens < 0:
            raise ContextContractInvalid("Context token contribution cannot be negative.")
        if self.loading_mode == "retrieval_only" and not self.pointer_target:
            raise ContextContractInvalid("Progressive-disclosure context requires a typed pointer target.")
        if self.disposition in {
            ContextDisposition.FORBIDDEN,
            ContextDisposition.UNAVAILABLE_NON_REQUIRED,
            ContextDisposition.NOT_APPLICABLE,
        } and self.governed_tokens:
            raise ContextContractInvalid("Excluded context cannot consume a phase token budget.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "reference_id": self.reference_id,
            "version": self.version,
            "artifact_id": self.artifact_id,
            "artifact_hash": self.artifact_hash,
            "integrity_source": self.integrity_source,
            "authoritative_source": self.authoritative_source,
            "provenance": list(self.provenance),
            "owning_responsibility": self.owning_responsibility,
            "consuming_module": self.consuming_module,
            "consuming_phase": self.consuming_phase,
            "inclusion_reason": self.inclusion_reason,
            "authority_boundary": self.authority_boundary,
            "content_role": self.content_role,
            "loading_mode": self.loading_mode,
            "may_influence": list(self.may_influence),
            "must_not_influence": list(self.must_not_influence),
            "disposition": self.disposition.value,
            "governed_tokens": self.governed_tokens,
            "pointer_target": self.pointer_target,
        }


@dataclass(frozen=True, slots=True)
class PhaseContextManifest:
    manifest_id: str
    manifest_hash: str
    schema_id: str
    phase_ref: str
    module_ref: str
    responsibility: str
    hard_budget: BudgetLimit
    soft_budget: BudgetLimit
    retrieval_policy: str
    overflow_behavior: str
    priority_order: tuple[str, ...]
    included: tuple[ResolvedContextItem, ...]
    excluded: tuple[ResolvedContextItem, ...]
    summarized: tuple[str, ...]
    retrieved: tuple[str, ...]
    compressed: tuple[str, ...]
    required: tuple[str, ...]
    conditionally_required: tuple[str, ...]
    optional: tuple[str, ...]
    forbidden: tuple[str, ...]
    unavailable_non_required: tuple[str, ...]
    not_applicable: tuple[str, ...]
    total_governed_tokens: int
    decision_rationale: tuple[tuple[str, str], ...]

    @classmethod
    def create(
        cls,
        *,
        phase_ref: str,
        module_ref: str,
        responsibility: str,
        policy: ContextBudgetPolicy,
        included: tuple[ResolvedContextItem, ...],
        excluded: tuple[ResolvedContextItem, ...],
    ) -> "PhaseContextManifest":
        required_total = sum(
            item.governed_tokens
            for item in included
            if item.disposition is ContextDisposition.REQUIRED
        )
        if required_total > policy.hard_budget.tokens:
            overflowing = tuple(
                item.reference_id
                for item in included
                if item.disposition is ContextDisposition.REQUIRED
            )
            raise ContextBudgetOverflow(
                "Required context exceeds the governed hard token budget; no context was truncated.",
                phase_ref=phase_ref,
                hard_budget_tokens=policy.hard_budget.tokens,
                required_tokens=required_total,
                overflowing_reference_ids=overflowing,
                remediation_choices=OVERFLOW_REMEDIATION_CHOICES,
                silent_truncation=False,
            )
        ordered_included = tuple(
            sorted(
                included,
                key=lambda item: (
                    GOVERNED_PRIORITY_ORDER.index(item.content_role), item.reference_id
                ),
            )
        )
        ordered_excluded = tuple(sorted(excluded, key=lambda item: item.reference_id))
        classes = {
            disposition: tuple(
                item.reference_id
                for item in (*ordered_included, *ordered_excluded)
                if item.disposition is disposition
            )
            for disposition in ContextDisposition
        }
        candidate = cls(
            manifest_id="pending",
            manifest_hash="pending",
            schema_id=PHASE_CONTEXT_MANIFEST_SCHEMA_ID,
            phase_ref=phase_ref,
            module_ref=module_ref,
            responsibility=responsibility,
            hard_budget=policy.hard_budget,
            soft_budget=policy.soft_budget,
            retrieval_policy=policy.retrieval_policy,
            overflow_behavior=policy.overflow_behavior,
            priority_order=GOVERNED_PRIORITY_ORDER,
            included=ordered_included,
            excluded=ordered_excluded,
            summarized=(),
            retrieved=(),
            compressed=(),
            required=classes[ContextDisposition.REQUIRED],
            conditionally_required=classes[ContextDisposition.CONDITIONAL],
            optional=classes[ContextDisposition.OPTIONAL],
            forbidden=classes[ContextDisposition.FORBIDDEN],
            unavailable_non_required=classes[ContextDisposition.UNAVAILABLE_NON_REQUIRED],
            not_applicable=classes[ContextDisposition.NOT_APPLICABLE],
            total_governed_tokens=sum(item.governed_tokens for item in ordered_included),
            decision_rationale=tuple(
                (item.reference_id, item.inclusion_reason)
                for item in (*ordered_included, *ordered_excluded)
            ),
        )
        candidate.validate(policy, verify_identity=False)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            manifest_id=f"phase-context-manifest_{digest}",
            manifest_hash=f"sha256:{digest}",
        )
        result.validate(policy)
        return result

    @property
    def all_items(self) -> tuple[ResolvedContextItem, ...]:
        return (*self.included, *self.excluded)

    def validate(self, policy: ContextBudgetPolicy, *, verify_identity: bool = True) -> None:
        policy.__post_init__()
        for item in self.all_items:
            item.__post_init__()
        all_ids = tuple(item.reference_id for item in self.all_items)
        included_ids = tuple(item.reference_id for item in self.included)
        excluded_ids = tuple(item.reference_id for item in self.excluded)
        class_ids = (
            *self.required,
            *self.conditionally_required,
            *self.optional,
            *self.forbidden,
            *self.unavailable_non_required,
            *self.not_applicable,
        )
        expected_classes = {
            disposition: tuple(
                item.reference_id
                for item in self.all_items
                if item.disposition is disposition
            )
            for disposition in ContextDisposition
        }
        if (
            self.schema_id != PHASE_CONTEXT_MANIFEST_SCHEMA_ID
            or self.phase_ref != policy.phase_ref
            or not self.module_ref.strip()
            or not self.responsibility.strip()
            or self.hard_budget != policy.hard_budget
            or self.soft_budget != policy.soft_budget
            or self.retrieval_policy != policy.retrieval_policy
            or self.overflow_behavior != policy.overflow_behavior
            or self.priority_order != GOVERNED_PRIORITY_ORDER
            or tuple(sorted(all_ids)) != tuple(sorted(policy.declared_references))
            or len(all_ids) != len(set(all_ids))
            or tuple(sorted(included_ids))
            != tuple(sorted((*policy.required_references, *policy.optional_references)))
            or tuple(sorted(excluded_ids)) != tuple(sorted(policy.excluded_references))
            or tuple(sorted(class_ids)) != tuple(sorted(all_ids))
            or len(class_ids) != len(set(class_ids))
            or self.required != expected_classes[ContextDisposition.REQUIRED]
            or self.conditionally_required != expected_classes[ContextDisposition.CONDITIONAL]
            or self.optional != expected_classes[ContextDisposition.OPTIONAL]
            or self.forbidden != expected_classes[ContextDisposition.FORBIDDEN]
            or self.unavailable_non_required
            != expected_classes[ContextDisposition.UNAVAILABLE_NON_REQUIRED]
            or self.not_applicable != expected_classes[ContextDisposition.NOT_APPLICABLE]
            or self.summarized
            or self.retrieved
            or self.compressed
            or self.total_governed_tokens != sum(item.governed_tokens for item in self.included)
            or self.total_governed_tokens > self.hard_budget.tokens
            or tuple(name for name, _ in self.decision_rationale) != all_ids
        ):
            raise ContextContractInvalid("Phase context manifest is incomplete, non-minimal, or policy-drifted.")
        if any(item.consuming_phase != self.phase_ref for item in self.all_items):
            raise ContextLineageInvalid("Every context item must bind to its exact consuming phase.")
        if any(
            item.reference_id not in policy.required_references
            or item.disposition is not ContextDisposition.REQUIRED
            for item in self.included
            if item.reference_id in policy.required_references
        ):
            raise ContextContractInvalid("Required context disposition drifted.")
        if any(
            item.disposition is ContextDisposition.REQUIRED
            and item.reference_id not in policy.required_references
            for item in self.all_items
        ):
            raise ContextContractInvalid("Unrequired context cannot be promoted to mandatory.")
        if verify_identity:
            digest = sha256(self.canonical_bytes()).hexdigest()
            if (
                self.manifest_id != f"phase-context-manifest_{digest}"
                or self.manifest_hash != f"sha256:{digest}"
            ):
                raise ContextContractInvalid("Phase context manifest content identity is invalid.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "phase_ref": self.phase_ref,
            "module_ref": self.module_ref,
            "responsibility": self.responsibility,
            "hard_budget": self.hard_budget.canonical_dict(),
            "soft_budget": self.soft_budget.canonical_dict(),
            "retrieval_policy": self.retrieval_policy,
            "overflow_behavior": self.overflow_behavior,
            "priority_order": list(self.priority_order),
            "included": [item.canonical_dict() for item in self.included],
            "excluded": [item.canonical_dict() for item in self.excluded],
            "summarized": list(self.summarized),
            "retrieved": list(self.retrieved),
            "compressed": list(self.compressed),
            "required": list(self.required),
            "conditionally_required": list(self.conditionally_required),
            "optional": list(self.optional),
            "forbidden": list(self.forbidden),
            "unavailable_non_required": list(self.unavailable_non_required),
            "not_applicable": list(self.not_applicable),
            "total_governed_tokens": self.total_governed_tokens,
            "decision_rationale": {name: reason for name, reason in self.decision_rationale},
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class MinimumCompleteContextGraph:
    graph_id: str
    graph_hash: str
    schema_id: str
    schema_version: str
    scope: str
    run_id: str
    target_profile_ref: str
    handoff_graph_id: str
    handoff_graph_hash: str
    accepted_handoff_id: str
    accepted_handoff_hash: str
    acceptance_decision_id: str
    acceptance_decision_hash: str
    phase_graph_id: str
    phase_graph_hash: str
    module_graph_id: str
    module_graph_hash: str
    capability_graph_id: str
    capability_graph_hash: str
    ir_id: str
    ir_hash: str
    source_lock_ref: str
    boundary_ref: str
    ratification_ref: str
    model_ref: str
    artifact_set_id: str
    constitutional_report_id: str
    constitutional_report_hash: str
    authority_identity: str
    context_input_path: str
    context_input_hash: str
    references: tuple[ReferenceDeclaration, ...]
    policies: tuple[ContextBudgetPolicy, ...]
    manifests: tuple[PhaseContextManifest, ...]
    manifest_categories: tuple[str, ...]
    conversation_history_allowed: bool
    silent_truncation_allowed: bool
    runtime_loading_allowed: bool
    production_eligible: bool
    certified: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        handoff_graph: PhaseHandoffGraph,
        phase_graph: PhaseGraph,
        handoff: InternalHandoff,
        decision: InternalHandoffDecision,
        references: tuple[ReferenceDeclaration, ...],
        policies: tuple[ContextBudgetPolicy, ...],
        manifests: tuple[PhaseContextManifest, ...],
        authority_identity: str,
    ) -> "MinimumCompleteContextGraph":
        candidate = cls(
            graph_id="pending",
            graph_hash="pending",
            schema_id=MINIMUM_CONTEXT_GRAPH_SCHEMA_ID,
            schema_version=MINIMUM_CONTEXT_GRAPH_SCHEMA_VERSION,
            scope=MINIMUM_CONTEXT_SCOPE,
            run_id=handoff_graph.run_id,
            target_profile_ref=handoff_graph.target_profile_ref,
            handoff_graph_id=handoff_graph.graph_id,
            handoff_graph_hash=handoff_graph.graph_hash,
            accepted_handoff_id=handoff.handoff_id,
            accepted_handoff_hash=handoff.handoff_hash,
            acceptance_decision_id=decision.decision_id,
            acceptance_decision_hash=decision.decision_hash,
            phase_graph_id=handoff_graph.phase_graph_id,
            phase_graph_hash=handoff_graph.phase_graph_hash,
            module_graph_id=handoff_graph.module_graph_id,
            module_graph_hash=handoff_graph.module_graph_hash,
            capability_graph_id=handoff_graph.capability_graph_id,
            capability_graph_hash=handoff_graph.capability_graph_hash,
            ir_id=handoff_graph.ir_id,
            ir_hash=handoff_graph.ir_hash,
            source_lock_ref=handoff_graph.source_lock_ref,
            boundary_ref=handoff_graph.boundary_ref,
            ratification_ref=handoff_graph.ratification_ref,
            model_ref=handoff_graph.model_ref,
            artifact_set_id=handoff_graph.artifact_set_id,
            constitutional_report_id=handoff_graph.constitutional_report_id,
            constitutional_report_hash=handoff_graph.constitutional_report_hash,
            authority_identity=authority_identity,
            context_input_path=MINIMUM_CONTEXT_INPUT_PATH,
            context_input_hash=f"sha256:{MINIMUM_CONTEXT_INPUT_SHA256}",
            references=tuple(sorted(references, key=lambda item: item.reference_id)),
            policies=tuple(sorted(policies, key=lambda item: item.phase_ref)),
            manifests=tuple(sorted(manifests, key=lambda item: item.phase_ref)),
            manifest_categories=MANIFEST_CATEGORIES,
            conversation_history_allowed=False,
            silent_truncation_allowed=False,
            runtime_loading_allowed=False,
            production_eligible=False,
            certified=False,
            outcome="PASS",
        )
        candidate.validate(handoff_graph, phase_graph, handoff, decision, verify_identity=False)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            graph_id=f"minimum-context-graph_{digest}",
            graph_hash=f"sha256:{digest}",
        )
        result.validate(handoff_graph, phase_graph, handoff, decision)
        return result

    @property
    def lineage_refs(self) -> tuple[str, ...]:
        return (
            self.source_lock_ref,
            self.boundary_ref,
            self.ratification_ref,
            self.model_ref,
            self.ir_id,
            self.artifact_set_id,
            self.constitutional_report_id,
            self.capability_graph_id,
            self.module_graph_id,
            self.phase_graph_id,
            self.handoff_graph_id,
            self.accepted_handoff_id,
            self.acceptance_decision_id,
        )

    @property
    def included_count(self) -> int:
        return sum(len(item.included) for item in self.manifests)

    @property
    def excluded_count(self) -> int:
        return sum(len(item.excluded) for item in self.manifests)

    def validate(
        self,
        handoff_graph: PhaseHandoffGraph,
        phase_graph: PhaseGraph,
        handoff: InternalHandoff,
        decision: InternalHandoffDecision,
        *,
        verify_identity: bool = True,
    ) -> None:
        handoff_graph.validate(phase_graph)
        handoff.validate(handoff_graph, phase_graph)
        receiver = next(phase for phase in phase_graph.phases if phase.phase_id == handoff.receiver_phase)
        decision.validate(handoff, receiver.failure_owner)
        reference_ids = tuple(item.reference_id for item in self.references)
        phase_ids = tuple(item.phase_id for item in phase_graph.phases)
        if (
            self.schema_id != MINIMUM_CONTEXT_GRAPH_SCHEMA_ID
            or self.schema_version != MINIMUM_CONTEXT_GRAPH_SCHEMA_VERSION
            or self.scope != MINIMUM_CONTEXT_SCOPE
            or self.run_id != handoff_graph.run_id
            or self.target_profile_ref != handoff_graph.target_profile_ref
            or self.handoff_graph_id != handoff_graph.graph_id
            or self.handoff_graph_hash != handoff_graph.graph_hash
            or self.accepted_handoff_id != handoff.handoff_id
            or self.accepted_handoff_hash != handoff.handoff_hash
            or decision.action is not InternalHandoffDecisionAction.ACCEPTED
            or self.acceptance_decision_id != decision.decision_id
            or self.acceptance_decision_hash != decision.decision_hash
            or self.phase_graph_id != handoff_graph.phase_graph_id
            or self.phase_graph_hash != handoff_graph.phase_graph_hash
            or self.module_graph_id != handoff_graph.module_graph_id
            or self.module_graph_hash != handoff_graph.module_graph_hash
            or self.capability_graph_id != handoff_graph.capability_graph_id
            or self.capability_graph_hash != handoff_graph.capability_graph_hash
            or self.ir_id != handoff_graph.ir_id
            or self.ir_hash != handoff_graph.ir_hash
            or self.source_lock_ref != handoff_graph.source_lock_ref
            or self.boundary_ref != handoff_graph.boundary_ref
            or self.ratification_ref != handoff_graph.ratification_ref
            or self.model_ref != handoff_graph.model_ref
            or self.artifact_set_id != handoff_graph.artifact_set_id
            or self.constitutional_report_id != handoff_graph.constitutional_report_id
            or self.constitutional_report_hash != handoff_graph.constitutional_report_hash
            or not self.authority_identity.strip()
            or self.context_input_path != MINIMUM_CONTEXT_INPUT_PATH
            or self.context_input_hash != f"sha256:{MINIMUM_CONTEXT_INPUT_SHA256}"
            or reference_ids != tuple(sorted(reference_ids))
            or len(reference_ids) != len(set(reference_ids))
            or tuple(item.phase_ref for item in self.policies) != tuple(sorted(phase_ids))
            or tuple(item.phase_ref for item in self.manifests) != tuple(sorted(phase_ids))
            or self.manifest_categories != MANIFEST_CATEGORIES
            or self.conversation_history_allowed
            or self.silent_truncation_allowed
            or self.runtime_loading_allowed
            or self.production_eligible
            or self.certified
            or self.outcome != "PASS"
        ):
            raise ContextLineageInvalid("Minimum Complete Context identity, authority, or lineage is invalid.")
        phase_by_id = {item.phase_id: item for item in phase_graph.phases}
        for declaration in self.references:
            declaration.__post_init__()
            if any(phase not in phase_by_id for phase in declaration.allowed_phases):
                raise ContextContractInvalid("Reference permits an undeclared phase.")
        for policy, manifest in zip(self.policies, self.manifests, strict=True):
            if set(policy.declared_references) != set(reference_ids):
                raise ContextContractInvalid("Every phase policy must explicitly classify every governed reference.")
            phase = phase_by_id[policy.phase_ref]
            if len(phase.module_refs) != 1 or manifest.module_ref != phase.module_refs[0]:
                raise ContextLineageInvalid("Context manifest module lineage is ambiguous or altered.")
            if manifest.responsibility != phase.responsibility:
                raise ContextLineageInvalid("Context manifest responsibility lineage is altered.")
            manifest.validate(policy)
        if verify_identity:
            digest = sha256(self.canonical_bytes()).hexdigest()
            if (
                self.graph_id != f"minimum-context-graph_{digest}"
                or self.graph_hash != f"sha256:{digest}"
            ):
                raise ContextContractInvalid("Minimum Complete Context graph identity is invalid.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "scope": self.scope,
            "run_id": self.run_id,
            "target_profile_ref": self.target_profile_ref,
            "handoff_graph_id": self.handoff_graph_id,
            "handoff_graph_hash": self.handoff_graph_hash,
            "accepted_handoff_id": self.accepted_handoff_id,
            "accepted_handoff_hash": self.accepted_handoff_hash,
            "acceptance_decision_id": self.acceptance_decision_id,
            "acceptance_decision_hash": self.acceptance_decision_hash,
            "phase_graph_id": self.phase_graph_id,
            "phase_graph_hash": self.phase_graph_hash,
            "module_graph_id": self.module_graph_id,
            "module_graph_hash": self.module_graph_hash,
            "capability_graph_id": self.capability_graph_id,
            "capability_graph_hash": self.capability_graph_hash,
            "ir_id": self.ir_id,
            "ir_hash": self.ir_hash,
            "source_lock_ref": self.source_lock_ref,
            "boundary_ref": self.boundary_ref,
            "ratification_ref": self.ratification_ref,
            "model_ref": self.model_ref,
            "artifact_set_id": self.artifact_set_id,
            "constitutional_report_id": self.constitutional_report_id,
            "constitutional_report_hash": self.constitutional_report_hash,
            "authority_identity": self.authority_identity,
            "context_input_path": self.context_input_path,
            "context_input_hash": self.context_input_hash,
            "references": [item.canonical_dict() for item in self.references],
            "policies": [item.canonical_dict() for item in self.policies],
            "manifests": [item.canonical_dict() for item in self.manifests],
            "manifest_categories": list(self.manifest_categories),
            "conversation_history_allowed": self.conversation_history_allowed,
            "silent_truncation_allowed": self.silent_truncation_allowed,
            "runtime_loading_allowed": self.runtime_loading_allowed,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class ContextCompilationReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    graph_id: str
    graph_hash: str
    handoff_id: str
    acceptance_decision_id: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    manifest_count: int
    reference_count: int
    included_count: int
    excluded_count: int
    summarized_count: int
    retrieved_count: int
    compressed_count: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        graph: MinimumCompleteContextGraph,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "ContextCompilationReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=CONTEXT_COMPILATION_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=graph.run_id,
            graph_id=graph.graph_id,
            graph_hash=graph.graph_hash,
            handoff_id=graph.accepted_handoff_id,
            acceptance_decision_id=graph.acceptance_decision_id,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            manifest_count=len(graph.manifests),
            reference_count=len(graph.references),
            included_count=graph.included_count,
            excluded_count=graph.excluded_count,
            summarized_count=sum(len(item.summarized) for item in graph.manifests),
            retrieved_count=sum(len(item.retrieved) for item in graph.manifests),
            compressed_count=sum(len(item.compressed) for item in graph.manifests),
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(
            candidate,
            receipt_id=f"context-compilation-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "graph_id": self.graph_id,
                "graph_hash": self.graph_hash,
                "handoff_id": self.handoff_id,
                "acceptance_decision_id": self.acceptance_decision_id,
                "authority_identity": self.authority_identity,
                "event_ids": list(self.event_ids),
                "stream_version": self.stream_version,
                "manifest_count": self.manifest_count,
                "reference_count": self.reference_count,
                "included_count": self.included_count,
                "excluded_count": self.excluded_count,
                "summarized_count": self.summarized_count,
                "retrieved_count": self.retrieved_count,
                "compressed_count": self.compressed_count,
                "outcome": self.outcome,
            }
        )

    def validate(self, graph: MinimumCompleteContextGraph) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != CONTEXT_COMPILATION_RECEIPT_SCHEMA_ID
            or self.run_id != graph.run_id
            or self.graph_id != graph.graph_id
            or self.graph_hash != graph.graph_hash
            or self.handoff_id != graph.accepted_handoff_id
            or self.acceptance_decision_id != graph.acceptance_decision_id
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.manifest_count != len(graph.manifests)
            or self.reference_count != len(graph.references)
            or self.included_count != graph.included_count
            or self.excluded_count != graph.excluded_count
            or self.summarized_count != 0
            or self.retrieved_count != 0
            or self.compressed_count != 0
            or self.outcome != "PASS"
            or self.receipt_id != f"context-compilation-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise ContextStateInvalid("Context compilation receipt does not match its graph.")


@dataclass(frozen=True, slots=True)
class ContextGraphInvalidation:
    invalidation_id: str
    invalidation_hash: str
    context_graph_ref: str
    handoff_graph_ref: str
    upstream_invalidation_ref: str
    affected_manifest_ids: tuple[str, ...]
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        context_graph_ref: str,
        handoff_graph_ref: str,
        upstream_invalidation_ref: str,
        affected_manifest_ids: tuple[str, ...],
        reason: str,
        authority_identity: str,
    ) -> "ContextGraphInvalidation":
        _unique(affected_manifest_ids, "Affected context manifests")
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            context_graph_ref=context_graph_ref,
            handoff_graph_ref=handoff_graph_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            affected_manifest_ids=tuple(sorted(affected_manifest_ids)),
            reason=reason,
            authority_identity=authority_identity,
        )
        if not all(
            value.strip()
            for value in (
                invalidation_id,
                context_graph_ref,
                handoff_graph_ref,
                upstream_invalidation_ref,
                reason,
                authority_identity,
            )
        ):
            raise ContextStateInvalid("Context invalidation identity is incomplete.")
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "invalidation_id": self.invalidation_id,
                "context_graph_ref": self.context_graph_ref,
                "handoff_graph_ref": self.handoff_graph_ref,
                "upstream_invalidation_ref": self.upstream_invalidation_ref,
                "affected_manifest_ids": list(self.affected_manifest_ids),
                "reason": self.reason,
                "authority_identity": self.authority_identity,
            }
        )


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
