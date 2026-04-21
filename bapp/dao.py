import hashlib

from bapp import db, app
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

##################################################

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


##################################################

def get_booking_by_id(booking_id):
    return db.session.get(Booking, booking_id)


def get_bookings_paginated(user_id, page=1, page_size=6):
    offset = (int(page) - 1) * int(page_size)
    query = Booking.query.filter(Booking.user_id == user_id).order_by(Booking.created_at.desc())
    return query.offset(offset).limit(page_size).all()

def count_user_bookings(user_id):
    return Booking.query.filter(Booking.user_id == user_id).count()

def update_booking_status(booking_id, new_status):
    booking=Booking.query.get(booking_id)

    if booking:
        booking.status=new_status
        db.session.commit()
        return booking
    return None


##################################################

def count_my_fields(user_id):
    return Field.query.filter(
        Field.user_id == user_id,
        Field.is_active == True
    ).count()

def get_fields_by_user_paginated(user_id, page=1, page_size=6):
    p = int(page) if page else 1
    ps = int(page_size) if page_size else 6
    offset = (p - 1) * ps
    return Field.query.filter(Field.user_id == user_id,
                              Field.is_active == True).offset(offset).limit(ps).all()


def add_field(name, field_type, price_per_hour, description, image, user_id):
    new_field = Field(
        name=name.strip(),
        field_type=field_type,
        price_per_hour=price_per_hour,
        description=description.strip() if description else "",
        image=image,
        user_id=user_id,
        is_active=True
    )
    try:
        db.session.add(new_field)
        db.session.commit()
        return new_field
    except Exception as e:
        db.session.rollback()
        print(f"Lỗi khi thêm sân: {str(e)}")
        return None


def update_field(field_id, name=None, field_type=None, price_per_hour=None, description=None, image=None,is_active=None):
    field = Field.query.get(field_id)
    if field:
        if name is not None:
            field.name = name
        if field_type is not None:
            field.field_type = field_type
        if price_per_hour is not None:
            field.price_per_hour = price_per_hour
        if description is not None:
            field.description = description
        if image is not None:
            field.image = image
        if is_active is not None:
            field.is_active = is_active

        db.session.commit()
        return field
    return None

def delete_field(field_id):
    field = Field.query.get(field_id)
    if field:
        field.is_active= False
        db.session.commit()
        return True
    return False

###########################################
