// TS-APP-UI-003 - usePipelineStatus hook
// WebSocket connection to /api/campaigns/{id}/status with REST fallback

import { useState, useEffect, useRef } from "react";
import type { CoarseNodeState } from "../lib/nodeState";
import { coarseFromWsState } from "../lib/nodeState";

const WS_BASE = import.meta.env.VITE_WS_BASE_URL ?? window.location.origin.replace("http", "ws");

export type ConnectionState = "connecting" | "open" | "closed" | "errored" | "no_run" | "multiple_runs";

export interface UsePipelineStatusOptions {
  onDirty: () => void;
}

export interface UsePipelineStatusResult {
  connectionState: ConnectionState;
  nodeVisual: Map<string, CoarseNodeState>;
}

export function usePipelineStatus(
  campaignId: string,
  opts: UsePipelineStatusOptions
): UsePipelineStatusResult {
  const [connectionState, setConnectionState] = useState<ConnectionState>("connecting");
  const [nodeVisual, setNodeVisual] = useState<Map<string, CoarseNodeState>>(new Map());
  const socketRef = useRef<WebSocket | null>(null);
  const backoffMsRef = useRef(1000);
  const stoppedRef = useRef(false);

  useEffect(() => {
    stoppedRef.current = false;
    backoffMsRef.current = 1000;

    function connect() {
      if (stoppedRef.current) return;

      const wsUrl = `${WS_BASE}/api/campaigns/${campaignId}/status`;
      const socket = new WebSocket(wsUrl);
      socketRef.current = socket;

      socket.onopen = () => {
        setConnectionState("open");
        backoffMsRef.current = 1000; // Reset backoff on successful connection
      };

      socket.onmessage = (evt: MessageEvent) => {
        try {
          const msg = JSON.parse(evt.data);

          switch (msg.type) {
            case "snapshot":
              // Initialize all nodes from snapshot
              setNodeVisual(
                new Map(
                  msg.run.nodes.map((n: { node_id: string; state: string }) => [
                    n.node_id,
                    coarseFromWsState(n.state),
                  ])
                )
              );
              break;

            case "node_state_changed":
              // Update single node visual state
              setNodeVisual((prev) => {
                const next = new Map(prev);
                next.set(msg.node.node_id, coarseFromWsState(msg.node.state));
                return next;
              });
              break;

            case "run_state_changed":
              // Invalidate tower data
              opts.onDirty();
              break;

            case "run_terminal":
              // Run completed or terminated - invalidate tower
              opts.onDirty();
              break;

            default:
              console.warn(`[usePipelineStatus] Unknown message type: ${msg.type}`);
          }
        } catch (err) {
          console.error("[usePipelineStatus] Failed to parse message:", err);
        }
      };

      socket.onclose = (evt: CloseEvent) => {
        if (stoppedRef.current) return;

        // Handle special close codes (TS-APP-API-005)
        if (evt.code === 4404) {
          setConnectionState("no_run");
          return; // Do not reconnect
        }
        if (evt.code === 4409) {
          setConnectionState("multiple_runs");
          return; // Do not reconnect
        }

        setConnectionState("closed");

        // Exponential backoff reconnection
        backoffMsRef.current = Math.min(backoffMsRef.current * 2, 15000);
        setTimeout(connect, backoffMsRef.current);
      };

      socket.onerror = () => {
        setConnectionState("errored");
      };
    }

    connect();

    return () => {
      stoppedRef.current = true;
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [campaignId, opts.onDirty]);

  return { connectionState, nodeVisual };
}
