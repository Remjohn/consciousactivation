"""
Pipeline Commander — Video lifecycle orchestration, state machine, batch queue.

FR-VID-09 §4: Sequences all 8 downstream modules (FR-VID-01 through FR-VID-08),
manages the 16-state lifecycle machine, provides checkpoint/resume, batch queue,
cost tracking, review state management, and auto-approve logic.

Technical Decision 1: State machine, not event bus.
Technical Decision 2: Parallel T2I + audio where safe.
Technical Decision 3: Checkpoint + resume on every state transition.
Technical Decision 4: Review UI in existing web app (state prepared here).
Technical Decision 5: Auto-approve for all beats ≥ 0.8.
"""

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    from .receipt_chain import write_receipt
except ImportError:
    from receipt_chain import write_receipt


logger = logging.getLogger("cmf.pipeline_commander")

# ---------------------------------------------------------------------------
# Constants — 16 Pipeline States (FR-VID-09 §2 Scope)
# ---------------------------------------------------------------------------

PIPELINE_STATES = [
    "PENDING",
    "GENERATING_T2I",
    "PROCESSING_AUDIO",
    "AUDIO_COMPLETE",
    "QUALITY_GATE",
    "GENERATING_I2V",
    "FINGERPRINTING",
    "ASSEMBLING_MANIFEST",
    "GENERATING_CAPTIONS",
    "RENDERING_PREVIEW",
    "READY_FOR_REVIEW",
    "REGENERATING",
    "RENDERING_FINAL",
    "APPROVED",
    "PUBLISHED",
    "FAILED",
]

PIPELINE_STATES_SET = set(PIPELINE_STATES)

# Valid state transitions — FR-VID-09 §4 state machine diagram
# Maps current_state → set of allowed next states
VALID_TRANSITIONS: dict[str, set[str]] = {
    "PENDING": {"GENERATING_T2I", "PROCESSING_AUDIO", "FAILED"},
    "GENERATING_T2I": {"QUALITY_GATE", "FAILED"},
    "PROCESSING_AUDIO": {"AUDIO_COMPLETE", "FAILED"},
    "AUDIO_COMPLETE": {"ASSEMBLING_MANIFEST", "FAILED"},
    "QUALITY_GATE": {"GENERATING_T2I", "GENERATING_I2V", "FAILED"},
    "GENERATING_I2V": {"FINGERPRINTING", "FAILED"},
    "FINGERPRINTING": {"ASSEMBLING_MANIFEST", "FAILED"},
    "ASSEMBLING_MANIFEST": {"GENERATING_CAPTIONS", "FAILED"},
    "GENERATING_CAPTIONS": {"RENDERING_PREVIEW", "FAILED"},
    "RENDERING_PREVIEW": {"READY_FOR_REVIEW", "FAILED"},
    "READY_FOR_REVIEW": {"REGENERATING", "RENDERING_FINAL", "FAILED"},
    "REGENERATING": {"RENDERING_PREVIEW", "FAILED"},
    "RENDERING_FINAL": {"APPROVED", "FAILED"},
    "APPROVED": {"PUBLISHED"},
    "PUBLISHED": set(),
    "FAILED": set(),
}

# Parallel states — these can be active simultaneously (TD2)
PARALLEL_STATES = {"GENERATING_T2I", "PROCESSING_AUDIO"}

# Beat approval statuses
BEAT_APPROVAL_STATUSES = {"PENDING_REVIEW", "APPROVED", "REGENERATING", "REJECTED"}

# Cost per operation — FR-VID-09 §8 AC7
COST_T2I_PER_KEYFRAME = 0.02
COST_I2V_PER_CLIP = 0.06

# Quality threshold for auto-approve — FR-VID-09 §3 TD5
AUTO_APPROVE_THRESHOLD = 0.8

# Max regenerations per beat — FR-VID-05 §10
MAX_REGENERATIONS_PER_BEAT = 10

# Default concurrent processing limit — FR-VID-09 §4 Stage 3
DEFAULT_CONCURRENT_LIMIT = 3

# Retry policies — FR-VID-09 §4 Stage 1 Step 4
RETRY_POLICY_STANDARD = {"max_retries": 3, "backoff_seconds": [1, 2, 4]}
RETRY_POLICY_INFRASTRUCTURE = {"max_retries": 3, "interval_seconds": 900}

