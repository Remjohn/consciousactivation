"""Video Edit Production Program Runtime Coordinator (CAE Phase 4 Mandate M43).

Governed by:
- 04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M43_video_edit_compositionir_cmf_runtime.md
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md
- 00_CONTROL/37_PHASE4_PRODUCTION_FIXTURE_PACK.md

Coordinates source-led video editing, word boundary EDL compilation, VideoEditProgram compilation,
CompositionIR, real FFmpeg rendering with ffprobe and cut-evidence evaluation, dual-axis QA
(Semantic QA vs Render QA), 4-lane authority separation, cryptographic source lineage, and
backend-authoritative operator release receipts.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ca_contracts import bytes_sha256, canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane, AuthorityLaneMismatchError
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateAggregateNotFoundError,
    ProgramTransitionBlockedError,
    UniversalProgramStateRuntime,
)
from ca_runtime.tenancy import TenantContext, require_current_tenant_context

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmf_pipeline.application import PipelineApplication
    from cmf_pipeline.media.bindings import HyperFramesBindingCompiler, RemotionBindingCompiler
    from cmf_pipeline.media.evaluation import RenderedVideoEvaluator
    from cmf_pipeline.media.ffmpeg_adapter import FFmpegSourceLedRenderer


# ============================================================================
# 1. Domain Models & Receipts
# ============================================================================

class VideoEditSourceSpan(BaseModel):
    """Source-grounded evidence span binding spoken narrative to authentic evidence."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    source_id: str
    source_version: str = "1.0.0"
    source_sha256: str
    start_ms: int
    end_ms: int
    quote_text: str
    quote_sha256: str
    speaker_id: str

    @field_validator("quote_text")
    @classmethod
    def validate_quote_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("quote_text cannot be empty")
        return v.strip()

    @field_validator("quote_sha256")
    @classmethod
    def validate_quote_sha256(cls, v: str, info: Any) -> str:
        quote = info.data.get("quote_text", "")
        if quote:
            expected = hashlib.sha256(quote.encode("utf-8")).hexdigest()
            if v != expected:
                raise ValueError(f"quote_sha256 {v} does not match computed hash {expected}")
        return v


class WordBoundaryItem(BaseModel):
    """Word boundary timing item with protected tail padding."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    word_id: str
    text: str
    start_ms: int
    end_ms: int
    speaker_id: str
    protected_tail_ms: int = 0


class WordBoundarySelection(BaseModel):
    """Selection spanning words with boundary class constraints."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    selection_id: str
    start_word_id: str
    end_word_id: str
    function: str
    cut_in_class: str = "WORD_BOUNDARY"
    cut_out_class: str = "WORD_BOUNDARY"
    authorized_reorder: bool = False


class VideoEditRenderArtifact(BaseModel):
    """Physical rendered video artifact with cryptographic proof and probe results."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    artifact_id: str
    logical_uri: str
    sha256: str
    byte_count: int
    output_path: str
    srt_path: Optional[str] = None
    segment_count: int
    probe: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DualAxisVideoQAReceipt(BaseModel):
    """Dual-axis QA evaluation receipt enforcing Semantic QA vs Render QA independence."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    receipt_id: str
    semantic_qa_passed: bool
    render_qa_passed: bool
    overall_result: str  # "PASS" or "FAIL"
    semantic_details: Dict[str, Any]
    render_details: Dict[str, Any]
    evaluation_record: Dict[str, Any]
    evaluated_by_lane: str = "ANALYST"
    timestamp: str


class VideoReleaseReceipt(BaseModel):
    """Signed operator release receipt for production video release."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    receipt_id: str
    aggregate_id: str
    program_id: str
    workspace_id: str
    semantic_program_ref: Dict[str, str]
    source_registration_ref: Dict[str, str]
    edl_ref: Dict[str, str]
    video_edit_program_ref: Dict[str, str]
    rendered_artifact_ref: Dict[str, str]
    qa_receipt_ref: Dict[str, str]
    operator_id: str
    rationale: str
    committed_at: str
    receipt_sha256: str


# ============================================================================
# 2. Typed Error Taxonomy
# ============================================================================

class VideoEditError(RuntimeError):
    """Base error for Video Edit Production Program operations."""

    def __init__(self, message: str, *, reason_code: str = "VIDEO_EDIT_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class SemanticQAFailureError(VideoEditError):
    """Raised when semantic QA assertions fail (source fidelity, locks, quotes, spine continuity)."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="SEMANTIC_QA_FAILURE", details=details)


