#!/usr/bin/env python3
"""
Generate TCM Way comics #07-#10 using PIL hand-drawn style.
Same quality standard as generate_comic_06.py — no AI artifacts.
"""
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

OUT = "C:/Users/Administrator/tcmway-blog/images"
FONT_PATHS = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/arial.ttf",
]
PANEL_W, PANEL_H = 480, 400
MARGIN = 20
BG_COLOR = (253, 245, 230)
OLIVE = (90, 100, 50)
GREEN = (80, 140, 60)
BROWN = (120, 80, 40)
SOFT_ORANGE = (210, 140, 60)
PANEL_BG = (255, 252, 245)
LINE_COLOR = (60, 50, 40)
RED_ACCENT = (180, 50, 40)
BLUE_ACCENT = (60, 100, 180)


def get_font(size):
    for fp in FONT_PATHS:
        try:
            return ImageFont.truetype(fp, size)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_ollie(draw, cx, cy, scale=1.0):
    """Draw Ollie owl mascot: brown body, green eyes, yin-yang pendant."""
    s = scale
    # Body
    bx, by = cx - int(50*s), cy - int(30*s)
    bw, bh = int(100*s), int(90*s)
    draw.ellipse([bx, by, bx+bw, by+bh], fill=(160, 120, 60), outline=LINE_COLOR, width=2)
    # Wings
    draw.arc([bx-int(10*s), by+int(10*s), bx+int(60*s), by+int(80*s)],
             30, 200, fill=(120, 90, 40), width=int(3*s))
    draw.arc([cx+int(10*s), by+int(10*s), cx+int(60*s), by+int(80*s)],
             340, 160, fill=(120, 90, 40), width=int(3*s))
    # Eyes
    for ex in [cx-int(18*s), cx+int(18*s)]:
        ey = cy - int(5*s)
        draw.ellipse([ex-int(12*s), ey-int(12*s), ex+int(12*s), ey+int(12*s)],
                     fill=(80, 160, 60), outline=LINE_COLOR, width=2)
        draw.ellipse([ex-int(4*s), ey-int(4*s), ex+int(4*s), ey+int(4*s)],
                     fill=(255, 255, 255))
    # Beak
    draw.polygon([
        (cx, cy+int(15*s)), (cx-int(10*s), cy+int(8*s)), (cx+int(10*s), cy+int(8*s))],
        fill=SOFT_ORANGE, outline=LINE_COLOR)
    # Yin-yang pendant
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
    """Draw one comic panel."""
    draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=PANEL_BG, outline=LINE_COLOR, width=2)
    # Title bar
    draw.rounded_rectangle([x+4, y+4, x+w-4, y+32], radius=8, fill=(235, 225, 210))
    f_title = get_font(15)
    draw.text((x+12, y+8), title, fill=OLIVE, font=f_title)
    # Text lines
    tx, ty = x + MARGIN, y + 42
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
    # Scene
    if scene_fn:
        scene_fn(draw, x, y, w, h)


# ── Scene functions for each comic ────────────────────────────────────

