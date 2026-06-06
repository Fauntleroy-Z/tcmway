#!/usr/bin/env python3
"""
Step 2: Convert SVG files to PNG.
Uses node.js + sharp for reliable cross-platform SVG→PNG conversion.
"""
import subprocess
import os
import sys

NODE_BIN = "/Users/a11/.workbuddy/binaries/node/versions/22.22.2/bin/node"
NODE_PATH = "/Users/a11/.workbuddy/binaries/node/workspace/node_modules"
IMAGES_DIR = "/Users/a11/tcmway-blog/images"

# Map SVG paths → output width
SVG_TARGETS = {
    "comic-16-yin-yang-seesaw.svg": 1200,
    # Add more as needed: "comic-XX-name.svg": 1200,
}

def svg_to_png(svg_path, png_path, width=1200):
    """Convert single SVG to PNG using node.js + sharp."""
    code = f'''
const sharp = require("sharp");
const fs = require("fs");
const svg = fs.readFileSync("{svg_path}");
sharp(svg).resize({width}).png().toFile("{png_path}")
  .then(info => console.log("OK:" + JSON.stringify(info)))
  .catch(err => {{ console.error("ERROR:" + err.message); process.exit(1); }});
'''
    env = os.environ.copy()
    env["NODE_PATH"] = NODE_PATH
    result = subprocess.run([NODE_BIN, "-e", code], capture_output=True, text=True, env=env)
    if result.stdout.startswith("OK:"):
        info = result.stdout[3:].strip()
        print(f"  ✅ {os.path.basename(png_path)} ({info})")
        return True
    else:
        print(f"  ❌ {os.path.basename(svg_path)}: {result.stderr}")
        return False

if __name__ == "__main__":
    print("🔄 Converting SVGs to PNGs...")
    success = 0
    for svg_name, width in SVG_TARGETS.items():
        svg_path = os.path.join(IMAGES_DIR, svg_name)
        png_path = svg_path.replace(".svg", ".png")
        if not os.path.exists(svg_path):
            print(f"  ⚠️  {svg_name} not found, skipping")
            continue
        if svg_to_png(svg_path, png_path, width):
            success += 1
        else:
            sys.exit(1)
    print(f"\n✅ {success} SVG(s) converted to PNG!")
