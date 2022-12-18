from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.views.admin_panel.forms import UploadForm
from werkzeug.utils import secure_filename
from app.views.main.models import File
from flask_login import current_user
from app.views.main.views import UPLOADS_FOLDER
import os
from app.config import STATIC_FODLER, ADMIN_PANEL_TEMPLATES
from app.utils import is_admin

admin_upload_bp = Blueprint('admin_upload_bp', __name__, template_folder=ADMIN_PANEL_TEMPLATES,
                            static_folder=STATIC_FODLER, url_prefix='/admin-uploads')


@admin_upload_bp.route('/', methods=['GET', 'POST'])
@is_admin
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        try:
            file = form.file.data
            yt_link = form.yt_link.data
            yt_link_id = None
            embed_yt_link = None

            if yt_link:
                yt_link_id = yt_link.split('=')[1].split('&')[0]
                embed_yt_link = "https://www.youtube.com/embed/" + str(yt_link_id)

            # If file already exists in database redirect file upload page
            file_exists = File.already_exists(file.filename)
            if file_exists:
                flash('ეს ფაილი უკვე არსებობს')
                return redirect(url_for('admin_upload_bp.upload_file'))
            
            filename = file.filename
            folder_name = ''.join([letter for letter in secure_filename(file.filename) if not letter.isnumeric()]).replace('.cha', '')
            child_folder = os.path.join(UPLOADS_FOLDER, 'cha', f'{folder_name}')

            print(os.path.exists(child_folder), child_folder)
            # Create folder if it does not exist
            if not os.path.exists(child_folder):
                os.makedirs(child_folder)

            filename = secure_filename(filename)
            file.save(os.path.join(child_folder, filename))
            file_model = File(file_name=filename, embed_yt_link=embed_yt_link, yt_link_id=yt_link_id)
            file_model.create()

            flash('ფაილი აიტვირთა წარმატებით!', 'success')
            return redirect(url_for('admin_upload_bp.upload_file'))

        except Exception as e:
            flash('File not saved', 'danger')
            print(e)
            return redirect(url_for('admin_upload_bp.upload_file'))
    return render_template('file_upload.html', form=form)
