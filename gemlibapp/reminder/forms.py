from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class ReminderEmailForm(FlaskForm):
    message = TextAreaField('Content for the reminder Email',
                                 validators=[DataRequired()],
                            widget=TextArea())
    submit = SubmitField('Store your template')

