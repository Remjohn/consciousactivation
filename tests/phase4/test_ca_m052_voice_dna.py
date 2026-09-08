"""CA-M052 / INV-VOICE-001 executable proof suite."""

from __future__ import annotations

import base64
import io
import importlib.util
import math
import sqlite3
import struct
import sys
import types
import wave
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
COLLISION_SRC = REPO_ROOT / "services" / "collision-intelligence" / "src"
CA_RUNTIME_SRC = REPO_ROOT / "packages" / "ca_runtime" / "src"
if str(COLLISION_SRC) not in sys.path:
    sys.path.insert(0, str(COLLISION_SRC))

from cae_collision_intelligence.composer import (  # noqa: E402
    SubjectVoiceDNAVerifier,
    TranscriptSegment,
    QuoteSpan,
    VoiceDNAExtractor,
    VoiceDNAGateRejectedError,
    VoiceDNAVerificationInput,
    VoiceDNAProfile,
)


def _load_runtime_module():
    """Load the mandated runtime file without executing ca_runtime.__init__ dependencies."""
    fake_package = types.ModuleType("ca_runtime")
    fake_package.__path__ = [str(CA_RUNTIME_SRC / "ca_runtime")]
    sys.modules.setdefault("ca_runtime", fake_package)

    class AuthorityLane(str, Enum):
        HUNTER = "HUNTER"
        ANALYST = "ANALYST"
        COMPOSER = "COMPOSER"
        COMMANDER = "COMMANDER"

    class Aggregate:
        aggregate_id = "aggregate-001"
        current_state = "HYPOTHESIS_FORMED"
        lifecycle = types.SimpleNamespace(value="ACTIVE")
        version = 1
        updated_at = "2026-09-08T14:00:00Z"

    class UniversalProgramStateRuntime:
        def __init__(self):
            self.aggregate = Aggregate()

        def get_aggregate(self, aggregate_id):
            return self.aggregate

        def initialize_program_state(self, **_kwargs):
            return self.aggregate

        def execute_transition(self, **_kwargs):
            return types.SimpleNamespace()

    state_mod = types.ModuleType("ca_runtime.program_state_runtime")
    state_mod.AuthorityLane = AuthorityLane
    state_mod.UniversalProgramStateRuntime = UniversalProgramStateRuntime
    state_mod.ProgramTransitionResult = object
    state_mod.ProgramStateAggregate = object
    sys.modules["ca_runtime.program_state_runtime"] = state_mod

    store_path = CA_RUNTIME_SRC / "ca_runtime" / "collision_hypothesis_store.py"
    store_spec = importlib.util.spec_from_file_location("ca_runtime.collision_hypothesis_store", store_path)
    store_mod = importlib.util.module_from_spec(store_spec)
    sys.modules[store_spec.name] = store_mod
    assert store_spec.loader is not None
    store_spec.loader.exec_module(store_mod)

    runtime_path = CA_RUNTIME_SRC / "ca_runtime" / "collision_hypothesis_program.py"
    runtime_spec = importlib.util.spec_from_file_location("ca_runtime.collision_hypothesis_program", runtime_path)
    runtime_mod = importlib.util.module_from_spec(runtime_spec)
    sys.modules[runtime_spec.name] = runtime_mod
    assert runtime_spec.loader is not None
    runtime_spec.loader.exec_module(runtime_mod)
    return runtime_mod, store_mod


RUNTIME, STORE = _load_runtime_module()


@dataclass(frozen=True)
class ConstitutionFixture:
    subject_id: str = "subject-001"
    revision: int = 1
    content_sha256: str = "a" * 64


