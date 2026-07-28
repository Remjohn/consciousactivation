import { useEffect, useRef, useState } from "react";

type ConnectionState = "idle" | "connecting" | "open" | "closed" | "error";

interface UseTypedWebSocketOptions {
  readonly enabled: boolean;
}

/**
 * Generic, reconnect-free WebSocket subscription. Deliberately does not retry —
 * the caller (e.g. TS-APP-UI-003's RunGraph) owns reconnect/backoff policy, since
 * TS-APP-API-005's close codes (4404/4409) mean "don't retry," not "retry."
 */
export function useTypedWebSocket<TMessage>(
  url: string | null,
  { enabled }: UseTypedWebSocketOptions,
) {
  const [state, setState] = useState<ConnectionState>("idle");
  const [lastMessage, setLastMessage] = useState<TMessage | null>(null);
  const [closeInfo, setCloseInfo] = useState<{ code: number; reason: string } | null>(null);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!enabled || !url) {
      setState("idle");
      return;
    }
    setState("connecting");
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => setState("open");
    socket.onmessage = (event) => {
      try {
        setLastMessage(JSON.parse(event.data) as TMessage);
      } catch {
        // malformed frame — ignored, connection stays open
      }
    };
    socket.onerror = () => setState("error");
    socket.onclose = (event) => {
      setState("closed");
      setCloseInfo({ code: event.code, reason: event.reason });
    };

    return () => socket.close();
  }, [url, enabled]);

  return { state, lastMessage, closeInfo };
}
