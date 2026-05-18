import pytest
from datetime import datetime, timedelta
from bapp.models import UserRole
from tests.test_base import test_client, test_app, test_session

import bapp.index



@pytest.fixture
def auth_user(mocker):
    class FakeUser:
        is_authenticated = True
        id = 1
        user_role = UserRole.USER
    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    return FakeUser()

@pytest.fixture
def sample_fields():
    class FakeField1: id = 1; name = "Sân Bóng Đá (Football)"
    class FakeField2: id = 2; name = "Sân Tennis"
    class FakeField3: id = 3; name = "Sân Cầu Lông (Badminton)"
    return [FakeField1(), FakeField2(), FakeField3()]

@pytest.fixture
def default_booking_mocks(mocker):
    class FakeField:
        id = 1
        name = "Sân Tiêu Chuẩn"

    class FakeSlot:
        id = 1
        name = "Slot Chuẩn"
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("19:00", "%H:%M").time()

    class FakeBooking:
        id = 1
        total_price = 300000
    
    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(FakeField(), FakeSlot()))
    mocker.patch('bapp.index.utils.calculate_duration', return_value=1.0)
    mocker.patch('bapp.index.dao.count_user_bookings_per_day', return_value=0)
    mocker.patch('bapp.index.dao.is_field_available', return_value=True)
    mocker.patch('bapp.index.dao.create_new_booking', return_value=FakeBooking())
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=0)



# TC_BOOK_01: Thành công 
def test_book_success(test_client, auth_user, default_booking_mocks):
    future_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    data = res.get_json()
    assert res.status_code == 201
    assert data['data']['booking_id'] == 1

# TC_BOOK_02: Chưa đăng nhập
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

# TC_BOOK_03: Đặt quá khứ 
def test_book_past_time(test_client, auth_user, default_booking_mocks):
    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': past_date
    })
    assert res.status_code == 400
    assert "Cannot book a court in the past" in res.get_json()['message']

# TC_BOOK_04: Dưới 1 tiếng 
def test_book_minimum_duration(test_client, mocker, auth_user, default_booking_mocks):
    mocker.patch('bapp.index.utils.calculate_duration', return_value=0.5) 
    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res.status_code == 400
    assert "Minimum booking duration is 1 hour" in res.get_json()['message']

# TC_BOOK_05: Đúng 1 tiếng 
def test_valid_minimum_duration(test_client, auth_user, default_booking_mocks):
    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res.status_code == 201

# TC_BOOK_06: Quá 3 sân/ngày 
def test_book_over_limit_per_day(test_client, mocker, auth_user, default_booking_mocks):
    mocker.patch('bapp.index.dao.count_user_bookings_per_day', return_value=3) 
    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res.status_code == 400
    assert "maximum of 3 courts per day" in res.get_json()['message']

# TC_BOOK_07: Trùng lịch 
def test_time_conflict_validation(test_client, mocker, auth_user, default_booking_mocks):
    mocker.patch('bapp.index.dao.is_field_available', return_value=False) 
    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res.status_code == 409
    assert "This court is already booked" in res.get_json()['message']

# TC_BOOK_08: Thiếu fields
def test_book_missing_fields(test_client, auth_user, default_booking_mocks):
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1'
    })
    assert res.status_code == 400
    assert "Missing required fields!" in res.get_json()['message']

# TC_BOOK_09: Sai format ngày
def test_booking_date_format(test_client, auth_user, default_booking_mocks):
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': '10-04-2025'
    })
    assert res.status_code == 400
    assert "Invalid date format" in res.get_json()['message']

# TC_BOOK_10: Sân/Giờ ảo 
def test_book_field_or_slot_not_exist(test_client, mocker, auth_user, default_booking_mocks):
    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(None, None))
    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res.status_code == 404
    assert "Field or time slot not found!" in res.get_json()['message']

# TC_BOOK_11: Database Error 
def test_book_internal_database_error(test_client, mocker, auth_user, default_booking_mocks):
    mocker.patch('bapp.index.dao.create_new_booking', side_effect=Exception("Simulated Database Error")) 
    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res.status_code == 500
    assert "Simulated Database Error" in res.get_json()['message']

# TC_BOOK_12: Race Condition
def test_book_concurrent_race_condition(test_client, mocker, auth_user, default_booking_mocks):
    mocker.patch('bapp.index.dao.is_field_available', side_effect=[True, False]) 
    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    res1 = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    res2 = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res1.status_code == 201
    assert res2.status_code == 409

# TC_BOOK_13: Xử lý Timezone 
def test_book_timezone_handling(test_client, auth_user, default_booking_mocks):
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res.status_code == 201

# TC_BOOK_14: Trạng thái sân thay đổi 
def test_court_status_changes_after_booking(test_client, mocker, auth_user, default_booking_mocks):
    mocker.patch('bapp.index.dao.is_field_available', side_effect=[True, False])
    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    res1 = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    res2 = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res1.status_code == 201
    assert res2.status_code == 409

# TC_BOOK_15: Đặt nhiều loại sân
def test_book_different_court_types(test_client, mocker, auth_user, default_booking_mocks, sample_fields):
    class FakeSlot: 
        id = 1
        name = "18:00 - 19:00"
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("19:00", "%H:%M").time()

    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    for field in sample_fields:
        mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(field, FakeSlot())) 
        res = test_client.post('/api/bookings', data={
            'field_id': str(field.id), 
            'time_slots_id': '1', 
            'booking_date': future_date
        })
        data = res.get_json()
        assert res.status_code == 201
        assert data['data']['field_name'] == field.name

#TC_BOOK_16: 


#TC_BOOK_17:



#TC_BOOK_18:





