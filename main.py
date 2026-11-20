#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120.

Copies the front-page image for Friday 20 November 2026 from
assets/entry.png to $MAKEFUN_OUTPUT_DIR/entry.png.

Standard library only: no network, no third-party packages. The run is
deterministic -- the same bytes are written on every run.
"""

import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024


def read_png_size(data):
    """Return (width, height) from a PNG's IHDR chunk, or None."""
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if data[12:16] != b"IHDR":
        return None
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def check_image(path, data):
    """Validate the image bytes against the competition's limits."""
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"{path}: {len(data)} bytes exceeds the 1 MiB limit"
        )
    size = read_png_size(data)
    if size is None:
        raise SystemExit(f"{path}: not a valid PNG file")
    width, height = size
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise SystemExit(
            f"{path}: {width}x{height} exceeds the "
            f"{MAX_DIMENSION}x{MAX_DIMENSION} limit"
        )
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "assets", "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    dest = os.path.join(out_dir, "entry.png")

    with open(source, "rb") as fh:
        data = fh.read()
    width, height = check_image(source, data)

    os.makedirs(out_dir, exist_ok=True)
    with open(dest, "wb") as fh:
        fh.write(data)

    with open(dest, "rb") as fh:
        written = fh.read()
    if written != data:
        raise SystemExit(f"{dest}: written bytes differ from the source")
    check_image(dest, written)

    digest = hashlib.sha256(data).hexdigest()
    print(
        f"entry.png: {width}x{height}, {len(data)} bytes, sha256 {digest}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
