#!/usr/bin/env python3
"""Build the X post text: @_myronera + make.fun play code + short meme copy."""
from __future__ import annotations

import argparse
import os
import re
import sys

from jokes import JOKES

MENTION = "@_myronera"
CODE_RE = re.compile(r"^[A-Z0-9]{2,10}(-[A-Z0-9]{4}){1,3}$")
MAX_LEN = 280


def build(joke: str, play_code: str) -> str:
    if joke not in JOKES:
        raise SystemExit(f"unknown joke '{joke}'. choose one of: {', '.join(JOKES)}")
    if not CODE_RE.match(play_code or ""):
        raise SystemExit(f"play code '{play_code}' does not look like a make.fun play code (e.g. MF-XXXX-XXXX)")
    top, bottom = JOKES[joke]["top"], JOKES[joke]["bottom"]
    text = f"{top.lower()}\n{bottom.lower()}\n\nbuilt by my agent. play it: {play_code} {MENTION} #makefun"
    if len(text) > MAX_LEN:
        raise SystemExit(f"post text is {len(text)} chars, over X's {MAX_LEN} limit")
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--joke", default="grind", choices=sorted(JOKES))
    ap.add_argument("--play-code", required=True)
    ap.add_argument("--out", default="out/post_text.txt")
    a = ap.parse_args()
    text = build(a.joke, a.play_code)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(f"wrote {a.out} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())