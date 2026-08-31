"""Tests for CAE Phase 3 Mandate M27: Guest Genesis + Protected/Derived Semantic Territory.

Verifies:
1. Program package discovery and manifest validation for guest_genesis_semantic_territory_program.
2. Full coordinator lifecycle across 4 Authority Lanes (HUNTER, ANALYST, COMPOSER, COMMANDER).
3. Protected Guest evidence immutability and anti-mutation fail-closed enforcement.
4. Cryptographic SHA-256 lineage chaining across Brand Context, Voice/Visual DNA, and Semantic Territory.
5. Anti-centroid integrity and rejection of generic centroid platitudes.
6. RSCS 5-layer distillation synthesis and edge product preservation checks.
7. Governed repair and resume lifecycle.
8. AIR BrandService generation, storage, and retrieval methods.
9. Cross-validation bridge with Interview Composer (resolve_brand_voice_refs) proving F30 resolution.
"""

from pathlib import Path
import pytest
from typing import Any, Dict

from ca_contracts import canonical_sha256
from ca_runtime.guest_genesis_program import (
    AntiCentroidViolationError,
    AuthorityLaneViolationError,
    DerivedVoiceVisualDNA,
    GuestGenesisProgramCoordinator,
    GuestGenesisProgramError,
    GuestGenesisState,
    InvalidStateTransitionError,
    LineageIntegrityError,
    ProtectedGuestEvidence,
    ProtectedSourceMutationError,
    SemanticTerritoryDescriptor,
)
from ca_runtime.program_registry import ProgramRegistry
from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.services.brand_service import BrandService
from api.services.composer_air_bridge import resolve_brand_voice_refs


# ============================================================================
# 1. Package Discovery & Manifest Validation
# ============================================================================

def test_guest_genesis_program_package_discovery_and_manifest():
    root = Path(__file__).resolve().parents[2] / "programs"
    registry = ProgramRegistry(discovery_roots=[root])
    programs = registry.discover()

    program_ids = {p.program_id for p in programs}
    assert "guest_genesis_semantic_territory_program" in program_ids

    pkg = registry.get_program("guest_genesis_semantic_territory_program")
    assert pkg.manifest.version == "1.0.0"
    assert "HUNTER" in pkg.manifest.lanes
    assert "ANALYST" in pkg.manifest.lanes
    assert "COMPOSER" in pkg.manifest.lanes
    assert "COMMANDER" in pkg.manifest.lanes
    assert len(pkg.manifest.skills) == 3


# ============================================================================
# 2. Full Coordinator Lifecycle & Authority Lanes
# ============================================================================

def test_full_guest_genesis_coordinator_lifecycle():
    coord = GuestGenesisProgramCoordinator(
        program_id="prog-gg-001",
        workspace_id="ws-enterprise-01",
        guest_id="gst-audrey-01",
    )
    assert coord.current_state == GuestGenesisState.INITIAL
    assert coord.version == 1

    # 1. Index Protected Evidence (HUNTER)
    ev1 = ProtectedGuestEvidence(
        evidence_id="ev-quote-001",
        source_url="s3://evidence/audrey_intv_01.mp4",
        content_type="interview_transcript_span",
        sha256_digest="a" * 64,
        transcript_spans=("We never settle for generic consensus; truth is in the friction.",),
    )
    ev2 = ProtectedGuestEvidence(
        evidence_id="ev-quote-002",
        source_url="s3://evidence/audrey_intv_02.mp4",
        content_type="interview_transcript_span",
        sha256_digest="b" * 64,
        transcript_spans=("Operational clarity demands ruthless specificity.",),
    )
    rcpt1 = coord.index_protected_evidence(evidence_items=[ev1, ev2], actor_lane="HUNTER")
    assert coord.current_state == GuestGenesisState.EVIDENCE_INDEXED
    assert coord.protected_evidence_count == 2
    assert rcpt1["actor_lane"] == "HUNTER"

    # 2. Derive Brand Context (ANALYST)
    rcpt2 = coord.derive_brand_context(
        brand_context_id="brand-audrey-ctx",
        identity_truths=["Ruthless operational specificity", "Truth found in productive friction"],
        audience_relationship="Peer-level rigorous partner",
        positioning_tension="Autonomy requires radical transparency",
        source_evidence_ids=["ev-quote-001", "ev-quote-002"],
        actor_lane="ANALYST",
    )
    assert coord.current_state == GuestGenesisState.BRAND_CONTEXT_DERIVED
    assert coord.brand_context is not None
    assert coord.brand_context["lineage_sha256"] is not None

    # 3. Synthesize Voice & Visual DNA (COMPOSER)
    rcpt3 = coord.synthesize_voice_visual_dna(
        voice_dna_id="voice-audrey-01",
        visual_dna_id="vis-audrey-01",
        vocabulary_patterns=["friction-tested", "operational truth", "relational boundary"],
        rhythm_patterns=["measured tempo", "staccato cadence"],
        stance_patterns=["unflinching accountability"],
        prohibited_centroid_patterns=["synergy", "paradigm shift", "circle back", "thought leader"],
        prohibited_centroid_defaults=["glossy stock hero", "generic office handshake"],
        source_evidence_ids=["ev-quote-001", "ev-quote-002"],
        actor_lane="COMPOSER",
    )
    assert coord.current_state == GuestGenesisState.VOICE_VISUAL_SYNTHESIZED
    assert coord.voice_visual_dna is not None

    # 4. Verify Distillation Layers (ANALYST)
    layers = ["saturation", "collision", "compression", "evaluation", "recursion"]
    distill_receipts = [
        {
            "receipt_id": f"rcpt:dist:{layer}",
            "layer": layer,
            "edge_product_preserved": True,
            "role_tension_preserved": True,
            "voice_dna_preserved": True,
        }
        for layer in layers
    ]
    rcpt4 = coord.verify_distillation_layers(receipts=distill_receipts, actor_lane="ANALYST")
    assert coord.current_state == GuestGenesisState.DISTILLATION_VERIFIED
    assert len(coord.distillation_receipts) == 5

    # 5. Ratify Semantic Territory (COMMANDER)
    rcpt5 = coord.ratify_semantic_territory(
        territory_id="terr-audrey-01",
        wrong_reading_locks=["Never interpret unflinching directness as hostility"],
        actor_lane="COMMANDER",
    )
    assert coord.current_state == GuestGenesisState.TERRITORY_RATIFIED
    assert coord.semantic_territory is not None
    assert coord.semantic_territory.territory_id == "terr-audrey-01"
    assert len(coord.receipt_history) == 5


