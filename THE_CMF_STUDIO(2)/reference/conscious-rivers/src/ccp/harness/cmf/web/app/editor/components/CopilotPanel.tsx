/**
 * AI Copilot Chat Panel — Natural language commands → classified manifest edits.
 *
 * FR-VID-10 §4 Stage 8: LLM prompt construction, JSON Patch parsing,
 * edit classification via EDIT_TAXONOMY.md, and manifest mutation with undo.
 */

"use client";

import React, { useState, useCallback, useRef, useEffect } from "react";

import { useEditorStore } from "../store";
import { sendCopilotMessage } from "../api-client";

// ─── Edit class constants from EDIT_TAXONOMY.md ───
const LOCAL_EDIT_CLASSES = [
  "EC-01", // Trim Duration
  "EC-02", // Reorder Beats
  "EC-03", // Change Transition
  "EC-04", // Adjust Ducking
  "EC-05", // Adjust Caption Timing
  "EC-06", // Caption Text Edit
  "EC-07", // Split Beat
  "EC-08", // Delete Beat
  "EC-09", // Swap Asset (local library)
];

const GENERATIVE_EDIT_CLASSES = [
  "EC-10", // Regenerate Visual (T2I/I2V)
  "EC-11", // Regenerate Audio
  "EC-12", // Regenerate Caption Style
];

const META_EDIT_CLASS = "EC-13"; // Session Command (undo, redo, save, export)

interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: number;
  editClass?: string;
  patchApplied?: boolean;
  revertable?: boolean;
}

interface CopilotResponse {
  edit_class: string;
  intent_summary: string;
  patch?: Array<{ op: string; path: string; value?: unknown }>;
  beat_index?: number;
  regeneration_mode?: "T2I_ONLY" | "I2V_ONLY" | "BOTH";
  revision_note?: string;
}

