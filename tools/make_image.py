#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026.

Everything is drawn programmatically with Pillow: no photos, no external
assets, no downloaded images. Run from the repository root:

    python3 tools/make_image.py

Writes assets/entry.png (1024x1024, under 1 MiB).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 46)
RED = (176, 42, 48)
BLUE = (31, 78, 121)
GOLD = (201, 162, 39)
GREY = (90, 90, 100)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_usa(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    for i in range(13):
        if i % 2 == 0:
            draw.rectangle([x, y + i * h / 13, x + w, y + (i + 1) * h / 13],
                           fill=(178, 34, 52))
    draw.rectangle([x, y, x + w * 0.4, y + h * 7 / 13], fill=(60, 59, 110))
    for r in range(5):
        for c in range(6):
            sx = x + 12 + c * (w * 0.4 - 20) / 5
            sy = y + 10 + r * (h * 7 / 13 - 18) / 4
            star(draw, sx, sy, 4, WHITE)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=2)
    star(draw, x + w * 0.22, y + h * 0.28, 16, (255, 222, 0))
    for sx, sy in [(0.52, 0.12), (0.64, 0.26), (0.64, 0.48), (0.52, 0.62)]:
        star(draw, x + w * sx, y + h * sy, 6, (255, 222, 0))


def flag_russia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 8], fill=RED)
    draw_centered(d, W // 2, 26, "THE WORLD IN ONE PAGE",
                  font(SERIF, 64), INK)
    # short side rules, clear of the date text
    d.line([48, 122, 220, 122], fill=INK, width=2)
    d.line([804, 122, 976, 122], fill=INK, width=2)
    draw_centered(d, W // 2, 106, "FRIDAY  \u2022  20 NOVEMBER 2026",
                  font(SANS_BOLD, 32), RED)
    d.line([48, 152, 976, 152], fill=INK, width=3)

    # ---- main story ----------------------------------------------------
    # panel 168..580
    d.rectangle([48, 168, 976, 580], outline=INK, width=3)
    d.rectangle([48, 168, 976, 208], fill=INK)
    draw_centered(d, W // 2, 176, "SHENZHEN  \u2014  FIRST-EVER TRILATERAL SUMMIT",
                  font(SANS_BOLD, 24), WHITE)

    # three flags, staggered, with clear labels below each
    flag_usa(d, 84, 232, 180, 118)
    d.text((88, 356), "USA", font=font(SANS_BOLD, 20), fill=GREY)
    flag_china(d, 84, 384, 180, 118)
    d.text((88, 508), "CHINA", font=font(SANS_BOLD, 20), fill=GREY)
    flag_russia(d, 292, 308, 180, 118)
    d.text((296, 432), "RUSSIA", font=font(SANS_BOLD, 20), fill=GREY)

    # headline + body on the right
    tx, tw = 510, 440
    y = 232
    for line in wrap(d, "THREE LEADERS SIGN A \u2018PEACE DECLARATION\u2019",
                     font(SERIF, 42), tw):
        d.text((tx, y), line, font=font(SERIF, 42), fill=INK)
        y += 50
    y += 6
    d.line([tx, y, tx + 120, y], fill=RED, width=5)
    y += 18
    body = ("Trump, Putin and Xi agree a four-point pact: UN reform, more "
            "oil, curbs on the ICC, and a pledge that nuclear war "
            "\u201cmust never be fought\u201d. Ukraine and Iran not mentioned.")
    for line in wrap(d, body, font(SANS, 23), tw):
        d.text((tx, y), line, font=font(SANS, 23), fill=INK)
        y += 30

    # ---- three smaller stories -----------------------------------------
    # panels 596..884 (288 tall); illustration lives in a fixed bottom band
    panels = [
        ("BRUSSELS", "100,000 A YEAR",
         "UK and EU agree a youth mobility scheme \u2014 100,000 places a "
         "year, each way."),
        ("TAIPEI", "MARKETS PLUNGE 6.2%",
         "Taiwan stocks cap their worst week since 1991; TSMC falls below "
         "NT$2,000."),
        ("KYIV", "MISSILES HIT KYIV",
         "Ballistic strikes hit bridges in the capital; two embassies "
         "damaged."),
    ]
    px, py, pw, ph = 48, 596, 296, 288
    gap = 20
    for i, (kicker, head, body) in enumerate(panels):
        x = px + i * (pw + gap)
        d.rectangle([x, py, x + pw, py + ph], outline=INK, width=3)
        d.rectangle([x, py, x + pw, py + 40], fill=BLUE)
        draw_centered(d, x + pw // 2, py + 8, kicker, font(SANS_BOLD, 22), WHITE)
        y = py + 54
        for line in wrap(d, head, font(SERIF, 32), pw - 24):
            draw_centered(d, x + pw // 2, y, line, font(SERIF, 32), RED)
            y += 38
        y += 4
        d.line([x + 40, y, x + pw - 40, y], fill=GOLD, width=3)
        y += 12
        for line in wrap(d, body, font(SANS, 20), pw - 28):
            d.text((x + 14, y), line, font=font(SANS, 20), fill=INK)
            y += 26

    # illustrations in the bottom band (y 840..876), clear of all text
    # Brussels: circle of stars
    x0 = px
    cx, cy = x0 + pw // 2, py + ph - 22
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline=GOLD, width=3)
    for k in range(8):
        ang = -math.pi / 2 + k * math.pi / 4
        star(d, cx + 14 * math.cos(ang), cy + 14 * math.sin(ang), 3.5, GOLD)
    # Taipei: falling chart
    x1 = px + pw + gap
    pts = [(x1 + 30, py + ph - 44), (x1 + 80, py + ph - 38),
           (x1 + 130, py + ph - 42), (x1 + 185, py + ph - 28),
           (x1 + 235, py + ph - 32), (x1 + 266, py + ph - 20)]
    d.line(pts, fill=RED, width=4, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 12, pts[-1][1] - 2),
               (pts[-1][0] - 3, pts[-1][1] + 12)], fill=RED)
    # Kyiv: skyline with a small blast above it
    x2 = px + 2 * (pw + gap)
    base = py + ph - 6
    for bx, bw, bh in [(x2 + 26, 32, 22), (x2 + 64, 26, 32), (x2 + 96, 38, 18),
                       (x2 + 140, 28, 28), (x2 + 174, 34, 20), (x2 + 214, 26, 26),
                       (x2 + 246, 24, 16)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=INK)
    star(d, x2 + pw // 2, py + ph - 44, 13, (255, 170, 0))
    star(d, x2 + pw // 2, py + ph - 44, 6, (255, 220, 80))

    # ---- footer --------------------------------------------------------
    d.line([48, 908, 976, 908], fill=INK, width=3)
    draw_centered(d, W // 2, 924,
                  "Sources: Reuters  \u2022  BBC  \u2022  Bloomberg  \u2022  Fox News  \u2022  The Times",
                  font(SANS, 21), GREY)
    draw_centered(d, W // 2, 956,
                  "One day's news in one image  \u2014  make.fun  \u2022  news-image-20261120",
                  font(SANS_BOLD, 21), INK)

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets", "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
