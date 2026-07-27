"""
Gate L — Pre-Pipeline Constraint Network (Pipeline Integrity Assurance).

FR-VID-09 §6: Before starting a new video pipeline, the commander must
answer ALL 6 questions. Violations prevent wasted pipeline execution.

Gate L Questions:
  Q1: Upstream asset completeness — beat cluster JSON + voiceover + music?
  Q2: RunningHub availability — proxy endpoints reachable?
  Q3: Concurrent budget — within batch queue limit?
  Q4: Disk space — ≥10GB free?
  Q5: Module health check — all 8 modules available?
  Q6: Resume detection — existing checkpoint for this beat_cluster_id?
"""

import logging
import os
from typing import Any, Optional

try:
    from .pipeline_commander import DEFAULT_CONCURRENT_LIMIT
except ImportError:
    from pipeline_commander import DEFAULT_CONCURRENT_LIMIT


logger = logging.getLogger("cmf.gate_l")

# Minimum disk space required — FR-VID-09 §6 Gate L Q4
MIN_DISK_SPACE_GB = 10

# All 8 downstream module names — FR-VID-09 §6 Gate L Q5
REQUIRED_MODULES = [
    "beat_cluster_parser",     # FR-VID-01 (parse)
    "timeline_generator",      # FR-VID-01 (assemble)
    "runninghub_client",       # FR-VID-02
    "i2v_client",              # FR-VID-03
    "t2i_quality_gate",        # FR-VID-04
    "fingerprint_tracker",     # FR-VID-05
    "audio_engine",            # FR-VID-06
    "caption_engine",          # FR-VID-07
    "render_orchestrator",     # FR-VID-08
]


# ---------------------------------------------------------------------------
# Q1 — Upstream Asset Completeness
# ---------------------------------------------------------------------------


def check_upstream_assets(
    beat_cluster_json: Any,
    voiceover_path: Optional[str],
    music_path: Optional[str],
) -> tuple[bool, str]:
    """
    Q1: Are all required upstream assets present?

    beat_cluster_json must be non-empty, voiceover and music paths must be provided.
    """
    missing = []
    if not beat_cluster_json:
        missing.append("beat_cluster_json")
    if not voiceover_path or not voiceover_path.strip():
        missing.append("voiceover_path")
    if not music_path or not music_path.strip():
        missing.append("music_path")

    if missing:
        return False, f"ASSETS_MISSING:{','.join(missing)}"
    return True, "OK"


# ---------------------------------------------------------------------------
# Q2 — RunningHub Availability
# ---------------------------------------------------------------------------


def check_runninghub_availability(
    t2i_reachable: bool, i2v_reachable: bool
) -> tuple[bool, str]:
    """
    Q2: Are both RunningHub proxy endpoints reachable?

    Accepts pre-checked reachability booleans (actual HTTP checks happen
    at the caller level — this validates the results).
    """
    unreachable = []
    if not t2i_reachable:
        unreachable.append("T2I_proxy")
    if not i2v_reachable:
        unreachable.append("I2V_proxy_plus")

    if unreachable:
        return False, f"RUNNINGHUB_UNREACHABLE:{','.join(unreachable)}"
    return True, "OK"


# ---------------------------------------------------------------------------
# Q3 — Concurrent Budget
# ---------------------------------------------------------------------------


def check_concurrent_budget(
    current_processing: int, concurrent_limit: int = DEFAULT_CONCURRENT_LIMIT
) -> tuple[bool, str]:
    """
    Q3: Is the batch queue within the concurrent processing limit?

    Returns pass if current_processing < concurrent_limit.
    """
    if current_processing >= concurrent_limit:
        return False, (
            f"CONCURRENT_LIMIT_REACHED(current={current_processing},"
            f"limit={concurrent_limit})"
        )
    return True, "OK"


# ---------------------------------------------------------------------------
# Q4 — Disk Space
# ---------------------------------------------------------------------------


