from typing import BinaryIO

from .EmbPattern import EmbPattern
from .ReadHelper import signed8


def read_exp_stitches(f: BinaryIO, out: EmbPattern):
    # Bulk-read all stitch data
    raw = f.read()
    data_len = len(raw)
    if data_len < 2:
        out.end()
        return

    # Local references for speed
    stitch = out.stitch
    move = out.move
    trim_fn = out.trim
    color_change = out.color_change

    offset = 0
    while offset <= data_len - 2:
        b0 = raw[offset]
        b1 = raw[offset + 1]
        offset += 2

        if b0 != 0x80:
            x = signed8(b0)
            y = -signed8(b1)
            stitch(x, y)
            continue

        control = b1
        if offset > data_len - 2:
            break
        b0 = raw[offset]
        b1 = raw[offset + 1]
        offset += 2

        x = signed8(b0)
        y = -signed8(b1)
        if control == 0x80:  # Trim
            trim_fn()
            continue
        elif control == 0x02:
            stitch(x, y)
            continue
        elif control == 0x04:  # Jump
            move(x, y)
            continue
        elif control == 0x01:  # Colorchange
            color_change()
            if x != 0 or y != 0:
                move(x, y)
            continue
        break  # Uncaught Control
    out.end()


def read(f: BinaryIO, out: EmbPattern, settings=None):
    read_exp_stitches(f, out)
