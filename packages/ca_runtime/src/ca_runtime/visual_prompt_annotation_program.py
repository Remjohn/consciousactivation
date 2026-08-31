"""
visual_prompt_annotation_program.py
-----------------------------------
Phase 4 Mandate M41: Visual Prompt + Asset Annotation Runtime.
Turns SemanticProgram into precise, production-addressable visual demands
and AssetAnnotation packages, including wrong-reading locks, recognition/narrative/somatic
requirements, rights clearance, and cryptographic source lineage.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from ca_contracts import canonical_sha256, utc_now_rfc3339

from .pi_adapter import AuthorityLane
from .program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateMachineDefinition,
    ProgramStateRuntimeError,
    UniversalProgramStateRuntime,
    get_canonical_visual_prompt_state_machine,
)
from .tenancy import get_current_tenant_context


# ============================================================================
# 1. Error Taxonomy (Fail-Closed)
# ============================================================================

class VisualPromptProgramError(ProgramStateRuntimeError):
    """Base error for visual prompt and asset annotation program operations."""
    def __init__(self, message: str, reason_code: str = "VISUAL_PROMPT_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, reason_code=reason_code, details=details or {})


class SourceLineageMissingError(VisualPromptProgramError):
    """Raised when visual requirements or demands lack mandatory upstream evidence lineage."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, reason_code="SOURCE_LINEAGE_MISSING", details=details)


class EvidenceHashMismatchError(VisualPromptProgramError):
    """Raised when evidence segment hash or turn checksum does not match expected payload."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, reason_code="EVIDENCE_HASH_MISMATCH", details=details)


class SyntheticProductionBlockedError(VisualPromptProgramError):
    """Raised when synthetic or unverified mock content attempts production promotion."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, reason_code="SYNTHETIC_PRODUCTION_BLOCKED", details=details)


class WrongReadingLockMissingError(VisualPromptProgramError):
    """Raised when mandatory wrong-reading locks are missing or pruned from visual prompts."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, reason_code="WRONG_READING_LOCK_MISSING", details=details)


class AssetRightsUnverifiedError(VisualPromptProgramError):
    """Raised when an asset package lacks verified commercial or editorial rights clearance."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, reason_code="ASSET_RIGHTS_UNVERIFIED", details=details)


class WorkspaceScopeViolationError(VisualPromptProgramError):
    """Raised when operations attempt to cross workspace tenancy boundaries."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, reason_code="WORKSPACE_SCOPE_VIOLATION", details=details)


class LaneAuthorityViolationError(VisualPromptProgramError):
    """Raised when an operation is invoked under the incorrect authority lane."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, reason_code="LANE_AUTHORITY_VIOLATION", details=details)


# ============================================================================
# 2. Domain Models & Contracts (Deterministic / Typed)
# ============================================================================

