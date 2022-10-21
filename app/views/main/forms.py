from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, EmailField


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(message="ეს ველი სავალდებულოა"), Email()], render_kw={"placeholder": "example@email.ge"})
    password = PasswordField('Password', validators=[DataRequired(message='ეს ველი სავალდებულოა'), Length(min=6, max=25)], render_kw={"placeholder": "********"})
    remember = BooleanField('Remember Me', render_kw={"id": "remember-user"})
    submit = SubmitField('Login')
    
    
class ResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(message="ეს ველი სავალდებულოა"), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('Password',validators=[DataRequired(message='ეს ველი სავალდებულოა'),Length(min=6, max=25)], render_kw={"placeholder": "********"})
    submit = SubmitField('Change Password')
