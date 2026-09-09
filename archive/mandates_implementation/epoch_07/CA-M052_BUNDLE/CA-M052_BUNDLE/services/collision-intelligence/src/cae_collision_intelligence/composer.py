"""
composer.py
-----------
Collision Hypothesis Composer intersecting 4 worlds into grounded editorial hypotheses.
"""

from __future__ import annotations

import difflib
import hashlib
import io
import json
import math
import re
import statistics
import struct
import wave
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from .domain import (
    CollisionHypothesis,
    CollisionRelationType,
    FalsificationCondition,
    HeritageCMFEval,
    NoveltyClicheAssessment,
    ObliqueLens,
)
from .errors import (
    TenantMismatchError,
    UngroundedAnalogyError,
)




VOICE_DNA_INVARIANT = "INV-VOICE-001"
VOICE_DNA_MAX_DRIFT_DEFAULT = 0.25
VOICE_DNA_MIN_DISTINCTIVENESS_DEFAULT = 0.65


def _freeze_voice_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_voice_value(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_voice_value(item) for item in value)
    return value


def _thaw_voice_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_voice_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_voice_value(item) for item in value]
    return value


class VoiceDNAGateRejectedError(ValueError):
    """Raised when synthesized expression violates INV-VOICE-001."""

    def __init__(self, message: str, *, report: "VoiceDNAGateReport") -> None:
        super().__init__(message)
        self.report = report


@dataclass(frozen=True, slots=True)
class TranscriptSegment:
    """Authoritative transcript segment with immutable speaker attribution."""

    speaker_id: str
    text: str

    def __post_init__(self) -> None:
        if not self.speaker_id.strip():
            raise ValueError("speaker_id cannot be empty")
        if not self.text.strip():
            raise ValueError("text cannot be empty")


@dataclass(frozen=True, slots=True)
class QuoteSpan:
    """A quote asserted by synthesized output and attributable to one speaker."""

    speaker_id: str
    text: str

    def __post_init__(self) -> None:
        if not self.speaker_id.strip():
            raise ValueError("quote speaker_id cannot be empty")
        if not self.text.strip():
            raise ValueError("quote text cannot be empty")


