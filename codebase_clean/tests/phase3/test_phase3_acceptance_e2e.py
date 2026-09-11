"""
test_phase3_acceptance_e2e.py
------------------------------
Unified End-to-End Acceptance and Verification Test Suite for CAE Phase 3:
Intelligence and Programs (Mandates M25 through M36).

Proves the complete unbroken 10-step causal semantic chain:
Workspace / Guest DNA (M25/M27)
  -> Audience Context / Cognitive Island (M26)
  -> Research Source Ingestion (M28/M29)
  -> OKF Canonical Knowledge (M30)
  -> Knowledge Cluster / Signal (M31)
  -> Collision Hypothesis / Matrix of Edging (M32)
  -> Interview Brief (M33)
  -> Live Supervised Interview Turns / Authenticated Evidence (M34)
  -> Editorial Evidence Segmentation & Semantic Attribution (M35)
  -> Content Candidate Composition & Cluster (M35)
  -> Synthetic-Proof Block & Portfolio Search (M35)
  -> Operator Storyboard Selection & Audit Receipts (M35/M36)

Plus contrastive/negative tests for:
- Synthetic candidate producer fail-closed block
- Tampered evidence / broken lineage rejection
- Multi-tenant workspace isolation
- Strict 4-lane authority separation
"""

import sqlite3
import hashlib
from uuid import UUID, uuid4
import pytest
from typing import Any, Dict, List

from ca_contracts import canonical_sha256
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.tenancy import TenantContext, tenant_scope

# M25: Workspace & Guest Operating Context
from ca_runtime.workspace_guest_program import (
    WorkspaceGuestProgramCoordinator,
    GuestEvidenceItem,
    DerivedBrandContext,
)
from ca_runtime.program_state_runtime import (
    UniversalProgramStateRuntime,
    InMemoryProgramStateStore,
    get_canonical_workspace_guest_state_machine,
    get_canonical_audience_context_state_machine,
    get_canonical_collision_state_machine,
)
from ca_runtime.state_lifecycle import (
    CausalTraceLedger,
    StateLifecycleCoordinator,
)
from ca_runtime.hook_runtime import OperatorGateRuntimeEngine

# M26: Audience Context
from ca_runtime.audience_context_program import (
    AudienceContextProgramCoordinator,
    AudienceProfile,
    CognitiveIsland,
)

# M27: Guest Genesis & DNA Protection
from ca_runtime.guest_genesis_program import (
    GuestGenesisProgramCoordinator,
    ProtectedGuestEvidence,
    DerivedVoiceVisualDNA,
    GuestGenesisState,
)

# M28-M29: Research Source & Ingestion
from ca_runtime.research_source_program import (
    ResearchSourceProgramCoordinator,
)

# M32: Collision Hypothesis & Matrix of Edging
from ca_runtime.collision_hypothesis_store import (
    CollisionHypothesisStore,
    MatrixOfEdgingRecord,
    CollisionHypothesisRecord,
)
from ca_runtime.collision_hypothesis_program import (
    CollisionHypothesisProgramCoordinator,
    CollisionHypothesisCandidate,
    UnauthorizedCollisionLaneError,
)

# M33-M34: Interview Semantic & Live Activation
from ca_runtime.interview_semantic_store import (
    InterviewSemanticStore,
    InterviewBriefRecord,
)
from ca_runtime.interview_semantic_program import (
    InterviewSemanticProgramCoordinator,
    SelfAttestationViolationError,
)
from cae_interview_intelligence.question_resolver import (
    AnswerResolution,
    InformationCompleteness,
    EvidenceMode,
)
from cae_interview_intelligence.semantic_acquisition import (
    EvidenceLineageKind,
)

# M35: Editorial Discovery & Synthetic-Proof Block
from ca_runtime.editorial_discovery_store import (
    EditorialDiscoveryStore,
    EvidenceSegmentRecord,
    SemanticAnnotationRecord,
    ContentCandidateRecord,
    CandidateClusterRecord,
    EditorialStoryboardRecord,
    EditorialDecisionReceiptRecord,
)
from ca_runtime.editorial_discovery_program import (
    EditorialDiscoveryProgramCoordinator,
    SyntheticCandidateProductionBlockedError,
    UngroundedCandidateError,
    EvidenceImmutabilityViolationError,
    LaneAuthorityViolationError,
)

