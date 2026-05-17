from typing import BinaryIO

from pystitch.EmbConstant import (
    COLOR_CHANGE,
    COMMAND_MASK,
    END,
    JUMP,
    STITCH,
    TRIM,
)
from pystitch.EmbPattern import EmbPattern
from pystitch.WriteHelper import write_int_16le, write_int_array_8

HEADER_SIZE = 0x1D78
STITCH_COUNT_OFFSET = 0x32


def write(pattern: EmbPattern, f: BinaryIO, settings=None) -> None:
    """
    Write pattern to SEW-formatted binary buffer.

    https://edutechwiki.unige.ch/en/Embroidery_format
    https://community.kde.org/Projects/Liberty/File_Formats/Janome_Embroidery_Format#SEW_Format
    """
    # Write initial null bytes for header
    f.write(bytes(HEADER_SIZE))
    f.seek(0)

    # Write color count
    color_count = len(pattern.threadlist)
    if color_count > 12:
        raise ValueError("Cannot store more than 12 colors in SEW format")
    write_int_16le(f, color_count)

    # Write index of each color
    for thread in pattern.threadlist:
        if not thread.catalog_number:
            continue
        index = int(thread.catalog_number)
        write_int_16le(f, index)

    # Write stitch count for each color
    f.seek(STITCH_COUNT_OFFSET, 0)
    for block in pattern.get_as_colorblocks():
        stitches, color = block
        # This may produce lower than actual values
        count = len([stitch for stitch in stitches if stitch[2] != COLOR_CHANGE])
        write_int_16le(f, count)

    # Write stitches
    f.seek(HEADER_SIZE, 0)
    xx = yy = 0
    for stitch in pattern.stitches:
        x, y, command = stitch
        command &= COMMAND_MASK
        dx = int(round(x - xx))
        dy = int(round(y - yy))
        xx += dx
        yy += dy
        if command == END:
            break
        elif command == STITCH:
            write_int_array_8(f, [dx, -dy])
        elif command == COLOR_CHANGE:
            write_int_array_8(f, [0x80, 0x01])
            write_int_array_8(f, [0x00, 0x00])
        elif command == TRIM:
            write_int_array_8(f, [0x80, 0x02])
            write_int_array_8(f, [0x00, 0x00])
        elif command == JUMP:
            write_int_array_8(f, [0x80, 0x02])
            write_int_array_8(f, [dx, -dy])

    # End pattern
    write_int_array_8(f, [0x80, 0x10])
