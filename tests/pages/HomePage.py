

from tests.pages.BasePage import BasePage
from selenium.webdriver.common.by import By
class HomePage(BasePage):
    URL = 'http://localhost:5173/'

    SEARCH_INPUT = (By.CSS_SELECTOR,'#root > div > main > div > div.filter-bar > input')
    BOOKING_BUTTON1 =(By.CSS_SELECTOR,'.container > div.grid > div:nth-child(1) > div.card-footer > button')
    BOOKING_BUTTON2 = (By.CSS_SELECTOR, '.container > div.grid > div:nth-child(2) > div.card-footer > button')




    def open_page(self):
        self.open(self.URL)
    def search(self, kw):
        self.typing(*self.SEARCH_INPUT,kw)
    def booking(self):
        self.click(*self.BOOKING_BUTTON1)
        self.driver.implicitly_wait(1)

