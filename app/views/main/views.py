from flask import redirect, render_template, request, url_for, Blueprint,flash
from flask_login import login_required, login_user, logout_user, current_user
from app.extensions import login_manager
from app.views.main.models import db
from app.config import UPLOADS_FOLDER, main_statics_folder as statics_folder, MAIN_TEMPLATE as template_folder
from app.views.main.models import User, AboutPage, File,Role
from app.views.main.forms import LoginForm, ResetForm,ResetPasswordForm
from app.utils import password_reset
from flask_mail import Message
import os

# Create blueprint



user_blueprint = Blueprint('user_blueprint',
                            __name__,
                            static_folder=statics_folder,
                            template_folder=template_folder,
                            url_prefix='/')



# register login manager with the application
@login_manager.user_loader
def load_user(user_id):
    # example 
    # This is User Model from your models file 
    # this function is called to load a user given an ID
    return User.query.get(user_id)



@login_required
@user_blueprint.route('/')
def index():
    # first_file_delete = File.query.order_by(File.id).first()
    # if first_file_delete:
    #     first_file_delete.delete()
    about = AboutPage.get_by_id(1)
    return render_template('index.html', about=about)


@user_blueprint.route('/create-roles')
def create_roles():
    Role.create_roles()
    return 'roles created'


@user_blueprint.route('/<string:child_name>')
@login_required
def child(child_name):
    # get all object from Files model where 'MAT' is in file name
    files = File.query.filter(File.file_name.like(f'%{child_name}%')).all()
    if not files:
        flash('არ არსებობს ამ ბავშვის ფაილები')
        return redirect(url_for('user_blueprint.index'))
    return redirect(url_for('user_blueprint.child_files', file=files[0].file_name, child_name=child_name))


@user_blueprint.route('/<string:child_name>/<string:file>')
@login_required
def child_files(child_name, file):
    child_files = File.query.filter(File.file_name.like(f'%{child_name}%')).all()
    child_files_with_file_name = File.query.filter(File.file_name.like(f'%{file}%')).first()
    first_five_file = child_files[:5]
    if not child_files or not child_files_with_file_name:
        flash('არასწორი მოთხოვნა, სცადეთ თავიდან')
        return redirect(url_for('user_blueprint.index'))

    #stripped_filename = file.split('.')[0]

    current_url = f"/{child_name}/{child_files_with_file_name.file_name.strip(child_name).strip('.cha')}"

    # find file with file name in static>uploads>cha>child_name
    cha_file = os.path.join(UPLOADS_FOLDER, 'cha', child_name.upper())

    with open(os.path.join(cha_file, file), 'r') as f:
        lines = f.readlines()

        file_head_data ={'head': [], 'ID': []}
        file_main_data = {'main': []}
        date = ''
        for line in lines:
            #print(line.strip('@').strip('\n').split('\t'))
            if 'ID' in line.strip('@').strip('\n').split('\t')[0]:
                file_head_data['ID'].append(line.strip('@').strip('\n').split('\t')[1].split('|'))
            if 'Date' in line.strip('@').strip('\n').split('\t')[0]:
                date = line.strip('@').strip('\n').split('\t')[1].split('|')[0]
            if '*' not in line.strip('@').strip('\n').split('\t')[0] \
                    and '' != line.strip('@').strip('\n').split('\t')[0] \
                    and '%' not in line.strip('@').strip('\n').split('\t')[0] \
                    and 'End' != line.strip('@').strip('\n').split('\t')[0]:

                file_head_data['head'].append(line.strip('@').strip('\n').split('\t'))

            else:
                if '' == line.strip('*').strip('%').strip('@').strip('\n').split('\t')[0] and len(file_main_data['main']) > 0:
                    # append line.strip('*').strip('%').strip('@').strip('\n').split('\t') to last element in file_main_data['main']
                    # print(file_main_data['main'][-1][1],line.strip('*').strip('%').strip('@').strip('\n').split('\t')[1])
                    file_main_data['main'][-1][1] += line.strip('*').strip('%').strip('@').strip('\n').split('\t')[1]
                if line.strip('*').strip('%').strip('@').strip('\n').split('\t')[0] != '':
                    file_main_data['main'].append(line.strip('*').strip('%').strip('@').strip('\n').split('\t'))


    # print(file_head_data['ID'])    

    return render_template('logged-main.html',
                           files=child_files,
                           file=file,
                           child_name=child_name,
                           one_file=child_files_with_file_name,
                           file_head_data=file_head_data,
                           file_main_data=file_main_data,
                           current_url=current_url,
                           date=date,
                           child_files=child_files,
                           first_five_file=first_five_file)






@user_blueprint.route('/about')
def about():
    about = AboutPage.get_by_id(1)
    return render_template('index.html', about=about)

@user_blueprint.route('/cha/<string:file_name>')
@login_required
def file(file_name):

    file_n = file_name
    file = File.query.filter_by(file_name=file_n).first()
    if not file:
        flash('არ არსებობს ეს ფაილი')
        return redirect(url_for('user_blueprint.index'))

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
        return redirect(url_for('user_blueprint.index'))
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            file_data += line + '<br>'

    return file_data


@user_blueprint.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_blueprint.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('user_blueprint.index'))
        else:

            flash('არასწორი მომხმარებელი ან პაროლი')
            return redirect(url_for('user_blueprint.login'))
    return render_template('login.html', form=form)


@user_blueprint.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('user_blueprint.index'))
    form = ResetForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            password_reset(body='body',email=[user.email],token=token,user_email=user.email)

        else:
            flash('მეილი არ არსებობს,გთხოვთ შეიყვანოთ სწორი მეილი')
            return redirect(url_for('user_blueprint.reset_password'))

        flash('თქვენი პაროლის შეცვლის ბმული გაიგზავნა თქვენს ელ.ფოსტაზე')
        return redirect(url_for('user_blueprint.login'))

    return render_template('reset.html', form=form)

@user_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reseting_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm(request.form)
    user = User.verify_reset_token(token)

    if not user:
        flash('პაროლის აღდგენისთვის განკუთვნილი დრო გავიდა, სცადეთ ხელახლა.')
        return redirect(url_for('user_blueprint.index'))

    if request.method == 'POST' and form.validate_on_submit():
        user.password = form.new_password.data
        db.session.commit()
        flash('თქვენი პაროლი წარმატებთ შეიცვალა.')
        print(token)
        return redirect(url_for('user_blueprint.index'))

    return render_template('pasw_reset.html',form=form)

# app errorhandlers
@user_blueprint.app_errorhandler(404)
def page_not_found(e):
    flash('ეს გვერდი არარსებობს!')
    return redirect(url_for('user_blueprint.index'))

@user_blueprint.app_errorhandler(500)
def internal_server_error(e):
    flash('სერვერის შეცდომა!')
    return redirect(url_for('user_blueprint.index'))


# Logout route
@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_blueprint.login'))

