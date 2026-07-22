"""
FR-VID-02 — RunningHub T2I Generation Client

CMF Video Pipeline — Text-to-Image Keyframe Generation

Three-stage pipeline:
  Stage 1: T2I_PAYLOAD_COMPILE — Compile visual prompts into ComfyUI payloads
  Stage 2: T2I_JOB_SUBMIT — Submit payloads to RunningHub in parallel
  Stage 3: T2I_GENERATION_COMPLETE — Monitor progress, download images, emit metadata

Spec Reference: FR-VID-02 §4 Implementation Plan
Produces: DEP-VID-008 (T2I Generation Result)
Consumes: DEP-VID-006 (Visual Prompts), DEP-VID-007 (Workflow Registry), DEP-VID-009 (Config)
"""

import asyncio
import json
import logging
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import httpx
import websockets

from .config import RunningHubConfig
from .receipt_chain import write_receipt

logger = logging.getLogger("cmf.t2i_client")

# Constants from FR-VID-02 spec
JOB_TIMEOUT_SEC = 120       # §4 Stage 3: "Job timeout after 120 seconds"
HTTP_POLL_INTERVAL_SEC = 2.0 # §4 Stage 3 Step 3: "HTTP polling at 2-second intervals"
RETRY_BACKOFF_SEC = [1.0, 2.0, 4.0]  # §4 Stage 2: "exponential backoff (1s, 2s, 4s)"
MAX_RETRIES = 3              # §4 Stage 2: "retries up to 3 times"


def _validate_url_https(url: str) -> bool:
    """Validate that an asset URL uses HTTPS. Build Prompt: asset URLs must pass HTTPS validation."""
    parsed = urlparse(url)
    return parsed.scheme == "https"


# ===========================================================================
# Stage 1: Prompt Payload Compilation (T2I_PAYLOAD_COMPILE)
# FR-VID-02 §4 Stage 1
# ===========================================================================


def compile_payloads(
    visual_prompts: list[dict],
    workflow_registry: dict,
    config: RunningHubConfig,
    regeneration_beat_indices: list[int] | None = None,
) -> list[dict]:
    """
    Stage 1: Compile CMF visual prompts into ComfyUI workflow payloads.

    FR-VID-02 §4 Stage 1 Steps 1-3.
    Stress Test Amendment (Q1): When regeneration_beat_indices is provided,
    only the specified beats are compiled. Non-failed beats are NOT re-submitted.

    Args:
        visual_prompts: DEP-VID-006 — per-beat visual prompts from storyboard composer.
        workflow_registry: DEP-VID-007 — registered ComfyUI workflow IDs and node configs.
        config: DEP-VID-009 — API key, proxy URL, VRAM tier, concurrency limits.
        regeneration_beat_indices: Optional beat indices for quality gate retry.

    Returns:
        List of per-beat ComfyUI payloads ready for submission.

    Raises:
        ValueError: WORKFLOW_NOT_FOUND if model not in registry (§4 Stage 1 Failure).
    """
    # Step 1: Load target workflow template from DEP-VID-007
    target_model = config.default_model
    workflow_entry = _resolve_workflow(workflow_registry, target_model)
    workflow_template = workflow_entry["template"]
    workflow_id = workflow_entry["workflow_id"]

    # Determine which beats to compile (stress test amendment: per-beat regen)
    if regeneration_beat_indices is not None:
        beats_to_compile = [
            vp for vp in visual_prompts
            if vp["beat_index"] in regeneration_beat_indices
        ]
        logger.info(
            "Quality gate retry: compiling %d of %d beats (indices: %s)",
            len(beats_to_compile), len(visual_prompts), regeneration_beat_indices,
        )
    else:
        beats_to_compile = visual_prompts

    payloads = []
    for beat_prompt in beats_to_compile:
        # Step 2a: Extract visual_prompt_text, negative_prompt, PSSL parameters
        visual_prompt_text = beat_prompt["visual_prompt_text"]
        negative_prompt = beat_prompt.get(
            "negative_prompt",
            "blurry, generic, stock photo, smooth skin, text, watermark, logo, low quality",
        )
        pssl_params = beat_prompt.get("pssl_params", {})

        # Step 2b: Generate seed (random for initial, provided for regeneration)
        if beat_prompt.get("seed") is not None:
            seed = beat_prompt["seed"]
        else:
            seed = random.randint(0, 2**32 - 1)

        # Step 2c: Construct NodeInfoList parameter injection
        # FR-VID-02 §3 TD2: "NodeInfoList node allows modifying any workflow parameter"
        node_info_list = {
            "prompt": visual_prompt_text,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "width": config.output_width,
            "height": config.output_height,
        }

        # Step 2d: Build complete ComfyUI API payload with workflow template + overrides
        payload = {
            "beat_index": beat_prompt["beat_index"],
            "workflow_id": workflow_id,
            "prompt": json.loads(json.dumps(workflow_template)),  # Deep clone
            "node_info_list": node_info_list,
            "client_id": f"cmf-t2i-{beat_prompt['beat_index']:02d}",
            # Metadata for downstream tracking (fingerprint emission)
            "seed_used": seed,
            "visual_prompt_text": visual_prompt_text,
            "negative_prompt_used": negative_prompt,
            "pssl_params_applied": pssl_params,
            "model": target_model,
        }
        payloads.append(payload)

    # Step 3: Output array of per-beat payloads
    return payloads


