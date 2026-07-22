from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.interview_contracts import (
    ContractRouteTarget,
    ExpressionState,
    FirstLineAnchorSet,
    RepairFollowups,
)
from ccp_studio.contracts.skills import (
    ConsciousInterviewBriefQuestion,
    ConsciousInterviewBriefSkillOutput,
    DSPyProgramSpec,
    JITSkillCompiler,
    SaturationContextBundle,
    SkillUseMode,
)
from ccp_studio.services.jit_skill_compiler_service import JITSkillCompilerError, JITSkillCompilerService


def _service(approved=True):
    service = JITSkillCompilerService()
    spec = DSPyProgramSpec(
        schema_version="cmf.dspy_program_spec.v1",
        dspy_program_spec_id=uuid4(),
        program_key="jit.expression_extraction",
        input_model="SaturationContextBundle",
        output_model="CompilerCandidateSet",
        version="2026.06.21",
        fixture_set_ids=[uuid4()],
        evaluation_target_ids=[uuid4()],
        eval_threshold=0.85,
    )
    service.register_program_spec(spec)
    compiler = JITSkillCompiler(
        schema_version="cmf.jit_skill_compiler.v1",
        skill_key="expression_extraction_jit",
        allowed_use_modes=[
            SkillUseMode.live_guest_induction,
            SkillUseMode.conscious_interview_brief,
            SkillUseMode.interview_engineering,
            SkillUseMode.transcript_extraction,
            SkillUseMode.routing_support,
        ],
        dspy_program_spec_id=spec.dspy_program_spec_id,
        registry_snapshot_id=uuid4(),
        output_schema="CompilerCandidateSet",
        compiler_fingerprint="jit-expression-extraction-v1",
        approved=approved,
    )
    service.register_compiler(compiler)
    return service, spec, compiler


def _transcript_context():
    return SaturationContextBundle(
        schema_version="cmf.saturation_context_bundle.v1",
        source_doc_refs=["source:interview:master"],
        transcript_segment_refs=["transcript:segment:12-18"],
        guest_dossier_id=uuid4(),
        audience_reality_brief_id=uuid4(),
        brand_context_version_id=uuid4(),
        primitive_candidate_ids=[uuid4()],
        prior_evaluation_receipt_ids=[uuid4()],
        failure_corpus_refs=["failure:generic-script", "failure:forced-route"],
    )


def _live_context():
    return SaturationContextBundle(
        schema_version="cmf.saturation_context_bundle.v1",
        guest_dossier_id=uuid4(),
        audience_reality_brief_id=uuid4(),
        brand_context_version_id=uuid4(),
        primitive_candidate_ids=[uuid4()],
        prior_evaluation_receipt_ids=[uuid4()],
        failure_corpus_refs=["failure:centroid-answer"],
    )


def _conscious_interview_brief_context():
    return SaturationContextBundle(
        schema_version="cmf.saturation_context_bundle.v1",
        source_doc_refs=["ccf:trigger-first-chain", "cral:signal-discovery"],
        guest_dossier_id=uuid4(),
        audience_reality_brief_id=uuid4(),
        context_premise_id=uuid4(),
        audience_deep_trigger_map_id=uuid4(),
        interviewer_resonance_context_id=uuid4(),
        matrix_brief_id=uuid4(),
        brand_context_version_id=uuid4(),
        cral_finding_refs=["cral:relevant", "cral:resonant"],
        audience_conversation_refs=["audience-comments:founder-recording-resistance"],
        primitive_candidate_ids=[uuid4()],
        invariant_field_refs=["invariant:activated-truth"],
        coalition_signature_refs=["coalition:recognition-exposure-edge"],
        edge_product_refs=["edge-product:question-that-causes-lived-scene"],
        ccf_orchestration_refs=["ccf:signal-provocation-reaction-coalition-output"],
        prior_evaluation_receipt_ids=[uuid4()],
        failure_corpus_refs=["failure:topic-first-question", "failure:persona-summary"],
    )


