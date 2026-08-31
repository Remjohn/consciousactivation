import React, { useState, useRef, useEffect } from "react";
import { sendChatCommand, type ChatCommandResult, type ProgramExecutionSummary } from "../../api/operator";

interface ChatMessage {
  id: string;
  sender: "operator" | "system";
  text: string;
  result?: ChatCommandResult;
  timestamp: string;
  isError?: boolean;
}

interface ChatSupervisionConsoleProps {
  workspaceId: string;
  activeExecution?: ProgramExecutionSummary | null;
  onStateMutated?: () => void;
}

const QUICK_COMMANDS = [
  { label: "/discover", cmd: "/discover" },
  { label: "/inspect", cmd: "/inspect" },
  { label: "/pause", cmd: "/pause" },
  { label: "/resume", cmd: "/resume" },
  { label: "/approve", cmd: '/approve gate_id="HUMAN_GATE" decision="APPROVE"' },
  { label: "/reject", cmd: '/reject gate_id="HUMAN_GATE" route="RETURN_TO_HUNTER" reason="Revision needed"' },
  { label: "/lineage", cmd: "/export-audit format=json" },
];

export function ChatSupervisionConsole({
  workspaceId,
  activeExecution,
  onStateMutated,
}: ChatSupervisionConsoleProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "init",
      sender: "system",
      text: "Operator Supervision Terminal ready. All commands map strictly to authoritative CAE typed state mutations.",
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendCommand = async (cmdToSend?: string) => {
    const rawCmd = (cmdToSend ?? inputText).trim();
    if (!rawCmd || isSubmitting) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: "operator",
      text: rawCmd,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!cmdToSend) setInputText("");
    setIsSubmitting(true);

    try {
      const result = await sendChatCommand({
        command: rawCmd,
        workspace_id: workspaceId,
        current_aggregate_id: activeExecution?.aggregate_id,
        expected_version: activeExecution?.version,
        expected_state_sha256: activeExecution?.state_hash,
      });

      const sysMsg: ChatMessage = {
        id: `sys-${Date.now()}`,
        sender: "system",
        text: result.message,
        result,
        timestamp: new Date().toLocaleTimeString(),
        isError: !result.success,
      };

      setMessages((prev) => [...prev, sysMsg]);

      // If command modified aggregate state, notify parent to refresh
      if (result.success && (result.state_version !== null || result.action_type === "RUN")) {
        onStateMutated?.();
      }
    } catch (err: any) {
      const errMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        sender: "system",
        text: `Command execution failed: ${err.message || String(err)}`,
        timestamp: new Date().toLocaleTimeString(),
        isError: true,
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendCommand();
    }
  };

  return (
    <div className="flex h-full flex-col rounded-lg border border-border bg-surface">
      {/* Console Header */}
      <div className="flex items-center justify-between border-b border-border px-4 py-2.5">
        <div className="flex items-center space-x-2">
          <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          <h3 className="text-xs font-semibold uppercase tracking-wider text-foreground">
            Chat Supervision Terminal
          </h3>
        </div>
        {activeExecution && (
          <div className="flex items-center space-x-2 text-xs">
            <span className="text-muted-foreground">Context:</span>
            <span className="font-mono text-foreground font-medium truncate max-w-[150px]">
              {activeExecution.program_id} (v{activeExecution.version})
            </span>
          </div>
        )}
      </div>

      {/* Quick Command Bar */}
      <div className="flex flex-wrap items-center gap-1.5 border-b border-border bg-surface-elevated/40 px-3 py-1.5">
        <span className="text-[11px] font-semibold text-muted-foreground mr-1">QUICK:</span>
        {QUICK_COMMANDS.map((qc) => (
          <button
            key={qc.label}
            onClick={() => handleSendCommand(qc.cmd)}
            disabled={isSubmitting}
            className="rounded bg-surface border border-border px-2 py-0.5 font-mono text-[11px] text-muted-foreground hover:border-accent hover:text-foreground transition-colors disabled:opacity-50"
          >
            {qc.label}
          </button>
        ))}
      </div>

      {/* Message Feed */}
      <div className="flex-1 space-y-3 overflow-y-auto p-4 max-h-[420px]">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex flex-col ${
              msg.sender === "operator" ? "items-end" : "items-start"
            }`}
          >
            <div className="flex items-center space-x-1.5 text-[10px] text-muted-foreground mb-1">
              <span className="font-semibold uppercase">{msg.sender}</span>
              <span>&bull;</span>
              <span>{msg.timestamp}</span>
            </div>

            <div
              className={`max-w-[85%] rounded-lg p-3 text-xs leading-relaxed ${
                msg.sender === "operator"
                  ? "bg-accent-solid text-accent-foreground font-mono"
                  : msg.isError
                  ? "bg-danger/10 border border-danger/30 text-danger"
                  : "bg-surface-elevated border border-border text-foreground"
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.text}</div>

              {msg.result && (
                <div className="mt-2.5 pt-2 border-t border-border/60 space-y-1 font-mono text-[11px]">
                  <div className="flex items-center space-x-2">
                    <span className="text-muted-foreground">Action:</span>
                    <span className="font-medium">{msg.result.action_type}</span>
                    <span className="text-muted-foreground">Lane:</span>
                    <span
                      className={`rounded px-1 text-[10px] uppercase ${
                        msg.result.lane === "COMMANDER"
                          ? "bg-purple-950/60 text-purple-300"
                          : "bg-blue-950/60 text-blue-300"
                      }`}
                    >
                      {msg.result.lane}
                    </span>
                  </div>

                  {msg.result.state_version !== null && (
                    <div className="text-muted-foreground">
                      State Version: <span className="text-foreground">{msg.result.state_version}</span>
                    </div>
                  )}

                  {msg.result.receipt_id && (
                    <div className="text-muted-foreground">
                      Receipt: <span className="text-accent">{msg.result.receipt_id}</span>
                    </div>
                  )}

                  {msg.result.warnings.length > 0 && (
                    <div className="text-amber-400">
                      Warnings: {msg.result.warnings.join(", ")}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <div className="border-t border-border p-3 bg-surface-elevated/20">
        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder='Type command (e.g. /run interview_semantic_program, /pause, /approve)...'
            disabled={isSubmitting}
            className="flex-1 rounded-md border border-border bg-surface px-3 py-2 font-mono text-xs text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50"
          />
          <button
            onClick={() => handleSendCommand()}
            disabled={isSubmitting || !inputText.trim()}
            className="rounded-md bg-accent-solid px-4 py-2 text-xs font-semibold text-accent-foreground hover:brightness-110 disabled:opacity-50 transition-all"
          >
            {isSubmitting ? "Running..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