PATCH_PROFILE_MODULE_MAP = {
    "TARGETED_VISUAL_PATCH": {
        "FR-VID-02": "prompt_refresh",
        "FR-VID-03": "clip_refresh",
        "FR-VID-04": "keyframe_quality_pass",
    },
    "EXTEND_HOLD_PATCH": {
        "FR-VID-03": "extend_hold",
    },
    "RHYTHM_REBALANCE_PATCH": {
        "FR-VID-03": "retime_neighbors",
    },
    "TIMING_REBALANCE_PATCH": {
        "FR-VID-02": "prompt_refresh",
        "FR-VID-03": "retime_neighbors",
        "FR-VID-04": "keyframe_quality_pass",
    },
}


# ---------------------------------------------------------------------------
# Pipeline ID Generation
# ---------------------------------------------------------------------------


def generate_pipeline_id() -> str:
    """Generate a pipeline ID in the pattern PIPE-YYYYMMDD-NNN."""
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    seq = str(uuid.uuid4().int % 1000).zfill(3)
    return f"PIPE-{date_str}-{seq}"


# ---------------------------------------------------------------------------
# State Machine — TD1
# ---------------------------------------------------------------------------


def validate_transition(current_state: str, next_state: str) -> tuple[bool, str]:
    """
    Validate a state machine transition.

    Returns (valid, reason). Invalid transitions are rejected per TD1.
    """
    if current_state not in PIPELINE_STATES_SET:
        return False, f"Unknown current state: {current_state}"
    if next_state not in PIPELINE_STATES_SET:
        return False, f"Unknown next state: {next_state}"
    allowed = VALID_TRANSITIONS.get(current_state, set())
    if next_state not in allowed:
        return False, (
            f"Illegal transition {current_state} → {next_state}. "
            f"Allowed: {sorted(allowed)}"
        )
    return True, "OK"


def create_pipeline_state(
    beat_cluster_id: str,
    project_id: str,
    beat_count: int,
    video_id: Optional[str] = None,
) -> dict:
    """
    Create a new pipeline state instance in PENDING state.

    Initializes beat approvals as PENDING_REVIEW for all beats.
    """
    pipeline_id = generate_pipeline_id()
    now = datetime.now(timezone.utc).isoformat()
    return {
        "pipeline_id": pipeline_id,
        "video_id": video_id or f"CMF-VID-{datetime.now(timezone.utc).strftime('%Y%m%d')}-001",
        "project_id": project_id,
        "beat_cluster_id": beat_cluster_id,
        "current_state": "PENDING",
        "state_history": [{"state": "PENDING", "entered_at": now}],
        "beat_approvals": [
            {
                "beat_index": i,
                "status": "PENDING_REVIEW",
                "quality_score": None,
                "regeneration_mode": None,
                "regeneration_count": 0,
            }
            for i in range(beat_count)
        ],
        "preview_render_url": None,
        "final_render_url": None,
        "total_generation_cost_usd": 0.0,
        "total_regenerations": 0,
        "checkpoint_path": None,
        "error": None,
        "created_at": now,
        "updated_at": now,
    }


def transition_state(
    state: dict, next_state_name: str, metadata: Optional[dict] = None
) -> tuple[bool, str]:
    """
    Attempt to transition the pipeline to next_state_name.

    Mutates the state dict in place on success.
    Returns (success, reason).
    """
    current = state["current_state"]
    valid, reason = validate_transition(current, next_state_name)
    if not valid:
        return False, reason

    now = datetime.now(timezone.utc).isoformat()
    entry = {"state": next_state_name, "entered_at": now}
    if metadata:
        entry["metadata"] = metadata
    state["state_history"].append(entry)
    state["current_state"] = next_state_name
    state["updated_at"] = now
    return True, "OK"


def transition_to_failed(state: dict, error_message: str) -> bool:
    """Transition to FAILED state with error details."""
    success, _ = transition_state(state, "FAILED", metadata={"error": error_message})
    if success:
        state["error"] = error_message
    return success


# ---------------------------------------------------------------------------
# Beat Approval Management — §4 Stage 2
# ---------------------------------------------------------------------------


def approve_beat(state: dict, beat_index: int) -> tuple[bool, str]:
    """Mark a beat as approved. Returns (success, reason)."""
    for ba in state["beat_approvals"]:
        if ba["beat_index"] == beat_index:
            ba["status"] = "APPROVED"
            state["updated_at"] = datetime.now(timezone.utc).isoformat()
            return True, "OK"
    return False, f"Beat {beat_index} not found"


def approve_all_beats(state: dict) -> int:
    """Approve all beats. Returns count of newly approved."""
    count = 0
    for ba in state["beat_approvals"]:
        if ba["status"] != "APPROVED":
            ba["status"] = "APPROVED"
            count += 1
    if count > 0:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
    return count


