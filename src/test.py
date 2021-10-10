import json
import os
from urllib.request import urlretrieve
from uuid import uuid4

from selenium.webdriver import ActionChains

from core.logger import logger
from core.utils import sleep, checking_category_for_proxy, \
    get_web_driver_options


def _download_image(category: str, subcategory: str, url):
    """ Скачивает изображения
    """
    index = 1
    path = f"media/{category}/{subcategory}"
    if len(os.listdir(path)) > 900:
        index += 1
        path = path.strip(str(index - 1)) + str(index)
        os.mkdir(path)
    filename = path + f"/{uuid4()}.jpg"
    urlretrieve(
        url=url,
        filename=filename
    )

    return filename


filenames = list()


def get_images(driver, category: str, subcategory: str) -> list:
    """ Собирает ссылки на изображения конкретного товара и скачивает их
    """
    image_urls = list()

    driver.execute_script("scrollBy(0,-500);")
    _images = driver.find_elements_by_class_name(
        "zoom-gallery__nav-item--image"
    )

    for img in _images:
        try:
            ActionChains(driver).move_to_element(img).perform()
            sleep()
            img_link = driver.find_element_by_class_name(
                "zoom-gallery__canvas-img"
            )
            _url = img_link.get_attribute("src")
            image_urls.append(_url)

            filename = _download_image(
                category=category,
                url=_url,
                subcategory=subcategory
            )
            filenames.append(filename)
        except Exception as e:
            print(e)
            continue

    logger.debug("Все изображения скачаны")
    return filenames


def get_images_invalid(driver, category: str, subcategory: str):
    """ Забирает изображение с товара, там где оно одно
    """
    driver.execute_script("scrollBy(0,-500);")
    image = driver.find_element_by_class_name("zoom-gallery__canvas-img")

    _url = image.get_attribute("src")
    filename = _download_image(
        category=category,
        url=_url,
        subcategory=subcategory
    )

    logger.debug("Все изображения скачаны")
    return filename


def main():

    _options = checking_category_for_proxy("videokarty")
    driver = get_web_driver_options(_options)

    try:

        driver.get("https://hotline.ua/computer-videokarty/msi-geforce-rtx-3060-gaming-x-12g/?tab=about")
        image_list = get_images(driver=driver, category="computer", subcategory="videokarty")
        print(image_list)
        with open("results/detail/data.json", "a", encoding="utf-8") as file:
            json.dump(image_list, file, indent=4, ensure_ascii=False)
            logger.debug("JSON файл заполнен")

    except Exception as e:
        pass

    finally:
        driver.quit()


if __name__ == '__main__':
    main()