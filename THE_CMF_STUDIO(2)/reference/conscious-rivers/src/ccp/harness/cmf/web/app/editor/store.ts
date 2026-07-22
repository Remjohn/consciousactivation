/**
 * CMF Editor Zustand Store — Manifest state, undo/redo, UI state, auto-save.
 *
 * FR-VID-10 §3 TD4: Zustand + temporal middleware for undo/redo (max 50 snapshots).
 * FR-VID-10 §3 TD1: Manifest IS the project file — single source of truth.
 * FR-VID-10 §4 Stage 1 Step 3: Initialize store with manifest, session metadata.
 * FR-VID-10 §4 Stage 1 Step 6: Auto-save to IndexedDB at 5-second interval.
 */

import { temporal } from "zundo";
import { create } from "zustand";

import type { CMFManifest } from "@cmf/remotion-compositions";

// ---------------------------------------------------------------------------
// Types — DEP-VID-028 Editor Session State
// ---------------------------------------------------------------------------

export interface EditorSessionState {
  session_id: string;
  video_id: string;
  pipeline_id: string;
  manifest_version: number;
  opened_at: string;
  last_save_at: string | null;
  last_auto_save_at: string | null;
  playhead_frame: number;
  selected_beat_index: number | null;
  selected_track: string;
  zoom_level: number;
  panel_layout: {
    inspector_visible: boolean;
    review_panel_visible: boolean;
    copilot_visible: boolean;
    timeline_height_px: number;
  };
  dirty: boolean;
  auto_save_enabled: boolean;
  auto_save_interval_ms: number;
}

export interface ReviewBeatState {
  beat_index: number;
  status: "PENDING_REVIEW" | "APPROVED" | "REGENERATING" | "REJECTED";
  quality_score: number;
  regen_count: number;
}

export interface EditorState {
  // Core manifest — THE authoritative state (FR-VID-10 §3 TD1)
  manifest: CMFManifest | null;

  // Session metadata (DEP-VID-028)
  session: EditorSessionState;

  // Review state (DEP-VID-027)
  beatReviews: ReviewBeatState[];

  // Pipeline state (DEP-VID-025)
  pipelineState: string;

  // Loading/error
  isLoading: boolean;
  error: string | null;

  // Actions — manifest mutations
  setManifest: (manifest: CMFManifest) => void;
  updateManifest: (updater: (manifest: CMFManifest) => CMFManifest) => void;

  // Actions — session state
  setPlayheadFrame: (frame: number) => void;
  setSelectedBeat: (index: number | null) => void;
  setSelectedTrack: (track: string) => void;
  setZoomLevel: (level: number) => void;
  togglePanel: (panel: "inspector" | "review" | "copilot") => void;
  markDirty: () => void;
  markSaved: () => void;
  markAutoSaved: () => void;

  // Actions — review
  setBeatReviews: (reviews: ReviewBeatState[]) => void;
  updateBeatReview: (index: number, status: ReviewBeatState["status"]) => void;
  setPipelineState: (state: string) => void;

