import pytest
from selenium.webdriver.chrome.service import Service
import os

os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
os.environ["TESTING"] = "true"

from bapp import app as bapp_app, db
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def test_app():
    bapp_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    bapp_app.config["TESTING"] = True
    bapp_app.config["WTF_CSRF_ENABLED"] = False

    with bapp_app.app_context():
        db.create_all()
        yield bapp_app
        db.drop_all()


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture
def test_session(test_app):
    yield db.session


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    driver_path_windows = os.path.join(base_dir, '.venv', 'chromedriver.exe')

    if os.path.exists(driver_path_windows):

        service = Service(executable_path=driver_path_windows)
    else:

        service = Service()

    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()