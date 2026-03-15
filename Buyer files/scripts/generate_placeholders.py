#!/usr/bin/env python3
"""Generate simple PNG placeholder images of arbitrary size.

This script does not depend on external libraries. It writes a solid background
and draws the provided size label in a very simple bitmap font.

Usage:
  python3 generate_placeholders.py 460x991 300x250

It will write files under "../assets/img/placeholders" relative to this script.
"""

import os
import sys
import zlib

# Basic 5x7 font for digits and 'x' and 'X'
FONT = {
    "0": [0b01110,
          0b10001,
          0b10011,
          0b10101,
          0b11001,
          0b10001,
          0b01110],
    "1": [0b00100,
          0b01100,
          0b00100,
          0b00100,
          0b00100,
          0b00100,
          0b01110],
    "2": [0b01110,
          0b10001,
          0b00001,
          0b00010,
          0b00100,
          0b01000,
          0b11111],
    "3": [0b01110,
          0b10001,
          0b00001,
          0b00110,
          0b00001,
          0b10001,
          0b01110],
    "4": [0b00010,
          0b00110,
          0b01010,
          0b10010,
          0b11111,
          0b00010,
          0b00010],
    "5": [0b11111,
          0b10000,
          0b11110,
          0b00001,
          0b00001,
          0b10001,
          0b01110],
    "6": [0b00110,
          0b01000,
          0b10000,
          0b11110,
          0b10001,
          0b10001,
          0b01110],
    "7": [0b11111,
          0b00001,
          0b00010,
          0b00100,
          0b01000,
          0b01000,
          0b01000],
    "8": [0b01110,
          0b10001,
          0b10001,
          0b01110,
          0b10001,
          0b10001,
          0b01110],
    "9": [0b01110,
          0b10001,
          0b10001,
          0b01111,
          0b00001,
          0b00010,
          0b01100],
    "x": [0b10001,
          0b01010,
          0b00100,
          0b00100,
          0b00100,
          0b01010,
          0b10001],
    "X": [0b10001,
          0b01010,
          0b00100,
          0b00100,
          0b00100,
          0b01010,
          0b10001],
    " ": [0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000,
          0b00000],
}


def make_png(width: int, height: int, label: str, out_path: str) -> None:
    """Create a simple PNG image file with a solid background and centered label."""

    # Background and text colors
    bg = (200, 200, 200)
    fg = (40, 40, 40)
    border = (120, 120, 120)

    # Build the pixel buffer (RGBA)
    row = bytearray()
    pixels = bytearray()

    # Determine font scaling
    scale = max(1, min(width // (len(label) * 6), height // 10))
    font_w = 5
    font_h = 7
    text_w = len(label) * (font_w + 1) * scale - scale
    text_h = font_h * scale
    text_x = max(0, (width - text_w) // 2)
    text_y = max(0, (height - text_h) // 2)

    def pixel(x: int, y: int) -> tuple[int, int, int, int]:
        # border
        if x < 1 or y < 1 or x >= width - 1 or y >= height - 1:
            return (*border, 255)
        # text
        if text_x <= x < text_x + text_w and text_y <= y < text_y + text_h:
            tx = (x - text_x) // scale
            ty = (y - text_y) // scale
            char_i = tx // (font_w + 1)
            if char_i < len(label):
                cx = tx % (font_w + 1)
                ch = label[char_i]
                glyph = FONT.get(ch, FONT.get(" "))
                if cx < font_w and 0 <= ty < font_h:
                    bit = (glyph[ty] >> (font_w - 1 - cx)) & 1
                    if bit:
                        return (*fg, 255)
        return (*bg, 255)

    for y in range(height):
        pixels.extend(bytes([0]))  # filter type 0
        for x in range(width):
            r, g, b, a = pixel(x, y)
            pixels.extend(bytes([r, g, b, a]))

    def png_chunk(chunk_type: bytes, data: bytes) -> bytes:
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xFFFFFFFF
        return len(data).to_bytes(4, 'big') + chunk + crc.to_bytes(4, 'big')

    png = bytearray(b"\x89PNG\r\n\x1a\n")
    # IHDR
    ihdr_data = (
        width.to_bytes(4, 'big') +
        height.to_bytes(4, 'big') +
        bytes([8, 6, 0, 0, 0])  # 8-bit, RGBA, deflate, no filter, no interlace
    )
    png.extend(png_chunk(b'IHDR', ihdr_data))

    # IDAT
    compressor = zlib.compressobj()
    compressed = compressor.compress(bytes(pixels)) + compressor.flush()
    png.extend(png_chunk(b'IDAT', compressed))

    # IEND
    png.extend(png_chunk(b'IEND', b''))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'wb') as f:
        f.write(png)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("Usage: generate_placeholders.py 460x991 300x200 ...")
        return 1

    out_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "placeholders")
    os.makedirs(out_dir, exist_ok=True)

    for size in argv:
        if 'x' not in size:
            print(f"Skipping invalid size: {size}")
            continue
        w_str, h_str = size.split('x', 1)
        try:
            w = int(w_str)
            h = int(h_str)
        except ValueError:
            print(f"Skipping invalid size: {size}")
            continue
        filename = f"placeholder-{w}x{h}.png"
        out_path = os.path.join(out_dir, filename)
        print(f"Generating {out_path} ({w}x{h})")
        make_png(w, h, f"{w}x{h}", out_path)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
