#!/usr/bin/env python3
"""Build timing.json from per-scene voiceover files.

Usage:
    python3 scene_timing.py <audio_dir> [--fps 30] [--head 0.25] [--tail 0.45]

Reads <audio_dir>/vo/scene-XX.(mp3|wav|m4a), measures each file with ffprobe,
adds breathing room before/after the VO, and writes <audio_dir>/timing.json.
Scene length in the video = head + VO + tail, rounded up to whole frames.
"""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

AUDIO_EXT = {".mp3", ".wav", ".m4a", ".aac"}


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    if out.returncode != 0 or not out.stdout.strip():
        raise RuntimeError(f"ffprobe could not read {path}: {out.stderr.strip()}")
    return float(out.stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio_dir")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--head", type=float, default=0.25, help="silence before VO (s)")
    ap.add_argument("--tail", type=float, default=0.45, help="hold after VO (s)")
    ap.add_argument("--target", type=float, default=60.0)
    args = ap.parse_args()

    if not shutil.which("ffprobe"):
        print("ffprobe not found. Install ffmpeg (brew install ffmpeg / apt install ffmpeg).", file=sys.stderr)
        return 1

    vo_dir = Path(args.audio_dir) / "vo"
    files = sorted(
        (p for p in vo_dir.iterdir() if p.suffix.lower() in AUDIO_EXT and re.match(r"scene-\d+", p.stem)),
        key=lambda p: int(re.search(r"\d+", p.stem).group()),
    ) if vo_dir.is_dir() else []
    if not files:
        print(f"No scene-XX audio files in {vo_dir}", file=sys.stderr)
        return 1

    scenes, cursor = [], 0
    for p in files:
        vo = duration(p)
        frames = math.ceil((args.head + vo + args.tail) * args.fps)
        scenes.append({
            "id": p.stem,
            "file": f"vo/{p.name}",
            "voSeconds": round(vo, 3),
            "voStartFrame": round(args.head * args.fps),
            "startFrame": cursor,
            "frames": frames,
            "seconds": round(frames / args.fps, 3),
        })
        cursor += frames

    total = cursor / args.fps
    result = {"fps": args.fps, "totalFrames": cursor, "totalSeconds": round(total, 2), "scenes": scenes}
    out = Path(args.audio_dir) / "timing.json"
    out.write_text(json.dumps(result, indent=2))

    for s in scenes:
        print(f"{s['id']:>10}  VO {s['voSeconds']:6.2f}s  scene {s['seconds']:6.2f}s")
    print(f"{'total':>10}  {total:.2f}s  → {out}")
    if abs(total - args.target) > 2:
        diff = total - args.target
        print(f"WARNING: {abs(diff):.1f}s {'over' if diff > 0 else 'under'} the {args.target:.0f}s target. "
              f"Trim or extend the script and regenerate only the affected scenes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
