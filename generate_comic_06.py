#!/usr/bin/env python3
"""
Generate TCM Way comic strips for Post #06: Spleen deficiency.
Two 4-panel comics: (1) Spleen fatigue, (2) Dampness.
Style: hand-drawn sketch feel, warm colors, Ollie the owl mascot.
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# ── Config ─────────────────────────────────────────────────────────────
# Use Windows-native paths (PIL on Windows can't open /c/... MSYS2 paths)
OUT = "C:/Users/Administrator/tcmway-blog/images"
FONT_PATHS = [
    "C:/Windows/Fonts/msyh.ttc",      # Microsoft YaHei
    "C:/Windows/Fonts/simsun.ttc",     # SimSun
    "C:/Windows/Fonts/arial.ttf",      # Arial fallback
]
PANEL_W, PANEL_H = 480, 400
MARGIN = 20
BG_COLOR = (253, 245, 230)        # warm cream
OLIVE = (90, 100, 50)
GREEN = (80, 140, 60)
BROWN = (120, 80, 40)
SOFT_ORANGE = (210, 140, 60)
PANEL_BG = (255, 252, 245)
LINE_COLOR = (60, 50, 40)

def winpath(fname):
    """Build a Windows-native absolute path for PIL."""
    return os.path.join(OUT, fname)

def get_font(size):
    for fp in FONT_PATHS:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            pass
    return ImageFont.load_default()

def draw_ollie(draw, cx, cy, scale=1.0):
    """Draw Ollie mascot: brown owl, green eyes, yin-yang pendant."""
    s = scale
    # Body (brown oval)
    bx, by = cx - int(50*s), cy - int(30*s)
    bw, bh = int(100*s), int(90*s)
    draw.ellipse([bx, by, bx+bw, by+bh], fill=(160, 120, 60), outline=LINE_COLOR, width=2)
    # Wing hints
    draw.arc([bx-int(10*s), by+int(10*s), bx+int(60*s), by+int(80*s)],
              30, 200, fill=(120, 90, 40), width=int(3*s))
    draw.arc([cx+int(10*s), by+int(10*s), cx+int(60*s), by+int(80*s)],
              340, 160, fill=(120, 90, 40), width=int(3*s))
    # Eyes (green, large circles with white dot)
    for ex in [cx-int(18*s), cx+int(18*s)]:
        ey = cy - int(5*s)
        draw.ellipse([ex-int(12*s), ey-int(12*s), ex+int(12*s), ey+int(12*s)],
                     fill=(80, 160, 60), outline=LINE_COLOR, width=2)
        draw.ellipse([ex-int(4*s), ey-int(4*s), ex+int(4*s), ey+int(4*s)],
                     fill=(255, 255, 255))
    # Beak (orange small triangle)
    draw.polygon([
        (cx, cy+int(15*s)),
        (cx-int(10*s), cy+int(8*s)),
        (cx+int(10*s), cy+int(8*s)),
    ], fill=SOFT_ORANGE, outline=LINE_COLOR)
    # Yin-yang pendant (small circle below beak)
    px, py = cx, cy + int(35*s)
    r = int(8*s)
    draw.ellipse([px-r, py-r, px+r, py+r], fill=(30, 30, 30), outline=LINE_COLOR, width=1)
    draw.chord([px-r, py-r, px+r, py+r], 180, 360, fill=(220, 220, 220), outline=LINE_COLOR)
    draw.ellipse([px-int(2.5*s), py-int(9*s), px+int(2.5*s), py-int(4*s)], fill=(30, 30, 30))
    draw.ellipse([px-int(2.5*s), py+int(4*s), px+int(2.5*s), py+int(9*s)], fill=(220, 220, 220))
    # Ear tufts
    draw.polygon([(cx-int(40*s), cy-int(25*s)), (cx-int(55*s), cy-int(65*s)), (cx-int(25*s), cy-int(40*s))],
                 fill=(140, 100, 50), outline=LINE_COLOR, width=2)
    draw.polygon([(cx+int(40*s), cy-int(25*s)), (cx+int(55*s), cy-int(65*s)), (cx+int(25*s), cy-int(40*s))],
                 fill=(140, 100, 50), outline=LINE_COLOR, width=2)

def draw_panel(draw, x, y, w, h, title, text_lines, ollie_pos=None, scene_fn=None):
    """Draw one comic panel with border, title bar, text, optional Ollie/scene."""
    # Background
    draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=PANEL_BG, outline=LINE_COLOR, width=2)
    # Title bar
    draw.rounded_rectangle([x+4, y+4, x+w-4, y+32], radius=8, fill=(235, 225, 210))
    try:
        f_title = get_font(15)
        draw.text((x+12, y+8), title, fill=OLIVE, font=f_title)
    except Exception:
        pass
    # Text area
    tx = x + MARGIN
    ty = y + 42
    f_text = get_font(13)
    wrapped = []
    for line in text_lines:
        if line:
            wrapped.extend(textwrap.wrap(line, width=42))
        else:
            wrapped.append("")
    for i, tl in enumerate(wrapped[:8]):
        draw.text((tx, ty + i * 20), tl, fill=(50, 45, 40), font=f_text)
    # Ollie
    if ollie_pos:
        ox, oy = ollie_pos
        draw_ollie(draw, x + ox, y + oy, scale=0.55)
    # Custom scene
    if scene_fn:
        scene_fn(draw, x, y, w, h)

def scene_desk(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 80
    # Desk
    draw.rectangle([x+30, cy+20, x+w-30, cy+35], fill=(180, 150, 100), outline=LINE_COLOR, width=2)
    # Person (stick)
    draw.ellipse([cx-15, cy-70, cx+15, cy-40], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    draw.line([(cx, cy-40), (cx, cy+10)], fill=LINE_COLOR, width=3)
    draw.line([(cx, cy-30), (cx-60, cy+15)], fill=LINE_COLOR, width=2)
    draw.line([(cx, cy-30), (cx+50, cy+15)], fill=LINE_COLOR, width=2)
    draw.line([(cx, cy+10), (cx-25, cy+40)], fill=LINE_COLOR, width=3)
    draw.line([(cx, cy+10), (cx+25, cy+40)], fill=LINE_COLOR, width=3)
    # Zzz
    draw.text((cx+20, cy-85), "z z z...", fill=(150, 150, 150), font=get_font(13))
    # Heavy arms note
    draw.text((x+45, cy-10), "lead arms", fill=BROWN, font=get_font(12))

def scene_factory(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 90
    # Factory building
    draw.rectangle([cx-70, cy-80, cx+70, cy+20], fill=(210, 200, 185), outline=LINE_COLOR, width=2)
    draw.polygon([(cx-80, cy-80), (cx, cy-120), (cx+80, cy-80)], fill=(180, 170, 155), outline=LINE_COLOR, width=2)
    # Chimney
    draw.rectangle([cx+30, cy-140, cx+50, cy-80], fill=(160, 150, 135), outline=LINE_COLOR, width=2)
    # Smoke (slow)
    draw.ellipse([cx+25, cy-160, cx+55, cy-145], outline=(200, 200, 200), width=1)
    draw.ellipse([cx+20, cy-180, cx+60, cy-162], outline=(210, 210, 210), width=1)
    draw.text((cx-60, cy-180), "zzz...", fill=(180, 180, 180), font=get_font(14))
    # Label
    draw.text((x+20, y+h-30), "Spleen factory: UNDERSTAFFED", fill=BROWN, font=get_font(12))

def scene_spoon(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 100
    # Hand
    draw.ellipse([cx-20, cy-10, cx+20, cy+20], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    # Spoon
    draw.rectangle([cx-3, cy-50, cx+3, cy], fill=(200, 200, 200), outline=LINE_COLOR, width=1)
    draw.ellipse([cx-12, cy-65, cx+12, cy-48], fill=(200, 200, 200), outline=LINE_COLOR, width=1)
    # Ice cream
    draw.ellipse([cx-10, cy-70, cx+10, cy-52], fill=(255, 220, 180), outline=(200, 160, 100), width=1)
    # Thought bubble
    draw.ellipse([cx+30, cy-90, cx+120, cy-55], outline=(180, 180, 180), width=1)
    draw.text((cx+38, cy-82), "sugar crash", fill=(180, 150, 100), font=get_font(12))
    draw.text((x+40, y+h-30), "Spoon hits the system", fill=BROWN, font=get_font(12))

def scene_damp(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 80
    # Body silhouette with drops
    draw.ellipse([cx-20, cy-60, cx+20, cy-30], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    draw.line([(cx, cy-30), (cx, cy+10)], fill=LINE_COLOR, width=3)
    # Rain drops
    for dx, dy in [(-30, -20), (-15, -45), (20, -30), (35, -55), (10, -60)]:
        draw.line([(cx+dx, cy+dy), (cx+dx+3, cy+dy+12)], fill=(100, 160, 220), width=2)
    # Puddle
    draw.ellipse([cx-40, cy+20, cx+40, cy+40], fill=(160, 200, 240), outline=(100, 160, 220), width=1)
    draw.text((x+20, y+h-30), "Dampness = internal wet clothes", fill=BROWN, font=get_font(12))

def scene_fix(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 90
    # Bowl of congee
    draw.ellipse([cx-40, cy, cx+40, cy+35], fill=(220, 230, 200), outline=LINE_COLOR, width=2)
    draw.ellipse([cx-35, cy-10, cx+35, cy+15], fill=(240, 250, 220), outline=LINE_COLOR, width=1)
    # Steam
    for sx in [cx-15, cx, cx+15]:
        draw.arc([sx-5, cy-30, sx+5, cy-15], 0, 180, fill=(200, 200, 200), width=1)
    # Checkmark
    draw.text((cx+50, cy-5), "OK!", fill=GREEN, font=get_font(16))
    draw.text((x+20, y+h-30), "Warm food = fuel, not friction", fill=GREEN, font=get_font(12))

def scene_radiator(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 120
    draw.rectangle([cx-40, cy, cx+40, cy+60], fill=(200, 200, 200), outline=LINE_COLOR, width=2)
    for i in range(3):
        draw.rectangle([cx+5, cy+10+i*15, cx+75, cy+20+i*15],
                       fill=(180, 220, 240), outline=(100, 160, 220), width=1)
    # Ice block
    draw.rectangle([cx-15, cy+15, cx, cy+45], fill=(180, 220, 255), outline=(100, 160, 220), width=1)
    draw.text((cx-25, cy+50), "ICE", fill=(100, 160, 220), font=get_font(11))

def scene_tea(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 110
    draw.rectangle([cx-20, cy, cx+20, cy+40], fill=(220, 230, 200), outline=LINE_COLOR, width=2)
    draw.ellipse([cx-18, cy-10, cx+18, cy+8], fill=(240, 250, 220), outline=LINE_COLOR, width=1)
    for sx in [cx-10, cx, cx+10]:
        draw.arc([sx-4, cy-25, sx+4, cy-12], 0, 180, fill=(200, 200, 200), width=1)
    draw.text((cx+35, cy-5), "Warm =", fill=GREEN, font=get_font(12))
    draw.text((cx+35, cy+15), "problem solved", fill=GREEN, font=get_font(12))


# ── Comic #1: Spleen Fatigue (4 panels) ──────────────────────────────
def make_comic_06_01():
    """Comic strip #1: 'You're not lazy, your Spleen is tired'."""
    W = PANEL_W * 2 + 40
    H = PANEL_H * 2 + 40
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Panel 1: The Label
    draw_panel(draw, 10, 10, PANEL_W, PANEL_H,
               "Panel 1: The Label",
               ["", "My arms feel like lead.", "Everyone says I'm lazy.", "Maybe they're right?"],
               ollie_pos=(PANEL_W//2, PANEL_H-100),
               scene_fn=scene_desk)

    # Panel 2: Spleen factory
    draw_panel(draw, PANEL_W+30, 10, PANEL_W, PANEL_H,
               "Panel 2: What's Actually Happening",
               ["", "Your Spleen is a factory.", "It's UNDERSTAFFED.", "No energy = no transport."],
               scene_fn=scene_factory)

    # Panel 3: Cold food damage
    draw_panel(draw, 10, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 3: The Real Cause",
               ["", "Iced latte for breakfast?", "Salad for lunch?", "That's your factory fuel."],
               ollie_pos=(PANEL_W//2, PANEL_H-110),
               scene_fn=scene_spoon)

    # Panel 4: The fix
    draw_panel(draw, PANEL_W+30, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 4: What to Do",
               ["", "Warm food. Rest after", "meals. Your Spleen", "isn't broken. Just tired."],
               scene_fn=scene_fix)

    out = winpath("comic-06-spleen.png")
    img.save(out, "PNG")
    print(f"Saved: {out}")
    return out


# ── Comic #2: Dampness (4 panels) ────────────────────────────────────
def make_comic_06_02():
    """Comic strip #2: Dampness explained."""
    W = PANEL_W * 2 + 40
    H = PANEL_H * 2 + 40
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Panel 1: Wet clothes feeling
    draw_panel(draw, 10, 10, PANEL_W, PANEL_H,
               "Panel 1: The Feeling",
               ["", "You feel heavy. Like", "you forgot to take", "off wet clothes."],
               scene_fn=scene_damp)

    # Panel 2: Ollie explains dampness
    draw_panel(draw, PANEL_W+30, 10, PANEL_W, PANEL_H,
               "Panel 2: Ollie Explains",
               ["", "Dampness = fluid that", "won't move.", "Spleen can't transport", "it out."],
               ollie_pos=(PANEL_W//2, PANEL_H-110))

    # Panel 3: What creates dampness
    draw_panel(draw, 10, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 3: The Causes",
               ["", "Cold food = ices up", "the radiator.", "Dairy + sugar =", "makes it worse."],
               scene_fn=scene_radiator)

    # Panel 4: The dry-off plan
    draw_panel(draw, PANEL_W+30, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 4: Dry Off",
               ["", "Cut the cold. Cut the", "sugar. Warm food,", "warm drinks."],
               scene_fn=scene_tea)

    out = winpath("comic-06-dampness.png")
    img.save(out, "PNG")
    print(f"Saved: {out}")
    return out


if __name__ == "__main__":
    print("Generating comic strip #1 (Spleen fatigue)...")
    make_comic_06_01()
    print("Generating comic strip #2 (Dampness)...")
    make_comic_06_02()
    print("Done! Both comic strips saved.")