def request_regeneration(
    state: dict, beat_index: int, mode: str, revision_note: str
) -> tuple[bool, str]:
    """
    Mark a beat for regeneration. Enforces max regeneration limit.

    Returns (success, reason).
    """
    valid_modes = {"T2I_ONLY", "I2V_ONLY", "BOTH"}
    if mode not in valid_modes:
        return False, f"Invalid mode '{mode}'. Must be one of: {sorted(valid_modes)}"
    if not revision_note or not revision_note.strip():
        return False, "Revision note is required"

    for ba in state["beat_approvals"]:
        if ba["beat_index"] == beat_index:
            if ba["regeneration_count"] >= MAX_REGENERATIONS_PER_BEAT:
                return False, (
                    f"Beat {beat_index} has reached the maximum of "
                    f"{MAX_REGENERATIONS_PER_BEAT} regenerations"
                )
            ba["status"] = "REGENERATING"
            ba["regeneration_mode"] = mode
            ba["regeneration_count"] += 1
            state["total_regenerations"] += 1
            state["updated_at"] = datetime.now(timezone.utc).isoformat()
            return True, "OK"
    return False, f"Beat {beat_index} not found"


def build_regeneration_dispatch(regeneration_plan: dict) -> dict:
    """
    Build the concrete Commander execution payload for a regeneration plan.

    This converts patch_selection from advisory metadata into an executable
    module dispatch and manifest patch contract.
    """
    patch_selection = regeneration_plan.get("patch_selection", {})
    patch_profile = patch_selection.get("patch_profile", "TARGETED_VISUAL_PATCH")
    targeted_fields = sorted(set(patch_selection.get("targeted_fields", [])))
    module_actions = PATCH_PROFILE_MODULE_MAP.get(patch_profile, PATCH_PROFILE_MODULE_MAP["TARGETED_VISUAL_PATCH"])

    available_calls = set(regeneration_plan.get("pipeline_calls", []))
    module_dispatch = {}
    for module_name, operation in module_actions.items():
        if module_name not in available_calls:
            continue
        module_dispatch[module_name] = {
            "enabled": True,
            "operation": operation,
            "targeted_fields": [
                field for field in targeted_fields
                if (
                    module_name == "FR-VID-02" and field.endswith("fallback_image_url")
                )
                or (
                    module_name == "FR-VID-03" and not field.endswith("fallback_image_url")
                )
                or module_name == "FR-VID-04"
            ],
        }

    return {
        "target_beat_index": patch_selection.get("target_beat_index"),
        "mode": regeneration_plan.get("mode"),
        "patch_profile": patch_profile,
        "module_dispatch": module_dispatch,
        "manifest_patch": {
            "targeted_fields": targeted_fields,
            "timing_patch_required": patch_selection.get("timing_patch_required", False),
            "surprise_patch_required": patch_selection.get("surprise_patch_required", False),
            "surprise_adjustment": patch_selection.get("surprise_adjustment"),
            "surprise_score": patch_selection.get("surprise_score"),
            "neighbor_consultation_indices": patch_selection.get("neighbor_consultation_indices", []),
            "corrective_moves": patch_selection.get("corrective_moves", []),
        },
    }


def set_quality_scores(state: dict, scores: dict[int, float]) -> None:
    """Set quality scores for beats. scores = {beat_index: score}."""
    for ba in state["beat_approvals"]:
        if ba["beat_index"] in scores:
            ba["quality_score"] = scores[ba["beat_index"]]
    state["updated_at"] = datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Auto-Approve Logic — TD5
# ---------------------------------------------------------------------------


def check_auto_approve_eligible(state: dict) -> bool:
    """
    Check if all beats meet the auto-approve threshold (≥ 0.8).

    Returns True only if every beat has a quality score >= threshold.
    """
    for ba in state["beat_approvals"]:
        score = ba.get("quality_score")
        if score is None or score < AUTO_APPROVE_THRESHOLD:
            return False
    return True


def auto_approve_if_eligible(state: dict) -> tuple[bool, str]:
    """
    Auto-approve all beats if eligible. Returns (approved, reason).

    TD5: Skip review for videos where all beats scored ≥ 0.8.
    """
    if not check_auto_approve_eligible(state):
        return False, "Not all beats meet auto-approve threshold"
    approve_all_beats(state)
    return True, "AUTO_APPROVED"


# ---------------------------------------------------------------------------
# Cost Tracking — §8 AC7
# ---------------------------------------------------------------------------


