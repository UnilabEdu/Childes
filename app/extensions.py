
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

mail = Mail()  
login_manager = LoginManager()
csrf = CSRFProtect()
admin = Admin(name='Admin', template_mode='bootstrap4')

db = SQLAlchemy()
migrate = Migrate()