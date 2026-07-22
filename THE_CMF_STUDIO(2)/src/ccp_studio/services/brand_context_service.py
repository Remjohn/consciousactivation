"""Brand Context version locking and forking service for TS-CMF-021."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.acting_library import ActingReferenceStatus
from ccp_studio.contracts.brand_context import (
    BrandContextAssetBundle,
    BrandContextForkRequest,
    BrandContextLineageRef,
    BrandContextReceipt,
    BrandContextStatus,
    BrandContextVersion,
    GenesisClearanceCertificate,
    brand_context_version_hash,
    new_brand_context_receipt,
)
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.creative_libraries import CreativeItemStatus
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.acting_library import InMemoryActingLibraryRepository
from ccp_studio.repositories.brand_context_versions import InMemoryBrandContextRepository
from ccp_studio.repositories.creative_library_items import InMemoryCreativeLibraryRepository
from ccp_studio.repositories.rig_manifests import InMemoryRigManifestRepository
from ccp_studio.services.command_bus import CommandBus


class BrandContextServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class BrandContextService:
    acting_repository: InMemoryActingLibraryRepository
    rig_repository: InMemoryRigManifestRepository
    creative_repository: InMemoryCreativeLibraryRepository
    repository: InMemoryBrandContextRepository = field(default_factory=InMemoryBrandContextRepository)

    def create_draft(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        asset_bundle: BrandContextAssetBundle,
        created_by_actor_id: UUID,
        parent_brand_context_version_id: UUID | None = None,
        approved_change_reason: str | None = None,
    ) -> BrandContextVersion:
        self._validate_asset_bundle(organization_id, brand_id, asset_bundle)
        version_id = uuid4()
        version_hash = self._hash_asset_bundle(
            brand_context_version_id=version_id,
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            parent_brand_context_version_id=parent_brand_context_version_id,
            asset_bundle=asset_bundle,
        )
        version = BrandContextVersion(
            schema_version="cmf.brand_context_version.v1",
            brand_context_version_id=version_id,
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=brand_genesis_session_id,
            parent_brand_context_version_id=parent_brand_context_version_id,
            status=BrandContextStatus.draft,
            version_hash=version_hash,
            asset_bundle=asset_bundle,
            approved_change_reason=approved_change_reason,
            created_by_actor_id=created_by_actor_id,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.repository.put_version(version)
        self.repository.put_receipt(
            new_brand_context_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_context_version_id=version.brand_context_version_id,
                action="CreateBrandContextDraftCommand",
                decision_code="BRAND_CONTEXT_VERSION_DRAFTED",
                evidence_refs=[version.version_hash],
            )
        )
        return version

    def lock_version(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_context_version_id: UUID,
        approved_by_actor_id: UUID,
    ) -> BrandContextVersion:
        version = self._version_for_brand(organization_id, brand_id, brand_context_version_id)
        if version.status != BrandContextStatus.draft:
            raise BrandContextServiceError("BRAND_CONTEXT_NOT_DRAFT", "Only draft context versions can be locked.")
        self._validate_asset_bundle(organization_id, brand_id, version.asset_bundle)
        certificate = GenesisClearanceCertificate(
            schema_version="cmf.genesis_clearance_certificate.v1",
            genesis_clearance_certificate_id=uuid4(),
            brand_context_version_id=version.brand_context_version_id,
            organization_id=organization_id,
            brand_id=brand_id,
            acting_library_version_id=version.asset_bundle.acting_library_version_id,
            rig_manifest_id=version.asset_bundle.rig_manifest_id,
            creative_library_receipt_ids=version.asset_bundle.creative_library_receipt_ids,
            evaluation_receipt_ids=version.asset_bundle.evaluation_receipt_ids,
            version_hash=version.version_hash,
            approved_by_actor_id=approved_by_actor_id,
            issued_at=utc_now(),
        )
        self.repository.put_certificate(certificate)
        locked = version.model_copy(
            update={
                "status": BrandContextStatus.locked,
                "clearance_certificate_id": certificate.genesis_clearance_certificate_id,
                "locked_by_actor_id": approved_by_actor_id,
                "locked_at": utc_now(),
                "updated_at": utc_now(),
            }
        )
        self.repository.put_version(locked)
        self.repository.put_receipt(
            new_brand_context_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_context_version_id=locked.brand_context_version_id,
                action="LockBrandContextVersionCommand",
                decision_code="GENESIS_CLEARANCE_CERTIFICATE_ISSUED",
                evidence_refs=[str(certificate.genesis_clearance_certificate_id), locked.version_hash],
            )
        )
        return locked

    def fork_version(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        parent_brand_context_version_id: UUID,
        replacement_asset_bundle: BrandContextAssetBundle,
        requested_by_actor_id: UUID,
        approved_by_actor_id: UUID,
        approved_change_reason: str,
        lock_child: bool = True,
    ) -> BrandContextVersion:
        parent = self._version_for_brand(organization_id, brand_id, parent_brand_context_version_id)
        if parent.status not in {BrandContextStatus.locked, BrandContextStatus.superseded}:
            raise BrandContextServiceError("BRAND_CONTEXT_NOT_LOCKED", "Forks require a locked parent context.")
        request = BrandContextForkRequest(
            schema_version="cmf.brand_context_fork_request.v1",
            brand_context_fork_request_id=uuid4(),
            parent_brand_context_version_id=parent.brand_context_version_id,
            organization_id=organization_id,
            brand_id=brand_id,
            approved_change_reason=approved_change_reason,
            requested_by_actor_id=requested_by_actor_id,
            approved_by_actor_id=approved_by_actor_id,
            created_at=utc_now(),
        )
        draft = self.create_draft(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_genesis_session_id=parent.brand_genesis_session_id,
            asset_bundle=replacement_asset_bundle,
            created_by_actor_id=requested_by_actor_id,
            parent_brand_context_version_id=parent.brand_context_version_id,
            approved_change_reason=approved_change_reason,
        )
        request = request.model_copy(update={"child_brand_context_version_id": draft.brand_context_version_id})
        self.repository.put_fork_request(request)
        child = (
            self.lock_version(
                organization_id=organization_id,
                brand_id=brand_id,
                brand_context_version_id=draft.brand_context_version_id,
                approved_by_actor_id=approved_by_actor_id,
            )
            if lock_child
            else draft
        )
        if child.status == BrandContextStatus.locked and parent.status == BrandContextStatus.locked:
            superseded = parent.model_copy(
                update={
                    "status": BrandContextStatus.superseded,
                    "superseded_by_brand_context_version_id": child.brand_context_version_id,
                    "updated_at": utc_now(),
                }
            )
            self.repository.put_version(superseded)
            self.repository.put_receipt(
                new_brand_context_receipt(
                    organization_id=organization_id,
                    brand_id=brand_id,
                    brand_context_version_id=parent.brand_context_version_id,
                    action="ForkBrandContextVersionCommand",
                    decision_code="BRAND_CONTEXT_VERSION_SUPERSEDED",
                    evidence_refs=[str(child.brand_context_version_id), approved_change_reason],
                )
            )
        return child

    def record_lineage_ref(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        downstream_object_id: UUID,
        downstream_object_type: str,
        brand_context_version_id: UUID,
    ) -> BrandContextLineageRef:
        version = self._version_for_brand(organization_id, brand_id, brand_context_version_id)
        if version.status not in {BrandContextStatus.locked, BrandContextStatus.superseded}:
            raise BrandContextServiceError("BRAND_CONTEXT_NOT_LOCKED", "Lineage requires a locked context version.")
        lineage_ref = BrandContextLineageRef(
            schema_version="cmf.brand_context_lineage_ref.v1",
            lineage_ref_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            downstream_object_id=downstream_object_id,
            downstream_object_type=downstream_object_type,
            brand_context_version_id=version.brand_context_version_id,
            brand_context_version_hash=version.version_hash,
            captured_at=utc_now(),
        )
        return self.repository.put_lineage_ref(lineage_ref)

    def resolve_lineage_ref(self, lineage_ref_id: UUID) -> BrandContextVersion:
        lineage = self.repository.lineage_refs.get(lineage_ref_id)
        if lineage is None:
            raise BrandContextServiceError("BRAND_CONTEXT_LINEAGE_REQUIRED", "Brand context lineage reference is required.")
        version = self.repository.versions.get(lineage.brand_context_version_id)
        if version is None or version.version_hash != lineage.brand_context_version_hash:
            raise BrandContextServiceError("BRAND_CONTEXT_LINEAGE_HASH_MISMATCH", "Stored lineage hash does not match context version.")
        return version

    def assert_context_selectable_for_production(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_context_version_id: UUID,
        allow_historical_superseded: bool = False,
    ) -> BrandContextVersion:
        version = self._version_for_brand(organization_id, brand_id, brand_context_version_id)
        if version.status == BrandContextStatus.draft:
            raise BrandContextServiceError("BRAND_CONTEXT_NOT_LOCKED", "Production requires a locked Brand Context Version.")
        if version.status == BrandContextStatus.superseded and not allow_historical_superseded:
            raise BrandContextServiceError("BRAND_CONTEXT_SUPERSEDED_REVIEW_REQUIRED", "Superseded Brand Context requires explicit historical use.")
        if version.status != BrandContextStatus.locked and not allow_historical_superseded:
            raise BrandContextServiceError("BRAND_CONTEXT_NOT_LOCKED", "Production requires a locked Brand Context Version.")
        return version

    def assert_asset_in_locked_context(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        brand_context_version_id: UUID,
        asset_id: UUID,
    ) -> None:
        version = self.assert_context_selectable_for_production(
            organization_id=organization_id,
            brand_id=brand_id,
            brand_context_version_id=brand_context_version_id,
        )
        bundle_ids = {
            version.asset_bundle.acting_library_version_id,
            version.asset_bundle.rig_manifest_id,
            *version.asset_bundle.micro_semiotic_anchor_ids,
            *version.asset_bundle.motion_recipe_ids,
            *version.asset_bundle.sfx_asset_ids,
            *version.asset_bundle.composition_preference_ids,
            *version.asset_bundle.platform_profile_ids,
        }
        if asset_id not in bundle_ids:
            raise BrandContextServiceError("BRAND_CONTEXT_ASSET_NOT_APPROVED", "Asset is not approved within this locked Brand Context Version.")

    def _validate_asset_bundle(self, organization_id: UUID, brand_id: UUID, asset_bundle: BrandContextAssetBundle) -> None:
        acting_version = self.acting_repository.versions.get(asset_bundle.acting_library_version_id)
        if acting_version is None or acting_version.organization_id != organization_id or acting_version.brand_id != brand_id:
            raise BrandContextServiceError("ACTING_LIBRARY_VERSION_REQUIRED", "Locked acting library version is required.")
        if not acting_version.locked:
            raise BrandContextServiceError("ACTING_LIBRARY_VERSION_NOT_LOCKED", "Acting library must be locked.")
        references = [self.acting_repository.references[item] for item in acting_version.acting_reference_ids]
        if any(reference.status != ActingReferenceStatus.locked for reference in references):
            raise BrandContextServiceError("ACTING_REFERENCE_NOT_APPROVED", "Acting references must be locked.")
        rig = self.rig_repository.manifests.get(asset_bundle.rig_manifest_id)
        if rig is None or rig.organization_id != organization_id or rig.brand_id != brand_id:
            raise BrandContextServiceError("RIG_MANIFEST_REQUIRED", "Approved rig manifest is required.")
        if rig.status != CreativeItemStatus.locked:
            raise BrandContextServiceError("RIG_NOT_APPROVED", "Rig manifest must be locked.")
        for item_id in [
            *asset_bundle.micro_semiotic_anchor_ids,
            *asset_bundle.motion_recipe_ids,
            *asset_bundle.sfx_asset_ids,
            *asset_bundle.composition_preference_ids,
            *asset_bundle.platform_profile_ids,
        ]:
            item = self.creative_repository.get_item(item_id)
            if item is None:
                raise BrandContextServiceError("CREATIVE_ITEM_REQUIRED", "Creative library item is required.")
            if item.organization_id != organization_id or item.brand_id != brand_id:
                raise BrandContextServiceError("BRAND_SCOPE_VIOLATION", "Creative item is outside the active brand scope.")
            if item.status not in {CreativeItemStatus.approved, CreativeItemStatus.locked}:
                raise BrandContextServiceError("CREATIVE_ITEM_NOT_APPROVED", "Creative item must be approved.")

    def _hash_asset_bundle(
        self,
        *,
        brand_context_version_id: UUID,
        organization_id: UUID,
        brand_id: UUID,
        brand_genesis_session_id: UUID,
        parent_brand_context_version_id: UUID | None,
        asset_bundle: BrandContextAssetBundle,
    ) -> str:
        acting_version = self.acting_repository.versions[asset_bundle.acting_library_version_id]
        rig = self.rig_repository.manifests[asset_bundle.rig_manifest_id]
        creative_hashes = []
        for item_id in [
            *asset_bundle.micro_semiotic_anchor_ids,
            *asset_bundle.motion_recipe_ids,
            *asset_bundle.sfx_asset_ids,
            *asset_bundle.composition_preference_ids,
            *asset_bundle.platform_profile_ids,
        ]:
            item = self.creative_repository.get_item(item_id)
            creative_hashes.append(getattr(item, "version_hash"))
        return brand_context_version_hash(
            {
                "brand_context_version_id": str(brand_context_version_id),
                "organization_id": str(organization_id),
                "brand_id": str(brand_id),
                "brand_genesis_session_id": str(brand_genesis_session_id),
                "parent_brand_context_version_id": str(parent_brand_context_version_id) if parent_brand_context_version_id else None,
                "acting_library_hash": acting_version.version_hash,
                "rig_hash": rig.version_hash,
                "creative_hashes": sorted(creative_hashes),
                "asset_bundle": asset_bundle.model_dump(mode="json"),
            }
        )

    def _version_for_brand(self, organization_id: UUID, brand_id: UUID, version_id: UUID) -> BrandContextVersion:
        version = self.repository.versions.get(version_id)
        if version is None:
            raise BrandContextServiceError("BRAND_CONTEXT_REQUIRED", "Brand Context Version is required.")
        if version.organization_id != organization_id or version.brand_id != brand_id:
            raise BrandContextServiceError("BRAND_SCOPE_VIOLATION", "Brand Context Version is outside the active brand scope.")
        return version


@dataclass
class BrandContextCommandHandler:
    command_type: str
    service: BrandContextService
    aggregate_type: str = "brand_context"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CreateBrandContextDraftCommand":
            version = self.service.create_draft(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                brand_genesis_session_id=UUID(payload["brand_genesis_session_id"]),
                asset_bundle=BrandContextAssetBundle(**payload["asset_bundle"]),
                created_by_actor_id=envelope.actor.actor_id,
            )
            return version.model_dump(mode="json")
        if self.command_type == "LockBrandContextVersionCommand":
            return self.service.lock_version(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                brand_context_version_id=UUID(payload["brand_context_version_id"]),
                approved_by_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "ForkBrandContextVersionCommand":
            return self.service.fork_version(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                parent_brand_context_version_id=UUID(payload["parent_brand_context_version_id"]),
                replacement_asset_bundle=BrandContextAssetBundle(**payload["replacement_asset_bundle"]),
                requested_by_actor_id=envelope.actor.actor_id,
                approved_by_actor_id=UUID(payload.get("approved_by_actor_id", str(envelope.actor.actor_id))),
                approved_change_reason=payload["approved_change_reason"],
            ).model_dump(mode="json")
        if self.command_type == "ResolveBrandContextLineageCommand":
            return self.service.resolve_lineage_ref(UUID(payload["lineage_ref_id"])).model_dump(mode="json")
        if self.command_type == "BlockStaleBrandContextCommand":
            return self.service.assert_context_selectable_for_production(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                brand_context_version_id=UUID(payload["brand_context_version_id"]),
            ).model_dump(mode="json")
        raise BrandContextServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("brand_context_version_id") or payload.get("parent_brand_context_version_id")
        if isinstance(raw, str):
            return UUID(raw)
        return envelope.brand_id


def register_brand_context_command_handlers(bus: CommandBus, service: BrandContextService) -> None:
    for command_type in [
        "CreateBrandContextDraftCommand",
        "LockBrandContextVersionCommand",
        "ForkBrandContextVersionCommand",
        "ResolveBrandContextLineageCommand",
        "BlockStaleBrandContextCommand",
    ]:
        bus.register_handler(BrandContextCommandHandler(command_type=command_type, service=service))
