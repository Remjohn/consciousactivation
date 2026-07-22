"""Migration workflows for TS-CMF-013 and TS-CMF-046."""

from ccp_studio.services.migration_service import MigrationService
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ccp_studio.contracts.comfy_template_migration import MigratedComfyWorkflowAsset
from ccp_studio.services.comfy_template_migration_service import ComfyTemplateMigrationService


@dataclass
class MigrationWorkflow:
    comfy_template_migration_service: ComfyTemplateMigrationService | None = None

    def stage0_comfy_template_to_worker_asset(
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
    ) -> MigratedComfyWorkflowAsset:
        if self.comfy_template_migration_service is None:
            raise RuntimeError("ComfyTemplateMigrationService is required for ComfyUI template migration.")
        return self.comfy_template_migration_service.migrate_template_to_worker_asset(
            legacy_source_path=legacy_source_path,
            template_json=template_json,
            required_inputs=required_inputs,
            output_contract=output_contract,
            compatibility_notes=compatibility_notes,
            known_defects=known_defects,
            eval_target=eval_target,
            eval_passed=eval_passed,
            reviewer_id=reviewer_id,
            actor_id=actor_id,
        )


__all__ = ["MigrationService", "MigrationWorkflow"]
