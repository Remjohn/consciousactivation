from __future__ import annotations
from ccp_studio.contracts.studio_pipeline_recipe_harness import *

class PipelineRecipeRegistryService:
    def _gate(self, gate_id, gate_type, sample_gate=False):
        return PipelineApprovalGate(gate_id=gate_id, gate_type=gate_type, status=PipelineApprovalStatus.PENDING, required_sample_types=['scene_sample','face_plate_sample','template_preview_sample'] if sample_gate else [])
    def _step(self, step_id, name, kind, deps=None, gate=None, roles=None, stage=None, services=None):
        return PipelineRecipeStep(step_id=step_id, display_name=name, step_kind=kind, depends_on=deps or [], approval_gate_id=gate, produces_artifact_roles=roles or [], orchestration_stage_ref=stage or step_id, existing_service_refs=services or [])
    def format02_golden_path(self):
        gates=[self._gate('provider_sample_first', PipelineApprovalGateType.SAMPLE_FIRST, True), self._gate('operator_final_approval', PipelineApprovalGateType.OPERATOR_APPROVAL)]
        S=PipelineStepKind; A=PipelineArtifactRole
        steps=[
            self._step('source_intake','Source Intake',S.SOURCE_INTAKE,roles=[A.SOURCE_REF]),
            self._step('narrative_story_doctor','Narrative Story Doctor',S.EXTRACTION,['source_intake'],services=['narrative_story_doctor_service']),
            self._step('format_intelligence','Format Intelligence',S.FORMAT_COMPILE,['narrative_story_doctor'],services=['format_intelligence_service']),
            self._step('format02_composition','Format 02 Composition',S.COMPOSITION,['format_intelligence'],roles=[A.INTERMEDIATE]),
            self._step('avatar_assets','Avatar Asset Production',S.AVATAR_ASSET,['format02_composition'],roles=[A.AVATAR_ASSET]),
            self._step('provider_samples','Provider Samples',S.PROVIDER_SAMPLE,['avatar_assets'],'provider_sample_first',[A.PROVIDER_OUTPUT]),
            self._step('timeline_render_contract','Timeline + Render Contract',S.TIMELINE,['provider_samples']),
            self._step('render_qa','Render QA',S.QA,['timeline_render_contract'],roles=[A.QA_RECEIPT]),
            self._step('approval_export','Approval + Export',S.EXPORT,['render_qa'],'operator_final_approval',[A.EXPORT]),]
        return PipelineRecipe(recipe_id=PipelineRecipeId.FORMAT02_GOLDEN_PATH, display_name='Format 02 Golden Path', description='Reusable Format 02 golden path recipe.', steps=steps, approval_gates=gates, required_input_artifact_roles=[A.INPUT,A.SOURCE_REF])
    def avatar_library_generation(self):
        S=PipelineStepKind; A=PipelineArtifactRole; gates=[self._gate('avatar_sample_first', PipelineApprovalGateType.SAMPLE_FIRST, True)]
        steps=[self._step('avatar_character_spec','Avatar Character Spec',S.AVATAR_ASSET,roles=[A.AVATAR_ASSET]), self._step('face_plate_sample','Face Plate Sample',S.PROVIDER_SAMPLE,['avatar_character_spec'],roles=[A.PROVIDER_OUTPUT]), self._step('sample_approval','Sample Approval',S.APPROVAL,['face_plate_sample'],'avatar_sample_first'), self._step('avatar_batch_generation','Avatar Batch Generation',S.PROVIDER_BATCH,['sample_approval'],'avatar_sample_first',[A.AVATAR_ASSET]), self._step('rig_export_qa','Rig Export QA',S.QA,['avatar_batch_generation'],roles=[A.QA_RECEIPT])]
        return PipelineRecipe(recipe_id=PipelineRecipeId.AVATAR_LIBRARY_GENERATION, display_name='Avatar Library Generation', description='Generate approved avatar library assets.', steps=steps, approval_gates=gates, required_input_artifact_roles=[A.SOURCE_REF])
    def supervisual_from_expression_moment(self):
        S=PipelineStepKind; A=PipelineArtifactRole
        steps=[self._step('expression_moment_input','Expression Moment Input',S.SOURCE_INTAKE,roles=[A.INPUT]), self._step('supervisual_program','SuperVisual Program',S.COMPOSITION,['expression_moment_input'],roles=[A.INTERMEDIATE]), self._step('supervisual_provider_sample','SuperVisual Provider Sample',S.PROVIDER_SAMPLE,['supervisual_program'],roles=[A.PROVIDER_OUTPUT]), self._step('review_receipt','Review Receipt',S.REVIEW,['supervisual_provider_sample'],roles=[A.APPROVAL_RECEIPT])]
        return PipelineRecipe(recipe_id=PipelineRecipeId.SUPERVISUAL_FROM_EXPRESSION_MOMENT, display_name='SuperVisual from Expression Moment', description='Create a SuperVisual from an expression moment.', steps=steps)
    def carousel_from_expression_moment(self):
        S=PipelineStepKind; A=PipelineArtifactRole
        steps=[self._step('expression_moment_input','Expression Moment Input',S.SOURCE_INTAKE,roles=[A.INPUT]), self._step('carousel_program','Carousel Program',S.FORMAT_COMPILE,['expression_moment_input'],roles=[A.INTERMEDIATE]), self._step('template_preview','Template Preview',S.COMPOSITION,['carousel_program'],roles=[A.TEMPLATE_PREVIEW]), self._step('approval_export','Approval + Export',S.EXPORT,['template_preview'],roles=[A.EXPORT])]
        return PipelineRecipe(recipe_id=PipelineRecipeId.CAROUSEL_FROM_EXPRESSION_MOMENT, display_name='Carousel from Expression Moment', description='Create a carousel from an expression moment.', steps=steps)
    def format01_story_video(self):
        S=PipelineStepKind; A=PipelineArtifactRole
        steps=[self._step('source_intake','A-roll Source Intake',S.SOURCE_INTAKE,roles=[A.SOURCE_REF]), self._step('story_extraction','Story Extraction',S.EXTRACTION,['source_intake']), self._step('story_video_plan','Story Video Plan',S.FORMAT_COMPILE,['story_extraction']), self._step('timeline','Timeline',S.TIMELINE,['story_video_plan']), self._step('proxy_render_qa','Proxy Render QA',S.QA,['timeline'],roles=[A.QA_RECEIPT]), self._step('approval_export','Approval + Export',S.EXPORT,['proxy_render_qa'],roles=[A.EXPORT])]
        return PipelineRecipe(recipe_id=PipelineRecipeId.FORMAT01_STORY_VIDEO, display_name='Format 01 Story Video', description='A-roll-led story video recipe. No filler B-roll.', steps=steps)
    def all_recipes(self): return [self.format02_golden_path(), self.avatar_library_generation(), self.supervisual_from_expression_moment(), self.carousel_from_expression_moment(), self.format01_story_video()]
