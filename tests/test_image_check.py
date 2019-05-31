import unittest
from classes.image_check import *
from classes.image_information import ImageInformation
from PIL import Image

class TestImageCheck(unittest.TestCase):
    def test_is_rule_001(self):
        ok_image = Image.open('tests/image/rule1_ok.jpg')
        #ok_image_base64 = img_to_base64(ok_image)
        json = ""
        x = ImageInformation(ok_image, "", json, "test")
        self.assertEqual(True, is_rule_001(x))

        ng_image = Image.open('tests/image/rule1_ng.jpg')
        #ok_image_base64 = img_to_base64(ok_image)
        json = ""
        x = ImageInformation(ok_image, "", json, "test")
        self.assertEqual(False, is_rule_001(x))


if __name__ == '__main__':
    unittest.main()