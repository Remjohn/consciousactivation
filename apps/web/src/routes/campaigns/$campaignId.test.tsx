import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from "vitest";
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";
import { renderWithRouter } from "../../test/renderWithRouter";
import { handlers } from "../../test/handlers";

/**
 * TS-APP-UI-003 — route test for the Control Tower page.
 *
 * The page is reached at `/campaigns/$campaignId` and replaces the UI-001
 * placeholder. Wave 4 Chat H's CampaignList/CampaignCard links here via
 *   <Link to="/campaigns/$campaignId" params={{ campaignId }} />
 * which is the link contract this route file must satisfy exactly (spec
 * Reconciliation 4 note).
 *
 * The real CampaignDetail mounts useControlTower (GET /tower) AND
 * usePipelineStatus, whose `useEffect` opens a `WebSocket` to
 * `/api/campaigns/{id}/status`. jsdom cannot service a real WS and the
 * unhandled connection crashes the vitest worker, so this test stubs
 * `global.WebSocket` with the same inert mock used by the
 * usePipelineStatus hook test (no reconnection, no network). Per-component
 * behaviour is covered by the control-tower component tests (AC-001..AC-013);
 * here we only assert the Control Tower page mounts and renders its hero once
 * GET /tower resolves.
 */

const TOWER_BODY = {
  campaign: { campaign_id: "camp-1", lifecycle_state: "RUNNING", autonomy_mode: "AUTOPILOT" },
  studio_binding: { primary_surface: "video-production" },
  order: { category_id: "short_form" },
  knowledge: {},
  runtime_health: [],
  artifacts: [],
  run_nodes: [],
  available_actions: [],
  exception_packages: [],
  timeline: null,
};

/** Inert WebSocket stub: records construction but never connects / reconnects. */
class StubWebSocket {
  static instances: StubWebSocket[] = [];
  onopen: ((e: Event) => void) | null = null;
  onmessage: ((e: MessageEvent) => void) | null = null;
  onclose: ((e: CloseEvent) => void) | null = null;
  onerror: ((e: Event) => void) | null = null;
  constructor(public url: string) {
    StubWebSocket.instances.push(this);
  }
  close() {}
  send() {}
}

const server = setupServer(
  ...handlers,
  http.get("/api/campaigns/:id/tower", () => HttpResponse.json(TOWER_BODY)),
);

beforeAll(() => {
  // vi.stubGlobal handles the read-only `WebSocket` global correctly and is
  // restored by vi.unstubAllGlobals in afterAll — direct assignment throws.
  vi.stubGlobal("WebSocket", StubWebSocket);
  server.listen();
});
afterEach(() => {
  StubWebSocket.instances = [];
  server.resetHandlers();
});
afterAll(() => {
  vi.unstubAllGlobals();
  server.close();
});

describe("campaigns/$campaignId route", () => {
  it("mounts the Control Tower page for a campaign", async () => {
    const { container, findByText } = renderWithRouter("/campaigns/camp-1");

    // The Control Tower page renders the "Run Progress" hero once the tower
    // projection loads. Waiting on it confirms the real CampaignDetail route
    // (not the old placeholder) is mounted and wired to GET /tower.
    expect(await findByText("Run Progress")).toBeInTheDocument();
    expect(container.querySelector(".control-tower-page")).not.toBeNull();
  });
});
