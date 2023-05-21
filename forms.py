from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import email_validator

from model import User
# from flask_login import current_user
# from flask_wtf.file import FileField, FileAllowed
# from wtforms.fields.html5 import DateField



class RegistrationForm(FlaskForm):
  '''Registration form'''
  fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
  lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
  password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Submit')