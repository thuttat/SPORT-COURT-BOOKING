import pytest
import concurrent.futures
from unittest.mock import patch, MagicMock
from datetime import date, datetime, time
from bapp.index import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# TC_BOOK_02
@patch('bapp.index.current_user')
def test_tc_book_02_without_login(mock_current_user, client):
    mock_current_user.is_authenticated = False

    response = client.post('/api/bookings', data={
        'field_id': 'c1',
        'time_slots_id': 'ts1',
        'booking_date': '2026-12-31'
    })

    json_data = response.get_json()
    assert response.status_code == 401
    assert json_data['message'] == "Please login to book a court"


# TC_BOOK_03
@patch('bapp.index.current_user')
@patch('bapp.index.utils.parse_date')
@patch('bapp.index.dao.get_field_and_slot')
def test_tc_book_03_past_time(mock_get_fs, mock_parse_date, mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_current_user.id = 1
    mock_parse_date.return_value = date(2000, 1, 1)
    mock_field = MagicMock()
    mock_slot = MagicMock()
    mock_slot.start_time = time(8, 0)
    mock_get_fs.return_value = (mock_field, mock_slot)

    response = client.post('/api/bookings', data={
        'field_id': 'c1', 'time_slots_id': 'ts1', 'booking_date': '2000-01-01'
    })

    assert response.status_code == 400
    assert response.get_json()['message'] == "Cannot book a court in the past"


# TC_BOOK_04
@patch('bapp.index.current_user')
@patch('bapp.index.utils.parse_date')
@patch('bapp.index.dao.get_field_and_slot')
@patch('bapp.index.dt_class')
@patch('bapp.index.utils.calculate_duration')
def test_tc_book_04_minimum_duration(mock_calc_duration, mock_dt, mock_get_fs, mock_parse_date, mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_current_user.id = 1
    mock_parse_date.return_value = date(2030, 1, 1)
    mock_dt.now.return_value = datetime(2029, 1, 1)
    mock_dt.combine.return_value = datetime(2030, 1, 1, 8, 0)

    mock_get_fs.return_value = (MagicMock(), MagicMock())
    mock_calc_duration.return_value = 0.5

    response = client.post('/api/bookings', data={
        'field_id': 'c1', 'time_slots_id': 'ts1', 'booking_date': '2030-01-01'
    })

    assert response.status_code == 400
    assert response.get_json()['message'] == "Minimum booking duration is 1 hour"


# TC_BOOK_06
@patch('bapp.index.current_user')
@patch('bapp.index.utils.parse_date')
@patch('bapp.index.dao.get_field_and_slot')
@patch('bapp.index.dt_class')
@patch('bapp.index.utils.calculate_duration')
@patch('bapp.index.dao.count_user_bookings_per_day')
def test_tc_book_06_quota_limit(mock_count_bookings, mock_calc_duration, mock_dt, mock_get_fs, mock_parse_date, mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_parse_date.return_value = date(2030, 1, 1)
    mock_dt.now.return_value = datetime(2029, 1, 1)
    mock_dt.combine.return_value = datetime(2030, 1, 1, 8, 0)
    mock_get_fs.return_value = (MagicMock(), MagicMock())
    mock_calc_duration.return_value = 2.0

    mock_count_bookings.return_value = 3

    response = client.post('/api/bookings', data={
        'field_id': 'c1', 'time_slots_id': 'ts1', 'booking_date': '2030-01-01'
    })

    assert response.status_code == 400
    assert response.get_json()['message'] == "You can only book a maximum of 3 courts per day"


# TC_BOOK_07
@patch('bapp.index.current_user')
@patch('bapp.index.utils.parse_date')
@patch('bapp.index.dao.get_field_and_slot')
@patch('bapp.index.dt_class')
@patch('bapp.index.utils.calculate_duration')
@patch('bapp.index.dao.count_user_bookings_per_day')
@patch('bapp.index.dao.is_field_available')
def test_tc_book_07_time_conflict(mock_is_available, mock_count_bookings, mock_calc_duration, mock_dt, mock_get_fs, mock_parse_date, mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_parse_date.return_value = date(2030, 1, 1)
    mock_dt.now.return_value = datetime(2029, 1, 1)
    mock_dt.combine.return_value = datetime(2030, 1, 1, 8, 0)
    mock_get_fs.return_value = (MagicMock(), MagicMock())
    mock_calc_duration.return_value = 1.0
    mock_count_bookings.return_value = 1

    mock_is_available.return_value = False

    response = client.post('/api/bookings', data={
        'field_id': 'c1', 'time_slots_id': 'ts1', 'booking_date': '2030-01-01'
    })
    assert response.status_code == 409
    assert response.get_json()['message'] == "This court is already booked"


# TC_BOOK_01 & TC_BOOK_05
@patch('bapp.index.current_user')
@patch('bapp.index.utils.parse_date')
@patch('bapp.index.dao.get_field_and_slot')
@patch('bapp.index.dt_class')
@patch('bapp.index.utils.calculate_duration')
@patch('bapp.index.dao.count_user_bookings_per_day')
@patch('bapp.index.dao.is_field_available')
@patch('bapp.index.dao.create_new_booking')
def test_tc_book_01_and_05_success(mock_create_booking, mock_is_available, mock_count_bookings, mock_calc_duration, mock_dt, mock_get_fs, mock_parse_date, mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_parse_date.return_value = date(2030, 1, 1)
    mock_dt.now.return_value = datetime(2029, 1, 1)
    mock_dt.combine.return_value = datetime(2030, 1, 1, 8, 0)

    mock_field = MagicMock()
    mock_field.name = "Sân bóng đá Mini A"
    mock_slot = MagicMock()
    mock_slot.name = "08:00 - 09:00"
    mock_get_fs.return_value = (mock_field, mock_slot)

    mock_calc_duration.return_value = 1.0
    mock_count_bookings.return_value = 0
    mock_is_available.return_value = True

    mock_new_booking = MagicMock()
    mock_new_booking.id = 999
    mock_new_booking.total_price = 200000
    mock_create_booking.return_value = mock_new_booking

    response = client.post('/api/bookings', data={
        'field_id': 'c1', 'time_slots_id': 'ts1', 'booking_date': '2030-01-01'
    })

    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data['status'] == "success"
    assert json_data['message'] == "Booking successful!"
    assert json_data['data']['booking_id'] == 999


# TC_BOOK_08
@patch('bapp.index.current_user')
def test_booking_missing_fields(mock_current_user, client):
    mock_current_user.is_authenticated = True
    response = client.post('/api/bookings', data={
        'field_id': 'c1',
        'time_slots_id': 'ts1'
    })

    assert response.status_code == 400
    assert response.get_json()['message'] == "Missing required fields!"


# TC_BOOK_09
@patch('bapp.index.current_user')
@patch('bapp.index.utils.parse_date')
def test_booking_invalid_date_format(mock_parse_date, mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_parse_date.return_value = None

    response = client.post('/api/bookings', data={
        'field_id': 'c1',
        'time_slots_id': 'ts1',
        'booking_date': '31-12-2026'
    })

    assert response.status_code == 400
    assert response.get_json()['message'] == "Invalid date format (YYYY-MM-DD)!"


# TC_BOOK_10
@patch('bapp.index.current_user')
@patch('bapp.index.utils.parse_date')
@patch('bapp.index.dao.get_field_and_slot')
def test_booking_not_found(mock_get_fs, mock_parse_date, mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_parse_date.return_value = date(2030, 1, 1)
    mock_get_fs.return_value = (None, None)

    response = client.post('/api/bookings', data={
        'field_id': 'fake_field_999',
        'time_slots_id': 'fake_slot_999',
        'booking_date': '2030-01-01'
    })

    assert response.status_code == 404
    assert response.get_json()['message'] == "Field or time slot not found!"


# TC_BOOK_11
@patch('bapp.index.current_user')
@patch('bapp.index.utils.parse_date')
@patch('bapp.index.dao.get_field_and_slot')
@patch('bapp.index.dt_class')
@patch('bapp.index.utils.calculate_duration')
@patch('bapp.index.dao.count_user_bookings_per_day')
@patch('bapp.index.dao.is_field_available')
@patch('bapp.index.dao.create_new_booking')
@patch('bapp.index.db.session.rollback')
def test_booking_internal_server_error(mock_rollback, mock_create_booking, mock_is_available, mock_count_bookings, mock_calc_duration, mock_dt, mock_get_fs, mock_parse_date, mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_parse_date.return_value = date(2030, 1, 1)
    mock_dt.now.return_value = datetime(2029, 1, 1)
    mock_dt.combine.return_value = datetime(2030, 1, 1, 8, 0)
    mock_get_fs.return_value = (MagicMock(), MagicMock())
    mock_calc_duration.return_value = 2.0
    mock_count_bookings.return_value = 0
    mock_is_available.return_value = True

    mock_create_booking.side_effect = Exception("Database connection lost!")

    response = client.post('/api/bookings', data={
        'field_id': 'c1', 'time_slots_id': 'ts1', 'booking_date': '2030-01-01'
    })

    assert response.status_code == 500
    assert response.get_json()['message'] == "Database connection lost!"
    mock_rollback.assert_called_once()


# TC_BOOK_12
@patch('bapp.index.current_user')
@patch('bapp.index.dao.is_field_available')
@patch('bapp.index.dao.create_new_booking')
def test_concurrency_prevent_double_booking(mock_create_booking, mock_is_available, mock_current_user):
    mock_current_user.is_authenticated = True
    mock_is_available.return_value = True

    mock_new_booking = MagicMock()
    mock_new_booking.id = 999
    mock_create_booking.return_value = mock_new_booking

    def make_booking_request():
        # VÁ LỖI FLASK CONTEXT: Tạo test_client mới cho từng luồng chạy song song
        with app.test_client() as thread_client:
            return thread_client.post('/api/bookings', data={
                'field_id': 'c1', 'time_slots_id': 'ts1', 'booking_date': '2030-01-01'
            })

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(make_booking_request) for _ in range(2)]
        responses = [f.result() for f in futures]

    success_count = sum(1 for r in responses if r.status_code == 201)
    assert success_count <= 1, "RACE CONDITION: Hệ thống cho phép 2 người đặt cùng 1 sân trong cùng 1 thời điểm!"


# TC_BOOK_13
@patch('bapp.index.current_user')
@patch('bapp.index.utils.parse_date')
@patch('bapp.index.dao.get_field_and_slot')
@patch('bapp.index.dt_class')
def test_logic_timezone_differences(mock_dt_class, mock_get_fs, mock_parse_date, mock_current_user, client):
    mock_current_user.is_authenticated = True
    mock_parse_date.return_value = date(2030, 1, 1)

    mock_field = MagicMock()
    mock_slot = MagicMock()
    mock_slot.start_time = time(8, 0)
    mock_get_fs.return_value = (mock_field, mock_slot)

    mock_dt_class.combine.return_value = datetime(2030, 1, 1, 8, 0, 0)
    mock_dt_class.now.return_value = datetime(2030, 1, 1, 10, 0, 0)

    response = client.post('/api/bookings', data={
        'field_id': 'c1', 'time_slots_id': 'ts1', 'booking_date': '2030-01-01'
    })

    assert response.status_code != 400