  // Actions — loading
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

// ---------------------------------------------------------------------------
// Default session state
// ---------------------------------------------------------------------------

function createDefaultSession(videoId: string): EditorSessionState {
  return {
    session_id: `EDIT-${Date.now()}`,
    video_id: videoId,
    pipeline_id: "",
    manifest_version: 0,
    opened_at: new Date().toISOString(),
    last_save_at: null,
    last_auto_save_at: null,
    playhead_frame: 0,
    selected_beat_index: null,
    selected_track: "visual",
    zoom_level: 1.0,
    panel_layout: {
      inspector_visible: true,
      review_panel_visible: true,
      copilot_visible: false,
      timeline_height_px: 200,
    },
    dirty: false,
    auto_save_enabled: true,
    auto_save_interval_ms: 5000,
  };
}

// ---------------------------------------------------------------------------
// Store — FR-VID-10 §4 Stage 1 Step 3 + Task 10
// ---------------------------------------------------------------------------

export const useEditorStore = create<EditorState>()(
  temporal(
    (set) => ({
      manifest: null,
      session: createDefaultSession(""),
      beatReviews: [],
      pipelineState: "",
      isLoading: false,
      error: null,

      setManifest: (manifest) =>
        set((state) => ({
          manifest,
          session: {
            ...state.session,
            manifest_version: state.session.manifest_version + 1,
            dirty: true,
          },
        })),

      updateManifest: (updater) =>
        set((state) => {
          if (!state.manifest) return state;
          return {
            manifest: updater(state.manifest),
            session: {
              ...state.session,
              manifest_version: state.session.manifest_version + 1,
              dirty: true,
            },
          };
        }),

      setPlayheadFrame: (frame) =>
        set((state) => ({
          session: { ...state.session, playhead_frame: frame },
        })),

      setSelectedBeat: (index) =>
        set((state) => ({
          session: { ...state.session, selected_beat_index: index },
        })),

      setSelectedTrack: (track) =>
        set((state) => ({
          session: { ...state.session, selected_track: track },
        })),

      setZoomLevel: (level) =>
        set((state) => ({
          session: { ...state.session, zoom_level: level },
        })),

      togglePanel: (panel) =>
        set((state) => {
          const key = `${panel}_visible` as keyof typeof state.session.panel_layout;
          if (key === "timeline_height_px") return state;
          return {
            session: {
              ...state.session,
              panel_layout: {
                ...state.session.panel_layout,
                [key]: !state.session.panel_layout[key as "inspector_visible" | "review_panel_visible" | "copilot_visible"],
              },
            },
          };
        }),

      markDirty: () =>
        set((state) => ({
          session: { ...state.session, dirty: true },
        })),

      markSaved: () =>
        set((state) => ({
          session: {
            ...state.session,
            dirty: false,
            last_save_at: new Date().toISOString(),
          },
        })),

      markAutoSaved: () =>
        set((state) => ({
          session: {
            ...state.session,
            last_auto_save_at: new Date().toISOString(),
          },
        })),

      setBeatReviews: (reviews) => set({ beatReviews: reviews }),

      updateBeatReview: (index, status) =>
        set((state) => ({
          beatReviews: state.beatReviews.map((r) =>
            r.beat_index === index ? { ...r, status } : r
          ),
        })),

      setPipelineState: (pipelineState) => set({ pipelineState }),

      setLoading: (isLoading) => set({ isLoading }),

      setError: (error) => set({ error }),
    }),
    {
      // FR-VID-10 §3 TD4: Max 50 undo snapshots
      limit: 50,
      // Only track manifest mutations for undo/redo — not UI state
      partialize: (state) => ({
        manifest: state.manifest,
      }),
    }
  )
);

// ---------------------------------------------------------------------------
// IndexedDB Auto-Save — FR-VID-10 §3 TD6 + Stage 1 Step 6
// ---------------------------------------------------------------------------

const IDB_DB_NAME = "cmf-editor";
const IDB_STORE_NAME = "auto-save";
const IDB_VERSION = 1;

function openAutoSaveDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(IDB_DB_NAME, IDB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(IDB_STORE_NAME)) {
        db.createObjectStore(IDB_STORE_NAME, { keyPath: "videoId" });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export async function saveToIndexedDB(
  videoId: string,
  manifest: CMFManifest
): Promise<void> {
  const db = await openAutoSaveDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(IDB_STORE_NAME, "readwrite");
    const store = tx.objectStore(IDB_STORE_NAME);
    store.put({
      videoId,
      manifest: JSON.parse(JSON.stringify(manifest)),
      savedAt: new Date().toISOString(),
    });
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

export async function loadFromIndexedDB(
  videoId: string
): Promise<{ manifest: CMFManifest; savedAt: string } | null> {
  const db = await openAutoSaveDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(IDB_STORE_NAME, "readonly");
    const store = tx.objectStore(IDB_STORE_NAME);
    const request = store.get(videoId);
    request.onsuccess = () => {
      if (request.result) {
        resolve({
          manifest: request.result.manifest,
          savedAt: request.result.savedAt,
        });
      } else {
        resolve(null);
      }
    };
    request.onerror = () => reject(request.error);
  });
}

export async function clearAutoSave(videoId: string): Promise<void> {
  const db = await openAutoSaveDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(IDB_STORE_NAME, "readwrite");
    const store = tx.objectStore(IDB_STORE_NAME);
    store.delete(videoId);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

// ---------------------------------------------------------------------------
// Auto-save interval manager — FR-VID-10 §4 Stage 1 Step 6
// ---------------------------------------------------------------------------

let autoSaveInterval: ReturnType<typeof setInterval> | null = null;

export function startAutoSave(videoId: string): void {
  stopAutoSave();
  autoSaveInterval = setInterval(async () => {
    const state = useEditorStore.getState();
    if (state.manifest && state.session.dirty) {
      try {
        await saveToIndexedDB(videoId, state.manifest);
        state.markAutoSaved();
      } catch (err) {
        console.error("Auto-save failed:", err);
      }
    }
  }, 5000);
}

export function stopAutoSave(): void {
  if (autoSaveInterval !== null) {
    clearInterval(autoSaveInterval);
    autoSaveInterval = null;
  }
}
