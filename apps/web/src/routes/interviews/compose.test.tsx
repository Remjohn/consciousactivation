import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { InterviewsComposePage } from "./compose";

describe("interviews/compose route", () => {
  it("renders the correct title and FR range", () => {
    render(<InterviewsComposePage />);
    expect(screen.getByText("Interview Composer")).toBeInTheDocument();
    expect(screen.getByText(/FR-APP-010\.\.012/)).toBeInTheDocument();
  });
});
