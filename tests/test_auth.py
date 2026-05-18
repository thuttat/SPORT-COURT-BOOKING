import pytest
from io import BytesIO
from bapp.models import UserRole
from tests.test_base import test_client, test_app, test_session


def get_mock_file(filename='avatar.png'):
    return (BytesIO(b"fake_image_data"), filename)


# TC_REG_01
def test_register_success(test_client, mocker):
    mocker.patch('cloudinary.uploader.upload', return_value={'secure_url': 'https://fake.url/avatar.png'})
    mocker.patch('bapp.index.dao.add_user')

    res = test_client.post('/api/register', data={
        'fullname': 'Test User',
        'email': 'test@gmail.com',
        'username': 'newuser',
        'password': 'ValidPass123!',
        'confirm': 'ValidPass123!',
        'avatar': get_mock_file()
    }, content_type='multipart/form-data')

    data = res.get_json()
    assert res.status_code == 201
    assert data['status'] == "success"


# TC_REG_02
@pytest.mark.parametrize("missing_field", [
    'fullname', 'email', 'username', 'password', 'confirm'
])
def test_register_missing_fields(test_client, missing_field):
    form_data = {
        'fullname': 'Test User', 'email': 'test@gmail.com', 'username': 'newuser',
        'password': 'ValidPass123!', 'confirm': 'ValidPass123!', 'avatar': get_mock_file()
    }
    form_data[missing_field] = ''

    res = test_client.post('/api/register', data=form_data, content_type='multipart/form-data')
    assert res.status_code == 400
    assert "Please fill out all required fields" in res.get_json()['message']


# TC_REG_03
def test_register_username_exists(test_client, mocker):
    mocker.patch('cloudinary.uploader.upload', return_value={'secure_url': 'url'})
    mocker.patch('bapp.index.dao.add_user', side_effect=Exception('Username already exists!'))

    res = test_client.post('/api/register', data={
        'fullname': 'Test User', 'email': 'test2@gmail.com', 'username': 'existuser',
        'password': 'ValidPass123!', 'confirm': 'ValidPass123!', 'avatar': get_mock_file()
    }, content_type='multipart/form-data')

    assert res.status_code == 400
    assert "Username already exists" in res.get_json()['message']


# TC_REG_04
def test_register_passwords_not_match(test_client):
    res = test_client.post('/api/register', data={
        'fullname': 'Test User', 'email': 'test@gmail.com', 'username': 'newuser',
        'password': 'ValidPass123!',
        'confirm': 'DifferentPass123!',
        'avatar': get_mock_file()
    }, content_type='multipart/form-data')

    assert res.status_code == 400
    assert "Passwords do not match" in res.get_json()['message']


# TC_REG_05
@pytest.mark.parametrize("invalid_email", ["test@gmail", "test.com", "test@.com", "test@gmail."])
def test_register_invalid_email(test_client, invalid_email):
    res = test_client.post('/api/register', data={
        'fullname': 'Test', 'email': invalid_email, 'username': 'newuser',
        'password': 'ValidPass123!', 'confirm': 'ValidPass123!', 'avatar': get_mock_file()
    }, content_type='multipart/form-data')

    assert res.status_code == 400
    assert "Invalid email format" in res.get_json()['message']


# TC_REG_06: IDOR Security Check
def test_register_prevent_admin_escalation(test_client, mocker):
    mocker.patch('cloudinary.uploader.upload', return_value={'secure_url': 'url'})
    mock_add = mocker.patch('bapp.index.dao.add_user')

    test_client.post('/api/register', data={
        'fullname': 'Hacker', 'email': 'hacker@gmail.com', 'username': 'hacker',
        'password': 'ValidPass123!', 'confirm': 'ValidPass123!', 'avatar': get_mock_file(),
        'user_role': 'ADMIN'
    }, content_type='multipart/form-data')

    kwargs = mock_add.call_args.kwargs
    assert kwargs['user_role'] == UserRole.USER


# TC_REG_07
def test_register_malicious_file(test_client):
    res = test_client.post('/api/register', data={
        'fullname': 'Test', 'email': 'test@gmail.com', 'username': 'newuser',
        'password': 'ValidPass123!', 'confirm': 'ValidPass123!',
        'avatar': get_mock_file('malware.exe')
    }, content_type='multipart/form-data')

    assert res.status_code == 400
    assert "Invalid file type" in res.get_json()['message']


# TC_REG_08
@pytest.mark.parametrize("invalid_pass", [
    "123456",
    "NoSymbol123",
    "short!1"
])
def test_register_invalid_password_format(test_client, invalid_pass):
    res = test_client.post('/api/register', data={
        'fullname': 'Test', 'email': 'test@gmail.com', 'username': 'newuser',
        'password': invalid_pass, 'confirm': invalid_pass, 'avatar': get_mock_file()
    }, content_type='multipart/form-data')

    assert res.status_code == 400
    assert "Invalid password format" in res.get_json()['message']


# TC_REG_09
def test_register_file_too_large(test_client):
    large_file_content = b"0" * (21 * 1024 * 1024)
    large_file = (BytesIO(large_file_content), 'huge_avatar.png')

    res = test_client.post('/api/register', data={
        'fullname': 'Test User', 
        'email': 'test@gmail.com', 
        'username': 'newuser',
        'password': 'ValidPass123!', 
        'confirm': 'ValidPass123!', 
        'avatar': large_file
    }, content_type='multipart/form-data')

    assert res.status_code == 400
    assert "This picture is too big" in res.get_json()['message']


#################################################################

# TC_LOG_01
def test_login_success(test_client, mocker):
    class FakeUser:
        id = 1
        username = 'validuser'
        fullname = 'Valid User'
        avatar = 'https://fake.url/avatar.png'
        is_active = True
        user_role = UserRole.USER

        def get_id(self):
            return str(self.id)

    mocker.patch('bapp.index.dao.auth_user', return_value=FakeUser())
    mocker.patch('flask_login.login_user', return_value=True)

    res = test_client.post('/api/login', data={'username': 'validuser', 'password': 'CorrectPass123!'})
    assert res.status_code == 200
    assert res.get_json()['status'] == "success"


# TC_LOG_02
def test_login_wrong_password(test_client, mocker):
    mocker.patch('bapp.index.dao.auth_user', return_value=None)

    res = test_client.post('/api/login', data={
        'username': 'validuser',
        'password': 'WrongPass999!'
    })
    assert res.status_code == 400
    assert "Invalid username or password" in res.get_json()['message']

# TC_LOG_03
def test_login_nonexistent_username(test_client, mocker):
    mocker.patch('bapp.index.dao.auth_user', return_value=None)

    res = test_client.post('/api/login', data={
        'username': 'userkhongtontai',
        'password': 'AnyPass123!'
    })
    assert res.status_code == 400
    assert "Invalid username or password" in res.get_json()['message']

######################################################################

# TC_OUT_01
def test_logout_success(test_client, mocker):
    mocker.patch('flask_login.logout_user')
    res = test_client.post('/api/logout')

    assert res.status_code == 200
    assert "Signed out successfully" in res.get_json()['message']


# TC_OUT_02
def test_logout_session_invalidation(test_client, mocker):
    class FakeUser:
        is_authenticated = False

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())

    res = test_client.post('/api/bookings', data={'field_id': '1', 'time_slots_id': '1', 'booking_date': '2026-12-31'})

    assert res.status_code in [401, 302]