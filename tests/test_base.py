import pytest
from selenium.webdriver.chrome.service import Service
import os

from bapp import app as bapp_app, db
from selenium import webdriver

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
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    driver_path = os.path.join(base_dir, '.venv', 'chromedriver.exe')

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

