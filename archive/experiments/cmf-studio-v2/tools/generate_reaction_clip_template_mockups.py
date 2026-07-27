from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "ux" / "mockups" / "reaction-clip-templates"
SOURCE_JSON = OUT_DIR / "_reaction-clip-compositions.draft.json"
CONTACT_SHEET = OUT_DIR / "_reaction-clip-contact-sheet.png"

W, H = 1080, 1920
TOP_H = 1000
SCENE_Y = TOP_H

BLACK = "#000000"
CHARCOAL = "#151515"
PANEL = "#202020"
WHITE = "#FFFFFF"
MUTED = "#8E8E93"
GOLD = "#FFC21A"
RED = "#FF3B3B"
BLUE = "#2DA7FF"
GREEN = "#34C759"
PURPLE = "#7C5CFF"
SOFT = "#F7F5EF"


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


F = {
    "xs": font(24),
    "sm": font(30),
    "body": font(38),
    "body_b": font(38, True),
    "h3": font(48, True),
    "h2": font(62, True),
    "h1": font(82, True),
    "mega": font(116, True),
}


def size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_w: int) -> list[str]:
    lines: list[str] = []
    for raw in text.split("\n"):
        words = raw.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if size(draw, candidate, fnt)[0] <= max_w:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_wrap(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.ImageFont,
    fill: str,
    max_w: int,
    gap: int = 10,
    align: str = "left",
) -> int:
    x, y = xy
    line_h = size(draw, "Ag", fnt)[1] + gap
    for line in wrap(draw, text, fnt, max_w):
        tw, _ = size(draw, line, fnt)
        tx = x if align == "left" else x + (max_w - tw) // 2
        draw.text((tx, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def center(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fnt: ImageFont.ImageFont, fill: str) -> None:
    x1, y1, x2, y2 = box
    tw, th = size(draw, text, fnt)
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2), text, font=fnt, fill=fill)


def fit(draw: ImageDraw.ImageDraw, text: str, max_w: int, start: int, bold: bool = True) -> ImageFont.ImageFont:
    for s in range(start, 17, -2):
        candidate = font(s, bold)
        if size(draw, text, candidate)[0] <= max_w:
            return candidate
    return font(18, bold)


def chip(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str, fg: str = BLACK) -> tuple[int, int, int, int]:
    x, y = xy
    tw, th = size(draw, text, F["xs"])
    box = (x, y, x + tw + 34, y + th + 22)
    draw.rounded_rectangle(box, radius=18, fill=fill)
    draw.text((x + 17, y + 10), text, font=F["xs"], fill=fg)
    return box


def ce_mark(draw: ImageDraw.ImageDraw, center_xy: tuple[int, int], accent: str) -> None:
    cx, cy = center_xy
    r = 38
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill="#160B0B", outline="#2D1717", width=4)
    draw.arc((cx - 26, cy - 26, cx + 26, cy + 26), 35, 325, fill=accent, width=12)
    draw.polygon([(cx + 8, cy - 14), (cx + 31, cy), (cx + 8, cy + 14)], fill=accent)


def header(draw: ImageDraw.ImageDraw, spec: dict[str, Any], dark: bool = True) -> None:
    fg = WHITE if dark else BLACK
    sub = MUTED if dark else "#666666"
    ce_mark(draw, (78, 74), spec["accent"])
    draw.text((132, 42), "CONSCIOUS ELITE", font=F["h3"], fill=fg)
    draw.text((134, 99), "reaction clip composition", font=F["sm"], fill=sub)
    chip(draw, (770, 48), spec["template_code"], spec["accent"])
    draw_wrap(draw, (770, 104), spec["format"], F["xs"], sub, 240, gap=4)


def title(draw: ImageDraw.ImageDraw, main: str, subtitle: str, dark: bool = True) -> None:
    fg = WHITE if dark else BLACK
    sub = MUTED if dark else "#666666"
    draw.text((70, 175), main, font=fit(draw, main, 940, 80, True), fill=fg)
    draw.text((72, 260), subtitle, font=F["body"], fill=sub)


