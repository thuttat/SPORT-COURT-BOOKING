from bapp import app, db
from bapp.models import User, Field, TimeSlots, UserRole, FieldType, Service
import datetime


def create_dummy_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        user1 = User(
            username='duyadmin',
            password='123',
            fullname='Nguyễn Triệu Duy',
            email='duy@gmail.com',
            user_role=UserRole.ADMIN,
            avatar='default.png'
        )
        db.session.add(user1)
        db.session.commit()

        fields = [
            Field(name='Sân Bóng VIP 1 (5 người)', field_type=FieldType.FOOTBALL, price_per_hour=200000,
                  description='Sân cỏ nhân tạo siêu mượt, có mái che', image='bong_vip1.jpg', user_id=user1.id),
            Field(name='Sân Bóng Thường 2 (7 người)', field_type=FieldType.FOOTBALL, price_per_hour=300000,
                  description='Sân ngoài trời, cỏ mới thay', image='bong_thuong.jpg', user_id=user1.id),
            Field(name='Sân Tennis Chuẩn ATP', field_type=FieldType.TENNIS, price_per_hour=250000,
                  description='Mặt sân cứng, đạt chuẩn thi đấu', image='tennis1.jpg', user_id=user1.id),
            Field(name='Sân Cầu Lông Số 1', field_type=FieldType.BADMINTON, price_per_hour=100000,
                  description='Sân thảm PVC chống trượt', image='caulong1.jpg', user_id=user1.id),
            Field(name='Sân Cầu Lông Số 2', field_type=FieldType.BADMINTON, price_per_hour=100000,
                  description='Sân thảm PVC chống trượt, gần quạt mát', image='caulong2.jpg', user_id=user1.id)
        ]
        db.session.add_all(fields)

        slots = [
            TimeSlots(name='Ca Sáng Sớm (5h30 - 7h00)', start_time=datetime.time(5, 30), end_time=datetime.time(7, 0),
                      price_multiplier=0.8),  # Giờ ế, giảm giá 20%
            TimeSlots(name='Ca Sáng (7h00 - 8h30)', start_time=datetime.time(7, 0), end_time=datetime.time(8, 30),
                      price_multiplier=1.0),
            TimeSlots(name='Ca Chiều (15h00 - 16h30)', start_time=datetime.time(15, 0), end_time=datetime.time(16, 30),
                      price_multiplier=1.0),
            TimeSlots(name='Ca Giờ Vàng 1 (17h00 - 18h30)', start_time=datetime.time(17, 0),
                      end_time=datetime.time(18, 30), price_multiplier=1.5),  # Giờ cao điểm, tăng giá 50%
            TimeSlots(name='Ca Giờ Vàng 2 (18h30 - 20h00)', start_time=datetime.time(18, 30),
                      end_time=datetime.time(20, 0), price_multiplier=1.5),
            TimeSlots(name='Ca Tối Muộn (20h00 - 21h30)', start_time=datetime.time(20, 0),
                      end_time=datetime.time(21, 30), price_multiplier=1.2),

            #test "KHUNG GIỜ ĐẶT TỐI THIỂU 1 GIỜ"
            TimeSlots(name='Ca Chớp Nhoáng (12h00 - 12h30)', start_time=datetime.time(12, 0),
                      end_time=datetime.time(12, 30), price_multiplier=1.0)
        ]
        db.session.add_all(slots)

        services = [
            Service(name='Nước khoáng Lavie', price=10000, unit='Chai'),
            Service(name='Bò húc (Redbull)', price=15000, unit='Lon'),
            Service(name='Thuê bóng thi đấu', price=50000, unit='Quả'),
            Service(name='Thuê trọng tài', price=150000, unit='Trận'),
            Service(name='Thuê áo Pitch (bộ)', price=30000, unit='Bộ 10 áo')
        ]
        db.session.add_all(services)

        db.session.commit()


if __name__ == '__main__':
    create_dummy_data()