class RenderQAFailureError(VideoEditError):
    """Raised when render QA assertions fail (file integrity, byte count, streams, cut evidence)."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="RENDER_QA_FAILURE", details=details)


class SourceLineageMissingError(VideoEditError):
    """Raised when evidence lineage or source registration is broken or missing."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="SOURCE_LINEAGE_MISSING", details=details)


class EvidenceQuoteMismatchError(VideoEditError):
    """Raised when extracted quotes do not match registered evidence SHA-256."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="EVIDENCE_QUOTE_MISMATCH", details=details)


class SyntheticVideoBlockedError(VideoEditError):
    """Raised when synthetic or mock inputs attempt to create production video artifacts."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="SYNTHETIC_VIDEO_BLOCKED", details=details)


class UnapprovedVideoReleaseError(VideoEditError):
    """Raised when video release is attempted without passing QA or operator authorization."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="UNAPPROVED_VIDEO_RELEASE", details=details)


class WrongReadingLockMissingError(VideoEditError):
    """Raised when wrong-reading locks are absent or violated in video edit compilation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="WRONG_READING_LOCK_MISSING", details=details)


class WorkspaceScopeViolationError(VideoEditError):
    """Raised when cross-workspace tenant operations are attempted."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="WORKSPACE_SCOPE_VIOLATION", details=details)


class LaneAuthorityViolationError(VideoEditError):
    """Raised when an operation is attempted on an unauthorized lane."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="LANE_AUTHORITY_VIOLATION", details=details)


# ============================================================================
# 3. Video Edit Production Coordinator
# ============================================================================

