from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin.contrib.fileadmin import FileAdmin
from flask import redirect, url_for, request, Blueprint
from flask_login import login_required, login_user, logout_user, current_user


class UserView(ModelView):
    
    def is_accessible(self):
        if current_user.is_authenticated:
            print(current_user)
            return current_user.is_admin()
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))
    
    can_delete = False
    can_edit = False
    edit_modal = True
    column_display_all_relations = True

class FileAdmina(FileAdmin):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin()
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))
    

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
        return redirect(url_for('login'))