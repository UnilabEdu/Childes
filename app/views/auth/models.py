from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt

from app.config import Config
from app.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column('password', db.String(120), unique=False, nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    # create create method
    @classmethod
    def create(cls, first_name, last_name, email, password):
        user = cls(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @classmethod
    def update(cls, id, **kwargs):
        user = cls.get_by_id(id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @classmethod
    def delete(cls):
        db.session.delete(cls)
        db.session.commit()
        return cls

    # create method has_role

    def is_admin(self):
        return 'admin' in [role.name for role in self.roles]

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_token(self, expires=30):
        return jwt.encode({'reset_password': self.email,
                           'exp': time() + expires},
                          key=Config.SECRET_KEY)

    @classmethod
    def verify_reset_token(cls,token):
        try:
            email = jwt.decode(token,
                               key=Config.SECRET_KEY,algorithms=['HS256'])['reset_password']
        except Exception as e:
            print(e)
            return
        return User.query.filter_by(email=email).first()


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', secondary='user_roles', overlaps='users, roles')

    @staticmethod
    def create_roles():
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()

    def __repr__(self):
        return self.name


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))