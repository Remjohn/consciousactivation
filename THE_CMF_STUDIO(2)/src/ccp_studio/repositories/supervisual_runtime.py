from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from ccp_studio.contracts.supervisual_runtime import (
    SuperVisualBuildRun,
    SuperVisualCommand,
    SuperVisualEvent,
    SuperVisualProject,
    SuperVisualSnapshot,
    SuperVisualStepRun,
    SuperVisualVariant,
)

T = TypeVar("T")


def _model_to_dict(model):
    if hasattr(model, "model_dump"):
        return model.model_dump(mode="json")
    return model.dict()


def _model_from_json(cls: type[T], text: str) -> T:
    if hasattr(cls, "model_validate_json"):
        return cls.model_validate_json(text)  # type: ignore[attr-defined]
    return cls.parse_raw(text)  # type: ignore[attr-defined]


class InMemorySuperVisualRuntimeRepository:
    def __init__(self):
        self.projects: dict[str, SuperVisualProject] = {}
        self.variants: dict[str, SuperVisualVariant] = {}
        self.snapshots: dict[str, SuperVisualSnapshot] = {}
        self.build_runs: dict[str, SuperVisualBuildRun] = {}
        self.step_runs: dict[str, SuperVisualStepRun] = {}
        self.events: dict[str, SuperVisualEvent] = {}
        self.commands: dict[str, SuperVisualCommand] = {}
        self.command_idempotency_index: dict[str, str] = {}
        self.project_bcv_index: dict[str, str] = {}
        self.variant_bcv_index: dict[str, str] = {}

    def create_project(self, project: SuperVisualProject) -> SuperVisualProject:
        self.projects[project.supervisual_project_id] = project
        self.project_bcv_index[project.supervisual_project_id] = project.brand_context_version_id
        return project

    def update_project(self, project: SuperVisualProject) -> SuperVisualProject:
        original_bcv = self.project_bcv_index.get(project.supervisual_project_id)
        if original_bcv and original_bcv != project.brand_context_version_id:
            raise ValueError("brand_context_version_id is immutable for SuperVisualProject")
        self.projects[project.supervisual_project_id] = project
        self.project_bcv_index.setdefault(project.supervisual_project_id, project.brand_context_version_id)
        return project

    def get_project(self, project_id: str) -> SuperVisualProject:
        return self.projects[project_id]

    def list_projects(self, brand_id: str | None = None) -> list[SuperVisualProject]:
        values = list(self.projects.values())
        if brand_id:
            values = [p for p in values if p.brand_id == brand_id]
        return sorted(values, key=lambda p: p.created_at)

    def create_variant(self, variant: SuperVisualVariant) -> SuperVisualVariant:
        self.variants[variant.supervisual_variant_id] = variant
        self.variant_bcv_index[variant.supervisual_variant_id] = variant.brand_context_version_id
        return variant

    def update_variant(self, variant: SuperVisualVariant) -> SuperVisualVariant:
        original_bcv = self.variant_bcv_index.get(variant.supervisual_variant_id)
        if original_bcv and original_bcv != variant.brand_context_version_id:
            raise ValueError("brand_context_version_id is immutable for SuperVisualVariant")
        self.variants[variant.supervisual_variant_id] = variant
        self.variant_bcv_index.setdefault(variant.supervisual_variant_id, variant.brand_context_version_id)
        return variant

    def get_variant(self, variant_id: str) -> SuperVisualVariant:
        return self.variants[variant_id]

    def list_variants(self, project_id: str) -> list[SuperVisualVariant]:
        return sorted([v for v in self.variants.values() if v.supervisual_project_id == project_id], key=lambda v: v.created_at)

    def create_snapshot(self, snapshot: SuperVisualSnapshot) -> SuperVisualSnapshot:
        self.snapshots[snapshot.supervisual_snapshot_id] = snapshot
        variant = self.get_variant(snapshot.supervisual_variant_id)
        variant.current_snapshot_id = snapshot.supervisual_snapshot_id
        self.update_variant(variant)
        return snapshot

    def get_snapshot(self, snapshot_id: str) -> SuperVisualSnapshot:
        return self.snapshots[snapshot_id]

    def get_latest_snapshot(self, variant_id: str) -> SuperVisualSnapshot | None:
        variant = self.get_variant(variant_id)
        if variant.current_snapshot_id:
            return self.snapshots.get(variant.current_snapshot_id)
        snapshots = [s for s in self.snapshots.values() if s.supervisual_variant_id == variant_id]
        return sorted(snapshots, key=lambda s: s.created_at)[-1] if snapshots else None

    def create_build_run(self, run: SuperVisualBuildRun) -> SuperVisualBuildRun:
        self.build_runs[run.supervisual_build_run_id] = run
        return run

    def update_build_run(self, run: SuperVisualBuildRun) -> SuperVisualBuildRun:
        self.build_runs[run.supervisual_build_run_id] = run
        return run

    def get_build_run(self, build_run_id: str) -> SuperVisualBuildRun:
        return self.build_runs[build_run_id]

    def list_active_build_runs(self, variant_id: str) -> list[SuperVisualBuildRun]:
        return [r for r in self.build_runs.values() if r.supervisual_variant_id == variant_id and r.status.value in {"created", "running"}]

    def create_step_run(self, step: SuperVisualStepRun) -> SuperVisualStepRun:
        self.step_runs[step.supervisual_step_run_id] = step
        return step

    def update_step_run(self, step: SuperVisualStepRun) -> SuperVisualStepRun:
        self.step_runs[step.supervisual_step_run_id] = step
        return step

    def append_event(self, event: SuperVisualEvent) -> SuperVisualEvent:
        self.events[event.supervisual_event_id] = event
        return event

    def list_events(self, project_id: str, variant_id: str | None = None) -> list[SuperVisualEvent]:
        values = [e for e in self.events.values() if e.supervisual_project_id == project_id]
        if variant_id:
            values = [e for e in values if e.supervisual_variant_id == variant_id]
        return sorted(values, key=lambda e: e.created_at)

    def create_command(self, command: SuperVisualCommand) -> SuperVisualCommand:
        if command.idempotency_key in self.command_idempotency_index:
            return self.commands[self.command_idempotency_index[command.idempotency_key]]
        self.commands[command.command_id] = command
        self.command_idempotency_index[command.idempotency_key] = command.command_id
        return command

    def update_command(self, command: SuperVisualCommand) -> SuperVisualCommand:
        self.commands[command.command_id] = command
        self.command_idempotency_index[command.idempotency_key] = command.command_id
        return command

    def get_command_by_idempotency_key(self, idempotency_key: str) -> SuperVisualCommand | None:
        command_id = self.command_idempotency_index.get(idempotency_key)
        return self.commands.get(command_id) if command_id else None


