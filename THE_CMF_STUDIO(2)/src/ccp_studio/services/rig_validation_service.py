"""Rig validation service for TS-CMF-020."""

from __future__ import annotations

from dataclasses import dataclass

from ccp_studio.contracts.rig_manifest import RigManifest


REQUIRED_BODY_LAYERS = {
    "torso",
    "head",
    "neck",
    "left_upper_arm",
    "left_forearm",
    "left_hand",
    "right_upper_arm",
    "right_forearm",
    "right_hand",
    "left_leg",
    "right_leg",
    "feet",
    "shadow",
}

REQUIRED_PREVIEW_TESTS = {
    "blink",
    "nod",
    "open_hands_explanation",
    "pointing",
    "shrug",
    "expression_swap",
    "mouth_flap",
    "subtle_stop_motion_jitter",
}


@dataclass
class RigValidationService:
    def blocker_codes(self, manifest: RigManifest) -> list[str]:
        blockers: list[str] = []
        if not manifest.layers:
            blockers.append("RIG_LAYER_MANIFEST_REQUIRED")
        if any(not layer.pivot_points for layer in manifest.layers):
            blockers.append("RIG_PIVOT_POINTS_REQUIRED")
        if not REQUIRED_BODY_LAYERS.issubset(set(manifest.body_layer_refs)):
            blockers.append("RIG_BODY_LAYERS_REQUIRED")
        if len(manifest.mouth_shape_refs) < 4:
            blockers.append("RIG_MOUTH_SHAPES_REQUIRED")
        if len(manifest.eye_brow_variant_refs) < 4:
            blockers.append("RIG_EYE_BROW_VARIANTS_REQUIRED")
        if len(manifest.gesture_variant_refs) < 4:
            blockers.append("RIG_GESTURE_VARIANTS_REQUIRED")
        preview_names = {test.test_name for test in manifest.preview_tests}
        if not REQUIRED_PREVIEW_TESTS.issubset(preview_names):
            blockers.append("RIG_PREVIEW_REQUIRED")
        if any(not test.passed for test in manifest.preview_tests):
            blockers.append("RIG_PREVIEW_FAILED")
        if not manifest.version_hash or manifest.version_hash == "missing":
            blockers.append("RIG_VERSION_HASH_REQUIRED")
        return list(dict.fromkeys(blockers))
