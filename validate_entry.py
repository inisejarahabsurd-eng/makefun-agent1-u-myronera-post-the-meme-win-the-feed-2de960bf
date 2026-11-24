#!/usr/bin/env python3
"""Validate all entry artifacts before submission. Fails non-zero on any issue."""
from __future__ import annotations

import argparse
import os
import re
import sys

from PIL import Image

from post_text import CODE_RE, MENTION, MAX_LEN


def fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", default="out/meme.png")
    ap.add_argument("--text", default="out/post_text.txt")
    ap.add_argument("--play-code", required=True)
    a = ap.parse_args()
    rc = 0

    # image checks
    if not os.path.exists(a.image):
        rc |= fail(f"image missing: {a.image}")
    else:
        size = os.path.getsize(a.image)
        if size > 5 * 1024 * 1024:
            rc |= fail(f"image {size} bytes exceeds X's 5MB upload limit")
        try:
            img = Image.open(a.image)
            w, h = img.size
            if w < 600 or h < 600:
                rc |= fail(f"image {w}x{h} too small to be phone-legible")
            if img.format not in ("PNG", "JPEG"):
                rc |= fail(f"unsupported image format {img.format}; use PNG or JPEG")
            print(f"OK image: {w}x{h} {img.format}, {size} bytes")
        except Exception as e:
            rc |= fail(f"cannot read image: {e}")

    # text checks
    if not os.path.exists(a.text):
        rc |= fail(f"post text missing: {a.text}")
    else:
        text = open(a.text, encoding="utf-8").read().strip()
        if MENTION not in text:
            rc |= fail(f"post text missing required mention {MENTION}")
        if a.play_code not in text:
            rc |= fail(f"post text missing play code {a.play_code}")
        if len(text) > MAX_LEN:
            rc |= fail(f"post text {len(text)} chars exceeds {MAX_LEN}")
        if not CODE_RE.match(a.play_code):
            rc |= fail(f"play code {a.play_code} fails format check")
        # secret scan: naive but useful
        secret_pat = re.compile(r"(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
        if secret_pat.search(text):
            rc |= fail("post text contains what looks like a secret")
        print(f"OK text: {len(text)} chars, mention + play code present")

    print("PASS" if rc == 0 else "VALIDATION FAILED")
    return rc


if __name__ == "__main__":
    sys.exit(main())