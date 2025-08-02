import unittest

from test.pattern_for_tests import *
import pystitch


class TestExplicitIOErrors(unittest.TestCase):
    def test_read_non_file(self):
        """
        1.5.0 adds explicit error raising.
        We test that now.
        """
        file1 = "nosuchfile.dst"
        self.assertRaises(IOError, lambda: pystitch.read(file1))

    def test_write_non_supported(self):
        """
        1.5.0 adds explicit error raising.
        We test that now.
        """
        pattern = get_simple_pattern()
        file1 = "nosuchfile.pdf"
        self.assertRaises(IOError, lambda: pystitch.write(pattern, file1))

    def test_write_no_writer(self):
        """
        1.5.0 adds explicit error raising.
        We test that now.
        """
        pattern = get_simple_pattern()
        file1 = "nosuchfile.dat"
        self.assertRaises(IOError, lambda: pystitch.write(pattern, file1))
