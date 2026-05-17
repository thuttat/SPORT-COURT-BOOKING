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


