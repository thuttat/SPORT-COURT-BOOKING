import hashlib

from bapp import db
from bapp.models import User, Field, TimeSlots, Booking, BookingStatus


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

def add_user(username, password,fullname,email,avatar,user_role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    existing_user=User.query.filter(User.username.__eq__(username.strip())).first()
    existing_email = User.query.filter(User.email.__eq__(email.strip())).first()
    if existing_user:
        raise Exception('Username already exists!')
    if existing_email:
        raise Exception('Email already exists!')
    u = User(username=username,
             password=password,
             fullname=fullname,
             email=email,
             avatar=avatar,
             user_role=user_role)
    db.session.add(u)
    db.session.commit()


def get_field_and_slot(field_id,time_slots_id):
    field=Field.query.get(field_id)
    time_slot=TimeSlots.query.get(time_slots_id)
    return field, time_slot

def is_field_available(field_id, booking_date,time_slots_id):
    existing_booking=Booking.query.filter(
        Booking.field_id==field_id,
        Booking.booking_date==booking_date,
        Booking.time_slots_id==time_slots_id,
        Booking.status!=BookingStatus.CANCELLED
    ).first()
    return existing_booking is None

def count_user_bookings_per_day(user_id, booking_date):
    return Booking.query.filter(
        Booking.user_id == user_id,
        Booking.booking_date == booking_date,
        Booking.status != BookingStatus.CANCELLED
    ).count()

def create_new_booking(user_id, field, time_slot, booking_date, duration):
    total_price = field.price_per_hour * duration * time_slot.price_multiplier
    new_booking = Booking(
        user_id=user_id,
        field_id=field.id,
        time_slots_id=time_slot.id,
        booking_date=booking_date,
        duration=duration,
        total_price=total_price,
        status=BookingStatus.PENDING
    )
    db.session.add(new_booking)
    db.session.commit()
    return new_booking