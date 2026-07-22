from __future__ import annotations

import json
from pathlib import Path
from textwrap import wrap
from typing import Any, Callable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
UX_DIR = ROOT / "docs" / "ux" / "mockups"
CAROUSEL_DIR = UX_DIR / "carousel-compositions"
SUPERVISUAL_DIR = UX_DIR / "supervisual-compositions"
OPERATOR_PUBLIC_MOCKUPS = ROOT / "operator-web" / "public" / "mockups"

W, H = 1080, 1350
BLACK = "#050505"
INK = "#0B0B0B"
WHITE = "#FFFFFF"
PAPER = "#F2EAD8"
PAPER_SHADOW = "#D5C8A9"
GOLD = "#FFC21A"
RED = "#FF3B3B"
BLUE = "#2DA7FF"
GREEN = "#38C172"
MUTED = "#8E8E93"
CHARCOAL = "#171717"
SOFT = "#F8F6EF"


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
    "tiny": font(20),
    "tiny_b": font(20, True),
    "xs": font(24),
    "sm": font(30),
    "sm_b": font(30, True),
    "body": font(38),
    "body_b": font(38, True),
    "h3": font(46, True),
    "h2": font(64, True),
    "h1": font(88, True),
    "mega": font(118, True),
}


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    avg = max(8, int(getattr(fnt, "size", 24) * 0.52))
    lines: list[str] = []
    for raw in text.split("\n"):
        if not raw:
            lines.append("")
            continue
        lines.extend(wrap(raw, max(1, max_width // avg)))
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.ImageFont,
    fill: str,
    max_width: int,
    line_gap: int = 10,
    align: str = "left",
) -> int:
    x, y = xy
    for line in wrap_text(draw, text, fnt, max_width):
        tw, _ = text_size(draw, line, fnt)
        tx = x if align == "left" else x + (max_width - tw) // 2
        draw.text((tx, y), line, font=fnt, fill=fill)
        y += getattr(fnt, "size", 24) + line_gap
    return y


def rr(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str | None = None, width: int = 1, radius: int = 10) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fnt: ImageFont.ImageFont, fill: str) -> None:
    x1, y1, x2, y2 = box
    tw, th = text_size(draw, text, fnt)
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2), text, font=fnt, fill=fill)


def chip(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str, fg: str = BLACK) -> tuple[int, int, int, int]:
    x, y = xy
    tw, th = text_size(draw, text, F["tiny_b"])
    box = (x, y, x + tw + 28, y + th + 18)
    rr(draw, box, fill, radius=14)
    draw.text((x + 14, y + 8), text, font=F["tiny_b"], fill=fg)
    return box


def ce_mark(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int = 35, accent: str = GOLD) -> None:
    cx, cy = center
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill="#140909", outline="#2B1515", width=4)
    draw.arc((cx - radius + 10, cy - radius + 10, cx + radius - 10, cy + radius - 10), 35, 325, fill=accent, width=10)
    draw.polygon([(cx + 7, cy - 12), (cx + 27, cy), (cx + 7, cy + 12)], fill=accent)


def paper_note(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str = PAPER_SHADOW) -> None:
    x1, y1, x2, y2 = box
    draw.polygon(
        [
            (x1 + 8, y1),
            (x2 - 12, y1 + 6),
            (x2, y2 - 9),
            (x1 + 14, y2),
            (x1, y1 + 18),
        ],
        fill=fill,
        outline=outline,
    )


def primitive_footer(draw: ImageDraw.ImageDraw, primitives: list[str], dark: bool = True) -> None:
    y = H - 112
    draw.line((60, y - 28, W - 60, y - 28), fill="#333333" if dark else "#D3CAB3", width=2)
    draw.text((60, y), "Primitive gate", font=F["tiny_b"], fill=GOLD if dark else INK)
    x = 260
    for primitive in primitives[:3]:
        box = chip(draw, (x, y - 5), primitive, "#2B2B2B" if dark else "#E9DDBB", WHITE if dark else INK)
        x = box[2] + 12


