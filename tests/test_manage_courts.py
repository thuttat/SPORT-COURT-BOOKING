import pytest
from datetime import datetime, timedelta
from bapp.models import UserRole, FieldType, BookingStatus
import bapp.index

from tests.test_base import test_client, test_app, test_session



@pytest.fixture
def auth_admin(mocker):
    class FakeAdmin:
        is_authenticated = True
        id = 1
        user_role = UserRole.ADMIN

    mocker.patch('flask_login.utils._get_user', return_value=FakeAdmin())
    return FakeAdmin()


@pytest.fixture
def auth_user(mocker):
    class FakeUser:
        is_authenticated = True
        id = 2
        user_role = UserRole.USER

    mocker.patch('flask_login.utils._get_user', return_value=FakeUser())
    return FakeUser()


@pytest.fixture
def mock_fields():
    class FakeField:
        id = 1
        name = "Sân Bóng VIP 1"
        field_type = FieldType.FOOTBALL
        price_per_hour = 200000.0
        description = "Sân cỏ nhân tạo"
        image = "default.jpg"
        is_active = True
        user_id = 1
        created_at = datetime(2025, 1, 1, 10, 0, 0)

    class FakeInactiveField:
        id = 2
        name = "Sân Cũ Đã Đóng"
        field_type = FieldType.TENNIS
        price_per_hour = 150000.0
        description = "Đã tắt"
        image = "old.jpg"
        is_active = False
        user_id = 1
        created_at = datetime(2024, 6, 1, 8, 0, 0)

    class FakeFieldOtherAdmin:
        id = 3
        name = "Sân Của Admin Khác"
        field_type = FieldType.BADMINTON
        price_per_hour = 100000.0
        description = "Không thuộc admin này"
        image = "other.jpg"
        is_active = True
        user_id = 99  

    return {
        "active": FakeField(),
        "inactive": FakeInactiveField(),
        "other_admin": FakeFieldOtherAdmin(),
    }


@pytest.fixture
def mock_bookings_for_field():
    class FakeSlotPast:
        start_time = (datetime.now() - timedelta(hours=2)).time()

    class FakeSlotFuture:
        start_time = (datetime.now() + timedelta(minutes=1)).time()

    class PastBooking:
        id = 10
        field_id = 1
        status = BookingStatus.CONFIRMED
        booking_date = datetime.now().date()
        time_slot = FakeSlotPast()

    class FutureBooking:
        id = 11
        field_id = 1
        status = BookingStatus.CONFIRMED
        booking_date = datetime.now().date()
        time_slot = FakeSlotFuture()

    return {
        "past": PastBooking(),
        "future": FutureBooking(),
    }



# TC_ADM_01: Non-admin user bị từ chối truy cập
def test_non_admin_access_denied(test_client, auth_user):
    res = test_client.get('/api/admin/fields')
    data = res.get_json()

    assert res.status_code == 403
    assert data['status'] == 'error'
    assert 'permission' in data['message'].lower() or 'forbidden' in data['message'].lower()



# TC_ADM_02: Tạo sân mới thành công với tên duy nhất
def test_add_new_field_success(test_client, auth_admin, mocker):
    class FakeNewField:
        id = 10
        name = "Sân Mới Unique"
        field_type = FieldType.FOOTBALL
        price_per_hour = 300000.0
        description = "Mô tả"
        image = "https://res.cloudinary.com/test/image.jpg"
        is_active = True
        created_at = datetime(2026, 5, 18, 10, 0, 0)

    # No existing field with that name
    mocker.patch('bapp.admin.Field.query') \
        .filter_by.return_value.first.return_value = None

    mocker.patch('bapp.admin.dao.add_field', return_value=FakeNewField())
    mocker.patch('bapp.admin.cloudinary.uploader.upload',
                 return_value={'secure_url': 'https://res.cloudinary.com/test/image.jpg'})

    res = test_client.post('/api/admin/fields', data={
        'name': 'Sân Mới Unique',
        'price_per_hour': '300000',
        'field_type': 'FOOTBALL',
        'description': 'Mô tả'
    })
    data = res.get_json()

    assert res.status_code == 201
    assert data['status'] == 'success'
    assert 'id' in data['data']


