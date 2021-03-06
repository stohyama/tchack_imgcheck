import requests
import base64
import json
import os
import sys
from classes import scraping
from classes.image_information import ImageInformation
import csv

def url_to_image(url: str) -> bytes:
    try:
        img = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('NewtorkError')
    except requests.exceptions.TooManyRedirects:
        print('TooManyRedirects')
    except requests.exceptions.HTTPError:
        print('BadResponse')
    return img.content


def img_to_base64(image: bytes) -> bytes:
    return base64.encodebytes(image)


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


# 全L1画像共通加工ルール    背景色白の基本パターン    画像サイズ    縦：600px 横：600px
def is_rule_001(image_info: ImageInformation) -> bool:
    im = image_info.image
    width, height = im.size
    return width == 600 and height == 600


# 全L1画像共通加工ルール    背景色白の基本パターン    容量    50kb以下
def is_rule_002(image_info: ImageInformation) -> bool:
    return False


def is_rule_003(image_info: ImageInformation) -> bool:  # 全L1画像共通加工ルール 背景色白の基本パターン 解像度 72dpi
    return False


def is_rule_004(image_info: ImageInformation) -> bool:
    return False

# 以下 is_rule_*** をつくっていってください

def check_all_rules(image_info: ImageInformation) -> list:
    check_results = []

    item_cd = image_info.item_code

    #すべてのルールを呼んできて、結果を配列に入れる
    check_results.append([item_cd,'is_rule_001',is_rule_001(image_info)])
    check_results.append([item_cd,'is_rule_002',is_rule_002(image_info)])
    check_results.append([item_cd,'is_rule_003',is_rule_003(image_info)])

    return check_results

def print_csv(check_results: list):
    with open('test_print003.csv','a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(check_results)

def main():
    lpm_url = "https://lohaco.jp/store/irisplaza/ksearch/?categoryLl=55"
    max_page = 100

    scraping_html_array = scraping.return_scraping_html_array(
        lpm_url, max_page)

    for array in scraping_html_array:
        print('test')
        image = url_to_image(array[1])
        image_base64 = img_to_base64(image)
        google_json = get_json_from_googlecloud_vision_api(image_base64)
        image_info = ImageInformation(image,image_base64,google_json,array[0])
        results = check_all_rules(image_info)
        path = "./"
        print_csv(results)


if __name__ == '__main__':
    main()
    sys.exit()
