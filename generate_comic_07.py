#!/usr/bin/env python3
"""
Generate TCM Way comic strip for Post #07: Six Signs of Health.
4-panel comic: body's signals vs. lab results.
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
    """Draw one comic panel with border, title bar, text, optional Ollie/scene."""
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
            # handle manual wrapping per line (max ~42 chars)
            if len(tl) > 40:
                import textwrap
                sublines = textwrap.wrap(tl, width=40)
                for j, sl in enumerate(sublines[:3]):
                    draw.text((tx, ty + (i+j) * 20), sl, fill=(50, 45, 40), font=f_text)
            else:
                draw.text((tx, ty + i * 20), tl, fill=(50, 45, 40), font=f_text)
        else:
            pass  # blank lines are spacing
    if ollie_pos:
        ox, oy = ollie_pos
        draw_ollie(draw, x + ox, y + oy, scale=0.55)
    if scene_fn:
        scene_fn(draw, x, y, w, h)

# -- Scene: Clinic / Doctor's Office ----------------------------------
def scene_clinic(draw, x, y, w, h):
    cx, cy = x + w//2, y + h - 100
    # Desk
    draw.rectangle([x+60, cy+30, x+w-60, cy+45], fill=(180, 150, 100), outline=LINE_COLOR, width=2)
    # Lab report paper
    draw.rectangle([x+80, cy-10, x+200, cy+30], fill=(255, 255, 255), outline=LINE_COLOR, width=2)
    draw.text((x+90, cy-2), "ALL NORMAL", fill=GREEN, font=get_font(13))
    draw.line([(x+90, cy+10), (x+190, cy+10)], fill=(200, 200, 200), width=1)
    draw.line([(x+90, cy+18), (x+160, cy+18)], fill=(200, 200, 200), width=1)
    # Cold feet (bottom area)
    draw.ellipse([cx+30, cy+20, cx+55, cy+50], fill=(160, 200, 240), outline=(100, 160, 220), width=2)
    draw.ellipse([cx+55, cy+15, cx+80, cy+48], fill=(160, 200, 240), outline=(100, 160, 220), width=2)
    draw.text((cx+35, cy+55), "ICE COLD", fill=(100, 140, 200), font=get_font(11))
    # Zzz label
    draw.text((x+260, cy-10), "waking at 3 AM", fill=BROWN, font=get_font(12))
    draw.text((x+260, cy+10), "every night...", fill=BROWN, font=get_font(12))
    # Arrow from lab to feet
    draw.line([(x+160, cy+20), (cx+30, cy+30)], fill=(200, 180, 160), width=1)

# -- Scene: 6 Health Signs Checklist ---------------------------------
def scene_checklist(draw, x, y, w, h):
    tx = x + 28
    ty = y + 110
    signs = [
        ("1. Sleep: fall asleep easily", (50, 45, 40)),
        ("2. Appetite: hungry at meals", (50, 45, 40)),
        ("3. Elimination: daily, easy", (50, 45, 40)),
        ("4. Thirst: normal, not excessive", (50, 45, 40)),
        ("5. Head cool, hands & feet WARM", (180, 50, 40)),  # highlighted
        ("6. Energy: wake refreshed", (50, 45, 40)),
    ]
    f_s = get_font(12)
    for i, (txt, clr) in enumerate(signs):
        draw.text((tx, ty + i*28), txt, fill=clr, font=f_s)
    # Red circle around #5
    draw.rounded_rectangle([x+25, y+195, x+330, y+223], radius=4, outline=(180, 50, 40), width=2)
    draw.text((x+335, y+198), "<-- KEY!", fill=(180, 50, 40), font=get_font(12))
    # Subtitle
    draw.text((x+28, y+80), "TCM says:", fill=OLIVE, font=get_font(14))
    draw.text((x+28, y+96), "Your body signals > lab numbers", fill=OLIVE, font=get_font(13))

# -- Scene: Split Screen (ignore vs observe) -------------------------
def scene_splitscreen(draw, x, y, w, h):
    # Divider line
    draw.line([(x+w//2, y+55), (x+w//2, y+h-30)], fill=(220, 210, 200), width=2)
    # Left side: IGNORE
    draw.text((x+60, y+70), "IGNORING signals:", fill=(170, 70, 50), font=get_font(14))
    # Person ignoring
    cx_l = x + w//4
    draw.ellipse([cx_l-15, y+120, cx_l+15, y+150], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    draw.line([(cx_l, y+150), (cx_l, y+200)], fill=LINE_COLOR, width=3)
    # Crossed arms
    draw.line([(cx_l-25, y+160), (cx_l+25, y+175)], fill=LINE_COLOR, width=2)
    draw.line([(cx_l+25, y+160), (cx_l-25, y+175)], fill=LINE_COLOR, width=2)
    draw.text((cx_l-60, y+210), "Still tired.", fill=(170, 70, 50), font=get_font(11))
    draw.text((cx_l-60, y+230), "Lab says fine?", fill=(170, 70, 50), font=get_font(11))

    # Right side: OBSERVE
    draw.text((x+w//2+40, y+70), "OBSERVING signals:", fill=(70, 130, 50), font=get_font(14))
    # Person observing
    cx_r = x + 3*w//4
    draw.ellipse([cx_r-15, y+120, cx_r+15, y+150], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    draw.line([(cx_r, y+150), (cx_r, y+200)], fill=LINE_COLOR, width=3)
    # Happy open arms
    draw.line([(cx_r, y+165), (cx_r-30, y+190)], fill=LINE_COLOR, width=2)
    draw.line([(cx_r, y+165), (cx_r+30, y+190)], fill=LINE_COLOR, width=2)
    # Checkmark
    draw.ellipse([cx_r-10, y+205, cx_r+10, y+225], fill=(70, 130, 50))
    draw.line([(cx_r-4, y+215), (cx_r-1, y+220)], fill=(255,255,255), width=2)
    draw.line([(cx_r-1, y+220), (cx_r+5, y+210)], fill=(255,255,255), width=2)
    draw.text((cx_r-55, y+235), "Noticed early!", fill=(70, 130, 50), font=get_font(11))

# -- Scene: 30-Second Self Check ------------------------------------
def scene_selfcheck(draw, x, y, w, h):
    tx = x + 30
    # Clock face
    cx_c = x + w - 80
    cy_c = y + 110
    draw.ellipse([cx_c-30, cy_c-30, cx_c+30, cy_c+30], fill=(255,255,255), outline=LINE_COLOR, width=2)
    draw.line([(cx_c, cy_c), (cx_c, cy_c-22)], fill=LINE_COLOR, width=2)
    draw.line([(cx_c, cy_c), (cx_c+16, cy_c)], fill=LINE_COLOR, width=1)
    draw.text((cx_c-25, cy_c-42), "30 sec", fill=OLIVE, font=get_font(12))

    steps = [
        "Daily Check (30 sec):",
        "",
        "1. Touch your feet at night",
        "   Warm? = Good!",
        "   Cold? = Warning sign",
        "",
        "2. How's your energy?",
        "   Refreshed? or dragging?",
    ]
    f_s = get_font(12)
    for i, s in enumerate(steps):
        clr = OLIVE if i == 0 else (50,45,40)
        draw.text((tx, y+75 + i*22), s, fill=clr, font=f_s)

    # Small Ollie
    draw_ollie(draw, x + w - 80, y + 200, scale=0.35)

# -- Comic: Six Signs of Health --------------------------------------
def make_comic_07():
    W = PANEL_W * 2 + 40
    H = PANEL_H * 2 + 40
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Panel 1: The Lab Results Lie
    draw_panel(draw, 10, 10, PANEL_W, PANEL_H,
               "Panel 1: Lab Says I'm Fine",
               ["", '"All normal!" the doctor says.', "But my feet are ice cold.", "And I wake up at 3 AM...", "Something is not right."],
               ollie_pos=(PANEL_W//2, PANEL_H-130),
               scene_fn=scene_clinic)

    # Panel 2: TCM's 6 Health Signs
    draw_panel(draw, PANEL_W+30, 10, PANEL_W, PANEL_H,
               "Panel 2: The 6 Health Signs",
               ["", "Western doctors check labs.", "TCM checks YOUR signals.", "Sleep. Appetite. Bowels. Thirst.", "Temperature. Energy."])

    # Panel 3: Ignore vs Observe
    draw_panel(draw, 10, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 3: Two Choices",
               ["", "You can ignore the signals...", "...or you can learn to read them.", "One path leads to chronic illness.", "The other leads to early warning."],
               scene_fn=scene_checklist)

    # Panel 4: The 30-Second Daily Check
    draw_panel(draw, PANEL_W+30, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 4: Your Daily Check",
               ["", "Your body talks. Every day.", "30 seconds. Before bed.", "Touch your feet. Are they warm?", "That one check = early detection."])

    out = winpath("comic-07-six-signs.png")
    img.save(out, "PNG")
    print(f"Saved: {out}")
    return out

if __name__ == "__main__":
    print("Generating comic #07 (Six Signs of Health)...")
    make_comic_07()
    print("Done!")
