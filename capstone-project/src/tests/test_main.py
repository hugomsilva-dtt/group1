import unittest
from utils.helpers import sample_helper

class TestMain(unittest.TestCase):
    def test_sample_helper(self):
        self.assertEqual(sample_helper(), "This is a helper function.")

if __name__ == "__main__":
    unittest.main()
