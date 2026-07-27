from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "ux" / "mockups" / "reaction-templates"
SOURCE_JSON = OUT_DIR / "_approval-preview-compositions.draft.json"
CONTACT_SHEET = OUT_DIR / "_reaction-template-contact-sheet.png"

W, H = 1080, 1920

BLACK = "#000000"
INK = "#0B0B0B"
CHARCOAL = "#161616"
PANEL = "#202020"
WHITE = "#FFFFFF"
MUTED = "#8E8E93"
SOFT = "#F5F5F2"
GOLD = "#FFC21A"
RED = "#FF3B3B"
BLUE = "#2DA7FF"
GREEN = "#34C759"
PURPLE = "#7C5CFF"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONTS = {
    "xs": font(24),
    "sm": font(30),
    "body": font(38),
    "body_b": font(38, True),
    "h3": font(48, True),
    "h2": font(62, True),
    "h1": font(82, True),
    "mega": font(122, True),
}


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int, bold: bool = True) -> ImageFont.ImageFont:
    for size in range(start_size, 17, -2):
        fnt = font(size, bold)
        if text_size(draw, text, fnt)[0] <= max_width:
            return fnt
    return font(18, bold)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for raw_line in text.split("\n"):
        words = raw_line.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if text_size(draw, candidate, fnt)[0] <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.ImageFont,
    fill: str,
    max_width: int,
    line_gap: int = 12,
    align: str = "left",
) -> int:
    x, y = xy
    lines = wrap_text(draw, text, fnt, max_width)
    line_h = text_size(draw, "Ag", fnt)[1] + line_gap
    for line in lines:
        tw, _ = text_size(draw, line, fnt)
        tx = x if align == "left" else x + (max_width - tw) // 2
        draw.text((tx, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def center_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fnt: ImageFont.ImageFont, fill: str) -> None:
    x1, y1, x2, y2 = box
    tw, th = text_size(draw, text, fnt)
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2), text, font=fnt, fill=fill)


def chip(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str, fg: str = BLACK) -> tuple[int, int, int, int]:
    x, y = xy
    fnt = FONTS["xs"]
    tw, th = text_size(draw, text, fnt)
    box = (x, y, x + tw + 34, y + th + 22)
    draw.rounded_rectangle(box, radius=18, fill=fill)
    draw.text((x + 17, y + 10), text, font=fnt, fill=fg)
    return box


def ce_mark(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int = 39, accent: str = GOLD) -> None:
    cx, cy = center
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill="#150B0B", outline="#2A1515", width=4)
    draw.arc((cx - radius + 11, cy - radius + 11, cx + radius - 11, cy + radius - 11), 35, 325, fill=accent, width=12)
    draw.polygon([(cx + 7, cy - 14), (cx + 29, cy), (cx + 7, cy + 14)], fill=accent)


def header(draw: ImageDraw.ImageDraw, spec: dict[str, Any], dark: bool = True) -> None:
    fg = WHITE if dark else BLACK
    sub = MUTED if dark else "#595959"
    accent = spec["accent"]
    ce_mark(draw, (82, 82), 39, accent=accent)
    draw.text((140, 44), "CONSCIOUS ELITE", font=FONTS["h3"], fill=fg)
    draw.text((143, 101), "CMF Studio operator preview", font=FONTS["sm"], fill=sub)
    chip(draw, (760, 50), spec["template_code"], accent)
    draw_wrapped(draw, (760, 105), spec["format"], FONTS["xs"], sub, 245, line_gap=4)


def footer(draw: ImageDraw.ImageDraw, spec: dict[str, Any], dark: bool = True) -> None:
    fg = WHITE if dark else BLACK
    sub = MUTED if dark else "#595959"
    y = H - 170
    draw.line((70, y, W - 70, y), fill="#303030" if dark else "#D0D0D0", width=2)
    draw.text((70, y + 30), "Operator checkpoints", font=FONTS["sm"], fill=sub)
    x = 70
    for checkpoint in spec["eval_checkpoints"]:
        box = chip(draw, (x, y + 78), checkpoint, "#2B2B2B" if dark else "#E8E8E8", fg)
        x = box[2] + 14
    draw.text((70, H - 54), "Draft preview only. Final composition JSON is created after approval.", font=FONTS["xs"], fill=sub)


