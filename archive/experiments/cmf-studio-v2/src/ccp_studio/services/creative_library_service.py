"""Rig and creative library service for TS-CMF-020."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.acting_library import ActingReferenceStatus
from ccp_studio.contracts.creative_libraries import (
    CompositionPreference,
    CreativeEvaluationState,
    CreativeItemStatus,
    CreativeLibraryItemKind,
    MicroSemioticAnchor,
    MotionBeat,
    MotionRecipe,
    PlatformProfile,
    SfxAsset,
    creative_hash,
    new_creative_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.rig_manifest import (
    RigLayer,
    RigManifest,
    RigPreviewTest,
    RigValidationReport,
    new_rig_preview_receipt,
    rig_manifest_hash,
)
from ccp_studio.repositories.acting_library import InMemoryActingLibraryRepository
from ccp_studio.repositories.creative_library_items import InMemoryCreativeLibraryRepository
from ccp_studio.repositories.rig_manifests import InMemoryRigManifestRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.rig_validation_service import RigValidationService


class CreativeLibraryServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class CreativeLibraryService:
    acting_repository: InMemoryActingLibraryRepository
    rig_repository: InMemoryRigManifestRepository = field(default_factory=InMemoryRigManifestRepository)
    creative_repository: InMemoryCreativeLibraryRepository = field(default_factory=InMemoryCreativeLibraryRepository)
    rig_validator: RigValidationService = field(default_factory=RigValidationService)

    def create_rig_manifest(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        acting_library_version_id: UUID,
        layers: list[RigLayer],
        mouth_shape_refs: list[str],
        eye_brow_variant_refs: list[str],
        gesture_variant_refs: list[str],
        body_layer_refs: list[str],
        preview_tests: list[RigPreviewTest],
    ) -> RigManifest:
        self._require_locked_acting_library(organization_id, brand_id, acting_library_version_id)
        manifest_id = uuid4()
        version_hash = rig_manifest_hash(
            {
                "manifest_id": str(manifest_id),
                "acting_library_version_id": str(acting_library_version_id),
                "layers": [layer.model_dump(mode="json") for layer in layers],
                "mouth_shape_refs": mouth_shape_refs,
                "eye_brow_variant_refs": eye_brow_variant_refs,
                "gesture_variant_refs": gesture_variant_refs,
                "body_layer_refs": body_layer_refs,
                "preview_tests": [test.model_dump(mode="json") for test in preview_tests],
            }
        )
        manifest = RigManifest(
            schema_version="cmf.rig_manifest.v1",
            rig_manifest_id=manifest_id,
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            acting_library_version_id=acting_library_version_id,
            layers=layers,
            mouth_shape_refs=mouth_shape_refs,
            eye_brow_variant_refs=eye_brow_variant_refs,
            gesture_variant_refs=gesture_variant_refs,
            body_layer_refs=body_layer_refs,
            preview_tests=preview_tests,
            version_hash=version_hash,
            status=CreativeItemStatus.draft,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.rig_repository.put_manifest(manifest)
        self.creative_repository.put_receipt(
            new_creative_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_genesis_session_id=brand_genesis_session_id,
                item_kind=CreativeLibraryItemKind.rig_manifest,
                item_id=manifest.rig_manifest_id,
                action="create_rig_manifest",
                decision_code="RIG_MANIFEST_CREATED",
                evidence_refs=[manifest.version_hash],
            )
        )
        return manifest

    def validate_rig_manifest(self, *, organization_id: UUID, brand_id: UUID, rig_manifest_id: UUID) -> RigValidationReport:
        manifest = self._rig_for_brand(organization_id, brand_id, rig_manifest_id)
        blockers = self.rig_validator.blocker_codes(manifest)
        failed = [test.test_name for test in manifest.preview_tests if not test.passed]
        report = RigValidationReport(
            schema_version="cmf.rig_validation_report.v1",
            rig_manifest_id=manifest.rig_manifest_id,
            organization_id=organization_id,
            brand_id=brand_id,
            passed=not blockers,
            blocker_codes=blockers,
            failed_preview_tests=failed,
            created_at=utc_now(),
        )
        self.rig_repository.put_validation_report(report)
        self.rig_repository.put_preview_receipt(
            new_rig_preview_receipt(
                manifest=manifest,
                decision_code="RIG_PREVIEW_PASSED" if report.passed else "RIG_PREVIEW_FAILED",
                blocker_codes=blockers,
                evidence_refs=failed or [manifest.version_hash],
            )
        )
        return report

    def approve_rig(self, *, organization_id: UUID, brand_id: UUID, rig_manifest_id: UUID) -> RigManifest:
        manifest = self._rig_for_brand(organization_id, brand_id, rig_manifest_id)
        self._reject_locked(manifest.status)
        report = self.validate_rig_manifest(
            organization_id=organization_id,
            brand_id=brand_id,
            rig_manifest_id=rig_manifest_id,
        )
        if not report.passed:
            failed = manifest.model_copy(update={"status": CreativeItemStatus.evaluation_failed, "updated_at": utc_now()})
            self.rig_repository.put_manifest(failed)
            raise CreativeLibraryServiceError(report.blocker_codes[0], "Rig manifest failed preview validation.")
        approved = manifest.model_copy(update={"status": CreativeItemStatus.approved, "updated_at": utc_now()})
        self.rig_repository.put_manifest(approved)
        return approved

    def lock_rig(self, *, organization_id: UUID, brand_id: UUID, rig_manifest_id: UUID) -> RigManifest:
        manifest = self._rig_for_brand(organization_id, brand_id, rig_manifest_id)
        if manifest.status != CreativeItemStatus.approved:
            raise CreativeLibraryServiceError("RIG_NOT_APPROVED", "Rig must be approved before lock.")
        locked = manifest.model_copy(update={"status": CreativeItemStatus.locked, "locked_at": utc_now(), "updated_at": utc_now()})
        return self.rig_repository.put_manifest(locked)

    def reject_rig(self, *, organization_id: UUID, brand_id: UUID, rig_manifest_id: UUID, reason: str) -> RigManifest:
        manifest = self._rig_for_brand(organization_id, brand_id, rig_manifest_id)
        self._reject_locked(manifest.status)
        rejected = manifest.model_copy(update={"status": CreativeItemStatus.rejected, "updated_at": utc_now()})
        self.rig_repository.put_manifest(rejected)
        self.creative_repository.put_receipt(
            new_creative_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_genesis_session_id=manifest.brand_genesis_session_id,
                item_kind=CreativeLibraryItemKind.rig_manifest,
                item_id=manifest.rig_manifest_id,
                action="reject_rig",
                decision_code="RIG_REJECTED",
                evidence_refs=[reason],
            )
        )
        return rejected

    def repair_rig_manifest(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        rig_manifest_id: UUID,
        layers: list[RigLayer] | None = None,
        preview_tests: list[RigPreviewTest] | None = None,
        repair_note: str,
    ) -> RigManifest:
        manifest = self._rig_for_brand(organization_id, brand_id, rig_manifest_id)
        self._reject_locked(manifest.status)
        updated_layers = layers if layers is not None else manifest.layers
        updated_preview_tests = preview_tests if preview_tests is not None else manifest.preview_tests
        version_hash = rig_manifest_hash(
            {
                "manifest_id": str(manifest.rig_manifest_id),
                "acting_library_version_id": str(manifest.acting_library_version_id),
                "layers": [layer.model_dump(mode="json") for layer in updated_layers],
                "mouth_shape_refs": manifest.mouth_shape_refs,
                "eye_brow_variant_refs": manifest.eye_brow_variant_refs,
                "gesture_variant_refs": manifest.gesture_variant_refs,
                "body_layer_refs": manifest.body_layer_refs,
                "preview_tests": [test.model_dump(mode="json") for test in updated_preview_tests],
                "repair_note": repair_note,
            }
        )
        repaired = manifest.model_copy(
            update={
                "layers": updated_layers,
                "preview_tests": updated_preview_tests,
                "version_hash": version_hash,
                "status": CreativeItemStatus.draft,
                "updated_at": utc_now(),
            }
        )
        self.rig_repository.put_manifest(repaired)
        self.creative_repository.put_receipt(
            new_creative_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_genesis_session_id=manifest.brand_genesis_session_id,
                item_kind=CreativeLibraryItemKind.rig_manifest,
                item_id=manifest.rig_manifest_id,
                action="repair_rig",
                decision_code="RIG_REPAIRED",
                evidence_refs=[repair_note, version_hash],
            )
        )
        return repaired

    def create_micro_semiotic_anchor(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        name: str,
        category: str,
        cultural_context: str,
        audience_signal: str,
        recognition_effects: list[str],
        visual_description: str,
        preferred_placement: list[str],
        subtlety_score: float,
        comment_potential_score: float,
        brand_fit_score: float,
        distraction_risk_score: float,
        legal_risk_score: float,
        use_constraints: list[str],
        source_refs: list[str],
    ) -> MicroSemioticAnchor:
        item_id = uuid4()
        version_hash = creative_hash(
            {
                "kind": "micro_semiotic_anchor",
                "item_id": str(item_id),
                "name": name,
                "category": category,
                "cultural_context": cultural_context,
                "visual_description": visual_description,
                "source_refs": source_refs,
            }
        )
        anchor = MicroSemioticAnchor(
            schema_version="cmf.micro_semiotic_anchor.v1",
            micro_semiotic_anchor_id=item_id,
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            name=name,
            category=category,
            cultural_context=cultural_context,
            audience_signal=audience_signal,
            recognition_effects=recognition_effects,
            visual_description=visual_description,
            preferred_placement=preferred_placement,
            subtlety_score=subtlety_score,
            comment_potential_score=comment_potential_score,
            brand_fit_score=brand_fit_score,
            distraction_risk_score=distraction_risk_score,
            legal_risk_score=legal_risk_score,
            use_constraints=use_constraints,
            source_refs=source_refs,
            version_hash=version_hash,
            status=CreativeItemStatus.draft,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        return self.creative_repository.put_anchor(anchor)

    def create_motion_recipe(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        name: str,
        motion_language: str,
        motion_intensity: str,
        max_simultaneous_moving_layers: int,
        beats: list[MotionBeat],
        source_refs: list[str],
        use_constraints: list[str],
        evaluation_state: CreativeEvaluationState,
    ) -> MotionRecipe:
        item_id = uuid4()
        recipe = MotionRecipe(
            schema_version="cmf.motion_recipe.v1",
            motion_recipe_id=item_id,
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            name=name,
            motion_language=motion_language,
            motion_intensity=motion_intensity,
            max_simultaneous_moving_layers=max_simultaneous_moving_layers,
            beats=beats,
            use_constraints=use_constraints,
            source_refs=source_refs,
            version_hash=creative_hash({"kind": "motion_recipe", "item_id": str(item_id), "beats": [beat.model_dump() for beat in beats]}),
            evaluation_state=evaluation_state,
            status=CreativeItemStatus.draft,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        return self.creative_repository.put_motion_recipe(recipe)

    def create_sfx_asset(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        category: str,
        event_mapping: str,
        asset_uri: str,
        use_context: str,
        source_refs: list[str],
        evaluation_state: CreativeEvaluationState,
    ) -> SfxAsset:
        item_id = uuid4()
        asset = SfxAsset(
            schema_version="cmf.sfx_asset.v1",
            sfx_asset_id=item_id,
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            category=category,
            event_mapping=event_mapping,
            asset_uri=asset_uri,
            use_context=use_context,
            source_refs=source_refs,
            version_hash=creative_hash({"kind": "sfx_asset", "item_id": str(item_id), "asset_uri": asset_uri, "source_refs": source_refs}),
            evaluation_state=evaluation_state,
            status=CreativeItemStatus.draft,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        return self.creative_repository.put_sfx_asset(asset)

    def create_composition_preference(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        name: str,
        aspect_ratio: str,
        subject_placement: str,
        text_safe_zones: list[str],
        negative_space_rules: list[str],
        source_refs: list[str],
        evaluation_state: CreativeEvaluationState,
    ) -> CompositionPreference:
        item_id = uuid4()
        preference = CompositionPreference(
            schema_version="cmf.composition_preference.v1",
            composition_preference_id=item_id,
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            name=name,
            aspect_ratio=aspect_ratio,
            subject_placement=subject_placement,
            text_safe_zones=text_safe_zones,
            negative_space_rules=negative_space_rules,
            source_refs=source_refs,
            version_hash=creative_hash({"kind": "composition_preference", "item_id": str(item_id), "negative_space_rules": negative_space_rules}),
            evaluation_state=evaluation_state,
            status=CreativeItemStatus.draft,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        return self.creative_repository.put_composition_preference(preference)

    def configure_platform_profile(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        platform: str,
        aspect_ratio: str,
        caption_requirements: list[str],
        negative_space_requirements: list[str],
        publishing_requirements: list[str],
    ) -> PlatformProfile:
        if not caption_requirements or not negative_space_requirements or not aspect_ratio or not publishing_requirements:
            raise CreativeLibraryServiceError("PLATFORM_PROFILE_RULES_REQUIRED", "Caption, negative-space, aspect, and publishing rules are required.")
        profile_id = uuid4()
        profile = PlatformProfile(
            schema_version="cmf.platform_profile.v1",
            platform_profile_id=profile_id,
            organization_id=organization_id,
            brand_id=brand_id,
            platform=platform,
            aspect_ratio=aspect_ratio,
            caption_requirements=caption_requirements,
            negative_space_requirements=negative_space_requirements,
            publishing_requirements=publishing_requirements,
            version_hash=creative_hash(
                {
                    "platform": platform,
                    "aspect_ratio": aspect_ratio,
                    "caption_requirements": caption_requirements,
                    "negative_space_requirements": negative_space_requirements,
                    "publishing_requirements": publishing_requirements,
                }
            ),
            status=CreativeItemStatus.approved,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.creative_repository.put_platform_profile(profile)
        self.creative_repository.put_receipt(
            new_creative_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                item_kind=CreativeLibraryItemKind.platform_profile,
                item_id=profile.platform_profile_id,
                action="configure_platform_profile",
                decision_code="PLATFORM_PROFILE_CONFIGURED",
                evidence_refs=[profile.version_hash],
            )
        )
        return profile

    def approve_creative_item(self, *, organization_id: UUID, brand_id: UUID, item_id: UUID) -> Any:
        item = self._creative_item_for_brand(organization_id, brand_id, item_id)
        if not getattr(item, "source_refs", ["platform-profile"]):
            raise CreativeLibraryServiceError("CREATIVE_ITEM_SOURCE_REQUIRED", "Creative library item source is required.")
        if not getattr(item, "version_hash", None):
            raise CreativeLibraryServiceError("CREATIVE_ITEM_VERSION_HASH_REQUIRED", "Creative library item version hash is required.")
        if isinstance(item, MicroSemioticAnchor):
            if item.legal_risk_score > 0.35 or item.distraction_risk_score > 0.4 or item.subtlety_score < 0.6 or item.brand_fit_score < 0.75:
                failed = item.model_copy(update={"status": CreativeItemStatus.evaluation_failed, "updated_at": utc_now()})
                self.creative_repository.put_anchor(failed)
                raise CreativeLibraryServiceError("CREATIVE_ITEM_EVALUATION_FAILED", "Micro-semiotic anchor failed risk or fit gate.")
            approved = item.model_copy(update={"status": CreativeItemStatus.approved, "updated_at": utc_now()})
            self.creative_repository.put_anchor(approved)
            return approved
        evaluation = getattr(item, "evaluation_state", None)
        if evaluation is None:
            raise CreativeLibraryServiceError("CREATIVE_ITEM_EVALUATION_REQUIRED", "Creative library item evaluation is required.")
        if not evaluation.passed:
            raise CreativeLibraryServiceError("CREATIVE_ITEM_EVALUATION_FAILED", "Creative library item failed evaluation.")
        approved = item.model_copy(update={"status": CreativeItemStatus.approved, "updated_at": utc_now()})
        self._put_creative_item(approved)
        return approved

    def select_creative_item(self, *, organization_id: UUID, brand_id: UUID, item_id: UUID) -> Any:
        item = self._creative_item_for_brand(organization_id, brand_id, item_id)
        if item.status not in {CreativeItemStatus.approved, CreativeItemStatus.locked}:
            raise CreativeLibraryServiceError("CREATIVE_ITEM_NOT_APPROVED", "Creative library item must be approved before selection.")
        return item

    def render_contract_profile_requirements(self, *, organization_id: UUID, brand_id: UUID, platform_profile_id: UUID) -> dict[str, Any]:
        profile = self.creative_repository.platform_profiles.get(platform_profile_id)
        if profile is None:
            raise CreativeLibraryServiceError("PLATFORM_PROFILE_REQUIRED", "Platform profile is required.")
        if profile.organization_id != organization_id or profile.brand_id != brand_id:
            raise CreativeLibraryServiceError("BRAND_SCOPE_VIOLATION", "Platform profile is outside the active brand scope.")
        if profile.status != CreativeItemStatus.approved:
            raise CreativeLibraryServiceError("PLATFORM_PROFILE_NOT_APPROVED", "Platform profile must be approved.")
        return {
            "platform": profile.platform,
            "aspect_ratio": profile.aspect_ratio,
            "caption_requirements": profile.caption_requirements,
            "negative_space_requirements": profile.negative_space_requirements,
            "publishing_requirements": profile.publishing_requirements,
            "profile_version_hash": profile.version_hash,
        }

    def _require_locked_acting_library(self, organization_id: UUID, brand_id: UUID, version_id: UUID) -> None:
        version = self.acting_repository.versions.get(version_id)
        if version is None:
            raise CreativeLibraryServiceError("ACTING_LIBRARY_VERSION_REQUIRED", "Acting library version is required.")
        if version.organization_id != organization_id or version.brand_id != brand_id:
            raise CreativeLibraryServiceError("BRAND_SCOPE_VIOLATION", "Acting library version is outside the active brand scope.")
        if not version.locked:
            raise CreativeLibraryServiceError("ACTING_LIBRARY_VERSION_NOT_LOCKED", "Paper-cut rig requires a locked acting library.")
        references = [self.acting_repository.references[item] for item in version.acting_reference_ids]
        if any(reference.status != ActingReferenceStatus.locked for reference in references):
            raise CreativeLibraryServiceError("ACTING_REFERENCE_NOT_APPROVED", "Paper-cut rig requires locked acting references.")

    def _rig_for_brand(self, organization_id: UUID, brand_id: UUID, rig_manifest_id: UUID) -> RigManifest:
        manifest = self.rig_repository.manifests.get(rig_manifest_id)
        if manifest is None:
            raise CreativeLibraryServiceError("RIG_MANIFEST_REQUIRED", "Rig manifest is required.")
        if manifest.organization_id != organization_id or manifest.brand_id != brand_id:
            raise CreativeLibraryServiceError("BRAND_SCOPE_VIOLATION", "Rig manifest is outside the active brand scope.")
        return manifest

    def _creative_item_for_brand(self, organization_id: UUID, brand_id: UUID, item_id: UUID) -> Any:
        item = self.creative_repository.get_item(item_id)
        if item is None:
            raise CreativeLibraryServiceError("CREATIVE_ITEM_REQUIRED", "Creative library item is required.")
        if item.organization_id != organization_id or item.brand_id != brand_id:
            raise CreativeLibraryServiceError("BRAND_SCOPE_VIOLATION", "Creative library item is outside the active brand scope.")
        return item

    def _put_creative_item(self, item: Any) -> None:
        if isinstance(item, MotionRecipe):
            self.creative_repository.put_motion_recipe(item)
        elif isinstance(item, SfxAsset):
            self.creative_repository.put_sfx_asset(item)
        elif isinstance(item, CompositionPreference):
            self.creative_repository.put_composition_preference(item)
        elif isinstance(item, PlatformProfile):
            self.creative_repository.put_platform_profile(item)

    @staticmethod
    def _reject_locked(status: CreativeItemStatus) -> None:
        if status == CreativeItemStatus.locked:
            raise CreativeLibraryServiceError("CREATIVE_ITEM_IMMUTABLE", "Locked creative item is immutable.")


@dataclass
class CreativeLibraryCommandHandler:
    command_type: str
    service: CreativeLibraryService
    aggregate_type: str = "creative_library"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "GenerateRigManifestCommand":
            manifest = self.service.create_rig_manifest(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                brand_genesis_session_id=UUID(payload["brand_genesis_session_id"]),
                acting_library_version_id=UUID(payload["acting_library_version_id"]),
                layers=[RigLayer(**item) for item in payload["layers"]],
                mouth_shape_refs=payload["mouth_shape_refs"],
                eye_brow_variant_refs=payload["eye_brow_variant_refs"],
                gesture_variant_refs=payload["gesture_variant_refs"],
                body_layer_refs=payload["body_layer_refs"],
                preview_tests=[RigPreviewTest(**item) for item in payload["preview_tests"]],
            )
            return manifest.model_dump(mode="json")
        if self.command_type == "RunRigPreviewTestsCommand":
            report = self.service.validate_rig_manifest(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                rig_manifest_id=UUID(payload["rig_manifest_id"]),
            )
            return report.model_dump(mode="json")
        if self.command_type == "RepairRigCommand":
            manifest = self.service.repair_rig_manifest(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                rig_manifest_id=UUID(payload["rig_manifest_id"]),
                layers=[RigLayer(**item) for item in payload["layers"]] if "layers" in payload else None,
                preview_tests=[RigPreviewTest(**item) for item in payload["preview_tests"]] if "preview_tests" in payload else None,
                repair_note=payload["repair_note"],
            )
            return manifest.model_dump(mode="json")
        if self.command_type == "ApproveRigCommand":
            return self.service.approve_rig(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                rig_manifest_id=UUID(payload["rig_manifest_id"]),
            ).model_dump(mode="json")
        if self.command_type == "ConfigurePlatformProfileCommand":
            profile = self.service.configure_platform_profile(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                platform=payload["platform"],
                aspect_ratio=payload["aspect_ratio"],
                caption_requirements=payload["caption_requirements"],
                negative_space_requirements=payload["negative_space_requirements"],
                publishing_requirements=payload["publishing_requirements"],
            )
            return profile.model_dump(mode="json")
        if self.command_type == "CreateCreativeLibraryItemCommand":
            item_kind = payload["item_kind"]
            if item_kind == CreativeLibraryItemKind.micro_semiotic_anchor.value:
                item = self.service.create_micro_semiotic_anchor(
                    organization_id=envelope.organization_id,
                    brand_id=envelope.brand_id,
                    brand_genesis_session_id=UUID(payload["brand_genesis_session_id"]),
                    name=payload["name"],
                    category=payload["category"],
                    cultural_context=payload["cultural_context"],
                    audience_signal=payload["audience_signal"],
                    recognition_effects=payload["recognition_effects"],
                    visual_description=payload["visual_description"],
                    preferred_placement=payload["preferred_placement"],
                    subtlety_score=payload["subtlety_score"],
                    comment_potential_score=payload["comment_potential_score"],
                    brand_fit_score=payload["brand_fit_score"],
                    distraction_risk_score=payload["distraction_risk_score"],
                    legal_risk_score=payload["legal_risk_score"],
                    use_constraints=payload.get("use_constraints", []),
                    source_refs=payload["source_refs"],
                )
                return item.model_dump(mode="json")
            if item_kind == CreativeLibraryItemKind.motion_recipe.value:
                item = self.service.create_motion_recipe(
                    organization_id=envelope.organization_id,
                    brand_id=envelope.brand_id,
                    brand_genesis_session_id=UUID(payload["brand_genesis_session_id"]),
                    name=payload["name"],
                    motion_language=payload["motion_language"],
                    motion_intensity=payload["motion_intensity"],
                    max_simultaneous_moving_layers=payload["max_simultaneous_moving_layers"],
                    beats=[MotionBeat(**item) for item in payload["beats"]],
                    source_refs=payload["source_refs"],
                    use_constraints=payload.get("use_constraints", []),
                    evaluation_state=CreativeEvaluationState(**payload["evaluation_state"]),
                )
                return item.model_dump(mode="json")
            if item_kind == CreativeLibraryItemKind.sfx_asset.value:
                item = self.service.create_sfx_asset(
                    organization_id=envelope.organization_id,
                    brand_id=envelope.brand_id,
                    brand_genesis_session_id=UUID(payload["brand_genesis_session_id"]),
                    category=payload["category"],
                    event_mapping=payload["event_mapping"],
                    asset_uri=payload["asset_uri"],
                    use_context=payload["use_context"],
                    source_refs=payload["source_refs"],
                    evaluation_state=CreativeEvaluationState(**payload["evaluation_state"]),
                )
                return item.model_dump(mode="json")
            if item_kind == CreativeLibraryItemKind.composition_preference.value:
                item = self.service.create_composition_preference(
                    organization_id=envelope.organization_id,
                    brand_id=envelope.brand_id,
                    brand_genesis_session_id=UUID(payload["brand_genesis_session_id"]),
                    name=payload["name"],
                    aspect_ratio=payload["aspect_ratio"],
                    subject_placement=payload["subject_placement"],
                    text_safe_zones=payload["text_safe_zones"],
                    negative_space_rules=payload["negative_space_rules"],
                    source_refs=payload["source_refs"],
                    evaluation_state=CreativeEvaluationState(**payload["evaluation_state"]),
                )
                return item.model_dump(mode="json")
            raise CreativeLibraryServiceError("CREATIVE_ITEM_KIND_UNSUPPORTED", item_kind)
        if self.command_type == "ApproveCreativeLibraryItemCommand":
            return self.service.approve_creative_item(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                item_id=UUID(payload["item_id"]),
            ).model_dump(mode="json")
        raise CreativeLibraryServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        for key in ["rig_manifest_id", "item_id", "platform_profile_id", "acting_library_version_id"]:
            raw = payload.get(key)
            if isinstance(raw, str):
                return UUID(raw)
            if isinstance(raw, UUID):
                return raw
        return envelope.brand_id


def register_creative_library_command_handlers(bus: CommandBus, service: CreativeLibraryService) -> None:
    for command_type in [
        "GenerateRigManifestCommand",
        "RunRigPreviewTestsCommand",
        "RepairRigCommand",
        "ApproveRigCommand",
        "CreateCreativeLibraryItemCommand",
        "ConfigurePlatformProfileCommand",
        "ApproveCreativeLibraryItemCommand",
    ]:
        bus.register_handler(CreativeLibraryCommandHandler(command_type=command_type, service=service))