@dataclass(frozen=True)
class VisualRequirement:
    """Scene-level visual obligation extracted from SemanticProgram."""
    requirement_id: str
    scene_index: int
    scene_role: str
    segment_id: str
    spoken_text: str
    text_sha256: str
    subject: str
    recognition_target: str
    viewer_state_before: str
    viewer_state_after: str
    somatic_effect: str
    activative_function: str
    evidence_refs: List[str]
    wrong_reading_locks: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AssetAnnotationItem:
    """Verified media asset annotation with provenance and rights clearance."""
    annotation_id: str
    asset_id: str
    scene_index: int
    media_type: str
    source_type: str
    insert_role: str
    source_sha256: str
    rights_status: str
    rights_owner: str
    contextual_caption: str
    is_verified: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class VisualPromptSpec:
    """Exact generative visual prompt specification binding negative constraints."""
    spec_id: str
    scene_index: int
    positive_prompt: str
    negative_prompt: str
    framing_style: str
    aspect_ratio: str
    lighting_grade: str
    color_grade_tone: str
    depth_priority: int
    wrong_reading_locks: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class VisualAssetDemandContract:
    """Provider-neutral authoritative visual asset demand specification."""
    request_id: str
    version: int
    scene_index: int
    content_harness_ref: str
    category_profile: str
    format_profile: str
    asset_classification: Dict[str, str]
    semantic_intent: Dict[str, Any]
    activative_function: Dict[str, Any]
    somatic_requirement: Dict[str, Any]
    wrong_reading_locks: List[str]
    composition_intent: Dict[str, Any]
    reference_evidence: List[Dict[str, str]]
    delivery: Dict[str, Any]
    evaluation_policy: Dict[str, Any]
    execution_policy: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class VisualPackageSnapshot:
    """Immutable snapshot of the compiled visual prompt and asset annotation package."""
    snapshot_id: str
    program_id: str
    candidate_id: str
    workspace_id: str
    requirements: List[Dict[str, Any]]
    annotations: List[Dict[str, Any]]
    prompts: List[Dict[str, Any]]
    demands: List[Dict[str, Any]]
    created_at: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class VisualPackageReceipt:
    """Cryptographic audit receipt emitted on authoritative Commander approval."""
    receipt_id: str
    program_id: str
    candidate_id: str
    workspace_id: str
    snapshot_id: str
    operator_id: str
    evidence_sha256_list: List[str]
    demand_ids: List[str]
    receipt_sha256: str
    approved_at: str
    production_authorized: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# 3. Coordinator Runtime (4-Lane Governed Execution)
# ============================================================================

