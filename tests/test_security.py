import pytest
from io import BytesIO
from datetime import datetime
from bapp.models import UserRole
from tests.test_base import test_client, test_app, test_session



@pytest.fixture
def auth_user(mocker):
    class FakeUser:
        is_authenticated = True
        id = 2
        user_role = UserRole.USER

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    return FakeUser()

def get_mock_file(filename='avatar.png'):
    return (BytesIO(b"fake_image_data"), filename)



# TC_SEC_01: Chống SQL Injection 
def test_sqli_prevention_on_login(test_client, mocker):
    malicious_payload = "' OR 1=1 --"
   
    mocker.patch('bapp.index.dao.auth_user', return_value=None)
    
    res = test_client.post('/api/login', data={
        'username': malicious_payload,
        'password': 'AnyPassword123!'
    })
    data = res.get_json()

    assert res.status_code == 400
    assert data['status'] == "error"
    assert "Invalid username or password" in data['message']
    assert 'data' not in data or data.get('data') is None




# TC_SEC_02: Chống XSS 
def test_xss_prevention_on_registration(test_client, mocker):
    mocker.patch('cloudinary.uploader.upload', return_value={'secure_url': 'url'})
    xss_payload = "<script>alert('XSS')</script>"

    mock_add = mocker.patch('bapp.index.dao.add_user')

    res = test_client.post('/api/register', data={
        'fullname': xss_payload,
        'email': 'tranb@gmail.com',
        'username': 'tranb01',
        'password': 'ValidPass123!',
        'confirm': 'ValidPass123!',
        'avatar': get_mock_file()
    }, content_type='multipart/form-data')

    assert res.status_code == 201
    kwargs = mock_add.call_args.kwargs
    stored_fullname = kwargs['fullname']

    response_body = res.get_data(as_text=True)
    assert '<script>' not in response_body 





# TC_SEC_03: Chống IDOR - Truy cập trái phép dữ liệu của người khác
def test_idor_prevention_viewing_others_booking(test_client, auth_user, mocker):
    class FakeOtherUserBooking:
        id = 1000
        user_id = 100 
        booking_date = datetime.now()
        total_price = 100000
        created_at = datetime.now()
        status = mocker.MagicMock(); 
        status.name = "CONFIRMED"
        field = mocker.MagicMock(); 
        field.name = "Sân VIP"
        time_slot = mocker.MagicMock(); 
        time_slot.name = "18:00 - 19:00"

    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=FakeOtherUserBooking())
   
    res = test_client.get('/api/my-bookings/1000')
    data = res.get_json()

    assert res.status_code == 403
    assert data['status'] == "error"
    assert "authorized" in data['message']




# TC_SEC_04: Chặn gọi API khi không có Token (chưa xác thực)
def test_unauthorized_api_access(test_client, mocker):
    class FakeGuest:
        is_authenticated = False 

    mocker.patch('flask_login.utils._get_user', return_value=FakeGuest())
    
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': '2026-12-31'
    })
    data = res.get_json()
    assert res.status_code == 401
    assert data['status'] == "error"
    assert "Authentication required. Please log in" in data['message']