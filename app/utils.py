from functools import wraps
from flask_login import current_user
from flask import redirect, url_for


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin():
            return f(*args, **kwargs)
        print('not admin')
        return redirect(url_for('user_blueprint.login'))
    return decorated_function