from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
import email_validator

from model import User
# from flask_login import current_user
# from flask_wtf.file import FileField, FileAllowed
# from wtforms.fields.html5 import DateField



class RegistrationForm(FlaskForm):
  '''Registration form'''
  fname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=20)])
  lname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[InputRequired(), Email()])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
  password2 = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
  submit = SubmitField('Submit')

class SignInForm(FlaskForm):
  '''sign in form'''

  email = StringField('Email', validators=[InputRequired(), Email()])
  password = PasswordField('Password', validators=[InputRequired()])
  submit = SubmitField('Sign In')
  
  
class CreateContactForm(FlaskForm):
  '''form for creating new contacts'''

  
class UpdateContactForm(FlaskForm):
  '''form to update existing contacts'''
  
  