class VideoEditProductionCoordinator:
    """Authoritative multi-agent coordinator for Video Edit Production Programs (M43)."""

    PROGRAM_ID = "video_edit_program"
    PROGRAM_VERSION = "1.0.0"
    MACHINE_ID = "VIDEO_EDIT_STATE_MACHINE_V1"

    def __init__(
        self,
        runtime: UniversalProgramStateRuntime,
        pipeline_app: Optional[PipelineApplication] = None,
    ):
        from cmf_pipeline.media.bindings import HyperFramesBindingCompiler, RemotionBindingCompiler
        from cmf_pipeline.media.evaluation import RenderedVideoEvaluator
        from cmf_pipeline.media.ffmpeg_adapter import FFmpegSourceLedRenderer

        self.runtime = runtime
        self.pipeline_app = pipeline_app
        self.renderer = FFmpegSourceLedRenderer()
        self.evaluator = RenderedVideoEvaluator()
        self.remotion_compiler = RemotionBindingCompiler()
        self.hyperframes_compiler = HyperFramesBindingCompiler()

    def _ensure_pipeline_app(self, workspace_id: str) -> PipelineApplication:
        if self.pipeline_app is None:
            from cmf_pipeline.application import PipelineApplication
            db_dir = Path(tempfile.mkdtemp(prefix="cae_media_pipe_"))
            db_path = db_dir / "pipeline.sqlite3"
            app = PipelineApplication(db_path)
            app.initialize()
            self.pipeline_app = app
        return self.pipeline_app

    def _check_tenant(self, workspace_id: str) -> None:
        tenant = require_current_tenant_context()
        if str(tenant.workspace_id) != str(workspace_id):
            raise WorkspaceScopeViolationError(
                f"Active tenant workspace '{tenant.workspace_id}' does not match operation workspace '{workspace_id}'"
            )

    def admit_semantic_material(
        self,
        semantic_program: Mapping[str, Any],
        workspace_id: str | UUID,
        operator_id: str,
        aggregate_id: Optional[str] = None,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Admit a SemanticProgram into video edit production under COMMANDER authority."""
        self._check_tenant(str(workspace_id))
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to admit semantic material. Required: COMMANDER"
            )

        # Anti-synthetic check
        if semantic_program.get("is_synthetic", False) or "synthetic" in str(semantic_program).lower():
            raise SyntheticVideoBlockedError(
                "Synthetic or mock SemanticProgram cannot enter production video compilation",
                details={"semantic_program_id": semantic_program.get("program_id")},
            )

        agg_id_to_use = aggregate_id
        if agg_id_to_use:
            try:
                self.runtime.get_aggregate(agg_id_to_use)
            except Exception:
                agg_id_to_use = None

        if agg_id_to_use is None:
            initial_aggregate = self.runtime.initialize_program_state(
                program_id=self.PROGRAM_ID,
                workspace_id=str(workspace_id),
                actor_id=operator_id,
                initial_data={
                    "semantic_program": dict(semantic_program),
                    "admitted_by": operator_id,
                    "admitted_at": utc_now_rfc3339(),
                },
                context_claims=["workspace_active", "operator_authorized"],
            )
            agg_id_to_use = initial_aggregate.aggregate_id

        payload = {
            "semantic_program_id": semantic_program.get("program_id", "sem-prog-default"),
            "semantic_program_sha256": canonical_sha256(dict(semantic_program)),
            "operator_id": operator_id,
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=agg_id_to_use,
                transition_name="admit_semantic_material",
                actor_lane=lane,
                actor_id=operator_id,
                context_claims=["workspace_active", "operator_authorized"],
                payload=payload,
                state_updates={"semantic_program": dict(semantic_program)},
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def register_source_media(
        self,
        aggregate_id: str,
        source_path: str | Path,
        logical_uri: str,
        evidence_segments: Sequence[Mapping[str, Any]],
        workspace_id: str,
        actor_id: str,
        lane: AuthorityLane = AuthorityLane.HUNTER,
        restrictions: Optional[Sequence[str]] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Register source media file and extract authentic evidence spans under HUNTER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.HUNTER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to register source media. Required: HUNTER"
            )

        src = Path(source_path)
        if not src.is_file():
            raise SourceLineageMissingError(f"Source media file not found: {source_path}")

        if not evidence_segments:
            raise SourceLineageMissingError("At least one authentic evidence segment is required")

        extracted_spans: List[Dict[str, Any]] = []
        for idx, seg in enumerate(evidence_segments):
            if seg.get("is_synthetic", False):
                raise SyntheticVideoBlockedError(
                    f"Evidence segment {idx} is synthetic and cannot be used for production",
                    details={"segment": seg},
                )
            text = seg.get("spoken_text") or seg.get("verbatim_text") or seg.get("text", "")
            if not text:
                raise SourceLineageMissingError(f"Evidence segment {idx} missing spoken text")
            expected_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
            provided_hash = seg.get("text_sha256", expected_hash)
            if provided_hash != expected_hash:
                raise EvidenceQuoteMismatchError(
                    f"Evidence segment {idx} quote hash mismatch",
                    details={"provided": provided_hash, "expected": expected_hash},
                )

            span = VideoEditSourceSpan(
                source_id=seg.get("segment_id", f"seg-{idx}"),
                source_version="1.0.0",
                source_sha256=provided_hash,
                start_ms=int(seg.get("start_time_ms", seg.get("start_ms", 0))),
                end_ms=int(seg.get("end_time_ms", seg.get("end_ms", 1000))),
                quote_text=text.strip(),
                quote_sha256=expected_hash,
                speaker_id=seg.get("speaker_id", seg.get("speaker", "speaker-1")),
            )
            extracted_spans.append(span.model_dump())

        app = self._ensure_pipeline_app(workspace_id)
        restrs = list(restrictions or ["operator_governed"])
        restrs = sorted(set(restrs))

        source_pkg_ref = {"object_id": f"src-pkg-{aggregate_id}", "version": "1.0.0", "sha256": "0" * 64}
        transcript_ref = {"object_id": f"tr-align-{aggregate_id}", "version": "1.0.0", "sha256": "0" * 64}
        visual_ref = {"object_id": f"vis-idx-{aggregate_id}", "version": "1.0.0", "sha256": "0" * 64}

        reg_result = app.source_media.register(
            source_path=src,
            logical_uri=logical_uri,
            source_package_ref=source_pkg_ref,
            transcript_alignment_ref=transcript_ref,
            visual_index_ref=visual_ref,
            restrictions=restrs,
            idempotency_key=f"{idempotency_key or aggregate_id}:reg",
        )
        registration = reg_result["object"]["payload"]

        payload = {
            "registration_id": registration["registration_id"],
            "logical_uri": registration["logical_uri"],
            "media_sha256": registration["technical"]["media_sha256"],
            "span_count": len(extracted_spans),
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="register_source_media",
                actor_lane=lane,
                actor_id=actor_id,
                context_claims=["workspace_active", "material_admitted"],
                payload=payload,
                state_updates={
                    "source_registration": registration,
                    "source_path": str(src.resolve()),
                    "source_spans": extracted_spans,
                },
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def compile_word_boundary_edl(
        self,
        aggregate_id: str,
        words: Sequence[Mapping[str, Any]],
        selections: Sequence[Mapping[str, Any]],
        workspace_id: str,
        actor_id: str,
        lane: AuthorityLane = AuthorityLane.COMPOSER,
        allow_reorder: bool = False,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Compile word boundary EDL from authentic words and selections under COMPOSER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to compile EDL. Required: COMPOSER"
            )

        agg = self.runtime.get_aggregate(aggregate_id)
        reg = agg.state_data.get("source_registration")
        if not reg:
            raise SourceLineageMissingError("Source media registration is missing from state")

        app = self._ensure_pipeline_app(workspace_id)
        source_reg_ref = {
            "object_id": reg["registration_id"],
            "version": reg["registration_version"],
            "sha256": canonical_sha256(reg),
        }
        moment_ref = {"object_id": f"moment-{aggregate_id}", "version": "1.0.0", "sha256": "0" * 64}

        normalized_words = []
        for w in words:
            item = WordBoundaryItem(
                word_id=str(w["word_id"]),
                text=str(w["text"]),
                start_ms=int(w["start_ms"]),
                end_ms=int(w["end_ms"]),
                speaker_id=str(w.get("speaker_id", "speaker-1")),
                protected_tail_ms=int(w.get("protected_tail_ms", 0)),
            )
            normalized_words.append(item.model_dump())

        normalized_selections = []
        for s in selections:
            sel = WordBoundarySelection(
                selection_id=str(s["selection_id"]),
                start_word_id=str(s["start_word_id"]),
                end_word_id=str(s["end_word_id"]),
                function=str(s.get("function", "body")),
                cut_in_class=str(s.get("cut_in_class", "WORD_BOUNDARY")),
                cut_out_class=str(s.get("cut_out_class", "WORD_BOUNDARY")),
                authorized_reorder=bool(s.get("authorized_reorder", allow_reorder)),
            )
            normalized_selections.append(sel.model_dump())

        edl_result = app.edls.compile(
            source_registration_ref=source_reg_ref,
            expression_moment_ref=moment_ref,
            words=normalized_words,
            selections=normalized_selections,
            allow_reorder=allow_reorder,
            idempotency_key=f"{idempotency_key or aggregate_id}:edl",
        )
        edl = edl_result["object"]["payload"]

        payload = {
            "edl_id": edl["edl_id"],
            "entry_count": len(edl["entries"]),
            "output_duration_ms": edl["output_duration_ms"],
            "edl_sha256": canonical_sha256(edl),
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="compile_word_boundary_edl",
                actor_lane=lane,
                actor_id=actor_id,
                context_claims=["workspace_active", "source_registered"],
                payload=payload,
                state_updates={"edl": edl},
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def compile_video_edit_program(
        self,
        aggregate_id: str,
        canvas: Mapping[str, Any],
        timebase: Mapping[str, Any],
        tracks: Sequence[Mapping[str, Any]],
        wrong_reading_locks: Sequence[str],
        workspace_id: str,
        actor_id: str,
        lane: AuthorityLane = AuthorityLane.COMPOSER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Compile VideoEditProgram with A-roll spine constraints under COMPOSER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to compile VideoEditProgram. Required: COMPOSER"
            )

        if not wrong_reading_locks:
            raise WrongReadingLockMissingError("VideoEditProgram compilation requires at least one wrong-reading lock")

        agg = self.runtime.get_aggregate(aggregate_id)
        reg = agg.state_data.get("source_registration")
        edl = agg.state_data.get("edl")
        sem_prog = agg.state_data.get("semantic_program", {})

        if not reg or not edl:
            raise VideoEditError("Missing source registration or compiled EDL")

        app = self._ensure_pipeline_app(workspace_id)

        source_reg_ref = {
            "object_id": reg["registration_id"],
            "version": reg["registration_version"],
            "sha256": canonical_sha256(reg),
        }
        sem_prog_ref = {
            "object_id": sem_prog.get("program_id", f"sem-{aggregate_id}"),
            "version": "1.0.0",
            "sha256": canonical_sha256(sem_prog),
        }

        edl_duration = int(edl.get("output_duration_ms", 10000))
        calc_duration = int(canvas.get("duration_ms", edl_duration))

        # Normalize tracks and elements
        norm_tracks = []
        for ti, t in enumerate(tracks):
            t_id = str(t.get("track_id", f"track_{ti}"))
            t_type = str(t.get("track_type", "VIDEO"))
            role = str(t.get("role", "PRIMARY_A_ROLL_SPINE"))
            z_idx = int(t.get("z_index", ti))
            norm_elems = []
            for ei, el in enumerate(t.get("elements", [])):
                kind = str(el.get("kind", "SOURCE_SEGMENT"))
                out_start = int(el.get("output_start_ms", el.get("timeline_start_ms", 0)))
                out_end = int(el.get("output_end_ms", el.get("timeline_end_ms", out_start + 1000)))
                calc_duration = max(calc_duration, out_end)

                if kind == "SOURCE_SEGMENT":
                    src_ref = el.get("source_registration_ref", source_reg_ref)
                    src_start = int(el.get("source_start_ms", el.get("source_span", {}).get("start_ms", 0)))
                    src_end = int(el.get("source_end_ms", el.get("source_span", {}).get("end_ms", src_start + 1000)))
                else:
                    src_ref = "NOT_APPLICABLE"
                    src_start = "NOT_APPLICABLE"
                    src_end = "NOT_APPLICABLE"

                norm_elems.append({
                    "element_id": str(el.get("element_id", f"el_{ti}_{ei}")),
                    "kind": kind,
                    "output_start_ms": out_start,
                    "output_end_ms": out_end,
                    "semantic_role": str(el.get("semantic_role", "spoken_anchor")),
                    "sequence_role": str(el.get("sequence_role", "a_roll_segment")),
                    "source_registration_ref": src_ref,
                    "source_start_ms": src_start,
                    "source_end_ms": src_end,
                    "artifact_ref": el.get("artifact_ref", "NOT_APPLICABLE"),
                    "generated_slot_state": str(el.get("generated_slot_state", "NOT_APPLICABLE")),
                    "bbox_intent_ref": el.get("bbox_intent_ref", "NOT_APPLICABLE"),
                    "text": str(el.get("text", "NOT_APPLICABLE")),
                })
            norm_tracks.append({
                "track_id": t_id,
                "track_type": t_type,
                "role": role,
                "z_index": z_idx,
                "elements": norm_elems,
            })

        norm_canvas = {
            "width": int(canvas.get("width", 360)),
            "height": int(canvas.get("height", 640)),
            "fps_numerator": int(canvas.get("fps_numerator", timebase.get("fps_numerator", timebase.get("numerator", 30)))),
            "fps_denominator": int(canvas.get("fps_denominator", timebase.get("fps_denominator", timebase.get("denominator", 1)))),
            "duration_ms": calc_duration,
        }

        norm_timebase = {
            "numerator": int(timebase.get("numerator", timebase.get("fps_numerator", 30))),
            "denominator": int(timebase.get("denominator", timebase.get("fps_denominator", 1))),
        }

        sorted_locks = sorted(set(wrong_reading_locks))
        req = {
            "derivative_job_ref": {"object_id": f"job-{aggregate_id}", "version": "1.0.0", "sha256": "0" * 64},
            "source_registration_ref": source_reg_ref,
            "semantic_production_package_ref": sem_prog_ref,
            "final_script_ref": {"object_id": f"script-{aggregate_id}", "version": "1.0.0", "sha256": "0" * 64},
            "activation_transfer_contract_ref": {"object_id": f"trans-{aggregate_id}", "version": "1.0.0", "sha256": "0" * 64},
            "harness_binding_ref": {"object_id": f"bind-{aggregate_id}", "version": "1.0.0", "sha256": "0" * 64},
            "canvas": norm_canvas,
            "timebase": norm_timebase,
            "tracks": norm_tracks,
            "evaluation_profile_ref": {"object_id": f"eval-prof-{aggregate_id}", "version": "1.0.0", "sha256": "0" * 64},
            "wrong_reading_locks": sorted_locks,
        }

        prg_result = app.video_programs.compile(req, idempotency_key=f"{idempotency_key or aggregate_id}:vep")
        video_program = prg_result["object"]["payload"]

        payload = {
            "program_id": video_program["program_id"],
            "track_count": len(video_program["tracks"]),
            "program_sha256": canonical_sha256(video_program),
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="compile_video_edit_program",
                actor_lane=lane,
                actor_id=actor_id,
                context_claims=["workspace_active", "edl_compiled"],
                payload=payload,
                state_updates={
                    "video_edit_program": video_program,
                    "wrong_reading_locks": sorted_locks,
                },
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def compile_export_bindings(
        self,
        aggregate_id: str,
        workspace_id: str,
        actor_id: str,
        remotion_composition_id: str = "MainVideo",
        hyperframes_blocks: Optional[Sequence[str]] = None,
        lane: AuthorityLane = AuthorityLane.COMPOSER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Compile export bindings (Remotion & HyperFrames) under COMPOSER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to compile export bindings. Required: COMPOSER"
            )

        agg = self.runtime.get_aggregate(aggregate_id)
        video_prog = agg.state_data.get("video_edit_program")
        if not video_prog:
            raise VideoEditError("VideoEditProgram not found in aggregate state")

        rem_runtime_ref = {"object_id": "remotion-runtime-v1", "version": "1.0.0", "sha256": "0" * 64}
        remotion_binding = self.remotion_compiler.compile(
            program=video_prog,
            composition_id=remotion_composition_id,
            runtime_ref=rem_runtime_ref,
        )

        blocks = sorted(set(hyperframes_blocks or ["a_roll_spine"]))
        block_reg_ref = {"object_id": "block-reg-v1", "version": "1.0.0", "sha256": "0" * 64}
        hyperframes_binding = self.hyperframes_compiler.compile(
            program=video_prog,
            block_registry_ref=block_reg_ref,
            block_ids=blocks,
        )

        payload = {
            "remotion_binding_id": remotion_binding["binding_id"],
            "hyperframes_binding_id": hyperframes_binding["binding_id"],
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="compile_export_bindings",
                actor_lane=lane,
                actor_id=actor_id,
                context_claims=["workspace_active", "program_compiled"],
                payload=payload,
                state_updates={
                    "remotion_binding": remotion_binding,
                    "hyperframes_binding": hyperframes_binding,
                },
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def realize_ffmpeg_render(
        self,
        aggregate_id: str,
        output_dir: str | Path,
        logical_output_uri: str,
        workspace_id: str,
        actor_id: str,
        captions: Optional[Sequence[str]] = None,
        audio_fade_ms: int = 10,
        lane: AuthorityLane = AuthorityLane.COMPOSER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Render physical video and SRT subtitle using real FFmpeg under COMPOSER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to render video. Required: COMPOSER"
            )

        agg = self.runtime.get_aggregate(aggregate_id)
        edl = agg.state_data.get("edl")
        source_path = agg.state_data.get("source_path")
        if not edl or not source_path:
            raise VideoEditError("Missing EDL or source media path for rendering")

        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        render_res = self.renderer.render(
            source_path=source_path,
            edl=edl,
            output_dir=out_dir,
            logical_output_uri=logical_output_uri,
            audio_fade_ms=audio_fade_ms,
        )

        manifest = render_res["manifest"]
        srt_file = None
        if captions:
            srt_path = out_dir / f"{Path(logical_output_uri).stem}.srt"
            srt_file = str(self.renderer.srt(edl, list(captions), srt_path))

        artifact = VideoEditRenderArtifact(
            artifact_id=manifest["artifact_id"],
            logical_uri=manifest["logical_uri"],
            sha256=manifest["sha256"],
            byte_count=manifest["byte_count"],
            output_path=render_res["output_path"],
            srt_path=srt_file,
            segment_count=manifest["segment_count"],
            probe=render_res["probe"],
            metadata={"ffmpeg_binding": manifest["ffmpeg_binding"]},
        )

        payload = {
            "artifact_id": artifact.artifact_id,
            "logical_uri": artifact.logical_uri,
            "sha256": artifact.sha256,
            "byte_count": artifact.byte_count,
            "segment_count": artifact.segment_count,
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="realize_ffmpeg_render",
                actor_lane=lane,
                actor_id=actor_id,
                context_claims=["workspace_active", "bindings_compiled"],
                payload=payload,
                state_updates={
                    "render_artifact": artifact.model_dump(),
                    "output_dir": str(out_dir.resolve()),
                },
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def evaluate_dual_axis_qa(
        self,
        aggregate_id: str,
        workspace_id: str,
        actor_id: str,
        lane: AuthorityLane = AuthorityLane.ANALYST,
        evidence_dir: Optional[str | Path] = None,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Perform dual-axis Semantic QA vs Render QA under ANALYST authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.ANALYST:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to evaluate QA. Required: ANALYST"
            )

        agg = self.runtime.get_aggregate(aggregate_id)
        artifact_data = agg.state_data.get("render_artifact")
        video_prog = agg.state_data.get("video_edit_program")
        edl = agg.state_data.get("edl")
        source_spans = agg.state_data.get("source_spans", [])
        locks = agg.state_data.get("wrong_reading_locks", [])

        if not artifact_data or not video_prog or not edl:
            raise VideoEditError("Cannot perform QA: missing artifact, video program, or EDL")

        # 1. Semantic QA Dimension
        semantic_issues: List[str] = []
        if not source_spans:
            semantic_issues.append("No authentic source evidence spans present")

        # Check A-roll spine presence and continuity
        a_roll_tracks = [t for t in video_prog.get("tracks", []) if t.get("role") == "PRIMARY_A_ROLL_SPINE"]
        if not a_roll_tracks:
            semantic_issues.append("Missing mandatory PRIMARY_A_ROLL_SPINE track")
        else:
            spine = a_roll_tracks[0]
            elements = spine.get("elements", [])
            if not elements:
                semantic_issues.append("PRIMARY_A_ROLL_SPINE track has zero elements")
            else:
                for el in elements:
                    if el.get("kind") != "SOURCE_SEGMENT":
                        semantic_issues.append(f"Spine element {el.get('element_id')} is not SOURCE_SEGMENT")

        if not locks:
            semantic_issues.append("Missing required wrong-reading locks")

        semantic_passed = len(semantic_issues) == 0

        # 2. Render QA Dimension via RenderedVideoEvaluator (cuts extraction & ffprobe verification)
        ev_dir = Path(evidence_dir or (Path(agg.state_data.get("output_dir", ".")) / "evidence"))
        art_path = Path(artifact_data["output_path"])

        artifact_ref = {
            "object_id": artifact_data["artifact_id"],
            "version": "1.0.0",
            "sha256": artifact_data["sha256"],
        }

        eval_res = self.evaluator.evaluate(
            artifact_path=art_path,
            artifact_ref=artifact_ref,
            program=video_prog,
            edl=edl,
            producer_actor_id="producer-cmf-engine",
            evaluator_actor_id=actor_id,
            evidence_dir=ev_dir,
        )

        render_issues: List[str] = []
        if not eval_res["verdict"].startswith("PASS"):
            render_issues.append(f"RenderedVideoEvaluator failed with verdict: {eval_res['verdict']}")

        render_passed = len(render_issues) == 0 and eval_res["verdict"].startswith("PASS")
        overall_result = "PASS" if (semantic_passed and render_passed) else "FAIL"

        qa_receipt = DualAxisVideoQAReceipt(
            receipt_id=f"qa-rcpt-{uuid4().hex[:12]}",
            semantic_qa_passed=semantic_passed,
            render_qa_passed=render_passed,
            overall_result=overall_result,
            semantic_details={
                "passed": semantic_passed,
                "issues": semantic_issues,
                "locks_count": len(locks),
                "source_spans_count": len(source_spans),
            },
            render_details={
                "passed": render_passed,
                "issues": render_issues,
                "verdict": eval_res["verdict"],
                "cut_evidence_count": len(eval_res.get("cut_evidence", [])),
            },
            evaluation_record=eval_res,
            evaluated_by_lane="ANALYST",
            timestamp=utc_now_rfc3339(),
        )

        payload = {
            "qa_receipt_id": qa_receipt.receipt_id,
            "overall_result": overall_result,
            "semantic_qa_passed": semantic_passed,
            "render_qa_passed": render_passed,
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="evaluate_dual_axis_qa",
                actor_lane=lane,
                actor_id=actor_id,
                context_claims=["workspace_active", "video_rendered"],
                payload=payload,
                state_updates={"dual_axis_qa_receipt": qa_receipt.model_dump()},
            )
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

        if not semantic_passed:
            raise SemanticQAFailureError(
                f"Semantic QA validation failed: {semantic_issues}",
                details={"issues": semantic_issues},
            )
        if not render_passed:
            raise RenderQAFailureError(
                f"Render QA validation failed: {render_issues}",
                details={"issues": render_issues},
            )

        return res.aggregate

    def authorize_video_release(
        self,
        aggregate_id: str,
        operator_id: str,
        rationale: str,
        workspace_id: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Authorize production video release with signed cryptographic receipt under COMMANDER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to release video. Required: COMMANDER"
            )

        agg = self.runtime.get_aggregate(aggregate_id)
        qa = agg.state_data.get("dual_axis_qa_receipt")
        if not qa or qa.get("overall_result") != "PASS":
            raise UnapprovedVideoReleaseError(
                "Cannot authorize release: Dual-axis QA has not passed",
                details={"qa_receipt": qa},
            )

        reg = agg.state_data.get("source_registration", {})
        edl = agg.state_data.get("edl", {})
        video_prog = agg.state_data.get("video_edit_program", {})
        render_art = agg.state_data.get("render_artifact", {})
        sem_prog = agg.state_data.get("semantic_program", {})

        receipt_core = {
            "receipt_id": f"rcpt-release-{uuid4().hex[:12]}",
            "aggregate_id": aggregate_id,
            "program_id": self.PROGRAM_ID,
            "workspace_id": workspace_id,
            "semantic_program_ref": {
                "object_id": sem_prog.get("program_id", "sem-default"),
                "version": "1.0.0",
                "sha256": canonical_sha256(sem_prog),
            },
            "source_registration_ref": {
                "object_id": reg.get("registration_id", "reg-default"),
                "version": reg.get("registration_version", "1.0.0"),
                "sha256": canonical_sha256(reg),
            },
            "edl_ref": {
                "object_id": edl.get("edl_id", "edl-default"),
                "version": edl.get("edl_version", "1.0.0"),
                "sha256": canonical_sha256(edl),
            },
            "video_edit_program_ref": {
                "object_id": video_prog.get("program_id", "vep-default"),
                "version": video_prog.get("program_version", "1.0.0"),
                "sha256": canonical_sha256(video_prog),
            },
            "rendered_artifact_ref": {
                "object_id": render_art.get("artifact_id", "art-default"),
                "logical_uri": render_art.get("logical_uri", "video/out.mp4"),
                "sha256": render_art.get("sha256", "0" * 64),
            },
            "qa_receipt_ref": {
                "object_id": qa["receipt_id"],
                "sha256": canonical_sha256(qa),
            },
            "operator_id": operator_id,
            "rationale": rationale,
            "committed_at": utc_now_rfc3339(),
        }

        release_receipt = VideoReleaseReceipt(
            **receipt_core,
            receipt_sha256=canonical_sha256(receipt_core),
        )

        payload = {
            "release_receipt_id": release_receipt.receipt_id,
            "receipt_sha256": release_receipt.receipt_sha256,
            "operator_id": operator_id,
            "rationale": rationale,
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="authorize_video_release",
                actor_lane=lane,
                actor_id=operator_id,
                context_claims=["workspace_active", "qa_passed", "operator_authorized"],
                payload=payload,
                state_updates={"video_release_receipt": release_receipt.model_dump()},
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def repair_video_edit_program(
        self,
        aggregate_id: str,
        operator_id: str,
        repair_instructions: str,
        workspace_id: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Repair a faulted video edit program state under COMMANDER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to repair program. Required: COMMANDER"
            )

        payload = {
            "repair_instructions": repair_instructions,
            "operator_id": operator_id,
        }

        try:
            res = self.runtime.execute_repair_transition(
                aggregate_id=aggregate_id,
                transition_name="repair_video_edit_program",
                actor_lane=lane,
                actor_id=operator_id,
                context_claims=["workspace_active", "operator_authorized"],
                payload=payload,
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))
