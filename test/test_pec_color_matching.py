import io
import unittest

from pystitch import EmbPattern, EmbThread, write_pec
from pystitch.PecReader import read_pec


def pattern_with_blocks(threads):
    pattern = EmbPattern()
    for thread in threads:
        pattern.add_block([(0, 0), (0, 100), (100, 100)], thread)
    return pattern


def write_then_read_pec(pattern):
    stream = io.BytesIO()
    write_pec(pattern, stream)
    stream.seek(8)  # skip the "#PEC0001" signature; read_pec starts at "LA:"
    result = EmbPattern()
    read_pec(stream, result)
    return result


class TestPecColorMatching(unittest.TestCase):

    def test_eggshell_then_white_is_not_swapped(self):
        eggshell = EmbThread({"rgb": (255, 255, 245), "name": "Eggshell", "catalog": "0101"})
        white = EmbThread({"rgb": (255, 255, 255), "name": "White", "catalog": "0015"})
        pattern = write_then_read_pec(pattern_with_blocks([eggshell, white]))
        self.assertEqual(len(pattern.threadlist), 2)
        self.assertNotEqual(pattern.threadlist[0].description, "White",  # it's Flesh Pink instead
                            "the Eggshell block should be shown as an off-white, not White")
        self.assertEqual(pattern.threadlist[1].description, "White",
                         "the White block should be shown as White")

    def test_same_thread_repeated_shares_an_index(self):
        red = EmbThread({"rgb": (255, 0, 0), "name": "Red"})
        pattern = write_then_read_pec(pattern_with_blocks([red, EmbThread(red)]))
        self.assertEqual(len(pattern.threadlist), 2)
        self.assertEqual(pattern.threadlist[0].description, pattern.threadlist[1].description)


if __name__ == "__main__":
    unittest.main()
