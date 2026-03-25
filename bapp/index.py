import cloudinary
import cloudinary.uploader
import re
from flask import request, jsonify
from flask_login import login_user, login_required, logout_user

from bapp import app, dao, login_manager, db
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


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)