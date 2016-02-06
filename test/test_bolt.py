import unittest

import bolt

class TestRunner(unittest.TestCase):

    def test_fail(self):
        self.fail("On purpose")


if __name__=="__main__":
    unittest.main()