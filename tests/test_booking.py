import pytest
from datetime import date, datetime, timedelta
from bapp.models import UserRole
from test_base import test_client, test_app, test_session

# TC_BOOK_02: 
def test_book_without_login(test_client, mocker):
    class FakeUser:
        is_authenticated = False
    
    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())

    res = test_client.post('/api/bookings', data={
        'field_id': '1',
        'time_slots_id': '1',
        'booking_date': '2026-12-31'
    })

    data = res.get_json()
    assert res.status_code == 401
    assert data['message'] == "Please login to book a court"


# TC_BOOK_03: 
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


# TC_BOOK_06:
def test_book_over_limit_per_day(test_client, mocker):
    class FakeUser:
        is_authenticated = True
        id = 1
        user_role = UserRole.USER

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    
    class FakeSlot:
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("19:00", "%H:%M").time()

    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(True, FakeSlot()))
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