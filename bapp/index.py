from datetime import datetime, timedelta,  timezone
import cloudinary
import cloudinary.uploader
import re
import datetime as dt_module
from datetime import datetime as dt_class

from flask import request, jsonify, render_template, redirect
from flask_login import login_user, login_required, logout_user, current_user

from bapp import app, dao, login_manager, db, utils
from bapp.decorators import admin_only
from bapp.models import UserRole, BookingStatus, Field, FieldType, Booking
from bapp.utils import allowed_file

@app.route('/')
def index():
    courts = [
        {"id": "c1", "name": "Sân bóng đá Mini A", "sport": "football", "location": "Quận 1", "price": 200000, "rating": 4.5, "available": True},
        {"id": "c2", "name": "Sân cầu lông VIP 1", "sport": "badminton", "location": "Quận 3", "price": 80000, "rating": 4.8, "available": True},
        {"id": "c3", "name": "Sân cầu lông TTTM", "sport": "badminton", "location": "Quận 8", "price": 45000, "rating": 4.9, "available": False},
        {"id": "c4", "name": "Sân tennis trung tâm", "sport": "tennis", "location": "Quận 7", "price": 300000, "rating": 4.6, "available": True},
        {"id": "c5", "name": "Sân tennis Hồ Tùng Mậu", "sport": "tennis", "location": "Quận 1", "price": 500000, "rating": 4.7, "available": True}
    ]
    return render_template("customer/home.html", courts=courts, current_date=dt_module.date.today().strftime("%Y-%m-%d"))

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/register')
def register_view():
    return render_template("register.html")

@app.route('/bookings')
def bookings_view():
    return render_template("customer/bookings.html")

@app.route('/profile')
def profile_view():
    return render_template("customer/profile.html")


@app.route('/api/login', methods=['POST'])
def login_my_user():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return jsonify({"status": "error", "message": "Please fill out all required fields"}), 400

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user)
        return jsonify({
            "status": "success",
            "message": "Log in successfully!",
            "data": {"id": user.id, "fullname": user.fullname, "username": user.username, "avatar": user.avatar, "role": user.user_role.name}
        }), 200
    return jsonify({"status": "error", "message": "Invalid username or password!"}), 400

@app.route('/api/logout', methods=['POST'])
def logout_my_user():
    logout_user()
    return jsonify({"status": "success", "message": "Signed out successfully!"}), 200

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')

