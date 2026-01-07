from typing import BinaryIO

from .EmbPattern import EmbPattern
from .DstReader import dst_read_stitches


def read(f: BinaryIO, out: EmbPattern, settings=None):
    dst_read_stitches(f, out, settings)
