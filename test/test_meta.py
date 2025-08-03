import unittest
from pathlib import Path
import os
import re

import pystitch


class TestMeta(unittest.TestCase):
    def test_readme(self):
        readme_path = Path(__file__).parent.parent / "README.md"
        content = readme_path.read_text()

        embroidery_formats = [f for f in pystitch.supported_formats() if f["category"] == "embroidery"]

        write_formats = "".join(sorted(list_item(f) for f in embroidery_formats if "writer" in f))
        updated_content, count = re.subn(r"(?<=Pystitch will write:\n)(\* .+\n)*", write_formats, content, count=1)
        self.assertEqual(count, 1, "expected README to contain `Pystitch will write:`")

        read_formats = "".join(sorted(list_item(f) for f in embroidery_formats if "reader" in f))
        updated_content, count = re.subn(
            r"(?<=Pystitch will read:\n)(\* .+\n)*", read_formats, updated_content, count=1
        )
        self.assertEqual(count, 1, "expected README to contain `Pystitch will read:`")

        # TODO: also generate color, quilting and utility format lists

        if "UPDATE" in os.environ:
            readme_path.write_text(updated_content)
            return

        self.assertEqual(content, updated_content, "README outdated, run `UPDATE=1 python -m unittest test.test_meta`")


def list_item(format):
    return f"* .{format['extension']} ({format['description']})\n"
