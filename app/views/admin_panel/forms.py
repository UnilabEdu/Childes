from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField as FF, FileAllowed, FileRequired
from app.views.main.models import File


class UploadForm(FlaskForm):
    # ფაილი უნდა იყოს .cha გაფართოების'
    file = FF('ფაილი', validators=[FileRequired(), FileAllowed(['cha'], 'ფაილი უნდა იყოს .cha გაფართოების')],
              render_kw={"class": "form-control form-control-lg", "id": "formFileLg"})

    yt_link = StringField('Youtube ვიდეოს მისამართი',
                          render_kw={"placeholder": "Youtube ვიდეოს მისამართი", "class": "form-control yt-link", })

    submit = SubmitField('ატვირთვა', render_kw={"class": "btn btn-outline-success", 'style': 'display:flex'})


    def validate_yt_link(self, embed_yt_link):
        if embed_yt_link.data and 'https://www.youtube.com/watch?v=' not in embed_yt_link.data:
            raise ValidationError('Youtube ვიდეოს მისამართი არასწორია')
        return True

    def validate_file(self, file):
        if File.already_exists(file.data.filename):
            raise ValidationError('ეს ფაილი უკვე ატვირთულია')
        return True

    # cha files allowed
    def validate_file(self, file):
        if file.data:
            filename = file.data.filename
            if filename[-4:] != '.cha':
                raise ValidationError('ფაილი უნდა იყოს .cha გაფართოების')
        return True
