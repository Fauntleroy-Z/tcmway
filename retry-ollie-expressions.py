#!/usr/bin/env python3
"""Retry failed Ollie expressions: ollie-wink and ollie-surprised."""

import subprocess
import os

BL = "/Users/a11/.workbuddy/binaries/node/versions/22.22.2/bin/bl"
OUT = "/Users/a11/tcmway-blog/images/ollie-promo/expressions"

BASE = (
    "Anthropomorphic SCREECH OWL character standing on two legs. "
    "HEAD: large rounded head with prominent pointed EAR TUFTS on top. Vermilion red #b83a2a. "
    "FACE: warm apricot #e8a87c face disc with soft peach blush on cheeks. "
    "EYES: large round golden-yellow eyes (#c9a84c gold iris, #1a1410 dark brown-black pupil). "
    "BEAK: short curved owl beak in vermilion #b83a2a with a thin gold accent line (#c9a84c). NO cat nose. NO snout. NO whiskers. "
    "NECK: golden yin-yang pendant (#c9a84c) on a delicate chain. "
    "BODY: owl body covered in FEATHERS (NOT fur). Brownish-red #b83a2a wings with apricot #e8a87c belly. Wing tips are feather-shaped. NO paws. NO hands. "
    "BACKGROUND: solid warm cream #fdf6ee. "
    "STYLE: hand-drawn storybook illustration, warm organic feel, soft radial gradients, gentle shadows. "
    "CRITICAL: This is an OWL. NOT a cat. NOT a fox. NOT a dog. NOT a bear. "
    "CHARACTER MUST BE IDENTICAL across all 8 images — same size, same pose, same colors. Only the facial expression changes."
)

# Only retry these two
RETRY = {
    "ollie-wink": (
        "EXPRESSION: Winking playfully. Right eye closed (drawn as a curved arc line). "
        "Left eye open normally, looking at the viewer. Small smile on the beak. "
        "A tiny sparkle/star near the closed eye. Playful, knowing, \"I told you so\" vibe."
    ),
    "ollie-surprised": (
        "EXPRESSION: Surprised, eyes wide. Both eyes enlarged — pupils smaller, more white showing around iris. "
        "Eyebrow tufts raised high. Beak slightly open in a small O shape. "
        "Maybe one small exclamation mark floating nearby. Shocked, \"no way!\" vibe."
    ),
}

def generate(name, expr_prompt):
    full_prompt = BASE + " " + expr_prompt
    
    cmd = [
        BL, "image", "generate",
        "--model", "qwen-image-2.0",
        "--size", "1024*1024",
        "--watermark", "false",
        "--out-dir", OUT,
        "--out-prefix", name,
        "--prompt", full_prompt,
    ]
    
    print(f"\n{'='*60}")
    print(f"RETRY: {name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        
        if result.returncode == 0:
            print(f"✅ {name} generated successfully")
            # Print last part of stdout (JSON result)
            print(result.stdout[-300:])
            return True
        else:
            print(f"❌ {name} FAILED")
            print(f"STDERR: {result.stderr[-200:]}")
            return False
    except Exception as e:
        print(f"❌ {name} EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    
    for name, prompt in RETRY.items():
        ok = generate(name, prompt)
        if ok:
            print(f"✅ {name}.png saved to {OUT}/")
        else:
            print(f"❌ {name} still failed after retry")
    
    print(f"\n{'='*60}")
    print("Retry complete. Check output directory.")
    print(f"{'='*60}")
