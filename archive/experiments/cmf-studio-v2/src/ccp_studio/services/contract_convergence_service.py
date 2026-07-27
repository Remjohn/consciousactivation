"""Contract convergence helpers for ontology V1.

The service adapts old component-specific contracts into canonical contracts.
It does not delete old contracts; migration remains additive until downstream
modules move to the canonical interfaces.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ccp_studio.contracts.creative_ingredients import CompositionRole, SourceReference, VisualIngredientProgram
from ccp_studio.contracts.frame_profiles import DEFAULT_FRAME_PROFILES, FrameDeliveryMode, FrameProfile, FrameProfileCode
from ccp_studio.contracts.ontology import CanonicalContractPath, ContractConvergenceReceipt, MigrationAction, convergence_receipt_hash
from ccp_studio.contracts.primitive_coalition import PrimitiveCoalitionContract, simple_triad_to_coalition
from ccp_studio.contracts.style_routes import SourceReferenceMode, StyleFamily, StyleRoute


CANONICAL_CONTRACT_PATHS: tuple[str, ...] = (
    "src/ccp_studio/contracts/ontology.py",
    "src/ccp_studio/contracts/primitive_coalition.py",
    "src/ccp_studio/contracts/frame_profiles.py",
    "src/ccp_studio/contracts/style_routes.py",
    "src/ccp_studio/contracts/visual_preproduction.py",
    "src/ccp_studio/contracts/creative_ingredients.py",
    "src/ccp_studio/contracts/registry_consolidation.py",
)


class ContractConvergenceServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class ProviderJobPreconditionResult:
    source_reference: SourceReference | str
    style_route: StyleRoute
    frame_profile: FrameProfile | FrameProfileCode
    composition_role: CompositionRole | str
    evaluation_requirements: dict[str, float]
    primitive_coalition_contract_id: str


@dataclass(frozen=True)
class ContractConvergenceService:
    actor_ref: str = "system"

    def new_receipt(
        self,
        *,
        source_contract_refs: list[str],
        canonical_contract_ref: str,
        decision: MigrationAction,
        adapter_required: bool = True,
        compatibility_notes: list[str] | None = None,
        test_refs: list[str] | None = None,
    ) -> ContractConvergenceReceipt:
        receipt_hash = convergence_receipt_hash(
            source_contract_refs=source_contract_refs,
            canonical_contract_ref=canonical_contract_ref,
            decision=decision,
            adapter_required=adapter_required,
            compatibility_notes=compatibility_notes or [],
            test_refs=test_refs or [],
        )
        return ContractConvergenceReceipt(
            source_contract_refs=source_contract_refs,
            canonical_contract_ref=canonical_contract_ref,
            decision=decision,
            adapter_required=adapter_required,
            compatibility_notes=compatibility_notes or [],
            test_refs=test_refs or [],
            receipt_hash=receipt_hash,
        )

    def project_primitive_triad_to_coalition(
        self,
        *,
        meaning_transform: str | None = None,
        delivery_shape: str | None = None,
        format_material: str | None = None,
        primitive_triads: list[Any] | None = None,
        coalition_intent: str,
        source_context_refs: dict[str, str] | None = None,
    ) -> PrimitiveCoalitionContract:
        if primitive_triads:
            by_role = {getattr(item, "role", None): getattr(item, "primitive_id", None) for item in primitive_triads}
            meaning_transform = meaning_transform or by_role.get("meaning_transform")
            delivery_shape = delivery_shape or by_role.get("delivery_shape")
            format_material = format_material or by_role.get("format_material")
        if not meaning_transform or not delivery_shape or not format_material:
            raise ContractConvergenceServiceError(
                "INVALID_PRIMITIVE_TRIAD",
                "Primitive triad projection requires meaning_transform, delivery_shape, and format_material.",
            )
        return simple_triad_to_coalition(
            meaning_transform=meaning_transform,
            delivery_shape=delivery_shape,
            format_material=format_material,
            coalition_intent=coalition_intent,
            source_context_refs=source_context_refs,
        )

    def primitive_triad_projection(self, **kwargs: Any) -> PrimitiveCoalitionContract:
        return self.project_primitive_triad_to_coalition(**kwargs)

    def validate_frame_profile_for_short_form(
        self,
        frame_profile: FrameProfile | FrameProfileCode | str,
        *,
        delivery_required: bool = True,
    ) -> FrameProfile:
        profile = self._resolve_frame_profile(frame_profile)
        if profile.code.value.startswith("16:9") and delivery_required:
            raise ContractConvergenceServiceError(
                "FRAME_PROFILE_SOURCE_ONLY",
                "16:9 frame profiles are source-only for short-form workflows and cannot be used as delivery frames.",
            )
        if delivery_required and profile.delivery_mode != FrameDeliveryMode.delivery:
            raise ContractConvergenceServiceError("FRAME_PROFILE_NOT_DELIVERY", f"{profile.code.value} is not a delivery frame.")
        return profile

    def validate_provider_job_preconditions(
        self,
        *,
        source_reference: SourceReference | str | None = None,
        style_route: StyleRoute | None = None,
        frame_profile: FrameProfile | FrameProfileCode | str | None = None,
        composition_role: CompositionRole | str | None = None,
        evaluation_requirements: dict[str, float] | None = None,
        primitive_coalition_contract_id: str | None = None,
        source_reference_mode: SourceReferenceMode | None = None,
        provider_job: VisualIngredientProgram | None = None,
        composition_allows_multi_style: bool = False,
    ) -> ProviderJobPreconditionResult:
        if provider_job is not None:
            source_reference = source_reference or provider_job.source_reference
            style_route = style_route or provider_job.style_route
            frame_profile = frame_profile or provider_job.frame_profile
            composition_role = composition_role or provider_job.composition_role
            evaluation_requirements = evaluation_requirements or provider_job.evaluation_requirements or provider_job.eval_requirements
            primitive_coalition_contract_id = primitive_coalition_contract_id or provider_job.primitive_coalition_contract_id
            source_reference_mode = source_reference_mode or provider_job.source_reference_mode
        if source_reference is None:
            raise ContractConvergenceServiceError("SOURCE_REFERENCE_REQUIRED", "Provider jobs require source_reference.")
        if style_route is None:
            raise ContractConvergenceServiceError("STYLE_ROUTE_REQUIRED", "Provider jobs require one primary style_route.")
        if frame_profile is None:
            raise ContractConvergenceServiceError("FRAME_PROFILE_REQUIRED", "Provider jobs require frame_profile.")
        if composition_role is None:
            raise ContractConvergenceServiceError("COMPOSITION_ROLE_REQUIRED", "Provider jobs require composition_role.")
        if not evaluation_requirements:
            raise ContractConvergenceServiceError("EVAL_REQUIREMENTS_REQUIRED", "Provider jobs require eval requirements.")
        if not primitive_coalition_contract_id:
            raise ContractConvergenceServiceError(
                "PRIMITIVE_COALITION_REQUIRED",
                "Provider jobs require primitive_coalition_contract_id.",
            )
        if style_route.family == StyleFamily.gmg and "," in style_route.route_code and not composition_allows_multi_style:
            raise ContractConvergenceServiceError(
                "GMG_AVERAGING_FORBIDDEN",
                "Provider jobs must not average GMG experts; use one primary style route unless composition explicitly allows assembly.",
            )
        if style_route.requires_real_reference and source_reference_mode not in {
            SourceReferenceMode.direct_real_reference,
            SourceReferenceMode.composite_real_references,
            None,
        }:
            raise ContractConvergenceServiceError("REAL_REFERENCE_REQUIRED", f"{style_route.route_code} requires real-life/source reference.")
        resolved_frame = self.validate_frame_profile_for_short_form(frame_profile)
        return ProviderJobPreconditionResult(
            source_reference=source_reference,
            style_route=style_route,
            frame_profile=resolved_frame,
            composition_role=composition_role,
            evaluation_requirements=evaluation_requirements,
            primitive_coalition_contract_id=primitive_coalition_contract_id,
        )

    def freeze_canonical_contract_paths(self, paths: list[str] | None = None) -> list[CanonicalContractPath]:
        return [
            CanonicalContractPath(path=path, module_name=Path(path).stem, notes=["Frozen canonical V1 contract path."])
            for path in (paths or list(CANONICAL_CONTRACT_PATHS))
        ]

    def summarize_contract_convergence_status(self) -> dict[str, Any]:
        frozen_paths = self.freeze_canonical_contract_paths()
        return {
            "actor_ref": self.actor_ref,
            "canonical_path_count": len(frozen_paths),
            "canonical_paths_frozen": all(path.frozen and path.migration_adr_required for path in frozen_paths),
            "adapter_policy": "old contracts are adapted or projected, not deleted",
        }

    def _resolve_frame_profile(self, frame_profile: FrameProfile | FrameProfileCode | str) -> FrameProfile:
        if isinstance(frame_profile, FrameProfile):
            return frame_profile
        code = frame_profile if isinstance(frame_profile, FrameProfileCode) else FrameProfileCode(frame_profile)
        for profile in DEFAULT_FRAME_PROFILES:
            if profile.code == code:
                return profile
        raise ContractConvergenceServiceError("FRAME_PROFILE_UNKNOWN", code.value)