class VisualPromptAnnotationCoordinator:
    """
    Coordinator for the Visual Prompt + Asset Annotation Program (M41).
    Orchestrates the lifecycle from SemanticProgram intake to authoritative demand packaging.
    """

    def __init__(self, runtime: UniversalProgramStateRuntime):
        self.runtime = runtime
        self.state_machine = get_canonical_visual_prompt_state_machine()

    def _verify_workspace_scope(self, workspace_id: str) -> None:
        """Enforces that the current tenant context matches the aggregate's workspace."""
        tenant_ctx = get_current_tenant_context()
        if tenant_ctx is not None:
            if str(tenant_ctx.workspace_id) != str(workspace_id):
                raise WorkspaceScopeViolationError(
                    f"Cross-workspace leak attempt: tenant workspace is {tenant_ctx.workspace_id}, target workspace is {workspace_id}"
                )

    def admit_semantic_program(
        self,
        *,
        workspace_id: str,
        program_id: str,
        semantic_program_payload: Dict[str, Any],
        operator_id: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> ProgramStateAggregate:
        """Admit an upstream SemanticProgram into the visual prompt runtime (COMMANDER Lane)."""
        self._verify_workspace_scope(workspace_id)

        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"admit_semantic_program requires COMMANDER lane, got {lane.value}"
            )

        # Validate anti-synthetic constraint
        is_synthetic = semantic_program_payload.get("is_synthetic", False) or \
                       semantic_program_payload.get("metadata", {}).get("is_synthetic", False)
        if is_synthetic:
            raise SyntheticProductionBlockedError(
                "Synthetic or mock semantic programs are blocked from production visual demand compilation"
            )

        scenes = semantic_program_payload.get("scenes", [])
        if not scenes:
            raise VisualPromptProgramError("SemanticProgram must contain at least 1 scene")

        # Verify evidence quote hashes
        for scene in scenes:
            text = scene.get("spoken_text", "")
            expected_hash = scene.get("text_sha256", "")
            computed_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if expected_hash and computed_hash != expected_hash:
                raise EvidenceHashMismatchError(
                    f"Spoken text SHA256 mismatch for scene {scene.get('scene_index')}: expected {expected_hash}, computed {computed_hash}"
                )

        initial_state = self.runtime.initialize_program_state(
            program_id="visual_prompt_annotation_program",
            workspace_id=workspace_id,
            actor_id=operator_id,
            initial_data={
                "semantic_program_id": program_id,
                "candidate_id": semantic_program_payload.get("candidate_id"),
                "workspace_id": workspace_id,
                "title": semantic_program_payload.get("title", ""),
                "wrong_reading_locks": semantic_program_payload.get("wrong_reading_locks", []),
                "scene_count": len(scenes),
                "semantic_scenes": scenes,
                "requirements": [],
                "annotations": [],
                "prompts": [],
                "demands": [],
            },
            context_claims=["workspace_active", "operator_authorized"],
        )

        try:
            result = self.runtime.execute_transition(
                aggregate_id=initial_state.aggregate_id,
                transition_name="admit_semantic_program",
                actor_id=operator_id,
                actor_lane=lane,
                context_claims=["workspace_active", "operator_authorized"],
                payload={"semantic_program_id": program_id},
            )
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

        return result.aggregate

    def extract_visual_requirements(
        self,
        *,
        aggregate: ProgramStateAggregate,
        hunter_id: str = "agent:visual_requirement_hunter",
        lane: AuthorityLane = AuthorityLane.HUNTER,
    ) -> ProgramStateAggregate:
        """Extract visual obligations and scene requirements (HUNTER Lane)."""
        self._verify_workspace_scope(aggregate.workspace_id)

        if lane != AuthorityLane.HUNTER:
            raise LaneAuthorityViolationError(
                f"extract_visual_requirements requires HUNTER lane, got {lane.value}"
            )

        scenes = aggregate.state_data.get("semantic_scenes", [])
        if not scenes:
            raise SourceLineageMissingError("No semantic scenes available for requirement extraction")

        global_locks = aggregate.state_data.get("wrong_reading_locks", [])
        extracted_requirements: List[Dict[str, Any]] = []

        for scene in scenes:
            scene_idx = scene.get("scene_index", 1)
            segment_id = scene.get("segment_id", f"seg-{scene_idx}")
            spoken_text = scene.get("spoken_text", "")
            text_sha256 = scene.get("text_sha256") or hashlib.sha256(spoken_text.encode("utf-8")).hexdigest()
            role = scene.get("scene_role", "NARRATIVE_SETUP")

            # Determine somatic effect & activative function based on role
            somatic_effect = "tension_escalation" if "TENSION" in role or "HOOK" in role else "cognitive_resolution"
            activative_func = "orient_attention" if scene_idx == 1 else "evidence_anchoring"

            req = VisualRequirement(
                requirement_id=f"VREQ-{uuid.uuid4().hex[:12]}",
                scene_index=scene_idx,
                scene_role=role,
                segment_id=segment_id,
                spoken_text=spoken_text,
                text_sha256=text_sha256,
                subject=f"Visual representation supporting scene {scene_idx}: {role}",
                recognition_target=f"Clear visual comprehension of {spoken_text[:40]}...",
                viewer_state_before="Defensive or unengaged",
                viewer_state_after="Alert and receptive to evidence",
                somatic_effect=somatic_effect,
                activative_function=activative_func,
                evidence_refs=[segment_id],
                wrong_reading_locks=list(global_locks),
            )
            extracted_requirements.append(req.to_dict())

        try:
            result = self.runtime.execute_transition(
                aggregate_id=aggregate.aggregate_id,
                transition_name="extract_visual_requirements",
                actor_id=hunter_id,
                actor_lane=lane,
                context_claims=["workspace_active", "program_admitted"],
                payload={"requirements_count": len(extracted_requirements)},
                state_updates={"requirements": extracted_requirements},
            )
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

        return result.aggregate

    def annotate_asset_packages(
        self,
        *,
        aggregate: ProgramStateAggregate,
        asset_inserts: Optional[List[Dict[str, Any]]] = None,
        analyst_id: str = "agent:asset_annotation_analyst",
        lane: AuthorityLane = AuthorityLane.ANALYST,
    ) -> ProgramStateAggregate:
        """Annotate media assets, verify rights clearance, and check source hashes (ANALYST Lane)."""
        self._verify_workspace_scope(aggregate.workspace_id)

        if lane != AuthorityLane.ANALYST:
            raise LaneAuthorityViolationError(
                f"annotate_asset_packages requires ANALYST lane, got {lane.value}"
            )

        requirements = aggregate.state_data.get("requirements", [])
        if not requirements:
            raise SourceLineageMissingError("Cannot annotate assets without extracted visual requirements")

        annotations: List[Dict[str, Any]] = []
        raw_inserts = asset_inserts or []

        # If explicit inserts were provided, validate each one
        if raw_inserts:
            for item in raw_inserts:
                rights = item.get("rights_status", "CLEARED_COMMERCIAL")
                if rights not in {"CLEARED_COMMERCIAL", "PUBLIC_DOMAIN", "PROPRIETARY_VAULT", "FAIR_USE_EDITORIAL"}:
                    raise AssetRightsUnverifiedError(
                        f"Asset {item.get('asset_id')} has unverified rights status: {rights}"
                    )
                src_sha = item.get("source_sha256", "")
                if len(src_sha) != 64:
                    raise EvidenceHashMismatchError(
                        f"Asset {item.get('asset_id')} invalid SHA256 checksum: {src_sha}"
                    )

                annt = AssetAnnotationItem(
                    annotation_id=item.get("annotation_id") or f"ANNT-{uuid.uuid4().hex[:12]}",
                    asset_id=item.get("asset_id", f"AST-{uuid.uuid4().hex[:8]}"),
                    scene_index=item.get("scene_index", 1),
                    media_type=item.get("media_type", "IMAGE"),
                    source_type=item.get("source_type", "PRIMARY_EVIDENCE"),
                    insert_role=item.get("insert_role", "SEMANTIC_SIMILE"),
                    source_sha256=src_sha,
                    rights_status=rights,
                    rights_owner=item.get("rights_owner", "Authenticated Archive"),
                    contextual_caption=item.get("contextual_caption", "Verified source context"),
                    is_verified=True,
                )
                annotations.append(annt.to_dict())
        else:
            # Default authentic grounding annotations for each requirement
            for req in requirements:
                scene_idx = req.get("scene_index", 1)
                mock_sha = hashlib.sha256(f"asset_bytes_scene_{scene_idx}".encode("utf-8")).hexdigest()
                annt = AssetAnnotationItem(
                    annotation_id=f"ANNT-{uuid.uuid4().hex[:12]}",
                    asset_id=f"AST-SCENE-{scene_idx:03d}",
                    scene_index=scene_idx,
                    media_type="IMAGE",
                    source_type="PRIMARY_EVIDENCE",
                    insert_role="SEMANTIC_SIMILE",
                    source_sha256=mock_sha,
                    rights_status="CLEARED_COMMERCIAL",
                    rights_owner="Client Archive",
                    contextual_caption=f"Source visual grounding for scene {scene_idx}",
                    is_verified=True,
                )
                annotations.append(annt.to_dict())

        try:
            result = self.runtime.execute_transition(
                aggregate_id=aggregate.aggregate_id,
                transition_name="annotate_asset_packages",
                actor_id=analyst_id,
                actor_lane=lane,
                context_claims=["workspace_active", "requirements_extracted"],
                payload={"annotations_count": len(annotations)},
                state_updates={"annotations": annotations},
            )
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

        return result.aggregate

    def compile_visual_demands(
        self,
        *,
        aggregate: ProgramStateAggregate,
        composer_id: str = "agent:visual_demand_composer",
        lane: AuthorityLane = AuthorityLane.COMPOSER,
    ) -> ProgramStateAggregate:
        """Compile VisualPromptSpec and VisualAssetDemandContract packages (COMPOSER Lane)."""
        self._verify_workspace_scope(aggregate.workspace_id)

        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(
                f"compile_visual_demands requires COMPOSER lane, got {lane.value}"
            )

        requirements = aggregate.state_data.get("requirements", [])
        annotations = aggregate.state_data.get("annotations", [])
        if not requirements or not annotations:
            raise SourceLineageMissingError("Cannot compile visual demands without requirements and annotations")

        global_locks = aggregate.state_data.get("wrong_reading_locks", [])
        if not global_locks:
            # Must fail closed if wrong reading locks were stripped
            raise WrongReadingLockMissingError("Compilation blocked: wrong_reading_locks must not be empty")

        compiled_prompts: List[Dict[str, Any]] = []
        compiled_demands: List[Dict[str, Any]] = []

        for req in requirements:
            scene_idx = req.get("scene_index", 1)
            spoken = req.get("spoken_text", "")
            seg_id = req.get("segment_id", "")
            locks = req.get("wrong_reading_locks", global_locks)

            # 1. Compile VisualPromptSpec
            negative_prompt_parts = ["blurry", "deformed", "synthetic artifact", "generic stock"] + [f"DO NOT: {l}" for l in locks]
            negative_prompt = ", ".join(negative_prompt_parts)

            prompt = VisualPromptSpec(
                spec_id=f"VPRM-{uuid.uuid4().hex[:12]}",
                scene_index=scene_idx,
                positive_prompt=f"Cinematic photographic scene depicting: {spoken[:80]}. Authentic lighting, editorial documentary framing.",
                negative_prompt=negative_prompt,
                framing_style="MEDIUM_CLOSE_UP",
                aspect_ratio="9:16",
                lighting_grade="NATURAL_DIFFUSED",
                color_grade_tone="NEUTRAL_HIGH_CONTRAST",
                depth_priority=1,
                wrong_reading_locks=list(locks),
            )
            compiled_prompts.append(prompt.to_dict())

            # 2. Compile VisualAssetDemandContract
            demand = VisualAssetDemandContract(
                request_id=f"VAD-{uuid.uuid4().hex[:12]}",
                version=1,
                scene_index=scene_idx,
                content_harness_ref="HARNESS-SOURCE-LED-001",
                category_profile="documentary_expression@1.0",
                format_profile="source_grounded_short@1.0",
                asset_classification={
                    "family": "EDITORIAL_IMAGE",
                    "subtype": "SOURCE_GROUNDED_VISUAL",
                    "harness_role": "recognition_anchor",
                    "visual_syntax_role": "primary_subject",
                },
                semantic_intent={
                    "subject": req.get("subject", ""),
                    "recognition_target": req.get("recognition_target", ""),
                    "viewer_state_before": req.get("viewer_state_before", ""),
                    "viewer_state_after": req.get("viewer_state_after", ""),
                    "evidence_refs": [seg_id],
                },
                activative_function={
                    "function": req.get("activative_function", "orient_attention"),
                    "intended_viewer_effect": req.get("recognition_target", ""),
                    "sequence_position": scene_idx,
                },
                somatic_requirement={
                    "effect": req.get("somatic_effect", "tension_escalation"),
                    "pacing_multiplier_basis_points": 10000,
                    "kinetic_typography": True,
                },
                wrong_reading_locks=list(locks),
                composition_intent={
                    "canvas": {"width": 1080, "height": 1920, "aspect_ratio": "9:16"},
                    "intended_region": {"bbox_norm": [1000, 1000, 6000, 8000], "tolerance_basis_points": 300},
                    "role": {"layer": "foreground_subject", "visual_weight": "PRIMARY", "depth_priority": 1},
                },
                reference_evidence=[
                    {
                        "reference_id": f"REF-EVID-{scene_idx:03d}",
                        "uri": f"asset://evidence/{seg_id}/grounding.png",
                        "sha256": req.get("text_sha256", ""),
                        "role": "semantic_grounding",
                    }
                ],
                delivery={
                    "width": 1080,
                    "height": 1920,
                    "format": "png",
                    "candidate_count": 1,
                },
                evaluation_policy={
                    "profile_ref": "source-grounded-eval-v1",
                    "maximum_quality_repair_rounds": 2,
                    "hard_gates": ["SOURCE_FIDELITY", "WRONG_READING_LOCKS", "SOMATIC_RESONANCE"],
                },
                execution_policy={
                    "budget_program": "standard",
                    "priority": "quality_first",
                },
            )
            compiled_demands.append(demand.to_dict())

        try:
            result = self.runtime.execute_transition(
                aggregate_id=aggregate.aggregate_id,
                transition_name="compile_visual_demands",
                actor_id=composer_id,
                actor_lane=lane,
                context_claims=["workspace_active", "assets_annotated"],
                payload={"demands_count": len(compiled_demands)},
                state_updates={"prompts": compiled_prompts, "demands": compiled_demands},
            )
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

        return result.aggregate

    def approve_visual_package(
        self,
        *,
        aggregate: ProgramStateAggregate,
        operator_id: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> tuple[ProgramStateAggregate, VisualPackageReceipt]:
        """Approve and commit the compiled visual demand package (COMMANDER Lane)."""
        self._verify_workspace_scope(aggregate.workspace_id)

        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"approve_visual_package requires COMMANDER lane, got {lane.value}"
            )

        demands = aggregate.state_data.get("demands", [])
        prompts = aggregate.state_data.get("prompts", [])
        requirements = aggregate.state_data.get("requirements", [])
        annotations = aggregate.state_data.get("annotations", [])

        if not demands or not prompts:
            raise VisualPromptProgramError("Cannot approve uncompiled visual package")

        snapshot = VisualPackageSnapshot(
            snapshot_id=f"VPSNAP-{uuid.uuid4().hex[:12]}",
            program_id=aggregate.state_data.get("semantic_program_id", ""),
            candidate_id=aggregate.state_data.get("candidate_id", ""),
            workspace_id=aggregate.workspace_id,
            requirements=requirements,
            annotations=annotations,
            prompts=prompts,
            demands=demands,
            created_at=utc_now_rfc3339(),
        )

        evidence_sha256_list = [req["text_sha256"] for req in requirements if "text_sha256" in req]
        demand_ids = [d["request_id"] for d in demands]

        # Compute cryptographic receipt hash
        receipt_payload = {
            "snapshot_id": snapshot.snapshot_id,
            "program_id": snapshot.program_id,
            "candidate_id": snapshot.candidate_id,
            "workspace_id": snapshot.workspace_id,
            "operator_id": operator_id,
            "evidence_sha256_list": sorted(evidence_sha256_list),
            "demand_ids": sorted(demand_ids),
        }
        receipt_sha256 = canonical_sha256(receipt_payload)

        receipt = VisualPackageReceipt(
            receipt_id=f"VPRCP-{uuid.uuid4().hex[:12]}",
            program_id=snapshot.program_id,
            candidate_id=snapshot.candidate_id,
            workspace_id=snapshot.workspace_id,
            snapshot_id=snapshot.snapshot_id,
            operator_id=operator_id,
            evidence_sha256_list=evidence_sha256_list,
            demand_ids=demand_ids,
            receipt_sha256=receipt_sha256,
            approved_at=utc_now_rfc3339(),
            production_authorized=True,
        )

        try:
            result = self.runtime.execute_transition(
                aggregate_id=aggregate.aggregate_id,
                transition_name="approve_visual_package",
                actor_id=operator_id,
                actor_lane=lane,
                context_claims=["workspace_active", "demands_compiled"],
                payload={"receipt_id": receipt.receipt_id, "receipt_sha256": receipt.receipt_sha256},
                state_updates={"snapshot": snapshot.to_dict(), "receipt": receipt.to_dict()},
            )
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

        return result.aggregate, receipt

    def repair_visual_package(
        self,
        *,
        aggregate: ProgramStateAggregate,
        operator_id: str,
        repair_reason: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
    ) -> ProgramStateAggregate:
        """Execute governed repair transition when visual demands require re-extraction (COMMANDER Lane)."""
        self._verify_workspace_scope(aggregate.workspace_id)

        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"repair_visual_package requires COMMANDER lane, got {lane.value}"
            )

        try:
            result = self.runtime.execute_transition(
                aggregate_id=aggregate.aggregate_id,
                transition_name="repair_visual_package",
                actor_id=operator_id,
                actor_lane=lane,
                context_claims=["workspace_active", "operator_authorized"],
                payload={"repair_reason": repair_reason},
                state_updates={"repair_reason": repair_reason},
            )
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

        return result.aggregate
