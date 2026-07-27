'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'next/navigation';

// ─── Types ───

interface Asset {
  key: string;
  filename: string;
  content_type: string;
  size_bytes: number;
  last_modified: string;
  thumbnail_url: string;
  presigned_url: string;
  beat_index: number | null;
}

// ─── API helpers ───

const API_BASE = process.env.NEXT_PUBLIC_PROJECT_API_URL || 'http://localhost:8000';

async function apiFetch<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('cmf_token') || 'dev-token' : 'dev-token';
  const res = await fetch(`${API_BASE}${path}`, {
    ...opts,
    headers: {
      Authorization: `Bearer ${token}`,
      ...opts.headers,
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(body.detail || body.error || `API ${res.status}`);
  }
  return res.json();
}

// ─── Helpers ───

const FOLDER_STRUCTURE = ['source', 'keyframes', 'clips', 'audio', 'captions', 'renders/preview', 'renders/review', 'renders/final', 'exports'];

const FOLDER_LABELS: Record<string, string> = {
  'source': '📂 Source Files',
  'keyframes': '🖼️ Keyframes',
  'clips': '🎬 Video Clips',
  'audio': '🎵 Audio',
  'captions': '📝 Captions',
  'renders/preview': '👁️ Preview Renders',
  'renders/review': '🔍 Review Renders',
  'renders/final': '✅ Final Renders',
  'exports': '📤 Exports',
};

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString();
}

function isImage(ct: string) { return ct.startsWith('image/'); }
function isVideo(ct: string) { return ct.startsWith('video/'); }
function isAudio(ct: string) { return ct.startsWith('audio/'); }

// ═══════════════════════════════════════════
// Folder Sidebar
// ═══════════════════════════════════════════

