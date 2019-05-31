import requests
import base64
import json
import os
import sys
import scraping
from image_information import ImageInformation
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


def is_rule_001(image_info: ImageInformation) -> bool:  # 全L1画像共通加工ルール    背景色白の基本パターン    画像サイズ    縦：600px 横：600px
    return False


def is_rule_002(image_info: ImageInformation) -> bool:  # 全L1画像共通加工ルール    背景色白の基本パターン    容量    50kb以下
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

def csv_output(check_results):
    with open('test_print001.csv','w') as file:
        writer = csv.writer(file)
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(check_results)

def main():
    lpm_url = "https://lohaco.jp/store/irisplaza/ksearch/?categoryLl=55"
    max_page = 100

    scraping_html_array = scraping.return_scraping_html_array(lpm_url, max_page)
    
    #ここから繰り返し文。見る商品数分だけ繰り返す。
    i = 0
    for item_info in scraping_html_array
    #while i <= len(scraping_html_array):
        img = url_to_image(item_info[1])
        img_base64 = img_to_base64(img)
        googlecloud_vision_json = get_json_from_googlecloud_vision_api(img_base64)
        #ImageInformationのインスタンスをつくるimage_info = ?
        #results = check_all_rules(image_info)
        #print_scv(image_info)


        check_results = check_all_rules()  #画像チェックの呼び出し

        csv_output(check_results) #csv掃き出しメソッド呼び出し

        i += 1
        #繰り返しここまで

if __name__ == '__main__':
    main()
    sys.exit()
