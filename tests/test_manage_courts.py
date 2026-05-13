import pytest
from datetime import datetime, timedelta
from bapp.models import UserRole
import bapp.index


@pytest.fixture
def auth_admin(mocker):
    class FakeAdmin:
        is_authenticated = True
        id = 1
        user_role = UserRole.ADMIN 
    mocker.patch('flask_login.utils._get_user', return_value=FakeAdmin())
    return FakeAdmin()

