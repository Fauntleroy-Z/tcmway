"""
fix_comics_v2.py — Robust watermark + shadow removal for comics #07-#10

Strategy:
  1. Direct pixel blending (no alpha compositing complexity)
  2. Cover bottom-right area with gradient-blended background color
  3. Shadow correction for #09
  4. Output: clean RGBA PNG → WebP

#01-#06 -new.png files are RGBA. This script preserves RGBA properly.
"""

from PIL import Image, ImageEnhance
import os
import math

IMG_DIR = r'C:\Users\Administrator\tcmway-blog\images'
WEBP_QUALITY = 85

COMICS = [
    ('comic-07-six-signs-new.png',          1.0, False),
    ('comic-08-cold-hands-new.png',          1.0, False),
    ('comic-09-six-layer-defense-new.png',   1.10, True),
    ('comic-10-stop-feeding-new.png',        1.0, False),
]

WEBP_MAP = {
    'comic-07-six-signs-new.png': 'comic-07-six-signs.webp',
    'comic-08-cold-hands-new.png': 'comic-08-cold-hands.webp',
    'comic-09-six-layer-defense-new.png': 'comic-09-six-layer-defense.webp',
    'comic-10-stop-feeding-new.png': 'comic-10-stop-feeding.webp',
}


def median_color(img, x1, y1, x2, y2):
    """Median color from a region — robust against outliers."""
    w, h = img.size
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    pix = img.load()
    rs, gs, bs = [], [], []
    for y in range(y1, y2):
        for x in range(x1, x2):
            r, g, b = pix[x, y][:3]
            rs.append(r); gs.append(g); bs.append(b)
    if not rs:
        return (240, 235, 225)
    rs.sort(); gs.sort(); bs.sort()
    n = len(rs)
    return (rs[n//2], gs[n//2], bs[n//2])


def blend_pixels(orig, cover, t):
    """Blend orig → cover with factor t (0=orig, 1=cover)."""
    return (
        int(orig[0] * (1-t) + cover[0] * t),
        int(orig[1] * (1-t) + cover[1] * t),
        int(orig[2] * (1-t) + cover[2] * t),
    )


def process_comic(fname, brightness_boost, shadow_fix):
    src = os.path.join(IMG_DIR, fname)
    if not os.path.exists(src):
        print(f"  ❌ Not found: {fname}")
        return False

    img = Image.open(src).convert('RGBA')
    w, h = img.size
    orig_size = os.path.getsize(src)
    print(f"  Input: {w}x{h} RGBA, {orig_size/1024:.0f}K")

    # ── Step 0: Crop bottom 150px shadow bar (1024x1024 → 1024x874) ──
    if h == 1024 and w == 1024:
        img = img.crop((0, 0, w, h - 150))
        w, h = img.size
        print(f"  Cropped: {w}x{h}")

    # ── Step 1: Brightness ──
    if brightness_boost != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness_boost)
        print(f"  Brightness +{int((brightness_boost-1)*100)}%")

    # ── Step 2: Shadow correction (radial vignette reduction) ──
    if shadow_fix:
        pix = img.load()
        cx, cy = w/2, h/2
        max_dist = math.sqrt(cx*cx + cy*cy)
        for y in range(h):
            for x in range(w):
                dist = math.sqrt((x-cx)**2 + (y-cy)**2) / max_dist
                boost = 1.0 + 0.10 * (dist ** 1.8)  # +10% at edges
                r, g, b, a = pix[x, y]
                pix[x, y] = (
                    min(255, int(r * boost)),
                    min(255, int(g * boost)),
                    min(255, int(b * boost)),
                    a,
                )
        print(f"  Vignette correction applied")

    # ── Step 3: Watermark cover with gradient blend ──
    # Cover: right 45%, bottom 30% (catches watermark wherever it is)
    cover_right = 0.45
    cover_bottom = 0.30
    x1 = int(w * (1 - cover_right))
    y1 = int(h * (1 - cover_bottom))
    cover_w = w - x1
    cover_h = h - y1

    # Sample BG from area just outside the cover region
    sample_x1 = max(0, x1 - 80)
    sample_y1 = max(0, y1 - 40)
    bg = median_color(img, sample_x1, sample_y1, x1, y1)
    print(f"  Cover: ({x1},{y1})-[{cover_w}x{cover_h}], BG=RGB{bg}")

    pix = img.load()
    changed = 0
    for py in range(y1, h):
        dy = (py - y1) / max(1, cover_h - 1)  # 0 at top, 1 at bottom
        for px in range(x1, w):
            dx = (px - x1) / max(1, cover_w - 1)  # 0 at left, 1 at right

            # Blend factor: 1 at corner (full cover), 0 at edges (no cover)
            t = min(dx, dy)  # diagonal gradient
            t = t * t * (3 - 2*t)  # ease-in-out

            # At t=1 (bottom-right): full BG color
            # At t=0 (left/top edges): partial blend
            blend = 0.15 + 0.85 * t  # Even at edge, 15% blend for smoothness

            orig_rgba = pix[px, py]
            new_rgb = blend_pixels(orig_rgba, bg, blend)
            pix[px, py] = new_rgb + (255,)  # Full opacity
            changed += 1

    print(f"  Pixels blended: {changed}")

    # ── Step 4: Additional edge feathering ──
    # Apply a narrow soft edge at the boundary to avoid visible seam
    feather_width = 20
    for py in range(max(0, y1 - feather_width), min(h, y1 + feather_width)):
        for px in range(max(0, x1 - feather_width), min(w, x1 + feather_width)):
            # Distance from the cover boundary corner (x1, y1)
            dist_from_boundary = min(
                abs(px - x1) / feather_width,
                abs(py - y1) / feather_width,
            )
            if dist_from_boundary < 1.0 and (px >= x1 or py >= y1):
                # Blend original with covered pixel
                orig_r, orig_g, orig_b, orig_a = pix[px, py]
                cover_r, cover_g, cover_b = bg
                t_feather = max(0, 1.0 - dist_from_boundary) * 0.3  # Max 30% blend at boundary
                pix[px, py] = (
                    int(orig_r * (1-t_feather) + cover_r * t_feather),
                    int(orig_g * (1-t_feather) + cover_g * t_feather),
                    int(orig_b * (1-t_feather) + cover_b * t_feather),
                    255,
                )

    # ── Save ──
    img.save(src, 'PNG', optimize=True)
    new_size = os.path.getsize(src)
    print(f"  ✅ {fname}: {orig_size/1024:.0f}K → {new_size/1024:.0f}K")
    return True


def to_webp(png_name):
    webp_name = WEBP_MAP.get(png_name)
    if not webp_name:
        return
    src = os.path.join(IMG_DIR, png_name)
    dst = os.path.join(IMG_DIR, webp_name)
    if not os.path.exists(src):
        print(f"  ❌ Source not found: {png_name}")
        return
    img = Image.open(src)
    # Check if there's actually transparency needed
    has_transparent = False
    data = list(img.getdata())
    for pixel in data[:min(500, len(data))]:  # Sample
        if len(pixel) > 3 and pixel[3] < 250:
            has_transparent = True
            break
    if not has_transparent:
        img = img.convert('RGB')
    img.save(dst, 'WEBP', quality=WEBP_QUALITY, optimize=True)
    print(f"  → {webp_name}: {os.path.getsize(dst)/1024:.0f}K")


def main():
    print("=" * 60)
    print("fix_comics_v2.py — Direct Pixel Blend Watermark Removal")
    print("=" * 60)

    for fname, boost, shadow in COMICS:
        print(f"\n{'─'*50}")
        print(f"▶ {fname}")
        if process_comic(fname, boost, shadow):
            to_webp(fname)

    print(f"\n{'='*60}")
    print("DONE. Commit + push to GitHub.")
    print("=" * 60)


if __name__ == '__main__':
    main()
