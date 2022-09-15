
from flask import Flask
from app.extensions import db, migrate, login_manager, csrf, admin
from app.admin_panel.views import UserView
from app.main.models import User
from flask_admin.contrib.fileadmin import FileAdmin
from app.main.views import users_blueprint
import os
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
uploads_folder_in_static_folder = os.path.join(static_folder, 'uploads')
print(static_folder)
# Create Flask application
def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    register_extensions(app)
    register_blueprints(app)
    register_admin(app) 
    return app

# Register extensions
def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'


# Register blueprints
def register_blueprints(application):
    pass
    # example of registering a blueprint
    # application.register_blueprint(users_blueprint, url_prefix='/users') 
    
def register_admin(app):
    admin.add_view(UserView(User, db.session, name='მომხმარებელი', endpoint='user', category='მომხმარებლები'))
    admin.add_view(FileAdmin(uploads_folder_in_static_folder, '/uploads', name='სტატიკური ფაილები'))
    admin.init_app(app)
