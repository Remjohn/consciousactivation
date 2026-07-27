import { useCallback, useEffect, useRef, useState } from "react";
import { getSuperVisualEvents } from "../api/supervisualRuntime";
import { normalizeApiError } from "../lib/apiClient";

export function useSuperVisualEvents(variantId, { poll = false, intervalMs = 5000 } = {}) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(Boolean(variantId));
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);

  const refresh = useCallback(async () => {
    if (!variantId) {
      setEvents([]);
      setLoading(false);
      return [];
    }
    setLoading(true);
    setError(null);
    try {
      const result = await getSuperVisualEvents(variantId);
      const nextEvents = result?.events || result?.items || result || [];
      setEvents(nextEvents);
      return nextEvents;
    } catch (err) {
      setError(normalizeApiError(err));
      throw err;
    } finally {
      setLoading(false);
    }
  }, [variantId]);

  useEffect(() => {
    refresh().catch(() => {});
  }, [refresh]);

  useEffect(() => {
    if (!poll || !variantId) return undefined;
    intervalRef.current = setInterval(() => {
      refresh().catch(() => {});
    }, intervalMs);
    return () => clearInterval(intervalRef.current);
  }, [poll, intervalMs, refresh, variantId]);

  return { events, loading, error, refresh };
}
