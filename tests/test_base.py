import pytest
from selenium.webdriver.chrome.service import Service
import os

os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
os.environ["TESTING"] = "true"

from bapp import app as bapp_app, db
import pytest
from bapp.models import UserRole



@pytest.fixture
def test_app():
    bapp_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    bapp_app.config["TESTING"] = True
    bapp_app.config["WTF_CSRF_ENABLED"] = False
    import bapp.index
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
def auth_admin(mocker):
    class FakeAdmin:
        is_authenticated = True
        id = 1
        user_role = UserRole.ADMIN
    mocker.patch('flask_login.utils._get_user', return_value=FakeAdmin())
    return FakeAdmin()

@pytest.fixture
def auth_user(mocker):
    class FakeUser:
        is_authenticated = True
        id = 2
        user_role = UserRole.USER
    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    return FakeUser()
