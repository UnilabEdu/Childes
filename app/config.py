
# Flask application config that need to be set before creating the app
import os


SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
basedir = os.path.abspath(os.path.dirname(__file__))
STATI_FOLDER = os.path.join(basedir, 'static')
FLASK_ADMIN_SWATCH = 'cerulean'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "data.sqlite")}'

SQLALCHEMY_TRACK_MODIFICATIONS = False