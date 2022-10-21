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
        print('not admin')
        return redirect(url_for('user_blueprint.login'))
    return decorated_function

def password_reset(body,email,token,user_email):
    msg = Message()
    msg.html = render_template('reset_password.html',token=token,user_email=user_email)
    msg.subject = 'პაროლის აღდგენა'
    msg.recipients = email
    msg.sender = 'minuwu@mailo.icu'
    msg.body = body
    mail.send(msg)
    print(msg)


    return msg

