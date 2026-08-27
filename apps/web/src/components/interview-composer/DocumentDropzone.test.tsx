import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { DocumentDropzone, getTierLimitForFile, type ManagedFileItem } from "./DocumentDropzone";

describe("DocumentDropzone", () => {
  it("determines correct tiered limits based on file type", () => {
    const docFile = new File(["dummy content"], "bio.pdf", { type: "application/pdf" });
    const audioFile = new File(["dummy audio"], "interview.mp3", { type: "audio/mp3" });
    const wavFile = new File(["dummy wav"], "recording.wav", { type: "audio/wav" });
    const videoFile = new File(["dummy video"], "raw_footage.mp4", { type: "video/mp4" });
    const captionFile = new File(["WEBVTT\n00:00 -> 00:01\nHi"], "captions.vtt", { type: "text/vtt" });

    expect(getTierLimitForFile(docFile).limitBytes).toBe(50 * 1024 * 1024);
    expect(getTierLimitForFile(audioFile).limitBytes).toBe(500 * 1024 * 1024);
    expect(getTierLimitForFile(wavFile).limitBytes).toBe(1024 * 1024 * 1024);
    expect(getTierLimitForFile(videoFile).limitBytes).toBe(4 * 1024 * 1024 * 1024);
    expect(getTierLimitForFile(captionFile).limitBytes).toBe(10 * 1024 * 1024);
    expect(getTierLimitForFile(captionFile).defaultClass).toBe("CAPTION_TRACK");
  });

  it("renders uploaded files with context class and allows changing context class", () => {
    const handleChange = vi.fn();
    const items: ManagedFileItem[] = [
      {
        id: "item-1",
        file: new File(["content"], "notes.pdf", { type: "application/pdf" }),
        context_class: "EVIDENCE_SOURCE",
        sha256: "abcdef1234567890",
      },
    ];

    render(<DocumentDropzone items={items} onChange={handleChange} />);

    expect(screen.getByTestId("file-name")).toHaveTextContent("notes.pdf");
    expect(screen.getByTestId("file-sha256")).toHaveTextContent("abcdef1234567890");

    const select = screen.getByTestId("file-context-class");
    fireEvent.change(select, { target: { value: "BRAND_VOICE" } });

    expect(handleChange).toHaveBeenCalledWith([
      expect.objectContaining({
        id: "item-1",
        context_class: "BRAND_VOICE",
      }),
    ]);
  });

  it("renders caption target selector when context class is CAPTION_TRACK", () => {
    const handleChange = vi.fn();
    const items: ManagedFileItem[] = [
      {
        id: "rec-1",
        file: new File(["recording"], "master_recording.mp4", { type: "video/mp4" }),
        context_class: "INTERVIEW_RECORDING",
        sha256: "111111",
      },
      {
        id: "cap-1",
        file: new File(["captions"], "transcript.vtt", { type: "text/vtt" }),
        context_class: "CAPTION_TRACK",
        caption_for: null,
        sha256: "222222",
      },
    ];

    render(<DocumentDropzone items={items} onChange={handleChange} />);

    expect(screen.getByTestId("caption-binding-section")).toBeInTheDocument();
    const captionSelect = screen.getByTestId("file-caption-for");
    expect(captionSelect).toBeInTheDocument();

    fireEvent.change(captionSelect, { target: { value: "master_recording.mp4" } });
    expect(handleChange).toHaveBeenCalledWith([
      items[0],
      expect.objectContaining({
        id: "cap-1",
        caption_for: "master_recording.mp4",
      }),
    ]);
  });
});
