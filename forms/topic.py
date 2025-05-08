from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, SubmitField, EmailField, BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class TopicReplyForm(FlaskForm):
    content = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Ответить')


class TopicCreateForm(FlaskForm):
    title = StringField('', validators=[DataRequired()])
    content = TextAreaField('', validators=[DataRequired()])
    sumbit = SubmitField('Создать')
