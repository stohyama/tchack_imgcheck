import requests
import base64
import json
import os
import sys
from classes.scraping import return_scraping_html_array


def img_to_base64(filepath):
    with open(filepath, 'rb') as img:
        img_byte = img.read()
    return base64.encodebytes(img_byte)


def get_json_from_googlecloud_vision_api(image_base64):
    GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
    API_KEY = os.environ.get('GOOGLE_API_KEY')
    # プロキシ突破
    os.environ.get('HTTP_PROXY')

    api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
    req_body = json.dumps({
        'requests': [{
            'image': {
                # bytes型のままではjsonに変換できないのでstring型に変換する
                'content': image_base64.decode('utf-8')
            },
            'features': [
                {
                    'type': 'IMAGE_PROPERTIES',
                },
                {
                    'type': 'SAFE_SEARCH_DETECTION',
                }
            ]
        }]
    })
    res = requests.post(api_url, data=req_body)
    return res.json()


def is_rule_001():  # 全L1画像共通加工ルール    背景色白の基本パターン    画像サイズ    縦：600px 横：600px
    # def is_rule_001(vision_api_json) -> vision_apiのjsonをつかう場合は、こう書く
    return False


def is_rule_002():  # 全L1画像共通加工ルール    背景色白の基本パターン    容量    50kb以下
    return False


def is_rule_003():  # 全L1画像共通加工ルール 背景色白の基本パターン 解像度 72dpi
    return False


def is_rule_004():
    return False

# 以下 is_rule_*** をつくっていってください


def main():
    lpm_url = "https://lohaco.jp/store/irisplaza/ksearch/?categoryLl=55"
    max_page = 100

    scraping_html_array = return_scraping_html_array(lpm_url, max_page)
    img_base64 = img_to_base64('./sample.jpg')
    googlecloud_vision_json = get_json_from_googlecloud_vision_api(img_base64)

    print('is_rule_001', is_rule_001())

    print('is_rule_002', is_rule_002())

    print('is_rule_003', is_rule_003())


if __name__ == '__main__':
    main()
    sys.exit()
