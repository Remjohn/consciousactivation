from __future__ import annotations

from ccp_studio.contracts.format02_composition_intelligence import Format02SceneProgram, Format02SceneRole
from ccp_studio.contracts.format_intelligence import Format02AvatarPaperCutExplainerProgram, FormatId
from ccp_studio.services.format02_composition_service import Format02CompositionService


class Format02FormatProgramToCompositionAdapterService:
    def __init__(self, composition_service: Format02CompositionService | None = None):
        self.composition_service = composition_service or Format02CompositionService()

    def compile_scene_program(
        self,
        program: Format02AvatarPaperCutExplainerProgram,
        *,
        scene_id: str | None = None,
        scene_role: Format02SceneRole = Format02SceneRole.TRUTH_DEFINE,
        headline_text: str | None = None,
        concept_statement: str | None = None,
    ) -> Format02SceneProgram:
        if program.format_id != FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER:
            raise ValueError("Format02 adapter requires a Format02AvatarPaperCutExplainerProgram")

        concept = concept_statement or self._derive_concept_statement(program)
        headline = headline_text or self._derive_headline(concept)
        avatar_ref = program.avatar_clip_requirements[0] if program.avatar_clip_requirements else "coach_avatar_v1"
        format_program_id = getattr(
            program,
            "format_program_id",
            getattr(program, "format_intelligence_program_id", None),
        )

        return self.composition_service.compile_scene_program(
            brand_id=program.brand_id,
            brand_context_version_id=program.brand_context_version_id,
            source_span_refs=program.source_span_refs,
            scene_id=scene_id or f"scene_{program.format_program_id}",
            scene_role=scene_role,
            concept_statement=concept,
            headline_text=headline,
            format_program_id=format_program_id,
            avatar_ref=avatar_ref,
            hero_object_asset_id=program.diagram_sequence_ref,
            hero_object_source_ref=program.source_span_refs[0],
            support_labels=[],
        )

    def _derive_concept_statement(self, program: Format02AvatarPaperCutExplainerProgram) -> str:
        if program.concept_node_refs:
            return str(program.concept_node_refs[0])
        return str(program.teachable_mechanism_ref)

    def _derive_headline(self, concept_statement: str) -> str:
        words = concept_statement.split()
        return " ".join(words[:7]) if len(words) > 7 else concept_statement