# ─────────────────────────────────────────────
# TC_ADM_03 – Tạo sân với tên đã tồn tại → lỗi
# ─────────────────────────────────────────────

def test_add_field_duplicate_name(test_client, auth_admin, mock_fields, mocker):
    """
    TC_ADM_03: Admin tạo sân với tên đã tồn tại → hệ thống báo lỗi duplicate.
    Expected: 400, message chứa 'already exists'
    """
    # Simulate existing field with same name
    mocker.patch(
        'bapp.admin.Field.query',
        **{'filter_by.return_value.first.return_value': mock_fields["active"]}
    )

    res = test_client.post('/api/admin/fields', data={
        'name': 'Sân Bóng VIP 1',  # already exists
        'price_per_hour': '200000',
        'field_type': 'FOOTBALL',
        'description': 'Trùng tên'
    })
    data = res.get_json()

    assert res.status_code == 400
    assert data['status'] == 'error'
    assert 'already exists' in data['message']


# ─────────────────────────────────────────────
# TC_ADM_04 – Xoá sân thành công (booking đã qua)
# ─────────────────────────────────────────────

def test_delete_field_with_only_past_bookings(test_client, auth_admin, mock_fields,
                                               mock_bookings_for_field, mocker):
    """
    TC_ADM_04: Admin xoá sân chỉ có booking đã kết thúc (past) → thành công.
    Expected: 200, status='success'
    """
    mocker.patch('bapp.admin.db.session.get', return_value=mock_fields["active"])
    mocker.patch(
        'bapp.admin.Booking.query',
        **{'filter.return_value.all.return_value': [mock_bookings_for_field["past"]]}
    )
    mocker.patch('bapp.admin.dao.delete_field', return_value=True)

    res = test_client.delete('/api/admin/fields/1')
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'


# ─────────────────────────────────────────────
# TC_ADM_05 – Xoá sân có booking tương lai → bị chặn
# ─────────────────────────────────────────────

def test_delete_field_with_future_booking(test_client, auth_admin, mock_fields,
                                           mock_bookings_for_field, mocker):
    """
    TC_ADM_05: Admin xoá sân có booking sắp tới (1 phút nữa) → hệ thống ngăn chặn.
    Expected: 400, message chứa 'future bookings'
    """
    mocker.patch('bapp.admin.db.session.get', return_value=mock_fields["active"])
    mocker.patch(
        'bapp.admin.Booking.query',
        **{'filter.return_value.all.return_value': [mock_bookings_for_field["future"]]}
    )

    res = test_client.delete('/api/admin/fields/1')
    data = res.get_json()

    assert res.status_code == 400
    assert data['status'] == 'error'
    assert 'future bookings' in data['message']


# ─────────────────────────────────────────────
# TC_ADM_06 – Cập nhật thông tin sân thành công
# ─────────────────────────────────────────────

def test_update_field_success(test_client, auth_admin, mock_fields, mocker):
    """
    TC_ADM_06: Admin cập nhật mô tả và giá của sân → thành công.
    Expected: 200, data phản ánh giá trị mới.
    """

    class UpdatedField:
        id = 1
        name = "Sân Bóng VIP 1"
        field_type = FieldType.FOOTBALL
        price_per_hour = 250000.0
        description = "Mô tả mới"
        image = "default.jpg"
        is_active = True

    mocker.patch('bapp.admin.db.session.get', return_value=mock_fields["active"])
    mocker.patch(
        'bapp.admin.Field.query',
        **{'filter.return_value.first.return_value': None}  # no duplicate name
    )
    mocker.patch('bapp.admin.dao.update_field', return_value=UpdatedField())

    res = test_client.patch('/api/admin/fields/1', data={
        'price_per_hour': '250000',
        'description': 'Mô tả mới'
    })
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['price_per_hour'] == 250000.0
    assert data['data']['description'] == 'Mô tả mới'


