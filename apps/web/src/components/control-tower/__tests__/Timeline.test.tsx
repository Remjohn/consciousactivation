// CAE-M0066 - Native editing surface tests

import { describe, it, expect, vi, beforeEach } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { Timeline } from "../Timeline";

const compile = { mutate: vi.fn(), isPending: false, isError: false, error: null };
const execute = { mutate: vi.fn(), isPending: false, isError: false, error: null, data: null };

vi.mock("../../../hooks/useRevision", () => ({
  useNativeEdit: () => ({ compile, execute }),
}));

const mockTimeline = {
  projection_id: "timeline:campaign-123:1",
  video_edit_program_ref: { object_id: "studio-campaign-state:campaign-123", sha256: "a".repeat(64), version: "1.0.0" },
  state: "NATIVE_EDITABLE_CANONICAL_PROGRAM",
  width: 1920, height: 1080, fps_numerator: 30, fps_denominator: 1, duration_frames: 100,
  tracks: [{
    track_id: "track-001", track_type: "VIDEO", role: "PRIMARY", z_index: 0, item_ids: ["item-001"],
    items: [{ item_id: "item-001", track_id: "track-001", kind: "VIDEO_CLIP", role: "PRIMARY", start_frame: 0, end_frame: 50, editable_operations: ["ADJUST_TIMING", "SUBSTITUTE_ASSET"], source_ref: { object_id: "asset-old", version: "1.0.0", sha256: "b".repeat(64) } }],
  }],
  items: [{ item_id: "item-001", track_id: "track-001", kind: "VIDEO_CLIP", role: "PRIMARY", start_frame: 0, end_frame: 50, editable_operations: ["ADJUST_TIMING", "SUBSTITUTE_ASSET"], source_ref: { object_id: "asset-old", version: "1.0.0", sha256: "b".repeat(64) } }],
};

beforeEach(() => { compile.mutate.mockReset(); execute.mutate.mockReset(); });

describe("Timeline native editor", () => {
  it("renders the editable canonical state", () => {
    render(<Timeline campaignId="campaign-123" timeline={mockTimeline} stateVersion={1} />);
    expect(screen.getByText("Native Timeline Editor")).toBeInTheDocument();
    expect(screen.getByText(/persisted to canonical campaign state/)).toBeInTheDocument();
  });

  it("requires an explicit selection before edit controls appear", () => {
    render(<Timeline campaignId="campaign-123" timeline={mockTimeline} stateVersion={1} />);
    expect(screen.queryByText("Adjust timing")).not.toBeInTheDocument();
  });

  it("previews a bounded timing change without auto-executing it", () => {
    render(<Timeline campaignId="campaign-123" timeline={mockTimeline} stateVersion={1} />);
    fireEvent.click(screen.getByRole("button", { name: /Edit item-001/ }));
    fireEvent.change(screen.getByLabelText("Timing delta frames"), { target: { value: "15" } });
    fireEvent.click(screen.getByRole("button", { name: "Adjust timing" }));
    expect(compile.mutate).toHaveBeenCalledTimes(1);
    expect(execute.mutate).not.toHaveBeenCalled();
    expect(screen.getByText("Adjust timing")).toBeInTheDocument();
  });

  it("supports asset substitution only with a real SHA-256", () => {
    render(<Timeline campaignId="campaign-123" timeline={mockTimeline} stateVersion={1} />);
    fireEvent.click(screen.getByRole("button", { name: /Edit item-001/ }));
    const substitute = screen.getByRole("button", { name: "Substitute asset" });
    expect(substitute).toBeDisabled();
    fireEvent.change(screen.getByLabelText("Replacement asset ID"), { target: { value: "asset-new" } });
    fireEvent.change(screen.getByLabelText("Replacement asset SHA256"), { target: { value: "c".repeat(64) } });
    expect(substitute).not.toBeDisabled();
    fireEvent.click(substitute);
    expect(compile.mutate).toHaveBeenCalledTimes(1);
  });

  it("executes only after a compiled program is explicitly confirmed", () => {
    compile.mutate.mockImplementation((_input, options) => options.onSuccess({ program_id: "revision:001", interpretation: "bounded timing edit" }));
    render(<Timeline campaignId="campaign-123" timeline={mockTimeline} stateVersion={1} />);
    fireEvent.click(screen.getByRole("button", { name: /Edit item-001/ }));
    fireEvent.change(screen.getByLabelText("Timing delta frames"), { target: { value: "10" } });
    fireEvent.click(screen.getByRole("button", { name: "Adjust timing" }));
    expect(execute.mutate).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "Confirm & Save" }));
    expect(execute.mutate).toHaveBeenCalledWith("revision:001");
  });
});
