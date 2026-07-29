// TS-APP-UI-003 - Timeline tests
// AC-012: Timeline renders tracks in z-index order with correctly scaled items

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { Timeline } from "../Timeline";

// Mock timeline data
const mockTimeline = {
  timeline_id: "tl-001",
  video_edit_program_ref: {
    object_id: "prog-123",
    sha256: "abc",
    version: "1",
  },
  tracks: [
    {
      track_id: "track-001",
      z_index: 0,
      items: [
        {
          item_id: "item-001",
          start_frame: 0,
          end_frame: 50,
        },
      ],
    },
    {
      track_id: "track-002",
      z_index: 1,
      items: [
        {
          item_id: "item-002",
          start_frame: 25,
          end_frame: 75,
        },
      ],
    },
  ],
  duration_frames: 100,
  fps_numerator: 30,
  fps_denominator: 1,
};

describe("Timeline", () => {
  it("should render 'Nothing compiled yet' when timeline is null (AC-010 variant)", () => {
    render(
      <Timeline
        campaignId="campaign-123"
        timeline={null}
      />
    );

    expect(screen.getByText(/Nothing has been compiled yet/)).toBeInTheDocument();
  });

  it("should render timeline with tracks (AC-012)", () => {
    render(
      <Timeline
        campaignId="campaign-123"
        timeline={mockTimeline}
      />
    );

    // Should show timeline header
    expect(screen.getByText("Timeline")).toBeInTheDocument();

    // Should show duration info - use getAllByText since it appears multiple times
    expect(screen.getAllByText(/3\.3s/).length).toBeGreaterThan(0); // 100 frames / 30 fps = 3.33s

    // Should render both tracks - the component shows "Track: track-001 (z-index: 0)"
    expect(screen.getByText(/track-001/)).toBeInTheDocument();
    expect(screen.getByText(/track-002/)).toBeInTheDocument();
  });

  it("should render tracks in correct DOM order (highest z-index first) (AC-012)", () => {
    const { container } = render(
      <Timeline
        campaignId="campaign-123"
        timeline={mockTimeline}
      />
    );

    // Get track container elements (they have rounded bg-ca-surface-raised class)
    const trackElements = container.querySelectorAll(".rounded.bg-ca-surface-raised");

    // Should have 2 track elements (the tracks, not other rounded elements)
    // Actually the component has multiple rounded elements, let's check for track text
    const trackTexts = screen.getAllByText(/Track:/);
    expect(trackTexts).toHaveLength(2);

    // track-002 (z_index: 1) should be first, track-001 (z_index: 0) should be second
    expect(trackTexts[0]).toHaveTextContent("track-002");
    expect(trackTexts[1]).toHaveTextContent("track-001");
  });

  it("should scale item width based on duration_frames (AC-012)", () => {
    const { container } = render(
      <Timeline
        campaignId="campaign-123"
        timeline={mockTimeline}
      />
    );

    // Get all item elements (they have absolute positioning with left/width styles)
    const itemElements = container.querySelectorAll("[style*='left:']");

    expect(itemElements.length).toBe(2);

    // Check that items have calculated widths as percentages
    itemElements.forEach((el) => {
      const style = (el as HTMLElement).style.width;
      expect(style).toMatch(/^\d+(\.\d+)?%$/);
    });

    // Tracks are sorted by z_index descending:
    // Track 1: track-002 (z_index: 1) with item-002 (25-75 frames)
    //   - left: 25%, width: 50%
    // Track 2: track-001 (z_index: 0) with item-001 (0-50 frames)
    //   - left: 0%, width: 50%

    // First item (from track-002): 25-75 frames out of 100 = 25% left, 50% width
    const firstItem = itemElements[0] as HTMLElement;
    expect(firstItem.style.left).toBe("25%");
    expect(firstItem.style.width).toBe("50%");

    // Second item (from track-001): 0-50 frames out of 100 = 0% left, 50% width
    const secondItem = itemElements[1] as HTMLElement;
    expect(secondItem.style.left).toBe("0%");
    expect(secondItem.style.width).toBe("50%");
  });

  it("should show fps info in header", () => {
    render(
      <Timeline
        campaignId="campaign-123"
        timeline={mockTimeline}
      />
    );

    // Check for the fps text in the header specifically
    const header = screen.getByText("Timeline").parentElement;
    expect(header).toHaveTextContent(/30\/1 fps/);
  });

  it("should render timeline ruler with time markers", () => {
    render(
      <Timeline
        campaignId="campaign-123"
        timeline={mockTimeline}
      />
    );

    // Should show time markers (0s, 0.8s, 1.7s, 2.5s, 3.3s)
    expect(screen.getByText("0.0s")).toBeInTheDocument();
    expect(screen.getByText("3.3s")).toBeInTheDocument();
  });
});
