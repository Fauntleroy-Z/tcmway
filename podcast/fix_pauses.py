#!/usr/bin/env python3
"""Fix rushed TTS — v2: split into temp files, insert silence, concat back.
Simpler and more reliable than massive filter_complex.
"""

import subprocess, sys, os, tempfile, shutil

MIN_GAP = 0.6     # extend gaps shorter than this
TARGET_GAP = 1.5  # target gap length
THRESH = -20      # dB
DUR = 0.3         # min silence to detect

def run_ff(cmd, timeout=120):
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
        "-f", "null", "/dev/null"
    ], timeout=60)
    
    gaps = []
    gs = None
    for line in out.split('\n'):
        if 'silence_start:' in line:
            gs = float(line.split('silence_start:')[1].strip())
        elif 'silence_end:' in line and gs is not None:
            ge = float(line.split('silence_end:')[1].split('|')[0].strip())
            gaps.append((gs, ge))
            gs = None
    return gaps

def get_dur(path):
    out = run_ff(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                  "-of", "csv=p=0", path])
    return float(out.strip())

def main():
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else inp.rsplit('.', 1)[0] + '-paced.mp3'
    
    print(f"Input: {inp}")
    total_dur = get_dur(inp)
    gaps = detect_gaps(inp)
    
    to_fix = [(s, e) for s, e in gaps if (e - s) < MIN_GAP]
    print(f"Gaps: {len(gaps)} total, {len(to_fix)} too short")
    
    if not to_fix:
        print("Already well-paced!")
        return
    
    # Build segment list with short gaps extended
    # Each segment: (start, end, extra_silence)
    segments = []
    cursor = 0.0
    
    for gs, ge in gaps:
        if gs > cursor:
            segments.append((cursor, gs, 0.0))
        
        gap_dur = ge - gs
        if gap_dur < MIN_GAP:
            extra = TARGET_GAP - gap_dur
            if extra < 0.1:
                extra = 0.1
            segments.append((gs, ge, extra))
        else:
            segments.append((gs, ge, 0.0))
        cursor = ge
    
    if cursor < total_dur:
        segments.append((cursor, total_dur, 0.0))
    
    # Create temp dir
    tmp = tempfile.mkdtemp(prefix="pacefix_")
    silence_file = os.path.join(tmp, "silence.wav")
    
    # Generate silence template (1s, 44100 Hz mono)
    run_ff([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=mono",
        "-t", "1", silence_file
    ])
    
    print(f"Processing {len(segments)} segments...")
    seg_files = []
    
    for i, (start, end, extra) in enumerate(segments):
        dur = end - start
        if dur < 0.01:
            continue
        
        seg_path = os.path.join(tmp, f"seg_{i:04d}.wav")
        run_ff([
            "ffmpeg", "-y", "-i", inp,
            "-ss", str(start), "-t", str(dur),
            "-c:a", "pcm_s16le", seg_path
        ])
        seg_files.append(seg_path)
        
        if extra > 0:
            # Add extra silence segment
            pad_path = os.path.join(tmp, f"pad_{i:04d}.wav")
            run_ff([
                "ffmpeg", "-y", "-i", silence_file,
                "-t", str(extra),
                "-c:a", "pcm_s16le", pad_path
            ])
            seg_files.append(pad_path)
            if i % 20 == 0:
                print(f"  ... {i}/{len(segments)}")
    
    # Build concat list
    list_path = os.path.join(tmp, "list.txt")
    with open(list_path, "w") as f:
        for sf in seg_files:
            f.write(f"file '{sf}'\n")
    
    print(f"Concatenating {len(seg_files)} files...")
    run_ff([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_path,
        "-c:a", "libmp3lame", "-b:a", "128k",
        out
    ], timeout=300)
    
    out_dur = get_dur(out)
    added = out_dur - total_dur
    size_mb = os.path.getsize(out) / 1e6
    m, s = divmod(int(out_dur), 60)
    print(f"Done: {out}  [{m}:{s:02d}]  {size_mb:.1f}MB  (+{added:.0f}s pauses)")
    
    # Cleanup
    shutil.rmtree(tmp)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: fix_pauses.py <input.mp3> [output.mp3]")
        sys.exit(1)
    main()
