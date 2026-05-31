
import unittest
import tempfile

from test.pattern_for_tests import *
from pystitch import *


class TestWrites(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_write_png(self):
        pattern = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".png") as fp:
            write_png(pattern, fp, {"background": "#F00", "linewidth": 5})

    def test_write_fancy_png(self):
        pattern = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".png") as fp:
            write_png(pattern, fp, {"background": "#F00", "linewidth": 5, "fancy": True})

    def test_write_guides_png(self):
        pattern = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".png") as fp:
            write_png(pattern, fp, {"background": "#F00", "linewidth": 5, "guides": True})

    def test_write_fancy_guides_png(self):
        pattern = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".png") as fp:
            write_png(pattern, fp, {"background": "#F00", "linewidth": 5, "fancy": True,  "guides": True})

    def test_write_dst_read_dst(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".dst") as fp:
            write_dst(pattern, fp)
            dst_pattern = read_dst(fp)
        self.assertEqual(len(dst_pattern.threadlist), 0)
        self.assertEqual(dst_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(dst_pattern.stitches, 0, -1)
        print("dst: ", dst_pattern.stitches)

    def test_write_exp_read_exp(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".exp") as fp:
            write_exp(pattern, fp)
            exp_pattern = read_exp(fp)
        self.assertEqual(len(exp_pattern.threadlist), 0)
        self.assertEqual(exp_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(exp_pattern)
        self.assertEqual(exp_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(exp_pattern.stitches, 0, -1)
        print("exp: ", exp_pattern.stitches)

    def test_write_vp3_read_vp3(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".vp3") as fp:
            write_vp3(pattern, fp)
            vp3_pattern = read_vp3(fp)
        self.assertEqual(len(vp3_pattern.threadlist), vp3_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(vp3_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(vp3_pattern)
        self.assertEqual(vp3_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(vp3_pattern.stitches, 0, -1)
        print("vp3: ", vp3_pattern.stitches)

    def test_write_jef_read_jef(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".jef") as fp:
            write_jef(pattern, fp)
            jef_pattern = read_jef(fp)
        self.assertEqual(len(jef_pattern.threadlist), jef_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(jef_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(jef_pattern)
        self.assertEqual(jef_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(jef_pattern.stitches, 0, -1)
        print("jef: ", jef_pattern.stitches)

    def test_write_pec_read_pec(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".pec") as fp:
            write_pec(pattern, fp)
            pec_pattern = read_pec(fp)
        self.assertEqual(len(pec_pattern.threadlist), pec_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(pec_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(pec_pattern)
        self.assertEqual(pec_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(pec_pattern.stitches, 0, -1)
        print("pec: ", pec_pattern.stitches)

    def test_write_pes_read_pes(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".pes") as fp:
            write_pes(pattern, fp)
            pes_pattern = read_pes(fp)
        self.assertEqual(len(pes_pattern.threadlist), pes_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(pes_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(pes_pattern)
        self.assertEqual(pes_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(pes_pattern.stitches, 0, -1)
        print("pes: ", pes_pattern.stitches)

    def test_write_xxx_read_xxx(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".xxx") as fp:
            write_xxx(pattern, fp)
            pattern = read_xxx(fp)
        self.assertEqual(len(pattern.threadlist), pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(pattern.stitches, 0, -1)
        print("xxx: ", pattern.stitches)

    def test_write_u01_read_u01(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(pattern, fp)
            u01_pattern = read_u01(fp)
        self.assertEqual(len(u01_pattern.threadlist), 0)
        self.assertEqual(u01_pattern.count_stitch_commands(NEEDLE_SET), 16)
        self.assertIsNotNone(u01_pattern)
        self.assertEqual(u01_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(u01_pattern.stitches, 0, -1)
        print("u01: ", u01_pattern.stitches)

    def test_write_csv_read_csv(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".csv") as fp:
            write_csv(pattern, fp, {"encode": True})
            csv_pattern = read_csv(fp)
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(len(csv_pattern.threadlist), csv_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)

    def test_write_gcode_read_gcode(self):
        pattern = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".gcode") as fp:
            write_gcode(pattern, fp)
            gcode_pattern = read_gcode(fp)
        self.assertIsNotNone(gcode_pattern)
        thread_count = len(gcode_pattern.threadlist)
        change_count = gcode_pattern.count_stitch_commands(COLOR_CHANGE) + 1
        print(thread_count)
        print(change_count)

        self.assertEqual(thread_count, change_count)
        self.assertEqual(gcode_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(gcode_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(gcode_pattern.stitches, 0, -1)

    def test_write_txt(self):
        pattern1 = get_big_pattern()
        pattern2 = get_big_pattern()
        with tempfile.NamedTemporaryFile(suffix=".txt") as fp:
            write_txt(pattern1, fp)
            write_txt(pattern2, fp, {"mimic": True})

    def test_write_pes_mismatched(self):
        pattern = EmbPattern()
        pattern += "red"
        pattern += "red"
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += COLOR_CHANGE
        pattern += (100, 0), (0, 100)
        pattern += COLOR_CHANGE
        pattern += (0, 0), (100, 100)
        pattern += COLOR_CHANGE
        pattern += (100, 0), (0, 100)
        with tempfile.NamedTemporaryFile(suffix=".pes") as fp:
            write_pes(pattern, fp, {"version": "6t"})
            write_pes(pattern, fp)

    def test_pes_writes_stop(self):
        """Test if pes can read/write a stop command."""
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        pattern += "blue"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        with tempfile.NamedTemporaryFile(suffix=".pes") as fp:
            write_pes(pattern, fp, {"version": "6t"})
            loaded = read_pes(fp)
        self.assertEqual(pattern.count_stitch_commands(STOP), 2)
        self.assertEqual(pattern.count_stitch_commands(COLOR_CHANGE), 1)
        self.assertEqual(pattern.count_threads(), 2)
        self.assertEqual(loaded.count_stitch_commands(STOP), 2)
        self.assertEqual(loaded.count_stitch_commands(COLOR_CHANGE), 1)
        self.assertEqual(loaded.count_threads(), 2)