def compute_generation_cost(
    beat_count: int, regeneration_count: int = 0
) -> float:
    """
    Compute total generation cost for a video.

    Base cost: T2I ($0.02) + I2V ($0.06) per beat = $0.08/beat.
    Regeneration cost: same per-beat rate per regeneration.
    """
    base_cost = beat_count * (COST_T2I_PER_KEYFRAME + COST_I2V_PER_CLIP)
    regen_cost = regeneration_count * (COST_T2I_PER_KEYFRAME + COST_I2V_PER_CLIP)
    return round(base_cost + regen_cost, 2)


def update_cost(state: dict) -> float:
    """Recalculate and update the cost on the pipeline state."""
    beat_count = len(state["beat_approvals"])
    regen_count = state.get("total_regenerations", 0)
    cost = compute_generation_cost(beat_count, regen_count)
    state["total_generation_cost_usd"] = cost
    return cost


# ---------------------------------------------------------------------------
# Checkpoint System — TD3
# ---------------------------------------------------------------------------


def serialize_checkpoint(state: dict, checkpoint_dir: str) -> str:
    """
    Serialize pipeline state to a checkpoint file.

    Returns the checkpoint file path.
    """
    os.makedirs(checkpoint_dir, exist_ok=True)
    pipeline_id = state["pipeline_id"]
    filename = f"{pipeline_id}.json"
    filepath = os.path.join(checkpoint_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, default=str)
    state["checkpoint_path"] = filepath
    return filepath


