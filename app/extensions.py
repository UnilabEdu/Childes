from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from app.views.admin_panel.views import DashboardView

mail = Mail()  
login_manager = LoginManager()
csrf = CSRFProtect()
admin = Admin(name='Admin', template_mode='bootstrap4', index_view=DashboardView())

db = SQLAlchemy()
migrate = Migrate()