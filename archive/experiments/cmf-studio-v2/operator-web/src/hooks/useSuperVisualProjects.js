import { useCallback, useEffect, useState } from "react";
import { createSuperVisualProject, listSuperVisualProjects } from "../api/supervisualRuntime";
import { normalizeApiError } from "../lib/apiClient";

export function useSuperVisualProjects({ autoLoad = true } = {}) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(autoLoad);
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await listSuperVisualProjects();
      setProjects(result?.projects || result?.items || result || []);
      return result;
    } catch (err) {
      setError(normalizeApiError(err));
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const createProject = useCallback(async (payload) => {
    setError(null);
    const result = await createSuperVisualProject(payload);
    await refresh();
    return result;
  }, [refresh]);

  useEffect(() => {
    if (autoLoad) refresh().catch(() => {});
  }, [autoLoad, refresh]);

  return { projects, loading, error, refresh, createProject };
}