# Comic #07: Six Signs of Health
def scn_sleep(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 80
    draw.ellipse([cx-40, cy-60, cx+40, cy], fill=(240, 230, 210), outline=LINE_COLOR, width=2)
    draw.text((cx-15, cy-40), "Zzz", fill=(150, 150, 150), font=get_font(16))

def scn_thermometer(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 40
    draw.line([(cx, cy-90), (cx, cy+20)], fill=(200, 200, 200), width=8)
    draw.ellipse([cx-12, cy+20, cx+12, cy+44], fill=(255, 60, 60), outline=LINE_COLOR, width=2)
    draw.text((cx-60, cy-100), "98.6", fill=GREEN, font=get_font(14))

def scn_checkmarks(draw, x, y, w, h):
    items = [("Sleep", 40), ("Appetite", 100), ("Energy", 160), ("Mood", 220)]
    for label, yy in items:
        draw.text((x+30, y+h-yy+10), "✓", fill=GREEN, font=get_font(16))
        draw.text((x+60, y+h-yy+10), label, fill=OLIVE, font=get_font(13))


# Comic #08: Cold Hands Warning
def scn_cold_hands(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 90
    draw.ellipse([cx-30, cy-50, cx+30, cy-10], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    for dx in [-20, 20]:
        draw.ellipse([cx+dx-8, cy-5, cx+dx+8, cy+8], fill=(180, 210, 240), outline=(100, 140, 200), width=2)
    draw.text((cx-50, cy-70), "Cold!", fill=BLUE_ACCENT, font=get_font(14))

def scn_flow(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 70
    for i in range(5):
        draw.arc([cx-60+i*25, cy-30, cx-30+i*25, cy], 0, 180, fill=BLUE_ACCENT, width=2)
    draw.arrow = None  # placeholder

def scn_frozen_pipes(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 80
    for i in range(3):
        yy = cy + i*25
        draw.rectangle([cx-80, yy, cx+80, yy+15], fill=(180, 210, 240), outline=BLUE_ACCENT, width=2)
    draw.text((cx-30, cy-20), "FROZEN", fill=BLUE_ACCENT, font=get_font(14))


# Comic #09: Six-Layer Defense
def scn_castle(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 60
    # Castle walls
    for i in range(6):
        yy = cy + i*10
        draw.rectangle([cx-70, yy-5, cx+70, yy+5], fill=(220-20*i, 200-15*i, 170-10*i), outline=LINE_COLOR, width=1)
    draw.text((cx-35, cy-20), "6 LAYERS", fill=BROWN, font=get_font(13))

def scn_gates(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 90
    labels = ["TaiYang", "YangMing", "ShaoYang", "TaiYin", "ShaoYin", "JueYin"]
    for i, lbl in enumerate(labels):
        yy = cy + i*14
        draw.rectangle([cx-60, yy, cx+60, yy+10], fill=(240-30*i, 220-25*i, 180-15*i), outline=LINE_COLOR, width=1)
        draw.text((cx-55, yy-2), lbl, fill=(40, 35, 30), font=get_font(9))


# Comic #10: Stop Feeding What You Fight
def scn_warrior(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 80
    draw.ellipse([cx-18, cy-50, cx+18, cy-15], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    draw.line([(cx-40, cy-45), (cx, cy-30)], fill=LINE_COLOR, width=3)
    draw.line([(cx+40, cy-45), (cx, cy-30)], fill=LINE_COLOR, width=3)
    draw.text((cx+25, cy-60), "vs.", fill=RED_ACCENT, font=get_font(14))

def scn_bowl(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 80
    draw.ellipse([cx-40, cy-5, cx+40, cy+35], fill=(220, 230, 200), outline=LINE_COLOR, width=2)
    draw.text((cx-15, cy+5), "WARM", fill=GREEN, font=get_font(14))
    draw.text((cx-70, cy-30), "←", fill=RED_ACCENT, font=get_font(18))
    draw.text((cx+50, cy-30), "✗", fill=RED_ACCENT, font=get_font(16))
    draw.text((cx+60, cy-10), "× ice × sugar", fill=(150, 100, 80), font=get_font(11))


# ── Comic Builder ────────────────────────────────────────────────────
def make_comic(title, panels, filename):
    """Build a 2x2 comic from 4 panel definitions.
    Each panel: {'title': str, 'lines': [str], 'ollie': bool, 'scene': fn|None}
    """
    W = PANEL_W * 2 + 40
    H = PANEL_H * 2 + 40
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    positions = [
        (10, 10),
        (PANEL_W + 30, 10),
        (10, PANEL_H + 30),
        (PANEL_W + 30, PANEL_H + 30),
    ]

    for i, (px, py) in enumerate(positions):
        if i >= len(panels):
            break
        p = panels[i]
        ollie = (PANEL_W//2, PANEL_H-110) if p.get('ollie') else None
        draw_panel(draw, px, py, PANEL_W, PANEL_H,
                   p['title'], p['lines'],
                   ollie_pos=ollie,
                   scene_fn=p.get('scene'))

    out = os.path.join(OUT, filename)
    img.save(out, "PNG")
    sz = os.path.getsize(out)
    print(f"  Saved: {filename} ({W}x{H}, {sz/1024:.0f}K)")
    return out


# ── Comic Definitions ─────────────────────────────────────────────────
COMICS = {
    "07": {
        "title": "Six Signs of Health",
        "filename": "comic-07-six-signs.png",
        "panels": [
            {"title": "Panel 1: Sleep Through the Night",
             "lines": ["", "Can you sleep 7-8 hours", "without waking up at", "3 AM every night?"],
             "scene": scn_sleep},
            {"title": "Panel 2: Normal Body Temperature",
             "lines": ["", "Your hands and feet", "stay warm. No chills.", "No night sweats."],
             "ollie": True, "scene": scn_thermometer},
            {"title": "Panel 3: Good Appetite",
             "lines": ["", "You feel hungry at", "meal times. Food", "tastes good. No bloat."],
             "scene": scn_checkmarks},
            {"title": "Panel 4: Steady Energy",
             "lines": ["", "Energy rises in morning.", "Steady through the day.", "Wind down at night."],
             "ollie": True},
        ]
    },
    "08": {
        "title": "Cold Hands Warning",
        "filename": "comic-08-cold-hands.png",
        "panels": [
            {"title": "Panel 1: The Sign",
             "lines": ["", "Your hands are always", "cold. Even in summer.", "This is a signal."],
             "scene": scn_cold_hands},
            {"title": "Panel 2: What Cold Means",
             "lines": ["", "Cold hands = cold", "inside. Your body is", "pulling heat inward."],
             "ollie": True, "scene": scn_flow},
            {"title": "Panel 3: The Pipe Analogy",
             "lines": ["", "Think of your body", "as pipes. Cold =", "pipes freeze up."],
             "scene": scn_frozen_pipes},
            {"title": "Panel 4: Warm It Up",
             "lines": ["", "Ginger tea. Warm socks.", "Move your body.", "Small choices, big fix."],
             "ollie": True},
        ]
    },
    "09": {
        "title": "Six-Layer Defense System",
        "filename": "comic-09-six-layer-defense.png",
        "panels": [
            {"title": "Panel 1: The Castle",
             "lines": ["", "Your body is a castle.", "It has 6 walls of", "defense, not just one."],
             "scene": scn_castle},
            {"title": "Panel 2: The Six Gates",
             "lines": ["", "TaiYang, YangMing, ShaoYang", "TaiYin, ShaoYin, JueYin", "Each gate = one layer."],
             "scene": scn_gates},
            {"title": "Panel 3: How Disease Moves",
             "lines": ["", "Disease enters through", "the outer gate. If not", "stopped, moves inward."],
             "ollie": True},
            {"title": "Panel 4: Your Job",
             "lines": ["", "Stop it at the gate.", "Early action = shallow.", "Delay = deep invasion."],
             "ollie": True},
        ]
    },
    "10": {
        "title": "Stop Feeding What You Fight",
        "filename": "comic-10-stop-feeding.png",
        "panels": [
            {"title": "Panel 1: The Battle",
             "lines": ["", "Your body is fighting", "something. Are you", "helping or hurting?"],
             "scene": scn_warrior},
            {"title": "Panel 2: Stop Feeding It",
             "lines": ["", "Cold, sugar, dairy,", "fried food = fuel for", "the wrong fire."],
             "ollie": True},
            {"title": "Panel 3: What to Eat",
             "lines": ["", "Congee. Warm soup.", "Ginger. Cinnamon.", "Simple food heals."],
             "scene": scn_bowl},
            {"title": "Panel 4: Trust Your Body",
             "lines": ["", "Your body knows how", "to heal. Give it the", "right conditions."],
             "ollie": True},
        ]
    },
}


if __name__ == "__main__":
    for num, comic in COMICS.items():
        print(f"Generating comic #{num}: {comic['title']}...")
        make_comic(comic['title'], comic['panels'], comic['filename'])
    print("\nAll 4 comics generated!")