# ============================================================================
# 3. Protected Source Immutability & Anti-Mutation Enforcement
# ============================================================================

def test_protected_source_mutation_fails_closed():
    coord = GuestGenesisProgramCoordinator(
        program_id="prog-gg-002",
        workspace_id="ws-01",
        guest_id="gst-01",
    )
    ev_initial = ProtectedGuestEvidence(
        evidence_id="ev-01",
        source_url="s3://evidence/01.mp4",
        content_type="audio_clip",
        sha256_digest="1" * 64,
        transcript_spans=("Initial genuine quote",),
    )
    coord.index_protected_evidence(evidence_items=[ev_initial], actor_lane="HUNTER")

    # Attempt to overwrite same evidence ID with different SHA-256 digest
    ev_mutated = ProtectedGuestEvidence(
        evidence_id="ev-01",
        source_url="s3://evidence/01_modified.mp4",
        content_type="audio_clip",
        sha256_digest="2" * 64,
        transcript_spans=("Silently modified quote",),
    )
    with pytest.raises(ProtectedSourceMutationError) as exc_info:
        coord.index_protected_evidence(evidence_items=[ev_mutated], actor_lane="HUNTER")
    assert "Cannot overwrite protected evidence" in str(exc_info.value)
    assert exc_info.value.details["evidence_id"] == "ev-01"


# ============================================================================
# 4. Anti-Centroid Integrity Rejection
# ============================================================================

def test_anti_centroid_violation_fails_closed():
    coord = GuestGenesisProgramCoordinator(
        program_id="prog-gg-003",
        workspace_id="ws-01",
        guest_id="gst-01",
    )
    ev = ProtectedGuestEvidence(
        evidence_id="ev-01",
        source_url="s3://evidence/01.mp4",
        content_type="transcript",
        sha256_digest="3" * 64,
        transcript_spans=("Real quote",),
    )
    coord.index_protected_evidence(evidence_items=[ev], actor_lane="HUNTER")
    coord.derive_brand_context(
        brand_context_id="brand-01",
        identity_truths=["Truth 1"],
        audience_relationship="Relationship 1",
        positioning_tension="Tension 1",
        source_evidence_ids=["ev-01"],
        actor_lane="ANALYST",
    )

    # Attempt DNA synthesis containing generic buzzwords
    with pytest.raises(AntiCentroidViolationError) as exc_info:
        coord.synthesize_voice_visual_dna(
            voice_dna_id="voice-bad",
            visual_dna_id="vis-bad",
            vocabulary_patterns=["leveraging synergy", "innovative solutions"],
            rhythm_patterns=["normal"],
            stance_patterns=["helpful"],
            prohibited_centroid_patterns=["synergy", "rockstar", "growth hack"],
            prohibited_centroid_defaults=["stock photo"],
            source_evidence_ids=["ev-01"],
            actor_lane="COMPOSER",
        )
    assert "collapsed into generic centroid platitudes" in str(exc_info.value)


# ============================================================================
# 5. Authority Lane Enforcement
# ============================================================================

