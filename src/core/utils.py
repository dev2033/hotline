import os
import random
import time
import json

from seleniumwire import webdriver

from core.config import HEADLESS_MODE, PAUSE, components_urls
from core.logger import logger


def sleep() -> None:
    """Засыпает"""
    time.sleep(random.randrange(5, 10))


def check_media_folders(input_category: str, subcategory_img: str):
    """ Проверяет, ли дирректории в проекте
    """
    if not os.path.exists(f"media/{input_category}") or \
            not os.path.exists(f"media/{input_category}/{subcategory_img}"):
        # os.mkdir(f"media/{input_category}")
        os.makedirs(f"media/{input_category}/{subcategory_img}/{subcategory_img}")

    # if not os.path.exists(f"media/{input_category}/{subcategory_img}"):
    #     os.mkdir(f"media/{input_category}/{subcategory_img}")


def check_is_file(category: str, file_name: str):
    """ Проверяет, есть ли файл с ссылками на товары,
        если есть, то удаляет его и записывает новый.
        Также проверяет наличие папки с названием категории
    """
    path_file = f"results/product_urls/{category}/{file_name}.json"
    if os.path.exists(path_file):
        confirm = input(
            "# Файл уже существует! Перезаписать его? (y/n): "
        )
        if confirm in ["Y", "y"]:
            os.remove(path_file)
        else:
            logger.debug("Сбор ссылок прекращен!")
            exit()

    if not os.path.exists(f"results/product_urls/{category}/"):
        os.mkdir(f"results/product_urls/{category}/")


def get_web_driver_options(_options: dict) -> any:
    """Возвращает опции веб драйвера"""
    options = webdriver.FirefoxOptions()
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    )
    options.set_preference("dom.webdriver.enabled", False)
    options.headless = HEADLESS_MODE

    profile = webdriver.FirefoxProfile()
    profile.set_preference('dom.webdriver.enabled', False)
    driver = webdriver.Firefox(
        executable_path="webdriver/geckodriver",
        options=options,
        seleniumwire_options=_options,
        firefox_profile=profile
    )
    driver.set_page_load_timeout(3600 * PAUSE * 2)
    return driver


