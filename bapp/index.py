from datetime import datetime, timedelta,  timezone, date
import cloudinary
import cloudinary.uploader
import re
import datetime as dt_module
from datetime import datetime as dt_class

from werkzeug.security import generate_password_hash

from flask import request, jsonify, render_template, redirect
from flask_login import login_user, login_required, logout_user, current_user

from bapp import app, dao, login_manager, db, utils
from bapp.decorators import admin_only, user_only
from bapp.models import User, UserRole, BookingStatus, Field, FieldType, Booking
from bapp.utils import allowed_file, validate_image

from bapp.admin import admin_bp
from bapp.payments import payment_bp

app.register_blueprint(admin_bp)
app.register_blueprint(payment_bp)

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
            "data": {
                "id": user.id,
                "fullname": user.fullname,
                "username": user.username,
                "avatar": user.avatar,
                "role": user.user_role.name
            }
        }), 200
    return jsonify({"status": "error", "message": "Invalid username or password!"}), 400



@app.route('/api/me', methods=['GET'])
@login_required
def get_current_user_info():
    return jsonify({
        "status": "success",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "fullname": current_user.fullname,
            "email": current_user.email,
            "avatar": current_user.avatar,
            "user_role": current_user.user_role.name
        }
    }), 200



@app.route('/api/profile', methods=['PATCH'])
@login_required
def update_profile():
    try:
        user = current_user
        new_fullname = request.form.get('fullname')
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        avatar_file = request.files.get('avatar')

        if new_fullname:
            user.fullname = new_fullname.strip()

        if new_email and new_email != user.email:
            import re
            email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if not re.match(email_pattern, new_email):
                return jsonify({"status": "error", "message": "Invalid email format!"}), 400
                
            existing_email = db.session.query(User).filter(User.email == new_email, User.id != user.id).first()
            if existing_email:
                return jsonify({
                    "status": "error", 
                    "message": "Email is already in use by another account"
                }), 400
            user.email = new_email.strip()

        if new_password:
            import re
            password_pattern = r"^(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"
            if not re.match(password_pattern, new_password):
                return jsonify({
                    "status": "error", 
                    "message": "Invalid password format! Minimum 8 chars and 1 special char required."
                }), 400
            user.password = generate_password_hash(new_password)

        if avatar_file:
            from bapp.utils import allowed_file
            if not allowed_file(avatar_file.filename):
                return jsonify({
                    "status": "error", 
                    "message": "Invalid file type! Only images are allowed!"
                }), 400
            res = cloudinary.uploader.upload(avatar_file)
            user.avatar = res['secure_url']

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Profile updated successfully!",
            "data": {
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname,
                "email": user.email,
                "avatar": user.avatar,
                "user_role": user.user_role.name
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500



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

    if avatar:
        is_valid, error_msg = validate_image(avatar)
        if not is_valid:
            return jsonify({"status": "error", "message": error_msg}), 400

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
@user_only
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
@user_only
def get_my_booking_details(id):
    booking = dao.get_booking_by_id(id)
    if not booking:
        return jsonify({"status": "error", "message": "Booking not found!"}), 404

    is_owner = booking.user_id == current_user.id

    if not (is_owner):
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
@user_only
def create_booking():
    try:
        user_id = current_user.id

        max_limit = app.config.get('MAX_CANCELLATIONS_PER_WEEK', 3) 
        cancellation_count = dao.count_cancellations_by_user(user_id)
        if cancellation_count >= max_limit:
            return jsonify({
                "status": "error",
                "message": "Your account is temporarily restricted from booking for 24 hours due to excessive cancellations."
            }), 403

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
@user_only
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
    
    #them cho tc
    max_limit = app.config.get('MAX_CANCELLATIONS_PER_WEEK', 3) 
    cancellation_count = dao.count_cancellations_by_user(current_user.id)
    if cancellation_count >= max_limit:
        return jsonify({
            "status": "error",
            "message": "Account restricted from booking for 24 hours due to excessive cancellations."
        }), 403


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


@app.route('/api/fields/<int:field_id>', methods=['GET'])
def get_field_detail(field_id):
    field = dao.get_field_by_id(field_id)
    if not field:
        return jsonify({"status": "error", "message": "Field not found!"}), 404

    if not field.is_active:
        return jsonify({"status": "error", "message": "This field is no longer available"}), 404

    return jsonify({
        "status": "success",
        "data": {
            "id": field.id,
            "name": field.name,
            "field_type": field.field_type.name,
            "price_per_hour": float(field.price_per_hour),
            "description": field.description,
            "image": field.image,
            "is_active": field.is_active
        }
    }), 200

################################################################

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)