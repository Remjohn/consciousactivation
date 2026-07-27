"""Surface state repositories for TS-CMF-007."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.surfaces import NotificationIntent, ObjectStateSnapshot


@dataclass
class InMemoryObjectStateRepository:
    snapshots: dict[tuple[str, UUID], ObjectStateSnapshot] = field(default_factory=dict)

    def put(self, snapshot: ObjectStateSnapshot) -> ObjectStateSnapshot:
        self.snapshots[(snapshot.object_type, snapshot.object_id)] = snapshot
        return snapshot

    def get(self, object_type: str, object_id: UUID) -> ObjectStateSnapshot | None:
        return self.snapshots.get((object_type, object_id))


@dataclass
class InMemoryNotificationIntentRepository:
    intents: dict[UUID, NotificationIntent] = field(default_factory=dict)

    def put(self, intent: NotificationIntent) -> NotificationIntent:
        self.intents[intent.notification_intent_id] = intent
        return intent