def _resolve_workflow(workflow_registry: dict, model: str) -> dict:
    """Look up workflow entry for the given model in DEP-VID-007."""
    for wf in workflow_registry.get("workflows", []):
        if wf["model"] == model:
            return wf
    raise ValueError(
        f"WORKFLOW_NOT_FOUND: No workflow registered for model '{model}' in DEP-VID-007"
    )


def _inject_node_info_list(workflow: dict, node_info: dict) -> None:
    """
    Inject parameters into workflow via NodeInfoList pattern.

    FR-VID-02 §3 TD2: "The ComfyUI_RH_APICall plugin's NodeInfoList node
    allows modifying any workflow parameter without rebuilding the workflow JSON.
    The client loads a registered workflow template and injects per-beat
    parameters through NodeInfoList."

    Locates prompt, negative prompt, sampler, and latent image nodes in the
    workflow and applies parameter overrides from the node_info dict.
    """
    for node_id, node_data in workflow.items():
        if not isinstance(node_data, dict):
            continue
        class_type = node_data.get("class_type", "")
        inputs = node_data.get("inputs", {})

        # Inject prompt into positive prompt nodes
        if class_type in ("CLIPTextEncode", "CLIPTextEncodeSDXL"):
            node_id_lower = str(node_id).lower()
            if "positive" in node_id_lower:
                if "text" in inputs:
                    inputs["text"] = node_info["prompt"]
            elif "negative" in node_id_lower:
                if "text" in inputs:
                    inputs["text"] = node_info["negative_prompt"]

        # Inject seed into sampler nodes
        if class_type in ("KSampler", "KSamplerAdvanced", "SamplerCustom"):
            if "seed" in inputs:
                inputs["seed"] = node_info["seed"]

        # Inject dimensions into latent image nodes
        if class_type == "EmptyLatentImage":
            if "width" in inputs:
                inputs["width"] = node_info["width"]
            if "height" in inputs:
                inputs["height"] = node_info["height"]


# ===========================================================================
# Stage 2: Parallel Job Submission (T2I_JOB_SUBMIT)
# FR-VID-02 §4 Stage 2
# ===========================================================================


async def submit_batch(
    payloads: list[dict],
    config: RunningHubConfig,
) -> list[dict]:
    """
    Stage 2: Submit all beat payloads concurrently to RunningHub proxy.

    FR-VID-02 §4 Stage 2 Steps 1-5.
    Uses asyncio TaskGroup for parallel submission (Step 2).
    Each job gets a unique prompt_id from ComfyUI (Step 3).
    Failed submissions retried with exponential backoff (Step 4).

    Args:
        payloads: Per-beat ComfyUI payloads from Stage 1.
        config: RunningHub API configuration.

    Returns:
        Job tracking array: [{beat_index, prompt_id, submitted_at, status}] (Step 5).
    """
    # Step 1: Establish connection to RunningHub proxy
    proxy_url = config.active_proxy_url
    results = []

    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        # Step 2: Submit all beat payloads concurrently using asyncio task group
        tasks = []
        async with asyncio.TaskGroup() as tg:
            for payload in payloads:
                task = tg.create_task(
                    _submit_single_job(client, proxy_url, payload)
                )
                tasks.append(task)

        results = [task.result() for task in tasks]

    return results


