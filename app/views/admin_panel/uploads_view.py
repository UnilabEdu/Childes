from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.views.admin_panel.forms import UploadForm
from werkzeug.utils import secure_filename
from app.views.main.models import File
from flask_login import current_user
from app.views.main.views import UPLOADS_FOLDER
import os
from app.config import STATIC_FODLER, ADMIN_PANEL_TEMPLATES
from app.utils import is_admin





admin_upload_bp = Blueprint('admin_upload_bp', __name__, template_folder=ADMIN_PANEL_TEMPLATES, static_folder=STATIC_FODLER, url_prefix='/admin-uploads')




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
                    ten_number = [i for i in range(0, 10)]
                    file_name = f.filename
                    for num in ten_number:
                        f.filename = f.filename.replace(str(num), '')
                    print(f.filename)
                    child_file_name = f.filename.replace('.cha', '')
                    
                    # create folder for MAT if does not exists in UPLOADS_FOLDER /cha/MAT files
                    # then save file in MAT folder
                    child_folder = os.path.join(UPLOADS_FOLDER, 'cha', f'{child_file_name}')
                    print(os.path.exists(child_folder),child_folder)
                    if not os.path.exists(child_folder):
                        os.makedirs(child_folder)
                    filename = secure_filename(file_name)
                    f.save(os.path.join(child_folder, filename))
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