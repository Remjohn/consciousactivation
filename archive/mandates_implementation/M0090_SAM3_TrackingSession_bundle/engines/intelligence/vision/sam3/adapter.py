"""Narrow SAM3 runtime adapter for CAE M0090.

The adapter owns no CAE semantic state. It maps governed TrackingPrompt inputs
into the current upstream SAM3 tracking predictor surface and converts model
masks into integer, normalized CAE geometry. Native SAM3 is injected so the
external runtime remains replaceable and can never bypass CAE validators.
"""

from __future__ import annotations

import math
from typing import Any, Callable, Iterable, Mapping, Optional, Protocol, Sequence

from ca_runtime.tracking_session import (
    BBoxGeometry,
    TrackFrame,
    TrackGap,
    TrackSegment,
    TrackingPrompt,
    TrackingPromptKind,
)


class Sam3RuntimeUnavailable(RuntimeError):
    """Native SAM3 runtime/checkpoints are unavailable in the current process."""


class Sam3RuntimeContractError(RuntimeError):
    """Injected predictor does not satisfy the required narrow SAM3 surface."""


class Sam3PredictorProtocol(Protocol):
    def init_state(self, *, video_path: str) -> Any: ...

    def add_new_points_or_box(
        self,
        inference_state: Any,
        *,
        frame_idx: int,
        obj_id: int,
        points: Optional[Any] = None,
        labels: Optional[Any] = None,
        rel_coordinates: bool = True,
        box: Optional[Any] = None,
    ) -> Any: ...

    def add_new_mask(self, inference_state: Any, *, frame_idx: int, obj_id: int, mask: Any) -> Any: ...

    def propagate_in_video(self, inference_state: Any, *, start_frame_idx: int) -> Iterable[Any]: ...


MaskLoader = Callable[[str], Any]


def _as_scalar(value: Any) -> float:
    if hasattr(value, "detach"):
        value = value.detach().cpu()
    if hasattr(value, "item"):
        return float(value.item())
    if isinstance(value, (list, tuple)) and len(value) == 1:
        return _as_scalar(value[0])
    return float(value)


def confidence_to_bps(score_logit: Any) -> int:
    """Convert upstream object-score logits to CAE integer confidence basis points."""
    logit = max(-60.0, min(60.0, _as_scalar(score_logit)))
    score = 1.0 / (1.0 + math.exp(-logit))
    return max(0, min(10_000, int(round(score * 10_000))))