class JsonFileSuperVisualRuntimeRepository(InMemorySuperVisualRuntimeRepository):
    def __init__(self, root_dir: str | Path = "storage/supervisual_runtime"):
        super().__init__()
        self.root_dir = Path(root_dir)
        for name in ["projects", "variants", "snapshots", "build_runs", "step_runs", "events", "commands"]:
            (self.root_dir / name).mkdir(parents=True, exist_ok=True)
        self._load_existing()

    def _path(self, collection: str, item_id: str) -> Path:
        return self.root_dir / collection / f"{item_id}.json"

    def _save(self, collection: str, item_id: str, model) -> None:
        self._path(collection, item_id).write_text(json.dumps(_model_to_dict(model), indent=2), encoding="utf-8")

    def _load_collection(self, collection: str, cls: type[T]) -> dict[str, T]:
        loaded = {}
        for path in (self.root_dir / collection).glob("*.json"):
            item = _model_from_json(cls, path.read_text(encoding="utf-8"))
            loaded[path.stem] = item
        return loaded

    def _load_existing(self) -> None:
        self.projects.update(self._load_collection("projects", SuperVisualProject))
        self.variants.update(self._load_collection("variants", SuperVisualVariant))
        self.snapshots.update(self._load_collection("snapshots", SuperVisualSnapshot))
        self.build_runs.update(self._load_collection("build_runs", SuperVisualBuildRun))
        self.step_runs.update(self._load_collection("step_runs", SuperVisualStepRun))
        self.events.update(self._load_collection("events", SuperVisualEvent))
        self.commands.update(self._load_collection("commands", SuperVisualCommand))
        self.command_idempotency_index = {c.idempotency_key: c.command_id for c in self.commands.values()}
        self.project_bcv_index = {p.supervisual_project_id: p.brand_context_version_id for p in self.projects.values()}
        self.variant_bcv_index = {v.supervisual_variant_id: v.brand_context_version_id for v in self.variants.values()}

    def create_project(self, project: SuperVisualProject) -> SuperVisualProject:
        item = super().create_project(project)
        self._save("projects", item.supervisual_project_id, item)
        return item

    def update_project(self, project: SuperVisualProject) -> SuperVisualProject:
        item = super().update_project(project)
        self._save("projects", item.supervisual_project_id, item)
        return item

    def create_variant(self, variant: SuperVisualVariant) -> SuperVisualVariant:
        item = super().create_variant(variant)
        self._save("variants", item.supervisual_variant_id, item)
        return item

    def update_variant(self, variant: SuperVisualVariant) -> SuperVisualVariant:
        item = super().update_variant(variant)
        self._save("variants", item.supervisual_variant_id, item)
        return item

    def create_snapshot(self, snapshot: SuperVisualSnapshot) -> SuperVisualSnapshot:
        item = super().create_snapshot(snapshot)
        self._save("snapshots", item.supervisual_snapshot_id, item)
        self._save("variants", self.variants[item.supervisual_variant_id].supervisual_variant_id, self.variants[item.supervisual_variant_id])
        return item

    def create_build_run(self, run: SuperVisualBuildRun) -> SuperVisualBuildRun:
        item = super().create_build_run(run)
        self._save("build_runs", item.supervisual_build_run_id, item)
        return item

    def update_build_run(self, run: SuperVisualBuildRun) -> SuperVisualBuildRun:
        item = super().update_build_run(run)
        self._save("build_runs", item.supervisual_build_run_id, item)
        return item

    def create_step_run(self, step: SuperVisualStepRun) -> SuperVisualStepRun:
        item = super().create_step_run(step)
        self._save("step_runs", item.supervisual_step_run_id, item)
        return item

    def update_step_run(self, step: SuperVisualStepRun) -> SuperVisualStepRun:
        item = super().update_step_run(step)
        self._save("step_runs", item.supervisual_step_run_id, item)
        return item

    def append_event(self, event: SuperVisualEvent) -> SuperVisualEvent:
        item = super().append_event(event)
        self._save("events", item.supervisual_event_id, item)
        return item

    def create_command(self, command: SuperVisualCommand) -> SuperVisualCommand:
        item = super().create_command(command)
        self._save("commands", item.command_id, item)
        return item

    def update_command(self, command: SuperVisualCommand) -> SuperVisualCommand:
        item = super().update_command(command)
        self._save("commands", item.command_id, item)
        return item