def carousel_header(draw: ImageDraw.ImageDraw, spec: dict[str, Any], dark: bool = False) -> None:
    fg = WHITE if dark else INK
    sub = MUTED if dark else "#5F584A"
    ce_mark(draw, (78, 72), 34, GOLD)
    draw.text((126, 38), "CONSCIOUS ELITE", font=F["sm_b"], fill=fg)
    draw.text((128, 80), "Carousel composition mockup", font=F["tiny"], fill=sub)
    chip(draw, (760, 42), spec["slide_atom_code"].replace("CAR-SL-", "SL-"), GOLD)
    draw.text((760, 92), spec["allowed_position"], font=F["tiny"], fill=sub)


def supervisual_header(draw: ImageDraw.ImageDraw, spec: dict[str, Any], dark: bool = True) -> None:
    fg = WHITE if dark else INK
    sub = MUTED if dark else "#5F584A"
    ce_mark(draw, (78, 72), 34, spec["accent"])
    draw.text((126, 38), "CONSCIOUS ELITE", font=F["sm_b"], fill=fg)
    draw.text((128, 80), "SuperVisual composition mockup", font=F["tiny"], fill=sub)
    chip(draw, (765, 42), spec["format_code"], spec["accent"])
    draw.text((765, 92), spec["composition_id"], font=F["tiny"], fill=sub)


def draw_face(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float, accent: str = GOLD, body: str = CHARCOAL) -> None:
    r = int(44 * scale)
    draw.ellipse((cx - r, cy - int(155 * scale), cx + r, cy - int(67 * scale)), fill="#CFCFCF", outline=accent, width=max(3, int(5 * scale)))
    rr(
        draw,
        (cx - int(86 * scale), cy - int(68 * scale), cx + int(86 * scale), cy + int(118 * scale)),
        body,
        outline=accent,
        width=max(3, int(5 * scale)),
        radius=max(8, int(16 * scale)),
    )
    draw.line((cx - int(50 * scale), cy - int(28 * scale), cx - int(126 * scale), cy + int(58 * scale)), fill=accent, width=max(3, int(6 * scale)))
    draw.line((cx + int(50 * scale), cy - int(28 * scale), cx + int(126 * scale), cy + int(58 * scale)), fill=accent, width=max(3, int(6 * scale)))


