/**
 * Workspace Context Provider for tenant isolation and active workspace governance.
 * Governed by SPEC-TWC-UI-001, MC-CAE-WS-001, DEC-TWC-001, and TS-APP-API-004 §5.
 */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useQueryClient } from "@tanstack/react-query";
import { ApiError } from "../api/ApiError";
import {
  createWorkspace as apiCreateWorkspace,
  getWorkspace as apiGetWorkspace,
  listWorkspaces as apiListWorkspaces,
  updateWorkspace as apiUpdateWorkspace,
  type CreateWorkspacePayload,
  type TenantHeaders,
  type UpdateWorkspacePayload,
  type Workspace,
} from "../api/tenancy";
import { useOperator } from "../auth/DevOperatorContext";

const LOCAL_STORAGE_KEY = "ca_active_workspace_id";

export interface WorkspaceContextValue {
  readonly activeWorkspace: Workspace | null;
  readonly activeWorkspaceId: string | null;
  readonly workspaces: readonly Workspace[];
  readonly isLoading: boolean;
  readonly error: ApiError | Error | null;
  readonly selectWorkspace: (workspaceId: string) => void;
  readonly createNewWorkspace: (payload: CreateWorkspacePayload) => Promise<Workspace>;
  readonly updateActiveWorkspace: (payload: UpdateWorkspacePayload) => Promise<Workspace>;
  readonly refreshWorkspaces: () => Promise<void>;
  readonly clearError: () => void;
}

const WorkspaceContext = createContext<WorkspaceContextValue | null>(null);

export interface WorkspaceProviderProps {
  readonly children: ReactNode;
  readonly initialWorkspaceId?: string;
}

