import hashlib

from bapp import db
from bapp.models import User


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

def add_user(username, password,fullname,email,avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(username=username, password=password,fullname=fullname,email=email,avatar=avatar)
    db.session.add(u)
    db.session.commit()