@dataclass(frozen=True, slots=True)
class VoiceDNAProfile:
    """Tenant/subject-bound immutable Voice DNA extracted from authoritative evidence."""

    tenant_id: str
    subject_id: str
    constitution_revision: int
    constitution_content_sha256: str
    acoustic_dna: Mapping[str, float]
    linguistic_dna: Mapping[str, Any]
    max_drift_score: float = VOICE_DNA_MAX_DRIFT_DEFAULT
    min_distinctiveness_score: float = VOICE_DNA_MIN_DISTINCTIVENESS_DEFAULT

    def __post_init__(self) -> None:
        if not self.tenant_id.strip() or not self.subject_id.strip():
            raise ValueError("tenant_id and subject_id are required")
        if self.constitution_revision < 1:
            raise ValueError("constitution_revision must be positive")
        if not re.fullmatch(r"[0-9a-f]{64}", self.constitution_content_sha256):
            raise ValueError("constitution_content_sha256 must be a SHA-256 hex digest")
        if not 0.0 <= self.max_drift_score <= 1.0:
            raise ValueError("max_drift_score must be within [0, 1]")
        if not 0.0 <= self.min_distinctiveness_score <= 1.0:
            raise ValueError("min_distinctiveness_score must be within [0, 1]")
        object.__setattr__(self, "acoustic_dna", _freeze_voice_value(self.acoustic_dna))
        object.__setattr__(self, "linguistic_dna", _freeze_voice_value(self.linguistic_dna))

    @property
    def binding_sha256(self) -> str:
        payload = {
            "invariant_id": VOICE_DNA_INVARIANT,
            "tenant_id": self.tenant_id,
            "subject_id": self.subject_id,
            "constitution_revision": self.constitution_revision,
            "constitution_content_sha256": self.constitution_content_sha256,
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    def as_mapping(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "subject_id": self.subject_id,
            "constitution_revision": self.constitution_revision,
            "constitution_content_sha256": self.constitution_content_sha256,
            "acoustic_dna": _thaw_voice_value(self.acoustic_dna),
            "linguistic_dna": _thaw_voice_value(self.linguistic_dna),
            "max_drift_score": self.max_drift_score,
            "min_distinctiveness_score": self.min_distinctiveness_score,
            "binding_sha256": self.binding_sha256,
        }


@dataclass(frozen=True, slots=True)
class QuoteDiffResult:
    """Character-exact quote verification result; no paraphrase is considered a match."""

    quote_index: int
    speaker_id: str
    text: str
    exact_match: bool
    attribution_match: bool
    source_segment_index: Optional[int]
    character_diff: str


@dataclass(frozen=True, slots=True)
class VoiceDNAGateReport:
    """Deterministic verification evidence for INV-VOICE-001."""

    invariant_id: str
    tenant_id: str
    subject_id: str
    constitution_revision: int
    constitution_binding_sha256: str
    quote_diffs: Tuple[QuoteDiffResult, ...]
    quote_fidelity_passed: bool
    acoustic_drift_score: float
    linguistic_drift_score: float
    voice_drift_score: float
    distinctiveness_score: float
    generic_style_score: Optional[float]
    accepted: bool
    max_drift_score: float
    min_distinctiveness_score: float
    rejection_reasons: Tuple[str, ...] = field(default_factory=tuple)

    def as_gate_checks(self) -> List[Dict[str, Any]]:
        return [
            {"gate": "QUOTE_CHARACTER_EXACT", "verdict": "PASS" if self.quote_fidelity_passed else "FAIL"},
            {"gate": "VOICE_DRIFT_THRESHOLD", "verdict": "PASS" if self.voice_drift_score <= self.max_drift_score else "FAIL"},
            {"gate": "ANTI_GENERICIZATION", "verdict": "PASS" if self.distinctiveness_score >= self.min_distinctiveness_score else "FAIL"},
        ]


@dataclass(frozen=True, slots=True)
class VoiceDNAVerificationInput:
    """Bounded synthesis input used by the runtime verification boundary."""

    tenant_id: str
    subject_id: str
    constitution_revision: int
    constitution_content_sha256: str
    source_segments: Tuple[TranscriptSegment, ...]
    synthesized_segments: Tuple[TranscriptSegment, ...]
    synthesized_quotes: Tuple[QuoteSpan, ...]
    source_audio_wav: bytes
    synthesized_audio_wav: bytes
    generic_style_score: Optional[float] = None


class VoiceDNAExtractor:
    """Extracts deterministic acoustic and linguistic features using only stdlib primitives."""

    _TOKEN_RE = re.compile(r"\b[\w]+(?:['’\-][\w]+)*\b", re.UNICODE)
    _SENTENCE_RE = re.compile(r"[^.!?]+(?:[.!?]+|$)", re.UNICODE)
    _STOPWORDS = frozenset(
        "a an and are as at be been being but by can could did do does for from had has have he her here him his how i if in into is it its just me might more most my no not of on one only or our she should so some than that the their them then there these they this to was we were what when where which who why will with would you your".split()
    )

    @classmethod
    def extract_linguistic_dna(cls, text: str, *, duration_seconds: Optional[float] = None) -> Dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("text cannot be empty")
        tokens = [token.casefold() for token in cls._TOKEN_RE.findall(text)]
        if not tokens:
            raise ValueError("text contains no lexical tokens")
        sentence_parts = [s.strip() for s in cls._SENTENCE_RE.findall(text) if s.strip()]
        sentence_lengths = [len(cls._TOKEN_RE.findall(s)) for s in sentence_parts] or [len(tokens)]
        counts: Dict[str, int] = {}
        for token in tokens:
            if len(token) >= 5 and token not in cls._STOPWORDS:
                counts[token] = counts.get(token, 0) + 1
        top_terms = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:25]
        total_content = sum(count for _, count in top_terms) or 1
        terminology = {term: round(count / total_content, 6) for term, count in top_terms}
        punctuation = {
            "question_rate": text.count("?") / max(1, len(sentence_parts)),
            "exclamation_rate": text.count("!") / max(1, len(sentence_parts)),
            "comma_rate": text.count(",") / max(1, len(tokens)),
            "semicolon_rate": text.count(";") / max(1, len(tokens)),
            "dash_rate": len(re.findall(r"[-—–]", text)) / max(1, len(tokens)),
        }
        function_words = sum(1 for token in tokens if token in cls._STOPWORDS)
        contractions = sum(1 for token in tokens if "'" in token or "’" in token)
        type_token_ratio = len(set(tokens)) / max(1, len(tokens))
        result: Dict[str, Any] = {
            "token_count": float(len(tokens)),
            "avg_word_length": statistics.mean(len(token) for token in tokens),
            "type_token_ratio": type_token_ratio,
            "function_word_ratio": function_words / max(1, len(tokens)),
            "contraction_ratio": contractions / max(1, len(tokens)),
            "avg_sentence_words": statistics.mean(sentence_lengths),
            "sentence_word_std": statistics.pstdev(sentence_lengths) if len(sentence_lengths) > 1 else 0.0,
            "sentence_count": float(len(sentence_lengths)),
            "terminology": terminology,
            "punctuation": punctuation,
        }
        if duration_seconds is not None:
            if duration_seconds <= 0:
                raise ValueError("duration_seconds must be positive")
            result["speaking_rate_wpm"] = len(tokens) / duration_seconds * 60.0
        return result

    @staticmethod
    def _decode_pcm(raw: bytes, *, sample_width: int, channels: int) -> List[float]:
        if sample_width not in (1, 2, 3, 4):
            raise ValueError("only PCM sample widths 1–4 bytes are supported")
        frame_width = sample_width * channels
        usable = len(raw) - (len(raw) % frame_width)
        samples: List[float] = []
        for offset in range(0, usable, frame_width):
            channel_values: List[float] = []
            for channel in range(channels):
                start = offset + channel * sample_width
                chunk = raw[start : start + sample_width]
                if sample_width == 1:
                    value = chunk[0] - 128
                    scale = 128.0
                elif sample_width == 2:
                    value = struct.unpack("<h", chunk)[0]
                    scale = 32768.0
                elif sample_width == 3:
                    value = int.from_bytes(chunk, byteorder="little", signed=True)
                    scale = 8388608.0
                else:
                    value = struct.unpack("<i", chunk)[0]
                    scale = 2147483648.0
                channel_values.append(value / scale)
            samples.append(sum(channel_values) / len(channel_values))
        return samples

    @classmethod
    def _estimate_pitch(cls, frame: Sequence[float], sample_rate: int) -> float:
        if len(frame) < 64:
            return 0.0
        mean = statistics.mean(frame)
        centered = [sample - mean for sample in frame]
        energy = sum(sample * sample for sample in centered)
        if energy < 1e-8:
            return 0.0
        min_lag = max(2, int(sample_rate / 400))
        max_lag = min(len(centered) // 2, int(sample_rate / 70))
        correlations: List[Tuple[int, float]] = []
        for lag in range(min_lag, max_lag + 1):
            corr = sum(centered[i] * centered[i - lag] for i in range(lag, len(centered)))
            norm = math.sqrt(
                sum(centered[i] * centered[i] for i in range(lag, len(centered)))
                * sum(centered[i - lag] * centered[i - lag] for i in range(lag, len(centered)))
            )
            if norm > 0:
                correlations.append((lag, corr / norm))
        if not correlations:
            return 0.0
        best_lag, best_corr = max(correlations, key=lambda item: item[1])
        if best_corr < 0.35:
            return 0.0
        # Prefer the smallest strong periodic lag to avoid selecting a low-frequency
        # subharmonic when the second/third harmonic has nearly the same autocorrelation.
        strong_lags = [lag for lag, corr in correlations if corr >= max(0.60, best_corr * 0.90)]
        selected_lag = min(strong_lags) if strong_lags else best_lag
        return sample_rate / selected_lag

    @classmethod
    def extract_acoustic_dna(cls, wav_bytes: bytes) -> Dict[str, float]:
        if not wav_bytes:
            raise ValueError("WAV input cannot be empty")
        try:
            with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                sample_rate = wav_file.getframerate()
                frame_count = wav_file.getnframes()
                raw = wav_file.readframes(frame_count)
        except (wave.Error, EOFError) as exc:
            raise ValueError("invalid PCM WAV input") from exc
        if channels < 1 or sample_rate <= 0 or frame_count <= 0:
            raise ValueError("WAV input has no usable audio frames")
        samples = cls._decode_pcm(raw, sample_width=sample_width, channels=channels)
        if not samples:
            raise ValueError("WAV input contains no PCM samples")
        duration_seconds = len(samples) / sample_rate
        rms = math.sqrt(statistics.mean(sample * sample for sample in samples))
        zcr = sum(1 for left, right in zip(samples, samples[1:]) if (left < 0 <= right) or (left >= 0 > right)) / max(1, len(samples) - 1)
        frame_size = min(len(samples), max(512, int(sample_rate * 0.04)))
        step = max(frame_size, int(sample_rate * 0.08))
        pitch_samples: List[float] = []
        start_positions = list(range(0, max(1, len(samples) - frame_size + 1), step))
        if len(start_positions) > 8:
            stride = max(1, len(start_positions) // 8)
            start_positions = start_positions[::stride][:8]
        for start in start_positions:
            pitch = cls._estimate_pitch(samples[start : start + frame_size], sample_rate)
            if pitch > 0:
                pitch_samples.append(pitch)
        return {
            "duration_seconds": duration_seconds,
            "rms_energy": rms,
            "zero_crossing_rate": zcr,
            "pitch_mean_hz": statistics.mean(pitch_samples) if pitch_samples else 0.0,
            "pitch_std_hz": statistics.pstdev(pitch_samples) if len(pitch_samples) > 1 else 0.0,
        }

    @classmethod
    def build_profile(
        cls,
        *,
        tenant_id: str,
        constitution: Any,
        source_segments: Sequence[TranscriptSegment],
        source_audio_wav: bytes,
        max_drift_score: float = VOICE_DNA_MAX_DRIFT_DEFAULT,
        min_distinctiveness_score: float = VOICE_DNA_MIN_DISTINCTIVENESS_DEFAULT,
    ) -> VoiceDNAProfile:
        if not source_segments:
            raise ValueError("at least one source transcript segment is required")
        subject_id = str(getattr(constitution, "subject_id", "")).strip()
        revision = int(getattr(constitution, "revision", 0))
        content_sha256 = str(getattr(constitution, "content_sha256", "")).lower()
        if not subject_id or revision < 1 or not content_sha256:
            raise ValueError("constitution must expose subject_id, revision, and content_sha256")
        combined_text = " ".join(segment.text for segment in source_segments)
        duration = cls.extract_acoustic_dna(source_audio_wav)["duration_seconds"]
        linguistic = cls.extract_linguistic_dna(combined_text, duration_seconds=duration)
        acoustic = cls.extract_acoustic_dna(source_audio_wav)
        return VoiceDNAProfile(
            tenant_id=tenant_id,
            subject_id=subject_id,
            constitution_revision=revision,
            constitution_content_sha256=content_sha256,
            acoustic_dna=acoustic,
            linguistic_dna=linguistic,
            max_drift_score=max_drift_score,
            min_distinctiveness_score=min_distinctiveness_score,
        )


class SubjectVoiceDNAVerifier:
    """Fail-closed Voice DNA verifier for immutable Subject Constitution-bound synthesis."""

    _ACOUSTIC_SCALES = {
        "pitch_mean_hz": 80.0,
        "pitch_std_hz": 40.0,
        "rms_energy": 0.12,
        "zero_crossing_rate": 0.08,
    }
    _LINGUISTIC_SCALES = {
        "avg_word_length": 2.0,
        "type_token_ratio": 0.25,
        "function_word_ratio": 0.15,
        "contraction_ratio": 0.10,
        "avg_sentence_words": 6.0,
        "sentence_word_std": 5.0,
        "speaking_rate_wpm": 35.0,
    }

    @staticmethod
    def _numeric_distance(expected: float, actual: float, scale: float) -> float:
        return min(1.0, abs(float(expected) - float(actual)) / max(scale, 1e-9))

    @classmethod
    def _compare_acoustic(cls, expected: Mapping[str, float], actual: Mapping[str, float]) -> float:
        distances = []
        for name, scale in cls._ACOUSTIC_SCALES.items():
            if name not in expected or name not in actual:
                return 1.0
            distances.append(cls._numeric_distance(expected[name], actual[name], scale))
        return statistics.mean(distances) if distances else 1.0

    @classmethod
    def _compare_linguistic(cls, expected: Mapping[str, Any], actual: Mapping[str, Any]) -> Tuple[float, float]:
        distances = []
        for name, scale in cls._LINGUISTIC_SCALES.items():
            if name not in expected or name not in actual:
                return 1.0, 0.0
            distances.append(cls._numeric_distance(float(expected[name]), float(actual[name]), scale))

        expected_terms = set(dict(expected.get("terminology", {})))
        actual_terms = set(dict(actual.get("terminology", {})))
        terminology_overlap = len(expected_terms & actual_terms) / max(1, len(expected_terms | actual_terms))

        expected_punct = dict(expected.get("punctuation", {}))
        actual_punct = dict(actual.get("punctuation", {}))
        punctuation_distances = [
            cls._numeric_distance(float(expected_punct.get(name, 0.0)), float(actual_punct.get(name, 0.0)), scale)
            for name, scale in {
                "question_rate": 0.10,
                "exclamation_rate": 0.10,
                "comma_rate": 0.08,
                "semicolon_rate": 0.05,
                "dash_rate": 0.05,
            }.items()
        ]
        distances.extend(punctuation_distances)
        drift = statistics.mean(distances) if distances else 1.0
        distinctiveness = 0.75 * terminology_overlap + 0.15 * (1.0 - statistics.mean(distances[:2])) + 0.10 * (1.0 - statistics.mean(punctuation_distances))
        return drift, max(0.0, min(1.0, distinctiveness))

    @staticmethod
    def _quote_diff(source_segments: Sequence[TranscriptSegment], quotes: Sequence[QuoteSpan]) -> Tuple[QuoteDiffResult, ...]:
        results: List[QuoteDiffResult] = []
        for index, quote in enumerate(quotes):
            match_index: Optional[int] = None
            attribution_match = False
            for segment_index, segment in enumerate(source_segments):
                if quote.speaker_id == segment.speaker_id and match_index is None:
                    match_index = segment_index
                    attribution_match = True
                if quote.text in segment.text and quote.speaker_id == segment.speaker_id:
                    match_index = segment_index
                    attribution_match = True
                    break
            exact = match_index is not None and attribution_match and quote.text in source_segments[match_index].text
            source_text = source_segments[match_index].text if match_index is not None else ""
            diff = "" if exact else "\n".join(
                difflib.ndiff(list(source_text or "<no matching source span>"), list(quote.text))
            )
            results.append(
                QuoteDiffResult(
                    quote_index=index,
                    speaker_id=quote.speaker_id,
                    text=quote.text,
                    exact_match=exact,
                    attribution_match=attribution_match,
                    source_segment_index=match_index,
                    character_diff=diff,
                )
            )
        return tuple(results)

    @classmethod
    def verify(
        cls,
        *,
        profile: VoiceDNAProfile,
        request: VoiceDNAVerificationInput,
        synthesized_audio_dna: Optional[Mapping[str, float]] = None,
        synthesized_linguistic_dna: Optional[Mapping[str, Any]] = None,
    ) -> VoiceDNAGateReport:
        if request.tenant_id != profile.tenant_id or request.subject_id != profile.subject_id:
            raise VoiceDNAGateRejectedError(
                "Voice DNA tenant/subject binding mismatch",
                report=VoiceDNAGateReport(
                    invariant_id=VOICE_DNA_INVARIANT,
                    tenant_id=request.tenant_id,
                    subject_id=request.subject_id,
                    constitution_revision=request.constitution_revision,
                    constitution_binding_sha256=profile.binding_sha256,
                    quote_diffs=tuple(),
                    quote_fidelity_passed=False,
                    acoustic_drift_score=1.0,
                    linguistic_drift_score=1.0,
                    voice_drift_score=1.0,
                    distinctiveness_score=0.0,
                    generic_style_score=request.generic_style_score,
                    accepted=False,
                    max_drift_score=profile.max_drift_score,
                    min_distinctiveness_score=profile.min_distinctiveness_score,
                    rejection_reasons=("TENANT_OR_SUBJECT_BINDING_MISMATCH",),
                ),
            )
        if request.constitution_revision != profile.constitution_revision or request.constitution_content_sha256.lower() != profile.constitution_content_sha256.lower():
            raise VoiceDNAGateRejectedError(
                "Voice DNA constitution revision/content binding mismatch",
                report=VoiceDNAGateReport(
                    invariant_id=VOICE_DNA_INVARIANT,
                    tenant_id=request.tenant_id,
                    subject_id=request.subject_id,
                    constitution_revision=request.constitution_revision,
                    constitution_binding_sha256=profile.binding_sha256,
                    quote_diffs=tuple(),
                    quote_fidelity_passed=False,
                    acoustic_drift_score=1.0,
                    linguistic_drift_score=1.0,
                    voice_drift_score=1.0,
                    distinctiveness_score=0.0,
                    generic_style_score=request.generic_style_score,
                    accepted=False,
                    max_drift_score=profile.max_drift_score,
                    min_distinctiveness_score=profile.min_distinctiveness_score,
                    rejection_reasons=("CONSTITUTION_BINDING_MISMATCH",),
                ),
            )

        quote_diffs = cls._quote_diff(request.source_segments, request.synthesized_quotes)
        quote_pass = bool(quote_diffs) and all(item.exact_match and item.attribution_match for item in quote_diffs)
        actual_audio = dict(synthesized_audio_dna or VoiceDNAExtractor.extract_acoustic_dna(request.synthesized_audio_wav))
        actual_text = " ".join(segment.text for segment in request.synthesized_segments)
        actual_linguistic = dict(synthesized_linguistic_dna or VoiceDNAExtractor.extract_linguistic_dna(actual_text, duration_seconds=actual_audio.get("duration_seconds")))
        acoustic_drift = cls._compare_acoustic(profile.acoustic_dna, actual_audio)
        linguistic_drift, distinctiveness = cls._compare_linguistic(profile.linguistic_dna, actual_linguistic)
        voice_drift = 0.45 * acoustic_drift + 0.55 * linguistic_drift
        reasons: List[str] = []
        if not quote_pass:
            reasons.append("CHARACTER_EXACT_QUOTE_DIFF_FAILED")
        if voice_drift > profile.max_drift_score:
            reasons.append("VOICE_DRIFT_THRESHOLD_EXCEEDED")
        if distinctiveness < profile.min_distinctiveness_score:
            reasons.append("ANTI_GENERICIZATION_THRESHOLD_FAILED")
        report = VoiceDNAGateReport(
            invariant_id=VOICE_DNA_INVARIANT,
            tenant_id=request.tenant_id,
            subject_id=request.subject_id,
            constitution_revision=profile.constitution_revision,
            constitution_binding_sha256=profile.binding_sha256,
            quote_diffs=quote_diffs,
            quote_fidelity_passed=quote_pass,
            acoustic_drift_score=round(acoustic_drift, 6),
            linguistic_drift_score=round(linguistic_drift, 6),
            voice_drift_score=round(voice_drift, 6),
            distinctiveness_score=round(distinctiveness, 6),
            generic_style_score=request.generic_style_score,
            accepted=not reasons,
            max_drift_score=profile.max_drift_score,
            min_distinctiveness_score=profile.min_distinctiveness_score,
            rejection_reasons=tuple(reasons),
        )
        if not report.accepted:
            raise VoiceDNAGateRejectedError(
                "Synthetic expression rejected by INV-VOICE-001: " + ", ".join(report.rejection_reasons),
                report=report,
            )
        return report


class CollisionHypothesisComposer:
    """Composes grounded CollisionHypothesis entities from multi-world inputs."""

    # Overused generic tropes that trigger cliché penalties
    COMMON_CLICHE_TERMS = {
        "10x your",
        "secret hack",
        "game changer",
        "unlock your potential",
        "mindset shift",
        "crush your goals",
        "hustle harder",
    }

    @classmethod
    def evaluate_cliche_risk(cls, text: str, semantic_distance: float = 0.80) -> NoveltyClicheAssessment:
        """Analyze text for overused viral clichés and tropes."""
        lower_text = text.lower()
        trope_hits = [trope for trope in cls.COMMON_CLICHE_TERMS if trope in lower_text]
        
        cliche_risk = min(1.0, len(trope_hits) * 0.40)
        is_quarantined = cliche_risk >= 0.70
        trope_pen = cliche_risk * 0.50

        return NoveltyClicheAssessment(
            semantic_distance_score=semantic_distance,
            cliche_risk_score=cliche_risk,
            trope_penalty=trope_pen,
            is_cliche_quarantined=is_quarantined,
        )

    @classmethod
    def evaluate_heritage_cmf(
        cls,
        surprise: float = 0.75,
        emotion: float = 0.80,
        specificity: float = 0.85,
        ai_slop_risk: float = 0.15,
    ) -> HeritageCMFEval:
        """Calculate OLD CMF viral potential as an advisory signal."""
        # Non-compensable: AI slop risk caps total potential
        base = (surprise * 0.35) + (emotion * 0.35) + (specificity * 0.30)
        slop_multiplier = max(0.10, 1.0 - ai_slop_risk)
        composite = base * slop_multiplier

        return HeritageCMFEval(
            surprise_score=surprise,
            emotion_score=emotion,
            specificity_score=specificity,
            ai_slop_risk=ai_slop_risk,
            composite_viral_potential=round(composite, 3),
        )

    @classmethod
    def compose(
        cls,
        *,
        workspace_id: str,
        title: str,
        relation_type: CollisionRelationType,
        audience_id: str,
        audience_tension_ref: str,
        guest_id: str,
        guest_lived_proof_citation: str,
        research_signal_id: str,
        bridge_statement: str,
        falsification_condition: FalsificationCondition,
        evidence_references: List[str],
        oblique_lens: Optional[ObliqueLens] = None,
        sda_invariant: str = "SDA-INV-001_ACTIVE_TENSION",
        surprise_score: float = 0.80,
        emotion_score: float = 0.80,
        specificity_score: float = 0.85,
    ) -> CollisionHypothesis:
        """Synthesize a complete CollisionHypothesis with 4-world grounding."""
        # Grounding check: Guest lived proof must be substantive
        if not guest_lived_proof_citation or len(guest_lived_proof_citation.strip()) < 10:
            raise UngroundedAnalogyError(
                "Cannot compose CollisionHypothesis: Guest lived proof citation is missing or unsubstantiated."
            )

        novelty_eval = cls.evaluate_cliche_risk(bridge_statement)
        cmf_eval = cls.evaluate_heritage_cmf(
            surprise=surprise_score,
            emotion=emotion_score,
            specificity=specificity_score,
            ai_slop_risk=novelty_eval.cliche_risk_score * 0.8,
        )

        return CollisionHypothesis(
            workspace_id=workspace_id,
            title=title,
            relation_type=relation_type,
            audience_id=audience_id,
            audience_tension_ref=audience_tension_ref,
            guest_id=guest_id,
            guest_lived_proof_citation=guest_lived_proof_citation,
            research_signal_id=research_signal_id,
            sda_invariant=sda_invariant,
            oblique_lens=oblique_lens,
            bridge_statement=bridge_statement,
            evidence_references=evidence_references,
            novelty_assessment=novelty_eval,
            falsification_condition=falsification_condition,
            heritage_eval=cmf_eval,
        )
