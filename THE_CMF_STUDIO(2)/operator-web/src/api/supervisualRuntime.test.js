import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import {
  createSuperVisualProject,
  getSuperVisualProject,
  listSuperVisualProjects,
} from "./supervisualRuntime";

describe("supervisualRuntime API client", () => {
  beforeEach(() => {
    global.fetch = vi.fn(async (url, options) => ({
      ok: true,
      headers: new Headers({ "content-type": "application/json" }),
      json: async () => ({ url, options, projects: [] }),
    }));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("lists projects from runtime API", async () => {
    await listSuperVisualProjects();
    expect(global.fetch).toHaveBeenCalledWith("/api/v1/supervisual/projects", expect.any(Object));
  });

  it("loads project detail route", async () => {
    await getSuperVisualProject("project_1");
    expect(global.fetch).toHaveBeenCalledWith("/api/v1/supervisual/projects/project_1", expect.any(Object));
  });

  it("sends idempotency key on project create", async () => {
    await createSuperVisualProject({
      title: "Test",
      brand_id: "brand_1",
      brand_context_version_id: "bcv_1",
    });
    const [, options] = global.fetch.mock.calls[0];
    const body = JSON.parse(options.body);
    expect(body.idempotency_key).toBeTruthy();
    expect(body.actor_id).toBeTruthy();
  });
});
