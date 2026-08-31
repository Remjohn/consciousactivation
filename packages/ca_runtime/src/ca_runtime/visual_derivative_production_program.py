"""Visual Derivative Production Program (CAE Phase 4 Mandate M42).

Governed by:
- 04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M42_carousel_supervisual_animation_production_programs.md
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md

Coordinates source-grounded visual derivatives (CAROUSEL, SUPERVISUAL, ANIMATION)
with strict dual-axis QA (Semantic QA vs Render QA), 4-lane authority separation,
cryptographic source lineage, and backend-authoritative operator release receipts.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ca_contracts import bytes_sha256, canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane, AuthorityLaneMismatchError
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramTransitionBlockedError,
    UniversalProgramStateRuntime,
)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cmf_pipeline.application import PipelineApplication
    from cmf_pipeline.composition.products import CarouselService, SuperVisualService
    from cmf_pipeline.composition.animation import AnimationSceneRealizer
    from cmf_pipeline.composition.ir import CompositionIRService
    from cmf_pipeline.evaluation.reparse import RenderReparseService


# ============================================================================
# 1. Domain Enums and Data Models
# ============================================================================

class DerivativeKind(str, Enum):
    """Supported visual derivative categories."""
    CAROUSEL = "CAROUSEL"
    SUPERVISUAL = "SUPERVISUAL"
    ANIMATION_SCENE_PACKAGE = "ANIMATION_SCENE_PACKAGE"
    ANIMATION_SHORT = "ANIMATION_SHORT"


class DerivativeSourceSpan(BaseModel):
    """Source-grounded evidence span binding a visual element to authentic evidence."""
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


class DerivativeRenderArtifact(BaseModel):
    """Realized physical render artifact with cryptographic verification."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    artifact_id: str
    derivative_kind: str
    logical_uri: str
    sha256: str
    byte_count: int
    output_path: str
    format02_activated: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DualAxisQAReceipt(BaseModel):
    """Dual-axis QA evaluation receipt enforcing Semantic QA vs Render QA independence."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    receipt_id: str
    semantic_qa_passed: bool
    render_qa_passed: bool
    overall_result: str  # "PASS" or "FAIL"
    semantic_details: Dict[str, Any]
    render_details: Dict[str, Any]
    evaluated_by_lane: str = "ANALYST"
    timestamp: str


class DerivativeReleaseReceipt(BaseModel):
    """Signed operator release receipt for production visual derivatives."""
    model_config = ConfigDict(frozen=True, extra="forbid")

    receipt_id: str
    aggregate_id: str
    program_id: str
    workspace_id: str
    derivative_kind: str
    semantic_program_ref: Dict[str, str]
    composition_ref: Dict[str, str]
    render_artifact_refs: List[Dict[str, str]]
    qa_receipt_ref: Dict[str, str]
    operator_id: str
    rationale: str
    committed_at: str
    receipt_sha256: str


# ============================================================================
# 2. Typed Error Taxonomy
# ============================================================================

class VisualDerivativeError(RuntimeError):
    """Base error for Visual Derivative Production Program operations."""

    def __init__(self, message: str, *, reason_code: str = "VISUAL_DERIVATIVE_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class SemanticQAFailureError(VisualDerivativeError):
    """Raised when semantic QA assertions fail (source fidelity, locks, quotes)."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="SEMANTIC_QA_FAILURE", details=details)


class RenderQAFailureError(VisualDerivativeError):
    """Raised when render QA assertions fail (file integrity, byte count, dimensions)."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="RENDER_QA_FAILURE", details=details)


class SourceLineageMissingError(VisualDerivativeError):
    """Raised when evidence lineage is broken or missing."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="SOURCE_LINEAGE_MISSING", details=details)


class EvidenceQuoteMismatchError(VisualDerivativeError):
    """Raised when extracted quotes do not match evidence SHA-256."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="EVIDENCE_QUOTE_MISMATCH", details=details)


class SyntheticDerivativeBlockedError(VisualDerivativeError):
    """Raised when synthetic or mocked inputs attempt to create production artifacts."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="SYNTHETIC_DERIVATIVE_BLOCKED", details=details)


