/**
 * CMF Editor Page — /editor/[videoId] route.
 *
 * FR-VID-10 §4 Stage 1: Editor shell with panel layout, manifest loading,
 * Zustand store initialization, IndexedDB auto-save, and Gate M enforcement.
 *
 * Gate M (Pre-Edit Constraint Network): Only opens for READY_FOR_REVIEW,
 * REGENERATING, or APPROVED pipeline states.
 */

"use client";

import React, { useCallback, useEffect, useRef, useState } from "react";

import { checkBackendHealth, fetchManifest } from "./api-client";
import {
  PreviewPanel,
  InspectorPanel,
  TimelineContainer,
  ReviewPanel,
  CopilotPanel,
  ExportModal,
} from "./components";
import {
  clearAutoSave,
  loadFromIndexedDB,
  startAutoSave,
  stopAutoSave,
  useEditorStore,
} from "./store";

// ---------------------------------------------------------------------------
// Gate M — Pipeline State Gating (FR-VID-10 §6 Gate M Q1)
// ---------------------------------------------------------------------------

const ALLOWED_STATES = new Set([
  "READY_FOR_REVIEW",
  "REGENERATING",
  "APPROVED",
]);

// ---------------------------------------------------------------------------
// Editor Page Component
// ---------------------------------------------------------------------------

interface EditorPageProps {
  params: { videoId: string };
}

