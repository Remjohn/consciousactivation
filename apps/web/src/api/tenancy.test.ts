import { describe, it, expect, beforeAll, afterEach, afterAll } from "vitest";
import { setupServer } from "msw/node";
import { handlers } from "../test/handlers";
import {
  createWorkspace,
  getWorkspace,
  listWorkspaces,
  updateWorkspace,
  addWorkspaceMembership,
  removeWorkspaceMembership,
  issueOperatorGrant,
  revokeOperatorGrant,
} from "./tenancy";
import { ApiError } from "./ApiError";

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("Tenancy API Client (api/tenancy.ts)", () => {
  it("creates a new workspace via POST /api/v1/workspaces", async () => {
    const ws = await createWorkspace({
      slug: "new-corp",
      display_name: "New Corp",
    });

    expect(ws.workspace_id).toBeDefined();
    expect(ws.slug).toBe("new-corp");
    expect(ws.display_name).toBe("New Corp");
    expect(ws.status).toBe("ACTIVE");
    expect(ws.receipt_id).toBeDefined();
  });

  it("handles 409 conflict when workspace slug already exists", async () => {
    await expect(
      createWorkspace({
        slug: "duplicate-slug",
        display_name: "Duplicate Corp",
      }),
    ).rejects.toThrowError(ApiError);
  });

  it("gets workspace details via GET /api/v1/workspaces/:workspaceId", async () => {
    const ws = await getWorkspace("11111111-1111-1111-1111-111111111111");
    expect(ws.workspace_id).toBe("11111111-1111-1111-1111-111111111111");
    expect(ws.slug).toBe("acme-production");
    expect(ws.display_name).toBe("Acme Production");
  });

  it("throws 404 for unknown workspaceId", async () => {
    await expect(getWorkspace("not-found")).rejects.toThrowError(ApiError);
  });

  it("lists workspaces via GET /api/v1/workspaces", async () => {
    const list = await listWorkspaces();
    expect(list.length).toBeGreaterThanOrEqual(2);
    expect(list[0].slug).toBe("acme-production");
  });

  it("updates workspace via PATCH /api/v1/workspaces/:workspaceId", async () => {
    const updated = await updateWorkspace("11111111-1111-1111-1111-111111111111", {
      display_name: "Updated Acme Production",
      status: "ACTIVE",
    });

    expect(updated.display_name).toBe("Updated Acme Production");
  });

  it("adds workspace membership via POST /api/v1/workspaces/:workspaceId/memberships", async () => {
    const membership = await addWorkspaceMembership("11111111-1111-1111-1111-111111111111", {
      actor_id: "carol@acme.com",
      role: "MEMBER",
    });

    expect(membership.actor_id).toBe("carol@acme.com");
    expect(membership.role).toBe("MEMBER");
    expect(membership.status).toBe("ACTIVE");
    expect(membership.receipt_id).toBeDefined();
  });

  it("rejects duplicate membership with 409", async () => {
    await expect(
      addWorkspaceMembership("11111111-1111-1111-1111-111111111111", {
        actor_id: "duplicate-member@test.com",
        role: "MEMBER",
      }),
    ).rejects.toThrowError(ApiError);
  });

  it("revokes membership via DELETE /api/v1/workspaces/:workspaceId/memberships/:actorId", async () => {
    const revoked = await removeWorkspaceMembership("11111111-1111-1111-1111-111111111111", "alice@acme.com");
    expect(revoked.status).toBe("REVOKED");
    expect(revoked.actor_id).toBe("alice@acme.com");
  });

  it("issues and revokes operator grants", async () => {
    const grant = await issueOperatorGrant("11111111-1111-1111-1111-111111111111", {
      operator_org_id: "00000000-0000-0000-0000-000000000001",
      operator_actor_id: "op-support-lead",
      justification: "Diagnosing campaign pipeline exception",
      expires_at: new Date(Date.now() + 86400000).toISOString(),
    });

    expect(grant.grant_id).toBeDefined();
    expect(grant.operator_actor_id).toBe("op-support-lead");

    const revoked = await revokeOperatorGrant("11111111-1111-1111-1111-111111111111", grant.grant_id);
    expect(revoked.revoked_at).toBeDefined();
  });
});