def check_disk_space(
    free_space_gb: float, min_required_gb: float = MIN_DISK_SPACE_GB
) -> tuple[bool, str]:
    """
    Q4: Is there sufficient disk space (≥10GB free)?

    Accepts pre-computed free space in GB.
    """
    if free_space_gb < min_required_gb:
        return False, (
            f"INSUFFICIENT_DISK(free={free_space_gb:.1f}GB,"
            f"required={min_required_gb}GB)"
        )
    return True, "OK"


# ---------------------------------------------------------------------------
# Q5 — Module Health Check
# ---------------------------------------------------------------------------


def check_module_health(
    module_status: dict[str, bool],
) -> tuple[bool, str]:
    """
    Q5: Do all 8 downstream modules respond to health checks?

    module_status maps module_name → is_healthy boolean.
    """
    unhealthy = []
    for mod in REQUIRED_MODULES:
        if not module_status.get(mod, False):
            unhealthy.append(mod)

    if unhealthy:
        return False, f"MODULES_UNHEALTHY:{','.join(unhealthy)}"
    return True, "OK"


# ---------------------------------------------------------------------------
# Q6 — Resume Detection
# ---------------------------------------------------------------------------


def check_resume_detection(
    checkpoint_path: Optional[str],
) -> tuple[bool, str]:
    """
    Q6: Is there an existing checkpoint for this beat_cluster_id?

    Returns (True, checkpoint_path) if a checkpoint exists,
    (True, "NO_CHECKPOINT") if none found. Never fails — it's informational.
    The commander decides whether to resume or start fresh.
    """
    if checkpoint_path:
        return True, f"CHECKPOINT_FOUND:{checkpoint_path}"
    return True, "NO_CHECKPOINT"


# ---------------------------------------------------------------------------
# Gate L Runner
# ---------------------------------------------------------------------------


def run_gate_l(
    beat_cluster_json: Any,
    voiceover_path: Optional[str],
    music_path: Optional[str],
    t2i_reachable: bool = True,
    i2v_reachable: bool = True,
    current_processing: int = 0,
    concurrent_limit: int = DEFAULT_CONCURRENT_LIMIT,
    free_space_gb: float = 100.0,
    module_status: Optional[dict[str, bool]] = None,
    checkpoint_path: Optional[str] = None,
) -> dict:
    """
    Run all 6 Gate L questions. Returns gate result dict.

    Q6 (resume detection) is informational — it never blocks the pipeline.
    """
    if module_status is None:
        module_status = {mod: True for mod in REQUIRED_MODULES}

    q1_pass, q1_detail = check_upstream_assets(beat_cluster_json, voiceover_path, music_path)
    q2_pass, q2_detail = check_runninghub_availability(t2i_reachable, i2v_reachable)
    q3_pass, q3_detail = check_concurrent_budget(current_processing, concurrent_limit)
    q4_pass, q4_detail = check_disk_space(free_space_gb)
    q5_pass, q5_detail = check_module_health(module_status)
    q6_pass, q6_detail = check_resume_detection(checkpoint_path)

    results = [
        {"question": 1, "name": "upstream_assets", "passed": q1_pass, "detail": q1_detail},
        {"question": 2, "name": "runninghub_availability", "passed": q2_pass, "detail": q2_detail},
        {"question": 3, "name": "concurrent_budget", "passed": q3_pass, "detail": q3_detail},
        {"question": 4, "name": "disk_space", "passed": q4_pass, "detail": q4_detail},
        {"question": 5, "name": "module_health", "passed": q5_pass, "detail": q5_detail},
        {"question": 6, "name": "resume_detection", "passed": q6_pass, "detail": q6_detail},
    ]

    # Q6 is informational, never blocks
    blocking_results = [r for r in results if r["question"] != 6]
    all_passed = all(r["passed"] for r in blocking_results)

    if not all_passed:
        failed = [r for r in blocking_results if not r["passed"]]
        logger.warning(
            "Gate L FAILED — %d violation(s): %s",
            len(failed),
            [f"Q{r['question']}:{r['detail']}" for r in failed],
        )

    return {
        "gate": "L",
        "passed": all_passed,
        "results": results,
    }