def render_carousel_slide(spec: dict[str, Any]) -> Image.Image:
    dark = spec["theme"] == "dark"
    bg = BLACK if dark else SOFT
    fg = WHITE if dark else INK
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    carousel_header(draw, spec, dark=dark)
    y = 160

    if spec["layout"] == "hook":
        draw.text((70, y), "THE REAL EDGE", font=F["h1"], fill=fg)
        draw.text((70, y + 100), "IS NOT WHERE", font=F["h2"], fill=fg)
        draw.text((70, y + 178), "PEOPLE THINK.", font=F["h2"], fill=RED)
        paper_note(draw, (590, 330, 950, 710), "#EDE2C6")
        center_text(draw, (610, 360, 930, 660), "ONE\nPREMISE", F["h2"], INK)
        draw.line((680, 770, 905, 835), fill=GOLD, width=10)
    elif spec["layout"] == "mirror":
        draw.text((70, y), "THIS IS WHAT", font=F["h2"], fill=fg)
        draw.text((70, y + 78), "YOUR AUDIENCE", font=F["h2"], fill=GOLD)
        draw.text((70, y + 155), "RECOGNIZES.", font=F["h2"], fill=fg)
        rr(draw, (90, 440, 990, 830), "#101010" if dark else WHITE, outline=GOLD, width=4)
        draw_face(draw, 290, 710, 1.0, GOLD)
        draw_wrapped(draw, (445, 510), "I thought I was alone in this exact tension.", F["body_b"], fg, 460)
    elif spec["layout"] == "stakes":
        draw.text((70, y), "THE COST", font=F["mega"], fill=RED)
        draw.text((70, y + 128), "IS QUIET.", font=F["h1"], fill=fg)
        rr(draw, (100, 420, 980, 820), "#151515" if dark else WHITE, outline="#333333" if dark else "#D0D0D0", width=3)
        for i, label in enumerate(["delay", "doubt", "lost trust"]):
            draw.text((150, 485 + i * 95), label.upper(), font=F["h3"], fill=GOLD if i == 1 else fg)
    elif spec["layout"] == "myth":
        paper_note(draw, (80, 180, 940, 415), "#F04B69")
        center_text(draw, (105, 210, 915, 390), "MYTH", F["mega"], WHITE)
        paper_note(draw, (120, 470, 975, 720), "#D8C9A2")
        draw_wrapped(draw, (170, 535), "What people say is not the actual problem.", F["h2"], INK, 760, 8, "center")
        draw.line((185, 810, 900, 730), fill=INK if not dark else WHITE, width=8)
    elif spec["layout"] == "mechanism":
        draw.text((70, y), "HOW IT", font=F["h1"], fill=fg)
        draw.text((70, y + 100), "ACTUALLY WORKS", font=F["h1"], fill=GOLD)
        labels = ["signal", "pattern", "question"]
        for i, label in enumerate(labels):
            x = 95 + i * 315
            rr(draw, (x, 480, x + 245, 665), "#111111" if dark else WHITE, outline=GOLD, width=4)
            center_text(draw, (x, 480, x + 245, 665), label.upper(), F["sm_b"], fg)
            if i < 2:
                draw.line((x + 250, 575, x + 305, 575), fill=GOLD, width=8)
    elif spec["layout"] == "pillar":
        draw.text((70, y), "3 PILLARS", font=F["mega"], fill=fg)
        for i, label in enumerate(["context", "contrast", "proof"]):
            x = 95 + i * 310
            rr(draw, (x, 420, x + 235, 835), "#111111" if dark else WHITE, outline=[GOLD, BLUE, GREEN][i], width=5)
            center_text(draw, (x, 470, x + 235, 580), str(i + 1), F["mega"], [GOLD, BLUE, GREEN][i])
            draw_wrapped(draw, (x + 25, 640), label.upper(), F["sm_b"], fg, 185, 8, "center")
    elif spec["layout"] == "juxtaposition":
        draw.text((70, y), "WOULD YOU", font=F["h1"], fill=fg)
        draw.text((70, y + 100), "CHOOSE THIS?", font=F["h1"], fill=GOLD)
        rr(draw, (80, 405, 500, 820), "#0F1A22" if dark else "#E7F2FF", outline=BLUE, width=8)
        rr(draw, (580, 405, 1000, 820), "#231111" if dark else "#FFF1F1", outline=RED, width=8)
        center_text(draw, (80, 405, 500, 820), "OLD\nFRAME", F["h2"], BLUE)
        center_text(draw, (580, 405, 1000, 820), "NEW\nFRAME", F["h2"], RED)
    elif spec["layout"] == "evidence":
        draw.text((70, y), "THE RECEIPT", font=F["h1"], fill=fg)
        rr(draw, (95, 365, 985, 805), "#111111" if dark else WHITE, outline="#333333" if dark else "#D6D6D6", width=3)
        for i, label in enumerate(["quote", "timestamp", "source"]):
            paper_note(draw, (145, 420 + i * 110, 900, 500 + i * 110), "#EFE7D2")
            draw.text((175, 438 + i * 110), label.upper(), font=F["sm_b"], fill=INK)
    elif spec["layout"] == "scene":
        draw.text((70, y), "MAKE IT", font=F["h1"], fill=fg)
        draw.text((70, y + 100), "CONCRETE.", font=F["h1"], fill=GOLD)
        rr(draw, (95, 395, 985, 830), "#111820", outline="#303030", width=3)
        draw.rectangle((95, 650, 985, 830), fill="#202C36")
        draw_face(draw, 540, 760, 1.15, GOLD)
        draw.text((135, 445), "scene / object / place", font=F["h3"], fill=WHITE)
    elif spec["layout"] == "break":
        draw.text((70, y), "PATTERN", font=F["mega"], fill=fg)
        draw.text((70, y + 130), "BREAK", font=F["mega"], fill=RED)
        for i in range(6):
            x = 105 + i * 150
            rr(draw, (x, 510 + (i % 2) * 55, x + 105, 650 + (i % 2) * 55), "#222222" if dark else WHITE, outline=GOLD if i == 3 else "#777777", width=4)
        draw.line((140, 835, 930, 760), fill=RED, width=10)
    elif spec["layout"] == "identity":
        draw.text((70, y), "FROM", font=F["h1"], fill=MUTED)
        draw.text((70, y + 92), "THE ROLE", font=F["h1"], fill=RED)
        draw.text((70, y + 210), "TO THE SELF", font=F["h1"], fill=GOLD)
        draw_face(draw, 290, 790, 1.0, RED)
        draw_face(draw, 730, 790, 1.0, GOLD)
        draw.line((410, 690, 610, 690), fill=fg, width=8)
    else:
        draw.text((70, y), "NOW APPLY IT", font=F["h1"], fill=fg)
        rr(draw, (105, 380, 975, 770), "#111111" if dark else WHITE, outline=GOLD, width=5)
        for i in range(3):
            draw.ellipse((150, 440 + i * 92, 205, 495 + i * 92), fill=GOLD)
            draw.text((235, 442 + i * 92), ["try this", "save this", "ask this"][i].upper(), font=F["body_b"], fill=fg)

    draw_wrapped(draw, (70, 930), spec["display_name"], F["h3"], fg, 870)
    draw_wrapped(draw, (70, 995), spec["meaning"], F["xs"], "#C7C7C7" if dark else "#4E493F", 900, 8)
    primitive_footer(draw, spec["primitives"], dark=dark)
    return img