def _tone_wav(*, frequency_hz: float = 220.0, amplitude: float = 0.25, duration_seconds: float = 2.0, sample_rate: int = 8000) -> bytes:
    samples = (
        struct.pack("<h", int(amplitude * 32767 * math.sin(2 * math.pi * frequency_hz * n / sample_rate)))
        for n in range(int(sample_rate * duration_seconds))
    )
    raw = b"".join(samples)
    output = io.BytesIO()
    with wave.open(output, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(raw)
    return output.getvalue()


def _source_segments():
    return (
        TranscriptSegment(
            "subject-001",
            "I tell people, build systems before you build scale. Scale punishes a weak habit. That's the whole point.",
        ),
    )


def _profile(source_audio: bytes | None = None, *, tenant_id: str = "tenant-001"):
    return VoiceDNAExtractor.build_profile(
        tenant_id=tenant_id,
        constitution=ConstitutionFixture(),
        source_segments=_source_segments(),
        source_audio_wav=source_audio or _tone_wav(),
    )


def _request(profile: VoiceDNAProfile, *, synthesized_text: str | None = None, synthesized_audio: bytes | None = None,
             quotes: tuple[QuoteSpan, ...] | None = None, tenant_id: str = "tenant-001",
             revision: int = 1, content_sha256: str = "a" * 64, generic_style_score: float | None = None):
    source_audio = _tone_wav()
    source = _source_segments()
    synthesized = (TranscriptSegment("subject-001", synthesized_text or source[0].text),)
    return VoiceDNAVerificationInput(
        tenant_id=tenant_id,
        subject_id="subject-001",
        constitution_revision=revision,
        constitution_content_sha256=content_sha256,
        source_segments=source,
        synthesized_segments=synthesized,
        synthesized_quotes=quotes or (QuoteSpan("subject-001", "build systems before you build scale"),),
        source_audio_wav=source_audio,
        synthesized_audio_wav=synthesized_audio or source_audio,
        generic_style_score=generic_style_score,
    )


def test_ca_m052_01_extracts_deterministic_acoustic_and_linguistic_dna():
    source = _source_segments()[0].text
    acoustic = VoiceDNAExtractor.extract_acoustic_dna(_tone_wav(frequency_hz=220.0))
    linguistic = VoiceDNAExtractor.extract_linguistic_dna(source, duration_seconds=2.0)

    assert acoustic["rms_energy"] > 0
    assert acoustic["zero_crossing_rate"] > 0
    assert acoustic["pitch_mean_hz"] > 70
    assert acoustic["pitch_std_hz"] >= 0
    assert linguistic["avg_sentence_words"] == pytest.approx(6.0)
    assert "systems" in linguistic["terminology"]
    assert "scale" in linguistic["terminology"]
    assert linguistic["speaking_rate_wpm"] == pytest.approx(540.0)


def test_ca_m052_02_profile_is_immutably_bound_to_tenant_subject_and_constitution():
    profile = _profile()
    assert profile.binding_sha256
    with pytest.raises((AttributeError, TypeError)):
        profile.subject_id = "other"  # type: ignore[misc]
    with pytest.raises(TypeError):
        profile.linguistic_dna["terminology"]["invented"] = 1.0  # type: ignore[index]

    request = _request(profile)
    report = SubjectVoiceDNAVerifier.verify(profile=profile, request=request)
    assert report.accepted is True
    assert report.constitution_binding_sha256 == profile.binding_sha256


def test_ca_m052_03_accepts_subject_exact_quote_and_matching_acoustic_linguistic_dna_even_with_generic_score():
    profile = _profile()
    request = _request(profile, generic_style_score=0.99)

    report = SubjectVoiceDNAVerifier.verify(profile=profile, request=request)

    assert report.accepted is True
    assert report.quote_fidelity_passed is True
    assert report.voice_drift_score == pytest.approx(0.0)
    assert report.distinctiveness_score == pytest.approx(1.0)
    assert report.generic_style_score == pytest.approx(0.99)


def test_ca_m052_04_rejects_paraphrased_quote_with_character_exact_diff():
    profile = _profile()
    request = _request(
        profile,
        quotes=(QuoteSpan("subject-001", "build a system before you build scale"),),
    )

    with pytest.raises(VoiceDNAGateRejectedError) as exc_info:
        SubjectVoiceDNAVerifier.verify(profile=profile, request=request)

    report = exc_info.value.report
    assert "CHARACTER_EXACT_QUOTE_DIFF_FAILED" in report.rejection_reasons
    assert report.quote_diffs[0].exact_match is False
    assert report.quote_diffs[0].attribution_match is True
    assert report.quote_diffs[0].character_diff


def test_ca_m052_05_rejects_quote_with_wrong_speaker_attribution():
    profile = _profile()
    request = _request(
        profile,
        quotes=(QuoteSpan("other-speaker", "build systems before you build scale"),),
    )

    with pytest.raises(VoiceDNAGateRejectedError) as exc_info:
        SubjectVoiceDNAVerifier.verify(profile=profile, request=request)

    report = exc_info.value.report
    assert "CHARACTER_EXACT_QUOTE_DIFF_FAILED" in report.rejection_reasons
    assert report.quote_diffs[0].attribution_match is False


def test_ca_m052_06_false_proof_generic_script_is_rejected_despite_high_generic_style_score_and_accurate_quote():
    profile = _profile()
    generic = "Build systems and unlock your potential. Scale smarter and crush your goals."
    request = _request(profile, synthesized_text=generic, generic_style_score=0.99)

    with pytest.raises(VoiceDNAGateRejectedError) as exc_info:
        SubjectVoiceDNAVerifier.verify(profile=profile, request=request)

    report = exc_info.value.report
    assert report.generic_style_score == pytest.approx(0.99)
    assert report.quote_fidelity_passed is True
    assert "ANTI_GENERICIZATION_THRESHOLD_FAILED" in report.rejection_reasons
    assert report.distinctiveness_score < profile.min_distinctiveness_score


def test_ca_m052_07_rejects_unacceptable_acoustic_voice_drift():
    profile = _profile()
    drifted_audio = _tone_wav(frequency_hz=350.0, amplitude=0.45, duration_seconds=1.4)
    request = _request(profile, synthesized_audio=drifted_audio)

    with pytest.raises(VoiceDNAGateRejectedError) as exc_info:
        SubjectVoiceDNAVerifier.verify(profile=profile, request=request)

    report = exc_info.value.report
    assert "VOICE_DRIFT_THRESHOLD_EXCEEDED" in report.rejection_reasons
    assert report.acoustic_drift_score > 0
    assert report.voice_drift_score > profile.max_drift_score


def test_ca_m052_08_rejects_cross_tenant_or_stale_constitution_binding():
    profile = _profile()

    with pytest.raises(VoiceDNAGateRejectedError) as tenant_exc:
        SubjectVoiceDNAVerifier.verify(profile=profile, request=_request(profile, tenant_id="tenant-999"))
    assert "TENANT_OR_SUBJECT_BINDING_MISMATCH" in tenant_exc.value.report.rejection_reasons

    with pytest.raises(VoiceDNAGateRejectedError) as revision_exc:
        SubjectVoiceDNAVerifier.verify(profile=profile, request=_request(profile, revision=2))
    assert "CONSTITUTION_BINDING_MISMATCH" in revision_exc.value.report.rejection_reasons


def test_ca_m052_09_runtime_persists_rejection_receipt_without_storing_rejected_hypothesis():
    conn = sqlite3.connect(":memory:")
    store = STORE.CollisionHypothesisStore(conn)
    coordinator = RUNTIME.CollisionHypothesisProgramCoordinator(
        workspace_id="tenant-001",
        store=store,
        state_runtime=RUNTIME.UniversalProgramStateRuntime(),
    )
    profile = _profile()
    request = _request(
        profile,
        synthesized_text="Build systems and unlock your potential. Scale smarter and crush your goals.",
        generic_style_score=0.99,
    )

    with pytest.raises(RUNTIME.VoiceDNAGateRejectedError):
        coordinator.verify_synthesis_voice_dna(
            workspace_id="tenant-001",
            portfolio_id="portfolio-001",
            hypothesis_id="HYP-VOICE-001",
            request={
                "tenant_id": request.tenant_id,
                "subject_id": request.subject_id,
                "constitution_revision": request.constitution_revision,
                "constitution_content_sha256": request.constitution_content_sha256,
                "profile": profile.as_mapping(),
                "source_segments": [{"speaker_id": segment.speaker_id, "text": segment.text} for segment in request.source_segments],
                "synthesized_segments": [{"speaker_id": segment.speaker_id, "text": segment.text} for segment in request.synthesized_segments],
                "synthesized_quotes": [{"speaker_id": quote.speaker_id, "text": quote.text} for quote in request.synthesized_quotes],
                "source_audio_wav_b64": base64.b64encode(request.source_audio_wav).decode(),
                "synthesized_audio_wav_b64": base64.b64encode(request.synthesized_audio_wav).decode(),
                "generic_style_score": request.generic_style_score,
            },
        )

    receipts = store.list_evaluation_receipts("tenant-001", portfolio_id="portfolio-001", hypothesis_id="HYP-VOICE-001")
    assert len(receipts) == 1
    receipt = receipts[0]
    assert receipt.decision == "REJECTED"
    assert receipt.evaluator_lane == "COMPOSER"
    assert receipt.signature
    assert not store.get_hypothesis("tenant-001", "HYP-VOICE-001")
    assert "ANTI_GENERICIZATION_THRESHOLD_FAILED" in receipt.gate_checks[-1]["reasons"]


def test_ca_m052_10_compose_boundary_honors_voice_dna_required_and_blocks_before_hypothesis_storage():
    conn = sqlite3.connect(":memory:")
    store = STORE.CollisionHypothesisStore(conn)
    coordinator = RUNTIME.CollisionHypothesisProgramCoordinator(
        workspace_id="tenant-001",
        store=store,
        state_runtime=RUNTIME.UniversalProgramStateRuntime(),
    )
    coordinator.evaluate_matrix_of_edging(
        workspace_id="tenant-001",
        matrix_id="matrix-001",
        broad_signal="scale",
        hidden_pressure="weak habits compound",
        surviving_edge="systems",
        identity_gap="execution gap",
        audience_reality="teams need clarity",
        desired_recognition="trusted operator",
        smallest_useful_movement="name the system",
    )
    profile = _profile()
    request = _request(profile, synthesized_text="Build systems and unlock your potential. Scale smarter and crush your goals.")
    candidate = RUNTIME.CollisionHypothesisCandidate(
        title="Systems before scale",
        relation_type="ANALOGY",
        audience_id="aud-001",
        audience_tension_ref="tension-001",
        guest_id="subject-001",
        guest_lived_proof_citation="source interview evidence proves systems insight",
        research_signal_id="research-001",
        bridge_statement="The subject's lived system-building principle connects directly to the audience's scale tension.",
        evidence_references=["interview:001"],
        refuting_observation="source evidence contradicts the systems claim",
        disconfirming_testimony="subject testimony denies the stated principle",
        boundary_limitation="principle does not apply outside operating systems",
        voice_dna_request={
            "tenant_id": request.tenant_id,
            "subject_id": request.subject_id,
            "constitution_revision": request.constitution_revision,
            "constitution_content_sha256": request.constitution_content_sha256,
            "profile": profile.as_mapping(),
            "source_segments": [{"speaker_id": segment.speaker_id, "text": segment.text} for segment in request.source_segments],
            "synthesized_segments": [{"speaker_id": segment.speaker_id, "text": segment.text} for segment in request.synthesized_segments],
            "synthesized_quotes": [{"speaker_id": quote.speaker_id, "text": quote.text} for quote in request.synthesized_quotes],
            "source_audio_wav_b64": base64.b64encode(request.source_audio_wav).decode(),
            "synthesized_audio_wav_b64": base64.b64encode(request.synthesized_audio_wav).decode(),
            "generic_style_score": 0.99,
        },
    )

    with pytest.raises(RUNTIME.VoiceDNAGateRejectedError):
        coordinator.compose_hypotheses(
            workspace_id="tenant-001",
            portfolio_id="portfolio-001",
            candidates=[candidate],
            matrix_id="matrix-001",
            voice_dna_required=True,
        )

    assert store.list_hypotheses("tenant-001") == []
    receipts = store.list_evaluation_receipts("tenant-001", portfolio_id="portfolio-001")
    assert len(receipts) == 1
    assert receipts[0].decision == "REJECTED"
