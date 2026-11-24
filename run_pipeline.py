#!/usr/bin/env python3
"""Orchestrate: render meme + build post text, then remind about manual steps."""
from __future__ import annotations

import argparse
import subprocess
import sys

MANUAL_STEPS = """
NEXT STEPS (manual, by the entrant):
1. Review out/meme.png (or .jpg if PNG exceeded 5MB) and out/post_text.txt.
2. Post from the PUBLIC X account at/after the bounty opening, before the deadline.
   Attach the image; post text already contains @_myronera and the play code.
3. Keep the post up. No bought engagement, bots, or pods.
4. Save the URL to out/post_url.txt.
5. Bundle transcripts with the OFFICIAL kit CLI from the unpacked kit:
     node cli/makefun.mjs bundle --session <log.json> --redact "<personal detail>"
     node cli/makefun.mjs check <bundle.tar.gz>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--joke", default="grind", choices=["grind", "paid", "leaderboard", "bugs", "deploy"])
    ap.add_argument("--play-code", required=True)
    ap.add_argument("--outdir", default="out")
    a = ap.parse_args()

    py = sys.executable
    r1 = subprocess.run([py, "generate_meme.py", "--joke", a.joke, "--out", f"{a.outdir}/meme.png"])
    if r1.returncode:
        return r1.returncode
    r2 = subprocess.run([py, "post_text.py", "--joke", a.joke, "--play-code", a.play_code, "--out", f"{a.outdir}/post_text.txt"])
    if r2.returncode:
        return r2.returncode
    r3 = subprocess.run([py, "validate_entry.py", "--image", f"{a.outdir}/meme.png", "--text", f"{a.outdir}/post_text.txt", "--play-code", a.play_code])
    if r3.returncode:
        return r3.returncode
    print(MANUAL_STEPS)
    return 0


if __name__ == "__main__":
    sys.exit(main())