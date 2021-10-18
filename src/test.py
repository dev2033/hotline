from selenium.webdriver import Firefox
from selenium.common.exceptions import NoSuchElementException


def main():
    driver = Firefox(executable_path="webdriver/geckodriver")

    driver.get("https://hotline.ua/computer-videokarty/biostar-radeon-rx-6700-xt-oc-va67s6tml9/")

    try:
        a = driver.find_element_by_class_name("busy").get_attribute("src")
        if a is None:
            print("ok")
            print(a)
        else:
            print("no")

    except Exception as e:
        driver.quit()
        print(e)

    finally:
        driver.quit()

    # print(a)


if __name__ == '__main__':
    main()