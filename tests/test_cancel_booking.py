import pytest
from datetime import datetime, timedelta, timezone
from bapp.models import BookingStatus, UserRole
import bapp.index

from tests.test_base import test_client, test_app, test_session


@pytest.fixture
def auth_user(mocker):
    class FakeUser:
        is_authenticated = True
        id = 1
        user_role = UserRole.USER

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    return FakeUser()


@pytest.fixture
def mock_bookings():

    class FakeField:
        id = 1; name = "Test"; price_per_hour = 100000
    class FakeSlot:
        id = 1; name = "18:00-19:00"
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time   = datetime.strptime("19:00", "%H:%M").time()

    class ValidBookingToCancel:
        id = 1
        user_id = 1
        status = "CONFIRMED"
        booking_date = datetime.now() + timedelta(days=1)

        time_slot = FakeSlot()

    class PastBooking:
        id = 2
        user_id = 1
        status = "COMPLETED"
        booking_date = datetime.now() - timedelta(days=1)

        time_slot = FakeSlot()

    now_in_vn = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=7)
    target_time = now_in_vn + timedelta(minutes=119)

    class FakeTooCloseSlot:
        start_time = target_time.time()

    class TooCloseBooking:
        id = 3
        user_id = 1
        status = "CONFIRMED"
        booking_date = target_time.date()
        time_slot = FakeTooCloseSlot()

    target_time_121 = now_in_vn + timedelta(minutes=121)
    class Fake121MinSlot:
        start_time = target_time_121.time()
    
    class Boundary121Booking:
        id = 6
        user_id = 1
        status = "CONFIRMED"
        booking_date = target_time_121.date()
        time_slot = Fake121MinSlot()


    class FakeOtherUserBooking:
        id = 4
        user_id = 99
        status = "CONFIRMED"
        booking_date = datetime.now()
        time_slot = FakeSlot()

    class AlreadyCancelledBooking:
        id = 5
        user_id = 1
        status = BookingStatus.CANCELLED

    class ActiveBooking:
        id = 5
        user_id = 1
        status = "CONFIRMED" 
        booking_date = datetime.now().date()
        class FakeActiveSlot:
            start_time = (datetime.now() - timedelta(minutes=30)).time()
        time_slot = FakeActiveSlot()
    
    class RestrictedUserBooking:
        id = 7
        user_id = 1
        status = "CONFIRMED"
        booking_date = datetime.now() + timedelta(days=2)
        class FakeSlot:
            start_time = datetime.strptime("10:00", "%H:%M").time()
        time_slot = FakeSlot()

    return {
        "valid": ValidBookingToCancel(),
        "past": PastBooking(),
        "too_close": TooCloseBooking(),
        "other_user": FakeOtherUserBooking(),
        "already_cancelled": AlreadyCancelledBooking(),
        "boundary_121": Boundary121Booking(),
        "active": ActiveBooking(),
        "restricted": RestrictedUserBooking(),
        "mock_field": FakeField(), 
        "mock_slot": FakeSlot(),  
    }
        




# TC_CAN_01: Hủy đơn đặt sân thành công (đúng 2h)
def test_cancel_booking_success(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["valid"])
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=0)
    mocker.patch('bapp.index.dao.update_booking_status', return_value=True)
    res = test_client.delete('/api/bookings/1')
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == "success"
    assert data['message'] == "Booking canceled successfully"


# TC_CAN_02: Hủy đơn đã đặt sân thành công (2h1')
def test_cancel_above_boundary_time(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["boundary_121"])
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=0)
    mocker.patch('bapp.index.dao.update_booking_status', return_value=True)
    res = test_client.delete('/api/bookings/6')
    data = res.get_json()
    
    assert res.status_code == 200
    assert data['status'] == "success"
    assert data['message'] == "Booking canceled successfully"
    

#TC_CAN_03: Hủy chỗ trước thgi quy định (1h59')
def test_cancel_below_boundary_time(test_client,mocker,auth_user,mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["too_close"])
    res = test_client.delete('/api/bookings/3')
    data = res.get_json()

    assert res.status_code == 400
    assert data['status'] == "error"
    assert "Cannot cancel a booking less than 2 hours before start time" in data['message']


# TC_CAN_04: Hủy đơn đặt sân của người dùng khác 
def test_cancel_unauthorized(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["other_user"])
    res = test_client.delete('/api/bookings/4')
    data = res.get_json()
    
    assert res.status_code == 403
    assert data['status'] == "error"
    assert "You are not authorized to cancel this booking" in data['message'] 


#TC_CAN_05: Hủy đơn đặt sân (sân đang diễn ra)
def test_cancel_booking_not_found(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["active"])
    res = test_client.delete('/api/bookings/5')
    data = res.get_json()
    
    assert res.status_code == 400
    assert data['status'] == "error"
    assert "Cannot cancel a court that is currently in use" in data['message']


#TC_CAN_06: Hạn chế tài khoản hủy (quá 3 lần/week)
def test_cancel_excessive_limit(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["restricted"])
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=3)
    mock_update = mocker.patch('bapp.index.dao.update_booking_status')
    res = test_client.delete('/api/bookings/7')
    data = res.get_json()
    
    assert res.status_code == 403 
    assert data['status'] == "error"
    assert "Account restricted from booking for 24 hours due to excessive cancellations" in data['message']
    mock_update.assert_not_called()

#TC_CAN_07: Sau khi hủy -> slot Available
def test_cancel_booking_after_slot_available(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["valid"])
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=0)  # ← thêm
    mocker.patch('bapp.index.dao.update_booking_status', return_value=True)

    res = test_client.delete('/api/bookings/1')
    assert res.status_code == 200

    mocker.patch('bapp.index.dao.get_all_time_slots', return_value=[])
    mocker.patch('bapp.index.dao.is_field_available', return_value=True)

    res_calendar = test_client.get('/api/fields/1/slots?date=2026-05-15')  
    data_calendar = res_calendar.get_json()

    assert res_calendar.status_code == 200
    assert data_calendar['status'] == 'success'
    assert all(slot['is_available'] for slot in data_calendar['data'])  


#TC_CAN_08: Hủy lần thứ 3/week được phép
def test_cancel_third_time_allowed(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["valid"])
    mocker.patch('bapp.index.dao.update_booking_status', return_value=True)
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=2)

    res = test_client.delete('/api/bookings/1')
    data = res.get_json()
    
    assert res.status_code == 200
    assert data['status'] == "success"
    assert data['message'] == "Booking canceled successfully"


#TC_CAN_09
def test_booking_blocked_during_restriction(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=4)
    fake_field = mock_bookings["mock_field"]
    fake_slot = mock_bookings["mock_slot"]
    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(fake_field, fake_slot))
    mocker.patch('bapp.index.utils.calculate_duration', return_value=1.0)

    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    res = test_client.post('/api/bookings', data={  
        'field_id': '1',
        'time_slots_id': '1',   
        'booking_date': future_date
    })
    data = res.get_json()

    assert res.status_code == 403
    assert data['status'] == "error"
    assert "Your account is temporarily restricted from booking for 24 hours" in data['message']