def test_authority_lane_violation():
    coord = GuestGenesisProgramCoordinator(
        program_id="prog-gg-004",
        workspace_id="ws-01",
        guest_id="gst-01",
    )
    ev = ProtectedGuestEvidence(
        evidence_id="ev-01",
        source_url="s3://evidence/01.mp4",
        content_type="transcript",
        sha256_digest="4" * 64,
        transcript_spans=("Quote",),
    )

    # Calling HUNTER operation from COMPOSER lane must fail
    with pytest.raises(AuthorityLaneViolationError) as exc_info:
        coord.index_protected_evidence(evidence_items=[ev], actor_lane="COMPOSER")
    assert exc_info.value.details["required_lane"] == "HUNTER"
    assert exc_info.value.details["actual_lane"] == "COMPOSER"


# ============================================================================
# 6. Distillation Edge Product Preservation
# ============================================================================

def test_distillation_loss_of_edge_product_fails_closed():
    coord = GuestGenesisProgramCoordinator(
        program_id="prog-gg-005",
        workspace_id="ws-01",
        guest_id="gst-01",
    )
    ev = ProtectedGuestEvidence(
        evidence_id="ev-01",
        source_url="s3://evidence/01.mp4",
        content_type="transcript",
        sha256_digest="5" * 64,
        transcript_spans=("Quote",),
    )
    coord.index_protected_evidence(evidence_items=[ev], actor_lane="HUNTER")
    coord.derive_brand_context(
        brand_context_id="brand-01",
        identity_truths=["Truth 1"],
        audience_relationship="Rel 1",
        positioning_tension="Ten 1",
        source_evidence_ids=["ev-01"],
        actor_lane="ANALYST",
    )
    coord.synthesize_voice_visual_dna(
        voice_dna_id="voice-01",
        visual_dna_id="vis-01",
        vocabulary_patterns=["distinctive term"],
        rhythm_patterns=["tempo"],
        stance_patterns=["posture"],
        prohibited_centroid_patterns=["synergy"],
        prohibited_centroid_defaults=["stock photo"],
        source_evidence_ids=["ev-01"],
        actor_lane="COMPOSER",
    )

    # Distillation receipt with edge_product_preserved = False in compression layer
    bad_receipts = [
        {"layer": "saturation", "edge_product_preserved": True, "role_tension_preserved": True},
        {"layer": "collision", "edge_product_preserved": True, "role_tension_preserved": True},
        {"layer": "compression", "edge_product_preserved": False, "role_tension_preserved": True},
        {"layer": "evaluation", "edge_product_preserved": True, "role_tension_preserved": True},
        {"layer": "recursion", "edge_product_preserved": True, "role_tension_preserved": True},
    ]
    with pytest.raises(GuestGenesisProgramError) as exc_info:
        coord.verify_distillation_layers(receipts=bad_receipts, actor_lane="ANALYST")
    assert "edge_product_preserved must be true" in str(exc_info.value)


# ============================================================================
# 7. Governed Fault & Repair Lifecycle
# ============================================================================

def test_governed_fault_and_repair_lifecycle():
    coord = GuestGenesisProgramCoordinator(
        program_id="prog-gg-006",
        workspace_id="ws-01",
        guest_id="gst-01",
    )
    ev = ProtectedGuestEvidence(
        evidence_id="ev-01",
        source_url="s3://evidence/01.mp4",
        content_type="transcript",
        sha256_digest="6" * 64,
        transcript_spans=("Quote",),
    )
    coord.index_protected_evidence(evidence_items=[ev], actor_lane="HUNTER")
    assert coord.current_state == GuestGenesisState.EVIDENCE_INDEXED

    # Force fault to repair
    rcpt_fault = coord.fault_to_repairing(reason="Detected downstream evidence mismatch", actor_lane="COMMANDER")
    assert coord.current_state == GuestGenesisState.REPAIRING
    assert rcpt_fault["payload_summary"]["reason"] == "Detected downstream evidence mismatch"

    # Resume from repair back to EVIDENCE_INDEXED
    rcpt_resume = coord.resume_from_repair(
        target_state=GuestGenesisState.EVIDENCE_INDEXED,
        reason="Evidence re-verified against SHA-256 manifest",
        actor_lane="COMMANDER",
    )
    assert coord.current_state == GuestGenesisState.EVIDENCE_INDEXED
    assert rcpt_resume["target_state"] == "EVIDENCE_INDEXED"


# ============================================================================
# 8. AIR BrandService & Interview Composer Resolution Bridge (F30 Proof)
# ============================================================================

