#!/usr/bin/env python3
"""
Generate TCM Way comic strip for Post #10: Stop Feeding What You Fight.
4-panel comic: supplement aisle -> garden fertilizer -> cold feet danger -> warm food alternative.
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

# -- Scene: Supplement Aisle ------------------------------------------
def scene_aisle(draw, x, y, w, h):
    # Shelf lines
    for sy in [y+75, y+115, y+155]:
        draw.line([(x+20, sy), (x+w-20, sy)], fill=(200, 190, 170), width=2)
    # Bottles
    bottles = [
        (x+40, y+65, "Vit D", (255, 220, 150)),
        (x+120, y+65, "Omega", (200, 200, 220)),
        (x+200, y+65, "Multi", (180, 220, 180)),
        (x+280, y+65, "Probio", (220, 180, 220)),
        (x+60, y+105, "Vit C", (255, 200, 150)),
        (x+160, y+105, "Iron", (200, 150, 150)),
        (x+260, y+105, "Zinc", (180, 200, 220)),
    ]
    for bx, by, lbl, clr in bottles:
        draw.rounded_rectangle([bx, by, bx+50, by+35], radius=4, fill=clr, outline=LINE_COLOR, width=1)
        draw.text((bx+3, by+10), lbl, fill=(50, 45, 40), font=get_font(9))

    # Shopping cart
    draw.ellipse([x+120, y+200, x+250, y+230], fill=(220, 210, 190), outline=LINE_COLOR, width=2)
    # Items in cart
    cart_items = [(x+130, y+180, (255, 220, 150)),
                  (x+170, y+175, (220, 180, 220)),
                  (x+210, y+180, (200, 200, 220))]
    for cx_i, cy_i, clr in cart_items:
        draw.rectangle([cx_i, cy_i, cx_i+30, cy_i+20], fill=clr, outline=LINE_COLOR, width=1)

    # Receipt
    draw.rectangle([x+320, y+200, x+430, y+300], fill=(255,255,255), outline=LINE_COLOR, width=1)
    draw.text((x+330, y+208), "Receipt", fill=(50,45,40), font=get_font(11))
    draw.text((x+330, y+228), "Vit D ..... $12.99", fill=(50,45,40), font=get_font(9))
    draw.text((x+330, y+244), "Omega .... $15.50", fill=(50,45,40), font=get_font(9))
    draw.text((x+330, y+260), "Multi .... $10.87", fill=(50,45,40), font=get_font(9))
    draw.text((x+330, y+276), "Probio ... $18.00", fill=(50,45,40), font=get_font(9))
    draw.line([(x+330, y+282), (x+420, y+282)], fill=(50,45,40), width=1)
    draw.text((x+330, y+286), "TOTAL: $47.36/mo", fill=(180, 50, 40), font=get_font(10))

    # Person standing
    px_c = x + 60
    draw.ellipse([px_c-15, y+195, px_c+15, y+225], fill=(240, 210, 170), outline=LINE_COLOR, width=2)
    draw.line([(px_c, y+225), (px_c, y+280)], fill=LINE_COLOR, width=3)
    # Thought bubble
    draw.ellipse([px_c+30, y+170, px_c+100, y+200], outline=(180, 180, 180), width=1)
    draw.text((px_c+38, y+178), "This is", fill=BROWN, font=get_font(9))
    draw.text((px_c+38, y+190), "healthy...", fill=BROWN, font=get_font(9))
    draw.text((x+330, y+310), "But still tired?", fill=(180, 50, 40), font=get_font(10))

# -- Scene: Garden - Fertilizer Feeds Weeds --------------------------
def scene_garden(draw, x, y, w, h):
    # Title
    draw.text((x+60, y+60), "Your body is a GARDEN.", fill=OLIVE, font=get_font(14))

    # Soil
    draw.ellipse([x+40, y+120, x+200, y+200], fill=(160, 130, 90), outline=LINE_COLOR, width=2)
    # Sun
    draw.ellipse([x+240, y+60, x+290, y+110], fill=(255, 240, 150), outline=(220, 200, 100), width=2)

    # Vegetables (left side)
    for vx, vy, vh in [(x+70, y+95, 30), (x+95, y+100, 25), (x+120, y+90, 35)]:
        draw.line([(vx, vy+vh), (vx, vy)], fill=GREEN, width=4)
        draw.ellipse([vx-8, vy-8, vx+8, vy+8], fill=(120, 180, 100), outline=GREEN, width=1)
    draw.text((x+50, y+140), "Veggies", fill=GREEN, font=get_font(10))
    draw.text((x+50, y+152), "growing OK", fill=GREEN, font=get_font(10))

    # Weeds (right side - growing faster)
    for wx, wy, wh in [(x+160, y+85, 40), (x+175, y+92, 35), (x+190, y+80, 45)]:
        draw.line([(wx, wy+wh), (wx, wy)], fill=(200, 100, 60), width=4)
        draw.ellipse([wx-5, wy-5, wx+5, wy+5], fill=(200, 100, 60), outline=(180, 70, 30), width=1)
    draw.text((x+155, y+165), "Weeds", fill=(200, 100, 60), font=get_font(11))
    draw.text((x+155, y+180), "growing FASTER!", fill=(200, 100, 60), font=get_font(11))

    # Fertilizer bag with arrow
    draw.rectangle([x+260, y+130, x+340, y+170], fill=(200, 220, 180), outline=LINE_COLOR, width=2)
    draw.text((x+268, y+138), "VITAMINS", fill=(50,45,40), font=get_font(9))
    draw.text((x+268, y+152), "= fertilizer", fill=(50,45,40), font=get_font(9))
    # Arrow from fertilizer to weeds
    draw.line([(x+260, y+150), (x+200, y+120)], fill=(200, 100, 60), width=2)
    draw.polygon([(x+200, y+120), (x+195, y+130), (x+208, y+128)], fill=(200, 100, 60))

    # Subtitle
    draw.text((x+30, y+300), "Nutrition feeds weeds AND vegetables.", fill=BROWN, font=get_font(11))
    draw.text((x+30, y+318), "You don't choose which one grows faster.", fill=BROWN, font=get_font(11))

# -- Scene: Cold Feet + Supplements = Danger -------------------------
def scene_cold_feet_danger(draw, x, y, w, h):
    cx = x + w//2
    # Feet (cold, blue)
    draw.ellipse([cx-60, y+140, cx-10, y+175], fill=(160, 200, 240), outline=(100, 160, 220), width=2)
    draw.ellipse([cx+10, y+145, cx+60, y+170], fill=(160, 200, 240), outline=(100, 160, 220), width=2)
    draw.text((cx-80, y+180), "COLD FEET", fill=(100, 140, 200), font=get_font(12))

    # Supplement bottle
    draw.rounded_rectangle([cx-15, y+90, cx+15, y+130], radius=4, fill=(180, 220, 180), outline=LINE_COLOR, width=2)
    draw.text((cx-12, y+105), "VIT", fill=(50,45,40), font=get_font(9))

    # Plus sign
    draw.text((cx-34, y+108), "+", fill=(180, 50, 40), font=get_font(18))

    # Danger zone box below
    draw.rounded_rectangle([x+60, y+210, x+w-60, y+300], radius=8, fill=(255, 240, 235), outline=(200, 100, 80), width=2)
    draw.text((x+90, y+220), "DANGER: Cancer environment!", fill=(180, 50, 40), font=get_font(13))
    draw.text((x+90, y+245), "Tumor cells eat nutrients", fill=(180, 50, 40), font=get_font(11))
    draw.text((x+90, y+265), "BEFORE your healthy cells do.", fill=(180, 50, 40), font=get_font(11))
    draw.text((x+90, y+285), "The tumor eats first.", fill=(180, 50, 40), font=get_font(11))

    # Big X over supplements
    draw.line([(x+30, y+85), (x+85, y+140)], fill=(200, 50, 30), width=3)
    draw.line([(x+85, y+85), (x+30, y+140)], fill=(200, 50, 30), width=3)

    # Title
    draw.text((x+70, y+60), "Ni Haixia's Rule:", fill=OLIVE, font=get_font(14))

# -- Scene: Simple Warm Food Plate -----------------------------------
def scene_warm_plate(draw, x, y, w, h):
    cx = x + w//2
    # Plate
    draw.ellipse([cx-80, y+100, cx+80, y+200], fill=(240, 235, 220), outline=LINE_COLOR, width=3)
    draw.ellipse([cx-55, y+113, cx+55, y+187], fill=(230, 225, 210), outline=(200, 190, 170), width=1)
    # Congee (rice bowl)
    draw.ellipse([cx-35, y+150, cx-5, y+180], fill=(245, 242, 235), outline=LINE_COLOR, width=1)
    for st_i in range(3):
        draw.arc([cx-32+st_i*10, y+140, cx-22+st_i*10, y+155], 0, 180, fill=(210, 210, 210), width=1)
    draw.text((cx-50, y+158), "Congee", fill=BROWN, font=get_font(9))
    # Ginger tea cup
    draw.rectangle([cx+5, y+150, cx+30, y+178], fill=(220, 210, 180), outline=LINE_COLOR, width=1)
    draw.text((cx+5, y+183), "Ginger", fill=BROWN, font=get_font(8))
    draw.text((cx+4, y+193), "tea", fill=BROWN, font=get_font(8))
    # Egg
    draw.ellipse([cx-50, y+190, cx-20, y+215], fill=(255, 245, 220), outline=(200, 180, 140), width=1)
    draw.ellipse([cx-42, y+195, cx-32, y+205], fill=(255, 220, 100), outline=LINE_COLOR, width=1)
    draw.text((cx-50, y+220), "Soft egg", fill=BROWN, font=get_font(9))
    # Cinnamon
    draw.text((cx-50, y+130), "Cinnamon", fill=BROWN, font=get_font(9))
    draw.arc([cx-45, y+138, cx-25, y+153], 0, 180, fill=(200, 150, 80), width=2)

    # Label
    draw.text((x+30, y+75), "What to eat instead:", fill=GREEN, font=get_font(14))

    # Price tag
    draw.rectangle([x+330, y+100, x+430, y+130], fill=(255,255,255), outline=GREEN, width=2)
    draw.text((x+338, y+108), "Cost: ~$3/day", fill=GREEN, font=get_font(11))

    # Subtitle
    draw.text((x+30, y+260), "Fix the engine first.", fill=GREEN, font=get_font(12))
    draw.text((x+30, y+282), "Then your body extracts what it needs.", fill=GREEN, font=get_font(12))

# -- Comic: Stop Feeding What You Fight -------------------------------
def make_comic_10():
    W = PANEL_W * 2 + 40
    H = PANEL_H * 2 + 40
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Panel 1: The Supplement Aisle
    draw_panel(draw, 10, 10, PANEL_W, PANEL_H,
               "Panel 1: The $47/Month Gamble",
               ["", "Vitamins. Omega-3. Probiotics.", "Multivitamins. $47.36 every month.", "And you still wake up tired.", "Here's a question no label asks:"],
               scene_fn=scene_aisle)

    # Panel 2: The Garden Problem
    draw_panel(draw, PANEL_W+30, 10, PANEL_W, PANEL_H,
               "Panel 2: Who Else Are You Feeding?",
               ["", "Nutrition doesn't discriminate.", "Vitamins feed your cells...", "...AND your disease.", "Fertilizer grows weeds fastest."],
               ollie_pos=(PANEL_W//2, PANEL_H-120),
               scene_fn=scene_garden)

    # Panel 3: The Cold Feet Rule
    draw_panel(draw, 10, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 3: Cold Feet? STOP Supplements.",
               ["", "If your hands and feet are cold,", "your Yang (fire) is too weak.", "Supplements become disease fuel.", "The tumor eats before you do."],
               scene_fn=scene_cold_feet_danger)

    # Panel 4: The Simple Alternative
    draw_panel(draw, PANEL_W+30, PANEL_H+30, PANEL_W, PANEL_H,
               "Panel 4: What to Eat Instead",
               ["", "Congee. Ginger tea. Soft egg.", "Cinnamon. Warm food. Simple meals.", "Fix your digestion first.", "Then your body handles the rest."],
               scene_fn=scene_warm_plate)

    out = winpath("comic-10-stop-feeding.png")
    img.save(out, "PNG")
    print(f"Saved: {out}")
    return out

if __name__ == "__main__":
    print("Generating comic #10 (Stop Feeding What You Fight)...")
    make_comic_10()
    print("Done!")
