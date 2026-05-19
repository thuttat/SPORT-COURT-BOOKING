import pytest
from datetime import datetime, timedelta
from bapp.models import UserRole, BookingStatus
from tests.test_base import test_client, test_app, test_session

# ==========================================
# FIXTURES (Giả lập phiên đăng nhập)
# ==========================================
@pytest.fixture
def auth_admin(mocker):
    class FakeAdmin:
        is_authenticated = True; 
        id = 1; 
        user_role = UserRole.ADMIN
    mocker.patch('flask_login.utils._get_user', return_value=FakeAdmin())
    return FakeAdmin()

@pytest.fixture
def auth_user(mocker):
    class FakeUser:
        is_authenticated = True; 
        id = 2; 
        user_role = UserRole.USER
    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    return FakeUser()




# TC_E2E_01: quy trình đặt sân và hủy đặt sân 
def test_e2e_booking_and_cancellation_flow(test_client, auth_user, mocker):
    future_date = (datetime.now() + timedelta(days=2))
    
    class FakeField: 
        id = 1; 
        name = "Sân E2E"; 
        price_per_hour = 100000
    class FakeSlot: 
        id = 1; 
        name = "18:00 - 19:00"; 
        price_multiplier = 1.0
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("19:00", "%H:%M").time()
    class FakeNewBooking: 
        id = 999; 
        total_price = 100000
    
    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(FakeField(), FakeSlot()))
    mocker.patch('bapp.index.dao.is_field_available', return_value=True)
    mocker.patch('bapp.index.dao.count_user_bookings_per_day', return_value=0)
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=0)
    mocker.patch('bapp.index.dao.create_new_booking', return_value=FakeNewBooking())

    res_book = test_client.post('/api/bookings', data={
        'field_id': '1', 
        'time_slots_id': '1', 
        'booking_date': future_date.strftime("%Y-%m-%d")
    })
    assert res_book.status_code == 201


    class FakeBookingToCancel:
        id = 999; user_id = auth_user.id; status = BookingStatus.CONFIRMED
        booking_date = future_date.date(); time_slot = FakeSlot()
    
    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=FakeBookingToCancel())
    mocker.patch('bapp.index.dao.update_booking_status', return_value=True)

    res_cancel = test_client.delete('/api/bookings/999')
    assert res_cancel.status_code == 200
    assert "Booking canceled successfully" in res_cancel.get_json()['message']




# TC_E2E_02: Flow admin thêm court mới và người dùng đặt sân đó
def test_e2e_admin_add_court_then_user_books(test_client, auth_admin, mocker):
    class FakeNewField:
        id = 99; name = "Court Z"; 
        price_per_hour = 100000; 
        description = ""; 
        image = "img"; 
        is_active = True
        created_at = datetime.now()
        field_type = mocker.MagicMock(); 
        field_type.name = "FOOTBALL"
  
    mocker.patch('bapp.admin.Field.query').filter_by.return_value.first.return_value = None
    mocker.patch('bapp.admin.dao.add_field', return_value=FakeNewField())

    res_add = test_client.post('/api/admin/fields', data={
        'name': 'Court Z', 
        'price_per_hour': '100000', 
        'field_type': 'FOOTBALL'
    })
    assert res_add.status_code == 201
    
  

    class FakeUser:
        is_authenticated = True; 
        id = 2; 
        user_role = UserRole.USER
    

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    
    class FakeSlot: 
        id = 1; name = "18:00 - 19:00"; 
        price_multiplier = 1.0
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("19:00", "%H:%M").time()
    class FakeNewBooking: 
        id = 1; 
        total_price = 100000
        
    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(FakeNewField(), FakeSlot()))
    mocker.patch('bapp.index.dao.is_field_available', return_value=True)
    mocker.patch('bapp.index.dao.count_user_bookings_per_day', return_value=0)
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=0)
    mocker.patch('bapp.index.dao.create_new_booking', return_value=FakeNewBooking())

    future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    res_book = test_client.post('/api/bookings', data={
        'field_id': '99', 
        'time_slots_id': '1', 
        'booking_date': future_date
    })
    assert res_book.status_code == 201





# TC_E2E_03: Chặn đặt chỗ sau lần thử thứ 4
def test_e2e_booking_blocked_on_4th_attempt(test_client, auth_user, mocker):
    class FakeField: 
        id = 1; 
        name = "Sân E2E"; 
        price_per_hour = 100000
    class FakeSlot: 
        id = 1; 
        name = "18:00 - 19:00";
        price_multiplier = 1.0
        start_time = datetime.strptime("18:00", "%H:%M").time()
        end_time = datetime.strptime("19:00", "%H:%M").time()
    
    mocker.patch('bapp.index.dao.get_field_and_slot', return_value=(FakeField(), FakeSlot()))
    mocker.patch('bapp.index.dao.is_field_available', return_value=True)
    mocker.patch('bapp.index.dao.count_cancellations_by_user', return_value=0)
    mocker.patch('bapp.index.dao.count_user_bookings_per_day', return_value=3)
    
    future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
   
    res = test_client.post('/api/bookings', data={
        'field_id': '1', 'time_slots_id': '1', 'booking_date': future_date
    })
    data = res.get_json()
    assert res.status_code == 400
    assert data['status'] == "error"
    assert "maximum of 3 courts per day" in data['message']