def _invoke(service, context=None, use_mode=SkillUseMode.transcript_extraction, **overrides):
    values = {
        "skill_key": "expression_extraction_jit",
        "use_mode": use_mode,
        "saturation_context": context or _transcript_context(),
        "candidate_texts": ["The guest rejects the inherited frame using a timestamped lived example."],
        "contrast_texts": ["A weaker candidate would summarize the topic without the source pressure."],
        "evidence_refs": ["transcript:segment:12-18", "primitive:frame-break"],
        "confidence": 0.91,
        "eval_score": 0.9,
        "reviewer_state": "not_required",
    }
    values.update(overrides)
    return service.invoke(**values)


def test_missing_saturation_context_rejects_compiler_output():
    service, _spec, _compiler = _service()
    incomplete = SaturationContextBundle(
        schema_version="cmf.saturation_context_bundle.v1",
        source_doc_refs=["source:interview"],
    )

    with pytest.raises(JITSkillCompilerError) as exc:
        _invoke(service, context=incomplete)

    assert exc.value.code == "SATURATION_CONTEXT_INCOMPLETE"


def test_compiler_results_include_contrast_anti_draft_evidence_confidence_and_receipt():
    service, spec, compiler = _service()
    context = _transcript_context()

    receipt = _invoke(service, context=context)
    candidate_set = next(iter(service.repository.candidate_sets.values()))
    calibration = next(iter(service.repository.calibration_reports.values()))
    layer = next(iter(service.repository.contrastive_layers.values()))

    assert receipt.dspy_program_spec_id == spec.dspy_program_spec_id
    assert receipt.dspy_program_version == spec.version
    assert receipt.registry_snapshot_id == compiler.registry_snapshot_id
    assert receipt.input_hashes[0] == context.stable_hash()
    assert receipt.output_schema == "CompilerCandidateSet"
    assert receipt.eval_score == 0.9
    assert receipt.evidence_refs == ["transcript:segment:12-18", "primitive:frame-break"]
    assert candidate_set.contrast_candidates
    assert candidate_set.candidates[0].confidence == 0.91
    assert calibration.passed is True
    assert layer.anti_centroid_checks


def test_output_without_saturation_citations_cannot_influence_routing_or_extraction():
    service, _spec, _compiler = _service()

    with pytest.raises(JITSkillCompilerError) as exc:
        _invoke(service, evidence_refs=[])

    assert exc.value.code == "SKILL_OUTPUT_UNGROUNDED"


def test_live_guest_induction_is_distinct_from_transcript_source_extraction():
    service, _spec, _compiler = _service()

    live_receipt = _invoke(
        service,
        context=_live_context(),
        use_mode=SkillUseMode.live_guest_induction,
        candidate_texts=["Ask the guest toward the lived contradiction without imposing the route."],
        contrast_texts=["Do not reuse a transcript extraction prompt during the live exchange."],
        evidence_refs=["guest-dossier:signal", "audience-reality:gap"],
    )
    transcript_receipt = _invoke(service)

    assert live_receipt.extraction_boundary == "live_guest_support"
    assert transcript_receipt.extraction_boundary == "transcript_source_extraction"


def test_conscious_interview_brief_requires_reverse_engineered_ccf_context():
    service, _spec, _compiler = _service()

    incomplete = SaturationContextBundle(
        schema_version="cmf.saturation_context_bundle.v1",
        guest_dossier_id=uuid4(),
        audience_reality_brief_id=uuid4(),
        prior_evaluation_receipt_ids=[uuid4()],
        failure_corpus_refs=["failure:generic-question"],
    )
    with pytest.raises(JITSkillCompilerError) as exc:
        _invoke(
            service,
            context=incomplete,
            use_mode=SkillUseMode.conscious_interview_brief,
            candidate_texts=["What made this contradiction impossible to ignore?"],
            contrast_texts=["Tell us about your journey."],
            evidence_refs=["context-premise:missing"],
        )
    assert exc.value.code == "SATURATION_CONTEXT_INCOMPLETE"
    assert "context_premise_id" in exc.value.message
    assert "interviewer_resonance_context_id" in exc.value.message
    assert "audience_conversation_refs" in exc.value.message
    assert "ccf_orchestration_refs" in exc.value.message

    receipt = _invoke(
        service,
        context=_conscious_interview_brief_context(),
        use_mode=SkillUseMode.conscious_interview_brief,
        candidate_texts=["Where did the audience's recurring complaint first become real in your own work?"],
        contrast_texts=["What topic do you want to talk about this month?"],
        evidence_refs=["context-premise:approved", "matrix:edge-product", "audience-comments:cluster"],
    )

    assert receipt.extraction_boundary == "conscious_interview_brief_compilation"


