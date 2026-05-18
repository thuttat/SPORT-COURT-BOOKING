import enum
from enum import Enum as RoleEnum
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import relationship

import bapp
from bapp import db
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Integer, Float, ForeignKey, Time, Date


class UserRole(RoleEnum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class FieldType(enum.Enum):
    FOOTBALL = 'FOOTBALL'
    TENNIS = 'TENNIS'
    BADMINTON = 'BADMINTON'

class BookingStatus(enum.Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    CONFIRMED = 'CONFIRMED'

class PaymentMethod(enum.Enum):
    VNPAY = 'VNPAY'
    CASH = 'CASH'


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class User(BaseModel,UserMixin):
    __tablename__ = 'user'
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    fullname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False,unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    avatar=Column(String(255), nullable=False)

    bookings = relationship('Booking', backref='user', lazy=True)

    def __str__(self):
        return self.username

class Field(BaseModel):
    __tablename__ = 'field'
    name = Column(String(255), nullable=False)
    field_type = Column(Enum(FieldType), nullable=False)
    price_per_hour=Column(Float,nullable=False)
    description = Column(String(255), nullable=False)
    image=Column(String(255), nullable=False)

    user_id=Column(Integer, ForeignKey('user.id'), nullable=False)
    bookings = relationship('Booking', backref='field', lazy=True)


class TimeSlots(BaseModel):
    __tablename__ = 'time_slots'
    name = Column(String(255), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    price_multiplier=Column(Float,nullable=False)

    bookings = relationship('Booking', backref='time_slot', lazy=True)

class Booking(BaseModel):
    __tablename__ = 'booking'
    booking_date = Column(Date, nullable=False)
    duration = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.PENDING)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    time_slots_id = Column(Integer, ForeignKey('time_slots.id'), nullable=False)

class Payment(BaseModel):
    __tablename__ = 'payment'
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    payment_time = Column(DateTime, default=datetime.now)

    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False, unique=True)

class Service(BaseModel):
    __tablename__ = 'service'
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    booking_details = relationship('BookingDetail', backref='service', lazy=True)


class BookingDetail(BaseModel):
    __tablename__ = 'booking_detail'
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)

    booking_id = Column(Integer, ForeignKey('booking.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    booking = relationship('Booking', backref='details')

if __name__ == '__main__':
    with bapp.app.app_context():
        # db.drop_all()
        db.create_all()
        db.session.commit()