export function WorkspaceProvider({ children, initialWorkspaceId }: WorkspaceProviderProps) {
  const operator = useOperator();
  const queryClient = useQueryClient();

  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [activeWorkspaceId, setActiveWorkspaceIdState] = useState<string | null>(() => {
    if (initialWorkspaceId) return initialWorkspaceId;
    try {
      return localStorage.getItem(LOCAL_STORAGE_KEY);
    } catch {
      return null;
    }
  });
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | Error | null>(null);

  const activeWorkspace = useMemo(() => {
    return workspaces.find((w) => w.workspace_id === activeWorkspaceId) ?? null;
  }, [workspaces, activeWorkspaceId]);

  const tenantHeaders: TenantHeaders = useMemo(() => {
    return {
      actor_id: operator.actor_id,
      workspace_id: activeWorkspaceId || undefined,
      role: "ADMIN",
      is_operator: operator.workflow_role === "operator",
    };
  }, [operator, activeWorkspaceId]);

  // Invalidate downstream caches upon workspace switch to prevent cross-tenant data leakage (HN-TWC-04)
  const selectWorkspace = useCallback(
    (workspaceId: string) => {
      setActiveWorkspaceIdState(workspaceId);
      try {
        localStorage.setItem(LOCAL_STORAGE_KEY, workspaceId);
      } catch {
        // localStorage unavailable in some sandboxes
      }
      setError(null);

      // Invalidate and reset all queries for tenant-isolated resources
      queryClient.invalidateQueries({ queryKey: ["campaigns"] });
      queryClient.invalidateQueries({ queryKey: ["interviews"] });
      queryClient.invalidateQueries({ queryKey: ["harnesses"] });
      queryClient.invalidateQueries({ queryKey: ["memberships"] });
      queryClient.invalidateQueries({ queryKey: ["operator-grants"] });
    },
    [queryClient],
  );

  const refreshWorkspaces = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const list = await apiListWorkspaces(tenantHeaders);
      if (list && list.length > 0) {
        setWorkspaces(list);
        if (!activeWorkspaceId || !list.some((w) => w.workspace_id === activeWorkspaceId)) {
          selectWorkspace(list[0].workspace_id);
        }
      } else if (activeWorkspaceId) {
        try {
          const single = await apiGetWorkspace(activeWorkspaceId, tenantHeaders);
          setWorkspaces([single]);
        } catch {
          // If active workspace is not found, clear state
          setWorkspaces([]);
        }
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err);
      } else if (err instanceof Error) {
        setError(err);
      }
    } finally {
      setIsLoading(false);
    }
  }, [tenantHeaders, activeWorkspaceId, selectWorkspace]);

  // First-login auto-create deriving display name from account identity (DEC-TWC-001)
  useEffect(() => {
    let isMounted = true;

    async function initWorkspace() {
      setIsLoading(true);
      setError(null);
      try {
        let currentList: Workspace[] = [];
        try {
          currentList = await apiListWorkspaces(tenantHeaders);
        } catch {
          currentList = [];
        }

        // If saved active ID exists, attempt to fetch it directly
        if (activeWorkspaceId && currentList.length === 0) {
          try {
            const fetched = await apiGetWorkspace(activeWorkspaceId, tenantHeaders);
            if (isMounted) {
              setWorkspaces([fetched]);
              setIsLoading(false);
              return;
            }
          } catch {
            // saved ID invalid/stale
          }
        }

        if (currentList.length > 0) {
          if (isMounted) {
            setWorkspaces(currentList);
            if (!activeWorkspaceId || !currentList.some((w) => w.workspace_id === activeWorkspaceId)) {
              selectWorkspace(currentList[0].workspace_id);
            }
            setIsLoading(false);
          }
          return;
        }

        // Auto-create workspace derived from account identity (DEC-TWC-001)
        const accountName = operator.actor_id || "Operator";
        const derivedDisplayName = `${accountName}'s Workspace`;
        const sanitizedSlug = `ws-${accountName.toLowerCase().replace(/[^a-z0-9]/g, "-").replace(/-+/g, "-").slice(0, 30)}`;

        try {
          const created = await apiCreateWorkspace(
            { slug: sanitizedSlug, display_name: derivedDisplayName },
            { actor_id: operator.actor_id, is_operator: true },
          );
          if (isMounted) {
            setWorkspaces([created]);
            selectWorkspace(created.workspace_id);
          }
        } catch (createErr) {
          if (createErr instanceof ApiError && createErr.status === 409) {
            // Idempotent recovery on conflict (already created by another tab/session)
            const fallbackList = await apiListWorkspaces(tenantHeaders);
            if (isMounted && fallbackList.length > 0) {
              setWorkspaces(fallbackList);
              selectWorkspace(fallbackList[0].workspace_id);
            }
          } else {
            if (isMounted) {
              setError(createErr instanceof Error ? createErr : new Error("Failed to initialize workspace"));
            }
          }
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err : new Error("Failed to initialize tenant context"));
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    initWorkspace();

    return () => {
      isMounted = false;
    };
  }, [operator.actor_id]);

  const createNewWorkspace = useCallback(
    async (payload: CreateWorkspacePayload): Promise<Workspace> => {
      setError(null);
      try {
        const created = await apiCreateWorkspace(payload, {
          actor_id: operator.actor_id,
          is_operator: true,
        });
        setWorkspaces((prev) => [...prev.filter((w) => w.workspace_id !== created.workspace_id), created]);
        selectWorkspace(created.workspace_id);
        return created;
      } catch (err) {
        const normalized = err instanceof ApiError ? err : new Error(String(err));
        setError(normalized);
        throw normalized;
      }
    },
    [operator.actor_id, selectWorkspace],
  );

  const updateActiveWorkspace = useCallback(
    async (payload: UpdateWorkspacePayload): Promise<Workspace> => {
      if (!activeWorkspaceId) {
        throw new Error("No active workspace selected");
      }
      setError(null);
      try {
        const updated = await apiUpdateWorkspace(activeWorkspaceId, payload, tenantHeaders);
        setWorkspaces((prev) => prev.map((w) => (w.workspace_id === updated.workspace_id ? updated : w)));
        return updated;
      } catch (err) {
        const normalized = err instanceof ApiError ? err : new Error(String(err));
        setError(normalized);
        throw normalized;
      }
    },
    [activeWorkspaceId, tenantHeaders],
  );

  const clearError = useCallback(() => setError(null), []);

  const value: WorkspaceContextValue = useMemo(
    () => ({
      activeWorkspace,
      activeWorkspaceId,
      workspaces,
      isLoading,
      error,
      selectWorkspace,
      createNewWorkspace,
      updateActiveWorkspace,
      refreshWorkspaces,
      clearError,
    }),
    [
      activeWorkspace,
      activeWorkspaceId,
      workspaces,
      isLoading,
      error,
      selectWorkspace,
      createNewWorkspace,
      updateActiveWorkspace,
      refreshWorkspaces,
      clearError,
    ],
  );

  return <WorkspaceContext.Provider value={value}>{children}</WorkspaceContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export function useWorkspace(): WorkspaceContextValue {
  const context = useContext(WorkspaceContext);
  if (!context) {
    return {
      activeWorkspace: null,
      activeWorkspaceId: null,
      workspaces: [],
      isLoading: false,
      error: null,
      selectWorkspace: () => {},
      createNewWorkspace: async () => {
        throw new Error("WorkspaceProvider not mounted");
      },
      updateActiveWorkspace: async (_payload: UpdateWorkspacePayload): Promise<Workspace> => {
        throw new Error("WorkspaceProvider not mounted");
      },
      refreshWorkspaces: async () => {},
      clearError: () => {},
    };
  }
  return context;
}