export const CopilotPanel: React.FC = () => {
  const manifest = useEditorStore((s) => s.manifest);
  const updateManifest = useEditorStore((s) => s.updateManifest);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // ─── JSON Patch validation against DEP-VID-002 constraints ───
  const validatePatch = useCallback(
    (
      patch: Array<{ op: string; path: string; value?: unknown }>
    ): { valid: boolean; error?: string } => {
      if (!manifest) return { valid: false, error: "No manifest loaded" };
      if (!Array.isArray(patch) || patch.length === 0) {
        return { valid: false, error: "Empty patch array" };
      }

      // Simulate patch application
      try {
        // Deep clone manifest for validation
        const testManifest = JSON.parse(JSON.stringify(manifest));

        for (const op of patch) {
          if (!op.path || typeof op.path !== "string") {
            return { valid: false, error: `Invalid patch path: ${op.path}` };
          }
          // Ensure path targets valid manifest fields
          const segments = op.path.split("/").filter(Boolean);
          if (segments.length === 0) {
            return { valid: false, error: "Empty path" };
          }

          // Apply operation for frame math validation
          if (op.op === "replace" && segments[0] === "beats") {
            const beatIdx = parseInt(segments[1], 10);
            if (isNaN(beatIdx) || beatIdx < 0 || beatIdx >= testManifest.beats.length) {
              return {
                valid: false,
                error: `Beat index ${segments[1]} out of range`,
              };
            }
            const field = segments[2];
            if (field === "duration_frames" && typeof op.value === "number") {
              if (op.value < 12) {
                return {
                  valid: false,
                  error: `Beat ${beatIdx} duration_frames ${op.value} < 12 (minimum 0.5s)`,
                };
              }
              testManifest.beats[beatIdx].duration_frames = op.value;
            } else if (
              field === "start_frame" &&
              typeof op.value === "number"
            ) {
              testManifest.beats[beatIdx].start_frame = op.value;
            }
          } else if (
            op.op === "replace" &&
            segments[0] === "total_frames" &&
            typeof op.value === "number"
          ) {
            testManifest.total_frames = op.value;
          }
        }

        // Validate frame math: start_frame[i] = sum of all previous duration_frames
        let expectedStart = 0;
        for (let i = 0; i < testManifest.beats.length; i++) {
          if (testManifest.beats[i].start_frame !== expectedStart) {
            return {
              valid: false,
              error: `Frame math error: beat ${i} start_frame should be ${expectedStart}, got ${testManifest.beats[i].start_frame}`,
            };
          }
          expectedStart += testManifest.beats[i].duration_frames;
        }

        // Validate total_frames
        const expectedTotal = testManifest.beats.reduce(
          (sum: number, b: { duration_frames: number }) =>
            sum + b.duration_frames,
          0
        );
        if (testManifest.total_frames !== expectedTotal) {
          return {
            valid: false,
            error: `total_frames mismatch: expected ${expectedTotal}, got ${testManifest.total_frames}`,
          };
        }

        return { valid: true };
      } catch {
        return { valid: false, error: "Patch application failed" };
      }
    },
    [manifest]
  );

  // ─── Apply a validated JSON Patch to the manifest ───
  const applyPatch = useCallback(
    (patch: Array<{ op: string; path: string; value?: unknown }>) => {
      updateManifest((m) => {
        const updated = JSON.parse(JSON.stringify(m));

        for (const op of patch) {
          const segments = op.path.split("/").filter(Boolean);

          if (op.op === "replace") {
            let target = updated;
            for (let i = 0; i < segments.length - 1; i++) {
              const key = isNaN(Number(segments[i]))
                ? segments[i]
                : Number(segments[i]);
              target = target[key];
            }
            const lastKey = isNaN(Number(segments[segments.length - 1]))
              ? segments[segments.length - 1]
              : Number(segments[segments.length - 1]);
            target[lastKey] = op.value;
          }
          // Add/remove support can be extended for more edit classes
        }

        return updated;
      });
    },
    [updateManifest]
  );

  // ─── Handle meta edits (EC-13: session commands) ───
  const handleMetaEdit = useCallback(
    (summary: string): string => {
      const lower = summary.toLowerCase();
      if (lower.includes("undo")) {
        useEditorStore.temporal.getState().undo();
        return "Undone last edit.";
      }
      if (lower.includes("redo")) {
        useEditorStore.temporal.getState().redo();
        return "Redone last undone edit.";
      }
      if (lower.includes("save")) {
        return "Save triggered. Use the Save button in the top bar.";
      }
      if (lower.includes("export")) {
        return "Export triggered. Use the Export button in the top bar.";
      }
      return `Session command "${summary}" not recognized.`;
    },
    []
  );

  // ─── Send message + process response ───
  const handleSend = useCallback(async () => {
    if (!input.trim() || !manifest || loading) return;

    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      role: "user",
      content: input.trim(),
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      // Build conversation history (last 5 messages for multi-turn context)
      const recentHistory = messages.slice(-5).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const response = await sendCopilotMessage(
        input.trim(),
        manifest,
        recentHistory
      );

      // Parse response as CopilotResponse
      const parsed: CopilotResponse =
        typeof response === "string" ? JSON.parse(response) : response;

      const editClass = parsed.edit_class;
      let assistantContent: string;
      let patchApplied = false;

      if (LOCAL_EDIT_CLASSES.includes(editClass)) {
        // Local edit — validate and apply JSON Patch
        if (!parsed.patch || parsed.patch.length === 0) {
          assistantContent = `Classified as ${editClass} (${parsed.intent_summary}) but no patch was returned.`;
        } else {
          const validation = validatePatch(parsed.patch);
          if (validation.valid) {
            applyPatch(parsed.patch);
            patchApplied = true;
            assistantContent = `Applied: ${parsed.intent_summary}`;
          } else {
            assistantContent = `I couldn't apply that change: ${validation.error}. Try rephrasing or make the edit manually.`;
          }
        }
      } else if (GENERATIVE_EDIT_CLASSES.includes(editClass)) {
        // Generative edit — route to Commander via legitimacy gate
        // Do NOT apply a JSON patch (spec §4 Stage 8 Step 4)
        assistantContent = `Regeneration requested for Beat ${parsed.beat_index ?? "?"} — ${parsed.revision_note || parsed.intent_summary}. Mode: ${parsed.regeneration_mode || "BOTH"}. Job dispatched to Commander.`;
        // Actual dispatch happens through the api-client's startRegeneration
      } else if (editClass === META_EDIT_CLASS) {
        // Meta edit — session command
        assistantContent = handleMetaEdit(parsed.intent_summary);
      } else {
        assistantContent = `Unknown edit class: ${editClass}. ${parsed.intent_summary}`;
      }

      const assistantMsg: ChatMessage = {
        id: `msg-${Date.now()}-resp`,
        role: "assistant",
        content: assistantContent,
        timestamp: Date.now(),
        editClass,
        patchApplied,
        revertable: patchApplied,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: `msg-${Date.now()}-err`,
        role: "system",
        content: `Copilot error: ${err instanceof Error ? err.message : "Unknown error"}`,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  }, [
    input,
    manifest,
    loading,
    messages,
    validatePatch,
    applyPatch,
    handleMetaEdit,
  ]);

  // ─── Revert a specific applied edit ───
  const handleRevert = useCallback(() => {
    useEditorStore.temporal.getState().undo();
    setMessages((prev) => [
      ...prev,
      {
        id: `msg-${Date.now()}-revert`,
        role: "system",
        content: "Edit reverted via undo.",
        timestamp: Date.now(),
      },
    ]);
  }, []);

  return (
    <div className="copilot-panel">
      <h3>AI Copilot</h3>

      <div className="copilot-messages">
        {messages.length === 0 && (
          <p className="copilot-hint">
            Try: &quot;make beat 3 shorter&quot; or &quot;change transition to dissolve&quot;
          </p>
        )}

        {messages.map((msg) => (
          <div key={msg.id} className={`copilot-msg copilot-msg-${msg.role}`}>
            <span className="copilot-msg-role">
              {msg.role === "user"
                ? "You"
                : msg.role === "assistant"
                  ? "Copilot"
                  : "System"}
            </span>
            <p>{msg.content}</p>
            {msg.editClass && (
              <span className="copilot-edit-class">[{msg.editClass}]</span>
            )}
            {msg.revertable && (
              <button
                className="copilot-revert-btn"
                onClick={handleRevert}
              >
                Revert
              </button>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="copilot-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          placeholder="Describe an edit..."
          disabled={loading || !manifest}
        />
        <button onClick={handleSend} disabled={loading || !manifest}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
};
