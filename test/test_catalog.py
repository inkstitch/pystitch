import unittest

import pystitch


class TestDataCatalog(unittest.TestCase):

    def test_catalog_files(self):
        for f in pystitch.supported_formats():
            self.assertIn("extensions", f)
            self.assertIn("extension", f)
            self.assertIn("description", f)
            self.assertIn("category", f)