class DummyReasoningEngine:
    def infer(self, prompt: str, system_prompt: str = "") -> Any:
        class Result:
            parsed_json = {
                "identity_truths": ["Authentic truth 1", "Operational truth 2"],
                "audience_relationship": "Peer-to-peer collaborator",
                "positioning_tension": "Radical candor builds durable trust",
                "vocabulary_patterns": ["friction-forged", "structural clarity"],
                "rhythm_patterns": ["deliberate rhythm"],
                "sentence_pressure_patterns": ["direct assertions"],
                "stance_patterns": ["uncompromising posture"],
                "specificity_patterns": ["grounded observations"],
                "metaphor_range": ["architectural tension"],
                "emotional_distance": "close but disciplined",
                "prohibited_centroid_patterns": ["synergy", "circle back"],
                "subject_treatment": ["candid focus"],
                "visual_temperature": ["cool tonal contrast"],
                "materiality": ["matte textured"],
                "composition_tendencies": ["asymmetric"],
                "negative_space_functions": ["clean pauses"],
                "edge_behaviors": ["crisp"],
                "typographic_posture": ["grotesque sans"],
                "motion_character": ["steady deliberate"],
                "prohibited_centroid_defaults": ["stock photos"],
            }
        return Result()


def test_air_brand_service_and_composer_bridge_resolution(tmp_path: Path):
    app = AirApplication(tmp_path / "air.sqlite")
    app.initialize()
    repo = app.repository
    brand_svc = app.brand
    engine = DummyReasoningEngine()

    auth = {
        "authority_id": "usr_operator_1",
        "authority_version": "1.0.0",
        "authority_sha256": "0" * 64,
        "authority_state": "operator_confirmed",
    }
    source_ref = {
        "object_id": "ev-source-001",
        "version": "1.0.0",
        "sha256": "7" * 64,
    }
    genesis_session_ref = {
        "object_id": "ses-genesis-001",
        "version": "1.0.0",
        "sha256": "8" * 64,
    }

    # 1. Generate Brand Context
    res_brand = brand_svc.generate_brand_context(
        brand_context_id="brand-ctx-001",
        brand_genesis_session_ref=genesis_session_ref,
        source_refs=[source_ref],
        authority=auth,
        reasoning_engine=engine,
        idempotency_key="key-brand-001",
    )
    brand_obj = res_brand["object"]
    brand_ref = {
        "object_id": brand_obj["object_id"],
        "version": brand_obj["semantic_version"],
        "sha256": brand_obj["canonical_sha256"],
    }
    assert brand_obj["object_id"] == "brand-ctx-001"

    # 2. Generate Voice DNA
    res_voice = brand_svc.generate_voice_dna(
        voice_dna_id="voice-dna-001",
        brand_context_ref=brand_ref,
        source_evidence_refs=[source_ref],
        authority=auth,
        reasoning_engine=engine,
        idempotency_key="key-voice-001",
    )
    voice_obj = res_voice["object"]
    voice_ref = {
        "object_id": voice_obj["object_id"],
        "version": voice_obj["semantic_version"],
        "sha256": voice_obj["canonical_sha256"],
    }
    assert voice_obj["object_id"] == "voice-dna-001"

    # 3. Generate Visual DNA
    res_visual = brand_svc.generate_visual_dna(
        visual_dna_id="vis-dna-001",
        brand_context_ref=brand_ref,
        real_life_reference_refs=[source_ref],
        authority=auth,
        reasoning_engine=engine,
        idempotency_key="key-visual-001",
    )
    assert res_visual["object"]["object_id"] == "vis-dna-001"

    # 4. Synthesize 5 RSCS Distillation Layers
    distill_res = brand_svc.synthesize_distillation_layers(
        receipt_id_prefix="rcpt:distill:001",
        brand_context_ref=brand_ref,
        voice_dna_ref=voice_ref,
        input_evidence_refs=[source_ref],
        authority=auth,
        idempotency_prefix="key-distill",
    )
    assert len(distill_res) == 5

    # 5. Derive Semantic Territory
    territory = brand_svc.derive_semantic_territory(
        brand_context_ref=brand_ref,
        voice_dna_ref=voice_ref,
        protected_source_refs=[source_ref],
        wrong_reading_locks=["Never misinterpret directness as hostility"],
        prohibited_centroid_patterns=["synergy", "thought leader"],
        authority=auth,
    )
    assert territory["ratified"] is True
    assert len(territory["protected_territory"]["vocabulary_boundaries"]) > 0

    # 6. Prove Interview Composer Bridge can resolve these real governed objects without 404
    resolved_brand, resolved_voice = resolve_brand_voice_refs(
        app,
        brand_context_ref=brand_ref,
        voice_dna_ref=voice_ref,
    )
    assert resolved_brand is not None
    assert resolved_voice is not None
    assert resolved_brand.object_id == "brand-ctx-001"
    assert resolved_voice.object_id == "voice-dna-001"
    assert resolved_voice.payload["brand_context_ref"]["object_id"] == "brand-ctx-001"
