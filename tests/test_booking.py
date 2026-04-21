import pytest
from datetime import datetime, timedelta
from bapp.models import UserRole
from tests.test_base import test_client, test_app, test_session

# DÒNG QUAN TRỌNG NHẤT: Import index để Flask nạp toàn bộ @app.route trước khi test
import bapp.index


# TC_BOOK_02
def test_book_without_login(test_client, mocker):
    class FakeUser:
        is_authenticated = False

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())

    res = test_client.post('/api/bookings', data={
        'field_id': '1',
        'time_slots_id': '1',
        'booking_date': '2026-12-31'
    })

    assert res.status_code in [401, 302]


# TC_BOOK_03
def test_book_past_time(test_client, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1
        user_role = UserRole.USER

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())

    class FakeField:
        id = 1
        name = "Sân 1"

    class FakeSlot:
        id = 1
        name = "Slot 1"
        start_time = datetime.strptime("08:00", "%H:%M").time()
        end_time = datetime.strptime("09:00", "%H:%M").time()

    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(FakeField(), FakeSlot()))

    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    res = test_client.post('/api/bookings', data={
        'field_id': '1',
        'time_slots_id': '1',
        'booking_date': past_date
    })

    data = res.get_json()
    assert res.status_code == 400
    assert "Cannot book a court in the past" in data['message']


# TC_BOOK_06
def test_book_over_limit_per_day(test_client, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1
        user_role = UserRole.USER

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())

    class FakeField:
        id = 1
        name = "Sân 1"

    class FakeSlot:
        id = 2
        name = "Slot 2"
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("19:00", "%H:%M").time()

    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(FakeField(), FakeSlot()))

    mocker.patch('bapp.index.dao.count_user_bookings_per_day', return_value=3)

    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

    res = test_client.post('/api/bookings', data={
        'field_id': '1',
        'time_slots_id': '2',
        'booking_date': future_date
    })

    data = res.get_json()
    assert res.status_code == 400
    assert "maximum of 3 courts per day" in data['message']


# TC_BOOK_01
def test_book_success(test_client, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1
        user_role = UserRole.USER

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())

    class FakeField:
        id = 1
        name = "Sân VIP"

    class FakeSlot:
        id = 3
        name = "Slot 3"
        start_time = datetime.strptime("20:00", "%H:%M").time()
        end_time = datetime.strptime("21:30", "%H:%M").time()

    class FakeBooking:
        id = 99
        total_price = 300000

    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(FakeField(), FakeSlot()))
    mocker.patch('bapp.index.dao.count_user_bookings_per_day', return_value=1)
    mocker.patch('bapp.index.dao.is_field_available', return_value=True)
    mocker.patch('bapp.index.dao.create_new_booking', return_value=FakeBooking())

    future_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

    res = test_client.post('/api/bookings', data={
        'field_id': '1',
        'time_slots_id': '3',
        'booking_date': future_date
    })

    data = res.get_json()
    assert res.status_code == 201
    assert data['status'] == "success"
    assert data['message'] == "Booking successful!"
    assert data['data']['booking_id'] == 99