def placeholder(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, fill: str, outline: str) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=8, fill=fill, outline=outline, width=5)
    for x in range(x1 + 28, x2 - 20, 48):
        draw.line((x, y1 + 18, x, y2 - 18), fill="#FFFFFF22", width=2)
    draw_wrap(draw, (x1 + 28, y1 + (y2 - y1) // 2 - 36), label, F["body_b"], WHITE, x2 - x1 - 56, gap=8, align="center")


def scene_background(draw: ImageDraw.ImageDraw, accent: str) -> None:
    for y in range(SCENE_Y, H):
        ratio = (y - SCENE_Y) / (H - SCENE_Y)
        level = int(8 + ratio * 26)
        draw.line((0, y, W, y), fill=(level, level, level))
    draw.rectangle((0, SCENE_Y, W, SCENE_Y + 7), fill=accent)
    draw.ellipse((-260, SCENE_Y + 310, 420, SCENE_Y + 990), fill="#101010", outline="#252525", width=3)
    draw.ellipse((680, SCENE_Y + 240, 1360, SCENE_Y + 920), fill="#101010", outline="#252525", width=3)
    draw.line((90, H - 205, W - 90, H - 205), fill="#333333", width=3)
    draw.text((70, H - 95), "upper-body interaction scene | background removed | synced to question and guest reaction", font=F["xs"], fill=MUTED)


def speech(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, accent: str, align: str = "left") -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=18, fill="#F6F3EA", outline=accent, width=4)
    draw_wrap(draw, (x1 + 24, y1 + 20), text, F["sm"], BLACK, x2 - x1 - 48, gap=7, align=align)


def person(draw: ImageDraw.ImageDraw, cx: int, y: int, label: str, accent: str, skin: str, suit: str, facing: str) -> None:
    head = (cx - 58, y, cx + 58, y + 116)
    draw.ellipse((head[0] - 8, head[1] - 8, head[2] + 8, head[3] + 8), fill="#FFFFFF22")
    draw.ellipse(head, fill=skin, outline="#F4E2CB", width=3)
    eye_y = y + 50
    draw.ellipse((cx - 24, eye_y, cx - 13, eye_y + 8), fill=BLACK)
    draw.ellipse((cx + 13, eye_y, cx + 24, eye_y + 8), fill=BLACK)
    if facing == "left":
        draw.arc((cx - 24, y + 64, cx + 18, y + 96), 10, 150, fill=BLACK, width=3)
    else:
        draw.arc((cx - 18, y + 64, cx + 24, y + 96), 30, 170, fill=BLACK, width=3)
    draw.rectangle((cx - 24, y + 112, cx + 24, y + 158), fill=skin)
    torso = [(cx - 185, y + 420), (cx - 140, y + 178), (cx - 52, y + 142), (cx + 52, y + 142), (cx + 140, y + 178), (cx + 185, y + 420)]
    draw.polygon(torso, fill=suit)
    draw.line((cx, y + 158, cx, y + 410), fill=accent, width=5)
    draw.arc((cx - 185, y + 250, cx - 65, y + 455), 235, 350, fill="#EAD3BC", width=24)
    draw.arc((cx + 65, y + 250, cx + 185, y + 455), 190, 305, fill="#EAD3BC", width=24)
    draw.rounded_rectangle((cx - 180, y + 430, cx + 180, y + 488), radius=28, fill=BLACK, outline=accent, width=3)
    center(draw, (cx - 180, y + 430, cx + 180, y + 488), label, F["sm"], WHITE)


def human_scene(draw: ImageDraw.ImageDraw, spec: dict[str, Any], mode: str = "duo") -> None:
    scene_background(draw, spec["accent"])
    if mode == "guest_only":
        speech(draw, (255, SCENE_Y + 92, 825, SCENE_Y + 205), "Guest reaction beat drives the visual reveal.", spec["accent"], "center")
        person(draw, 540, SCENE_Y + 250, "GUEST", spec["accent"], "#B98763", "#111111", "left")
        return
    speech(draw, (70, SCENE_Y + 78, 495, SCENE_Y + 195), "Interviewer question frames the tension.", spec["accent"])
    speech(draw, (585, SCENE_Y + 78, 1010, SCENE_Y + 195), "Guest answer triggers the mechanic.", spec["accent"])
    person(draw, 305, SCENE_Y + 255, "INTERVIEWER", spec["accent"], "#9B674C", "#101010", "right")
    person(draw, 770, SCENE_Y + 255, "GUEST", spec["accent"], "#C78E69", "#141414", "left")


def divider(draw: ImageDraw.ImageDraw, accent: str) -> None:
    draw.rectangle((0, TOP_H - 8, W, TOP_H + 8), fill=accent)


def render_vrs(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    x = 70
    for text, fill in [("WOULD", WHITE), ("YOU", RED), ("RATHER", WHITE)]:
        d.text((x, 180), text, font=F["h1"], fill=fill)
        x += size(d, text, F["h1"])[0] + 20
    draw_wrap(d, (72, 272), "Interviewer asks. Guest chooses. Template reacts.", F["body"], MUTED, 940)
    placeholder(d, (70, 355, 505, 805), "OPTION A\nprovocation visual", "#17252D", BLUE)
    placeholder(d, (575, 355, 1010, 805), "OPTION B\ncontrast visual", "#2A1717", RED)
    center(d, (495, 790, 585, 875), "OR", F["h3"], GOLD)
    center(d, (80, 835, 495, 930), "Preserve freedom\nand lose status?", F["body_b"], WHITE)
    center(d, (585, 835, 1000, 930), "Gain authority\nand lose truth?", F["body_b"], WHITE)
    divider(d, spec["accent"])
    human_scene(d, spec)
    return img


def render_tier(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    title(d, "GUEST RANKS THE TRUTH", "Ranking UI occupies the upper half.")
    y = 335
    for label, color in [("S", GOLD), ("A", GREEN), ("B", BLUE), ("C", PURPLE), ("D", RED)]:
        d.rounded_rectangle((70, y, 185, y + 95), radius=6, fill=color)
        center(d, (70, y, 185, y + 95), label, F["h2"], BLACK)
        d.rounded_rectangle((205, y, 1010, y + 95), radius=6, fill="#111111", outline="#343434", width=2)
        for i in range(4):
            x = 230 + i * 185
            d.rounded_rectangle((x, y + 20, x + 138, y + 75), radius=8, fill=PANEL, outline="#515151", width=2)
            center(d, (x, y + 20, x + 138, y + 75), f"CLIP {i+1}", F["xs"], WHITE)
        y += 115
    draw_wrap(d, (70, 925), "Beat sync: guest says rank, UI locks tier, scene below preserves the human reaction.", F["sm"], MUTED, 940)
    divider(d, spec["accent"])
    human_scene(d, spec)
    return img


def render_blind(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    title(d, "BLIND RANK", "The next reveal is unknown to the guest.")
    for i, y in enumerate([345, 465, 585, 705, 825], start=1):
        d.rounded_rectangle((90, y, 990, y + 88), radius=10, fill="#111111", outline="#383838", width=3)
        d.text((120, y + 14), f"#{i}", font=F["h3"], fill=GOLD if i == 3 else WHITE)
        d.text((215, y + 25), "CURRENT REACTION" if i == 3 else "LOCKED SLOT", font=F["body_b"], fill=WHITE)
        d.rounded_rectangle((790, y + 18, 955, y + 70), radius=26, fill=GOLD if i == 3 else "#2B2B2B")
        center(d, (790, y + 18, 955, y + 70), "PLACE" if i == 3 else "WAIT", F["xs"], BLACK if i == 3 else MUTED)
    divider(d, spec["accent"])
    human_scene(d, spec)
    return img


def render_proposal(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), SOFT)
    d = ImageDraw.Draw(img)
    header(d, spec, dark=False)
    title(d, "RANK THESE PROPOSALS", "Question creates alternatives. Guest orders them.", dark=False)
    cards = [
        ("1", "The safe path", "Status protected, signal diluted."),
        ("2", "The honest path", "Risk visible, authority compounds."),
        ("3", "The viral path", "Reaction spikes, trust may decay."),
    ]
    y = 355
    for number, heading, body in cards:
        d.rounded_rectangle((90, y, 990, y + 145), radius=8, fill=WHITE, outline="#D6D2C9", width=3)
        d.ellipse((125, y + 32, 205, y + 112), fill=GOLD)
        center(d, (125, y + 32, 205, y + 112), number, F["h3"], BLACK)
        d.text((235, y + 30), heading, font=F["h3"], fill=BLACK)
        d.text((236, y + 88), body, font=F["sm"], fill="#444444")
        y += 165
    divider(d, spec["accent"])
    human_scene(d, spec)
    return img


def render_bracket(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    title(d, "CHOICE BRACKET", "Repeated decisions expose the guest's values.")
    boxes = [
        ((70, 355, 410, 440), "Comfort"),
        ((70, 500, 410, 585), "Conviction"),
        ((70, 645, 410, 730), "Attention"),
        ((70, 790, 410, 875), "Legacy"),
        ((665, 430, 1010, 520), "Winner A"),
        ((665, 720, 1010, 810), "Winner B"),
        ((665, 575, 1010, 675), "FINAL WINNER"),
    ]
    for box, label in boxes:
        fill = GOLD if "FINAL" in label else "#111111"
        d.rounded_rectangle(box, radius=8, fill=fill, outline=spec["accent"] if "Winner" in label or "FINAL" in label else "#444444", width=4)
        center(d, box, label, F["body_b"], BLACK if fill == GOLD else WHITE)
    for y in [397, 542, 687, 832]:
        d.line((410, y, 530, y), fill=WHITE, width=4)
    d.line((530, 397, 530, 542), fill=WHITE, width=4)
    d.line((530, 687, 530, 832), fill=WHITE, width=4)
    d.line((530, 470, 665, 470), fill=WHITE, width=4)
    d.line((530, 760, 665, 760), fill=WHITE, width=4)
    d.line((837, 520, 837, 575), fill=WHITE, width=4)
    d.line((837, 720, 837, 675), fill=WHITE, width=4)
    divider(d, spec["accent"])
    human_scene(d, spec)
    return img


def render_mirror(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    header(d, spec)
    title(d, "WHICH VERSION ARE YOU?", "Guest insight becomes audience self-diagnosis.")
    placeholder(d, (70, 355, 505, 725), "TYPE A\nperformer self", "#24170C", GOLD)
    placeholder(d, (575, 355, 1010, 725), "TYPE B\nconscious self", "#102118", GREEN)
    center(d, (490, 495, 590, 600), "VS", F["h2"], WHITE)
    traits = [("Needs applause", "Needs alignment"), ("Optimizes image", "Optimizes signal"), ("Avoids tension", "Uses tension")]
    y = 775
    for left, right in traits:
        d.text((110, y), left, font=F["body_b"], fill=GOLD)
        d.text((610, y), right, font=F["body_b"], fill=WHITE)
        y += 58
    divider(d, spec["accent"])
    human_scene(d, spec)
    return img


def render_authority(spec: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), SOFT)
    d = ImageDraw.Draw(img)
    header(d, spec, dark=False)
    title(d, "AUTHORITY LADDER", "Reaction is distilled into teachable authority.", dark=False)
    ladder = [("1", "Opinion"), ("2", "Experience"), ("3", "Principle"), ("4", "Authority")]
    y = 350
    for number, label in ladder:
        fill = GOLD if number == "4" else BLACK
        d.rounded_rectangle((150, y, 930, y + 110), radius=8, fill=WHITE, outline="#D5D0C8", width=3)
        d.rectangle((150, y, 250, y + 110), fill=fill)
        center(d, (150, y, 250, y + 110), number, F["h2"], BLACK if fill == GOLD else WHITE)
        d.text((285, y + 31), label, font=F["h3"], fill=BLACK)
        if number != "4":
            d.line((540, y + 110, 540, y + 145), fill=BLACK, width=5)
        y += 145
    divider(d, spec["accent"])
    human_scene(d, spec)
    return img


COMPOSITIONS: list[dict[str, Any]] = [
    {
        "template_code": "VRS-SPLIT",
        "title": "Versus Split Screen",
        "format": "short video / visual poll / carousel cover",
        "accent": BLUE,
        "renderer": "render_vrs",
        "file": "vrs-split-reaction-clip.png",
        "source_app": "apps/react-debate",
        "human_scene_mode": "duo",
    },
    {
        "template_code": "TRK-TIER",
        "title": "Tier List Ranking",
        "format": "ranking short / carousel sequence",
        "accent": GOLD,
        "renderer": "render_tier",
        "file": "trk-tier-reaction-clip.png",
        "source_app": "apps/react-tierlist",
        "human_scene_mode": "duo",
    },
    {
        "template_code": "RNK-BLIND",
        "title": "Blind Ranking",
        "format": "blind ranking short video",
        "accent": GOLD,
        "renderer": "render_blind",
        "file": "rnk-blind-reaction-clip.png",
        "source_app": "apps/react-blind-rank",
        "human_scene_mode": "duo",
    },
    {
        "template_code": "RNK-PROPOSAL",
        "title": "Proposal Ranking",
        "format": "proposal ranking quiz",
        "accent": GOLD,
        "renderer": "render_proposal",
        "file": "rnk-proposal-reaction-clip.png",
        "source_app": "apps/react-ranking-quiz",
        "human_scene_mode": "duo",
    },
    {
        "template_code": "ELM-BRACKET",
        "title": "Choice Bracket",
        "format": "elimination choice video",
        "accent": RED,
        "renderer": "render_bracket",
        "file": "elm-bracket-reaction-clip.png",
        "source_app": "apps/react-elimination",
        "human_scene_mode": "duo",
    },
    {
        "template_code": "MIR-QUIZ",
        "title": "Mirror Quiz",
        "format": "mirror quiz / identity diagnostic",
        "accent": GREEN,
        "renderer": "render_mirror",
        "file": "mir-quiz-reaction-clip.png",
        "source_app": "apps/react-mirror-quiz",
        "human_scene_mode": "duo",
    },
    {
        "template_code": "AUTH-LADDER",
        "title": "Authority Ladder Quiz",
        "format": "authority quiz / teaching sequence",
        "accent": GOLD,
        "renderer": "render_authority",
        "file": "auth-ladder-reaction-clip.png",
        "source_app": "apps/react-authority-quiz",
        "human_scene_mode": "duo",
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
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source = {
        "schema": "cmf.composition.reaction_clip_preview.v0",
        "status": "draft_for_visual_approval_not_final_template_json",
        "canonical_layout": {
            "canvas": {"width": W, "height": H, "unit": "px", "aspect_ratio": "9:16"},
            "zones": {
                "reaction_ui_zone": {
                    "position": "upper",
                    "height_px": TOP_H,
                    "role": "mechanic UI synchronized to interviewer question and guest reaction beat",
                },
                "human_scene_zone": {
                    "position": "lower",
                    "height_px": H - TOP_H,
                    "role": "upper-body interviewer and guest with removed backgrounds composited into scene",
                    "supported_modes": ["duo_interaction", "guest_only_reaction"],
                },
            },
        },
        "beat_sync_contract": [
            "interviewer_question",
            "guest_reaction",
            "mechanic_state_change",
            "reveal_or_lock",
        ],
        "compositions": COMPOSITIONS,
    }
    SOURCE_JSON.write_text(json.dumps(source, indent=2), encoding="utf-8")


def make_contact_sheet(paths: list[Path]) -> None:
    tw, th = 270, 480
    pad = 32
    label_h = 58
    cols = 4
    rows = 2
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * pad, rows * (th + label_h) + (rows + 1) * pad), "#101010")
    d = ImageDraw.Draw(sheet)
    for i, path in enumerate(paths):
        source = Image.open(path).convert("RGB")
        source.thumbnail((tw, th), Image.Resampling.LANCZOS)
        x = pad + (i % cols) * (tw + pad)
        y = pad + (i // cols) * (th + label_h + pad)
        sheet.paste(source, (x + (tw - source.width) // 2, y))
        label = path.stem.upper()
        label_f = fit(d, label, tw, 24, True)
        center(d, (x, y + th + 10, x + tw, y + th + label_h), label, label_f, WHITE)
    sheet.save(CONTACT_SHEET)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_source_json()
    paths: list[Path] = []
    for spec in COMPOSITIONS:
        image = RENDERERS[spec["renderer"]](spec)
        out = OUT_DIR / spec["file"]
        image.save(out)
        paths.append(out)
    make_contact_sheet(paths)
    print(f"Wrote {len(paths)} reaction clip previews to {OUT_DIR}")
    print(f"Wrote draft JSON source to {SOURCE_JSON}")
    print(f"Wrote contact sheet to {CONTACT_SHEET}")


if __name__ == "__main__":
    main()
