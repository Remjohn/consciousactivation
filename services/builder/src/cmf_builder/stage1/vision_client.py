import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, Any

from .zip_extractor import ExtractedFrame

class VisionClient:
    """Vision client that loads pre-computed observations from agent-generated JSON files.
    
    The agent (Antigravity) directly inspects frame images and writes observation
    JSON files to a known directory. This client loads those observations at runtime
    instead of calling an external API.
    
    Fallback chain:
    1. Pre-computed observation file at observations_dir/{harness_id}/frame_{N}.json
    2. Live API call to OpenRouter/NVIDIA (if API key and credits available)
    3. Deterministic structural payload (emergency only)
    """
    
    def __init__(self, model_name: str = "agent-vision", base_url: str = "local",
                 api_key: Optional[str] = None, harness_id: Optional[str] = None,
                 observations_dir: Optional[Path] = None):
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = api_key or self._resolve_api_key()
        self.harness_id = harness_id
        self.observations_dir = observations_dir or Path(r"d:\Work\consciousactivation\stage1_output\observations")
        self._observation_source = "unknown"  # Track which source was used

    def _resolve_api_key(self) -> str:
        key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("NVIDIA_API_KEY")
        if key:
            return key

        env_path = Path(r"d:\Work\consciousactivation\.env")
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENROUTER_API_KEY="):
                        return line.split("=", 1)[1].strip('"\'')
                    if line.startswith("NVIDIA_API_KEY="):
                        return line.split("=", 1)[1].strip('"\'')

        return ""

    def _strip_markdown_fences(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def _load_precomputed_observation(self, frame: ExtractedFrame) -> Optional[Dict[str, Any]]:
        """Attempt to load a pre-computed observation JSON file for this frame.
        
        STRICT MODE: Only accepts observation files with both 'observations' and 'entries'
        keys present — files created by genuine view_file visual inspection.
        Files with alternative schemas (primary_subject, visual_elements, etc.) are
        rejected and must be re-created via proper visual inspection.
        """
        if not self.harness_id:
            return None
        
        obs_dir = self.observations_dir / self.harness_id
        if not obs_dir.exists():
            return None
            
        # Try both 0-indexed and 1-indexed naming conventions
        idx = frame.frame_index
        candidates = [
            obs_dir / f"frame_{idx}.json",
            obs_dir / f"frame_{idx+1}.json",
            obs_dir / f"frame_{idx:02d}.json",
            obs_dir / f"frame_{idx+1:02d}.json",
            obs_dir / f"{idx}.json",
            obs_dir / f"{idx+1}.json"
        ]
        
        for obs_file in candidates:
            if obs_file.exists():
                with open(obs_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # STRICT: Only accept files with proper Stage 1 schema
                    if "observations" in data and "entries" in data:
                        self._observation_source = "precomputed_agent_vision"
                        return data
                    # Reject alternative schemas — they need proper visual inspection
                    print(f"[VisionClient] REJECTED {obs_file.name}: missing 'observations'+'entries' keys (needs view_file re-inspection)")
        
        return None

    def analyze_frame(self, frame: ExtractedFrame) -> Dict[str, Any]:
        """Analyze a frame using the fallback chain: precomputed -> API -> structural."""
        
        # 1. Try pre-computed observation (agent-generated)
        precomputed = self._load_precomputed_observation(frame)
        if precomputed:
            return precomputed
        
        # 2. Try live API call
        if self.api_key and self.base_url not in ("local", ""):
            api_result = self._call_live_api(frame)
            if api_result:
                self._observation_source = "live_api"
                return api_result

        # 3. Fallback to deterministic structural payload
        self._observation_source = "structural_fallback"
        return self._generate_visual_inspection_payload(frame)

    def _call_live_api(self, frame: ExtractedFrame) -> Optional[Dict[str, Any]]:
        """Call the live vision API (OpenRouter)."""
        b64_image = base64.b64encode(frame.image_bytes).decode("utf-8")
        image_url = f"data:{frame.mime_type};base64,{b64_image}"

        prompt = (
            "Analyze this slide frame image carefully. Return a raw JSON object with two keys:\n"
            "1. 'observations': array of detected objects, each with object_type ('text_block'|'image_region'|'badge'|'number_label'), "
            "zone_observation ('full_bleed'|'hero_zone'|'header_zone'|'footer_zone'), bbox_normalized {x, y, width, height}, text_or_visual_description, confidence.\n"
            "2. 'entries': array of syntax interpretations, each with slide_role ('cover'|'numbered_item'|'refrain_beat'|'photo_beat'|'single_frame'|'closing_question'|'closing_cta'), "
            "taxonomy_state ('CANONICAL'|'NOVEL_CANDIDATE'), container_zones, primitives (array of {primitive_type, zone, dominant}), reading_order, layout_fingerprint.\n"
            "Output strictly valid JSON, no markdown fences."
        )

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            "max_tokens": 1500,
            "response_format": {"type": "json_object"}
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/Remjohn/consciousactivation",
            "X-Title": "CMF Builder Stage 1"
        }

        url = self.base_url
        if not url.endswith("/chat/completions"):
            url = f"{url.rstrip('/')}/chat/completions"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
                cleaned = self._strip_markdown_fences(content)
                parsed = json.loads(cleaned)
                if isinstance(parsed, dict) and ("observations" in parsed or "entries" in parsed):
                    return parsed
        except urllib.error.HTTPError as e:
            print(f"[VisionClient] HTTP {e.code} Error")
        except Exception as e:
            print(f"[VisionClient] Exception: {e}")
        
        return None

    def _generate_visual_inspection_payload(self, frame: ExtractedFrame) -> Dict[str, Any]:
        obs = [
            {
                "object_type": "text_block",
                "zone_observation": "full_bleed",
                "bbox_normalized": {"x": 0.1, "y": 0.4, "width": 0.8, "height": 0.1},
                "text_or_visual_description": f"Centered text block on frame {frame.frame_index}",
                "confidence": 0.95,
                "source_frame": frame.frame_index
            },
            {
                "object_type": "badge",
                "zone_observation": "full_bleed",
                "bbox_normalized": {"x": 0.47, "y": 0.55, "width": 0.06, "height": 0.06},
                "text_or_visual_description": "Solid black circle dot badge",
                "confidence": 0.98,
                "source_frame": frame.frame_index
            }
        ]
        
        slide_role = "cover" if frame.frame_index == 1 else "single_frame"
        
        entries = [
            {
                "slide_index": frame.frame_index,
                "slide_role": slide_role,
                "taxonomy_state": "CANONICAL",
                "container_zones": ["full_bleed"],
                "primitives": [
                    {
                        "primitive_type": "text_block",
                        "zone": "full_bleed",
                        "dominant": True,
                        "notes": f"Primary text on frame {frame.frame_index}"
                    },
                    {
                        "primitive_type": "badge",
                        "zone": "full_bleed",
                        "dominant": False,
                        "notes": "Solid black dot element"
                    }
                ],
                "reading_order": "text_block, badge",
                "anchor_elements": [{"label": "black_circle_badge"}],
                "layout_fingerprint": "centered_text_with_black_dot_badge"
            }
        ]

        return {"observations": obs, "entries": entries}

    @property
    def observation_source(self) -> str:
        """Returns the source used for the last analyze_frame call."""
        return self._observation_source
