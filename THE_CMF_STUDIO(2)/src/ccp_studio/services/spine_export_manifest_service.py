from __future__ import annotations

from ccp_studio.contracts.avatar_asset_production import SpineExportManifest


class SpineExportManifestService:
    def compile_export_manifest(self, *, avatar_id: str, source_stretchy_manifest_id: str, output_json_ref: str, license_confirmed: bool) -> SpineExportManifest:
        return SpineExportManifest(
            avatar_id=avatar_id,
            source_stretchy_manifest_id=source_stretchy_manifest_id,
            output_json_ref=output_json_ref,
            license_confirmed=license_confirmed,
            animation_clip_refs=["raise_finger", "open_palm_reveal", "point_to_card"],
        )
