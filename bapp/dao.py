from datetime import datetime, timedelta
import re

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import func

from bapp import db, app
from bapp.models import User, Field, TimeSlots, Booking, BookingStatus


def get_user_by_id(id):
    return db.session.get(User, id)


def auth_user(username, password):
    user = User.query.filter(User.username == username.strip()).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def validate_register_input(username, password, fullname, email):    
    username = username.strip()
    if len(username) < 5:
        raise ValueError('Username must be at least 5 characters long!')
    if len(username) > 50:
        raise ValueError('Username must not exceed 50 characters!')
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError('Username can only contain letters, numbers, and underscores!')

   
    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters long!')
    if not re.search(r'[0-9]', password):
        raise ValueError('Password must contain at least one number!')
    if not re.search(r'[a-z]', password):
        raise ValueError('Password must contain at least one lowercase letter!')
    if not re.search(r'[A-Z]', password):
        raise ValueError('Password must contain at least one uppercase letter!')
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        raise ValueError('Password must contain at least one special character!')

    
    fullname = fullname.strip() if fullname else ''
    if not fullname or len(fullname) < 2:
        raise ValueError('Full name must be at least 2 characters!')
    if len(fullname) > 255:
        raise ValueError('Full name is too long!')

   
    email = email.strip() if email else ''
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        raise ValueError('Invalid email format!')

def add_user(username, password,fullname,email,avatar,user_role):
    validate_register_input(username, password, fullname, email)
    password = generate_password_hash(password)
    existing_user=User.query.filter(User.username.__eq__(username.strip())).first()
    existing_email = User.query.filter(User.email.__eq__(email.strip())).first()
    if existing_user:
        raise ValueError('Username already exists!')
    if existing_email:
        raise ValueError('Email already exists!')
    u = User(username=username,
             password=password,
             fullname=fullname,
             email=email,
             avatar=avatar,
             user_role=user_role)
    try:
        db.session.add(u)
        db.session.commit()
        return u
    except Exception as e:
        db.session.rollback()
        raise

##################################################

def get_field_and_slot(field_id, time_slots_id):
    field = db.session.get(Field, field_id)
    time_slot = db.session.get(TimeSlots, time_slots_id)
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
    try:
        db.session.add(new_booking)
        db.session.commit()
        return new_booking
    except Exception as e:
        db.session.rollback()
        raise 

##################################################

def get_booking_by_id(booking_id):
    return db.session.get(Booking, booking_id)


def get_bookings_paginated(user_id, page=1, page_size=6):
    return Booking.query.filter(Booking.user_id == user_id).order_by(Booking.created_at.desc()).paginate(page=int(page), per_page=int(page_size), error_out=False)


def update_booking_status(booking_id, new_status):
    booking = db.session.get(Booking, booking_id)
    if booking:
        booking.status=new_status
        try:
            db.session.commit()
            return booking
        except Exception:
            db.session.rollback()
            raise
    return None

def count_cancellations_by_user(user_id):
    seven_days_ago = datetime.now() - timedelta(days=7)
    count = Booking.query.filter(
        Booking.user_id == user_id,
        Booking.status == BookingStatus.CANCELLED,
        Booking.created_at >= seven_days_ago
    ).count()
    return count


##################################################

def get_fields_by_user_paginated(user_id, page=1, page_size=6, include_inactive=False):
    query = Field.query.filter(Field.user_id == user_id)
    if not include_inactive:
        query = query.filter(Field.is_active == True)
    return query.paginate(page=int(page), per_page=int(page_size), error_out=False)

def get_active_fields_paginated(page=1, page_size=10):
    return Field.query.filter_by(is_active=True).paginate(page=page, per_page=page_size, error_out=False)

def get_field_by_id(field_id):
    return db.session.get(Field, field_id)

def get_fully_booked_field_ids(booking_date):
    total_slots = TimeSlots.query.count()
    query = db.session.query(Booking.field_id).filter(
        Booking.booking_date == booking_date,
        Booking.status != BookingStatus.CANCELLED
    ).group_by(Booking.field_id).having(func.count(Booking.id) >= total_slots).all()
    return [row.field_id for row in query]

def get_all_time_slots():
    return TimeSlots.query.order_by(TimeSlots.start_time).all()


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
        raise

def update_field(field_id, name=None, field_type=None, price_per_hour=None, description=None, image=None,is_active=None):
    field = db.session.get(Field, field_id)
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

        try:
            db.session.commit()
            return field
        except Exception:
            db.session.rollback()
            raise
    return None

def delete_field(field_id):
    field = db.session.get(Field, field_id)
    if field:
        field.is_active= False
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise
    return False

###########################################
