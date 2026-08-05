#!/usr/bin/env python3
"""
Harness Vision Analyst — Stage 1 of 2-Stage Harness Compilation Pipeline.

WHAT IT DOES:
  - Extracts image specimens from a raw harness .zip file.
  - For long video screenshot sequences (e.g. 50-100+ frames), automatically
    samples 15-20 evenly spaced keyframes across the timeline.
  - Sends each sampled keyframe to a vision model via OpenRouter or NVIDIA API.
  - Collapses visually duplicate frames into canonical slide/scene roles.
  - Outputs a structured `VISUAL_SYNTAX_ANALYSIS.json` file.

WHAT IT DOES NOT DO:
  - Does not write manifest.json (that is Stage 2 for the harness model e.g. GLM 5.2).
  - Does not call cmf-builder.
  - Does not render, edit, or produce any content.

SUPPORTED PROVIDERS & ENDPOINTS:
  1. OpenRouter (Default)
     Base URL: https://openrouter.ai/api/v1
     API Key:  OPENROUTER_API_KEY
     Models:   google/gemini-2.5-flash
               qwen/qwen3.7-flash
               nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
               google/gemma-4-26b-a4b-it:free
               google/gemma-4-31b-it:free

  2. NVIDIA API Catalog
     Base URL: https://integrate.api.nvidia.com/v1
     API Key:  NVIDIA_API_KEY
     Models:   nvidia/nemotron-3-ultra-550b-a55b
               meta/llama-3.2-90b-vision-instruct

USAGE:
  python harness_vision_analyst.py <path-to-harness.zip> [options]

EXAMPLES:
  # OpenRouter default with max 20 keyframe samples
  python harness_vision_analyst.py harness.zip

  # Sample max 15 keyframes from a video screenshot folder
  python harness_vision_analyst.py video_harness.zip --max-samples 15

  # NVIDIA API direct with Nemotron Ultra
  python harness_vision_analyst.py harness.zip --provider nvidia --model nvidia/nemotron-3-ultra-550b-a55b
"""

import argparse
import base64
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

DEFAULT_VISION_MODEL = "google/gemini-2.5-flash"
DEFAULT_MAX_SAMPLES = 20

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# ---------------------------------------------------------------------------
# Vision Model Prompt
# ---------------------------------------------------------------------------

PER_SLIDE_SYSTEM_PROMPT = """\
You are a Visual Syntax Analyst for the Conscious Activations Builder system.
Your job is to analyse a single slide/frame image and produce a structured JSON description
of its visual layout for harness compilation. You do NOT generate content, suggest captions,
or interpret the topic meaning of the image.

You MUST return ONLY a valid JSON object. No markdown fences. No explanation outside JSON.

Required JSON structure:
{
  "slide_index": <integer>,
  "layout_fingerprint": "<a brief structural description used to detect duplicates, e.g. 'header_text + full_bleed_photo + footer_badge'>",
  "container_zones": ["<zone_name>", ...],
  "primitives": [
    {
      "primitive_type": "<one of the canonical types>",
      "zone": "<which zone it lives in>",
      "dominant": <true if this is the visually dominant element>,
      "notes": "<any attribute observations: font weight, overlap, anchor continuity across slides, contrast>"
    }
  ],
  "reading_order": "<brief description of natural eye-path through the slide>",
  "anchor_elements": ["<elements that appear fixed/consistent across slides, e.g. badge in footer>"],
  "is_duplicate_of": <null or slide_index of the earlier slide this is visually identical to>,
  "candidate_slide_role": "<one canonical slide role from the taxonomy>"
}

Canonical primitive types: text_block, image_region, grid_cluster, comparison_pair, badge,
number_label, icon_row, caption_plate, callout_arrow, flow_diagram.

Canonical container zones: header_zone, hero_zone, footer_zone, overlay_zone, full_bleed.

Canonical slide roles: cover, numbered_item, comparison_beat, refrain_beat, photo_beat,
grid_collage, closing_question, closing_cta, closing_comparison, testimonial, single_frame.

Deduplication rule: if this slide's layout_fingerprint is structurally identical to a previous
slide (same zones, same primitive types in same positions, only TEXT CONTENT is different),
set is_duplicate_of to the slide_index of the first occurrence. Slides that are duplicates
contribute the same slide role but are NOT counted as unique visual syntax patterns.
"""

# ---------------------------------------------------------------------------
# Core Functions
# ---------------------------------------------------------------------------