@app.route('/api/register', methods=['POST'])
def register_user():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    avatar = request.files.get('avatar')

    if not all([fullname, email, username, password, confirm, avatar]):
        return jsonify({"status": "error", "message": "Please fill out all required fields!"}), 400

    password_pattern = r"^(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
    if not re.match(password_pattern, password):
        return jsonify({"status": "error", "message": "Invalid password format!"}), 400

    if password != confirm:
        return jsonify({"status": "error", "message": "Passwords do not match!"}), 400

    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_pattern, email):
        return jsonify({"status": "error", "message": "Invalid email format!"}), 400

    if avatar and not allowed_file(avatar.filename):
        return jsonify({"status": "error", "message": "Invalid file type! Only images (PNG, JPG, JPEG) are allowed!"}), 400

    try:
        res = cloudinary.uploader.upload(avatar)
        avatar_path = res['secure_url']
        # role = request.form.get('user_role', 'USER').upper()
        # role_enum = UserRole.ADMIN if role == 'ADMIN' else UserRole.USER

        dao.add_user(
            fullname=fullname,
            username=username,
            password=password,
            email=email,
            avatar=avatar_path,
            user_role=UserRole.USER
        )
        return jsonify({
            "status": "success",
            "message": "Registered successfully!",
            "data": {
                "username": username,
                "email": email
            }
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

#####################################################################

@app.route('/api/my-bookings', methods=['GET'])
@login_required
def get_my_bookings():
    page = request.args.get('page', 1, type=int)
    page_size = app.config.get('PAGE_SIZE')

    pagination = dao.get_bookings_paginated(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )

    results = []
    for b in pagination.items:  
        results.append({
            "id": b.id,
            "field_name": b.field.name,
            "field_type": b.field.field_type.name,
            "booking_date": b.booking_date.strftime("%Y-%m-%d"),
            "time_slot": b.time_slot.name,
            "total_price": float(b.total_price),
            "status": b.status.name,
            "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({
        "status": "success",
        "data": results,
        "pagination": {
            "total_items": pagination.total,   
            "total_pages": pagination.pages,   
            "current_page": page,
            "page_size": page_size,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }), 200



@app.route('/api/my-bookings/<int:id>', methods=['GET'])
@login_required
def get_my_booking_details(id):
    booking = dao.get_booking_by_id(id)
    if not booking:
        return jsonify({"status": "error", "message": "Booking not found!"}), 404

    is_owner = booking.user_id == current_user.id
    is_field_admin = current_user.user_role == UserRole.ADMIN and booking.field.user_id == current_user.id

    if not (is_owner or is_field_admin):
        return jsonify({
            "status": "error",
            "message": "You are not authorized to view this booking detail"
        }), 403

    return jsonify({
        "status": "success",
        "data": {
            "id": booking.id,
            "field_name": booking.field.name,
            "field_type": booking.field.field_type.name,
            "booking_date": booking.booking_date.strftime("%Y-%m-%d"),
            "time_slot": booking.time_slot.name,
            "total_price": float(booking.total_price),
            "status": booking.status.name,
            "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    }), 200


@app.route('/api/bookings', methods=['POST'])
@login_required
def create_booking():
    try:
        user_id = current_user.id
        field_id = request.form.get('field_id')
        time_slots_id = request.form.get('time_slots_id')
        booking_date_str = request.form.get('booking_date')

        if not all([field_id, time_slots_id, booking_date_str]):
            return jsonify({"status": "error", "message": "Missing required fields!"}), 400

        booking_date = utils.parse_date(booking_date_str)
        if not booking_date:
            return jsonify({"status": "error", "message": "Invalid date format (YYYY-MM-DD)!"}), 400

        field, time_slot = dao.get_field_and_slot(field_id, time_slots_id)
        if not field or not time_slot:
            return jsonify({"status": "error", "message": "Field or time slot not found!"}), 404

        booking_datetime = dt_class.combine(booking_date, time_slot.start_time)
        now_in_vi = dt_class.utcnow() + timedelta(hours=7)
        if booking_datetime < now_in_vi:
            return jsonify({"status": "error", "message": "Cannot book a court in the past"}), 400

        duration = utils.calculate_duration(time_slot.start_time, time_slot.end_time)
        if duration < 1.0:
            return jsonify({"status": "error", "message": "Minimum booking duration is 1 hour"}), 400

        daily_bookings = dao.count_user_bookings_per_day(user_id, booking_date)
        if daily_bookings >= 3:
            return jsonify({"status": "error", "message": "You can only book a maximum of 3 courts per day"}), 400

        if not dao.is_field_available(field_id, booking_date, time_slots_id):
            return jsonify({"status": "error", "message": "This court is already booked"}), 409

        new_booking = dao.create_new_booking(user_id, field, time_slot, booking_date, duration)
        return jsonify({
            "status": "success",
            "message": "Booking successful!",
            "data": {
                "booking_id": new_booking.id,
                "field_name": field.name,
                "time_slot": time_slot.name,
                "total_price": new_booking.total_price
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
@login_required
def cancel_booking(booking_id):
    booking_order = dao.get_booking_by_id(booking_id)
    if not booking_order:
        return jsonify({"status": "error", "message": "Booking not found!"}), 404

    if booking_order.user_id != current_user.id:
        return jsonify({"status": "error", "message": "You are not authorized to cancel this booking"}), 403

    if booking_order.status == BookingStatus.CANCELLED:
        return jsonify({"status": "error", "message": "This booking is already cancelled."}), 400

    start_datetime = datetime.combine(booking_order.booking_date, booking_order.time_slot.start_time)
    now_in_vn = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=7)
    time_diff = start_datetime - now_in_vn
    minutes_diff = time_diff.total_seconds() / 60
    if minutes_diff < 0:
        return jsonify({
            "status": "error",
            "message": "Cannot cancel a court that is currently in use"}), 400
    if minutes_diff <= 120:
        return jsonify({
            "status": "error",
            "message": "Cannot cancel a booking less than 2 hours before start time"}), 400

    dao.update_booking_status(booking_id, BookingStatus.CANCELLED)
    return jsonify({
        "status": "success",
        "message": "Booking canceled successfully"
    }), 200

########################################################################
@app.route('/api/fields', methods=['GET'])
def get_all_active_fields_for_customer():
    page = request.args.get('page', 1, type=int)
    page_size = app.config.get('PAGE_SIZE', 10)
    date_str = request.args.get('date')  

    pagination = dao.get_active_fields_paginated(page=page, page_size=page_size)

    fully_booked_ids = []
    if date_str:
        booking_date = utils.parse_date(date_str)
        if not booking_date:
            return jsonify({"status": "error", "message": "Invalid date format (YYYY-MM-DD)!"}), 400
        fully_booked_ids = dao.get_fully_booked_field_ids(booking_date)

    results = []
    for f in pagination.items:  
        results.append({
            "id": f.id,
            "name": f.name,
            "field_type": f.field_type.name,
            "price_per_hour": float(f.price_per_hour),
            "description": f.description,
            "image": f.image,
            "is_available": (f.id not in fully_booked_ids) if date_str else None
        })

    return jsonify({
        "status": "success",
        "data": results,
        "pagination": {
            "total_items": pagination.total,
            "total_pages": pagination.pages,
            "current_page": page,
            "has_next": pagination.has_next
        }
    }), 200

@app.route('/api/my-fields', methods=['GET'])
@login_required
def get_my_fields():
    if current_user.user_role != UserRole.ADMIN:
        return jsonify({
            "status": "error", 
            "message": "Access Denied. Admin privileges required."
        }), 403

    page = request.args.get('page', 1, type=int)
    page_size = app.config.get('PAGE_SIZE', 6)

    pagination = dao.get_fields_by_user_paginated(current_user.id, page=page, page_size=page_size)

    results = []
    for f in pagination.items:  
        results.append({
            "id": f.id,
            "name": f.name,
            "field_type": f.field_type.name,
            "price_per_hour": float(f.price_per_hour),
            "description": f.description,
            "image": f.image,
            "is_active": f.is_active
        })

    return jsonify({
        "status": "success",
        "data": results,
        "pagination": {
            "total_items": pagination.total,  
            "total_pages": pagination.pages,
            "current_page": page,
            "has_next": pagination.has_next
        }
    }), 200



@app.route('/api/fields/<int:field_id>/slots', methods=['GET'])
def get_slots_by_date(field_id):
    date_str = request.args.get('date') 
    if not date_str:
        return jsonify({"status": "error", "message": "Date is required"}), 400
        
    booking_date = utils.parse_date(date_str)
    all_slots = dao.get_all_time_slots()
    
    results = []
    for s in all_slots:
        available = dao.is_field_available(field_id, booking_date, s.id)
        duration = utils.calculate_duration(s.start_time, s.end_time)
        results.append({
            "id": s.id,
            "display": f"{s.start_time.strftime('%H:%M')} - {s.end_time.strftime('%H:%M')}",
            "is_available": available,
            "price_multiplier": s.price_multiplier,
            "duration": duration
        })
    return jsonify({
        "status": "success", 
        "data": results
    }), 200



@app.route('/api/fields', methods=['POST'])
@login_required
@admin_only
def add_new_field():
    name = request.form.get('name')
    price = request.form.get('price_per_hour')
    ftype_str = request.form.get('field_type')
    description = request.form.get('description')

    if Field.query.filter_by(name=name).first():
        return jsonify({"status": "error", "message": "Court name already exists"}), 400

    image_url = "https://res.cloudinary.com/dyupzyqwj/image/upload/v1774885674/siqqkjjrpotnvfjtoij7.jpg"
    file = request.files.get('image')
    if file:
        res = cloudinary.uploader.upload(file)
        image_url = res['secure_url']
    try:
        field_type_enum = FieldType[ftype_str.upper()]
        new_f = dao.add_field(
            name=name,
            field_type=field_type_enum,
            price_per_hour=float(price),
            description=description,
            image=image_url,
            user_id=current_user.id
        )
        return jsonify({
            "status": "success",
            "message": "System saves the new court successfully",
            "data": {
                "id": new_f.id,
                "name": new_f.name,
                "field_type": new_f.field_type.name,
                "price_per_hour": new_f.price_per_hour,
                "description": new_f.description,
                "image": new_f.image,
                "created_at": new_f.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/fields/<int:field_id>', methods=['PATCH'])
@login_required
@admin_only
def update_field(field_id):
    field = db.session.get(Field, field_id)
    if not field:
        return jsonify({"message": "Field not found"}), 404

    if field.user_id != current_user.id:
        return jsonify({"status": "error", "message": "Access Denied"}), 403

    data_to_update = {}
    new_name = request.form.get('name')

    if new_name:
        if Field.query.filter(Field.name == new_name, Field.id != field_id).first():
            return jsonify({"message": "Court name already exists"}), 400
        data_to_update['name'] = new_name

    file = request.files.get('image')
    if file:
        res = cloudinary.uploader.upload(file)
        data_to_update['image'] = res['secure_url']

    price = request.form.get('price_per_hour')
    if price:
        data_to_update['price_per_hour'] = float(price)

    description = request.form.get('description')
    if description:
        data_to_update['description'] = description.strip()

    field_type = request.form.get('field_type')
    if field_type:
        try:
            data_to_update['field_type'] = FieldType[field_type.upper()]
        except KeyError:
            return jsonify({"message": "Invalid field type"}), 400

    if data_to_update:
        updated_field = dao.update_field(field_id, **data_to_update)

        if updated_field:
            return jsonify({
                "status": "success",
                "message": "Court updated successfully",
                "data": {
                    "id": updated_field.id,
                    "name": updated_field.name,
                    "field_type": updated_field.field_type.name,
                    "price_per_hour": float(updated_field.price_per_hour),
                    "description": updated_field.description,
                    "image": updated_field.image,
                    "is_active": updated_field.is_active
                }
            }), 200
    else:
        return jsonify({"status": "error", "message": "No data provided to update"}), 400

    return jsonify({"status": "error", "message": "Something went wrong during update"}), 500


@app.route('/api/fields/<int:field_id>', methods=['DELETE'])
@login_required
@admin_only
def delete_field(field_id):
    field = db.session.get(Field, field_id)
    if not field:
        return jsonify({"message": "Field not found"}), 404

    if field.user_id != current_user.id:
        return jsonify({"message": "Access Denied"}), 403

    now = datetime.now()
    upcoming_booking = Booking.query.filter(
        Booking.field_id == field_id,
        Booking.status == BookingStatus.PENDING
    ).all()

    for b in upcoming_booking:
        start_datetime = datetime.combine(b.booking_date, b.time_slot.start_time)
        if start_datetime > now:
            return jsonify({
                "status": "error",
                "message": "Cannot delete this court because it has future bookings"
            }), 400
        
    dao.delete_field(field_id)

    return jsonify({
        "status": "success",
        "message": "Field deleted (inactivated) successfully"
    }), 200

################################################################

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)