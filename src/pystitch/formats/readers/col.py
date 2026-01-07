from typing import TextIO
from ...core.pattern import EmbPattern
from ...core.thread import EmbThread

READ_FILE_IN_TEXT_MODE = True


def read(f: TextIO, out: EmbPattern, settings=None):
    count = int(f.readline())
    for i in range(0, count):
        line = f.readline()
        splits = line.split(",")
        thread = EmbThread()
        thread.catalog_number = splits[0]
        thread.set_color(int(splits[1]), int(splits[2]), int(splits[3]))
        out.add_thread(thread)
