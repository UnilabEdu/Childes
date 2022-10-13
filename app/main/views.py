

from flask import redirect, render_template, request, url_for, Blueprint,flash
from flask_login import login_required, login_user, logout_user, current_user
from app.extensions import login_manager, mail
from app.config import basedir, STATI_FOLDER, uploads_folder, main_statics_folder as statics_folder, main_template_folder as template_folder
from app.main.models import User, Role, UserRoles, AboutPage, File
from app.main.forms import LoginForm, ResetForm
from flask_mail import Message
import os
import jwt


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
    about = AboutPage.get_by_id(1)
    return render_template('index.html', about=about)
# @user_blueprint.route('/create-roles')
# def create_roles():
#     Role.create_roles()
#     return 'roles created'



@user_blueprint.route('/<string:child_name>')
@login_required
def child(child_name):
    #mat_folder = os.path.join(STATI_FOLDER, 'uploads', 'cha', 'MAT')
    #print(os.listdir(mat_folder))
    # get all object from Files model where 'MAT' is in file name
    files = File.query.filter(File.file_name.like(f'%{child_name}%')).all()
    if not files:
        flash('არ არსებობს ამ ბავშვის ფაილები')
        return redirect(url_for('user_blueprint.index'))
    print(files)
    return redirect(url_for('user_blueprint.child_files', file=files[0].file_name, child_name=child_name))


@user_blueprint.route('/<string:child_name>/<string:file>')
@login_required
def child_files(child_name, file):
    child_files = File.query.filter(File.file_name.like(f'%{child_name}%')).all()
    child_files_with_file_name = File.query.filter(File.file_name.like(f'%{file}%')).first()
    print(child_files)
    if not child_files or not child_files_with_file_name:
        flash('არასწორი მოთხოვნა, სცადეთ თავიდან')
        return redirect(url_for('user_blueprint.index'))
    
    #stripped_filename = file.split('.')[0]
    print(child_files_with_file_name.file_name.strip(child_name).strip('.cha'))
    current_url = f"/{child_name}/{child_files_with_file_name.file_name.strip(child_name).strip('.cha')}"

    # find file with file name in static>uploads>cha>child_name
    cha_file = os.path.join(uploads_folder, 'cha', child_name.upper())
    
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
                           child_files=child_files)






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
    
    cha_file_in_mat_folder = os.path.join(uploads_folder, 'cha', f'{child_file_name}')

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
        print('validated')
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            print('user')
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('user_blueprint.index'))
        else:
            print('error')
            flash('არასწორი მომხმარებელი ან პაროლი')
            return redirect(url_for('user_blueprint.login'))
    return render_template('login.html', form=form)


@user_blueprint.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('user_blueprint.index'))
    form = ResetForm()
    if form.validate_on_submit():
        print('validated')
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print('user',user)
            #token = user.get_reset_token()
            print(type(user.email))
            msg = Message()
            msg.subject = 'პაროლის აღდგენა'
            msg.recipients = [user.email]
            msg.sender = 'minuwu@mailo.icu'
            msg.body = f'გამარჯობა {user.first_name}!'
            mail.send(msg)

            
        flash('თქვენი პაროლის შეცვლის ბმული გაიგზავნა თქვენს ელ.ფოსტაზე')
        return redirect(url_for('user_blueprint.login'))
    print(form.errors)
    return render_template('reset.html', form=form)

@user_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reseting_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return 'reset password'

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