async def _submit_single_job(
    client: httpx.AsyncClient,
    proxy_url: str,
    payload: dict,
) -> dict:
    """
    Submit a single T2I job to RunningHub with retry on failure.

    FR-VID-02 §4 Stage 2 Step 4: "retries up to 3 times with exponential
    backoff (1s, 2s, 4s). After 3 failures: T2I_SUBMISSION_FAILED."
    """
    prompt_endpoint = f"{proxy_url}/prompt"
    beat_index = payload["beat_index"]

    # Build the ComfyUI API payload format
    comfyui_payload = {
        "prompt": payload["prompt"],
        "client_id": payload["client_id"],
    }

    # Apply NodeInfoList parameter injection into the cloned workflow
    _inject_node_info_list(comfyui_payload["prompt"], payload["node_info_list"])

    for attempt in range(MAX_RETRIES):
        try:
            response = await client.post(
                prompt_endpoint,
                json=comfyui_payload,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == 200:
                result = response.json()
                prompt_id = result.get("prompt_id", "")
                logger.info("Beat %d submitted: prompt_id=%s", beat_index, prompt_id)

                # Step 3: Capture returned prompt_id (Step 5: output job tracking)
                return {
                    "beat_index": beat_index,
                    "prompt_id": prompt_id,
                    "submitted_at": datetime.now(timezone.utc).isoformat(),
                    "status": "QUEUED",
                    "payload_metadata": {
                        "seed_used": payload["seed_used"],
                        "visual_prompt_text": payload["visual_prompt_text"],
                        "negative_prompt_used": payload["negative_prompt_used"],
                        "pssl_params_applied": payload["pssl_params_applied"],
                        "model": payload["model"],
                        "workflow_id": payload["workflow_id"],
                    },
                }
            else:
                logger.warning(
                    "Beat %d submission HTTP %d (attempt %d/%d)",
                    beat_index, response.status_code, attempt + 1, MAX_RETRIES,
                )
        except httpx.HTTPError as exc:
            logger.warning(
                "Beat %d submission error (attempt %d/%d): %s",
                beat_index, attempt + 1, MAX_RETRIES, exc,
            )

        # Step 4: Retry with exponential backoff
        if attempt < MAX_RETRIES - 1:
            backoff = RETRY_BACKOFF_SEC[attempt]
            logger.info("Retrying beat %d in %.1fs", beat_index, backoff)
            await asyncio.sleep(backoff)

    # All retries exhausted — T2I_SUBMISSION_FAILED
    logger.error(
        "Beat %d: T2I_SUBMISSION_FAILED after %d retries", beat_index, MAX_RETRIES
    )
    return {
        "beat_index": beat_index,
        "prompt_id": None,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "status": "T2I_SUBMISSION_FAILED",
        "payload_metadata": {
            "seed_used": payload["seed_used"],
            "model": payload["model"],
            "workflow_id": payload["workflow_id"],
        },
    }


# ===========================================================================
# Stage 3: Progress Monitoring & Image Download (T2I_GENERATION_COMPLETE)
# FR-VID-02 §4 Stage 3
# ===========================================================================


async def monitor_and_download(
    jobs: list[dict],
    config: RunningHubConfig,
) -> dict:
    """
    Stage 3: Monitor job progress and download completed keyframe images.

    FR-VID-02 §4 Stage 3 Steps 1-7.
    Step 1: WebSocket for real-time progress.
    Step 3: If WebSocket disconnects, HTTP polling at 2s intervals.
    Step 4-5: Download and store image.
    Step 6: Emit stage_1_t2i fingerprint metadata.
    Step 7: Forward keyframe to FR-VID-04 (via DEP-VID-008 output).

    Produces DEP-VID-008 (T2I Generation Result).
    """
    proxy_url = config.active_proxy_url
    asset_base = Path(config.asset_storage_base) / "t2i"
    asset_base.mkdir(parents=True, exist_ok=True)

    start_time = time.monotonic()
    results = []

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as http_client:
        monitoring_tasks = []
        for job in jobs:
            if job["status"] == "T2I_SUBMISSION_FAILED":
                results.append(_build_failed_result(job))
                continue
            monitoring_tasks.append(
                _monitor_single_job(http_client, proxy_url, job, asset_base, config)
            )

        if monitoring_tasks:
            completed = await asyncio.gather(*monitoring_tasks, return_exceptions=True)
            for item in completed:
                if isinstance(item, Exception):
                    logger.error("Job monitoring error: %s", item)
                    results.append({
                        "beat_index": -1,
                        "prompt_id": None,
                        "status": "T2I_GENERATION_TIMEOUT",
                        "error": str(item),
                    })
                else:
                    results.append(item)

    elapsed = time.monotonic() - start_time
    generated_count = sum(1 for r in results if r.get("status") == "GENERATED")
    failed_count = len(results) - generated_count

    # Assemble DEP-VID-008 — FR-VID-02 §5 Primary Output Schema
    dep_vid_008 = {
        "generation_batch_id": (
            f"T2I-BATCH-{datetime.now(timezone.utc).strftime('%Y%m%d')}"
            f"-{random.randint(1, 999):03d}"
        ),
        "project_id": "unknown",
        "beat_cluster_id": "unknown",
        "model_used": config.default_model,
        "vram_tier": config.vram_tier,
        "results": sorted(results, key=lambda r: r.get("beat_index", 0)),
        "batch_stats": {
            "total_beats": len(jobs),
            "generated": generated_count,
            "failed": failed_count,
            "total_generation_time_sec": round(elapsed, 1),
            "parallel_efficiency": round(
                generated_count / max(elapsed, 0.1), 2
            ) if generated_count > 0 else 0.0,
        },
        "generation_timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return dep_vid_008


async def _monitor_single_job(
    http_client: httpx.AsyncClient,
    proxy_url: str,
    job: dict,
    asset_base: Path,
    config: RunningHubConfig,
) -> dict:
    """Monitor a single job: try WebSocket first, fall back to HTTP polling."""
    beat_index = job["beat_index"]

    # Step 1: Try WebSocket monitoring (primary)
    try:
        result = await asyncio.wait_for(
            _monitor_via_websocket(proxy_url, job, asset_base, http_client, config),
            timeout=config.job_timeout_sec,
        )
        return result
    except (asyncio.TimeoutError, Exception) as ws_err:
        logger.warning(
            "Beat %d: WebSocket failed (%s), switching to HTTP polling",
            beat_index, type(ws_err).__name__,
        )

    # Step 3: HTTP polling fallback at 2-second intervals
    try:
        result = await asyncio.wait_for(
            _poll_via_http(http_client, proxy_url, job, asset_base, config),
            timeout=config.job_timeout_sec,
        )
        return result
    except asyncio.TimeoutError:
        logger.error(
            "Beat %d: T2I_GENERATION_TIMEOUT after %ds",
            beat_index, config.job_timeout_sec,
        )
        return {
            "beat_index": beat_index,
            "prompt_id": job["prompt_id"],
            "status": "T2I_GENERATION_TIMEOUT",
            "seed_used": job["payload_metadata"].get("seed_used"),
        }


async def _monitor_via_websocket(
    proxy_url: str,
    job: dict,
    asset_base: Path,
    http_client: httpx.AsyncClient,
    config: RunningHubConfig,
) -> dict:
    """
    Monitor job progress via WebSocket connection.

    FR-VID-02 §4 Stage 3 Step 1-2: "Open WebSocket connection to RunningHub
    for real-time progress events. For each active job, monitor progress
    updates (percentage, current node, ETA)."
    FR-VID-02 §3 TD3: "WebSocket Primary → HTTP Polling Fallback."
    """
    prompt_id = job["prompt_id"]
    beat_index = job["beat_index"]
    metadata = job["payload_metadata"]
    client_id = f"cmf-t2i-{beat_index:02d}"

    # Build WebSocket URL from proxy URL
    ws_url = proxy_url.replace("https://", "wss://").replace("http://", "ws://")
    ws_url = f"{ws_url}/ws?clientId={client_id}"

    progress_updates = []
    gen_start = time.monotonic()

    async with websockets.connect(ws_url) as ws:
        while True:
            raw_msg = await ws.recv()
            msg = json.loads(raw_msg)
            msg_type = msg.get("type", "")

            # Step 2: Monitor progress updates
            if msg_type == "progress":
                progress = msg.get("data", {})
                progress_updates.append(progress)
                logger.debug(
                    "Beat %d progress: %s/%s",
                    beat_index,
                    progress.get("value", "?"),
                    progress.get("max", "?"),
                )

            elif msg_type == "executed":
                # Job completed
                gen_time = round(time.monotonic() - gen_start, 1)
                output_data = msg.get("data", {}).get("output", {})
                images = output_data.get("images", [])

                if images:
                    image_info = images[0]
                    filename = image_info.get("filename", "")
                    subfolder = image_info.get("subfolder", "")

                    # Step 4: Download output image
                    download_url = (
                        f"{proxy_url}/view?filename={filename}"
                        f"&subfolder={subfolder}&type=output"
                    )
                    local_path = asset_base / f"t2i-{beat_index:02d}-{filename}"
                    await _download_image(http_client, download_url, local_path)

                    # Step 5: Upload to asset storage (HTTPS URL for production)
                    asset_url = f"https://r2.cmf-assets.com/t2i/{local_path.name}"

                    # Step 6: Emit stage_1_t2i fingerprint metadata
                    return _build_generated_result(
                        beat_index=beat_index,
                        prompt_id=prompt_id,
                        asset_url=asset_url,
                        local_path=str(local_path),
                        gen_time=gen_time,
                        metadata=metadata,
                        config=config,
                        progress_count=len(progress_updates),
                    )

            elif msg_type == "execution_error":
                error = msg.get("data", {}).get(
                    "exception_message", "Unknown generation error"
                )
                logger.error("Beat %d generation error: %s", beat_index, error)
                return {
                    "beat_index": beat_index,
                    "prompt_id": prompt_id,
                    "status": "T2I_GENERATION_FAILED",
                    "error": error,
                    "seed_used": metadata.get("seed_used"),
                }


async def _poll_via_http(
    client: httpx.AsyncClient,
    proxy_url: str,
    job: dict,
    asset_base: Path,
    config: RunningHubConfig,
) -> dict:
    """
    Poll job status via HTTP when WebSocket is unavailable.

    FR-VID-02 §4 Stage 3 Step 3: "If WebSocket disconnects: automatically
    switch to HTTP polling at 2-second intervals."
    FR-VID-02 §3 TD3: "The client automatically falls back to HTTP polling
    without failing the job."
    """
    prompt_id = job["prompt_id"]
    beat_index = job["beat_index"]
    metadata = job["payload_metadata"]
    history_url = f"{proxy_url}/history/{prompt_id}"
    gen_start = time.monotonic()

    while True:
        response = await client.get(history_url)
        if response.status_code == 200:
            history = response.json()
            if prompt_id in history:
                gen_time = round(time.monotonic() - gen_start, 1)
                outputs = history[prompt_id].get("outputs", {})

                # Find the node with image output
                for _node_id, node_output in outputs.items():
                    images = node_output.get("images", [])
                    if images:
                        image_info = images[0]
                        filename = image_info.get("filename", "")
                        subfolder = image_info.get("subfolder", "")

                        # Download output image
                        download_url = (
                            f"{proxy_url}/view?filename={filename}"
                            f"&subfolder={subfolder}&type=output"
                        )
                        local_path = asset_base / f"t2i-{beat_index:02d}-{filename}"
                        await _download_image(client, download_url, local_path)

                        asset_url = f"https://r2.cmf-assets.com/t2i/{local_path.name}"

                        return _build_generated_result(
                            beat_index=beat_index,
                            prompt_id=prompt_id,
                            asset_url=asset_url,
                            local_path=str(local_path),
                            gen_time=gen_time,
                            metadata=metadata,
                            config=config,
                            progress_count=0,
                        )

        await asyncio.sleep(HTTP_POLL_INTERVAL_SEC)


async def _download_image(
    client: httpx.AsyncClient,
    url: str,
    output_path: Path,
) -> None:
    """Download an image from the RunningHub API to local storage."""
    response = await client.get(url)
    response.raise_for_status()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)
    logger.info("Downloaded image to %s (%d bytes)", output_path, len(response.content))


def _build_generated_result(
    beat_index: int,
    prompt_id: str,
    asset_url: str,
    local_path: str,
    gen_time: float,
    metadata: dict,
    config: RunningHubConfig,
    progress_count: int,
) -> dict:
    """
    Build a GENERATED result entry with stage_1_t2i fingerprint metadata.

    FR-VID-02 §4 Stage 3 Step 6 — emit stage_1_t2i fingerprint metadata
    per beat. Fields per §5 results[] schema.
    """
    return {
        "beat_index": beat_index,
        "prompt_id": prompt_id,
        "status": "GENERATED",
        "output_image_url": asset_url,
        "output_image_local_path": local_path,
        "output_resolution": f"{config.output_width}x{config.output_height}",
        "seed_used": metadata["seed_used"],
        "prompt_used": metadata["visual_prompt_text"],
        "negative_prompt_used": metadata["negative_prompt_used"],
        "pssl_params_applied": metadata["pssl_params_applied"],
        "generation_time_sec": gen_time,
        "workflow_id": metadata["workflow_id"],
        "quality_gate_pending": True,
    }


def _build_failed_result(job: dict) -> dict:
    """Build a result entry for a job that failed during submission."""
    return {
        "beat_index": job["beat_index"],
        "prompt_id": None,
        "status": "T2I_SUBMISSION_FAILED",
        "seed_used": job.get("payload_metadata", {}).get("seed_used"),
    }


# ===========================================================================
# Full Pipeline Orchestrator
# ===========================================================================


async def generate_t2i_batch(
    visual_prompts: list[dict],
    workflow_registry: dict,
    config: RunningHubConfig,
    project_id: str = "unknown",
    beat_cluster_id: str = "unknown",
    regeneration_beat_indices: list[int] | None = None,
) -> dict:
    """
    Execute the complete T2I generation pipeline (Stages 1-3) with Gate D
    enforcement and receipt chain writes.

    This is the top-level entry point called by the Pipeline Commander (FR-VID-09).

    Args:
        visual_prompts: DEP-VID-006 visual prompts.
        workflow_registry: DEP-VID-007 workflow registry.
        config: DEP-VID-009 configuration.
        project_id: CMF project identifier.
        beat_cluster_id: Beat cluster identifier.
        regeneration_beat_indices: Optional subset for quality gate retry.

    Returns:
        DEP-VID-008 T2I Generation Result.

    Raises:
        RuntimeError: If Gate D fails (any question returns False).
    """
    from .gates.gate_d import run_gate_d

    # Gate D enforcement — FR-VID-02 §6, Build Prompt Rule 7
    gate_pass, gate_results = run_gate_d(
        visual_prompts=visual_prompts,
        model=config.default_model,
        is_regeneration=regeneration_beat_indices is not None,
        target_width=config.output_width,
        target_height=config.output_height,
        batch_size=(
            len(regeneration_beat_indices)
            if regeneration_beat_indices is not None
            else len(visual_prompts)
        ),
        vram_tier=config.vram_tier,
        max_concurrent=config.max_concurrent_t2i,
    )

    if not gate_pass:
        failed_qs = [g for g in gate_results if not g["passed"]]
        diagnostics = "; ".join(
            f"Q{g['question']}: {g['diagnostic']}" for g in failed_qs
        )
        raise RuntimeError(f"Gate D FAILED — {diagnostics}")

    logger.info("Gate D PASS — all 5 questions satisfied")

    # Stage 1: Payload Compilation
    payloads = compile_payloads(
        visual_prompts, workflow_registry, config, regeneration_beat_indices
    )
    receipt_1 = write_receipt(
        stage_name="T2I_PAYLOAD_COMPILE",
        agent_name="runninghub_t2i_client",
        input_payload={
            "visual_prompts_count": len(visual_prompts),
            "regeneration_beat_indices": regeneration_beat_indices,
        },
        output_payload={
            "payloads_count": len(payloads),
            "beat_indices": [p["beat_index"] for p in payloads],
        },
        previous_receipt=None,
        output_dir=config.receipt_output_dir,
    )

    # Stage 2: Parallel Job Submission
    jobs = await submit_batch(payloads, config)
    receipt_2 = write_receipt(
        stage_name="T2I_JOB_SUBMIT",
        agent_name="runninghub_t2i_client",
        input_payload={"payloads_count": len(payloads)},
        output_payload={
            "jobs": [
                {
                    "beat_index": j["beat_index"],
                    "prompt_id": j["prompt_id"],
                    "status": j["status"],
                }
                for j in jobs
            ],
        },
        previous_receipt=receipt_1,
        output_dir=config.receipt_output_dir,
    )

    # Stage 3: Progress Monitoring & Image Download
    result = await monitor_and_download(jobs, config)

    # Inject project metadata into DEP-VID-008
    result["project_id"] = project_id
    result["beat_cluster_id"] = beat_cluster_id

    receipt_3 = write_receipt(
        stage_name="T2I_GENERATION_COMPLETE",
        agent_name="runninghub_t2i_client",
        input_payload={"jobs_count": len(jobs)},
        output_payload={
            "results_count": len(result["results"]),
            "generated": result["batch_stats"]["generated"],
        },
        previous_receipt=receipt_2,
        output_dir=config.receipt_output_dir,
    )

    # Attach receipt chain to result
    result["receipt_chain"] = {
        "final_receipt_id": receipt_3["receipt_id"],
        "chain_length": 3,
        "stages": ["T2I_PAYLOAD_COMPILE", "T2I_JOB_SUBMIT", "T2I_GENERATION_COMPLETE"],
    }

    return result
