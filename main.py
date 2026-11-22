#!/usr/bin/env python3
"""Copy the baked front-page image to the grader output directory.

Standard library only, no network, no randomness. The image is the
repository's own entry.png, drawn by draw-news-image-20261122.py.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"main.py: error: {message}", file=sys.stderr)
    return 1


def read_png(path):
    try:
        data = path.read_bytes()
    except OSError as exc:
        return None, f"cannot read {path}: {exc}"
    if len(data) < 33:
        return None, "file too short to be a PNG"
    if data[:8] != PNG_MAGIC:
        return None, "not a PNG (bad magic)"
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        return None, f"dimensions {width}x{height} exceed {MAX_DIM}x{MAX_DIM}"
    if len(data) > MAX_BYTES:
        return None, f"size {len(data)} exceeds {MAX_BYTES} bytes"
    if struct.unpack(">I", data[8:12])[0] != 13 or data[12:16] != b"IHDR":
        return None, "first chunk is not IHDR"
    # Walk every chunk: a truncated or trailing-garbage file must fail
    # instead of shipping a PNG a viewer cannot finish decoding.
    pos = 8
    seen_iend = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            return None, f"chunk {ctype!r} at {pos} runs past end of file"
        if ctype == b"IEND":
            if length != 0 or end != len(data):
                return None, "IEND is not the final chunk"
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        return None, "no IEND chunk: file is truncated"
    return data, None


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is not set")
    data, error = read_png(source)
    if error is not None:
        return fail(error)
    dest = Path(out_dir) / "entry.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"main.py: wrote {dest} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
