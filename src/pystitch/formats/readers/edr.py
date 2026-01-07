from typing import BinaryIO

from ...core.pattern import EmbPattern
from ...core.thread import EmbThread
from ..read_helper import read_int_8


def read(f: BinaryIO, out: EmbPattern, settings=None):
    while True:
        red = read_int_8(f)
        green = read_int_8(f)
        blue = read_int_8(f)
        if blue is None:
            return
        f.seek(1, 1)
        thread = EmbThread()
        thread.set_color(red, green, blue)
        out.add_thread(thread)
