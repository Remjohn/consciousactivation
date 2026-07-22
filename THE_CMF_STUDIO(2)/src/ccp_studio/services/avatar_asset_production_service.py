from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import AvatarAssetProductionPlan, AvatarCharacterSpec
from ccp_studio.services.avatar_action_timeline_service import AvatarActionTimelineService
from ccp_studio.services.avatar_face_plate_approval_service import AvatarFacePlateApprovalService
from ccp_studio.services.avatar_paper_body_layer_service import AvatarPaperBodyLayerService
from ccp_studio.services.avatar_psd_layer_service import AvatarPSDLayerService
from ccp_studio.services.stretchy_studio_manifest_service import StretchyStudioManifestService


class AvatarAssetProductionService:
    def __init__(self):
        self.psd_layers = AvatarPSDLayerService()
        self.face_plates = AvatarFacePlateApprovalService()
        self.body_layers = AvatarPaperBodyLayerService()
        self.action_timeline = AvatarActionTimelineService()
        self.stretchy = StretchyStudioManifestService()

    def create_character_spec(
        self,
        *,
        avatar_id: str,
        brand_id: str,
        brand_context_version_id: str,
        character_name: str = "Coach Guide Avatar",
        identity_anchor_refs: list[str] | None = None,
    ) -> AvatarCharacterSpec:
        return AvatarCharacterSpec(
            avatar_id=avatar_id,
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
            character_name=character_name,
            identity_anchor_refs=identity_anchor_refs or ["identity_anchor_face", "identity_anchor_outfit"],
        )

    def compile_production_plan(self, spec: AvatarCharacterSpec) -> AvatarAssetProductionPlan:
        requirements = self.psd_layers.compile_canonical_layer_requirements()
        return AvatarAssetProductionPlan(
            avatar_character_spec=spec,
            psd_layer_requirements=requirements,
        )

    def compile_default_asset_stack(self, spec: AvatarCharacterSpec, *, approved_by: str = "operator") -> dict:
        plan = self.compile_production_plan(spec)
        face_set = self.face_plates.compile_approved_face_plate_set(avatar_id=spec.avatar_id, approved_by=approved_by)
        body_set = self.body_layers.compile_body_layer_set(avatar_id=spec.avatar_id)
        timeline = self.action_timeline.compile_canonical_action_timeline(spec.avatar_id)
        stretchy = self.stretchy.compile_import_manifest(
            avatar_id=spec.avatar_id,
            source_psd_ref="assets/avatar/coach_avatar_layers.psd",
            layer_requirements=plan.psd_layer_requirements,
            action_timeline_ref=timeline.avatar_action_timeline_id,
        )
        return {
            "production_plan": plan,
            "face_plate_approval_set": face_set,
            "body_layer_set": body_set,
            "action_timeline": timeline,
            "stretchy_studio_import_manifest": stretchy,
        }
