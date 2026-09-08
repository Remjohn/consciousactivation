"""
Deterministic cross-window media chunking and stitching.

CA-M014 / FR-014
-----------------
Windows are processing views over one immutable source stream. They are not
independent evidence. A frame is identified by source coordinates rather than
by text or model output, and overlap is reconciled only when the two copies
have identical source identity and timing metadata.

This module deliberately does not reconstruct or "smooth" missing content.
When continuity cannot be proven, it fails closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


class CrossWindowChunkingError(ValueError):
    """Base error for an unverifiable cross-window media layout."""


class WindowIdentityError(CrossWindowChunkingError):
    """Window identity, source identity, or stream identity is inconsistent."""


class WindowOrderError(CrossWindowChunkingError):
    """Window sequence or predecessor/successor metadata is invalid."""


class WindowOverlapError(CrossWindowChunkingError):
    """Overlap metadata or overlap membership is invalid."""


class BoundaryFrameError(CrossWindowChunkingError):
    """A frame crossing/occupying an overlap boundary was lost or altered."""


class TimestampAlignmentError(CrossWindowChunkingError):
    """Frame timestamps/durations are not deterministic and aligned."""


class SourceContinuityError(CrossWindowChunkingError):
    """Source-frame coordinates contain a gap or cannot prove continuity."""


class UnsupportedReconstructionError(CrossWindowChunkingError):
    """The caller supplied reconstructed content instead of source frames."""


@dataclass(frozen=True, slots=True)
class MediaFrame:
    """An immutable source-frame reference.

    ``source_frame_index`` is the authoritative identity within a stream.
    ``pts_us`` and ``duration_us`` are integer microsecond coordinates. The
    digest identifies the exact source payload; it is never used to infer or
    synthesize content.
    """

    source_frame_index: int
    pts_us: int
    duration_us: int
    payload_sha256: str
    kind: str

    def __post_init__(self) -> None:
        if self.source_frame_index < 0:
            raise SourceContinuityError("source_frame_index must be non-negative")
        if self.pts_us < 0:
            raise TimestampAlignmentError("pts_us must be non-negative")
        if self.duration_us <= 0:
            raise TimestampAlignmentError("duration_us must be positive")
        if self.kind not in {"audio", "video"}:
            raise UnsupportedReconstructionError(
                "frame kind must be 'audio' or 'video'"
            )
        digest = self.payload_sha256.lower()
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise BoundaryFrameError(
                "payload_sha256 must be a 64-character SHA-256 digest"
            )

    @property
    def end_us(self) -> int:
        return self.pts_us + self.duration_us

    @property
    def identity(self) -> tuple[str, int]:
        return self.kind, self.source_frame_index

    @property
    def fingerprint(self) -> tuple[str, int, int, int, str]:
        return (
            self.kind,
            self.source_frame_index,
            self.pts_us,
            self.duration_us,
            self.payload_sha256.lower(),
        )


@dataclass(frozen=True, slots=True)
class MediaWindow:
    """A deterministic processing window over an immutable source stream.

    ``start_us``/``end_us`` are nominal window coordinates. Frames are
    selected by source-time intersection, so a frame crossing a boundary is
    retained whole. The same source frame may therefore appear in two
    adjacent windows; stitching removes that duplicate by source identity.
    """

    window_id: str
    sequence: int
    source_media_sha256: str
    stream_id: str
    start_us: int
    end_us: int
    frames: tuple[MediaFrame, ...]
    predecessor_window_id: str | None = None
    successor_window_id: str | None = None
    overlap_start_us: int | None = None
    overlap_end_us: int | None = None

    def __post_init__(self) -> None:
        if not self.window_id:
            raise WindowIdentityError("window_id is required")
        if self.sequence < 0:
            raise WindowOrderError("window sequence must be non-negative")
        if self.end_us <= self.start_us:
            raise TimestampAlignmentError(
                "window end must be greater than window start"
            )
        digest = self.source_media_sha256.lower()
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise WindowIdentityError(
                "source_media_sha256 must be a 64-character SHA-256 digest"
            )
        if not self.stream_id:
            raise WindowIdentityError("stream_id is required")
        if (self.overlap_start_us is None) != (self.overlap_end_us is None):
            raise WindowOverlapError(
                "overlap_start_us and overlap_end_us must be supplied together"
            )
        if self.overlap_start_us is not None:
            if not (
                self.start_us < self.overlap_start_us < self.overlap_end_us <= self.end_us
            ):
                raise WindowOverlapError("overlap must be strictly inside the window")
        last: tuple[int, int] | None = None
        for frame in self.frames:
            if frame.pts_us >= self.end_us or frame.end_us <= self.start_us:
                raise TimestampAlignmentError(
                    f"frame {frame.source_frame_index} is outside window {self.window_id}"
                )
            key = (frame.source_frame_index, frame.pts_us)
            if last is not None and key < last:
                raise TimestampAlignmentError(
                    f"frames in window {self.window_id} are not source-order deterministic"
                )
            last = key


@dataclass(frozen=True, slots=True)
class StitchedMedia:
    """The de-duplicated, source-ordered frame view proven by the stitcher."""

    source_media_sha256: str
    stream_id: str
    frames: tuple[MediaFrame, ...]
    contributing_window_ids: tuple[str, ...]
    overlap_frame_indices: tuple[int, ...]


def _intersects(frame: MediaFrame, start_us: int, end_us: int) -> bool:
    return frame.pts_us < end_us and frame.end_us > start_us


def make_sliding_windows(
    frames: Iterable[MediaFrame],
    *,
    source_media_sha256: str,
    stream_id: str,
    window_duration_us: int,
    overlap_us: int,
    start_us: int = 0,
) -> tuple[MediaWindow, ...]:
    """Build deterministic windows without splitting source frames.

    The nominal windows advance by ``window_duration_us - overlap_us``.
    Every frame intersecting a window is included in full. Consequently a
    frame that straddles a nominal boundary is retained in both neighboring
    windows when it lies in their overlap. No transcript text or media payload
    is fabricated.
    """

    source_frames = tuple(frames)
    if not source_frames:
        raise SourceContinuityError("cannot window an empty source frame sequence")
    if window_duration_us <= 0:
        raise WindowOverlapError("window_duration_us must be positive")
    if overlap_us <= 0 or overlap_us >= window_duration_us:
        raise WindowOverlapError(
            "overlap_us must be greater than zero and less than window duration"
        )
    if start_us < 0:
        raise TimestampAlignmentError("start_us must be non-negative")

    ordered = sorted(
        source_frames,
        key=lambda f: (f.pts_us, f.kind, f.source_frame_index),
    )
    per_kind_last: dict[str, int] = {}
    for frame in ordered:
        last_index = per_kind_last.get(frame.kind)
        if last_index is not None and frame.source_frame_index <= last_index:
            raise SourceContinuityError(
                f"{frame.kind} source frame indices are not strictly increasing"
            )
        per_kind_last[frame.kind] = frame.source_frame_index

    step = window_duration_us - overlap_us
    final_end = max(frame.end_us for frame in ordered)
    windows: list[MediaWindow] = []
    sequence = 0
    cursor = start_us

    while cursor < final_end:
        end = cursor + window_duration_us
        predecessor = windows[-1] if windows else None
        overlap_start = cursor if predecessor is not None else None
        overlap_end = min(predecessor.end_us, end) if predecessor is not None else None
        selected = tuple(
            frame for frame in ordered if _intersects(frame, cursor, end)
        )
        if not selected:
            raise SourceContinuityError(
                f"window {sequence} contains no source frames; source continuity is unproven"
            )
        window = MediaWindow(
            window_id=f"window-{sequence:06d}",
            sequence=sequence,
            source_media_sha256=source_media_sha256,
            stream_id=stream_id,
            start_us=cursor,
            end_us=end,
            frames=selected,
            predecessor_window_id=predecessor.window_id if predecessor else None,
            overlap_start_us=overlap_start,
            overlap_end_us=overlap_end,
        )
        if predecessor is not None:
            previous = windows[-1]
            windows[-1] = MediaWindow(
                window_id=previous.window_id,
                sequence=previous.sequence,
                source_media_sha256=previous.source_media_sha256,
                stream_id=previous.stream_id,
                start_us=previous.start_us,
                end_us=previous.end_us,
                frames=previous.frames,
                predecessor_window_id=previous.predecessor_window_id,
                successor_window_id=window.window_id,
                overlap_start_us=previous.overlap_start_us,
                overlap_end_us=previous.overlap_end_us,
            )
        windows.append(window)
        sequence += 1
        cursor += step

    return tuple(windows)


def stitch_windows(windows: Sequence[MediaWindow]) -> StitchedMedia:
    """Reconcile overlapping windows into one source-ordered frame sequence.

    The operation is deterministic and fail-closed:
    * sequence and predecessor/successor links must agree;
    * adjacent nominal windows must have a declared overlap;
    * duplicate overlap frames must have identical source coordinates and
      payload digests;
    * every source-frame index in the covered range must be present exactly
      once after reconciliation;
    * any frame intersecting a declared overlap must occur in both windows;
    * no generated text, frame, timestamp, or payload may be introduced.
    """

    if not windows:
        raise WindowOrderError("at least one window is required")

    ordered_windows = tuple(sorted(windows, key=lambda w: w.sequence))
    if any(
        a.sequence == b.sequence and a.window_id != b.window_id
        for a, b in zip(ordered_windows, ordered_windows[1:])
    ):
        raise WindowOrderError("window sequences must be unique")
    if tuple(w.sequence for w in ordered_windows) != tuple(range(len(ordered_windows))):
        raise WindowOrderError("window sequences must be contiguous from zero")

    ids = [w.window_id for w in ordered_windows]
    if len(ids) != len(set(ids)):
        raise WindowIdentityError("window_id values must be unique")

    source = ordered_windows[0].source_media_sha256.lower()
    stream = ordered_windows[0].stream_id
    for index, window in enumerate(ordered_windows):
        if window.source_media_sha256.lower() != source or window.stream_id != stream:
            raise WindowIdentityError("all windows must reference one source media stream")
        expected_predecessor = (
            ordered_windows[index - 1].window_id if index else None
        )
        expected_successor = (
            ordered_windows[index + 1].window_id
            if index + 1 < len(ordered_windows)
            else None
        )
        if window.predecessor_window_id != expected_predecessor:
            raise WindowOrderError(
                f"window {window.window_id} has incorrect predecessor metadata"
            )
        if window.successor_window_id != expected_successor:
            raise WindowOrderError(
                f"window {window.window_id} has incorrect successor metadata"
            )

        if index == 0:
            if (
                window.overlap_start_us is not None
                or window.overlap_end_us is not None
            ):
                raise WindowOverlapError(
                    "first window cannot declare a predecessor overlap"
                )
            continue

        previous = ordered_windows[index - 1]
        expected_start = max(previous.start_us, window.start_us)
        expected_end = min(previous.end_us, window.end_us)
        if expected_end <= expected_start:
            raise WindowOverlapError(
                f"adjacent windows {previous.window_id} and {window.window_id} do not overlap"
            )
        if (window.overlap_start_us, window.overlap_end_us) != (
            expected_start,
            expected_end,
        ):
            raise WindowOverlapError(
                f"window {window.window_id} overlap metadata does not match source coordinates"
            )

        previous_overlap = {
            frame.identity: frame
            for frame in previous.frames
            if _intersects(frame, expected_start, expected_end)
        }
        current_overlap = {
            frame.identity: frame
            for frame in window.frames
            if _intersects(frame, expected_start, expected_end)
        }
        if set(previous_overlap) != set(current_overlap):
            raise BoundaryFrameError(
                f"overlap frame identity differs between {previous.window_id} and {window.window_id}"
            )
        for identity, previous_frame in previous_overlap.items():
            current_frame = current_overlap[identity]
            if previous_frame.fingerprint != current_frame.fingerprint:
                raise BoundaryFrameError(
                    f"conflicting overlap frame {identity} has different source/timestamp/payload identity"
                )

    by_identity: dict[tuple[str, int], MediaFrame] = {}
    contributing: list[str] = []
    overlap_indices: set[int] = set()

    for window in ordered_windows:
        contributing.append(window.window_id)
        for frame in window.frames:
            existing = by_identity.get(frame.identity)
            if existing is None:
                by_identity[frame.identity] = frame
            elif existing.fingerprint != frame.fingerprint:
                raise BoundaryFrameError(
                    f"duplicate source frame {frame.identity} has conflicting metadata"
                )

    frames = tuple(
        sorted(
            by_identity.values(),
            key=lambda f: (f.pts_us, f.kind, f.source_frame_index),
        )
    )

    per_kind: dict[str, list[MediaFrame]] = {}
    for frame in frames:
        per_kind.setdefault(frame.kind, []).append(frame)
    for kind, kind_frames in per_kind.items():
        indices = [frame.source_frame_index for frame in kind_frames]
        if indices != list(range(indices[0], indices[-1] + 1)):
            raise SourceContinuityError(
                f"{kind} source-frame sequence contains a dropped boundary frame"
            )
        for previous, current in zip(kind_frames, kind_frames[1:]):
            if current.pts_us < previous.pts_us:
                raise TimestampAlignmentError(
                    f"{kind} timestamps are not monotonic after stitching"
                )

    for previous, current in zip(ordered_windows, ordered_windows[1:]):
        overlap_start = current.overlap_start_us
        overlap_end = current.overlap_end_us
        assert overlap_start is not None and overlap_end is not None
        for frame in previous.frames:
            if _intersects(frame, overlap_start, overlap_end):
                overlap_indices.add(frame.source_frame_index)

    return StitchedMedia(
        source_media_sha256=source,
        stream_id=stream,
        frames=frames,
        contributing_window_ids=tuple(contributing),
        overlap_frame_indices=tuple(sorted(overlap_indices)),
    )


__all__ = [
    "BoundaryFrameError",
    "CrossWindowChunkingError",
    "MediaFrame",
    "MediaWindow",
    "SourceContinuityError",
    "StitchedMedia",
    "TimestampAlignmentError",
    "UnsupportedReconstructionError",
    "WindowIdentityError",
    "WindowOrderError",
    "WindowOverlapError",
    "make_sliding_windows",
    "stitch_windows",
]
