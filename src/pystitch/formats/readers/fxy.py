from typing import BinaryIO

from .dsz import z_stitch_encoding_read
from ...core.pattern import EmbPattern


def read(f: BinaryIO, out: EmbPattern, settings=None):
    f.seek(0x100)
    z_stitch_encoding_read(f, out)
