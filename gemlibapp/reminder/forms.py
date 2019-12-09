from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea


class ReminderEmailForm(FlaskForm):
    message = TextAreaField('Content for the reminder Email',
                                 validators=[DataRequired()],
                            widget=TextArea())
    subject = StringField('Subject', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Store your template')

