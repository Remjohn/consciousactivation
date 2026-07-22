from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "ui" / "composition-boards"

BLACK = "#050505"
INK = "#0b0b0b"
WHITE = "#f7f7f2"
MUTED = "#9b9b9b"
GOLD = "#ffc21a"
RED = "#ff3b30"
BLUE = "#2da8ff"
GREEN = "#42c66b"
PAPER = "#eee7d5"
PAPER_DARK = "#cdbb8d"
PANEL = "#101010"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


F = {
    "board": font(50, True),
    "sub": font(24),
    "tiny": font(16),
    "small": font(18, True),
    "body": font(20),
    "body_bold": font(22, True),
    "card": font(26, True),
    "hero": font(36, True),
    "label": font(18, True),
    "mono": font(16),
}


def draw_wrapped(draw: ImageDraw.ImageDraw, xy, text: str, fill: str, fnt, width: int, line_gap: int = 4):
    x, y = xy
    avg = max(7, int(fnt.size * 0.52))
    lines = []
    for raw in text.split("\n"):
        lines.extend(wrap(raw, max(1, width // avg)) or [""])
    for line in lines:
        draw.text((x, y), line, fill=fill, font=fnt)
        y += fnt.size + line_gap
    return y


def rr(draw: ImageDraw.ImageDraw, box, fill, outline=None, width=1, radius=8):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def line(draw: ImageDraw.ImageDraw, p1, p2, fill, width=4):
    draw.line([p1, p2], fill=fill, width=width)


def arrow(draw: ImageDraw.ImageDraw, p1, p2, fill, width=4):
    line(draw, p1, p2, fill, width)
    x1, y1 = p1
    x2, y2 = p2
    dx = 1 if x2 >= x1 else -1
    draw.polygon([(x2, y2), (x2 - 16 * dx, y2 - 10), (x2 - 16 * dx, y2 + 10)], fill=fill)


def chip(draw, x, y, text, fill=GOLD, ink=BLACK):
    pad_x = 10
    pad_y = 6
    bbox = draw.textbbox((0, 0), text, font=F["tiny"])
    w = bbox[2] - bbox[0] + pad_x * 2
    h = bbox[3] - bbox[1] + pad_y * 2
    rr(draw, (x, y, x + w, y + h), fill, radius=6)
    draw.text((x + pad_x, y + pad_y - 1), text, fill=ink, font=F["tiny"])
    return x + w + 8


def avatar(draw, cx, cy, scale=1.0, accent=GOLD, side="guest"):
    head_r = int(26 * scale)
    torso_w = int(88 * scale)
    torso_h = int(120 * scale)
    draw.ellipse((cx - head_r, cy - 130 * scale, cx + head_r, cy - 78 * scale), fill="#d8d8d8", outline=accent, width=max(2, int(4 * scale)))
    rr(
        draw,
        (cx - torso_w // 2, cy - 78 * scale, cx + torso_w // 2, cy + torso_h),
        fill="#1b1b1b" if side == "guest" else "#2a2a2a",
        outline=accent,
        width=max(2, int(4 * scale)),
        radius=12,
    )
    draw.line((cx - torso_w // 2, cy - 10 * scale, cx - torso_w, cy + 58 * scale), fill=accent, width=max(3, int(5 * scale)))
    draw.line((cx + torso_w // 2, cy - 10 * scale, cx + torso_w, cy + 58 * scale), fill=accent, width=max(3, int(5 * scale)))


@dataclass
class Comp:
    n: int
    code: str
    title: str
    route: str
    promise: str
    zones: str
    layout: str
    accent: str = GOLD


def top_meta(draw, x, y, w, spec: Comp):
    rr(draw, (x + 18, y + 18, x + w - 18, y + 82), "#111111", outline="#282828", radius=8)
    chip(draw, x + 32, y + 34, f"{spec.n:02d} {spec.code}", spec.accent)
    draw.text((x + 192, y + 31), spec.route, fill=WHITE, font=F["small"])
    draw.text((x + 32, y + 88), "WS: guest workspace  |  asset: GUEST-" + spec.code + f"-{spec.n:03d}", fill=MUTED, font=F["tiny"])


def footer(draw, x, y, w, h, spec: Comp):
    rr(draw, (x + 18, y + h - 108, x + w - 18, y + h - 20), "#111111", outline="#2a2a2a", radius=8)
    draw.text((x + 32, y + h - 96), "composition_json", fill=spec.accent, font=F["label"])
    draw_wrapped(draw, (x + 32, y + h - 70), spec.zones, MUTED, F["mono"], w - 70, line_gap=1)


def story_layout(draw, x, y, w, h, spec: Comp):
    top_meta(draw, x, y, w, spec)
    sx, sy = x + 28, y + 122
    sw, sh = w - 56, 540
    rr(draw, (sx, sy, sx + sw, sy + sh), "#070707", outline="#333333", radius=8)
    if spec.layout == "closeup":
        draw.rectangle((sx, sy, sx + sw, sy + sh), fill="#0a0a0a")
        draw.ellipse((sx + 130, sy + 50, sx + sw - 130, sy + 315), fill="#2d2d2d", outline=GOLD, width=5)
        avatar(draw, sx + sw // 2, sy + 455, 1.0, spec.accent)
        rr(draw, (sx + 42, sy + sh - 170, sx + sw - 42, sy + sh - 82), "#000000", outline=GOLD, radius=8)
        draw_wrapped(draw, (sx + 64, sy + sh - 155), "emotional subtitle from the interview moment", WHITE, F["body_bold"], sw - 128)
    elif spec.layout == "object-split":
        draw.rectangle((sx, sy, sx + sw // 2, sy + sh), fill="#151515")
        draw.rectangle((sx + sw // 2, sy, sx + sw, sy + sh), fill="#090909")
        rr(draw, (sx + 42, sy + 64, sx + sw // 2 - 36, sy + 370), "#302412", outline=GOLD, width=4)
        draw.text((sx + 70, sy + 170), "memory\nobject", fill=GOLD, font=F["hero"], spacing=6)
        avatar(draw, sx + sw * 3 // 4, sy + 420, .9, spec.accent)
        rr(draw, (sx + sw // 2 + 30, sy + sh - 175, sx + sw - 30, sy + sh - 78), "#000000", outline="#555555")
        draw_wrapped(draw, (sx + sw // 2 + 48, sy + sh - 158), "object -> memory -> testimony", WHITE, F["body_bold"], sw // 2 - 88)
    elif spec.layout == "story-arc":
        rr(draw, (sx + 45, sy + 90, sx + sw - 45, sy + 310), "#151515", outline=GOLD, width=3)
        draw.text((sx + 70, sy + 115), "RUPTURE ARC", fill=WHITE, font=F["hero"])
        for i, label in enumerate(["before", "rupture", "after"]):
            px = sx + 90 + i * 170
            draw.ellipse((px, sy + 430, px + 70, sy + 500), fill=spec.accent)
            draw.text((px - 6, sy + 515), label, fill=WHITE, font=F["label"])
            if i < 2:
                arrow(draw, (px + 82, sy + 464), (px + 150, sy + 464), "#666666", 4)
        draw.line((sx + 70, sy + sh - 132, sx + sw - 70, sy + sh - 132), fill=GOLD, width=5)
    elif spec.layout == "scene":
        draw.rectangle((sx, sy, sx + sw, sy + sh), fill="#111827")
        for i in range(4):
            rr(draw, (sx + 45 + i * 118, sy + 105 + i * 12, sx + 150 + i * 118, sy + 360 + i * 12), "#262626", outline="#777777")
        avatar(draw, sx + sw // 2, sy + 440, .8, spec.accent)
        draw.text((sx + 68, sy + sh - 166), "scene reconstruction", fill=GOLD, font=F["hero"])
    elif spec.layout == "interview-lens":
        draw.rectangle((sx, sy, sx + sw, sy + sh), fill="#090909")
        avatar(draw, sx + 185, sy + 430, .8, BLUE, "interviewer")
        avatar(draw, sx + 400, sy + 430, .8, GOLD)
        rr(draw, (sx + 48, sy + 80, sx + sw - 48, sy + 185), "#151515", outline=GOLD, width=3)
        draw_wrapped(draw, (sx + 70, sy + 100), "interviewer question card", WHITE, F["body_bold"], sw - 140)
        draw.arc((sx + 135, sy + 250, sx + 455, sy + 570), 200, 340, fill="#666666", width=4)
    else:
        for i in range(3):
            rr(draw, (sx + 44, sy + 70 + i * 145, sx + sw - 44, sy + 170 + i * 145), "#151515", outline=GOLD if i == 1 else "#555555")
            draw.text((sx + 66, sy + 96 + i * 145), ["SOURCE", "EMOTION", "DISTILLATION"][i], fill=WHITE, font=F["body_bold"])
        avatar(draw, sx + sw // 2, sy + sh - 110, .6, spec.accent)
    draw_wrapped(draw, (x + 34, y + 705), spec.title, WHITE, F["card"], w - 68)
    draw_wrapped(draw, (x + 34, y + 765), spec.promise, MUTED, F["body"], w - 68)
    footer(draw, x, y, w, h, spec)


def edu_layout(draw, x, y, w, h, spec: Comp):
    top_meta(draw, x, y, w, spec)
    sx, sy = x + 28, y + 122
    sw, sh = w - 56, 540
    rr(draw, (sx, sy, sx + sw, sy + sh), PAPER, outline=PAPER_DARK, radius=8)
    if spec.layout == "papercut-stage":
        for i, c in enumerate(["#d9cda6", "#c8b06a", "#f5f0dc"]):
            rr(draw, (sx + 45 + i * 20, sy + 75 + i * 30, sx + sw - 65 + i * 6, sy + sh - 140 + i * 6), c, outline="#a28c52")
        avatar(draw, sx + 160, sy + 430, .7, INK)
        draw.ellipse((sx + 300, sy + 170, sx + 475, sy + 345), fill=GOLD, outline=INK, width=4)
        arrow(draw, (sx + 250, sy + 395), (sx + 430, sy + 395), INK, 5)
    elif spec.layout == "river":
        draw.polygon([(sx, sy + 520), (sx + 160, sy + 380), (sx + 300, sy + 535), (sx + sw, sy + 350), (sx + sw, sy + sh), (sx, sy + sh)], fill="#87c27f")
        draw.polygon([(sx, sy + 630), (sx + 175, sy + 470), (sx + 320, sy + 640), (sx + sw, sy + 470), (sx + sw, sy + sh), (sx, sy + sh)], fill="#4c8f54")
        draw.line((sx + 75, sy + 125, sx + sw - 75, sy + 125), fill=INK, width=6)
        draw.text((sx + 80, sy + 145), "bank", fill=INK, font=F["body_bold"])
        draw.text((sx + sw - 180, sy + 145), "flow", fill=INK, font=F["body_bold"])
        arrow(draw, (sx + 170, sy + 265), (sx + sw - 145, sy + 265), GOLD, 7)
    elif spec.layout == "framework":
        for i, label in enumerate(["context", "primitive", "question"]):
            rr(draw, (sx + 70, sy + 95 + i * 150, sx + sw - 70, sy + 205 + i * 150), "#fffaf0", outline=INK, width=4)
            draw.text((sx + 105, sy + 128 + i * 150), label.upper(), fill=INK, font=F["body_bold"])
            if i < 2:
                arrow(draw, (sx + sw // 2, sy + 212 + i * 150), (sx + sw // 2, sy + 250 + i * 150), GOLD, 5)
    elif spec.layout == "timeline":
        draw.line((sx + 75, sy + 220, sx + sw - 75, sy + 220), fill=INK, width=5)
        for i, label in enumerate(["research", "edge", "brief", "extract"]):
            px = sx + 80 + i * 125
            draw.ellipse((px, sy + 185, px + 70, sy + 255), fill=GOLD, outline=INK, width=3)
            draw_wrapped(draw, (px - 8, sy + 275), label, INK, F["label"], 90)
        avatar(draw, sx + 135, sy + 430, .65, INK)
    elif spec.layout == "contrast":
        rr(draw, (sx + 45, sy + 85, sx + sw - 45, sy + 315), "#fffaf0", outline=RED, width=5)
        rr(draw, (sx + 45, sy + 360, sx + sw - 45, sy + 590), "#fffaf0", outline=GOLD, width=5)
        draw.text((sx + 75, sy + 150), "SURFACE ANSWER", fill=RED, font=F["hero"])
        draw.text((sx + 75, sy + 425), "DEEPER PREMISE", fill=INK, font=F["hero"])
    else:
        for i in range(5):
            rr(draw, (sx + 45 + i * 90, sy + 88 + (i % 2) * 70, sx + 125 + i * 90, sy + 168 + (i % 2) * 70), "#fffaf0", outline=INK)
        avatar(draw, sx + 180, sy + 430, .7, INK)
        rr(draw, (sx + 260, sy + 410, sx + sw - 45, sy + 590), "#fffaf0", outline=GOLD, width=4)
        draw_wrapped(draw, (sx + 285, sy + 435), "interview brief question engine", INK, F["body_bold"], sw - 330)
    draw_wrapped(draw, (x + 34, y + 705), spec.title, INK if False else WHITE, F["card"], w - 68)
    draw_wrapped(draw, (x + 34, y + 765), spec.promise, MUTED, F["body"], w - 68)
    footer(draw, x, y, w, h, spec)


def frb_layout(draw, x, y, w, h, spec: Comp):
    top_meta(draw, x, y, w, spec)
    sx, sy = x + 28, y + 122
    sw, sh = w - 56, 540
    rr(draw, (sx, sy, sx + sw, sy + sh), "#070707", outline="#303030", radius=8)
    if spec.layout == "myth-reality":
        rr(draw, (sx + 35, sy + 70, sx + sw - 35, sy + 285), "#171717", outline=RED, width=5)
        rr(draw, (sx + 35, sy + 335, sx + sw - 35, sy + 550), "#171717", outline=GOLD, width=5)
        draw.text((sx + 68, sy + 130), "MYTH", fill=RED, font=F["hero"])
        draw.text((sx + 68, sy + 395), "REALITY", fill=GOLD, font=F["hero"])
    elif spec.layout == "verdict":
        draw.text((sx + 105, sy + 135), "FALSE FRAME", fill=WHITE, font=F["hero"])
        draw.line((sx + 80, sy + 260, sx + sw - 80, sy + 90), fill=RED, width=12)
        rr(draw, (sx + 75, sy + 390, sx + sw - 75, sy + 560), "#1b1b1b", outline=GOLD, width=4)
        draw.text((sx + 115, sy + 440), "NEW FRAME", fill=GOLD, font=F["hero"])
    elif spec.layout == "evidence-wall":
        for i in range(6):
            px = sx + 48 + (i % 2) * 235
            py = sy + 65 + (i // 2) * 170
            rr(draw, (px, py, px + 190, py + 120), "#181818", outline=GOLD if i == 2 else "#555555")
            draw.text((px + 16, py + 42), "receipt", fill=WHITE, font=F["body_bold"])
        line(draw, (sx + 144, sy + 185), (sx + 380, sy + 355), RED, 3)
        line(draw, (sx + 380, sy + 185), (sx + 144, sy + 525), RED, 3)
    elif spec.layout == "heatmap":
        for i in range(4):
            for j in range(4):
                colors = ["#251414", "#482016", "#775112", "#c19114"]
                rr(draw, (sx + 70 + j * 96, sy + 92 + i * 96, sx + 150 + j * 96, sy + 172 + i * 96), colors[(i + j) % 4], outline="#2a2a2a")
        draw.text((sx + 80, sy + 470), "contradiction heat", fill=GOLD, font=F["hero"])
    elif spec.layout == "receipts":
        avatar(draw, sx + 130, sy + 430, .72, GOLD)
        for i, lab in enumerate(["quote", "clip", "source"]):
            rr(draw, (sx + 250, sy + 105 + i * 150, sx + sw - 50, sy + 215 + i * 150), "#171717", outline=GOLD if i == 1 else "#555555")
            draw.text((sx + 275, sy + 138 + i * 150), lab.upper(), fill=WHITE, font=F["body_bold"])
    else:
        rr(draw, (sx + 45, sy + 90, sx + sw - 45, sy + 240), "#171717", outline=RED, width=4)
        rr(draw, (sx + 45, sy + 345, sx + sw - 45, sy + 555), "#171717", outline=GOLD, width=4)
        arrow(draw, (sx + sw // 2, sy + 260), (sx + sw // 2, sy + 335), WHITE, 6)
        draw.text((sx + 80, sy + 135), "PROVOCATION", fill=RED, font=F["body_bold"])
        draw.text((sx + 80, sy + 410), "REFRAME", fill=GOLD, font=F["hero"])
    draw_wrapped(draw, (x + 34, y + 705), spec.title, WHITE, F["card"], w - 68)
    draw_wrapped(draw, (x + 34, y + 765), spec.promise, MUTED, F["body"], w - 68)
    footer(draw, x, y, w, h, spec)


def rrc_layout(draw, x, y, w, h, spec: Comp):
    top_meta(draw, x, y, w, spec)
    sx, sy = x + 28, y + 122
    sw, sh = w - 56, 540
    rr(draw, (sx, sy, sx + sw, sy + sh), "#070707", outline="#303030", radius=8)
    split = sy + sh // 2
    draw.rectangle((sx, sy, sx + sw, split), fill="#101010")
    draw.rectangle((sx, split, sx + sw, sy + sh), fill="#0a0a0a")
    line(draw, (sx, split), (sx + sw, split), GOLD, 5)
    if spec.layout == "vs":
        rr(draw, (sx + 45, sy + 70, sx + sw // 2 - 20, split - 55), "#161616", outline=BLUE, width=5)
        rr(draw, (sx + sw // 2 + 20, sy + 70, sx + sw - 45, split - 55), "#161616", outline=RED, width=5)
        draw.text((sx + sw // 2 - 42, sy + 182), "VS", fill=WHITE, font=F["hero"])
        avatar(draw, sx + 185, split + 215, .72, BLUE, "interviewer")
        avatar(draw, sx + 390, split + 215, .78, GOLD)
    elif spec.layout == "tier":
        for i, lab in enumerate(["S", "A", "B", "C"]):
            color = [GOLD, BLUE, "#777777", RED][i]
            rr(draw, (sx + 50, sy + 55 + i * 62, sx + sw - 50, sy + 105 + i * 62), "#171717", outline=color, width=3)
            draw.text((sx + 72, sy + 66 + i * 62), lab, fill=color, font=F["body_bold"])
        avatar(draw, sx + sw // 2, split + 218, .82, GOLD)
    elif spec.layout == "blind-rank":
        for i in range(5):
            rr(draw, (sx + 75 + i * 82, sy + 72, sx + 135 + i * 82, sy + 240), "#171717", outline=GOLD if i == 2 else "#666666", width=3)
            draw.text((sx + 95 + i * 82, sy + 138), str(i + 1), fill=WHITE, font=F["body_bold"])
        avatar(draw, sx + 180, split + 215, .7, BLUE, "interviewer")
        avatar(draw, sx + 390, split + 215, .77, GOLD)
    elif spec.layout == "mirror":
        rr(draw, (sx + 45, sy + 70, sx + sw - 45, split - 50), "#171717", outline=GOLD, width=5)
        draw.text((sx + 82, sy + 110), "MIRROR QUIZ", fill=GOLD, font=F["hero"])
        for i in range(3):
            rr(draw, (sx + 75 + i * 130, sy + 210, sx + 175 + i * 130, sy + 270), "#000000", outline="#666666")
        avatar(draw, sx + sw // 2, split + 220, .82, GOLD)
    elif spec.layout == "elimination":
        for i in range(4):
            rr(draw, (sx + 58 + (i % 2) * 250, sy + 58 + (i // 2) * 115, sx + 225 + (i % 2) * 250, sy + 125 + (i // 2) * 115), "#171717", outline=RED if i == 1 else GOLD)
        draw.text((sx + sw // 2 - 45, sy + 210), "WIN?", fill=WHITE, font=F["hero"])
        avatar(draw, sx + 170, split + 215, .7, BLUE, "interviewer")
        avatar(draw, sx + 405, split + 215, .76, GOLD)
    else:
        rr(draw, (sx + 55, sy + 90, sx + sw - 55, split - 65), "#171717", outline=GOLD, width=4)
        draw_wrapped(draw, (sx + 82, sy + 125), "quote highlight + emotional pause", WHITE, F["body_bold"], sw - 164)
        avatar(draw, sx + 150, split + 215, .6, BLUE, "interviewer")
        avatar(draw, sx + 310, split + 215, .74, GOLD)
        rr(draw, (sx + 390, split + 105, sx + sw - 48, split + 225), "#161616", outline="#555555")
        draw.text((sx + 410, split + 142), "room\nrecognizes", fill=GOLD, font=F["body_bold"], spacing=2)
    draw.text((sx + 42, sy + 18), "UPPER: reaction UI / prompt / poll / proof", fill=MUTED, font=F["tiny"])
    draw.text((sx + 42, split + 18), "LOWER: cutout upper bodies + scene background", fill=MUTED, font=F["tiny"])
    draw_wrapped(draw, (x + 34, y + 705), spec.title, WHITE, F["card"], w - 68)
    draw_wrapped(draw, (x + 34, y + 765), spec.promise, MUTED, F["body"], w - 68)
    footer(draw, x, y, w, h, spec)


BOARDS = [
    (
        "01_CINEMATIC_STORY_COMMENTARY",
        "SV-CSC - Cinematic Story Commentary",
        "Make them feel the story: transformation, witness, backstory, worst-case moment.",
        story_layout,
        [
            Comp(1, "SV-CSC", "Witness Close-Up", "Cinematic Story", "Guest face and emotional subtitle carry the clip.", "scene_bg, guest_closeup, subtitle_track, memory_broll, eval_badges", "closeup"),
            Comp(2, "SV-CSC", "Memory Object Split", "Cinematic Story", "A symbolic object links the story to a lived memory.", "object_panel, guest_panel, quote_overlay, source_receipt, audio_wave", "object-split"),
            Comp(3, "SV-CSC", "Worst-Case Story Arc", "Cinematic Story", "Before, rupture, after: narrative state induction made visible.", "arc_beats, broll_slots, emotional_caption, score_strip", "story-arc"),
            Comp(4, "SV-CSC", "Scene Reconstruction", "Cinematic Story", "A remembered place becomes the visual anchor.", "scene_panels, subject_cutout, atmosphere, subtitle_track", "scene"),
            Comp(5, "SV-CSC", "Interview Lens", "Cinematic Story", "Question and answer remain visible as the origin of the clip.", "question_card, guest_cutout, interviewer_cutout, response_caption", "interview-lens"),
            Comp(6, "SV-CSC", "Evidence To Emotion", "Cinematic Story", "Source receipt, emotional beat, primitive distillation.", "source_card, emotion_card, primitive_card, guest_marker", "evidence"),
        ],
    ),
    (
        "02_EDUCATIONAL_PAPERCUT_EXPLAINER",
        "SV-EDU - Educational / Explainer",
        "Make them understand the idea: PaperCut, avatar explainer, diagrams, frameworks.",
        edu_layout,
        [
            Comp(7, "SV-EDU", "PaperCut Concept Stage", "PaperCut Explainer", "Layered paper scene with avatar pose and diagram.", "paper_layers, avatar_pose_01_64, diagram_nodes, caption_track", "papercut-stage", GOLD),
            Comp(8, "SV-EDU", "River Metaphor Board", "PaperCut Explainer", "Concept visualized as river, bank, and flow.", "metaphor_scene, arrow_path, concept_labels, motion_layers", "river", GOLD),
            Comp(9, "SV-EDU", "Framework Blackboard", "Animated Avatar", "Three-step reasoning stack for guest expertise.", "step_cards, avatar_pointer, subtitle_track, eval_badges", "framework", GOLD),
            Comp(10, "SV-EDU", "Process Timeline", "Animated Avatar", "Research to edge to brief to extraction.", "timeline_nodes, avatar_pose, transition_arrows, source_tags", "timeline", GOLD),
            Comp(11, "SV-EDU", "Contrastive Teaching", "PaperCut Explainer", "Surface answer against deeper context premise.", "surface_panel, premise_panel, correction_arrow, captions", "contrast", GOLD),
            Comp(12, "SV-EDU", "Question Engine", "Animated Avatar", "Educational clip keeps interview brief logic visible.", "question_card, concept_graph, avatar_rig, primitive_badges", "question-engine", GOLD),
        ],
    ),
    (
        "03_CHALLENGER_FRAME_BREAKER",
        "SV-FRB - Challenger / Frame Breaker",
        "Make them question the frame: provocation, contradiction, proof, reframe.",
        frb_layout,
        [
            Comp(13, "SV-FRB", "Myth Vs Reality", "Frame Breaker", "Directly breaks a false audience premise.", "myth_panel, reality_panel, receipt_link, verdict_caption", "myth-reality", RED),
            Comp(14, "SV-FRB", "Verdict Slash", "Frame Breaker", "A wrong frame is visibly crossed out.", "false_frame, slash_layer, new_frame, guest_reaction", "verdict", RED),
            Comp(15, "SV-FRB", "Evidence Wall", "Frame Breaker", "Pinned receipts build authority before the punchline.", "receipt_cards, red_threads, quote_pin, score_strip", "evidence-wall", RED),
            Comp(16, "SV-FRB", "Contradiction Heatmap", "Frame Breaker", "Matrix of Edging rendered as visual tension.", "edge_matrix, contradiction_cells, heat_score, caption_track", "heatmap", RED),
            Comp(17, "SV-FRB", "Authority Receipts", "Personal Brand Commentary", "Guest claim backed by quote, clip, and source.", "guest_cutout, quote_receipt, clip_receipt, source_receipt", "receipts", RED),
            Comp(18, "SV-FRB", "Provocation To Reframe", "Conscious Reactions", "The clip starts sharp but lands with a clearer frame.", "provocation_card, reframe_card, transition_arrow, CTA_prompt", "provocation", RED),
        ],
    ),
    (
        "04_REACTION_RECOGNITION_CLIPS",
        "SV-RRC - Reaction / Recognition Clip",
        "Make them trust or participate: living reactions, polls, duels, recognition moments.",
        rrc_layout,
        [
            Comp(19, "SV-RRC", "Living Reaction Split", "Living Commentary", "Upper reaction UI, lower guest and interviewer cutouts.", "reaction_ui, prompt_card, guest_cutout, interviewer_cutout, caption_track", "vs", BLUE),
            Comp(20, "SV-RRC", "Tier List Reaction", "Conscious Reactions", "Ranking UI reacts to what the guest just said.", "tier_ui, guest_cutout, reaction_caption, result_badge", "tier", BLUE),
            Comp(21, "SV-RRC", "Blind Ranking Clip", "Conscious Reactions", "Guest answers while ranking slots remain suspenseful.", "rank_slots, duo_cutouts, reveal_state, timer_layer", "blind-rank", BLUE),
            Comp(22, "SV-RRC", "Mirror Quiz", "Conscious Reactions", "Audience recognizes themselves through the guest answer.", "quiz_card, choice_buttons, guest_cutout, recognition_caption", "mirror", BLUE),
            Comp(23, "SV-RRC", "Elimination Duel", "Conscious Reactions", "Two ideas compete while the live reaction decides.", "bracket_ui, interviewer_cutout, guest_cutout, verdict_badge", "elimination", BLUE),
            Comp(24, "SV-RRC", "Recognition Pause", "Living Commentary", "A soft human-proof moment after something lands.", "quote_highlight, pause_marker, room_reaction, emotional_caption", "recognition", BLUE),
        ],
    ),
]


def make_board(slug, title, subtitle, renderer, comps):
    W, H = 1900, 2300
    card_w, card_h = 560, 980
    margin_x, gap_x = 80, 50
    top = 210
    gap_y = 60
    img = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    draw.text((margin_x, 55), title, fill=WHITE, font=F["board"])
    draw.text((margin_x, 123), subtitle, fill=MUTED, font=F["sub"])
    draw.text((margin_x, 160), "24 visual composition approval set - JSON-minded zones before renderer build", fill=GOLD, font=F["body_bold"])
    chip(draw, W - 520, 68, "CONSCIOUS ELITE", GOLD)
    chip(draw, W - 520, 112, "CMF STUDIO", WHITE)

    for idx, comp in enumerate(comps):
        col = idx % 3
        row = idx // 3
        x = margin_x + col * (card_w + gap_x)
        y = top + row * (card_h + gap_y)
        rr(draw, (x, y, x + card_w, y + card_h), "#050505", outline="#363636", width=3, radius=8)
        renderer(draw, x, y, card_w, card_h, comp)

    footer_text = "Approval meaning: choose visual grammar, not final copy. Each selected layout becomes a composition JSON template, render route, eval target, and operator review card."
    draw_wrapped(draw, (margin_x, H - 82), footer_text, MUTED, F["body"], W - 2 * margin_x)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"CMF_24_COMPOSITIONS_BOARD_{slug}.png"
    img.save(path)
    return path


def main():
    paths = []
    for board in BOARDS:
        paths.append(make_board(*board))
    index = OUT / "README.md"
    lines = [
        "# CMF Studio - 24 Visual Composition Approval Boards",
        "",
        "These boards show the visual grammar for the four canonical CMF video slots before JSON template and renderer implementation.",
        "",
    ]
    for path in paths:
        lines.append(f"- {path.name}")
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
