from selenium.common import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class DriverService:
    def __init__(self):
        self.driver = self.get_driver()

    @staticmethod
    def get_driver():
        print("\ncreate driver\n")
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Remote(
            "http://browser:4444/wd/hub",
            DesiredCapabilities.CHROME,
            options=options,
        )
        return driver

    def get_attr(self, by, value, text=False, driver=None):
        if driver is None:
            driver = self.driver
        try:
            result = driver.find_element(by, value)
            if text:
                return result
            else:
                return result.text
        except NoSuchElementException:
            return None

    def close_driver(self):
        self.driver.close()
