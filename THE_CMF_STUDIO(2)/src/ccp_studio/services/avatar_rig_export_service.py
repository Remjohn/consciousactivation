from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import AvatarRigExportManifest, RuntimeExportTarget


class AvatarRigExportService:
    def compile_rig_export_manifest(
        self,
        *,
        avatar_id: str,
        stretchy_studio_import_manifest_id: str,
        spine_export_manifest_id: str | None = None,
        dragonbones_export_manifest_id: str | None = None,
        remotion_layer_payload_id: str | None = None,
    ) -> AvatarRigExportManifest:
        targets = [RuntimeExportTarget.STRETCHY_STUDIO, RuntimeExportTarget.REMOTION]
        if spine_export_manifest_id:
            targets.append(RuntimeExportTarget.SPINE)
        if dragonbones_export_manifest_id:
            targets.append(RuntimeExportTarget.DRAGONBONES)
        return AvatarRigExportManifest(
            avatar_id=avatar_id,
            stretchy_studio_import_manifest_id=stretchy_studio_import_manifest_id,
            spine_export_manifest_id=spine_export_manifest_id,
            dragonbones_export_manifest_id=dragonbones_export_manifest_id,
            remotion_layer_payload_id=remotion_layer_payload_id,
            export_targets=targets,
        )
