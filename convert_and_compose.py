#!/usr/bin/env python3
"""
Step 2: Convert SVG panels to PNG (using managed Python with cairosvg),
then compose 4 panels into 2x2 grid (using system Python with PIL).

Usage: Run this with the managed Python for cairosvg conversion,
then compose with system Python.
"""
import subprocess
import os
import sys

MANAGED_PY = "/Users/a11/.workbuddy/binaries/python/envs/default/bin/python3"
OUT_DIR = "/Users/a11/tcmway-blog/images"
CREAM_COLOR = (253, 246, 238)
PANEL_SIZE = 512

def svg_to_png(svg_path, png_path):
    """Convert SVG to PNG using cairosvg (requires managed Python)."""
    import cairosvg
    with open(svg_path, 'r') as f:
        svg = f.read()
    cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to=png_path, output_width=PANEL_SIZE, output_height=PANEL_SIZE)
    print(f"  🖼️  {png_path}")

def compose_grid(png_list, output_path):
    """Compose 4 panels into 2x2 grid."""
    from PIL import Image
    grid = Image.new("RGB", (PANEL_SIZE*2, PANEL_SIZE*2), CREAM_COLOR)
    positions = [(0,0), (PANEL_SIZE,0), (0,PANEL_SIZE), (PANEL_SIZE,PANEL_SIZE)]
    for (x, y), png_path in zip(positions, png_list):
        img = Image.open(png_path)
        grid.paste(img, (x, y))
    grid.save(output_path, "PNG")
    print(f"  💾 {output_path}")

def process_comic(name, output_filename):
    tmp_dir = f"/tmp/tcmway-comics/{name}"
    png_list = []
    
    print(f"\n📦 {name}:")
    for i in range(1, 5):
        svg_path = f"{tmp_dir}/panel_{i}.svg"
        png_path = f"{tmp_dir}/panel_{i}.png"
        svg_to_png(svg_path, png_path)
        png_list.append(png_path)
    
    output_path = os.path.join(OUT_DIR, f"{output_filename}.png")
    compose_grid(png_list, output_path)

if __name__ == "__main__":
    process_comic("comic-11-cold-progression", "comic-11-cold-progression-new")
    process_comic("comic-16-yin-yang-seesaw", "comic-16-yin-yang-seesaw")
    print("\n✅ All done!")
