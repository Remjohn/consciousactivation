"""JIT skill compiler service for TS-CMF-015."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.skills import (
    AntiDraftCalibrationReport,
    CompilerCandidateSet,
    ContrastivePromptLayer,
    DSPyProgramSpec,
    JITSkillCompiler,
    SaturationContextBundle,
    SkillInvocationReceipt,
    SkillUseMode,
    new_compiler_candidate,
)
from ccp_studio.repositories.skill_invocation_records import InMemorySkillInvocationRepository


class JITSkillCompilerError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class JITSkillCompilerService:
    repository: InMemorySkillInvocationRepository = field(default_factory=InMemorySkillInvocationRepository)

    def register_program_spec(self, spec: DSPyProgramSpec) -> DSPyProgramSpec:
        if not spec.evaluation_target_ids:
            raise JITSkillCompilerError("SKILL_EVAL_TARGET_REQUIRED", "DSPy program spec requires eval targets.")
        return self.repository.put_program_spec(spec)

    def register_compiler(self, compiler: JITSkillCompiler) -> JITSkillCompiler:
        if compiler.dspy_program_spec_id not in self.repository.dspy_program_specs:
            raise JITSkillCompilerError("SKILL_EVAL_TARGET_REQUIRED", "Registered DSPy program spec is required.")
        return self.repository.put_compiler(compiler)

    def invoke(
        self,
        *,
        skill_key: str,
        use_mode: SkillUseMode,
        saturation_context: SaturationContextBundle,
        candidate_texts: list[str],
        contrast_texts: list[str],
        evidence_refs: list[str],
        confidence: float,
        eval_score: float,
        reviewer_state: str | None = None,
        attempts_state_mutation: bool = False,
        hidden_prompt_stack: bool = False,
    ) -> SkillInvocationReceipt:
        if hidden_prompt_stack:
            raise JITSkillCompilerError("HIDDEN_PROMPT_STACK_BLOCKED", "Hidden prompt stacks are forbidden.")
        if attempts_state_mutation:
            raise JITSkillCompilerError("SKILL_STATE_MUTATION_FORBIDDEN", "Skill compilers cannot mutate canonical state.")
        compiler = self.repository.compilers.get(skill_key)
        if compiler is None or not compiler.approved:
            raise JITSkillCompilerError("SKILL_NOT_APPROVED", "Approved JIT skill compiler is required.")
        if use_mode not in compiler.allowed_use_modes:
            raise JITSkillCompilerError("SKILL_USE_MODE_NOT_ALLOWED", "Compiler is not approved for this use mode.")
        spec = self.repository.dspy_program_specs[compiler.dspy_program_spec_id]
        self.validate_saturation_context(use_mode=use_mode, bundle=saturation_context)
        if not evidence_refs:
            raise JITSkillCompilerError("SKILL_OUTPUT_UNGROUNDED", "Compiler output requires evidence refs.")
        if spec.eval_threshold is not None and eval_score < spec.eval_threshold:
            raise JITSkillCompilerError("ANTI_DRAFT_GATE_FAILED", "Eval score is below threshold.")
        candidate_set = CompilerCandidateSet(
            schema_version="cmf.compiler_candidate_set.v1",
            compiler_candidate_set_id=uuid4(),
            candidates=[
                new_compiler_candidate(text=text, evidence_refs=evidence_refs, confidence=confidence)
                for text in candidate_texts
            ],
            contrast_candidates=[
                new_compiler_candidate(text=text, evidence_refs=evidence_refs, confidence=max(confidence - 0.1, 0))
                for text in contrast_texts
            ],
        )
        calibration = self.run_anti_draft_calibration(
            candidate_texts=[candidate.text for candidate in candidate_set.candidates],
            evidence_refs=evidence_refs,
        )
        if not calibration.passed:
            self.repository.put_calibration_report(calibration)
            raise JITSkillCompilerError(calibration.failure_code or "ANTI_DRAFT_GATE_FAILED", "Anti-draft gate failed.")
        layer = ContrastivePromptLayer(
            schema_version="cmf.contrastive_prompt_layer.v1",
            contrastive_prompt_layer_id=uuid4(),
            positive_pressure=["source-specific expression", "evidence-backed induction"],
            negative_space=["generic script", "uncited route leap"],
            anti_centroid_checks=["avoid safest average phrasing"],
            evidence_refs=evidence_refs,
        )
        self.repository.put_candidate_set(candidate_set)
        self.repository.put_calibration_report(calibration)
        self.repository.put_contrastive_layer(layer)
        receipt = SkillInvocationReceipt(
            schema_version="cmf.skill_invocation_receipt.v1",
            skill_invocation_receipt_id=uuid4(),
            skill_key=skill_key,
            use_mode=use_mode,
            dspy_program_spec_id=spec.dspy_program_spec_id,
            dspy_program_version=spec.version,
            registry_snapshot_id=compiler.registry_snapshot_id,
            input_hashes=[saturation_context.stable_hash()],
            output_schema=compiler.output_schema,
            evidence_refs=evidence_refs,
            eval_score=eval_score,
            reviewer_state=reviewer_state,
            extraction_boundary=self._extraction_boundary(use_mode),
            decision_code="SKILL_INVOCATION_ACCEPTED",
            created_at=utc_now(),
        )
        return self.repository.put_invocation_receipt(receipt)

    def validate_saturation_context(self, *, use_mode: SkillUseMode, bundle: SaturationContextBundle) -> None:
        missing: list[str] = []
        if use_mode in {SkillUseMode.transcript_extraction, SkillUseMode.source_expression_contrast}:
            if not bundle.source_doc_refs:
                missing.append("source_doc_refs")
            if not bundle.transcript_segment_refs:
                missing.append("transcript_segment_refs")
        if use_mode in {
            SkillUseMode.live_guest_induction,
            SkillUseMode.interview_engineering,
            SkillUseMode.narrative_induction,
            SkillUseMode.conscious_interview_brief,
        }:
            if bundle.guest_dossier_id is None:
                missing.append("guest_dossier_id")
            if bundle.audience_reality_brief_id is None:
                missing.append("audience_reality_brief_id")
        if use_mode in {SkillUseMode.conscious_interview_brief, SkillUseMode.interview_engineering}:
            if not bundle.source_doc_refs:
                missing.append("source_doc_refs")
            if bundle.context_premise_id is None:
                missing.append("context_premise_id")
            if bundle.audience_deep_trigger_map_id is None:
                missing.append("audience_deep_trigger_map_id")
            if bundle.interviewer_resonance_context_id is None:
                missing.append("interviewer_resonance_context_id")
            if bundle.matrix_brief_id is None:
                missing.append("matrix_brief_id")
            if not bundle.cral_finding_refs:
                missing.append("cral_finding_refs")
            if not bundle.audience_conversation_refs:
                missing.append("audience_conversation_refs")
            if not bundle.ccf_orchestration_refs:
                missing.append("ccf_orchestration_refs")
        if use_mode in {
            SkillUseMode.routing_support,
            SkillUseMode.evaluation_support,
            SkillUseMode.source_expression_contrast,
            SkillUseMode.conscious_interview_brief,
            SkillUseMode.interview_engineering,
        } and not bundle.primitive_candidate_ids:
            missing.append("primitive_candidate_ids")
        if use_mode == SkillUseMode.scene_prompt_support_after_route:
            scene_missing: list[str] = []
            if bundle.expression_moment_id is None:
                scene_missing.append("expression_moment_id")
            if bundle.route_receipt_id is None:
                scene_missing.append("route_receipt_id")
            if bundle.complete_editing_session_id is None:
                scene_missing.append("complete_editing_session_id")
            if scene_missing:
                raise JITSkillCompilerError(
                    "SCENE_PROMPT_SUPPORT_PRE_ROUTE_BLOCKED",
                    f"Scene prompt support requires approved post-route context: {', '.join(scene_missing)}.",
                )
        if not bundle.failure_corpus_refs:
            missing.append("failure_corpus_refs")
        if not bundle.prior_evaluation_receipt_ids:
            missing.append("prior_evaluation_receipt_ids")
        if missing:
            raise JITSkillCompilerError(
                "SATURATION_CONTEXT_INCOMPLETE",
                f"Saturation context is missing: {', '.join(missing)}.",
            )

    @staticmethod
    def run_anti_draft_calibration(*, candidate_texts: list[str], evidence_refs: list[str]) -> AntiDraftCalibrationReport:
        joined = " ".join(candidate_texts).lower()
        genericity_score = 0.9 if any(term in joined for term in ["generic", "script", "content pillar"]) else 0.1
        citation_coverage = 1.0 if evidence_refs else 0.0
        passed = genericity_score < 0.5 and citation_coverage >= 1.0
        return AntiDraftCalibrationReport(
            schema_version="cmf.anti_draft_calibration_report.v1",
            anti_draft_calibration_report_id=uuid4(),
            genericity_score=genericity_score,
            citation_coverage=citation_coverage,
            passed=passed,
            failure_code=None if passed else "ANTI_DRAFT_GATE_FAILED",
            evidence_refs=evidence_refs,
        )

    @staticmethod
    def _extraction_boundary(use_mode: SkillUseMode) -> str:
        if use_mode == SkillUseMode.live_guest_induction:
            return "live_guest_support"
        if use_mode == SkillUseMode.conscious_interview_brief:
            return "conscious_interview_brief_compilation"
        if use_mode == SkillUseMode.interview_engineering:
            return "interview_brief_engineering"
        if use_mode == SkillUseMode.narrative_induction:
            return "guest_narrative_induction"
        if use_mode == SkillUseMode.transcript_extraction:
            return "transcript_source_extraction"
        if use_mode == SkillUseMode.source_expression_contrast:
            return "source_expression_contrast"
        if use_mode == SkillUseMode.scene_prompt_support_after_route:
            return "post_route_scene_prompt_support"
        return use_mode.value