def render_supervisual(spec: dict[str, Any]) -> Image.Image:
    dark = spec["theme"] == "dark"
    bg = BLACK if dark else SOFT
    fg = WHITE if dark else INK
    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)
    supervisual_header(draw, spec, dark=dark)

    if spec["layout"] == "binary":
        draw.text((65, 170), "WHO IS", font=F["mega"], fill=fg)
        draw.text((65, 300), "RIGHT?", font=F["mega"], fill=spec["accent"])
        rr(draw, (70, 465, 500, 865), "#191010" if dark else "#FFF0F0", outline=RED, width=7)
        rr(draw, (580, 465, 1010, 865), "#0E1A13" if dark else "#ECFFF1", outline=GREEN, width=7)
        center_text(draw, (70, 465, 500, 865), "OLD\nBELIEF", F["h2"], RED)
        center_text(draw, (580, 465, 1010, 865), "NEW\nLEVER", F["h2"], GREEN)
    elif spec["layout"] == "proof":
        draw.text((65, 170), "THIS CHANGED", font=F["h1"], fill=fg)
        draw.text((65, 270), "THE GAME.", font=F["h1"], fill=spec["accent"])
        rr(draw, (95, 420, 985, 870), "#111111" if dark else WHITE, outline=spec["accent"], width=5)
        draw_face(draw, 840, 805, 1.05, spec["accent"])
        paper_note(draw, (145, 490, 730, 650), "#EFE7D2")
        draw_wrapped(draw, (175, 525), "source-backed claim with visible receipt", F["body_b"], INK, 500)
    elif spec["layout"] == "scenario":
        draw.text((65, 170), "ONE SCENE.", font=F["h1"], fill=fg)
        draw.text((65, 270), "TWO FUTURES.", font=F["h1"], fill=spec["accent"])
        rr(draw, (80, 430, 1000, 875), "#101010" if dark else WHITE, outline="#333333" if dark else "#CCCCCC", width=4)
        draw.line((540, 430, 540, 875), fill=spec["accent"], width=5)
        draw_wrapped(draw, (130, 560), "default path", F["h3"], RED, 320, align="center")
        draw_wrapped(draw, (615, 560), "conscious path", F["h3"], GREEN, 320, align="center")
    elif spec["layout"] == "object":
        draw.text((65, 170), "THE OBJECT", font=F["h1"], fill=fg)
        draw.text((65, 270), "SAYS IT.", font=F["h1"], fill=spec["accent"])
        draw.ellipse((360, 455, 735, 830), fill="#211A10" if dark else "#E9DDBB", outline=spec["accent"], width=8)
        center_text(draw, (360, 455, 735, 830), "SYMBOL", F["h2"], spec["accent"])
        draw.line((250, 790, 390, 720), fill=WHITE if dark else INK, width=5)
    elif spec["layout"] == "emotional":
        draw.text((65, 170), "A MOMENT", font=F["h1"], fill=fg)
        draw.text((65, 270), "YOU FEEL.", font=F["h1"], fill=spec["accent"])
        rr(draw, (95, 410, 985, 885), "#0E1218", outline="#2C3340", width=3)
        draw.rectangle((95, 695, 985, 885), fill="#111827")
        draw_face(draw, 560, 840, 1.25, spec["accent"])
        draw.line((165, 515, 915, 465), fill=spec["accent"], width=5)
    elif spec["layout"] == "urgency":
        draw.text((65, 170), "THE PRESSURE", font=F["h1"], fill=fg)
        draw.text((65, 270), "HAS A SHAPE.", font=F["h1"], fill=spec["accent"])
        for i in range(5):
            rr(draw, (160 + i * 120, 470 + i * 55, 285 + i * 120, 705 + i * 45), "#1B1B1B" if dark else WHITE, outline=spec["accent"] if i == 4 else "#777777", width=4)
        draw.text((245, 860), "compression visual", font=F["h3"], fill=fg)
    elif spec["layout"] == "quote":
        draw_face(draw, 820, 945, 1.4, spec["accent"])
        draw_wrapped(draw, (70, 170), "Knowledge is POWER.", F["h1"], fg, 720)
        draw_wrapped(draw, (70, 380), "Awareness is FREEDOM.", F["h1"], spec["accent"], 780)
        draw.line((70, 650, 690, 650), fill=spec["accent"], width=6)
    elif spec["layout"] == "blackquote":
        draw.text((85, 240), "\"", font=font(190, True), fill=spec["accent"])
        draw_wrapped(draw, (135, 365), "The point is not to look impressive. The point is to make the signal undeniable.", F["h2"], fg, 805, 14)
        draw.text((135, 825), "- Guest insight", font=F["body_b"], fill=MUTED)
    else:
        draw.text((65, 160), "LIVE SESSION", font=F["h1"], fill=fg)
        rr(draw, (85, 320, 995, 860), "#111111" if dark else WHITE, outline=spec["accent"], width=5)
        draw_face(draw, 300, 790, 1.1, spec["accent"])
        draw_wrapped(draw, (500, 450), "Expert teaching moment, guest proof, and brand-forward authority.", F["h2"], fg, 400)

    draw_wrapped(draw, (70, 960), spec["title"], F["h3"], fg, 900)
    draw_wrapped(draw, (70, 1022), spec["visual_feel"], F["xs"], "#D6D6D6" if dark else "#4E493F", 890, 8)
    primitive_footer(draw, spec["primitives"], dark=dark)
    return img


