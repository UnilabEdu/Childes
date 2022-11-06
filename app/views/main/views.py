from flask import redirect, render_template, url_for, Blueprint,flash
from flask_login import login_required
from app.config import UPLOADS_FOLDER, TEMPLATE_FOLDER
from app.views.main.models import AboutPage, File
import os

# Create blueprint
main_blueprint = Blueprint('main_blueprint', __name__, template_folder=TEMPLATE_FOLDER, url_prefix='/')


@login_required
@main_blueprint.route('/')
def index():
    about = AboutPage.get_by_id(1)
    return render_template('main/index.html', about=about)


@main_blueprint.route('/child/<string:child_name>')
@login_required
def child(child_name):
    # get all object from Files model where 'MAT' is in file name
    files = File.query.filter(File.file_name.like(f'%{child_name}%')).all()
    if not files:
        flash('არ არსებობს ამ ბავშვის ფაილები')
        return redirect(url_for('main_blueprint.index'))
    return redirect(url_for('main_blueprint.child_files', file=files[0].file_name, child_name=child_name))


@main_blueprint.route('/child/<string:child_name>/<string:file>')
@login_required
def child_files(child_name, file):
    child_all_files = File.query.filter(File.file_name.like(f'%{child_name}%')).all()
    cha_filename = File.query.filter(File.file_name.like(f'%{file}%')).first()
    next_files = File.query.filter(File.file_name.like(f'%{child_name}%')).offset(cha_filename.id).limit(5).all()

    if not child_all_files or not cha_filename:
        flash('არასწორი მოთხოვნა, სცადეთ თავიდან')
        return redirect(url_for('main_blueprint.index'))

    cha_file_dir = os.path.join(UPLOADS_FOLDER, 'cha', child_name.upper())
    with open(os.path.join(cha_file_dir, file), 'r') as f:
        lines = f.readlines()

        file_head_data ={'head': [], 'ID': []}
        file_main_data = {'main': []}
        date = ''
        for line in lines:
            parsed_line = line.strip('@').strip('\n').split('\t')
            if 'ID' in parsed_line[0]:
                file_head_data['ID'].append(parsed_line[1].split('|'))
            if 'Date' in parsed_line[0]:
                date = parsed_line[1].split('|')[0]

            if '*' not in parsed_line[0] and '' != parsed_line[0] and '%' not in parsed_line[0] and 'End' != parsed_line[0]:
                file_head_data['head'].append(parsed_line)
            else:
                parsed_line = line.strip('*').strip('%').strip('@').strip('\n').split('\t')
                if '' == parsed_line[0] and len(file_main_data['main']) > 0:
                    file_main_data['main'][-1][1] += parsed_line[1]
                if parsed_line[0] != '':
                    file_main_data['main'].append(line.strip('*').strip('%').strip('@').strip('\n').split('\t'))

    return render_template('main/chafile_view.html',
                           child_name=child_name,
                           one_file=cha_filename,
                           file_head_data=file_head_data,
                           file_main_data=file_main_data,
                           date=date,
                           child_files=child_all_files,
                           first_five_file=next_files)


@main_blueprint.route('/cha/<string:file_name>')
@login_required
def file(file_name):

    file_n = file_name
    file = File.query.filter_by(file_name=file_n).first()
    if not file:
        flash('არ არსებობს ეს ფაილი')
        return redirect(url_for('main_blueprint.index'))

    # stripping file name for having only child name
    ten_number = [i for i in range(0, 10)]
    for num in ten_number:
        file_name = file_name.replace(str(num), '')
    child_file_name = file_name.replace('.cha', '')

    cha_file_in_mat_folder = os.path.join(UPLOADS_FOLDER, 'cha', f'{child_file_name}')

    file = os.path.join(cha_file_in_mat_folder, file_n)

    # read with line by line
    file_data = ''
    if not os.path.exists(file):
        flash('მოხდა სეცდომა ფაილის გახსნასთან დაკავშირებით!')
        return redirect(url_for('main_blueprint.index'))
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            file_data += line + '<br>'

    return file_data


