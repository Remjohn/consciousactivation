from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_pipeline.media.chunking import (
    BoundaryFrameError,
    MediaFrame,
    SourceContinuityError,
    UnsupportedReconstructionError,
    WindowOrderError,
    make_sliding_windows,
    stitch_windows,
)


SOURCE_SHA256 = "a" * 64
STREAM_ID = "video:0"


def _digest(index: int, kind: str = "video") -> str:
    return f"{index:064x}"[-64:]


def _frame(
    index: int,
    pts_us: int,
    duration_us: int = 1_000_000,
    *,
    kind: str = "video",
) -> MediaFrame:
    return MediaFrame(
        source_frame_index=index,
        pts_us=pts_us,
        duration_us=duration_us,
        payload_sha256=_digest(index, kind),
        kind=kind,
    )


def _fixture_frames() -> tuple[MediaFrame, ...]:
    # Frame 2 crosses the 2-second window boundary. It must be retained whole
    # in both adjacent processing windows and deduplicated only at stitch time.
    return (
        _frame(0, 0, 900_000),
        _frame(1, 900_000, 900_000),
        _frame(2, 1_800_000, 600_000),
        _frame(3, 2_400_000, 800_000),
        _frame(4, 3_200_000, 800_000),
    )


def _windows() -> tuple:
    return make_sliding_windows(
        _fixture_frames(),
        source_media_sha256=SOURCE_SHA256,
        stream_id=STREAM_ID,
        window_duration_us=2_000_000,
        overlap_us=500_000,
    )


def test_sliding_windows_preserve_boundary_frame_whole_and_explicit_overlap():
    windows = _windows()

    assert len(windows) == 3
    assert windows[0].successor_window_id == windows[1].window_id
    assert windows[1].predecessor_window_id == windows[0].window_id
    assert (windows[1].overlap_start_us, windows[1].overlap_end_us) == (
        1_500_000,
        2_000_000,
    )

    # Frame 2 straddles the 2-second boundary and is present in both windows.
    assert 2 in {frame.source_frame_index for frame in windows[0].frames}
    assert 2 in {frame.source_frame_index for frame in windows[1].frames}
    assert next(
        frame for frame in windows[0].frames if frame.source_frame_index == 2
    ).end_us == 2_400_000


def test_stitch_is_deterministic_and_deduplicates_overlap_by_source_identity():
    windows = _windows()

    stitched = stitch_windows(windows)

    assert [frame.source_frame_index for frame in stitched.frames] == [0, 1, 2, 3, 4]
    assert stitched.overlap_frame_indices == (1, 2, 3, 4)
    assert stitched.contributing_window_ids == tuple(window.window_id for window in windows)

    again = stitch_windows(tuple(reversed(windows)))
    assert again.frames == stitched.frames
    assert again.overlap_frame_indices == stitched.overlap_frame_indices
    assert again.contributing_window_ids == stitched.contributing_window_ids


def test_duplicate_overlap_with_changed_timestamp_or_payload_fails_closed():
    windows = list(_windows())
    second = windows[1]
    frames = list(second.frames)
    boundary_index = next(
        i for i, frame in enumerate(frames) if frame.source_frame_index == 2
    )
    frames[boundary_index] = replace(
        frames[boundary_index],
        pts_us=1_800_001,
        payload_sha256="b" * 64,
    )
    windows[1] = replace(second, frames=tuple(frames))

    with pytest.raises(BoundaryFrameError, match="conflicting overlap frame"):
        stitch_windows(tuple(windows))


def test_missing_boundary_frame_fails_closed_instead_of_smoothing():
    windows = list(_windows())
    second = windows[1]
    windows[1] = replace(
        second,
        frames=tuple(
            frame
            for frame in second.frames
            if frame.source_frame_index != 2
        ),
    )

    with pytest.raises(BoundaryFrameError, match="overlap frame identity differs"):
        stitch_windows(tuple(windows))


def test_reordered_windows_fail_even_if_the_frame_sets_are_identical():
    windows = list(_windows())
    first, second = windows[0], windows[1]
    windows[0] = replace(
        first,
        predecessor_window_id=second.window_id,
        successor_window_id=None,
    )

    with pytest.raises(WindowOrderError, match="incorrect predecessor"):
        stitch_windows(tuple(windows))


def test_missing_continuity_relation_fails_closed():
    windows = list(_windows())
    windows[1] = replace(windows[1], predecessor_window_id=None)

    with pytest.raises(WindowOrderError, match="incorrect predecessor"):
        stitch_windows(tuple(windows))


def test_dropped_source_frame_is_rejected_after_overlap_reconciliation():
    windows = list(_windows())
    # Remove frame 3 from every window containing it. This simulates a true
    # source drop rather than an overlap-only omission.
    windows = [
        replace(
            window,
            frames=tuple(
                frame
                for frame in window.frames
                if frame.source_frame_index != 3
            ),
        )
        for window in windows
    ]

    with pytest.raises(SourceContinuityError, match="dropped boundary frame"):
        stitch_windows(tuple(windows))


def test_unsupported_fabricated_reconstruction_cannot_enter_the_media_contract():
    with pytest.raises(
        UnsupportedReconstructionError, match="audio.*video"
    ):
        MediaFrame(
            source_frame_index=7,
            pts_us=2_000_000,
            duration_us=500_000,
            payload_sha256="c" * 64,
            kind="model-generated-text",
        )


def test_audio_and_video_keep_independent_source_identity_and_timestamp_order():
    frames = (
        _frame(0, 0, 20_000, kind="audio"),
        _frame(0, 0, 33_333, kind="video"),
        _frame(1, 20_000, 20_000, kind="audio"),
        _frame(1, 33_333, 33_333, kind="video"),
        _frame(2, 40_000, 20_000, kind="audio"),
        _frame(2, 66_666, 33_333, kind="video"),
    )
    windows = make_sliding_windows(
        frames,
        source_media_sha256=SOURCE_SHA256,
        stream_id=STREAM_ID,
        window_duration_us=50_000,
        overlap_us=20_000,
    )

    stitched = stitch_windows(windows)

    assert [(f.kind, f.source_frame_index) for f in stitched.frames] == [
        ("audio", 0),
        ("video", 0),
        ("audio", 1),
        ("video", 1),
        ("audio", 2),
        ("video", 2),
    ]
    assert all(
        frame.pts_us + frame.duration_us > frame.pts_us
        for frame in stitched.frames
    )


def test_single_window_requires_no_overlap_and_preserves_exact_source_frames():
    windows = make_sliding_windows(
        _fixture_frames()[:2],
        source_media_sha256=SOURCE_SHA256,
        stream_id=STREAM_ID,
        window_duration_us=5_000_000,
        overlap_us=1_000_000,
    )

    assert len(windows) == 1
    stitched = stitch_windows(windows)
    assert stitched.frames == _fixture_frames()[:2]
    assert stitched.overlap_frame_indices == ()


def test_boundary_frame_is_never_split_or_retimed_by_windowing():
    boundary = _frame(8, 1_900_000, 300_000)
    frames = (
        _frame(7, 1_000_000, 900_000),
        boundary,
        _frame(9, 2_200_000, 800_000),
    )
    windows = make_sliding_windows(
        frames,
        source_media_sha256=SOURCE_SHA256,
        stream_id=STREAM_ID,
        window_duration_us=2_000_000,
        overlap_us=500_000,
    )

    copies = [
        frame
        for window in windows
        for frame in window.frames
        if frame.source_frame_index == boundary.source_frame_index
    ]
    assert len(copies) == 2
    assert all(frame == boundary for frame in copies)
