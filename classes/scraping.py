from retry import retry
from bs4 import BeautifulSoup
import requests
import os
import time

def get_url_exclude_extension(string_url):
    return_str = os.path.splitext(string_url)
    return return_str[0], return_str[1]


def get_item_code_from_href(string_href):
    return string_href.split('/')[2]


@retry(tries=3, delay=2, backoff=2)
def return_scraping_html_array(lpm_url, max_page):
    return_array = []
    pg = '&resultCount=100&page='
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
    }

    for count in range(max_page):  # 無限ループにならないように、最大繰り返し回数を指定
        print(str(count + 1) + 'ページ目')
        try:
            soup = BeautifulSoup(requests.get(
                lpm_url + pg + str(count+1)).content, 'html5lib')
        except requests.exceptions.ConnectionError:
            print('NewtorkError')
        except requests.exceptions.TooManyRedirects:
            print('TooManyRedirects')
        except requests.exceptions.HTTPError:
            print('BadResponse')

        for inner_box in soup.find_all(class_="innerBox"):
            for img in inner_box.find_all('img'):
                item_code = get_item_code_from_href(
                    inner_box.a.get('href'))
                url, extension = get_url_exclude_extension(img.get("src"))

                # 検索ページの商品画像URLから3L画像のURLを取得
                url_3L = url[:-1] + "3L" + extension
                array = [item_code, url_3L]
                return_array.append(array)

        # 次へボタンがなかったら終了
        if bool(soup.find(class_='nextBtn')) == False:
            return return_array

        time.sleep(2)
