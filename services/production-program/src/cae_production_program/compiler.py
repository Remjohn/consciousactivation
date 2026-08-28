"""
compiler.py
-----------
Compiler compiling approved candidate snapshots and verified asset catalogs into a SemanticProgram.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional, Tuple

from .domain import (
    CompositionHandoffReceipt,
    SceneRole,
    SemanticProgram,
    SemanticSceneSpec,
    SFLModulationProfile,
    VisualAudioSpecs,
)
from .errors import (
    EvidenceQuoteMismatchError,
    StoryArcGeometryMutationError,
    TimingDiscontinuityError,
    UnapprovedAssetInsertionError,
)


class ProductionProgramCompiler:
    """Compiles Operator-approved editorial units into a deterministic SemanticProgram."""

    @classmethod
    def compile_program(
        cls,
        *,
        candidate_id: str,
        workspace_id: str,
        title: str,
        semantic_intent: str,
        story_arc: str,
        scenes_data: List[Dict[str, Any]],
        approved_asset_ids: List[str],
        visual_audio_specs: Optional[VisualAudioSpecs] = None,
    ) -> Tuple[SemanticProgram, CompositionHandoffReceipt]:
        """Compiles scene data, verifies evidence hashes and asset IDs, and generates a handoff receipt."""
        compiled_scenes: List[SemanticSceneSpec] = []
        evidence_hashes: List[str] = []
        referenced_assets: List[str] = []
        current_time = 0.0

        for idx, s in enumerate(scenes_data, start=1):
            spoken_text = s["spoken_text"]
            text_sha256 = s["text_sha256"]

            # 1. Evidence quote checksum verification
            computed_hash = hashlib.sha256(spoken_text.encode("utf-8")).hexdigest()
            if computed_hash != text_sha256:
                raise EvidenceQuoteMismatchError(
                    f"Evidence text '{spoken_text}' does not match registered hash '{text_sha256}' in scene {idx}."
                )

            start_t = s.get("start_time", current_time)
            end_t = s["end_time"]
            duration = round(end_t - start_t, 2)
            if duration <= 0:
                raise TimingDiscontinuityError(f"Scene {idx} duration {duration}s is invalid.")

            # 2. Asset approval verification
            scene_assets = s.get("asset_inserts", [])
            for asset in scene_assets:
                aid = asset.get("asset_id")
                if aid not in approved_asset_ids:
                    raise UnapprovedAssetInsertionError(
                        f"Scene {idx} attempts to insert unapproved asset '{aid}' not found in approved catalog."
                    )
                if aid not in referenced_assets:
                    referenced_assets.append(aid)

            scene_spec = SemanticSceneSpec(
                scene_index=idx,
                scene_role=s["scene_role"],
                segment_id=s["segment_id"],
                spoken_text=spoken_text,
                text_sha256=text_sha256,
                start_time=start_t,
                end_time=end_t,
                duration=duration,
                asset_inserts=scene_assets,
                sfl_profile=s.get("sfl_profile", SFLModulationProfile()),
            )
            compiled_scenes.append(scene_spec)
            evidence_hashes.append(text_sha256)
            current_time = end_t

        total_duration = round(sum(sc.duration for sc in compiled_scenes), 2)

        program = SemanticProgram(
            candidate_id=candidate_id,
            workspace_id=workspace_id,
            title=title,
            semantic_intent=semantic_intent,
            story_arc=story_arc,
            scenes=compiled_scenes,
            total_duration=total_duration,
            visual_audio_specs=visual_audio_specs or VisualAudioSpecs(),
        )

        receipt = CompositionHandoffReceipt(
            program_id=program.program_id,
            candidate_id=candidate_id,
            compiler_version="1.0.0",
            evidence_sha256_list=evidence_hashes,
            asset_id_list=referenced_assets,
        )

        return program, receipt
