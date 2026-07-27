import { useCallback, useEffect, useState } from "react";
import { getSuperVisualSnapshot } from "../api/supervisualRuntime";
import { normalizeApiError } from "../lib/apiClient";

export function useSuperVisualSnapshot(variantId, { autoLoad = true } = {}) {
  const [snapshot, setSnapshot] = useState(null);
  const [loading, setLoading] = useState(Boolean(variantId && autoLoad));
  const [error, setError] = useState(null);

  const refresh = useCallback(async () => {
    if (!variantId) {
      setSnapshot(null);
      setLoading(false);
      return null;
    }
    setLoading(true);
    setError(null);
    try {
      const result = await getSuperVisualSnapshot(variantId);
      setSnapshot(result?.snapshot || result);
      return result;
    } catch (err) {
      setError(normalizeApiError(err));
      throw err;
    } finally {
      setLoading(false);
    }
  }, [variantId]);

  useEffect(() => {
    if (autoLoad) refresh().catch(() => {});
  }, [autoLoad, refresh]);

  return { snapshot, loading, error, refresh, setSnapshot };
}
