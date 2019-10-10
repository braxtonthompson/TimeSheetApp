from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange

class TimesheetForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=9, max=9, message='Invalid C-Number.')])
    password = PasswordField('Password', validators=[DataRequired()])
    hours_worked = IntegerField('Hours Worked', validators=[DataRequired(), NumberRange(min=30, max=100, message='Please enter a valid number of hours.')])
    submit = SubmitField('Submit')
    remember = BooleanField('Remember Info')