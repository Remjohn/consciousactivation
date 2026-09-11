import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { DevOperatorProvider } from "../../auth/DevOperatorContext";
import { InterviewsComposePage } from "./compose";

describe("interviews/compose route", () => {
  it("renders the correct title and FR range", () => {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    render(
      <QueryClientProvider client={queryClient}>
        <DevOperatorProvider>
          <InterviewsComposePage />
        </DevOperatorProvider>
      </QueryClientProvider>,
    );
    expect(screen.getByText("Interview Composer")).toBeInTheDocument();
    expect(screen.getByText(/FR-APP-010/)).toBeInTheDocument();
  });
});