CAROUSEL_SPECS: list[dict[str, Any]] = [
    {
        "slide_atom_code": "CAR-SL-001-HOOK-PREMISE",
        "display_name": "Hook Premise Cover",
        "meaning": "Name the edge, contradiction, promise, or question that makes the sequence worth swiping.",
        "allowed_position": "first slide",
        "layout": "hook",
        "theme": "light",
        "primitives": ["PRM-PRS-015", "PRM-BUS-003", "PRM-VSG-001"],
    },
    {
        "slide_atom_code": "CAR-SL-002-AUDIENCE-MIRROR",
        "display_name": "Audience Mirror",
        "meaning": "Make the audience recognize itself before teaching or challenging it.",
        "allowed_position": "early or middle",
        "layout": "mirror",
        "theme": "dark",
        "primitives": ["PRM-PRS-015", "PRM-PRS-032", "PRM-VSG-024"],
    },
    {
        "slide_atom_code": "CAR-SL-003-STAKES-COST",
        "display_name": "Stakes and Cost",
        "meaning": "Show what the current belief, habit, or blind spot is costing.",
        "allowed_position": "early or middle",
        "layout": "stakes",
        "theme": "dark",
        "primitives": ["PRM-PRS-015", "PRM-BUS-003", "PRM-VSG-024"],
    },
    {
        "slide_atom_code": "CAR-SL-004-MYTH-BREAK",
        "display_name": "Myth Break",
        "meaning": "Separate the false belief from the truer frame without flattening nuance.",
        "allowed_position": "early or middle",
        "layout": "myth",
        "theme": "light",
        "primitives": ["PRM-PRS-015", "PRM-PRS-032", "PRM-VSG-001"],
    },
    {
        "slide_atom_code": "CAR-SL-005-MECHANISM-REVEAL",
        "display_name": "Mechanism Reveal",
        "meaning": "Reveal the causal logic behind the insight instead of only stating the result.",
        "allowed_position": "middle",
        "layout": "mechanism",
        "theme": "dark",
        "primitives": ["PRM-PRS-032", "PRM-PRS-025", "PRM-BUS-012"],
    },
    {
        "slide_atom_code": "CAR-SL-006-THREE-PILLAR-MAP",
        "display_name": "Three-Pillar Map",
        "meaning": "Give the audience a compact cognitive map it can remember and reuse.",
        "allowed_position": "middle",
        "layout": "pillar",
        "theme": "light",
        "primitives": ["PRM-PRS-025", "PRM-PRS-032", "PRM-BUS-012"],
    },
    {
        "slide_atom_code": "CAR-SL-007-JUXTAPOSITION",
        "display_name": "Juxtaposition Split",
        "meaning": "Place two frames or futures in direct visual contact so the contrast becomes obvious.",
        "allowed_position": "middle",
        "layout": "juxtaposition",
        "theme": "dark",
        "primitives": ["PRM-PRS-015", "PRM-VSG-018", "PRM-VSG-001"],
    },
    {
        "slide_atom_code": "CAR-SL-008-EVIDENCE-OBJECT",
        "display_name": "Evidence Object",
        "meaning": "Turn proof into a visible object, receipt, timestamp, or quoted artifact.",
        "allowed_position": "middle",
        "layout": "evidence",
        "theme": "light",
        "primitives": ["PRM-PRS-032", "PRM-BUS-003", "PRM-VSG-001"],
    },
    {
        "slide_atom_code": "CAR-SL-009-CONCRETE-SCENE",
        "display_name": "Concrete Scene",
        "meaning": "Replace abstraction with a specific place, object, human pressure, or lived scene.",
        "allowed_position": "middle",
        "layout": "scene",
        "theme": "dark",
        "primitives": ["PRM-PRS-032", "PRM-VSG-018", "PRM-VSG-024"],
    },
    {
        "slide_atom_code": "CAR-SL-010-PATTERN-BREAK",
        "display_name": "Pattern Break",
        "meaning": "Interrupt the reader's expected rhythm with a visual or semantic reset.",
        "allowed_position": "middle",
        "layout": "break",
        "theme": "light",
        "primitives": ["PRM-HUM-032", "PRM-HUM-034", "PRM-VSG-018"],
    },
    {
        "slide_atom_code": "CAR-SL-011-REFRAME-IDENTITY",
        "display_name": "Reframe and Identity Shift",
        "meaning": "Move the reader from role-based thinking to a clearer self-understanding.",
        "allowed_position": "late",
        "layout": "identity",
        "theme": "dark",
        "primitives": ["PRM-PRS-015", "PRM-BUS-003", "PRM-VSG-024"],
    },
    {
        "slide_atom_code": "CAR-SL-012-APPLICATION-CTA",
        "display_name": "Application CTA",
        "meaning": "Close with an action that preserves the intelligence of the sequence.",
        "allowed_position": "last slide",
        "layout": "cta",
        "theme": "light",
        "primitives": ["PRM-PRS-025", "PRM-PRS-032", "PRM-BUS-012"],
    },
]


