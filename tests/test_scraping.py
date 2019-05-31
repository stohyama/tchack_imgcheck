import unittest
from classes.scraping import *


class TestScraping(unittest.TestCase):
    def test_get_url_exclude_extension(self):
        path, extension = get_url_exclude_extension(
            "https://askul.c.yimg.jp/lpm/img/irisplaza/561780_smn_01_3L.jpg")
        self.assertEqual(
            "https://askul.c.yimg.jp/lpm/img/irisplaza/561780_smn_01_3L", path)
        self.assertEqual(".jpg", extension)

    def test_get_item_code_from_href(self):
        # /product/L06613482/
        self.assertEqual(
            'L06613482', get_item_code_from_href("/product/L06613482/"))

    def test_return_scraping_html_array(self):
        url = 'https://lohaco.jp/store/irisplaza/ksearch/?categoryLl=58'
        actual = return_scraping_html_array(url, 5)
        self.assertEqual(True, len(actual) > 0)


if __name__ == '__main__':
    unittest.main()
