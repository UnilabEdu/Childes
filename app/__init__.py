from flask import Flask, flash, url_for, redirect
from app.extensions import db, migrate, login_manager, csrf, admin, mail
from app.views.admin_panel.views import File_View, UserView, LogoutView, LoginView, FilesView, AboutPageView, MainPageView, DashboardView
from app.views.main.models import File, AboutPage
from app.views.auth.models import Role, User
from app.views.main.views import main_blueprint
from app.views.admin_panel.uploads_view import admin_upload_bp
from app.views.auth.views import user_blueprint
from app.config import Config, DevConfig, ProdConfig
from app.config import STATIC_FODLER as static_folder, BASEDIR
from app.commands import init_db, populate_db

BLUEPRINTS = [main_blueprint, user_blueprint, admin_upload_bp]
COMMANDS = [init_db, populate_db]

# Create Flask application
def create_app():
    app = Flask(__name__)
    set_environment(app)
    register_extensions(app)
    register_blueprints(app)
    register_admin(app)
    register_errorhandlers(app)
    register_commands(app)
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
        application.register_blueprint(bp)


def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)


def register_errorhandlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        flash('ეს გვერდი არარსებობს!')
        return redirect(url_for('main_blueprint.index'))

    @app.errorhandler(500)
    def internal_server_error(e):
        flash('სერვერის შეცდომა!')
        return redirect(url_for('main_blueprint.index'))


def register_admin(app):
    admin.add_view(UserView(User, db.session, name='მომხმარებლები', endpoint='users',))
    # add log out view to admin panel
    # files upload
    admin.add_view(FilesView(User, db.session, name='ფაილების ატვირთვა', endpoint='files'))
    admin.add_view(File_View(File, db.session, name='ფაილების მოდელები'))

    # about page view
    admin.add_view(AboutPageView(AboutPage, db.session, name='ჩვენ შესახებ', endpoint='about'))
    admin.add_view(LoginView(Role, db.session, name='შესვლა'))
    # go to index page 
    admin.add_view(MainPageView(User, db.session, name='მთავარი გვერდი'))
    #admin.add_view(LogoutView(User, db.session, name='გასვლა'))
    admin.init_app(app)


def set_environment(app):
    env = 'dev'
    if env == 'prod':
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)
