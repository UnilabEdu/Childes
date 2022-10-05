from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, Blueprint, Markup
from app.admin_panel.forms import UploadForm
from werkzeug.utils import secure_filename
from app.main.models import File
from flask_login import current_user
from app.main.views import user_blueprint
import os
from app.config import basedir, STATI_FOLDER
# static folder from app/static/


ADMIN_PANEL_FOLDER = os.path.join(basedir, 'admin_panel')


admin_upload_bp = Blueprint('admin_upload_bp', __name__, template_folder='templates', static_folder=STATI_FOLDER, url_prefix='/admin-uploads')


@admin_upload_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if current_user.is_authenticated:
        if current_user.is_admin():
            form = UploadForm()
            if request.method == 'POST':
                if form.validate_on_submit():
                    try:
                        f = form.file.data
                        # split name -> example.png result example 
                        file_name = f.filename.split('.')[0]
                        f.save(os.path.join(
                            STATI_FOLDER, 'uploads', secure_filename(f.filename)))
                        print(file_name,'app/static/uploads/'+f.filename,form.yt_link.data)
                        file_model = File(file_name=f.filename, yt_link=form.yt_link.data)
                        file_model.create()
                        flash('File Saved', 'success')
                        return redirect(url_for('admin_upload_bp.upload_file'))
                    except Exception as e:
                        flash('File not saved', 'danger')
                        print(e)
                        return redirect(url_for('admin_upload_bp.upload_file'))
                return render_template('file_upload.html', form=form)
            return render_template('file_upload.html', form=form)
        return redirect(url_for('index'))
    return redirect(url_for('index'))