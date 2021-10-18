import json
import time

from seleniumwire import webdriver

from core.config import PAUSE
from core.logger import logger
from parser.utils import (
    get_detail_ua,
    get_images,
    get_images_invalid
)
from core.utils import check_media_folders


data = list()
invalid_urls = list()


def get_detail_specs_ua(
        driver: webdriver.Firefox,
        input_category: str,
        input_file_name: str,
        subcategory_img: str,
        rus_lang: bool
) -> list:
    """ Получает Детальные характеристики на товар
    """

    check_media_folders(
        input_category=input_category,
        subcategory_img=subcategory_img
    )
    try:
        with open(
                f"results/product_urls/{input_category}/{input_file_name}.json",
                "r",
                encoding='utf-8'
        ) as file:
            index = 1
            urls = json.load(file)
            manufacturer_link = ""

            for url in urls:
                try:
                    driver.get(url + "?tab=about")
                    logger.info("Перешел на страницу")

                    if rus_lang:
                        lang_classes = driver.find_elements_by_class_name(
                            "lang__link")[:2]
                        if "lang__link--disabled" in lang_classes[0]\
                                .get_attribute("class").split():
                            logger.info("Уже русский")
                        else:
                            lang_classes[0].click()
                            logger.info("Переключил на русский язык")

                    # Загружает изображения -------------------------
                    nav_list = driver.find_element_by_class_name("zoom-gallery__nav-list")
                    if nav_list.is_displayed():
                        image_list = get_images(
                            driver=driver,
                            category=input_category,
                            subcategory=subcategory_img
                        )
                    else:
                        image_list = get_images_invalid(
                            driver=driver,
                            category=input_category,
                            subcategory=subcategory_img
                        )
                    time.sleep(2)
                    # -----------------------------------------------

                    driver.find_elements_by_class_name(
                        "header__switcher-item"
                    )[1].click()
                    title = driver.find_element_by_class_name("title__main").text
                    vendor_code = ""
                    if "(" in title:
                        vendor_code = title.split("(")[-1].strip(")")
                    try:
                        description = driver.find_element_by_class_name(
                            "cropper-text"
                        ).text
                    except Exception:
                        description = ""

                    table_spec = driver.find_element_by_class_name(
                        "specifications__table"
                    )
                    tags = table_spec.find_elements_by_tag_name("tr")
                    detail_specs = list()

                    for tag in tags:
                        try:
                            key = tag.find_elements_by_tag_name("td")[0].text
                            value = tag.find_elements_by_tag_name("td")[1]

                            if key in ['', '\n'] and value.text in ['', '\n']:
                                continue
                            else:
                                key = key.strip(":")
                                manufacturer_link = value \
                                    .find_element_by_tag_name("a") \
                                    .get_attribute("data-outer-link") \
                                    if key in [
                                        "Товар на сайті виробника",
                                        "Товар на сайте производителя"
                                    ] else ""
                        except Exception as e:
                            continue

                        detail_specs.append({key: value.text})

                    main_specs = get_detail_ua(driver)
                    if rus_lang:
                        data_objects = {
                            "url": url,
                            "vendor_code": vendor_code,
                            "title": title,
                            "description": description,
                            "Товар на сайте производителя": manufacturer_link,
                            "Изображения": image_list,
                            "Характеристики": {
                                "основные": main_specs,
                                "детальные": detail_specs
                            }
                        }
                    else:
                        data_objects = {
                            "url": url,
                            "vendor_code": vendor_code,
                            "title": title,
                            "description": description,
                            "Товар на сайті виробника": manufacturer_link,
                            "Зображення": image_list,
                            "Характеристики": {
                                "основні": main_specs,
                                "детальні": detail_specs
                            }
                        }
                    data.append(data_objects)

                    logger.success(f"JSON сформирован. Объектов - {index}")

                    index += 1
                    if index == 400:
                        # driver.set_page_load_timeout(3600 * PAUSE)
                        time.sleep(3600 * PAUSE)

                    time.sleep(7 if index % 10 != 0 else 60*1)

                except Exception as e:
                    logger.error(e)
                    invalid_urls.append(url)
                    continue

    except Exception as e:
        logger.error(e)
        driver.quit()

    finally:
        with open("results/invalid_urls/invalid_urls.txt", "w") as file:
            for item in invalid_urls:
                file.write(item + "\n")
        driver.quit()

    return data
