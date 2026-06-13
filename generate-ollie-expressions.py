#!/usr/bin/env python3
"""
Generate 8 Ollie expression images using Bailian CLI.
Base prompt (same for all 8) + expression-specific prompt appended.
"""

import subprocess
import os
import sys

BL = "/Users/a11/.workbuddy/binaries/node/versions/22.22.2/bin/bl"
OUT = "/Users/a11/tcmway-blog/images/ollie-promo/expressions"

# Base prompt (immutable part, same for all 8 images)
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

# Expression prompts
EXPRESSIONS = {
    "ollie-smile": (
        "EXPRESSION: Smiling warmly. Both eyes slightly curved upward (happy arcs). "
        "Small curved smile line on the beak area. Gentle, friendly, welcoming."
    ),
    
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
    
    "ollie-thinking": (
        "EXPRESSION: Thinking deeply. One eye slightly narrowed (squinting), other eye normal. "
        "Eyebrow tufts asymmetrical — one raised, one lowered. "
        "Beak slightly pursed to one side. A tiny question mark \"?\" nearby. "
        "Contemplative, \"hmm, let me think about this\" vibe."
    ),
    
    "ollie-serious": (
        "EXPRESSION: Serious and stern. Eyebrow tufts angled downward (V shape). "
        "Eyes half-lidded, looking directly at viewer. Beak set in a straight firm line. "
        "No smile. Authoritative, \"I'm not joking\" vibe. Like a teacher about to correct a mistake."
    ),
    
    "ollie-nervous": (
        "EXPRESSION: Nervous, slightly anxious. Eyes wide with pupils shifted to one side (looking away). "
        "A tiny sweat drop on the side of the head. Beak making a small wavy line. "
        "Eyebrow tufts raised in worry. \"This is a bit complicated...\" vibe."
    ),
    
    "ollie-sleepy": (
        "EXPRESSION: Sleepy, dozing off. Both eyes half-closed (drawn as drooping arcs). "
        "Small \"Zzz\" floating above head. Beak slightly open in a tiny O. "
        "Head tilted very slightly to one side. \"I may have nodded off\" vibe. "
        "(This is Ollie's signature trait — he's always sleepy.)"
    ),
    
    "ollie-pleading": (
        "EXPRESSION: Pleading, puppy-dog eyes. Eyes extra large with big shiny highlights (wet-looking). "
        "Eyebrow tufts raised in the middle (sad/worried shape). "
        "Beak making a small downturned curve. \"How could you?\" or \"Please?\" vibe."
    ),
}

def generate(name, expr_prompt):
    full_prompt = BASE + " " + expr_prompt
    out_prefix = name
    
    cmd = [
        BL, "image", "generate",
        "--model", "qwen-image-2.0",
        "--size", "1024*1024",
        "--watermark", "false",
        "--out-dir", OUT,
        "--out-prefix", out_prefix,
        "--prompt", full_prompt,
    ]
    
    print(f"\n{'='*60}")
    print(f"Generating: {name}")
    print(f"Prompt length: {len(full_prompt)} chars")
    print(f"{'='*60}")
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,  # 5 min timeout per image
    )
    
    if result.returncode == 0:
        print(f"✅ {name} generated successfully")
        print(result.stdout[-200:])  # Print last 200 chars
        return True
    else:
        print(f"❌ {name} FAILED")
        print(f"STDOUT: {result.stdout[-300:]}")
        print(f"STDERR: {result.stderr[-300:]}")
        return False

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    
    print(f"Output directory: {OUT}")
    print(f"Total expressions to generate: {len(EXPRESSIONS)}")
    print(f"{'='*60}")
    
    success = 0
    failed = []
    
    for i, (name, prompt) in enumerate(EXPRESSIONS.items(), 1):
        print(f"\nProgress: {i}/{len(EXPRESSIONS)}")
        ok = generate(name, prompt)
        if ok:
            success += 1
        else:
            failed.append(name)
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: {success}/{len(EXPRESSIONS)} succeeded")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    print(f"{'='*60}")
