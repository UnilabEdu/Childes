from flask import redirect, render_template, url_for, Blueprint, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from app.views.auth.forms import LoginForm, ResetForm,ResetPasswordForm
from app.extensions import login_manager, db
from app.views.auth.models import User
from app.utils import password_reset
from app.config import TEMPLATE_FOLDER

user_blueprint = Blueprint('user_blueprint', __name__, template_folder=TEMPLATE_FOLDER, url_prefix='/')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@user_blueprint.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('main_blueprint.index'))
        else:
            flash('არასწორი ელ-ფოსტა ან პაროლი')
            return redirect(url_for('user_blueprint.login'))
    return render_template('auth/login.html', form=form)


@user_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main_blueprint.index'))

    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            password_reset(body='body',email=[user.email],token=token,user_email=user.email)

        else:
            flash('ელ-ფოსტა არასწორია, გთხოვთ მიუთითოთ სწორი მისამართი.')
            return redirect(url_for('user_blueprint.reset_password'))

        flash('თქვენი პაროლის შეცვლის ბმული გაიგზავნა თქვენს ელ-ფოსტაზე.')
        return redirect(url_for('user_blueprint.login'))

    return render_template('auth/forgot_password.html', form=form)


@user_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def resetting_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ResetPasswordForm(request.form)
    user = User.verify_reset_token(token)

    if not user:
        flash('პაროლის აღდგენისთვის განკუთვნილი დრო გავიდა, სცადეთ ხელახლა.')
        return redirect(url_for('main_blueprint.index'))

    if request.method == 'POST' and form.validate_on_submit():
        user.password = form.new_password.data
        db.session.commit()
        flash('თქვენი პაროლი წარმატებთ შეიცვალა.')
        return redirect(url_for('main_blueprint.index'))

    return render_template('auth/reset_password.html',form=form)


# Logout route
@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_blueprint.login'))
