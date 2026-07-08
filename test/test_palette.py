import unittest

from pystitch import EmbPattern, EmbThread
from pystitch.EmbThreadPec import get_thread_set, EmbThreadPec
from pystitch.EmbThread import build_unique_palette, build_nonrepeat_palette, build_palette


class TestPalettes(unittest.TestCase):

    def test_unique_palette(self):
        """Similar elements should not plot to the same palette index"""
        pattern = EmbPattern()
        pattern += "#FF0001"
        pattern += "Blue"
        pattern += "Blue"
        pattern += "Red"
        threadset = get_thread_set()
        palette = build_unique_palette(threadset,pattern.threadlist)
        self.assertNotEqual(palette[0], palette[3], "Red and altered Red")
        self.assertEqual(palette[1], palette[2], "Blue and Blue")

    def test_unique_palette_same_thread_repeated_shares_an_index(self):
        red = EmbThread({"rgb": (255, 0, 0), "name": "Red"})
        threadset = get_thread_set()
        palette = build_unique_palette(threadset, [red, EmbThread(red)])
        self.assertEqual(palette[0], palette[1])

    def test_unique_palette_large(self):
        """Excessive palette entries that all map, should be mapped"""
        pattern = EmbPattern()
        for _ in range(0, 100):
            pattern += "black"
        threadset = get_thread_set()
        palette = build_unique_palette(threadset, pattern.threadlist)
        self.assertEqual(palette[0], palette[1])

    def test_unique_palette_unmap(self):
        """Excessive palette entries can't all map, should map what it can and repeat"""
        pattern = EmbPattern()
        for i in range(0, 100):
            thread = EmbThread()
            thread.set_color(i, i, i)
            pattern += thread
        threadset = get_thread_set()
        palette = build_unique_palette(threadset, pattern.threadlist)
        palette.sort()

    def test_unique_palette_max(self):
        """If the entries equal the list they should all map."""
        pattern = EmbPattern()
        threadset = get_thread_set()
        for i in range(0, len(threadset)-2):
            thread = EmbThread()
            thread.set_color(i, i, i)
            pattern += thread
        palette = build_unique_palette(threadset, pattern.threadlist)
        palette.sort()
        for i in range(1, len(palette)):
            self.assertNotEqual(palette[i-1], palette[i])

    def test_unique_palette_order_invariant(self):
        """thread assignment should not be greedy, it should minimize the total shift of colors.
        i.e just because eggshell comes first and its closest color is white, it shouldn't be
        assigned to white, as there is a better match later in the threadlist (actual white)
        """
        eggshell = EmbThread({"rgb": (255, 255, 245), "name": "Eggshell", "catalog": "0101"})
        white = EmbThread({"rgb": (255, 255, 255), "name": "White", "catalog": "0015"})
        machine_black = EmbThreadPec(0, 0, 0, "Black", "20")
        machine_white = EmbThreadPec(255, 255, 255, "White", "1")
        palette = build_unique_palette([machine_black, machine_white], [eggshell, white])
        self.assertEqual(0, palette[0],
                            "Eggshell should be assigned to the Black thread")
        self.assertEqual(1, palette[1],
                         "White should be assigned to the White thread")

    def test_nonrepeat_palette_moving(self):
        """The almost same color should not get plotted to the same palette index"""
        pattern = EmbPattern()
        pattern += "Red"
        pattern += "Blue"
        pattern += "#0100FF"
        pattern += "Red"
        threadset = get_thread_set()
        palette = build_nonrepeat_palette(threadset,pattern.threadlist)
        self.assertEqual(palette[0], palette[3], "Red and Red")
        self.assertNotEqual(palette[1], palette[2], "Blue and altered Blue")

    def test_nonrepeat_palette_stay_moved(self):
        """An almost same moved, only temporary"""
        pattern = EmbPattern()
        pattern += "Red"
        pattern += "Blue"
        pattern += "#0100FF"
        pattern += "Red"
        pattern += "#0100FF"
        threadset = get_thread_set()
        palette = build_nonrepeat_palette(threadset,pattern.threadlist)
        self.assertEqual(palette[0], palette[3], "Red and Red")
        self.assertNotEqual(palette[1], palette[2], "Blue and altered Blue")
        self.assertNotEqual(palette[2], palette[4], "same color, but color was moved")

    def test_nonrepeat_palette_same(self):
        """The same exact same color if repeated should remain"""
        pattern = EmbPattern()
        pattern += "Red"
        pattern += "Blue"
        pattern += "#0000FF"  # actual blue
        pattern += "Red"
        threadset = get_thread_set()
        palette = build_nonrepeat_palette(threadset,pattern.threadlist)
        self.assertEqual(palette[0], palette[3], "Red and Red")
        self.assertEqual(palette[1], palette[2], "Blue and Blue")

    def test_palette(self):
        """Similar colors map to the same index"""
        pattern = EmbPattern()
        pattern += "#FF0001"
        pattern += "Blue"
        pattern += "Blue"
        pattern += "Red"
        threadset = get_thread_set()
        palette = build_palette(threadset,pattern.threadlist)
        self.assertEqual(palette[0], palette[3], "Red and altered Red")
        self.assertEqual(palette[1], palette[2], "Blue and Blue")
