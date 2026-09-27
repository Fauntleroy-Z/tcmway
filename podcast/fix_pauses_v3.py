#!/usr/bin/env python3
"""fix_pauses v3 "refined" - repair only abnormally short gaps, preserve natural rhythm.

Why v3 exists
-------------
v1 (fix_pauses.py) stretched EVERY gap < MIN_GAP to a single TARGET_GAP=1.0s.
On EP16 that turned a naturally flowing read (2 pauses >=0.5s per 60s) into a
choppy one (14 pauses per 60s) - the "stitched" feel the owner heard.

SOP intent was always "sentence-boundary pauses >= ~0.7s", not "every breath
becomes 1 second". v3 restores that intent heuristically:

  * conservative detection (-25 dB, >=0.25 s) - only true silence counts
  * adaptive split: gaps below T are treated as squeezed; gaps >= T are kept
  * repair target is a natural short pause (~0.45-0.60 s), NEVER 1.0 s
  * long gaps (>2 s, e.g. section breaks) are never touched

Usage: python3 fix_pauses_v3.py <input.mp3> [output.mp3]
"""

import os
import shutil
import subprocess
import sys
import tempfile

THRESH = float(os.environ.get("FP_THRESH", -25))
DUR = float(os.environ.get("FP_DUR", 0.25))
FLOOR = float(os.environ.get("FP_FLOOR", 0.32))
CAP = float(os.environ.get("FP_CAP", 0.45))
TARGET_MIN = float(os.environ.get("FP_TMIN", 0.45))
TARGET_MAX = float(os.environ.get("FP_TMAX", 0.60))
LONG_SAFE = 2.0


def run_ff(cmd, timeout=600):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    combined = r.stdout + r.stderr
    if r.returncode != 0:
        print(f"FFMPEG ERROR:\n{combined[-500:]}")
        sys.exit(1)
    return combined


def detect_gaps(path):
    out = run_ff([
        "ffmpeg", "-i", path,
        "-af", f"silencedetect=n={THRESH}dB:d={DUR}",
        "-f", "null", "/dev/null",
    ], timeout=600)
    gaps, gs = [], None
    for line in out.split("\n"):
        if "silence_start:" in line:
            gs = float(line.split("silence_start:")[1].strip())
        elif "silence_end:" in line and gs is not None:
            ge = float(line.split("silence_end:")[1].split("|")[0].strip())
            gaps.append((gs, ge))
            gs = None
    return gaps


def get_dur(path):
    out = run_ff(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                  "-of", "csv=p=0", path])
    return float(out.strip())


def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return 0.0
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def main():
    if len(sys.argv) < 2:
        print("Usage: fix_pauses_v3.py <input.mp3> [output.mp3]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else inp.rsplit(".", 1)[0] + "-refined.mp3"

    total = get_dur(inp)
    gaps = detect_gaps(inp)
    body = [e - s for s, e in gaps if 0.1 <= (e - s) <= LONG_SAFE]
    M = median(body)

    T = max(FLOOR, min(CAP, M * 0.65)) if M else FLOOR
    target = max(TARGET_MIN, min(TARGET_MAX, (M * 0.9) if M else TARGET_MIN))
    squeezed = [(s, e) for s, e in gaps if (e - s) < T and (e - s) <= LONG_SAFE]

    print(f"input {inp}")
    print(f"  gaps detected (>= {DUR}s @ {THRESH}dB): {len(gaps)}")
    print(f"  body-gap median: {M:.3f}s -> squeezed threshold T={T:.3f}s, repair target={target:.3f}s")
    print(f"  squeezed gaps to repair: {len(squeezed)}")

    if not squeezed:
        print("Nothing to repair - rhythm already natural. Copying input.")
        shutil.copy(inp, out)
        return

    segments, cursor = [], 0.0
    for gs, ge in gaps:
        if gs > cursor:
            segments.append((cursor, gs, 0.0))
        g = ge - gs
        if g < T and g <= LONG_SAFE:
            segments.append((gs, ge, max(0.05, target - g)))
        else:
            segments.append((gs, ge, 0.0))
        cursor = ge
    if cursor < total:
        segments.append((cursor, total, 0.0))

    tmp = tempfile.mkdtemp(prefix="pacev3_")
    sil = os.path.join(tmp, "sil.wav")
    run_ff(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono",
            "-t", "1", sil])

    seg_files = []
    for i, (s, e, extra) in enumerate(segments):
        d = e - s
        if d < 0.01:
            continue
        seg = os.path.join(tmp, f"seg_{i:04d}.wav")
        run_ff(["ffmpeg", "-y", "-i", inp, "-ss", str(s), "-t", str(d),
                "-c:a", "pcm_s16le", seg])
        seg_files.append(seg)
        if extra > 0.001:
            pad = os.path.join(tmp, f"pad_{i:04d}.wav")
            run_ff(["ffmpeg", "-y", "-i", sil, "-t", str(extra),
                    "-c:a", "pcm_s16le", pad])
            seg_files.append(pad)

    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for sf in seg_files:
            f.write(f"file '{sf}'\n")

    run_ff(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
            "-c:a", "libmp3lame", "-b:a", "128k", out], timeout=900)

    new = get_dur(out)
    print(f"  -> {out}  [{int(new)//60}:{int(new)%60:02d}]  added {new-total:+.1f}s pauses")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
