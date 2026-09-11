import { render, screen } from "@testing-library/react";
import { describe, it, expect, beforeAll } from "vitest";
import { setupServer } from "msw/node";
import { handlers } from "../../test/handlers";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { HarnessPicker } from "./HarnessPicker";

// AC-008

const server = setupServer(...handlers);

beforeAll(() => server.listen());

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  );
}

describe("HarnessPicker", () => {
  it("AC-008: Format 02 harness is disabled (format02_harness_is_disabled)", async () => {
    renderWithQuery(<HarnessPicker onSelect={() => {}} />);

    // Wait for harnesses to load
    await screen.findByTestId("harness-picker");

    // The 2d_character_animation harness should be disabled
    const deferredBadge = screen.getByTestId("harness-deferred-harness:2d_anim_001");
    expect(deferredBadge).toHaveTextContent("Deferred");

    // The card button should be disabled
    const card = deferredBadge.closest("button");
    expect(card).toBeDisabled();
  });

  it("generic mode harness is disabled", async () => {
    renderWithQuery(<HarnessPicker onSelect={() => {}} />);

    await screen.findByTestId("harness-picker");

    const genericDeferred = screen.getByTestId("harness-deferred-harness:generic_001");
    expect(genericDeferred).toHaveTextContent("Deferred");
  });
});
