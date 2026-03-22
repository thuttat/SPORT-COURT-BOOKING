from enum import Enum as RoleEnum
from datetime import datetime

from flask_login import UserMixin

import bapp
from bapp import db
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Integer


class UserRole(RoleEnum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

class User(BaseModel,UserMixin):
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    fullname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False,unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    avatar=Column(String(255), nullable=True)

    def __str__(self):
        return self.username


if __name__ == '__main__':
    with bapp.app_context():
        db.create_all()
        db.session.commit()