# ─────────────────────────────────────────────
# TC_ADM_07 – Đặt sân về trạng thái Maintenance (is_active=False)
# ─────────────────────────────────────────────

def test_set_field_to_maintenance(test_client, auth_admin, mock_fields, mocker):
    """
    TC_ADM_07: Admin tắt sân (is_active=False) → sân không còn hiển thị cho user.
    Expected: 200, is_active=False trong response.
    """

    class InactiveField:
        id = 1
        name = "Sân Bóng VIP 1"
        field_type = FieldType.FOOTBALL
        price_per_hour = 200000.0
        description = "Sân cỏ nhân tạo"
        image = "default.jpg"
        is_active = False

    mocker.patch('bapp.admin.db.session.get', return_value=mock_fields["active"])
    mocker.patch('bapp.admin.Field.query',
                 **{'filter.return_value.first.return_value': None})
    mocker.patch('bapp.admin.dao.update_field', return_value=InactiveField())

    res = test_client.patch('/api/admin/fields/1', data={'is_active': 'false'})
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['is_active'] is False


# ─────────────────────────────────────────────
# TC_ADM_08 – Admin xem danh sách tất cả sân (Read)
# ─────────────────────────────────────────────

def test_admin_get_all_fields(test_client, auth_admin, mock_fields, mocker):
    """
    TC_ADM_08: Admin truy cập trang Manage Courts → hiển thị danh sách đầy đủ.
    Expected: 200, data là list, có pagination.
    """

    class FakePagination:
        items = [mock_fields["active"], mock_fields["inactive"]]
        total = 2
        pages = 1
        has_next = False

    mocker.patch('bapp.admin.dao.get_fields_by_user_paginated',
                 return_value=FakePagination())

    res = test_client.get('/api/admin/fields')
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)
    assert len(data['data']) == 2
    assert 'pagination' in data


# ─────────────────────────────────────────────
# TC_ADM_09 – Bật lại sân từ Maintenance về Active
# ─────────────────────────────────────────────

def test_reactivate_field_from_maintenance(test_client, auth_admin, mock_fields, mocker):
    """
    TC_ADM_09: Admin bật lại sân đang Maintenance → is_active=True.
    Expected: 200, is_active=True trong response.
    """

    class ReactivatedField:
        id = 2
        name = "Sân Cũ Đã Đóng"
        field_type = FieldType.TENNIS
        price_per_hour = 150000.0
        description = "Đã mở lại"
        image = "old.jpg"
        is_active = True

    mocker.patch('bapp.admin.db.session.get', return_value=mock_fields["inactive"])
    mocker.patch('bapp.admin.Field.query',
                 **{'filter.return_value.first.return_value': None})
    mocker.patch('bapp.admin.dao.update_field', return_value=ReactivatedField())

    res = test_client.patch('/api/admin/fields/2', data={'is_active': 'true'})
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['is_active'] is True


# ─────────────────────────────────────────────
# TC_ADM_10 – Xoá sân chưa từng được đặt → thành công
# ─────────────────────────────────────────────

def test_delete_field_no_bookings(test_client, auth_admin, mock_fields, mocker):
    """
    TC_ADM_10: Admin xoá sân chưa có booking nào → thành công.
    Expected: 200, status='success'
    """
    mocker.patch('bapp.admin.db.session.get', return_value=mock_fields["active"])
    mocker.patch(
        'bapp.admin.Booking.query',
        **{'filter.return_value.all.return_value': []}  # no bookings at all
    )
    mocker.patch('bapp.admin.dao.delete_field', return_value=True)

    res = test_client.delete('/api/admin/fields/1')
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'


# ─────────────────────────────────────────────
# TC_ADM_11 – Admin không thể truy cập trang User (user_only endpoint)
# ─────────────────────────────────────────────

