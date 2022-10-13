
# Flask application config that need to be set before creating the app
import os

SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'


basedir = os.path.abspath(os.path.dirname(__file__))
STATI_FOLDER = os.path.join(basedir, 'static')
uploads_folder = os.path.join(basedir, 'uploads')
# find css fold in app>main>front>css 
main_statics_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main', 'front')
main_template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main', 'html')

ADMIN_PANEL_FOLDER = os.path.join(basedir, 'admin_panel')


FLASK_ADMIN_SWATCH = 'cerulean'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "data.sqlite")}'

SQLALCHEMY_TRACK_MODIFICATIONS = False