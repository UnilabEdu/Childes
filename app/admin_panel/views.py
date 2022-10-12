import imghdr
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin.contrib.fileadmin import FileAdmin
from flask import redirect, url_for, request, Blueprint, Markup
from flask_login import login_required, login_user, logout_user, current_user
from flask_admin.form.upload import FileUploadField
from wtforms.validators import ValidationError
from app.main.models import User



class UserView(ModelView):
    
    # def is_accessible(self):
    #     if current_user.is_authenticated:
    #         print(current_user)
    #         return current_user.is_admin()
    #     return False
    
    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for('login'))
    
    can_delete = False
    can_edit = True
    edit_modal = True
    column_display_all_relations = True

class AboutPageView(ModelView):
    
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin()
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))
    
    can_delete = False
    can_create = True 
    can_edit = True
    edit_modal = True
    column_display_all_relations = True

class File_View(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin()
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))
    
    can_edit = True
 



class LogoutView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin()
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

    def _handle_view(self, name, **kwargs):
        return redirect(url_for('logout'))
    
    

class LoginView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return True
        return False
    
    def _handle_view(self, name, **kwargs):
        return redirect(url_for('user_blueprint.login'))
    
    
class FilesView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin()
        return False
    
    def _handle_view(self, name, **kwargs):
        return redirect(url_for('admin_upload_bp.upload_file'))