def test_admin_cannot_access_user_only_page(test_client, auth_admin):
    """
    TC_ADM_11: Admin cố truy cập endpoint chỉ dành cho USER role → bị từ chối.
    Expected: 403 Forbidden
    """
    res = test_client.get('/api/my-bookings')
    data = res.get_json()

    assert res.status_code == 403
    assert data['status'] == 'error'
    assert 'permission' in data['message'].lower() or 'forbidden' in data['message'].lower()


# ─────────────────────────────────────────────
# TC_ADM_12 – Dashboard hiển thị số liệu thống kê đúng
# ─────────────────────────────────────────────

def test_dashboard_summary_data(test_client, auth_admin, mocker):
    """
    TC_ADM_12: Admin xem Dashboard → hiển thị đúng total_fields, total_bookings.
    Expected: 200, data có các key thống kê cần thiết.
    """
    # Patch the DB query calls inside get_dashboard_summary
    mock_field_query = mocker.patch('bapp.admin.Field.query')
    mock_field_query.filter_by.return_value.count.side_effect = [5, 4]  # total, active

    mock_booking_query = mocker.patch('bapp.admin.Booking.query')
    mock_booking_query.join.return_value.filter.return_value.count.return_value = 20
    mock_booking_query.join.return_value.filter.return_value \
        .filter.return_value.count.return_value = 3

    res = test_client.get('/api/admin/dashboard/summary')
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'
    for key in ('total_fields', 'active_fields', 'total_bookings', 'bookings_today'):
        assert key in data['data']


# ─────────────────────────────────────────────
# TC_ADM_13 – Dashboard chart phân loại sân đúng loại thể thao
# ─────────────────────────────────────────────

def test_dashboard_chart_sport_distribution(test_client, auth_admin, mocker):
    """
    TC_ADM_13: Admin xem biểu đồ phân loại sân → dữ liệu phản ánh đúng tỉ lệ loại sân.
    Expected: 200, data là list chứa sport và count.
    """
    mocker.patch(
        'bapp.admin.db.session.query',
        return_value=mocker.MagicMock(
            filter=mocker.MagicMock(
                return_value=mocker.MagicMock(
                    group_by=mocker.MagicMock(
                        return_value=mocker.MagicMock(
                            all=mocker.MagicMock(return_value=[
                                (FieldType.FOOTBALL, 3),
                                (FieldType.BADMINTON, 2),
                                (FieldType.TENNIS, 1),
                            ])
                        )
                    )
                )
            )
        )
    )

    res = test_client.get('/api/admin/dashboard/chart-sport')
    data = res.get_json()

    assert res.status_code == 200
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)
    sports = [item['sport'] for item in data['data']]
    assert 'FOOTBALL' in sports or len(data['data']) >= 1


# ─────────────────────────────────────────────
# Bonus – Admin không thể thao tác trên sân của Admin khác
# ─────────────────────────────────────────────

def test_admin_cannot_edit_other_admins_field(test_client, auth_admin, mock_fields, mocker):
    """
    Bonus: Admin A không được phép sửa/xoá sân thuộc Admin B.
    Expected: 403 Access Denied
    """
    mocker.patch('bapp.admin.db.session.get', return_value=mock_fields["other_admin"])

    res = test_client.patch('/api/admin/fields/3', data={'description': 'Cố sửa'})
    data = res.get_json()

    assert res.status_code == 403
    assert data['status'] == 'error'
    assert 'Access Denied' in data['message']


def test_admin_cannot_delete_other_admins_field(test_client, auth_admin, mock_fields, mocker):
    """
    Bonus: Admin A không được xoá sân của Admin B.
    Expected: 403 Access Denied
    """
    mocker.patch('bapp.admin.db.session.get', return_value=mock_fields["other_admin"])

    res = test_client.delete('/api/admin/fields/3')
    data = res.get_json()

    assert res.status_code == 403
    assert data['status'] == 'error'
    assert 'Access Denied' in data['message']