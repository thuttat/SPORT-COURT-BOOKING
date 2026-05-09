import pytest
from datetime import datetime, timedelta
from bapp.models import UserRole
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
    class ValidBookingToCancel:
        id = 1
        user_id = 1
        status = "CONFIRMED"
        booking_date = datetime.now() + timedelta(days=1) 
        
    class PastBooking:
        id = 2
        user_id = 1
        status = "COMPLETED"
        booking_date = datetime.now() - timedelta(days=1)
        
    return {
        "valid": ValidBookingToCancel(),
        "past": PastBooking()
    }




# TC_CAN_01: Hủy đơn đặt sân hợp lệ thành công 
def test_cancel_booking_success(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["valid"])
    mocker.patch('bapp.index.dao.update_booking_status', return_value=True)

    res = test_client.patch('/api/bookings/1/cancel') 
    
    data = res.get_json()
    
    assert res.status_code == 200
    assert data['status'] == "success"


# TC_CAN_02: Cố tình hủy đơn đã đặt
def test_cancel_past_booking(test_client, mocker, auth_user, mock_bookings):
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=mock_bookings["past"])

    res = test_client.delete('/api/bookings/2')
    
    data = res.get_json()
    
    assert res.status_code == 400
    assert data['status'] == "error"
    