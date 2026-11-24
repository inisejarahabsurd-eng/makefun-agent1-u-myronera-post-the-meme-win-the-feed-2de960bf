#!/usr/bin/env python3
"""Render the make.fun meme image. Deterministic, offline, Pillow-only.

Output: 1080x1350 PNG (4:5, X-friendly, phone-legible), <=5MB.
"""
from __future__ import annotations

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from jokes import JOKES

W, H = 1080, 1350
BG_TOP = (13, 17, 23)
BG_BOT = (28, 34, 46)
ACCENT = (88, 214, 141)
ACCENT2 = (255, 202, 58)
TXT = (245, 245, 245)
SUB = (160, 168, 182)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/impact.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()  # bitmap fallback; renderer will shrink text


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text: str, max_w: int, max_lines: int, start: int, min_size: int = 56):
    size = start
    while size >= min_size:
        font = load_font(size)
        lines = wrap(draw, text, font, max_w)
        if len(lines) <= max_lines:
            return font, lines
        size -= 6
    font = load_font(min_size)
    return font, wrap(draw, text, font, max_w)


def draw_banner(draw, y: int, text: str, color: tuple, max_w: int, anchor: str) -> int:
    font, lines = fit_text(draw, text, max_w, 3, 88)
    line_h = int(font.size * 1.15)
    for ln in lines:
        draw.text((W // 2, y), ln, font=font, fill=color, anchor=anchor)
        y += line_h if anchor == "ma" else -line_h
    return y


def robot(draw, cx: int, cy: int, s: float = 1.0):
    """Draw the agent-bot graphic: rounded head, visor, antenna, smile, bounty badge."""
    hw, hh = int(200 * s), int(150 * s)
    # antenna
    draw.line([(cx, cy - hh), (cx, cy - hh - 60 * s)], fill=SUB, width=int(10 * s))
    pulse = [(cx, cy - hh - 85 * s), 28 * s]
    draw.ellipse([cx - pulse[1], pulse[0][1] - pulse[1], cx + pulse[1], pulse[0][1] + pulse[1]], fill=ACCENT2)
    # head
    draw.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh], radius=int(60 * s), fill=(38, 46, 62), outline=(70, 80, 100), width=int(6 * s))
    # visor
    vw, vh = int(150 * s), int(52 * s)
    draw.rounded_rectangle([cx - vw, cy - vh, cx + vw, cy + vh], radius=int(26 * s), fill=(10, 12, 16))
    # eyes
    ex = int(70 * s)
    ey_r = int(18 * s)
    draw.ellipse([cx - ex - ey_r, cy - ey_r, cx - ex + ey_r, cy + ey_r], fill=ACCENT)
    draw.ellipse([cx + ex - ey_r, cy - ey_r, cx + ex + ey_r, cy + ey_r], fill=ACCENT)
    # smile
    draw.arc([cx - 60 * s, cy + vh, cx + 60 * s, cy + vh + 70 * s], 20, 160, fill=TXT, width=int(8 * s))
    # badge: $ bounty chip
    bx, by = cx + hw + int(10 * s), cy - hh - int(10 * s)
    draw.rounded_rectangle([bx - 55 * s, by - 55 * s, bx + 55 * s, by + 55 * s], radius=int(20 * s), fill=ACCENT2)
    draw.text((bx, by - 6 * s), "$", font=load_font(int(56 * s)), fill=(20, 20, 20), anchor="mm")


def terminal(draw, x: int, y: int, w: int, h: int):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=(18, 22, 30), outline=(60, 70, 90), width=5)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        draw.ellipse([x + 24 + i * 40, y + 20, x + 48 + i * 40, y + 44], fill=c)
    rows = [
        ("$ agent enter --bounty make.fun", SUB),
        ("> compiling meme ........ OK", ACCENT),
        ("> leaderboard: #1  [you]", ACCENT2),
        ("> payout: crypto sent", ACCENT),
    ]
    f = load_font(34)
    for i, (t, c) in enumerate(rows):
        draw.text((x + 28, y + 70 + i * 52), t, font=f, fill=c)


def render(joke: str, out_path: str) -> str:
    if joke not in JOKES:
        raise SystemExit(f"unknown joke '{joke}'. choose one of: {', '.join(JOKES)}")
    top, bottom = JOKES[joke]["top"], JOKES[joke]["bottom"]

    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    # vertical gradient background
    for yy in range(H):
        t = yy / H
        d.line([(0, yy), (W, yy)], fill=tuple(int(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT)))

    pad = 60
    max_w = W - 2 * pad

    # top banner (measure height first by drawing on scratch)
    scratch = ImageDraw.Draw(Image.new("RGB", (W, H)))
    f, lines = fit_text(scratch, top, max_w, 3, 88)
    th = len(lines) * int(f.size * 1.15)
    draw_banner(d, pad, top, TXT, max_w, "ma")

    # bottom banner
    fb, blines = fit_text(scratch, bottom, max_w, 3, 88)
    bh = len(blines) * int(fb.size * 1.15)

    # middle graphic zone
    zone_top = pad + th + 40
    zone_bot = H - pad - bh - 40
    mid = (zone_top + zone_bot) // 2
    terminal(d, 90, mid - 60, W - 180, 260)
    robot(d, W // 2, mid + 320 if mid + 320 < zone_bot else mid + 140, s=1.0)

    # bottom banner, drawn upward from H - pad
    draw_banner(d, H - pad, bottom, TXT, max_w, "md")

    # watermark strip
    d.text((W // 2, H - 28), "made by an agent on make.fun", font=load_font(28), fill=SUB, anchor="md")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    img.save(out_path, "PNG", optimize=True)
    # size guard: X limit is 5MB
    if os.path.getsize(out_path) > 5 * 1024 * 1024:
        jpg = out_path.rsplit(".", 1)[0] + ".jpg"
        img.save(jpg, "JPEG", quality=88, optimize=True)
        os.remove(out_path)
        out_path = jpg
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate the make.fun meme image")
    ap.add_argument("--joke", default="grind", choices=sorted(JOKES), help="which copy to render")
    ap.add_argument("--out", default="out/meme.png", help="output path")
    a = ap.parse_args()
    path = render(a.joke, a.out)
    print(f"wrote {path} ({os.path.getsize(path)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())