import { useCallback, useEffect, useState } from "react";
import { getSuperVisualProject } from "../api/supervisualRuntime";
import { normalizeApiError } from "../lib/apiClient";

export function useSuperVisualProject(projectId) {
  const [projectDetail, setProjectDetail] = useState(null);
  const [loading, setLoading] = useState(Boolean(projectId));
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    if (!projectId) {
      setProjectDetail(null);
      setLoading(false);
      return null;
    }
    setLoading(true);
    setError(null);
    try {
      const result = await getSuperVisualProject(projectId);
      setProjectDetail(result);
      return result;
    } catch (err) {
      setError(normalizeApiError(err));
      throw err;
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    refresh().catch(() => {});
  }, [refresh]);

  return { projectDetail, loading, error, refresh };
}
