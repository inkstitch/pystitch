from pathlib import Path
import unittest

import pystitch

DATA = Path(__file__).parent / "data"


def stitch_positions(pattern):
    return [
        (x, y)
        for x, y, command in pattern.stitches
        if command & pystitch.COMMAND_MASK == pystitch.STITCH
    ]


# triangle.dst was written by pystitch; triangle.zhs is the same design exported
# from EZ Design as ZHS, so their stitch positions must match exactly. ZHS deltas
# are plain signed bytes: an earlier version of this reader added 1 to x or y
# deltas of 63 or more and subtracted 1 from those of -63 or less.
class TestReadZhs(unittest.TestCase):
    def test_read_zhs_matches_source_dst(self):
        source = pystitch.read(DATA / "triangle.dst")
        pattern = pystitch.read(DATA / "triangle.zhs")
        self.assertEqual(stitch_positions(pattern), stitch_positions(source))

    def test_read_zhs_bounds_match_source_dst(self):
        source = pystitch.read(DATA / "triangle.dst")
        pattern = pystitch.read(DATA / "triangle.zhs")
        self.assertEqual(pattern.bounds(), source.bounds())
