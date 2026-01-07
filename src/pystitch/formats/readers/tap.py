from typing import BinaryIO

from ...core.pattern import EmbPattern
from .dst import dst_read_stitches


def read(f: BinaryIO, out: EmbPattern, settings=None):
    dst_read_stitches(f, out, settings)
