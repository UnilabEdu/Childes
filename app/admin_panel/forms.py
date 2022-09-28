from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_wtf.file import FileField as FF, FileAllowed, FileRequired
from app.main.models import File
class UploadForm(FlaskForm):
    file = FF('ფაილი', validators=[FileRequired()],
                     render_kw={"class": "form-control form-control-lg","id":"formFileLg"})
    yt_link = StringField('Youtube ვიდეოს მისამართი',
                          render_kw={"placeholder": "Youtube ვიდეოს მისამართი"
                                     , "class": "form-control yt-link",},
                          validators=[DataRequired()],
                          )
    submit = SubmitField('ატვირთვა', render_kw={"class": "btn btn-outline-success"})
    
    def validate_yt_link(self, yt_link):
        if 'https://www.youtube.com/watch?v=' not in yt_link.data:
            raise ValidationError('Youtube ვიდეოს მისამართი არასწორია')
        return True
    
    def validate_file(self, file):
        print(File.already_exists(file.data.filename))
        if File.already_exists(file.data.filename):
            raise ValidationError('ეს ფაილი უკვე ატვირთულია')
        return True
    
    def validate_file_yt(self, yt_link):
        print(yt_link.data)
        if File.already_exists_yt(yt_link.data):
            raise ValidationError('ვიდეო უკვე არსებობს')
        return True
    # def validate_file(self, file):
    #     if file.data:
    #         filename = file.data.filename
    #         if filename[-4:] != '.cha': 
    #             raise ValidationError('ფაილი უნდა იყოს .cha გაფართოების')
    #     return True
    
