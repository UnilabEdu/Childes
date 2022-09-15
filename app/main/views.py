
from flask import redirect, render_template, request, url_for, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from app.extensions import login_manager
from app.main.models import User
# Create blueprint

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')
                            
# register login manager with the application
@login_manager.user_loader
def load_user(user_id):
    # example 
    # This is User Model from your models file 
    # this function is called to load a user given an ID
    return User.query.get(user_id)

# Simple index page route
@users_blueprint.route('/')
@login_required
def index():
    return 'hello world'

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return 'login test'

# Logout route
@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

