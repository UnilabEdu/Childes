from functools import wraps
from flask_login import current_user
from flask import redirect, url_for
from flask_mail import Message
from app.extensions import mail
from flask import render_template


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin():
            return f(*args, **kwargs)
        return redirect(url_for('user_blueprint.login'))
    return decorated_function


def password_reset(body,email,token,user_email):
    msg = Message(subject="პაროლის აღდგენა", recipients=email, sender="minuwu@mailo.icu", body=body)
    msg.html = render_template('mail_body.html', token=token,user_email=user_email)
    mail.send(msg)

    return msg

