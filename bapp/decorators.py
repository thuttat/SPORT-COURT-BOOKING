from functools import wraps
from flask import request, redirect, url_for, jsonify
from flask_login import current_user

from bapp.models import UserRole


def loggedin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return jsonify({
                "status": "error",
                "message": "You are already logged in, you cannot perform this action!"
            }), 403

        return f(*args, **kwargs)

    return decorated_function


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({
                    "status": "error",
                    "message": "Authentication required. Please log in"
                }), 401

            if current_user.user_role not in roles:
                return jsonify({
                    "status": "error",
                    "message": "Forbidden. You do not have permission to access this resource!"
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_only(f):
    return role_required(UserRole.ADMIN)(f)

def login_required_custom(f):
    return role_required(UserRole.ADMIN, UserRole.USER)(f)


def user_only(f):
    return role_required(UserRole.USER)(f)