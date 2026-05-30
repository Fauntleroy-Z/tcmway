#!/usr/bin/env python3
"""
Generate TCM Way comic strip for Post #09: Six-Layer Defense System.
4-panel comic: castle walls -> wrong approach -> 6-layer map -> healing in reverse.
Style: hand-drawn sketch feel, warm colors, Ollie the owl mascot.
No watermark. No Chinese text. No cropping.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

# -- Config -----------------------------------------------------------
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
    draw.ellipse([bx, by, bx+bw, by+bh], fill=(160, 120, 60), outline=LINE_COLOR, width=2)
    draw.arc([bx-int(10*s), by+int(10*s), bx+int(60*s), by+int(80*s)],
              30, 200, fill=(120, 90, 40), width=int(3*s))
    draw.arc([cx+int(10*s), by+int(10*s), cx+int(60*s), by+int(80*s)],
              340, 160, fill=(120, 90, 40), width=int(3*s))
    for ex in [cx-int(18*s), cx+int(18*s)]:
        ey = cy - int(5*s)
        draw.ellipse([ex-int(12*s), ey-int(12*s), ex+int(12*s), ey+int(12*s)],
                     fill=(80, 160, 60), outline=LINE_COLOR, width=2)
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
                 fill=(140, 100, 50), outline=LINE_COLOR, width=2)
    draw.polygon([(cx+int(40*s), cy-int(25*s)), (cx+int(55*s), cy-int(65*s)), (cx+int(25*s), cy-int(40*s))],
                 fill=(140, 100, 50), outline=LINE_COLOR, width=2)

def draw_panel(draw, x, y, w, h, title, text_lines, ollie_pos=None, scene_fn=None):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=PANEL_BG, outline=LINE_COLOR, width=2)
    draw.rounded_rectangle([x+4, y+4, x+w-4, y+32], radius=8, fill=(235, 225, 210))
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

# -- Scene: Castle with 6 walls ---------------------------------------
def scene_castle(draw, x, y, w, h):
    cx = x + w//2
    base_y = y + h - 30
    # Castle body
    wall_colors = [(180, 160, 140), (170, 155, 135), (160, 150, 130),
                   (150, 145, 125), (140, 140, 120), (130, 135, 115)]
    for i in range(6):
        wy = base_y - i*30 - 20
        wh = 28
        draw.rectangle([cx-80+i*8, wy, cx+80-i*8, wy+wh],
                       fill=wall_colors[i], outline=LINE_COLOR, width=1)
    # Castle tower
    draw.rectangle([cx-20, base_y-205, cx+20, base_y-180], fill=(140, 130, 115), outline=LINE_COLOR, width=2)
    draw.polygon([(cx-25, base_y-180), (cx, base_y-210), (cx+25, base_y-180)],
                 fill=(180, 60, 50), outline=LINE_COLOR, width=2)
    # Gate
    draw.arc([cx-15, base_y-30, cx+15, base_y+5], 180, 360, fill=LINE_COLOR, width=2)
    draw.rectangle([cx-15, base_y-12, cx+15, base_y+5], outline=LINE_COLOR, width=2)
    # Enemy at gate
    draw.ellipse([cx+90, base_y-60, cx+110, base_y-40], fill=(220, 100, 80), outline=LINE_COLOR, width=2)
    draw.line([(cx+100, base_y-40), (cx+100, base_y-15)], fill=LINE_COLOR, width=2)
    draw.text((cx+75, base_y-80), "Enemy at", fill=(180, 50, 40), font=get_font(10))
    draw.text((cx+75, base_y-68), "Gate 1!", fill=(180, 50, 40), font=get_font(10))
    # Arrow pointing to gate
    draw.line([(cx+90, base_y-30), (cx+30, base_y-15)], fill=(180, 50, 40), width=2)

# -- Scene: Wrong Medicine (cold pill goes down) ----------------------
def scene_wrong_meds(draw, x, y, w, h):
    cx = x + w//2
    # Person on surface
    draw.ellipse([cx-15, y+80, cx+15, y+110], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    # Fever lines
    for fx in [cx-20, cx-10, cx, cx+10, cx+20]:
        draw.arc([fx-6, y+65, fx+6, y+80], 0, 180, fill=(200, 80, 40), width=1)
    draw.text((cx+20, y+70), "FEVER", fill=(200, 80, 40), font=get_font(11))

    # Cold pill
    draw.ellipse([cx-8, y+120, cx+8, y+136], fill=(180, 220, 255), outline=(100, 160, 220), width=2)
    draw.text((cx-12, y+123), "C", fill=(100, 160, 220), font=get_font(9))
    draw.text((cx+15, y+140), "COLD medicine", fill=(100, 140, 200), font=get_font(10))

    # Arrow down through layers
    draw.line([(cx, y+140), (cx, y+280)], fill=(180, 50, 40), width=2)
    # Arrowhead
    draw.polygon([(cx, y+280), (cx-8, y+268), (cx+8, y+268)], fill=(180, 50, 40))

    # Layers being crossed
    for li, ly in enumerate([y+165, y+190, y+215]):
        draw.line([(cx-40, ly), (cx+40, ly)], fill=(200, 180, 160), width=1)
        draw.text((cx-120, ly-6), "Wall " + str(li+1), fill=BROWN, font=get_font(9))

    # Deep organs
    draw.text((cx-50, y+285), "Driven deep into", fill=(180, 50, 40), font=get_font(11))
    draw.text((cx-50, y+305), "Yin territory!", fill=(180, 50, 40), font=get_font(12))

    # Ollie warning
    draw_ollie(draw, x + 380, y + 240, scale=0.35)

# -- Scene: 6 Layers Labeled ------------------------------------------
def scene_six_layers(draw, x, y, w, h):
    tx = x + 25
    ty = y + 55
    layers = [
        ("WALL 1: Taiyang (Skin)", GREEN, "YANG"),
        ("WALL 2: Shaoyang (Hinge)", GREEN, "YANG"),
        ("WALL 3: Yangming (Furnace)", GREEN, "YANG"),
        ("--- CROSS INTO YIN ---", BROWN, ""),
        ("WALL 4: Taiyin (Spleen/Lung)", (180, 50, 40), "YIN"),
        ("WALL 5: Shaoyin (Heart/Kidney)", (180, 50, 40), "YIN"),
        ("WALL 6: Jueyin (Liver/Last)", (180, 50, 40), "YIN"),
    ]
    f_s = get_font(12)
    for i, (txt, clr, territory) in enumerate(layers):
        draw.text((tx, ty + i*26), txt, fill=clr, font=f_s)
        if territory:
            draw.text((x+330, ty + i*26), territory, fill=clr, font=get_font(10))
    # Castle icon
    draw_rectangle_simple(draw, x+360, y+120, 50, 60)

def draw_rectangle_simple(draw, cx, cy, w_s, h_s):
    """Draw a tiny castle icon."""
    draw.rectangle([cx-w_s//2, cy-h_s//2, cx+w_s//2, cy+h_s//2], fill=(200, 185, 160), outline=LINE_COLOR, width=1)
    draw.rectangle([cx-5, cy-h_s//2+5, cx+5, cy-h_s//2+20], fill=(180, 160, 140), outline=LINE_COLOR, width=1)
    draw.polygon([(cx-8, cy-h_s//2+5), (cx, cy-h_s//2-10), (cx+8, cy-h_s//2+5)],
                 fill=(180, 60, 50), outline=LINE_COLOR, width=1)

# -- Scene: Healing in Reverse ----------------------------------------
def scene_healing_reverse(draw, x, y, w, h):
    cx = x + w//2
    # Arrow going UP (outward)
    draw.line([(cx-80, y+300), (cx-80, y+100)], fill=GREEN, width=3)
    draw.polygon([(cx-80, y+100), (cx-90, y+115), (cx-70, y+115)], fill=GREEN)
    draw.text((cx-130, y+190), "Disease", fill=GREEN, font=get_font(11))
    draw.text((cx-130, y+210), "EXITS ->", fill=GREEN, font=get_font(12))

    # Person getting better
    draw.ellipse([cx+30, y+120, cx+60, y+150], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    draw.line([(cx+45, y+150), (cx+45, y+210)], fill=LINE_COLOR, width=3)
    draw.line([(cx+45, y+165), (cx+15, y+195)], fill=LINE_COLOR, width=2)
    draw.line([(cx+45, y+165), (cx+75, y+195)], fill=LINE_COLOR, width=2)
    # Smile
    draw.arc([cx+38, y+128, cx+52, y+140], 0, 180, fill=LINE_COLOR, width=1)
    # Sun/good energy
    draw.ellipse([cx+50, y+95, cx+80, y+125], fill=(255, 240, 150), outline=(220, 200, 100), width=2)
    # Rashes/skin (good sign)
    for rx, ry in [(cx+85, y+155), (cx+95, y+165), (cx+75, y+170)]:
        draw.ellipse([rx-4, ry-4, rx+4, ry+4], fill=(200, 140, 100), outline=(180, 100, 60), width=1)
    draw.text((cx+65, y+178), "Skin rash =", fill=GREEN, font=get_font(9))
    draw.text((cx+65, y+190), "good sign!", fill=GREEN, font=get_font(9))

    # Subtitle
    draw.text((x+30, y+310), "Getting 'worse' = getting better in TCM", fill=GREEN, font=get_font(11))

# -- Comic: Six-Layer Defense -----------------------------------------
def make_comic_09():
    W = PANEL_W * 2 + 40
    H = PANEL_H * 2 + 40
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Panel 1: The Castle Inside You
    draw_panel(draw, 10, 10, PANEL_W, PANEL_H,
               "Panel 1: Your Body Is a Castle",
               ["", "You have 6 walls of defense.", "Each wall protects deeper organs.", "A simple cold hits Wall 1.", "Fight it there. Win there."],
               scene_fn=scene_castle)

    # Panel 2: The Wrong Move
    draw_panel(draw, PANEL_W+30, 10, PANEL_W, PANEL_H,
               "Panel 2: The Wrong Way to Fight",
               ["", "Cold medicine suppresses the", "fever. But the pathogen goes DEEPER.", "Days later: 'Why do I feel worse?'", "You opened the gate!"],
               scene_fn=scene_wrong_meds)

    # Panel 3: The 6-Layer Map
    draw_panel(draw, 10, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 3: Ollie's 6-Layer Map",
               ["", "The Yang layers fight at the surface.", "The Yin layers are where", "chronic illness hides.", "Know which layer = know the strategy."],
               ollie_pos=(PANEL_W-70, PANEL_H-80),
               scene_fn=scene_six_layers)

    # Panel 4: Healing Goes Backwards
    draw_panel(draw, PANEL_W+30, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 4: Healing in Reverse",
               ["", "Disease moves INWARD.", "Healing moves OUTWARD.", "Fever and rashes = the enemy", "evacuating. Celebrate it!"],
               scene_fn=scene_healing_reverse)

    out = winpath("comic-09-six-layer-defense.png")
    img.save(out, "PNG")
    print(f"Saved: {out}")
    return out

if __name__ == "__main__":
    print("Generating comic #09 (Six-Layer Defense)...")
    make_comic_09()
    print("Done!")
