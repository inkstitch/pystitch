from typing import BinaryIO

from .dst import dst_read_stitches
from ...core.pattern import EmbPattern


def read(f: BinaryIO, out: EmbPattern, settings=None):
    f.seek(0x100)
    dst_read_stitches(f, out, settings)
