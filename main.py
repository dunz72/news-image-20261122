#!/usr/bin/env python3
"""Copy the finished front page to the harness output directory.

The entry image (entry.png) is stored in this repository, already drawn.
This program does nothing but copy it byte-for-byte to the output
directory the grader expects.

No third-party libraries, no fonts, no network, no clock, no randomness:
Python's standard library only, so it runs in any bare sandbox (the
grader's pinned python image has no Pillow installed).
"""

import hashlib
import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
SOURCE_NAME = "entry.png"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def find_source() -> str:
    """Locate entry.png next to this script, or under MAKEFUN_BOT_DIR."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(here, SOURCE_NAME)
    if os.path.isfile(candidate):
        return candidate
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if bot_dir:
        candidate = os.path.join(bot_dir, SOURCE_NAME)
        if os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError(
        f"{SOURCE_NAME} not found next to {__file__}"
        + (f" or under MAKEFUN_BOT_DIR={bot_dir}" if bot_dir else "")
    )


def main() -> int:
    source_path = find_source()
    with open(source_path, "rb") as handle:
        data = handle.read()

    if data[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        raise ValueError(f"{source_path}: not a PNG file (bad signature)")
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"{source_path}: {len(data)} bytes exceeds limit {MAX_BYTES}"
        )

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, SOURCE_NAME)
    with open(out_path, "wb") as handle:
        handle.write(data)

    # Verify the copy byte-for-byte: re-read what was written and compare
    # digests, so a truncated or corrupted write fails loudly instead of
    # silently submitting a broken image.
    with open(out_path, "rb") as handle:
        written = handle.read()
    source_digest = sha256_hex(data)
    if sha256_hex(written) != source_digest:
        raise ValueError(f"{out_path}: copy does not match {source_path}")

    print("wrote", out_path, len(data), "bytes", "sha256", source_digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
