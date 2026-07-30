import { describe, it, expect, beforeAll, afterAll, afterEach } from "vitest";
import { setupServer } from "msw/node";
import { renderWithRouter } from "../../test/renderWithRouter";
import { handlers } from "../../test/handlers";

/**
 * Route-level test for /campaigns/new (the new-campaign wizard).
 *
 * Originally a UI-001 placeholder test that imported a named
 * `CampaignsNewPage` export and rendered it in isolation. UI-002 replaced
 * the placeholder: new.tsx now registers a route whose component is the real
 * CampaignNew page and no longer exports that named symbol. Render the real
 * route tree via the shared renderWithRouter helper instead. Shared handlers
 * cover the wizard's calls; AppShell's TopBar also fires useHealth() →
 * /api/health, left to the default MSW "warn" behaviour.
 */

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("campaigns/new route", () => {
  it("renders the New Campaign wizard", async () => {
    const { findByText } = renderWithRouter("/campaigns/new");

    // CampaignNew's step-1 surface includes an "Existing Source" / import panel.
    expect(await findByText(/new campaign/i)).toBeInTheDocument();
  });
});
