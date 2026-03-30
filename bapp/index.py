

import cloudinary
import cloudinary.uploader
import re
from flask import request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime as dt_class

from bapp import app, dao, login_manager, db, utils
from bapp.models import UserRole


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
                "username": user.username
            }
        }), 200
    else:
        return jsonify({"status": "error", "message": "Invalid username or password!"}), 400


@app.route('/api/logout', methods=['POST'])
def logout_my_user():
    logout_user()
    return jsonify({"status": "success", "message": "Signed out successfully!"}), 200


@app.route('/api/register', methods=['POST'])
def register_user():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    avatar = request.files.get('avatar')

    if not fullname or not email or not username or not password or not confirm or not avatar:
        return jsonify({"status": "error", "message": "Please fill out all required fields!"}), 400

    if password != confirm:
        return jsonify({"status": "error", "message": "Passwords do not match!"}), 400

    if not re.match(email_pattern, email):
        return jsonify({"status": "error", "message": "Invalid email format!"}), 400

    try:
        res = cloudinary.uploader.upload(avatar)
        avatar_path = res['secure_url']
        role = request.form.get('user_role')
        if role and role.strip().upper() == 'ADMIN':
            role_enum = UserRole.ADMIN
        else:
            role_enum = UserRole.USER
        dao.add_user(
            fullname=fullname,
            username=username,
            password=password,
            email=email,
            avatar=avatar_path,
            user_role=role_enum
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


@app.route('/api/bookings', methods=['POST'])
def create_booking():
    try:
        if not current_user.is_authenticated:
            return jsonify({"status":"error", "message": "Please login to book a court"}), 401

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
        if booking_datetime < dt_class.now():
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
        from bapp import db
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)