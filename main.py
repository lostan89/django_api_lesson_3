import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    api_url = "https://api.vk.ru/method/utils.getShortLink"
    payload = {"access_token": token, "v": "5.81", "url": url}
    response = requests.post(api_url, params=payload)
    response.raise_for_status()
    vk_short_link = response.json()
    return vk_short_link["response"]["short_url"]


def count_clicks(token, key):
    api_url = "https://api.vk.ru/method/utils.getLinkStats"
    payload = {"access_token": token, "v": "5.81", "key": key, "interval": "forever"}
    response = requests.post(api_url, params=payload)
    response.raise_for_status()
    clicks_count = response.json()["response"]["stats"]
    return clicks_count[0]["views"]


def is_shorten_link(url, token):
    api_url = "https://api.vk.ru/method/utils.getShortLink"
    payload = {"access_token": token, "v": "5.81", "url": url}
    response = requests.post(api_url, params=payload)
    response.raise_for_status()
    vk_short_link = response.json()
    return "error" in vk_short_link


def main():
    parser = argparse.ArgumentParser(
        description='Введите ссылку для работы программы'
        )
    parser.add_argument('link', help='Ссылка')
    args = parser.parse_args()
    load_dotenv()
    token = os.environ["VK_ACCESS_TOKEN"]
    print(args.link)
    url = args.link
    parsed_url = urlparse(url).path[1:]
    if is_shorten_link(url, token):
        try:
            print("Количество кликов по ссылке:", count_clicks(token, parsed_url))
        except IndexError:
            print("По ссылке никто не кликнул")
        except KeyError:
            print("Неверный формат ссылки")
    else:
        try:
            print("Сокращенная ссылка:", shorten_link(token, url))
        except KeyError:
            print("Неверный формат ссылки")


if __name__ == "__main__":
    main()
