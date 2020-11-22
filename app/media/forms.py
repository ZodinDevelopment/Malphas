from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, FileField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User, Video, Photo



class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    comment  = TextAreaField("Comment...", validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField("Submit")


class UploadVideoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=1, max=140)], default="None.")
    upload = FileField("Video File", validators=[FileRequired()])
    submit = SubmitField("Upload")

    def validate_title(self, title):
        video = Video.query.filter_by(title=title.data).first()
        if video is not None:
            raise ValidationError("Title already taken.")


class UploadPhotoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    upload = FileField("Image File", validators=[FileRequired()])
    submit = SubmitField("Upload")

    def validate_title(self, title):
        photo = Photo.query.filter_by(title=title.data).first()
        if photo is not None:
            raise ValidationError("Title already taken.")
