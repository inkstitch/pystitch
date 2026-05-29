from pathlib import Path
import tempfile
import unittest

from test.pattern_for_tests import *
import pystitch


class TestExplicitIOErrors(unittest.TestCase):
    def test_read_non_file(self):
        """
        1.5.0 adds explicit error raising.
        We test that now.
        """
        with tempfile.TemporaryDirectory() as tmpdirname:
            file1 = Path(tmpdirname) / "nosuchfile.dst"
            with self.assertRaises(IOError):
                pystitch.read(str(file1))

    def test_write_non_supported(self):
        """
        1.5.0 adds explicit error raising.
        We test that now.
        """
        pattern = get_simple_pattern()
        with tempfile.TemporaryDirectory() as tmpdirname:
            file1 = Path(tmpdirname) / "nosuchfile.pdf"
            with self.assertRaises(IOError):
                pystitch.write(pattern, str(file1))

    def test_write_no_writer(self):
        """
        1.5.0 adds explicit error raising.
        We test that now.
        """
        pattern = get_simple_pattern()
        with tempfile.TemporaryDirectory() as tmpdirname:
            file1 = Path(tmpdirname) / "nosuchfile.dat"
            with self.assertRaises(IOError):
                pystitch.write(pattern, str(file1))
