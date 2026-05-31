
import unittest
import tempfile

from test.pattern_for_tests import *


class TestColorFormats(unittest.TestCase):

    def test_write_read_col(self):
        with tempfile.NamedTemporaryFile(suffix=".col") as fp:
            file1 = fp.name
            for m in range(0, 50):
                pattern = EmbPattern()
                for i in range(4, 20):
                    pattern.add_thread(EmbThread("random"))
                write(pattern, file1)
                w_pattern = read(file1)
                self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
                for q in range(0, len(pattern.threadlist)):
                    self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)

    def test_write_read_edr(self):
        with tempfile.NamedTemporaryFile(suffix=".edr") as fp:
            file1 = fp.name
            for m in range(0, 50):
                pattern = EmbPattern()
                for i in range(4, 20):
                    pattern.add_thread(EmbThread("random"))
                write(pattern, file1)
                w_pattern = read(file1)
                self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
                for q in range(0, len(pattern.threadlist)):
                    self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)

    def test_write_read_inf(self):
        with tempfile.NamedTemporaryFile(suffix=".inf") as fp:
            file1 = fp.name
            for m in range(0, 50):
                pattern = EmbPattern()
                for i in range(4, 20):
                    pattern.add_thread(EmbThread("random"))
                write(pattern, file1)
                w_pattern = read(file1)
                self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
                for q in range(0, len(pattern.threadlist)):
                    self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)

    def test_write_edr_dst(self):
        pattern = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".edr") as fp1, \
             tempfile.NamedTemporaryFile(suffix=".dst") as fp2:
            file1 = fp1.name
            file2 = fp2.name
            write(pattern, file1)
            write(pattern, file2)
            w_pattern = read(file1)
            w_pattern = read(file2, pattern=w_pattern)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)

    def test_write_dst_edr(self):
        pattern = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".dst") as fp1, \
             tempfile.NamedTemporaryFile(suffix=".edr") as fp2:
            file1 = fp1.name
            file2 = fp2.name
            write(pattern, file1)
            write(pattern, file2)
            w_pattern = read(file1)
            w_pattern = read(file2, pattern=w_pattern)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)

    def test_write_dst_col(self):
        pattern = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".dst") as fp1, \
             tempfile.NamedTemporaryFile(suffix=".col") as fp2:
            file1 = fp1.name
            file2 = fp2.name
            write(pattern, file1)
            write(pattern, file2)
            w_pattern = read(file1)
            w_pattern = read(file2, pattern=w_pattern)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)

    def test_write_dst_inf(self):
        pattern = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".dst") as fp1, \
             tempfile.NamedTemporaryFile(suffix=".inf") as fp2:
            file1 = fp1.name
            file2 = fp2.name
            write(pattern, file1)
            write(pattern, file2)
            w_pattern = read(file1)
            w_pattern = read(file2, pattern=w_pattern)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)
