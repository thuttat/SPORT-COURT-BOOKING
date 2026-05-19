from unittest.mock import MagicMock

import pytest
from io import BytesIO
from tests.test_base import test_app, test_client, test_session, auth_admin, auth_user
from bapp.models import Field, FieldType, Booking, BookingStatus, TimeSlots, User, UserRole
from bapp import db
from datetime import date, timedelta, time
from werkzeug.security import generate_password_hash


#TC_INT_01
def test_TC_INT_01_session_expiration(test_client):
    res = test_client.post('/api/bookings')
    assert res.status_code in [302, 401], \
        f"Expect 302 hoặc 401 khi chưa login, nhận: {res.status_code}"


#TC_INT_02
def test_TC_INT_02_admin_maintenance_with_future_bookings(test_client, auth_admin, mocker):
    mock_field = MagicMock(spec=Field)
    mock_field.id = 1
    mock_field.user_id = 1
    mock_field.is_active = True

    mocker.patch('bapp.db.session.get', return_value=mock_field)

    mock_booking = MagicMock(spec=Booking)
    mock_booking.booking_date = date.today() + timedelta(days=3)
    mock_booking.status = BookingStatus.CONFIRMED

    mock_slot = MagicMock()
    mock_slot.start_time = time(7, 0)
    mock_booking.time_slot = mock_slot

    mock_query = MagicMock()
    mock_query.filter.return_value.all.return_value = [mock_booking]
    mocker.patch('bapp.admin.Booking.query', mock_query)

    res = test_client.delete('/api/admin/fields/1')

    assert res.status_code == 400, \
        f"Expect 400 khi có future booking, nhận: {res.status_code}"

    json_data = res.get_json()
    assert "future" in json_data["message"].lower(), \
        f"Message phải đề cập future booking: '{json_data['message']}'"

#TC_INT_03
def test_TC_INT_03_cloudinary_rollback_on_db_fail(test_client, mocker):
    mocker.patch(
        'cloudinary.uploader.upload',
        return_value={'secure_url': 'https://fake.url/img.jpg'}
    )
    mocker.patch('bapp.dao.add_user', side_effect=Exception("DB Crash"))

    data = {
        'fullname': 'Test User',
        'email': 'test@test.com',
        'username': 'testuser',
        'password': 'Test@1234!',
        'confirm': 'Test@1234!',
        'avatar': (BytesIO(b'fake image bytes'), 'avatar.jpg'),
    }

    res = test_client.post('/api/register', data=data, content_type='multipart/form-data')

    assert res.status_code in [400, 500], \
        f"Expect 400/500 khi DB crash, nhận: {res.status_code}"
    assert res.get_json()["status"] == "error"


#TC_INT_04
def test_TC_INT_04_cloudinary_timeout_graceful(test_client, mocker):
    mocker.patch(
        'cloudinary.uploader.upload',
        side_effect=TimeoutError("Connection timed out")
    )

    data = {
        'fullname': 'Test User',
        'email': 'test@test.com',
        'username': 'testuser',
        'password': 'Test@1234!',
        'confirm': 'Test@1234!',
        'avatar': (BytesIO(b'fake image bytes'), 'avatar.jpg'),
    }

    res = test_client.post('/api/register', data=data, content_type='multipart/form-data')

    assert res.status_code in [400, 500], \
        f"Expect 400/500 khi cloudinary timeout, nhận: {res.status_code}"
    assert res.get_json()["status"] == "error"