import random
import unittest

from pystitch.EmbCompress import expand, compress

class TestReadHus(unittest.TestCase):
    @unittest.skip("")
    def test_fake_compression(self):
        for _ in range(10):
            s = random.randint(10, 100000)
            test_bytes = bytearray(random.getrandbits(8) for _ in range(s))
            compressed_bytes = compress(test_bytes)
            uncompressed = bytearray(expand(compressed_bytes, len(test_bytes)))
            self.assertEqual(test_bytes, uncompressed)