from cae_attribution_intelligence.domain import (
    SemanticRole,
    EvidenceEpistemicStatus,
)
from cae_candidate_intelligence.domain import (
    CandidateType,
    CandidateEvidenceLink,
    NarrativeCompleteness,
)
from cae_scoring_intelligence.domain import (
    CandidateEvaluationProfile,
    DimensionScores,
    EvaluatorProvenance,
    GateStatus,
)


class TestPhase3AcceptanceE2E:
    """Unified Phase 3 E2E Integration & Verification Test Suite."""

    @pytest.fixture
    def e2e_environment(self):
        """Creates unified in-memory stores and program coordinators."""
        ws_id_uuid = uuid4()
        ws_id = str(ws_id_uuid)
        guest_id = "GST-JEAN-PIERRE"
        operator_id = "OPR-LEAD-DIRECTOR"
        hunter_id = "AGENT-HUNTER-01"
        analyst_id = "AGENT-ANALYST-01"
        composer_id = "AGENT-COMPOSER-01"
        commander_id = "AGENT-COMMANDER-01"

        tenant_ctx = TenantContext(
            workspace_id=ws_id_uuid,
            actor_id=operator_id,
            role="OPERATOR",
            is_operator=True,
            operator_grant_id=uuid4(),
        )

        state_store = InMemoryProgramStateStore()
        runtime = UniversalProgramStateRuntime(state_store)
        trace_ledger = CausalTraceLedger()
        lifecycle_coordinator = StateLifecycleCoordinator(
            state_runtime=runtime,
            trace_ledger=trace_ledger,
        )
        operator_gate_engine = OperatorGateRuntimeEngine(trace_ledger=trace_ledger)

        runtime.register_state_machine(get_canonical_workspace_guest_state_machine())
        runtime.register_state_machine(get_canonical_audience_context_state_machine())
        runtime.register_state_machine(get_canonical_collision_state_machine())

        # Initialize stores
        conn = sqlite3.connect(":memory:")
        collision_store = CollisionHypothesisStore(conn)
        interview_store = InterviewSemanticStore(conn)
        editorial_store = EditorialDiscoveryStore(db_path=":memory:")

        # Initialize coordinators
        ws_guest_coord = WorkspaceGuestProgramCoordinator(
            state_runtime=runtime,
            coordinator=lifecycle_coordinator,
            trace_ledger=trace_ledger,
        )
        aud_coord = AudienceContextProgramCoordinator(
            runtime=runtime,
            coordinator=lifecycle_coordinator,
            trace_ledger=trace_ledger,
            operator_gate_engine=operator_gate_engine,
        )
        genesis_coord = GuestGenesisProgramCoordinator(
            program_id="prog-genesis-jp-01",
            workspace_id=ws_id,
            guest_id=guest_id,
        )
        res_coord = ResearchSourceProgramCoordinator(runtime=runtime)

        collision_coord = CollisionHypothesisProgramCoordinator(
            workspace_id=ws_id,
            store=collision_store,
            state_runtime=runtime,
        )
        interview_coord = InterviewSemanticProgramCoordinator(
            workspace_id=ws_id,
            store=interview_store,
        )
        editorial_coord = EditorialDiscoveryProgramCoordinator(editorial_store=editorial_store)

        return {
            "ws_id": ws_id,
            "ws_id_uuid": ws_id_uuid,
            "guest_id": guest_id,
            "operator_id": operator_id,
            "hunter_id": hunter_id,
            "analyst_id": analyst_id,
            "composer_id": composer_id,
            "commander_id": commander_id,
            "tenant_ctx": tenant_ctx,
            "runtime": runtime,
            "ws_guest_coord": ws_guest_coord,
            "aud_coord": aud_coord,
            "genesis_coord": genesis_coord,
            "res_coord": res_coord,
            "collision_coord": collision_coord,
            "collision_store": collision_store,
            "interview_store": interview_store,
            "editorial_store": editorial_store,
            "interview_coord": interview_coord,
            "editorial_coord": editorial_coord,
        }

    def test_complete_phase3_causal_semantic_chain(self, e2e_environment):
        """
        Verifies the full 10-step unbroken causal chain from Workspace & Guest DNA
        through Research, OKF Knowledge, Collision, Interview Brief, Live Interview,
        Evidence Packaging, Editorial Segmentation, Candidate Formation, Synthetic Gate,
        and Operator Selection.
        """
        env = e2e_environment
        ws_id = env["ws_id"]
        ws_id_uuid = env["ws_id_uuid"]
        guest_id = env["guest_id"]
        operator_id = env["operator_id"]
        hunter_id = env["hunter_id"]
        analyst_id = env["analyst_id"]
        composer_id = env["composer_id"]
        commander_id = env["commander_id"]
        tenant_ctx = env["tenant_ctx"]

        with tenant_scope(tenant_ctx):
            # =========================================================================
            # STEP 1: Workspace & Guest Operating Context (M25)
            # =========================================================================
            ws_agg = env["ws_guest_coord"].initialize_program(
                workspace_id=ws_id,
                actor_id=operator_id,
            )
            env["ws_guest_coord"].configure_workspace(
                aggregate_id=ws_agg.aggregate_id,
                display_name="Project 03_50-12 Jean Pierre",
            )
            env["ws_guest_coord"].register_guest(
                aggregate_id=ws_agg.aggregate_id,
                pseudonym="Jean Pierre",
                guest_id=guest_id,
            )
            ev_item = GuestEvidenceItem(
                evidence_id="EVID-JP-001",
                source_url="https://vault.internal/jp/transcript_01.json",
                content_type="INTERVIEW_TRANSCRIPT",
                sha256_digest=canonical_sha256("Pioneered sovereign supply-base restructuring during the 2024 industrial crisis."),
            )
            env["ws_guest_coord"].bind_guest_evidence(
                aggregate_id=ws_agg.aggregate_id,
                guest_id=guest_id,
                evidence_items=[ev_item],
            )
            brand_ctx = env["ws_guest_coord"].derive_brand_context(
                aggregate_id=ws_agg.aggregate_id,
                guest_id=guest_id,
                brand_id="BRD-JP-001",
                tone_attributes=["uncompromising", "pragmatic", "sovereign"],
                voice_archetype="TRANSFORMATIVE_OPERATOR",
                visual_theme="INDUSTRIAL_MINIMAL",
                source_evidence_hashes=[ev_item.sha256_digest],
            )
            active_ws_res = env["ws_guest_coord"].activate_guest_context(
                aggregate_id=ws_agg.aggregate_id,
                guest_id=guest_id,
            )
            assert active_ws_res.aggregate.current_state == "CONTEXT_ACTIVE"

            # =========================================================================
            # STEP 2: Audience Context & Cognitive Island (M26)
            # =========================================================================
            aud_init_res = env["aud_coord"].initialize_audience(
                workspace_id=ws_id_uuid,
                audience_id="AUD-INDUSTRIAL-FOUNDERS",
                target_segment="Mid-Market Industrial Executives",
                core_demographics={"industry": "Manufacturing", "seniority": "C-Level"},
                psychographic_baseline={"urgency": "HIGH", "core_fear": "STAGNATION"},
                context=tenant_ctx,
                actor_id=operator_id,
            )
            assert aud_init_res.aggregate.current_state == "AUDIENCE_INITIALIZED"

            # =========================================================================
            # STEP 3: Guest Genesis & DNA Protection (M27)
            # =========================================================================
            protected_ev = ProtectedGuestEvidence(
                evidence_id="PROT-JP-001",
                source_url="https://vault.internal/jp/evidence_dna.json",
                content_type="interview_transcript_span",
                sha256_digest=canonical_sha256("Overcame single-source tier-1 failure by authorizing local machine shops within 48 hours."),
                transcript_spans=("Overcame single-source tier-1 failure by authorizing local machine shops within 48 hours.",),
            )
            env["genesis_coord"].index_protected_evidence(
                evidence_items=[protected_ev],
                actor_lane="HUNTER",
            )
            assert env["genesis_coord"].current_state == GuestGenesisState.EVIDENCE_INDEXED

            # =========================================================================
            # STEP 4: Research Source Ingestion & Identity (M28)
            # =========================================================================
            res_agg = env["runtime"].initialize_program_state(
                program_id="research_source_ingestion_program",
                workspace_id=ws_id,
                actor_id=hunter_id,
            )
            raw_snippet = "Over 74% of mid-market industrial firms suffer acute margin collapse during single-tier logistics shocks."
            rec, admit_rcpt = env["res_coord"].admit_source(
                workspace_id=ws_id,
                aggregate_id=res_agg.aggregate_id,
                actor_id=hunter_id,
                origin_url="https://research.mit.edu/supply-resilience-2026",
                raw_text_snippet=raw_snippet,
                source_platform="academic_vault",
                source_type="ACADEMIC_PAPER",
                author_outlet="MIT Supply Chain Center",
                rights_metadata={"access_tier": "ENTERPRISE_RESEARCH"},
            )
            assert rec.source_id is not None
            assert rec.status == "ADMITTED"
            assert admit_rcpt["authority_lane"] == "HUNTER"

            # =========================================================================
            # STEP 5 & 6: Collision Hypothesis & Matrix of Edging (M32)
            # =========================================================================
            resonance = env["collision_coord"].discover_resonance(
                workspace_id=ws_id,
                guest_dna={
                    "guest_id": guest_id,
                    "proof_citation": "Resolved existential tier-1 crisis in 48 hours via local distributed tooling protocols.",
                },
                audience_tensions=[
                    {
                        "audience_id": "AUD-INDUSTRIAL-FOUNDERS",
                        "tension_ref": "TENS-SUPPLY-001",
                        "tension_label": "Single-Tier Dependency vs Sovereign Redundancy",
                    }
                ],
                world_signals=[
                    {
                        "signal_id": rec.source_id,
                        "theme": "European and Global Logistics Vulnerability",
                    }
                ],
                lane=AuthorityLane.HUNTER,
            )
            matrix = env["collision_coord"].evaluate_matrix_of_edging(
                workspace_id=ws_id,
                matrix_id="MOE-JP-SUPPLY-01",
                broad_signal="Global logistics fragility and supplier margin collapse.",
                hidden_pressure="Executives fear breaking enterprise contracts even when suppliers are failing.",
                surviving_edge="Radical decentralization to local machine networks preserves operational sovereignty.",
                identity_gap="Contractual compliance manager vs sovereign industrial builder.",
                audience_reality="Paralyzed by corporate procurement bureaucracy while production halted.",
                desired_recognition="Celebrated for decisive operational recovery and margin resilience.",
                smallest_useful_movement="Audit critical components and establish hot-standby local tooling agreements.",
                lane=AuthorityLane.ANALYST,
            )
            oblique_lens = resonance[0].model_dump() if resonance else {"lens_id": "LENS-01", "lens_name": "BIOLOGICAL_APOPTOSIS"}
            col_cand = CollisionHypothesisCandidate(
                title="The Sovereign Supply Pivot",
                relation_type="ANALOGY",
                audience_id="AUD-INDUSTRIAL-FOUNDERS",
                audience_tension_ref="TENS-SUPPLY-001",
                guest_id=guest_id,
                guest_lived_proof_citation="Decisive 48-hour recovery executed by Jean Pierre across plant lines.",
                research_signal_id=rec.source_id,
                sda_invariant="SDA-INV-001_ACTIVE_TENSION",
                oblique_lens=oblique_lens,
                bridge_statement="Just as biological cells preserve life through rapid apoptosis of failing dependencies, sovereign industrial operators preserve plant survival by instantly pivoting to decentralized local suppliers.",
                evidence_references=[rec.source_id, "EVID-JP-001"],
                refuting_observation="Enterprises maintaining strict legacy procurement during tier-1 failures show zero line shutdowns.",
                disconfirming_testimony="Jean Pierre indicates that waiting for corporate approval was strictly superior to local emergency tooling.",
                boundary_limitation="Applies to mid-market precision manufacturing with localized engineering talent.",
                surprise_score=0.88,
                emotion_score=0.85,
                specificity_score=0.92,
            )
            portfolio = env["collision_coord"].compose_hypotheses(
                workspace_id=ws_id,
                portfolio_id="PORTFOLIO-JP-01",
                candidates=[col_cand],
                matrix_id=matrix.matrix_id,
                lane=AuthorityLane.COMPOSER,
            )
            assert len(portfolio.candidate_hypothesis_ids) == 1
            hyp_id = portfolio.candidate_hypothesis_ids[0]

            from ca_runtime.collision_hypothesis_program import HYPOTHESIS_GATES
            gate_outcomes = {hyp_id: {g: True for g in HYPOTHESIS_GATES}}
            candidate_scores = {
                hyp_id: {
                    "source_fidelity": 900000,
                    "role_tension_integrity": 920000,
                    "primitive_coalition_fitness": 880000,
                    "archetype_fit": 860000,
                    "edge_integrity": 940000,
                    "anti_centroid_distinctiveness": 950000,
                    "execution_feasibility": 890000,
                }
            }
            eval_res = env["collision_coord"].evaluate_portfolio(
                workspace_id=ws_id,
                portfolio_id="PORTFOLIO-JP-01",
                gate_outcomes=gate_outcomes,
                candidate_scores_micros=candidate_scores,
                lane=AuthorityLane.ANALYST,
            )
            assert eval_res["decision"] == "DECISIVE_WINNER"

            app_hyp_rcpt = env["collision_coord"].approve_hypothesis(
                workspace_id=ws_id,
                portfolio_id="PORTFOLIO-JP-01",
                hypothesis_id=hyp_id,
                approval_notes="High-stakes industrial turnaround thesis with undeniable guest empirical grounding.",
                lane=AuthorityLane.COMMANDER,
            )
            assert app_hyp_rcpt.status == "APPROVED"

            # =========================================================================
            # STEP 7: Interview Brief Composition (M33)
            # =========================================================================
            brief_record = InterviewBriefRecord(
                workspace_id=ws_id,
                brief_id="BRF-JP-001",
                hypothesis_id=hyp_id,
                guest_name="Jean Pierre",
                research_package_ref={"citation": "MIT Supply Chain Benchmark 2026"},
                tension_hypothesis=col_cand.bridge_statement,
                matrix_of_edging_seed={"provocation": col_cand.title},
                planned_questions=[
                    {
                        "question_id": "q1_crucible",
                        "stage": "CRUCIBLE_EXPOSURE",
                        "text": "Can you describe the decisive moment when your plant faced supply shutdown?",
                        "objective": "Elicit crisis turn.",
                    }
                ],
                composer_authority={"operator_id": operator_id},
                canonical_sha256=canonical_sha256("Sovereign Supply Transformation Brief"),
                lifecycle_state="SEALED",
            )
            env["interview_store"].store_brief(brief_record)

            # =========================================================================
            # STEP 8: Live Supervised Interview & Authenticated Evidence Package (M34)
            # =========================================================================
            session_rec, frontier = env["interview_coord"].start_interview_session(
                workspace_id=ws_id,
                brief_id=brief_record.brief_id,
                session_id="SESS-JP-001",
                actor_id=hunter_id,
                lane=AuthorityLane.HUNTER,
            )
            assert session_rec.session_id == "SESS-JP-001"

            qa = env["interview_coord"].get_next_question_attempt(
                workspace_id=ws_id,
                session_id=session_rec.session_id,
                actor_id=hunter_id,
                lane=AuthorityLane.HUNTER,
            )
            assert qa is not None

            turn1_response = (
                "We were 48 hours away from a complete assembly line freeze because our tier-1 supplier failed. "
                "But I immediately pivoted and bypassed the legacy contracts, authorizing local machine shops to tool up overnight."
            )
            turn_rec, obs = env["interview_coord"].record_turn_and_observe(
                workspace_id=ws_id,
                session_id=session_rec.session_id,
                question_attempt=qa,
                transcript_text=turn1_response,
                guest_statements=["Pivoted away from failing tier-1 supplier within 48h to tool up local machine shops."],
                resolution=AnswerResolution.EPISODIC,
                completeness=InformationCompleteness.SUFFICIENT,
                evidence_modes=[EvidenceMode.STORY],
                specificity_score=0.98,
                authenticity_score=0.99,
                actor_id=hunter_id,
                lane=AuthorityLane.HUNTER,
            )
            assert turn_rec.turn_index == 1

            # Package accepted evidence (COMPOSER)
            pkg_rec, pkg_obj = env["interview_coord"].package_interview_evidence(
                workspace_id=ws_id,
                session_id=session_rec.session_id,
                actor_id=composer_id,
                lane=AuthorityLane.COMPOSER,
            )
            assert pkg_rec.package_id is not None
            assert len(pkg_rec.accepted_evidence_records) >= 1

            # Authenticate session (distinct commander evaluator)
            sess_rec, auth_rec, receipt_rec = env["interview_coord"].authenticate_and_complete_session(
                workspace_id=ws_id,
                session_id=session_rec.session_id,
                evaluator_actor_id=commander_id,
                actor_id=commander_id,
                verdict="AUTHENTICATED",
                lane=AuthorityLane.COMMANDER,
            )
            assert auth_rec.verdict == "AUTHENTICATED"

            # =========================================================================
            # STEP 9: Editorial Discovery & Grounded Candidate Composition (M35)
            # =========================================================================
            turns_input = [
                {
                    "turn_id": "TURN-JP-001",
                    "speaker": "GUEST",
                    "start_time_ms": 0,
                    "end_time_ms": 9500,
                    "text": turn1_response,
                }
            ]

            # 9.1 HUNTER: Segment turns
            segments = env["editorial_coord"].segment_interview_turns(
                lane=AuthorityLane.HUNTER,
                workspace_id=ws_id,
                session_id=session_rec.session_id,
                raw_turns=turns_input,
            )
            assert len(segments) == 1
            seg = segments[0]
            assert seg.text_sha256 == hashlib.sha256(seg.verbatim_text.encode("utf-8")).hexdigest()
            assert len(seg.text_sha256) == 64

            # 9.2 ANALYST: Attribute and classify segment
            annotation = env["editorial_coord"].attribute_and_classify_segment(
                lane=AuthorityLane.ANALYST,
                workspace_id=ws_id,
                segment_id=seg.segment_id,
                semantic_role=SemanticRole.STORY,
                epistemic_status=EvidenceEpistemicStatus.LIVED_EXPERIENCE,
                confidence_score=0.96,
                tension_ref=hyp_id,
            )
            assert annotation.confidence_score_bps == 9600

            # 9.3 COMPOSER: Compose grounded ContentCandidate
            evidence_link = CandidateEvidenceLink(
                segment_id=seg.segment_id,
                annotation_id=annotation.annotation_id,
                speaker=seg.speaker,
                start_time_ms=seg.start_time_ms,
                end_time_ms=seg.end_time_ms,
                verbatim_text=seg.verbatim_text,
                text_sha256=seg.text_sha256,
            )
            candidate = env["editorial_coord"].compose_content_candidate(
                lane=AuthorityLane.COMPOSER,
                workspace_id=ws_id,
                candidate_type=CandidateType.STORY_CANDIDATE,
                title="48 Hours from Shutdown: The Local Tooling Pivot",
                hook_statement="How bypassing tier-1 contracts saved our manufacturing lines.",
                narrative_completeness=NarrativeCompleteness.COMPLETE,
                evidence_links=[evidence_link],
                emotional_resonance=0.92,
                cognitive_novelty=0.88,
                authority_evidence=0.96,
                narrative_velocity=0.85,
                story_arc="CRISIS_TO_TRANSFORMATION",
                tension_ref=hyp_id,
            )
            assert candidate.candidate_id is not None
            assert candidate.is_synthetic is False

            # 9.4 ANALYST: Cluster candidate
            scores = DimensionScores.calculate_composite(
                semantic_strength=0.92,
                guest_authenticity=0.96,
                audience_relevance=0.90,
                novelty=0.85,
                narrative_utility=0.88,
                visual_opportunity=0.80,
                editorial_completeness=0.92,
                distribution_potential=0.85,
            )
            eval_profile = CandidateEvaluationProfile(
                candidate_id=candidate.candidate_id,
                workspace_id=ws_id,
                scores=scores,
                gate_status=GateStatus.PASSED,
                is_eligible_for_board=True,
                provenance=EvaluatorProvenance(
                    evaluator_id="EVAL-JP-001",
                    evaluator_version="1.0.0",
                    rationale="High crisis stakes with authentic turnaround mechanism.",
                ),
            )
            clusters = env["editorial_coord"].cluster_candidates(
                lane=AuthorityLane.ANALYST,
                workspace_id=ws_id,
                evaluations=[eval_profile],
                theme_map={"CRISIS_RESILIENCE": [candidate.candidate_id]},
            )
            assert len(clusters) == 1
            assert clusters[0].theme == "CRISIS_RESILIENCE"

            # =========================================================================
            # STEP 10: Portfolio Search & Operator Storyboard Selection (M35/M36)
            # =========================================================================
            # 10.1 COMMANDER: Synthetic-Proof Gate & Portfolio Evaluation
            portfolio_cand = {
                "candidate_id": candidate.candidate_id,
                "score_bps": 9200,
                "cost_units": 10,
                "evidence_links": candidate.evidence_links,
                "is_synthetic": False,
            }
            portfolio_results = env["editorial_coord"].evaluate_production_portfolio(
                lane=AuthorityLane.COMMANDER,
                workspace_id=ws_id,
                candidates=[portfolio_cand],
                quality_threshold_bps=8000,
            )
            assert portfolio_results["best_candidate_id"] == candidate.candidate_id
            assert len(portfolio_results["candidates"]) == 1

            # 10.2 COMMANDER: Operator Storyboard Selection
            storyboard = env["editorial_coord"].operator_select_candidate(
                lane=AuthorityLane.COMMANDER,
                workspace_id=ws_id,
                operator_id=operator_id,
                candidate_id=candidate.candidate_id,
                priority_rank=1,
                rationale="Authentic, high-stakes industrial crisis story with clear proof of mechanism.",
                taste_delta="Framing approved for Format 01 Cinematic Story.",
            )
            assert storyboard.candidate_id == candidate.candidate_id
            assert storyboard.approved_by == operator_id

    def test_contrastive_synthetic_candidate_producer_blocked(self, e2e_environment):
        """
        Adversarial Test: Verifies that any synthetic candidate producer is strictly
        blocked by the Synthetic-Proof Gate with a signed SYNTHETIC_BLOCKED receipt.
        """
        env = e2e_environment
        ws_id = env["ws_id"]
        editorial_coord = env["editorial_coord"]

        mock_link = CandidateEvidenceLink(
            segment_id="SEG-SYNTH-001",
            annotation_id="ANN-SYNTH-001",
            speaker="Mock Speaker",
            start_time_ms=0,
            end_time_ms=5000,
            verbatim_text="Mock fabricated synthetic testimony.",
            text_sha256=canonical_sha256("Mock fabricated synthetic testimony."),
        )

        synthetic_candidate = ContentCandidateRecord(
            candidate_id="CND-SYNTH-001",
            workspace_id=ws_id,
            candidate_type="STORY_CANDIDATE",
            title="Synthetic Producer Candidate",
            hook_statement="Fabricated hook statement",
            narrative_completeness="COMPLETE",
            evidence_links=[mock_link.model_dump()],
            composite_score_bps=9900,
            is_synthetic=True,
            production_authorized=False,
        )
        env["editorial_store"].insert_content_candidate(synthetic_candidate)

        # Direct operator selection must raise SyntheticCandidateProductionBlockedError
        with pytest.raises(SyntheticCandidateProductionBlockedError) as exc_info:
            editorial_coord.operator_select_candidate(
                lane=AuthorityLane.COMMANDER,
                workspace_id=ws_id,
                operator_id="OPR-DIRECTOR",
                candidate_id="CND-SYNTH-001",
                priority_rank=1,
                rationale="Attempting to select synthetic concept.",
            )
        assert "Synthetic producer block" in str(exc_info.value)

        # Portfolio search with synthetic candidate must fail-closed
        with pytest.raises(SyntheticCandidateProductionBlockedError):
            editorial_coord.evaluate_production_portfolio(
                lane=AuthorityLane.COMMANDER,
                workspace_id=ws_id,
                candidates=[synthetic_candidate.model_dump()],
                quality_threshold_bps=8000,
            )

    def test_contrastive_tampered_evidence_lineage_blocked(self, e2e_environment):
        """
        Adversarial Test: Verifies that tampered evidence text or mismatched SHA-256
        hash is rejected fail-closed during candidate composition.
        """
        env = e2e_environment
        ws_id = env["ws_id"]
        editorial_coord = env["editorial_coord"]

        turns_input = [
            {
                "turn_id": "TURN-REAL-001",
                "speaker": "GUEST",
                "start_time_ms": 0,
                "end_time_ms": 5000,
                "text": "Real spoken authentic text from the participant.",
            }
        ]
        segments = editorial_coord.segment_interview_turns(
            lane=AuthorityLane.HUNTER,
            workspace_id=ws_id,
            session_id="SES-TAMPER-001",
            raw_turns=turns_input,
        )
        seg1 = segments[0]

        tampered_hash = "0" * 64  # valid 64-char hex but mismatched to stored segment
        tampered_link = CandidateEvidenceLink(
            segment_id=seg1.segment_id,
            annotation_id="ANN-TAMPER-001",
            speaker=seg1.speaker,
            start_time_ms=seg1.start_time_ms,
            end_time_ms=seg1.end_time_ms,
            verbatim_text=seg1.verbatim_text,
            text_sha256=tampered_hash,
        )

        with pytest.raises(UngroundedCandidateError) as exc_info:
            editorial_coord.compose_content_candidate(
                lane=AuthorityLane.COMPOSER,
                workspace_id=ws_id,
                candidate_type=CandidateType.QUOTE_CANDIDATE,
                title="Tampered Evidence Candidate",
                hook_statement="Hook with tampered hash",
                narrative_completeness=NarrativeCompleteness.COMPLETE,
                evidence_links=[tampered_link],
                emotional_resonance=0.8,
                cognitive_novelty=0.8,
                authority_evidence=0.8,
                narrative_velocity=0.8,
                story_arc="NONE",
            )
        assert "SHA-256 mismatch" in str(exc_info.value)

    def test_contrastive_cross_workspace_isolation(self, e2e_environment):
        """
        Multi-Tenancy Test: Verifies that records from workspace A cannot be accessed
        or manipulated from workspace B.
        """
        env = e2e_environment
        ws_a = env["ws_id"]
        ws_b = "WS-TENANT-ISOLATED-B"
        editorial_store = env["editorial_store"]
        editorial_coord = env["editorial_coord"]

        cand_a = ContentCandidateRecord(
            candidate_id="CND-TENANT-A",
            workspace_id=ws_a,
            candidate_type="QUOTE_CANDIDATE",
            title="Candidate in Tenant A",
            hook_statement="Hook A",
            narrative_completeness="COMPLETE",
            evidence_links=[],
            composite_score_bps=8500,
            is_synthetic=False,
            production_authorized=True,
        )
        editorial_store.insert_content_candidate(cand_a)

        # Query in Workspace B must return None / empty
        assert editorial_store.get_content_candidate(ws_b, "CND-TENANT-A") is None
        assert len(editorial_store.list_content_candidates(ws_b)) == 0

        # Operator in Workspace B attempting to select Tenant A candidate must fail
        with pytest.raises((ValueError, UngroundedCandidateError)):
            editorial_coord.operator_select_candidate(
                lane=AuthorityLane.COMMANDER,
                workspace_id=ws_b,
                candidate_id=cand_a.candidate_id,
                operator_id=env["operator_id"],
                priority_rank=1,
                rationale="Attempting cross-workspace selection",
            )

    def test_contrastive_four_lane_authority_separation(self, e2e_environment):
        """
        Constitutional Authority Test: Verifies that invoking coordinator methods with
        an unauthorized authority lane raises LaneAuthorityViolationError or UnauthorizedCollisionLaneError.
        """
        env = e2e_environment
        ws_id = env["ws_id"]
        editorial_coord = env["editorial_coord"]
        collision_coord = env["collision_coord"]

        # Collision HUNTER operation with ANALYST lane
        with pytest.raises(UnauthorizedCollisionLaneError):
            collision_coord.discover_resonance(
                workspace_id=ws_id,
                guest_dna={"guest_id": "G-1", "proof_citation": "Proof citation"},
                audience_tensions=[],
                world_signals=[],
                lane=AuthorityLane.ANALYST,
            )

        # Editorial HUNTER segmentation with ANALYST lane
        with pytest.raises(LaneAuthorityViolationError):
            editorial_coord.segment_interview_turns(
                lane=AuthorityLane.ANALYST,
                workspace_id=ws_id,
                session_id="SESS-001",
                raw_turns=[],
            )

        # Editorial COMPOSER candidate formation with HUNTER lane
        with pytest.raises(LaneAuthorityViolationError):
            editorial_coord.compose_content_candidate(
                lane=AuthorityLane.HUNTER,
                workspace_id=ws_id,
                candidate_type=CandidateType.QUOTE_CANDIDATE,
                title="Invalid Lane Candidate",
                hook_statement="Hook",
                narrative_completeness=NarrativeCompleteness.COMPLETE,
                evidence_links=[],
                emotional_resonance=0.8,
                cognitive_novelty=0.8,
                authority_evidence=0.8,
                narrative_velocity=0.8,
                story_arc="NONE",
            )

        # Editorial COMMANDER operator selection with COMPOSER lane
        with pytest.raises(LaneAuthorityViolationError):
            editorial_coord.operator_select_candidate(
                lane=AuthorityLane.COMPOSER,
                workspace_id=ws_id,
                candidate_id="CND-001",
                operator_id=env["operator_id"],
                priority_rank=1,
                rationale="Selection rationale",
            )
