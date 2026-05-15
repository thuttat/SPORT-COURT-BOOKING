from tests.pages.HomePage import HomePage
from tests.test_base import test_app, driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#TC search
def test_search_courts(driver):
    kw = 'VIP'
    home = HomePage(driver=driver)
    home.open_page()
    home.search(kw)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".container .court-name"))
    )

    results = driver.find_elements(By.CSS_SELECTOR, ".container .court-name")
    assert len(results) > 0, "Không tìm thấy sân nào"
    assert all(kw in r.text for r in results), f"Có sân không chứa từ khóa '{kw}'"

#TC button & navigate
def test_booking_redirects_to_court_page(driver):
    home = HomePage(driver=driver)
    home.open_page()
    home.booking()

    expected_url = 'http://localhost:5173/court/1'
    driver.save_screenshot(f'url.png')
    WebDriverWait(driver, 1)

    assert driver.current_url == expected_url, \
        f"URL sai: expected {expected_url}, got {driver.current_url}"