from coverage import results
from sqlalchemy.sql.coercions import expect

from tests.pages.HomePage import HomePage
from tests.test_base import test_app, driver
from selenium.webdriver.common.by import By
import time

def test_search_courts(driver):
    # driver.get('http://localhost:5173/')
    # e = driver.find_element(By.CSS_SELECTOR,'#root > div > main > div > div.filter-bar > input')
    kw ='Mini'
    # e.send_keys(kw)
    home = HomePage(driver=driver)
    home.open_page()
    home.search(kw)


    time.sleep(1)

    results = driver.find_elements(By.CSS_SELECTOR,".container .court-name")
    assert all(kw in r.text for r in results)

def test_booking(driver):
    home = HomePage(driver=driver)
    home.open_page()
    home.booking()

    court = driver.find_element(By.CSS_SELECTOR,'#root > div > main > div > div.grid > div:nth-child(1)')
    expected_url ='http://localhost:5173/court/c1'
    assert court.get_attribute('href') == expected_url