def resolve_api_credentials(provider: str | None, base_url_arg: str | None, api_key_arg: str | None, model: str) -> tuple[str, str]:
    """Determine the base_url and api_key to use."""
    api_key = api_key_arg or ""
    base_url = base_url_arg or ""

    if not provider:
        if base_url_arg and "nvidia.com" in base_url_arg:
            provider = "nvidia"
        elif "integrate.api.nvidia.com" in base_url:
            provider = "nvidia"
        else:
            provider = "openrouter"

    if provider == "nvidia":
        base_url = base_url or NVIDIA_BASE_URL
        api_key = api_key or os.environ.get("NVIDIA_API_KEY", "").strip() or os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            sys.exit("ERROR: Neither NVIDIA_API_KEY nor OPENROUTER_API_KEY environment variable is set.")
    else:
        base_url = base_url or OPENROUTER_BASE_URL
        api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            sys.exit("ERROR: OPENROUTER_API_KEY environment variable is not set.")

    return base_url, api_key


def extract_images(zip_path: Path, max_samples: int = DEFAULT_MAX_SAMPLES) -> list[tuple[str, bytes]]:
    """
    Return list of (filename, image_bytes) sorted by filename.
    If total images exceed max_samples, sample max_samples keyframes evenly across the sequence.
    """
    with zipfile.ZipFile(zip_path, "r") as zf:
        all_names = sorted(
            n for n in zf.namelist()
            if Path(n).suffix.lower() in IMAGE_EXTENSIONS
        )
        if not all_names:
            sys.exit(
                f"ERROR: No image files found in {zip_path.name}.\n"
                "This zip contains 0 visual specimens. Per system rule, harnesses with 0 images cannot be processed."
            )

        total = len(all_names)
        if total > max_samples:
            # Sample max_samples evenly spaced frames including start and end
            indices = [int(i * (total - 1) / (max_samples - 1)) for i in range(max_samples)]
            sampled_names = [all_names[idx] for idx in sorted(set(indices))]
            print(f"  Note: Sequence has {total} images. Sampling {len(sampled_names)} evenly spaced keyframes across timeline.")
        else:
            sampled_names = all_names

        images = [(name, zf.read(name)) for name in sampled_names]
    return images


def image_to_data_url(image_bytes: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower().lstrip(".")
    mime = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
        "gif": "image/gif",
    }.get(ext, "image/jpeg")
    b64 = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime};base64,{b64}"


def analyse_slide(client, model: str, slide_index: int, filename: str, image_bytes: bytes) -> dict:
    """Call the vision model for a single slide. Returns parsed JSON dict."""
    data_url = image_to_data_url(image_bytes, filename)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": PER_SLIDE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Analyse frame {slide_index} (filename: {filename}). Return ONLY the JSON object as specified.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url},
                    },
                ],
            },
        ],
        temperature=0.0,
        max_tokens=1024,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  WARNING: Could not parse JSON for frame {slide_index}. Raw response:\n{raw[:300]}")
        result = {
            "slide_index": slide_index,
            "parse_error": str(e),
            "raw_response": raw[:500],
            "layout_fingerprint": "PARSE_ERROR",
            "container_zones": [],
            "primitives": [],
            "reading_order": "",
            "anchor_elements": [],
            "is_duplicate_of": None,
            "candidate_slide_role": "UNKNOWN",
        }
    result["slide_index"] = slide_index
    result["source_filename"] = filename
    return result


def build_deduplication_summary(slide_analyses: list[dict]) -> dict:
    """Collapse duplicate slides/frames into unique layout groups."""
    unique_layouts = {}
    unique_roles = []
    duplicate_count = 0

    for s in slide_analyses:
        fp = s.get("layout_fingerprint", "")
        is_dup = s.get("is_duplicate_of")
        if is_dup is not None:
            duplicate_count += 1
            continue
        if fp not in unique_layouts:
            unique_layouts[fp] = s["slide_index"]
            unique_roles.append({
                "slide_role": s.get("candidate_slide_role", "UNKNOWN"),
                "first_slide_index": s["slide_index"],
                "layout_fingerprint": fp,
                "container_zones": s.get("container_zones", []),
                "primitives": s.get("primitives", []),
                "reading_order": s.get("reading_order", ""),
                "anchor_elements": s.get("anchor_elements", []),
            })

    return {
        "total_slides_analysed": len(slide_analyses),
        "unique_layout_count": len(unique_roles),
        "duplicate_slides_collapsed": duplicate_count,
        "unique_slide_roles": unique_roles,
    }