function AssetFolderTree({
  selectedPrefix,
  onSelect,
  assetCounts,
}: {
  selectedPrefix: string;
  onSelect: (prefix: string) => void;
  assetCounts: Record<string, number>;
}) {
  return (
    <div className="w-52 border-r border-gray-200 bg-gray-50 flex flex-col h-full">
      <div className="p-3 border-b border-gray-200">
        <span className="font-semibold text-sm text-gray-800">Asset Folders</span>
      </div>
      <div className="flex-1 overflow-y-auto py-1">
        <div
          className={`flex items-center gap-2 px-3 py-1.5 text-sm cursor-pointer rounded mx-1 hover:bg-gray-100 ${
            selectedPrefix === '' ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700'
          }`}
          onClick={() => onSelect('')}
        >
          <span>📁</span>
          <span className="flex-1">All Assets</span>
        </div>
        {FOLDER_STRUCTURE.map(folder => (
          <div
            key={folder}
            className={`flex items-center gap-2 px-3 py-1.5 text-sm cursor-pointer rounded mx-1 hover:bg-gray-100 ${
              selectedPrefix === folder ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700'
            }`}
            style={{ paddingLeft: folder.includes('/') ? '32px' : '12px' }}
            onClick={() => onSelect(folder)}
          >
            <span className="truncate flex-1">{FOLDER_LABELS[folder] || folder}</span>
            {(assetCounts[folder] || 0) > 0 && (
              <span className="text-xs text-gray-400">{assetCounts[folder]}</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// Asset Card
// ═══════════════════════════════════════════

function AssetCard({
  asset,
  selected,
  onToggleSelect,
  onPreview,
}: {
  asset: Asset;
  selected: boolean;
  onToggleSelect: () => void;
  onPreview: () => void;
}) {
  return (
    <div
      className={`group bg-white border rounded-lg overflow-hidden hover:shadow-md transition-shadow cursor-pointer relative ${
        selected ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-200'
      }`}
      onClick={onPreview}
    >
      {/* Selection checkbox */}
      <div className="absolute top-2 left-2 z-10" onClick={e => e.stopPropagation()}>
        <input type="checkbox" checked={selected} onChange={onToggleSelect}
          className="opacity-0 group-hover:opacity-100 checked:opacity-100 transition-opacity" />
      </div>

      {/* Thumbnail */}
      <div className="h-32 bg-gray-100 flex items-center justify-center overflow-hidden">
        {isImage(asset.content_type) ? (
          <img src={asset.presigned_url} alt={asset.filename} className="w-full h-full object-cover" loading="lazy" />
        ) : isVideo(asset.content_type) ? (
          <div className="text-center">
            <span className="text-3xl">🎬</span>
            <div className="text-xs text-gray-400 mt-1">Video</div>
          </div>
        ) : isAudio(asset.content_type) ? (
          <div className="text-center">
            <span className="text-3xl">🎵</span>
            <div className="text-xs text-gray-400 mt-1">Audio</div>
          </div>
        ) : (
          <span className="text-3xl">📄</span>
        )}
      </div>

      {/* Info */}
      <div className="p-2">
        <p className="text-xs font-medium text-gray-800 truncate" title={asset.filename}>{asset.filename}</p>
        <div className="flex items-center gap-2 mt-1 text-xs text-gray-400">
          <span>{formatSize(asset.size_bytes)}</span>
          {asset.beat_index !== null && (
            <span className="bg-purple-50 text-purple-600 px-1 rounded">Beat {asset.beat_index}</span>
          )}
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// Preview Panel
// ═══════════════════════════════════════════

function PreviewPanel({
  asset,
  projectId,
  onClose,
}: {
  asset: Asset;
  projectId: string;
  onClose: () => void;
}) {
  return (
    <div className="w-96 border-l border-gray-200 bg-white flex flex-col h-full">
      {/* Header */}
      <div className="p-3 border-b border-gray-200 flex items-center justify-between">
        <span className="text-sm font-semibold truncate">{asset.filename}</span>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600">✕</button>
      </div>

      {/* Preview */}
      <div className="flex-1 overflow-y-auto">
        <div className="bg-gray-900 flex items-center justify-center min-h-[200px]">
          {isImage(asset.content_type) ? (
            <img src={asset.presigned_url} alt={asset.filename} className="max-w-full max-h-[400px] object-contain" />
          ) : isVideo(asset.content_type) ? (
            <video src={asset.presigned_url} controls className="max-w-full max-h-[400px]" />
          ) : isAudio(asset.content_type) ? (
            <div className="p-8 w-full">
              <audio src={asset.presigned_url} controls className="w-full" />
            </div>
          ) : (
            <div className="p-8 text-gray-400 text-center">
              <span className="text-4xl">📄</span>
              <div className="mt-2">No preview available</div>
            </div>
          )}
        </div>

        {/* Metadata */}
        <div className="p-4 space-y-3">
          <div>
            <span className="text-xs text-gray-500 block">S3 Key</span>
            <span className="text-sm text-gray-800 break-all">{asset.key}</span>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <span className="text-xs text-gray-500 block">Type</span>
              <span className="text-sm text-gray-800">{asset.content_type}</span>
            </div>
            <div>
              <span className="text-xs text-gray-500 block">Size</span>
              <span className="text-sm text-gray-800">{formatSize(asset.size_bytes)}</span>
            </div>
            <div>
              <span className="text-xs text-gray-500 block">Last Modified</span>
              <span className="text-sm text-gray-800">{formatDate(asset.last_modified)}</span>
            </div>
            {asset.beat_index !== null && (
              <div>
                <span className="text-xs text-gray-500 block">Beat</span>
                <span className="text-sm text-gray-800">Beat {asset.beat_index}</span>
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex flex-col gap-2 pt-2">
            <a
              href={asset.presigned_url}
              download={asset.filename}
              className="text-center px-3 py-2 bg-gray-100 rounded text-sm hover:bg-gray-200"
            >
              ⬇ Download
            </a>
            <button
              onClick={() => navigator.clipboard.writeText(asset.presigned_url)}
              className="px-3 py-2 bg-gray-100 rounded text-sm hover:bg-gray-200"
            >
              📋 Copy URL
            </button>
            <button
              onClick={() => window.location.href = `/editor/${projectId}?swapAsset=${encodeURIComponent(asset.key)}`}
              className="px-3 py-2 bg-blue-50 text-blue-700 rounded text-sm hover:bg-blue-100"
            >
              🎬 Use in Editor
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// Main Page
// ═══════════════════════════════════════════

export default function AssetsPage() {
  const params = useParams();
  const projectId = params?.projectId as string;

  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPrefix, setSelectedPrefix] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [previewAsset, setPreviewAsset] = useState<Asset | null>(null);
  const [uploading, setUploading] = useState(false);

  // Asset counts per folder
  const [assetCounts, setAssetCounts] = useState<Record<string, number>>({});

  const fetchAssets = useCallback(async () => {
    if (!projectId) return;
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (selectedPrefix) params.set('prefix', selectedPrefix);
      if (typeFilter !== 'all') params.set('type', typeFilter);

      const data = await apiFetch<{ assets: Asset[]; total: number }>(
        `/api/projects/${encodeURIComponent(projectId)}/assets?${params}`
      );
      setAssets(data.assets);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [projectId, selectedPrefix, typeFilter]);

  // Fetch all assets once for counts
  const fetchCounts = useCallback(async () => {
    if (!projectId) return;
    try {
      const data = await apiFetch<{ assets: Asset[] }>(
        `/api/projects/${encodeURIComponent(projectId)}/assets`
      );
      const counts: Record<string, number> = {};
      for (const a of data.assets) {
        for (const folder of FOLDER_STRUCTURE) {
          if (a.key.startsWith(folder + '/') || a.key.startsWith(folder)) {
            counts[folder] = (counts[folder] || 0) + 1;
          }
        }
      }
      setAssetCounts(counts);
    } catch { /* non-critical */ }
  }, [projectId]);

  useEffect(() => { fetchAssets(); }, [fetchAssets]);
  useEffect(() => { fetchCounts(); }, [fetchCounts]);

  // Filter by search
  const filteredAssets = searchQuery
    ? assets.filter(a =>
        a.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
        a.content_type.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (a.beat_index !== null && `beat ${a.beat_index}`.includes(searchQuery.toLowerCase()))
      )
    : assets;

  const toggleSelect = (key: string) => {
    setSelectedIds(prev => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  // Upload handler
  const handleUpload = async (files: FileList) => {
    if (!projectId) return;
    setUploading(true);
    const subfolder = selectedPrefix || 'source';

    for (const file of Array.from(files)) {
      const formData = new FormData();
      formData.append('file', file);

      const token = localStorage.getItem('cmf_token') || 'dev-token';
      await fetch(
        `${API_BASE}/api/projects/${encodeURIComponent(projectId)}/assets/upload?subfolder=${encodeURIComponent(subfolder)}`,
        {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` },
          body: formData,
        }
      );
    }

    setUploading(false);
    fetchAssets();
    fetchCounts();
  };

  // Bulk delete
  const handleBulkDelete = async () => {
    if (!projectId || selectedIds.size === 0) return;
    if (!confirm(`Delete ${selectedIds.size} asset(s)?`)) return;

    const token = localStorage.getItem('cmf_token') || 'dev-token';
    await fetch(`${API_BASE}/api/projects/${encodeURIComponent(projectId)}/assets`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ keys: Array.from(selectedIds) }),
    });

    setSelectedIds(new Set());
    fetchAssets();
    fetchCounts();
  };

  // Drag-and-drop
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files.length > 0) {
      handleUpload(e.dataTransfer.files);
    }
  };

  return (
    <div className="flex h-screen bg-white">
      {/* Folder sidebar */}
      <AssetFolderTree
        selectedPrefix={selectedPrefix}
        onSelect={setSelectedPrefix}
        assetCounts={assetCounts}
      />

      {/* Main area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <div className="border-b border-gray-200 px-4 py-3 flex items-center gap-3">
          <button onClick={() => window.history.back()} className="text-sm text-gray-500 hover:text-gray-700">← Back</button>
          <span className="text-sm font-semibold text-gray-800">Assets: {projectId}</span>
          <div className="flex-1" />

          <input
            type="text"
            placeholder="Search by filename, type, or beat…"
            className="max-w-xs border rounded px-3 py-1.5 text-sm"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
          />
          <select className="border rounded px-2 py-1.5 text-sm" value={typeFilter} onChange={e => setTypeFilter(e.target.value)}>
            <option value="all">All types</option>
            <option value="image">Images</option>
            <option value="video">Video</option>
            <option value="audio">Audio</option>
          </select>

          <label className="px-3 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 cursor-pointer">
            {uploading ? 'Uploading…' : '⬆ Upload'}
            <input type="file" multiple className="hidden" onChange={e => e.target.files && handleUpload(e.target.files)} />
          </label>
        </div>

        {/* Bulk actions */}
        {selectedIds.size > 0 && (
          <div className="bg-blue-50 px-4 py-2 flex items-center gap-3 border-b border-blue-200">
            <span className="text-sm text-blue-700">{selectedIds.size} selected</span>
            <button onClick={handleBulkDelete} className="text-xs text-red-600 hover:underline">Delete</button>
            <button onClick={() => setSelectedIds(new Set())} className="text-xs text-gray-500 hover:underline">Clear</button>
          </div>
        )}

        {/* S3 offline warning */}
        {error && (
          <div className="bg-yellow-50 px-4 py-2 text-sm text-yellow-700 border-b border-yellow-200">
            ⚠ S3 offline — showing cached data. Error: {error}
          </div>
        )}

        {/* Grid */}
        <div
          className="flex-1 overflow-y-auto p-4"
          onDragOver={e => { e.preventDefault(); e.stopPropagation(); }}
          onDrop={handleDrop}
        >
          {loading && <div className="text-center text-gray-400 py-8">Loading assets…</div>}

          {!loading && filteredAssets.length === 0 && (
            <div className="text-center py-16 text-gray-400">
              <div className="text-4xl mb-4">📂</div>
              <p>No assets in this folder yet.</p>
              <p className="text-sm mt-1">Drag and drop files here or click Upload.</p>
            </div>
          )}

          {!loading && filteredAssets.length > 0 && (
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-3">
              {filteredAssets.map(a => (
                <AssetCard
                  key={a.key}
                  asset={a}
                  selected={selectedIds.has(a.key)}
                  onToggleSelect={() => toggleSelect(a.key)}
                  onPreview={() => setPreviewAsset(a)}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Preview panel */}
      {previewAsset && (
        <PreviewPanel
          asset={previewAsset}
          projectId={projectId}
          onClose={() => setPreviewAsset(null)}
        />
      )}
    </div>
  );
}
