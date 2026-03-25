import hashlib

from bapp import db
from bapp.models import User


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
