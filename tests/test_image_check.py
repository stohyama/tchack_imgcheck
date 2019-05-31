import unittest
from classes.image_check import *
from classes.image_information import ImageInformation


class TestImageCheck(unittest.TestCase):
    def test_is_rule_001(self):
        x = ImageInformation(1, 2, 3, 4)
        self.assertEqual(True, is_rule_001(x))


if __name__ == '__main__':
    unittest.main()
