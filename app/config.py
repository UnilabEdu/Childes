
# Flask application config that need to be set before creating the app
import os

SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'


BASEDIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FODLER = os.path.join(BASEDIR, 'static')
UPLOADS_FOLDER = os.path.join(BASEDIR, 'uploads')
# find css fold in app>main>front>css 
main_statics_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'front')
MAIN_TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
MAIN_TEMPLATE = os.path.join(MAIN_TEMPLATE_FOLDER, 'main')
ADMIN_PANEL_TEMPLATES = os.path.join(MAIN_TEMPLATE_FOLDER, 'admin_panel')

print(main_statics_folder, MAIN_TEMPLATE_FOLDER)

ADMIN_PANEL_FOLDER = os.path.join(BASEDIR, 'admin_panel')


FLASK_ADMIN_SWATCH = 'cerulean'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASEDIR, "data.sqlite")}'

SQLALCHEMY_TRACK_MODIFICATIONS = False