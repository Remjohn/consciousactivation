from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from cmf_builder.domain.run import EventStreamInvalid, Run


class CheckpointInvalid(Exception):
    code = "CheckpointInvalid"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class Checkpoint:
    checkpoint_id: str
    run_id: str
    stream_version: int
    input_hash: str
    profile_hash: str
    policy_hash: str
    state_hash: str
    human_decision_receipt_ids: tuple[str, ...]
    created_at: datetime

    @classmethod
    def from_run(
        cls,
        run: Run,
        *,
        checkpoint_id: str,
        input_hash: str,
        policy_hash: str,
        created_at: datetime,
    ) -> "Checkpoint":
        return cls(
            checkpoint_id=checkpoint_id,
            run_id=run.run_id,
            stream_version=run.stream_version,
            input_hash=input_hash,
            profile_hash=run.target_profile.profile_hash,
            policy_hash=policy_hash,
            state_hash=run.state_hash(),
            human_decision_receipt_ids=run.human_decision_receipt_ids,
            created_at=created_at,
        )


class CheckpointManager:
    def select_latest_valid(
        self,
        run: Run,
        checkpoints: tuple[Checkpoint, ...],
        *,
        input_hash: str,
        policy_hash: str,
    ) -> tuple[Checkpoint | None, tuple[str, ...]]:
        if not checkpoints:
            return None, ()
        invalid: list[str] = []
        ordered = sorted(
            checkpoints,
            key=lambda item: (item.stream_version, item.created_at, item.checkpoint_id),
            reverse=True,
        )
        for checkpoint in ordered:
            try:
                state_hash = run.state_hash_at(checkpoint.stream_version)
            except EventStreamInvalid:
                invalid.append(checkpoint.checkpoint_id)
                continue
            if (
                checkpoint.run_id != run.run_id
                or checkpoint.input_hash != input_hash
                or checkpoint.profile_hash != run.target_profile.profile_hash
                or checkpoint.policy_hash != policy_hash
                or checkpoint.state_hash != state_hash
            ):
                invalid.append(checkpoint.checkpoint_id)
                continue
            return checkpoint, tuple(invalid)
        raise CheckpointInvalid(
            "No valid checkpoint matches the current run inputs, profile and policy.",
            run_id=run.run_id,
            invalid_checkpoint_ids=tuple(invalid),
        )
