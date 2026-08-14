#!/usr/bin/env python3
"""Assemble podcast audio parts into final epNN.mp3 (deploy-time).

Why: large mp3 files (~21MB) fail to git-push through the local proxy in one
connection, so episodes are committed as epNN.part0/1/2.mp3 and merged here
at deploy time on GitHub Actions (which has ffmpeg).

Usage: python3 podcast/scripts/assemble-parts.py
"""

import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PODCAST_DIR = os.path.join(ROOT, "podcast")


def main():
    parts = sorted(glob.glob(os.path.join(PODCAST_DIR, "ep*.part*.mp3")))
    if not parts:
        print("assemble-parts: no parts found, nothing to do")
        return 0

    groups = {}
    for p in parts:
        m = re.match(r"ep(\d+)\.part(\d+)\.mp3$", os.path.basename(p))
        if not m:
            continue
        groups.setdefault(int(m.group(1)), []).append((int(m.group(2)), p))

    for ep in sorted(groups):
        group = [p for _, p in sorted(groups[ep])]
        out = os.path.join(PODCAST_DIR, f"ep{ep:02d}.mp3")
        print(f"assemble-parts: merging {len(group)} parts -> {os.path.basename(out)}")
        inputs = []
        for p in group:
            inputs += ["-i", p]
        flt = "".join(
            f"[{i}:a]aformat=sample_fmts=fltp:channel_layouts=mono[a{i}];"
            for i in range(len(group))
        )
        flt += "".join(f"[a{i}]" for i in range(len(group)))
        flt += f"concat=n={len(group)}:v=0:a=1[aout]"
        r = subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", *inputs,
             "-filter_complex", flt, "-map", "[aout]", "-ar", "44100",
             "-b:a", "128k", out],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print(f"assemble-parts ERROR for {out}: {r.stderr[-300:]}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
