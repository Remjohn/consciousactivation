from __future__ import annotations

import struct
import zlib


def _chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def rgba_png(width: int, height: int, pixel) -> bytes:
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            r,g,b,a = pixel(x,y)
            row.extend((r & 255,g & 255,b & 255,a & 255))
        rows.append(bytes(row))
    raw=b"".join(rows)
    return b"\x89PNG\r\n\x1a\n"+_chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,8,6,0,0,0))+_chunk(b"IDAT",zlib.compress(raw,9))+_chunk(b"IEND",b"")


def gray_png(width: int, height: int, pixel) -> bytes:
    rows=[]
    for y in range(height):
        row=bytearray([0])
        for x in range(width): row.append(pixel(x,y)&255)
        rows.append(bytes(row))
    return b"\x89PNG\r\n\x1a\n"+_chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,8,0,0,0,0))+_chunk(b"IDAT",zlib.compress(b"".join(rows),9))+_chunk(b"IEND",b"")


def dimensions(data: bytes) -> tuple[int,int]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or data[12:16] != b"IHDR":
        raise ValueError("not a PNG")
    return struct.unpack(">II", data[16:24])
