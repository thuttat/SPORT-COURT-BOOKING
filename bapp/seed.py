import datetime
from bapp import app, db
from bapp.models import (
    User, Field, TimeSlots, Booking, Payment,
    Service, BookingDetail,
    UserRole, FieldType, BookingStatus, PaymentMethod
)
from werkzeug.security import generate_password_hash

TODAY = datetime.date.today()
NOW = datetime.datetime.now()


def create_dummy_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        slots = [
            TimeSlots(name='Ca Sáng Sớm (5h30 - 7h00)',
                      start_time=datetime.time(5, 30), end_time=datetime.time(7, 0),
                      price_multiplier=0.8),
            TimeSlots(name='Ca Sáng (7h00 - 8h30)',
                      start_time=datetime.time(7, 0), end_time=datetime.time(8, 30),
                      price_multiplier=1.0),
            TimeSlots(name='Ca Chiều (15h00 - 16h30)',
                      start_time=datetime.time(15, 0), end_time=datetime.time(16, 30),
                      price_multiplier=1.0),
            TimeSlots(name='Ca Giờ Vàng 1 (17h00 - 18h30)',
                      start_time=datetime.time(17, 0), end_time=datetime.time(18, 30),
                      price_multiplier=1.5),
            TimeSlots(name='Ca Giờ Vàng 2 (18h30 - 20h00)',
                      start_time=datetime.time(18, 30), end_time=datetime.time(20, 0),
                      price_multiplier=1.5),
            TimeSlots(name='Ca Tối Muộn (20h00 - 21h30)',
                      start_time=datetime.time(20, 0), end_time=datetime.time(21, 30),
                      price_multiplier=1.2),
            TimeSlots(name='Ca Chớp Nhoáng (12h00 - 12h30)',
                      start_time=datetime.time(12, 0), end_time=datetime.time(12, 30),
                      price_multiplier=1.0),
        ]
        db.session.add_all(slots)
        db.session.commit()

        slot_sang_som   = slots[0]
        slot_sang       = slots[1]
        slot_chieu      = slots[2]
        slot_vang1      = slots[3]
        slot_vang2      = slots[4]
        slot_toi        = slots[5]
        slot_chop_nhoang = slots[6]


        pwd = generate_password_hash('User@12345')

        admin = User(username='duyadmin', password=generate_password_hash('Admin@12345'),
                     fullname='Nguyễn Triệu Duy', email='duy@gmail.com',
                     user_role=UserRole.ADMIN, avatar='default.png')

        user_normal = User(username='user_normal', password=pwd,
                           fullname='Nguyễn Văn A', email='usernormal@gmail.com',
                           user_role=UserRole.USER, avatar='default.png')

        user_3bk = User(username='user_3bookings', password=pwd,
                        fullname='Trần Thị B', email='user3bk@gmail.com',
                        user_role=UserRole.USER, avatar='default.png')

        user_2bk = User(username='user_2bookings', password=pwd,
                        fullname='Lê Văn C', email='user2bk@gmail.com',
                        user_role=UserRole.USER, avatar='default.png')

        user_restricted = User(username='user_restricted', password=pwd,
                               fullname='Phạm Thị D', email='userrestricted@gmail.com',
                               user_role=UserRole.USER, avatar='default.png')

        user_2cancels = User(username='user_2cancels', password=pwd,
                             fullname='Hoàng Văn E', email='user2cancels@gmail.com',
                             user_role=UserRole.USER, avatar='default.png')

        user_other = User(username='user_other', password=pwd,
                          fullname='Vũ Thị F', email='userother@gmail.com',
                          user_role=UserRole.USER, avatar='default.png')


        user_many = User(username='user_many_bk', password=pwd,
                         fullname='Đỗ Văn G', email='usermany@gmail.com',
                         user_role=UserRole.USER, avatar='default.png')

        db.session.add_all([admin, user_normal, user_3bk, user_2bk,
                            user_restricted, user_2cancels, user_other, user_many])
        db.session.commit()

        field_fb1 = Field(name='Sân Bóng VIP 1 (5 người)',
                          field_type=FieldType.FOOTBALL, price_per_hour=200000,
                          description='Sân cỏ nhân tạo siêu mượt, có mái che',
                          image='bong_vip1.jpg', user_id=admin.id, is_active=True)
        field_fb2 = Field(name='Sân Bóng Thường 2 (7 người)',
                          field_type=FieldType.FOOTBALL, price_per_hour=300000,
                          description='Sân ngoài trời, cỏ mới thay',
                          image='bong_thuong.jpg', user_id=admin.id, is_active=True)
        field_tn  = Field(name='Sân Tennis Chuẩn ATP',
                          field_type=FieldType.TENNIS, price_per_hour=250000,
                          description='Mặt sân cứng, đạt chuẩn thi đấu',
                          image='tennis1.jpg', user_id=admin.id, is_active=True)
        field_bd1 = Field(name='Sân Cầu Lông Số 1',
                          field_type=FieldType.BADMINTON, price_per_hour=100000,
                          description='Sân thảm PVC chống trượt',
                          image='caulong1.jpg', user_id=admin.id, is_active=True)
        field_bd2 = Field(name='Sân Cầu Lông Số 2',
                          field_type=FieldType.BADMINTON, price_per_hour=100000,
                          description='Sân thảm PVC chống trượt, gần quạt mát',
                          image='caulong2.jpg', user_id=admin.id, is_active=True)

        field_maintenance = Field(name='Sân Bóng Bảo Trì',
                                  field_type=FieldType.FOOTBALL, price_per_hour=200000,
                                  description='Đang bảo trì, tạm ngừng hoạt động',
                                  image='bong_maintenance.jpg', user_id=admin.id, is_active=False)

        field_no_booking = Field(name='Sân Mới Chưa Có Lịch',
                                 field_type=FieldType.TENNIS, price_per_hour=200000,
                                 description='Sân mới khai trương, chưa có đặt lịch',
                                 image='tennis_new.jpg', user_id=admin.id, is_active=True)
        field_future_booking = Field(name='Sân Có Lịch Tương Lai',
                                     field_type=FieldType.BADMINTON, price_per_hour=100000,
                                     description='Sân có booking tương lai, không được xóa',
                                     image='caulong_future.jpg', user_id=admin.id, is_active=True)

        db.session.add_all([field_fb1, field_fb2, field_tn, field_bd1, field_bd2,
                            field_maintenance, field_no_booking, field_future_booking])
        db.session.commit()

        services = [
            Service(name='Nước khoáng Lavie', price=10000, unit='Chai'),
            Service(name='Bò húc (Redbull)', price=15000, unit='Lon'),
            Service(name='Thuê bóng thi đấu', price=50000, unit='Quả'),
            Service(name='Thuê trọng tài', price=150000, unit='Trận'),
            Service(name='Thuê áo Pitch (bộ)', price=30000, unit='Bộ 10 áo'),
        ]
        db.session.add_all(services)
        db.session.commit()

        bookings_to_add = []

        bk_3bk_1 = Booking(user_id=user_3bk.id, field_id=field_fb1.id,
                            time_slots_id=slot_sang_som.id, booking_date=TODAY,
                            duration=1.5, total_price=240000, status=BookingStatus.CONFIRMED)
        bk_3bk_2 = Booking(user_id=user_3bk.id, field_id=field_tn.id,
                            time_slots_id=slot_sang.id, booking_date=TODAY,
                            duration=1.5, total_price=375000, status=BookingStatus.PENDING)
        bk_3bk_3 = Booking(user_id=user_3bk.id, field_id=field_bd1.id,
                            time_slots_id=slot_chieu.id, booking_date=TODAY,
                            duration=1.5, total_price=150000, status=BookingStatus.PENDING)
        bookings_to_add += [bk_3bk_1, bk_3bk_2, bk_3bk_3]

        # ── TC_BOOK_16: user_2bk đã có đúng 2 booking hôm nay ──
        bk_2bk_1 = Booking(user_id=user_2bk.id, field_id=field_fb2.id,
                            time_slots_id=slot_sang_som.id, booking_date=TODAY,
                            duration=1.5, total_price=360000, status=BookingStatus.CONFIRMED)
        bk_2bk_2 = Booking(user_id=user_2bk.id, field_id=field_tn.id,
                            time_slots_id=slot_sang.id, booking_date=TODAY,
                            duration=1.5, total_price=375000, status=BookingStatus.CONFIRMED)
        bookings_to_add += [bk_2bk_1, bk_2bk_2]


        bk_occupied = Booking(user_id=user_normal.id, field_id=field_fb1.id,
                              time_slots_id=slot_vang1.id, booking_date=TODAY,
                              duration=1.5, total_price=450000, status=BookingStatus.CONFIRMED)
        bookings_to_add.append(bk_occupied)

        now_minus_30 = (NOW - datetime.timedelta(minutes=30)).time().replace(second=0, microsecond=0)
        now_plus_60  = (NOW + datetime.timedelta(minutes=60)).time().replace(second=0, microsecond=0)
        slot_active_now = TimeSlots(
            name=f'Ca Đang Diễn Ra ({now_minus_30.strftime("%H:%M")} - {now_plus_60.strftime("%H:%M")})',
            start_time=now_minus_30,
            end_time=now_plus_60,
            price_multiplier=1.0
        )
        db.session.add(slot_active_now)
        db.session.commit()

        bk_active = Booking(user_id=user_normal.id, field_id=field_bd2.id,
                            time_slots_id=slot_active_now.id, booking_date=TODAY,
                            duration=1.5, total_price=150000, status=BookingStatus.CONFIRMED)
        bookings_to_add.append(bk_active)
        start_lt2h = (NOW + datetime.timedelta(hours=1, minutes=59)).time().replace(second=0, microsecond=0)
        end_lt2h   = (NOW + datetime.timedelta(hours=3, minutes=29)).time().replace(second=0, microsecond=0)
        slot_lt2h = TimeSlots(
            name=f'Ca Sắp Diễn Ra < 2h ({start_lt2h.strftime("%H:%M")} - {end_lt2h.strftime("%H:%M")})',
            start_time=start_lt2h,
            end_time=end_lt2h,
            price_multiplier=1.0
        )
        db.session.add(slot_lt2h)
        db.session.commit()

        bk_lt2h = Booking(user_id=user_normal.id, field_id=field_tn.id,
                          time_slots_id=slot_lt2h.id, booking_date=TODAY,
                          duration=1.5, total_price=375000, status=BookingStatus.PENDING)
        bookings_to_add.append(bk_lt2h)

        start_eq2h = (NOW + datetime.timedelta(hours=2)).time().replace(second=0, microsecond=0)
        end_eq2h   = (NOW + datetime.timedelta(hours=3, minutes=30)).time().replace(second=0, microsecond=0)
        slot_eq2h = TimeSlots(
            name=f'Ca Boundary Đúng 2h ({start_eq2h.strftime("%H:%M")} - {end_eq2h.strftime("%H:%M")})',
            start_time=start_eq2h,
            end_time=end_eq2h,
            price_multiplier=1.0
        )
        db.session.add(slot_eq2h)
        db.session.commit()

        bk_eq2h = Booking(user_id=user_normal.id, field_id=field_bd1.id,
                          time_slots_id=slot_eq2h.id, booking_date=TODAY,
                          duration=1.5, total_price=150000, status=BookingStatus.PENDING)
        bookings_to_add.append(bk_eq2h)
        start_gt2h = (NOW + datetime.timedelta(hours=2, minutes=1)).time().replace(second=0, microsecond=0)
        end_gt2h   = (NOW + datetime.timedelta(hours=3, minutes=31)).time().replace(second=0, microsecond=0)
        slot_gt2h = TimeSlots(
            name=f'Ca Trên 2h ({start_gt2h.strftime("%H:%M")} - {end_gt2h.strftime("%H:%M")})',
            start_time=start_gt2h,
            end_time=end_gt2h,
            price_multiplier=1.0
        )
        db.session.add(slot_gt2h)
        db.session.commit()

        bk_gt2h = Booking(user_id=user_normal.id, field_id=field_fb2.id,
                          time_slots_id=slot_gt2h.id, booking_date=TODAY,
                          duration=1.5, total_price=450000, status=BookingStatus.PENDING)
        bookings_to_add.append(bk_gt2h)


        tomorrow = TODAY + datetime.timedelta(days=1)
        bk_other_user = Booking(user_id=user_other.id, field_id=field_fb1.id,
                                time_slots_id=slot_toi.id, booking_date=tomorrow,
                                duration=1.5, total_price=360000, status=BookingStatus.CONFIRMED)
        bookings_to_add.append(bk_other_user)


        future_date = TODAY + datetime.timedelta(days=3)
        bk_future = Booking(user_id=user_normal.id, field_id=field_future_booking.id,
                            time_slots_id=slot_vang1.id, booking_date=future_date,
                            duration=1.5, total_price=150000, status=BookingStatus.CONFIRMED)
        bookings_to_add.append(bk_future)


        end_1min_ago = (NOW - datetime.timedelta(minutes=1)).time().replace(second=0, microsecond=0)
        start_past   = (NOW - datetime.timedelta(hours=1, minutes=31)).time().replace(second=0, microsecond=0)
        slot_just_ended = TimeSlots(
            name=f'Ca Vừa Kết Thúc 1 Phút ({start_past.strftime("%H:%M")} - {end_1min_ago.strftime("%H:%M")})',
            start_time=start_past,
            end_time=end_1min_ago,
            price_multiplier=1.0
        )
        db.session.add(slot_just_ended)
        db.session.commit()

        bk_just_ended = Booking(user_id=user_normal.id, field_id=field_fb2.id,
                                time_slots_id=slot_just_ended.id, booking_date=TODAY,
                                duration=1.5, total_price=450000, status=BookingStatus.COMPLETED)
        bookings_to_add.append(bk_just_ended)


        for i in range(3):
            cancel_date = TODAY - datetime.timedelta(days=i + 1)
            bk_cancelled = Booking(
                user_id=user_restricted.id,
                field_id=field_bd1.id,
                time_slots_id=slot_sang.id,
                booking_date=cancel_date,
                duration=1.5,
                total_price=150000,
                status=BookingStatus.CANCELLED
            )
            bk_cancelled.created_at = datetime.datetime.now() - datetime.timedelta(days=i + 1)
            bookings_to_add.append(bk_cancelled)

        bk_restricted_pending = Booking(
            user_id=user_restricted.id, field_id=field_bd2.id,
            time_slots_id=slot_vang2.id,
            booking_date=TODAY + datetime.timedelta(days=2),
            duration=1.5, total_price=150000, status=BookingStatus.CONFIRMED
        )
        bookings_to_add.append(bk_restricted_pending)

        for i in range(2):
            cancel_date = TODAY - datetime.timedelta(days=i + 1)
            bk_2c = Booking(
                user_id=user_2cancels.id,
                field_id=field_tn.id,
                time_slots_id=slot_chieu.id,
                booking_date=cancel_date,
                duration=1.5,
                total_price=375000,
                status=BookingStatus.CANCELLED
            )
            bk_2c.created_at = datetime.datetime.now() - datetime.timedelta(days=i + 1)
            bookings_to_add.append(bk_2c)

        bk_2c_pending = Booking(
            user_id=user_2cancels.id, field_id=field_fb1.id,
            time_slots_id=slot_vang1.id,
            booking_date=TODAY + datetime.timedelta(days=2),
            duration=1.5, total_price=300000, status=BookingStatus.PENDING
        )
        bookings_to_add.append(bk_2c_pending)

        many_dates = [TODAY - datetime.timedelta(days=i) for i in range(7)]
        for i, d in enumerate(many_dates):
            field_cycle = [field_fb1, field_fb2, field_tn, field_bd1, field_bd2,
                           field_fb1, field_fb2][i]
            slot_cycle  = [slot_sang_som, slot_sang, slot_chieu, slot_sang_som,
                           slot_sang, slot_chieu, slot_sang_som][i]
            status_cycle = BookingStatus.COMPLETED if i > 0 else BookingStatus.CONFIRMED
            bk_m = Booking(
                user_id=user_many.id,
                field_id=field_cycle.id,
                time_slots_id=slot_cycle.id,
                booking_date=d,
                duration=1.5,
                total_price=150000,
                status=status_cycle
            )
            bookings_to_add.append(bk_m)

        bk_past = Booking(
            user_id=user_normal.id, field_id=field_fb2.id,
            time_slots_id=slot_sang_som.id,
            booking_date=TODAY - datetime.timedelta(days=5),
            duration=1.5, total_price=360000, status=BookingStatus.COMPLETED
        )
        bookings_to_add.append(bk_past)

        # ── TC_BOOK_15: đặt 3 loại sân — đã có football (bk_occupied),
        #    thêm tennis + badminton future ──
        bk_tennis_future = Booking(
            user_id=user_normal.id, field_id=field_tn.id,
            time_slots_id=slot_sang_som.id,
            booking_date=TODAY + datetime.timedelta(days=5),
            duration=1.5, total_price=375000, status=BookingStatus.CONFIRMED
        )
        bk_badminton_future = Booking(
            user_id=user_normal.id, field_id=field_bd1.id,
            time_slots_id=slot_sang.id,
            booking_date=TODAY + datetime.timedelta(days=5),
            duration=1.5, total_price=150000, status=BookingStatus.CONFIRMED
        )
        bookings_to_add += [bk_tennis_future, bk_badminton_future]


        bk_for_cancel_slot = Booking(
            user_id=user_normal.id, field_id=field_bd2.id,
            time_slots_id=slot_vang2.id,
            booking_date=TODAY + datetime.timedelta(days=1),
            duration=1.5, total_price=150000, status=BookingStatus.CONFIRMED
        )
        bookings_to_add.append(bk_for_cancel_slot)

        db.session.add_all(bookings_to_add)
        db.session.commit()


        payment = Payment(
            booking_id=bk_past.id,
            amount=bk_past.total_price,
            payment_method=PaymentMethod.CASH
        )
        db.session.add(payment)

        bd = BookingDetail(
            booking_id=bk_occupied.id,
            service_id=services[0].id,
            quantity=2,
            unit_price=services[0].price
        )
        db.session.add(bd)

        db.session.commit()
        print("=" * 60)


if __name__ == '__main__':
    create_dummy_data()