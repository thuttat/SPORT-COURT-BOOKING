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




def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                "status": "error",
                "message": "Authentication required. Please log in"
            }), 401

        if current_user.user_role != UserRole.ADMIN:
            return jsonify({
                "status": "error",
                "message": "Access Denied. Admin privileges required."
            }), 403
            
        return f(*args, **kwargs)
    return decorated_function




def user_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                "status": "error",
                "message": "Authentication required. Please log in"
            }), 401

        if current_user.user_role != UserRole.USER:
            return jsonify({
                "status": "error",
                "message": "You cannot access this page with admin role"
            }), 403
            
        return f(*args, **kwargs)
    return decorated_function