def test_conscious_interview_brief_output_uses_interview_asset_contract_shape():
    route = ContractRouteTarget(
        schema_version="cmf.contract_route_target.v1",
        core_archetype_ref="archetype.conceptual_contrast.v1",
        asset_derivative_refs=["derivative.identity_mirror.v1", "derivative.quote_to_question.v1"],
        cmf_render_mode_refs=["cmf.personal_brand_commentary.v1"],
        guest_asset_pack_potential=["video", "carousel", "poll_visual"],
    )
    question = ConsciousInterviewBriefQuestion(
        schema_version="cmf.conscious_interview_brief_question.v1",
        question_id=uuid4(),
        main_question="Before we talk about the framework, where did that audience wound first become real in your work?",
        source_pressure_refs=["cral:resonant", "audience-comments:cluster"],
        context_premise_ref=uuid4(),
        matrix_brief_ref=uuid4(),
        primitive_candidate_ids=[uuid4()],
        interviewer_resonance_context_ref=uuid4(),
        target_expression_states=[ExpressionState.cinematic, ExpressionState.vulnerability],
        route_target=route,
        edge_product_refs=["edge-product:recognition-exposure"],
        first_line_anchors=FirstLineAnchorSet(
            schema_version="cmf.first_line_anchor_set.v1",
            cinematic="The first time I saw this clearly, I was...",
            emotional="What nobody understood in that moment was...",
            reels_hook="People call it resistance, but what it really was...",
        ),
        depth_anchor="What did it cost before it became something you could teach?",
        expected_source_material=["specific scene", "cost", "identity tension"],
        landing_eval_targets=["emotional_recognition", "principle", "unresolved_tension"],
        repair_followups=RepairFollowups(
            schema_version="cmf.repair_followups.v1",
            too_historical="Not historically; what did it do to you in that room?",
            too_abstract="Can you bring us back to the body of the moment?",
            too_flat="What part of that answer still feels too easy?",
            not_clip_ready="Can we restart with the first-line anchor and stay inside the scene?",
        ),
        intended_guest_reaction="specific lived recognition before teaching",
        intended_extraction_outcome="source-backed Expression Moment with clean clip start",
        anti_centroid_check="Reject if the answer becomes a generic topic explanation.",
    )
    output = ConsciousInterviewBriefSkillOutput(
        schema_version="cmf.conscious_interview_brief_skill_output.v1",
        interview_brief_skill_output_id=uuid4(),
        question_contracts=[question],
        ccf_reverse_engineering_chain=[
            "guest_truth",
            "interviewer_resonance",
            "audience_reality",
            "matrix_edge",
            "target_expression_state",
            "first_line_anchor",
            "depth_anchor",
            "landing_eval",
        ],
    )

    assert output.question_contracts[0].first_line_anchors.complete is True
    assert output.question_contracts[0].clip_start_rule == "start_at_selected_first_line_anchor"
    assert output.question_contracts[0].route_target.asset_derivative_refs


def test_anti_draft_failure_rejects_generic_output():
    service, _spec, _compiler = _service()

    with pytest.raises(JITSkillCompilerError) as exc:
        _invoke(service, candidate_texts=["This generic content pillar script sounds polished."])

    assert exc.value.code == "ANTI_DRAFT_GATE_FAILED"


def test_compiler_cannot_mutate_canonical_state():
    service, _spec, _compiler = _service()

    with pytest.raises(JITSkillCompilerError) as exc:
        _invoke(service, attempts_state_mutation=True)

    assert exc.value.code == "SKILL_STATE_MUTATION_FORBIDDEN"


def test_unapproved_skill_cannot_run():
    service, _spec, _compiler = _service(approved=False)

    with pytest.raises(JITSkillCompilerError) as exc:
        _invoke(service)

    assert exc.value.code == "SKILL_NOT_APPROVED"


def test_hidden_prompt_stack_is_blocked():
    service, _spec, _compiler = _service()

    with pytest.raises(JITSkillCompilerError) as exc:
        _invoke(service, hidden_prompt_stack=True)

    assert exc.value.code == "HIDDEN_PROMPT_STACK_BLOCKED"
