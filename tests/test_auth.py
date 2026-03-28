import pytest
from io import BytesIO
from unittest.mock import patch

from bapp.index import *


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def get_mock_avatar():
    return (BytesIO(b"fake_image_data"), 'avatar.png')


# 1. TC_REG_01
@patch('cloudinary.uploader.upload')
@patch('bapp.index.dao.add_user')
def test_register_success(mock_add_user, mock_cloudinary, client):
    mock_cloudinary.return_value = {'secure_url': 'https://res.cloudinary.com/fake_avatar.png'}
    mock_add_user.return_value = True

    response = client.post('/api/register', data={
        'fullname': 'Test User',
        'email': 'test@gmail.com',
        'username': 'newuser',
        'password': 'ValidPass123',
        'confirm': 'ValidPass123',
        'avatar': get_mock_avatar()
    }, content_type='multipart/form-data')

    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['status'] == "success"
    assert json_data['message'] == "Registered successfully!"


# 2. TC_REG_02
def test_register_missing_fields(client):
    response = client.post('/api/register', data={
        'email': 'test@gmail.com',
        'username': 'newuser',
        'password': 'ValidPass123',
        'confirm': 'ValidPass123'
    })

    json_data = response.get_json()
    assert response.status_code == 400
    assert json_data['status'] == "error"
    assert json_data['message'] == "Please fill out all required fields!"


# 3. TC_REG_03
@patch('cloudinary.uploader.upload')
@patch('bapp.index.dao.add_user')
def test_register_exist_username(mock_add_user, mock_cloudinary, client):
    mock_cloudinary.return_value = {'secure_url': 'https://res.cloudinary.com/fake_avatar.png'}
    mock_add_user.side_effect = Exception("Username already exists!")

    response = client.post('/api/register', data={
        'fullname': 'Test User',
        'email': 'test@gmail.com',
        'username': 'existuser',
        'password': 'ValidPass123',
        'confirm': 'ValidPass123',
        'avatar': get_mock_avatar()
    }, content_type='multipart/form-data')

    assert response.status_code == 400
    assert response.get_json()['message'] == "Username already exists!"


# 4. TC_REG_04
def test_register_password_mismatch(client):
    response = client.post('/api/register', data={
        'fullname': 'Test User',
        'email': 'test@gmail.com',
        'username': 'newuser',
        'password': 'ValidPass123',
        'confirm': 'DifferentPass',
        'avatar': get_mock_avatar()
    }, content_type='multipart/form-data')

    assert response.status_code == 400
    assert response.get_json()['message'] == "Passwords do not match!"


# 5. TC_REG_05
def test_register_invalid_email(client):
    response = client.post('/api/register', data={
        'fullname': 'Test User',
        'email': 'invalid-email-format',
        'username': 'newuser',
        'password': 'ValidPass123',
        'confirm': 'ValidPass123',
        'avatar': get_mock_avatar()
    }, content_type='multipart/form-data')

    assert response.status_code == 400
    assert response.get_json()['message'] == "Invalid email format!"



class MockUser:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.is_active = True
        self.is_authenticated = True

    def get_id(self):
        return str(self.id)


# 6. TC_LOG_01
@patch('bapp.index.dao.auth_user')
def test_login_success(mock_auth_user, client):
    mock_auth_user.return_value = MockUser(id=1, username="testuser")

    response = client.post('/api/login', data={
        'username': 'testuser',
        'password': 'RightPassword123'
    })

    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['status'] == "success"
    assert json_data['data']['username'] == "testuser"


# 7. TC_LOG_02
@patch('bapp.index.dao.auth_user')
def test_login_fail_wrong_password(mock_auth_user, client):
    mock_auth_user.return_value = None

    response = client.post('/api/login', data={
        'username': 'testuser',
        'password': 'WrongPassword123'
    })

    assert response.status_code == 400
    assert response.get_json()['message'] == "Invalid username or password!"


# 8. TC_LOG_03
@patch('bapp.index.dao.auth_user')
def test_login_fail_wrong_username(mock_auth_user, client):
    mock_auth_user.return_value = None

    response = client.post('/api/login', data={
        'username': 'notexistuser',
        'password': 'ValidPassword123'
    })

    assert response.status_code == 400
    assert response.get_json()['message'] == "Invalid username or password!"


# 9. TC_OUT_04
def test_logout_success(client):
    response = client.post('/api/logout')

    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data['status'] == "success"
    assert json_data['message'] == "Signed out successfully!"