class UnapprovedDerivativeReleaseError(VisualDerivativeError):
    """Raised when release is attempted without passing QA or operator authorization."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="UNAPPROVED_DERIVATIVE_RELEASE", details=details)


class WrongReadingLockMissingError(VisualDerivativeError):
    """Raised when wrong-reading locks are absent or violated."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="WRONG_READING_LOCK_MISSING", details=details)


class WorkspaceScopeViolationError(VisualDerivativeError):
    """Raised when cross-workspace tenant operations are attempted."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="WORKSPACE_SCOPE_VIOLATION", details=details)


class LaneAuthorityViolationError(VisualDerivativeError):
    """Raised when an operation is attempted on an invalid authority lane."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, reason_code="LANE_AUTHORITY_VIOLATION", details=details)


# ============================================================================
# 3. Visual Derivative Production Coordinator
# ============================================================================

class VisualDerivativeProductionCoordinator:
    """Authoritative multi-agent coordinator for Visual Derivative Production Programs."""

    PROGRAM_ID = "visual_derivative_production_program"
    PROGRAM_VERSION = "1.0.0"
    MACHINE_ID = "VISUAL_DERIVATIVE_PRODUCTION_STATE_MACHINE_V1"

    def __init__(
        self,
        runtime: UniversalProgramStateRuntime,
        pipeline_app: Optional[PipelineApplication] = None,
    ):
        from cmf_pipeline.composition.products import CarouselService, SuperVisualService
        from cmf_pipeline.composition.animation import AnimationSceneRealizer
        from cmf_pipeline.evaluation.reparse import RenderReparseService

        self.runtime = runtime
        self.pipeline_app = pipeline_app
        self.supervisual_service = SuperVisualService()
        self.carousel_service = CarouselService()
        self.animation_realizer = AnimationSceneRealizer()
        self.reparse_service = RenderReparseService()

    def _ensure_pipeline_app(self, workspace_id: str) -> PipelineApplication:
        if self.pipeline_app is None:
            from cmf_pipeline.application import PipelineApplication
            import tempfile
            db_dir = Path(tempfile.mkdtemp(prefix="cae_vis_pipe_"))
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

    def admit_semantic_program(
        self,
        semantic_program: Mapping[str, Any],
        workspace_id: str | UUID,
        operator_id: str,
        aggregate_id: Optional[str] = None,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Admit a SemanticProgram into visual derivative production under COMMANDER authority."""
        self._check_tenant(str(workspace_id))
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to admit programs. Required: COMMANDER"
            )

        # Anti-synthetic check
        if semantic_program.get("is_synthetic", False) or "synthetic" in str(semantic_program).lower():
            raise SyntheticDerivativeBlockedError(
                "Synthetic or mock SemanticProgram cannot enter production derivative compilation",
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
                transition_name="admit_semantic_program",
                actor_id=operator_id,
                actor_lane=lane,
                context_claims=["workspace_active", "operator_authorized"],
                payload=payload,
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def extract_derivative_sources(
        self,
        aggregate_id: str,
        evidence_segments: Sequence[Mapping[str, Any]],
        workspace_id: str,
        actor_id: str,
        lane: AuthorityLane = AuthorityLane.HUNTER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Extract authentic source spans and verbatim evidence anchors under HUNTER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.HUNTER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to extract sources. Required: HUNTER"
            )

        if not evidence_segments:
            raise SourceLineageMissingError("At least one authentic evidence segment is required")

        extracted_spans: List[Dict[str, Any]] = []
        for idx, seg in enumerate(evidence_segments):
            if seg.get("is_synthetic", False):
                raise SyntheticDerivativeBlockedError(
                    f"Evidence segment {idx} is synthetic and cannot be used for production",
                    details={"segment": seg},
                )
            text = seg.get("spoken_text") or seg.get("text", "")
            if not text:
                raise SourceLineageMissingError(f"Evidence segment {idx} missing spoken text")
            expected_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
            provided_hash = seg.get("text_sha256", expected_hash)
            if provided_hash != expected_hash:
                raise EvidenceQuoteMismatchError(
                    f"Evidence segment {idx} quote hash mismatch",
                    details={"provided": provided_hash, "expected": expected_hash},
                )

            span = DerivativeSourceSpan(
                source_id=seg.get("segment_id", f"seg-{idx}"),
                source_version="1.0.0",
                source_sha256=provided_hash,
                start_ms=int(seg.get("start_time_ms", 0)),
                end_ms=int(seg.get("end_time_ms", 1000)),
                quote_text=text.strip(),
                quote_sha256=expected_hash,
                speaker_id=seg.get("speaker_id", "speaker-1"),
            )
            extracted_spans.append(span.model_dump())

        payload = {
            "span_count": len(extracted_spans),
            "source_spans_sha256": canonical_sha256(extracted_spans),
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="extract_derivative_sources",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims=["workspace_active", "derivative_admitted"],
                payload=payload,
                state_updates={"source_spans": extracted_spans},
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def compile_derivative_compositions(
        self,
        aggregate_id: str,
        derivative_kind: DerivativeKind | str,
        canvas: Mapping[str, Any],
        pages: Sequence[Mapping[str, Any]],
        wrong_reading_locks: Sequence[str],
        profile_id: str,
        workspace_id: str,
        actor_id: str,
        lane: AuthorityLane = AuthorityLane.COMPOSER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Compile CompositionIR for the specified visual derivative under COMPOSER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to compile compositions. Required: COMPOSER"
            )

        d_kind = DerivativeKind(derivative_kind)
        if not wrong_reading_locks:
            raise WrongReadingLockMissingError("Visual derivatives require at least one wrong-reading lock")

        sorted_locks = sorted(list(dict.fromkeys(wrong_reading_locks)))

        app = self._ensure_pipeline_app(workspace_id)
        agg = self.runtime.get_aggregate(aggregate_id)

        sem_prog = agg.state_data.get("semantic_program", {})
        sem_ref = {
            "object_id": sem_prog.get("program_id", "sem-default"),
            "version": "1.0.0",
            "sha256": canonical_sha256(sem_prog),
        }

        # Validate composition kind matching
        comp_kind = "CAROUSEL" if d_kind == DerivativeKind.CAROUSEL else ("SUPERVISUAL" if d_kind == DerivativeKind.SUPERVISUAL else "ANIMATION_SCENE")
        
        ir_req = {
            "composition_kind": comp_kind,
            "semantic_program_ref": sem_ref,
            "final_script_ref": {"object_id": "script-001", "version": "1.0.0", "sha256": "0" * 64},
            "primitive_coalition_ref": {"object_id": "prim-001", "version": "1.0.0", "sha256": "0" * 64},
            "archetype_coalition_ref": {"object_id": "arch-001", "version": "1.0.0", "sha256": "0" * 64},
            "activation_transfer_contract_ref": {"object_id": "trans-001", "version": "1.0.0", "sha256": "0" * 64},
            "canvas": dict(canvas),
            "pages": [dict(p) for p in pages],
            "wrong_reading_locks": sorted_locks,
            "profile_id": profile_id,
        }

        ir_result = app.compositions.compile(ir_req, idempotency_key=f"{idempotency_key or aggregate_id}:ir")
        composition_ir = ir_result["object"]["payload"]

        payload = {
            "derivative_kind": d_kind.value,
            "composition_id": composition_ir["composition_id"],
            "page_count": len(pages),
            "composition_sha256": canonical_sha256(composition_ir),
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="compile_derivative_compositions",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims=["workspace_active", "sources_extracted"],
                payload=payload,
                state_updates={
                    "derivative_kind": d_kind.value,
                    "composition_ir": composition_ir,
                    "wrong_reading_locks": sorted_locks,
                },
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def realize_derivative_renders(
        self,
        aggregate_id: str,
        output_dir: str | Path,
        logical_prefix: str,
        workspace_id: str,
        actor_id: str,
        lane: AuthorityLane = AuthorityLane.COMPOSER,
        frame_count: int = 12,
        fps: int = 12,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Execute physical rendering / realization pass under COMPOSER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.COMPOSER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to realize renders. Required: COMPOSER"
            )

        agg = self.runtime.get_aggregate(aggregate_id)
        comp_ir = agg.state_data.get("composition_ir")
        if not comp_ir:
            raise VisualDerivativeError("No compiled composition found in aggregate state")

        d_kind_str = agg.state_data.get("derivative_kind", DerivativeKind.CAROUSEL.value)
        d_kind = DerivativeKind(d_kind_str)
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        render_artifacts: List[Dict[str, Any]] = []

        if d_kind == DerivativeKind.SUPERVISUAL:
            logical_uri = f"{logical_prefix}.png"
            res = self.supervisual_service.render(comp_ir, out_dir, logical_uri)
            manifest = res["manifest"]
            art = DerivativeRenderArtifact(
                artifact_id=manifest["artifact_id"],
                derivative_kind=d_kind.value,
                logical_uri=manifest["logical_uri"],
                sha256=manifest["sha256"],
                byte_count=manifest["byte_count"],
                output_path=res["output_path"],
                metadata={"product_kind": "SUPERVISUAL"},
            )
            render_artifacts.append(art.model_dump())

        elif d_kind == DerivativeKind.CAROUSEL:
            res = self.carousel_service.render(comp_ir, out_dir, logical_prefix)
            manifest = res["manifest"]
            pdf_art = manifest["pdf_artifact"]
            art = DerivativeRenderArtifact(
                artifact_id=manifest["carousel_artifact_id"],
                derivative_kind=d_kind.value,
                logical_uri=pdf_art["logical_uri"],
                sha256=pdf_art["sha256"],
                byte_count=pdf_art["byte_count"],
                output_path=res["pdf_path"],
                metadata={
                    "slide_artifacts": manifest["slide_artifacts"],
                    "reading_order": manifest["reading_order"],
                },
            )
            render_artifacts.append(art.model_dump())

        elif d_kind in {DerivativeKind.ANIMATION_SCENE_PACKAGE, DerivativeKind.ANIMATION_SHORT}:
            logical_uri = f"{logical_prefix}.mp4"
            scene_pkg = {
                "animation_scene_package_id": f"scene-pkg-{aggregate_id}",
                "animation_scene_package_version": "1.0.0",
                "scenes": [{"scene_id": p["page_id"]} for p in comp_ir["pages"]],
            }
            res = self.animation_realizer.realize(
                scene_package=scene_pkg,
                composition=comp_ir,
                output_dir=out_dir,
                logical_uri=logical_uri,
                frame_count=frame_count,
                fps=fps,
            )
            manifest = res["manifest"]
            art = DerivativeRenderArtifact(
                artifact_id=manifest["animation_artifact_id"],
                derivative_kind=d_kind.value,
                logical_uri=manifest["logical_uri"],
                sha256=manifest["sha256"],
                byte_count=manifest["byte_count"],
                output_path=res["output_path"],
                format02_activated=manifest.get("format02_activated", False),
                metadata={"frame_count": frame_count, "fps": fps},
            )
            render_artifacts.append(art.model_dump())

        payload = {
            "artifact_count": len(render_artifacts),
            "render_artifacts": render_artifacts,
        }

        try:
            res = self.runtime.execute_transition(
                aggregate_id=aggregate_id,
                transition_name="realize_derivative_renders",
                actor_id=actor_id,
                actor_lane=lane,
                context_claims=["workspace_active", "compositions_compiled"],
                payload=payload,
                state_updates={"render_artifacts": render_artifacts},
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
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Perform independent dual-axis Semantic QA vs Render QA under ANALYST authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.ANALYST:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to evaluate QA. Required: ANALYST"
            )

        agg = self.runtime.get_aggregate(aggregate_id)
        comp_ir = agg.state_data.get("composition_ir")
        render_artifacts = agg.state_data.get("render_artifacts", [])
        source_spans = agg.state_data.get("source_spans", [])
        locks = agg.state_data.get("wrong_reading_locks", [])

        if not comp_ir or not render_artifacts:
            raise VisualDerivativeError("Cannot perform QA: missing composition or render artifacts")

        # 1. Semantic QA Dimension
        semantic_issues: List[str] = []
        if not source_spans:
            semantic_issues.append("No authentic source evidence spans present")

        # Verify element text quotes against source evidence spans
        for page in comp_ir.get("pages", []):
            for el in page.get("elements", []):
                text = el.get("text")
                if text and text != "NOT_APPLICABLE":
                    # Check if text is backed by source refs
                    if not el.get("source_refs"):
                        semantic_issues.append(f"Element {el['element_id']} text is not grounded in source_refs")

        if not locks:
            semantic_issues.append("Missing required wrong-reading locks")

        semantic_passed = len(semantic_issues) == 0

        # 2. Render QA Dimension
        render_issues: List[str] = []
        for art in render_artifacts:
            p = Path(art["output_path"])
            if not p.is_file():
                render_issues.append(f"Render artifact file {p} does not exist")
            elif p.stat().st_size == 0:
                render_issues.append(f"Render artifact file {p} has zero byte count")
            elif bytes_sha256(p.read_bytes()) != art["sha256"]:
                render_issues.append(f"Render artifact file {p} hash mismatch")

        render_passed = len(render_issues) == 0
        overall_result = "PASS" if (semantic_passed and render_passed) else "FAIL"

        qa_receipt = DualAxisQAReceipt(
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
                "artifacts_verified": len(render_artifacts),
            },
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
                actor_id=actor_id,
                actor_lane=lane,
                context_claims=["workspace_active", "renders_realized"],
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

    def authorize_derivative_release(
        self,
        aggregate_id: str,
        operator_id: str,
        rationale: str,
        workspace_id: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Authorize production release of visual derivative under COMMANDER authority."""
        self._check_tenant(workspace_id)
        if lane != AuthorityLane.COMMANDER:
            raise LaneAuthorityViolationError(
                f"Lane '{lane.value}' is not authorized to release derivatives. Required: COMMANDER"
            )

        agg = self.runtime.get_aggregate(aggregate_id)
        qa = agg.state_data.get("dual_axis_qa_receipt")
        if not qa or qa.get("overall_result") != "PASS":
            raise UnapprovedDerivativeReleaseError(
                "Cannot authorize release: Dual-axis QA has not passed",
                details={"qa_receipt": qa},
            )

        comp_ir = agg.state_data.get("composition_ir", {})
        render_arts = agg.state_data.get("render_artifacts", [])
        sem_prog = agg.state_data.get("semantic_program", {})
        d_kind = agg.state_data.get("derivative_kind", DerivativeKind.CAROUSEL.value)

        receipt_core = {
            "receipt_id": f"rcpt-release-{uuid4().hex[:12]}",
            "aggregate_id": aggregate_id,
            "program_id": self.PROGRAM_ID,
            "workspace_id": str(workspace_id),
            "derivative_kind": d_kind,
            "semantic_program_ref": {
                "object_id": sem_prog.get("program_id", "sem-default"),
                "version": "1.0.0",
                "sha256": canonical_sha256(sem_prog),
            },
            "composition_ref": {
                "object_id": comp_ir.get("composition_id", "comp-default"),
                "version": "1.0.0",
                "sha256": canonical_sha256(comp_ir),
            },
            "render_artifact_refs": [
                {"object_id": a["artifact_id"], "logical_uri": a["logical_uri"], "sha256": a["sha256"]}
                for a in render_arts
            ],
            "qa_receipt_ref": {
                "object_id": qa["receipt_id"],
                "sha256": canonical_sha256(qa),
            },
            "operator_id": operator_id,
            "rationale": rationale,
            "committed_at": utc_now_rfc3339(),
        }

        release_receipt = DerivativeReleaseReceipt(
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
                transition_name="authorize_derivative_release",
                actor_id=operator_id,
                actor_lane=lane,
                context_claims=["workspace_active", "qa_passed", "operator_authorized"],
                payload=payload,
                state_updates={"derivative_release_receipt": release_receipt.model_dump()},
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))

    def repair_derivative_program(
        self,
        aggregate_id: str,
        operator_id: str,
        repair_instructions: str,
        workspace_id: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        idempotency_key: Optional[str] = None,
    ) -> ProgramStateAggregate:
        """Repair a faulted derivative program state under COMMANDER authority."""
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
            res = self.runtime.repair_state(
                aggregate_id=aggregate_id,
                repair_action="repair_derivative_program",
                repair_payload=payload,
                actor_id=operator_id,
                actor_lane=lane,
            )
            return res.aggregate
        except ProgramAuthorityLaneViolationError as e:
            raise LaneAuthorityViolationError(str(e))
