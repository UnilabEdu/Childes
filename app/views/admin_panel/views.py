from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from wtforms import PasswordField
from flask import redirect, url_for
from flask_login import current_user


class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user_blueprint.login'))


class DashboardView(AdminIndexView):
    def is_visible(self):
        return False


class UserView(SecureModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def on_model_change(self, form, model, is_created):
        if form.new_password.data != "":
            model.password = form.new_password.data

    column_list = ["first_name", "last_name", "email", "roles"]
    form_extra_fields = {'new_password': PasswordField('Password')}
    form_columns = ("roles", "first_name", "last_name", "email", "new_password")

    can_delete = False
    can_edit = True
    edit_modal = True
    column_display_all_relations = True


class AboutPageView(SecureModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    can_delete = False
    can_create = True 
    can_edit = True
    edit_modal = True
    column_display_all_relations = True


class File_View(SecureModelView):
    form_excluded_columns = ["file_name"]
    can_create = False

    edit_modal = True
    can_edit = True


class LogoutView(SecureModelView):
    def _handle_view(self, name, **kwargs):
        return redirect(url_for('user_blueprint.logout'))


class MainPageView(ModelView):
    def _handle_view(self, name, **kwargs):
        return redirect(url_for('main_blueprint.index'))
    

class LoginView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return True
        return False
    
    def _handle_view(self, name, **kwargs):
        return redirect(url_for('user_blueprint.login'))
    
    
class FilesView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def _handle_view(self, name, **kwargs):
        return redirect(url_for('admin_upload_bp.upload_file'))