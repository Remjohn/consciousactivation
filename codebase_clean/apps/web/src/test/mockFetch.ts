import { vi } from "vitest";

interface MockResponse {
  readonly status: number;
  readonly body: unknown;
}

/**
 * Builds a `fetch` mock that routes by EXACT request pathname, returning a fresh
 * `Response` per call (so `Response.body` is never read twice — the cause of the
 * "Body has already been read" failures when renderWithRouter's full AppShell
 * also fetched /api/health).
 *
 * Matching is on `new URL(input).pathname` ONLY — never `url.includes(pattern)`,
 * because "/api/harnesses/def-1" is a substring of "/api/harnesses/def-1/eligibility"
 * and would mis-route eligibility calls to the detail handler. An unregistered path
 * throws loudly so a missing mock never silently serves wrong-shape data to a route.
 */
export function createUrlRouter(handlers: Record<string, MockResponse>) {
  return vi.fn(async (input: RequestInfo | URL, _init?: RequestInit) => {
    const raw = typeof input === "string" ? input : input.toString();
    const pathname = new URL(raw, "http://localhost").pathname;
    const entry = handlers[pathname];
    if (!entry) {
      throw new Error(
        `Unhandled fetch pathname: ${pathname}\nRegistered: ${Object.keys(handlers).join(", ")}`,
      );
    }
    return new Response(JSON.stringify(entry.body), {
      status: entry.status,
      headers: { "Content-Type": "application/json" },
    });
  });
}
