import pytest
from datetime import datetime
from bapp.models import UserRole, FieldType, BookingStatus

from tests.test_base import test_client, test_app, test_session


@pytest.fixture
def auth_user(mocker):
    class FakeUser:
        is_authenticated = True
        id = 2
        username = "nguyenauser"
        fullname = "Nguyen Van A"
        email = "nguyena@gmail.com"
        avatar = "avatar.png"
        user_role = UserRole.USER

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    return FakeUser()



# TC_GUEST_01: Khách xem danh sách sân không cần đăng nhập
def test_guest_view_courts(test_client, mocker):
    class FakeField:
        id = 1; 
        name = "Sân Bóng Guest"; 
        price_per_hour = 100000; 
        description = "Mô tả"; 
        image = "img.jpg"
        field_type = mocker.MagicMock(); 
        field_type.name = "FOOTBALL"

    class FakePagination:
        items = [FakeField()]; 
        total = 1; 
        pages = 1; 
        has_next = False

    mocker.patch('bapp.index.dao.get_active_fields_paginated', return_value=FakePagination())
    
    res = test_client.get('/api/fields')
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']) > 0

# TC_GUEST_02: Khách có thể lọc sân theo loại hình thể thao
def test_guest_filter_courts_by_sport_type(test_client, mocker):
    class FakePagination:
        items = []
        total = 0
        pages = 1
        has_next = False
    
    mocker.patch('bapp.index.dao.get_active_fields_paginated', return_value=FakePagination())
  
    res = test_client.get('/api/fields?sport_type=TENNIS')
    data = res.get_json()
    assert res.status_code == 200
    assert data['status'] == 'success'


# TC_GUEST_03: Khách có thể tìm kiếm sân theo tên
def test_guest_search_court_by_name(test_client, mocker):
    class FakePagination:
        items = []
        total = 0
        pages = 1
        has_next = False
    
    mocker.patch('bapp.index.dao.get_active_fields_paginated', return_value=FakePagination())
    
    res = test_client.get('/api/fields?search=VIP')
    data = res.get_json()
    assert res.status_code == 200
    assert data['status'] == 'success'



# TC_USER_01: User xem chi tiết 1 booking
def test_user_view_booking_detail(test_client, auth_user, mocker):
    class FakeBookingDetail:
        id = 1; user_id = auth_user.id; booking_date = datetime.now(); total_price = 150000; created_at = datetime.now()
        status = mocker.MagicMock(); status.name = "CONFIRMED"
        field = mocker.MagicMock(); field.name = "Sân 1"; field.field_type.name = "FOOTBALL"
        time_slot = mocker.MagicMock(); time_slot.name = "18:00 - 19:00"

    mocker.patch('bapp.index.dao.get_booking_by_id', return_value=FakeBookingDetail())
    
    res = test_client.get('/api/my-bookings/1')
    data = res.get_json()

    assert res.status_code == 200
    assert data['data']['field_name'] == "Sân 1"



# TC_USER_02: Phân trang lịch sử đặt sân
def test_user_booking_history_pagination(test_client, auth_user, mocker):
    class FakePagination:
        items = []; 
        total = 15; 
        pages = 3; 
        has_next = True; 
        has_prev = True
    
    mocker.patch('bapp.index.dao.get_bookings_paginated', return_value=FakePagination())
    
    res = test_client.get('/api/my-bookings?page=2')
    data = res.get_json()

    assert res.status_code == 200
    assert data['pagination']['current_page'] == 2
    assert data['pagination']['total_pages'] == 3



# TC_USER_03: Kiểm tra "Upcoming" và "His" có hiển thị đúng thông tin đặt chỗ hay không
def test_user_booking_tabs_upcoming_and_history(test_client, auth_user, mocker):
    class FakePagination:
        items = []
        total = 0
        pages = 1
        has_next = False
        has_prev = False
    
    mocker.patch('bapp.index.dao.get_bookings_paginated', return_value=FakePagination())
    
    res_upcoming = test_client.get('/api/my-bookings?tab=upcoming')
    assert res_upcoming.status_code == 200

    res_history = test_client.get('/api/my-bookings?tab=history')
    assert res_history.status_code == 200



# TC_USER_04: Kiểm tra trang Profile lấy đúng thông tin 
def test_user_profile_information(test_client, auth_user):
    res = test_client.get('/api/me')
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['fullname'] == "Nguyen Van A"
    assert data['data']['email'] == "nguyena@gmail.com"