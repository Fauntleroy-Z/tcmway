#!/usr/bin/env python3
"""
Generate TCM Way comic strip for Post #08: Cold Hands Warning.
4-panel comic: ice hands -> cancer environment -> feet test -> warm up plan.
Style: hand-drawn sketch feel, warm colors, Ollie the owl mascot.
No watermark. No Chinese text. No cropping.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

# -- Config -----------------------------------------------------------
OUT = "C:/Users/Administrator/tcmway-blog/images"
FONT_PATHS = [
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/calibri.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/msyh.ttc",
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

def winpath(fname):
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
    bx, by = cx - int(50*s), cy - int(30*s)
    bw, bh = int(100*s), int(90*s)
    draw.ellipse([bx, by, bx+bw, by+bh], fill=(160, 120, 60), outline=LINE_COLOR, width=1)
    draw.arc([bx-int(10*s), by+int(10*s), bx+int(60*s), by+int(80*s)],
              30, 200, fill=(120, 90, 40), width=int(2*s))
    draw.arc([cx+int(10*s), by+int(10*s), cx+int(60*s), by+int(80*s)],
              340, 160, fill=(120, 90, 40), width=int(2*s))
    for ex in [cx-int(18*s), cx+int(18*s)]:
        ey = cy - int(5*s)
        draw.ellipse([ex-int(12*s), ey-int(12*s), ex+int(12*s), ey+int(12*s)],
                     fill=(80, 160, 60), outline=LINE_COLOR, width=1)
        draw.ellipse([ex-int(4*s), ey-int(4*s), ex+int(4*s), ey+int(4*s)],
                     fill=(255, 255, 255))
    draw.polygon([
        (cx, cy+int(15*s)),
        (cx-int(10*s), cy+int(8*s)),
        (cx+int(10*s), cy+int(8*s)),
    ], fill=SOFT_ORANGE, outline=LINE_COLOR)
    px, py = cx, cy + int(35*s)
    r = int(8*s)
    draw.ellipse([px-r, py-r, px+r, py+r], fill=(30, 30, 30), outline=LINE_COLOR, width=1)
    draw.chord([px-r, py-r, px+r, py+r], 180, 360, fill=(220, 220, 220), outline=LINE_COLOR)
    draw.ellipse([px-int(2.5*s), py-int(9*s), px+int(2.5*s), py-int(4*s)], fill=(30, 30, 30))
    draw.ellipse([px-int(2.5*s), py+int(4*s), px+int(2.5*s), py+int(9*s)], fill=(220, 220, 220))
    draw.polygon([(cx-int(40*s), cy-int(25*s)), (cx-int(55*s), cy-int(65*s)), (cx-int(25*s), cy-int(40*s))],
                 fill=(140, 100, 50), outline=LINE_COLOR, width=1)
    draw.polygon([(cx+int(40*s), cy-int(25*s)), (cx+int(55*s), cy-int(65*s)), (cx+int(25*s), cy-int(40*s))],
                 fill=(140, 100, 50), outline=LINE_COLOR, width=1)

def draw_panel(draw, x, y, w, h, title, text_lines, ollie_pos=None, scene_fn=None):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=PANEL_BG, outline=LINE_COLOR, width=1)
    draw.rounded_rectangle([x+4, y+4, x+w-4, y+32], radius=8, fill=(240, 235, 225))
    try:
        f_title = get_font(15)
        draw.text((x+12, y+8), title, fill=OLIVE, font=f_title)
    except Exception:
        pass
    tx = x + MARGIN
    ty = y + 42
    f_text = get_font(13)
    for i, tl in enumerate(text_lines[:8]):
        if tl:
            draw.text((tx, ty + i * 20), tl, fill=(50, 45, 40), font=f_text)
    if ollie_pos:
        ox, oy = ollie_pos
        draw_ollie(draw, x + ox, y + oy, scale=0.55)
    if scene_fn:
        scene_fn(draw, x, y, w, h)

# -- Scene: Ice Hands / Check Engine Light ----------------------------
def scene_ice_hands(draw, x, y, w, h):
    cx = x + w//2
    # Person with ice hands
    draw.ellipse([cx-15, y+90, cx+15, y+120], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    draw.line([(cx, y+120), (cx, y+180)], fill=LINE_COLOR, width=3)
    # Arms out with "ice"
    draw.line([(cx, y+140), (cx-70, y+155)], fill=LINE_COLOR, width=3)
    draw.line([(cx, y+140), (cx+70, y+155)], fill=LINE_COLOR, width=3)
    # Ice blocks on hands
    for hx in [cx-70, cx+55]:
        draw.rectangle([hx-12, y+140, hx+12, y+165], fill=(180, 220, 255), outline=(100, 160, 220), width=2)
        draw.text((hx-18, y+168), "ICE", fill=(100, 140, 200), font=get_font(10))
    # Shiver lines
    for sx in [cx-50, cx-30, cx-10, cx+10, cx+30, cx+50]:
        draw.arc([sx-8, y+165, sx+8, y+185], 0, 180, fill=(150, 180, 210), width=1)
    # Check engine light
    draw.ellipse([cx-25, y+195, cx+25, y+245], fill=(255, 200, 60), outline=(200, 150, 20), width=3)
    draw.text((cx-22, y+210), "CHECK", fill=(180, 50, 40), font=get_font(10))
    draw.text((cx-22, y+224), "ENGINE", fill=(180, 50, 40), font=get_font(10))
    draw.text((x+20, y+260), "Not just 'poor circulation'", fill=BROWN, font=get_font(11))

# -- Scene: Cancer Environment Diagram --------------------------------
def scene_cancer_env(draw, x, y, w, h):
    tx = x + 28
    ty = y + 80
    f_s = get_font(13)
    # Equation
    draw.text((tx, ty), "Cancer environment =", fill=(180, 50, 40), font=get_font(14))
    draw.text((tx, ty+30), "  Yin Shi (cold stagnant fluid)", fill=(50, 45, 40), font=f_s)
    draw.text((tx, ty+55), "  +  Yang Bu Zu (no fire)", fill=(50, 45, 40), font=f_s)
    draw.text((tx, ty+80), "  +  Excess nutrition", fill=(50, 45, 40), font=f_s)

    # Visual: container with ice + fire out
    cx = x + w - 100
    cy = y + 170
    # Container
    draw.rectangle([cx-40, cy-10, cx+40, cy+60], outline=LINE_COLOR, width=2)
    # Ice cubes inside
    for ix, iy in [(cx-20, cy+5), (cx+5, cy+15), (cx-10, cy+30)]:
        draw.rectangle([ix-8, iy-8, ix+8, iy+8], fill=(180, 220, 255), outline=(100, 160, 220), width=1)
    # Fire (out/extinguished)
    draw.arc([cx-12, cy-5, cx+12, cy+15], 180, 360, fill=(200, 200, 200), width=1)
    # X over the fire
    draw.line([(cx-15, cy-10), (cx+15, cy+5)], fill=(180, 50, 40), width=2)
    draw.line([(cx+15, cy-10), (cx-15, cy+5)], fill=(180, 50, 40), width=2)
    # Label
    draw.text((cx-40, cy+65), "Yang FIRE = gone", fill=(180, 50, 40), font=get_font(11))

# -- Scene: Feet Test -------------------------------------------------
def scene_feet_test(draw, x, y, w, h):
    cx = x + w//2
    # Bed scene
    draw.rectangle([x+40, y+120, x+w-40, y+155], fill=(200, 185, 160), outline=LINE_COLOR, width=2)
    # Person in bed
    draw.ellipse([cx-18, y+80, cx+18, y+115], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    # Blanket
    draw.rectangle([x+40, y+115, x+w-40, y+125], fill=(220, 200, 180), outline=LINE_COLOR, width=1)
    # Feet poking out
    # Left foot: blue/cold
    draw.ellipse([x+50, y+145, x+110, y+170], fill=(160, 200, 240), outline=(100, 160, 220), width=2)
    draw.text((x+55, y+175), "COLD", fill=(100, 140, 200), font=get_font(11))
    # Right foot: warm/red
    draw.ellipse([x+370, y+145, x+430, y+170], fill=(240, 180, 160), outline=(200, 140, 100), width=2)
    draw.text((x+365, y+175), "WARM", fill=(200, 100, 60), font=get_font(11))
    # Checkmark on warm
    draw.ellipse([x+390, y+190, x+410, y+210], fill=GREEN)
    draw.line([(x+396, y+200), (x+399, y+205)], fill=(255,255,255), width=2)
    draw.line([(x+399, y+205), (x+405, y+195)], fill=(255,255,255), width=2)
    # Title
    draw.text((x+80, y+55), "Before bed: touch your feet.", fill=OLIVE, font=get_font(14))

# -- Scene: Warm-Up Action Plan ---------------------------------------
def scene_warmup(draw, x, y, w, h):
    tx = x + 28
    ty = y + 75
    f_s = get_font(12)
    items = [
        ("1. Ginger tea (warming)", GREEN),
        ("2. Cooked food, not salads", GREEN),
        ("3. Foot soak 15 min", GREEN),
        ("4. Cut iced drinks", GREEN),
    ]
    for i, (txt, clr) in enumerate(items):
        draw.text((tx, ty + i*32), txt, fill=clr, font=f_s)
    # Cup of tea
    cx = x + w - 90
    cy = y + 200
    draw.rectangle([cx-20, cy, cx+20, cy+40], fill=(220, 230, 200), outline=LINE_COLOR, width=2)
    draw.ellipse([cx-18, cy-10, cx+18, cy+8], fill=(240, 250, 220), outline=LINE_COLOR, width=1)
    for sx in [cx-10, cx, cx+10]:
        draw.arc([sx-4, cy-25, sx+4, cy-12], 0, 180, fill=(200, 200, 200), width=1)
    draw.text((cx-30, cy+45), "Simple wins.", fill=GREEN, font=get_font(11))

# -- Comic: Cold Hands Warning ----------------------------------------
def make_comic_08():
    W = PANEL_W * 2 + 40
    H = PANEL_H * 2 + 40
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Panel 1: Ice Hands = Check Engine Light
    draw_panel(draw, 10, 10, PANEL_W, PANEL_H,
               "Panel 1: What Cold Hands Mean",
               ["", "Hands like ice. Feet like", "blocks. Doctor says:", '"Just poor circulation."', "That is your CHECK ENGINE light."],
               scene_fn=scene_ice_hands)

    # Panel 2: Cancer Environment
    draw_panel(draw, PANEL_W+30, 10, PANEL_W, PANEL_H,
               "Panel 2: The Cancer Connection",
               ["", "Cancer needs TWO things:", "cold stagnant fluid + nutrition.", "Cold hands = your body", "is the right environment."],
               ollie_pos=(PANEL_W//2, PANEL_H-110),
               scene_fn=scene_cancer_env)

    # Panel 3: The Feet Test
    draw_panel(draw, 10, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 3: The Simplest Test Ever",
               ["", "At night, before bed:", "touch your own feet.", "Warm? Good. Cold? Warning.", "Cancer patients: check daily!"],
               scene_fn=scene_feet_test)

    # Panel 4: What To Do
    draw_panel(draw, PANEL_W+30, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 4: Warm Yourself Up",
               ["", "No more iced coffee.", "No more raw salads.", "Ginger tea. Foot soaks.", "Warm feet = warm immune system."],
               scene_fn=scene_warmup)

    out = winpath("comic-08-cold-hands.png")
    img.save(out, "PNG")
    print(f"Saved: {out}")
    return out

if __name__ == "__main__":
    print("Generating comic #08 (Cold Hands Warning)...")
    make_comic_08()
    print("Done!")
