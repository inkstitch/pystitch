from typing import BinaryIO

from ...core.pattern import EmbPattern
from .exp import read_exp_stitches
from ..read_helper import read_int_32le


def read(f: BinaryIO, out: EmbPattern, settings=None):
    # File starts with STX
    f.seek(0x0C, 1)
    color_start_position = read_int_32le(f)
    dunno_block_start_position = read_int_32le(f)
    stitch_start_position = read_int_32le(f)
    f.seek(stitch_start_position, 0)
    read_exp_stitches(f, out)
