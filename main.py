#!/usr/bin/env python3
"""Entry program for news-image-20261118.

Copies the front-page image (entry.png, shipped beside this file)
byte-for-byte to the output location. The output directory comes from
$MAKEFUN_OUTPUT_DIR: it may name a directory (the image is written
inside it as entry.png) or a file path ending in entry.png. The output
directory is created if needed; it is never deleted, and only its
contents are ever touched. No network, no timestamps, no randomness:
two runs write identical bytes.
"""

import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def resolve_output():
    target = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    if target.endswith("entry.png"):
        return target
    return os.path.join(target, "entry.png")


def main():
    out_path = resolve_output()
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    with open(SOURCE, "rb") as fh:
        expected = hashlib.sha256(fh.read()).hexdigest()
    shutil.copyfile(SOURCE, out_path)
    with open(out_path, "rb") as fh:
        actual = hashlib.sha256(fh.read()).hexdigest()
    if actual != expected:
        print("error: copied file does not match entry.png", file=sys.stderr)
        return 1
    size = os.path.getsize(out_path)
    print("wrote %s (%d bytes, sha256 %s)" % (out_path, size, actual))
    return 0


if __name__ == "__main__":
    sys.exit(main())