def placeholder(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    label: str,
    fill: str,
    outline: str = WHITE,
    dark_text: bool = False,
) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=6, fill=fill, outline=outline, width=5)
    for offset in range(0, x2 - x1, 42):
        draw.line((x1 + offset, y1, x1, y1 + offset), fill="#FFFFFF22", width=2)
    fnt = fit_text(draw, label, x2 - x1 - 70, 38, True)
    center_text(draw, box, label, fnt, BLACK if dark_text else WHITE)


def operator_rail(draw: ImageDraw.ImageDraw, spec: dict[str, Any]) -> None:
    x1, y1, x2, y2 = 700, 1260, 1010, 1710
    draw.rounded_rectangle((x1, y1, x2, y2), radius=8, fill="#101010", outline="#343434", width=2)
    draw.text((x1 + 25, y1 + 25), "Operator Queue", font=FONTS["sm"], fill=GOLD)
    y = y1 + 82
    for label, value in spec["operator_fields"]:
        draw.text((x1 + 25, y), label, font=FONTS["xs"], fill=MUTED)
        y += 31
        y = draw_wrapped(draw, (x1 + 25, y), value, FONTS["xs"], WHITE, x2 - x1 - 50, line_gap=5)
        y += 18


def render_vrs(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    x = 70
    y = 205
    for text, fill in [("WOULD", WHITE), ("YOU", RED), ("RATHER", WHITE)]:
        d.text((x, y), text, font=FONTS["h1"], fill=fill)
        x += text_size(d, text, FONTS["h1"])[0] + 22
    d.text((70, 315), "Live reaction split-screen template", font=FONTS["body"], fill=MUTED)
    placeholder(d, (70, 430, 505, 1060), "OPTION A\nprovocation visual", "#18242B", BLUE)
    placeholder(d, (575, 430, 1010, 1060), "OPTION B\ncontrast visual", "#2B1818", RED)
    center_text(d, (70, 1095, 505, 1210), "Preserve freedom\nand lose status?", FONTS["body_b"], WHITE)
    center_text(d, (575, 1095, 1010, 1210), "Gain authority\nand lose truth?", FONTS["body_b"], WHITE)
    center_text(d, (496, 1010, 584, 1110), "OR", FONTS["h3"], GOLD)
    operator_rail(d, spec)
    draw_wrapped(d, (70, 1290), "Routing rule: use when the interview answer creates a clean binary tension or moral fork.", FONTS["body"], WHITE, 590, 13)
    footer(d, spec)
    return img


def render_tier(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    d.text((70, 205), "GUEST RANKS THE TRUTH", font=FONTS["h2"], fill=WHITE)
    d.text((70, 285), "Tier-list editing template", font=FONTS["body"], fill=MUTED)
    labels = [("S", GOLD), ("A", GREEN), ("B", BLUE), ("C", PURPLE), ("D", RED)]
    y = 405
    for label, color in labels:
        d.rounded_rectangle((70, y, 210, y + 145), radius=6, fill=color)
        center_text(d, (70, y, 210, y + 145), label, FONTS["mega"], BLACK)
        d.rounded_rectangle((230, y, 1010, y + 145), radius=6, fill="#111111", outline="#343434", width=2)
        for i in range(4):
            x = 260 + i * 180
            d.rounded_rectangle((x, y + 28, x + 132, y + 117), radius=8, fill="#252525", outline="#555555", width=2)
            center_text(d, (x, y + 28, x + 132, y + 117), f"CLIP {i+1}", FONTS["xs"], WHITE)
        y += 166
    draw_wrapped(d, (70, 1290), "Routing rule: use when the guest gives comparative judgment, hierarchy, preference, maturity scale, or authority ranking.", FONTS["body"], WHITE, 590, 13)
    operator_rail(d, spec)
    footer(d, spec)
    return img


def render_blind(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    d.text((70, 205), "BLIND RANK", font=FONTS["mega"], fill=WHITE)
    d.text((70, 335), "The guest decides before seeing the next signal", font=FONTS["body"], fill=MUTED)
    for i, y in enumerate([470, 620, 770, 920, 1070], start=1):
        d.rounded_rectangle((70, y, 1010, y + 115), radius=10, fill="#101010", outline="#333333", width=2)
        d.text((95, y + 21), f"#{i}", font=FONTS["h2"], fill=GOLD if i == 3 else WHITE)
        d.text((190, y + 35), "LOCKED SLOT" if i != 3 else "CURRENT REACTION", font=FONTS["body_b"], fill=WHITE)
        d.rounded_rectangle((770, y + 27, 965, y + 88), radius=30, fill=GOLD if i == 3 else "#2B2B2B")
        center_text(d, (770, y + 27, 965, y + 88), "PLACE HERE" if i == 3 else "WAITING", FONTS["xs"], BLACK if i == 3 else MUTED)
    draw_wrapped(d, (70, 1290), "Routing rule: use when suspense, prediction, or forced prioritization makes the reaction more engaging than the statement alone.", FONTS["body"], WHITE, 590, 13)
    operator_rail(d, spec)
    footer(d, spec)
    return img


def render_proposal(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), SOFT)
    d = ImageDraw.Draw(img)
    header(d, spec, dark=False)
    d.text((70, 205), "RANK THESE PROPOSALS", font=FONTS["h2"], fill=BLACK)
    d.text((70, 285), "Audience-facing choice sequence", font=FONTS["body"], fill="#606060")
    cards = [
        ("1", "The safe path", "Status is protected, signal is diluted."),
        ("2", "The honest path", "Risk is visible, authority compounds."),
        ("3", "The viral path", "Reaction spikes, trust may decay."),
    ]
    y = 420
    for number, title, body in cards:
        d.rounded_rectangle((70, y, 1010, y + 230), radius=8, fill=WHITE, outline="#DADADA", width=3)
        d.ellipse((105, y + 45, 205, y + 145), fill=GOLD)
        center_text(d, (105, y + 45, 205, y + 145), number, FONTS["h2"], BLACK)
        d.text((240, y + 48), title, font=FONTS["h3"], fill=BLACK)
        draw_wrapped(d, (240, y + 110), body, FONTS["body"], "#444444", 700, 10)
        y += 265
    d.rounded_rectangle((70, 1260, 650, 1645), radius=8, fill=BLACK)
    draw_wrapped(d, (105, 1305), "Routing rule: use when the interview produces strategic alternatives the audience can judge or reorder.", FONTS["body"], WHITE, 500, 13)
    operator_rail(d, spec)
    footer(d, spec, dark=False)
    return img


def render_bracket(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    d.text((70, 205), "ELIMINATION BRACKET", font=FONTS["h2"], fill=WHITE)
    d.text((70, 285), "This vs that until one belief survives", font=FONTS["body"], fill=MUTED)
    items = [
        ((70, 430, 410, 545), "Comfort"),
        ((70, 620, 410, 735), "Conviction"),
        ((70, 810, 410, 925), "Attention"),
        ((70, 1000, 410, 1115), "Legacy"),
        ((670, 525, 1010, 640), "Winner A"),
        ((670, 905, 1010, 1020), "Winner B"),
        ((670, 720, 1010, 840), "FINAL WINNER"),
    ]
    for box, label in items:
        fill = GOLD if "FINAL" in label else "#111111"
        outline = GOLD if "Winner" in label or "FINAL" in label else "#404040"
        d.rounded_rectangle(box, radius=8, fill=fill, outline=outline, width=4)
        center_text(d, box, label, FONTS["body_b"], BLACK if fill == GOLD else WHITE)
    for y in [487, 677, 867, 1057]:
        d.line((410, y, 530, y), fill=WHITE, width=4)
    d.line((530, 487, 530, 677), fill=WHITE, width=4)
    d.line((530, 867, 530, 1057), fill=WHITE, width=4)
    d.line((530, 582, 670, 582), fill=WHITE, width=4)
    d.line((530, 962, 670, 962), fill=WHITE, width=4)
    d.line((840, 640, 840, 720), fill=WHITE, width=4)
    d.line((840, 905, 840, 840), fill=WHITE, width=4)
    draw_wrapped(d, (70, 1290), "Routing rule: use when repeated contrastive decisions expose the guest's hierarchy of values.", FONTS["body"], WHITE, 590, 13)
    operator_rail(d, spec)
    footer(d, spec)
    return img


def render_mirror(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    d.text((70, 205), "WHICH VERSION ARE YOU?", font=FONTS["h2"], fill=WHITE)
    d.text((70, 285), "Mirror quiz from guest insight", font=FONTS["body"], fill=MUTED)
    placeholder(d, (70, 420, 505, 900), "TYPE A\nperformer self", "#24170C", GOLD)
    placeholder(d, (575, 420, 1010, 900), "TYPE B\nconscious self", "#102118", GREEN)
    center_text(d, (482, 590, 598, 720), "VS", FONTS["h1"], WHITE)
    traits = [
        ("Needs applause", "Needs alignment"),
        ("Optimizes image", "Optimizes signal"),
        ("Repeats scripts", "Finds truth"),
        ("Avoids tension", "Uses tension"),
    ]
    y = 990
    for left, right in traits:
        d.text((110, y), left, font=FONTS["body_b"], fill=GOLD)
        d.text((610, y), right, font=FONTS["body_b"], fill=WHITE)
        y += 90
    draw_wrapped(d, (70, 1370), "Routing rule: use when a guest insight becomes audience self-diagnosis, identity sorting, or reflective contrast.", FONTS["body"], WHITE, 590, 13)
    operator_rail(d, spec)
    footer(d, spec)
    return img


def render_authority(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), SOFT)
    d = ImageDraw.Draw(img)
    header(d, spec, dark=False)
    d.text((70, 205), "AUTHORITY LADDER", font=FONTS["h2"], fill=BLACK)
    d.text((70, 285), "From raw reaction to teachable authority", font=FONTS["body"], fill="#606060")
    ladder = [
        ("1", "Opinion", "A claim without earned context."),
        ("2", "Experience", "A lived pattern with stakes."),
        ("3", "Principle", "A compressed rule that transfers."),
        ("4", "Authority", "A repeatable frame others can use."),
    ]
    y = 410
    for number, title, body in ladder:
        d.rounded_rectangle((130, y, 930, y + 160), radius=8, fill=WHITE, outline="#D3D3D3", width=3)
        d.rectangle((130, y, 250, y + 160), fill=GOLD if number == "4" else BLACK)
        center_text(d, (130, y, 250, y + 160), number, FONTS["h1"], BLACK if number == "4" else WHITE)
        d.text((285, y + 34), title, font=FONTS["h3"], fill=BLACK)
        draw_wrapped(d, (285, y + 94), body, FONTS["body"], "#444444", 590, 8)
        if number != "4":
            d.line((530, y + 160, 530, y + 195), fill=BLACK, width=5)
        y += 195
    d.rounded_rectangle((70, 1370, 650, 1710), radius=8, fill=BLACK)
    draw_wrapped(d, (105, 1410), "Routing rule: use when the system can distill a guest answer into authority progression or teaching sequence.", FONTS["body"], WHITE, 500, 13)
    operator_rail(d, spec)
    footer(d, spec, dark=False)
    return img


COMPOSITIONS: list[dict[str, Any]] = [
    {
        "template_code": "VRS-SPLIT",
        "format": "short video / visual poll / carousel cover",
        "title": "Versus Split Screen",
        "accent": BLUE,
        "renderer": "render_vrs",
        "file": "vrs-split-versus.png",
        "source_app": "apps/react-debate",
        "operator_fields": [
            ("Guest workspace", "Brand-safe clips and claims only"),
            ("Input primitive", "Provocation + contrast pair"),
            ("Approval gate", "Binary tension is real"),
        ],
        "eval_checkpoints": ["contrast", "guest-fit", "safe-area"],
    },
    {
        "template_code": "TRK-TIER",
        "format": "ranking short / carousel sequence",
        "title": "Tier List Ranking",
        "accent": GOLD,
        "renderer": "render_tier",
        "file": "trk-tier-list.png",
        "source_app": "apps/react-tierlist",
        "operator_fields": [
            ("Guest workspace", "Use guest-specific clips"),
            ("Input primitive", "Hierarchy or comparison"),
            ("Approval gate", "Ranking logic is defensible"),
        ],
        "eval_checkpoints": ["ranking-logic", "clip-fit", "reuse"],
    },
    {
        "template_code": "RNK-BLIND",
        "format": "blind ranking short video",
        "title": "Blind Ranking",
        "accent": GOLD,
        "renderer": "render_blind",
        "file": "rnk-blind-ranking.png",
        "source_app": "apps/react-blind-rank",
        "operator_fields": [
            ("Guest workspace", "No cross-guest leakage"),
            ("Input primitive", "Suspense ordering"),
            ("Approval gate", "Reveal sequence is coherent"),
        ],
        "eval_checkpoints": ["suspense", "order", "retention"],
    },
    {
        "template_code": "RNK-PROPOSAL",
        "format": "proposal ranking quiz",
        "title": "Proposal Ranking",
        "accent": BLACK,
        "renderer": "render_proposal",
        "file": "rnk-proposal-ranking.png",
        "source_app": "apps/react-ranking-quiz",
        "operator_fields": [
            ("Guest workspace", "Audience context attached"),
            ("Input primitive", "Strategic alternatives"),
            ("Approval gate", "Each option is distinct"),
        ],
        "eval_checkpoints": ["choice-quality", "clarity", "audience"],
    },
    {
        "template_code": "ELM-BRACKET",
        "format": "elimination bracket video",
        "title": "Elimination Bracket",
        "accent": RED,
        "renderer": "render_bracket",
        "file": "elm-bracket-choice.png",
        "source_app": "apps/react-elimination",
        "operator_fields": [
            ("Guest workspace", "Value conflicts only"),
            ("Input primitive", "Repeated choices"),
            ("Approval gate", "Final winner has meaning"),
        ],
        "eval_checkpoints": ["stakes", "values", "payoff"],
    },
    {
        "template_code": "MIR-QUIZ",
        "format": "mirror quiz / identity diagnostic",
        "title": "Mirror Quiz",
        "accent": GREEN,
        "renderer": "render_mirror",
        "file": "mir-quiz-mirror.png",
        "source_app": "apps/react-mirror-quiz",
        "operator_fields": [
            ("Guest workspace", "Voice DNA constrained"),
            ("Input primitive", "Identity contrast"),
            ("Approval gate", "Does not flatten the guest"),
        ],
        "eval_checkpoints": ["identity", "ethics", "shareability"],
    },
    {
        "template_code": "AUTH-LADDER",
        "format": "authority quiz / teaching sequence",
        "title": "Authority Ladder Quiz",
        "accent": GOLD,
        "renderer": "render_authority",
        "file": "auth-ladder-quiz.png",
        "source_app": "apps/react-authority-quiz",
        "operator_fields": [
            ("Guest workspace", "Doctrine and primitives linked"),
            ("Input primitive", "Authority progression"),
            ("Approval gate", "Distillation earns the claim"),
        ],
        "eval_checkpoints": ["doctrine", "authority", "teaching"],
    },
]


RENDERERS = {
    "render_vrs": render_vrs,
    "render_tier": render_tier,
    "render_blind": render_blind,
    "render_proposal": render_proposal,
    "render_bracket": render_bracket,
    "render_mirror": render_mirror,
    "render_authority": render_authority,
}


def write_source_json() -> None:
    draft = {
        "schema": "cmf.composition.approval_preview.v0",
        "status": "draft_for_visual_approval_not_production_template",
        "canvas": {"width": W, "height": H, "unit": "px"},
        "brand": {
            "name": "Conscious Elite",
            "colors": {
                "black": BLACK,
                "white": WHITE,
                "gold": GOLD,
                "red": RED,
                "blue": BLUE,
                "green": GREEN,
            },
        },
        "compositions": COMPOSITIONS,
    }
    SOURCE_JSON.write_text(json.dumps(draft, indent=2), encoding="utf-8")


def make_contact_sheet(paths: list[Path]) -> None:
    thumb_w, thumb_h = 270, 480
    pad = 32
    label_h = 58
    cols = 4
    rows = 2
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * pad, rows * (thumb_h + label_h) + (rows + 1) * pad), "#101010")
    d = ImageDraw.Draw(sheet)
    for i, path in enumerate(paths):
        source = Image.open(path).convert("RGB")
        source.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = pad + (i % cols) * (thumb_w + pad)
        y = pad + (i // cols) * (thumb_h + label_h + pad)
        sheet.paste(source, (x + (thumb_w - source.width) // 2, y))
        label = path.stem.upper()
        label_font = fit_text(d, label, thumb_w, 24, True)
        center_text(d, (x, y + thumb_h + 10, x + thumb_w, y + thumb_h + label_h), label, label_font, WHITE)
    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_source_json()
    paths: list[Path] = []
    for spec in COMPOSITIONS:
        image = RENDERERS[spec["renderer"]](spec)
        out_path = OUT_DIR / spec["file"]
        image.save(out_path)
        paths.append(out_path)
    make_contact_sheet(paths)
    print(f"Wrote {len(paths)} template previews to {OUT_DIR}")
    print(f"Wrote draft JSON source to {SOURCE_JSON}")
    print(f"Wrote contact sheet to {CONTACT_SHEET}")


if __name__ == "__main__":
    main()
