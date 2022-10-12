
from app.extensions import db
from flask_login import UserMixin, AnonymousUserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
import os

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    roles = db.relationship('Role', secondary='user_roles')
    
    
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
    
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
        return self.password == password
    
    def get_reset_token(self, expires=500):
        return jwt.encode({'reset_password': f'{self.email}',
                           'exp':    time() + expires},
                           key=os.getenv('SECRET_KEY_FLASK'))
    
    def verify_reset_token(token):
        try:
            email = jwt.decode(token,
              key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
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


class File(db.Model):
    __tablename__ = 'files'
    
    
    
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), unique=True, nullable=False)
    yt_link = db.Column(db.String(80), unique=True, nullable=False)

    
    
    def create(self,commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        if commit:
            db.session.add(self)
            db.session.commit()
    
    
    def strip(self, child_name):
        return self.file_name.strip(child_name).strip('.cha')
    
    # create method already_exists with file_name
    @classmethod
    def already_exists(cls, file_name):
        return cls.query.filter_by(file_name=file_name).first() is not None 

    @classmethod
    def already_exists_yt(cls, yt_link):
        return cls.query.filter_by(yt_link=yt_link).first() is not None
    
    @staticmethod
    def get_by_name(name):
        return File.query.filter_by(file_name=name).first()
    
    @classmethod
    def update(cls, id, **kwargs):
        file = cls.get_by_id(id)
        for key, value in kwargs.items():
            setattr(file, key, value)
        db.session.commit()
        return file

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def __repr__(self):
        return self.file_name
    
    
class AboutPage(db.Model):
    __tablename__ = 'about_page'
    
    id = db.Column(db.Integer, primary_key=True)
    goals = db.Column(db.Text, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    who_worked = db.Column(db.Text, nullable=False)
    
    def create(self,commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        if commit:
            db.session.add(self)
            db.session.commit()
            
    @staticmethod
    def get_by_id(id):
        return AboutPage.query.get(id)
    
    @classmethod
    def update(cls, id, **kwargs):
        about_page = cls.get_by_id(id)
        for key, value in kwargs.items():
            setattr(about_page, key, value)
        db.session.commit()
        return about_page

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    def __repr__(self):
        return self.title