SUPERVISUAL_SPECS: list[dict[str, Any]] = [
    {
        "format_code": "SPV-CON",
        "composition_id": "CONCEPTUAL_CONTRAST_POSTER_DARK",
        "title": "Conceptual Contrast Poster",
        "visual_feel": "Binary tension, immediate legibility, strong contrast, one decisive question.",
        "layout": "binary",
        "theme": "dark",
        "accent": GOLD,
        "primitives": ["PRM-PRS-015", "PRM-VSG-001", "PRM-VSG-024"],
    },
    {
        "format_code": "SPV-CON",
        "composition_id": "POWERFUL_DEMONSTRATION_SINGLE",
        "title": "Source-Backed Demonstration",
        "visual_feel": "A claim becomes credible because proof is staged inside the frame.",
        "layout": "proof",
        "theme": "dark",
        "accent": BLUE,
        "primitives": ["PRM-PRS-032", "PRM-BUS-003", "PRM-VSG-001"],
    },
    {
        "format_code": "SPV-CON",
        "composition_id": "ONE_SCENE_TWO_SCENARIOS",
        "title": "One Scene, Two Scenarios",
        "visual_feel": "A single situation divides into two possible futures or interpretations.",
        "layout": "scenario",
        "theme": "light",
        "accent": RED,
        "primitives": ["PRM-PRS-015", "PRM-VSG-018", "PRM-VSG-024"],
    },
    {
        "format_code": "SPV-SYM",
        "composition_id": "CARTOON_OBJECT_METAPHOR",
        "title": "Symbolic Object Metaphor",
        "visual_feel": "One object carries the full concept without becoming decorative filler.",
        "layout": "object",
        "theme": "dark",
        "accent": GOLD,
        "primitives": ["PRM-HUM-025", "PRM-VSG-021", "PRM-VSG-024"],
    },
    {
        "format_code": "SPV-SYM",
        "composition_id": "MAIN_CHARACTER_EMOTIONAL_SCENE",
        "title": "Main Character Emotional Scene",
        "visual_feel": "A felt human moment, cinematic negative space, and one specific emotional signal.",
        "layout": "emotional",
        "theme": "dark",
        "accent": GREEN,
        "primitives": ["PRM-ACT-005", "PRM-VOC-009", "PRM-VSG-016"],
    },
    {
        "format_code": "SPV-SYM",
        "composition_id": "PROBLEM_AMPLIFICATION_URGENCY",
        "title": "Pressure Shape",
        "visual_feel": "The hidden pressure behind the problem becomes spatial, visible, and inspectable.",
        "layout": "urgency",
        "theme": "light",
        "accent": RED,
        "primitives": ["PRM-PRS-015", "PRM-BUS-003", "PRM-VSG-024"],
    },
    {
        "format_code": "SPV-PRM",
        "composition_id": "QUOTE_ON_CLOSEUP_COMMENTARY",
        "title": "Premium Quote Closeup",
        "visual_feel": "Brand-forward quote treatment with human presence and controlled authority.",
        "layout": "quote",
        "theme": "dark",
        "accent": GOLD,
        "primitives": ["PRM-BUS-003", "PRM-VSG-001", "PRM-VSG-021"],
    },
    {
        "format_code": "SPV-PRM",
        "composition_id": "MINIMAL_BLACK_QUOTE_CARD",
        "title": "Minimal Black Quote Card",
        "visual_feel": "A premium stillness frame where the sentence, spacing, and emphasis carry authority.",
        "layout": "blackquote",
        "theme": "dark",
        "accent": GOLD,
        "primitives": ["PRM-PRS-025", "PRM-VSG-001", "PRM-VSG-024"],
    },
    {
        "format_code": "SPV-PRM",
        "composition_id": "EXPERT_FLYER_MINIMAL",
        "title": "Expert Authority Flyer",
        "visual_feel": "Polished promotional authority without losing source-backed specificity.",
        "layout": "flyer",
        "theme": "light",
        "accent": GOLD,
        "primitives": ["PRM-PRS-032", "PRM-BUS-012", "PRM-VSG-001"],
    },
]


