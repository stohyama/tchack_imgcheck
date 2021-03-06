import unittest
from classes.image_information import ImageInformation


class TestImageInformation(unittest.TestCase):
    def test__image_information(self):
        x = ImageInformation(1, 2, 3, 4)
        self.assertEqual(1, x.image)
        self.assertEqual(2, x.image_base64)
        self.assertEqual(4, x.google_vison_api_json)


if __name__ == '__main__':
    unittest.main()
