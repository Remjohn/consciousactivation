import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { apiFetch } from "./http";
import { ApiError } from "./ApiError";

describe("apiFetch", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("throws ApiError with status null on network failure", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockRejectedValue(new TypeError("network down"));

    await expect(apiFetch("/api/health")).rejects.toMatchObject(
      new ApiError("Network request failed — is the gateway running?", null, null),
    );
  });

  it("throws ApiError with parsed error_code on a typed 4xx/5xx body", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: false,
      status: 503,
      json: async () => ({
        error_code: "SERVICE_DEGRADED",
        message: "one or more services degraded",
        service: "vae",
        timestamp: "2026-07-27T00:00:00Z",
      }),
    });

    await expect(apiFetch("/api/health")).rejects.toMatchObject({
      status: 503,
      errorCode: "SERVICE_DEGRADED",
      service: "vae",
    });
  });

  it("returns parsed JSON on 200", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ status: "ok" }),
    });

    await expect(apiFetch("/api/health")).resolves.toEqual({ status: "ok" });
  });
});
