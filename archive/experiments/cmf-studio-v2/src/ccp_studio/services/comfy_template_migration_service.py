"""ComfyUI template migration service for TS-CMF-046."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.comfy_gpu_worker import ComfyWorkflowAsset
from ccp_studio.contracts.comfy_template_migration import (
    ComfyWorkflowInputContract,
    ComfyWorkflowOutputContract,
    MigratedComfyWorkflowAsset,
    TemplateCompatibilityNote,
    WorkerAssetStatus,
    comfy_template_hash,
    new_template_migration_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.comfy_template_migration import InMemoryComfyTemplateMigrationRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.comfy_gpu_worker_service import ComfyGpuWorkerService


class ComfyTemplateMigrationError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ComfyTemplateMigrationService:
    gpu_worker_service: ComfyGpuWorkerService | None = None
    repository: InMemoryComfyTemplateMigrationRepository = field(default_factory=InMemoryComfyTemplateMigrationRepository)

    def migrate_template_to_worker_asset(
        self,
        *,
        legacy_source_path: str,
        template_json: dict[str, Any],
        required_inputs: list[dict[str, Any]],
        output_contract: dict[str, Any],
        compatibility_notes: list[dict[str, Any]] | None,
        known_defects: list[str],
        eval_target: str,
        eval_passed: bool,
        reviewer_id: UUID,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> MigratedComfyWorkflowAsset:
        if not required_inputs:
            raise ComfyTemplateMigrationError("COMFY_WORKFLOW_INPUTS_REQUIRED", "Comfy workflow assets require typed inputs.")
        if not output_contract.get("output_contract"):
            raise ComfyTemplateMigrationError("COMFY_WORKFLOW_OUTPUT_CONTRACT_REQUIRED", "Comfy workflow assets require an output contract.")
        if not eval_target:
            raise ComfyTemplateMigrationError("COMFY_WORKFLOW_EVAL_TARGET_REQUIRED", "Comfy workflow assets require an eval target.")
        content_hash = comfy_template_hash(template_json)
        now = utc_now()
        asset = self.repository.put_asset(
            MigratedComfyWorkflowAsset(
                schema_version="cmf.migrated_comfy_workflow_asset.v1",
                comfy_workflow_asset_id=uuid4(),
                legacy_source_path=legacy_source_path,
                content_hash=content_hash,
                storage_uri=f"worker-assets/comfyui-workflows/{content_hash}.json",
                required_inputs=[
                    ComfyWorkflowInputContract(schema_version="cmf.comfy_workflow_input_contract.v1", **item)
                    for item in required_inputs
                ],
                output_contract=ComfyWorkflowOutputContract(schema_version="cmf.comfy_workflow_output_contract.v1", **output_contract),
                compatibility_notes=[
                    TemplateCompatibilityNote(schema_version="cmf.template_compatibility_note.v1", **item)
                    for item in (compatibility_notes or [])
                ],
                known_defects=known_defects,
                eval_target=eval_target,
                eval_passed=eval_passed,
                reviewer_id=reviewer_id,
                status=WorkerAssetStatus.draft if eval_passed else WorkerAssetStatus.inactive,
                created_at=now,
                updated_at=now,
            )
        )
        self.repository.put_receipt(
            new_template_migration_receipt(
                actor_id=actor_id,
                status=asset.status,
                decision_code="COMFY_TEMPLATE_MIGRATED_TO_WORKER_ASSET",
                evidence_refs=[asset.legacy_source_path, asset.content_hash, asset.storage_uri],
                asset=asset,
                command_id=command_id,
            )
        )
        return asset

    def validate_comfy_workflow_inputs(self, *, comfy_workflow_asset_id: UUID, provided_inputs: dict[str, Any]) -> dict[str, Any]:
        asset = self._asset(comfy_workflow_asset_id)
        missing = [
            item.input_name
            for item in asset.required_inputs
            if item.required and item.input_name not in provided_inputs
        ]
        if missing:
            raise ComfyTemplateMigrationError("COMFY_WORKFLOW_INPUT_MISSING", f"Missing required Comfy workflow inputs: {', '.join(missing)}")
        for item in asset.required_inputs:
            if item.validation_rule == "sha256" and not str(provided_inputs.get(item.input_name, "")).startswith("sha256"):
                raise ComfyTemplateMigrationError("COMFY_WORKFLOW_INPUT_HASH_REQUIRED", f"{item.input_name} must be a sha256 hash.")
        return {"validated": True, "input_names": sorted(provided_inputs)}

    def activate_comfy_workflow_asset(
        self,
        comfy_workflow_asset_id: UUID,
        *,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> MigratedComfyWorkflowAsset:
        asset = self._asset(comfy_workflow_asset_id)
        if not asset.eval_passed:
            updated = self._update_asset_status(asset, WorkerAssetStatus.inactive)
            self.repository.put_receipt(
                new_template_migration_receipt(
                    actor_id=actor_id,
                    status=updated.status,
                    decision_code="COMFY_WORKFLOW_ASSET_ACTIVATION_BLOCKED",
                    evidence_refs=["EVAL_TARGET_NOT_PASSED"],
                    asset=updated,
                    command_id=command_id,
                )
            )
            raise ComfyTemplateMigrationError("COMFY_WORKFLOW_EVAL_NOT_PASSED", "Failed eval templates remain inactive.")
        if asset.status == WorkerAssetStatus.revalidation_required:
            raise ComfyTemplateMigrationError("COMFY_WORKFLOW_REVALIDATION_REQUIRED", "Template must be revalidated before activation.")
        active = self._update_asset_status(asset, WorkerAssetStatus.active)
        self._sync_gpu_worker_asset(active, approved=True)
        self.repository.put_receipt(
            new_template_migration_receipt(
                actor_id=actor_id,
                status=active.status,
                decision_code="COMFY_WORKFLOW_ASSET_ACTIVATED",
                evidence_refs=[active.content_hash, active.storage_uri],
                asset=active,
                command_id=command_id,
            )
        )
        return active

    def deactivate_comfy_workflow_asset(
        self,
        comfy_workflow_asset_id: UUID,
        *,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> MigratedComfyWorkflowAsset:
        asset = self._update_asset_status(self._asset(comfy_workflow_asset_id), WorkerAssetStatus.inactive)
        self._sync_gpu_worker_asset(asset, approved=False)
        self.repository.put_receipt(
            new_template_migration_receipt(
                actor_id=actor_id,
                status=asset.status,
                decision_code="COMFY_WORKFLOW_ASSET_DEACTIVATED",
                evidence_refs=[asset.content_hash],
                asset=asset,
                command_id=command_id,
            )
        )
        return asset

    def require_comfy_workflow_revalidation(
        self,
        comfy_workflow_asset_id: UUID,
        *,
        actor_id: UUID,
        reason: str,
        command_id: UUID | None = None,
    ) -> MigratedComfyWorkflowAsset:
        asset = self._update_asset_status(self._asset(comfy_workflow_asset_id), WorkerAssetStatus.revalidation_required)
        self._sync_gpu_worker_asset(asset, approved=False)
        self.repository.put_receipt(
            new_template_migration_receipt(
                actor_id=actor_id,
                status=asset.status,
                decision_code="COMFY_WORKFLOW_REVALIDATION_REQUIRED",
                evidence_refs=[reason],
                asset=asset,
                command_id=command_id,
            )
        )
        return asset

    def _sync_gpu_worker_asset(self, asset: MigratedComfyWorkflowAsset, *, approved: bool) -> None:
        if self.gpu_worker_service is None:
            return
        self.gpu_worker_service.repository.put_workflow_asset(
            ComfyWorkflowAsset(
                schema_version="cmf.comfy_workflow_asset.v1",
                workflow_asset_id=asset.comfy_workflow_asset_id,
                name=asset.legacy_source_path.split("/")[-1],
                workflow_hash=asset.content_hash,
                template_uri=asset.storage_uri,
                migrated_from_legacy_template=asset.legacy_source_path,
                approved=approved,
                approved_at=asset.updated_at,
            )
        )

    def _update_asset_status(self, asset: MigratedComfyWorkflowAsset, status: WorkerAssetStatus) -> MigratedComfyWorkflowAsset:
        updated = asset.model_copy(update={"status": status, "updated_at": utc_now()})
        return self.repository.put_asset(updated)

    def _asset(self, comfy_workflow_asset_id: UUID) -> MigratedComfyWorkflowAsset:
        asset = self.repository.assets.get(comfy_workflow_asset_id)
        if asset is None:
            raise ComfyTemplateMigrationError("COMFY_WORKFLOW_ASSET_REQUIRED", "Comfy workflow asset is required.")
        return asset


@dataclass
class ComfyTemplateMigrationCommandHandler:
    command_type: str
    service: ComfyTemplateMigrationService
    aggregate_type: str = "comfy_workflow_asset"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "migration_steward", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "MigrateComfyTemplateToWorkerAssetCommand":
            return self.service.migrate_template_to_worker_asset(
                legacy_source_path=payload["legacy_source_path"],
                template_json=payload["template_json"],
                required_inputs=payload["required_inputs"],
                output_contract=payload["output_contract"],
                compatibility_notes=payload.get("compatibility_notes"),
                known_defects=payload.get("known_defects", []),
                eval_target=payload["eval_target"],
                eval_passed=bool(payload.get("eval_passed", True)),
                reviewer_id=payload["reviewer_id"] if isinstance(payload.get("reviewer_id"), UUID) else UUID(payload.get("reviewer_id", str(envelope.actor.actor_id))),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ValidateComfyWorkflowInputsCommand":
            return self.service.validate_comfy_workflow_inputs(
                comfy_workflow_asset_id=UUID(payload["comfy_workflow_asset_id"]),
                provided_inputs=payload["provided_inputs"],
            )
        if self.command_type == "ActivateComfyWorkflowAssetCommand":
            return self.service.activate_comfy_workflow_asset(
                UUID(payload["comfy_workflow_asset_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "DeactivateComfyWorkflowAssetCommand":
            return self.service.deactivate_comfy_workflow_asset(
                UUID(payload["comfy_workflow_asset_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "RequireComfyWorkflowRevalidationCommand":
            return self.service.require_comfy_workflow_revalidation(
                UUID(payload["comfy_workflow_asset_id"]),
                actor_id=envelope.actor.actor_id,
                reason=payload["reason"],
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise ComfyTemplateMigrationError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("comfy_workflow_asset_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_comfy_template_migration_command_handlers(bus: CommandBus, service: ComfyTemplateMigrationService) -> None:
    for command_type in [
        "MigrateComfyTemplateToWorkerAssetCommand",
        "ValidateComfyWorkflowInputsCommand",
        "ActivateComfyWorkflowAssetCommand",
        "DeactivateComfyWorkflowAssetCommand",
        "RequireComfyWorkflowRevalidationCommand",
    ]:
        bus.register_handler(ComfyTemplateMigrationCommandHandler(command_type=command_type, service=service))
