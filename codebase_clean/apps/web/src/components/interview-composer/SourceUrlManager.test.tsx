import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { SourceUrlManager } from "./SourceUrlManager";
import type { SourceUrlItem } from "../../api/types";

describe("SourceUrlManager", () => {
  it("renders empty state and adds a valid URL with context class", () => {
    const handleChange = vi.fn();
    const urls: SourceUrlItem[] = [];

    render(<SourceUrlManager urls={urls} onChange={handleChange} />);

    expect(screen.getByTestId("source-url-manager")).toBeInTheDocument();
    expect(screen.getByText("0 added")).toBeInTheDocument();

    const input = screen.getByTestId("source-url-input");
    const classSelect = screen.getByTestId("source-url-class-select");
    const addBtn = screen.getByTestId("source-url-add-btn");

    fireEvent.change(input, { target: { value: "https://en.wikipedia.org/wiki/Audrey_Hepburn" } });
    fireEvent.change(classSelect, { target: { value: "IDENTITY_DNA" } });
    fireEvent.click(addBtn);

    expect(handleChange).toHaveBeenCalledWith([
      {
        url: "https://en.wikipedia.org/wiki/Audrey_Hepburn",
        context_class: "IDENTITY_DNA",
      },
    ]);
  });

  it("rejects invalid URL formats with error message", () => {
    const handleChange = vi.fn();

    render(<SourceUrlManager urls={[]} onChange={handleChange} />);

    const input = screen.getByTestId("source-url-input");
    const addBtn = screen.getByTestId("source-url-add-btn");

    fireEvent.change(input, { target: { value: "not-a-valid-url" } });
    fireEvent.click(addBtn);

    expect(handleChange).not.toHaveBeenCalled();
    expect(screen.getByTestId("source-url-error")).toHaveTextContent(
      "Invalid URL format. Must start with http:// or https://"
    );
  });

  it("allows removing an existing URL", () => {
    const handleChange = vi.fn();
    const urls: SourceUrlItem[] = [
      { url: "https://example.com/1", context_class: "EVIDENCE_SOURCE" },
      { url: "https://example.com/2", context_class: "CONTEXT_PREMISE" },
    ];

    render(<SourceUrlManager urls={urls} onChange={handleChange} />);

    expect(screen.getByText("2 added")).toBeInTheDocument();
    const removeButtons = screen.getAllByTestId("source-url-remove-btn");
    expect(removeButtons).toHaveLength(2);

    fireEvent.click(removeButtons[0]);
    expect(handleChange).toHaveBeenCalledWith([urls[1]]);
  });
});
