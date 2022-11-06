# Flask application config that need to be set before creating the app
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

STATIC_FODLER = os.path.join(BASEDIR, 'static')
UPLOADS_FOLDER = os.path.join(BASEDIR, 'uploads')
main_statics_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'front')
TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
ADMIN_PANEL_TEMPLATES = os.path.join(TEMPLATE_FOLDER, 'admin_panel')


class Config:
    """Base Config."""
    ADMIN_PANEL_FOLDER = os.path.join(BASEDIR, 'admin_panel')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'

    # find css fold in app>main>front>css


class ProdConfig(Config):
    """Production Config."""
    FLASK_ADMIN_SWATCH = 'cerulean'
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'b751eb87d05854'
    MAIL_PASSWORD = '5f89c3ea1bb1ef'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASEDIR, "data.sqlite")}'


class DevConfig(Config):
    """Development Config."""
    FLASK_ADMIN_SWATCH = 'cerulean'
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'b751eb87d05854'
    MAIL_PASSWORD = '5f89c3ea1bb1ef'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASEDIR, "data.sqlite")}'
