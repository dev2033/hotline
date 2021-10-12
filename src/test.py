import json
import time

from seleniumwire import webdriver

from itertools import cycle

from core.config import HEADLESS_MODE


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


def main():
    with open(
            f"results/product_urls/computer/videokarty.json",
            "r",
            encoding='utf-8'
    ) as file:
        urls = json.load(file)
        proxies = get_proxy()
        for url in urls:
            for i in range(0, len(proxies)):
                try:
                    print("Proxy selected: {}".format(proxies[i]))
                    options = webdriver.ChromeOptions()
                    options.add_argument(
                        '--proxy-server={}'.format(proxies[i]))
                    driver = webdriver.Chrome(options=options,
                                              executable_path=r'C:\WebDrivers\chromedriver.exe')
                    driver.get(
                        "https://www.whatismyip.com/proxy-check/?iref=home")
                    if "Proxy Type" in WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located(
                                    (By.CSS_SELECTOR, "p.card-text"))):
                        break
                except Exception:
                    driver.quit()
            print("Proxy Invoked")



if __name__ == '__main__':
    main()