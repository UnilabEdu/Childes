from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, Blueprint, Markup
from app.admin_panel.forms import UploadForm
from werkzeug.utils import secure_filename
from app.main.models import File
from flask_login import current_user
from app.main.views import user_blueprint, uploads_folder
import os
from app.config import basedir, STATI_FOLDER, main_statics_folder as statics_folder, ADMIN_PANEL_FOLDER
from functools import wraps




admin_upload_bp = Blueprint('admin_upload_bp', __name__, template_folder='templates', static_folder=STATI_FOLDER, url_prefix='/admin-uploads')


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            print('authenticated')
            if current_user.is_admin():
                return f(*args, **kwargs)
        print('not admin')
        return redirect(url_for('user_blueprint.login'))
    return decorated_function



@admin_upload_bp.route('/', methods=['GET', 'POST'])
@is_admin
def upload_file():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                f = form.file.data
                yt_link = form.yt_link.data
                print(f)
                # if file already exists in database redirect file upload page
                check_file = File.already_exists(f.filename) or File.already_exists_yt(yt_link)
                print(File.already_exists(f.filename), File.already_exists_yt(yt_link))
                if not check_file:
                    if 'MAT' in f.filename:
                        # create folder for MAT if does not exists in uploads_folder /cha/MAT files
                        # then save file in MAT folder
                        mat_folder = os.path.join(uploads_folder, 'cha', 'MAT')
                        print(os.path.exists(mat_folder),mat_folder)
                        if not os.path.exists(mat_folder):
                            os.makedirs(mat_folder)
                        filename = secure_filename(f.filename)
                        f.save(os.path.join(mat_folder, filename))
                        file_model = File(file_name=filename, yt_link=form.yt_link.data)
                        file_model.create()
                    if 'ALE' in f.filename:
                        ale_folder = os.path.join(uploads_folder, 'cha', 'ALE')
                        if not os.path.exists(ale_folder):
                            os.makedirs(ale_folder)
                        filename = secure_filename(f.filename)
                        f.save(os.path.join(ale_folder, filename))
                        file_model = File(file_name=filename, yt_link=form.yt_link.data)
                        file_model.create()
                    if 'GAB' in f.filename:
                        gab_folder = os.path.join(uploads_folder, 'cha', 'GAB')
                        if not os.path.exists(gab_folder):
                            os.makedirs(gab_folder)
                        filename = secure_filename(f.filename)
                        f.save(os.path.join(gab_folder, filename))
                        file_model = File(file_name=filename, yt_link=form.yt_link.data)
                        file_model.create()
                    if 'ANA' in f.filename:
                        ana_folder = os.path.join(uploads_folder, 'cha', 'ANA')
                        if not os.path.exists(ana_folder):
                            os.makedirs(ana_folder)
                        filename = secure_filename(f.filename)
                        f.save(os.path.join(ana_folder, filename))
                        file_model = File(file_name=filename, yt_link=form.yt_link.data)
                        file_model.create()
                    
                    flash('ფაილი აიტვირთა წარმატებით!', 'success')
                    return redirect(url_for('admin_upload_bp.upload_file'))
                else:
                    flash('ეს ფაილი ან იუთიბის მისამართი უკვე არსებობს')
                    return redirect(url_for('admin_upload_bp.upload_file'))
            except Exception as e:
                flash('File not saved', 'danger')
                print(e)
                return redirect(url_for('admin_upload_bp.upload_file'))
        return render_template('file_upload.html', form=form)
    return render_template('file_upload.html', form=form)