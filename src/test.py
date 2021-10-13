import json
import os
import time
from uuid import uuid4

from selenium.webdriver import ActionChains
from seleniumwire import webdriver

from itertools import cycle

from core import logger
from core.config import HEADLESS_MODE
from core.utils import sleep, checking_category_for_proxy, \
    get_web_driver_options, check_media_folders
from parser.utils import _download_image


def get_driver(_options):
    options = webdriver.FirefoxOptions()
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    )
    options.set_preference("dom.webdriver.enabled", False)
    options.headless = False

    profile = webdriver.FirefoxProfile()
    profile.set_preference('dom.webdriver.enabled', False)
    driver = webdriver.Firefox(
        executable_path="webdriver/geckodriver",
        options=options,
        firefox_profile=profile,
        seleniumwire_options=_options,
    )
    return driver


def get_proxy():
    return [
        {'proxy': {
            'http': 'http://2cS0DX:KxmqBV@193.32.153.27:8000',
            'https': 'https://2cS0DX:KxmqBV@193.32.153.27:8000',
        }},
        {'proxy': {
                'http': 'http://kKVvLB:VBAk1a@176.107.182.181:60702',
                'https': 'https://kKVvLB:VBAk1a@176.107.182.181:60702',
            }},
        {'proxy': {
                'http': 'http://madcros:Z9x0KzI@194.38.22.186:65233',
                'https': 'https://madcros:Z9x0KzI@194.38.22.186:65233',
            }},
        {'proxy': {
                'http': 'http://madcros:Z9x0KzI@176.114.8.234:65233',
                'https': 'https://madcros:Z9x0KzI@176.114.8.234:65233',
            }},
    ]

filenames = []


def main():
    urls = [
        "https://hotline.ua/computer-processory/amd-ryzen-7-5800x-100-100000063wof/",
        "https://hotline.ua/computer-processory/amd-ryzen-5-5600x-100-100000065box/"
    ]
    _options = checking_category_for_proxy("videokarty")
    driver = get_web_driver_options(_options)
    try:
        for url in urls:
            driver.get(url + "?tab=about")

            nav_list = driver.find_element_by_class_name("zoom-gallery__nav-list")
            if nav_list.is_displayed():
                print("NAV exists")
            else:
                print("NAV not exists")


    except Exception as e:
        print(e)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()