export default function EditorPage({ params }: EditorPageProps) {
  const { videoId } = params;
  const store = useEditorStore();
  const [showExport, setShowExport] = useState(false);
  const [restorePrompt, setRestorePrompt] = useState<{
    savedAt: string;
  } | null>(null);
  const [backendOnline, setBackendOnline] = useState(true);
  const [gateError, setGateError] = useState<string | null>(null);
  const initRef = useRef(false);

  // -----------------------------------------------------------------------
  // Initialization — FR-VID-10 §4 Stage 1 Steps 1-6
  // -----------------------------------------------------------------------
  useEffect(() => {
    if (initRef.current) return;
    initRef.current = true;

    async function init() {
      store.setLoading(true);
      store.setError(null);

      // Gate M Q6: Backend connectivity check
      const healthy = await checkBackendHealth();
      setBackendOnline(healthy);

      try {
        // Stage 1 Step 2: Fetch manifest from backend
        const manifest = await fetchManifest(videoId);

        // Gate M Q1: Pipeline state validity check
        // (Pipeline state is usually sent alongside the manifest or fetched separately)
        const pipelineState = (manifest as Record<string, unknown>).pipeline_state as string || "READY_FOR_REVIEW";
        if (!ALLOWED_STATES.has(pipelineState)) {
          setGateError(
            `Video is still in "${pipelineState}" state — editor available after review stage.`
          );
          store.setLoading(false);
          return;
        }
        store.setPipelineState(pipelineState);

        // Gate M Q2: Manifest schema compliance (basic structural check)
        if (
          !manifest.beats ||
          !Array.isArray(manifest.beats) ||
          !manifest.fps ||
          !manifest.width ||
          !manifest.height
        ) {
          setGateError(
            "Manifest failed schema validation — missing required fields (beats, fps, width, height)."
          );
          store.setLoading(false);
          return;
        }

        // Gate M Q3: Asset availability check (check first few assets)
        const missingAssets = manifest.beats.filter(
          (b) => b.asset_status !== "RESOLVED" && !b.fallback_image_url
        );
        if (missingAssets.length > 0) {
          console.warn(
            `${missingAssets.length} beats have unresolved assets — editor will show placeholders.`
          );
        }

        // Gate M Q4: Audio file availability (warn if missing)
        if (!manifest.audio?.voiceover_path && !manifest.audio?.music_path) {
          console.warn(
            "No audio files referenced in manifest — preview will be silent."
          );
        }

        // Gate M Q5: Caption data presence (warn if missing)
        if (!manifest.captions || manifest.captions.length === 0) {
          console.warn(
            "Captions not yet generated — caption track will be empty."
          );
        }

        // Stage 1 Step 4: Check IndexedDB for existing auto-save
        const autoSaved = await loadFromIndexedDB(videoId);
        if (autoSaved && autoSaved.savedAt > (manifest as Record<string, unknown>).updated_at as string) {
          setRestorePrompt({ savedAt: autoSaved.savedAt });
          // Store server manifest initially — user decides
          store.setManifest(manifest);
        } else {
          // Stage 1 Step 3: Initialize Zustand store
          store.setManifest(manifest);
        }

        // Initialize beat reviews from manifest
        const reviews = manifest.beats.map((beat) => ({
          beat_index: beat.beat_index,
          status: "PENDING_REVIEW" as const,
          quality_score: 0,
          regen_count: 0,
        }));
        store.setBeatReviews(reviews);

        // Stage 1 Step 6: Start auto-save
        startAutoSave(videoId);
      } catch (err) {
        store.setError(
          err instanceof Error ? err.message : "Failed to load manifest"
        );
      } finally {
        store.setLoading(false);
      }
    }

    init();

    return () => {
      stopAutoSave();
    };
  }, [videoId]); // eslint-disable-line react-hooks/exhaustive-deps

  // -----------------------------------------------------------------------
  // Auto-save restore handlers
  // -----------------------------------------------------------------------
  const handleRestore = useCallback(async () => {
    const autoSaved = await loadFromIndexedDB(videoId);
    if (autoSaved) {
      store.setManifest(autoSaved.manifest);
    }
    setRestorePrompt(null);
  }, [videoId, store]);

  const handleDiscard = useCallback(async () => {
    await clearAutoSave(videoId);
    setRestorePrompt(null);
  }, [videoId]);

  // -----------------------------------------------------------------------
  // Keyboard shortcuts — FR-VID-10 Task 10
  // -----------------------------------------------------------------------
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.ctrlKey || e.metaKey) && e.key === "z" && !e.shiftKey) {
        e.preventDefault();
        useEditorStore.temporal.getState().undo();
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "z" && e.shiftKey) {
        e.preventDefault();
        useEditorStore.temporal.getState().redo();
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        // Trigger explicit save via API
        store.markSaved();
      }
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [store]);

  // -----------------------------------------------------------------------
  // Gate M rejection
  // -----------------------------------------------------------------------
  if (gateError) {
    return (
      <div className="cmf-editor-gate-error">
        <div className="gate-error-content">
          <h2>Editor Unavailable</h2>
          <p>{gateError}</p>
        </div>
      </div>
    );
  }

  // -----------------------------------------------------------------------
  // Loading state
  // -----------------------------------------------------------------------
  if (store.isLoading) {
    return (
      <div className="cmf-editor-loading">
        <p>Loading editor…</p>
      </div>
    );
  }

  if (store.error) {
    return (
      <div className="cmf-editor-error">
        <h2>Error</h2>
        <p>{store.error}</p>
      </div>
    );
  }

  if (!store.manifest) return null;

  // -----------------------------------------------------------------------
  // Editor Shell Layout — FR-VID-10 §4 Stage 1 Step 5
  // -----------------------------------------------------------------------
  return (
    <div className="cmf-editor">
      {/* Auto-save restore prompt */}
      {restorePrompt && (
        <div className="cmf-editor-restore-banner">
          <p>
            Unsaved changes found from {restorePrompt.savedAt}. Restore?
          </p>
          <button onClick={handleRestore}>Restore</button>
          <button onClick={handleDiscard}>Discard</button>
        </div>
      )}

      {/* Backend offline banner — Gate M Q6 */}
      {!backendOnline && (
        <div className="cmf-editor-offline-banner">
          Pipeline offline — edits saved locally, regeneration unavailable.
        </div>
      )}

      {/* Top bar */}
      <header className="cmf-editor-topbar">
        <div className="topbar-left">
          <h1>{store.manifest.video_id}</h1>
          <span className="pipeline-badge">{store.pipelineState}</span>
          {store.session.dirty && <span className="dirty-indicator">●</span>}
        </div>
        <div className="topbar-actions">
          <button
            onClick={() => useEditorStore.temporal.getState().undo()}
            title="Undo (Ctrl+Z)"
          >
            ↩ Undo
          </button>
          <button
            onClick={() => useEditorStore.temporal.getState().redo()}
            title="Redo (Ctrl+Shift+Z)"
          >
            ↪ Redo
          </button>
          <button onClick={() => store.markSaved()}>💾 Save</button>
          <button onClick={() => setShowExport(true)}>📤 Export</button>
        </div>
      </header>

      {/* Main content area */}
      <div className="cmf-editor-main">
        {/* Center-left: Preview player (Stage 2) */}
        <div className="cmf-editor-preview">
          <PreviewPanel manifest={store.manifest} />
        </div>

        {/* Center-right: Inspector panel */}
        {store.session.panel_layout.inspector_visible && (
          <div className="cmf-editor-inspector">
            <InspectorPanel />
          </div>
        )}

        {/* Right sidebar: Tabbed panels */}
        <div className="cmf-editor-sidebar">
          {store.session.panel_layout.review_panel_visible && (
            <ReviewPanel videoId={videoId} />
          )}
          {store.session.panel_layout.copilot_visible && (
            <CopilotPanel videoId={videoId} />
          )}
        </div>
      </div>

      {/* Bottom: Multi-track timeline (Stage 3) */}
      <div className="cmf-editor-timeline">
        <TimelineContainer />
      </div>

      {/* Export modal (Stage 7) */}
      {showExport && (
        <ExportModal
          videoId={videoId}
          onClose={() => setShowExport(false)}
        />
      )}
    </div>
  );
}