def load_checkpoint(checkpoint_path: str) -> Optional[dict]:
    """
    Load a pipeline state from a checkpoint file.

    Returns None if the file doesn't exist.
    """
    if not os.path.exists(checkpoint_path):
        return None
    with open(checkpoint_path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_checkpoint(beat_cluster_id: str, checkpoint_dir: str) -> Optional[str]:
    """
    Search for an existing checkpoint for a given beat_cluster_id.

    Returns the checkpoint file path if found, None otherwise.
    """
    if not os.path.isdir(checkpoint_dir):
        return None
    for filename in os.listdir(checkpoint_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(checkpoint_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("beat_cluster_id") == beat_cluster_id:
                    return filepath
            except (json.JSONDecodeError, KeyError):
                continue
    return None


# ---------------------------------------------------------------------------
# Batch Queue — §4 Stage 3
# ---------------------------------------------------------------------------


def create_job_queue(concurrent_limit: int = DEFAULT_CONCURRENT_LIMIT) -> dict:
    """Create an empty job queue."""
    return {
        "queue_id": f"QUEUE-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{str(uuid.uuid4().int % 1000).zfill(3)}",
        "concurrent_limit": concurrent_limit,
        "jobs": [],
        "stats": {
            "total_queued": 0,
            "total_processing": 0,
            "total_completed": 0,
            "total_failed": 0,
        },
    }


def enqueue_job(
    queue: dict,
    pipeline_id: str,
    beat_cluster_id: str,
    project_id: str = "",
    priority: int = 50,
    auto_approve: bool = False,
) -> dict:
    """
    Add a job to the queue. Jobs are sorted by priority (desc) then FIFO.

    Returns the created job entry.
    """
    now = datetime.now(timezone.utc).isoformat()
    job = {
        "pipeline_id": pipeline_id,
        "beat_cluster_id": beat_cluster_id,
        "project_id": project_id,
        "priority": max(0, min(100, priority)),
        "status": "QUEUED",
        "queued_at": now,
        "started_at": None,
        "completed_at": None,
        "auto_approve": auto_approve,
    }
    queue["jobs"].append(job)
    queue["stats"]["total_queued"] += 1
    return job


def dequeue_next(queue: dict) -> Optional[dict]:
    """
    Get the next job to process, respecting priority and concurrent limit.

    Returns the job entry if one is available, None if queue is full or empty.
    """
    processing_count = sum(1 for j in queue["jobs"] if j["status"] == "PROCESSING")
    if processing_count >= queue["concurrent_limit"]:
        return None

    # Sort candidates by priority (desc) then queue time (asc)
    candidates = [j for j in queue["jobs"] if j["status"] == "QUEUED"]
    if not candidates:
        return None

    candidates.sort(key=lambda j: (-j["priority"], j["queued_at"]))
    job = candidates[0]
    job["status"] = "PROCESSING"
    job["started_at"] = datetime.now(timezone.utc).isoformat()
    queue["stats"]["total_queued"] -= 1
    queue["stats"]["total_processing"] += 1
    return job


def complete_job(queue: dict, pipeline_id: str, success: bool = True) -> Optional[dict]:
    """Mark a job as completed or failed."""
    for job in queue["jobs"]:
        if job["pipeline_id"] == pipeline_id and job["status"] == "PROCESSING":
            job["status"] = "COMPLETED" if success else "FAILED"
            job["completed_at"] = datetime.now(timezone.utc).isoformat()
            queue["stats"]["total_processing"] -= 1
            if success:
                queue["stats"]["total_completed"] += 1
            else:
                queue["stats"]["total_failed"] += 1
            return job
    return None


def get_queue_status(queue: dict) -> dict:
    """Return a summary of the queue status."""
    return {
        "concurrent_limit": queue["concurrent_limit"],
        "total_jobs": len(queue["jobs"]),
        **queue["stats"],
    }


# ---------------------------------------------------------------------------
# Review UI State Builder — §4 Stage 2 (TD4)
# ---------------------------------------------------------------------------


def build_review_state(state: dict) -> dict:
    """
    Build the review UI state from the pipeline state (DEP-VID-027).

    Determines auto-approve eligibility and render-final readiness.
    """
    all_approved = all(
        ba["status"] == "APPROVED" for ba in state["beat_approvals"]
    )
    auto_eligible = check_auto_approve_eligible(state)

    if all_approved:
        review_status = "ALL_APPROVED"
    else:
        review_status = "IN_REVIEW"

    return {
        "pipeline_id": state["pipeline_id"],
        "video_id": state["video_id"],
        "review_status": review_status,
        "preview_url": state.get("preview_render_url"),
        "beats": [
            {
                "beat_index": ba["beat_index"],
                "approval_status": ba["status"],
                "quality_score": ba.get("quality_score"),
                "thumbnail_url": None,
                "regeneration_count": ba.get("regeneration_count", 0),
                "last_revision_note": None,
            }
            for ba in state["beat_approvals"]
        ],
        "auto_approve_eligible": auto_eligible,
        "total_cost_usd": state.get("total_generation_cost_usd", 0.0),
        "render_final_enabled": all_approved,
    }


# ---------------------------------------------------------------------------
# Receipt-writing entry points — §4
# ---------------------------------------------------------------------------


def run_pipeline_init(
    beat_cluster_id: str,
    project_id: str,
    beat_count: int,
    output_dir: str = ".",
    previous_receipt: Optional[dict] = None,
) -> dict:
    """
    Initialize a new pipeline instance. Writes PIPELINE_INIT receipt.

    Returns {state, receipt}.
    """
    state = create_pipeline_state(beat_cluster_id, project_id, beat_count)

    receipt = write_receipt(
        stage_name="PIPELINE_INIT",
        agent_name="pipeline_commander",
        input_payload={
            "beat_cluster_id": beat_cluster_id,
            "project_id": project_id,
            "beat_count": beat_count,
        },
        output_payload=state,
        previous_receipt=previous_receipt,
        output_dir=output_dir,
    )

    return {"state": state, "receipt": receipt}


def run_batch_queue_manage(
    queue: dict,
    action: str,
    output_dir: str = ".",
    previous_receipt: Optional[dict] = None,
    **kwargs: Any,
) -> dict:
    """
    Manage the batch queue. Writes BATCH_QUEUE_MANAGE receipt.

    Actions: 'enqueue', 'dequeue', 'complete', 'status'.
    """
    result: Any = None
    if action == "enqueue":
        result = enqueue_job(
            queue,
            pipeline_id=kwargs.get("pipeline_id", generate_pipeline_id()),
            beat_cluster_id=kwargs.get("beat_cluster_id", ""),
            project_id=kwargs.get("project_id", ""),
            priority=kwargs.get("priority", 50),
            auto_approve=kwargs.get("auto_approve", False),
        )
    elif action == "dequeue":
        result = dequeue_next(queue)
    elif action == "complete":
        result = complete_job(
            queue,
            pipeline_id=kwargs.get("pipeline_id", ""),
            success=kwargs.get("success", True),
        )
    elif action == "status":
        result = get_queue_status(queue)
    else:
        result = {"error": f"Unknown action: {action}"}

    receipt = write_receipt(
        stage_name="BATCH_QUEUE_MANAGE",
        agent_name="pipeline_commander",
        input_payload={"action": action, **kwargs},
        output_payload=result if result else {"action": action, "result": None},
        previous_receipt=previous_receipt,
        output_dir=output_dir,
    )

    return {"result": result, "receipt": receipt}
