from flask import Flask
from app.extensions import db, migrate, login_manager, csrf, admin, mail
from app.views.admin_panel.views import File_View, UserView, LogoutView, LoginView, FilesView, AboutPageView
from app.views.main.models import Role, User, File, AboutPage
from app.views.main.views import user_blueprint
from app.views.admin_panel.uploads_view import admin_upload_bp
from app.config import Config, DevConfig, ProdConfig
from app.config import STATIC_FODLER as static_folder, BASEDIR
import os

UPLOADS_FOLDER_in_static_folder = os.path.join(BASEDIR)
print(static_folder)

BLUEPRINTS = [user_blueprint, admin_upload_bp]


# Create Flask application
def create_app():
    app = Flask(__name__)
    set_environment(app)
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


# Register blueprints
def register_blueprints(application):
    for bp in BLUEPRINTS:
        print(bp)
        application.register_blueprint(bp)


def register_admin(app):
    admin.add_view(UserView(User, db.session, name='მომხმარებელი', endpoint='users', category='მომხმარებლები'))
    # add log out view to admin panel
    # files upload
    admin.add_view(FilesView(User, db.session, name='ფაილების ატვირთვა', endpoint='files', category='ფაილები'))
    admin.add_view(File_View(File, db.session, name='ფაილები'))

    # about page view
    admin.add_view(AboutPageView(AboutPage, db.session, name='ჩვენს შესახებ', endpoint='about', category='გვერდები'))
    admin.add_view(LoginView(Role, db.session, name='შესვლა'))
    admin.add_view(LogoutView(User, db.session, name='გასვლა'))
    admin.init_app(app)


def set_environment(app):
    env = 'dev'
    if env == 'prod':
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)
