
from flask import Flask
from app.extensions import db, migrate, login_manager, csrf, admin, mail
from app.admin_panel.views import File_View, UserView, LogoutView, LoginView, FilesView, AboutPageView
from app.main.models import Role, User, File, AboutPage
from flask_admin.contrib.fileadmin import FileAdmin
from app.main.views import index, login, logout, user_blueprint
from app.admin_panel.uploads_view import admin_upload_bp
from flask_admin.contrib import rediscli
from app.config import STATI_FOLDER as static_folder, basedir
import os
uploads_folder_in_static_folder = os.path.join(basedir)
print(static_folder)

BPS = [user_blueprint, admin_upload_bp]

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
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user_blueprint.login'

# register blueprint urls
def register_blueprint_urls():
    user_blueprint.add_url_rule('/childes/geo/', view_func=index, methods=['GET', 'POST'])
    user_blueprint.add_url_rule('/childes/login', view_func=login, methods=['GET', 'POST'])
    user_blueprint.add_url_rule('/childes/logout', view_func=logout, methods=['GET', 'POST'])


# Register blueprints
def register_blueprints(application):
    register_blueprint_urls()
    for bp in BPS:
        print(bp)
        application.register_blueprint(bp)
    
def register_admin(app):
    admin.add_view(UserView(User, db.session, name='მომხმარებელი', endpoint='users', category='მომხმარებლები'))
    # add log out view to admin panel
    # files upload
    admin.add_view(FilesView(User, db.session, name='ფაილების ატვირთვა', endpoint='files', category='ფაილები'))
    admin.add_view(File_View(File,db.session, name='ფაილები'))

    # about page view
    admin.add_view(AboutPageView(AboutPage, db.session, name='ჩვენს შესახებ', endpoint='about', category='გვერდები'))
    admin.add_view(LoginView(Role, db.session, name='შესვლა'))
    admin.add_view(LogoutView(User, db.session, name='გასვლა'))
    admin.init_app(app)