def run(zip_path: Path, model: str, provider: str | None, base_url_arg: str | None, api_key_arg: str | None, max_samples: int, output_dir: Path) -> None:
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("ERROR: openai package not installed. Run: pip install openai")

    base_url, api_key = resolve_api_credentials(provider, base_url_arg, api_key_arg, model)

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    print(f"Harness Vision Analyst")
    print(f"  Input zip:     {zip_path}")
    print(f"  Base URL:      {base_url}")
    print(f"  Vision model:  {model}")
    print(f"  Max keyframes: {max_samples}")
    print(f"  Output dir:    {output_dir}")
    print()

    images = extract_images(zip_path, max_samples=max_samples)
    print(f"Processing {len(images)} keyframe specimen(s).")
    print()

    slide_analyses = []
    for i, (filename, image_bytes) in enumerate(images, start=1):
        print(f"  [{i:02d}/{len(images)}] Analysing {filename}...", end=" ", flush=True)
        result = analyse_slide(client, model, i, filename, image_bytes)
        is_dup = result.get("is_duplicate_of")
        role = result.get("candidate_slide_role", "?")
        fp = result.get("layout_fingerprint", "")[:60]
        if is_dup:
            print(f"DUPLICATE of frame {is_dup} ({role}) | {fp}")
        else:
            print(f"UNIQUE -> {role} | {fp}")
        slide_analyses.append(result)

    print()
    dedup = build_deduplication_summary(slide_analyses)
    print(f"Visual Syntax Deduplication Summary:")
    print(f"  Total keyframes analysed:  {dedup['total_slides_analysed']}")
    print(f"  Unique layout patterns:    {dedup['unique_layout_count']}")
    print(f"  Duplicates collapsed:      {dedup['duplicate_slides_collapsed']}")
    print()

    harness_name = zip_path.stem
    zip_sha256 = hashlib.sha256(zip_path.read_bytes()).hexdigest()

    output = {
        "schema": "harness-visual-syntax-analysis/v1",
        "harness_name": harness_name,
        "source_zip": zip_path.name,
        "source_zip_sha256": zip_sha256,
        "vision_model_used": model,
        "base_url": base_url,
        "max_samples": max_samples,
        "deduplication_summary": dedup,
        "all_slide_analyses": slide_analyses,
        "stage_2_instructions": (
            "Feed this file together with the harness drill markdown files "
            "(ONE_HARNESS_BUILD_PROMPT.md, DRILL_ME_FORMAT.md, HARNESS_GAP_ANALYSIS_AND_BUILD_SKILL.md) "
            "to the manifest authoring model (GLM 5.2 or equivalent non-vision model). "
            "The authoring model must produce manifest.json using ONLY deduplication_summary.unique_slide_roles "
            "as its visual syntax source — it must NOT re-derive layout from raw images."
        ),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{harness_name}_VISUAL_SYNTAX_ANALYSIS.json"
    out_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved: {out_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage 1 Vision Analyst — analyses harness specimens via OpenRouter or NVIDIA vision models.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # OpenRouter default (Gemini Flash, max 20 keyframes)
  python harness_vision_analyst.py atomic_harnesses_visual_syntax/format04_conscious_reaction/format04_tier_list.zip

  # Sample max 15 keyframes from a video screenshot folder
  python harness_vision_analyst.py video_harness.zip --max-samples 15

  # NVIDIA API direct
  python harness_vision_analyst.py harness.zip --provider nvidia --model nvidia/nemotron-3-ultra-550b-a55b
""",
    )
    parser.add_argument("zip_path", type=Path, help="Path to the raw harness .zip file.")
    parser.add_argument(
        "--model",
        type=str,
        default=os.environ.get("VISION_MODEL", DEFAULT_VISION_MODEL),
        help=f"Vision model slug (default: {DEFAULT_VISION_MODEL}).",
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=["openrouter", "nvidia"],
        help="Provider preset: 'openrouter' (https://openrouter.ai/api/v1) or 'nvidia' (https://integrate.api.nvidia.com/v1).",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=DEFAULT_MAX_SAMPLES,
        help=f"Maximum keyframe screenshots to sample across timeline (default: {DEFAULT_MAX_SAMPLES}).",
    )
    parser.add_argument("--base-url", type=str, help="Custom OpenAI-compatible base URL.")
    parser.add_argument("--api-key", type=str, help="API key (overrides OPENROUTER_API_KEY / NVIDIA_API_KEY).")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("tools/vision_analysis_output"),
        help="Directory to write the VISUAL_SYNTAX_ANALYSIS.json output.",
    )

    args = parser.parse_args()

    if not args.zip_path.exists():
        sys.exit(f"ERROR: File not found: {args.zip_path}")
    if not zipfile.is_zipfile(args.zip_path):
        sys.exit(f"ERROR: Not a valid zip file: {args.zip_path}")

    run(args.zip_path, args.model, args.provider, args.base_url, args.api_key, args.max_samples, args.output_dir)


if __name__ == "__main__":
    main()
