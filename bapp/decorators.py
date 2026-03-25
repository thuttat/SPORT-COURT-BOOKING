from functools import wraps
from flask import request, redirect, url_for, jsonify
from flask_login import current_user


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