import pytest
from selenium.webdriver.chrome.service import Service

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
    service = Service(executable_path='../.venv/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

