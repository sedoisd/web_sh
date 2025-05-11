from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, SubmitField, EmailField, BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

class ObjectContent(FlaskForm):
    object_name = StringField('', validators=[DataRequired()])
    content = TextAreaField('')
    submit = SubmitField('Создать')