/**
 * Typed API client for /api/v1/workspaces.
 * Governed by SPEC-TWC-UI-001, TS-CAE-TEN-001, and TS-APP-API-004 §5.
 */

import { ApiError } from "./ApiError";
import { apiFetch } from "./http";

export type WorkspaceRole = "ADMIN" | "MEMBER" | "VIEWER";
export type WorkspaceStatus = "ACTIVE" | "SUSPENDED" | "ARCHIVED";

export interface Workspace {
  workspace_id: string;
  slug: string;
  display_name: string;
  status: WorkspaceStatus;
  created_at: string;
  updated_at: string;
  receipt_id: string;
}

export interface WorkspaceMembership {
  membership_id: string;
  workspace_id: string;
  actor_id: string;
  role: WorkspaceRole;
  status: "ACTIVE" | "REVOKED";
  created_at: string;
  updated_at?: string | null;
  receipt_id: string;
}

export interface OperatorGrant {
  grant_id: string;
  operator_org_id: string;
  workspace_id: string;
  operator_actor_id: string;
  justification: string;
  expires_at: string;
  revoked_at?: string | null;
  created_at: string;
  receipt_id: string;
}

export interface CreateWorkspacePayload {
  slug: string;
  display_name: string;
}

export interface UpdateWorkspacePayload {
  display_name?: string;
  status?: WorkspaceStatus;
}

export interface AddMembershipPayload {
  actor_id: string;
  role: WorkspaceRole;
}

export interface IssueOperatorGrantPayload {
  operator_org_id: string;
  operator_actor_id: string;
  justification: string;
  expires_at: string;
}

export interface TenantHeaders {
  actor_id?: string;
  workspace_id?: string;
  role?: string;
  is_operator?: boolean;
  operator_grant_id?: string;
}

function buildHeaders(headers?: TenantHeaders): HeadersInit {
  const h: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (headers?.actor_id) {
    h["X-Actor-Id"] = headers.actor_id;
  }
  if (headers?.workspace_id) {
    h["X-Workspace-Id"] = headers.workspace_id;
  }
  if (headers?.role) {
    h["X-Role"] = headers.role;
  }
  if (headers?.is_operator !== undefined) {
    h["X-Is-Operator"] = headers.is_operator ? "true" : "false";
  }
  if (headers?.operator_grant_id) {
    h["X-Operator-Grant-Id"] = headers.operator_grant_id;
  }
  return h;
}

/**
 * Provision a new workspace via POST /api/v1/workspaces
 */
export async function createWorkspace(
  payload: CreateWorkspacePayload,
  headers?: TenantHeaders,
): Promise<Workspace> {
  return apiFetch<Workspace>("/api/v1/workspaces", {
    method: "POST",
    headers: buildHeaders(headers),
    body: JSON.stringify(payload),
  });
}

/**
 * Get workspace details via GET /api/v1/workspaces/{workspace_id}
 */
export async function getWorkspace(
  workspaceId: string,
  headers?: TenantHeaders,
): Promise<Workspace> {
  return apiFetch<Workspace>(`/api/v1/workspaces/${encodeURIComponent(workspaceId)}`, {
    method: "GET",
    headers: buildHeaders(headers),
  });
}

/**
 * List workspaces via GET /api/v1/workspaces
 */
export async function listWorkspaces(
  headers?: TenantHeaders,
): Promise<Workspace[]> {
  return apiFetch<Workspace[]>("/api/v1/workspaces", {
    method: "GET",
    headers: buildHeaders(headers),
  });
}

/**
 * List workspace memberships via GET /api/v1/workspaces/{workspace_id}/memberships
 */
export async function listWorkspaceMemberships(
  workspaceId: string,
  headers?: TenantHeaders,
): Promise<WorkspaceMembership[]> {
  return apiFetch<WorkspaceMembership[]>(
    `/api/v1/workspaces/${encodeURIComponent(workspaceId)}/memberships`,
    {
      method: "GET",
      headers: buildHeaders(headers),
    },
  );
}

/**
 * Update workspace settings via PATCH /api/v1/workspaces/{workspace_id}
 */
export async function updateWorkspace(
  workspaceId: string,
  payload: UpdateWorkspacePayload,
  headers?: TenantHeaders,
): Promise<Workspace> {
  return apiFetch<Workspace>(`/api/v1/workspaces/${encodeURIComponent(workspaceId)}`, {
    method: "PATCH",
    headers: buildHeaders(headers),
    body: JSON.stringify(payload),
  });
}

/**
 * Add a member to workspace via POST /api/v1/workspaces/{workspace_id}/memberships
 */
export async function addWorkspaceMembership(
  workspaceId: string,
  payload: AddMembershipPayload,
  headers?: TenantHeaders,
): Promise<WorkspaceMembership> {
  return apiFetch<WorkspaceMembership>(
    `/api/v1/workspaces/${encodeURIComponent(workspaceId)}/memberships`,
    {
      method: "POST",
      headers: buildHeaders(headers),
      body: JSON.stringify(payload),
    },
  );
}

/**
 * Revoke workspace membership via DELETE /api/v1/workspaces/{workspace_id}/memberships/{actor_id}
 */
export async function removeWorkspaceMembership(
  workspaceId: string,
  actorId: string,
  headers?: TenantHeaders,
): Promise<WorkspaceMembership> {
  return apiFetch<WorkspaceMembership>(
    `/api/v1/workspaces/${encodeURIComponent(workspaceId)}/memberships/${encodeURIComponent(actorId)}`,
    {
      method: "DELETE",
      headers: buildHeaders(headers),
    },
  );
}

/**
 * Issue an operator access grant via POST /api/v1/workspaces/{workspace_id}/operator-grants
 */
export async function issueOperatorGrant(
  workspaceId: string,
  payload: IssueOperatorGrantPayload,
  headers?: TenantHeaders,
): Promise<OperatorGrant> {
  return apiFetch<OperatorGrant>(
    `/api/v1/workspaces/${encodeURIComponent(workspaceId)}/operator-grants`,
    {
      method: "POST",
      headers: buildHeaders(headers),
      body: JSON.stringify(payload),
    },
  );
}

/**
 * Revoke an operator grant via DELETE /api/v1/workspaces/{workspace_id}/operator-grants/{grant_id}
 */
export async function revokeOperatorGrant(
  workspaceId: string,
  grantId: string,
  headers?: TenantHeaders,
): Promise<OperatorGrant> {
  return apiFetch<OperatorGrant>(
    `/api/v1/workspaces/${encodeURIComponent(workspaceId)}/operator-grants/${encodeURIComponent(grantId)}`,
    {
      method: "DELETE",
      headers: buildHeaders(headers),
    },
  );
}
