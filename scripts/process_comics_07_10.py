"""
Post-process comic images #07-#10 using the EXACT same method as #01-#06.

#01-#06 workflow (verified from git history + file analysis):
  1. Generate with Hunyuan API → 1024x1024 PNG with watermark + bottom shadow bar
  2. Crop bottom 150px → 1024x874 (removes shadow bar)
  3. Remove "图片由AI生成" watermark from bottom-right
  4. Run soften_watermark_v3.py → gradient feather blend
  5. Blog posts reference -new.png directly

This script handles steps 2-3. Then soften_watermark_v3.py handles step 4.
"""

from PIL import Image, ImageDraw
import os

IMG_DIR = r'C:\Users\Administrator\tcmway-blog\images'

# (filename, right_ratio, bottom_ratio, blend_strength_for_soften)
COMICS = [
    ('comic-07-six-signs-new.png', 0.30, 0.18, 190),
    ('comic-08-cold-hands-new.png', 0.28, 0.18, 180),
    ('comic-09-six-layer-defense-new.png', 0.28, 0.18, 185),
    ('comic-10-stop-feeding-new.png', 0.30, 0.18, 190),
]


def crop_bottom_shadow(img):
    """Crop bottom 150px to remove AI-generated shadow/color bar (1024x1024 → 1024x874)."""
    w, h = img.size
    new_h = h - 150
    return img.crop((0, 0, w, new_h))


def remove_watermark(img, right_ratio=0.28, bottom_ratio=0.18):
    """
    Remove "图片由AI生成" watermark from bottom-right corner.
    Strategy: sample colors from the area just LEFT of the watermark,
    then cover the watermark region with the average background color.
    """
    w, h = img.size
    x_start = int(w * (1 - right_ratio))
    y_start = int(h * (1 - bottom_ratio))

    # Convert to RGB for processing
    if img.mode == 'RGBA':
        img_rgb = Image.new('RGB', img.size, (255, 255, 255))
        img_rgb.paste(img, mask=img.split()[-1])
        img = img_rgb

    # Sample background color from left-side and above the watermark area
    sample_w = min(80, x_start)
    sample_h = min(20, h - y_start)
    colors = []

    # Sample from above the watermark area
    for x in range(max(0, x_start - 30), min(w, x_start + 50)):
        for y in range(max(0, y_start - 15), y_start):
            if 0 <= x < w and 0 <= y < h:
                colors.append(img.getpixel((x, y)))

    # Sample from left of watermark area
    for x in range(x_start - sample_w, x_start):
        for y in range(y_start, y_start + sample_h):
            if 0 <= x < w and 0 <= y < h:
                colors.append(img.getpixel((x, y)))

    if not colors:
        avg_color = (240, 235, 225)
    else:
        avg_color = tuple(sum(c) // len(colors) for c in zip(*colors))

    # Cover watermark area with sampled background color
    cover_x1 = x_start - 10
    cover_y1 = max(y_start - 10, 0)
    draw = ImageDraw.Draw(img)
    draw.rectangle([cover_x1, cover_y1, w, h], fill=avg_color)

    return img


def main():
    print("=" * 60)
    print("Comic Post-Processor for #07-#10")
    print("Method: SAME as #01-#06 (crop + watermark removal)")
    print("=" * 60)

    processed = []
    for fname, rp, bp, strength in COMICS:
        src_path = os.path.join(IMG_DIR, fname)
        if not os.path.exists(src_path):
            print(f"\n❌ SKIP: {fname} not found")
            continue

        print(f"\n{'─'*50}")
        print(f"▶ {fname}")
        img = Image.open(src_path)
        print(f"  Original: {img.size[0]}x{img.size[1]}, mode={img.mode}")

        # Step 1: Crop bottom shadow bar
        img = crop_bottom_shadow(img)
        print(f"  After crop: {img.size[0]}x{img.size[1]}")

        # Step 2: Remove watermark
        img = remove_watermark(img, rp, bp)
        print(f"  After watermark removal: {img.size[0]}x{img.size[1]}")

        # Step 3: Save cleaned -new.png (overwrite)
        img.save(src_path, 'PNG', optimize=True)
        file_size = os.path.getsize(src_path)
        print(f"  ✅ Saved: {fname} ({file_size/1024:.1f} KB)")
        processed.append((fname, rp, bp, strength))

    print(f"\n{'='*60}")
    print(f"DONE: {len(processed)} comics processed")
    print("Next: run soften_watermark_v3.py for gradient feather blend")
    print("=" * 60)

    # Print parameters for soften_watermark_v3.py
    print("\n# Add to soften_watermark_v3.py COMICS list:")
    for fname, rp, bp, strength in processed:
        print(f"    ('{fname}', {rp:.2f}, {bp:.2f}, {strength}),")


if __name__ == '__main__':
    main()
