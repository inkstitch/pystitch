from typing import BinaryIO

from .DszReader import z_stitch_encoding_read
from .EmbPattern import EmbPattern


def read(f: BinaryIO, out: EmbPattern, settings=None):
    f.seek(0x100)
    z_stitch_encoding_read(f, out)
