from pathlib import Path
import unittest
import tempfile

from test.pattern_for_tests import get_shift_pattern

import pystitch
from pystitch import EmbPattern, EmbThread


class TestColorFormats(unittest.TestCase):
    def assertPatternColorsEqual(self, pattern0, pattern1):
        self.assertEqual(len(pattern0.threadlist), len(pattern1.threadlist))
        self.assertEqual(
            [thread.color for thread in pattern0.threadlist],
            [thread.color for thread in pattern1.threadlist],
        )

    def test_write_read_col(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            file1 = Path(tmpdirname) / "color.col"
            for _ in range(50):
                pattern = EmbPattern()
                for _ in range(4, 20):
                    pattern.add_thread(EmbThread("random"))
                pystitch.write(pattern, file1)
                w_pattern = pystitch.read(file1)
                self.assertPatternColorsEqual(pattern, w_pattern)

    def test_write_read_edr(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            file1 = Path(tmpdirname) / "color.edr"
            for _ in range(50):
                pattern = EmbPattern()
                for _ in range(4, 20):
                    pattern.add_thread(EmbThread("random"))
                pystitch.write(pattern, file1)
                w_pattern = pystitch.read(file1)
                self.assertPatternColorsEqual(pattern, w_pattern)

    def test_write_read_inf(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            file1 = Path(tmpdirname) / "color.inf"
            for _ in range(0, 50):
                pattern = EmbPattern()
                for _ in range(4, 20):
                    pattern.add_thread(EmbThread("random"))
                pystitch.write(pattern, file1)
                w_pattern = pystitch.read(file1)
                self.assertPatternColorsEqual(pattern, w_pattern)

    def test_write_edr_dst(self):
        pattern = get_shift_pattern()
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdir = Path(tmpdirname)
            file1 = tmpdir / "color.edr"
            file2 = tmpdir / "color.dst"
            pystitch.write(pattern, file1)
            pystitch.write(pattern, file2)
            w_pattern = pystitch.read(file1)
            w_pattern = pystitch.read(file2, pattern=w_pattern)
        self.assertPatternColorsEqual(pattern, w_pattern)

    def test_write_dst_edr(self):
        pattern = get_shift_pattern()
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdir = Path(tmpdirname)
            file1 = tmpdir / "color.dst"
            file2 = tmpdir / "color.edr"
            pystitch.write(pattern, file1)
            pystitch.write(pattern, file2)
            w_pattern = pystitch.read(file1)
            w_pattern = pystitch.read(file2, pattern=w_pattern)
        self.assertPatternColorsEqual(pattern, w_pattern)

    def test_write_dst_col(self):
        pattern = get_shift_pattern()
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdir = Path(tmpdirname)
            file1 = tmpdir / "color.dst"
            file2 = tmpdir / "color.col"
            pystitch.write(pattern, file1)
            pystitch.write(pattern, file2)
            w_pattern = pystitch.read(file1)
            w_pattern = pystitch.read(file2, pattern=w_pattern)
        self.assertPatternColorsEqual(pattern, w_pattern)

    def test_write_dst_inf(self):
        pattern = get_shift_pattern()
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdir = Path(tmpdirname)
            file1 = tmpdir / "color.dst"
            file2 = tmpdir / "color.inf"
            pystitch.write(pattern, file1)
            pystitch.write(pattern, file2)
            w_pattern = pystitch.read(file1)
            w_pattern = pystitch.read(file2, pattern=w_pattern)
        self.assertPatternColorsEqual(pattern, w_pattern)
