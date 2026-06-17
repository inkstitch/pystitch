import tempfile
import unittest

from test.pattern_for_tests import get_big_pattern

from pystitch import *
from pystitch import encode_thread_change, decode_embroidery_command
from pystitch import write_u01, read_u01


class TestDataPreservation(unittest.TestCase):

    def test_preserve_u01_needles(self):
        pattern = get_big_pattern()
        pattern.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, None, 6, 0))

        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(pattern, fp)
            read_pattern = read_u01(fp)

        for cmd in read_pattern.get_match_commands(NEEDLE_SET):
            print(decode_embroidery_command(cmd[2]))