def formatter_json_file():
    """ Форматирует файлы json
    """
    while True:
        category = input("# Введите название категории: ")
        subcategory = input("# Введите название подкатегории: ")
        input_filename = input("# Введите название форматируемого файла: ")
        out_filename = input("# Введите название выходного файла: ")
        path_to_file = f"results/detail/{category}/{subcategory}/{input_filename}.json"
        try:
            with open(path_to_file, "r", encoding="utf-8") as file:
                data = json.loads(file.read())
                for i, v in enumerate(data):
                    try:
                        data[i].pop("url")
                        detail = \
                            data[i].get("Характеристики").get("детальні") or \
                            data[i].get("Характеристики").get("детальные")
                        for item in detail:
                            if item.get("Товар на сайті виробника") or \
                                    item.get("Товар на сайте производителя"):
                                detail.remove(item)

                    except KeyError as e:
                        continue
        except FileNotFoundError:
            logger.error("File not found")
        else:
            path_to_out_filename = f"results/format_files/{category}/" \
                                   f"{subcategory}/{out_filename}.json"

            if not os.path.exists(f"results/format_files/{category}"):
                os.mkdir(f"results/format_files/{category}")

            if not os.path.exists(f"results/format_files/{category}/{subcategory}"):
                os.mkdir(f"results/format_files/{category}/{subcategory}")

            with open(path_to_out_filename, "a", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            logger.success(f"Файл сохранен: /{path_to_out_filename}")
            break


def check_product_name(product_name: str):
    """ Проверяет название продукта, чтобы начать парсинг
    """
    for index, value in enumerate(components_urls):
        _index = index + 1
        if _index == int(product_name):
            return value


def checking_category_for_proxy(subcategory: str) -> dict:
    """ Проверяет название подкатегории и возвращает прокси
    """
    _options = {}
    if subcategory == "processory":
        _options = {
            'proxy': {
                'http': 'http://2cS0DX:KxmqBV@193.32.153.27:8000',
                'https': 'https://2cS0DX:KxmqBV@193.32.153.27:8000',
            }
        }
    elif subcategory == "zhestkie-diski":
        _options = {
            'proxy': {
                'http': 'http://kKVvLB:VBAk1a@176.107.182.181:60702',
                'https': 'https://kKVvLB:VBAk1a@176.107.182.181:60702',
            }
        }
    elif subcategory == "ofisnye-kresla":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@194.38.22.186:65233',
                'https': 'https://madcros:Z9x0KzI@194.38.22.186:65233',
            }
        }
        """asdsadsadasd"""
    elif subcategory == "karty-podpiski-onlajn-servisov":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@176.114.8.234:65233',
                'https': 'https://madcros:Z9x0KzI@176.114.8.234:65233',
            }
        }
    elif subcategory == "zhestkie-diski":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@88.218.190.156:65233',
                'https': 'https://madcros:Z9x0KzI@88.218.190.156:65233',
            }
        }
    elif subcategory == "opticheskie-nakopiteli":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@185.166.219.168',
                'https': 'https://madcros:Z9x0KzI@185.166.219.168:65233',
            }
        }
    elif subcategory == "televizory":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@5.180.102.47:65233',
                'https': 'https://madcros:Z9x0KzI@5.180.102.47:65233',
            }
        }
    elif subcategory == "noutbuki-netbuki":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@193.203.48.215:65233',
                'https': 'https://madcros:Z9x0KzI@193.203.48.215:65233',
            }
        }
    elif subcategory == "dopolnitelnoe-oborudovanie-dlya-igrovyh-pristavok":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@91.226.213.71:65233',
                'https': 'https://madcros:Z9x0KzI@91.226.213.71:65233',
            }
        }
    elif subcategory == "naushniki-garnitury":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@93.190.44.121:65233',
                'https': 'https://madcros:Z9x0KzI@93.190.44.121:65233',
            }
        }
    elif subcategory == "ochki-virtualnoj-realnosti":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@45.154.118.137:65233',
                'https': 'https://madcros:Z9x0KzI@45.154.118.137:65233',
            }
        }
    elif subcategory == "gejmpady-dzhojstiki-ruli":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@212.90.111.112:65233',
                'https': 'https://madcros:Z9x0KzI@212.90.111.112:65233',
            }
        }
    elif subcategory == "igry-dlya-pristavok":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@95.46.8.160:65233',
                'https': 'https://madcros:Z9x0KzI@95.46.8.160:65233',
            }
        }
    elif subcategory == "igrovye-pristavki":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@139.28.39.115:65233',
                'https': 'https://madcros:Z9x0KzI@139.28.39.115:65233',
            }
        }
    elif subcategory == "kompyuternye-aksessuary":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@31.131.19.118:65233',
                'https': 'https://madcros:Z9x0KzI@31.131.19.118:65233',
            }
        }
    elif subcategory == "ofisnye-i-kompyuternye-stoly":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@87.247.154.185:65233',
                'https': 'https://madcros:Z9x0KzI@87.247.154.185:65233',
            }
        }
    elif subcategory == "nastolnye-kompyutery":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@185.252.24.252:65233',
                'https': 'https://madcros:Z9x0KzI@185.252.24.252:65233',
            }
        }
    elif subcategory == "servery":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@193.169.87.69:65233',
                'https': 'https://madcros:Z9x0KzI@193.169.87.69:65233',
            }
        }
    elif subcategory == "kontrollery-platy":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@176.103.53.213:65233',
                'https': 'https://madcros:Z9x0KzI@176.103.53.213:65233',
            }
        }
    elif subcategory == "kardridery":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@185.230.88.135:65233',
                'https': 'https://madcros:Z9x0KzI@185.230.88.135:65233',
            }
        }
    elif subcategory == "usb-flash-drajvy":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@176.107.183.131:65233',
                'https': 'https://madcros:Z9x0KzI@176.107.183.131:65233',
            }
        }
    elif subcategory == "flash-karty":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@91.234.35.109:65233',
                'https': 'https://madcros:Z9x0KzI@91.234.35.109:65233',
            }
        }
    elif subcategory == "web-kamery":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@91.217.90.210:65233',
                'https': 'https://madcros:Z9x0KzI@91.217.90.210:65233',
            }
        }
    elif subcategory == "graficheskie-planshety":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@91.211.91.150:65233',
                'https': 'https://madcros:Z9x0KzI@91.211.91.150:65233',
            }
        }
    elif subcategory == "monitory":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@91.207.60.222:65233',
                'https': 'https://madcros:Z9x0KzI@91.207.60.222:65233',
            }
        }
    elif subcategory == "kovriki-dlya-myshi":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@91.229.79.83:65233',
                'https': 'https://madcros:Z9x0KzI@91.229.79.83:65233',
            }
        }
    elif subcategory == "opticheskie-nakopiteli":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@194.40.243.209:65233',
                'https': 'https://madcros:Z9x0KzI@194.40.243.209:65233',
            }
        }
    elif subcategory == "tv-tyunery":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@31.41.219.234:65233',
                'https': 'https://madcros:Z9x0KzI@31.41.219.234:65233',
            }
        }
    elif subcategory == "aksessuary-dlya-korpusov-kulerov":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@193.22.96.248:65233',
                'https': 'https://madcros:Z9x0KzI@193.22.96.248:65233',
            }
        }
    elif subcategory == "termopasta":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@185.167.161.249:65233',
                'https': 'https://madcros:Z9x0KzI@185.167.161.249:65233',
            }
        }
    elif subcategory == "zvukovye-karty":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@45.136.206.67:65233',
                'https': 'https://madcros:Z9x0KzI@45.136.206.67:65233',
            }
        }
    elif subcategory == "karmany-dlya-hdd":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@185.225.226.152:65233',
                'https': 'https://madcros:Z9x0KzI@185.225.226.152:65233',
            }
        }
    elif subcategory == "kulery-i-radiatory":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@193.228.52.227:65233',
                'https': 'https://madcros:Z9x0KzI@193.228.52.227:65233',
            }
        }
    elif subcategory == "bloki-pitaniya":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@45.9.236.137:65233',
                'https': 'https://madcros:Z9x0KzI@45.9.236.137:65233',
            }
        }
    elif subcategory == "videokarty":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@185.157.79.119:65233',
                'https': 'https://madcros:Z9x0KzI@185.157.79.119:65233',
            }
        }
    elif subcategory == "korpusa":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@45.137.155.234:65233',
                'https': 'https://madcros:Z9x0KzI@45.137.155.234:65233',
            }
        }
    elif subcategory == "materinskie-platy":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@185.247.208.68:65233',
                'https': 'https://madcros:Z9x0KzI@185.247.208.68:65233',
            }
        }
    elif subcategory == "diski-ssd":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@31.148.99.167:65233',
                'https': 'https://madcros:Z9x0KzI@31.148.99.167:65233',
            }
        }
    elif subcategory == "moduli-pamyati-dlya-pk-i-noutbukov":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@193.42.107.7:65233',
                'https': 'https://madcros:Z9x0KzI@193.42.107.7:65233',
            }
        }
    elif subcategory == "myshi-klaviatury":
        _options = {
            'proxy': {
                'http': 'http://madcros:Z9x0KzI@93.170.123.99:65233',
                'https': 'https://madcros:Z9x0KzI@93.170.123.99:65233',
            }
        }

    return _options
