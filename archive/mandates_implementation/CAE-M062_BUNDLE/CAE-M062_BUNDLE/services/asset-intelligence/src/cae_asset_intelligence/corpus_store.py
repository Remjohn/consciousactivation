"""Filesystem-derived storage for CAE-M0062 scene corpus, index, and receipts."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable

import hashlib

from .corpus import IngestReceipt, SceneIndex, SceneRecord, CorpusIntegrityError


class SceneCorpusStore:
    """Controlled namespace for derived corpus artifacts; source bytes remain external."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.scenes_dir = self.root / "scenes"
        self.receipts_dir = self.root / "receipts"
        self.index_dir = self.root / "index"
        for directory in (self.scenes_dir, self.receipts_dir, self.index_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def put_scene(self, scene: SceneRecord) -> None:
        self._put_immutable(self.scenes_dir / f"{scene.scene_id}.json", scene.model_dump(mode="json"))

    def put_receipt(self, receipt: IngestReceipt) -> None:
        self._put_immutable(self.receipts_dir / f"{receipt.receipt_id}.json", receipt.model_dump(mode="json"))

    def verify_scene(self, scene: SceneRecord, source_bytes: bytes, media_duration: float) -> bool:
        """Verify the exact source hash and declared scene time range before retrieval use."""
        actual_hash = hashlib.sha256(source_bytes).hexdigest()
        if actual_hash != scene.source_sha256:
            raise CorpusIntegrityError("Scene source hash does not match provided media bytes")
        if scene.start_time < 0 or scene.end_time <= scene.start_time or scene.end_time > media_duration:
            raise CorpusIntegrityError("Scene time range is outside the verified source duration")
        return True

    def reindex(self) -> Path:
        records = [SceneRecord.model_validate(json.loads(path.read_text())) for path in sorted(self.scenes_dir.glob("*.json"))]
        payload = SceneIndex.build(records)
        path = self.index_dir / "scene-index.json"
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":"), indent=2))
        os.replace(temp, path)
        return path

    def load_index(self) -> dict[str, tuple[str, ...]]:
        path = self.index_dir / "scene-index.json"
        if not path.exists():
            return {}
        raw = json.loads(path.read_text())
        return {str(k): tuple(str(item) for item in v) for k, v in raw.items()}

    def search(self, query: str) -> tuple[str, ...]:
        return SceneIndex.search(self.load_index(), query)

    @staticmethod
    def _put_immutable(path: Path, payload: object) -> None:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), indent=2)
        if path.exists():
            existing = path.read_text()
            if existing != encoded:
                raise ValueError(f"Immutable record collision at {path.name}")
            return
        temp = path.with_suffix(path.suffix + ".tmp")
        temp.write_text(encoded)
        os.replace(temp, path)
