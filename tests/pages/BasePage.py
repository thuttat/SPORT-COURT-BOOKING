from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIMEOUT = 10

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((by, value))
        )

    def finds(self, by, value):
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_all_elements_located((by, value))
        )

    def typing(self, by, value, text):
        e = self.find(by, value)
        e.send_keys(text)

    def click(self, by, value):
        e = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable((by, value))
        )
        e.click()