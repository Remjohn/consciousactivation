import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { BrandVoicePicker } from "./BrandVoicePicker";
import type { UploadedDocumentSummary } from "../../api/types";

describe("BrandVoicePicker", () => {
  const mockBrandAssets: UploadedDocumentSummary[] = [
    {
      asset_id: "ast-bv-1",
      original_filename: "audrey_brand_voice_guide.pdf",
      bytes: 20480,
      media_type: "application/pdf",
      sha256: "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
      context_class: "BRAND_VOICE",
    },
  ];

  it("renders verified BRAND_VOICE assets in dropdown and notifies on change", () => {
    const handleChange = vi.fn();

    render(
      <BrandVoicePicker
        availableBrandAssets={mockBrandAssets}
        value={null}
        rawJson=""
        onChange={handleChange}
      />
    );

    expect(screen.getByTestId("brand-voice-picker")).toBeInTheDocument();
    const select = screen.getByTestId("brand-voice-select");
    expect(select).toBeInTheDocument();

    fireEvent.change(select, { target: { value: "ast-bv-1" } });

    expect(handleChange).toHaveBeenCalledWith(
      {
        object_id: "ast-bv-1",
        version: "1",
        sha256: "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
      },
      JSON.stringify({
        object_id: "ast-bv-1",
        version: "1",
        sha256: "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
      })
    );
  });

  it("allows switching to manual JSON override mode", () => {
    const handleChange = vi.fn();

    render(
      <BrandVoicePicker
        availableBrandAssets={mockBrandAssets}
        value={null}
        rawJson=""
        onChange={handleChange}
      />
    );

    const toggleBtn = screen.getByTestId("brand-voice-mode-toggle");
    fireEvent.click(toggleBtn);

    const rawInput = screen.getByTestId("brand-context-ref-input");
    expect(rawInput).toBeVisible();

    fireEvent.change(rawInput, { target: { value: '{"object_id":"custom","version":"1","sha256":"abc"}' } });
    expect(handleChange).toHaveBeenCalled();
  });
});
