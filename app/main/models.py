from app.extensions import db
from flask_login import UserMixin, AnonymousUserMixin, current_user


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='user_roles')
    
    
    @staticmethod
    def create(**kwargs):
        user = User(**kwargs)
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


