#!/usr/bin/env python3
"""Entry point for make.fun news-image-20261126 (b167, V163 ATLAS BANNER).

Stdlib only: the grader runs with the standard library and nothing else,
so this file imports os/shutil only and copies the pre-rendered entry.png
(build-time, rendered by gen.py with Pillow) into the output directory.
The destination is always $MAKEFUN_OUTPUT_DIR/entry.png (default "out"),
never next to this file: the grader's repo copy is read-only.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py: " + src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote " + dst)


if __name__ == "__main__":
    main()