def slugify(value: str) -> str:
    return value.lower().replace("_", "-").replace(" ", "-")


def write_json(path: Path, schema: str, items: list[dict[str, Any]]) -> None:
    payload = {
        "schema": schema,
        "status": "draft_visual_approval_not_production_template",
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
        "primitive_policy": {
            "minimum_validated_primitives": 3,
            "required_roles": ["meaning_transform", "delivery_shape", "format_material"],
        },
        "compositions": items,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def make_contact_sheet(paths: list[Path], target: Path, cols: int) -> None:
    thumb_w, thumb_h = 300, 375
    label_h = 96
    pad = 36
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * pad, rows * (thumb_h + label_h) + (rows + 1) * pad), "#101010")
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(paths):
        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = pad + (i % cols) * (thumb_w + pad)
        y = pad + (i // cols) * (thumb_h + label_h + pad)
        sheet.paste(img, (x + (thumb_w - img.width) // 2, y))
        label = path.stem.upper().replace("CAR-SL-", "SL-").replace("SPV-", "")
        draw_wrapped(draw, (x, y + thumb_h + 8), label, F["tiny_b"], WHITE, thumb_w, line_gap=3, align="center")
    sheet.save(target)


def write_readme() -> None:
    readme = UX_DIR / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# CMF Studio UX Mockups",
                "",
                "Generated visual approval assets for composition families.",
                "",
                "## Still Visuals",
                "",
                "- `carousel-compositions/`: 12 carousel slide-atom mockups plus a contact sheet.",
                "- `supervisual-compositions/`: 9 SuperVisual family mockups plus a contact sheet.",
                "",
                "Regenerate with:",
                "",
                "```bash",
                "python tools/generate_still_visual_mockups.py",
                "```",
                "",
                "These are approval mockups, not production render templates. Production still visuals must be compiled from composition JSON, primitive gates, and renderer receipts.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def generate_family(
    output_dir: Path,
    specs: list[dict[str, Any]],
    renderer: Callable[[dict[str, Any]], Image.Image],
    json_name: str,
    schema: str,
    cols: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    OPERATOR_PUBLIC_MOCKUPS.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    source_specs: list[dict[str, Any]] = []
    for spec in specs:
        image = renderer(spec)
        if "slide_atom_code" in spec:
            filename = f"{slugify(spec['slide_atom_code'])}.png"
        else:
            filename = f"{slugify(spec['format_code'])}-{slugify(spec['composition_id'])}.png"
        out = output_dir / filename
        image.save(out)
        paths.append(out)
        item = dict(spec)
        item["preview_file"] = filename
        source_specs.append(item)
    write_json(output_dir / json_name, schema, source_specs)
    contact_name = "_carousel-composition-contact-sheet.png" if "carousel" in json_name else "_supervisual-composition-contact-sheet.png"
    make_contact_sheet(paths, output_dir / contact_name, cols)
    make_contact_sheet(paths, OPERATOR_PUBLIC_MOCKUPS / contact_name, cols)


def main() -> None:
    generate_family(
        CAROUSEL_DIR,
        CAROUSEL_SPECS,
        render_carousel_slide,
        "_carousel-compositions.draft.json",
        "cmf.carousel_composition_mockups.v1",
        4,
    )
    generate_family(
        SUPERVISUAL_DIR,
        SUPERVISUAL_SPECS,
        render_supervisual,
        "_supervisual-compositions.draft.json",
        "cmf.supervisual_composition_mockups.v1",
        3,
    )
    write_readme()
    print(f"Wrote carousel mockups to {CAROUSEL_DIR}")
    print(f"Wrote SuperVisual mockups to {SUPERVISUAL_DIR}")


if __name__ == "__main__":
    main()
