import { describe, it, expect, beforeAll, afterAll, afterEach } from "vitest";
import { setupServer } from "msw/node";
import { renderWithRouter } from "../../test/renderWithRouter";
import { handlers } from "../../test/handlers";

/**
 * Route-level test for /campaigns (the campaign list).
 *
 * Originally a UI-001 placeholder test that imported a named
 * `CampaignsIndexPage` export and rendered it in isolation. UI-002 replaced
 * the placeholder: index.tsx now registers a route whose component is the real
 * CampaignList page and no longer exports that named symbol. Render the real
 * route tree via the shared renderWithRouter helper instead (same pattern as
 * CampaignList.test.tsx). The shared handlers cover /api/campaigns; AppShell's
 * TopBar also fires useHealth() → /api/health, left to the default MSW
 * "warn" behaviour (proven harmless by the passing CampaignList test).
 */

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("campaigns/index route", () => {
  it("renders the Campaigns page heading", async () => {
    const { findByRole } = renderWithRouter("/campaigns");

    // The Campaigns <h1> heading is what identifies the page; the sidebar nav
    // also contains the text "Campaigns" (active link), so findByRole("heading")
    // disambiguates.
    expect(await findByRole("heading", { name: "Campaigns" })).toBeInTheDocument();
  });
});
