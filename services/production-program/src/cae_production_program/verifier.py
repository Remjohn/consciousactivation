"""
verifier.py
-----------
Verification logic for upstream semantic authority and rendering conformance (CAE-M11).
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict

from .domain import SemanticProgram
from .errors import (
    EvidenceQuoteMismatchError,
    StoryArcGeometryMutationError,
    UnapprovedAssetInsertionError,
)


class ProductionProgramVerifier:
    """Enforces that downstream realization engines faithfully realize the SemanticProgram without altering meaning."""

    @classmethod
    def verify_render_conformance(
        cls,
        program: SemanticProgram,
        render_spec: Dict[str, Any],
    ) -> bool:
        """Verifies that a rendered composition spec strictly conforms to upstream semantic authority."""
        # 1. Story arc verification
        rendered_arc = render_spec.get("story_arc")
        if rendered_arc != program.story_arc:
            raise StoryArcGeometryMutationError(
                f"Render mutated story arc geometry! Program expects '{program.story_arc}', got '{rendered_arc}'."
            )

        # 2. Spoken quotes verification
        rendered_scenes = render_spec.get("scenes", [])
        if len(rendered_scenes) != len(program.scenes):
            raise ValueError(
                f"Render scene count mismatch! Program has {len(program.scenes)} scenes, render has {len(rendered_scenes)}."
            )

        for prog_scene, rend_scene in zip(program.scenes, rendered_scenes):
            rend_text = rend_scene.get("spoken_text", "")
            computed_hash = hashlib.sha256(rend_text.encode("utf-8")).hexdigest()
            if computed_hash != prog_scene.text_sha256:
                raise EvidenceQuoteMismatchError(
                    f"Render quote mismatch in scene {prog_scene.scene_index}! Text was altered from upstream evidence."
                )

            # 3. Asset references verification
            prog_assets = {a["asset_id"] for a in prog_scene.asset_inserts if "asset_id" in a}
            rend_assets = {a["asset_id"] for a in rend_scene.get("asset_inserts", []) if "asset_id" in a}
            unapproved = rend_assets - prog_assets
            if unapproved:
                raise UnapprovedAssetInsertionError(
                    f"Render injected unapproved assets {unapproved} into scene {prog_scene.scene_index}!"
                )

        return True
