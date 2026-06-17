from pathlib import Path
import tempfile
import unittest

from test.pattern_for_tests import get_shift_pattern, get_simple_pattern, get_random_pattern_small_halfs, get_random_pattern_large

from pystitch import *
from pystitch import EmbPattern, EmbThread
from pystitch import encode_thread_change, decode_embroidery_command


class TestEmbpattern(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_thread_reorder(self):
        shift = get_shift_pattern()
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, thread=1, order=0))
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, 0, None, 1))
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, 1, None, 0))
        self.assertEqual(0xFFFFFF & shift.threadlist[0].color, 0xFF0000)
        self.assertEqual(0xFFFFFF & shift.threadlist[1].color, 0x0000FF)
        with tempfile.NamedTemporaryFile(suffix=".pes") as fp:
            write_pes(shift, fp, {"pes version": 6})
            fp.seek(0)
            read_pattern = read_pes(fp)
        for thread in read_pattern.threadlist:
            print(0xFFFFFF & thread.color)
        self.assertEqual((0xFFFFFF & read_pattern.threadlist[0].color), 0x0000FF)
        self.assertEqual((0xFFFFFF & read_pattern.threadlist[1].color), 0xFF0000)

    def test_needle_count_limited_set(self):
        shift = get_shift_pattern()
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, None, 6, 0))
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, 4, 6, 7))
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, None, 3, 0))
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 7})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        self.assertEqual(needle_pattern.count_stitch_commands(NEEDLE_SET), 16)
        first = True
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            print(cmd)
            if first:
                # self.assertEqual(cmd[2], 3)
                first = False
            self.assertLessEqual(cmd[2], 7)

    def test_needle_count_limit1(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 1})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        self.assertEqual(needle_pattern.count_stitch_commands(STOP), 16)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLess(cmd[2], 1)

    def test_needle_count_limit2(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 2})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 2)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)

    def test_needle_count_limit3(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 3})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 3)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)

    def test_needle_count_limit4(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 4})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 4)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)

    def test_needle_count_limit5(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 5})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 5)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)

    def test_needle_count_limit6(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 6})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 6)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)

    def test_needle_count_limit7(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 7})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 7)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)

    def test_needle_count_limit8(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 8})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 8)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)

    def test_needle_count_limit9(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 9})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 9)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)

    def test_needle_count_limit10(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 10})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 10)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)

    def test_u01_tie_on(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(shift, fp, {"needle_count": 10, "tie_on": CONTINGENCY_TIE_ON_THREE_SMALL})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 10)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.assertEqual(needle_pattern.count_stitch_commands(STITCH), 16 * (5 + 4))
        # 5 for the actual stitch pattern. 3 small, and 1 extra tieon, start.

    def test_u01_tie_off(self):
        shift = get_shift_pattern()
        with tempfile.NamedTemporaryFile(suffix=".u01") as fp:
            write_u01(get_shift_pattern(), fp, {"needle_count": 10, "tie_off": CONTINGENCY_TIE_OFF_THREE_SMALL})
            fp.seek(0)
            needle_pattern = read_u01(fp)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 10)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.assertEqual(needle_pattern.count_stitch_commands(STITCH), 16 * (5 + 4))
        # 5 for the actual stitch pattern. 3 small, and 1 extra tieoff, end.

    def test_write_dst_read_dst_long_jump(self):
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 200)], "red")

        with tempfile.NamedTemporaryFile(suffix=".dst") as fp:
            write_dst(pattern, fp)
            fp.seek(0)
            dst_pattern = read_dst(fp)

        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 2)
        self.assertEqual(dst_pattern.stitches[1][1], 100)
        print("dst: ", dst_pattern.stitches)

    def test_write_dst_read_dst_random_stitch(self):
        with tempfile.NamedTemporaryFile(suffix=".dst") as fp:
            for i in range(0, 12):
                max = (i * 10) + 1
                pattern = get_random_pattern_small_halfs()
                write_dst(pattern, fp,
                        {"long_stitch_contingency": CONTINGENCY_LONG_STITCH_SEW_TO, "max_stitch": max})
                fp.seek(0)
                dst_pattern = read_dst(fp)
                xx = 0
                yy = 0
                command = NO_COMMAND
                for stitch in dst_pattern.stitches:
                    dx = stitch[0] - xx
                    dy = stitch[1] - yy
                    xx += dx
                    yy += dy
                    last_command = command
                    command = stitch[2] & COMMAND_MASK
                    if command == STITCH and last_command == STITCH:
                        self.assertLessEqual(dx, max)
                        self.assertLessEqual(dy, max)
                self.assertIsNotNone(dst_pattern)

    def test_write_dst_read_dst_long_jump_random_small(self):
        with tempfile.NamedTemporaryFile(suffix=".dst") as fp:
            for i in range(0, 1000):
                pattern = get_random_pattern_small_halfs()
                write_dst(pattern, fp,
                        {"long_stitch_contingency": CONTINGENCY_LONG_STITCH_SEW_TO})
                fp.seek(0)
                dst_pattern = read_dst(fp)
                self.assertIsNotNone(dst_pattern)

    def test_write_dst_read_dst_long_jump_random_large(self):
        with tempfile.NamedTemporaryFile(suffix=".dst") as fp:
            for i in range(0, 5):
                pattern = get_random_pattern_large()
                write_dst(pattern, fp,
                        {"long_stitch_contingency": CONTINGENCY_LONG_STITCH_SEW_TO})
                fp.seek(0)
                dst_pattern = read_dst(fp)
                self.assertIsNotNone(dst_pattern)

    def test_write_dst_read_dst_divide(self):
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 2)], "red")

        with tempfile.NamedTemporaryFile(suffix=".dst") as fp:
            write_dst(pattern, fp, {"scale": 100, "long_stitch_contingency": CONTINGENCY_LONG_STITCH_SEW_TO})
            fp.seek(0)
            dst_pattern = read_dst(fp)

        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 3)
        self.assertEqual(dst_pattern.stitches[1][1], 100)
        print("dst: ", dst_pattern.stitches)

    def test_write_csv_read_csv_raw(self):
        pattern = get_simple_pattern()
        with tempfile.TemporaryDirectory() as tmpdirname:
            file1 = Path(tmpdirname) / "file.csv"
            write_csv(pattern, file1)
            csv_pattern = read_csv(file1)
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_BREAK), 3)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)

    def test_write_csv_read_csv_needle(self):
        pattern = get_simple_pattern()
        with tempfile.TemporaryDirectory() as tmpdirname:
            file2 = Path(tmpdirname) / "file2.csv"
            write_csv(pattern, file2, {"thread_change_command": NEEDLE_SET, "encode": True})
            csv_pattern = read_csv(file2)
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(NEEDLE_SET), 3)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        print("csv: ", csv_pattern.stitches)

    def test_write_csv_read_csv_color(self):
        pattern = get_simple_pattern()
        with tempfile.TemporaryDirectory() as tmpdirname:
            file3 = Path(tmpdirname) / "file3.csv"
            write_csv(pattern, file3, {"thread_change_command": COLOR_CHANGE, "encode": True})
            csv_pattern = read_csv(file3)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_CHANGE), 2)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)

    def test_write_csv_read_csv_encoded_command(self):
        pattern = EmbPattern()
        encoded_command = encode_thread_change(SET_CHANGE_SEQUENCE, 3, 4, 1)
        pattern.add_command(encoded_command)
        with tempfile.TemporaryDirectory() as tmpdirname:
            file1 = Path(tmpdirname) / "file-encoded.csv"
            write_csv(pattern, file1)
            csv_pattern = read_csv(file1)
        self.assertIsNotNone(csv_pattern)
        print("csv-encoded: ", csv_pattern.stitches)
        self.assertEqual(encoded_command, csv_pattern.stitches[-1][2])

    def test_issue_87(self):
        """
        Initial test raised by issue 87.
        """
        pattern = EmbPattern()
        stitches_1 = [[0, 1], [2, 3]]
        stitches_2 = [[4, 5], [6, 7]]
        pattern.add_block(stitches_1, 0xFF0000)
        pattern.add_block(stitches_2, 0x0000FF)
        blocks = list(pattern.get_as_colorblocks())
        for q in blocks:
            print(q)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(len(blocks[0][0]), 2)  # 0,1 and 2,3
        self.assertEqual(len(blocks[1][0]), 2)  # 4,5 and 6,7

    def test_issue_87_2(self):
        """
        Tests a pattern arbitrarily starting with a color change.
        With two predefined blocks. The blocks should maintain their blockness.
        The color change should isolate 0 stitches, of an unknown color.
        :return:
        """
        pattern = EmbPattern()
        stitches_1 = [[0, 1], [2, 3]]
        stitches_2 = [[4, 5], [6, 7]]

        pattern.color_change()
        pattern.add_thread('random')
        pattern.add_block(stitches_1, 0xFF0000)
        pattern.add_block(stitches_2, 0x0000FF)
        blocks = list(pattern.get_as_colorblocks())
        # for q in blocks:
        #     print(q)
        self.assertEqual(blocks[1][1].color, 0xFF0000)
        self.assertEqual(blocks[2][1].color, 0x0000FF)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(len(blocks[0][0]), 1)
        self.assertEqual(len(blocks[1][0]), 2)
        self.assertEqual(len(blocks[2][0]), 2)

        for block in blocks:
            stitch_block = block[0]
            for stitch in stitch_block:
                self.assertNotEqual(stitch[2], COLOR_BREAK)

        pattern = EmbPattern()
        pattern.add_thread('random')
        pattern.color_change()  # end block 1, empty
        pattern.add_thread(0xFF0000)
        pattern += stitches_1
        pattern.color_change()  # end block 2
        pattern.add_thread(0x0000FF)
        pattern += stitches_2
        blocks = list(pattern.get_as_colorblocks())
        # end block 3, no explicit end.
        # for q in blocks:
        #     print(q)
        self.assertEqual(blocks[0][0][-1][2], COLOR_CHANGE)  # Color change ends the block.
        self.assertEqual(blocks[1][0][-1][2], COLOR_CHANGE)  # Color change ends the block.
        self.assertEqual(blocks[1][1].color, 0xFF0000)
        self.assertEqual(blocks[2][1].color, 0x0000FF)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(len(blocks[0][0]), 1)
        self.assertEqual(len(blocks[1][0]), 3)
        self.assertEqual(len(blocks[2][0]), 2)  # Final color change is part of no block.
        pattern.color_change()  # end block 3
        blocks = list(pattern.get_as_colorblocks())
        self.assertEqual(len(blocks[2][0]), 3) # Final block with colorchange.

    def test_issue_87_3(self):
        """
        Tests a pattern arbitrarily starting with a needle_set.
        With two predefined blocks. The blocks should maintain their blockness.
        The needle set should not contribute a block. Initial needle_set, only
        define a starting needle.
        :return:
        """
        pattern = EmbPattern()
        pattern.needle_change()
        stitches_1 = [[0, 1], [2, 3]]
        stitches_2 = [[4, 5], [6, 7]]
        pattern.add_block(stitches_1, 0xFF0000)
        pattern.add_block(stitches_2, 0x0000FF)
        blocks = list(pattern.get_as_colorblocks())
        # for q in blocks:
        #     print(q)
        self.assertEqual(blocks[0][1], 0xFF0000)
        self.assertEqual(blocks[1][1], 0x0000FF)
        self.assertEqual(len(blocks), 2)
        for block in blocks:
            stitch_block = block[0]
            for stitch in stitch_block:
                self.assertNotEqual(stitch[2], COLOR_BREAK)

        pattern = EmbPattern()

        pattern.needle_change()  # start block 0
        pattern += stitches_1
        pattern.add_thread(EmbThread(0xFF0000))

        pattern.needle_change()  # start block 1
        pattern += stitches_1
        pattern.add_thread(EmbThread(0x0000FF))

        pattern.needle_change()  # start block 2
        pattern.add_thread(EmbThread('random'))

        blocks = list(pattern.get_as_colorblocks())
        for q in blocks:
            print(q)
        # Mask is required here since needle_set automatically appends extended data.
        self.assertEqual(blocks[0][0][0][2] & COMMAND_MASK, NEEDLE_SET)  # Needle_set starts the block.
        self.assertEqual(blocks[1][0][0][2] & COMMAND_MASK, NEEDLE_SET)  # Needle_set starts the block.
        self.assertEqual(blocks[0][1], 0xFF0000)
        self.assertEqual(blocks[1][1], 0x0000FF)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(len(blocks[0][0]), 3)
        self.assertEqual(len(blocks[1][0]), 3)
        self.assertEqual(len(blocks[2][0]), 1)

    def test_issue_87_4(self):
        """
        Tests a pattern arbitrarily starting with a color break.
        With two predefined blocks. The blocks should maintain their blockness.
        And ending with another arbitrary color break. This should give exactly
        2 blocks which were defined as prepended colorbreaks postpended color breaks
        are not to have an impact.
        :return:
        """
        pattern = EmbPattern()
        pattern += COLOR_BREAK
        stitches_1 = [[0, 1], [2, 3]]
        stitches_2 = [[4, 5], [6, 7]]
        pattern.add_block(stitches_1, 0xFF0000)
        pattern.add_block(stitches_2, 0x0000FF)
        pattern += COLOR_BREAK
        blocks = list(pattern.get_as_colorblocks())
        for q in blocks:
            print(q)

        for block in blocks:
            stitch_block = block[0]
            for stitch in stitch_block:
                self.assertNotEqual(stitch[2], COLOR_BREAK)
        self.assertEqual(blocks[0][1], 0xFF0000)
        self.assertEqual(blocks[1][1], 0x0000FF)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(len(blocks[0][0]), 2)
        self.assertEqual(len(blocks[1][0]), 2)