def _mask_bbox(mask: Any, *, width_px: int, height_px: int) -> BBoxGeometry:
    """Compute a deterministic bbox from a single boolean/score mask."""
    if hasattr(mask, "detach"):
        mask = mask.detach().cpu()
        if hasattr(mask, "squeeze"):
            mask = mask.squeeze()
        if hasattr(mask, "nonzero"):
            nz = mask > 0
            indices = nz.nonzero(as_tuple=False)
            if int(indices.shape[0]) == 0:
                raise Sam3RuntimeContractError("SAM3 returned an empty target mask")
            ys = indices[:, -2]
            xs = indices[:, -1]
            min_x = int(xs.min().item())
            max_x = int(xs.max().item())
            min_y = int(ys.min().item())
            max_y = int(ys.max().item())
        else:
            raise Sam3RuntimeContractError("unsupported tensor mask type")
    else:
        # Lightweight fallback for test doubles and list-backed masks.
        rows = mask.tolist() if hasattr(mask, "tolist") else mask
        points = [(y, x) for y, row in enumerate(rows) for x, value in enumerate(row) if value]
        if not points:
            raise Sam3RuntimeContractError("SAM3 returned an empty target mask")
        min_y = min(y for y, _ in points)
        max_y = max(y for y, _ in points)
        min_x = min(x for _, x in points)
        max_x = max(x for _, x in points)

    mask_height = max(1, height_px)
    mask_width = max(1, width_px)
    x_bps = (min_x * 10_000) // mask_width
    y_bps = (min_y * 10_000) // mask_height
    right_bps = min(10_000, ((max_x + 1) * 10_000 + mask_width - 1) // mask_width)
    bottom_bps = min(10_000, ((max_y + 1) * 10_000 + mask_height - 1) // mask_height)
    return BBoxGeometry(
        x_bps=x_bps,
        y_bps=y_bps,
        width_bps=max(1, right_bps - x_bps),
        height_bps=max(1, bottom_bps - y_bps),
    )


class Sam3TrackingAdapter:
    """Compile CAE prompts into the current SAM3 tracker predictor surface."""

    RUNTIME_OBJECT_ID = 1

    def __init__(self, predictor: Sam3PredictorProtocol, *, mask_loader: Optional[MaskLoader] = None) -> None:
        self.predictor = predictor
        self.mask_loader = mask_loader
        self._states: dict[str, Any] = {}

    def start_session(self, *, runtime_session_id: str, video_path: str) -> None:
        if not video_path:
            raise Sam3RuntimeContractError("video_path is required for native SAM3")
        try:
            self._states[runtime_session_id] = self.predictor.init_state(video_path=video_path)
        except Exception as exc:  # noqa: BLE001 - boundary converts native failures to CAE runtime errors.
            raise Sam3RuntimeUnavailable("SAM3 init_state failed; native runtime is unavailable") from exc

    def seed(self, *, runtime_session_id: str, prompt: TrackingPrompt) -> None:
        if runtime_session_id not in self._states:
            raise Sam3RuntimeContractError("SAM3 runtime session has not been started")
        state = self._states[runtime_session_id]
        if prompt.kind == TrackingPromptKind.MASK:
            if self.mask_loader is None:
                raise Sam3RuntimeContractError("MASK prompt requires an injected immutable mask loader")
            mask = self.mask_loader(prompt.mask_ref or "")
            self.predictor.add_new_mask(
                state,
                frame_idx=prompt.frame_index,
                obj_id=self.RUNTIME_OBJECT_ID,
                mask=mask,
            )
            return

        points = None
        labels = None
        box = None
        if prompt.kind == TrackingPromptKind.BOX:
            assert prompt.box is not None
            box = _box_to_relative_coords(prompt.box)
        elif prompt.kind == TrackingPromptKind.POINT:
            assert prompt.point is not None
            points = [[prompt.point.x_bps / 10_000, prompt.point.y_bps / 10_000]]
            labels = [1]
        elif prompt.kind == TrackingPromptKind.FACE:
            # CAE face selection is operator evidence; SAM3 receives only its geometric seed.
            if prompt.box is not None:
                box = _box_to_relative_coords(prompt.box)
            elif prompt.point is not None:
                points = [[prompt.point.x_bps / 10_000, prompt.point.y_bps / 10_000]]
                labels = [1]
        else:
            raise Sam3RuntimeContractError(f"unsupported prompt kind: {prompt.kind}")
        self.predictor.add_new_points_or_box(
            state,
            frame_idx=prompt.frame_index,
            obj_id=self.RUNTIME_OBJECT_ID,
            points=points,
            labels=labels,
            rel_coordinates=True,
            box=box,
        )

    def propagate(
        self,
        *,
        runtime_session_id: str,
        target_id: str,
        segment_id: str,
        start_frame: int,
        end_frame: int,
        source_frame_hashes: Mapping[int, str],
        width_px: int,
        height_px: int,
    ) -> TrackSegment:
        if runtime_session_id not in self._states:
            raise Sam3RuntimeContractError("SAM3 runtime session has not been started")
        if not source_frame_hashes:
            raise Sam3RuntimeContractError("missing source frame hash coverage for governed output")
        state = self._states[runtime_session_id]
        try:
            outputs = list(
                self.predictor.propagate_in_video(
                    state,
                    start_frame_idx=start_frame,
                )
            )
        except Exception as exc:  # noqa: BLE001 - runtime boundary; fail closed.
            raise Sam3RuntimeUnavailable("SAM3 propagation failed") from exc

        frames: list[TrackFrame] = []
        for output in outputs:
            if not isinstance(output, (tuple, list)) or len(output) < 4:
                raise Sam3RuntimeContractError("SAM3 propagation output shape is unsupported")
            frame_index = int(output[0])
            if frame_index < start_frame or frame_index > end_frame:
                continue
            masks = output[3]
            object_scores = output[4] if len(output) >= 5 else None
            if masks is None:
                continue
            first_mask = masks[0] if hasattr(masks, "__getitem__") else masks
            if object_scores is None:
                raise Sam3RuntimeContractError("SAM3 object score logits are required for governed confidence")
            score = object_scores[0] if hasattr(object_scores, "__getitem__") else object_scores
            source_hash = source_frame_hashes.get(frame_index)
            if source_hash is None:
                raise Sam3RuntimeContractError(
                    f"missing source frame hash for tracked frame {frame_index}"
                )
            if not isinstance(source_hash, str) or len(source_hash) != 64:
                raise Sam3RuntimeContractError("source frame hash must be a SHA-256 digest")
            frames.append(
                TrackFrame(
                    frame_index=frame_index,
                    source_frame_sha256=source_hash,
                    confidence_bps=confidence_to_bps(score),
                    bbox=_mask_bbox(first_mask, width_px=width_px, height_px=height_px),
                )
            )
        frames.sort(key=lambda frame: frame.frame_index)
        covered = {frame.frame_index for frame in frames}
        gaps: list[TrackGap] = []
        missing_start: Optional[int] = None
        for index in range(start_frame, end_frame + 1):
            if index in covered:
                if missing_start is not None:
                    gaps.append(TrackGap(start_frame=missing_start, end_frame=index - 1, reason="MODEL_NO_OUTPUT"))
                    missing_start = None
            elif missing_start is None:
                missing_start = index
        if missing_start is not None:
            gaps.append(TrackGap(start_frame=missing_start, end_frame=end_frame, reason="MODEL_NO_OUTPUT"))
        return TrackSegment(
            segment_id=segment_id,
            target_id=target_id,
            start_frame=start_frame,
            end_frame=end_frame,
            frames=frames,
            gaps=gaps,
        )


def _box_to_relative_coords(box: BBoxGeometry) -> Sequence[float]:
    # This is runtime-only data; CAE never persists these floats.
    return [
        box.x_bps / 10_000,
        box.y_bps / 10_000,
        (box.x_bps + box.width_bps) / 10_000,
        (box.y_bps + box.height_bps) / 10_000,
    ]


__all__ = [
    "Sam3PredictorProtocol",
    "Sam3RuntimeContractError",
    "Sam3RuntimeUnavailable",
    "Sam3TrackingAdapter",
    "confidence_to_bps",
]
