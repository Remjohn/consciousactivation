#!/usr/bin/env python3
"""
Harness Vision Analyst — Stage 1 of 2-Stage Harness Compilation Pipeline.

WHAT IT DOES:
  - Extracts all image specimens from a raw harness .zip file.
  - Sends each image to a vision model via OpenRouter (e.g. google/gemini-2.5-flash).
  - Collapses visually duplicate slides into canonical slide roles.
  - Outputs a structured `VISUAL_SYNTAX_ANALYSIS.json` file.

WHAT IT DOES NOT DO:
  - Does not write the manifest.json (that is Stage 2 for the harness model e.g. GLM 5.2).
  - Does not call cmf-builder.
  - Does not render, edit, or produce any content.

USAGE:
  python harness_vision_analyst.py <path-to-harness.zip> [options]

DEPENDENCIES:
  pip install openai

ENVIRONMENT:
  OPENROUTER_API_KEY=<your key>   Required.
  VISION_MODEL=<model slug>       Optional. Default: google/gemini-2.5-flash
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
DEFAULT_VISION_MODEL = "google/gemini-2.5-flash"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Canonical slide roles from the Visual Syntax Composition Compiler skill.
# Claude/GLM will choose one per deduplicated layout group.
CANONICAL_SLIDE_ROLES = [
    "cover",
    "numbered_item",
    "comparison_beat",
    "refrain_beat",
    "photo_beat",
    "grid_collage",
    "closing_question",
    "closing_cta",
    "closing_comparison",
    "testimonial",
    "single_frame",  # supervisuals only
]

CANONICAL_PRIMITIVE_TYPES = [
    "text_block",
    "image_region",
    "grid_cluster",
    "comparison_pair",
    "badge",
    "number_label",
    "icon_row",
    "caption_plate",
    "callout_arrow",
    "flow_diagram",
]

CANONICAL_ZONES = [
    "header_zone",
    "hero_zone",
    "footer_zone",
    "overlay_zone",
    "full_bleed",
]

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


def get_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        sys.exit("ERROR: OPENROUTER_API_KEY environment variable is not set.")
    return key


def extract_images(zip_path: Path) -> list[tuple[str, bytes]]:
    """Return list of (filename, image_bytes) sorted by filename."""
    images = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = sorted(
            n for n in zf.namelist()
            if Path(n).suffix.lower() in IMAGE_EXTENSIONS
        )
        if not names:
            sys.exit(
                f"ERROR: No image files found in {zip_path.name}.\n"
                "This zip contains no visual specimens. Remove it from the harness library."
            )
        for name in names:
            images.append((name, zf.read(name)))
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
                        "text": f"Analyse slide {slide_index} (filename: {filename}). Return ONLY the JSON object as specified.",
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
    # Strip accidental markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  WARNING: Could not parse JSON for slide {slide_index}. Raw response:\n{raw[:300]}")
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
    result["slide_index"] = slide_index  # enforce correct index
    result["source_filename"] = filename
    return result


def build_deduplication_summary(slide_analyses: list[dict]) -> dict:
    """
    Collapse duplicate slides into unique layout groups.
    Returns a summary of unique visual syntax patterns.
    """
    unique_layouts = {}  # fingerprint -> first slide_index
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
        "total_slides": len(slide_analyses),
        "unique_layout_count": len(unique_roles),
        "duplicate_slides_collapsed": duplicate_count,
        "unique_slide_roles": unique_roles,
    }


def run(zip_path: Path, model: str, output_dir: Path) -> None:
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("ERROR: openai package not installed. Run: pip install openai")

    client = OpenAI(
        api_key=get_api_key(),
        base_url=OPENROUTER_BASE_URL,
    )

    print(f"Harness Vision Analyst")
    print(f"  Input zip:    {zip_path}")
    print(f"  Vision model: {model}")
    print(f"  Output dir:   {output_dir}")
    print()

    images = extract_images(zip_path)
    print(f"Found {len(images)} image specimen(s) to analyse.")
    print()

    slide_analyses = []
    for i, (filename, image_bytes) in enumerate(images, start=1):
        print(f"  [{i:02d}/{len(images)}] Analysing {filename}...", end=" ", flush=True)
        result = analyse_slide(client, model, i, filename, image_bytes)
        is_dup = result.get("is_duplicate_of")
        role = result.get("candidate_slide_role", "?")
        fp = result.get("layout_fingerprint", "")[:60]
        if is_dup:
            print(f"DUPLICATE of slide {is_dup} ({role}) | {fp}")
        else:
            print(f"UNIQUE -> {role} | {fp}")
        slide_analyses.append(result)

    print()
    dedup = build_deduplication_summary(slide_analyses)
    print(f"Visual Syntax Deduplication Summary:")
    print(f"  Total slides:              {dedup['total_slides']}")
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


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage 1 Vision Analyst — analyses harness specimens via OpenRouter vision model.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python harness_vision_analyst.py atomic_harnesses_visual_syntax/carousels/CAR-JUX-Jealousy-1-1-10.zip
  python harness_vision_analyst.py atomic_harnesses_visual_syntax/supervisuals/TWQ-IMG-Portrait.zip --model anthropic/claude-3.5-sonnet
  python harness_vision_analyst.py myharness.zip --output-dir ./analysis_output/

Environment variables:
  OPENROUTER_API_KEY   Required. Your OpenRouter API key.
  VISION_MODEL         Optional override for the vision model slug.
""",
    )
    parser.add_argument(
        "zip_path",
        type=Path,
        help="Path to the raw harness .zip file.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.environ.get("VISION_MODEL", DEFAULT_VISION_MODEL),
        help=f"OpenRouter vision model slug (default: {DEFAULT_VISION_MODEL}).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("tools/vision_analysis_output"),
        help="Directory to write the VISUAL_SYNTAX_ANALYSIS.json output (default: tools/vision_analysis_output/).",
    )

    args = parser.parse_args()

    if not args.zip_path.exists():
        sys.exit(f"ERROR: File not found: {args.zip_path}")
    if not zipfile.is_zipfile(args.zip_path):
        sys.exit(f"ERROR: Not a valid zip file: {args.zip_path}")

    run(args.zip_path, args.model, args.output_dir)


if __name__ == "__main__":
    main()
